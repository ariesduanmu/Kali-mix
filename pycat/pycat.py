#! /usr/bin/env python3
import argparse
import subprocess
import threading
import socket
import sys
import ssl
import os
import tempfile
import datetime

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes

class PyCat():
    def __init__(self, host, port, execute, listen, verbose, ssl_mode=True):
        self.buffer = b""
        self.listen = listen
        self.ssl = ssl_mode
        if self.ssl:
            if self.listen:
                self.keypath, self.certpath = self.generate_cert()
                self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
                self.context.load_cert_chain(self.certpath, self.keypath)
            else:
                self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                self.context.check_hostname = False
                self.context.verify_mode = ssl.CERT_NONE
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.exec = execute
        self.port = port
        self.verbose = verbose
        self.host = host or '0.0.0.0'
        self.main_func = self.nc_listen if self.listen else self.nc_connect
        self.main()

    def exit(self):
        self.sock.close()
        os.remove(self.cert_file)
        os.remove(self.key_file)
        # self.socket.shutdown(socket.SHUT_RDWR)

    def generate_cert(self):
        _, keypath = tempfile.mkstemp()
        _, certpath = tempfile.mkstemp()
        key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

        with open(keypath, "wb") as f:
            f.write(key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            ))
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"CA"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, u"San Francisco"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"My Company"),
            x509.NameAttribute(NameOID.COMMON_NAME, u"mysite.com"),
        ])
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            # Our certificate will be valid for 10 days
            datetime.datetime.utcnow() + datetime.timedelta(days=10)
        ).add_extension(
            x509.SubjectAlternativeName([x509.DNSName(u"localhost")]),
            critical=False,
        # Sign our certificate with our private key
        ).sign(key, hashes.SHA256(), default_backend())
        # Write our certificate out to disk.
        with open(certpath, "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
        return keypath, certpath

    def read(self, length=1024):
        return self.socket.recv(length)

    def nc_connect(self):
        try:
            self.sock.connect((self.host, self.port))
            if self.ssl:
                self.sock = self.context.wrap_socket(self.sock)
                while True:
                    buf = input("Input: ")
                    buf += "\n"
                    self.sock.send(buf.encode("utf-8"))

                    recv_len = 1
                    response = b""
                    while recv_len:
                        data = self.sock.recv(4096)
                        recv_len = len(data)
                        response += data
                        if recv_len < 4096:
                            break
                    print(response.decode("utf-8"))
               
        except Exception as e:
            print(f"[-] Exiting...exception: {e}")

    def nc_listen(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)

        if self.ssl:
            self.sock = self.context.wrap_socket(self.sock, server_side=True)
        
        while True:
            conn, addr = self.sock.accept()
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
        cmd = f"{self.exec} {command}"
        if self.exec == "/bin/bash" or self.exec == "/bin/sh":
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
    parser.add_argument('-s', '--ssl', action="store_true", help='Encrypt connection')
    parser.add_argument('-p', '--port', type=int, help='Port to listen on')
    parser.add_argument('-i', '--ip', type=str, default="localhost", help='Ip to connect to')
    parser.add_argument('-e', '--exec', type=str, default="/bin/echo", help='progress to exec client\'s command')
    args = parser.parse_args()

    return args.ip, args.port, args.exec, args.listen, args.verbose, args.ssl

if __name__ == '__main__':
    PyCat(*parse_arguments())


