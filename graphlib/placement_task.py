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
        [[0],[5,5,6],[8], [7]],
        [[5,5,6], [0], [3,7], [4]],
        [[8], [3,7], [0], [inf]],
        [[7], [4], [inf], [0]]
    ]
    base_array = [1,2,4, 3]
    center = MaxSupply(base_matrix,base_array)
    res = center.find_best_places_for_max_supply(2)
    for r in res:
        print(vars(r))


class Node:
    def __init__(self, index_of_node = 0, distance_to_farthest_point = 0):
        self.index_of_node = index_of_node
        self.distance_to_farthest_point = distance_to_farthest_point


class MaxSupply:
    def __init__(self, distance_matrix, weight_array):
        self.distance_matrix = distance_matrix
        self.weight_array = weight_array
        self.matrix_short_dist = None
        self.points_on_limit = []
        self.segments_array = []


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
    
    
    def find_best_medians(self, limit):
        find_answer = False
        res, res_arr = -1, None
        for i in range(len(self.distance_matrix)):
            res, res_arr = self.find_medians(i)
            if (res >= limit or limit <= 0):
                find_answer = True
                break
        if (find_answer):
            return res, res_arr
        return -1, None 
        
    def find_medians(self, count_nodes = 0, arr_nodes = None):
        if self.matrix_short_dist is None:
            self._algo_floid()
        if (not arr_nodes):
            arr_nodes = [-1 for i in range(count_nodes + 1)]
        ans = -1
        ans_arr = []
        for i in range(0, len(self.distance_matrix)):
            if (i in arr_nodes):
                continue
            arr_nodes[count_nodes] = i
            if (count_nodes > 0):
                
                res, res_arr = self.find_medians(count_nodes - 1, arr_nodes.copy())
                
            else:
                
                arr_nodes_distance = [1/self.weight_array[x] for x in arr_nodes]
  
                for k in range(len(self.distance_matrix)):
                    if (k in arr_nodes):
                        continue
                    min = inf
                    min_j = -1
                    for j in range(len(arr_nodes)):
                        if (min > self.matrix_short_dist[arr_nodes[j]][k] + self.weight_array[k]):
                            min = self.matrix_short_dist[arr_nodes[j]][k] + self.weight_array[k]
                            min_j = j
                    
                    arr_nodes_distance[min_j] += 1 / min

                res, res_arr = sum(arr_nodes_distance), arr_nodes.copy()
            if (ans < res):
                ans = res
                ans_arr = res_arr
        return ans, ans_arr


    def find_best_places_for_max_supply(self, limit=0):
        '''
        Find absolute centers
        '''
        
        res, res_arr = self.find_best_medians(limit)
        return [Node(res_arr[i], res) for i in range(0, len(res_arr))]
            


if __name__ == '__main__':
    main()