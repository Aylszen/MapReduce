import os
import multiprocessing
from worker import Worker
from task import Task
from masterprocess import *
from workerprocess import *
from datareader import DataReader
M = 5  # Number of Map tasks/processes
R = 5  # Number of Reduce tasks/processes

if __name__ == '__main__':
    data_reader = DataReader()
    data_reader.open_file('input_files/lorem_ipsum_20_paragraphs.txt', "r")
    splitted_file = data_reader.split_file_by_lines()
    data_reader.close_file()
    for i in range(len(splitted_file)):
        data_reader.open_file('splitted_files/split' + str(i) + '.txt', "w")
        data_reader.save_file(splitted_file[i])
        data_reader.close_file()

    host = '192.168.1.104'  # client/server ip
    port = 4000
    path_split = 'splitted_files/'
    path_map = 'map_files/'
    path_reduce = 'reduce/'
    path_shuffle = 'shuffle/'

    master = MasterProcess(host, port, path_split, path_map, path_reduce, path_shuffle, M)
    master.start()
    workers = []
    for i in range(M):
        client = WorkerProcess("Worker" + str(i + 1), host, port + i + 1, host, port)
        client.start()
        workers.append(client)


