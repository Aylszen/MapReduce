class MapReduce:

    def __init__(self, task):
        self.task = task

    @staticmethod
    def map(key, value):
        # key: document name
        # value: document contents
        print("map")
        for word in len(value.split()):
            return word, 1

    @staticmethod
    def reduce(key, values):
        # key: a word
        # values: a list of counts
        print("reduce")
        return key, sum(values)
