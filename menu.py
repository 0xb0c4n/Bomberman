import pyxel

class Menu:
    def __init__(self):
        self.show = True
        self.i = 0

    def update(self):
        if pyxel.btnp(pyxel.KEY_DOWN) and self.i < 2:
            self.i += 1
        elif pyxel.btnp(pyxel.KEY_UP) and self.i > 0:
            self.i -= 1
    
    def draw(self):
        pyxel.cls(0)
        pyxel.text(65,20,"Bomberman by 0xb0c4n", pyxel.frame_count % 12)
        pyxel.text(80,40,"Solo", 7)
        pyxel.text(80,60,"1v1", 7)
        pyxel.text(80,80,"Multiplayer", 7)
        pyxel.tri(70,39+20*self.i,75,42+20*self.i,70,45+20*self.i,7)