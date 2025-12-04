import random


class Sheep:
    def __init__(self, x, y, step=0.5):
        self._x = x
        self._y = y
        self._step = step

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def step(self):
        return self._step

    def move(self):

        directions = [
            (-self.step, 0),  # left
            (self.step, 0),   # right
            (0, -self.step),  # down
            (0, self.step),  # up
        ]

        dx, dy = random.choice(directions)

        self.x += dx
        self.y += dy
