from functools import partial

from PyQt5.QtWidgets import QApplication, QMessageBox

_ = partial(QApplication.translate, 'About')


class About:
    def __init__(self, parent):
        self.parent = parent

    def show(self):
        title = _('About')
        authors = [
            'Nikita Boyarskikh <N02@yandex.ru>',
            'Zabava Alexey <zabava.alex@gmail.com>',
            'Lee Daniil <leedaniil98@gmail.com>',
            'Spasenov Ivan <spasenovivan@mail.ru>'
        ]

        text = _('Created by:\n')
        text += '\n'.join(map(_, authors))

        QMessageBox.about(self.parent, title, text)
