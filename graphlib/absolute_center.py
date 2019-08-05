import copy
import numpy as np
import math
import sys

inf = sys.float_info.max # infinity value max float

def main():
    base_matrix = [
        [[0], [8,1], [inf], [5]],
        [[8,1], [0], [8], [2,3]],
        [[inf], [8], [0], [1,5,8]],
        [[5], [2,3], [1,5,8], [0]]
    ]
    center = AbsoluteCenter(base_matrix)
    print(center.find_abs_center(2580))

class Node:
    def __init__(self, index_of_node = 0, distance_to_farthest_point = 0):
        self.index_of_node = index_of_node
        self.distance_to_farthest_point = distance_to_farthest_point

class Edge:
    def __init__(self, distance_to_farthest_point = 0, 
                    edge_shift_from_first_point = 0, 
                    first_point = 0, 
                    second_point = 0, 
                    index_of_list_edges_ki = 0):
        self.distance_to_farthest_point = distance_to_farthest_point
        self.edge_shift_from_first_point = edge_shift_from_first_point
        self.first_point = first_point
        self.second_point = second_point
        self.index_of_list_edges_ki = index_of_list_edges_ki

class AbsoluteCenter:
    def __init__(self, matrix):
        self.matrix = matrix
        self.matrix_short_dist = None

    def _from_multigraph_to_graph(self):
        if len(self.matrix) != 0:
            matrix = [[] for i in range (0, len(self.matrix))]
            for k in range(0, len(self.matrix)):
                for i in range(0, len(self.matrix)):
                    matrix[k].append(min(self.matrix[k][i]))
            return matrix
        else:
            raise Exception("Matrix is empty")
    
    def _algo_floid(self):
        if len(self.matrix) != 0:
            matrix = self._from_multigraph_to_graph()
            for k in range(0, len(matrix)):
                for i in range(0, len(matrix)):
                    for j in range(0, len(matrix)):
                        matrix[i][j] = min(matrix[i][j], matrix[i][k] + matrix[k][j])

            self.matrix_short_dist = matrix

        else:
            raise Exception("Matrix is empty")

    def _find_abs_node_centers(self):
        '''
        Returns list with potential node centers
        '''

        if self.matrix_short_dist is None:
            self._algo_floid()
        return list(np.amax(self.matrix_short_dist, 0))

    def _find_abs_edge_centers(self):
        '''
        Returns array of edge centers
        as [(edge_length, shift_from_first_node, index_first_node, index_second_node)]
        '''

        if self.matrix_short_dist is None:
            self._algo_floid()

        arr_min_rib = []
        edge_shift_from_first_point = 0

        for k in range(0, len(self.matrix)):
            for i in range(k, len(self.matrix)):
                if (i == k):
                    continue
                for index_of_list_edges_ki in range(0, len(self.matrix[k][i])):
                    if (self.matrix[k][i][index_of_list_edges_ki] == inf) :
                        continue
                    distance_to_farthest_point = inf
                    for f in np.arange(0.1, 1, 0.1):
                        max_len_rib = -1
                        for j in range(0, len(self.matrix)):
                            current_min = min(f * self.matrix[k][i][index_of_list_edges_ki] + self.matrix_short_dist[k][j], (1 - f) * self.matrix[k][i][index_of_list_edges_ki] +  self.matrix_short_dist[i][j])    
                            if (max_len_rib < current_min):
                                max_len_rib = current_min

                        if (distance_to_farthest_point > max_len_rib):
                            distance_to_farthest_point = max_len_rib
                            edge_shift_from_first_point = f * self.matrix[k][i][index_of_list_edges_ki]

                    arr_min_rib.append((distance_to_farthest_point, edge_shift_from_first_point, k, i, index_of_list_edges_ki))
        return arr_min_rib
    
    def find_abs_center(self, limit=0):
        '''
        Find absolute centers
        '''
        edges = self._find_abs_edge_centers()
        nodes = self._find_abs_node_centers()

        if (limit <= 0):
            eps = 10**(-7)
            min_node = min(nodes)
            min_edge = min(edges, key=lambda x: x[0])

            if min_node < min_edge[0]:
                return [Node(i, x) for i, x in enumerate(nodes) if math.fabs(x-min_node) < eps]
            else:
                return [x for i, x in enumerate(edges) if math.fabs(x[0]-min_edge[0]) < eps]
        else: 
            res = [Node(i, x) for i, x in enumerate(nodes) if x <= limit] + [Edge(x[0], x[1], x[2], x[3], x[4]) for i, x in enumerate(edges) if x[0] <= limit]
            return res
            


if __name__ == '__main__':
    main()