from utilities import clamp, generate_random_color
import random
from screen import M_WIDTH, M_HEIGHT, SCREEN_CENTER, WIDTH, HEIGHT
from pygame.math import Vector2 as V2
import pygame as pg
from fruit import LIST_FRUITS


class enemy:

    speed = 3
    enemy_list = []

    def __init__(
        self,
        radius=20,
    ):
        self.xy = V2(random.randint(0, M_WIDTH), random.randint(0, M_HEIGHT))
        self.color = generate_random_color()
        self.radius = radius
        enemy.enemy_list.append(self)

    def set_pos(self, pos):
        self.xy = pos

    def set_radius(self, radius):
        self.radius = radius

    def get_pos(self):
        return self.xy

    def get_color(self):
        return self.color

    def get_radius(self):
        return self.radius

    def direction(self, player_pos, player_radius):
        """renvoie la direction de déplacement"""
        return direction_auto(self.xy, self.radius, player_pos, player_radius)

    def differential_pos(self, player_pos, player_radius):
        """renvoie la différence de position entre deux temps d'horloges"""
        return self.direction(player_pos, player_radius) * enemy.speed

    def eat_fruit(self):
        """mange les fruits qui sont dans sont rayon"""
        for f in LIST_FRUITS:
            if (self.xy - f.xy).length() < self.radius:
                # formule pour ajouter à l'air de l'ennemie l'air du fruit
                self.set_radius((self.radius**2 + f.radius**2) ** (1 / 2))
                del LIST_FRUITS[LIST_FRUITS.index(f)]

    def eat_enemies(self):
        """mange les enemies qui sont dans sont rayon"""
        list = [en for en in enemy.enemy_list if en != self]
        for en in list:
            if (self.xy - en.xy).length() < self.radius and self.radius >= en.radius:
                # formule pour ajouter à l'air de l'ennemie
                self.set_radius((self.radius**2 + en.radius**2) ** (1 / 2))
                del enemy.enemy_list[enemy.enemy_list.index(en)]


# affichage enemies
def draw_enemies(screen, position):
    """affiche les ennemies"""
    for en in enemy.enemy_list:
        center = en.get_pos() - position + SCREEN_CENTER
        pg.draw.circle(screen, en.get_color(), center, en.get_radius())


# Bouger
def move_enemies(player_pos, player_radius):
    """bouge chaque ennemie un par un"""
    for en in enemy.enemy_list:
        new_pos = en.get_pos() + en.differential_pos(player_pos, player_radius)
        new_pos.x = clamp(new_pos.x, 0, M_WIDTH)
        new_pos.y = clamp(new_pos.y, 0, M_HEIGHT)
        en.set_pos(new_pos)


# Ennemies mange des fruits
def enemies_eat_fruits():
    for en in enemy.enemy_list:
        en.eat_fruit()


# Ennemies mange d'autres ennemies
def enemies_eat_enemies():
    for en in enemy.enemy_list:
        en.eat_enemies()


# player mange enemies
def eat_enemies(position, size) -> int:
    """si l'ennemie' est assez proche, le mange. Renvoie la nouvelle taille après absorbation d'un ou plusieurs ennemies"""
    for en in enemy.enemy_list:
        if (position - en.get_pos()).length() < size:
            # formule pour ajouter à l'air du blob l'air du fruit
            size = (size**2 + en.get_radius() ** 2) ** (1 / 2)
            del enemy.enemy_list[enemy.enemy_list.index(en)]
    return size


def is_inside_of_screen(pos_eatable, position):
    """renvoie si un objet mangeable (fruit, joueur, ou ennemie) est affiché pour l'objet à position"""
    return (
        (pos_eatable - position).x > -WIDTH / 2
        and (pos_eatable - position).x < WIDTH / 2
        and (pos_eatable - position).y > -HEIGHT / 2
        and (pos_eatable - position).y < HEIGHT / 2
    )


def eval_eatable(distance_eatable, r_eatable, radius):
    """donne un nombre correspondant à l'évaluation d'intéret à aller vers un objet mangeable plutôt qu'un autre"""
    if r_eatable > radius:
        return -1
    return 100 / distance_eatable + r_eatable


def eval_dangerosity(distance_enemy):
    """évalue la dangerositée de rester prêt d'un enemy plus gros que nous"""
    return 100 / distance_enemy


def direction_auto(position, radius, player_pos, player_radius):
    """fonction qui donne la nouvelle direction"""

    eval_max = 0
    direction = V2(0, 0)

    # direction des meilleurs fruits
    for f in LIST_FRUITS:
        if not is_inside_of_screen(f.xy, position):
            continue
        pos_fruit_relative = f.xy - position
        distance_fruit = pos_fruit_relative.length()
        eval = eval_eatable(distance_fruit, f.radius, radius)
        if eval > eval_max:
            eval_max = eval
            direction = pos_fruit_relative.normalize()

    # direction des meilleurs ennemies à manger ou fuite
    list = [en for en in enemy.enemy_list if en.get_pos() != position]
    for en in list:
        if not is_inside_of_screen(en.get_pos(), position):
            continue
        pos_enemy_relative = en.get_pos() - position
        distance_enemy = pos_enemy_relative.length()
        eval = eval_eatable(distance_enemy, en.radius, radius)

        if eval > eval_max:
            eval_max = eval
            direction = pos_enemy_relative.normalize()

        elif eval == -1:
            direction -= (
                eval_dangerosity(distance_enemy) * pos_enemy_relative.normalize()
            )

    # direction du joueur si bien à manger ou fuite
    if not is_inside_of_screen(player_pos, position):
        return direction
    pos_player_relative = player_pos - position
    distance_player = pos_player_relative.length()
    eval = eval_eatable(distance_player, player_radius, radius)

    if eval > eval_max:
        eval_max = eval
        direction = pos_player_relative.normalize()

    elif eval == -1:
        direction -= eval_dangerosity(distance_player) * pos_player_relative.normalize()

    direction = direction.normalize()
    return direction
