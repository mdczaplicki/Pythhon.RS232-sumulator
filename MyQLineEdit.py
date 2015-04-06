__author__ = 'Marek'
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class MyQLineEdit(QLineEdit):
    def __init__(self, method):
        super(MyQLineEdit, self).__init__()
        self.abc = method()

    def keyPressEvent(self, k):
        if k.key() == Qt.Key_Enter:
            self.abc()