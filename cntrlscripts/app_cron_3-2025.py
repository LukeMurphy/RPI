import os

# from os import listdir
# from os.path import isfile, join, isdir
# from os import walk
# import datetime
# import subprocess
# import sys
import time

# This is probably the file to set as the machine's startup desktop
# if the machine is under remote control
path = "/home/daemon104/Documents/RPI/cntrlscripts/"
appChanger = f"{path}app_changer.sh"
appListIndex = 0

timeToCheck = 15

def runScript(arg="startup"):
    global timeToCheck,appListIndex
    try:
        execCmd = f"{appList[appListIndex][0]} -{appListIndex}"
        print(execCmd)
        os.system(execCmd)
        appListIndex = 1 if appListIndex == 0 else 0
    except Exception as e:
        print("There was an issue:")
        print(e)
    # end try
    time.sleep(timeToCheck)
    runScript("cron")

runScript("startup")
