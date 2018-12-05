# -*- coding: utf-8 -*-
import socket


class SocketConnection():
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port

    def run_server(self, connections=5):
        self.sock.bind((self.host, self.port))
        self.sock.listen(connections)
        while True:
            client_socket, addr = self.sock.accept()
            client_thread = threading.Thread(target=self.server_client_handler, args=(client_socket,))
            client_thread.start()

    def run_client(self):
        self.sock.connect((self.host, self.port))
        self.client_action()

    def server_client_handler(self, client_socket):
        pass

    def client_action(self):
        pass

    def close(self):
        self.sock.close()

