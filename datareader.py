from os import walk

class DataReader:

    def open_file(self, path, mode):
        self.file = open(path, mode)

    def split_file_by_lines(self):
        content = self.file.read()
        content_list = content.splitlines()
        return content_list

    def close_file(self):
        self.file.close()

    @staticmethod
    def remove_empty_lines(path):
        with open(path, 'r+') as fd:
            lines = fd.readlines()
            fd.seek(0)
            fd.writelines(line for line in lines if line.strip())
            fd.truncate()

    def save_map_to_file(self, data_list):
        for element in data_list:
            self.file.write(str(element[0]) + " " + str(element[1]) + '\n')

    def read_map_from_file(self):
        data_list = []
        lines = self.file.readlines()
        for line in lines:
            line_split = line.split()
            data_list.append((line_split[0], int(line_split[1])))
        return data_list

    def save_file(self, content):
        self.file.write(content)

    @staticmethod
    def read_all_file_names_from_location(path_read):
        return next(walk(path_read), (None, None, []))[2]  # [] if no file


