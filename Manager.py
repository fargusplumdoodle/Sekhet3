#!/usr/bin/python3.6
import json
import pdb
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

        self.logs = {}

        self.target_output_file = 'data.json'
        self.num_clients = 0

        # END CONSTRUCTOR, NOW WILL MONITOR INDEFINITELY #
        self.monitor()

    def monitor(self):
        while True:
            # ## BEGIN CLIENT HANDLING ####

            if len(self.s.q) == 0:
                time.sleep(2)
            else:
                # ONLY RAN WHEN THERE IS A QUEUE
                if len(self.s.active_clients) < self.s.max_active_clients:
                    # we have room to add another
                    client = self.s.q.popleft()
                    ch = Server.ClientHandler(client, name=self.num_clients)
                    self.s.active_clients.add(ch)
                    self.num_clients += 1
                    ch.start()

            # RAN EVERY 2 SECONDS AT MOST #

            kick = []
            for client in self.s.active_clients:
                if not client.isAlive():
                    kick.append(client)

                # Collecting info from server after it has collected it from the client(s)
                if client.waiting:
                    self.logs = client.logs
                    client.done = True
                    self.vp.print('Got logs, Number of logs: %s' % len(self.logs))
                    kick.append(client)

            for dead_client in kick:
                self.s.active_clients.remove(dead_client)

            self.process_logs()
            #print('All Logs: ', len(self.logs))

            # ## END CLIENT HANDLING ####

    def process_logs(self):
        '''Here we need to remove duplicates'''
        if len(self.logs) != 0:

            # TODO: Make so program also can accept old information

            # Writing to file
            output = open(self.target_output_file, 'w')

            len_data = len(self.logs)
            block_size = 1024

            iterate = len_data / block_size

            written = 0
            self.vp.print('Writing data to file')
            success = True
            try:
                while written < iterate:
                    start = written * block_size
                    end = start + block_size
                    written += 1
                    output.write(self.logs[start:end])
            except OSError:
                self.vp.print('Error unable to write to file')
                success = False
            finally:
                output.close()
            if success:
                self.vp.print('Successfully completed writing logs to file')
            else:
                self.vp.print('Failed to write to file, data lost')

            self.logs = []








if __name__ == '__main__':
    m = Manager()

