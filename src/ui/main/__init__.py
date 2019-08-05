from functools import partial

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QErrorMessage, QMessageBox

from history import History
from serializer import SerializerError
from serializer.json import JsonSerializer
from storage.exceptions import StorageError
from storage.filesystem import FileSystemStorage
from ui.about import About
from ui.editor import GraphScene
from .Main import Ui_Main

_ = partial(QApplication.translate, 'Main')


class Main(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.storage = FileSystemStorage(self, serializer=JsonSerializer())
        self.history = History(self)
        self.ui = Ui_Main()
        self.scene = GraphScene(self)
        self.setupUi()

    def setupUi(self):
        self.ui.setupUi(self)
        self.setCentralWidget(self.ui.graphicsView)
        self.ui.graphicsView.setAcceptDrops(True)
        self.ui.graphicsView.setScene(self.scene)

    def handleError(self, title, msg):
        error_message = QErrorMessage(self)
        error_message.setWindowTitle(_(title))
        error_message.showMessage(_(msg))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        self.scene.setSceneRect(0, 0, size.w, size.h)

    @pyqtSlot(bool)
    def on_storage_openChanged(self, opened):
        self.ui.actionSave.setEnabled(opened)
        self.ui.actionSaveAs.setEnabled(opened)
        self.ui.actionClose.setEnabled(opened)

    @pyqtSlot()
    def on_actionNew_triggered(self):
        self.storage.new()

    @pyqtSlot()
    def on_actionOpen_triggered(self):
        try:
            self.storage.open()
        except StorageError as e:
            self.handleError('Failed to open file', str(e))
        except SerializerError as e:
            self.handleError('Corrupted file', str(e))

    @pyqtSlot()
    def on_actionSave_triggered(self):
        try:
            self.storage.save()
        except StorageError as e:
            self.handleError('Failed to save file', str(e))

    @pyqtSlot()
    def on_actionSaveAs_triggered(self):
        self.storage.saveAs()

    @pyqtSlot()
    def on_actionClose_triggered(self):
        self.storage.close()

    @pyqtSlot()
    def on_actionQuit_triggered(self):
        if not self.history.clear:
            title = _('Exit')
            text = _('Are you sure you want to exit?\nAll changes will be lost')
            reply = QMessageBox.question(self, title, text, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                QApplication.quit()
        else:
            QApplication.quit()

    @pyqtSlot()
    def on_actionUndo_triggered(self):
        self.history.undo()

    @pyqtSlot()
    def on_actionRedo_triggered(self):
        self.history.redo()

    @pyqtSlot()
    def on_actionAbout_triggered(self):
        About(self).show()
