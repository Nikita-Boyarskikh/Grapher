from PyQt5.QtCore import pyqtSignal, QObject, QMetaObject

from data import Graph


class StorageBase(QObject):
    openChanged = pyqtSignal(bool)

    def __init__(self, parent):
        super().__init__(parent)
        self.data = None
        self.opened = False
        self.setObjectName('storage')
        QMetaObject.connectSlotsByName(parent)

    def emit(self):
        self.openChanged.emit(self.opened)

    def _write(self):
        raise NotImplementedError()

    def _read(self):
        raise NotImplementedError()

    def close(self):
        self.opened = False
        self.data = None
        self.emit()

    def save(self):
        if self.opened:
            self._write()

    def saveAs(self):
        if self.opened:
            self.save()

    def open(self):
        self.opened = True
        self._read()
        self.emit()

    def new(self):
        self.opened = True
        self.data = Graph()
        self.emit()
