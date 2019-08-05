import copy
import numpy as np
import math
import sys

inf = sys.float_info.max # infinity value max float

def main():
    # base_matrix = [
    #     [[[5,1]], [[8,4],[1,7]], [[inf,0], [5]]],
    #     [[8,1], [0], [8], [2,3]],
    #     [[inf], [8], [0], [1,5,8]],
    #     [[5], [2,3], [1,5,8], [0]]
    # ]

    base_matrix = [
        [[0], [5,3,1], [6], [inf], [inf]],
        [[5,3,1], [0], [2], [6], [7]],
        [[6], [2], [0], [3,2], [inf]],
        [[inf], [6], [3,2], [0], [5]],
        [[inf], [7], [inf], [5], [0]]
    ]
    base_array = [8,10,3,4,1]
    center = AbsoluteCenter(base_matrix)
    center._find_place_with_max_supply()

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
        self.dijkstra_results = None

    
    def _algo_dijkstra(self, node): 
        if len(self.matrix) != 0:
            u = [False for i in range (0, len(self.matrix))]
            path = [(0,0) for i in range (0, len(self.matrix))]
            d = [inf for i in range (0, len(self.matrix))]
            d[node] = 0
            for i in range(0, len(self.matrix)):
                v = -1
                for j in range(0, len(self.matrix)):
                    if (not u[j] and (v == -1 or d[j] < d[v])):
                        v = j
                if (d[v] == inf):
                    break
                u[v] = True
                for j in range (0, len(self.matrix)):
                    for x in range (0, len(self.matrix[v][j])):
                        if (self.matrix[v][j][x] == 0 or self.matrix[v][j][x] == inf):
                            continue
                        to = j
                        
                        length = self.matrix[v][j][x]
                        if (d[v] + length < d[to]):
                            d[to] = d[v] + length
                            path[to] = (v,x)
            return path, d
        else:
            raise Exception("Matrix is empty")

    def _get_path_between_nodes(self, path_array, first_node, second_node):
        path = []
        path.append((second_node,0))
        while (second_node != first_node) :
            second_node = p[second_node][0]
            path.append((second_node, p[second_node][1]))
        return list(reversed(path))

    def _algo_dijkstra_for_each_node(self):
        if len(self.matrix) != 0:
            self.dijkstra_results = []
            for i in range(0, len(self.matrix)):
                path_array, distance_array = self._algo_dijkstra(i)
                self.dijkstra_results.append((path_array, distance_array))
        else:
            raise Exception("Matrix is empty")
        # for i in range (0, len(self.dijkstra_results)) :
        #     print(self.dijkstra_results[i])
        return self.dijkstra_results


    def _find_place_with_max_supply(self):
        '''
        Returns array of edge centers
        as [(edge_length, shift_from_first_node, index_first_node, index_second_node)]
        '''

        if self.dijkstra_results is None:
            self._algo_dijkstra_for_each_node()
        arr_max_supply_points = []
        edge_shift_from_first_point = 0
        for k in range(0, len(self.matrix)):
            for i in range(k, len(self.matrix)):
                if (i == k):
                    continue
                for index_of_list_edges_ki in range(0, len(self.matrix[k][i])):
                    if (self.matrix[k][i][index_of_list_edges_ki] == inf) :
                        continue
                    max_len_rib = -1
                    for f in np.arange(0.1, 1, 0.1):
                        distance_to_j = 0
                        for j in range(0, len(self.matrix)):
                            distance_to_j += min(f * self.matrix[k][i][index_of_list_edges_ki] + self.dijkstra_results[k][1][j], (1 - f) * self.matrix[k][i][index_of_list_edges_ki] +  self.dijkstra_results[i][1][j])    

                        if (distance_to_j > max_len_rib):
                            max_len_rib = distance_to_j
                            edge_shift_from_first_point = f * self.matrix[k][i][index_of_list_edges_ki]

                    arr_max_supply_points.append((distance_to_j, edge_shift_from_first_point, k, i, index_of_list_edges_ki))
        for i in range (0, len(arr_max_supply_points)) :
            print(arr_max_supply_points[i])
        return arr_max_supply_points
    
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