import copy
import numpy as np
import math
import sys
from pprint import pprint
import json

inf = sys.float_info.max # infinity value max float

def main():
    # base_matrix = [
    #     [[[5,1]], [[8,4],[1,7]], [[inf,0], [5]]],
    #     [[8,1], [0], [8], [2,3]],
    #     [[inf], [8], [0], [1,5,8]],
    #     [[5], [2,3], [1,5,8], [0]]
    # ]

    base_matrix = [
        [[0], [4], [6]],
        [[4], [0], [8]],
        [[6], [8], [0]]
    ]
    base_array = [8,10,20,4,1]
    center = MaxSupply(base_matrix,base_array)
    busy_edges = [[[] for j in range (0, len(base_matrix))] for i in range (0, len(base_matrix))]
    ss = center._find_all_points_on_limit(0, 3, busy_edges)
    print('#######################################')
    for s in ss:
        print(s)
    


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

class MaxSupply:
    def __init__(self, distance_matrix, weight_array):
        self.distance_matrix = distance_matrix
        self.weight_array = weight_array
        self.matrix_short_dist = None
        self.points_on_limit = []


    def _from_multigraph_to_graph(self):
        if len(self.distance_matrix) != 0:
            matrix = [[] for i in range (0, len(self.distance_matrix))]
            for k in range(0, len(self.distance_matrix)):
                for i in range(0, len(self.distance_matrix)):
                    matrix[k].append(min(self.distance_matrix[k][i]))
            return matrix
        else:
            raise Exception("Matrix is empty")

    def _algo_floid(self):
        if len(self.distance_matrix) != 0:
            matrix = self._from_multigraph_to_graph()
            for k in range(0, len(matrix)):
                for i in range(0, len(matrix)):
                    for j in range(0, len(matrix)):
                        matrix[i][j] = min(matrix[i][j], matrix[i][k] + matrix[k][j])

            self.matrix_short_dist = matrix

        else:
            raise Exception("Matrix is empty")
    
    # def _algo_dijkstra(self, node): 
    #     if len(self.distance_matrix) != 0:
    #         u = [False for i in range (0, len(self.distance_matrix))]
    #         path = [(0,0) for i in range (0, len(self.distance_matrix))]
    #         d = [inf for i in range (0, len(self.distance_matrix))]
    #         d[node] = 0
    #         for i in range(0, len(self.distance_matrix)):
    #             v = -1
    #             for j in range(0, len(self.distance_matrix)):
    #                 if (not u[j] and (v == -1 or d[j] < d[v])):
    #                     v = j
    #             if (d[v] == inf):
    #                 break
    #             u[v] = True
    #             for j in range (0, len(self.distance_matrix)):
    #                 for x in range (0, len(self.distance_matrix[v][j])):
    #                     if (self.distance_matrix[v][j][x] == 0 or self.distance_matrix[v][j][x] == inf):
    #                         continue
    #                     to = j
                        
    #                     length = self.distance_matrix[v][j][x]
    #                     if (d[v] + length < d[to]):
    #                         d[to] = d[v] + length
    #                         path[to] = (v,x)
    #         return path, d
    #     else:
    #         raise Exception("Matrix is empty")

    # def _get_path_between_nodes(self, path_array, first_node, second_node):
    #     path = []
    #     path.append((second_node,0))
    #     while (second_node != first_node) :
    #         second_node = p[second_node][0]
    #         path.append((second_node, p[second_node][1]))
    #     return list(reversed(path))

    # def _algo_dijkstra_for_each_node(self):
    #     if len(self.distance_matrix) != 0:
    #         self.dijkstra_results = []
    #         for i in range(0, len(self.distance_matrix)):
    #             path_array, distance_array = self._algo_dijkstra(i)
    #             self.dijkstra_results.append((path_array, distance_array))
    #     else:
    #         raise Exception("Matrix is empty")
    #     # for i in range (0, len(self.dijkstra_results)) :
    #     #     print(self.dijkstra_results[i])
    #     return self.dijkstra_results


    def _find_places_with_max_supply(self):
        '''
        Returns array of edge centers
        as [(edge_length, shift_from_first_node, index_first_node, index_second_node)]
        '''

        if self.matrix_short_dist is None:
            self._algo_floid()
        arr_max_supply_points = []
        edge_shift_from_first_point = 0
        for k in range(0, len(self.distance_matrix)):
            for i in range(k, len(self.distance_matrix)):
                if (i == k):
                    continue
                for index_of_list_edges_ki in range(0, len(self.distance_matrix[k][i])):
                    if (self.distance_matrix[k][i][index_of_list_edges_ki] == inf) :
                        continue
                    max_len_rib = -1
                    for f in np.arange(0.1, 1, 0.1):
                        supply_to_j = 0
                        for j in range(0, len(self.distance_matrix)):
                             supply_to_j += self.weight_array[j] + min(f * self.distance_matrix[k][i][index_of_list_edges_ki] + self.matrix_short_dist[k][j], (1 - f) * self.distance_matrix[k][i][index_of_list_edges_ki] +  self.matrix_short_dist[i][j])    

                        if (supply_to_j > max_len_rib):
                            max_len_rib = supply_to_j
                            edge_shift_from_first_point = f * self.distance_matrix[k][i][index_of_list_edges_ki]

                    arr_max_supply_points.append((max_len_rib, edge_shift_from_first_point, k, i, index_of_list_edges_ki))

        return arr_max_supply_points
    
    def _find_all_points_on_limit(self, index_for_k, limit, busy_edges, append_of_array_in_point = True):
        if (limit <= 0):
            return None
        for k in range(index_for_k, len(self.distance_matrix)):
            for i in range(0, len(self.distance_matrix)):
                if (i == k):
                    continue
                for index_of_list_edges_ki in range(0, len(self.distance_matrix[k][i])):
                    if (self.distance_matrix[k][i][index_of_list_edges_ki] == inf) :
                        continue
                    if (append_of_array_in_point):
                            busy_edges = [[[] for j in range (0, len(self.distance_matrix))] for i in range (0, len(self.distance_matrix))]
                    if ((index_of_list_edges_ki in busy_edges[k][i])):
                        continue

                    busy_edges[k][i].append(index_of_list_edges_ki)
                    busy_edges[i][k].append(index_of_list_edges_ki)
                    
                    copy_limit = limit

                    if (self.distance_matrix[k][i][index_of_list_edges_ki] < copy_limit):
                        
                        copy_limit -= self.distance_matrix[k][i][index_of_list_edges_ki]
                        
                        if (append_of_array_in_point):
                            self.points_on_limit.append([(k,i,index_of_list_edges_ki)])
                        else:
                            self.points_on_limit[-1].append((k,i,index_of_list_edges_ki))
                        self._find_all_points_on_limit(i, copy_limit, busy_edges, False)
                    else:
                        if (append_of_array_in_point):
                            self.points_on_limit.append([(k,i,index_of_list_edges_ki, copy_limit)])
                        else:
                            self.points_on_limit[-1].append((k,i,index_of_list_edges_ki, copy_limit))
                            return
        return self.points_on_limit

    def _find_all_segments(self):
        print()

    def find_best_places_for_max_supply(self, limit=0):
        '''
        Find absolute centers
        '''
        places = self._find_places_with_max_supply()

        if (limit <= 0):
            eps = 10**(-7)
            max_supply_place = max(places, key=lambda x: x[0])

            return [Edge(x[0], x[1], x[2], x[3], x[4]) for i, x in enumerate(places) if math.fabs(x[0]-max_supply_place[0]) < eps]
        else: 
            res = [Edge(x[0], x[1], x[2], x[3], x[4]) for i, x in enumerate(places) if x[0] >= limit]
            return res
            


if __name__ == '__main__':
    main()