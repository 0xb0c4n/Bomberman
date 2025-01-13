from classes import *
from menu import *
from utils import DB

import pyxel 

class App:
    def __init__(self):
        self.menu = Menu()

        self.grille = Grille(13,13)
        self.grille.position_init()

        self.player1 = Bomber(0,0,"player1",self.grille,1, "right")
        self.player1.spawn()
        self.player2 = Bomber(12,12,"player2",self.grille,2, "left")
        self.player2.spawn()

        self.anim_counter = 0

        pyxel.init(208, 208, title="Bomberman", fps=24, display_scale=3)
        pyxel.load("ressources.pyxres")
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
                            self.player1.direction = direction
                        else:
                            self.player2.goto(direction)
                            self.player2.direction = direction


    def bombarder(self):
        if pyxel.btnp(pyxel.KEY_E):
            self.player1.dropBomb()
        elif pyxel.btnp(pyxel.KEY_J):
            self.player2.dropBomb()

    def draw_grille(self):
        for i in range(self.grille.l):
            for j in range(self.grille.h):
                case = self.grille.get_case(i, j)
                if case.bomb != None:
                    pyxel.blt(16*i, 16*j, 0, 0, 48,16,16)
                if case.bomber != []:
                    for player in case.bomber:
                        if not(player.dead):
                            u, v = DB.SPRITES[player.direction]
                            pyxel.blt(16*i, 16*j, 0, u, v, 16, 16)
                        else:
                            pyxel.cls(0)
                            self.grille.end = True
                            alive_player = self.player1.nom if self.player2.dead else self.player2.nom
                            pyxel.text(80,50,alive_player + " wins !",7)
                            pyxel.text(60,70,"Press [ENTER] to restart",7)
                            if pyxel.btnp(pyxel.KEY_RETURN):
                                self.menu.show = True
                                self.player1.dead = False
                                self.player2.dead = False
                                self.grille.end = False
                                self.grille.position_init()



                if case.terrain == PARAMS.PILLIER and not self.grille.end:
                    pyxel.blt(16*i, 16*j, 0, 48,48,  16, 16)
                elif case.terrain == PARAMS.BRIQUE and not self.grille.end:
                    pyxel.blt(16*i, 16*j, 0, 64, 48, 16, 16)
                


    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        
        self.deplacement()
        self.bombarder()

        self.grille.manage_bombs()

    def calcul_portee(self, core: tuple, portee):
        x, y = core

        def handle_direction(dx, dy):
            for step in range(1, portee + 1):
                case = self.grille.get_case(x + step * dx, y + step * dy)
                if case is None: 
                    break
                if case.terrain == PARAMS.PILLIER:
                    break
                case.en_explosion = True
                if case.terrain == PARAMS.BRIQUE:
                    break

        handle_direction(-1, 0)  
        handle_direction(1, 0)  
        handle_direction(0, -1) 
        handle_direction(0, 1)  
        handle_direction(0, 0)


    def draw(self):
        if self.menu.show:
            self.menu.update()
            self.menu.draw()
        else:
            if self.menu.mode == "quit":
                pyxel.quit()
            else:
                pyxel.cls(0)

                for bomb in self.grille.explosions_anim:
                    duree = 12
                    c_x, c_y = DB.SPRITES["explosions"][(pyxel.frame_count // duree) % 4]
                    x, y = bomb.x - 2, bomb.y - 2
                    pyxel.blt(x*16, y*16, 0, c_x, c_y, 80,80)
                    


                self.draw_grille()

App()