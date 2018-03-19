from State import State
from Token import Token
from Tokens import STRING

class String_State(State):
    def __init__(self, input, index, line_index):
        self.input = input
        self.index = index
        self.line_index = line_index
        self.line_count = 0

    def get_token(self):
        begin_index = self.index
        if self.input[self.index] is '\"':
            if not self.increment_string_length():
                return self.undefined(self.get_string_value(begin_index), self.line_index, self.line_count)
            
            return_token = Token(STRING, self.line_index)
            return_token.set_line_count(self.line_count)
            return_token.set_value(self.get_string_value(begin_index))
            return return_token
        return self.reject()     

    def increment_string_length(self):
        self.index += 1
        while self.index < len(self.input) and self.input[self.index] is not '\"':
            if self.input[self.index] == '\n':
                self.line_count += 1
            self.index += 1
        if self.index < len(self.input):
            self.index += 1
            if self.index < len(self.input) and self.input[self.index] is '\"':
                return self.increment_string_length()
            return True
        return False

    def get_string_value(self, begin_index):
        return_value = ''
        while begin_index < len(self.input) and begin_index < self.index:
            return_value += str(self.input[begin_index])
            begin_index += 1
        return return_value
