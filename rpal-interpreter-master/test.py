# Import the subprocess module to run external scripts
import subprocess
# Import the os module to interact with the operating system
import os
# Arguments to be passed to the called script
arg1 = "test_cases/test"

# Get a list of all files in the test_cases directory
dir=os.listdir("test_cases")
for file in dir :
    # print("output for file: ", file ,end=" ")
    # Run the external script 'myrpal.py' with the file as an argument
    subprocess.run(['python', 'myrpal.py', "test_cases\\"+ file])



