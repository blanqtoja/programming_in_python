
from src.sheep import Sheep
from src.wolf import Wolf


class Simulation:
    # the maximum number of rounds: 50;
    # the number of sheep: 15;
    # the absolute value of the limit imposed on each coordinate of the initial positions of sheep: 10.0 (which implies that the respective range is [-10.0; 10.0]);
    # the distance of sheep movement: 0.5;
    # the distance of wolf movement: 1.0.
    def __init__(self, max_rounds = 50, sheeps_count = 15, initial_position_limit = 10, sheep_step = 0.5, wolf_step = 1.0):
        sheeps = list(Sheep(initial_position_limit = initial_position_limit, step = sheep_step) for _ in range(max_rounds)) 
        wolf = Wolf(x=0, y=0, step = wolf_step)

        