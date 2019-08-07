class StorageError(Exception):
    def __init__(self, *args, msg=None):
        self.msg = msg or super().__str__()

    def __str__(self):
        return self.msg
