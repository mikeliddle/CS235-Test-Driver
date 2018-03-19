#!/usr/bin/python3

# Author: Mike Liddle
# Brigham Young University
import subprocess
import requests
import os
import shutil
import re
from ConfigFile import ConfigFile
from ConfigFile import LogFile
import _thread
from threading import Lock

DEBUG = True
WIN_DEBUG = True

lock_compile_file = Lock()
lock_email_file = Lock()

ROOT_DIR = 'path'

if WIN_DEBUG:
    ROOT_DIR = 'path'

config_file_object = ConfigFile(ROOT_DIR + 'compiler_global.cfg')

email_log_file = ROOT_DIR + 'logs/email_log_file.out'
grade_log_file = ROOT_DIR + 'logs/W2018_autogrades.out'
error_log_file = ROOT_DIR + 'logs/Python_errors.out'
debug_log_file = ROOT_DIR + 'logs/Python_debug.out'
compile_log_file = ROOT_DIR + 'logs/W2018_compile.out'


def compile_code(lab_name, net_id, email, log_date):
    exe_name = 'run_me'
    information_string = ""
    information_string += 'compiling files:\n'

    all_files = []
    for f in os.listdir('.'):
        if os.path.isfile(f) and re.search('cpp', f):
            p = subprocess.run(['/usr/bin/file', '-i', f],
                               stdout=subprocess.PIPE)
            file_info = p.stdout.decode('utf-8').split(":")
            file_info = file_info[1].split(";")
            file_info = file_info[1].split("=")
            if file_info[1].strip() == "us-ascii":
                all_files.append(f)
            else:
                information_string += 'invalid file encoding: ' + \
                    file_info[1] + '\n'

    if len(all_files) < 1:
        information_string += 'No valid files detected!' + '\n'

    compile_command = ['/usr/bin/g++', '-g',
                       '-Wall', '-std=c++17', '-o', exe_name]
    for file in all_files:
        information_string += file + '\n'
        compile_command.append(file)

    information_string += '\ng++ -g -Wall -std=c++17 -o ' + exe_name + ' *.cpp' + '\n'

    if not WIN_DEBUG:
        p = subprocess.run(
            compile_command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

        if not DEBUG:
            grade = p.stdout.decode('utf-8')

        compile_error = p.stderr.decode('utf-8')
        information_string += compile_error + '\n'

        if p.returncode == 0:
            information_string += 'Compilation Succeeded!\n'
        else:
            information_string += 'Compilation Failed!\n'

        with open(compile_log_file, 'a+') as compile_log:
            compile_log.write(
                ','.join([log_date, lab_name, net_id, email, str(p.returncode)]) + '\n')
    else:
        information_string += 'Compilation Not Performed.\n'

    return information_string


def run_student_code(lab_name, net_id, email, log_date):
    os.chdir("TMP_DELETE")

    # print("current directory: " + os.getcwd())

    # compile the code.
    information_string = compile_code(lab_name, net_id, email, log_date)

    # write to the compile file
    lock_compile_file.acquire()

    compile_file_name = net_id + '.' + lab_name + '.compile.out'
    compile_file = open(compile_file_name, 'w+')
    compile_file.write(information_string)
    compile_file.close()
    shutil.copy(compile_file_name, '../' + compile_file_name)
    
    lock_compile_file.release()

    # dynamically set the subject line
    if 'Compilation Succeeded' in information_string:
        subject = 'Compilation Succeeded - ' + lab_name + ' - ' + net_id
    else:
        subject = 'Compilation Failed - ' + lab_name + ' - ' + net_id

    if DEBUG:
        # don't want to pester students with debugging emails.
        email = 'test@company.com'

    body = 'UPDATES: the autocompiler now enforces file encoding to be utf-8 ascii encoding. If you do not get an attachment with your email, please contact a TA.  If your attachment says, "invalid file encoding" please verify the encoding of the files by extracting them from the zip archive you created and then checking their encoding before talking to a TA.  \n\nYour compilation results are attached.'

    email_data = {'email': email, 'subject': subject, 'body': body}
    email_files = {'compile': open(
        net_id + '.' + lab_name + '.compile.out', 'rb')}

    r = requests.post("endpoint.php", data=email_data,
                      files=email_files)

    # send email
    if not DEBUG:
        lock_email_file.acquire()

        with open(email_log_file, 'a+') as email_file:
            log_entry_list = (log_date, net_id, email,
                              lab_name, str(r.status_code))
            email_file.write(','.join(log_entry_list) + '\n')
        
        lock_email_file.release()

    else:
        lock_email_file.acquire()
        
        with open(email_log_file, 'a+') as email_file:
            log_entry_list = (log_date, net_id, email, lab_name, 'test')
            email_file.write(','.join(log_entry_list) + '\n')
        
        lock_email_file.release()

    # self-cleanup
    os.chdir('..')
    shutil.rmtree('TMP_DELETE')


def submission_driver():
    log_file = LogFile(config_file_object.log_file_path)

    while True:
        try:
            os.chdir(ROOT_DIR)

            if log_file.check_last_line(config_file_object.current_line):
                log_entry = log_file.get_line(config_file_object.current_line)

                if DEBUG:
                    with open(debug_log_file, 'a+') as debug_file:
                        debug_file.write(
                            'log_entry: ' + ','.join(log_entry) + '\n')

                config_file_object.increment_current_line()

                log_date = log_entry[0]
                lab = log_entry[1]
                file_name = log_entry[5].strip('()')
                net_id = log_entry[2]
                email = log_entry[6]

                os.chdir(config_file_object.live_dir + net_id)

                if not os.path.exists("TMP_DELETE"):
                    os.mkdir("TMP_DELETE")
                else:
                    if DEBUG:
                        with open(debug_log_file, 'a+') as debug_file:
                            debug_file.write('Removing TMP_DELETE\n')
                    shutil.rmtree("TMP_DELETE")
                    os.mkdir("TMP_DELETE")

                if DEBUG:
                    with open(debug_log_file, 'a+') as debug_file:
                        debug_file.write(str(os.getcwd()) + '\n')

                if not WIN_DEBUG:  # unzip doesn't exist on Windows systems.
                    subprocess.call(['/usr/bin/unzip', '-o', '-qq', file_name, '-d', 'TMP_DELETE'],
                                    stdin=subprocess.DEVNULL)
                else:
                    with open(debug_log_file, 'a+') as debug_file:
                        debug_file.write('Unzipping file: ' + file_name + '\n')
                _thread.start_new_thread(run_student_code, (lab, net_id, email, log_date))

        except KeyboardInterrupt:
            exit(0)
        except Exception as error:
            # log any error messages.
            with open(error_log_file, 'a+') as error_log:
                error_log.write(str(error) + '\n')


submission_driver()
