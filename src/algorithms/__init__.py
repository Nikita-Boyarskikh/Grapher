import sys
from typing import List

from data import Result, Graph, Edge
from utils import build_empty_square_matrix


class Algorithm:
    def __init__(self, data: Graph, limit=0):
        self.data = data
        self.limit = limit
        self.check_data()
        self.node_indexes = {}
        self.node_ids = {}
        self.distance_matrix = self._build_distance_matrix()

    def _build_distance_matrix(self):
        distance_matrix = build_empty_square_matrix(len(self.data.nodes))

        # create indexes for node ids
        i = 0
        for node in self.data.nodes.values():
            if node.id not in self.node_indexes:
                self.node_indexes[node.id] = i
                i += 1

        # fill distance matrix with edge weights
        for edge in self.data.edges.values():
            start_node_index = self.node_indexes[edge.start_node.id]
            end_node_index = self.node_indexes[edge.end_node.id]
            weight = self._get_edge_weight(edge)
            distance_matrix[start_node_index][end_node_index].append(weight)
            distance_matrix[end_node_index][start_node_index].append(weight)

        # fill empty distance with inf
        for i, _ in enumerate(distance_matrix):
            assert len(distance_matrix) == len(distance_matrix[i])
            for j, _ in enumerate(distance_matrix[i]):
                if not distance_matrix[i][j]:
                    distance_matrix[i][j].append(0 if i == j else sys.float_info.max)

        return distance_matrix

    def _from_multigraph_to_graph(self):
        matrix = [[] for _ in range(0, len(self.distance_matrix))]
        for k in range(0, len(self.distance_matrix)):
            for i in range(0, len(self.distance_matrix)):
                matrix[k].append(min(self.distance_matrix[k][i]))
        return matrix

    def _algo_floid(self):
        matrix = self._from_multigraph_to_graph()
        for k in range(0, len(matrix)):
            for i in range(0, len(matrix)):
                for j in range(0, len(matrix)):
                    matrix[i][j] = min(matrix[i][j], matrix[i][k] + matrix[k][j])

        self.matrix_short_dist = matrix

    def check_data(self):
        pass

    def _get_edge_weight(self, edge: Edge) -> float:
        raise NotImplementedError()

    def calc(self) -> List[Result]:
        raise NotImplementedError()
