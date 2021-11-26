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
    def __init__(self, host, port, path, path_map, path_reduce, num_of_workers):
        super().__init__()
        self.worker_machines_in_use = []
        self.host = host
        self.port = port
        self.num_of_workers = num_of_workers
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        print("Server Started: ", self.host, ", port: ", self.port)
        self.worker_machines = []
        self.path = path
        self.path_map = path_map
        self.path_reduce = path_reduce
        self.map_tasks = []

    def listen(self):
        while True:
            data, address = self.sock.recvfrom(1024)
            message = pickle.loads(data)
            if message.message_type == enums.MessageType.SETUP:
                print("Worker connected: ", address)
                self.worker_machines.append((message.ip, message.port))
                response = ResponseMessage(enums.Response.SUCCESSFUL)
                data_string = pickle.dumps(response)
                self.sock.sendto(data_string, address)
                if self.num_of_workers == len(self.worker_machines):
                    self.assign_tasks()
            if message.message_type == enums.MessageType.COMPLETE_TASK:
                self.complete_task(address)
                self.assign_tasks()

    def run(self):
        threading.Thread(target=self.listen, args=()).start()
        self.create_map_tasks()

    def create_map_tasks(self):
        files = next(walk(self.path), (None, None, []))[2]  # [] if no file
        for file in files:
            self.map_tasks.append(Task(enums.TaskTypes.MAP, self.path + file, self.path_map, enums.State.IDLE, enums.TaskTypes.NONE))

    def assign_tasks(self):

        for map_task in self.map_tasks:
            if map_task.state == enums.State.IDLE:
                if map_task.worker == enums.TaskTypes.NONE:
                    for worker in self.worker_machines:
                        if worker not in self.worker_machines_in_use:
                            map_task.worker = worker
                            self.worker_machines_in_use.append(worker)
                            task_message = TaskMessage(enums.TaskTypes.MAP, map_task.path_read, map_task.path_save)
                            data_string = pickle.dumps(task_message)
                            self.sock.sendto(data_string, (worker[0], worker[1]))
                            map_task.state = enums.State.IN_PROGRESS
                            break

    def complete_task(self, worker):
        for map_task in self.map_tasks:
            if map_task.state == enums.State.IN_PROGRESS:
                map_task.state = enums.State.COMPLETED
                self.worker_machines_in_use.remove(map_task.worker)
