from State import State
from Token import Token
from Tokens import ID


class Id_State(State):
    def __init__(self, input, index, line_index):
        self.input = input
        self.index = index
        self.line_index = line_index

    def get_end_index(self, i):
        while self.is_char_accepted(i) and not self.is_space(self.input[i]):
            i += 1
        return i

    def get_string(self, input, begin_index, end_index):
        value = ''

        while begin_index < end_index:
            value += str(input[begin_index])
            begin_index += 1

        return value

    def get_token(self):
        if not str(self.input[self.index]).isalpha():
            return self.reject()

        end_index = self.get_end_index(self.index)

        id_token = Token(ID, self.line_index)
        id_token.set_value(self.get_string(self.input, self.index, end_index))
        return id_token

    def is_space(self, value):
        if value == ' ' or value == '\n' or value == '\r' or value == '\t':
            return True
        return False

    def is_char_accepted(self, i):
        return str(i).isalpha() or str(i).isdigit()
