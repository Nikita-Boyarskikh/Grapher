from functools import partial

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QDialog, QColorDialog

from .NodePrompt import Ui_NodePrompt

_ = partial(QApplication.translate, 'Node Prompt')


class NodePrompt:
    def __init__(self):
        self.color = QColor('black')
        self.textColor = QColor('white')
        self.ui = Ui_NodePrompt()

    def changeColor(self, color):
        self.color = color
        self.ui.currentColorLabel.setText(color.name())
        self.ui.currentColorLabel.setStyleSheet('color: ' + color.name())
        self.ui.currentColorPushButton.setStyleSheet('background-color: ' + color.name())

    def changeTextColor(self, color):
        self.textColor = color
        self.ui.currentTextColorLabel.setText(color.name())
        self.ui.currentTextColorLabel.setStyleSheet('color: ' + color.name())
        self.ui.currentTextColorPushButton.setStyleSheet('background-color: ' + color.name())

    def onCurrentColorPushButtonPressed(self):
        color = QColorDialog.getColor(self.color, _('SelectColor'))
        self.changeColor(color)

    def onCurrentTextColorPushButtonPressed(self):
        color = QColorDialog.getColor(self.color, _('Select text color'))
        self.changeTextColor(color)

    def show(self, parent, accept, reject):
        dialog = QDialog(parent)
        self.ui.setupUi(dialog)

        self.ui.currentColorPushButton.pressed.connect(self.onCurrentColorPushButtonPressed)
        self.ui.currentTextColorPushButton.pressed.connect(self.onCurrentTextColorPushButtonPressed)
        self.ui.buttonBox.accepted.connect(accept)
        self.ui.buttonBox.rejected.connect(reject)

        dialog.show()
