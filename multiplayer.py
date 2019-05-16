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
from modules import playerClass
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
				print("\n>> CREATING Player: " + str(i))
				workDetails = masterConfig.workSets[i]
				workConfig = configuration.Config()
				cfgToFetch = masterConfig.workConfigParser.get(workDetails, 'cfg')
				canvasOffsetX = int(masterConfig.workConfigParser.get(workDetails, 'canvasOffsetX'))
				canvasOffsetY = int(masterConfig.workConfigParser.get(workDetails, 'canvasOffsetY'))
				canvasRotation = float(masterConfig.workConfigParser.get(workDetails, 'canvasRotation'))
				workArgument = masterConfig.path + "/configs/" + cfgToFetch  # + ".cfg"

				## This loads the config file for the work as listed in the
				## mulitplayer manifest
				parser = configparser.ConfigParser()
				parser.read(workArgument)

				print(">> FETCHING: " + str(i) + " " + cfgToFetch)
				player = playerClass.PlayerObject(workConfig, parser, masterConfig, instanceNumber=i)
				player.appRoot = workWindow.root
				player.canvasXPosition = 0
				player.delay = (i+1) * 1000

				player.configure()
				player.work.workId = i
				player.work.config = workConfig
				# forcing this to be 0 as things get jittery when doing final
				# composition
				player.work.config.rotation = 0

				player.renderer = renderClass.CanvasElement(workWindow.root, masterConfig)
				player.renderer.config = workConfig
				player.renderer.setUp()
				player.renderer.config.canvasOffsetX = canvasOffsetX
				player.renderer.config.canvasOffsetY = canvasOffsetY
				player.renderer.config.canvasRotation = canvasRotation

				## sets the render function -- in the multi player situation, this just draws
				## the final animation to each player's final image - the canvas is not updated
				## since that is handled by the main app window process thread
				player.work.config.render = player.renderer.render
				workWindow.players.append(player)

				# For now, only running two at a time .....
				if i == 0 :
					procCall1(player.work)
				else :
					procCall2(player.work)


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
		time.sleep(.01)


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

def loadTheConfig(config) :

			print(">>  Multiplayer running loadTheConfig **")
			config.workConfigParser = configparser.ConfigParser()

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

			config.MID = args.mname
			config.path = args.path
			argument = config.path + "/configs/" + args.cfg  # + ".cfg"

			config.workConfigParser.read(argument)

			config.startTime = time.time()
			config.currentTime = time.time()
			config.reloadConfig = False
			config.doingReload = False
			config.checkForConfigChanges = False
			config.loadFromArguments = loadFromArguments
			config.fileName = argument
			config.brightnessOverride = None

			# Optional 4th argument to override the brightness set in the
			# config
			if(args.brightnessOverride != None):
				brightnessOverride = args.brightnessOverride
				config.brightness = float(float(brightnessOverride) / 100)
				config.brightnessOverride = float(float(brightnessOverride) / 100)

			f = os.path.getmtime(argument)
			config.delta = int((config.startTime - f))
			print(">> LAST MODIFIED DELTA: " + str(config.delta))

			config.workSets = list(map(lambda x: x, config.workConfigParser.get("worksList", 'works').split(',')))
			config.screenHeight = int(config.workConfigParser.get("worksList", 'screenHeight'))
			config.screenWidth =  int(config.workConfigParser.get("worksList", 'screenWidth'))
			config.canvasOffsetX = int(config.workConfigParser.get("worksList", 'canvasOffsetX'))
			config.canvasOffsetY = int(config.workConfigParser.get("worksList", 'canvasOffsetY'))
			config.windowXOffset = int(config.workConfigParser.get("worksList", 'windowXOffset'))
			config.windowYOffset = int(config.workConfigParser.get("worksList", 'windowYOffset'))

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



