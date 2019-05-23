#!/usr/bin/python
# Two instance player

'''
p4-3x8-informal/quilt-triangles-b

p4-3x8-informal/quilt
'''

import os
import sys
import getopt, random
import time
import configparser
from modules import configuration
from modules.configuration import bcolors
from modules.configuration import Config

from modules import workobject
from modules.rendering import renderClass, appWindow
import argparse
import threading


# Create a blank dummy object container for now
#config = type('', (object,), {})()

##########################################################################
#
#
# -------   Reads configuration files and sets defaults
# -------   Piece is initiated by command line: e.g.
# sudo python /Users/lamshell/Documents/Dev/LED-MATRIX-RPI/RPI/player.py studio-mac ./ configs/fludd.cfg &
#
#
##########################################################################

def loadFromArguments(reloading=False):

	if(reloading == False):
		try:
			###
			# Expects 3 arguments:
			#		name-of-machine
			#       the local path
			#		the config file to load
			'''
			args = sys.argv
			print("Arguments passed to player.py:")
			print(args)
			'''
		   
			print(">>  Multiplayer running loadFromArguments **")

			masterConfig = configuration.Config()
			masterConfig.path = "."

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


			for i in  range(0, len(masterConfig.workSets)):
				workDetails = masterConfig.workSets[i]

				print(bcolors.OKBLUE + "\n>> CREATING Player: " + str(i) + bcolors.ENDC)
				cfgToFetch = masterConfig.workConfigParser.get(workDetails, 'cfg')
				canvasOffsetX = int(masterConfig.workConfigParser.get(workDetails, 'canvasOffsetX'))
				canvasOffsetY = int(masterConfig.workConfigParser.get(workDetails, 'canvasOffsetY'))
				canvasRotation = float(masterConfig.workConfigParser.get(workDetails, 'canvasRotation'))
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
				workObject.renderer.config.canvasOffsetX = canvasOffsetX
				workObject.renderer.config.canvasOffsetY = canvasOffsetY
				workObject.renderer.config.canvasRotation = canvasRotation
				workObject.config.render = workObject.renderer.render

				workWindow.players.append(workObject)

				#print(bcolors.FAIL + ">> PlayerObject loading the work: " + str(player.work.config.__dict__) + bcolors.ENDC)

				# For now, only running two work threads at a time .....
				if i == 0 :
					procCall1(workObject)
				else :
					procCall2(workObject)


			print(">> ")
			procCall0(workWindow)
			workWindow.run()


		except getopt.GetoptError as err:
			# print help information and exit:
			print("Error:" + str(err))
	else:
		print(">> reloading: " + config.fileName)



def proc1(work):
	print(">> PROC1")
	work.runWork()


def proc2(work):
	print(">> PROC2")
	work.runWork()


def proc0(workWindow):
	print(">> PROC0 -- overall renderer")
	while True:
		workWindow.renderer.updateTheCanvas(workWindow.players)
		time.sleep(workWindow.masterConfig.repaintDelay )


def procCall0(workWindow) :
	print(">> ProcCall 0 WORKWINDOW THREAD STARTING")
	t0  = threading.Thread.__init__(proc0(workWindow))
	t0.start()
	#thrd = threading.Thread(target=proc0, kwargs=dict(workWindow=workWindow))
	#thrd.start()
	#thrd.join()



def procCall1(work) :
	print(">> ProcCall 1 THREAD STARTING")
	thrd = threading.Thread(target=proc1, kwargs=dict(work=work))
	thrd.start()
	#thrd.join()


def procCall2(work) :
	print(">> ProcCall 2 THREAD STARTING")
	thrd2 = threading.Thread(target=proc2, kwargs=dict(work=work))
	thrd2.start()
	#thrd2.join()





''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def loadTheConfig(masterConfig) :

			print(">>  Multiplayer running loadTheConfig **")
			masterConfig.workConfigParser = configparser.ConfigParser()

			'''
			example:
			python player.py -cfg p4-6x5/stroop2
			python player.py -mname daemon3 -path ./ -cfg p4-6x5/stroop2&
			'''

			parser = argparse.ArgumentParser(description='Process')
			parser.add_argument('-mname', type=str, default="local",help='machine name (optional)')
			parser.add_argument('-path', type=str, default="./", help='directory (optional)')
			parser.add_argument('-cfg', type=str, required=True,help='Config File - just need sub-folder and name - e.g. p4-6x5/repeater.cfg')
			parser.add_argument('-brightnessOverride', type=int, help='brightness param to override the config value (optional)')
			args = parser.parse_args()

			print(">>  Config Arguments --> " + str(args) + " **")

			'''
			config.MID = args[1]
			config.path = args[2]
			argument = args[3]
			'''

			masterConfig.MID = args.mname
			masterConfig.path = args.path
			argument = masterConfig.path + "/configs/" + args.cfg  # + ".cfg"

			masterConfig.workConfigParser.read(argument)

			masterConfig.startTime = time.time()
			masterConfig.currentTime = time.time()
			masterConfig.reloadConfig = False
			masterConfig.doingReload = False
			masterConfig.checkForConfigChanges = False
			masterConfig.loadFromArguments = loadFromArguments
			masterConfig.fileName = argument
			masterConfig.brightnessOverride = None

			# Optional 4th argument to override the brightness set in the
			# config
			if(args.brightnessOverride != None):
				brightnessOverride = args.brightnessOverride
				masterConfig.brightness = float(float(brightnessOverride) / 100)
				masterConfig.brightnessOverride = float(float(brightnessOverride) / 100)

			f = os.path.getmtime(argument)
			masterConfig.delta = int((masterConfig.startTime - f))
			print(">> LAST MODIFIED DELTA: " + str(masterConfig.delta))

			masterConfig.workSets = list(map(lambda x: x, masterConfig.workConfigParser.get("worksList", 'works').split(',')))
			masterConfig.screenHeight = int(masterConfig.workConfigParser.get("worksList", 'screenHeight'))
			masterConfig.screenWidth =  int(masterConfig.workConfigParser.get("worksList", 'screenWidth'))
			masterConfig.canvasOffsetX = int(masterConfig.workConfigParser.get("worksList", 'canvasOffsetX'))
			masterConfig.canvasOffsetY = int(masterConfig.workConfigParser.get("worksList", 'canvasOffsetY'))
			masterConfig.windowXOffset = int(masterConfig.workConfigParser.get("worksList", 'windowXOffset'))
			masterConfig.windowYOffset = int(masterConfig.workConfigParser.get("worksList", 'windowYOffset'))

			try:
				masterConfig.repaintDelay = float(masterConfig.workConfigParser.get("worksList", 'repaintDelay'))
			except Exception as e:
				print(str(e))
				masterConfig.repaintDelay = .01


			return True

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


def main():
	loadFromArguments()
	'''
	# Threading now handled by renderer - e.g. see modules/rendertohub.py
	thrd = threading.Thread(target=configure)
	threads.append(thrd)
	thrd.start()
	'''

# Kick off .......
if __name__ == "__main__":
	main()



