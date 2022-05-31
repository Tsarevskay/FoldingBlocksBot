import keyboard
import time
import numpy as np
import pyautogui

from tap_start_restart import tap_start_game
from finding_coordinates_and_colors import get_square_size_color_matrix
from solution_algorithm import run
from swipe import select_direction


time.sleep(2)
start = tap_start_game((795, 835, 280, 50))
time.sleep(1)

while True:
    if keyboard.is_pressed('q'):
        break
    pyautogui.moveTo(661, 225)
    matrix, lst_colors_coord = get_square_size_color_matrix()
    matrix_origin = np.array(matrix)
    matrix_origin_copy = matrix_origin.copy()
    con = run(matrix_origin_copy, matrix_origin)
    res = select_direction(con, lst_colors_coord)
    time.sleep(2)
    result_tap = tap_start_game((795, 789, 280, 50))
    time.sleep(1)
