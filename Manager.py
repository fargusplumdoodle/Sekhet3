#!/usr/bin/python4.6
import threading
import Client
import Server
import time
from Printer import VerbosityPrinter as vp
from collections import deque
import socket

class Manager(object):

    def __init__(self):

        self.port = 12345
        self.verbosity = 2
        self.name = 'Manager'
        self.vp = vp(self.verbosity, name=self.name)
        self.clients = set()
        self.servers = []


        # Creating Client and Server Thread Objects
        while True:
            try:
                self.s = Server.ServerListener(port=self.port)
                break
            except OSError as e:
                self.vp.print('Initialization failed, attempting next port: %s' % self.port)
                self.port += 1

        self.createClients(10)

        # Initiating Server
        self.vp.print('Starting Server')
        self.s.start()
        self.vp.print('Starting Clients')
        self.startClients()

        self.monitor()

    def createClients(self, numClients):
        for x in range(numClients):
            self.clients.add(Client.Client(name=x, port=self.port))

    def startClients(self):
        for client in self.clients:
            client.start()

    def monitor(self):
        while True:
            if len(self.s.q) == 0:
                time.sleep(2)
                continue

            if len(self.s.active_clients) < self.s.max_active_clients:
                # we have room to add another
                client = self.s.q.popleft()
                ch = Server.ClientHandler(client)
                self.s.active_clients.add(ch)
                ch.start()

            kick = []
            for client in self.s.active_clients:
                if not client.isAlive():
                    kick.append(client)

            for dead_client in kick:
                self.s.active_clients.remove(dead_client)
if __name__ == '__main__':
    m = Manager()
