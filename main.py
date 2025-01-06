from classes import *
from menu import *
from utils import DB

import pyxel 

class App:
    def __init__(self):
        self.menu = Menu()
        self.menuwin = MenuWin()

        self.grille = Grille(13,13)
        self.grille.position_init()

        self.player1 = Bomber(0,0,"player1",self.grille,1)
        self.player1.spawn()
        self.player2 = Bomber(12,12,"player2",self.grille,2)
        self.player2.spawn()

        pyxel.init(208, 208, title="Bomberman", fps=30, display_scale=3)
        pyxel.load("ressources.pyxres")
        pyxel.run(self.update, self.draw)

    def deplacement(self):
        for k in pyxel.__dict__.keys():
            if k.startswith('KEY_'):
                if pyxel.btn(getattr(pyxel, k)):
                   for elt in DB.KEYS:
                       if k in elt:
                        player = elt.index(k)
                        direction = DB.KEYS[elt]
                        if player == 0:
                            self.player1.goto_fluid(direction)
                        else:
                            self.player2.goto_fluid(direction)

    def bombarder(self):
        if pyxel.btnp(pyxel.KEY_E):
            self.player1.dropBomb()
        elif pyxel.btnp(pyxel.KEY_J):
            self.player2.dropBomb()

    def draw_grille(self):
        for i in range(self.grille.l):
            for j in range(self.grille.h):
                case = self.grille.get_case(i, j)

                if case.bomber != []:
                    for player in case.bomber:
                        if not(player.dead):
                            pyxel.rect(player.move_x, player.move_y, 16, 16, player.id)

                if case.bomb != None:
                    pyxel.rect(16*i, 16*j, 16,16 , 3)

                if case.terrain == PARAMS.PILLIER:
                    pyxel.blt(16*i, 16*j,0, 48, 48, 16, 16)
                elif case.terrain == PARAMS.BRIQUE:
                    pyxel.blt(16*i, 16*j, 0, 64, 48, 16, 16)

    def update(self):
        #Quit window
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        
        self.deplacement()
        self.bombarder()

        self.grille.manage_bombs()

    def draw(self):
        if self.menu.show:
            self.menu.update()
            self.menu.draw()
        elif self.menuwin.show:
            self.menuwin.draw()
        else:
            pyxel.cls(0)
            self.draw_grille()

App()