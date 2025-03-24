import os
import random
import time

# This is probably the file to set as the machine's startup desktop
# if the machine is under remote control
path = "/home/daemon104/Documents/RPI/cntrlscripts/"
appChanger = f"{path}app_changer.sh"
appListIndex = 2

timeToCheck = 90

def runScript(arg="startup"):
    global timeToCheck,appListIndex,appChanger
    try:
        execCmd = f"{appChanger} {appListIndex}"
        print(execCmd)
        os.system(execCmd)
        appListIndex = 2 if appListIndex == 1 else 1
        timeToCheck = random.randint(90, 300)
    except Exception as e:
        print("There was an issue:")
        print(e)
    # end try
    time.sleep(timeToCheck)
    runScript("cron")

runScript("startup")
