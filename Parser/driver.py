from Lexer import Lexer
from Parser import Parser

def main(file_name):
    if fileNotValid(file_name):
        print("INVALID FILE!")
        return 1

    lexer = Lexer()
    if file_name is not "":
        lexer.analyze_file(file_name)
        parser = Parser(lexer.get_tokens)


def fileNotValid(file):
    l_file = open(file, 'r')

    if l_file.closed:
        return True

    l_file.close()
    return False
