import multiprocessing
import socket
import pickle
from messages import *


class WorkerProcess(multiprocessing.Process):
    def __init__(self, name, host, port, server_host, server_port):
        super().__init__()
        self.name = name
        self.host = host
        self.port = port
        self.is_connected = False
        self.server_host = server_host
        self.server_port = server_port
        self.server = (self.server_host, self.server_port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        print(name, "was created, ip: ", self.host, "port: ", self.port)

    def connect(self):
        message = Message(self.host, self.port, self.name)
        data_string = pickle.dumps(message)

        while True:
            if not self.is_connected:
                self.sock.sendto(data_string, self.server)
                data, address = self.sock.recvfrom(1024)
                response = pickle.loads(data)
                if response.response.SUCCESSFUL:
                    self.is_connected = True
                    print("Good job: ", response.response)

    def run(self):
        self.connect()




