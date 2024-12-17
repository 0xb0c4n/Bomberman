from utils import *

class PARAMS:
    LISTE = (0,1,2)
    VIDE = 0
    BRIQUE = 1
    PILLIER = 2

    PROBAS = {
        VIDE: 0.20,
        BRIQUE: 0.80
    }

    COEFS_GO = {
        "up": (0,-1),
        "down": (0,1),
        "left": (-1,0),
        "right": (1,0)
    }

class Bomber:
    def __init__(self, x, y, nom, grille, id):
        self.x = x
        self.y = y
        self.nom = nom
        self.dead = False
        self.grille = grille
        self.id = id
    
    def spawn(self):
        case = self.grille.get_case(self.x, self.y)
        case.bomber.append(self)
    
    def goto(self, direction):
        move_cpl = PARAMS.COEFS_GO[direction]
        new_x = self.x+move_cpl[0]
        new_y = self.y+move_cpl[1]

        if new_x < 0 or new_y < 0 or new_x >= self.grille.l or new_y >= self.grille.h:
            pass
        elif self.grille.cases[new_x][new_y].terrain != 0:
            pass
        else:
            next_case = self.grille.cases[new_x][new_y]
            current_case = self.grille.cases[self.x][self.y]

            current_case.bomber.pop()
            next_case.bomber.append(self)
            
            self.x = new_x
            self.y = new_y

class Case:
    def __init__(self, x, y, terrain):
        self.x = x
        self.y = y
        self.terrain = terrain
        self.bomber = []
        self.bomb = None
        self.en_explosion = False

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
                    ligne.append(Case(i,j,PARAMS.VIDE))
                elif not(est_pair(i)) and not(est_pair(j)):
                    ligne.append(Case(i, j, PARAMS.PILLIER))
                elif (i in [0, 1, self.l - 2, self.l - 1]) and (j in [0, 1, self.h - 2, self.h - 1]):
                    ligne.append(Case(i,j,PARAMS.VIDE))
                else:
                    terrain = probas(PARAMS.PROBAS)
                    ligne.append(Case(i,j,terrain))

            self.cases.append(ligne)

    def get_case(self, x, y):
        return self.cases[x][y]
    
class Bomb:
    def __init__(self):
        pass
