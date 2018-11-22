import random
import time
from Printer import VerbosityPrinter as vp
import GetLog
import socket
import pdb
import json
import threading


class Client(threading.Thread):

    def __init__(self, port=9899, name=0, verbose=4):

        super(Client, self).__init__()

        self.verbose = verbose
        self.name = 'Client-%s' % name
        self.vp = vp(self.verbose, name=self.name)

        self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.pl = 1024

        self.port = port

        # TODO: use config file for this
        self.log_queries = ['UFW BLOCK', 'UFW ALLOW']

        self.logs = self.getLogs(self.log_queries)
        self.analyzeLogs()
        self.vp.print('Logs: %s' % len(self.logs))

    def analyzeLogs(self):
        for log in self.logs:
            print(log)

    def getLogs(self, log_queries):
        '''
        Gets all logs associated with the specified parameter
        :log_queries: ['str', 'str']
        '''
        logs = []
        for query in log_queries:
            logs += GetLog.GetLog(query)

        # For temperature
        logs.append(GetLog.GetTemp())

        return logs

    def run(self):
        try:
            self.c.connect( ('localhost', self.port) )

            data = self.c.recv(self.pl)
            if data != b'READY':
                raise ValueError('Invalid response from server, expecting READY')
            self.vp.print('Start')

            # #### BEGIN PROTOCOL #####1

            logs = json.dumps(self.logs)
            self.c.send(logs.encode('utf-8'))

            # #### END PROTOCOL #####1##

            self.c.send(b'DONE')
            self.vp.print('Finished')
        except Exception as e:
            self.vp.print('Error: %s' % str(e))
            self.c.close()
            exit(2)

    def get_data(self,  timeout=10):
        data = []
        for x in range(timeout):
            chunk = self.c.recv(self.pl)
            if chunk == b'':
                return b''.join(data)
            else:
                data.append(chunk)
        raise ConnectionError('Error: No data recieved in %s tries' % timeout)

