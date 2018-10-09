# Submission Driver ReadMe

## SETUP

  1. Naming conventions - We use a naming convention for all folders with content that will
     change from semester to semester.  Every file and folder in question should be prefixed
     with <semester><year>_<file name>, for example, W2018_Submissions.  This information should
     be updated in the file compiler_global.cfg which is explained later.

  2. Create the Submission directory for the new semester.

  3. Create the log file for lab submissions in that directory.

  4. Update these changes in the file compiler_global.cfg

  5. Create the student folder structure and update that in compiler_global.cfg

  6. Make sure the runCompileDriver.sh script is running under the instructor's user in CronLog
        (See note below)

  7. Make sure the emailEndpoint is in the correct location.

  8. Run and test to verify that it is working.


## HISTORY

This project was originally conceived to be an automatic grader for CS 235 labs.  Thus, much of
the project structure was designed focused on that.  The language of choice for much of the 
project is BASH.  The unix environment has many powerful tools that have long term support and 
good documentation, as well as several examples online.  Bash scripts are easy to run through 
CRON, a unix interrupt service, and can easily call other executable files, combine inputs, and 
log results.  The project later was repurposed to be a Code Review system where this project 
would do submission validation and grade compilation and logging.  As such there are duplicate 
files that have different names, but near identical implementation.

The old Submission scripts are deprecated.  They have not been tested as thoroughly as the compile 
scripts, but do, however, nearly the same task as the compile scripts.  The scripts are currently 
being run on the ta-3 lab machine by user proper.  This machine may be reached by using ssh to 
first connect to the CS department, then using ssh to switch to the ta-3 machine.

## IMPORTANT FILES

**RunCompileDriver.sh**

  This file checks to see if the file compileDriver.sh is running, and if it is, it will do 
  nothing, otherwise it will run compileDriver.sh in the background.  This file is supposed to 
  be run from CRON to keep the compileDriver constantly running.  If for some reason this gets 
  removed from the cron tasks, it is easy to reinstall.  Since it does minimal each iteration, it 
  is trivial to run this script every minute.  The syntax in cron would be as follows:

    * * * * * /path/to/script/RunCompileDriver.sh &>> /path/to/log/CronLog.txt

  To add this to CRON type "crontab -e".  This will open up a user's cron for editing, allowing 
  a user to add a Cron Job.

  Another thing to note is the command, 
  
    'ps auxw | grep Compile_Driver.py | grep /usr/bin/python3'

  This command will grab all running processes, search for the one that is compileDriver.sh, and
  makes sure that it is not grep, but a bash script being run, and even more specifically, being
  run by the specified user.  "$USER" is a global variable declared at the top of the file.  

**Compile_Driver.py**

  *NOTE: the following was written while this script was in the bash phase.  Most of it is still
  accurate, with only a few exceptions, like the start of paragraph 4.*

  This file has several global variables.  The first is ROOT_DIR, which is the directory where this
  script is located.  We keep track of this as our project root for when we need to "restart." The
  next is configFile, which specifies which configuration file we will be using for this running
  of the script.  This may be changed in the code, or with a command line flag.  I would suggest
  using the command line flag when possible.  Next is the LogFile.  This is pulled from the config
  file.  The next three variables are the same as what they are in the config file.  Three functions
  are defined in this script: submission_driver, run_student_code, and print_usage.  I will explain
  the first two.  
  
  submission_driver is the main routine.  It has an infinite loop that will first
  check the log file to see the most recent submission.  Next it will take that submission and parse
  the data into usable variables.  After that we unzip the code file into a temporary directory 
  and run the code through the run_student_code method.

  run_student_code will store the output of the compile result in a variable $grade.  It runs a 
  unix utility, timeout, which will stop execution after a certain increment of time, currently
  set to 30 seconds(30s).  We are redirecting the errors into the compiler output, and all other
  output into the variable $grade.  Then we will check if the program timed out or not, and
  lastly we send the email to the students.  This is done through a large convoluted curl request
  which I will now explain.
    
  "curl -X POST" this defines the method of our http request.  We are doing a post request to the 
  endpoint: "https://students.cs.byu.edu/~cs235ta/emailEndpoint/emailTa.php"  This is a script that
  handles emailing the students and TA's based on the parameters submitted.  -F defines a member of
  the request body in a key value pair.  First we define the email to be the students email address
  ('-F "email=$email"').  Next we make the subject line read "$labName Compile Results for $netId".
  We then define the body, and then upload our file(-f"compile=@$.....").  This last portion is
  different as it has an @ which means we are going to load that file and send the binary.  In 
  other words, this is us uploading a file, not passing a file path. This is all followed by the
  endpoint we are sending the request to.

**ConfigFile.py**

  This file contains two classes: ConfigFile and LogFile.  These are not to be confused with the 
  LogFile class for the grade generator, which has some key differences.  

  This is essentially an easy python interface for the config file and the log file.  Use the get 
  methods where possible as they return absolute paths.  The file is easy to extend, but is coded
  such that order matters.  It matters that the order for reading and writing is the same as each
  other and the same as they are in the config file itself.  If the order is not held, data will
  become corrupt by an invalid read, which will then be written and percolated.  For more information 
  refer to the code itself, specifically the constructor (__init__)

**compiler_global.cfg**

  There are a few lines in this file which should be fairly self-explanatory.  The first line 
  has the current line number, which corresponds to the next line to be read in the log file.
  The next line has an absolute file path to the log file we will be reading.  THe line after 
  that is the absolute file path to the directory where the student code folders will be.  The 
  grade log line(next) is an absolute file path to the log file where the grades will be logged.
  The last line is the output log file, this is used for debugging and may be a relative or absolute
  file path. To reset the compileDriver script, put 0 or 1 as the value for CURRENT_LINE, which
  will tell the script to start from the beginning of the log file and run until it can't read
  any more lines.
