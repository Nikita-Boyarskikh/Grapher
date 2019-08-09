from PyQt5.QtCore import QRectF
from PyQt5.QtWidgets import QGraphicsItem


class GraphItem(QGraphicsItem):
    def __init__(self):
        super().__init__()
        self.rect = QRectF()

        self.setFlag(self.ItemHasNoContents)
        self.setAcceptDrops(True)

    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget=None):
        pass

    def setRect(self, *args):
        if len(args) == 1:
            # QRectF
            self.rect = args[0]
        else:
            # w, h
            self.rect = QRectF(*args)

    def dropEvent(self, event):
        node = event.mimeData().property('node')
        if node:
            cursor_position = event.scenePos()
            node.x = cursor_position.x()
            node.y = cursor_position.y()
            self.scene().addNode(node)
