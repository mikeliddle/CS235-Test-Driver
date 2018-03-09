#!/usr/bin/python3


class CodeRunner:
    def __init__(self, lab_num, test_path, main_file):
        self.lab_num = lab_num
        self.test_path = test_path
        self.main_file = main_file

    def replace_main(self):
        main_file = open(self.main_file, mode='rw')
        file = main_file.read(len(main_file))
        
        for x in range(0, len(file)):
            continue
        pass

    def compile_code(self):
        pass

    def run_testcases(self):
        pass
