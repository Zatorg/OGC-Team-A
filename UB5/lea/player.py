import random
import constants as c


class Player:
    def __init__(self):
        self.actions = {0: c.UP, 1: c.LEFT, 2: c.DOWN, 3: c.RIGHT}

    def random_action(self):
        return random.randint(0,3)