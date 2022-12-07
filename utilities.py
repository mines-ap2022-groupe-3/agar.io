import random
from math import floor
import pygame as pg
from pygame.math import Vector2 as V2
from collections import namedtuple


# Global variables
from screen import M_WIDTH, M_HEIGHT, SCREEN_CENTER

PROBA_APPARITION_FRUIT = 0.05
NB_MAX_FRUIT = 40
RAYON_FRUIT_MIN = 5
RAYON_FRUIT_MAX = 12

Fruit = namedtuple("Fruit", ["xy", "color", "radius"])
LIST_FRUITS = []

MAX_SPEED = 100


# Utilities
def round_to(n, div):
    """arrondi n"""
    return floor(n / div) * div


def clamp(value, min_value, max_value):
    """renvoie min_value si value<min_value, max_value si value>max_value, value sinon"""
    return min(max_value, max(value, min_value))


def generate_random_color():
    """génère une couleur aléatoire"""
    return random.randrange(255), random.randrange(255), random.randrange(255)


def generate_random_fruit_position():
    """génère une position aléatoire"""
    x, y = random.randint(0, M_WIDTH), random.randint(0, M_HEIGHT)
    return V2(x, y)


def generate_random_fruit_radius():
    """génère un rayon aléatoire entre RAYON_FRUIT_MIN et RAYON_FRUIT_MAX"""
    r = random.randint(RAYON_FRUIT_MIN, RAYON_FRUIT_MAX)
    return r


def generate_fruit():
    """génère un fruit aléatoirement sur le screen"""
    if len(LIST_FRUITS) == 0 or (
        random.random() < PROBA_APPARITION_FRUIT and len(LIST_FRUITS) < NB_MAX_FRUIT
    ):
        xy = generate_random_fruit_position()
        color = generate_random_color()
        radius = generate_random_fruit_radius()
        LIST_FRUITS.append(Fruit(xy, color, radius))


# Manger fruit
def eat_fruit(position, size) -> int:
    """si le fruit est assez proche, le mange. Renvoie la nouvelle taille après absorbation d'un ou plusieurs fruits"""
    for f in LIST_FRUITS:
        if (position - f.xy).length() < size:
            # formule pour ajouter à l'air du blob l'air du fruit
            size = (size**2 + f.radius**2) ** (1 / 2)
            del LIST_FRUITS[LIST_FRUITS.index(f)]
    return size


def new_direction():
    """donne la nouvelle direction normalisée"""
    new_direction = V2(pg.mouse.get_pos()) - V2(SCREEN_CENTER)
    if new_direction.magnitude() >= MAX_SPEED:
        new_direction = new_direction.normalize()
    else:
        new_direction = new_direction / MAX_SPEED

    return new_direction
