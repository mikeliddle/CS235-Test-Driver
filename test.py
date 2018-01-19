#!/usr/bin/python3

# Author: Mike Liddle
# Brigham Young University
import subprocess
import requests
import os
import shutil
import logging
import re
from ConfigFile import ConfigFile
from LogFile import LogFile

log = logging.getLogger()

DEBUG = False
# print("DEBUG: " + str(DEBUG))

ROOT_DIR = '/users/groups/cs235ta/submission_driver'

if DEBUG:
    ROOT_DIR = 'C:\\users\\malid\\workspace\\submission_driver'

config_file_object = ConfigFile(ROOT_DIR + 'compiler_global2.cfg')

# config_file_object = open(ROOT_DIR + '/compiler_global2.cfg', 'r+')
#
# d_current_line = int(config_file_object.readline()[13:].strip('\n'))
# log_file = open(config_file_object.readline()[9:].strip('\n'), 'r')
# live_dir = config_file_object.readline()[9:].strip('\n')
# grade_log_file = config_file_object.readline()[10:].strip('\n')
# out_file = config_file_object.readline()[9:].strip('\n')

# everything works up to this point.
# print("current_line: " + str(d_current_line))
# print("live_dir: " + live_dir)
# print("grade_log_file: " + grade_log_file)
# print("out_file: " + out_file)

command = 'timeout 30s compileCode.sh'


def compile_code():
    exe_name = 'run_me'
    information_string = 'compiling files:\n'

    all_files = [f for f in os.listdir('.') if os.path.isfile(f) and re.search('cpp', f)]
    for file in all_files:
        information_string += file.name + '\n'

    information_string += '\ng++ -g -Wall -std=c++17 -o ' + exe_name + ' *.cpp' + '\n'

    p = subprocess.run(['/usr/bin/g++', '-g', '-Wall', '-std=c++17', '-o', exe_name, ' '.join(all_files)],
                       stderr=subprocess.PIPE, stdout=subprocess.PIPE)

    grade = p.stdout
    compile_error = p.stderr

    if compile_error == "":
        information_string += 'Compilation Succeeded!\n'
    else:
        information_string += 'Compilation Failed\n'

    return information_string


def run_student_code(lab_name, net_id, email, log_date):
    os.chdir("TMP_DELETE")

    print("current directory: " + os.getcwd())

    shutil.copy(ROOT_DIR + '/SubmissionDriver/compileCode.sh', 'compileCode.sh')

    # compile the code.
    compile_code()
    #    command_to_run = command + " " + net_id + " " + lab_name + " " + log_date +
    # " 2> ../" + net_id + "." + lab_name + ".compile.out"

    # send email
    r = requests.post("https://students.cs.byu.edu/~cs235ta/emailEndpoint/emailTa.php",
                      data={'email': email, 'subject': lab_name + ' Compile Results for ' + net_id,
                            'body': 'Your compilation results are attached.', 'compile': 'compileFile'})

    print("EMAIL STATUS CODE: " + str(r.status_code))

    # self-cleanup
    os.chdir("..")
    shutil.rmtree("TMP_DELETE")


def submission_driver():
    i = 0

    while True:
        os.chdir(ROOT_DIR)
        log_file = config_file_object.log_file()

        config_file_object.seek(0)
        current_line = int(config_file_object.readline()[13:].strip('\n'))

        print("Current_line: " + str(current_line))

        if config_file_object.log_file.closed:
            config_file_object.set_current_line(0)
        else:
            while i < current_line:
                config_file_object.log_file.readline()
                i += 1
                print('i: ' + str(i) + ' current_line: ' + str(current_line))

            log_entry = log_file.readline().strip('\n').split(',')

            print("log_entry: " + ','.join(log_entry))

            config_file_object.increment_current_line()
            i += 1

            log_date = log_entry[0]
            lab = log_entry[1]
            file_name = log_entry[3].strip('()')
            net_id = log_entry[2]
            email = log_entry[4]

            os.chdir(config_file_object.live_dir + net_id)

            if not os.path.exists("TMP_DELETE"):
                os.mkdir("TMP_DELETE")
            else:
                shutil.rmtree("TMP_DELETE")
                os.mkdir("TMP_DELETE")

            print('\n' + os.getcwd() + '\n')

            subprocess.call(['/usr/bin/unzip', '-o', '-qq', file_name, '-d', 'TMP_DELETE'],
                            stdin=subprocess.DEVNULL)

            run_student_code(lab, net_id, email, log_date)


submission_driver()
