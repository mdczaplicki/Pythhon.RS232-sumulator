__author__ = 'Marekaaaa'

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import binascii as ba
import sys

a = QApplication(sys.argv)


class Server(QWidget):
    def __init__(self):
        super(Server, self).__init__()
        self.initialize_user_interface()

    grid_layout = QGridLayout()
    icon = QIcon("icon.png")

    text_label = QLabel()
    text_box = QTextEdit()
    text_button = QPushButton()

    bin_label = QLabel()
    bin_box = QTextEdit()
    bin_button = QPushButton()

    def initialize_user_interface(self):
        self.setWindowTitle("RS232 Simulator")
        self.setLayout(self.grid_layout)
        self.setMaximumSize(300, 350)
        self.setMinimumSize(300, 350)
        self.setWindowIcon(self.icon)
        self.resize(300, 350)
        self.show()

        self.text_label.setText("Text to send:")
        self.grid_layout.addWidget(self.text_label, 0, 0)

        self.text_box.setFixedHeight(25)
        self.grid_layout.addWidget(self.text_box, 1, 0)
        self.text_box.setFocus()

        self.text_button.setText("Convert")
        self.text_button.clicked.connect(self.convert_to_bin)
        self.grid_layout.addWidget(self.text_button, 2, 0)

        self.bin_label.setText("Converted text:")
        self.grid_layout.addWidget(self.bin_label, 3, 0)

        self.bin_box.setReadOnly(True)
        self.bin_box.viewport().setCursor(Qt.ArrowCursor)
        self.bin_box.setStyleSheet("QTextEdit, QLineEdit {"
                                   "background-color: #d0d0d0;"
                                   "}")
        self.grid_layout.addWidget(self.bin_box, 4, 0)

        self.bin_button.setText("Send")
        self.grid_layout.addWidget(self.bin_button, 5, 0)

    @staticmethod
    def check_dictionary(temp_text) -> str:
        file = open("dict.txt", mode='r')
        for line in file.readlines():
            line = line[:-1]
            if line in temp_text.lower():
                temp_text = temp_text.replace(line, "*" * len(line))
        return temp_text

    @staticmethod
    def text_to_ascii(temp_text) -> list:
        out = []
        for i in temp_text:
            out.append(ord(i))
        return out

    @staticmethod
    def ascii_to_bin(temp_list) -> str:
        out = ""
        for i in temp_list:
            out += '1' + bin(i)[2:] + '11'
        return out

    def convert_to_bin(self):
        """ Step by step for every conversion process."""
        temp_text = self.text_box.toPlainText()
        temp_text = self.check_dictionary(temp_text)
        temp_text = self.text_to_ascii(temp_text)
        temp_text = self.ascii_to_bin(temp_text)
        self.bin_box.setText(temp_text)


s = Server()

sys.exit(a.exec())