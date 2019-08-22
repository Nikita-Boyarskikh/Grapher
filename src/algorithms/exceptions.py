class AlgorithmError(Exception):
    def __init__(self, *args, msg=None):
        super().__init__(*args)
        self.msg = msg or super().__str__()

    def __str__(self):
        return self.msg


class DataInvalidError(AlgorithmError):
    pass
