#!/usr/bin/env python

import utilities
import screen as sc
import fruit
from screen import MyScreen
import pygame as pg
from pygame.math import Vector2 as V2


def main():
    clock = pg.time.Clock()

    # on initialise pygame et on crée une fenêtre de 800x800 pixels
    pg.init()
    my_screen = MyScreen()

    # On donne un titre à la fenetre
    pg.display.set_caption("agario")

    blob_size = sc.BLOB_SIZE_IN
    color = utilities.generate_random_color()
    speed = 4
    position = V2(sc.MAP) / 2
    SCREEN_CENTER = sc.SCREEN / 2
    MAX_SPEED = 100
  
    class MyScreen:
    def __init__(self, screen):
        self.screen = screen

    def draw_background(self):
        full_screen = pg.Rect(0, 0, WIDTH, HEIGHT)
        pg.draw.rect(self.screen, BACKGROUND_COLOR, full_screen)


    def draw_map(self, position, tile_size=TILE_SIZE):
        display_rect = pg.Rect(
            position.x - self.SCREEN_CENTER.x, position.y - self.SCREEN_CENTER.y, WIDTH, HEIGHT
        )

        first_square_left = int(max(0, round_to(display_rect.left, tile_size)))
        first_square_top = int(max(0, round_to(display_rect.top, tile_size)))

        last_square_right = int(min(M_WIDTH, first_square_left + WIDTH))
        last_square_bottom = int(min(M_HEIGHT, first_square_top + HEIGHT))

    # Draw verticals lines
    # left = 105
    # right = 745
    # tuile = 50
        for i in range(first_square_left, last_square_right + 1, tile_size):
            pos_i = i - display_rect.x
            pg.draw.line(self.screen, BOARD_COLOR, (pos_i, 0), (pos_i, HEIGHT))

    # Draw horizontals lines
        for j in range(first_square_top, last_square_bottom + 1, tile_size):
            pos_j = j - display_rect.y
            pg.draw.line(self.screen, BOARD_COLOR, (0, pos_j), (WIDTH, pos_j))


    def draw_blob(self, screen, size, color=None):
        x, y = self.SCREEN_CENTER
        pg.draw.circle(self.screen, color, (x, y), size)


    def draw_overmap(self, screen, position):
        display_rect = pg.Rect(
            position.x - self.SCREEN_CENTER.x, position.y - self.SCREEN_CENTER.y, WIDTH, HEIGHT
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
    
    def draw_fruits(self, screen, position):
        """affiche les fruits"""
        for f in LIST_FRUITS:
            center = f.xy - position + sc.SCREEN_CENTER
            pg.draw.circle(screen, f.color, center, f.radius)

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

        my_screen = MyScreen(screen)
        my_screen.draw_background(screen)
        my_screen.draw_map(screen, position)
        my_screen.draw_overmap(screen, position)

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
    main()
    # print(round_to(105, 19))






