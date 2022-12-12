#!/usr/bin/env python

import utilities
import screen as sc
import fruit
import pygame as pg
from pygame.math import Vector2 as V2
import pygame_menu as pg_menu
from pygame.color import THECOLORS as COLORS
from pygame.math import Vector2 as V2
import pygame_menu as pg_menu

PLAYER_NAME = "Player"

INDEX = [
    ("Black", "black"),
    ("White", "white"),
    ("Blue", "blue"),
    ("Red", "red"),
    ("Green", "green"),
]


def change_color_background(index, color):
    """Permet de changer la couleur du fond d'écran à partir du menu"""
    global BACKGROUND_COLOR
    BACKGROUND_COLOR = COLORS[color]


def change_color_blop(index, color):
    """Permet de changer la couleur du blop à partir du menu"""
    global COLOR_BLOP
    COLOR_BLOP = COLORS[color]


def get_player_name(name):
    """Permet de récupérer le nom du joueur à partir du menu"""
    global PLAYER_NAME
    PLAYER_NAME = name


def PAUSE_MENU(pauseMenu, screen):
    """Pour faire tourner le menu pause"""
    while pauseMenu.is_enabled():
        events = pg.event.get()
        pauseMenu.draw(screen)
        pauseMenu.update(events)
        pg.display.update()


def change_color_background(index, color):
    """Permet de changer la couleur du fond d'écran à partir du menu"""
    global BACKGROUND_COLOR
    BACKGROUND_COLOR = COLORS[color]


def change_color_blop(index, color):
    """Permet de changer la couleur du blop à partir du menu"""
    global COLOR_BLOP
    COLOR_BLOP = COLORS[color]


def get_player_name(name):
    """Permet de récupérer le nom du joueur à partir du menu"""
    global PLAYER_NAME
    PLAYER_NAME = name


def PAUSE_MENU(pauseMenu, screen):
    """Pour faire tourner le menu pause"""
    while pauseMenu.is_enabled():
        events = pg.event.get()
        pauseMenu.draw(screen)
        pauseMenu.update(events)
        pg.display.update()


def main():
    clock = pg.time.Clock()

    # on initialise pygame et on crée une fenêtre de 800x800 pixels
    pg.init()
    screen = pg.display.set_mode((sc.WIDTH, sc.HEIGHT))

    # On donne un titre à la fenetre
    pg.display.set_caption("agario")

    blob_size = sc.BLOB_SIZE_IN
    color = utilities.generate_random_color()    
    
    # Création du menu de pause et initialisation des différents éléments
    pauseMenu = pg_menu.Menu(
        "Pause", sc.WIDTH / 2, sc.HEIGHT / 2, theme=pg_menu.themes.THEME_BLUE
    )
    pauseMenu.add.text_input("Name : ", default="Player", onchange=get_player_name)
    pauseMenu.add.selector(
        "Couleur du fond : ", INDEX, onchange=change_color_background
    )
    pauseMenu.add.selector("Couleur du blop : ", INDEX, onchange=change_color_blop)
    pauseMenu.add.button("Continuer", pauseMenu.disable)
    pauseMenu.add.button("Recommencer", main)
    pauseMenu.add.button("Quitter", pg_menu.events.EXIT)
    pauseMenu.disable()  # par défault on n'affiche pas le menu
    speed = 4
    position = V2(sc.MAP) / 2
    SCREEN_CENTER = sc.SCREEN / 2
    MAX_SPEED = 100

    # La boucle du jeu
    done = False
    while not done:
        # FPS
        clock.tick(60)

        # Je commence par regarder si je dois afficher le menu
        if pauseMenu.is_enabled():
            PAUSE_MENU(pauseMenu, screen)

        # On trouve la nouvelle direction/position
        new_direction = V2(pg.mouse.get_pos()) - V2(SCREEN_CENTER)
        if new_direction.magnitude() >= MAX_SPEED:
            new_direction = new_direction.normalize()
        else:
            new_direction = new_direction / MAX_SPEED

        position += new_direction * speed

        pg.display.set_caption(
            f"agario - {position.x=:5.0f} - {position.y=:5.0f} - Partie de {PLAYER_NAME}"
        )

        # On s'assure que la position ne sorte pas de la map
        position.x = utilities.clamp(position.x, 0, sc.M_WIDTH)
        position.y = utilities.clamp(position.y, 0, sc.M_HEIGHT)

        sc.draw_background(screen)
        sc.draw_map(screen, position)
        sc.draw_overmap(screen, position)

        fruit.generate_fruit()
        blob_size = fruit.eat_fruit(position, size=blob_size)
        fruit.draw_fruits(screen, position)
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
                if event.key == pg.K_p:
                    # Si la touche "p" est appuyée on rentre dans le menu Pause
                    pauseMenu.enable()
    pg.quit()


# if python says run, then we should run
if __name__ == "__main__":
    main()
