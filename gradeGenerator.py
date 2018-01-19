#!/usr/bin/python3

class ClassGrades:
    def __init__(self):
        self.


LOG_DIR = '/users/groups/cs235ta/public_html/W2018_submissions/'
LOG_FILE = LOG_DIR + 'W2018_completed_reviews_log.txt'

# set containing all students netId's
student_net_ids = set()

# this is a mapping of a student to their review scores.
code_review_mapping = {'netId': [13, 13, 13], 'netId2': [13, 15, 15]}
# this is a mapping of a student to whether or not they did each code review.
code_reviewer_mapping = {'netId': [1, 1, 1], 'netId2': [1, 1, 0]}


# params:
# lab_name = the name of the lab in the log file.
# learning_suite_name = the name of the lab in learning suite.
def generate_grade_csv(lab_name, learning_suite_name):
    with open(LOG_FILE) as log_file:
        current_line = log_file.readline()
        split_string = current_line.split(',')
        # split_string[0] = date; [1] = netID; [2] = lab_name; [3] = IDE; [4] = score1; [5] = score2;
        # [6-7] = detail; [8] = reviewer; [9] = reviewer_email

        if split_string[2] == lab_name:
            current_net_id = split_string[1]
            student_net_ids.add(current_net_id)  # netID will be added to the set if it's not there.
            key_set = set(code_review_mapping.keys())  # scores are added here.

            if current_net_id in key_set:
                code_review_mapping[current_net_id].add(split_string[4] + split_string[5])
            else:
                code_review_mapping[current_net_id] = list(split_string[4] + split_string[5])


# end generate_grade_csv


if len(sys.argv) < 2:
    print("USAGE: ./gradeGenerator.py [lab_name] [learning_suite_name]")
else:
    lab_name = sys.argv[0]
    learning_suite_name = sys.argv[1]

    generate_grade_csv(lab_name, learning_suite_name)
# end program
