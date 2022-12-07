import random
from math import floor
from pygame.math import Vector2 as V2

SCREEN = V2(1200, 800)
WIDTH, HEIGHT = SCREEN


# Utilities
def round_to(n, div):
    return floor(n / div) * div


def clamp(value, min_value, max_value):
    return min(max_value, max(value, min_value))


def generate_random_color():
    return random.randrange(255), random.randrange(255), random.randrange(255)


def generate_random_position():
    return random.randint(0, HEIGHT), random.randint(0, WIDTH)
