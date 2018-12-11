# -*- coding: utf-8 -*-
# @Author: ariesduanmu
# @Date:   2018-12-10 19:53:25
# @Last Modified by:   ariesduanmu
# @Last Modified time: 2018-12-11 14:50:47
import socket, ssl

HOST, PORT, SERVERCERT = "localhost", 8888, 'server_2.crt'
HOSTNAME = "mysite.com"
def handle(conn):
    conn.write(b"GET / HTTP/1.1\n")
    print(conn.recv().decode())

def main():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations(SERVERCERT)

    with socket.create_connection((HOST, PORT)) as sock:
        with context.wrap_socket(sock, server_hostname=HOSTNAME) as ssock:
            print(ssock.version())
            try:
                handle(ssock)
            finally:
                ssock.close()

if __name__ == "__main__":
    main()