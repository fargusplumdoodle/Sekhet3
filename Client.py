
import socket
import threading


class Client(threading.Thread):

    def __init__(self, port):
        super(Server, self).__init__()

        self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port
        self.c.connect('localhost', self.port)
        self.pl = 1024

        print('Waiting for connection')
        self.c.get_data()

    def get_data(self, timeout=10):
        data = []
        for x in range(timeout):
            chunk = self.c.recv(self.pl)
            if chunk == b'':
                return b''.join(data)
            else:
                data.append(chunk)
            count += 1
        raise ConnectionError('Error: No data recieved in %s tries' % timeout)

