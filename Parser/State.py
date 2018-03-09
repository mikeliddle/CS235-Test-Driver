from Token import Token
from States import *
from Tokens import *

class State(object):

    def __init__(self, input, index, line_index):
        self.input = input
        self.index = index
        self.line_index = line_index
        pass

    def get_token(self):
        pass

    def reject(self):
        pass
    
    def undefined(self, value, line_index, line_count):
        undefined_token = Token(UNDEFINED, line_index)
        undefined_token.set_line_count(line_count)
        undefined_token.set_value(value)
        return undefined_token
