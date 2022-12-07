from fruit import LIST_FRUITS
from pygame.math import Vector2 as V2


# POSITION_ENEMY = V2(0, 0)
# VITESSE_ENEMY = 3


def direction_auto(position):
    """fonction qui donne la nouvelle direction"""

    for f in LIST_FRUITS:
        center = f.xy - position + sc.SCREEN_CENTER
