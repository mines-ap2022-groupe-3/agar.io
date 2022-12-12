import pygame as pg
import pygame_menu as pg_menu
from pygame.color import THECOLORS as COLORS
import screen as sc


INDEX = [
    ("Black", "black"),
    ("White", "white"),
    ("Blue", "blue"),
    ("Red", "red"),
    ("Green", "green"),
]


def change_color_background(index, color):
    """Permet de changer la couleur du fond d'écran à partir du menu"""
    sc.BACKGROUND_COLOR = COLORS[color]


def change_color_blop(index, color):
    """Permet de changer la couleur du blop à partir du menu"""
    sc.COLOR_BLOP = COLORS[color]


def change_player_name(name):
    """Permet de récupérer le nom du joueur à partir du menu"""
    sc.PLAYER_NAME = name


def display_pause_menu(pauseMenu, screen):
    """Pour faire tourner le menu pause"""
    while pauseMenu.is_enabled():
        events = pg.event.get()
        pauseMenu.draw(screen)
        pauseMenu.update(events)
        pg.display.update()
