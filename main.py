#!/usr/bin/env python

# Utilities
import pygame as pg
from pygame.math import Vector2 as V2
import utilities as ut
import screen as sc


# Global variables
from screen import WIDTH, HEIGHT, SCREEN_CENTER, MAP, M_WIDTH, M_HEIGHT

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
    color = ut.generate_random_color()
    speed = 4
    position = V2(MAP) / 2

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

        pg.display.set_caption(f"agario - {position.x=:5.0f} - {position.y=:5.0f}")

        # On s'assure que la position ne sorte pas de la map
        position.x = ut.clamp(position.x, 0, M_WIDTH)
        position.y = ut.clamp(position.y, 0, M_HEIGHT)

        ut.generate_fruit()
        blob_size = ut.eat_fruit(position, size=blob_size)

        sc.draw_background(screen)
        sc.draw_map(screen, position)
        sc.draw_overmap(screen, position)
        sc.draw_fruits(screen, position)
        sc.draw_blob(screen, size=blob_size, color=color)

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
