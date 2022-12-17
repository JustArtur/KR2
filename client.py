import socket
import sys
import PyQt6.QtWidgets as qtw
from functools import partial


class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calculator')
        self.setLayout(qtw.QVBoxLayout())
        self._generate_keypad()
        self.server = ClientSocket()
        self.show()

    def _generate_keypad(self):
        container = qtw.QWidget()
        container.setLayout(qtw.QGridLayout())

        buttons = [
            ["7", "8", "9", "/", "C"],
            ["4", "5", "6", "*", "("],
            ["1", "2", "3", "-", ")"],
            ["0", "00", ".", "+", "="],
        ]
        # creating result_field
        self.result_field = qtw.QLineEdit()
        container.layout().addWidget(self.result_field, 0, 0, 1, 5)
        # creating history button
        hist_btn = qtw.QPushButton('History')
        hist_btn.clicked.connect(self._display_history)
        container.layout().addWidget(hist_btn, 1, 0, 1, 5)
        # creating buttons
        for row, values in enumerate(buttons):
            for column, value in enumerate(values):
                btn = qtw.QPushButton(value)
                btn.clicked.connect(partial(self._button_press, value))
                container.layout().addWidget(btn, row+2, column)
        self.layout().addWidget(container)

    def _button_press(self, value):
        if value == '=':
            self._display_result()
            return
        self._clear() if value == 'C' else self._display_text(value)
        

    def _display_text(self, value):
        self.result_field.setText(self.result_field.text()+value)

    def _clear(self):
        self.result_field.setText('')

    def _display_history(self):
        self.server.send_data('hist')
        history = self.server.recieve_data()
        self.result_field.setText(history)

    def _display_result(self):
        self.server.send_data(self.result_field.text())
        self.result_field.setText(self.result_field.text() + '=' + self.server.recieve_data())


class ClientSocket():
    def __init__(self):
        self.server = socket.socket()
        self.connect()

    def connect(self):
        self.server.connect(('127.0.0.1', 3000))

    def send_data(self, data):
        self.server.send(data.encode())
        print(f"Sending {data}...")

    def recieve_data(self):
        data = self.server.recv(1024).decode()
        print(f"Client get {data}")
        return data





app = qtw.QApplication([])
mw = MainWindow()
app.exec()