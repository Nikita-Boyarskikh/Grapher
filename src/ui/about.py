from functools import partial

from PyQt5.QtWidgets import QApplication, QMessageBox

from utils.html import p, link, ul, li

_ = partial(QApplication.translate, 'About')


class About:
    def __init__(self, parent):
        self.parent = parent

    def show(self):
        title = _('About')
        authors_with_emails = {
            'Nikita Boyarskikh': 'N02@yandex.ru',
            'Zabava Alexey': 'zabava.alex@gmail.com',
            'Lee Daniil': 'leedaniil98@gmail.com',
            'Spasenov Ivan': 'spasenovivan@mail.ru'
        }

        text = p(_('Created by:\n'))
        text += ul(
            ''.join(
                li(
                    _(name) + ' ' + link('&lt;' + email + '&gt;', href='mailto:' + email)
                ) for name, email in authors_with_emails.items()
            )
        )

        QMessageBox.about(self.parent, title, text)
