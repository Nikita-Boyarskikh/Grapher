from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication

from storage.filesystem import FileSystemStorage
from ui.about import About
from .Main import Ui_Main


class Main(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.storage = FileSystemStorage(self)
        self.ui = Ui_Main()
        self.setupUi()

    def setupUi(self):
        self.ui.setupUi(self)
        self.setCentralWidget(self.ui.graphicsView)

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
        self.storage.open()

    @pyqtSlot()
    def on_actionSave_triggered(self):
        self.storage.save()

    @pyqtSlot()
    def on_actionSaveAs_triggered(self):
        self.storage.saveAs()

    @pyqtSlot()
    def on_actionClose_triggered(self):
        self.storage.close()

    @pyqtSlot()
    def on_actionQuit_triggered(self):
        QApplication.quit()

    @pyqtSlot()
    def on_actionUndo_triggered(self):
        pass

    @pyqtSlot()
    def on_actionRedo_triggered(self):
        pass

    @pyqtSlot()
    def on_actionAbout_triggered(self):
        About(self).show()
