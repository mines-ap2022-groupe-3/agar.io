#!/usr/bin/env python

import screen as sc
import pygame as pg
from movable import Movable
from player import Player
from bot import generate_bot
from fruit import Fruit, generate_fruit


MAX_SPEED = 100
SCREEN_CENTER = sc.SCREEN / 2


def main():
    clock = pg.time.Clock()

    # on initialise pygame et on crée une fenêtre de 800x800 pixels
    pg.init()
    screen = pg.display.set_mode((sc.WIDTH, sc.HEIGHT))

    # On donne un titre à la fenetre
    pg.display.set_caption("agario")

    player = Player()

    # La boucle du jeu
    done = False
    while not done:
        # FPS
        clock.tick(60)

        pg.display.set_caption(
            f"agario - {player.get_pos().x=:5.0f} - {player.get_pos().y=:5.0f}"
        )

        # drawing map
        sc.draw_background(screen)
        sc.draw_map(screen, player.get_pos())
        sc.draw_overmap(screen, player.get_pos())

        # generate enemies and fruits
        generate_bot()
        generate_fruit()

        # Move and eat
        for movable in Movable.movable_list:
            movable.eat_other_movables()
            movable.eat_fruits()
            movable.move(movable.differential_pos())

        # draw movables and fruits on screen
        for f in Fruit.fruits_list:
            sc.draw_fruit(f, screen, player.get_pos())
        for m in Movable.movable_list:
            sc.draw_movable(m, screen, player.get_pos())

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
