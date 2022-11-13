#!/usr/bin/python

import argparse
import configparser
import getopt
import os
import sys
import time
import math
import random

from datetime import datetime
import pytz
from pytz import timezone

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


def timeChecker(sequenceConfig) :

	sequenceConfig.currentTime = time.time()

	# uncomment to debug
	#print(bcolors.WARNING + "** " + "sequence-player.py checking the time ... " + str(round(sequenceConfig.currentTime - sequenceConfig.startTime)) + " / " + str(sequenceConfig.currentPieceDuration) + ""  + bcolors.ENDC)
	
	tz = pytz.timezone('US/Eastern')
	now = tz.localize(datetime.now())
	#now = datetime.now()
	current_time = now.strftime("%H:%M")
	#print("Current Time =", current_time, now, now.minute, now.hour)

	#if sequenceConfig.currentTime - sequenceConfig.startTime > sequenceConfig.currentPieceDuration:
	if current_time in sequenceConfig.startPieceTimes and sequenceConfig.isPlayingAPiece == False:

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

		sequenceConfig.isPlayingAPiece = True
		sequenceConfig.currentPieceDuration = round(random.uniform(sequenceConfig.workList[pieceToPlay][1], sequenceConfig.workList[pieceToPlay][2]))
		sequenceConfig.startPieceTimes =  sequenceConfig.workList[pieceToPlay][3]
		sequenceConfig.stopPieceTimes =  sequenceConfig.workList[pieceToPlay][4]
		
		# Launch the next player
		commandString = sequenceConfig.commadStringPyth  + " " + sequenceConfig.workListDirectory + sequenceConfig.workList[pieceToPlay][0] + "&"
		print("Command:  " + commandString)
		os.system(commandString)

		sequenceConfig.playCount = sequenceConfig.playCount+1

		if sequenceConfig.playCount > sequenceConfig.repeatCountTrigger :
			sequenceConfig.playCount = 0

		# wait for the player to load before cleaning up
		# time.sleep(1)
		# checkAndEndPieces(sequenceConfig)

	if current_time in sequenceConfig.stopPieceTimes and sequenceConfig.isPlayingAPiece == True:
		sequenceConfig.isPlayingAPiece = False
		checkAndEndPieces(sequenceConfig)




def checkAndEndPieces(sequenceConfig) :
		# Now check all the running python scripts and kill the one before the one that was just launched
		# assumes only these two are running 
		print(bcolors.WARNING + "==========> count play : " + str(sequenceConfig.playCount))
		print("Running python instances are :")

		try:
			listOfProcsRaw = subprocess.check_output("ps -ef | pgrep -i -f 'player.py'", stdin=None, stderr=None, shell=True, universal_newlines=True)
			#print(listOfProcsRaw)
			listOfProcs = listOfProcsRaw.split("\n")
		except Exception as e:
			print(str(e))
			listOfProcs = []

		#print(listOfProcs)

		try:
			for p in listOfProcs[:2] :
				print (" : Should be killing " + p)
				if p != "" :
					subprocess.run(["kill " + p], shell=True, check=True)
		except Exception as e:
			print(str(e))
		print(bcolors.ENDC)


def iterateCheck(sequenceConfig) :
	while 1==1 :
		# checks the time every second - could configure this if really
		# necessary
		time.sleep(20)
		timeChecker(sequenceConfig)	


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

		argument = sequenceConfig.path + "" + args.cfg  # + ".cfg"
		print(bcolors.OKBLUE + "** " + argument + ""  + bcolors.ENDC)
		workconfig.read(argument)

		sequenceConfig.fileName = argument
		sequenceConfig.fileNameRaw = args.cfg


		sequenceConfig.playInOrder = (workconfig.getboolean("displayconfig", "playInOrder"))
		sequenceConfig.commadStringPyth = (workconfig.get("displayconfig", "commadStringPyth"))
		sequenceConfig.playOrder = 0 

		sequenceConfig.workListDirectory = workconfig.get("displayconfig", "workListDirectory")
		sequenceConfig.workListManifest = list(workconfig.get("displayconfig","workList").split(','))
		sequenceConfig.currentPieceDuration = 1
		sequenceConfig.playCount = 0

	
		tz = pytz.timezone('US/Eastern')
		now = tz.localize(datetime.now())
		#now = datetime.now()
		current_time = now.strftime("%H:%M")
		print("Current Time =", current_time, now, now.minute, now.hour)

		sequenceConfig.startPieceTimes = [current_time]
		sequenceConfig.stopPieceTimes = []
		sequenceConfig.isPlayingAPiece = False


		try:
			sequenceConfig.repeatCountTrigger = int(workconfig.get("displayconfig", "repeatCountTrigger"))
		except Exception as e:
			print(str(e))
			sequenceConfig.repeatCountTrigger = 100


		sequenceConfig.workList = []

		for w in sequenceConfig.workListManifest :
			work = workconfig.get(w, "work")
			startPiece = workconfig.get(w, "startPiece").split(",")
			stopPiece = workconfig.get(w, "stopPiece").split(",")
			minDuration = float(workconfig.get(w, "minDuration"))
			maxDuration = float(workconfig.get(w, "maxDuration"))
			try:
				brightnessOverride = float(workconfig.get(w,"brightnessOverride"))
			except Exception as e:
				print(str(e))
				brightnessOverride = None


			sequenceConfig.workList.append([work,minDuration,maxDuration,startPiece,stopPiece,brightnessOverride])

		print("--------------------------------")
		print("--------------------- WorkList")
		print(sequenceConfig.workList)


		pieceToPlay = round(random.uniform(0, len(sequenceConfig.workList)-1))
		pieceToPlay = 0


		timeChecker(sequenceConfig)
		iterateCheck(sequenceConfig)



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
