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
from ConfigFile import LogFile

log = logging.getLogger()

DEBUG = False
WIN_DEBUG = False

ROOT_DIR = '/users/groups/cs235ta/submission_driver/'

if WIN_DEBUG:
    ROOT_DIR = 'C:\\users\\malid\\workspace\\CS235\\'

config_file_object = ConfigFile(ROOT_DIR + 'compiler_global2.cfg')


def compile_code():
    exe_name = 'run_me'
    information_string = 'compiling files:\n'

    all_files = [f for f in os.listdir('.') if os.path.isfile(f) and re.search('cpp', f)]
    for file in all_files:
        information_string += file + '\n'

    information_string += '\ng++ -g -Wall -std=c++17 -o ' + exe_name + ' *.cpp' + '\n'

    if not WIN_DEBUG:
        p = subprocess.run(['/usr/bin/g++', '-g', '-Wall', '-std=c++17', '-o', exe_name, ' '.join(all_files)],
                           stderr=subprocess.PIPE, stdout=subprocess.PIPE)

        if not DEBUG:
            grade = p.stdout

        compile_error = p.stderr

        if compile_error == "":
            information_string += 'Compilation Succeeded!\n'
        else:
            information_string += 'Compilation Failed!\n'
    else:
        information_string += 'Compilation performed.\n'

    return information_string


def run_student_code(lab_name, net_id, email, log_date):
    os.chdir("TMP_DELETE")

    print("current directory: " + os.getcwd())

    if not WIN_DEBUG:
        shutil.copy(ROOT_DIR + '/SubmissionDriver/compileCode.sh', 'compileCode.sh')

    # compile the code.
    compile_code()

    # send email
    if not DEBUG or WIN_DEBUG:
        r = requests.post("https://students.cs.byu.edu/~cs235ta/emailEndpoint/emailTa.php", data={'email': email, 'subject': lab_name + ' Compile Results for ' + net_id, 'body': 'Your compilation results are attached.', 'compile': 'compileFile'})

        print("EMAIL STATUS CODE: " + str(r.status_code))
    else:
        print("EMAIL REQUEST SKIPPED!")

    # self-cleanup
    os.chdir("..")
    shutil.rmtree("TMP_DELETE")


def submission_driver():
    log_file = LogFile(config_file_object.log_file_path)

    while True:
        os.chdir(ROOT_DIR)

        if log_file.check_last_line(config_file_object.current_line):
            log_entry = log_file.get_line(config_file_object.current_line)

            print("log_entry: " + ','.join(log_entry))

            config_file_object.increment_current_line()

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

            print(os.getcwd() + '\n')

            if not WIN_DEBUG:
                subprocess.call(['/usr/bin/unzip', '-o', '-qq', file_name, '-d', 'TMP_DELETE'], stdin=subprocess.DEVNULL)

            run_student_code(lab, net_id, email, log_date)


submission_driver()
