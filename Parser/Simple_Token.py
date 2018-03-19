from State import State
from Token import Token
from Tokens import *


class Simple_Token(State):
    def __init__(self, input, index, line_index):
        self.input = input
        self.index = index
        self.line_index = line_index

    def get_token(self):
        input_string = ''
        input_string = str(self.input[self.index])

        if str(input_string[0]).isalpha():
            input_string = self.get_string_value()

        input_string = self.get_string_if_colon(input_string)

        l_type = self.lookup_symbol(input_string)

        if l_type is not None:
            simple_token = Token(l_type, self.line_index)
            simple_token.set_value(input_string)
            return simple_token

        return self.reject()

    def get_string_if_colon(self, original_string):
        if original_string is ":":
            if self.index + 1 < len(self.input) and self.input[self.index + 1] is '-':
                self.index += 1
                original_string += self.input[self.index]

        return original_string

    def get_string_value(self):
        input_string = ''
        begin_index = self.index
        self.index = self.get_end_index(self.index)

        while begin_index < self.index:
            input_string += str(self.input[begin_index])
            begin_index += 1

        return input_string

    def get_end_index(self, i):
        while str(self.input[i]).isalpha():
            i += 1
        return i

    def lookup_symbol(self, value):
        if value is ",":
            return COMMA
        elif value is ".":
            return PERIOD
        elif value is "?":
            return Q_MARK
        elif value is "(":
            return LEFT_PAREN
        elif value is ")":
            return RIGHT_PAREN
        elif value is ":":
            return COLON
        elif value is ":-":
            return COLON_DASH
        elif value is "*":
            return MULTIPLY
        elif value is "+":
            return ADD
        elif value is "main":
            return MAIN
        elif value is "int":
            return INT
        elif value is "function":
            return FUNCTION
        elif value is "class":
            return CLASS
        elif value is "void":
            return VOID
        elif value is "const":
            return CONST
        elif value is "return":
            return RETURN
        elif value is "float":
            return FLOAT
        elif value is "double":
            return DOUBLE
        elif value is "namespace":
            return NAMESPACE
        elif value is "std":
            return STD
        elif value is "string":
            return STRING
        elif value is "char":
            return CHAR
        elif value is "unsigned":
            return UNSIGNED
        elif value is "static":
            return STATIC
        elif value is " ":
            return WHITESPACE
        elif value is "\n":
            return NEW_LINE
        elif value is "\t":
            return WHITESPACE
        else:
            return None
