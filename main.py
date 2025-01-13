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

    def draw(self):
        if self.menu.show:
            self.menu.update()
            self.menu.draw()
        else:
            if self.menu.mode == "quit":
                pyxel.quit()
            else:
                pyxel.cls(0)
                self.draw_grille()
                
                duree_animation = 92
            
                for elt in self.grille.animations:
                    frame_progress = pyxel.frame_count % duree_animation
                    if frame_progress < duree_animation:
                        frame_offset = (frame_progress // (duree_animation // 6)) * 16
                        pyxel.blt(
                            16 * elt.x, 
                            16 * elt.y, 
                            0, 
                            80 + frame_offset, 
                            48, 
                            16, 
                            16
                        )

                if pyxel.frame_count % duree_animation == 0 and len(self.grille.animations) > 0:
                    for elt in self.grille.animations:
                        elt.terrain = PARAMS.VIDE
                        elt.en_explosion = False
                    self.grille.animations.clear()

App()