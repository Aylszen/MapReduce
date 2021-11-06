import os
import multiprocessing

from datareader import DataReader
M = 5  # Number of Map tasks/processes
R = 5  # Number of Reduce tasks/processes

if __name__ == '__main__':
    data_reader = DataReader()
    data_reader.open_file('input_files/lorem_ipsum_20_paragraphs.txt')
    splitted_file = data_reader.split_file_by_lines()
    data_reader.close_file()

    # Establish communication queues
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()

    # Start workers
