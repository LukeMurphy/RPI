#!/usr/bin/python

import argparse
import configparser
import getopt
import os
import sys
import platform
import time
import math
import random

import noise

from PIL import (
    Image,
    ImageChops,
    ImageDraw,
    ImageEnhance,
    ImageFilter,
    ImageFont,
    ImageOps,
)
from multiprocessing import Pool
from modules import configuration, player_module
from modules.rendering import appWindow
from modules.configuration import bcolors

import subprocess
from subprocess import check_output


"""
This file runs as a daemon to mange the sequence of players
Mange is right
I can barely remember how this works

basically it starts a new player and kills off the previous one over and over again to
avoid a memory leak by having one player re-load new configs that I had the last time
not elegant but way more maintainable  ;)

"""


def timeChecker(sequenceConfig, config):
    sequenceConfig.currentTime = time.time()

    # uncomment to debug
    # print(
    #     f"{bcolors.WARNING}** sequence-player.py checking the time ... {str(round(sequenceConfig.currentTime - sequenceConfig.startTime))} / {str(sequenceConfig.currentPieceDuration)}"
    #     + ""
    #     + bcolors.ENDC
    # )

    if sequenceConfig.currentTime - sequenceConfig.startTime > sequenceConfig.currentPieceDuration:
        _select_next_piece(sequenceConfig)
        _launch_next_player(sequenceConfig)
        _kill_old_players(sequenceConfig)


def _select_next_piece(sequenceConfig):
    sequenceConfig.startTime = time.time()

    if sequenceConfig.playInOrder:
        sequenceConfig.playOrder = (sequenceConfig.playOrder + 1) % len(sequenceConfig.workList)
        pieceToPlay = sequenceConfig.playOrder
    else:
        pieceToPlay = random.randrange(len(sequenceConfig.workList))

    work = sequenceConfig.workList[pieceToPlay]
    print(bcolors.WARNING)
    print("---------------------------------------------------------------------------------------")
    print(f"Piece Playing is: {pieceToPlay}")
    print(work)
    # print("---------------------------------------------------------------------------------------")

    sequenceConfig.currentPieceDuration = round(random.uniform(work[1], work[2]))


def _launch_next_player(sequenceConfig):
    scriptsPath = f"{os.path.dirname(__file__)}/"
    pieceToPlay = sequenceConfig.playOrder if sequenceConfig.playInOrder else random.randrange(len(sequenceConfig.workList))
    work = sequenceConfig.workList[pieceToPlay]

    brightnessOverrideString = f"{work[3]}" if work[3] else ""
    # commandString = "player.py"
    commandString = f"{scriptsPath}player.py"
    arg1 = "-cfg"
    arg2 = f"{work[0]}"
    arg4 = brightnessOverrideString

    print("---------------------------------------------------------------------------------------")
    print("Sequencer is calling :\n" + commandString)
    print("---------------------------------------------------------------------------------------")
    print(bcolors.ENDC)

    if arg4 != "":
        arg3 = "-brightnessOverride"
        subprocess.Popen(["python3", commandString, arg1, arg2, arg3, arg4])
    else:
        subprocess.Popen(["python3", commandString, arg1, arg2])
    sequenceConfig.playCount += 1


def _kill_old_players(sequenceConfig):
    time.sleep(3)

    try:
        listOfProcs = check_output("ps -ef | pgrep -f -a player", stdin=None, stderr=None, shell=True, universal_newlines=True).split("\n")
        print(bcolors.WARNING)
        print("---------------------------------------------------------------------------------------")
        print("Sequencer is killing off old window(s)")
        print(f"count play : {sequenceConfig.playCount}")
        print(f"Running player instances are : {len(str(sequenceConfig.currentPID))}")
        print(listOfProcs)
        # print("---------------------------------------------------------------------------------------")
        listToCheck = listOfProcs[:-2]
        print(listToCheck)
        # print(len(listToCheck))
        print("---------------------------------------------------------------------------------------")

        if len(listToCheck) == 2:
            # just kill the first in the list (i.e. the oldest player running)
            # but this does not cover if there are more than two running ....
            subprocess.run([f"kill {listToCheck[0]}"], shell=True, check=True)
        elif len(listToCheck) > 2:
            try:
                for p in listToCheck[:-1]:
                    if str(sequenceConfig.currentPID) not in p:
                        len(str(sequenceConfig.currentPID))
                        print("---------------------------------------------------------------------------------------")
                        print(f"{str(sequenceConfig.currentPID)} : Should be killing {p}")
                        len(str(sequenceConfig.currentPID))
                        subprocess.run([f"kill {p}"], shell=True, check=True)
            except Exception as e:
                print(e)
        # comment:
        print("---------------------------------------------------------------------------------------")
        print(bcolors.ENDC)
    except Exception as e:
        print(e)

        # end try



def loadWorkConfig(work, sequenceConfig):

    workconfig = configparser.ConfigParser()
    # config = configuration.Config()
    config = configuration.ArtWorkConfig("SEQUENCER PLAYER")
    config.startTime = time.time()
    config.currentTime = time.time()
    config.reloadConfig = False
    config.doingReload = False
    config.checkForConfigChanges = False
    config.brightnessOverride = work[3]

    config.renderImageFull = sequenceConfig.renderImageFull
    config.isRunning = True
    # This is so the Player does not create a window
    config.standAlone = False
    config.callBack = lambda: timeChecker(sequenceConfig, config)

    config.MID = ""
    config.path = sequenceConfig.path

    argument = f"{config.path}/configs/{work[0]}"

    print(bcolors.WARNING)
    print("---------------------------------------------------------------------------------------")
    print(f"Sequencer: first work cfg {work[0]}")
    print(f"Sequencer: loading {argument}")
    print("---------------------------------------------------------------------------------------")
    print(bcolors.ENDC)
    workconfig.read(argument)
    config.fileName = argument

    sequenceConfig.currentPID = os.getpid()
    print("---------------------------------------------------------------------------------------")
    print(f"Sequence Player PID is: {sequenceConfig.currentPID}")
    print("---------------------------------------------------------------------------------------")

    callBack(sequenceConfig, config)


def callBack(sequenceConfig, config):
    while True:
        time.sleep(1)
        timeChecker(sequenceConfig, config)


def loadConfigFile():
    parser = argparse.ArgumentParser(description="Process")
    parser.add_argument("-mname", type=str, default="local", help="machine name (optional)")
    parser.add_argument("-path", type=str, default="./", help="directory (optional)")
    parser.add_argument(
        "-cfg",
        type=str,
        required=False,
        help="Config File - just need sub-folder and name - e.g. p4-6x5/repeater.cfg",
    )
    parser.add_argument(
        "-brightnessOverride",
        type=int,
        help="brightness param to override the config value (optional)",
    )
    return parser.parse_args()


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def loadSequenceFile():
    print(f"{bcolors.WARNING}\n\n\n************************************************\n\n")
    args = loadConfigFile()

    if args.cfg != None:

        workconfig = configparser.ConfigParser()

        _loadSequencer_print_args("Inital Sequencer Arguments: \n", args)

        # sequenceConfig = configuration.Config()
        sequenceConfig = configuration.ArtWorkConfig("SEQUENCER")
        sequenceConfig.startTime = time.time()
        sequenceConfig.currentTime = time.time()
        sequenceConfig.MID = args.mname
        sequenceConfig.path = args.path

        print("script: sys.argv[0] is", repr(sys.argv[0]))
        print("script: __file__ is", repr(__file__))
        print("script: cwd is", repr(os.getcwd()))
        print("config: path  is", repr(args.path))

        # Automating the config path a bit better
        # assumes that if no -path is specified, it defaults to ./ so
        # just to be sure get the abs path
        if sequenceConfig.path == "./":
            sequenceConfig.path = __file__.replace("sequencer.v2.py", "") + "/"

        argument = f"{sequenceConfig.path}configs/{args.cfg}"

        _loadSequencer_print_args("-cfg sequencer argument: \n", argument)
        workconfig.read(argument)

        sequenceConfig.fileName = argument
        sequenceConfig.fileNameRaw = args.cfg

        sequenceConfig.playInOrder = workconfig.getboolean("displayconfig", "playInOrder")
        sequenceConfig.playOrder = 0

        sequenceConfig.workListManifest = list(workconfig.get("displayconfig", "workList").split(","))
        sequenceConfig.currentPieceDuration = 1
        sequenceConfig.playCount = 0

        sequenceConfig.workList = []

        for w in sequenceConfig.workListManifest:
            work = workconfig.get(w, "work")
            minDuration = float(workconfig.get(w, "minDuration"))
            maxDuration = float(workconfig.get(w, "maxDuration"))
            try:
                brightnessOverride = float(workconfig.get(w, "brightnessOverride"))
            except Exception as e:
                print(f" ==> brightnessOverride not defined {e} ")
                brightnessOverride = None

            sequenceConfig.workList.append([work, minDuration, maxDuration, brightnessOverride])

        print(f"{bcolors.WARNING}---------------------------------------------------------------------------------------")
        print("WorkList:")
        print(sequenceConfig.workList)

        sequenceConfig.mainAppWindow = appWindow.AppWindow(sequenceConfig)
        sequenceConfig.mainAppWindow.setUp()
        sequenceConfig.mainAppWindow.createMainCanvas()

        pieceToPlay = round(random.SystemRandom().uniform(0, len(sequenceConfig.workList) - 1))
        pieceToPlay = 0
        loadWorkConfig(sequenceConfig.workList[pieceToPlay], sequenceConfig)
        print(f"{bcolors.ENDC}")


def _loadSequencer_print_args(arg0, arg1):
    print(bcolors.WARNING)
    print("---------------------------------------------------------------------------------------")
    print(arg0 + str(arg1))
    # print("---------------------------------------------------------------------------------------")
    print(bcolors.ENDC)

    # sequenceConfig.mainAppWindow.run()


def main():
    global config, threads

    loadSequenceFile()

    """
    # Threading now handled by renderer - e.g. see modules/render.py
    thrd = threading.Thread(target=configure)
    threads.append(thrd)
    thrd.start()
    """


# Kick off .......
if __name__ == "__main__":
    main()
