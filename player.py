#!/usr/bin/python
#import modules
import PIL.Image
import PIL.ImageTk
from PIL import Image, ImageTk, ImageDraw, ImageFont

import numpy
import os, sys, getopt, time, random, math, datetime, textwrap
import gc
import ConfigParser, io
import threading
import importlib 
import resource
from subprocess import call

from modules import configuration
from configs import localconfig
#from cntrlscripts import off_signal

global thrd, config
global imageTop,imageBottom,image,config,transWiring


## Create a blank dummy object container for now
#config = type('', (object,), {})()

###################################################
# -------   Reads configuration files and sets
# -------   defaults                             *#
###################################################
def configure() :
	#global group, groups, config
	#global action, scroll, machine, bluescreen, user, carouselSign, imgLoader, concentric, flash, blend, sqrs
	global config, workconfig, path, tempImage
	gc.enable()
	try: 

		####
		# Having trouble loading the local configuration file based on relative path
		# so hacking things by loading from a Python file called localconfig.py
		# Please fix me  ;(
		## 

		baseconfig = localconfig
		path = baseconfig.path

		#baseconfig = ConfigParser.ConfigParser()
		#baseconfig.read('localconfig.cfg')
		config = configuration

		# Machine ID
		config.MID = baseconfig.MID
		# Default Work Instance ID
		config.WRKINID = baseconfig.WRKINID
		# Default Local Path
		config.path = baseconfig.path


		# Load the default work

		print("Loading " + config.path  + '/configs/pieces/' + config.WRKINID + ".cfg" + " to run.")

		workconfig = ConfigParser.ConfigParser()
		workconfig.read(config.path  + '/configs/pieces/' + config.WRKINID + ".cfg")

		config.screenHeight = int(workconfig.get("displayconfig", 'screenHeight'))
		config.screenWidth =  int(workconfig.get("displayconfig", 'screenWidth'))
		config.tileSize = (int(workconfig.get("displayconfig", 'tileSizeHeight')),int(workconfig.get("displayconfig", 'tileSizeWidth')))
		config.rows = int(workconfig.get("displayconfig", 'rows'))
		config.cols = int(workconfig.get("displayconfig", 'cols'))
		config.brightness =  float(workconfig.get("displayconfig", 'brightness'))
		config.minBrightness  = float(workconfig.get("displayconfig", 'minBrightness'))
		config.work = workconfig.get("displayconfig", 'work')
		config.rendering = workconfig.get("displayconfig", 'rendering')

		# Create the image-canvas for the work
		config.renderImage = PIL.Image.new("RGBA", (config.actualScreenWidth, 32))
		config.renderImageFull = PIL.Image.new("RGBA", (config.screenWidth, config.screenHeight))
		config.image = PIL.Image.new("RGBA", (config.screenWidth, config.screenHeight))
		config.draw = ImageDraw.Draw(config.image)
		#config.render = render

		work = importlib.import_module('pieces.'+str(config.work))
		work.config = config
		work.workConfig = workconfig

		# Setting up based on how the work is displayed

		if(config.rendering == "hat") :
			from modules import rendertohat
			r = rendertohat
			config.matrixTiles = int(workconfig.get("displayconfig", 'matrixTiles'))
			config.transWiring = bool(workconfig.getboolean("displayconfig", 'transWiring'))
			config.actualScreenWidth  = int(workconfig.get("displayconfig", 'actualScreenWidth'))
			r.config = config
			r.setUp()
			config.render = r.render
			work.main()

		if(config.rendering == "hub") :
			from modules import rendertohub
			config.useFilters  = (workconfig.getboolean("displayconfig", 'useFilters'))
			r = rendertohub
			r.config = config
			r.work = work
			config.render = r.render
			work.main(False)
			r.setUp()

		if(config.rendering == "out") :
			from modules import rendertofile
			config.useFilters  = (workconfig.getboolean("displayconfig", 'useFilters'))
			r = rendertofile
			r.config = config
			r.work = work
			r.fps = int(workconfig.get("output", 'fps'))
			r.duration = int(workconfig.get("output", 'duration'))

			config.render = r.render
			work.main(False)
			
			r.setUp("video")


	except getopt.GetoptError as err:
		# print help information and exit:
		print ("Error:" + str(err))
		return False


def main():
	global config
	configure()

if __name__ == "__main__":
	main()
