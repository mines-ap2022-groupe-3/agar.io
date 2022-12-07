#!/usr/bin/env python

from math import sqrt

import pygame as pg
from pygame.color import THECOLORS as COLORS
from pygame.math import Vector2 as V2
from utilities import generate_random_color, clamp, generate_random_position
from draw import (
    draw_fruit,
    draw_overmap,
    draw_map,
    draw_background,
    draw_blob,
    WIDTH,
    HEIGHT,
    M_HEIGHT,
    M_WIDTH,
    MAP,
    SCREEN_CENTER,
)

MAX_SPEED = 100

FRUITS_NUMBER = 20


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
    pos_fruit = []
    color_fruit = []
    for i in range(FRUITS_NUMBER):
        pos_fruit.append(generate_random_position())
        color_fruit.append(generate_random_color())

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
        for i in range(FRUITS_NUMBER):
            pos_fruit[i] -= new_direction * speed

        pg.display.set_caption(f"agario - {position.x=:5.0f} - {position.y=:5.0f}")

        # On s'assure que la position ne sorte pas de la map
        position.x = clamp(position.x, 0, M_WIDTH)
        position.y = clamp(position.y, 0, M_HEIGHT)

        draw_background(screen)
        draw_map(screen, position)
        draw_overmap(screen, position)

        for i in range(FRUITS_NUMBER):
            draw_fruit(screen, pos_fruit[i], color=color_fruit[i])

        draw_blob(screen, size=blop_size, color=color)

        # manger le fruit
        for i in range(FRUITS_NUMBER):
            if (
                sqrt(
                    (pos_fruit[i][0] - SCREEN_CENTER[0]) ** 2
                    + (pos_fruit[i][1] - SCREEN_CENTER[1]) ** 2
                )
                <= blop_size
            ):
                blop_size += 5
                pos_fruit[i] = generate_random_position()
                color_fruit[i] = generate_random_color()

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
