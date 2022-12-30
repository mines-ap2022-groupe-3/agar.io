import utilities
import screen as sc
import fruit
import pygame as pg
from pygame.math import Vector2 as V2
import random
import numpy as np
from collections import namedtuple
from collections import defaultdict
from pygame.color import THECOLORS as COLORS

OVERMAP_BG = COLORS["white"]
BOARD_COLOR = COLORS["grey"]
BACKGROUND_COLOR = COLORS["black"]

SCREEN = V2(1200, 800)
WIDTH, HEIGHT = SCREEN
SCREEN_CENTER = SCREEN / 2

TILE_SIZE = 50

MAP = 2 * SCREEN
M_WIDTH, M_HEIGHT = MAP

MAX_SPEED = 100

PROBA_APPARITION_FRUIT = 0.05
NB_MAX_FRUIT = 40
RAYON_FRUIT_MIN = 5
RAYON_FRUIT_MAX = 12

BLOB_SIZE_IN = 20


class Utilities:
    def __init__(self) -> None:
        pass

    def round_to(self, n, div):
        return np.floor(n / div) * div

    def clamp(self, value, min_value, max_value):
        return min(max_value, max(value, min_value))

    def couleur_debut(self):
        SCREEN2 = V2(400, 400)
        pg.display.set_mode(SCREEN2)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            # un type de pg.KEYDOWN signifie que l'on a appuyé une touche du clavier
            elif event.type == pg.KEYDOWN:
                # si la touche est "Q" ou "escape" on veut quitter le programme
                if event.key == pg.K_q or event.key == pg.K_ESCAPE:
                    done = True
                elif event.key == pg.K_b:
                    return COLORS["blue"]
                elif event.key == pg.K_r:
                    return COLORS["red"]
                elif event.key == pg.K_y:
                    return COLORS["yellow"]

    def generate_random_color(self):
        return random.randrange(255), random.randrange(255), random.randrange(255)


class Drawing_functions:
    # Drawing functions

    def __init__(self) -> None:
        pass

    def draw_background(self, screen):
        full_screen = pg.Rect(0, 0, WIDTH, HEIGHT)
        pg.draw.rect(screen, BACKGROUND_COLOR, full_screen)

    def draw_map(self, screen, position, tile_size=TILE_SIZE):
        display_rect = pg.Rect(
            position.x - SCREEN_CENTER.x, position.y - SCREEN_CENTER.y, WIDTH, HEIGHT
        )

        first_square_left = int(
            max(0, Utilities.round_to(display_rect.left, tile_size))
        )
        first_square_top = int(max(0, Utilities.round_to(display_rect.top, tile_size)))

        last_square_right = int(min(M_WIDTH, first_square_left + WIDTH))
        last_square_bottom = int(min(M_HEIGHT, first_square_top + HEIGHT))

        # Draw verticals lines
        # left = 105
        # right = 745
        # tuile = 50
        for i in range(first_square_left, last_square_right + 1, tile_size):
            pos_i = i - display_rect.x
            pg.draw.line(screen, BOARD_COLOR, (pos_i, 0), (pos_i, HEIGHT))

        # Draw horizontals lines
        for j in range(first_square_top, last_square_bottom + 1, tile_size):
            pos_j = j - display_rect.y
            pg.draw.line(screen, BOARD_COLOR, (0, pos_j), (WIDTH, pos_j))

    def draw_blob(self, screen, size, color=None):
        x, y = SCREEN_CENTER
        pg.draw.circle(screen, color, (x, y), size)

    def draw_overmap(self, screen, position):
        display_rect = pg.Rect(
            position.x - SCREEN_CENTER.x, position.y - SCREEN_CENTER.y, WIDTH, HEIGHT
        )

        if display_rect.left < 0:
            mask = pg.Rect(0, 0, -display_rect.left, HEIGHT)
            pg.draw.rect(screen, OVERMAP_BG, mask)

        if display_rect.top < 0:
            mask = pg.Rect(0, 0, WIDTH, -display_rect.top)
            pg.draw.rect(screen, OVERMAP_BG, mask)

        if display_rect.right >= M_WIDTH:
            mask = pg.Rect(M_WIDTH - display_rect.right + WIDTH, 0, WIDTH, HEIGHT)
            pg.draw.rect(screen, OVERMAP_BG, mask)

        if display_rect.bottom >= M_HEIGHT:
            mask = pg.Rect(0, M_HEIGHT - display_rect.bottom + HEIGHT, WIDTH, HEIGHT)
            pg.draw.rect(screen, OVERMAP_BG, mask)


# Fruit = namedtuple("Fruit", ["xy", "color", "radius"])
# LIST_FRUITS = [    ]


class Fruits:
    # génération fruit
    def __init__(self, Fruit, LIST_FRUITS) -> None:
        self.fruit = Fruit
        self.LIST_FRUITS = LIST_FRUITS

    def generate_random_fruit_position(self):
        """génère une position aléatoire"""
        x, y = random.randint(0, M_WIDTH), random.randint(0, M_HEIGHT)
        return V2(x, y)

    def generate_random_fruit_radius(self):
        """génère un rayon aléatoire entre RAYON_FRUIT_MIN et RAYON_FRUIT_MAX"""
        r = random.randint(RAYON_FRUIT_MIN, RAYON_FRUIT_MAX)
        return r

    def generate_fruit(self):
        """génère un fruit aléatoirement sur le screen"""
        if len(self.LIST_FRUITS) == 0 or (
            random.random() < PROBA_APPARITION_FRUIT
            and len(self.LIST_FRUITS) < NB_MAX_FRUIT
        ):
            xy = Fruits.generate_random_fruit_position()
            color = Utilities.generate_random_color()
            radius = Fruits.generate_random_fruit_radius()
            self.LIST_FRUITS.append(self.Fruit(xy, color, radius))

    # affichage fruits

    def draw_fruits(self, screen, position):
        """affiche les fruits"""
        for f in self.LIST_FRUITS:
            center = f.xy - position + SCREEN_CENTER
            pg.draw.circle(screen, f.color, center, f.radius)

    # Manger fruit

    def eat_fruit(self, position, size) -> int:
        """si le fruit est assez proche, le mange. Renvoie la nouvelle taille après absorbation d'un ou plusieurs fruits"""
        for f in self.LIST_FRUITS:
            if (position - f.xy).length() < size:
                # formule pour ajouter à l'air du blob l'air du fruit
                size = (size**3 + f.radius**3) ** (1 / 3)
                del self.LIST_FRUITS[self.LIST_FRUITS.index(f)]
        return size


class Game:
    def __init__(self) -> None:
        pass

    def main():
        clock = pg.time.Clock()

        # on initialise pygame et on crée une fenêtre de 800x800 pixels
        pg.init()
        screen = pg.display.set_mode((sc.WIDTH, sc.HEIGHT))

        # On donne un titre à la fenetre
        pg.display.set_caption("agario")

        blob_size = sc.BLOB_SIZE_IN
        color = utilities.generate_random_color()
        speed = 4
        position = V2(sc.MAP) / 2
        SCREEN_CENTER = sc.SCREEN / 2
        MAX_SPEED = 100

        # La boucle du jeu
        done = False
        while not done:
            # FPS
            clock.tick(60)

            # On trouve la nouvelle direction/position
            new_direction = V2(pg.mouse.get_pos()) - V2(SCREEN_CENTER)
            if new_direction.magnitude() >= MAX_SPEED:
                new_direction = new_direction.normalize()
            else:
                new_direction = new_direction / MAX_SPEED

            position += new_direction * speed

            pg.display.set_caption(f"agario - {position.x=:5.0f} - {position.y=:5.0f}")

            # On s'assure que la position ne sorte pas de la map
            position.x = utilities.clamp(position.x, 0, sc.M_WIDTH)
            position.y = utilities.clamp(position.y, 0, sc.M_HEIGHT)

            sc.draw_background(screen)
            sc.draw_map(screen, position)
            sc.draw_overmap(screen, position)

            fruit.generate_fruit()
            blob_size = fruit.eat_fruit(position, size=blob_size)
            fruit.draw_fruits(screen, position)
            sc.draw_blob(screen, size=blob_size, color=color)

            pg.display.update()

            # on itère sur tous les évênements qui ont eu lieu depuis le précédent appel
            # ici donc tous les évènements survenus durant la seconde précédente
            for event in pg.event.get():
                # chaque évênement à un type qui décrit la nature de l'évênement
                # un type de pg.QUIT signifie que l'on a cliqué sur la "croix" de la fenêtre
                if event.type == pg.QUIT:
                    done = True
                # un type de pg.KEYDOWN signifie que l'on a appuyé une touche du clavier
                elif event.type == pg.KEYDOWN:
                    # si la touche est "Q" ou "escape" on veut quitter le programme
                    if event.key == pg.K_q or event.key == pg.K_ESCAPE:
                        done = True

        pg.quit()


# if python says run, then we should run
if __name__ == "__main__":
    Game.main()
    # print(round_to(105, 19))
