from utilities import generate_random_color, clamp
from pygame.math import Vector2 as V2
import pygame as pg
from movable import Movable


class Player(Movable):

    max_speed = 100

    def __init__(
        self,
        color=generate_random_color(),
        radius=20,
        v2_map=V2(2400, 1600),
        v2_screen=V2(1200, 800),
    ):
        xy = V2(v2_map.x / 2, v2_map.y / 2)
        super().__init__(radius, xy, color, v2_screen)
        Movable.movable_list.append(self)

    def differential_pos(self):
        """renvoie la différence de position entre deux temps d'horloges"""
        # find the new direction from mouse
        new_direction = V2(pg.mouse.get_pos()) - self.v2_screen / 2
        regression_coefficiant = clamp(
            (new_direction / Player.max_speed).length(), 0, 1
        )

        # implement a V2 newton force that pushes the blob towards the mouse
        if new_direction != V2(0, 0):
            force = new_direction.normalize() * regression_coefficiant
        # from a discretized newton 2nd law : ma = force => dr = c*f + previous_dr * factor where factor corresponds to frixion forces, to slow down with the mouse
        factor = (regression_coefficiant * (2 - regression_coefficiant)) ** (1 / 2)
        diff_position = 0.5 * force + self.get_dr() * factor

        # limit the speed of the blob
        length_diff_position = clamp(diff_position.length(), 0, self.speed())
        diff_position = diff_position.normalize() * length_diff_position
        # set the new differencial position for the next call
        self.set_dr(diff_position)

        return diff_position
