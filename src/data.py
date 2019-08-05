from collections import namedtuple


Node = namedtuple('Node', [
    'id',
    'name',
    'x',
    'y',
    'weight'
])


Edge = namedtuple('Edge', [
    'id',
    'start_node',
    'end_node',
    'weight'
])


Result = namedtuple('Result', [
    'target',  # Node or EdgeWithPoint
    'score'
])


Graph = namedtuple('Graph', [
    'nodes',
    'edges',
    'results'
])


class EdgeWithPoint(Edge):
    def __init__(self, *args, offset=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.offset = offset  # from start node
