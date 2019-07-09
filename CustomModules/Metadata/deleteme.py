import sys
import os
#We need to set the sys path for the modules to be imported
two_up = os.path.abspath(os.path.join(os.getcwd(),"../.."))
print (two_up)
sys.path.append(two_up)
import Secrets.config as config

print (os.getcwd()+"\n"+config.TEST_VALUE)