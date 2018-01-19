#!/usr/bin/python3

import sys
from LogFile import LogFile


DEBUG = False


class ClassGrades:
    def __init__(self, lab_name):
        self.lab_name = lab_name
        self.LOG_DIR = '/users/groups/cs235ta/public_html/W2018_submissions/'
        self.LOG_FILE = self.LOG_DIR + 'W2018_completed_reviews_log.txt'

        if DEBUG:
            self.LOG_FILE = 'W2018_code_reviews_log.txt'

        self.log_object = LogFile(self.LOG_FILE)

        # set containing all students netId's
        self.student_net_ids = set()

        # this is a mapping of a student to their review scores.
        self.code_review_mapping = {}  # {'netId': [13, 13, 13], 'netId2': [13, 15, 15]}
        # this is a mapping of a student to whether or not they did each code review.
        self.code_reviewer_mapping = {}  # {'netId': [1, 1, 1], 'netId2': [1, 1, 0]}

    def add_student(self, net_id):
        self.student_net_ids.add(net_id)

    def log_object(self):
        return self.log_object

    @staticmethod
    def calc_sum(values):
        sum_value = 0
        counter = 0

        for i in values:
            sum_value = sum_value + i
            counter = counter + 1

        return sum_value // counter

    def create_csv(self, learning_suite_name):
        out_file = open(self.lab_name + '_results.csv', 'w+')
        file_contents = list()
        file_contents.append('net_id,' + learning_suite_name + ',score1,score2,score3\n')

        for key in self.code_review_mapping.keys():
            line = list()
            for i in self.code_review_mapping[key]:
                line.append(str(i))

            avg_score = self.calc_sum(self.code_review_mapping[key])
            string_line = key + ',' + str(avg_score) + ',' + ','.join(line) + '\n'
            file_contents.append(string_line)

        out_file.writelines(file_contents)


# params:
# lab_name = the name of the lab in the log file.
# learning_suite_name = the name of the lab in learning suite.
def generate_grade_csv(lab_name, learning_suite_name):
    grade_object = ClassGrades(lab_name)
    log_file = grade_object.log_object

    # split_string[0] = date; [1] = netID; [2] = lab_name; [3] = IDE; [4] = score1; [5] = score2;
    # [6-7] = detail; [8] = reviewer; [9] = reviewer_email

    for line in log_file.file_contents:
        # print("?" + line[2] + "=" + lab_name + "?")
        if line[2] == lab_name:
            current_net_id = line[1]
            grade_object.add_student(current_net_id)  # netID will be added to the set if it's not there.
            key_set = set(grade_object.code_review_mapping.keys())  # scores are added here.

            if current_net_id in key_set:
                grade_object.code_review_mapping[current_net_id].append(int(line[4]) + int(line[5]))
            else:
                grade_object.code_review_mapping[current_net_id] = list()
                grade_object.code_review_mapping[current_net_id].append(int(line[4]) + int(line[5]))

    grade_object.create_csv(learning_suite_name)


# end generate_grade_csv


if len(sys.argv) < 2:
    print("USAGE: gradeGenerator.py [lab_name] [learning_suite_name]")
else:
    generate_grade_csv(sys.argv[1], sys.argv[2])
# end program
