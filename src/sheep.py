import random


class Sheep:
    def __init__(self, x, y, step=0.5):

        self._x = x
        self._y = y
        self._step = step

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def step(self):
        return self._step

    def move(self):
        dir = random.randint(0, 4)

        # left
        if dir == 0:
            self.x -= self.x

        # rigth
        if dir == 1:
            self.x += self.x

        # down
        if dir == 3:
            self.y -= self.y
        # up
        if dir == 4:
            self.y += self.y
