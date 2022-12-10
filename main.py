#!/usr/bin/env python

import screen as sc
import fruit
import pygame as pg
import enemy as e
from pygame.math import Vector2 as V2
import player
import movable as mov


MAX_SPEED = 100
SCREEN_CENTER = sc.SCREEN / 2


def main():
    clock = pg.time.Clock()

    # on initialise pygame et on crée une fenêtre de 800x800 pixels
    pg.init()
    screen = pg.display.set_mode((sc.WIDTH, sc.HEIGHT))

    # On donne un titre à la fenetre
    pg.display.set_caption("agario")

    blob = player.Player()
    player_position = V2(sc.MAP) / 2

    # La boucle du jeu
    done = False
    while not done:
        # FPS
        clock.tick(60)

        pg.display.set_caption(
            f"agario - {player_position.x=:5.0f} - {player_position.y=:5.0f}"
        )

        # Finding position
        player_position = blob.get_pos()

        # drawing map
        sc.draw_background(screen)
        sc.draw_map(screen, player_position)
        sc.draw_overmap(screen, player_position)

        # generate enemies and fruits
        e.generate_enemies()
        fruit.generate_fruit()

        # Move and eat
        e.move_enemies()
        player.move_player(blob)
        mov.movables_eat()

        # draw movables and fruits on screen
        for f in fruit.Fruit.fruits_list:
            sc.draw_fruit(f, screen, player_position)
        for m in mov.Movable.movable_list:
            sc.draw_movable(m, screen, player_position)

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
