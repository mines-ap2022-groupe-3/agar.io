import random
import pygame
from math import floor
import screen as sc
import os
import numpy as np
import matplotlib.pyplot as plt

# Utilities
def round_to(n, div):
    return floor(n / div) * div


def clamp(value, min_value, max_value):
    return min(max_value, max(value, min_value))


def generate_random_color():
    return random.randrange(255), random.randrange(255), random.randrange(255)


def screenshot(screen):
    if not os.path.exists("screenshot/PNG"):
        os.mkdir("screenshot/PNG")
    return pygame.image.save(
        screen,
        "screenshot/PNG/screenshot" + str(len(os.listdir("screenshot/PNG"))) + ".png",
    )


def screenshot_txt(list_fruits, coord_blop):
    if not os.path.exists("screenshot/TXT"):
        os.mkdir("screenshot/TXT")
    map = np.full((int(sc.M_HEIGHT / 50) + 1, int(sc.M_WIDTH / 50) + 1), " ")
    for parameters in list_fruits:
        map[int(parameters[0].y / 50), int(parameters[0].x / 50)] = "."
    map[int(coord_blop.y / 50), int(coord_blop.x / 50)] = "O"

    with open(
        "screenshot/TXT/screenshot" + str(len(os.listdir("screenshot"))) + ".txt", "w"
    ) as file:
        char = ""
        for i in range(map.shape[0]):
            for j in range(map.shape[1]):
                char += map[i, j]
            char += "\n"
        file.write(char)
        file.close()
