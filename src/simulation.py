
import csv
import json
from random import randrange

from src.sheep import Sheep
from src.wolf import Wolf


class Simulation:
    # the maximum number of rounds: 50;
    # the number of sheep: 15;
    # the absolute value of the limit imposed on each coordinate of the initial positions of sheep: 10.0 (which implies that the respective range is [-10.0; 10.0]);
    # the distance of sheep movement: 0.5;
    # the distance of wolf movement: 1.0.
    def __init__(self, sheeps_count=15, initial_position_limit=10, sheep_step=0.5, wolf_step=1.0):

        self.sheeps = list(
            Sheep(
                x=randrange(-initial_position_limit,
                            initial_position_limit),
                y=randrange(-initial_position_limit,
                            initial_position_limit),
                step=sheep_step
            ) for _ in range(sheeps_count))
        self.wolf = Wolf(x=0, y=0, step=wolf_step)

    def distance_to_sheep(self, sheep):
        dx = sheep.x - self.wolf.x
        dy = sheep.y - self.wolf.y

        return dx * dx + dy * dy

    def run(self, max_rounds=50):
        log_rounds = []
        csv_logs = []

        for round_no in range(max_rounds):

            sheeps_alive = [(i, s)
                            for i, s in enumerate(self.sheeps) if s is not None]

            if not sheeps_alive:
                break

            for i, sheep in sheeps_alive:
                sheep.move()

            nearest_index, nearest_sheep = min(
                sheeps_alive, key=lambda t: self.distance_to_sheep(t[1])
            )

            # move wolf
            is_eaten = self.wolf.move(nearest_sheep)

            if is_eaten:
                chase_msg = f"Wolf ate sheep #{nearest_index}"

                # sheep was eaten, set None
                self.sheeps[nearest_index] = None
            else:
                chase_msg = f"Wolf is chasing sheep #{nearest_index}"

            alive_count = sum(1 for s in self.sheeps if s is not None)

            print(
                f"Round {round_no}\n"
                f"  Wolf position: x={self.wolf.x:.3f}, y={self.wolf.y:.3f}\n"
                f"  Alive sheep: {alive_count}\n"
                f"  {chase_msg}\n"
            )

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

        with open("pos.json", "w") as f:
            json.dump(log_rounds, f, indent=4)

        with open("alive.csv", "w", newline="") as f:
            fieldnames = ['round_no', 'alive_count']
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(csv_logs)
