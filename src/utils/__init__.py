from PyQt5.QtGui import QColor


def throw(exc):
    raise exc


def find(arr: list, expr, default=None):
    return next((el for el in arr if expr(el)), default)


def reverseColor(color: QColor) -> QColor:
    return QColor(255 - color.red(), 255 - color.green(), 255 - color.blue())
