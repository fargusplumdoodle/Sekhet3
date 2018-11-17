
import time
from Printer import VerbosityPrinter as vp
import socket
import threading


class Client(threading.Thread):

    def __init__(self, port, name=0, verbose=4):
        super(Client, self).__init__()



        self.verbose = verbose
        self.name = 'Client-%s' % name
        self.vp = vp(self.verbose, name=self.name)

        self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port
        self.c.connect( ('localhost', self.port) )
        self.pl = 1024

        self.vp.print('Waiting for connection', 4)
        data = self.get_data()

        self.vp.print(data, 4)
        self.vp.print(type(data), 4)



    def get_data(self, timeout=10):
        data = []
        for x in range(timeout):
            chunk = self.c.recv(self.pl)
            if chunk == b'':
                return b''.join(data)
            else:
                data.append(chunk)
        raise ConnectionError('Error: No data recieved in %s tries' % timeout)

