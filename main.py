import numpy as np
import math

inf = 10**10

def main():
    # FLOID
    base_matrix = [
        [0, 7, 5, 3],
        [7, 0, 7, 600.5],
        [5, 7, 0, 3],
        [3, 600.5, 3, 0]
    ]
    matrix_after_floid = algo_floid(base_matrix)
    print_matrix(matrix_after_floid)
    absolute_center_node = np.amax(matrix_after_floid, 0)
    print("Абсолютный центр вершин = {}".format(absolute_center_node))

    print()
    
    # HAKIMI
    base_matrix = [
        [0, 7, 5, 3],
        [7, 0, 7, 600.5],
        [5, 7, 0, 3],
        [3, 600.5, 3, 0]
    ]
    absolute_center_edges = algo_hakimi(base_matrix, matrix_after_floid)
    print("Абсолютный центр ребер = {}".format(absolute_center_edges))
  

def print_matrix(matrix):
    for i in matrix:
        print(i, end="\n")

def algo_floid(matrix):
    for k in range(0, len(matrix)):
        for i in range(0, len(matrix)):
            for j in range(0, len(matrix)):
                matrix[i][j] = min(matrix[i][j], matrix[i][k] + matrix[k][j])
    return matrix

def algo_hakimi(matrix, matrix_floid):
    arr_min_rib = []
    for k in range(0, len(matrix)):
        for i in range(k, len(matrix)):
            if (i == k or matrix[k][i] == inf) :
                continue

            max_len_rib = -1
            for f in np.arange(0.1, 1, 0.1):
                for j in range(0, len(matrix)):
                    if (j == k or i == j ) :
                        continue

                    current_min = min(f * matrix[k][i] + matrix_floid[k][j], (1 - f) * matrix[k][i] +  matrix_floid[i][j])
                    
                    if (max_len_rib < current_min):
                        max_len_rib = current_min

            arr_min_rib.append(max_len_rib)
    return arr_min_rib


if __name__ == '__main__':
    main()



   # m = [
    #     [0,   1,   inf, 8,   6],
    #     [1,   0,   inf, inf, 5],
    #     [inf, inf, 0,   3,   7],
    #     [8,   inf, 3,   0,   1],
    #     [6,   5,   7,   1,   0]
    # ]