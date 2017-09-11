#!/usr/bin/python
#import modules
import PIL.Image
from PIL import Image, ImageDraw, ImageFont
from PIL import ImageChops

import numpy
import os, sys, getopt, time, random, math, datetime, textwrap
import gc
import ConfigParser, io
import threading
import importlib 
import resource
from subprocess import call

from modules import configuration
#from configs import localconfig

global thrd, config
global imageTop,imageBottom,image,config,transWiring
threads = []
workconfig = ConfigParser.ConfigParser()

## Create a blank dummy object container for now
#config = type('', (object,), {})()

######################################################################################################
#
#
# -------   Reads configuration files and sets defaults    
# -------   Piece is initiated by command line: e.g.                     
# sudo python /Users/lamshell/Documents/Dev/LED-MATRIX-RPI/RPI/player.py studio-mac ./ configs/fludd.cfg &
#
#
######################################################################################################

def loadFromArguments(reloading=False):
	global config, workconfig, path, tempImage, threads, thrd

	if(reloading == False) :
		try: 
			###
			# Expects 3 arguments:
			#		name-of-machine
			#       the local path
			#		the config file to load

			args = sys.argv
			print("Arguments passed to player.py:")
			print(args)

			config = configuration

			# Load the default work
			

			if(len(args) > 1):
				config.MID = args[1]
				config.path = args[2]
				argument = args[3]

				workconfig.read(argument)

				config.startTime = time.time()
				config.currentTime = time.time()
				config.reloadConfig = False
				config.doingReload = False
				config.checkForConfigChanges =  False
				config.loadFromArguments = loadFromArguments
				config.fileName = argument

				if(len(args) > 4):
					brightnessOverride = args[4]
					config.brightness = float(float(brightnessOverride)/100)

				f = os.path.getmtime(argument)
				config.delta = int((config.startTime - f ))
				print (argument, "LAST MODIFIED DELTA: ", config.delta)
			else :
				# Machine ID
				config.MID = baseconfig.MID
				# Default Work Instance ID
				config.WRKINID = baseconfig.WRKINID
				# Default Local Path
				config.path = baseconfig.path
				print("Loading " + config.path  + '/configs/pieces/' + config.WRKINID + ".cfg" + " to run.")
				workconfig.read(config.path  + '/configs/pieces/' + config.WRKINID + ".cfg")

			configure()

		except getopt.GetoptError as err:
			# print help information and exit:
			print ("Error:" + str(err))
	else :
		workconfig.read(config.fileName)
		configure()


def configure() :
	global config, workconfig, path, tempImage, threads, thrd
	#gc.enable()

	### Sets up for testing live config chages
	try:
		config.checkForConfigChanges = (workconfig.getboolean("displayconfig", 'checkForConfigChanges'))
	except  Exception as e: 
		print (str(e))
		config.checkForConfigChanges = False

	try: 

		config.screenHeight = int(workconfig.get("displayconfig", 'screenHeight'))
		config.screenWidth =  int(workconfig.get("displayconfig", 'screenWidth'))
		#config.tileSize = (int(workconfig.get("displayconfig", 'tileSizeHeight')),int(workconfig.get("displayconfig", 'tileSizeWidth')))
		config.tileSize = (int(workconfig.get("displayconfig", 'tileSizeWidth')),int(workconfig.get("displayconfig", 'tileSizeHeight')))
		config.rows = int(workconfig.get("displayconfig", 'rows'))
		config.cols = int(workconfig.get("displayconfig", 'cols'))
		config.brightness =  float(workconfig.get("displayconfig", 'brightness'))
		config.minBrightness  = float(workconfig.get("displayconfig", 'minBrightness'))
		config.work = workconfig.get("displayconfig", 'work')
		config.rendering = workconfig.get("displayconfig", 'rendering')

		# Create the image-canvas for the work
		config.renderImage = PIL.Image.new("RGBA", (config.screenWidth*config.rows, 32))
		config.renderImageFull = PIL.Image.new("RGBA", (config.screenWidth, config.screenHeight))
		config.image = PIL.Image.new("RGBA", (config.screenWidth, config.screenHeight))
		config.draw = ImageDraw.Draw(config.image)
		config.renderDraw = ImageDraw.Draw(config.renderImageFull)
		#config.render = render

		print("Loading:", str(config.work))
		work = importlib.import_module('pieces.'+str(config.work))
		work.config = config
		work.workConfig = workconfig

		# Setting up based on how the work is displayed

		if(config.rendering == "hat") :
			# The AdaFruit specific LED matrix HAT
			from modules import rendertohat
			# this tests for the power-down RPI switch
			from cntrlscripts import stest
			thrd = threading.Thread(target=stest.__main__)
			threads.append(thrd)
			thrd.start()

			r = rendertohat
			config.matrixTiles = int(workconfig.get("displayconfig", 'matrixTiles'))
			config.transWiring = (workconfig.getboolean("displayconfig", 'transWiring'))
			config.actualScreenWidth  = int(workconfig.get("displayconfig", 'actualScreenWidth'))
			config.canvasWidth = int(workconfig.get("displayconfig", 'canvasWidth'))
			config.canvasHeight = int(workconfig.get("displayconfig", 'canvasHeight'))
			config.rotation = float(workconfig.get("displayconfig", 'rotation'))
			config.rotationTrailing = (workconfig.getboolean("displayconfig", 'rotationTrailing'))
			config.fullRotation = (workconfig.getboolean("displayconfig", 'fullRotation'))
			r.config = config
			r.setUp()
			config.render = r.render
			config.updateCanvas = r.updateCanvas
			work.main()

		if(config.rendering == "hub") :
			from modules import rendertohub

			config.useFilters  = (workconfig.getboolean("displayconfig", 'useFilters'))
			config.rotation = float(workconfig.get("displayconfig", 'rotation'))
			config.rotationTrailing = (workconfig.getboolean("displayconfig", 'rotationTrailing'))
			config.fullRotation = (workconfig.getboolean("displayconfig", 'fullRotation'))
			config.canvasWidth = int(workconfig.get("displayconfig", 'canvasWidth'))
			config.canvasHeight = int(workconfig.get("displayconfig", 'canvasHeight'))

			config.isRPI = False

			try :
				config.isRPI = (workconfig.getboolean("displayconfig", 'isRPI')) 
			except Exception as e: 
				print (str(e))

			if(config.isRPI == True) : 
				from cntrlscripts import stest
				thrd = threading.Thread(target=stest.__main__)
				threads.append(thrd)
				thrd.start()
			
			# Create the image-canvas for the work
			# Because rotation is an option, recreate accordingly
			# And to be sure, make the renderImageFull bigger than necessary - 		
			config.renderImage = PIL.Image.new("RGBA", (config.canvasWidth * config.rows, 32))
			config.renderImageFull = PIL.Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
			config.renderDraw = ImageDraw.Draw(config.renderImageFull)
			config.image = PIL.Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
			config.draw = ImageDraw.Draw(config.image)
			
			r = rendertohub
			r.config = config
			r.work = work
			r.canvasOffsetX = int(workconfig.get("displayconfig", 'canvasOffsetX'))
			r.canvasOffsetY = int(workconfig.get("displayconfig", 'canvasOffsetY'))
			config.windowXOffset = int(workconfig.get("displayconfig", 'windowXOffset'))
			config.windowYOffset = int(workconfig.get("displayconfig", 'windowYOffset'))

			config.drawBeforeConversion = r.drawBeforeConversion
			config.render = r.render
			config.updateCanvas = r.updateCanvas
			work.main(False)

			print("Setting Up", config.doingReload)
			if(config.doingReload == False) : r.setUp()

		if(config.rendering == "out") :
			from modules import rendertofile
			config.useFilters  = (workconfig.getboolean("displayconfig", 'useFilters'))
			config.rotation = float(workconfig.get("displayconfig", 'rotation'))
			config.rotationTrailing = (workconfig.getboolean("displayconfig", 'rotationTrailing'))
			config.fullRotation = (workconfig.getboolean("displayconfig", 'fullRotation'))
			r = rendertofile
			r.config = config
			r.work = work
			r.work.x = r.work.y = 0
			r.fps = int(workconfig.get("output", 'fps'))
			r.duration = int(workconfig.get("output", 'duration'))


			# Test white rectangle on main rendering image
			#config.renderDraw.rectangle((0,0,400,300), fill=(255,255,255))

			config.render = r.render
			config.updateCanvas = r.updateCanvas
			work.main(False)
			
			r.setUp("video")


	except getopt.GetoptError as err:
		# print help information and exit:
		print ("Error:" + str(err))
		return False


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def main():
	global config, threads
	loadFromArguments()
	'''
	# Threading now handled by renderer - e.g. see modules/rendertohub.py
	thrd = threading.Thread(target=configure)
	threads.append(thrd)
	thrd.start()
	'''
	
### Kick off .......
if __name__ == "__main__":
	main()
