import json

from serializer import Serializer


class JsonSerializer(Serializer):
    @staticmethod
    def str_to_obj(data):
        return json.loads(data)

    @staticmethod
    def obj_to_str(data):
        return json.dumps(data)
