import argparse
import configparser
import sys
import logging
from src.simulation import Simulation

def setup_logging(log_level: str) -> None:
    '''Sets up logging configuration.'''
    if not log_level:
        return
    
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {log_level}')
    
    # Handler reset for every run
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    logging.basicConfig(
        filename='chase.log',
        filemode='w',
        level=numeric_level,
        format='%(levelname)s:%(message)s'
    )


def load_config(config_file: str) -> dict:
    '''Loads configuration from a file INI'''
    config = configparser.ConfigParser()
    config.read(config_file)

    try:
        settings = {
            'init_pos_limit': float(config['Sheep']['InitPosLimit']),
            'sheep_move_dist': float(config['Sheep']['MoveDist']),
            'wolf_move_dist': float(config['Wolf']['MoveDist']),
        }

        logging.debug(f"Loaded config values: {settings}")

        if settings['wolf_move_dist'] <= 0 or settings['sheep_move_dist'] <= 0:
            raise ValueError("Movement distances must be positive numbers")

    except KeyError as e:
        raise ValueError(f"Missing missing key in config file: {e}")
    except ValueError as e:
        raise ValueError(f"Invalid value in config file: {e}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Wolf and Sheep Simulation")
    parser.add_argument('-c', '--config', 
                        help='Path to configuration file')
    parser.add_argument('-l', '--log', 
                        help='Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)')
    parser.add_argument('-r', '--rounds', 
                        type=int, default=50, 
                        help='Maximum number of rounds')
    parser.add_argument('-s', '--sheep', default=15,
                        type=int, help='Number of sheep')
    parser.add_argument('-w', '--wait', 
                        action='store_true', help='Wait for key press after each round')

    args = parser.parse_args()
    if args.log:
        try:
            setup_logging(args.log)
        except ValueError as e:
            print(f"Error setting up logging: {e}")
            sys.exit(1)
    
    if args.rounds <= 0:
        raise ValueError("The maximum number of rounds must be in integer greater than 0")
    if args.sheep <= 0:
        raise ValueError("The number of sheep must be in integer greater than 0")

    sim_params = {
        'initial_position_limit': 10.0,
        'sheep_step': 0.5,
        'wolf_step': 1.0,
    }

    if args.config:
        try:
            config_values = load_config(args.config)
            sim_params['initial_position_limit'] = config_values['init_pos_limit']
            sim_params['sheep_step'] = config_values['sheep_move_dist']
            sim_params['wolf_step'] = config_values['wolf_move_dist']
        except Exception as e:
            print(f"Configuration error: {e}")
            sys.exit(1)

    simulation = Simulation(
        sheeps_count=args.sheep,
        initial_position_limit=sim_params['initial_position_limit'],
        sheep_step=sim_params['sheep_step'],
        wolf_step=sim_params['wolf_step']
    )

    simulation.run(max_rounds=args.rounds, wait=args.wait)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        logging.critical(f"Unhandled exception: {e}", exc_info=True)