#!/usr/bin/env python3
import zmq
import threading
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QTextEdit,
                             QLineEdit, QVBoxLayout, QHBoxLayout)


class Phantoms(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "Phantoms"
        self.left = 0
        self.top = 0
        self.width = 640
        self.height = 480

        self.message_input = QLineEdit()
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.text_display.setFontPointSize(12)
        self.text_display.setFontFamily("Arial")

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.message_input)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.text_display)
        self.vbox.addLayout(self.hbox)

        self.setLayout(self.vbox)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)
        self.show()


class Client(Phantoms):
    def __init__(self, username, rhost, port_req, port_sub):
        super().__init__()
        self.message_input.returnPressed.connect(lambda: self.send_message())

        self.username = username
        self.rhost = rhost
        self.port_req = port_req
        self.port_sub = port_sub

        context = zmq.Context()
        self.client_req = context.socket(zmq.REQ)
        self.client_req.connect("tcp://{}:{}".format(rhost, port_req))

        self.client_sub = context.socket(zmq.SUB)
        self.client_sub.setsockopt(zmq.SUBSCRIBE, b"")
        self.client_sub.connect("tcp://{}:{}".format(rhost, port_sub))

        messaging_thread = threading.Thread(target=self.get_message)
        messaging_thread.start()

    def send_message(self):
        message = self.message_input.text()
        self.client_req.send_pyobj((self.username, message))
        server_response = self.client_req.recv_string()
        if server_response != "OK":
            pass
        self.message_input.clear()

    def get_message(self):
        while True:
            username, message = self.client_sub.recv_pyobj()
            self.text_display.append("{} : {}".format(username, message))


if __name__ == "__main__":
    username = input("Username ? : ")
    phantoms = QApplication(sys.argv)
    ex = Client(username, '127.0.0.1', 8080, 8081)
    sys.exit(phantoms.exec())
