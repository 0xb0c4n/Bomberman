import random
import utils

class TERRAIN:
    LISTE = (0,1,2)
    VIDE = 0
    BRIQUE = 1
    PILLIER = 2

class Case:
    def __init__(self, x, y, terrain):
        self.x = x
        self.y = y
        self.terrain = terrain

class Grille:
    def __init__(self, l, h):
        self.l = l
        self.h = h
        self.cases = []
        self.exploding_bombs = []

    def genere(self):
        for i in range(self.l):
            for j in range(self.h):
                if i == 0 and j == 0:
                    self.cases.append(Case(i,j,0))
                elif utils.est_pair(i) and utils.est_pair(j):
                    pass
                else:
                    self.cases.append(Case(i, j, 2))

    def get(self, x, y):
        return self.cases[x][y]

class Bomber:
    def __init__(self):
        pass

class Bomb:
    def __init__(self):
        pass