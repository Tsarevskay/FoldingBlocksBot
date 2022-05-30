import operator
import numpy as np
import consts


def search_max_coord(coord: list, direction: str) -> tuple[int, int]:
    """
    Finds the boundaries of the shape.
    Args:
        coord: The list of coordinates of the shape.
        direction: Swipe direction.

    Returns:
        Coordinates (x, y) of the maximum element of the shape in the matrix, depending on the swipe.
    """
    if direction in ('UP', 'DOWN'):
        max_el = coord[0][0]
    else:
        max_el = coord[0][1]
    min_el = coord[0][0]
    max_coord = 0
    for i in coord:
        if direction == 'RIGHT':
            if i[1] >= max_el:
                max_el = i[1]
                max_coord = i
        if direction == 'UP':
            if i[0] <= min_el:
                min_el = i[0]
                max_coord = i
        if direction == 'DOWN':
            if i[0] >= max_el:
                max_el = i[0]
                max_coord = i
    return max_coord


def reshape_matrix(matrix: np.array, min_c: tuple, max_c: tuple, direction: str) -> np.array:
    """
    Cuts a copy of the matrix to the maximum coordinates.
    Args:
        matrix: The original matrix with the shape.
        min_c: The coordinate (x, y) of the minimum element in the matrix.
        max_c: The coordinate (x, y) of the maximum element in the matrix.
        direction: Swipe direction.

    Returns:
        A new cropped matrix along the maximum edges of the shape, or None if something went wrong.
    """
    if direction in ('RIGHT', 'LEFT'):
        return matrix[:, min_c[1]:max_c[1]+1]
    elif direction in ('UP', 'DOWN'):
        return matrix[min_c[0]:max_c[0]+1, :]
    else:
        return None


def create_0_1_matrix(matrix: np.array, colors: int) -> np.array:
    """
    Encodes the matrix into a matrix with 0 and 1, where 1 is the coordinates of the shape.
    Args:
        matrix: The original matrix with all the shapes.
        colors: The color of the figure.

    Returns:
        A matrix with just the right shape.
    """
    for idx, row in enumerate(matrix):
        for jdx, column in enumerate(row):
            if column == colors:
                matrix[idx][jdx] = 1
            else:
                matrix[idx][jdx] = 0
    matrix = matrix.astype(int)
    # print(f'Matrix 0_1 = {matrix}')
    return matrix


def finds_max_left_point(lst_coord: list) -> tuple[int, int]:
    """
    Finds the leftmost coordinate of the shape.
    Args:
        lst_coord: A list of all the coordinates of the shape in the matrix.

    Returns:
        The x, y coordinates of the leftmost point of the figure.
    """
    min_x = min(lst_coord, key=operator.itemgetter(1))[1]
    min_y = min(lst_coord, key=operator.itemgetter(0))[0]
    return min_y, min_x


def swipe_to(direction: str, matrix: np.array, max_left_coord: tuple[int, int]) -> list:
    """
    Makes a swipe of a shape in a given direction in the matrix.
    Args:
        direction: Swipe direction.
        matrix: A matrix of 0 and 1.
        max_left_coord: Coordinates of the leftmost point of the figure.

    Returns:
        Coordinates of new points in the matrix after the swipe.
    """
    x_len = len(matrix[0])
    y_len = len(matrix)
    coord = []
    for idx, row in enumerate(matrix):
        for jdx, column in enumerate(row):
            if column == 1:
                if direction == 'LEFT':
                    coord.append((jdx - x_len + max_left_coord[1], idx))
                if direction == 'RIGHT':
                    coord.append((jdx + x_len + max_left_coord[1], idx))
                if direction == 'UP':
                    coord.append((jdx, idx - y_len + max_left_coord[0]))
                if direction == 'DOWN':
                    coord.append((jdx, idx + y_len + max_left_coord[0]))
    return coord


def search_figure(direction: str, origin_matrix: np.array, colors: int) -> tuple[tuple, np.array, np.array, np.array]:
    """
    By the transmitted color, it searches for the coordinates of the shape in the matrix and swipes in the right direction.
    Args:
        direction: Swipe direction.
        origin_matrix: The original matrix with all the shapes.
        colors: The color of the shape we are looking for.

    Returns:
        The coordinates of the shape after the swipe, the matrix with the inverted shape, the original matrix,
        the cropped matrix on the shape.
    """
    matrix_copy = np.copy(origin_matrix)
    matrix_0_1 = create_0_1_matrix(matrix_copy, colors)
    lst_coord = list(zip(*np.where(matrix_0_1)))
    max_left_coord = finds_max_left_point(lst_coord)
    if direction in ('RIGHT', 'LEFT'):
        max_coord = search_max_coord(lst_coord, 'RIGHT')
        reshape_new_matrix = reshape_matrix(matrix_0_1, max_left_coord, max_coord, direction)
        matrix_flip = np.flip(reshape_new_matrix, 1)
    elif direction in ('UP', 'DOWN'):
        min_coord = search_max_coord(lst_coord, 'UP')
        max_coord = search_max_coord(lst_coord, 'DOWN')
        # print(f'{min_coord=}, {max_coord=}')
        reshape_new_matrix = reshape_matrix(matrix_copy, min_coord, max_coord, direction)
        matrix_flip = np.flip(reshape_new_matrix, 0)
    else:
        matrix_flip = None
        reshape_new_matrix = None
    # print(f'Reshape new matrix = {reshape_new_matrix}')
    # print(f'Swipe matrix_1 {matrix_flip}')
    coord = swipe_to(direction, matrix_flip, max_left_coord)
    return coord, matrix_flip, matrix_copy, reshape_new_matrix


def is_cheek_len(coord: list, matrix: np.array) -> tuple[bool, np.array]:
    """
    Checks whether the shape has gone beyond the boundaries of the matrix after the swipe.
    Args:
        coord: Coordinates of the shape after the swipe.
        matrix: A matrix of 0 and 1.

    Returns:
        True if the shape did not go beyond the boundaries of the matrix after the swipe, otherwise False.
        A new matrix after the shape swipe.
    """
    for i in coord:
        if i[0] < 0:
            # print(f"вышел за границу x слева")
            return False, matrix
        elif i[0] > len(matrix[0])-1:
            # print(f"вышел за границу x справа")
            return False, matrix
        elif i[1] < 0:
            # print(f"вышел за границу y сверху")
            return False, matrix
        elif i[1] > len(matrix)-1:
            # print(f"вышел за границу y снизу")
            return False, matrix
        else:
            matrix[i[1]][i[0]] = 1
    matrix = matrix.astype(int)
    # print(f'New matrix = {matrix}')
    return True, matrix


def is_cheek_colors(matrix: np.array, coord: list) -> bool:
    """
    Checks which color the new coordinates of the shape hit after the swipe.
    Args:
        matrix: The original matrix with all the shapes.
        coord: Coordinates of the shape after the swipe.

    Returns:
        True if the shape can be rotated in this direction, otherwise False.
    """
    result = []
    for i in coord:
        if matrix[i[1]][i[0]] == consts.GRAY:
            result.append(1)
        else:
            result.append(0)
    if set(result) == {1}:
        return True
    else:
        return False


def paints_over(matrix: np.array, num_color: int, coord: list) -> np.array:
    """
    Updates the original matrix, filling in the coordinates with the desired color after a successful swipe.
    Args:
        matrix:  The original matrix with all the shapes.
        num_color: The number of the shape color.
        coord: Coordinates of the shape after the swipe.

    Returns:
        Updated matrix.
    """
    for i in coord:
        matrix[i[1]][i[0]] = num_color
    return matrix


def move_to(matrix: np.array, num_color: int, direction: str, matrix_origin: np.array) -> np.array:
    """
    Checks whether it is possible to swipe the shape in a given direction.
    Args:
        matrix: A copy of the original matrix.
        num_color: The number of the shape color.
        direction: Swipe direction.
        matrix_origin: The original matrix with all the shapes.

    Returns:
        A new matrix, if the swipe can be done, otherwise None.
    """
    coord_swipe, matrix_swipe, copy_matrix, reshape_new_matrix = search_figure(direction, matrix_origin, num_color)
    res_len, final_matrix = is_cheek_len(coord_swipe, copy_matrix)
    if res_len:
        res_color = is_cheek_colors(matrix_origin, coord_swipe)
        if res_color:
            return paints_over(matrix_origin, num_color, coord_swipe)
    else:
        return None


def rec(matrix, color, matrix_origin, condition):
    uniq_direction = ['LEFT', 'RIGHT', 'UP', 'DOWN']
    matrix = np.array(matrix)
    condition = condition
    matr_cont = []
    n_dir = 0

    for direction in uniq_direction:
        if (consts.GRAY not in set(np.unique(matr_cont))) and (matr_cont != []):
            return "WIN", condition, matr_cont
        # print(f'{n_dir=}')
        # print(f'{direction=}')
        if n_dir >= 4:
            n_dir = 0
            return None, condition, matr_cont
        else:
            matrix_res = move_to(matrix, color, direction, matrix_origin)
            print(matrix_res)
            if matrix_res is None:
                n_dir += 1
            else:
                condition += [{color: direction}, matrix_res]
                matr_cont = matrix_res
    if (consts.GRAY not in set(np.unique(matr_cont))) and (matr_cont != []):
        return "WIN", condition, matr_cont
    if n_dir == 4:
        return 'Change color', condition, matr_cont
    if n_dir < 4:
        n_dir = 0
    res, condition, matr_cont = rec(matr_cont, color, matrix_origin, condition)
    if res == 'WIN' or res == 'Change color':
        return res, condition, matr_cont


def run(matrix_origin_copy: np.array, matrix_origin: np.array) -> list:
    """
    Finds the direction of swipes for all colors to pass the level
    Args:
        matrix_origin_copy: A copy of the original matrix.
        matrix_origin: The original matrix with all the shapes.

    Returns:
        List of tuples. A tuple consists of dictionaries and a matrix. The dictionary contains the color of the shape
        and the direction of the swipe, the matrix stores the state of the step.
    """
    condition = []
    matrix_origin_copy = np.array(matrix_origin_copy)
    matrix_origin = np.array(matrix_origin)
    uniq_colors = set(np.unique(matrix_origin_copy))
    uniq_colors -= {consts.GRAY, consts.BACKGROUND}
    uniq_colors = list(uniq_colors)
    for color in uniq_colors:
        res, condition, matr_cont = rec(matrix_origin_copy, color, matrix_origin, condition)
        condition = condition
        if res == 'WIN':
            print('win')
            break
        else:
            matrix_origin_copy = matr_cont.copy()
    return condition
