from functools import partial

from PyQt5.QtWidgets import QDialog, QApplication

from ui.about.About import Ui_About

_ = partial(QApplication.translate, 'About')


class About(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_About()

        self.authors = [
            'Nikita Boyarskikh <N02@yandex.ru>',
            'Zabava Alexey <zabava.alex@gmail.com>',
            'Lee Daniil <leedaniil98@gmail.com>',
            'Spasenov Ivan <spasenovivan@mail.ru>'
        ]

        self.text = _('Created by:\n')
        self.text += '\n'.join(map(_, self.authors))

        self.setupUi()

    def setupUi(self):
        self.ui.setupUi(self)
        self.ui.aboutTextLabel.setText(self.text)
