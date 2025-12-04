from math import sqrt


class Wolf:
    def __init__(self, x=0, y=0, step=1.0):
        self._x = x
        self._y = y
        self._step = step

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    # kurde tyyy ja nie wiedziałem że ty znasz takie chwyty
    # na plus w sensie, jak coś to nie mówię tego uszczypliwie 
    # 👌👌
    @property   
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def step(self):
        return self._step

    def move(self, sheep):

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
