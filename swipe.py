import pyautogui
from consts import Directions


def swipe_left(start_x, start_y):
    pyautogui.moveTo(661+start_x, 225+start_y)
    pyautogui.dragTo(x=661+start_x-100, y=225+start_y, duration=2, button='left')


def swipe_right(start_x, start_y):
    pyautogui.moveTo(661+start_x, 225+start_y)
    pyautogui.dragTo(x=661+start_x+100, y=225+start_y, duration=2, button='left')


def swipe_up(start_x, start_y):
    pyautogui.moveTo(661+start_x, 225+start_y)
    pyautogui.dragTo(x=661+start_x, y=225+start_y-100, duration=2, button='left')


def swipe_down(start_x, start_y):
    pyautogui.moveTo(661+start_x, 225+start_y)
    pyautogui.dragTo(x=661+start_x, y=225+start_y+100, duration=2, button='left')


def select_direction(condition: list, colors_coord: dict) -> bool:
    """
    Makes a swipe in the right direction.
    Args:
        condition: List of directions for swipe.
        colors_coord: The x and y coordinates from where to start the swipe.

    Returns:
        True when all swipes are completed.
    """
    for i in condition[::2]:
        direction = list(i.values())[0]
        coord = colors_coord[list(i.keys())[0]]
        print(direction, coord[0], coord[1])
        if direction == Directions.RIGHT:
            swipe_right(coord[0], coord[1])
        if direction == Directions.LEFT:
            swipe_left(coord[0], coord[1])
        if direction == Directions.DOWN:
            swipe_down(coord[0], coord[1])
        if direction == Directions.UP:
            swipe_up(coord[0], coord[1])
    return True
