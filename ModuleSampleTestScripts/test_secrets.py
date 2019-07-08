import sys
import os
#We need to set the sys path for the modules to be imported
sys.path.append(os.getcwd())
import Secrets.config as config

#We had put a key value pair like below in config.py
#TEST_VALUE='teamwork'
test_value='teamwork'

assert (config.TEST_VALUE == test_value),"secrets config call failed"

print ("\nTest Passed.")