from utils import *
import pyxel

class PARAMS:
    """Objet pour stocker des paramètres de bases"""
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
    """Objet du personnage jouable"""
    def __init__(self, x:int, y:int, nom:str, grille: object, id: int, direction: str):
        self.x = x
        self.y = y
        self.move_x = x
        self.move_y = y
        self.nom = nom
        self.dead = False
        self.grille = grille
        self.id = id
        self.direction = direction
        self.launched = False
    
    def spawn(self):
        """Méthode ajoutant un bomberman aux coordonnées renseignés dans le constructeur"""
        case = self.grille.get_case(self.x, self.y)
        case.bomber.append(self)

    def goto(self, direction: str):
        """Méthode de déplacement du bomberman en place
        Prend en paramètre une direction de type str"""
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
        """Méthode permettant de lâcher des bombes sur la case où se situe le bomberman"""
        self.grille.cases[self.x][self.y].bomb = Bomb(self.x, self.y, self.id)
        self.launched = True

class Case:
    """Objet désignant la case"""
    def __init__(self, x:int, y:int, terrain:int):
        self.x = x
        self.y = y
        self.terrain = terrain
        self.bomber = []
        self.bomb = None
        self.en_explosion = False

class Grille:
    """Objet désignant la grille"""
    def __init__(self, l:int, h:int):
        self.l = l
        self.h = h
        self.cases = []
        self.exploding_bombs = []
        self.animations = []
        self.explosions_anim = []
        self.changing_bricks = []
        self.counter = [None] * 2
        self.end = False

    def position_init(self):
        """Initialise avec des probas prédéfinies (float) une grille remplie avec des paramètres précis """
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

    def get_case(self, x:int, y:int):
        """Renvoie un objet Case
        Prend en paramètre ses coordonnées x et y (integer)"""
        if not(self.l <= x or self.h <= y) and not(x < 0 or y < 0):
            return self.cases[x][y]
    
    def manage_bombs(self):
        """Méthode permettant de gérer les bombes dans la grille"""
        def decrementer():
            """Sous-méthode permettant de décrémenter le compte à rebours et de commencer l'explosion à la fin"""
            for i in range(self.l):
                for j in range(self.h):
                    case = self.get_case(i, j)

                    if case.bomb != None:
                        if pyxel.frame_count % 24 == 0:
                            case.bomb.compte_a_rebours(1)
                        if case.bomb.rebours == 0:
                            self.exploding_bombs.append(case.bomb)
                            self.explosions_anim.append(case.bomb)
                            self.counter.append(None)
                            case.bomb = None
        
        def exploser():
            """Sous-méthode permettant de calculer l'impact de la bombe en fonction de sa portee"""
            def handle_direction(dx:int, dy:int):
                """Prend deux entiers relatifs dx et dy compris entre -1 et 1 inclus pour mettre
                les cases en explosion."""
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
                handle_direction(0, 0) 

        def change_terrain():
            """Change le type de terrain après le passage de la bombe (sauf pour les briques)"""
            for i in range(self.l):
                for j in range(self.h):
                    case = self.get_case(i,j)

                    if case.en_explosion and case.terrain != PARAMS.BRIQUE:
                        case.en_explosion = False
                        self.exploding_bombs = self.exploding_bombs[:-1]
                        if case.bomber != []:
                            for player in case.bomber:
                                player.dead = True
                                self.animations.clear()
                        elif case.bomb != None:
                            self.exploding_bombs.append(case.bomb)

        decrementer()
        exploser()
        change_terrain()

class Bomb:
    """Objet de la Bombe"""
    def __init__(self, x:int, y:int, id:int):
        self.x = x
        self.y = y
        self.portee = 2
        self.rebours = 5
        self.l_id = id
    
    def compte_a_rebours(self, n:int):
        """Méthode enlevant n au compte à rebours
        Prend en paramètre un entier n"""
        self.rebours -= n
        