#!/usr/bin/env python3
import sys

from PyQt5.QtCore import QTranslator, QLocale, QLibraryInfo
from PyQt5.QtWidgets import QApplication

from ui.Main import Main

if __name__ == '__main__':
    # create application
    app = QApplication(sys.argv)

    # install translator
    qtTranslator = QTranslator()
    qtTranslator.load(QLocale.system().name(), QLibraryInfo.location(QLibraryInfo.TranslationsPath))
    app.installTranslator(qtTranslator)

    # create and show window
    window = Main()
    window.show()
    sys.exit(app.exec_())
