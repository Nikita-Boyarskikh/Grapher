from PyQt5.QtCore import Qt, QRectF, QLineF, QPointF, QMimeData, QPoint
from PyQt5.QtGui import QDrag, QPixmap, QPainter
from PyQt5.QtWidgets import QGraphicsItem, QApplication


class Node(QGraphicsItem):
    radius = 15

    def __init__(self, parent, node, color=None, textColor=None):
        super().__init__(parent)
        self.data = node
        self.color = color
        self.textColor = textColor

        self.setupUi()

    @property
    def diameter(self):
        return self.radius * 2

    def setupUi(self):
        self.setAcceptHoverEvents(True)
        self.setToolTip(self.data.name)
        # BUG: https://bugreports.qt.io/browse/QTBUG-71296
        self.setCursor(Qt.OpenHandCursor)
        self.setAcceptedMouseButtons(Qt.LeftButton)

    def boundingRect(self):
        return QRectF(-self.radius, -self.radius, self.diameter, self.diameter)

    def paint(self, painter, style_option_graphics_item, widget=None):
        if self.color is not None:
            painter.setBrush(self.color)

        if self.textColor is not None:
            painter.setPen(self.textColor)

        rect = QRectF(-self.radius, -self.radius, self.diameter, self.diameter)
        painter.drawEllipse(rect)
        painter.drawText(rect, Qt.AlignCenter, str(self.data.weight))

    def setPos(self, *args):
        if len(args) == 1:
            # QPoint/QPoint
            x, y = args[0].x(), args[0].y()
        else:
            # float, float
            x, y = args

        # handle scene boundaries
        x = max(min(x, (self.scene().width() - self.diameter)), 0)
        y = max(min(y, (self.scene().height() - self.diameter)), 0)

        super().setPos(x, y)

    def mousePressEvent(self, event):
        self.setCursor(Qt.ClosedHandCursor)

    def mouseReleaseEvent(self, event):
        self.setCursor(Qt.OpenHandCursor)

    def paintOnPixmap(self, pixmap):
        painter = QPainter(pixmap)
        painter.translate(self.radius, self.radius)
        painter.setRenderHint(QPainter.Antialiasing)
        self.paint(painter, None, None)
        painter.end()
        return painter

    def drawPixmap(self):
        pixmap = QPixmap(self.diameter, self.diameter)
        pixmap.fill(Qt.white)
        self.paintOnPixmap(pixmap)
        pixmap.setMask(pixmap.createHeuristicMask())
        return pixmap

    def drag(self, widget):
        self.scene().removeItem(self)
        drag = QDrag(widget)
        mime = QMimeData()
        mime.setProperty('node', self.data)
        drag.setMimeData(mime)
        pixmap = self.drawPixmap()
        drag.setPixmap(pixmap)
        drag.setHotSpot(QPoint(self.radius, self.radius))
        drag.exec()

    def mouseMoveEvent(self, event):
        if QLineF(QPointF(event.screenPos()), QPointF(event.buttonDownScreenPos(Qt.LeftButton))).length() < QApplication.startDragDistance():
            return
        self.drag(event.widget())
