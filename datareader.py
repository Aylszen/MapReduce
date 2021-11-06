class DataReader:

    def open_file(self, path):
        self.file = open(path, "r")

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