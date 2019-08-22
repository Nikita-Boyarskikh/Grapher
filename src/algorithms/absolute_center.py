# TODO: refactor it

import sys
from dataclasses import dataclass

import math

from algorithms import Algorithm
from data import Result, Edge
from utils import build_empty_square_matrix, composite_id

inf = sys.float_info.max


@dataclass
class Segment:
    distance_to_first_point: float
    distance_to_second_point: float
    bit_mask_nodes: int
    # TODO


@dataclass
class Point:
    edge: Edge
    node_bit_mask: int = 0


class AbsoluteCenter(Algorithm):
    precision = 10 ** -7

    def __init__(self, data, limit=0):
        super().__init__(data, limit=limit)
        self.matrix_short_dist = None
        self.points_on_limit = []
        self.segments_array = []

    def _find_abs_node_centers(self):
        """
        Yield potential node centers
        """

        if self.matrix_short_dist is None:
            self._algo_floid()
        return (max(self.matrix_short_dist, key=lambda x: x[i])[i] for i, _ in enumerate(self.matrix_short_dist[0]))

    def _find_abs_edge_centers(self):
        """
        Yield edge centers
        as [(edge_length, shift_from_first_node, index_first_node, index_second_node)]
        """

        if self.matrix_short_dist is None:
            self._algo_floid()

        edge_shift_from_first_point = 0

        for k in range(0, len(self.distance_matrix)):
            for i in range(k, len(self.distance_matrix)):
                if i == k:
                    continue
                for index_of_list_edges_ki in range(0, len(self.distance_matrix[k][i])):
                    if self.distance_matrix[k][i][index_of_list_edges_ki] == inf:
                        continue
                    distance_to_farthest_point = inf
                    for f in range(1, 10):
                        f *= 0.1  # iterate over 0.1 to 1.0 by 0.1
                        max_len_rib = -1
                        for j in range(0, len(self.distance_matrix)):
                            current_min = min(
                                f * self.distance_matrix[k][i][index_of_list_edges_ki] + self.matrix_short_dist[k][j],
                                (1 - f) * self.distance_matrix[k][i][index_of_list_edges_ki]
                                + self.matrix_short_dist[i][j]
                            )
                            if max_len_rib < current_min:
                                max_len_rib = current_min

                        if distance_to_farthest_point > max_len_rib:
                            distance_to_farthest_point = max_len_rib
                            edge_shift_from_first_point = f * self.distance_matrix[k][i][index_of_list_edges_ki]

                    start_node_id, end_node_id = 0, 0
                    for node_id, node_index in self.node_indexes.items():
                        if node_index == k:
                            start_node_id = node_id
                        if node_index == i:
                            end_node_id = node_id
                    edge = self.data.edges.get(composite_id(start_node_id, end_node_id, index_of_list_edges_ki)) or \
                        self.data.edges.get(composite_id(end_node_id, start_node_id, index_of_list_edges_ki))
                    edge.offset = edge_shift_from_first_point
                    yield Result(edge, distance_to_farthest_point)

    def _list_of_nodes_to_bit_mask(self, nodes):
        length = len(self.distance_matrix)
        res = 0
        for i in range(0, length):
            if i in nodes:
                res += 2 ** i
        return res

    def _find_all_points_on_limit(self):
        busy_edges = build_empty_square_matrix(len(self.distance_matrix))
        self._find_all_points_on_limit_wrapper(0, busy_edges, self.limit)

    def _find_all_points_on_limit_wrapper(self, index_for_k, busy_edges, limit, append_of_array_in_point=True, first_node=-1):
        if limit <= 0:
            return None
        for k in range(index_for_k, len(self.distance_matrix)):
            for i in range(0, len(self.distance_matrix)):
                if i == k:
                    continue
                for index_of_list_edges_ki in range(0, len(self.distance_matrix[k][i])):
                    if self.distance_matrix[k][i][index_of_list_edges_ki] == inf:
                        continue
                    if append_of_array_in_point:
                        busy_edges = build_empty_square_matrix(len(self.distance_matrix))
                    if index_of_list_edges_ki in busy_edges[k][i]:
                        continue

                    busy_edges[k][i].append(index_of_list_edges_ki)
                    busy_edges[i][k].append(index_of_list_edges_ki)

                    copy_limit = limit

                    if self.distance_matrix[k][i][index_of_list_edges_ki] < copy_limit:

                        copy_limit -= self.distance_matrix[k][i][index_of_list_edges_ki]

                        if append_of_array_in_point:
                            self.points_on_limit.append((k,i,index_of_list_edges_ki, self.distance_matrix[k][i][index_of_list_edges_ki], self._list_of_nodes_to_bit_mask([k])))
                        else:
                            self.points_on_limit.append((k,i,index_of_list_edges_ki, self.distance_matrix[k][i][index_of_list_edges_ki], self._list_of_nodes_to_bit_mask([first_node])))
                        self._find_all_points_on_limit_wrapper(i, busy_edges, copy_limit, False, k)
                    else:
                        if append_of_array_in_point:
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

        while len(self.segments_array[-1]) > 1:
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

    def find_best_segments(self):
        self._find_all_points_on_limit()
        self._find_all_segments()

        all_nodes_bit = 2 ** len(self.distance_matrix) - 1

        arr_segments = []
        for segment in self.segments_array:
            arr_segments += segment
        arr_segments.sort(key=lambda x: x[-1], reverse=True)

        arr_segments_res = []
        nodes_bit = 0
        for segment in arr_segments:
            if nodes_bit | segment[5] != nodes_bit:
                nodes_bit |= segment[5]
                arr_segments_res.append(segment)
            if nodes_bit & all_nodes_bit == all_nodes_bit:
                return arr_segments_res

    def _get_edge_weight(self, edge: Edge) -> float:
        return edge.length

    def calc(self):
        """
        Find absolute centers
        """
        if not self.limit:
            edges = list(self._find_abs_edge_centers())
            nodes = list(self._find_abs_node_centers())
            min_node_score = min(nodes)
            min_edge_score = min(edge.score for edge in edges)

            if min_node_score < min_edge_score:
                for node_id, node_index in self.node_indexes.items():
                    score = nodes[node_index]
                    if math.fabs(score - min_node_score) < self.precision:
                        node = self.data.nodes[node_id]
                        yield Result(node, score)
            else:
                for edge in edges:
                    if math.fabs(edge.score - min_edge_score) < self.precision:
                        yield edge
        else:
            best_segments = self.find_best_segments()
            if best_segments:
                for node_id, node_index in list(self.node_indexes.items())[:len(best_segments)]:
                    segment = best_segments[node_index]
                    for node_id, node_index in self.node_indexes.items():
                        if node_index == segment[0]:
                            start_node_id = node_id
                        if node_index == segment[1]:
                            end_node_id = node_id
                    edge = self.data.edges.get(composite_id(start_node_id, end_node_id, segment[2])) or \
                        self.data.edges.get(composite_id(end_node_id, start_node_id, segment[2]))
                    edge.offset = min(segment[3], segment[4])  # TODO: Think about how to display it
                    yield Result(edge, self.limit)
