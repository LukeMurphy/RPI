import logging
import os
import time
import threading
import subprocess
import concurrent.futures

from multiprocessing import Process

duration = 5
configPath = "/Users/lamshell/Documents/Dev/LEDELI/RPI/configs/dev/"

logger = logging.getLogger(__name__)
logging.basicConfig(filename="results.log", level=logging.INFO)


class ThreadedPlayer:
    def __init__(self, link, name=None):
        self.link = link
        self.name = name

    def start(self, tStopRef):
        self.proc = subprocess.Popen(["python3", "../player.py", "-cfg", self.link])
        runOk = True
        timeRange = 3
        for _count in range(4, 0, -1):
            print(f"{_count} {self.name} {self.proc.poll()}")
            if self.proc.poll() == 1:
                runOk = False
                break

            if self.proc.poll() is None and _count < (timeRange - 1):
                break

            time.sleep(1)

        if not runOk:
            print(f"Name: {self.name} has not run correctly")
            logger.info(f"{self.name} {self.link}")
        else:
            print(f"Name: {self.name} has run OK")

        self.proc.terminate()
        tStopRef.set()


def _get_config_files(configPath):
    fullList = []
    # filterResults = len(filterText) > 1
    for root, dirs, files in os.walk(configPath, topdown=False):
        for name in files:
            fullPath = os.path.join(root, name)
            if name.endswith(".cfg") and not name.endswith(".py") and name != ".DS_Store":
                res = os.stat(fullPath)
                if "asset_configs" not in fullPath and "/marks" not in fullPath and "/textures" not in fullPath and "/colors" not in fullPath and "manifest" not in fullPath and "sequence" not in fullPath:
                    fullList.append((name, fullPath.split("/configs/")[1]))

    return fullList


def main():
    # links = [
    #     ["working player","reference-configs/256x320-spritesheet_obearx.cfg"],
    #     ["busted","reference-configs/256x320-spritesheet_obearx_.cfg"],
    # ]

    links = _get_config_files(configPath)

    for link in links:
        print(link)
        t1_stop = threading.Event()
        _t1 = ThreadedPlayer(link[1], link[0])
        t1 = threading.Thread(target=_t1.start, args=[t1_stop])
        t1.start()
        time.sleep(3)


def thread1(arg1, link, stop_event):
    subprocess.Popen(["python3", "../player.py", "-cfg", link])


if __name__ == "__main__":
    main()
