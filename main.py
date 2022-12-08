#!/usr/bin/env python

import utilities
import screen as sc
import fruit
import pygame as pg


def main():
    clock = pg.time.Clock()

    # on initialise pygame et on crée une fenêtre de 800x800 pixels
    pg.init()
    screen = pg.display.set_mode((sc.WIDTH, sc.HEIGHT))

    # On donne un titre à la fenetre
    pg.display.set_caption("agario")

    blob_size = utilities.BLOB_SIZE_IN
    color = utilities.generate_random_color()
    position = utilities.MAP_CENTER

    # La boucle du jeu
    done = False
    while not done:
        # FPS
        clock.tick(60)

        # On déplace
        position += utilities.differencial_position(pg.mouse.get_pos())

        # On s'assure que la position ne sorte pas de la map
        position.x = utilities.clamp(position.x, 0, sc.M_WIDTH)
        position.y = utilities.clamp(position.y, 0, sc.M_HEIGHT)

        # génération des fruits aléatoirement
        fruit.generate_fruit()
        # On mange les fruits à l'intérieur du blob
        blob_size = fruit.eat_fruit(position, size=blob_size)

        # On affiche tout
        sc.draw_background(screen)
        sc.draw_map(screen, position)
        sc.draw_overmap(screen, position)
        sc.draw_blob(screen, size=blob_size, color=color)
        sc.draw_fruits(screen, position)

        pg.display.set_caption(f"agario - {position.x=:5.0f} - {position.y=:5.0f}")
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
