from Lexer import Lexer
from Parser import Parser

def main(file_name):
    try:
        fileNotValid(file_name)
    except:
        print("INVALID FILE!")
        return 1

    lexer = Lexer()
    if file_name is not "":
        lexer.analyze_file(file_name)
        for token in lexer.get_tokens():
             print(token.get_value())
        print("done")
        # parser = Parser(lexer.get_tokens)


def fileNotValid(file):
    with open(file, 'r') as f:
        return False
    return True

main("main.cpp")
