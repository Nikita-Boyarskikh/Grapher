import sys

from algorithms import Algorithm
from algorithms.exceptions import DataInvalidError
from data import Result, Edge

inf = sys.float_info.max


class MaxSupply(Algorithm):
    def __init__(self, data, limit=0):
        super().__init__(data, limit=limit)
        self.weight_array = [0 for _ in self.data.nodes.values()]
        for node in self.data.nodes.values():
            node_index = self.node_indexes[node.id]
            self.weight_array[node_index] = node.weight
        self.matrix_short_dist = None
        self.points_on_limit = []
        self.segments_array = []

    def find_best_medians(self):
        res, res_arr = -1, []
        for i in range(len(self.distance_matrix)):
            res, res_arr = self.find_medians(i)
            if res >= self.limit or self.limit <= 0:
                break
        return res, res_arr

    def find_medians(self, count_nodes=0, arr_nodes=None):
        if self.matrix_short_dist is None:
            self._algo_floid()
        if not arr_nodes:
            arr_nodes = [-1 for i in range(count_nodes + 1)]
        ans = -1
        ans_arr = []
        for i in range(0, len(self.distance_matrix)):
            if i in arr_nodes:
                continue
            arr_nodes[count_nodes] = i
            if count_nodes > 0:
                res, res_arr = self.find_medians(count_nodes - 1, arr_nodes.copy())
            else:

                arr_nodes_distance = [1/self.weight_array[x] for x in arr_nodes]
  
                for k in range(len(self.distance_matrix)):
                    if k in arr_nodes:
                        continue
                    min = inf
                    min_j = -1
                    for j in range(len(arr_nodes)):
                        if min > self.matrix_short_dist[arr_nodes[j]][k] + self.weight_array[k]:
                            min = self.matrix_short_dist[arr_nodes[j]][k] + self.weight_array[k]
                            min_j = j

                    arr_nodes_distance[min_j] += 1 / min

                res, res_arr = sum(arr_nodes_distance), arr_nodes.copy()
            if ans < res:
                ans = res
                ans_arr = res_arr
        return ans, ans_arr

    def check_data(self):
        if not all(edge.speed > 0 for edge in self.data.edges.values()):
            raise DataInvalidError('All edges must have positive speed')
        if not all(edge.length > 0 for edge in self.data.edges.values()):
            raise DataInvalidError('All edges must have positive length')
        if not all(node.weight > 0 for node in self.data.nodes.values()):
            raise DataInvalidError('All nodes must have positive weight')

    def _get_edge_weight(self, edge: Edge) -> float:
        return edge.length / edge.speed

    def calc(self):
        """
        Find absolute centers
        """
        res, res_arr = self.find_best_medians()
        for node_id, node_index in self.node_indexes.items():
            if node_index in res_arr:
                node = self.data.nodes[node_id]
                yield Result(node, res)
