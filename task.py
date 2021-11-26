import time
from enums import TaskTypes
from mapreduce import *


class Task(object):
    def __init__(self, task_type, path_read, path_save, state, worker):
        self.task_type = task_type
        self.path_read = path_read
        self.path_save = path_save
        self.state = state
        self.worker = worker

    def __call__(self):
        time.sleep(0.5)  # pretend to take some time to do the work
        if self.task_type == TaskTypes.MAP:
            MapReduce.map()
        elif self.task_type == TaskTypes.REDUCE:
            MapReduce.reduce()
        return "DONE"

    def __str__(self):
        return '%s' % self.task_type
