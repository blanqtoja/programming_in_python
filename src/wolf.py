from math import sqrt


class Wolf:
    def __init__(self, x: float = 0, y: float = 0, step: float = 1.0):
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

    def move(self, sheep: Sheep) -> bool:

        dx = sheep.x - self.x
        dy = sheep.y - self.y

        length = sqrt(dx * dx + dy * dy)
        if length <= self.step:
            self.x = sheep.x
            self.y = sheep.y
            return True

        # normalize
        ux = dx / length
        uy = dy / length

        self.x += ux * self.step
        self.y += uy * self.step
        return False
