from utilities import generate_random_color
import random
from screen import M_WIDTH, M_HEIGHT, WIDTH, HEIGHT
from pygame.math import Vector2 as V2
from fruit import Fruit
from movable import Movable


MAX_ENEMY_NB = 10


class Enemy(Movable):

    speed = 3.5

    def __init__(
        self,
        radius=20,
    ):
        self.xy = V2(random.randint(0, M_WIDTH), random.randint(0, M_HEIGHT))
        self.color = generate_random_color()
        self.radius = radius
        Movable.movable_list.append(self)

    # automatic movement
    # préparation des directions
    def is_inside_of_screen(self, pos):
        """renvoie si un objet mangeable (fruit, joueur, ou ennemie) est affiché pour l'objet à position"""
        return (
            abs((pos - self.xy).x) < WIDTH / 2 and abs((pos - self.xy).y) < HEIGHT / 2
        )

    def direction_auto(self):
        """fonction qui donne la nouvelle direction"""

        eval_max = 0
        direction = V2(1, 0)

        # direction des meilleurs fruits
        for f in Fruit.fruits_list:
            if not self.is_inside_of_screen(f.xy):
                continue
            pos_fruit_relative = f.xy - self.xy
            distance_fruit = pos_fruit_relative.length()
            eval = eval_eatable(distance_fruit, f.radius, self.radius)
            if eval > eval_max:
                eval_max = eval
                direction = pos_fruit_relative.normalize()

        # direction des meilleurs ennemies à manger ou fuite
        list = [m for m in Movable.movable_list if self != m]
        for m in list:
            if not self.is_inside_of_screen(m.get_pos()):
                continue
            pos_relative = m.get_pos() - self.xy
            distance_enemy = pos_relative.length()
            eval = eval_eatable(distance_enemy, m.get_radius(), self.radius)

            if eval > eval_max:
                eval_max = eval
                direction = pos_relative.normalize()

            elif eval == -1:
                direction -= eval_dangerosity(distance_enemy) * pos_relative.normalize()

        direction = direction.normalize()
        return direction

    def differential_pos(self):
        """renvoie la différence de position entre deux temps d'horloges"""
        return self.direction_auto() * Enemy.speed


#generate enemies
def generate_enemies():
    enemy_list = [mov for mov in Movable.movable_list if isinstance(mov, Enemy)]
    for _ in range(len(enemy_list), MAX_ENEMY_NB):
        Enemy()


# Bouger
def move_enemies():
    """bouge chaque movable un par un"""
    enemy_list = [mov for mov in Movable.movable_list if isinstance(mov, Enemy)]
    for en in enemy_list:
        en.new_pos(en.differential_pos())


# fonctions d'évaluation
def eval_eatable(distance_eatable, r_eatable, radius):
    """donne un nombre correspondant à l'évaluation d'intéret à aller vers un objet mangeable plutôt qu'un autre"""
    if r_eatable > radius:
        return -1
    return 50 / distance_eatable + r_eatable


def eval_dangerosity(distance_enemy):
    """évalue la dangerositée de rester prêt d'un enemy plus gros que nous"""
    return 50 / distance_enemy
