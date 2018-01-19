#!/usr/bin/python3


class ConfigFile(object):
    def __init__(self, file_path):
        # define all members.
        self.file_path = file_path
        self.file_object = open(file_path, 'r+')
        self.current_line = 0
        self.log_file = ""
        self.log_file_path = ""
        self.live_dir = 0
        self.grade_log_file = 0
        self.out_file = 0
        self.file_contents = self.file_object.readline(10000)

        # initialize file.
        self.parse_config_file()
        self.file_object.close()

    # end __init__

    def parse_config_file(self):
        self.current_line = int(self.file_object.readline()[13:].strip('\n'))
        self.log_file_path = self.file_object.readline()[9:].strip('\n')
        self.log_file = open(self.log_file_path, 'r')
        self.live_dir = self.file_object.readline()[9:].strip('\n')
        self.grade_log_file = self.file_object.readline()[10:].strip('\n')
        self.out_file = self.file_object.readline()[9:].strip('\n')

        # init log file:
        i = 0
        while i < self.current_line:
            self.log_file.readLine()

    # end parse_config_file

    def log_file(self):
        return self.log_file

    def closed(self):
        self.file_object = open(self.file_path, 'r+')
        if self.file_object.closed:
            return True
        else:
            self.file_object.close()
            return False

    # end closed

    def set_current_line(self, new_line):
        self.current_line = new_line
        self.write_file()

    def increment_current_line(self):
        self.current_line = self.current_line + 1
        self.write_file()

    # end increment_current_line

    def write_file(self):
        self.file_object = open(self.file_path, 'w')

        str_current_line = 'CURRENT_LINE:' + str(self.current_line)
        str_log_file = 'LOG_FILE:' + str(self.log_file_path)
        str_live_dir = 'LIVE_DIR:' + str(self.live_dir)
        str_grade_log = 'GRADE_LOG:' + str(self.grade_log_file)
        str_out_file = 'OUT_FILE:' + str(self.out_file)
        string_to_write = "\n".join([str_current_line, str_log_file, str_live_dir, str_grade_log, str_out_file])

        self.file_object.write(string_to_write)

        self.file_object.close()

    # end write_file
