import random

#Classes

class DB:
    KEYS = {
        ("KEY_Z", "KEY_UP"): "up",
        ("KEY_S", "KEY_DOWN"): "down",
        ("KEY_Q", "KEY_LEFT"): "left",
        ("KEY_D", "KEY_RIGHT"): "right"
    }

#Utils

def est_pair(i: int) -> bool:
    return i % 2 == 0

def probas(liste: dict):
    prob = random.random()
    cumul = 0
    for event in liste:
        cumul += liste[event]
        if prob <= cumul:
            return event