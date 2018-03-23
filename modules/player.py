#!/usr/bin/python
#import modules
import PIL.Image
from PIL import Image, ImageDraw, ImageFont
from PIL import ImageChops

#import numpy
import os, sys, getopt, time, random, math, datetime, textwrap
import gc
#import ConfigParser
import configparser
import io
import threading
import importlib 
import resource
from subprocess import call

from modules import configuration
#from configs import localconfig

global thrd, config
global imageTop,imageBottom,image,config,transWiring

threads = []

#workconfig = configparser.ConfigParser()

def configure() :
	global config, workconfig, path, tempImage, threads, thrd
	#gc.enable()

	print("setting config values")

	### Sets up for testing live config chages
	try:
		config.checkForConfigChanges = (workconfig.getboolean("displayconfig", 'checkForConfigChanges'))
	except  Exception as e: 
		print (str(e))
		config.checkForConfigChanges = False

	try :
		config.usePixelSort  = (workconfig.getboolean("displayconfig", 'usePixelSort'))
		config.unsharpMaskPercent  = int(workconfig.get("displayconfig", 'unsharpMaskPercent'))
		config.blurRadius  = int(workconfig.get("displayconfig", 'blurRadius'))
		config.pixSortXOffset  = int(workconfig.get("displayconfig", 'pixSortXOffset'))
		config.pixSortYOffset  = int(workconfig.get("displayconfig", 'pixSortYOffset'))
		config.pixSortboxHeight  = int(workconfig.get("displayconfig", 'pixSortboxHeight'))
		config.pixSortboxWidth  = int(workconfig.get("displayconfig", 'pixSortboxWidth'))
		config.pixSortgap  = int(workconfig.get("displayconfig", 'pixSortgap'))
		config.pixSortprobDraw  = float(workconfig.get("displayconfig", 'pixSortprobDraw'))
		config.pixSortprobGetNextColor  = float(workconfig.get("displayconfig", 'pixSortprobGetNextColor'))
		config.pixSortProbDecriment  = float(workconfig.get("displayconfig", 'pixSortProbDecriment'))
		config.pixSortSizeDecriment  = float(workconfig.get("displayconfig", 'pixSortSizeDecriment'))
		config.pixSortSampleVariance  = int(workconfig.get("displayconfig", 'pixSortSampleVariance'))
		config.pixSortDrawVariance  = int(workconfig.get("displayconfig", 'pixSortDrawVariance'))
		config.pixSortDirection = str(workconfig.get("displayconfig", 'pixSortDirection'))
		config.randomColorProbabilty = float(workconfig.get("displayconfig", 'randomColorProbabilty'))
		config.brightnessVarLow = float(workconfig.get("displayconfig", 'brightnessVarLow'))
		config.brightnessVarHi = float(workconfig.get("displayconfig", 'brightnessVarHi'))
		config.pixelSortAppearanceProb = float(workconfig.get("displayconfig", 'pixelSortAppearanceProb'))

	except Exception as e:
		print (str(e))
		config.usePixelSort = False
		config.unsharpMaskPercent  = 50
		config.blurRadius  = 0
		config.pixSortXOffset = 0
		config.pixSortYOffset = 0
		config.pixSortboxHeight = 40
		config.pixSortboxWidth = 96
		config.pixSortgap = 2
		config.pixSortprobDraw = .5
		config.pixSortprobGetNextColor = .2
		config.pixSortSizeDecriment = .5
		config.pixSortProbDecriment = .5
		config.pixSortSampleVariance = 10
		config.pixSortDrawVariance = 10
		config.pixSortDirection = 'lateral'
		config.randomColorProbabilty = .002
		config.pixelSortAppearanceProb = 1

		config.brightnessVarLow = .8
		config.brightnessVarHi = 1

	## used when repositioning a block of an image -- sculptural pieces when
	## card configurations can't handle simple set up

	try :
		config.remapImageBlock = (workconfig.getboolean("displayconfig", 'remapImageBlock'))
		config.remapImageBlockSection = workconfig.get("displayconfig", 'remapImageBlockSection').split(",")
		config.remapImageBlockSection = tuple([int(i) for i in config.remapImageBlockSection])
		config.remapImageBlockDestination = workconfig.get("displayconfig", 'remapImageBlockDestination').split(",")
		config.remapImageBlockDestination = tuple([int(i) for i in config.remapImageBlockDestination])
	except Exception as e:
		print (str(e))
		config.remapImageBlock = False

	try :
		config.imageXOffset = int(workconfig.get("displayconfig","imageXOffset"))
		config.imageYOffset = int(workconfig.get("displayconfig","imageYOffset"))
	except Exception as e:
		print (str(e))
		config.imageXOffset = 0
		config.imageYOffset = 0

	config.screenHeight = int(workconfig.get("displayconfig", 'screenHeight'))
	config.screenWidth =  int(workconfig.get("displayconfig", 'screenWidth'))
	#config.tileSize = (int(workconfig.get("displayconfig", 'tileSizeHeight')),int(workconfig.get("displayconfig", 'tileSizeWidth')))
	config.tileSize = (int(workconfig.get("displayconfig", 'tileSizeWidth')),int(workconfig.get("displayconfig", 'tileSizeHeight')))
	config.rows = int(workconfig.get("displayconfig", 'rows'))
	config.cols = int(workconfig.get("displayconfig", 'cols'))

	config.brightness =  float(workconfig.get("displayconfig", 'brightness'))
	if(config.brightnessOverride is not None) : config.brightness = config.brightnessOverride

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

	# Setting up based on how the work is displayed
	print("Loading:", str(config.work))
	work = importlib.import_module('pieces.'+str(config.work))
	work.config = config
	work.workConfig = workconfig



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
		config.useFilters  = (workconfig.getboolean("displayconfig", 'useFilters'))

		try :
			config.isRPI = (workconfig.getboolean("displayconfig", 'isRPI')) 
		except Exception as e: 
			config.useFilters = False
			config.isRPI = True
			print (str(e))
		
		r.config = config
		r.work = work
		r.canvasOffsetX = int(workconfig.get("displayconfig", 'canvasOffsetX'))
		r.canvasOffsetY = int(workconfig.get("displayconfig", 'canvasOffsetY'))
		config.windowXOffset = int(workconfig.get("displayconfig", 'windowXOffset'))
		config.windowYOffset = int(workconfig.get("displayconfig", 'windowYOffset'))
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

		try :
			config.isRPI = (workconfig.getboolean("displayconfig", 'isRPI')) 
		except Exception as e: 
			config.usePixSort = False
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
		config.renderImageFull = PIL.Image.new("RGBA", (config.screenWidth, config.screenHeight))

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


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''