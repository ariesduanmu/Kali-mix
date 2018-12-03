import argparse
import socket
import subprocess
import threading
import sys

class PyCat():
    def __init__(self, host, port, command, listen):
        self.buffer = b""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.command = command
        self.port = port
        self.host = host if host else '0.0.0.0'
        self.listen = listen
        self.main_func = self.nc_listen if self.listen else self.nc_connect
        print(f"main_func: {self.main_func}")
        self.main()

    def exit(self):
        self.socket.close()
        self.socket.shutdown()

    def read(self, length=1024):
        return self.socket.recv(length)

    def nc_connect(self):
        try:
            self.socket.connect((self.host, self.port))
            while True:
                recv_len = 1
                response = b""
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data
                    if recv_len < 4096:
                        break
                print(response.decode("utf-8"))
                buf = input("Input: ")
                buf += "\n"
                self.socket.send(buf.encode("utf-8"))
        except Exception as e:
            print(f"[-] Exiting...exception: {e}")
            self.socket.close()

    def nc_listen(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)

        while True:
            client_socket, addr = self.socket.accept()
            print(f"Receive client socket: {client_socket}")
            client_thread = threading.Thread(target=self.client_handler, args=(client_socket,))
            client_thread.start()

    def client_handler(self, client_socket):
        if self.command:
            client_socket.send(b"<PYCAT:#> ")
            while True:
                cmd_buf = b""
                while b"\n" not in cmd_buf:
                    cmd_buf += client_socket.recv(1024)
                response = self.exec_command(cmd_buf.decode("utf-8"))
                client_socket.send(response + b"<PYCAT:#> ")

    def exec_command(self, command):
        command = command.rstrip()
        print(f"Command: {command}")
        try:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        except:
            output = b"Failed to execute command.\n"
        return output

    def main(self):
        try:
            self.main_func()
        except KeyboardInterrupt:
            print('[!] ^C revieved, Exiting...')
        except EOFError:
            print('[!] ^D revieved, Exiting...')


def parse_arguments():
    parser = argparse.ArgumentParser(usage='%(prog)s [options]',
                                     description='PyCat',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog='Examples:\npycat -lp 443\npycat -i 127.0.0.1 -p 443 -c')
    parser.add_argument('-l', '--listen', action="store_true", help='Listen')
    parser.add_argument('-p', '--port', type=int, help='Port to listen on')
    parser.add_argument('-i', '--ip', type=str, default="localhost", help='Ip to connect to')
    parser.add_argument('-c', '--command', action="store_true", help='The command to execute')
    args = parser.parse_args()

    if (args.listen or args.ip) and not args.port:
        parser.error('Specify which port to connect to')
    elif not args.listen and not args.ip:
        parser.error('Specify --listen or --ip')
    return args

if __name__ == '__main__':
    args = parse_arguments()
    PyCat(args.ip, args.port, args.command, args.listen)


