from functools import partial

from PyQt5.QtCore import Qt, QRectF, QLineF, QMimeData, QPoint, pyqtSignal, QMetaObject, QCoreApplication
from PyQt5.QtGui import QDrag, QPixmap, QPainter, QPen, QPainterPath
from PyQt5.QtWidgets import QApplication, QGraphicsObject

from data import Node
from ui.editor import NodePrompt

tr = QApplication.tr


class NodeItem(QGraphicsObject):
    taken = pyqtSignal()
    selected = pyqtSignal(bool)
    radius = 15
    borderWidth = 5
    labelHeight = 20

    def __init__(self, parent, node: Node):
        super().__init__(parent)
        self.data = node
        self.prompt = None
        self.isSelected = False
        self.isTaken = False

        self.ellipse_rect = QRectF(-self.radius, -self.radius, self.diameter, self.diameter)
        self.setupUi()

    @property
    def diameter(self):
        return self.radius * 2

    def setupUi(self):
        self.setToolTip(self.data.name)
        # BUG: https://bugreports.qt.io/browse/QTBUG-71296
        self.setCursor(Qt.OpenHandCursor)
        self.setAcceptedMouseButtons(Qt.LeftButton | Qt.RightButton)
        QMetaObject.connectSlotsByName(self.parent())

    def boundingRect(self):
        return QRectF(
            -self.radius - self.borderWidth / 2,
            -self.radius - self.labelHeight,
            self.diameter + self.borderWidth,
            self.diameter + self.labelHeight
        )

    def shape(self) -> QPainterPath:
        path = QPainterPath()
        path.addEllipse(self.ellipse_rect)
        return path

    def paint(self, painter, style_option_graphics_item, widget=None):
        if self.data.color is not None:
            painter.setBrush(self.data.color)

        if self.isSelected and self.data.textColor:
            painter.setPen(QPen(self.data.textColor, self.borderWidth))

        painter.drawEllipse(self.ellipse_rect)

        if self.data.textColor is not None:
            painter.setPen(self.data.textColor)
        painter.drawText(self.ellipse_rect, Qt.AlignCenter, str(self.data.id))

        painter.setPen(Qt.black)
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

    def select(self, selected):
        if self.isSelected != selected:
            self.isSelected = selected
            self.selected.emit(selected)
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setCursor(Qt.OpenHandCursor)
            if not self.isTaken:
                self.select(not self.isSelected)
        elif event.button() == Qt.RightButton:
            self.prompt = NodePrompt(
                parent=self.parentWidget(),
                title=tr('Edit node'),
                accept=self.accept,
                name=self.data.name,
                weight=self.data.weight,
                color=self.data.color,
                textColor=self.data.textColor
            )
            self.prompt.show()
        else:
            super().mouseReleaseEvent(event)

    def accept(self):
        self.data.name = self.prompt.name
        self.data.weight = self.prompt.weight
        self.data.color = self.prompt.color
        self.data.textColor = self.prompt.textColor
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
        self.isTaken = False

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

        self.isTaken = True
        self.select(False)
        self.taken.emit()
        self.drag(event.widget())
