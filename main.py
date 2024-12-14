from classes import *

import pyxel 

class App:
    def __init__(self):
        self.grille = Grille(13,13)
        self.grille.position_init()

        pyxel.init(520, 520, title="Hello Pyxel")
        pyxel.run(self.update, self.draw)


    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.cls(7)
        for i in range(self.grille.l):
            for j in range(self.grille.h):
                case = self.grille.get_case(i, j)
                if case.bomber:
                    pyxel.rect(40*i, 40*j, 40, 40, 1)
                elif case.terrain == TERRAIN.PILLIER:
                    pyxel.rect(40*i, 40*j, 40, 40, 0)
                elif case.terrain == TERRAIN.BRIQUE:
                    pyxel.rect(40*i, 40*j, 40, 40, 13)

                


App()