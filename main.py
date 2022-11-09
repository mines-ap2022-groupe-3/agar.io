#!/usr/bin/env python

import random
from math import floor, sqrt

import pygame as pg
from pygame.color import THECOLORS as COLORS
from pygame.math import Vector2 as V2

OVERMAP_BG = COLORS["grey"]
BOARD_COLOR = COLORS["grey"]
BACKGROUND_COLOR = COLORS["black"]

SCREEN = V2(1200, 800)
WIDTH, HEIGHT = SCREEN
SCREEN_CENTER = SCREEN / 2

TILE_SIZE = 50

MAP = 2 * SCREEN
M_WIDTH ,  M_HEIGHT = MAP

MAX_SPEED = 100


# Utilities
def round_to(n, div) :
    return floor(n / div) * div


def clamp(value, min_value, max_value) :
    return min(max_value, max(value, min_value))


def generate_random_color() :
    return random.randrange(255), random.randrange(255), random.randrange(255)


# Drawing functions
def draw_background(screen) :
    full_screen = pg.Rect(0, 0, WIDTH, HEIGHT)
    pg.draw.rect(screen, BACKGROUND_COLOR, full_screen)


def draw_map(screen, position, tile_size=TILE_SIZE) :
    display_rect = pg.Rect(
        position.x - SCREEN_CENTER.x, position.y - SCREEN_CENTER.y, WIDTH, HEIGHT
    )

    first_square_left = int(max(0, round_to(display_rect.left, tile_size)))
    first_square_top = int(max(0, round_to(display_rect.top, tile_size)))

    last_square_right = int(min(M_WIDTH, first_square_left + WIDTH))
    last_square_bottom = int(min(M_HEIGHT, first_square_top + HEIGHT))

    # Draw verticals lines
    # left = 105
    # right = 745
    # tuile = 50
    for i in range(first_square_left, last_square_right + 1, tile_size):
        pos_i = i - display_rect.x
        pg.draw.line(screen, BOARD_COLOR, (pos_i, 0), (pos_i, HEIGHT))

    # Draw horizontals lines
    for j in range(first_square_top, last_square_bottom + 1, tile_size):
        pos_j = j - display_rect.y
        pg.draw.line(screen, BOARD_COLOR, (0, pos_j), (WIDTH, pos_j))


def draw_blob(screen, size=20, color=None):
    x, y = SCREEN_CENTER
    pg.draw.circle(screen, color, (x, y), size)


def draw_overmap(screen, position):
    display_rect = pg.Rect(
        position.x - SCREEN_CENTER.x, position.y - SCREEN_CENTER.y, WIDTH, HEIGHT
    )

    if display_rect.left < 0:
        mask = pg.Rect(0, 0, -display_rect.left, HEIGHT)
        pg.draw.rect(screen, OVERMAP_BG, mask)

    if display_rect.top < 0:
        mask = pg.Rect(0, 0, WIDTH, -display_rect.top)
        pg.draw.rect(screen, OVERMAP_BG, mask)

    if display_rect.right >= M_WIDTH:
        mask = pg.Rect(M_WIDTH - display_rect.right + WIDTH, 0, WIDTH, HEIGHT)
        pg.draw.rect(screen, OVERMAP_BG, mask)

    if display_rect.bottom >= M_HEIGHT:
        mask = pg.Rect(0, M_HEIGHT - display_rect.bottom + HEIGHT, WIDTH, HEIGHT)
        pg.draw.rect(screen, OVERMAP_BG, mask)


def random_position_generator():
    return random.randint(0, HEIGHT), random.randint(0, WIDTH)


def draw_fruit(screen, position, size=5, color=None):
    x, y = position
    pg.draw.circle(screen, color, (x, y), size)


def main():
    clock = pg.time.Clock()

    # on initialise pygame et on crée une fenêtre de 800x800 pixels
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))

    # On donne un titre à la fenetre
    pg.display.set_caption("agario")

    color = generate_random_color()
    speed = 4
    position = V2(MAP) / 2
    pos_fruit = random_position_generator()
    color_fruit = generate_random_color()
    blop_size = 20

    # La boucle du jeu
    done = False
    while not done:
        # FPS
        clock.tick(60)

        # On trouve la nouvelle direction/position
        new_direction = V2(pg.mouse.get_pos()) - V2(SCREEN_CENTER)
        if new_direction.magnitude() >= MAX_SPEED:
            new_direction = new_direction.normalize()
        else:
            new_direction = new_direction / MAX_SPEED

        position += new_direction * speed
        pos_fruit -= new_direction * speed

        pg.display.set_caption(f"agario - {position.x=:5.0f} - {position.y=:5.0f}")

        # On s'assure que la position ne sorte pas de la map
        position.x = clamp(position.x, 0, M_WIDTH)
        position.y = clamp(position.y, 0, M_HEIGHT)

        draw_background(screen)
        draw_map(screen, position)
        draw_overmap(screen, position)

        draw_fruit(screen, pos_fruit, color=color_fruit)

        draw_blob(screen, size=blop_size, color=color)

        # manger le fruit
        if (
            sqrt(
                (pos_fruit[0] - SCREEN_CENTER[0]) ** 2
                + (pos_fruit[1] - SCREEN_CENTER[1]) ** 2
            )
            <= blop_size
        ):
            blop_size += 5
            pos_fruit = random_position_generator()
            color_fruit = generate_random_color()

        pg.display.update()

        # on itère sur tous les évênements qui ont eu lieu depuis le précédent appel
        # ici donc tous les évènements survenus durant la seconde précédente
        for event in pg.event.get():
            # chaque évênement à un type qui décrit la nature de l'évênement
            # un type de pg.QUIT signifie que l'on a cliqué sur la "croix" de la fenêtre
            if event.type == pg.QUIT:
                done = True
            # un type de pg.KEYDOWN signifie que l'on a appuyé une touche du clavier
            elif event.type == pg.KEYDOWN:
                # si la touche est "Q" ou "escape" on veut quitter le programme
                if event.key == pg.K_q or event.key == pg.K_ESCAPE:
                    done = True

    pg.quit()


# if python says run, then we should run
if __name__ == "__main__":
    main()
    # print(round_to(105, 19))
