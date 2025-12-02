from math import sqrt


class Wolf:
    def __init__(self, x=0, y=0, step=1.0):
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

    def move(self, sheep):

        dx = sheep.x - self.x
        dy = sheep.y - self.y

        length = sqrt(dx * dx + dy * dy)

        if length <= self.step:
            self.x = sheep.x
            self.y = sheep.x
            return False

        # normalize
        ux = dx / length
        uy = dy / length

        self.x += ux * self.step
        self.y += uy * self.step
        return True
