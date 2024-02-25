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

initPath = './remotecontrol-remote-to-lukelab.sh startup'
timeToCheck = 30

def runScript() :
    global initPath, timeToCheck
    initPath = './remotecontrol-remote-to-lukelab.sh cron'
    try:
        # comment: 
        os.system(initPath)
    except Exception as e:
        print(str(e))
    # end try
    time.sleep(timeToCheck)
    runScript()
    
    
runScript()