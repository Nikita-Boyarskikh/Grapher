from collections import defaultdict
from functools import partial
from typing import Optional

from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QTransform
from PyQt5.QtWidgets import QGraphicsScene, QApplication

from data import Graph, Node, Result, Edge
from ui.editor.EdgePrompt import EdgePrompt
from ui.editor.NodePrompt import NodePrompt
from ui.editor.edge import EdgeItem
from ui.editor.node import NodeItem
from ui.editor.graph import GraphItem
from ui.editor.result import ResultItem

_ = partial(QApplication.translate, 'Editor')


class GraphScene(QGraphicsScene):
    def __init__(self, parent):
        super().__init__(parent)
        self.reset()

    @property
    def uid(self):
        self.counter += 1
        return self.counter

    def reset(self):
        self.clear()
        self.nodePrompt = None
        self.data = Graph()
        self.graph = GraphItem()
        self.addItem(self.graph)
        self.graph.setRect(self.sceneRect())
        self.counter = 0
        self.edges_matrix = defaultdict(lambda: defaultdict(list))
        self.edges = {}
        self.selected_node = None

    def setData(self, data: Optional[Graph]):
        if data:
            for edge in data.edges:
                self.edges_matrix[edge.start_node.id][edge.end_node.id].append(edge)
            for end_nodes in self.edges_matrix.values():
                for edges in end_nodes.values():
                    for edge in edges:
                        self.addEdge(edge)
            for node in data.nodes:
                self.addNode(node)
            for result in data.results:
                self.addResult(result)
        self.update()

    def iterEdgesByNode(self, node: Node):
        for start_nodes in self.edges_matrix.values():
            for edge in start_nodes[node.id]:
                yield edge
        for edges in self.edges_matrix[node.id].values():
            for edge in edges:
                yield edge

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            item_under_cursor = self.itemAt(event.scenePos(), QTransform())
            if isinstance(item_under_cursor, GraphItem):
                self.showNodePrompt(partial(self.createNode, event.scenePos()))
            elif isinstance(item_under_cursor, NodeItem) and self.selected_node:
                # do not pass release event to node if first node already selected, just create edge between
                self.addEdgeByNode(item_under_cursor.data)
            else:
                super().mouseReleaseEvent(event)
        else:
            super().mouseReleaseEvent(event)

    def setSceneRect(self, *args):
        super().setSceneRect(*args)
        self.graph.setRect(*args)

    def showNodePrompt(self, accept):
        self.nodePrompt = NodePrompt(self.parent(), _('Create node'), accept)
        self.nodePrompt.show()

    def createNode(self, position):
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
        self.nodePrompt = None

        if self.selected_node:
            self.addEdgeByNode(node)

        self.addNode(node)

    def addNode(self, node: Node):
        self.data.nodes.append(node)
        ui_node = NodeItem(self.graph, node)
        self.addItem(ui_node)
        ui_node.setPos(node.x, node.y)
        ui_node.taken.connect(partial(self.on_node_taken, ui_node))
        ui_node.selected.connect(partial(self.on_node_selected, ui_node))

        for edge in self.iterEdgesByNode(node):
            self.addEdge(edge)

    def addEdgeByNode(self, node: Node):
        self.selected_node.isSelected = False
        self.selected_node.update()
        self.showEdgePrompt(partial(self.createEdge, self.selected_node.data, node))
        self.selected_node = None

    def showEdgePrompt(self, accept):
        self.edgePrompt = EdgePrompt(self.parent(), accept)
        self.edgePrompt.show()

    def createEdge(self, start_node: Node, end_node: Node):
        edge = Edge(
            id=self.uid,
            start_node=start_node,
            end_node=end_node,
            length=self.edgePrompt.length,
            speed=self.edgePrompt.speed
        )
        self.edgePrompt = None

        self.addEdge(edge)

    def addEdge(self, edge: Edge):
        # TODO: Fix from end to start edges
        edges_between_these_nodes = self.edges_matrix[edge.start_node.id][edge.end_node.id]
        if edge in edges_between_these_nodes:
            index = edges_between_these_nodes.index(edge)
        else:
            index = len(edges_between_these_nodes)
            edges_between_these_nodes.append(edge)

        curve = (2 * (index % 2) - 1) * ((index + 1) // 2) / len(edges_between_these_nodes)

        self.data.edges.append(edge)
        ui_edge = EdgeItem(self.graph, edge, curve)
        self.addItem(ui_edge)
        ui_edge.setPos(edge.start_node.x, edge.start_node.y)
        self.edges[edge.id] = ui_edge

    def addResult(self, result: Result):
        self.data.results.append(result)
        ui_result = ResultItem(self.graph, result)
        self.addItem(ui_result)
        ui_result.setPos(result.target.x, result.target.y)

    def on_node_taken(self, node: NodeItem):
        for edge in self.iterEdgesByNode(node.data):
            edge_item = self.edges[edge.id]
            self.removeItem(edge_item)

    def on_node_selected(self, node_item: NodeItem, selected: bool):
        if selected:
            self.selected_node = node_item
        else:
            self.selected_node = None
