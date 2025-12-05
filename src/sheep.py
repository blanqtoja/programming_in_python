import random


class Sheep:
    def __init__(self, x: float, y: float, step: float = 0.5):
        self._x = x
        self._y = y
        self._step = step

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        self._x = value

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        self._y = value

    @property
    def step(self) -> float:
        return self._step

    def move(self) -> None:

        directions = [
            (-self.step, 0),  # left
            (self.step, 0),   # right
            (0, -self.step),  # down
            (0, self.step),  # up
        ]

        dx, dy = random.choice(directions)

        self.x += dx
        self.y += dy
