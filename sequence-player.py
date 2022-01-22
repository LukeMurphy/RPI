#!/usr/bin/python

import argparse
import configparser
import getopt
import os
import sys
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
'''


def timeChecker(sequenceConfig, config) :
	sequenceConfig.currentTime = time.time()

	print(sequenceConfig.currentTime - sequenceConfig.startTime, sequenceConfig.currentPieceDuration )

	if sequenceConfig.currentTime - sequenceConfig.startTime > sequenceConfig.currentPieceDuration :
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

		sequenceConfig.currentPieceDuration = random.uniform(sequenceConfig.workList[pieceToPlay][1], sequenceConfig.workList[pieceToPlay][2])
		
		# Launch the next player
		commandString = sequenceConfig.commadStringPyth  + " " + sequenceConfig.workListDirectory + sequenceConfig.workList[pieceToPlay][0] + "&"
		print("Command:  " + commandString)
		os.system(commandString)

		sequenceConfig.playCount=sequenceConfig.playCount+1
		print("==========> count play : " + str(sequenceConfig.playCount))

		# wait for the player to load before cleaning up
		time.sleep(1)

		# Now check all the running python scripts and kill the one before the one that was just launched
		listOfProcs = check_output("ps -ef | pgrep -i python", stdin=None, stderr=None, shell=True, universal_newlines=True).split("\n")

		print("Running python instances are :")
		print(listOfProcs)

		try:
			for p in listOfProcs[:-2] :
				print(p)
				if p != str(sequenceConfig.currentPID) and p != "":
					print (str(sequenceConfig.currentPID) + " : Should be killing " + p)
					subprocess.run(["kill " + p], shell=True, check=True)
		except Exception as e:
			print(str(e))




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

	argument = config.path + "/configs/" + sequenceConfig.workListDirectory + work[0]

	print(bcolors.WARNING + "** ")
	print("Sequencer: " + work[0] + ":" + argument)
	print(bcolors.ENDC)
	workconfig.read(argument)
	config.fileName = argument


	sequenceConfig.currentPID = os.getpid()
	print("Sequence Player PID is: " + str(sequenceConfig.currentPID))

	'''

	if (sequenceConfig.playCount > sequenceConfig.repeatCountTrigger) :

		sequenceConfig.playCount = 0
		# Clean threads!

		#print(sequenceConfig.mainAppWindow.activeWork.config.isRunning)
		#print(sequenceConfig.mainAppWindow.activeWork)
		#print(sequenceConfig.mainAppWindow.activeWork.config.standAlone)
		print("DONE .....")
		#exit()
		#sequenceConfig.mainAppWindow.activeWork.config.isRunning = False
		#sequenceConfig.mainAppWindow.activeWork.config.callBack()
		#os.system( config.path  + sequenceConfig.restartScript)

	
	# ****************************************** #
	# Sets off the piece based on loading the initiail configs #
	# ****************************************** #
	'''
	'''
	player.configure(config, workconfig)
	config.cnvs = sequenceConfig.cnvs
	sequenceConfig.mainAppWindow.startWork(config.workRefForSequencer)
	'''

	fakeCallBack(sequenceConfig, config)

def fakeCallBack(sequenceConfig, config) :
	while 1==1 :
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

		print(bcolors.OKBLUE + "** " + str(args) + ""  + bcolors.ENDC)
		sequenceConfig = configuration.Config()
		sequenceConfig.startTime = time.time()
		sequenceConfig.currentTime = time.time()
		sequenceConfig.MID = args.mname
		sequenceConfig.path = args.path

		argument = sequenceConfig.path + "/configs/" + args.cfg  # + ".cfg"
		workconfig.read(argument)

		sequenceConfig.fileName = argument
		sequenceConfig.fileNameRaw = args.cfg

		sequenceConfig.imageXOffset = int(workconfig.get("displayconfig", "imageXOffset"))
		sequenceConfig.imageYOffset = int(workconfig.get("displayconfig", "imageYOffset"))

		sequenceConfig.canvasOffsetX = int(workconfig.get("displayconfig", "canvasOffsetX"))
		sequenceConfig.canvasOffsetY = int(workconfig.get("displayconfig", "canvasOffsetY"))

		sequenceConfig.screenHeight = int(workconfig.get("displayconfig", "screenHeight"))
		sequenceConfig.screenWidth = int(workconfig.get("displayconfig", "screenWidth"))

		sequenceConfig.windowXOffset = int(workconfig.get("displayconfig", "windowXOffset"))
		sequenceConfig.windowYOffset = int(workconfig.get("displayconfig", "windowYOffset"))


		sequenceConfig.playInOrder = (workconfig.getboolean("displayconfig", "playInOrder"))
		sequenceConfig.commadStringPyth = (workconfig.get("displayconfig", "commadStringPyth"))
		sequenceConfig.playOrder = 0 

		try:
			sequenceConfig.forceBGSwap  = (workconfig.getboolean("displayconfig", "forceBGSwap"))
		except Exception as e:
			print(str(e))
			sequenceConfig.forceBGSwap  = False

		sequenceConfig.workListDirectory = workconfig.get("displayconfig", "workListDirectory")
		sequenceConfig.workListManifest = list(workconfig.get("displayconfig","workList").split(','))
		sequenceConfig.currentPieceDuration = 1
		sequenceConfig.playCount = 0

		try:
			sequenceConfig.restartScript = workconfig.get("displayconfig", "restartScript")
			sequenceConfig.repeatCountTrigger = int(workconfig.get("displayconfig", "repeatCountTrigger"))
		except Exception as e:
			print(str(e))
			sequenceConfig.restartScript = '/cntrlscripts/restart_full_sequencer.sh'
			sequenceConfig.repeatCountTrigger = 100


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


		print(sequenceConfig.workList)


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
