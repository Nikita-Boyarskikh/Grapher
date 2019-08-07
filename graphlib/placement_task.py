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
        [[0], [10], [inf], [15], [inf]],
        [[10], [0], [4], [inf], [5]],
        [[inf], [4], [0], [10], [3]],
        [[15], [inf], [10], [0], [1]],
        [[inf], [5], [3], [1], [0]],
    ]
    base_array = [8,10,20,4,1]
    center = MaxSupply(base_matrix,base_array)

    print(center.find_best_segments(10))


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
    
    
             
    def _list_of_nodes_to_bit_mask(self, nodes):
        length = len(self.distance_matrix)
        res = ''
        for i in range(0, length ):
            if (i in nodes):
                res += '1'
            else:
                res += '0'
        res = res[::-1]
        return int(res, 2)

    
    def _find_all_points_on_limit(self, limit):
        busy_edges = [[[] for j in range (0, len(self.distance_matrix))] for i in range (0, len(self.distance_matrix))]
        self._find_all_points_on_limit_wrapper(0, limit, busy_edges)

    def _find_all_points_on_limit_wrapper(self, index_for_k, limit, busy_edges, append_of_array_in_point = True, first_node = -1):
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
                            self.points_on_limit.append((k,i,index_of_list_edges_ki, self.distance_matrix[k][i][index_of_list_edges_ki], self._list_of_nodes_to_bit_mask([k])))
                        else:
                            self.points_on_limit.append((k,i,index_of_list_edges_ki, self.distance_matrix[k][i][index_of_list_edges_ki], self._list_of_nodes_to_bit_mask([first_node])))
                        self._find_all_points_on_limit_wrapper(i, copy_limit, busy_edges, False, k)
                    else:
                        if (append_of_array_in_point):
                            self.points_on_limit.append((k,i,index_of_list_edges_ki, copy_limit, self._list_of_nodes_to_bit_mask([k])))
                        else:
                            self.points_on_limit.append((k,i,index_of_list_edges_ki, copy_limit, self._list_of_nodes_to_bit_mask([first_node])))
                            return
        return self.points_on_limit

    def _find_all_segments(self):       
        self.segments_array.append([])
        matrix_of_bools = [[False for j in range(0, len(self.points_on_limit))] for i in range(0, len(self.points_on_limit))]
        for i in range(0, len(self.points_on_limit)):
            for j in range(0, len(self.points_on_limit)):
                if (i == j or matrix_of_bools[i][j]):
                    continue
                matrix_of_bools[i][j] = True
                matrix_of_bools[j][i] = True
                ii = self.points_on_limit[i][0]
                jj = self.points_on_limit[i][1]
     
                length_of_edge = self.distance_matrix[ii][jj][self.points_on_limit[i][2]]
                distance_to_second_point = length_of_edge - self.points_on_limit[i][3]
                distance_to_first_point = self.points_on_limit[i][3]
                if (distance_to_first_point > distance_to_second_point):
                    distance_to_first_point, distance_to_second_point = distance_to_second_point, distance_to_first_point
                bit_mask_nodes = self.points_on_limit[i][4] | self.points_on_limit[j][4]
                if (self.points_on_limit[i][0] == self.points_on_limit[j][1] and
                    self.points_on_limit[i][1] == self.points_on_limit[j][0] and 
                    self.points_on_limit[i][2] == self.points_on_limit[j][2] and 
                    self.points_on_limit[i][3] + self.points_on_limit[j][3] >= length_of_edge
                    ):                    
                     
                    
                    self.segments_array[0].append([self.points_on_limit[i][0], self.points_on_limit[i][1], self.points_on_limit[i][2], distance_to_first_point, distance_to_second_point, bit_mask_nodes])
                
                elif (
                    self.points_on_limit[i][2] == self.points_on_limit[j][2] and
                    self.points_on_limit[i][0] == self.points_on_limit[j][0] and
                    self.points_on_limit[i][1] == self.points_on_limit[j][1] 
                    ):   

                    if (self.points_on_limit[i][3] < self.points_on_limit[j][3]):
                        self.segments_array[0].append([self.points_on_limit[i][0], self.points_on_limit[i][1], self.points_on_limit[i][2], 0, self.points_on_limit[i][3], bit_mask_nodes])
                    else:
                        self.segments_array[0].append([self.points_on_limit[i][0], self.points_on_limit[i][1], self.points_on_limit[i][2], 0, self.points_on_limit[j][3], bit_mask_nodes])

        
        while (len(self.segments_array[-1]) > 1):
            self.segments_array.append([])
            matrix_of_bools = [[False for j in range(0, len(self.segments_array[-2]))] for i in range(0, len(self.segments_array[-2]))]
            for i in range(0, len(self.segments_array[-2])):
                for j in range(0, len(self.segments_array[-2])):
                    if (i == j or matrix_of_bools[i][j]):
                        continue
                    matrix_of_bools[i][j] = True
                    matrix_of_bools[j][i] = True
                    ii = self.segments_array[-2][i][0]
                    jj = self.segments_array[-2][i][1]
                    length_of_edge = self.distance_matrix[ii][jj][self.segments_array[-2][i][2]]
                    bit_mask_nodes = self.segments_array[-2][i][5] | self.segments_array[-2][j][5]
                    
                    if (
                        self.segments_array[-2][i][2] == self.segments_array[-2][j][2] and
                        (self.segments_array[-2][i][0] == self.segments_array[-2][j][1] and
                        self.segments_array[-2][i][1] == self.segments_array[-2][j][0] or
                        self.segments_array[-2][i][0] == self.segments_array[-2][j][0] and
                        self.segments_array[-2][i][1] == self.segments_array[-2][j][1])
                        ):

                        segment_first = 0
                        segment_second = 0
                        distt_1_1 = self.segments_array[-2][i][3]
                        distt_1_2 = self.segments_array[-2][i][4]
                        if (self.segments_array[-2][i][0] == self.segments_array[-2][j][0]):
                            distt_2_1 = self.segments_array[-2][j][3]
                            distt_2_2 = self.segments_array[-2][j][4]
                        else:
                            distt_2_1 = length_of_edge - self.segments_array[-2][j][3]
                            distt_2_2 = length_of_edge - self.segments_array[-2][j][4]
                        if (distt_1_2 >= distt_2_1 and distt_1_1 <= distt_2_2):
                            if (distt_2_1 <= distt_1_1):
                                if (distt_2_2 <= distt_1_2):
                                    segment_first = distt_1_1
                                    segment_second = distt_2_2
                                else:
                                    segment_first = distt_1_1
                                    segment_second = distt_1_2
                            else:
                                if (distt_2_2 <= distt_1_2):
                                    segment_first = distt_2_1
                                    segment_second = distt_2_2
                                else:
                                    segment_first = distt_2_1
                                    segment_second = distt_1_2
                        else:
                            continue
                        new_segment = [self.segments_array[-2][i][0], self.segments_array[-2][i][1], self.segments_array[-2][i][2], segment_first, segment_second, bit_mask_nodes]
                        if new_segment not in self.segments_array[-1]:
                            self.segments_array[-1].append(new_segment)  


    def find_best_segments(self, limit):

        self._find_all_points_on_limit(limit)
        self._find_all_segments()
        

        res = ''.join(['1' for i in range(len(self.distance_matrix))])
        all_nodes_bit = int(res, 2)

        arr_segments = []
        for i in range (0, len(self.segments_array)):
            arr_segments += self.segments_array[i]
        arr_segments.sort(key=lambda x: x[-1], reverse=True)

        arr_segments_res = []
        nodes_bit = 0
        for i in range(0, len(arr_segments)):
            if (nodes_bit | arr_segments[i][5] != nodes_bit):
                nodes_bit |= arr_segments[i][5]
                arr_segments_res.append(arr_segments[i])
            if (nodes_bit & all_nodes_bit == all_nodes_bit):
                break
        if (nodes_bit & all_nodes_bit == all_nodes_bit):
            return arr_segments_res 
        else:
            return None 
        

    def find_best_places_for_max_supply(self, limit=0):
        '''
        Find absolute centers
        '''
        

        if (limit <= 0):
            eps = 10**(-7)
            places = self._find_places_with_max_supply()
            max_supply_place = max(places, key=lambda x: x[0])
            return [Edge(x[0], x[1], x[2], x[3], x[4]) for i, x in enumerate(places) if math.fabs(x[0]-max_supply_place[0]) < eps]
        else: 
            res = [Edge(x[0], x[1], x[2], x[3], x[4]) for i, x in enumerate(places) if x[0] >= limit]
            return res
            


if __name__ == '__main__':
    main()