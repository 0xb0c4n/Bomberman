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
        self.move_x = x
        self.move_y = y
        self.nom = nom
        self.dead = False
        self.grille = grille
        self.id = id
    
    def spawn(self):
        case = self.grille.get_case(self.x, self.y)
        case.bomber.append(self)

    def goto_fluid(self, direction):
        move_cpl = PARAMS.COEFS_GO[direction]

        n_case_x = self.x+move_cpl[0]
        n_case_y = self.y+move_cpl[1]
        
        if self.grille.cases[n_case_x][n_case_y].terrain == 0:
            print(n_case_x)
            coef_add = 16/20
            self.move_x += coef_add * move_cpl[0]
            self.move_y += coef_add * move_cpl[1]

            if self.move_x % 16 == 0:
                next_case = self.grille.cases[n_case_x][n_case_y]
                current_case = self.grille.cases[self.x][self.y]

                current_case.bomber.pop()
                next_case.bomber.append(self)
                
                self.x += n_case_x
                self.y += n_case_y
    


    def goto(self, direction):
        move_cpl = PARAMS.COEFS_GO[direction]
        new_x = self.x+move_cpl[0]
        new_y = self.y+move_cpl[1]

        if not(new_x < 0 or new_y < 0 or new_x >= self.grille.l or new_y >= self.grille.h) and not(self.grille.cases[new_x][new_y].terrain != 0):
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
        self.animations = []

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
        if not(self.l <= x or self.h <= y) and not(x < 0 or y < 0):
            return self.cases[x][y]
    
    def manage_bombs(self):
        def decrementer():
            for i in range(self.l):
                for j in range(self.h):
                    case = self.get_case(i, j)

                    if case.bomb != None:
                        if pyxel.frame_count % 24 == 0:
                            case.bomb.compte_a_rebours(1)
                        if case.bomb.rebours == 0:
                            self.exploding_bombs.append(case.bomb)

                            case.bomb = None
        
        def exploser():
            def handle_direction(dx, dy):
                for step in range(1, portee + 1):
                    case = self.get_case(elt.x + step * dx, elt.y + step * dy)
                    if case is None:
                        break
                    if case.terrain == PARAMS.PILLIER:
                        break
                    case.en_explosion = True
                    if case.terrain == PARAMS.BRIQUE:
                        self.animations.append(case)
                        break

            for elt in self.exploding_bombs:
                portee = elt.portee
                handle_direction(-1, 0)  
                handle_direction(1, 0)  
                handle_direction(0, -1) 
                handle_direction(0, 1)   

        def change_terrain():
            for i in range(self.l):
                for j in range(self.h):
                    case = self.get_case(i,j)

                    if case.en_explosion and case.terrain != PARAMS.BRIQUE:
                        case.en_explosion = False
                        self.exploding_bombs = self.exploding_bombs[:-1]
                        if case.bomber != []:
                            for player in case.bomber:
                                player.dead = True
                        elif case.bomb != None:
                            self.exploding_bombs.append(case.bomb)

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
        