#!/usr/bin/python3.6
from Printer import VerbosityPrinter as vp
import GetLog
import Client

class Manager(object):
    def __init__(self):

        self.port = 9899
        self.verbosity = 4
        self.name = 'Manager'
        self.vp = vp(self.verbosity, name=self.name)

        self.c = Client.Client(server='10.0.0.99')
        self.c.start()

if __name__ == '__main__':
    m = Manager()
