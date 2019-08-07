from PyQt5.QtCore import QObject


# TODO
class History(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.history = []

    @property
    def clear(self):
        return True

    def undo(self):
        pass

    def redo(self):
        pass
