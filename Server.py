import time
from collections import deque
import json
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


    def run(self):
        # Accepting request
        self.vp.print('Initiating Server on port %s' % self.port)
        try:
            while True:
                client_soc, client_addr = self.s.accept()
                self.q.append(client_soc)
                self.vp.print('Got Client')
        except Exception as e:
            self.vp.print('Error: %s' % str(e))
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
        self.done = False
        self.waiting = False
        self.logs = None

    def run(self):
        self.client_soc.send(b'READY')

        # #### BEGIN PROTOCOL #####1

        logs = self.get_data(self.client_soc).decode('utf-8')

        # #### END PROTOCOL #####1##

        self.logs = json.loads(logs)

        # PROTOCOL COMPLETE, data has been recieved.
        # Going dormant until our data has been collected by the manager

        self.waiting = True
        self.vp.print('Finished with client')
        timeout = 100
        count = 0
        while count < timeout:
            # Sleeping 2 seconds
            self.vp.print('WAITING')
            time.sleep(2)
            count += 1

    def stop(self):
        self.vp.print('exiting')
        exit(0)


    def get_data(self, client_soc, timeout=10):
        data = []
        for x in range(timeout):
            chunk = client_soc.recv(self.pl)
            if chunk == b'':
                return b''.join(data)
            elif chunk[-4:] == b'DONE':
                data.append(chunk[:-4])
                return b''.join(data)
            else:
                data.append(chunk)
        raise ConnectionError('Error: No data recieved in %s tries' % timeout)



