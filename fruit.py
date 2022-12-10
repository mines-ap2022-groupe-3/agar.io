import random
from pygame.math import Vector2 as V2
from utilities import generate_random_color
from screen import M_HEIGHT, M_WIDTH


class Fruit:

    apparition_proba_fruit = 0.10
    max_nb_fruit = 50
    fruit_min_radius = 5
    fruit_max_radius = 12
    fruits_list = []

    def __init__(self):

        self.xy = V2(random.randint(0, M_WIDTH), random.randint(0, M_HEIGHT))
        self.color = generate_random_color()
        self.radius = random.randint(Fruit.fruit_min_radius, Fruit.fruit_max_radius)
        Fruit.fruits_list.append(self)

    def set_pos(self, pos):
        self.xy = pos

    def set_radius(self, radius):
        self.radius = radius

    def set_color(self, color):
        self.color = color

    def get_pos(self):
        return self.xy

    def get_color(self):
        return self.color

    def get_radius(self):
        return self.radius

    def eat_fruit(self, blob_position, blob_size) -> int:
        """si le fruit est assez proche, le mange. Renvoie la nouvelle taille après absorbation d'un ou plusieurs fruits"""
        if (blob_position - self.xy).length() < blob_size:
            # formule pour ajouter à l'air du blob l'air du fruit
            blob_size = (blob_size**2 + self.radius**2) ** (1 / 2)
            del Fruit.fruits_list[Fruit.fruits_list.index(self)]
        return blob_size


def generate_fruit():
    """generate a fruit randomly on screen"""
    if len(Fruit.fruits_list) == 0 or (
        random.random() < Fruit.apparition_proba_fruit
        and len(Fruit.fruits_list) < Fruit.max_nb_fruit
    ):
        Fruit()
