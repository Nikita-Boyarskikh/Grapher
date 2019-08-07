from functools import partial
from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsScene, QApplication

from data import Graph, Node
from ui.editor.NodePrompt import NodePrompt
from ui.editor.node import Node as UiNode
from ui.editor.graph import Graph as GraphItem

_ = partial(QApplication.translate, 'Editor')


class GraphScene(QGraphicsScene):
    def __init__(self, parent):
        super().__init__(parent)
        self.nodePrompt = None
        self.data = Graph()
        self.graph = GraphItem()
        self.addItem(self.graph)
        self.counter = 0

    def reset(self):
        self.clear()
        self.nodePrompt = None
        self.data = Graph()
        self.graph = GraphItem()
        self.addItem(self.graph)
        self.counter = 0

    def setData(self, data: Optional[Graph]):
        if data:
            for node in data.nodes:
                self.addNode(node)
            for edge in data.edges:
                self.addEdge(edge)
            for result in data.results:
                self.addResult(result)
        self.update()

    @property
    def uid(self):
        self.counter += 1
        return self.counter

    def addNode(self, node):
        self.data.nodes.append(node)
        ui_node = UiNode(self.graph, node)
        self.addItem(ui_node)
        ui_node.setPos(node.x, node.y)

    def addEdge(self, edge):
        self.data.edges.append(edge)
        # TODO

    def addResult(self, result):
        self.data.results.append(result)
        # TODO

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.nodePrompt = NodePrompt(self.parent(), partial(self.accept, event.scenePos()))
            self.nodePrompt.show()
        else:
            super().mouseReleaseEvent(event)

    def setSceneRect(self, *args):
        super().setSceneRect(*args)
        self.graph.setRect(*args)

    def accept(self, position):
        node_id = self.uid
        node = Node(
            id=node_id,
            name=self.nodePrompt.name or _('Node {}').format(node_id),
            x=position.x(),
            y=position.y(),
            weight=self.nodePrompt.weight,
            color=self.nodePrompt.color,
            textColor=self.nodePrompt.textColor
        )
        self.addNode(node)
