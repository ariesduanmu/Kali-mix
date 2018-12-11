#! /usr/bin/env python3
import argparse
import subprocess
import threading
import socket
import sys
import ssl

class PyCat():
    def __init__(self, host, port, execute, listen, verbose, ssl_mode=True, keypath="server_2.key", certpath="server_2.crt", hostname="mysite.com"):
        self.buffer = b""
        self.listen = listen
        self.ssl = ssl_mode
        self.keypath = keypath
        self.certpath = certpath
        self.execute = execute
        self.port = port
        self.verbose = verbose
        self.host = host or '0.0.0.0'
        self.hostname = hostname
        
        self.main_func = self.nc_listen if self.listen else self.nc_connect
        self.main()

    def exit(self):
        pass
        # self.socket.close()
        # self.socket.shutdown(socket.SHUT_RDWR)

    def read(self, length=1024):
        return self.socket.recv(length)

    def nc_connect(self):
        try:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            context.load_verify_locations(self.certpath)

            with socket.create_connection((self.host, self.port)) as sock:
                with context.wrap_socket(sock, server_hostname=self.hostname) as ssock:
                    print(ssock.version())
                    try:
                        while True:
                            buf = input("Input: ")
                            buf += "\n"
                            ssock.send(buf.encode("utf-8"))

                            recv_len = 1
                            response = b""
                            while recv_len:
                                data = ssock.recv(4096)
                                recv_len = len(data)
                                response += data
                                if recv_len < 4096:
                                    break
                            print(response.decode("utf-8"))
                    finally:
                        ssock.close()                
        except Exception as e:
            print(f"[-] Exiting...exception: {e}")

    def nc_listen(self):
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(self.certpath, self.keypath)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
            sock.bind((self.host, self.port))
            sock.listen(5)
            with context.wrap_socket(sock, server_side=True) as ssock:
                while True:
                    conn, addr = ssock.accept()
                    try:
                        if self.verbose:
                            print(f"Receive client socket: {conn}")
                        while True:
                            cmd_buf = b""
                            while b"\n" not in cmd_buf:
                                cmd_buf += conn.recv(1024)
                            # TODO: can't capture client exit
                            if len(cmd_buf) == 0:
                                break
                            response = self.exec_command(cmd_buf.decode("utf-8"))
                            conn.send(response)
                        if self.verbose:
                            print(f"Closing: {conn}")
                        conn.close()

                        # client_thread = threading.Thread(target=self.client_handler, args=(conn,))
                        # client_thread.start()
                    except ssl.SSLError as e:
                        print(e)
                    finally:
                        conn.close()

    def client_handler(self, client_socket):
        while True:
            cmd_buf = b""
            while b"\n" not in cmd_buf:
                cmd_buf += client_socket.recv(1024)
            # TODO: can't capture client exit
            if len(cmd_buf) == 0:
                break
            response = self.exec_command(cmd_buf.decode("utf-8"))
            client_socket.send(response)
        if self.verbose:
            print(f"Closing: {client_socket}")
        client_socket.close()

    def exec_command(self, command):
        command = command.rstrip()
        print(command)
        cmd = f"{self.execute} {command}"
        if self.execute == "/bin/bash" or self.execute == "/bin/sh":
            cmd = command
        output, stderr = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).communicate()
        if stderr:
            output = b"Failed to execute command." + stderr + b"\n"
        return output

    def main(self):
        try:
            self.main_func()
        except KeyboardInterrupt:
            self.exit()
            print('[!] ^C revieved, Exiting...')
        except EOFError:
            self.exit()
            print('[!] ^D revieved, Exiting...')

# nc -l 8000
# cat /tmp/fifo | nc localhost 8000 | nc -l 9000 > /tmp/fifo
# nc -n 192.168.1.102 9000


def parse_arguments():
    parser = argparse.ArgumentParser(usage='%(prog)s [options]',
                                     description='PyCat',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog='Examples:\npycat -lp 443\npycat -i 127.0.0.1 -p 443 -c')
    parser.add_argument('-l', '--listen', action="store_true", help='Listen')
    parser.add_argument('-v', '--verbose', action="store_true", help='verbose')
    parser.add_argument('-p', '--port', type=int, help='Port to listen on')
    parser.add_argument('-i', '--ip', type=str, default="localhost", help='Ip to connect to')
    parser.add_argument('-e', '--exec', type=str, default="/bin/echo", help='progress to exec client\'s command')
    args = parser.parse_args()

    return args

if __name__ == '__main__':
    args = parse_arguments()
    PyCat(args.ip, args.port, args.exec, args.listen, args.verbose)


