from State import State
from Token import Token
from Tokens import UNDEFINED

class Undefined(State):
    def __init__(self, input, index, line_index):
        self.input = input
        self.index = index
        self.line_index = line_index
        self.line_count = 0

    def get_token(self):
        return_token = Token(UNDEFINED, self.line_index)
        param = ''
        param += self.input[self.line_index]
        return_token.set_value(param)
        return return_token

    def get_string_value(self):
        value = ''
        is_end = False

        while not is_end:
            value += str(self.input[self.index])
            self.index += 1
            is_end = self.is_end_char(self.index)

        return value

    def is_end_char(self, index):
        return self.input[index] is '\n' or self.input[index] is ' '