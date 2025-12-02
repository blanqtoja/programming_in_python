from math import sqrt


class Wolf:
    def __init__(self, x = 0, y = 0, step = 1.0):
        self.x = x
        self.y = y
        self.step = step
        self.active = True 

    def move(self, sheep):

        dx = sheep.x - self.x 
        dy = sheep.y - self.y 

        length = sqrt(dx * dx + dy * dy)

        if length <= self.step:
            sheep.deactivate()
            self.x = sheep.get_x()
            self.y = sheep.get_y()
            return
        
        # normalize 
        ux = dx / length
        uy = dy / length

        self.x += ux * self.step
        self.y += uy * self.step
