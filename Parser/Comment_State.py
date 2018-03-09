LINE_COMMENT = 0
BLOCK_COMMENT = 1

from State import State
from Token import Token
from Tokens import COMMENT


class Comment_State(State):
    def __init__(self, input, index, line_index):
        self.input = input
        self.index = index
        self.line_index = line_index
        self.type = LINE_COMMENT
        self.line_count = 0

    def get_Token(self):
        return_token = Token(COMMENT, self.line_index)
        begin_index = self.index

        if self.input[self.index] == '/':
            self.index += 1

            if self.input[self.index] == '/':
                self.type = LINE_COMMENT
            elif self.input[self.index] == '*':
                self.type = BLOCK_COMMENT
            else:
                print("COMMENT STATE ERROR!")
                exit(1)

            if self.type is LINE_COMMENT:
                self.index += 1

                if not self.increment_line_length():
                    return self.undefined(self.get_string_value(begin_index), self.line_index, self.line_count)

                return_token.set_value(self.get_string_value(begin_index))
                return_token.set_line_count(self.line_count)

                return return_token
            elif self.type is BLOCK_COMMENT:
                self.index += 1

                if not self.increment_block_length():
                    return self.undefined(self.get_string_value(begin_index), self.line_index, self.line_count)

                return_token.set_value(self.get_string_value(begin_index))
                return_token.set_line_count(self.line_count)
                return return_token
            else:
                return self.undefined(self.get_string_value(begin_index), self.line_index, self.line_count)
        else:
            return self.reject()

    def increment_block_length(self):
        while self.index < len(self.input) and self.input[self.index] != '*':

            if self.input[self.index] is '\n':
                self.line_count += 1

            self.index += 1

        if self.index < len(self.input):

            self.index += 1

            if self.index < len(self.input) and self.input[self.index] == '/':
                self.index += 1
                return True

            return self.increment_block_length()

        return False

    def increment_line_length(self):
        while self.index < len(self.input) and self.input[self.index] != '\n':
            self.index += 1
        return True

    def get_string_value(self, begin_index):
        return_value = ''
        while begin_index < self.index:
            return_value += str(self.input[begin_index])
            begin_index += 1
        return return_value
