# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './src/ui/Main/Main.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Main(object):
    def setupUi(self, Main):
        Main.setObjectName("Main")
        Main.resize(808, 579)
        Main.setAcceptDrops(True)
        self.graphicsView = QtWidgets.QGraphicsView(Main)
        self.graphicsView.setMouseTracking(True)
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
        self.menuRun = QtWidgets.QMenu(self.menuBar)
        self.menuRun.setObjectName("menuRun")
        Main.setMenuBar(self.menuBar)
        self.actionSaveAs = QtWidgets.QAction(Main)
        self.actionSaveAs.setObjectName("actionSaveAs")
        self.actionOpen = QtWidgets.QAction(Main)
        self.actionOpen.setObjectName("actionOpen")
        self.actionNew = QtWidgets.QAction(Main)
        self.actionNew.setObjectName("actionNew")
        self.actionSave = QtWidgets.QAction(Main)
        self.actionSave.setObjectName("actionSave")
        self.actionQuit = QtWidgets.QAction(Main)
        self.actionQuit.setObjectName("actionQuit")
        self.actionUndo = QtWidgets.QAction(Main)
        self.actionUndo.setObjectName("actionUndo")
        self.actionRedo = QtWidgets.QAction(Main)
        self.actionRedo.setObjectName("actionRedo")
        self.actionAbout = QtWidgets.QAction(Main)
        self.actionAbout.setObjectName("actionAbout")
        self.actionFind_absolute_center = QtWidgets.QAction(Main)
        self.actionFind_absolute_center.setObjectName("actionFind_absolute_center")
        self.actionFind_max_supply = QtWidgets.QAction(Main)
        self.actionFind_max_supply.setObjectName("actionFind_max_supply")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSaveAs)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)
        self.menuHelp.addAction(self.actionAbout)
        self.menuRun.addAction(self.actionFind_absolute_center)
        self.menuRun.addAction(self.actionFind_max_supply)
        self.menuRun.addAction(Main.actionClear)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuEdit.menuAction())
        self.menuBar.addAction(self.menuRun.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(Main)
        QtCore.QMetaObject.connectSlotsByName(Main)

    def retranslateUi(self, Main):
        _translate = QtCore.QCoreApplication.translate
        Main.setWindowTitle(_translate("Main", "Grapher"))
        self.menuFile.setTitle(_translate("Main", "File"))
        self.menuEdit.setTitle(_translate("Main", "Edit"))
        self.menuHelp.setTitle(_translate("Main", "Help"))
        self.menuRun.setTitle(_translate("Main", "Run"))
        self.actionSaveAs.setText(_translate("Main", "Save as..."))
        self.actionOpen.setText(_translate("Main", "Open..."))
        self.actionNew.setText(_translate("Main", "New..."))
        self.actionSave.setText(_translate("Main", "Save"))
        self.actionQuit.setText(_translate("Main", "Quit"))
        self.actionUndo.setText(_translate("Main", "Undo"))
        self.actionRedo.setText(_translate("Main", "Redo"))
        self.actionAbout.setText(_translate("Main", "About"))
        self.actionFind_absolute_center.setText(_translate("Main", "Find absolute center"))
        self.actionFind_max_supply.setText(_translate("Main", "Find maximal supply"))

