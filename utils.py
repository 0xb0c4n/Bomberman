import random

#Classes

class DB:
    KEYS = {
        ("KEY_Z", "KEY_UP"): "up",
        ("KEY_S", "KEY_DOWN"): "down",
        ("KEY_Q", "KEY_LEFT"): "left",
        ("KEY_D", "KEY_RIGHT"): "right"
    }

    SPRITES = {
        "up": (48,16),
        "down": (48,0),
        "left": (0,0),
        "right": (0,16),
        "explosions": {
            0: (0,64),
            1: (64,64),
            2: (0,144),
            3: (64,144)
        }
    }


#Utils

def est_pair(i: int) -> bool:
    """Renvoie un booléen correspondant à la parité d'un entier i
    Prend en paramètre en entier i"""
    return i % 2 == 0

def probas(liste: dict):
    """Renvoie un évènement aléatoire à partir d'un dictionnaire d'évènements
    Prend en paramètre un dictionnaire d'évènements avec leurs probabilités (float)"""
    prob = random.random()
    cumul = 0
    for event in liste:
        cumul += liste[event]
        if prob <= cumul:
            return event