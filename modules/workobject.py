#!/usr/bin/python
# import modules
import configparser
import datetime
import getopt
import importlib
import math
import os
import random
import sys
import textwrap
import threading
import time

import PIL.Image
from modules import configuration
from modules.configuration import Config, bcolors
from modules.rendering import renderClass
from PIL import Image, ImageChops, ImageDraw, ImageFont


class WorkObject:
	def __init__(self, workArgument, instanceNumber=0):
		print("** WorkObject OBJECT INIT")
		self.instanceNumber = instanceNumber
		self.config = configuration.Config()
		self.workConfig = configparser.ConfigParser()
		self.workConfig.read(workArgument)
		self.workConfigFile = workArgument
		print(bcolors.WARNING + ">> FETCHING: " + " " + workArgument + bcolors.ENDC)

		self.configure()

	def runWork(self):
		# global blocks, config, XOs
		print("** WorkObject RUNNING WORK " + str(self.config.workName))
		# gc.enable()

		while True:
			self.workModule.iterate(self.config)
			time.sleep(self.config.delay)

	def configure(self):
		# global  path, tempImage, threads, thrd
		# gc.enable()

		print(">> PlayerObject setting self.config values")

		### Sets up for testing live self.config chages
		try:
			self.config.checkForConfigChanges = self.workConfig.getboolean(
				"displayconfig", "checkForConfigChanges"
			)
		except Exception as e:
			print(str(e))
			self.config.checkForConfigChanges = False

		try:
			self.config.usePixelSort = self.workConfig.getboolean(
				"displayconfig", "usePixelSort"
			)
			self.config.pixelSortRotatesWithImage = self.workConfig.getboolean(
				"displayconfig", "pixelSortRotatesWithImage"
			)
			self.config.unsharpMaskPercent = int(
				self.workConfig.get("displayconfig", "unsharpMaskPercent")
			)
			self.config.blurRadius = int(
				self.workConfig.get("displayconfig", "blurRadius")
			)
			self.config.pixSortXOffset = int(
				self.workConfig.get("displayconfig", "pixSortXOffset")
			)
			self.config.pixSortYOffset = int(
				self.workConfig.get("displayconfig", "pixSortYOffset")
			)
			self.config.pixSortboxHeight = int(
				self.workConfig.get("displayconfig", "pixSortboxHeight")
			)
			self.config.pixSortboxWidth = int(
				self.workConfig.get("displayconfig", "pixSortboxWidth")
			)
			self.config.pixSortgap = int(
				self.workConfig.get("displayconfig", "pixSortgap")
			)
			self.config.pixSortprobDraw = float(
				self.workConfig.get("displayconfig", "pixSortprobDraw")
			)
			self.config.pixSortprobGetNextColor = float(
				self.workConfig.get("displayconfig", "pixSortprobGetNextColor")
			)
			self.config.pixSortProbDecriment = float(
				self.workConfig.get("displayconfig", "pixSortProbDecriment")
			)
			self.config.pixSortSizeDecriment = float(
				self.workConfig.get("displayconfig", "pixSortSizeDecriment")
			)
			self.config.pixSortSampleVariance = int(
				self.workConfig.get("displayconfig", "pixSortSampleVariance")
			)
			self.config.pixSortDrawVariance = int(
				self.workConfig.get("displayconfig", "pixSortDrawVariance")
			)
			self.config.pixSortDirection = str(
				self.workConfig.get("displayconfig", "pixSortDirection")
			)
			self.config.randomColorProbabilty = float(
				self.workConfig.get("displayconfig", "randomColorProbabilty")
			)
			self.config.brightnessVarLow = float(
				self.workConfig.get("displayconfig", "brightnessVarLow")
			)
			self.config.brightnessVarHi = float(
				self.workConfig.get("displayconfig", "brightnessVarHi")
			)
			self.config.pixelSortAppearanceProb = float(
				self.workConfig.get("displayconfig", "pixelSortAppearanceProb")
			)

		except Exception as e:
			print(str(e))
			self.config.usePixelSort = False
			self.config.pixelSortRotatesWithImage = True
			self.config.unsharpMaskPercent = 50
			self.config.blurRadius = 0
			self.config.pixSortXOffset = 0
			self.config.pixSortYOffset = 0
			self.config.pixSortboxHeight = 40
			self.config.pixSortboxWidth = 96
			self.config.pixSortgap = 2
			self.config.pixSortprobDraw = 0.5
			self.config.pixSortprobGetNextColor = 0.2
			self.config.pixSortSizeDecriment = 0.5
			self.config.pixSortProbDecriment = 0.5
			self.config.pixSortSampleVariance = 10
			self.config.pixSortDrawVariance = 10
			self.config.pixSortDirection = "lateral"
			self.config.randomColorProbabilty = 0.002
			self.config.pixelSortAppearanceProb = 1

			self.config.brightnessVarLow = 0.8
			self.config.brightnessVarHi = 1

		## used when repositioning a block of an image -- sculptural pieces when
		## card configurations can't handle simple set up

		try:
			self.config.remapImageBlock = self.workConfig.getboolean(
				"displayconfig", "remapImageBlock"
			)
			self.config.remapImageBlockSection = self.workConfig.get(
				"displayconfig", "remapImageBlockSection"
			).split(",")
			self.config.remapImageBlockSection = tuple(
				[int(i) for i in self.config.remapImageBlockSection]
			)
			self.config.remapImageBlockDestination = self.workConfig.get(
				"displayconfig", "remapImageBlockDestination"
			).split(",")
			self.config.remapImageBlockDestination = tuple(
				[int(i) for i in self.config.remapImageBlockDestination]
			)
			self.config.filterRemap = True
		except Exception as e:
			print(str(e))
			self.config.remapImageBlock = False
			self.config.filterRemap = False

		try:
			self.config.remapImageBlockSectionRotation = float(
				self.workConfig.get("displayconfig", "remapImageBlockSectionRotation")
			)
		except Exception as e:
			self.config.remapImageBlockSectionRotation = 0

		try:
			self.config.remapImageBlock2 = self.workConfig.getboolean(
				"displayconfig", "remapImageBlock2"
			)
			self.config.remapImageBlockSection2 = self.workConfig.get(
				"displayconfig", "remapImageBlockSection2"
			).split(",")
			self.config.remapImageBlockSection2 = tuple(
				[int(i) for i in self.config.remapImageBlockSection2]
			)
			self.config.remapImageBlockDestination2 = self.workConfig.get(
				"displayconfig", "remapImageBlockDestination2"
			).split(",")
			self.config.remapImageBlockDestination2 = tuple(
				[int(i) for i in self.config.remapImageBlockDestination2]
			)
		except Exception as e:
			print(str(e))
			self.config.remapImageBlock2 = False

		try:
			self.config.remapImageBlockSection2Rotation = float(
				self.workConfig.get("displayconfig", "remapImageBlockSection2Rotation")
			)
		except Exception as e:
			self.config.remapImageBlockSection2Rotation = 0

		try:
			self.config.remapImageBlock3 = self.workConfig.getboolean(
				"displayconfig", "remapImageBlock3"
			)
			self.config.remapImageBlockSection3 = self.workConfig.get(
				"displayconfig", "remapImageBlockSection3"
			).split(",")
			self.config.remapImageBlockSection3 = tuple(
				[int(i) for i in self.config.remapImageBlockSection3]
			)
			self.config.remapImageBlockDestination3 = self.workConfig.get(
				"displayconfig", "remapImageBlockDestination3"
			).split(",")
			self.config.remapImageBlockDestination3 = tuple(
				[int(i) for i in self.config.remapImageBlockDestination3]
			)
		except Exception as e:
			print(str(e))
			self.config.remapImageBlock3 = False

		try:
			self.config.remapImageBlockSection3Rotation = float(
				self.workConfig.get("displayconfig", "remapImageBlockSection3Rotation")
			)
		except Exception as e:
			self.config.remapImageBlockSection3Rotation = 0

		try:
			self.config.remapImageBlock4 = self.workConfig.getboolean(
				"displayconfig", "remapImageBlock4"
			)
			self.config.remapImageBlockSection4 = self.workConfig.get(
				"displayconfig", "remapImageBlockSection4"
			).split(",")
			self.config.remapImageBlockSection4 = tuple(
				[int(i) for i in self.config.remapImageBlockSection4]
			)
			self.config.remapImageBlockDestination4 = self.workConfig.get(
				"displayconfig", "remapImageBlockDestination4"
			).split(",")
			self.config.remapImageBlockDestination4 = tuple(
				[int(i) for i in self.config.remapImageBlockDestination4]
			)
		except Exception as e:
			print(str(e))
			self.config.remapImageBlock4 = False

		try:
			self.config.remapImageBlockSection4Rotation = float(
				self.workConfig.get("displayconfig", "remapImageBlockSection4Rotation")
			)
		except Exception as e:
			self.config.remapImageBlockSection4Rotation = 0

		try:
			self.config.remapImageBlock5 = self.workConfig.getboolean(
				"displayconfig", "remapImageBlock5"
			)
			self.config.remapImageBlockSection5 = self.workConfig.get(
				"displayconfig", "remapImageBlockSection5"
			).split(",")
			self.config.remapImageBlockSection5 = tuple(
				[int(i) for i in self.config.remapImageBlockSection5]
			)
			self.config.remapImageBlockDestination5 = self.workConfig.get(
				"displayconfig", "remapImageBlockDestination5"
			).split(",")
			self.config.remapImageBlockDestination5 = tuple(
				[int(i) for i in self.config.remapImageBlockDestination5]
			)
		except Exception as e:
			print(str(e))
			self.config.remapImageBlock5 = False

		try:
			self.config.remapImageBlockSection5Rotation = float(
				self.workConfig.get("displayconfig", "remapImageBlockSection5Rotation")
			)
		except Exception as e:
			self.config.remapImageBlockSection5Rotation = 0

		try:
			self.config.remapImageBlock6 = self.workConfig.getboolean(
				"displayconfig", "remapImageBlock6"
			)
			self.config.remapImageBlockSection6 = self.workConfig.get(
				"displayconfig", "remapImageBlockSection6"
			).split(",")
			self.config.remapImageBlockSection6 = tuple(
				[int(i) for i in self.config.remapImageBlockSection6]
			)
			self.config.remapImageBlockDestination6 = self.workConfig.get(
				"displayconfig", "remapImageBlockDestination6"
			).split(",")
			self.config.remapImageBlockDestination6 = tuple(
				[int(i) for i in self.config.remapImageBlockDestination6]
			)
		except Exception as e:
			print(str(e))
			self.config.remapImageBlock6 = False

		try:
			self.config.remapImageBlockSection6Rotation = float(
				self.workConfig.get("displayconfig", "remapImageBlockSection6Rotation")
			)
		except Exception as e:
			self.config.remapImageBlockSection6Rotation = 0



		try:
			self.config.imageXOffset = int(
				self.workConfig.get("displayconfig", "imageXOffset")
			)
			self.config.imageYOffset = int(
				self.workConfig.get("displayconfig", "imageYOffset")
			)
		except Exception as e:
			print(str(e))
			self.config.imageXOffset = 0
			self.config.imageYOffset = 0

		try:
			self.config.useBlur = self.workConfig.getboolean("displayconfig", "useBlur")
			self.config.blurXOffset = int(
				self.workConfig.get("displayconfig", "blurXOffset")
			)
			self.config.blurYOffset = int(
				self.workConfig.get("displayconfig", "blurYOffset")
			)
			self.config.blurSectionWidth = int(
				self.workConfig.get("displayconfig", "blurSectionWidth")
			)
			self.config.blurSectionHeight = int(
				self.workConfig.get("displayconfig", "blurSectionHeight")
			)
			self.config.sectionBlurRadius = int(
				self.workConfig.get("displayconfig", "sectionBlurRadius")
			)
			self.config.blurSection = (
				self.config.blurXOffset,
				self.config.blurYOffset,
				self.config.blurXOffset + self.config.blurSectionWidth,
				self.config.blurYOffset + self.config.blurSectionHeight,
			)
		except Exception as e:
			print(str(e))
			self.config.useBlur = False

		try:
			self.config.redBoost = float(
				self.workConfig.get("displayconfig", "redBoost")
			)
			self.config.greenBoost = float(
				self.workConfig.get("displayconfig", "greenBoost")
			)
			self.config.blueBoost = float(
				self.workConfig.get("displayconfig", "blueBoost")
			)
		except Exception as e:
			self.config.redBoost = 1
			self.config.greenBoost = 1
			self.config.blueBoost = 1
			print(str(e))

		try:
			self.config.brightnessVariation = self.workConfig.getboolean(
				"displayconfig", "brightnessVariation"
			)
			self.config.brightnessVariationProb = float(
				self.workConfig.get("displayconfig", "brightnessVariationProb")
			)
			self.config.destinationBrightness = random.uniform(
				0.1, self.config.brightness
			)
			self.config.baseBrightness = self.config.brightness
			self.config.brightnessVariationTransition = False
		except Exception as e:
			self.config.brightnessVariation = False
			self.config.brightnessVariationProb = 0
			print(str(e))

		self.config.screenHeight = int(
			self.workConfig.get("displayconfig", "screenHeight")
		)
		self.config.screenWidth = int(
			self.workConfig.get("displayconfig", "screenWidth")
		)
		# self.config.tileSize = (int(self.workConfig.get("displayconfig", 'tileSizeHeight')),int(self.workConfig.get("displayconfig", 'tileSizeWidth')))
		self.config.tileSize = (
			int(self.workConfig.get("displayconfig", "tileSizeWidth")),
			int(self.workConfig.get("displayconfig", "tileSizeHeight")),
		)
		self.config.rows = int(self.workConfig.get("displayconfig", "rows"))
		self.config.cols = int(self.workConfig.get("displayconfig", "cols"))

		self.config.brightness = float(
			self.workConfig.get("displayconfig", "brightness")
		)

		try:
			self.config.brightness = self.config.brightnessOverride
		except Exception as e:
			print(str(e))

		self.config.minBrightness = float(
			self.workConfig.get("displayconfig", "minBrightness")
		)
		self.config.workName = self.workConfig.get("displayconfig", "work")
		self.config.rendering = self.workConfig.get("displayconfig", "rendering")

		# Create the image-canvas for the work
		"""
		"""
		self.config.renderImage = PIL.Image.new(
			"RGBA", (self.config.screenWidth * self.config.rows, 32)
		)
		self.config.renderImageFull = PIL.Image.new(
			"RGBA", (self.config.screenWidth, self.config.screenHeight)
		)
		self.config.image = PIL.Image.new(
			"RGBA", (self.config.screenWidth, self.config.screenHeight)
		)
		self.config.draw = ImageDraw.Draw(self.config.image)
		self.config.renderDraw = ImageDraw.Draw(self.config.renderImageFull)

		self.config.useFilters = self.workConfig.getboolean(
			"displayconfig", "useFilters"
		)
		self.config.rotation = float(self.workConfig.get("displayconfig", "rotation"))
		self.config.rotationTrailing = self.workConfig.getboolean(
			"displayconfig", "rotationTrailing"
		)
		self.config.fullRotation = self.workConfig.getboolean(
			"displayconfig", "fullRotation"
		)
		self.config.canvasWidth = int(
			self.workConfig.get("displayconfig", "canvasWidth")
		)
		self.config.canvasHeight = int(
			self.workConfig.get("displayconfig", "canvasHeight")
		)

		try:
			self.config.ditherBlurRadius = int(
				self.workConfig.get("displayconfig", "ditherBlurRadius")
			)
			self.config.ditherUnsharpMaskPercent = int(
				self.workConfig.get("displayconfig", "ditherUnsharpMaskPercent")
			)
		except Exception as e:
			self.config.ditherBlurRadius = 0
			self.config.ditherUnsharpMaskPercent = 30
			print(str(e))

		print(self.config.ditherUnsharpMaskPercent)

		# Create the image-canvas for the work
		# Because rotation is an option, recreate accordingly
		# And to be sure, make the renderImageFull bigger than necessary -
		self.config.renderImage = PIL.Image.new(
			"RGBA", (self.config.canvasWidth * self.config.rows, 32)
		)
		self.config.renderImageFull = PIL.Image.new(
			"RGBA", (self.config.canvasWidth, self.config.canvasHeight)
		)

		self.config.renderDraw = ImageDraw.Draw(self.config.renderImageFull)
		self.config.image = PIL.Image.new(
			"RGBA", (self.config.canvasWidth, self.config.canvasHeight)
		)
		self.config.draw = ImageDraw.Draw(self.config.image)

		try:
			self.config.useLastOverlay = self.workConfig.getboolean(
				"displayconfig", "useLastOverlay"
			)
			self.config.useLastOverlayProb = float(
				self.workConfig.get("displayconfig", "useLastOverlayProb")
			)
			self.config.renderImageFullOverlay = Image.new(
				"RGBA", (self.config.canvasWidth, self.config.canvasHeight)
			)
			self.config.renderDrawOver = ImageDraw.Draw(
				self.config.renderImageFullOverlay
			)
		except Exception as e:
			print(str(e))
			self.config.useLastOverlay = False

		self.config.canvasOffsetX = int(
			self.workConfig.get("displayconfig", "canvasOffsetX")
		)
		self.config.canvasOffsetY = int(
			self.workConfig.get("displayconfig", "canvasOffsetY")
		)
		self.config.windowXOffset = int(
			self.workConfig.get("displayconfig", "windowXOffset")
		)
		self.config.windowYOffset = int(
			self.workConfig.get("displayconfig", "windowYOffset")
		)

		# Setting up based on how the work is displayed
		print(
			bcolors.FAIL
			+ ">> WorkObject loading the work: "
			+ str(self.config.workName)
			+ bcolors.ENDC
		)
		importlib.invalidate_caches()
		self.workModule = importlib.import_module("" + str(self.config.workName))
		print(">> WorkObject running main on work")
		self.workModule.main(self.config, self.workConfig, False)
