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

app1 = "/usr/bin/python3 /home/daemon104/Documents/RPI/player.py -cfg prod/p4-6x8-paintings.cfg"
app1_endcmd = "ps -ef | pgrep -f player.py | xargs kill -9"

app2 = "/home/daemon104/Documents/electron-quick-start-linux-x64/electron-quick-start"
app2_endcmd = "ps -ef | pgrep -f electron | xargs kill -9"

appList = [[app1, app1_endcmd],[app2,app2_endcmd]]
appListIndex = 0
appListPrevIndex = 1

timeToCheck = 15

def runScript(arg="startup"):
    global timeToCheck
    try:
        runChange()
    except Exception as e:
        print("There was an issue:")
        print(e)
    # end try
    time.sleep(timeToCheck)
    runScript("cron")


def runChange():
    global appList, appListIndex, appListPrevIndex
    
    execCmd = f"{appList[appListIndex][0]}"
    print(execCmd)
    os.system(execCmd)

    execCmd = f"{appList[appListPrevIndex][1]}"
    print(execCmd)
    os.system(execCmd)

    appListPrevIndex = appListIndex
    appListIndex = 1 if appListIndex == 0 else 0


runScript("startup")
