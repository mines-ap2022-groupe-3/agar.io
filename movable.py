from fruit import Fruit
from utilities import clamp
from screen import M_WIDTH, M_HEIGHT
from circle import Circle
from pygame.math import Vector2 as V2


class Movable(Circle):
    """movable is player or enemy"""

    movable_list = []

    def __init__(self, radius, xy, color):
        super().__init__(radius, xy, color)
        self.split_list = [self]
        self.dr = V2(0, 0)

    def get_dr(self):
        return self.dr

    def set_dr(self, dr):
        self.dr = dr

    def eat(self):
        """mange les enemies de enemy_list et fruits de fruits_list qui sont dans son rayon"""
        list = [m for m in Movable.movable_list if m != self]
        for m in list:
            if self.circle_inside_self(m):
                # formule pour ajouter à l'air de l'ennemie
                self.set_radius((self.radius**2 + m.get_radius() ** 2) ** (1 / 2))
                del Movable.movable_list[Movable.movable_list.index(m)]

        for f in Fruit.fruits_list:
            if self.circle_inside_self(f):
                self.set_radius((self.radius**2 + f.get_radius() ** 2) ** (1 / 2))
                del Fruit.fruits_list[Fruit.fruits_list.index(f)]

    def move(self):
        """return the new position after one clock time"""
        new_pos = self.xy + self.differential_pos()
        new_pos.x = clamp(new_pos.x, 0, M_WIDTH)
        new_pos.y = clamp(new_pos.y, 0, M_HEIGHT)

        self.set_pos(new_pos)

    def speed(self):
        return 100 / self.radius
