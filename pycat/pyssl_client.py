# -*- coding: utf-8 -*-
# @Author: ariesduanmu
# @Date:   2018-12-10 19:53:25
# @Last Modified by:   ariesduanmu
# @Last Modified time: 2018-12-11 09:41:24
import socket, ssl

HOST, PORT, SERVERCERT = "localhost", 8888, 'server.crt'

def handle(conn):
    conn.write(b"GET / HTTP/1.1\n")
    print(conn.recv().decode())

def main():
    sock = socket.socket(socket.AF_INET)
    conn = ssl.wrap_socket(sock,
                           ca_certs=SERVERCERT,
                           cert_reqs=ssl.CERT_REQUIRED)
    try:
        conn.connect((HOST, PORT))
        handle(conn)
    finally:
        conn.close()

if __name__ == "__main__":
    main()