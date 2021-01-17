#!/usr/bin/python
# Two instance player

"""
p4-3x8-informal/quilt-triangles-b

p4-3x8-informal/quilt
"""

import argparse
import configparser
import getopt
import os
import random
import sys
import threading
import time

from threading import Timer
from modules import configuration, workobject
from modules.configuration import Config, bcolors
from modules.rendering import appWindow, renderClass

# Create a blank dummy object container for now
# config = type('', (object,), {})()

##########################################################################
#
#
# -------   Reads configuration files and sets defaults
# -------   Piece is initiated by command line: e.g.
# sudo python /Users/lamshell/Documents/Dev/LED-MATRIX-RPI/RPI/player.py studio-mac ./ configs/fludd.cfg &
#
#
##########################################################################


def loadFromArguments(masterConfig, reloading=False):

	if reloading == False:

		###
		# Expects 3 arguments:
		# 		name-of-machine
		#       the local path
		# 		the config file to load
		"""
		args = sys.argv
		print("Arguments passed to player.py:")
		print(args)
		"""

		loadTheConfig(masterConfig)

		# Set up the app window
		workWindow = appWindow.AppWindow(masterConfig)
		workWindow.setUp()

		# set up the common rendder -- i.e. everything renders here
		# but really there should be more than one renderImageFull ....
		workWindow.renderer = renderClass.CanvasElement(workWindow.root, masterConfig)
		workWindow.renderer.masterConfig = masterConfig
		workWindow.renderer.canvasXPosition = 0
		workWindow.renderer.delay = 1
		workWindow.renderer.setUpCanvas(workWindow.root)
		workWindow.renderer.setUp()

		workWindow.players = []

	else:
		#### TO BE IMPLEMENTED - NEED TO KILL ALL THE THREADS AND THEN
		#### RELOAD WINDOW ETC
		print(">> reloading: ")

	for i in range(0, len(masterConfig.workSets)):
		workDetails = masterConfig.workSets[i]

		print(bcolors.OKBLUE + "\n>> CREATING Player: " + str(i) + bcolors.ENDC)
		cfgToFetch = masterConfig.workConfigParser.get(workDetails, "cfg")
		canvasOffsetX = int(
			masterConfig.workConfigParser.get(workDetails, "canvasOffsetX")
		)
		canvasOffsetY = int(
			masterConfig.workConfigParser.get(workDetails, "canvasOffsetY")
		)
		canvasRotation = float(
			masterConfig.workConfigParser.get(workDetails, "canvasRotation")
		)
		workArgument = masterConfig.path + "/configs/" + cfgToFetch  # + ".cfg"

		## This loads the config file for the work as listed in the
		## mulitplayer manifest
		workObject = workobject.WorkObject(workArgument, instanceNumber=i)
		workObject.workId = i

		# forcing this to be 0 as things get jittery when doing final
		# composition
		workObject.config.rotation = 0

		## sets the render function -- in the multi player situation, this just draws
		## the final animation to each player's final image - the canvas is not updated
		## since that is handled by the main app window process thread
		# This could be done in the WorkObject itself if I pass more stuff there ...
		workObject.renderer = renderClass.CanvasElement(workWindow.root, masterConfig)
		workObject.renderer.config = workObject.config
		workObject.renderer.setUp()

		try:
			randomChange =	masterConfig.workConfigParser.getboolean(workDetails, "randomChange")
		except Exception as e:
			print(str(e))
			randomChange = True

		workObject.renderer.config.randomChange = randomChange


		if randomChange == False :
			workObject.renderer.config.canvasOffsetX = canvasOffsetX
			workObject.renderer.config.canvasOffsetY = canvasOffsetY
			workObject.renderer.config.canvasRotation = canvasRotation
		else :
			workObject.renderer.config.canvasOffsetX = 0
			workObject.renderer.config.canvasOffsetY = 0
			workObject.renderer.config.canvasRotation = 0

		workObject.renderer.config.canvasOffsetX_init = canvasOffsetX
		workObject.renderer.config.canvasOffsetY_init = canvasOffsetY
		workObject.renderer.config.canvasRotation_init = canvasRotation

		workObject.config.render = workObject.renderer.render

		workWindow.players.append(workObject)

		# print(bcolors.FAIL + ">> PlayerObject loading the work: " + str(player.work.config.__dict__) + bcolors.ENDC)

		# For now, only running two work threads at a time .....
		startWorkThread(workObject, i)

	print(">> ")
	startWindowThread(workWindow)
	workWindow.run()


def runWork(work):
	print(">> runWork")
	work.runWork()


def runWindow(workWindow):
	print(">> runWindow -- overall renderer")
	while True:
		workWindow.renderer.updateTheCanvas(workWindow.players)
		time.sleep(workWindow.masterConfig.repaintDelay)

		############################################################
		######  Check if config file has changed and reload    #####
		############################################################

		if workWindow.masterConfig.checkForConfigChanges == True:
			workWindow.masterConfig.currentTime = time.time()
			f = os.path.getmtime(workWindow.masterConfig.windowConfig)
			workWindow.masterConfig.delta = workWindow.masterConfig.currentTime - f

			if workWindow.masterConfig.delta <= 1:
				if workWindow.masterConfig.reloadConfig == False:
					print("LAST MODIFIED DELTA: ", workWindow.masterConfig.delta)
					workWindow.doingReload = True
					configure(workWindow.masterConfig)
					loadFromArguments(masterConfig, True)
				workWindow.masterConfig.reloadConfig = True
			else:
				workWindow.masterConfig.reloadConfig = False

		for work in workWindow.players:

			#if random.random() <.1 :
				#work.renderer.config.canvasOffsetX = canvasOffsetX
				#work.renderer.config.canvasOffsetY = canvasOffsetY
				#work.renderer.config.canvasRotation = random.uniform(-work.config.canvasRotation,work.config.canvasRotation)

			if work.config.checkForConfigChanges == True:
				work.currentTime = time.time()
				f = os.path.getmtime(work.workConfigFile)
				work.delta = work.currentTime - f

				if work.delta <= 1:
					if work.reloadConfig == False:
						print("LAST MODIFIED DELTA: ", work.delta)
						work.doingReload = True

						work.workConfig.read(work.workConfigFile)
						work.configure()
						# work.config.loadFromArguments(True)
					work.reloadConfig = True
				else:
					work.reloadConfig = False


def startWindowThread(workWindow):
	print("\n>> startWindowThread 0 WORKWINDOW THREAD STARTING")
	t0 = threading.Thread.__init__(runWindow(workWindow))
	masterConfig.threads.append(t0)
	t0.start()
	# thrd = threading.Thread(target=proc0, kwargs=dict(workWindow=workWindow))
	# thrd.start()
	# thrd.join()


def startWorkThread(work, i):
	print(">> startWorkThread THREAD STARTING " + str(i))

	work.config.running = True
	#work.testFCU(work.config)
	thrd = threading.Thread(target=runWork, kwargs=dict(work=work))
	masterConfig.threads.append(thrd)
	thrd.start()
	# thrd.join()

	t  = Timer(3.0, unLoadWork, [masterConfig,thrd,work])
	t.start()


def unLoadWork(masterConfig,thrd,work):
	print("-----> Ending Thread" + str(work))

	work.config.running = False
	#work.endRunning(work.config)

	


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def loadTheConfig(masterConfig):
	"""
		example:
		python player.py -cfg p4-6x5/stroop2
		python player.py -mname daemon3 -path ./ -cfg p4-6x5/stroop2&
		"""

	parser = argparse.ArgumentParser(description="Process")
	parser.add_argument(
		"-mname", type=str, default="local", help="machine name (optional)"
	)
	parser.add_argument("-path", type=str, default="./", help="directory (optional)")
	parser.add_argument(
		"-cfg",
		type=str,
		required=True,
		help="Config File - just need sub-folder and name - e.g. p4-6x5/repeater.cfg",
	)
	parser.add_argument(
		"-brightnessOverride",
		type=int,
		help="brightness param to override the config value (optional)",
	)
	args = parser.parse_args()

	print(">>  Config Arguments --> " + str(args) + " **")

	"""
		config.MID = args[1]
		config.path = args[2]
		argument = args[3]
		"""

	masterConfig.MID = args.mname
	masterConfig.path = args.path
	masterConfig.windowConfig = masterConfig.path + "/configs/" + args.cfg

	masterConfig.startTime = time.time()
	masterConfig.currentTime = time.time()
	masterConfig.reloadConfig = False
	masterConfig.doingReload = False
	masterConfig.checkForConfigChanges = False
	masterConfig.loadFromArguments = loadFromArguments
	masterConfig.fileName = masterConfig.windowConfig
	masterConfig.brightnessOverride = None

	# Optional 4th argument to override the brightness set in the
	# config
	if args.brightnessOverride != None:
		brightnessOverride = args.brightnessOverride
		masterConfig.brightness = float(float(brightnessOverride) / 100)
		masterConfig.brightnessOverride = float(float(brightnessOverride) / 100)

	f = os.path.getmtime(masterConfig.windowConfig)
	masterConfig.delta = int((masterConfig.startTime - f))
	print(">> LAST MODIFIED DELTA: " + str(masterConfig.delta))

	configure(masterConfig)


def configure(masterConfig):
	print(">>  Multiplayer running loadTheConfig **")
	masterConfig.workConfigParser = configparser.ConfigParser()
	masterConfig.workConfigParser.read(masterConfig.windowConfig)

	masterConfig.workSets = list(
		map(
			lambda x: x,
			masterConfig.workConfigParser.get("worksList", "works").split(","),
		)
	)
	masterConfig.screenHeight = int(
		masterConfig.workConfigParser.get("worksList", "screenHeight")
	)
	masterConfig.screenWidth = int(
		masterConfig.workConfigParser.get("worksList", "screenWidth")
	)
	masterConfig.canvasOffsetX = int(
		masterConfig.workConfigParser.get("worksList", "canvasOffsetX")
	)
	masterConfig.canvasOffsetY = int(
		masterConfig.workConfigParser.get("worksList", "canvasOffsetY")
	)
	masterConfig.windowXOffset = int(
		masterConfig.workConfigParser.get("worksList", "windowXOffset")
	)
	masterConfig.windowYOffset = int(
		masterConfig.workConfigParser.get("worksList", "windowYOffset")
	)

	try:
		masterConfig.repaintDelay = float(
			masterConfig.workConfigParser.get("worksList", "repaintDelay")
		)
	except Exception as e:
		print(str(e))
		masterConfig.repaintDelay = 0.01
	
	try:
		masterConfig.useFilters = masterConfig.workConfigParser.getboolean("worksList", "useFilters")
	except Exception as e:
		print(str(e))
		masterConfig.useFilters = False

	
	try:
		masterConfig.useBlur = masterConfig.workConfigParser.getboolean("worksList", "useBlur")
		masterConfig.blurXOffset = int(masterConfig.workConfigParser.get("worksList", "blurXOffset"))
		masterConfig.blurYOffset = int(masterConfig.workConfigParser.get("worksList", "blurYOffset"))
		masterConfig.blurSectionWidth = int(
			masterConfig.workConfigParser.get("worksList", "blurSectionWidth")
		)
		masterConfig.blurSectionHeight = int(
			masterConfig.workConfigParser.get("worksList", "blurSectionHeight")
		)
		masterConfig.sectionBlurRadius = int(
			masterConfig.workConfigParser.get("worksList", "sectionBlurRadius")
		)
		masterConfig.blurSection = (
			masterConfig.blurXOffset,
			masterConfig.blurYOffset,
			masterConfig.blurXOffset + masterConfig.blurSectionWidth,
			masterConfig.blurYOffset + masterConfig.blurSectionHeight,
		)
	except Exception as e:
		print(str(e))
		masterConfig.useBlur = False


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
print(">>  Multiplayer running loadFromArguments **")

masterConfig = configuration.Config()
masterConfig.path = "."
masterConfig.checkForConfigChanges = True
masterConfig.threads = []


def main():
	loadFromArguments(masterConfig)


# Kick off .......
if __name__ == "__main__":
	main()
