class SerializerError(Exception):
    def __init__(self, *args, msg=None):
        super().__init__(*args)
        self.msg = msg or super().__str__()

    def __str__(self):
        return self.msg


class NodeNotFound(SerializerError):
    def __init__(self, node_id, *args, msg=None):
        super().__init__(*args, msg=msg or self.get_msg(node_id))

    @staticmethod
    def get_msg(node_id):
        return 'Node with id={} is not found'.format(node_id)


class EdgeNotFound(SerializerError):
    def __init__(self, edge_id, *args, msg=None):
        super().__init__(*args, msg=msg or self.get_msg(edge_id))

    @staticmethod
    def get_msg(edge_id):
        return 'Edge with id={} is not found'.format(edge_id)
