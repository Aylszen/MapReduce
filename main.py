import os
import multiprocessing
from worker import Worker
from task import Task
from masterprocess import *
from clientprocess import *
from datareader import DataReader
M = 5  # Number of Map tasks/processes
R = 5  # Number of Reduce tasks/processes

if __name__ == '__main__':
    data_reader = DataReader()
    data_reader.open_file('input_files/lorem_ipsum_20_paragraphs.txt')
    splitted_file = data_reader.split_file_by_lines()
    data_reader.close_file()

    # Establish communication queues
    #tasks = multiprocessing.JoinableQueue()
    #results = multiprocessing.Queue()

    # Start workers
    #num_workers = 5
    #print('Creating %d workers' % num_workers)
    #workers = [Worker(tasks, results) for i in range(num_workers)]

    #for w in workers:
    #    w.start()

    # Enqueue jobs
    #num_jobs = 10
    #for i in range(num_jobs):
    #    tasks.put(Task(1))

    # Add a poison pill for each consumer
    #for i in range(num_workers):
    #    tasks.put(None)

    #tasks.join()
    #while num_jobs:
    #    result = results.get()
    #    print('Result:', result)
    #    num_jobs -= 1

    host = '192.168.1.104'  # client/server ip
    port1 = 4002
    port2 = 4006

    master = MasterProcess(host, port1)
    master.start()
    client = WorkerProcess(host, port2, host, port1)
    client.start()
