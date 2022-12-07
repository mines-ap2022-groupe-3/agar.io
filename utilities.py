import random
import pygame
from math import floor

# Utilities
def round_to(n, div):
    return floor(n / div) * div


def clamp(value, min_value, max_value):
    return min(max_value, max(value, min_value))


def generate_random_color():
    return random.randrange(255), random.randrange(255), random.randrange(255)


def screenshot(screen, count):
    return pygame.image.save(screen, "screenshot/screenshot" + str(count) + ".png")
