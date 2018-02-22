#!/usr/bin/python3
import os


class TokenState:
    WHITESPACE = 0  # <WHITESPACE>:= *[\n,\t,\r,\ ]
    TITLE = 1  # <TITLE>:= <VALUE>:<WHITESPACE>
    ID = 2  # <ID>:= <VALUE>
    VALUE = 3  # <VALUE>:= *[0:9]
    SEPARATOR = 4  # <SEP>:= [\,,\ ,\:,\t,\n{1}
    INDEX = 5
    NAME = 6
    ACTION = 7
    UNDEFINED = 8
    INVALID = 9
    RAW = 10


class ParseState:
    NULL = 0
    IN_TOKEN = 3
    TOKEN_END = 3
    WILD_CARD = 5
    IN_EXPRESSION = 9
    EXPRESSION_END = 13
    VALUE = 1


class SmartDiff:
    def __init__(self, test_file, key_file):
        self.has_grammar = False
        self.file = test_file
        self.key_file = key_file

        # ---- Parse key file ----
        self.key = list()
        self.grammar = list()

        with open(key_file, 'r') as key_file:
            self.key = key_file.read().split('\n')

    def read_grammar(self):
        line_tracker = 0
        line = self.key[line_tracker]
        line_tracker += 1
        if line == "***GRAMMAR***":
            self.has_grammar = True
            line = self.key[line_tracker]
            line_tracker += 1

        while not line == "***END_GRAMMAR***":
            state = ParseState.NULL
            i = 0
            while i < len(line):
                if state == ParseState.NULL:
                    if line[i] == '<':
                        state ^= ParseState.IN_TOKEN
                    elif line[i] == '>':
                        state ^= ParseState.TOKEN_END
                    elif line[i] == '(':
                        self.grammar.append(Tokens.EXPRESSION_BEGIN)
                    elif line[i] == ')':
                        self.grammar.append(Tokens.EXPRESSION_END)
                    elif line[i] == '*':
                        self.grammar.append(Tokens.WILDCARD)
                    else:
                        print("INVALID GRAMMAR!")
                    i += 1

                elif state == ParseState.IN_TOKEN:
                    tmp_line = line[i:(i + 6)]
                    if tmp_line == 'ACTION':
                        self.grammar.append(Tokens.ACTION)
                        i += 7
                        state ^= ParseState.TOKEN_END
                    elif line[i:(i + 3)] == 'SEP':
                        self.grammar.append(Tokens.SEP)
                        i += 4
                        state ^= ParseState.TOKEN_END
                    elif line[i:(i + 3)] == 'INT':
                        self.grammar.append(Tokens.INT)
                        i += 4
                        state ^= ParseState.TOKEN_END
                    else:
                        print("SOMETHING WENT WRONG!")
                else:
                    print("SOMETHING WENT WRONG!")

            line = self.key[line_tracker]
            line_tracker += 1

    def tokenize(self, file):
        tokenized_file = list()
        with open(file, 'r') as file:
            file_contents = file.read().split('\n')
            line_index = 0
            while line_index < len(file_contents):
                line = file_contents[line_index].strip(' \n\t\r')  # remove leading and trailing whitespace.
                line_index += 1

                if line == '***GRAMMAR***':  # if this is a key file, remove the grammar.
                    while line != '***END_GRAMMAR***':
                        line = file_contents[line_index].strip(' \n\t\r')
                        line_index += 1

                    line = file_contents[line_index].strip(' \n\t\r')
                    line_index += 1

                char_index = 0
                state = ParseState.NULL
                while char_index < len(line):
                    if state == ParseState.NULL:
                        if line[char_index] in Tokens.whitespace:
                            char_index += 1
                            continue
                        elif line[char_index].isalpha():
                            state = TokenState.ID
                            tokenized_file.append(Tokens.ID)

                            while line[char_index].isalnum():
                                char_index += 1
                            continue
                    elif state == TokenState.ID or state == TokenState.VALUE:
                        if line[char_index] in Tokens.value_separators or line[char_index] in Tokens.result_separators:
                            state = TokenState.SEPARATOR
                            tokenized_file.append(Tokens.SEP)
                        elif line[char_index] in Tokens.punctuation:
                            state = TokenState.SEPARATOR
                            tokenized_file.append(Tokens.SEP)
                        char_index += 1
                    elif state == TokenState.SEPARATOR:
                        test_char = line[char_index]
                        if line[char_index].isalpha():
                            tokenized_file.append(Tokens.STRING)
                            while line[char_index].isalnum():
                                char_index += 1
                            state = TokenState.VALUE
                        elif line[char_index].isnumeric():
                            tokenized_file.append(Tokens.INT)
                            while line[char_index].isnumeric():
                                char_index += 1
                            state = TokenState.VALUE

        return tokenized_file


class Tokens:
    INT = 0
    STRING = 1
    SEP = 2
    ACTION = 3
    ID = 3
    EXPRESSION_BEGIN = 4
    EXPRESSION_END = 5
    WILDCARD = 6

    whitespace = {" ", "\t", "\n", "\r"}
    value_separators = {",", " ", ":", "\t", "\n"}
    result_separators = {":", "=", "=>"}
    arithmetic_operators = {"+", "-", "/", "*", "%", "&", "|", "~"}
    new_line = "\n"
    parentheses = {"[", "{", "(", "<", ">", ")", "}", "]"}
    punctuation = {".", ",", "!", "?", ":", ";"}
    quotes = {"'", '"'}


def driver():
    my_diff = SmartDiff('key_file2.txt', 'key_file1.txt')
    my_diff.read_grammar()
    test_output = my_diff.tokenize(my_diff.file)

    print(my_diff.grammar)


driver()
''' grammar notes:
=========================================================================================
<Title>:\n
<ID> =
=========================================================================================
<Title>:\n
<ID>(<val>*<,<val>>).
<ID> Undefined <ID>
=========================================================================================
<name>\n
*(<value><sep>\n)
\n
3(<name>\n
<id><sep> <size><sep><val><sep><index><sep><val><sep><mode><sep><val>
*(<value><sep>\n))
\n
<fib_title>\n
<id><sep> <size><sep><val><sep><index><sep><val><sep><mode><sep><val>\n
<sum><sep><val>+<val>*(+<val>)
=========================================================================================
<Type><sep>[<Type>]
*(<action><sep><val><sep><result>\n || <action><sep><result>)
=========================================================================================
*(<input_expression><sep><postfix_expression><sep><result>)
=========================================================================================
*(<Action>:*\s<value>\n)
'''
