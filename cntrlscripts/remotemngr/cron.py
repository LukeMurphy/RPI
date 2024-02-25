import os
from os import listdir
from os.path import isfile, join, isdir
from os import walk
import datetime
import subprocess
import sys
import time


# This is probably the file to set as the machine's startup desktop 
# if the machine is under remote control

initPath = './remotecontrol-remote-to-lukelab.sh'
timeToCheck = 15

def runScript(arg='startup') :
    global initPath, timeToCheck
    try:
        # comment: 
        execCmd = initPath + " " + arg
        print(execCmd)
        os.system(execCmd)
    except Exception as e:
        print("There was an issue:")
        print(str(e))
    # end try
    time.sleep(timeToCheck)
    runScript("cron")
    
    
runScript('startup')