from utilities import generate_random_color, clamp
from screen import M_WIDTH, M_HEIGHT, SCREEN_CENTER
from pygame.math import Vector2 as V2
import pygame as pg
from movable import Movable


class Player(Movable):

    max_speed = 100

    def __init__(
        self,
        xy=V2(M_WIDTH / 2, M_HEIGHT / 2),
        color=generate_random_color(),
        radius=20,
    ):
        super().__init__(radius, xy, color)
        Movable.movable_list.append(self)

    def differential_pos(self):
        """renvoie la différence de position entre deux temps d'horloges"""
        # On trouve la nouvelle direction/position
        new_direction = V2(pg.mouse.get_pos()) - V2(SCREEN_CENTER)
        regression_coefficiant = clamp(
            (new_direction / Player.max_speed).length(), 0, 1
        )

        force = new_direction.normalize() * regression_coefficiant

        diff_position = 0.5 * force + self.get_dr()

        length_diff_position = clamp(diff_position.length(), 0, self.speed())
        diff_position = diff_position.normalize() * length_diff_position
        self.set_dr(diff_position)

        return diff_position
