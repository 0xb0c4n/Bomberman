from classes import *

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


    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.cls(7)
        for i in range(self.grille.l):
            for j in range(self.grille.h):
                case = self.grille.get_case(i, j)
                if case.bomber != None:
                    pyxel.rect(40*i, 40*j, 40, 40, 1)
                elif case.terrain == TERRAIN.PILLIER:
                    pyxel.rect(40*i, 40*j, 40, 40, 0)
                elif case.terrain == TERRAIN.BRIQUE:
                    pyxel.rect(40*i, 40*j, 40, 40, 13)

                


App()