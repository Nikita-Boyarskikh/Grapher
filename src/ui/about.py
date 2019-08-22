from functools import partial

from PyQt5.QtWidgets import QMessageBox, QApplication

from utils.html import p, link, ul, li

tr = partial(QApplication.translate, '@default')


class About:
    def __init__(self, parent):
        self.parent = parent

    def show(self):
        title = tr('About')
        authors_with_emails = {
            tr('Nikita Boyarskikh'): 'N02@yandex.ru',
            tr('Zabava Alexey'): 'zabava.alex@gmail.com',
            tr('Lee Daniil'): 'chuvag01@gmail.com',
            tr('Spasenov Ivan'): 'spasenovivan@mail.ru'
        }

        text = p(tr('Created by:\n'))
        text += ul(
            ''.join(
                li(
                    tr(name) + ' ' + link('&lt;' + email + '&gt;', href='mailto:' + email)
                ) for name, email in authors_with_emails.items()
            )
        )

        QMessageBox.about(self.parent, title, text)
