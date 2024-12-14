from utils import *

class TERRAIN:
    LISTE = (0,1,2)
    VIDE = 0
    BRIQUE = 1
    PILLIER = 2

    PROBAS = {
        VIDE: 0.14,
        BRIQUE: 0.86
    }

class Bomber:
    def __init__(self, x, y, nom, grille):
        self.x = x
        self.y = y
        self.nom = nom
        self.dead = False
        self.grille = grille

class Case:
    def __init__(self, x, y, terrain, bomber=False):
        self.x = x
        self.y = y
        self.terrain = terrain
        self.bomber = bomber

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
                if (i == 0 and j == 0) or (i == self.l - 1 and j == self.h - 1):
                    ligne.append(Case(i,j,TERRAIN.VIDE, True))
                elif not(est_pair(i)) and not(est_pair(j)):
                    ligne.append(Case(i, j, TERRAIN.PILLIER))
                elif (i in [0, 1, self.l - 2, self.l - 1]) and (j in [0, 1, self.h - 2, self.h - 1]):
                    ligne.append(Case(i,j,TERRAIN.VIDE))
                else:
                    terrain = probas(TERRAIN.PROBAS)
                    ligne.append(Case(i,j,terrain))

            self.cases.append(ligne)

    def get_case(self, x, y):
        return self.cases[x][y]
    
class Bomb:
    def __init__(self):
        pass
