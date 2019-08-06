from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsScene

from data import Graph, Node
from ui.editor.NodePrompt import NodePrompt
from ui.editor.node import Node as UiNode
from ui.editor.graph import Graph as GraphItem


class GraphScene(QGraphicsScene):
    def __init__(self, parent):
        super().__init__(parent)
        self.data = Graph()
        self.graph = GraphItem()
        self.addItem(self.graph)
        self.counter = 0

    @property
    def uid(self):
        self.counter += 1
        return self.counter

    def addNode(self, node):
        ui_node = UiNode(None, node, QColor(100, 100, 100), QColor('white'))
        self.addItem(ui_node)
        ui_node.setPos(node.x, node.y)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            NodePrompt().show(self.parent(), self.accept, self.reject)
            cursor_position = event.scenePos()
            node = Node(self.uid, '', cursor_position.x(), cursor_position.y(), 1)
            self.addNode(node)
        else:
            super().mouseReleaseEvent(event)

    def setSceneRect(self, *args):
        super().setSceneRect(*args)
        self.graph.setRect(*args)

    def accept(self):
        print('accept')

    def reject(self):
        print('reject')
