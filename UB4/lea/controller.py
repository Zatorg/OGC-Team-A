import logic
from puzzle import GameGrid

class Controller:
    def __init__(self):
        #Todo: add size parameter
        self.gui = GameGrid()
        self.logic = logic.GameLogic()


