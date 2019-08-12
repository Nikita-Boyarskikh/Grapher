# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './src/ui/editor/EdgePrompt/EdgePrompt.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_EdgePrompt(object):
    def setupUi(self, EdgePrompt):
        EdgePrompt.setObjectName("EdgePrompt")
        EdgePrompt.setWindowModality(QtCore.Qt.WindowModal)
        EdgePrompt.resize(400, 230)
        self.verticalWidget = QtWidgets.QWidget(EdgePrompt)
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
        self.lengthLabel = QtWidgets.QLabel(self.verticalWidget)
        self.lengthLabel.setObjectName("lengthLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.lengthLabel)
        self.lengthDoubleSpinBox = QtWidgets.QDoubleSpinBox(self.verticalWidget)
        self.lengthDoubleSpinBox.setObjectName("lengthDoubleSpinBox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lengthDoubleSpinBox)
        self.currentColorPushButton = QtWidgets.QPushButton(self.verticalWidget)
        self.currentColorPushButton.setObjectName("currentColorPushButton")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.currentColorPushButton)
        self.colorLabel = QtWidgets.QLabel(self.verticalWidget)
        self.colorLabel.setObjectName("colorLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.colorLabel)
        self.speedDoubleSpinBox = QtWidgets.QDoubleSpinBox(self.verticalWidget)
        self.speedDoubleSpinBox.setObjectName("speedDoubleSpinBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.speedDoubleSpinBox)
        self.speedLabel = QtWidgets.QLabel(self.verticalWidget)
        self.speedLabel.setObjectName("speedLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.speedLabel)
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.verticalWidget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(EdgePrompt)
        self.buttonBox.accepted.connect(EdgePrompt.close)
        self.buttonBox.rejected.connect(EdgePrompt.close)
        QtCore.QMetaObject.connectSlotsByName(EdgePrompt)

    def retranslateUi(self, EdgePrompt):
        _translate = QtCore.QCoreApplication.translate
        EdgePrompt.setWindowTitle(_translate("EdgePrompt", "Create edge"))
        self.titleLabel.setText(_translate("EdgePrompt", "Create edge"))
        self.lengthLabel.setText(_translate("EdgePrompt", "Length: "))
        self.currentColorPushButton.setText(_translate("EdgePrompt", "Change color"))
        self.colorLabel.setText(_translate("EdgePrompt", "Color: "))
        self.speedLabel.setText(_translate("EdgePrompt", "Speed: "))

