from States import *
from Tokens import NEW_LINE, WHITESPACE, COMMENT, MY_EOF
from Token import Token
from Comment_State import Comment_State
from Id_State import Id_State


class Lexer(object):
    def __init__(self):
        self.file_line_index = 0
        self.current_line_index = 1
        self.tokens = list()
        self.nextState = TOKEN_STATE

    def analyze_file(self, file_name):
        input = self.get_file_as_string(file_name)
        index = 0

        while index != len(input):
            token = self.get_token(input, index)
            if self.nextState is NO_STATE:
                if token is not None:
                    index += token.string_size()
                    self.current_line_index += token.get_line_count()

                    if token.get_type() is NEW_LINE:
                        self.current_line_index += 1
                        token = None
                    elif token.get_type() is WHITESPACE and token.get_type() is not COMMENT:
                        self.tokens.append(token)
                    else:
                        token = None
                    self.nextState = TOKEN_STATE
                else:
                    index += 1
                    self.nextState = TOKEN_STATE

        end_of_file = Token(MY_EOF, self.current_line_index)
        self.tokens.append(end_of_file)

    def get_token(self, input, index):
        new_token = None
        current_state = None

        if self.nextState is TOKEN_STATE:
            current_state = SimpleToken(input, index, self.current_line_index)
            new_token = self.get_token_from_state(input, index, current_state)

            if new_token is not None:
                self.nextState = NO_STATE

        if self.nextState is ID_STATE:
            current_state = Id_State(input, index, self.current_line_index)
            new_token = self.get_token_from_state(input, index, current_state)

            if new_token is not None:
                self.nextState = NO_STATE

        elif self.nextState is STRING_STATE:
            current_state = String_State(input, index, self.current_line_index)
            new_token = self.get_token_from_state(input, index, current_state)

            if new_token is not None:
                self.nextState = NO_STATE

        elif self.nextState is COMMENT_STATE:
            current_state = Comment_State(
                input, index, self.current_line_index)
            new_token = self.get_token_from_state(input, index, current_state)

            if new_token is not None:
                self.nextState = NO_STATE

        else:
            current_state = Undefined(input, index, self.current_line_index)
            new_token = current_state.get_token()

        return new_token

    def get_token_from_state(self, input, index, currentState):
        new_token = None
        if currentState is not None:
            new_token = currentState.get_token()

        self.nextState += 1
        return new_token

    def get_tokens(self):
        return self.tokens

    def get_file_as_string(self, file_path):
        # // open file at given path.
        input = ''
        with open(file_path) as f:
            input = f.read()

        return input
