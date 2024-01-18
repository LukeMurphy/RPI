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

from modules import configuration, player
from modules.rendering import appWindow
from modules.configuration import bcolors

import subprocess
from subprocess import check_output


'''
This file runs as a daemon to mange the sequence of players
Mange is right
I can barely remember how this works

basically it starts a new player and kills off the previous one over and over again to
avoid a memory leak by having one player re-load new configs that I had the last time
not elegant but way more maintainable  ;)

'''


def timeChecker(sequenceConfig, config) :

    sequenceConfig.currentTime = time.time()

    # uncomment to debug
    #print(bcolors.WARNING + "** " + "sequence-player.py checking the time ... " + str(round(sequenceConfig.currentTime - sequenceConfig.startTime)) + " / " + str(sequenceConfig.currentPieceDuration) + ""  + bcolors.ENDC)
    

    if sequenceConfig.currentTime - sequenceConfig.startTime > sequenceConfig.currentPieceDuration:
        sequenceConfig.startTime = time.time()

        if sequenceConfig.playInOrder == True :
            sequenceConfig.playOrder += 1
            if sequenceConfig.playOrder >= len(sequenceConfig.workList) :
                sequenceConfig.playOrder = 0
            pieceToPlay = sequenceConfig.playOrder
        else :
            pieceToPlay = round(random.uniform(0, len(sequenceConfig.workList)))
            if pieceToPlay == len(sequenceConfig.workList) :
                pieceToPlay = 0

        print("Piece Playing is: " + str(pieceToPlay))
        print(sequenceConfig.workList[pieceToPlay])

        sequenceConfig.currentPieceDuration = round(random.uniform(sequenceConfig.workList[pieceToPlay][1], sequenceConfig.workList[pieceToPlay][2]))
        
        # Launch the next player
        # should be able to infer this without explicit specifications in the config
        # commandString = sequenceConfig.commadStringPyth  + " " + sequenceConfig.workListDirectory + sequenceConfig.workList[pieceToPlay][0] + "&"
        scriptsPath = __file__.replace('sequencer.v2.py','')+ "/"
        commandString = "python3 " + scriptsPath + "player.py"  + " -cfg " + sequenceConfig.workList[pieceToPlay][0] + "&"
        
        print(bcolors.WARNING)
        print("--------------------------------")
        print("Sequencer is calling :\n" + commandString)
        print("--------------------------------")
        print(bcolors.ENDC)
        
        os.system(commandString)

        sequenceConfig.playCount=sequenceConfig.playCount+1

        # moved to a time-based re
        # if sequenceConfig.playCount > sequenceConfig.repeatCountTrigger :
        # 	sequenceConfig.playCount = 0

        # wait for the player to load before cleaning up
        time.sleep(3)

        # Now check all the running python scripts and kill the one before the one that was just launched
        # assumes only these two are running 
        try:
            listOfProcs = check_output("ps -ef | pgrep -f -a player", stdin=None, stderr=None, shell=True, universal_newlines=True).split("\n")

            print(bcolors.WARNING)
            print("--------------------------------")
            print("Sequencer is killing off old window(s)")
            print("count play : " + str(sequenceConfig.playCount))
            print("Running player instances are : " + str(len(str(sequenceConfig.currentPID))))
            print(listOfProcs)
            print("----")
            listToCheck = listOfProcs[:-2]
            print(listToCheck)
            # print(len(listToCheck))
            print("----")
            
            if len(listToCheck) == 2  :
                # just kill the first in the list (i.e. the oldest player running)
                # but this does not cover if there are more than two running ....
                subprocess.run(["kill " + listToCheck[0]], shell=True, check=True)
            elif len(listToCheck) > 2 :
                try:
                    for p in listToCheck[:-1] :
                        if str(sequenceConfig.currentPID) not in p:
                            len(str(sequenceConfig.currentPID))
                            print (str(sequenceConfig.currentPID) + " : Should be killing " + p)
                            len(str(sequenceConfig.currentPID))
                            subprocess.run(["kill " + p], shell=True, check=True)
                except Exception as e:
                    print(str(e))
            # comment: 
            print("--------------------------------")
            print(bcolors.ENDC)
        except Exception as e:
            print(str(e))
        
        # end try




def loadWorkConfig(work, sequenceConfig):

    workconfig = configparser.ConfigParser()
    config = configuration.Config()
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
    config.callBack = lambda : timeChecker(sequenceConfig, config)

    config.MID = ""
    config.path = sequenceConfig.path

    argument = config.path + "/configs/" + work[0]

    print(bcolors.WARNING)
    print("--------------------------------")
    print("Sequencer: first work cfg " + work[0])
    print("Sequencer: loading " + argument)
    print("--------------------------------")
    print(bcolors.ENDC)
    workconfig.read(argument)
    config.fileName = argument


    sequenceConfig.currentPID = os.getpid()
    print("--------------------------------")
    print("Sequence Player PID is: " + str(sequenceConfig.currentPID))
    print("--------------------------------")

    fakeCallBack(sequenceConfig, config)



def fakeCallBack(sequenceConfig, config) :
    while 1==1 :
        # checks the time every second - could configure this if really
        # necessary
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
    args = parser.parse_args()
    return args

"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
def loadSequenceFile():

    args = loadConfigFile()

    if args.cfg != None:

        workconfig = configparser.ConfigParser()

        print(bcolors.OKBLUE)
        print("--------------------------------")
        print("Inital Sequencer Arguments: \n" + str(args))
        print("--------------------------------")
        print(bcolors.ENDC) 
        
        sequenceConfig = configuration.Config()
        sequenceConfig.startTime = time.time()
        sequenceConfig.currentTime = time.time()
        sequenceConfig.MID = args.mname
        sequenceConfig.path = args.path
        
        
        print("-----------------------------------------")
        print ("script: sys.argv[0] is", repr(sys.argv[0]))
        print ("script: __file__ is", repr(__file__))
        print ("script: cwd is", repr(os.getcwd()))
        print ("config: path  is", repr(args.path))
        
        # Automating the config path a bit better
        # assumes that if no -path is specified, it defaults to ./ so 
        # just to be sure get the abs path
        if sequenceConfig.path == './' :
            sequenceConfig.path = __file__.replace('sequencer.v2.py','')+ "/"
            

        argument = sequenceConfig.path + "configs/" + args.cfg  # + ".cfg"
        
        print(bcolors.OKBLUE)
        print("--------------------------------")
        print("-cfg sequencer argument: \n" + str(argument))
        print("--------------------------------")
        print(bcolors.ENDC)

        workconfig.read(argument)

        sequenceConfig.fileName = argument
        sequenceConfig.fileNameRaw = args.cfg

        sequenceConfig.playInOrder = (workconfig.getboolean("displayconfig", "playInOrder"))
        sequenceConfig.playOrder = 0 

        sequenceConfig.workListManifest = list(workconfig.get("displayconfig","workList").split(','))
        sequenceConfig.currentPieceDuration = 1
        sequenceConfig.playCount = 0

        sequenceConfig.workList = []

        for w in sequenceConfig.workListManifest :
            work = workconfig.get(w, "work")
            minDuration = float(workconfig.get(w, "minDuration"))
            maxDuration = float(workconfig.get(w, "maxDuration"))
            try:
                brightnessOverride = float(workconfig.get(w,"brightnessOverride"))
            except Exception as e:
                print(str(e))
                brightnessOverride = None


            sequenceConfig.workList.append([work,minDuration,maxDuration,brightnessOverride])

        print("--------------------------------")
        print("WorkList:")
        print(sequenceConfig.workList)
        print("--------------------------------")


        sequenceConfig.mainAppWindow = appWindow.AppWindow(sequenceConfig)
        sequenceConfig.mainAppWindow.setUp()
        sequenceConfig.mainAppWindow.createMainCanvas()

        pieceToPlay = round(random.uniform(0, len(sequenceConfig.workList)-1))
        pieceToPlay = 0
        loadWorkConfig(sequenceConfig.workList[pieceToPlay], sequenceConfig)

        #sequenceConfig.mainAppWindow.run()




def main():
    global config, threads

    loadSequenceFile()
    
    """
    # Threading now handled by renderer - e.g. see modules/rendertohub.py
    thrd = threading.Thread(target=configure)
    threads.append(thrd)
    thrd.start()
    """


# Kick off .......
if __name__ == "__main__":
    main()
