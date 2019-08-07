# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './src/ui/editor/NodePrompt/NodePrompt.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_NodePrompt(object):
    def setupUi(self, NodePrompt):
        NodePrompt.setObjectName("NodePrompt")
        NodePrompt.setWindowModality(QtCore.Qt.WindowModal)
        NodePrompt.resize(400, 230)
        self.verticalWidget = QtWidgets.QWidget(NodePrompt)
        self.verticalWidget.setGeometry(QtCore.QRect(10, 10, 380, 200))
        self.verticalWidget.setObjectName("verticalWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.titleLabel = QtWidgets.QLabel(self.verticalWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleLabel.sizePolicy().hasHeightForWidth())
        self.titleLabel.setSizePolicy(sizePolicy)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setObjectName("titleLabel")
        self.verticalLayout.addWidget(self.titleLabel)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout.setObjectName("formLayout")
        self.nameLabel = QtWidgets.QLabel(self.verticalWidget)
        self.nameLabel.setObjectName("nameLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.nameLabel)
        self.nameLineEdit = QtWidgets.QLineEdit(self.verticalWidget)
        self.nameLineEdit.setObjectName("nameLineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.nameLineEdit)
        self.weightLabel = QtWidgets.QLabel(self.verticalWidget)
        self.weightLabel.setObjectName("weightLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.weightLabel)
        self.weightDoubleSpinBox = QtWidgets.QDoubleSpinBox(self.verticalWidget)
        self.weightDoubleSpinBox.setObjectName("weightDoubleSpinBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.weightDoubleSpinBox)
        self.colorLabel = QtWidgets.QLabel(self.verticalWidget)
        self.colorLabel.setObjectName("colorLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.colorLabel)
        self.textColorLabel = QtWidgets.QLabel(self.verticalWidget)
        self.textColorLabel.setObjectName("textColorLabel")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.textColorLabel)
        self.currentColorPushButton = QtWidgets.QPushButton(self.verticalWidget)
        self.currentColorPushButton.setObjectName("currentColorPushButton")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.currentColorPushButton)
        self.currentTextColorPushButton = QtWidgets.QPushButton(self.verticalWidget)
        self.currentTextColorPushButton.setObjectName("currentTextColorPushButton")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.currentTextColorPushButton)
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.verticalWidget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(NodePrompt)
        self.buttonBox.accepted.connect(NodePrompt.close)
        self.buttonBox.rejected.connect(NodePrompt.close)
        QtCore.QMetaObject.connectSlotsByName(NodePrompt)

    def retranslateUi(self, NodePrompt):
        _translate = QtCore.QCoreApplication.translate
        NodePrompt.setWindowTitle(_translate("NodePrompt", "Add node"))
        self.titleLabel.setText(_translate("NodePrompt", "Create node"))
        self.nameLabel.setText(_translate("NodePrompt", "Name: "))
        self.weightLabel.setText(_translate("NodePrompt", "Weight: "))
        self.colorLabel.setText(_translate("NodePrompt", "Color: "))
        self.textColorLabel.setText(_translate("NodePrompt", "Text color: "))
        self.currentColorPushButton.setText(_translate("NodePrompt", "Change color"))
        self.currentTextColorPushButton.setText(_translate("NodePrompt", "Change color"))

