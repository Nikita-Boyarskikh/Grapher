import math
import sys
from functools import partial

from PyQt5.QtCore import Qt, QPointF, QRectF, QSizeF
from PyQt5.QtGui import QPainterPath, QFontMetrics, QFont
from PyQt5.QtWidgets import QGraphicsLineItem, QWidget, QApplication

from data import Edge

tr = QApplication.tr


class EdgeItem(QGraphicsLineItem):
    max_curve_angle = math.pi / 4

    def __init__(self, parent: QWidget, edge: Edge, index: int, total: int):
        super().__init__(0, 0, edge.end_node.x - edge.start_node.x, edge.end_node.y - edge.start_node.y, parent)

        self.data = edge
        self.index = index
        self.total = total
        self.center = (self.line().p1() + self.line().p2()) / 2
        self.label = str(self.data.length)

        self.quad_center = self._get_quad_center() if self.index and self.line().length() else None
        self.label_rect = self._get_label_rect()
        self.path = self._get_path()

        self.setToolTip(str(self.data.speed))

    def _get_quad_center(self):
        # WARNING!!! A lot of mathematics!
        # from -max_curve_angle to max_curve_angle (linear inverse depends on curve_coefficient)=
        curve_coefficient = (2 * (self.index % 2) - 1) * ((self.index + 1) // 2)
        angle = self.max_curve_angle * curve_coefficient / (self.total // 2)
        half_line_length = self.line().length() / 2
        center_offset = half_line_length * math.tan(abs(angle))
        center_distance = math.sqrt(half_line_length ** 2 + center_offset ** 2)
        center_angle = -self.line().angle() / 180 * math.pi + math.atan2(center_offset, half_line_length)
        point = QPointF(center_distance * math.cos(center_angle), center_distance * math.sin(center_angle))

        # flip point around center
        if angle // abs(angle) == -1:
            return 2 * self.center - point
        return point

    def _get_path(self):
        path = QPainterPath()
        if not self.line().length():
            return path

        path.moveTo(self.line().p1())
        if self.index:
            path.quadTo(self.quad_center, self.line().p2())
        else:
            path.lineTo(self.line().p2())
        return path

    def _get_label_rect(self):
        font = QFont()
        metrics = QFontMetrics(font)
        height = metrics.height()
        width = metrics.width(self.label)
        return QRectF(self.quad_center or self.center, QSizeF(width, height))

    def paint(self, painter, option, widget=None):
        painter.setPen(Qt.black)
        painter.drawPath(self.path)
        painter.drawText(self.label_rect, self.label)

    def boundingRect(self) -> QRectF:
        rect = super().boundingRect()
        if self.index and self.line().length():
            top = min(self.quad_center.y(), rect.top())
            bottom = max(self.quad_center.y(), rect.bottom())
            left = min(self.quad_center.x(), rect.left())
            right = max(self.quad_center.x(), rect.right())
            rect = QRectF(left, top, right - left, bottom - top)
        return rect

    def shape(self) -> QPainterPath:
        path = QPainterPath(self.path)
        path.addRect(self.label_rect)
        return path
