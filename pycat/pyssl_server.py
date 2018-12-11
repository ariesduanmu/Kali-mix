# -*- coding: utf-8 -*-
# @Author: ariesduanmu
# @Date:   2018-12-10 20:10:49
# @Last Modified by:   ariesduanmu
# @Last Modified time: 2018-12-11 23:10:49
import socket, ssl, os
import datetime

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes

HOST, PORT, CERT, KEY = 'localhost', 8888, 'server_2.crt', 'server_2.key'

def generate_cert(keypath, certpath):
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    with open(keypath, "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.BestAvailableEncryption(b"passphrase"),
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


def handle(conn):
    print(conn.recv())
    conn.write('HTTP/1.1 200 OK\n\n{}'.format(conn.getpeername()[0]).encode())

def main():

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(CERT, KEY)
    # context.check_hostname = False
    # context.verify_mode = ssl.CERT_NONE

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        sock.bind((HOST, PORT))
        sock.listen(5)
        with context.wrap_socket(sock, server_side=True) as ssock:
            while True:
                conn, addr = ssock.accept()
                try:
                    handle(conn)
                except ssl.SSLError as e:
                    print(e)
                finally:
                    conn.close()

if __name__ == '__main__':
    if not os.path.exists(KEY) or not os.path.exists(CERT):
        generate_cert(KEY, CERT)
    main()