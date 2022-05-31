import operator
import os
from PIL import Image
import time
import numpy as np
import cv2
import pyautogui
from scipy.spatial import KDTree
from webcolors import hex_to_rgb, CSS3_HEX_TO_NAMES
import consts as c


def convert_rgb_to_names(rgb_tuple: tuple) -> str:
    """
    Gets the color name from rgb.
    Args:
        rgb_tuple: color space for screens.

    Returns:
        The name of the color.
    """
    css3_db = CSS3_HEX_TO_NAMES
    names = []
    rgb_values = []
    for color_hex, color_name in css3_db.items():
        names.append(color_name)
        rgb_values.append(hex_to_rgb(color_hex))
    kdt_db = KDTree(rgb_values)
    distance, index = kdt_db.query(rgb_tuple)
    return names[index]


def marks_up_screenshot() -> list:
    """
    Finds the coordinates of all the corners of the squares in the screenshot.
    Returns:
        The list of coordinates of all corners of squares in the screenshot.
    """
    time.sleep(2)
    screen = pyautogui.screenshot(os.path.join('images', 'screenshot.png'), region=(661, 225, 549, 625))
    img = cv2.imread('images/screenshot.png')
    gray = np.float32(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
    corners = np.int0(cv2.goodFeaturesToTrack(gray, 190, 0.007, 60))
    lst = []
    for corner in corners:
        x, y = corner.ravel()
        cv2.circle(img, (x, y), 4, 255, -1)
        xy = "%d,%d" % (x, y)
        cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                    1.0, (0, 0, 0), thickness=1)
        lst.append([x, y])
    cv2.imwrite('images/Corner.png', img)
    return lst


def get_coord(lst: list) -> tuple[float, float, float]:
    """
    Finds the coordinates of the leftmost point (x, y) and the length from the corner of the square to the center.
    Args:
        lst: A list of all the found coordinates of the corners in the screenshot.

    Returns:
       The x coordinate, the Y coordinate, and the size of half a square.
    """
    lst = sorted(lst)
    list_1 = lst[0:7]
    list2 = sorted(list_1, key=operator.itemgetter(1))
    a = list2[0]
    b = list2[1]
    if b[1] - a[1] <= 5:
        half = (b[0] - a[0]) / 2
    else:
        half = (b[1] - a[1]) / 2
    if half < 0:
        half = (a[0] - b[0]) / 2
        x_origin = a[0] - half
        y_origin = a[1] - half
    else:
        x_origin = a[0]+half
        y_origin = a[1]+half
    print(f'{half=}')
    print(f'coord centre first square: {x_origin=}, {y_origin=}')
    return x_origin, y_origin, half


def get_matrix(x_origin: float, y_origin: float, half: float) -> tuple[list, dict]:
    """
    Starting from the first leftmost upper square, passes through each square,
    recognizing its color and creates a representation of the shape in the form of a matrix.
    Args:
        x_origin: The x-coordinate of the angle for the uppermost left square.
        y_origin: The н-coordinate of the angle for the uppermost left square.
        half:  The size of a half square.

    Returns:
        A matrix consisting of the names of the colors of the squares that displays the shape on the screen, dictionary,
        where the key is the name of the color, the value is a tuple of the coordinates (x, y) of this square.
    """
    img = Image.open('images/screenshot.png')
    x = x_origin
    y = y_origin
    lst_colors_coord = {}
    res = img.getpixel((x, y))
    color = convert_rgb_to_names(res)
    lst_colors_coord[color] = (x, y)
    lst_colors = [color]
    n = 0
    m = 0
    while True:
        x = x + (2.1*half)
        m += 1
        if x >= 549:
            n += 1
            x = x_origin
            y = y + (2*half)
            if y >= 620:
                break
            else:
                m = 0
                res = img.getpixel((x, y))
                color = convert_rgb_to_names(res)
                lst_colors.append(color)
                lst_colors_coord[color] = (x, y)
        else:
            res = img.getpixel((x, y))
            color = convert_rgb_to_names(res)
            lst_colors.append(color)
            lst_colors_coord[color] = (x, y)
    m = m
    n = n
    nev = [lst_colors[i:i+m] for i in range(0, len(lst_colors), m)]
    return nev, lst_colors_coord


def encodes_matrix(matrix_colors: list) -> tuple[list, dict]:
    """
    Turns a list from a list of colors of squares into a matrix of numbers,
    where each color is encoded with a unique digit.
    Args:
        matrix_colors: A list of lists with names of colors for squares.

    Returns:
        Dictionary, where the key is the name of the color, the value is the digit to which the color corresponds.
    """
    matrix_colors = np.array(matrix_colors)
    uniq_colors = set(np.unique(matrix_colors))
    uniq_colors -= {c.GRAY_name, c.BACKGROUND_name}
    dict_colors = {c.GRAY_name: c.GRAY, c.BACKGROUND_name: c.BACKGROUND}
    dict_new = {name: count + 3 for count, name in enumerate(uniq_colors)}
    dict_colors.update(dict_new)
    matrix_new = np.copy(matrix_colors)
    for old, new in dict_colors.items():
        matrix_new[matrix_colors == old] = new
    matrix_new = matrix_new.astype(int)
    return matrix_new, dict_colors


def encodes_dict(lst_colors_coord: list, dict_colors: dict) -> dict:
    """
    Creates a dictionary from the color number and its coordinates.
    Args:
        lst_colors_coord: dictionary, where the key is the name of the color,
        and the value is the coordinates of the color.
        dict_colors: a dictionary where the key is the name of the color
        and the value is a digital representation of the color.

    Returns:
        Dictionary where the key is the color number, the value is the color coordinates.
    """
    result = {}
    for key, value in lst_colors_coord.items():
        if key in dict_colors.keys():
            result[dict_colors[key]] = value
        else:
            result[key] = value
    return result


def get_square_size_color_matrix():
    lst = marks_up_screenshot()
    x_origin, y_origin, half = get_coord(lst)
    nev, lst_colors_coord = get_matrix(x_origin, y_origin, half)
    matrix, dict_colors = encodes_matrix(nev)
    lst_colors_coord = encodes_dict(lst_colors_coord, dict_colors)
    return matrix, lst_colors_coord
