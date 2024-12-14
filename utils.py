import random

def est_pair(i: int):
    return i % 2 == 0

def probas(liste: dict):
    prob = random.random()
    cumul = 0
    for event in liste:
        cumul += liste[event]
        if prob <= cumul:
            return event