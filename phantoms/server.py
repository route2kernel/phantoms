#!/usr/bin/env python3
import zmq


class Server():
    def __init__(self, port_rep, port_pub):
        self.port_rep = port_rep
        self.port_pub = port_pub

        context = zmq.Context()

        self.socket_rep = context.socket(zmq.REP)
        self.socket_pub = context.socket(zmq.PUB)
        self.socket_rep.bind("tcp://*:{}".format(self.port_rep))
        self.socket_pub.bind("tcp://*:{}".format(self.port_pub))

    def run(self):
        while True:
            username, message = self.socket_rep.recv_pyobj()
            self.socket_rep.send_string("OK")
            print("received message...")

            self.socket_pub.send_pyobj((username, message))
            print("message broadcasted!")


if __name__ == "__main__":
    chat = Server(8080, 8081)
    chat.run()
