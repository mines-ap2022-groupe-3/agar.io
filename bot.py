from utilities import generate_random_color, clamp
import random
from pygame.math import Vector2 as V2
from fruit import Fruit
from movable import Movable


MAX_BOT_NB = 10


class Bot(Movable):
    def __init__(self, radius=20, v2_screen=V2(1200, 800), v2_map=V2(2400, 1600)):
        xy = V2(random.randint(0, v2_map.x), random.randint(0, v2_map.y))
        color = generate_random_color()
        super().__init__(radius, xy, color, v2_screen)
        Movable.movable_list.append(self)

    # automatic movement
    # préparation des directions
    def is_inside_of_screen(self, pos):
        """renvoie si un objet mangeable (fruit, joueur, ou ennemie) est affiché pour l'objet à position"""
        return (
            abs((pos - self.xy).x) < self.v2_screen.x / 2
            and abs((pos - self.xy).y) < self.v2_screen.y / 2
        )

    def direction_auto(self):
        """fonction qui donne la nouvelle direction"""

        eval_max = 0
        direction = V2(1 - 2 * random.random(), 2 * random.random() - 1).normalize()

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
            if (m.get_pos() - self.xy).length() > 0:
                pos_relative = m.get_pos() - self.xy
            else:
                continue
            distance_enemy = pos_relative.length()
            eval = eval_eatable(distance_enemy, m.get_radius(), self.radius)

            if eval > eval_max:
                eval_max = eval
                direction += pos_relative.normalize()

            elif eval == -1:
                direction -= (
                    eval_dangerosity(distance_enemy, m.get_radius())
                    * pos_relative.normalize()
                )

        if direction.length() > 0:
            return direction.normalize()
        else:
            return V2(0, 0)

    def differential_pos(self):
        """renvoie la différence de position entre deux temps d'horloges"""
        # from a discretized newton 2nd law : ma = force => dr = c*f + previous_dr where force=direction
        diff_position = 0.5 * self.direction_auto() + self.get_dr()

        # limit speed
        length_diff_position = clamp(diff_position.length(), 0, self.speed())
        diff_position = diff_position.normalize() * length_diff_position

        # set the new differential position for next call
        self.set_dr(diff_position)
        return diff_position


# Generate bots
def generate_bot(v2_screen, v2_map):
    bot_list = [mov for mov in Movable.movable_list if isinstance(mov, Bot)]
    for _ in range(len(bot_list), MAX_BOT_NB):
        Bot(v2_screen=v2_screen, v2_map=v2_map)


# fonctions d'évaluation
def eval_eatable(distance_eatable, r_eatable, radius):
    """donne un nombre correspondant à l'évaluation d'intéret à aller vers un objet mangeable plutôt qu'un autre"""
    # if it is approximately our size, we don't consider it
    if r_eatable > radius * 0.9:
        return 0
    # ennemy is dangerous
    elif r_eatable > radius:
        return -1
    return 50 / (distance_eatable + 1) + r_eatable


def eval_dangerosity(distance_enemy, radius_enemy):
    """évalue la dangerositée de rester prêt d'un enemy plus gros que nous"""
    return 10000 / (distance_enemy - radius_enemy) + 100 * radius_enemy
