from functools import partial

from PyQt5.QtWidgets import QFileDialog, QApplication

from storage import StorageBase
from storage.exceptions import StorageError

tr = QApplication.tr


class FileSystemStorage(StorageBase):
    def __init__(self, serializer):
        super().__init__()
        self.serializer = serializer
        self.extension = '.graph'
        self.fileFilter = tr('Graph (*{})'.format(self.extension))
        self.file_path = None

    def _read(self):
        try:
            with open(self.file_path, 'r') as file:
                self.serializer.deserialize(file.read())
                self.data = self.serializer.data
        except IOError as e:
            raise StorageError(msg=str(e))

    def _write(self):
        try:
            with open(self.file_path, 'w') as file:
                self.serializer.data = self.data
                file.write(self.serializer.serialize())
        except IOError as e:
            raise StorageError(msg=str(e))

    def _check_filename(self):
        if not self.file_path.endswith(self.extension):
            self.file_path += self.extension
        return self.file_path != self.extension

    def _getSaveFileName(self, caption):
        self.file_path, name = QFileDialog.getSaveFileName(None, caption, filter=self.fileFilter)
        return self._check_filename()

    def _getOpenFileName(self, caption):
        self.file_path, name = QFileDialog.getOpenFileName(None, caption, filter=self.fileFilter)
        return self._check_filename()

    def new(self):
        if self._getSaveFileName(tr('Create new graph')):
            super().new()

    def open(self):
        if self._getOpenFileName(tr('Open graph')):
            super().open()

    def saveAs(self):
        if self.opened:
            if self._getSaveFileName(tr('Save graph')):
                super().saveAs()

