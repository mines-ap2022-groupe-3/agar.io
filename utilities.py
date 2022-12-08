import random
from math import floor
from pygame.math import Vector2 as V2

# Global Variables
SCREEN = V2(1200, 800)
WIDTH, HEIGHT = SCREEN
SCREEN_CENTER = SCREEN / 2

MAP = 2 * SCREEN
M_WIDTH, M_HEIGHT = MAP
MAP_CENTER = V2(MAP) / 2

MAX_DIRECTION_MAGNETUDE = 100
BLOB_SPEED = 4
BLOB_SIZE_IN = 20


# Utilities
def round_to(n, div):
    """arrondi n en base div"""
    return floor(n / div) * div


def clamp(value, min_value, max_value):
    """Renvoie value si value est compris entre min_value et max_value. Si value>max_value, renvoie max_value. Si value<min_value, renvoie min_value"""
    return min(max_value, max(value, min_value))


def generate_random_color():
    """génère une couleur aléatoire"""
    return random.randrange(255), random.randrange(255), random.randrange(255)


def new_direction(position):
    """On trouve la direction du blob"""
    new_direction = V2(position) - V2(SCREEN_CENTER)
    if new_direction.magnitude() >= MAX_DIRECTION_MAGNETUDE:
        new_direction = new_direction.normalize()
    else:
        new_direction = new_direction / MAX_DIRECTION_MAGNETUDE

    return new_direction


def differencial_position(position):
    """Renvoie la différence entre la position et la nouvelle position après un temps d'horloge (c'est à dire dr = direction * BLOB_SPEED où BLOB_SPEED est un facteur adimenssionné)"""
    return new_direction(position) * BLOB_SPEED
