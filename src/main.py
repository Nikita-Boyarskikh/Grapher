#!/usr/bin/env python3
import sys
import fix_qt_import_error

from PyQt5.QtCore import QTranslator, QLocale, QLibraryInfo
from PyQt5.QtWidgets import QApplication

from ui.Main import Main

if __name__ == '__main__':
    # create application
    app = QApplication(sys.argv)

    # install translator
    qtSystemTranslator = QTranslator()
    qtSystemTranslator.load(QLocale.system().name(), QLibraryInfo.location(QLibraryInfo.TranslationsPath))
    qtTranslator = QTranslator()
    qtTranslator.load(QLocale.system().name() + '.qm', 'translations')
    app.installTranslator(qtTranslator)
    app.installTranslator(qtSystemTranslator)

    # create and show window
    window = Main()
    window.show()
    sys.exit(app.exec_())
