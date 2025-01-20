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
        if pyxel.btnp(pyxel.KEY_E) and not self.player1.launched:
            self.player1.dropBomb()
        elif pyxel.btnp(pyxel.KEY_J) and not self.player2.launched:
            self.player2.dropBomb()


    def reset(self):
        self.menu.show = True
        self.grille = Grille(13,13)
        self.grille.position_init()

        self.player1 = Bomber(0,0,"player1",self.grille,1, "right")
        self.player1.spawn()
        self.player2 = Bomber(12,12,"player2",self.grille,2, "left")
        self.player2.spawn()


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
                                self.reset()

                if case.terrain == PARAMS.PILLIER and not self.grille.end:
                    pyxel.blt(16*i, 16*j, 0, 48,48,  16, 16)
                elif case.terrain == PARAMS.BRIQUE and not self.grille.end and not case.en_explosion:
                    pyxel.blt(16*i, 16*j, 0, 64, 48, 16, 16)
                


    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        
        self.deplacement()
        self.bombarder()

        self.grille.manage_bombs()

    def _calcul_portee(self, core: tuple, portee):
        xt, yt = core
        
        def handle_direction(dx, dy):
            for step in range(1, portee + 1):
                new_x = xt + step * dx
                new_y = yt + step * dy
                case = self.grille.get_case(new_x, new_y)
                if case is None:
                    break
                if case.terrain == PARAMS.PILLIER:
                    break
                case.en_explosion = True
                if case.terrain == PARAMS.BRIQUE:
                    break
            return (new_x, new_y) 
        
        limits = {"gauche": handle_direction(-1, 0), "droite": handle_direction(1, 0), "haut": handle_direction(0, -1), "bas": handle_direction(0, 1)}
        return limits
    
    def _change_limits(self, direction: str):
        facteurs_x = ("gauche", "droite")
        facteurs_y = ("haut", "bas")
        if direction == facteurs_x[0] and self.limites[direction][0] > self.x:
            self.cx += 16
            self.sx -= 16
            self.x += 1
        elif direction == facteurs_x[1] and self.limites[direction][0] <= self.x + 5:
            xc,yc = self.limites[direction]
            case = self.grille.get_case(xc,yc)
            if case is not None and not case.terrain == PARAMS.VIDE:
                self.sx -= 16
        elif direction == facteurs_y[0] and self.limites[direction][1] > self.y:
            self.cy += 16
            self.sy -= 16
            self.y += 1
        elif direction == facteurs_y[1] and self.limites[direction][1] <= self.y + 5:
            xc,yc = self.limites[direction]
            case = self.grille.get_case(xc,yc)
            if case is not None and not case.terrain == PARAMS.VIDE:
                self.sy -= 16

    def draw(self):
        if self.menu.show:
            self.menu.update()
            self.menu.draw()
        else:
            if self.menu.mode == "quit":
                pyxel.quit()
            else:
                pyxel.cls(0)
                for i in range(len(self.grille.explosions_anim) - 1, -1, -1):  
                    if self.grille.counter[i] is None:
                        self.grille.counter[i] = pyxel.frame_count

                    

                    temps = self.grille.counter[i]
                    duree_ex = 6
                    duree_br = 4
                    coef_ex = (pyxel.frame_count // duree_ex) % 4
                    coef_br = (pyxel.frame_count // duree_br) % 6

                    # explosions
                    bomb = self.grille.explosions_anim[i]
                    self.cx, self.cy = DB.SPRITES["explosions"][coef_ex]
                    self.sx = 80
                    self.sy = 80
                    self.x, self.y = bomb.x - 2, bomb.y - 2
                    self.limites = self._calcul_portee((bomb.x, bomb.y), 2)

                    for item in list(self.limites.keys()):
                        self._change_limits(item)

                    # briques
                    self.cxb, self.cyb = 80 + 16 * coef_br, 48


                    if temps + 24 > pyxel.frame_count:
                        pyxel.blt(self.x * 16, self.y * 16, 0, self.cx, self.cy, self.sx, self.sy)            
                        for elt in self.grille.animations:
                            if elt.x == bomb.x and elt.y == bomb.y:
                                pass
                            else:
                                self.xb, self.yb = elt.x, elt.y
                                pyxel.blt(16*self.xb, 16*self.yb, 0, self.cxb, self.cyb, 16, 16)
                    else:
                        self.grille.explosions_anim.pop(i)
                        self.grille.counter.pop(i)

                        case = self.grille.get_case(bomb.x, bomb.y)
                        l_id = self.player1 if bomb.l_id == 1 else self.player2
                        l_id.launched = False

                        case.bomb = None

                        for i in range(len(self.grille.animations)- 1, -1, -1):
                            self.grille.animations[i].terrain = PARAMS.VIDE
                            self.grille.animations.pop(i)

                self.draw_grille()

App()