#!/usr/bin/env python3
import sys
import socket
import socketserver


class ForwardServer(socketserver.ThreadingTCPServer):
    daemon_threads = True
    allow_reuse_address = True

class BaseHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            try:
                data = self.receive(self.request)
                print(data)
                self.transock.send(data)
                remote_data = self.receive(self.transock)
                print(remote_data)
                self.request.send(remote_data)
            except:
                break

    def receive(self, sock):
        response = b""
        recv_len = 1
        while recv_len:
            data = sock.recv(4096)
            recv_len = len(data)
            response += data
            if recv_len < 4096:
                break
        return response

def port_forward(local_port, forward_sock):
    class SubHandler(BaseHandler):
        transock = forward_sock

    ForwardServer(('localhost', local_port), SubHandler).serve_forever()

if __name__ == "__main__":
    remote_host = sys.argv[1]
    remote_port = int(sys.argv[2])
    local_port = int(sys.argv[3])

    forward_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    forward_sock.connect((remote_host, remote_port))

    port_forward(local_port, forward_sock)


