from functools import partial

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QErrorMessage, QMessageBox, QInputDialog, QApplication

from algorithms.exceptions import AlgorithmError
from history import History
from algorithms.absolute_center import AbsoluteCenter
from algorithms.max_supply import MaxSupply
from serializer import SerializerError
from serializer.json import JsonSerializer
from storage.exceptions import StorageError
from storage.filesystem import FileSystemStorage
from ui.about import About
from ui.editor import GraphScene
from .Main import Ui_Main

tr = partial(QApplication.translate, '@default')


# TODO: Hot keys
class Main(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.storage = FileSystemStorage(serializer=JsonSerializer())
        self.history = History(self)
        self.ui = Ui_Main()
        self.scene = GraphScene(self)
        self.setupUi()

    def setupUi(self):
        self.ui.setupUi(self)
        self.setCentralWidget(self.ui.graphicsView)
        self.ui.graphicsView.setScene(self.scene)

    def handleError(self, title, msg):
        error_message = QErrorMessage(self)
        error_message.setWindowTitle(tr(title))
        error_message.showMessage(tr(msg))

    def shouldSave(self):
        if not self.history.clear:
            title = tr('Exit')
            text = tr('Are you sure you want to exit?\nAll changes will be lost')
            reply = QMessageBox.question(self, title, text, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                return True
        return False

    def showLimitDialog(self):
        limit, ok = QInputDialog.getDouble(
            self, tr('Input limit'), tr('Limit: '),
            value=0.0,
            min=0.0,
            decimals=2
        )
        if ok:
            return limit

    def data_is_complete(self):
        if not self.scene.data.nodes or not self.scene.data.edges:
            title = tr('Graph is empty')
            text = tr('You should create at least one node and at least one edge')
            QMessageBox.warning(self, title, text)
            return False
        return True

    def closeEvent(self, event):
        event.accept()
        if self.shouldSave():
            event.ignore()

    def resizeEvent(self, event):
        margins = self.ui.graphicsView.contentsMargins()
        window_width = event.size().width() - margins.left() - margins.right()
        window_height = event.size().height() - self.ui.menuBar.size().height() - margins.top() - margins.bottom()
        self.scene.setSceneRect(0, 0, window_width, window_height)
        super().resizeEvent(event)

    @pyqtSlot()
    def on_actionNew_triggered(self):
        if not self.shouldSave() and self.storage.new():
            self.scene.reset()

    @pyqtSlot()
    def on_actionOpen_triggered(self):
        try:
            if not self.shouldSave():
                self.storage.open()
        except StorageError as e:
            self.handleError('Failed to open file', str(e))
        except SerializerError as e:
            self.handleError('Corrupted file', str(e))

        self.scene.reset()
        self.scene.setData(self.storage.data)

    @pyqtSlot()
    def on_actionSave_triggered(self):
        try:
            self.storage.data = self.scene.data
            self.storage.save()
        except StorageError as e:
            self.handleError('Failed to save file', str(e))

    @pyqtSlot()
    def on_actionSaveAs_triggered(self):
        self.storage.data = self.scene.data
        self.storage.saveAs()

    @pyqtSlot()
    def on_actionQuit_triggered(self):
        self.close()

    @pyqtSlot()
    def on_actionUndo_triggered(self):
        self.history.undo()

    @pyqtSlot()
    def on_actionRedo_triggered(self):
        self.history.redo()

    @pyqtSlot()
    def on_actionFind_absolute_center_triggered(self):
        if self.data_is_complete():
            limit = self.showLimitDialog()
            if limit is not None:
                try:
                    results = AbsoluteCenter(self.scene.data, limit=limit).calc()
                    self.scene.clearResults()
                    for result in results:
                        self.scene.addResult(result)
                    self.scene.update()
                except AlgorithmError as e:
                    return self.handleError(tr('Algorithm error'), tr(str(e)))

    @pyqtSlot()
    def on_actionFind_max_supply_triggered(self):
        if self.data_is_complete():
            limit = self.showLimitDialog()
            if limit is not None:
                try:
                    results = MaxSupply(self.scene.data, limit=limit).calc()
                    self.scene.clearResults()
                    for result in results:
                        self.scene.addResult(result)
                    self.scene.update()
                except AlgorithmError as e:
                    return self.handleError(tr('Algorithm error'), tr(str(e)))

    @pyqtSlot()
    def on_actionAbout_triggered(self):
        About(self).show()
