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
        return self.opened

    def saveAs(self):
        if self.opened:
            return self.save()
        return self.opened

    def open(self):
        self.opened = True
        self._read()
        return self.opened

    def new(self):
        self.opened = True
        self.data = Graph()
        return self.opened
