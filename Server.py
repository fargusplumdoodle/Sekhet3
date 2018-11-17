import time
import socket
import threading
from Printer import VerbosityPrinter as vp


class Server(threading.Thread):
    def __init__(self, port, name=0, verbose=4):
        super(Server, self).__init__()

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.bind_address = '0.0.0.0'
        self.port = port

        self.verbose = verbose
        self.name = 'Server-%s' % name
        self.vp = vp(verbose, name=self.name)


        self.s.bind( ( self.bind_address, self.port) )
        self.s.listen(5)
        self.vp.print('Initiating Server')

    def run(self):
        while True:
            # Accepting request
            self.vp.print('waiting for client')
            client_soc, client_addr = self.s.accept()

            # Sending to handle client
            self.handleClient(client_soc)

    def handleClient(self, client_soc):
        self.print('Got client')
        client_soc.send(b'READY')



