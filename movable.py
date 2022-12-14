from fruit import Fruit
from utilities import clamp
from screen import M_WIDTH, M_HEIGHT
from circle import Circle


class Movable(Circle):
    """movable is player or enemy"""

    movable_list = []

    def eat_fruits(self):
        """eat all fruits inside the blob"""
        for f in Fruit.fruits_list:
            self.set_radius(f.eat_fruit(self))

    def eat_other_movables(self):
        """mange les enemies de enemy_list qui sont dans son rayon"""
        list = [m for m in Movable.movable_list if m != self]
        for m in list:
            if self.circle_center_inside_self(m) and self.radius >= m.get_radius():
                # formule pour ajouter à l'air de l'ennemie
                self.set_radius((self.radius**2 + m.get_radius() ** 2) ** (1 / 2))
                del Movable.movable_list[Movable.movable_list.index(m)]

    def move(self):
        """return the new position after one clock time"""
        new_pos = self.xy + self.differential_pos()
        new_pos.x = clamp(new_pos.x, 0, M_WIDTH)
        new_pos.y = clamp(new_pos.y, 0, M_HEIGHT)

        self.set_pos(new_pos)

    def speed(self):
        return 100 / (self.radius)


# movables eat other movables and fruits
def movables_eat():
    for m in Movable.movable_list:
        m.eat_other_movables()
        m.eat_fruits()
