from enum import Enum


class TaskTypes(Enum):
    MAP = 1
    REDUCE = 2


class State(Enum):
    IDLE = 1
    IN_PROGRESS = 2
    COMPLETED = 3
