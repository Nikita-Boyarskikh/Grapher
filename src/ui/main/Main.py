# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './src/ui/main/Main.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Main(object):
    def setupUi(self, Main):
        Main.setObjectName("Main")
        Main.resize(808, 579)
        self.graphicsView = QtWidgets.QGraphicsView(Main)
        self.graphicsView.setEnabled(False)
        self.graphicsView.setObjectName("graphicsView")
        self.menuBar = QtWidgets.QMenuBar(Main)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 808, 22))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menuBar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        Main.setMenuBar(self.menuBar)
        self.actionSaveAs = QtWidgets.QAction(Main)
        self.actionSaveAs.setEnabled(False)
        self.actionSaveAs.setObjectName("actionSaveAs")
        self.actionLoad = QtWidgets.QAction(Main)
        self.actionLoad.setObjectName("actionLoad")
        self.actionOpen = QtWidgets.QAction(Main)
        self.actionOpen.setObjectName("actionOpen")
        self.actionNew = QtWidgets.QAction(Main)
        self.actionNew.setObjectName("actionNew")
        self.actionSave = QtWidgets.QAction(Main)
        self.actionSave.setEnabled(False)
        self.actionSave.setObjectName("actionSave")
        self.actionClose = QtWidgets.QAction(Main)
        self.actionClose.setEnabled(False)
        self.actionClose.setObjectName("actionClose")
        self.actionQuit = QtWidgets.QAction(Main)
        self.actionQuit.setObjectName("actionQuit")
        self.actionUndo = QtWidgets.QAction(Main)
        self.actionUndo.setObjectName("actionUndo")
        self.actionRedo = QtWidgets.QAction(Main)
        self.actionRedo.setObjectName("actionRedo")
        self.actionAbout = QtWidgets.QAction(Main)
        self.actionAbout.setObjectName("actionAbout")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSaveAs)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClose)
        self.menuFile.addAction(self.actionQuit)
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)
        self.menuHelp.addAction(self.actionAbout)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuEdit.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(Main)
        QtCore.QMetaObject.connectSlotsByName(Main)

    def retranslateUi(self, Main):
        _translate = QtCore.QCoreApplication.translate
        Main.setWindowTitle(_translate("Main", "Grapher"))
        self.menuFile.setTitle(_translate("Main", "File"))
        self.menuEdit.setTitle(_translate("Main", "Edit"))
        self.menuHelp.setTitle(_translate("Main", "Help"))
        self.actionSaveAs.setText(_translate("Main", "Save as..."))
        self.actionLoad.setText(_translate("Main", "Load..."))
        self.actionOpen.setText(_translate("Main", "Open..."))
        self.actionNew.setText(_translate("Main", "New..."))
        self.actionSave.setText(_translate("Main", "Save"))
        self.actionClose.setText(_translate("Main", "Close"))
        self.actionQuit.setText(_translate("Main", "Quit"))
        self.actionUndo.setText(_translate("Main", "Undo"))
        self.actionRedo.setText(_translate("Main", "Redo"))
        self.actionAbout.setText(_translate("Main", "About"))

