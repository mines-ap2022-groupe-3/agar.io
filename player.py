from utilities import generate_random_color
from screen import M_WIDTH, M_HEIGHT, SCREEN_CENTER
from pygame.math import Vector2 as V2
import pygame as pg
from movable import Movable


class Player(Movable):

    speed = 4
    max_speed = 100

    def __init__(
        self,
        xy=V2(M_WIDTH / 2, M_HEIGHT / 2),
        color=generate_random_color(),
        radius=20,
    ):
        self.xy = xy
        self.color = color
        self.radius = radius
        Movable.movable_list.append(self)

    def differential_pos(self):
        """renvoie la différence de position entre deux temps d'horloges"""
        # On trouve la nouvelle direction/position
        new_direction = V2(pg.mouse.get_pos()) - V2(SCREEN_CENTER)
        if new_direction.magnitude() >= Player.max_speed:
            differential_position = new_direction.normalize() * Player.speed
        else:
            differential_position = new_direction / Player.max_speed * Player.speed

        return differential_position


# Bouger
def move_player(player):
    """bouge chaque movable un par un"""
    player.move(player.differential_pos())
