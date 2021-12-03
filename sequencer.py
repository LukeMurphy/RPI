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


def timeChecker(sequenceConfig):
	sequenceConfig.currentTime = time.time()

	if sequenceConfig.currentTime - sequenceConfig.startTime > sequenceConfig.currentPieceDuration:
		sequenceConfig.startTime = time.time()

		if (sequenceConfig.playCount > sequenceConfig.repeatCountTrigger) :
			# Just clean out any stragglers just in case
			print("==========> Ending ALL WINDOWS ")    
			os.system("ps -ef | pgrep -f player | xargs kill -9;")
			sequenceConfig.playCount = 0

		if sequenceConfig.playInOrder == True:
			sequenceConfig.playOrder += 1
			if sequenceConfig.playOrder >= len(sequenceConfig.workList):
				sequenceConfig.playOrder = 0
			pieceToPlay = sequenceConfig.playOrder
		else:
			pieceToPlay = round(random.uniform(
				0, len(sequenceConfig.workList)))
			if pieceToPlay == len(sequenceConfig.workList):
				pieceToPlay = 0

		print("Piece Playing is: " + str(pieceToPlay))

		sequenceConfig.currentPieceDuration = random.uniform(
			sequenceConfig.workList[pieceToPlay][1], sequenceConfig.workList[pieceToPlay][2])

		# This is now specified in the config file
		#commadStringPyth = "python3 /Users/lamshell/Documents/Dev/RPI/player.py -path /Users/lamshell/Documents/Dev/RPI -mname studio -cfg"
		currentPID = os.popen("ps -ef | pgrep -f player").read()

		print("Current PID = {}".format(currentPID))
		#os.system("ps -ef | pgrep -f player | xargs kill -9;")

		runString = sequenceConfig.commadStringPyth + " " + \
			sequenceConfig.workListDirectory + \
			sequenceConfig.workList[pieceToPlay][0] + "&"

		os.system(sequenceConfig.commadStringPyth + " " +
				  sequenceConfig.workListDirectory + sequenceConfig.workList[pieceToPlay][0] + "&")

		# then kill the underlying window
		# this is a dirtyish solution but was getting gnarly issues with stack-overflows
		#loadWorkConfig(sequenceConfig.workList[pieceToPlay], sequenceConfig)


		print("==========> count play : " + str(sequenceConfig.playCount)	+ " / " + str(sequenceConfig.repeatCountTrigger))
		if sequenceConfig.playCount >=1 or len(str(currentPID))!= 0 :
			print("==========> Ending back window in 2 seconds")	
			time.sleep(2)
			os.system("kill -9 " + str(currentPID))

		sequenceConfig.playCount = sequenceConfig.playCount + 1


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
	config.callBack = lambda: timeChecker(sequenceConfig, config)

	config.MID = ""
	config.path = sequenceConfig.path

	argument = config.path + "/configs/" + \
		sequenceConfig.workListDirectory + work[0]

	print(bcolors.WARNING + "** ")
	print("Sequencer: " + work[0] + ":" + argument)
	print(bcolors.ENDC)
	workconfig.read(argument)
	config.fileName = argument
	sequenceConfig.playCount = sequenceConfig.playCount+1
	print("==========> count play : " + str(sequenceConfig.playCount))

	# This does not get called anymore -

	if (sequenceConfig.playCount > sequenceConfig.repeatCountTrigger):
		# Clean threads!
		pass
		# print(sequenceConfig.mainAppWindow.activeWork.config.isRunning)
		# print(sequenceConfig.mainAppWindow.activeWork)
		# print(sequenceConfig.mainAppWindow.activeWork.config.standAlone)
		#print("DONE .....")
		# exit()
		#sequenceConfig.mainAppWindow.activeWork.config.isRunning = False
		# sequenceConfig.mainAppWindow.activeWork.config.callBack()
		#os.system( config.path  + sequenceConfig.restartScript)

	# ****************************************** #
	# Sets off the piece based on loading the initiail configs #
	# ****************************************** #

	'''
	player.configure(config, workconfig)
	config.cnvs = sequenceConfig.cnvs
	sequenceConfig.mainAppWindow.startWork(config.workRefForSequencer)
	'''


# This timer just checks the time and if the piece has played its allotted
# amount, load the next one and then close the window of the one playing
# a second or two later -- was having trouble with stack-overflow by reloading
# the same player into one window - and not being able to thread TKinter

def fakeCallBack(sequenceConfig):
	while 1 == 1:
		time.sleep(1)
		timeChecker(sequenceConfig)


def loadConfigFile():
	parser = argparse.ArgumentParser(description="Process")
	parser.add_argument("-mname", type=str, default="local",
						help="machine name (optional)")
	parser.add_argument("-path", type=str, default="./",
						help="directory (optional)")
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

		print(bcolors.OKBLUE + "** " + str(args) + "" + bcolors.ENDC)
		sequenceConfig = configuration.Config()
		sequenceConfig.startTime = time.time()
		sequenceConfig.currentTime = time.time()
		sequenceConfig.MID = args.mname
		sequenceConfig.path = args.path

		argument = sequenceConfig.path + "/configs/" + args.cfg  # + ".cfg"
		workconfig.read(argument)

		sequenceConfig.fileName = argument
		sequenceConfig.fileNameRaw = args.cfg

		sequenceConfig.imageXOffset = int(
			workconfig.get("displayconfig", "imageXOffset"))
		sequenceConfig.imageYOffset = int(
			workconfig.get("displayconfig", "imageYOffset"))

		sequenceConfig.canvasOffsetX = int(
			workconfig.get("displayconfig", "canvasOffsetX"))
		sequenceConfig.canvasOffsetY = int(
			workconfig.get("displayconfig", "canvasOffsetY"))

		sequenceConfig.screenHeight = int(
			workconfig.get("displayconfig", "screenHeight"))
		sequenceConfig.screenWidth = int(
			workconfig.get("displayconfig", "screenWidth"))

		sequenceConfig.windowXOffset = int(
			workconfig.get("displayconfig", "windowXOffset"))
		sequenceConfig.windowYOffset = int(
			workconfig.get("displayconfig", "windowYOffset"))

		sequenceConfig.playInOrder = (
			workconfig.getboolean("displayconfig", "playInOrder"))
		sequenceConfig.playOrder = 0

		try:
			sequenceConfig.forceBGSwap = (
				workconfig.getboolean("displayconfig", "forceBGSwap"))
		except Exception as e:
			print(str(e))
			sequenceConfig.forceBGSwap = False

		sequenceConfig.workListDirectory = workconfig.get(
			"displayconfig", "workListDirectory")
		sequenceConfig.workListManifest = list(
			workconfig.get("displayconfig", "workList").split(','))
		sequenceConfig.currentPieceDuration = 1
		sequenceConfig.playCount = 0

		try:
			sequenceConfig.restartScript = workconfig.get(
				"displayconfig", "restartScript")
		except Exception as e:
			print(str(e))
			sequenceConfig.restartScript = '/cntrlscripts/restart_full_sequencer.sh'

		try:
			sequenceConfig.repeatCountTrigger = int(
				workconfig.get("displayconfig", "repeatCountTrigger"))
		except Exception as e:
			print(str(e))
			sequenceConfig.repeatCountTrigger = 100

		sequenceConfig.commadStringPyth = workconfig.get(
			"displayconfig", "commadStringPyth")

		sequenceConfig.workList = []

		for w in sequenceConfig.workListManifest:
			work = workconfig.get(w, "work")
			minDuration = float(workconfig.get(w, "minDuration"))
			maxDuration = float(workconfig.get(w, "maxDuration"))
			try:
				brightnessOverride = float(
					workconfig.get(w, "brightnessOverride"))
			except Exception as e:
				print(str(e))
				brightnessOverride = None

			sequenceConfig.workList.append(
				[work, minDuration, maxDuration, brightnessOverride])

		print(sequenceConfig.workList)

		'''
		sequenceConfig.mainAppWindow = appWindow.AppWindow(sequenceConfig)
		sequenceConfig.mainAppWindow.setUp()
		sequenceConfig.mainAppWindow.createMainCanvas()

		pieceToPlay = round(random.uniform(0, len(sequenceConfig.workList)-1))
		pieceToPlay = 0
		loadWorkConfig(sequenceConfig.workList[pieceToPlay], sequenceConfig)
		'''

		fakeCallBack(sequenceConfig)

		# sequenceConfig.mainAppWindow.run()


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
