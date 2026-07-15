import os
import subprocess
import time

# used for Linux machines to reset which piece is set to run - must be coordinated
# with a USB drive called "CONTROLLER" that has a file called "playlist.txt" - V1
# ---------------------------- #
base = "/home/daemon125/Documents/"
usbPath = "/media/daemon125/CONTROLLER"
availablePieces = [
    "staging/p2.5-informal-384x320/hashing-marks-v3-minimals.cfg",
    "staging/p2.5-informal-384x320/repeatblocks-v7.cfg",
    "staging/p2.5-informal-384x320/actionmarks-v3_1_c.cfg"]

pieceNames = ["hashing-marks","repeat-blocks","action-marks"]
timeToCheck = 5
# ---------------------------- #
os.environ["DISPLAY"] = ":0"
playlistFile = f"{usbPath}/playlist.txt"
launchString = f"/usr/bin/python3 {base}RPI/player.py -path {base}RPI/ -cfg "

# Tracks running piece processes: config_path -> subprocess.Popen
running_procs = {}

def runScript(arg="startup"):
    global initPath, timeToCheck
    try:
        res = os.system(f"ls {usbPath}")
        if res == 0 :
            with open(playlistFile) as file:
                lines = [line.rstrip() for line in file]
                print(lines)
                for _playIndex in range(0, len(pieceNames)) :
                    if lines[0] == pieceNames[_playIndex] :
                        break
            cfg_rel = availablePieces[_playIndex]
            cmd = ["python3", "-u", base + "RPI/player.py", "-path", base + "RPI/", "-mname", "studio", "-cfg", cfg_rel]
            os.system("ps -ef | pgrep -f Player | xargs kill -9;")
            os.system("ps -ef | pgrep -f player.py | xargs kill -9")
            proc = subprocess.Popen(cmd, text=True, bufsize=1)

            with open(f"{base}startart.sh","w") as file :
                file.write(f"{launchString}{cfg_rel}")
            time.sleep(5)
            os.system(f"umount {usbPath}")
            time.sleep(5)
            runScript("cron")
        else :
            time.sleep(timeToCheck)
            runScript("cron")
    except Exception as e:
        print("There was an issue:")
        print(e)
    # end try
    time.sleep(timeToCheck)
    if arg != "cron":
        runScript("cron")

runScript("startup")