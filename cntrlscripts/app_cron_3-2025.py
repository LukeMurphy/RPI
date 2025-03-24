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

app1 = "start_app1.sh"
app1_endcmd = "shut_player_down.sh"

app2 = "start_app2.sh"
app2_endcmd = "shut_electronplayer_down.sh"

appList = [[app1, app1_endcmd],[app2,app2_endcmd]]
appListIndex = 1
appListPrevIndex = 0

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
