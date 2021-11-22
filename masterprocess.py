import multiprocessing
import socket
import pickle
import threading

import enums
from messages import *


class MasterProcess(multiprocessing.Process):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        print("Server Started: ", self.host, ", port: ", self.port)

    def listen(self):
        while True:
            data, address = self.sock.recvfrom(1024)
            message = pickle.loads(data)
            if message.message_type == enums.MessageType.SETUP:
                print("Worker connected: ", address)
                response = ResponseMessage(enums.Response.SUCCESSFUL)
                data_string = pickle.dumps(response)
                self.sock.sendto(data_string, address)

    def run(self):
        threading.Thread(target=self.listen, args=()).start()
