import random

class Sheep:
    def __init__(self, initial_position_limit, step = 0.5):

        init_x = random.random(-initial_position_limit, initial_position_limit)
        init_y = random.random(-initial_position_limit, initial_position_limit)

        self.x = init_x
        self.y = init_y
        self.step = step
        self.active = True 
    
    
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

    def deactivate(self):
        self.active = False
