import pyxel

class Menu:
    def __init__(self):
        self.show = True
        self.mode = None
        self.i = 0
        self.dico = {
            0: "play",
            1: "quit"
        }

    def update(self):
        if pyxel.btnp(pyxel.KEY_DOWN) and self.i < 1:
            self.i += 1
        elif pyxel.btnp(pyxel.KEY_UP) and self.i > 0:
            self.i -= 1
        elif pyxel.btnp(pyxel.KEY_RETURN):
            self.mode = self.dico[self.i]
            self.show = False
    
    def draw(self):
        pyxel.cls(0)
        pyxel.text(65,20,"Bomberman by 0xb0c4n", pyxel.frame_count % 12)
        pyxel.text(80,40,"Play", 7)
        pyxel.text(80,60,"Quit", 7)
        pyxel.tri(70,39+20*self.i,75,42+20*self.i,70,45+20*self.i,7)
