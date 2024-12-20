from utils import *
import pyxel

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

    def dropBomb(self):
        self.grille.cases[self.x][self.y].bomb = Bomb(self.x, self.y)

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
        if not(self.l <= x or self.h <= y) and not(self.l < 0 or self.h < 0):
            return self.cases[x][y]
    
    def manage_bombs(self):
        def decrementer():
            for i in range(self.l):
                for j in range(self.h):
                    case = self.get_case(i, j)

                    if case.bomb != None:
                        if pyxel.frame_count % 30 == 0:
                            case.bomb.compte_a_rebours(1)
                        if case.bomb.rebours == 0:
                            self.exploding_bombs.append(case.bomb)
                            case.bomb = None
        
        def exploser():
            for elt in self.exploding_bombs:
                portee = elt.portee
                for i_x in range(-portee,1):
                    case_x = self.get_case(elt.x-i_x, elt.y)
                    if case_x != None and case_x.terrain != PARAMS.PILLIER:
                        case_x.en_explosion = True
                    elif case_x != None and case_x.terrain == PARAMS.BRIQUE:
                        case_x.en_explosion = True
                        i_x = portee 
                    else:
                        break
                for j_x in range(1, portee+1):
                    case_x = self.get_case(elt.x+i_x, elt.y)
                    if case_x != None and case_x.terrain != PARAMS.PILLIER:
                        case_x.en_explosion = True
                    elif case_x != None and case_x.terrain == PARAMS.BRIQUE:
                        case_x.en_explosion = True
                        j_x = portee 
                    else:
                        break
                for i_y in range(-portee,1):
                    case_y = self.get_case(elt.x, elt.y-i_y)
                    if case_y != None and case_y.terrain != PARAMS.PILLIER:
                        case_y.en_explosion = True
                    elif case_y != None and case_x.terrain == PARAMS.BRIQUE:
                        case_x.en_explosion = True
                        i_y = portee 
                    else:
                        break
                for j_y in range(1, portee+1):
                    case_y = self.get_case(elt.x, elt.y+j_y)
                    if case_y != None and case_y.terrain != PARAMS.PILLIER:
                        case_y.en_explosion = True
                    elif case_y != None and case_x.terrain == PARAMS.BRIQUE:
                        case_x.en_explosion = True
                        j_y = portee 
                    else:
                        break

        def change_terrain():
            for i in range(self.l):
                for j in range(self.h):
                    case = self.get_case(i,j)

                    if case.en_explosion:
                        case.en_explosion = False
                        self.exploding_bombs = self.exploding_bombs[:-1]
                        if case.terrain == PARAMS.BRIQUE:
                            case.terrain = PARAMS.VIDE
                        elif case.bomber != []:
                            for player in case.bomber:
                                player.dead = True

        decrementer()
        exploser()
        change_terrain()

class Bomb:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.portee = 2
        self.rebours = 5
    
    def compte_a_rebours(self, n):
        self.rebours -= n
        