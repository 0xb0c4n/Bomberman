from utils import *

import random

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
    
    def __str__(self):
        return str(self.terrain)

class Grille:
    def __init__(self, l, h):
        self.l = l
        self.h = h
        self.cases = []
        self.exploding_bombs = []

    def position_init(self):
        for i in range(self.h):
            ligne = []
            for j in range(self.l):
                if (i == 0 or i == self.l-1) and (j == 0 or j == self.h-1):
                    ligne.append(Case(i,j,TERRAIN.VIDE))
                elif not(est_pair(i)) and not(est_pair(j)):
                    ligne.append(Case(i, j, TERRAIN.PILLIER))
                else:
                    ligne.append(Case(i,j,random.choice((TERRAIN.BRIQUE, TERRAIN.VIDE))))

            self.cases.append(ligne)

    def get_case(self, x, y):
        return self.cases[x][y]
    
class Bomb:
    def __init__(self):
        pass
