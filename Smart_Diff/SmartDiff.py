#!/usr/bin/python3

import sys

def smart_diff(file1, file2):
    with open(file1, "r") as f1:
        with open(file2, "r") as f2:
            i = 0
            j = 0
            student_file = f1.read()
            key_file = f2.read()

            while i < len(file1) and j < len(file2):
                mode = compare(student_file[i], key_file[j])
                if mode == 1:
                    i += 1
                elif mode == 2:
                    j += 1
                elif mode == 3:
                    i += 1
                    j += 1
                else:
                    return False

def compare(value1, value2):
    if is_whitespace(value1):
        return 1
    elif is_whitespace(value2):
        return 2
    elif value1 == value2:
        return 3
    return 0

def is_whitespace(character):
    return character == ' ' or character == '\t' or character == '\r' or character == '\n'

smart_diff(sys.argv[1], sys.argv[2])