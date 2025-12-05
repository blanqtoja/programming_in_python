import csv
import logging
import json
from random import uniform

from src.sheep import Sheep
from src.wolf import Wolf


class Simulation:
    '''
    the maximum number of rounds: 50;
    the number of sheep: 15;
    the absolute value of the limit imposed on each coordinate of the initial positions of sheep: 
    10.0 (which implies that the respective range is [-10.0; 10.0]);
    the distance of sheep movement: 0.5;
    the distance of wolf movement: 1.0.
    '''
    def __init__(self, 
                 sheeps_count: int = 15, 
                 initial_position_limit: int = 10, 
                 sheep_step: float = 0.5, 
                 wolf_step: float = 1.0):
        
        self.sheeps = []
        for i in range(sheeps_count):
            start_x = uniform(-initial_position_limit, initial_position_limit)
            start_y = uniform(-initial_position_limit, initial_position_limit)
            
            self.sheeps.append(Sheep(x=start_x, y=start_y, step=sheep_step))

            logging.debug(f"Sheep #{i} init pos: x={start_x:.3f}, y={start_y:.3f}")
            
        logging.info("Initial positions of all sheep were determined")
        self.wolf = Wolf(x=0, y=0, step=wolf_step)

    def distance_to_sheep(self, sheep: Sheep) -> float:
        dx = sheep.x - self.wolf.x
        dy = sheep.y - self.wolf.y

        return dx * dx + dy * dy

    def run(self, max_rounds: int = 50, wait: bool = False) -> None:
        log_rounds = []
        csv_logs = []

        for round_no in range(1, max_rounds + 1):

            logging.info(f"New round started: {round_no}")

            sheeps_alive = [(i, s)
                            for i, s in enumerate(self.sheeps) if s is not None]

            if not sheeps_alive:
                logging.info("Simulation terminated: All sheep eaten")
                print("All sheeps eaten")
                break

            for i, sheep in sheeps_alive:
                sheep.move()
                logging.debug(f"Sheep #{i} moved to: x={sheep.x:.3f}, y={sheep.y:.3f}")

            logging.info("All alive sheep moved")

            nearest_index, nearest_sheep = min(
                sheeps_alive, key = lambda t: self.distance_to_sheep(t[1])
            )

            dist = self.distance_to_sheep(nearest_sheep) ** 0.5
            logging.debug(f"Wolf determined closest sheep: #{nearest_index}, distance: {dist:.3f}")

            # move wolf
            is_eaten = self.wolf.move(nearest_sheep)
            logging.debug(f"Wolf moved to: x={self.wolf.x:.3f}, y={self.wolf.y:.3f}")
            logging.info("Wolf moved")

            if is_eaten:
                chase_msg = f"Wolf ate sheep #{nearest_index}"
                logging.info(f"Sheep #{nearest_index} was eaten")
                # sheep was eaten, set None
                self.sheeps[nearest_index] = None
            else:
                chase_msg = f"Wolf is chasing sheep #{nearest_index}"
                logging.info(f"Wolf is chasing sheep #{nearest_index}")

            alive_count = sum(1 for s in self.sheeps if s is not None)

            logging.info(f"Round {round_no} ending. Alive sheep count: {alive_count}")

            print(
                f"Round {round_no}\n"
                f"  Wolf position: x={self.wolf.x:.3f}, y={self.wolf.y:.3f}\n"
                f"  Alive sheep: {alive_count}\n"
                f"  {chase_msg}\n"
            )

            if wait:
                input("Press Enter to continue to the next round...")

            round_data = {
                "round_no": round_no,
                "wolf_pos": [self.wolf.x, self.wolf.y],
                "sheep_pos": [
                    [s.x, s.y] if s is not None else None
                    for s in self.sheeps
                ]
            }

            log_rounds.append(round_data)
            csv_logs.append({"round_no": round_no, "alive_count": alive_count})
            
            if round_no == max_rounds:
                logging.info("Simulation terminated: Max rounds reached") 

        with open("pos.json", "w") as f:
            json.dump(log_rounds, f, indent=4)

        logging.debug("Information saved to pos.json")

        with open("alive.csv", "w", newline="") as f:
            fieldnames = ['round_no', 'alive_count']
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(csv_logs)

        logging.debug("Information saved to alive.csv")
