import random
from math import floor

import pygame as pg
from pygame.color import THECOLORS as COLORS
from pygame.math import Vector2 as V2

import time
import pyautogui
import matplotlib.pyplot as plt

import screen as s
def round_to(n, div):
    return floor(n / div) * div


def clamp(value, min_value, max_value):
    return min(max_value, max(value, min_value))


def generate_random_color():
    return random.randrange(255), random.randrange(255), random.randrange(255)


def take_screenshot(screen):
    myscreen = pyautogui.screenshot(region=(50, 0, s.WIDTH, s.HEIGHT))
    myscreen.save("myscreen.jpg")


def fichier_text():
    f = open("map.txt", "w")
    im = plt.imread("myscreen.jpg")
    for i in range(len(im)):
        for j in range(len(im[0])):
            if im[i][j] == s.BACKGROUND_COLOR or im[i][j] == s.BOARD_COLOR:
                f.write(" ")
            else:
                f.write("o")
        f.write("\n")
