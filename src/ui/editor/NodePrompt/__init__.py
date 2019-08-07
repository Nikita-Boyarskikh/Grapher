from functools import partial

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QDialog, QColorDialog

from .NodePrompt import Ui_NodePrompt

_ = partial(QApplication.translate, 'Node Prompt')


class NodePrompt(QDialog):
    def __init__(self, parent, accept=None, reject=None, name='', weight=0.0, color=None, textColor=None):
        super().__init__(parent)
        self.name = name
        self.weight = weight
        self.color = color or QColor('black')
        self.textColor = textColor or QColor('white')

        self.ui = Ui_NodePrompt()
        self.setupUi()

        if accept:
            self.ui.buttonBox.accepted.connect(accept)
        if reject:
            self.ui.buttonBox.rejected.connect(reject)

    def setupUi(self):
        self.ui.setupUi(self)

        self.ui.nameLineEdit.setText(self.name)
        self.ui.weightDoubleSpinBox.setValue(self.weight)
        self.changeColor(self.color)
        self.changeTextColor(self.textColor)

    @staticmethod
    def reverseColor(color):
        return QColor(255 - color.red(), 255 - color.green(), 255 - color.blue())

    def changeColor(self, color):
        self.color = color
        self.ui.currentColorPushButton.setStyleSheet(
            'background-color: {backgroundColorName}; color: {colorName}'.format(
                colorName=self.reverseColor(color).name(),
                backgroundColorName=color.name()
            )
        )

    def changeTextColor(self, color):
        self.textColor = color
        self.ui.currentTextColorPushButton.setStyleSheet(
            'background-color: {backgroundColorName}; color: {colorName}'.format(
                colorName=self.reverseColor(color).name(),
                backgroundColorName=color.name()
            )
        )

    @pyqtSlot()
    def on_currentColorPushButton_pressed(self):
        color = QColorDialog.getColor(self.color, self, _('SelectColor'))
        if color.isValid():
            self.changeColor(color)

    @pyqtSlot()
    def on_currentTextColorPushButton_pressed(self):
        color = QColorDialog.getColor(self.color, self, _('Select text color'))
        if color.isValid():
            self.changeTextColor(color)

    @pyqtSlot(str)
    def on_nameLineEdit_textChanged(self, value: str):
        self.name = value

    @pyqtSlot(float)
    def on_weightDoubleSpinBox_valueChanged(self, value: float):
        self.weight = value
