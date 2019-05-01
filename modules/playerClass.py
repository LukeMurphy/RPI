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

class PlayerObject:

	def __init__(self, config, workconfig, masterConfig, instanceNumber):
		print("PlayerObject init: " + str(instanceNumber))
		self.config = config
		self.workconfig = workconfig
		self.instanceNumber = instanceNumber
		self.masterConfig = masterConfig


	def configure(self) :
		global  path, tempImage, threads, thrd
		#gc.enable()
		
		print("setting self.config values")

		### Sets up for testing live self.config chages
		try:
			self.config.checkForConfigChanges = (self.workconfig.getboolean("displayconfig", 'checkForConfigChanges'))
		except  Exception as e: 
			print (str(e))
			self.config.checkForConfigChanges = False

		try :
			self.config.usePixelSort  = (self.workconfig.getboolean("displayconfig", 'usePixelSort'))
			self.config.pixelSortRotatesWithImage  = (self.workconfig.getboolean("displayconfig", 'pixelSortRotatesWithImage'))
			self.config.unsharpMaskPercent  = int(self.workconfig.get("displayconfig", 'unsharpMaskPercent'))
			self.config.blurRadius  = int(self.workconfig.get("displayconfig", 'blurRadius'))
			self.config.pixSortXOffset  = int(self.workconfig.get("displayconfig", 'pixSortXOffset'))
			self.config.pixSortYOffset  = int(self.workconfig.get("displayconfig", 'pixSortYOffset'))
			self.config.pixSortboxHeight  = int(self.workconfig.get("displayconfig", 'pixSortboxHeight'))
			self.config.pixSortboxWidth  = int(self.workconfig.get("displayconfig", 'pixSortboxWidth'))
			self.config.pixSortgap  = int(self.workconfig.get("displayconfig", 'pixSortgap'))
			self.config.pixSortprobDraw  = float(self.workconfig.get("displayconfig", 'pixSortprobDraw'))
			self.config.pixSortprobGetNextColor  = float(self.workconfig.get("displayconfig", 'pixSortprobGetNextColor'))
			self.config.pixSortProbDecriment  = float(self.workconfig.get("displayconfig", 'pixSortProbDecriment'))
			self.config.pixSortSizeDecriment  = float(self.workconfig.get("displayconfig", 'pixSortSizeDecriment'))
			self.config.pixSortSampleVariance  = int(self.workconfig.get("displayconfig", 'pixSortSampleVariance'))
			self.config.pixSortDrawVariance  = int(self.workconfig.get("displayconfig", 'pixSortDrawVariance'))
			self.config.pixSortDirection = str(self.workconfig.get("displayconfig", 'pixSortDirection'))
			self.config.randomColorProbabilty = float(self.workconfig.get("displayconfig", 'randomColorProbabilty'))
			self.config.brightnessVarLow = float(self.workconfig.get("displayconfig", 'brightnessVarLow'))
			self.config.brightnessVarHi = float(self.workconfig.get("displayconfig", 'brightnessVarHi'))
			self.config.pixelSortAppearanceProb = float(self.workconfig.get("displayconfig", 'pixelSortAppearanceProb'))

		except Exception as e:
			print (str(e))
			self.config.usePixelSort = False
			self.config.pixelSortRotatesWithImage = True
			self.config.unsharpMaskPercent  = 50
			self.config.blurRadius  = 0
			self.config.pixSortXOffset = 0
			self.config.pixSortYOffset = 0
			self.config.pixSortboxHeight = 40
			self.config.pixSortboxWidth = 96
			self.config.pixSortgap = 2
			self.config.pixSortprobDraw = .5
			self.config.pixSortprobGetNextColor = .2
			self.config.pixSortSizeDecriment = .5
			self.config.pixSortProbDecriment = .5
			self.config.pixSortSampleVariance = 10
			self.config.pixSortDrawVariance = 10
			self.config.pixSortDirection = 'lateral'
			self.config.randomColorProbabilty = .002
			self.config.pixelSortAppearanceProb = 1

			self.config.brightnessVarLow = .8
			self.config.brightnessVarHi = 1

		## used when repositioning a block of an image -- sculptural pieces when
		## card configurations can't handle simple set up

		try :
			self.config.remapImageBlock = (self.workconfig.getboolean("displayconfig", 'remapImageBlock'))
			self.config.remapImageBlockSection = self.workconfig.get("displayconfig", 'remapImageBlockSection').split(",")
			self.config.remapImageBlockSection = tuple([int(i) for i in self.config.remapImageBlockSection])
			self.config.remapImageBlockDestination = self.workconfig.get("displayconfig", 'remapImageBlockDestination').split(",")
			self.config.remapImageBlockDestination = tuple([int(i) for i in self.config.remapImageBlockDestination])
			self.config.filterRemap = True
		except Exception as e:
			print (str(e))
			self.config.remapImageBlock = False
			self.config.filterRemap = False
		
		try :
			self.config.remapImageBlockSectionRotation = float(self.workconfig.get("displayconfig", 'remapImageBlockSectionRotation'))
		except Exception as e:
			self.config.remapImageBlockSectionRotation = 0	

		try :
			self.config.remapImageBlock2 = (self.workconfig.getboolean("displayconfig", 'remapImageBlock2'))
			self.config.remapImageBlockSection2 = self.workconfig.get("displayconfig", 'remapImageBlockSection2').split(",")
			self.config.remapImageBlockSection2 = tuple([int(i) for i in self.config.remapImageBlockSection2])
			self.config.remapImageBlockDestination2 = self.workconfig.get("displayconfig", 'remapImageBlockDestination2').split(",")
			self.config.remapImageBlockDestination2 = tuple([int(i) for i in self.config.remapImageBlockDestination2])
		except Exception as e:
			print (str(e))
			self.config.remapImageBlock2 = False	


		try :
			self.config.remapImageBlockSection2Rotation = float(self.workconfig.get("displayconfig", 'remapImageBlockSection2Rotation'))
		except Exception as e:
			self.config.remapImageBlockSection2Rotation = 0


		try :
			self.config.remapImageBlock3 = (self.workconfig.getboolean("displayconfig", 'remapImageBlock3'))
			self.config.remapImageBlockSection3 = self.workconfig.get("displayconfig", 'remapImageBlockSection3').split(",")
			self.config.remapImageBlockSection3 = tuple([int(i) for i in self.config.remapImageBlockSection3])
			self.config.remapImageBlockDestination3 = self.workconfig.get("displayconfig", 'remapImageBlockDestination3').split(",")
			self.config.remapImageBlockDestination3 = tuple([int(i) for i in self.config.remapImageBlockDestination3])
		except Exception as e:
			print (str(e))
			self.config.remapImageBlock3 = False


		try :
			self.config.remapImageBlockSection3Rotation = float(self.workconfig.get("displayconfig", 'remapImageBlockSection3Rotation'))
		except Exception as e:
			self.config.remapImageBlockSection3Rotation = 0


		try :
			self.config.remapImageBlock4 = (self.workconfig.getboolean("displayconfig", 'remapImageBlock4'))
			self.config.remapImageBlockSection4 = self.workconfig.get("displayconfig", 'remapImageBlockSection4').split(",")
			self.config.remapImageBlockSection4 = tuple([int(i) for i in self.config.remapImageBlockSection4])
			self.config.remapImageBlockDestination4 = self.workconfig.get("displayconfig", 'remapImageBlockDestination4').split(",")
			self.config.remapImageBlockDestination4 = tuple([int(i) for i in self.config.remapImageBlockDestination4])
		except Exception as e:
			print (str(e))
			self.config.remapImageBlock4 = False


		try :
			self.config.remapImageBlockSection4Rotation = float(self.workconfig.get("displayconfig", 'remapImageBlockSection4Rotation'))
		except Exception as e:
			self.config.remapImageBlockSection4Rotation = 0


		try :
			self.config.imageXOffset = int(self.workconfig.get("displayconfig","imageXOffset"))
			self.config.imageYOffset = int(self.workconfig.get("displayconfig","imageYOffset"))
		except Exception as e:
			print (str(e))
			self.config.imageXOffset = 0
			self.config.imageYOffset = 0


		try :
			self.config.useBlur  = self.workconfig.getboolean("displayconfig", 'useBlur')
			self.config.blurXOffset = int(self.workconfig.get("displayconfig", 'blurXOffset'))
			self.config.blurYOffset = int(self.workconfig.get("displayconfig", 'blurYOffset'))
			self.config.blurSectionWidth = int(self.workconfig.get("displayconfig", 'blurSectionWidth'))
			self.config.blurSectionHeight = int(self.workconfig.get("displayconfig", 'blurSectionHeight'))
			self.config.sectionBlurRadius = int(self.workconfig.get("displayconfig", 'sectionBlurRadius'))
			self.config.blurSection = (self.config.blurXOffset, self.config.blurYOffset, self.config.blurXOffset + self.config.blurSectionWidth, self.config.blurYOffset + self.config.blurSectionHeight)
		except Exception as e: 
			print (str(e))
			self.config.useBlur  = False


		try:
			self.config.redBoost = float(self.workconfig.get("displayconfig", 'redBoost'))
			self.config.greenBoost = float(self.workconfig.get("displayconfig", 'greenBoost'))
			self.config.blueBoost = float(self.workconfig.get("displayconfig", 'blueBoost'))
		except Exception as e: 
			self.config.redBoost = 1
			self.config.greenBoost = 1
			self.config.blueBoost = 1
			print (str(e))

		try:
			self.config.brightnessVariation = (self.workconfig.getboolean("displayconfig", 'brightnessVariation'))
			self.config.brightnessVariationProb = float(self.workconfig.get("displayconfig", 'brightnessVariationProb'))
			self.config.destinationBrightness = random.uniform(.1, self.config.brightness)
			self.config.baseBrightness = self.config.brightness
			self.config.brightnessVariationTransition = False
		except Exception as e: 
			self.config.brightnessVariation = False
			self.config.brightnessVariationProb = 0
			print (str(e))


		self.config.screenHeight = int(self.workconfig.get("displayconfig", 'screenHeight'))
		self.config.screenWidth =  int(self.workconfig.get("displayconfig", 'screenWidth'))
		#self.config.tileSize = (int(self.workconfig.get("displayconfig", 'tileSizeHeight')),int(self.workconfig.get("displayconfig", 'tileSizeWidth')))
		self.config.tileSize = (int(self.workconfig.get("displayconfig", 'tileSizeWidth')),int(self.workconfig.get("displayconfig", 'tileSizeHeight')))
		self.config.rows = int(self.workconfig.get("displayconfig", 'rows'))
		self.config.cols = int(self.workconfig.get("displayconfig", 'cols'))

		self.config.brightness =  float(self.workconfig.get("displayconfig", 'brightness'))
		if(self.config.brightnessOverride is not None) : self.config.brightness = self.config.brightnessOverride

		self.config.minBrightness  = float(self.workconfig.get("displayconfig", 'minBrightness'))
		self.config.work = self.workconfig.get("displayconfig", 'work')
		self.config.rendering = self.workconfig.get("displayconfig", 'rendering')

		# Create the image-canvas for the work
		self.config.renderImage = PIL.Image.new("RGBA", (self.config.screenWidth*self.config.rows, 32))
		self.config.renderImageFull = PIL.Image.new("RGBA", (self.config.screenWidth, self.config.screenHeight))
		self.config.image = PIL.Image.new("RGBA", (self.config.screenWidth, self.config.screenHeight))
		self.config.draw = ImageDraw.Draw(self.config.image)
		self.config.renderDraw = ImageDraw.Draw(self.config.renderImageFull)


		# Setting up based on how the work is displayed
		print("Loading:", str(self.config.work))
		work = importlib.import_module('pieces.'+str(self.config.work))
		work.config = self.config
		work.workConfig = self.workconfig

		self.work = work

		#if(self.config.rendering == "hat") : renderUsingIDAFruitHat(work)
		

		##############################################################
		# ------------------------------------------------------------

		if(self.config.rendering == "hub") : 
			self.renderUsingLINSNHub(self.work)

		# ------------------------------------------------------------
		#if(self.config.rendering == "out") : renderUsingFFMPEG(work)
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
		work.config.matrixTiles = int(work.workconfig.get("displayconfig", 'matrixTiles'))
		work.config.transWiring = (work.workconfig.getboolean("displayconfig", 'transWiring'))
		work.config.actualScreenWidth  = int(work.workconfig.get("displayconfig", 'actualScreenWidth'))
		work.config.canvasWidth = int(work.workconfig.get("displayconfig", 'canvasWidth'))
		work.config.canvasHeight = int(work.workconfig.get("displayconfig", 'canvasHeight'))
		work.config.rotation = float(work.workconfig.get("displayconfig", 'rotation'))
		work.config.rotationTrailing = (work.workconfig.getboolean("displayconfig", 'rotationTrailing'))
		work.config.fullRotation = (work.workconfig.getboolean("displayconfig", 'fullRotation'))
		work.config.useFilters  = (work.workconfig.getboolean("displayconfig", 'useFilters'))

		try :
			work.config.isRPI = (work.workconfig.getboolean("displayconfig", 'isRPI')) 
		except Exception as e: 
			work.config.useFilters = False
			work.config.isRPI = True
			print (str(e))
		
		r.self.config = work.config
		r.work = work
		r.canvasOffsetX = int(work.workconfig.get("displayconfig", 'canvasOffsetX'))
		r.canvasOffsetY = int(work.workconfig.get("displayconfig", 'canvasOffsetY'))
		work.config.windowXOffset = int(work.workconfig.get("displayconfig", 'windowXOffset'))
		work.config.windowYOffset = int(work.workconfig.get("displayconfig", 'windowYOffset'))
		r.setUp()
		work.config.render = r.render
		work.config.updateCanvas = r.updateCanvas
		work.main()
	'''
	def renderUsingLINSNHub(self, work):

		from modules.rendering import rendertohub
		import threading

		self.work = work

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

		self.r = rendertohub.renderCanvasCreate(work.config)
		self.r.config = work.config
		self.r.work = work

		try :
			work.config.useLastOverlay  = work.workConfig.getboolean("displayconfig", 'useLastOverlay')
			work.config.useLastOverlayProb  = float(work.workConfig.get("displayconfig", 'useLastOverlayProb'))
			work.config.renderImageFullOverlay = Image.new("RGBA", (work.config.canvasWidth, work.config.canvasHeight))
			work.config.renderDrawOver = ImageDraw.Draw(work.config.renderImageFullOverlay)
		except Exception as e: 
			print (str(e))
			work.config.useLastOverlay  = False


		self.r.canvasOffsetX = int(work.workConfig.get("displayconfig", 'canvasOffsetX'))
		self.r.canvasOffsetY = int(work.workConfig.get("displayconfig", 'canvasOffsetY'))
		work.config.windowXOffset = int(work.workConfig.get("displayconfig", 'windowXOffset'))
		work.config.windowYOffset = int(work.workConfig.get("displayconfig", 'windowYOffset'))
		work.config.drawBeforeConversion = self.r.drawBeforeConversion
		work.config.render = self.r.render
		work.config.updateCanvas = self.r.updateCanvas

		self.work = work
		self.work.main(False)

		print("Setting Up - Reload? ", work.config.doingReload)
		
		'''
		## Initialize the renderer
		## For now, just two player instances taking diff configs etc
		if(work.config.doingReload == False) : 
			self.r.setUp(self.masterConfig, self.work.config, True, self.instanceNumber)

		'''


	'''
	def renderUsingFFMPEG(work):

		from modules.rendering import rendertofile
		self.config.useFilters  = (self.workconfig.getboolean("displayconfig", 'useFilters'))
		self.config.rotation = float(self.workconfig.get("displayconfig", 'rotation'))
		self.config.rotationTrailing = (self.workconfig.getboolean("displayconfig", 'rotationTrailing'))
		self.config.fullRotation = (self.workconfig.getboolean("displayconfig", 'fullRotation'))
		r = rendertofile
		r.self.config = self.config
		r.work = work
		r.work.x = r.work.y = 0
		r.fps = int(self.workconfig.get("output", 'fps'))
		r.duration = int(self.workconfig.get("output", 'duration'))

		# Test white rectangle on main rendering image
		#self.config.renderDraw.rectangle((0,0,400,300), fill=(255,255,255))

		self.config.render = r.render
		self.config.updateCanvas = r.updateCanvas
		work.main(False)
		
		r.setUp("video")
	'''

	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''