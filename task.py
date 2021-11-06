import time
from enums import TaskTypes
from mapreduce import *


class Task(object):
    def __init__(self, task_type):
        self.task_type = task_type

    def __call__(self):
        if self.task_type == TaskTypes.MAP:
            MapReduce.map()
            time.sleep(2)  # pretend to take some time to do the work
        elif self.task_type == TaskTypes.REDUCE:
            MapReduce.reduce()
        return "DONE"

    def __str__(self):
        return '%s' % self.task_type
