
import socket
import threading


class Server(threading.Thread):
    def __init__(self, port):
        super(Server, self).__init__()

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.bind_address = '0.0.0.0'
        self.port = port

        self.s.bind(self.bind_address, self.port)
        self.s.listen(5)

    def run(self):
        while True:
            client_soc, client_addr = self.s.accept()


    def handleClient(self, client_soc):
        client_soc.send(b'READY')


