class LogFile(object):
    def __init__(self, file_name):
        self.file = open(file_name, 'r')
        self.file_contents = list()

        while True:
            current_line = self.file.readline()
            if current_line == "":
                break

            split_string = current_line.split(',')
            self.file_contents.append(split_string)
