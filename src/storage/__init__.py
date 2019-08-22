from data import Graph


class StorageBase:
    def __init__(self):
        self.data = None
        self.opened = False

    def _write(self):
        raise NotImplementedError()

    def _read(self):
        raise NotImplementedError()

    def save(self):
        if self.opened:
            self._write()

    def saveAs(self):
        if self.opened:
            self.save()

    def open(self):
        self.opened = True
        self._read()

    def new(self):
        self.opened = True
        self.data = Graph()
