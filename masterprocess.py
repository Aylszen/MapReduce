import multiprocessing
import socket
import pickle
import threading
from os import listdir
from os.path import isfile, join
from os import walk
import enums
from messages import *
from task import Task


class MasterProcess(multiprocessing.Process):
    def __init__(self, host, port, path):
        super().__init__()
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        print("Server Started: ", self.host, ", port: ", self.port)
        self.worker_machines = []
        self.path = path
        self.map_tasks = []

    def listen(self):
        while True:
            data, address = self.sock.recvfrom(1024)
            message = pickle.loads(data)
            if message.message_type == enums.MessageType.SETUP:
                print("Worker connected: ", address)
                self.worker_machines.append((message.ip, message.port, message.name))
                print(self.worker_machines)
                response = ResponseMessage(enums.Response.SUCCESSFUL)
                data_string = pickle.dumps(response)
                self.sock.sendto(data_string, address)

    def run(self):
        threading.Thread(target=self.listen, args=()).start()
        self.create_map_tasks()

    def create_map_tasks(self):
        #files = [f for f in listdir(self.path) if isfile(join(self.path), f)]
        files = next(walk(self.path), (None, None, []))[2]  # [] if no file
        for file in files:
            self.map_tasks.append(Task(enums.TaskTypes.MAP, self.path + file, enums.State.IDLE))
        print(files)
        print(self.map_tasks)
