import copy
import numpy as np
import math
import sys

inf = sys.float_info.max # infinity value max float

def main():
    base_matrix = [
        [0, 1, inf, 3],
        [1, 0 ,1, 4],
        [inf, 1, 0, 4],
        [3, 4, 4, 0]
    ]
    center = AbsoluteCenter(base_matrix, 0)
    print(center.find_abs_center())

class AbsoluteCenter:
    def __init__(self, matrix, limit=0):
        self.matrix = matrix
        self.limit = limit
        self.matrix_short_dist = None
    
    def _algo_floid(self):
        if len(self.matrix) != 0:
            matrix = copy.deepcopy(self.matrix)
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
        edge_koef = 0

        for k in range(0, len(self.matrix)):
            for i in range(k, len(self.matrix)):
                if (i == k or self.matrix[k][i] == inf) :
                    continue

                min_len_ribs = inf
                for f in np.arange(0.1, 1, 0.1):
                    max_len_rib = -1
                    for j in range(0, len(self.matrix)):
   
                        current_min = min(f * self.matrix[k][i] + self.matrix_short_dist[k][j], (1 - f) * self.matrix[k][i] +  self.matrix_short_dist[i][j])
                        
                        if (max_len_rib < current_min):
                            max_len_rib = current_min

                    if (min_len_ribs > max_len_rib):
                        min_len_ribs = max_len_rib
                        edge_koef = f * self.matrix[k][i]

                arr_min_rib.append((min_len_ribs, edge_koef, k, i))
        return arr_min_rib
    
    def find_abs_center(self):
        '''
        Find absolute centers
        '''
        edges = self._find_abs_edge_centers()
        nodes = self._find_abs_node_centers()

        if (self.limit <= 0):
            eps = 10**(-7)
            min_node = min(nodes)
            min_edge = min(edges, key=lambda x: x[0])

            if min_node < min_edge[0]:
                return {'nodes': [(i, x) for i, x in enumerate(nodes) if math.fabs(x-min_node) < eps]}
            else:
                return {'edges': [x for i, x in enumerate(edges) if math.fabs(x[0]-min_edge[0]) < eps]}
        else: 
            return {
                'nodes': [(i, x) for i, x in enumerate(nodes) if x <= self.limit], 
                'edges': [x for i, x in enumerate(edges) if x[0] <= self.limit],
            }

if __name__ == '__main__':
    main()