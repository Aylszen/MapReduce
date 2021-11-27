import sys
from datareader import DataReader
from collections import Counter
import time


class MapReduce:

    def __init__(self, task):
        self.task = task

    @staticmethod
    def map(value):
        # value: document contents
        map_list = []
        for word in value.split():
            map_list.append((word, 1))
        return map_list

    @staticmethod
    def reduce(key, values):
        # key: a word
        # values: a list of counts
        return key, sum(values)

    @staticmethod
    def combine(value):
        # value: document contents
        unique = []
        [unique.append(item) for item in value if item not in unique]
        counter = Counter(value)
        value_dict = counter.items()
        for elem in value_dict:
            unique_ind = unique.index(elem[0])
            temp_list = list(unique[unique_ind])
            temp_list[1] = elem[1]
            unique[unique_ind] = tuple(temp_list)
        return unique


def run(argv):
    #input_data = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Aliquam etiam erat velit scelerisque. Faucibus purus in massa tempor. Pellentesque habitant morbi tristique senectus et. Viverra orci sagittis eu volutpat odio facilisis mauris. Pharetra et ultrices neque ornare. Viverra suspendisse potenti nullam ac tortor vitae purus. Justo laoreet sit amet cursus sit. Tempus imperdiet nulla malesuada pellentesque elit eget gravida cum. Vulputate dignissim suspendisse in est ante in nibh. Volutpat lacus laoreet non curabitur. Amet cursus sit amet dictum sit. Morbi leo urna molestie at elementum eu facilisis sed. Rutrum tellus pellentesque eu tincidunt tortor aliquam. Id neque aliquam vestibulum morbi blandit."
    task = argv[0]
    path_read = argv[1]
    path_save = argv[2]
    path_save_map = "map_files/"

    if task.upper() == "MAP":
        data_reader = DataReader()
        data_reader.open_file(path_read, "r")
        input_data = data_reader.file.read()
        result = MapReduce.map(input_data)
        data_reader = DataReader()
        data_reader.open_file(path_save_map + path_read.split("/")[1], "w")
        data_reader.save_map_to_file(result)
        data_reader.close_file()

    elif task.upper() == "REDUCE":
        data_reader = DataReader()
        data_reader.open_file(path_read, "r")
        map_data = data_reader.read_map_from_file()
        data_reader.close_file()
        reduce_result = []
        #for map_elem in map_data:
        #    print(type(map_elem))
        #    print(map_elem[0])
        #    print(map_elem[1])
        #    reduce_result.append(MapReduce.reduce(map_elem[0], map_elem[1]))

    elif task.upper() == "COMBINE":
        data_reader = DataReader()
        data_reader.open_file(path_save, "r")
        map_data = data_reader.read_map_from_file()
        result = MapReduce.combine(map_data)
        data_reader.close_file()
        #data_reader.open_file("map_files/map_file_1.txt","w")
        data_reader.save_map_to_file(result)


if __name__ == '__main__':
    run(sys.argv[1:])
