from collections import defaultdict

from data import Node, Edge, Result, Graph, EdgeWithPoint
from serializer.exceptions import NodeNotFound, EdgeNotFound, SerializerError
from utils import throw, find


class Serializer:
    def __init__(self):
        self.data = None

    @staticmethod
    def obj_to_str(data):
        raise NotImplementedError()

    @staticmethod
    def str_to_obj(data):
        raise NotImplementedError()

    @staticmethod
    def _get_or_raise(obj, obj_type, key):
        return obj.get(key) or throw(SerializerError('{} object must contains key "{}"'.format(obj_type, key)))

    @staticmethod
    def _assert(condition, msg):
        if not condition:
            raise SerializerError(msg=msg)

    def _find_node(self, node_id):
        return find(self.data.nodes, lambda node: node.id == node_id) or throw(NodeNotFound(node_id))

    def _find_edge(self, edge_id):
        return find(self.data.edges, lambda edge: edge.id == edge_id) or throw(EdgeNotFound(edge_id))

    @staticmethod
    def serialize_node(node):
        assert isinstance(node, Node)
        return {
            'id': node.id,
            'name': node.name,
            'x': node.x,
            'y': node.y,
            'weight': node.weight
        }

    @staticmethod
    def serialize_edge(edge):
        assert isinstance(edge, Edge)
        return {
            'id': edge.id,
            'start_node': edge.start_node.id,
            'end_node': edge.end_node.id,
            'weight': edge.weight
        }

    @staticmethod
    def serialize_result(result):
        assert isinstance(result, Result)

        target_is_node = isinstance(result.target, Node)
        return {
            ('node' if target_is_node else 'edge'): result.target.id,
            'score': result.score
        }

    def serialize(self):
        assert isinstance(self.data, Graph)

        obj = defaultdict(list)
        for node in self.data.nodes:
            obj['nodes'].append(self.serialize_node(node))

        for edge in self.data.edges:
            obj['edges'].append(self.serialize_edge(edge))

        for result in self.data.results:
            obj['results'].append(self.serialize_result(result))

        return self.obj_to_str(obj)

    def deserialize_node(self, node):
        id_ = self._get_or_raise(node, 'Node', 'id')
        name = self._get_or_raise(node, 'Node', 'name')
        x = self._get_or_raise(node, 'Node', 'x')
        y = self._get_or_raise(node, 'Node', 'y')
        weight = self._get_or_raise(node, 'Node', 'weight')
        return Node(id_, name, x, y, weight)

    def deserialize_edge(self, edge):
        id_ = self._get_or_raise(edge, 'Edge', 'id')
        start_node_id = self._get_or_raise(edge, 'Edge', 'start_node')
        end_node_id = self._get_or_raise(edge, 'Edge', 'end_node')
        weight = self._get_or_raise(edge, 'Edge', 'weight')
        start_node = self._find_node(start_node_id)
        end_node = self._find_node(end_node_id)
        offset = edge.get('offset')
        return EdgeWithPoint(id_, start_node, end_node, weight, offset=offset)

    def deserialize_result(self, result):
        score = self._get_or_raise(result, 'Result', 'score')
        node_id = result.get('node')
        edge_id = result.get('edge')

        if node_id:
            target = self._find_node(node_id)
        elif edge_id:
            target = self._find_edge(edge_id)
        else:
            raise SerializerError(msg='Result object must contains key "node" or "edge"')

        return Result(target, score)

    def deserialize(self, data):
        obj = self.str_to_obj(data)
        self._assert(isinstance(obj, dict), 'Json must be an object')
        nodes_list = self._get_or_raise(obj, 'Json', 'nodes')
        self._assert(isinstance(nodes_list, list), 'Nodes must be an array')
        edges_list = self._get_or_raise(obj, 'Json', 'edges')
        self._assert(isinstance(edges_list, list), 'Edges must be an array')
        results_list = self._get_or_raise(obj, 'Json', 'results')
        self._assert(isinstance(results_list, list), 'Results must be an array')

        self.data = Graph([], [], [])
        for node in nodes_list:
            self.data.nodes.append(self.deserialize_node(node))

        for edge in edges_list:
            self.data.edges.append(self.deserialize_edge(edge))

        for result in results_list:
            self.data.results.append(self.deserialize_result(result))
