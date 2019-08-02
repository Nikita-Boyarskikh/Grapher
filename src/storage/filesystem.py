import json
from functools import partial

from PyQt5.QtWidgets import QFileDialog, QApplication

from storage import StorageBase

_ = partial(QApplication.translate, 'FileSystemStorageMixin')


class FileSystemStorage(StorageBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.extension = '.graph'
        self.fileFilter = _('Graph (*{})'.format(self.extension))
        self.file_path = None

    def _read(self):
        with open(self.file_path, 'r') as file:
            self.data = json.load(file)

    def _write(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.data, file)

    def _getSaveFileName(self, caption):
        self.file_path, name = QFileDialog.getSaveFileName(None, caption, filter=self.fileFilter)
        if self.file_path:
            self.file_path += self.extension
        return self.file_path != ''

    def _getOpenFileName(self, caption):
        self.file_path, name = QFileDialog.getOpenFileName(None, caption, filter=self.fileFilter)
        if self.file_path:
            self.file_path += self.extension
        return self.file_path != ''

    def new(self):
        if self._getSaveFileName(_('Create new graph')):
            super().new()

    def open(self):
        if self._getOpenFileName(_('Open graph')):
            super().open()

    def saveAs(self):
        if self.opened:
            if self._getSaveFileName(_('Save graph')):
                super().saveAs()

    def close(self):
        self.file_path = None
        super().close()
