import utilities as utls
import random
import screen
from collections import namedtuple


PROBA_APPARITION_FRUIT = 0.05
NB_MAX_FRUIT = 40
RAYON_FRUIT_MIN = 5
RAYON_FRUIT_MAX = 12

# génération fruit
Fruit = namedtuple("Fruit", ["xy", "color", "radius"])
LIST_FRUITS = []


def generate_random_fruit_radius():
    """génère un rayon aléatoire entre RAYON_FRUIT_MIN et RAYON_FRUIT_MAX"""
    r = random.randint(RAYON_FRUIT_MIN, RAYON_FRUIT_MAX)
    return r


def generate_fruit():
    """génère un fruit aléatoirement sur le screen"""
    if len(LIST_FRUITS) == 0 or (
        random.random() < PROBA_APPARITION_FRUIT and len(LIST_FRUITS) < NB_MAX_FRUIT
    ):
        xy = screen.generate_random_fruit_position()
        color = utls.generate_random_color()
        radius = generate_random_fruit_radius()
        LIST_FRUITS.append(Fruit(xy, color, radius))


# Manger fruit


def eat_fruit(position, size) -> int:
    """si le fruit est assez proche, le mange. Renvoie la nouvelle taille après absorbation d'un ou plusieurs fruits"""
    for f in LIST_FRUITS:
        if (position - f.xy).length() < size:
            # formule pour ajouter à l'air du blob l'air du fruit
            size = (size**3 + f.radius**3) ** (1 / 3)
            del LIST_FRUITS[LIST_FRUITS.index(f)]
    return size
