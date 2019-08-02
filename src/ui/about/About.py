# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './src/ui/about/About.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_About(object):
    def setupUi(self, About):
        About.setObjectName("About")
        About.resize(500, 300)
        self.aboutTextLabel = QtWidgets.QLabel(About)
        self.aboutTextLabel.setGeometry(QtCore.QRect(0, 0, 500, 300))
        self.aboutTextLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.aboutTextLabel.setObjectName("aboutTextLabel")

        self.retranslateUi(About)
        QtCore.QMetaObject.connectSlotsByName(About)

    def retranslateUi(self, About):
        _translate = QtCore.QCoreApplication.translate
        About.setWindowTitle(_translate("About", "About"))
        self.aboutTextLabel.setText(_translate("About", "TextLabel"))

