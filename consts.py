from enum import Enum

GRAY_name = 'darkgray'
BACKGROUND_name = 'antiquewhite'
GRAY = 1
BACKGROUND = 2


class Directions(str, Enum):
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    UP = 'UP'
    DOWN = 'DOWN'
