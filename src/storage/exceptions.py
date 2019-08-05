class StorageError(Exception):
    def __init__(self, *args, msg=None):
        self.msg = msg or str(self)

    def __str__(self):
        return self.msg
