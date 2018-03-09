from Tokens import *

class Token(object):
    def __init__(self, l_type, line):
        self.type = l_type
        self.line = line
        self.line_count = 0
        self.value = ""

    def set_type(self, l_type):
        self.type = l_type
    
    def set_value(self, value):
        self.value = value

    def get_line_count(self):
        return self.line_count

    def set_line_count(self, line_count):
        self.line_count = line_count

    def string_size(self):
        return len(self.value)
