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


def timeChecker(sequenceConfig, config) :
	sequenceConfig.currentTime = time.time()

	if sequenceConfig.currentTime - sequenceConfig.startTime > sequenceConfig.currentPieceDuration :
		sequenceConfig.startTime = time.time()

		if sequenceConfig.playInOrder == True :
			sequenceConfig.playOrder += 1
			if sequenceConfig.playOrder >= len(sequenceConfig.workList) :
				sequenceConfig.playOrder = 0
			pieceToPlay = sequenceConfig.playOrder
		else :
			pieceToPlay = round(random.uniform(0, len(sequenceConfig.workList)-1))

		print("Piece Playing is: " + str(pieceToPlay))

		sequenceConfig.currentPieceDuration = random.uniform(sequenceConfig.workList[pieceToPlay][1], sequenceConfig.workList[pieceToPlay][2])
		loadWorkConfig(sequenceConfig.workList[pieceToPlay], sequenceConfig)


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



	# ****************************************** #
	# Sets off the piece based on loading the initiail configs #
	# ****************************************** #
	player.configure(config, workconfig)
	config.cnvs = sequenceConfig.cnvs
	sequenceConfig.mainAppWindow.startWork(config.workRefForSequencer)



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
		sequenceConfig.playOrder = 0 

		sequenceConfig.forceBGSwap  = (workconfig.getboolean("displayconfig", "forceBGSwap"))

		sequenceConfig.workListDirectory = workconfig.get("displayconfig", "workListDirectory")
		sequenceConfig.workListManifest = list(workconfig.get("displayconfig","workList").split(','))
		sequenceConfig.currentPieceDuration = 1

		sequenceConfig.workList = []

		for w in sequenceConfig.workListManifest :
			work = workconfig.get(w, "work")
			minDuration = int(workconfig.get(w, "minDuration"))
			maxDuration = int(workconfig.get(w, "maxDuration"))
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

		sequenceConfig.mainAppWindow.run()




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
