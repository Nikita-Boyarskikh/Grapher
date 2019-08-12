from functools import partial

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QDialog, QColorDialog

from utils import reverseColor
from .EdgePrompt import Ui_EdgePrompt

_ = partial(QApplication.translate, 'Edge Prompt')


class EdgePrompt(QDialog):
    def __init__(self, parent, accept=None, reject=None, length=0.0, speed=0.0, color=None):
        super().__init__(parent)
        self.length = length
        self.speed = speed
        self.color = color or QColor('black')

        self.ui = Ui_EdgePrompt()
        self.setupUi()

        if accept:
            self.ui.buttonBox.accepted.connect(accept)
        if reject:
            self.ui.buttonBox.rejected.connect(reject)

    def setupUi(self):
        self.ui.setupUi(self)

        self.ui.lengthDoubleSpinBox.setValue(self.length)
        self.ui.speedDoubleSpinBox.setValue(self.speed)
        self.changeColor(self.color)

    def changeColor(self, color):
        self.color = color
        self.ui.currentColorPushButton.setStyleSheet(
            'background-color: {backgroundColorName}; color: {colorName}'.format(
                colorName=reverseColor(color).name(),
                backgroundColorName=color.name()
            )
        )

    @pyqtSlot()
    def on_currentColorPushButton_pressed(self):
        color = QColorDialog.getColor(self.color, self, _('Select color'))
        if color.isValid():
            self.changeColor(color)

    @pyqtSlot(float)
    def on_lengthDoubleSpinBox_valueChanged(self, value: float):
        self.length = value

    @pyqtSlot(float)
    def on_speedDoubleSpinBox_valueChanged(self, value: float):
        self.speed = value
