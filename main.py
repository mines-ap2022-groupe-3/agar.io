#!/usr/bin/env python

import pygame as pg
from pygame.math import Vector2 as V2
from utilities import generate_random_color, clamp, generate_random_position
from draw import (
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

from fruits import generate_fruit, eat_fruit, draw_fruits, FRUITS_NUMBER


MAX_SPEED = 100
BLOB_SIZE_IN = 20


def main():
    clock = pg.time.Clock()

    # on initialise pygame et on crée une fenêtre de 800x800 pixels
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))

    # On donne un titre à la fenetre
    pg.display.set_caption("agario")

    blob_size = BLOB_SIZE_IN
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
        # for i in range(FRUITS_NUMBER):
        # pos_fruit[i] -= new_direction * speed

        pg.display.set_caption(f"agario - {position.x=:5.0f} - {position.y=:5.0f}")

        # On s'assure que la position ne sorte pas de la map
        position.x = clamp(position.x, 0, M_WIDTH)
        position.y = clamp(position.y, 0, M_HEIGHT)

        draw_background(screen)
        draw_map(screen, position)
        draw_overmap(screen, position)

        draw_blob(screen, color=color)

        generate_fruit()
        blob_size = eat_fruit(position, size=blob_size)
        draw_fruits(screen, position)
        draw_blob(screen, size=blob_size, color=color)

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
