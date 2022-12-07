import random
from math import floor

import pygame as pg
from pygame.color import THECOLORS as COLORS
from pygame.math import Vector2 as V2
from collections import namedtuple

OVERMAP_BG = COLORS["white"]
BOARD_COLOR = COLORS["grey"]
BACKGROUND_COLOR = COLORS["black"]

SCREEN = V2(1200, 800)
WIDTH, HEIGHT = SCREEN
SCREEN_CENTER = SCREEN / 2

TILE_SIZE = 50

MAP = 2 * SCREEN
M_WIDTH, M_HEIGHT = MAP

MAX_SPEED = 100

PROBA_APPARITION_FRUIT = 0.05
NB_MAX_FRUIT = 40
RAYON_FRUIT_MIN = 5
RAYON_FRUIT_MAX = 12

BLOB_SIZE_IN = 20


def round_to(n, div):
    return floor(n / div) * div


def clamp(value, min_value, max_value):
    return min(max_value, max(value, min_value))


def couleur_debut():
    SCREEN2 = V2(400, 400)
    pg.display.set_mode(SCREEN2)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        # un type de pg.KEYDOWN signifie que l'on a appuyé une touche du clavier
        elif event.type == pg.KEYDOWN:
            # si la touche est "Q" ou "escape" on veut quitter le programme
            if event.key == pg.K_q or event.key == pg.K_ESCAPE:
                done = True
            elif event.key == pg.K_b:
                return COLORS["blue"]
            elif event.key == pg.K_r:
                return COLORS["red"]
            elif event.key == pg.K_y:
                return COLORS["yellow"]
