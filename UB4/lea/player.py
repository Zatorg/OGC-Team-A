import random
import constants as c


class Player:
    def __init__(self):
        self.actions = {0: c.UP, 1: c.DOWN, 2: c.LEFT, 3: c.RIGHT}

    def move(self):
        r = random.randint(0,3)
        return self.actions[r]