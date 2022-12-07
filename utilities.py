import random
from math import floor
import pyautogui
import screen as sc

# Utilities
def round_to(n, div):
    return floor(n / div) * div


def clamp(value, min_value, max_value):
    return min(max_value, max(value, min_value))


def generate_random_color():
    return random.randrange(255), random.randrange(255), random.randrange(255)


def take_screenshot(screen):
    myscreen = pyautogui.screenshot(region=(50, 0, sc.WIDTH, sc.HEIGHT))
    myscreen.save("myscreen.jpg")
