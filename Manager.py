#!/usr/bin/python3.6
import threading
import Client
import Server
import time
from Printer import VerbosityPrinter as vp

class Manager(object):
    def __init__(self):

        self.port = 9899
        self.verbosity = 4
        self.name = 'Manager'
        self.vp = vp(self.verbosity, name=self.name)
        self.servers = []

        # Creating Client and Server Thread Objects
        while True:
            try:
                self.s = Server.ServerListener(port=self.port)
                break
            except OSError as e:
                self.vp.print('Initialization failed, attempting next port: %s' % self.port)
                self.port += 1

        # Initiating Server
        self.vp.print('Starting Server')
        self.s.start()

        self.logs = []

        self.num_clients = 0
        self.monitor()

    def monitor(self):
        while True:
            # ## BEGIN CLIENT HANDLING ####
            if len(self.s.q) == 0:
                time.sleep(2)
            else:
                if len(self.s.active_clients) < self.s.max_active_clients:
                    # we have room to add another
                    client = self.s.q.popleft()
                    ch = Server.ClientHandler(client, name=self.num_clients)
                    self.s.active_clients.add(ch)
                    self.num_clients += 1
                    ch.start()

            kick = []
            for client in self.s.active_clients:
                if not client.isAlive():
                    kick.append(client)

                if client.waiting:
                    self.logs += client.logs
                    self.vp.print('Got logs, Number of logs: %s' % len(self.logs))
                    client.stop()
                    kick.append(client)

            for dead_client in kick:
                self.s.active_clients.remove(dead_client)

            # ## END CLIENT HANDLING ####





if __name__ == '__main__':
    m = Manager()

