import random
import time


class Player:
    def __init__(self, ID, name, board=None):
        self.Id = ID
        if board is not None:
            self.Board = board
            self.settings = {'name': name, 'cords':self.generStartPos()}

    def generStartPos(self):
        cords = [random.randint(0, 100), random.randint(0, 100)]
        while cords in (tuple(item) for item in self.Board):
            cords = [random.randint(0, 100), random.randint(0, 100)]
        return cords