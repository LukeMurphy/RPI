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
		   
			# Load the default work
			masterConfig = configuration.Config()
			masterConfig.path = "."

			print("** Multiplayer running loadFromArguments **")
			loadTheConfig(masterConfig)

			'''
			##########################################################################
			#
			Create the main app window


			##########################################################################
			'''

			masterConfig.windowXOffset = 100
			masterConfig.windowYOffset = 100
			masterConfig.buff = 8
			masterConfig.screenWidth = 700
			masterConfig.screenHeight = 700

			workWindow = appWindow.AppWindow(masterConfig)
			workWindow.setUp()
			workWindow.renderer = renderClass.CanvasElement(workWindow.root, masterConfig)
			workWindow.renderer.masterConfig = masterConfig
			workWindow.renderer.canvasXPosition = 0
			workWindow.renderer.delay = 1
			workWindow.renderer.setUp(workWindow.root)

			players = []


			for i in  range(0, len(masterConfig.workSets)):
				workDetails = masterConfig.workSets[i]
				workConfig = configuration.Config()
				cfg = masterConfig.workConfig.get(workDetails, 'cfg')
				workArgument = masterConfig.path + "/configs/" + cfg  # + ".cfg"

				parser = configparser.ConfigParser()
				parser.read(workArgument)
				print("** Player: " + str(i))
				player = playerClass.PlayerObject(workConfig, parser, masterConfig, instanceNumber=i)
				player.appRoot = workWindow.root
				player.canvasXPosition = 0
				player.delay = (i+1) * 1000
				player.configure()
				player.work.config = workConfig
				player.work.config.render = workWindow.renderer.render
				player.renderer = workWindow.renderer
				player.work.workId = i
				if i == 0 :
					player.work.config.xOffset = [i]
				else :
					player.work.config.xOffset.append(i * 500)

				#player.work.config.canvasOffsetX = i * 100

				players.append(player)


				if i == 0 :
					#procCall1(player.work)
					#workWindow.root.after(player.renderer.delay, procCall1, player.renderer)
					pass
				else :
					#procCall2(player.work)
					#workWindow.root.after(player.renderer.delay, procCall2, player.renderer)
					pass


			exit()
			procCall0(workWindow)
			workWindow.run()
			#GUI.start()
			#workWindow.run()


		except getopt.GetoptError as err:
			# print help information and exit:
			print("Error:" + str(err))
	else:
		print("reloading: " + config.fileName)
		#workconfig.read(config.fileName)
		#player.configure(config, workconfig)


def proc1(work):
	print("PROC1")
	work.runWork()
	#renderer.work.config.render = renderer.render
	#renderer.work.runWork()
	'''
	while True:
		#renderer.work.config.render = renderer.render
		renderer.cnvs.create_rectangle(round(random.uniform(0,100)), round(random.uniform(0,100)), 10, 10, fill="green")
		time.sleep(.1)
	'''

def proc2(work):
	print("PROC2")
	work.runWork()
	#renderer.work.config.render = renderer.render
	#renderer.work.runWork()
	'''
	while True:
		#renderer.work.config.render = renderer.render
		renderer.cnvs.create_rectangle(round(random.uniform(0,100)), round(random.uniform(0,100)), 10, 10, fill="blue")
		time.sleep(.5)
	'''

def proc0(workWindow):
	while True:
		workWindow.renderer.updateTheCanvas()
		time.sleep(.02)


def procCall0(workWindow) :
	print("ProcCall 0")
	#thrd = threading.Thread(target=proc0, kwargs=dict(workWindow=workWindow))
	#thrd.start()
	#thrd.join()

	t0  = threading.Thread.__init__(proc0(workWindow))
	t0.start()


def procCall1(work) :
	print("ProcCall 1")
	thrd = threading.Thread(target=proc1, kwargs=dict(work=work))
	thrd.start()
	#thrd.join()


def procCall2(work) :
	print("ProcCall 2")
	thrd2 = threading.Thread(target=proc2, kwargs=dict(work=work))
	thrd2.start()
	#thrd2.join()



''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def loadTheConfig(config) :

			print("** Multiplayer running loadTheConfig **")
			config.workConfig = configparser.ConfigParser()

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

			print("** Config Arguments --> " + str(args) + " **")

			'''
			config.MID = args[1]
			config.path = args[2]
			argument = args[3]
			'''

			config.MID = args.mname
			config.path = args.path

			argument = config.path + "/configs/" + args.cfg  # + ".cfg"

			config.workConfig.read(argument)

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
			print("** LAST MODIFIED DELTA: " + str(config.delta))

			config.workSets = list(map(lambda x: x, config.workConfig.get("worksList", 'works').split(',')))

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



