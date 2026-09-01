import time
import threading
import os

#used for Linux machines that stall auto-launched pyhon scripts ....

os.environ["DISPLAY"] = ":0"
initPath = '/home/daemon125/Documents/startart.sh'
initPath2 = '/home/daemon125/Documents/checkusb.sh'
timeToCheck = 30


def runScript(arg="startup"):
    global initPath, timeToCheck
    try:
        if arg == "cron":
            os.system("ps -ef | pgrep -f player.py | xargs kill -9")
        execCmd = f"{initPath}"
        print(execCmd)
        os.system(execCmd)
    except Exception as e:
        print("There was an issue:")
        print(e)
    # end try
    time.sleep(timeToCheck)
    if arg != "cron":
        runScript("cron")
        
os.system(f"{initPath2}")
runScript("startup")