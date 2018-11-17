
#!/usr/bin/python4.6
import Client
import Server

class Manager(object):

    def __init__(self):

        self.port = 12345

        # Creating Client and Server Thread Objects
        s = Server.Server(self.port)
        c = Client.Client(self.port)

        # Initiating Server
        s.start()
        c.start()


if __name__ == '__main__':
    m = Manager()
