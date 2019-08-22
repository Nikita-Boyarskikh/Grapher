import math
from collections import defaultdict
from functools import partial
from typing import Optional, Iterable

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
from utils import composite_id, bezier

tr = partial(QApplication.translate, '@default')


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
        self.moving_edges = []
        self.selected_node = None

    def setData(self, data: Optional[Graph]):
        if data:
            for edge in data.edges.values():
                self.addEdge(edge)
            for node in data.nodes.values():
                self.addNode(node)
            for result in data.results:
                self.addResult(result)
        self.update()

    def iterEdgesByNode(self, node: Node) -> Iterable[Edge]:
        for edges in self.edges_matrix[node.id].values():
            for edge in edges:
                yield edge

    def iterEdgesByNodes(self, start_node: Node, end_node: Node) -> Iterable[Edge]:
        for edge in self.edges_matrix[start_node.id][end_node.id]:
            yield edge

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            item_under_cursor = self.itemAt(event.scenePos(), QTransform())
            if isinstance(item_under_cursor, GraphItem):
                self.showNodePrompt(partial(self.createNode, event.scenePos()))
            elif isinstance(item_under_cursor, NodeItem) and self.selected_node:
                # do not pass release event to node if first node already selected, just create edge between
                if item_under_cursor == self.selected_node:
                    self.selected_node.isSelected = False
                    self.selected_node.update()
                    self.selected_node = None
                else:
                    self.addEdgeByNode(item_under_cursor.data)
            else:
                super().mouseReleaseEvent(event)
        else:
            super().mouseReleaseEvent(event)

    def setSceneRect(self, *args):
        super().setSceneRect(*args)
        self.graph.setRect(*args)

    def showNodePrompt(self, accept):
        self.nodePrompt = NodePrompt(self.parent(), tr('Create node'), accept)
        self.nodePrompt.show()

    def createNode(self, position):
        node_id = self.uid
        node = Node(
            id=node_id,
            name=self.nodePrompt.name or tr('Node {}').format(node_id),
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
        self.data.nodes[node.id] = node
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
        index = len(self.edges_matrix[start_node.id][end_node.id])
        edge = Edge(
            id=composite_id(start_node.id, end_node.id, index),
            start_node=start_node,
            end_node=end_node,
            length=self.edgePrompt.length,
            speed=self.edgePrompt.speed
        )
        self.edgePrompt = None

        self.addEdge(edge)

    def addEdge(self, edge: Edge):
        edges_between_these_nodes = self.edges_matrix[edge.start_node.id][edge.end_node.id]
        total = len(edges_between_these_nodes)
        if edge not in edges_between_these_nodes:
            total += 1

        # Recreate edges with new total
        for i, edge_between_these_nodes in enumerate(edges_between_these_nodes):
            edge_item = self.edges[edge_between_these_nodes.id]
            self.removeItem(edge_item)
            self.addEdgeItem(edge_between_these_nodes, i, total)

        # Get new index
        if edge in edges_between_these_nodes:
            index = edges_between_these_nodes.index(edge)
        else:
            index = len(edges_between_these_nodes)
            self.edges_matrix[edge.start_node.id][edge.end_node.id].append(edge)
            self.edges_matrix[edge.end_node.id][edge.start_node.id].append(edge)

        # Create edge
        self.data.edges[edge.id] = edge
        self.addEdgeItem(edge, index, total)

    def addEdgeItem(self, edge: Edge, index: int, total: int):
        ui_edge = EdgeItem(self.graph, edge, index, total)
        self.addItem(ui_edge)
        ui_edge.setPos(edge.start_node.x, edge.start_node.y)
        self.edges[edge.id] = ui_edge

    def addResult(self, result: Result):
        self.data.results.append(result)
        ui_result = ResultItem(self.graph, result)
        self.addItem(ui_result)
        if isinstance(result.target, Node):
            ui_result.setPos(result.target.x, result.target.y)
        else:
            ui_edge = self.edges[result.target.id]
            start_point = QPointF(result.target.start_node.x, result.target.start_node.y)
            end_point = QPointF(result.target.end_node.x, result.target.end_node.y)
            offset = result.target.offset or 0
            if result.target.length:
                offset /= result.target.length

            position = bezier(start_point, end_point, start_point + ui_edge.quad_center, offset)
            ui_result.setPos(position)

    def clearResults(self):
        self.data.results.clear()
        for item in self.items():
            if isinstance(item, ResultItem):
                self.removeItem(item)
        self.update()

    def on_node_taken(self, node: NodeItem):
        self.moving_edges.clear()
        self.clearResults()
        del self.data.nodes[node.data.id]
        for edge in list(self.iterEdgesByNode(node.data)):
            edge_item = self.edges[edge.id]
            self.removeItem(edge_item)
            del self.edges[edge.id]
            del self.data.edges[edge.id]
            self.edges_matrix[edge.start_node.id][edge.end_node.id].remove(edge)
            self.edges_matrix[edge.end_node.id][edge.start_node.id].remove(edge)
            self.moving_edges.append(edge)

    def on_node_selected(self, node_item: NodeItem, selected: bool):
        if selected:
            self.selected_node = node_item
        else:
            self.selected_node = None
