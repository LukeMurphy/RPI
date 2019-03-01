#!/usr/bin/python
#import modules
import os, sys, getopt, time, random, math, datetime, textwrap
import importlib 
import configparser

import PIL.Image
from PIL import Image, ImageDraw, ImageFont
from PIL import ImageChops

'''
import gc
import io
import threading
import resource
from subprocess import call
'''

from modules import configuration
global thrd, config
global imageTop,imageBottom,image,config,transWiring

threads = []

def configure(config, workconfig) :
	global  path, tempImage, threads, thrd
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
		config.pixelSortRotatesWithImage  = (workconfig.getboolean("displayconfig", 'pixelSortRotatesWithImage'))
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
		config.pixelSortRotatesWithImage = True
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
		config.filterRemap = True
	except Exception as e:
		print (str(e))
		config.remapImageBlock = False
		config.filterRemap = False
	
	try :
		config.remapImageBlockSectionRotation = float(workconfig.get("displayconfig", 'remapImageBlockSectionRotation'))
	except Exception as e:
		config.remapImageBlockSectionRotation = 0	

	try :
		config.remapImageBlock2 = (workconfig.getboolean("displayconfig", 'remapImageBlock2'))
		config.remapImageBlockSection2 = workconfig.get("displayconfig", 'remapImageBlockSection2').split(",")
		config.remapImageBlockSection2 = tuple([int(i) for i in config.remapImageBlockSection2])
		config.remapImageBlockDestination2 = workconfig.get("displayconfig", 'remapImageBlockDestination2').split(",")
		config.remapImageBlockDestination2 = tuple([int(i) for i in config.remapImageBlockDestination2])
	except Exception as e:
		print (str(e))
		config.remapImageBlock2 = False	

	try :
		config.remapImageBlockSection2Rotation = float(workconfig.get("displayconfig", 'remapImageBlockSection2Rotation'))
	except Exception as e:
		config.remapImageBlockSection2Rotation = 0

	try :
		config.remapImageBlock3 = (workconfig.getboolean("displayconfig", 'remapImageBlock3'))
		config.remapImageBlockSection3 = workconfig.get("displayconfig", 'remapImageBlockSection3').split(",")
		config.remapImageBlockSection3 = tuple([int(i) for i in config.remapImageBlockSection3])
		config.remapImageBlockDestination3 = workconfig.get("displayconfig", 'remapImageBlockDestination3').split(",")
		config.remapImageBlockDestination3 = tuple([int(i) for i in config.remapImageBlockDestination3])
	except Exception as e:
		print (str(e))
		config.remapImageBlock3 = False

	try :
		config.remapImageBlockSection3Rotation = float(workconfig.get("displayconfig", 'remapImageBlockSection3Rotation'))
	except Exception as e:
		config.remapImageBlockSection3Rotation = 0

	try :
		config.imageXOffset = int(workconfig.get("displayconfig","imageXOffset"))
		config.imageYOffset = int(workconfig.get("displayconfig","imageYOffset"))
	except Exception as e:
		print (str(e))
		config.imageXOffset = 0
		config.imageYOffset = 0

	try :
		config.useBlur  = workconfig.getboolean("displayconfig", 'useBlur')
		config.blurXOffset = int(workconfig.get("displayconfig", 'blurXOffset'))
		config.blurYOffset = int(workconfig.get("displayconfig", 'blurYOffset'))
		config.blurSectionWidth = int(workconfig.get("displayconfig", 'blurSectionWidth'))
		config.blurSectionHeight = int(workconfig.get("displayconfig", 'blurSectionHeight'))
		config.sectionBlurRadius = int(workconfig.get("displayconfig", 'sectionBlurRadius'))
		config.blurSection = (config.blurXOffset, config.blurYOffset, config.blurXOffset + config.blurSectionWidth, config.blurYOffset + config.blurSectionHeight)
	except Exception as e: 
		print (str(e))
		config.useBlur  = False

	try:
		config.redBoost = float(workconfig.get("displayconfig", 'redBoost'))
		config.greenBoost = float(workconfig.get("displayconfig", 'greenBoost'))
		config.blueBoost = float(workconfig.get("displayconfig", 'blueBoost'))

		
	except Exception as e: 
		
		config.redBoost = 1
		config.greenBoost = 1
		config.blueBoost = 1

		print (str(e))


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


	# Setting up based on how the work is displayed
	print("Loading:", str(config.work))
	work = importlib.import_module('pieces.'+str(config.work))
	work.config = config
	work.workConfig = workconfig

	#if(config.rendering == "hat") : renderUsingIDAFruitHat(work)
	if(config.rendering == "hub") : renderUsingLINSNHub(work)
	#if(config.rendering == "out") : renderUsingFFMPEG(work)
'''
def renderUsingIDAFruitHat(work):
	
	# The AdaFruit specific LED matrix HAT
	from modules.rendering import rendertohat
	# this tests for the power-down RPI switch
	from cntrlscripts import stest
	thrd = threading.Thread(target=stest.__main__)
	threads.append(thrd)
	thrd.start()

	r = rendertohat
	work.config.matrixTiles = int(work.workConfig.get("displayconfig", 'matrixTiles'))
	work.config.transWiring = (work.workConfig.getboolean("displayconfig", 'transWiring'))
	work.config.actualScreenWidth  = int(work.workConfig.get("displayconfig", 'actualScreenWidth'))
	work.config.canvasWidth = int(work.workConfig.get("displayconfig", 'canvasWidth'))
	work.config.canvasHeight = int(work.workConfig.get("displayconfig", 'canvasHeight'))
	work.config.rotation = float(work.workConfig.get("displayconfig", 'rotation'))
	work.config.rotationTrailing = (work.workConfig.getboolean("displayconfig", 'rotationTrailing'))
	work.config.fullRotation = (work.workConfig.getboolean("displayconfig", 'fullRotation'))
	work.config.useFilters  = (work.workConfig.getboolean("displayconfig", 'useFilters'))

	try :
		work.config.isRPI = (work.workConfig.getboolean("displayconfig", 'isRPI')) 
	except Exception as e: 
		work.config.useFilters = False
		work.config.isRPI = True
		print (str(e))
	
	r.config = work.config
	r.work = work
	r.canvasOffsetX = int(work.workConfig.get("displayconfig", 'canvasOffsetX'))
	r.canvasOffsetY = int(work.workConfig.get("displayconfig", 'canvasOffsetY'))
	work.config.windowXOffset = int(work.workConfig.get("displayconfig", 'windowXOffset'))
	work.config.windowYOffset = int(work.workConfig.get("displayconfig", 'windowYOffset'))
	r.setUp()
	work.config.render = r.render
	work.config.updateCanvas = r.updateCanvas
	work.main()
'''
def renderUsingLINSNHub(work):

	from modules.rendering import rendertohub
	import threading

	work.config.useFilters  = (work.workConfig.getboolean("displayconfig", 'useFilters'))
	work.config.rotation = float(work.workConfig.get("displayconfig", 'rotation'))
	work.config.rotationTrailing = (work.workConfig.getboolean("displayconfig", 'rotationTrailing'))
	work.config.fullRotation = (work.workConfig.getboolean("displayconfig", 'fullRotation'))
	work.config.canvasWidth = int(work.workConfig.get("displayconfig", 'canvasWidth'))
	work.config.canvasHeight = int(work.workConfig.get("displayconfig", 'canvasHeight'))

	try :
		work.config.isRPI = (work.workConfig.getboolean("displayconfig", 'isRPI')) 
	except Exception as e: 
		work.config.usePixSort = False
		work.config.isRPI = False
		print (str(e))

	if(work.config.isRPI == True) : 
		from cntrlscripts import stest
		thrd = threading.Thread(target=stest.__main__)
		threads.append(thrd)
		thrd.start()
	
	# Create the image-canvas for the work
	# Because rotation is an option, recreate accordingly
	# And to be sure, make the renderImageFull bigger than necessary - 		
	work.config.renderImage = PIL.Image.new("RGBA", (work.config.canvasWidth * work.config.rows, 32))
	work.config.renderImageFull = PIL.Image.new("RGBA", (work.config.canvasWidth, work.config.canvasHeight))
	work.config.renderImageFull = PIL.Image.new("RGBA", (work.config.screenWidth, work.config.screenHeight))

	work.config.renderDraw = ImageDraw.Draw(work.config.renderImageFull)
	work.config.image = PIL.Image.new("RGBA", (work.config.canvasWidth, work.config.canvasHeight))
	work.config.draw = ImageDraw.Draw(work.config.image)

	
	r = rendertohub
	r.config = work.config
	r.work = work

	try :
		work.config.useLastOverlay  = work.workConfig.getboolean("displayconfig", 'useLastOverlay')
		work.config.useLastOverlayProb  = float(work.workConfig.get("displayconfig", 'useLastOverlayProb'))
		work.config.renderImageFullOverlay = Image.new("RGBA", (work.config.canvasWidth, work.config.canvasHeight))
		work.config.renderDrawOver = ImageDraw.Draw(work.config.renderImageFullOverlay)
	except Exception as e: 
		print (str(e))
		work.config.useLastOverlay  = False


	r.canvasOffsetX = int(work.workConfig.get("displayconfig", 'canvasOffsetX'))
	r.canvasOffsetY = int(work.workConfig.get("displayconfig", 'canvasOffsetY'))
	work.config.windowXOffset = int(work.workConfig.get("displayconfig", 'windowXOffset'))
	work.config.windowYOffset = int(work.workConfig.get("displayconfig", 'windowYOffset'))

	work.config.drawBeforeConversion = r.drawBeforeConversion
	work.config.render = r.render
	work.config.updateCanvas = r.updateCanvas
	work.main(False)

	print("Setting Up", work.config.doingReload)
	if(work.config.doingReload == False) : r.setUp()
'''
def renderUsingFFMPEG(work):

	from modules.rendering import rendertofile
	config.useFilters  = (workConfig.getboolean("displayconfig", 'useFilters'))
	config.rotation = float(workConfig.get("displayconfig", 'rotation'))
	config.rotationTrailing = (workConfig.getboolean("displayconfig", 'rotationTrailing'))
	config.fullRotation = (workConfig.getboolean("displayconfig", 'fullRotation'))
	r = rendertofile
	r.config = config
	r.work = work
	r.work.x = r.work.y = 0
	r.fps = int(workConfig.get("output", 'fps'))
	r.duration = int(workConfig.get("output", 'duration'))

	# Test white rectangle on main rendering image
	#config.renderDraw.rectangle((0,0,400,300), fill=(255,255,255))

	config.render = r.render
	config.updateCanvas = r.updateCanvas
	work.main(False)
	
	r.setUp("video")
'''

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''