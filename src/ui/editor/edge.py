import math
from functools import partial

from PyQt5.QtCore import Qt, QLineF, QPointF
from PyQt5.QtGui import QPainterPath
from PyQt5.QtWidgets import QGraphicsLineItem, QWidget, QApplication

from data import Edge

_ = partial(QApplication.translate, 'Edge')


class EdgeItem(QGraphicsLineItem):
    def __init__(self, parent: QWidget, edge: Edge, curve: float):
        super().__init__(0, 0, edge.end_node.x - edge.start_node.x, edge.end_node.y - edge.start_node.y, parent)
        self.data = edge
        self.curve_coefficient = curve
        self.setToolTip(str(self.data.speed))

    @property
    def center(self):
        return (self.line().p1() + self.line().p2()) / 2

    @property
    def quad_center(self):
        # from -45 to 45 (linear inverse depends on curve_coefficient)
        angle = math.pi / 4 * self.curve_coefficient
        center_distance = QLineF(self.line().p2(), self.center).length()
        center_offset = center_distance * math.tan(1 / angle)
        a = self.line().p2().x() / self.line().p2().y()
        x = center_offset / math.sqrt(1 + a**2)
        y = center_offset * a / math.sqrt(1 + a**2)
        return QPointF(x, y)

    def paint(self, painter, option, widget=None):
        path = QPainterPath()
        path.moveTo(self.line().p1())
        if self.curve_coefficient:
            quad_center = self.quad_center
            path.quadTo(quad_center, self.line().p2())
        else:
            path.lineTo(self.line().p2())
        painter.drawPath(path)

        painter.setPen(Qt.black)
        painter.drawText(self.center, str(self.data.length))
