import time
from collections import deque
import NetworkingTools as nt
import socket
import threading
from Printer import VerbosityPrinter as vp

class ServerListener(threading.Thread):
    def __init__(self, port, name=0, verbose=4):
        super(ServerListener, self).__init__()

        self.pl = 1024

        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.bind_address = '0.0.0.0'

        self.s.bind((self.bind_address, self.port))
        self.s.listen(5)

        self.verbose = verbose
        self.name = 'Server-%s' % name
        self.vp = vp(verbose, name=self.name)

        self.q = deque()
        self.active_clients = set()
        self.max_active_clients = 3

        self.vp.print('Initiating Server')

    def run(self):
        # Accepting request
        try:
            while True:
                client_soc, client_addr = self.s.accept()
                self.q.append(client_soc)
        except Exception as e:
            self.vp.pritn('Error: %s' % str(e))
            self.s.close()
            exit(2)


class ClientHandler(threading.Thread):
    def __init__(self, client_soc, name=0, verbose=4):
        super(ClientHandler, self).__init__()
        self.pl = 1024
        self.client_soc = client_soc
        self.name = 'Server-' + str(name)
        self.verbose = 4
        self.vp = vp(name=self.name, v=self.verbose)

    def run(self):
        self.client_soc.send(b'READY')
        response = self.client_soc.recv(self.pl)
        if response != b'DONE':
            self.client_soc.close()
            self.vp.print('Error')




