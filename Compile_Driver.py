#!/usr/bin/python3

#============== Compile_Driver.py ====================#
#                                                     #
# Author: Mike Liddle                                 #
# Brigham Young University                            #
#                                                     #
# Purpose: this software is to be used for the        #
#          autocompilation and grading of students'   #
#          code for CS 235 at BYU.                    #
#                                                     #
# Files:   Compile_Driver.py, ConfigFile.py           #
#                                                     #
#=====================================================#

import subprocess
import requests
import os
import shutil
import datetime
import re
from ConfigFile import ConfigFile
from ConfigFile import LogFile

# variables used for debugging the code
DEBUG = False
WIN_DEBUG = False

# specifies the root directory for the program to be run in.
ROOT_DIR = 'path'

# if running on a windows machine, adjust accordingly.
if WIN_DEBUG:
    ROOT_DIR = 'path'

# create the config file object from the file.
config_file_object = ConfigFile(ROOT_DIR + 'compiler_global.cfg')


#=====================================================#
# compile_code                                        #
#    compiles the student code and composes an info   #
#    string that reports the compilation status.      #
#                                                     #
#=====================================================#
def compile_code(lab_name, net_id, email, log_date):
    global config_file_object

    exe_name = 'run_me'
    information_string = ""
    information_string += 'compiling files:\n'

    all_files = []
    # include all cpp files in compilation, check file encoding.
    for f in os.listdir('.'):
        # this is what checks the extension "*.cpp"
        if os.path.isfile(f) and re.search('cpp', f):
            # the following process gets the file encoding.
            p = subprocess.run(['/usr/bin/file', '-i', f],
                               stdout=subprocess.PIPE)
            file_info = p.stdout.decode('utf-8').split(":")
            file_info = file_info[1].split(";")
            file_info = file_info[1].split("=")
            file_info[1] = file_info[1].strip()

            # is the file encoding one of our accepted encodings?
            if file_info[1] == "us-ascii" or file_info[1] == "utf-8":
                all_files.append(f)
            else:
                # if not, still try to compile, but report it as invalid.
                information_string += 'invalid file encoding: \"' + \
                    file_info[1] + '\" for file: ' + str(f) + '\n'
                all_files.append(f)

    # if there are no files, report that.
    if len(all_files) < 1:
        information_string += 'No valid files detected!' + '\n'

    compile_command = [config_file_object.compiler, '-g',
                       '-Wall', '-std=c++17', '-o', exe_name]
    for file in all_files:
        information_string += file + '\n'
        compile_command.append(file)

    # report the command we used to the user.
    information_string += '\ng++ -g -Wall -std=c++17 -o ' + exe_name + ' *.cpp' + '\n'

    # g++ won't work on windows, act accordingly.
    if not WIN_DEBUG:
        p = subprocess.run(
            compile_command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

        # grab the output from g++ and put it in the info string.
        compile_error = p.stderr.decode('utf-8')
        information_string += compile_error + '\n'

        # tell the user whether compilation succeeded or failed.
        if p.returncode == 0:
            information_string += 'Compilation Succeeded!\n'
        else:
            information_string += 'Compilation Failed!\n'

        # log the result as well with the student information in case of errors.
        with open(config_file_object.compile_log, 'a+') as compile_log:
            compile_log.write(
                ','.join([log_date, lab_name, net_id, email, str(p.returncode)]) + '\n')
    else:
        information_string += 'Compilation Not Performed.\n'

    return information_string


#=====================================================#
# run_student_code                                    #
#    runs the compilation, then any other needful     #
#    actions, including emailing the student the      #
#    results of compilation.  This is where extension #
#    of functionality should happen.                  #
#                                                     #
#=====================================================#
def run_student_code(lab_name, net_id, email, log_date):
    global config_file_object

    os.chdir("TMP_DELETE")

    # compile the code.
    information_string = compile_code(lab_name, net_id, email, log_date)

    # write to the student compile file
    compile_file_name = net_id + '.' + lab_name + '.compile.out'
    compile_file = open(compile_file_name, 'w+')
    compile_file.write(information_string)
    compile_file.close()
    shutil.copy(compile_file_name, '../' + compile_file_name)

    # dynamically set the subject line for the reporting email.
    if 'Compilation Succeeded' in information_string:
        subject = 'Compilation Succeeded - ' + lab_name + ' - ' + net_id
    else:
        subject = 'Compilation Failed - ' + lab_name + ' - ' + net_id

    if DEBUG:
        # don't want to pester students with debugging emails.
        email = 'test@company.com'

    # This is the body of the message.  Feel free to change and update this as needed.
    body = 'UPDATES: the autocompiler now enforces file encoding to be utf-8 ascii encoding. If you do not get an attachment with your email, please contact a TA.  If your attachment says, "invalid file encoding" please verify the encoding of the files by extracting them from the zip archive you created and then checking their encoding before talking to a TA.  \n\nYour compilation results are attached.'

    # create the email object
    email_data = {'email': email, 'subject': subject, 'body': body}
    email_files = {'compile': open(
        net_id + '.' + lab_name + '.compile.out', 'rb')}

    # send the HTTP request to the endpoint to send the email.
    r = requests.post("endpoint.php", data=email_data,
                      files=email_files)

    # send email and log the result.
    if not DEBUG:
        with open(config_file_object.get_email_log(), 'a+') as email_file:
            log_entry_list = (log_date, net_id, email,
                              lab_name, str(r.status_code))
            email_file.write(','.join(log_entry_list) + '\n')
    else:
        with open(config_file_object.get_email_log(), 'a+') as email_file:
            log_entry_list = (log_date, net_id, email, lab_name, 'test')
            email_file.write(','.join(log_entry_list) + '\n')

    # self-cleanup, the rm usually fails, but everything inside gets removed, which does the trick.
    os.chdir('..')
    shutil.rmtree('TMP_DELETE')

#=====================================================#
# submission_driver                                   #
#    this is the main driver function, it handles     #
#    logic for reading a submission from the log and  #
#    parsing the entry to run the student code.  This #
#    shouldn't need much if any maintenance for       #
#    functionality.                                   #
#                                                     #
#=====================================================#


def submission_driver():
    global config_file_object

    # this creates the log file object from the log file given in our config folder.
    log_file = LogFile(config_file_object.log_file_path)

    # run this loop indefinitely.  Cron should handle any breaking from this loop.
    while True:
        # wrap everything in a try/except to handle errors gracefully and report them.
        try:
            # we start in the root directory.
            os.chdir(config_file_object.root_dir)
            # check to see if our log file exists
            valid_log_line = log_file.check_last_line(
                config_file_object.current_line)
            if valid_log_line > 0:
                # if it exists, we get the line we are on.
                log_entry = log_file.get_line(config_file_object.current_line)

                # log information in the debuf file when debugging.
                if DEBUG:
                    with open(config_file_object.get_debug_log(), 'a+') as debug_file:
                        debug_file.write(
                            'log_entry: ' + ','.join(log_entry) + '\n')

                # increment the current line count so we know to do the next entry next.
                config_file_object.increment_current_line()

                # split and parse the log entry.
                log_date = log_entry[0]
                lab = log_entry[1]
                file_name = log_entry[5].strip('()')
                net_id = log_entry[2]
                email = log_entry[6]

                # move into the student's folder on the server.
                os.chdir(config_file_object.live_dir + net_id)

                # if they don't have a TMP_DELETE folder, create it.
                if not os.path.exists("TMP_DELETE"):
                    os.mkdir("TMP_DELETE")
                else:
                    # otherwise, remove the folder and recreate it.
                    if DEBUG:
                        with open(config_file_object.get_debug_log(), 'a+') as debug_file:
                            debug_file.write('Removing TMP_DELETE\n')
                    shutil.rmtree("TMP_DELETE")
                    os.mkdir("TMP_DELETE")

                # log the current directory when debugging.
                if DEBUG:
                    with open(config_file_object.get_debug_log(), 'a+') as debug_file:
                        debug_file.write(str(os.getcwd()) + '\n')

                # unzip the student code zip archive.
                # unzip -o -qq <file_name> -d TMP_DELETE
                if not WIN_DEBUG:  # unzip doesn't exist on Windows systems.
                    subprocess.call([config_file_object.unzip, '-o', '-qq', file_name, '-d', 'TMP_DELETE'],
                                    stdin=subprocess.DEVNULL)
                else:
                    with open(config_file_object.get_debug_log(), 'a+') as debug_file:
                        debug_file.write('Unzipping file: ' + file_name + '\n')

                # run the student code.
                run_student_code(lab, net_id, email, log_date)

            elif valid_log_line < 0:
                # if the log file has been removed, tell the config file to start over at 0.
                config_file_object.set_current_line(0)
        except KeyboardInterrupt:
            # ctrl + c SIGINT, just exit.
            exit(0)
        except Exception as error:
            # log any error messages.
            with open(config_file_object.get_error_log(), 'a+') as error_log:
                error_log.write(str(datetime.datetime.now()) +
                                ': ' + str(error) + '\n')


# run the driver.
submission_driver()
