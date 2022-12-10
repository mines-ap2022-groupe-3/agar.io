from utilities import round_to
import pygame as pg
from pygame.color import THECOLORS as COLORS
from pygame.math import Vector2 as V2


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
BLOB_SIZE_IN = 20


# Drawing functions
def draw_background(screen):
    full_screen = pg.Rect(0, 0, WIDTH, HEIGHT)
    pg.draw.rect(screen, BACKGROUND_COLOR, full_screen)


def draw_map(screen, position, tile_size=TILE_SIZE):
    display_rect = pg.Rect(
        position.x - SCREEN_CENTER.x, position.y - SCREEN_CENTER.y, WIDTH, HEIGHT
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
        pg.draw.line(screen, BOARD_COLOR, (pos_i, 0), (pos_i, HEIGHT))

    # Draw horizontals lines
    for j in range(first_square_top, last_square_bottom + 1, tile_size):
        pos_j = j - display_rect.y
        pg.draw.line(screen, BOARD_COLOR, (0, pos_j), (WIDTH, pos_j))


def draw_overmap(screen, position):
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
