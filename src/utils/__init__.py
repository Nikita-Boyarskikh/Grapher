from typing import List

from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QColor


def throw(exc):
    raise exc


def reverseColor(color: QColor) -> QColor:
    return QColor(255 - color.red(), 255 - color.green(), 255 - color.blue())


def composite_id(*ids: int, delimiter='|') -> str:
    return delimiter.join(map(str, ids))


def build_empty_square_matrix(n: int) -> List[List[List]]:
    """
    :param n: size of matrix
    :return: square matrix (n x n) of lists
    """
    return [[[] for _ in range(0, n)] for _ in range(0, n)]


def bezier(start_point: QPointF, end_point: QPointF, curve_center: QPointF, x: float) -> QPointF:
    """
    Quadratic bezier curve function
    """
    return (1 - x) ** 2 * start_point + 2 * x * (1 - x) * curve_center + x ** 2 * end_point
