from classes import *
from utils import DB

import pyxel 

class App:
    def __init__(self):
        self.grille = Grille(13,13)
        self.grille.position_init()

        self.player1 = Bomber(0,0,"player1",self.grille,1)
        self.player1.spawn()
        self.player2 = Bomber(12,12,"player2",self.grille,2)
        self.player2.spawn()

        pyxel.init(520, 520, title="Bomberman")
        pyxel.run(self.update, self.draw)

    def deplacement(self):
        for k in pyxel.__dict__.keys():
            if k.startswith('KEY_'):
                if pyxel.btnp(getattr(pyxel, k)):
                   for elt in DB.KEYS:
                       if k in elt:
                        player = elt.index(k)
                        direction = DB.KEYS[elt]
                        if player == 0:
                            self.player1.goto(direction)
                        else:
                            self.player2.goto(direction)


    def update(self):
        #Quit window
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        
        self.deplacement()

    def draw(self):
        pyxel.cls(7)
        for i in range(self.grille.l):
            for j in range(self.grille.h):
                case = self.grille.get_case(i, j)
                if case.bomber != []:
                    for _ in case.bomber:
                        pyxel.rect(40*i, 40*j, 40, 40, _.id)
                elif case.terrain == PARAMS.PILLIER:
                    pyxel.rect(40*i, 40*j, 40, 40, 0)
                elif case.terrain == PARAMS.BRIQUE:
                    pyxel.rect(40*i, 40*j, 40, 40, 13)

                


App()