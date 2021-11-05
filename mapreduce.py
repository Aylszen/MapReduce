class MapReduce:

    def __init__(self, task):
        self.task = task

    @staticmethod
    def map(key, value):
        # key: document name
        # value: document contents
        print("map")

    @staticmethod
    def reduce(key, values):
        # key: a word
        # values: a list of counts
        print("reduce")
