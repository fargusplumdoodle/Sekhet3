import random
import time
from Printer import VerbosityPrinter as vp
import GetLog
import socket
import pdb
import json
import threading
import Printer


class Client(threading.Thread):

    def __init__(self, port=9899, server='localhost' ,name=0, verbose=4):

        super(Client, self).__init__()

        self.verbose = verbose
        self.name = 'Client-%s' % name
        self.vp = vp(self.verbose, name=self.name)

        self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.pl = 1024
        self.server = server
        self.port = port

        print('connecting to %s:%s' % (self.server, self.port))
        # TODO: use config file for this
        self.log_queries = ['UFW BLOCK', 'UFW ALLOW']

        #self.logs =
        self.sysInfo = {
            'hostname': GetLog.GetHostname(),
            'battery': GetLog.GetBattery(),
            'temp': GetLog.GetTemp(),
            'totalblocks': 0
        }
        self.ufw = {}
        self.analyzeLogs()

    def analyzeLogs(self):
        '''
        This function just sorts all of the information gathered about the ufw blocks
        :return:
        '''
        logs = self.getLogs(self.log_queries)

        # TODO: shrink IPV6 addresses

        for log in logs:
            # creating entry if it does not exist
            if log['src'] not in self.ufw:
                self.ufw[log['src']] = {
                    'freq': 0,
                    'times': []
                }

            # recording information about what may be some jerk trying to get into
            # my laptop but most likely is just some program thats bugging out
            self.ufw[log['src']]['freq'] += 1
            self.ufw[log['src']]['times'].append(log['date'])
            self.ufw[log['src']]['port'] = log['port']

            self.sysInfo['totalblocks'] += 1

            try:
                self.ufw[log['src']]['hostname'] = socket.gethostbyaddr(log['src'])
            except:
                self.ufw[log['src']]['hostname'] = 'No reverse lookup address specified'

    def getLogs(self, log_queries):
        '''
        Gets all logs associated with the specified parameter
        :log_queries: ['str', 'str']
        '''
        logs = []
        for query in log_queries:
            logs += GetLog.GetData(query)
        return logs

    def run(self):
        try:
            while True:
                try:
                    if self.port > 9949:
                        self.vp.print('Failed to connect to server')
                        exit(-1)

                    self.c.connect( (self.server, self.port) )
                    break
                except ConnectionError as e:
                    self.vp.print('Initialization failed, attempting next port: %s' % self.port)
                    self.port += 1

            data = self.c.recv(self.pl)
            if data != b'READY':
                raise ValueError('Invalid response from server, expecting READY')
            self.vp.print('Start')

            # #### BEGIN PROTOCOL #####1

            payload = {
                'ufw': self.ufw,
                'sys': self.sysInfo
            }
            Printer.print_json(payload)
            payload = json.dumps(payload)
            self.c.send(payload.encode('utf-8'))

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

