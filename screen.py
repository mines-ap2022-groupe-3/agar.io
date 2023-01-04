from utilities import round_to
import pygame as pg
from pygame.color import THECOLORS as COLORS
from pygame.math import Vector2 as V2


OVERMAP_BG = COLORS["white"]
BOARD_COLOR = COLORS["grey"]
BACKGROUND_COLOR = COLORS["black"]

TILE_SIZE = 50


class MyScreen:
    def __init__(self, width=1200, height=800, map_width=2400, map_height=1600):
        self.screen = pg.display.set_mode((width, height))
        self.v2_screen = V2(width, height)
        self.v2_map = V2(map_width, map_height)

    def width(self):
        return self.v2_screen[0]

    def height(self):
        return self.v2_screen[1]

    def screen_center(self):
        return self.v2_screen / 2

    def map_width(self):
        return self.v2_map[0]

    def map_height(self):
        return self.v2_map[1]

    def draw_background(self):
        full_screen = pg.Rect(0, 0, self.width(), self.height())
        pg.draw.rect(self.screen, BACKGROUND_COLOR, full_screen)

    def draw_map(self, position, tile_size=TILE_SIZE):
        display_rect = pg.Rect(
            position.x - self.screen_center().x,
            position.y - self.screen_center().y,
            self.width(),
            self.height(),
        )

        first_square_left = int(max(0, round_to(display_rect.left, tile_size)))
        first_square_top = int(max(0, round_to(display_rect.top, tile_size)))

        last_square_right = int(min(self.map_width(), first_square_left + self.width()))
        last_square_bottom = int(
            min(self.map_height(), first_square_top + self.height())
        )

        # Draw verticals lines
        # left = 105
        # right = 745
        # tuile = 50
        for i in range(first_square_left, last_square_right + 1, tile_size):
            pos_i = i - display_rect.x
            pg.draw.line(self.screen, BOARD_COLOR, (pos_i, 0), (pos_i, self.height()))

        # Draw horizontals lines
        for j in range(first_square_top, last_square_bottom + 1, tile_size):
            pos_j = j - display_rect.y
            pg.draw.line(self.screen, BOARD_COLOR, (0, pos_j), (self.width(), pos_j))

    def draw_overmap(self, position):
        display_rect = pg.Rect(
            position.x - self.screen_center().x,
            position.y - self.screen_center().y,
            self.width(),
            self.height(),
        )

        if display_rect.left < 0:
            mask = pg.Rect(0, 0, -display_rect.left, self.height())
            pg.draw.rect(self.screen, OVERMAP_BG, mask)

        if display_rect.top < 0:
            mask = pg.Rect(0, 0, self.width(), -display_rect.top)
            pg.draw.rect(self.screen, OVERMAP_BG, mask)

        if display_rect.right >= self.map_width():
            mask = pg.Rect(
                self.map_width() - display_rect.right + self.width(),
                0,
                self.width(),
                self.height(),
            )
            pg.draw.rect(self.screen, OVERMAP_BG, mask)

        if display_rect.bottom >= self.map_height():
            mask = pg.Rect(
                0,
                self.map_height() - display_rect.bottom + self.height(),
                self.width(),
                self.height(),
            )
            pg.draw.rect(self.screen, OVERMAP_BG, mask)

    def draw_movable(self, movable, player_position):
        """draw movable on screen"""
        center = movable.get_pos() - player_position + self.screen_center()
        pg.draw.circle(self.screen, movable.get_color(), center, movable.get_radius())

    def draw_fruit(self, fruit, player_position):
        """draw fruit"""
        center = fruit.get_pos() - player_position + self.screen_center()
        pg.draw.circle(self.screen, fruit.get_color(), center, fruit.get_radius())

    def display_box(self, x, y, width, message, time_left=-1):
        "Print a message in a box on x, y position"
        fontobject = pg.font.Font(None, 18)
        pg.draw.rect(
            self.screen,
            (0, 0, 0),
            (x + 2, y + 2, width, 20),
            0,
        )
        pg.draw.rect(
            self.screen,
            (255, 255, 255),
            (x, y, width + 4, 24),
            1,
        )

        if len(message) != 0:
            self.screen.blit(
                fontobject.render(message, 1, (255, 255, 255)),
                (x + 2, y + 2),
            )
        pg.display.flip()
