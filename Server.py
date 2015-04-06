__author__ = 'Marek'

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import binascii as ba
import sys

a = QApplication(sys.argv)


class MyQLineEdit(QLineEdit):
    def __init__(self):
        super(MyQLineEdit, self).__init__()

    def keyPressEvent(self, k):
        if k.key() == Qt.Key_Return or k.key() == Qt.Key_Enter:
            s.convert_to_bin()
        QLineEdit.keyPressEvent(self, k)


class MyQWidget(QWidget):
    def __init__(self):
        super(MyQWidget, self).__init__()
        self.setWindowIcon(self.icon)

    icon = QIcon("icon.png")


class Client(MyQWidget):
    def __init__(self):
        super(Client, self).__init__()
        self.initialize_user_interface()

    grid_layout = QGridLayout()
    text_box = QTextEdit()
    text_label = QLabel()

    def initialize_user_interface(self):
        self.setWindowTitle("RS232 Simulator - Client")
        self.setLayout(self.grid_layout)
        self.setMaximumSize(300, 200)
        self.setMinimumSize(300, 200)
        self.resize(300, 200)
        self.move(50, 50)
        self.show()

        self.text_label.setText("Received text:")
        self.grid_layout.addWidget(self.text_label)

        self.text_box.setReadOnly(True)
        self.text_box.viewport().setCursor(Qt.ArrowCursor)
        self.text_box.setStyleSheet("QTextEdit, QLineEdit {"
                                    "background-color: #d0d0d0;"
                                    "}")
        self.grid_layout.addWidget(self.text_box)

c = Client()


class Server(MyQWidget):
    def __init__(self):
        super(Server, self).__init__()
        self.initialize_user_interface()

    grid_layout = QGridLayout()

    text_box = MyQLineEdit()
    text_label = QLabel()
    text_button = QPushButton()

    bin_label = QLabel()
    bin_box = QTextEdit()
    bin_button = QPushButton()

    def initialize_user_interface(self):
        self.setWindowTitle("RS232 Simulator - Server")
        self.setLayout(self.grid_layout)
        self.setMaximumSize(300, 350)
        self.setMinimumSize(300, 350)
        self.resize(300, 350)
        self.show()

        self.text_label.setText("Text to send:")
        self.grid_layout.addWidget(self.text_label, 0, 0)

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
        self.bin_button.clicked.connect(self.convert_to_text)
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
            out += '1' + '0' * (8 - len(bin(i)[2:])) + bin(i)[2:] + '11'
        return out

    def convert_to_bin(self):
        """ Step by step for every conversion process."""
        temp_text = self.text_box.displayText()
        temp_text = self.check_dictionary(temp_text)
        temp_text = self.text_to_ascii(temp_text)
        temp_text = self.ascii_to_bin(temp_text)
        self.bin_box.setText(temp_text)

    @staticmethod
    def remove_start_stop(temp_text) -> str:
        return ''.join('' if i % 11 in [0, 9, 10]
                       else char for i, char in enumerate(temp_text))

    @staticmethod
    def bin_to_ascii(temp_text) -> list:
        temp_list = []
        for i in range(int(len(temp_text) / 8)):
            temp_list.append(int(temp_text[i*8:i*8+8], 2))
        print(temp_list)

    def convert_to_text(self):
        c.text_box.setText(self.bin_to_ascii(self.remove_start_stop(self.bin_box.toPlainText())))

s = Server()

sys.exit(a.exec())