from PyQt5.QtCore import Qt, QRectF, QLineF, QMimeData, QPoint
from PyQt5.QtGui import QDrag, QPixmap, QPainter
from PyQt5.QtWidgets import QGraphicsItem, QApplication

from ui.editor import NodePrompt


class Node(QGraphicsItem):
    radius = 15
    labelHeight = 20

    def __init__(self, parent, node):
        super().__init__(parent)
        self.data = node
        self.nodePrompt = None

        self.setupUi()

    @property
    def diameter(self):
        return self.radius * 2

    def setupUi(self):
        self.setToolTip(self.data.name)
        # BUG: https://bugreports.qt.io/browse/QTBUG-71296
        self.setCursor(Qt.OpenHandCursor)
        self.setAcceptedMouseButtons(Qt.LeftButton | Qt.RightButton)

    def boundingRect(self):
        return QRectF(-self.radius, -self.radius - self.labelHeight, self.diameter, self.diameter + self.labelHeight)

    def paint(self, painter, style_option_graphics_item, widget=None):
        if self.data.color is not None:
            painter.setBrush(self.data.color)

        if self.data.textColor is not None:
            painter.setPen(self.data.textColor)

        ellipse_rect = QRectF(-self.radius, -self.radius, self.diameter, self.diameter)
        painter.drawEllipse(ellipse_rect)
        painter.drawText(ellipse_rect, Qt.AlignCenter, str(self.data.id))

        if self.data.color is not None:
            painter.setPen(self.data.color)

        painter.drawText(
            -self.radius,
            -self.radius - self.labelHeight,
            self.diameter,
            self.labelHeight,
            Qt.AlignHCenter,
            str(self.data.weight)
        )

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
        if event.button() == Qt.LeftButton:
            self.setCursor(Qt.ClosedHandCursor)
        elif event.button() == Qt.RightButton:
            pass
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setCursor(Qt.OpenHandCursor)
        elif event.button() == Qt.RightButton:
            self.nodePrompt = NodePrompt(
                parent=self.parentWidget(),
                accept=self.accept,
                name=self.data.name,
                weight=self.data.weight,
                color=self.data.color,
                textColor=self.data.textColor
            )
            self.nodePrompt.show()
        else:
            super().mouseReleaseEvent(event)

    def accept(self):
        self.data.name = self.nodePrompt.name
        self.data.weight = self.nodePrompt.weight
        self.data.color = self.nodePrompt.color
        self.data.textColor = self.nodePrompt.textColor
        self.update()

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
        drag_distance = QLineF(event.screenPos(), event.buttonDownScreenPos(Qt.LeftButton)).length()
        if drag_distance < QApplication.startDragDistance():
            return
        self.drag(event.widget())
