#!/usr/bin/python
# import modules
import datetime
import gc
import getopt
import importlib
import io
import math
import os
import random
import sys
import textwrap
import time
from random import shuffle
from subprocess import call
from modules.configuration import bcolors
from modules.faderclass import FaderObj
from modules import badpixels, colorutils, configuration
from modules.imagesprite import ImageSprite
from PIL import (
	Image,
	ImageChops,
	ImageDraw,
	ImageEnhance,
	ImageFilter,
	ImageMath,
	ImagePalette,
)

xPos = 320
yPos = 0

bads = badpixels


def main(run=True):
	global config, workConfig, blocks, simulBlocks, bads
	#gc.enable()

	print("Image Piece Loaded")
	config.playSpeed = float(workConfig.get("images", "playSpeed"))

	config.imageToLoad = workConfig.get("images", "i1")
	config.useBlanks = workConfig.getboolean("images", "useBlanks")
	config.useImageFilter = workConfig.getboolean("images", "useImageFilter")

	config.lines = int(workConfig.get("images", "lines"))
	config.boxHeight = int(workConfig.get("images", "boxHeight"))
	config.boxWidth = int(workConfig.get("images", "boxWidth"))
	config.xPos1 = int(workConfig.get("images", "xPos1"))
	config.yPosBase = int(workConfig.get("images", "yPosBase"))
	config.targetClrs = (workConfig.get("images", "targetClrs")).split(",")
	config.targetClrs = list(map(lambda x: int(x), config.targetClrs))
	config.imageFilterProb = float(workConfig.get("images", "imageFilterProb"))
	config.bgFilterProb = float(workConfig.get("images", "bgFilterProb"))
	config.targetPalette = workConfig.get("images", "targetPalette")

	config.clrBlkWidth = int(workConfig.get("images", "clrBlkWidth"))
	config.clrBlkHeight = int(workConfig.get("images", "clrBlkHeight"))
	config.overlayxPosOrig = int(workConfig.get("images", "overlayxPos"))
	config.overlayyPosOrig = int(workConfig.get("images", "overlayyPos"))
	config.overlayxPos = int(workConfig.get("images", "overlayxPos"))
	config.overlayyPos = int(workConfig.get("images", "overlayyPos"))
	config.overlayChangeProb = float(workConfig.get("images", "overlayChangeProb"))
	config.overlayChangePosProb = float(workConfig.get("images", "overlayChangePosProb"))
	config.animateProb = float(workConfig.get("images", "animateProb"))
	config.imageGlitchProb = float(workConfig.get("images", "imageGlitchProb"))



	try:
		config.overlayChangeSizeProb = float(workConfig.get("images", "overlayChangeSizeProb"))
	except Exception as e:
		print(bcolors.FAIL + "** " + bcolors.BOLD)
		print(str(e))
		config.overlayChangeSizeProb = float(workConfig.get("images", "overlayChangePosProb"))

	try:
		config.pausePlayProb = float(workConfig.get("images", "pausePlayProb"))
		config.releasePauseProb = float(workConfig.get("images", "releasePauseProb"))
		config.imageGlitchDisplacementVerical = float(workConfig.get("images", "imageGlitchDisplacementVerical"))
		config.imageGlitchDisplacementHorizontal = int(workConfig.get("images", "imageGlitchDisplacementHorizontal"))
		config.imageGlitchCountLimit = int(workConfig.get("images", "imageGlitchCountLimit"))
		config.glitchChanceWhenPausedFactor = float(workConfig.get("images", "glitchChanceWhenPausedFactor"))
	except Exception as e:
		print(bcolors.FAIL + "** " + bcolors.BOLD)
		print(str(e))
		config.pausePlayProb = 0.001
		config.releasePauseProb = 0.001
		config.imageGlitchDisplacementHorizontal = 10
		config.imageGlitchDisplacementVerical = 10
		config.imageGlitchCountLimit = 20
		config.animateProb = 1.0
		config.glitchChanceWhenPausedFactor = 10.0


	try:
		config.imageGlitchDisplacement = float(workConfig.get("images", "imageGlitchDisplacementVerical"))
	except Exception as e:
		print(bcolors.FAIL + "** " + bcolors.BOLD)
		print(str(e))
		config.imageGlitchDisplacement = 15


	## Generate image holders
	config.workImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.workImageDraw = ImageDraw.Draw(config.workImage)

	config.canvasImage = Image.new("RGBA", (config.canvasWidth * 10, config.canvasHeight))
	config.canvasImageDraw = ImageDraw.Draw(config.canvasImage)

	config.imageLayer = Image.new("RGBA", (config.canvasWidth * 10, config.canvasHeight))
	config.imageLayerDraw = ImageDraw.Draw(config.canvasImage)

	## Sets the image size  -- should probably be set to canvasHeight
	config.channelHeight = config.canvasHeight

	## New configs
	try:
		config.animateProb = float(workConfig.get("images", "animateProb"))
		config.verticalOrientation = int(workConfig.get("images", "verticalOrientation"))
		config.resetProbability =float(workConfig.get("images", "resetProbability"))
	except Exception as e:
		print(bcolors.FAIL + "** " + bcolors.BOLD)
		print(str(e))
		config.animateProb = .5
		config.verticalOrientation = 0
		config.resetProbability = .001

	try:
		config.resizeToFit = workConfig.getboolean("images", "resizeToFit")
	except Exception as e:
		print(bcolors.FAIL + "** " + bcolors.BOLD)
		print(str(e))
		config.resizeToFit = False

	try:
		config.glitchCountRestFactor = float(workConfig.get("images", "glitchCountRestFactor"))
	except Exception as e:
		print(bcolors.FAIL + "** " + bcolors.BOLD)
		print(str(e))
		config.glitchCountRestFactor = 1000

	try:
		config.forceGlitchFrameCount = int(
			workConfig.get("images", "forceGlitchFrameCount")
		)
	except Exception as e:
		print(bcolors.FAIL + "** " + bcolors.BOLD)
		print(str(e))
		config.forceGlitchFrameCount = 220

	try:
		config.doingRefreshCount  = int(
			workConfig.get("images", "doingRefreshCount")
		)
	except Exception as e:
		print(bcolors.FAIL + "** " + bcolors.BOLD)
		print(str(e))
		config.doingRefreshCount = 10



	print(bcolors.OKBLUE + "** " + bcolors.BOLD)

	config.colorOverlay = (255, 0, 255)


	config.imagePath = config.path + "/assets/imgs/"
	config.imageList = [config.imageToLoad]

	if config.useBlanks:
		bads.config = config
		bads.setBlanks = bads.setBlanksOnImage
		bads.numberOfDeadPixels = 5
		bads.probabilityOfBlockBlanks = 0.8
		bads.colsRange = (5, 40)
		bads.rowsRange = (5, 40)
		bads.setBlanks()

	
	config.imgLoader = ImageSprite(config)
	config.imgLoader.debug = False
	config.imgLoader.action = "play"
	config.imgLoader.xOffset = 0
	config.imgLoader.yOffset = 0
	config.imgLoader.endX = config.screenWidth
	config.imgLoader.endY = config.screenHeight
	config.imgLoader.useJitter = True
	config.imgLoader.useBlink = True
	config.imgLoader.brightnessFactor = 0.9
	config.imgLoader.imageGlitchCountLimit = config.imageGlitchCountLimit
	config.imgLoader.pausePlayProb = config.pausePlayProb
	config.imgLoader.releasePauseProb = config.releasePauseProb
	config.imgLoader.imageGlitchProb = config.imageGlitchProb
	config.imgLoader.glitchChanceWhenPausedFactor = config.glitchChanceWhenPausedFactor
	config.imgLoader.config = config
	# processImage = True, resizeImage = True, randomizeDirection = True, randomizeColor = True
	config.imgLoader.make(config.imagePath + config.imageList[0], 0, 0, False, config.resizeToFit, False, True)


	config.f = FaderObj()
	config.f.setUp(config.renderImageFull, config.workImage)
	config.f.doingRefreshCount = config.doingRefreshCount
	config.renderImageFullOld = config.renderImageFull.copy()
	config.fadingDone = True

	config.glitchCount = 0
	config.pausePlay = False


	if run:
		runWork()

def runWork():
	print(bcolors.OKGREEN + "** " + bcolors.BOLD)
	print("Running image.py")
	print(bcolors.ENDC)
	# gc.enable()

	while config.isRunning == True:
		iterate()
		time.sleep(config.playSpeed)
		if config.standAlone == False :
			config.callBack()

def performChanges() :



	if config.imgLoader.action == "play" :
		if random.random() < config.animateProb:
			## holdAnimation
			config.imgLoader.animate(False)
		else:
			config.imgLoader.animate(True)

	x, y = config.workImage.size
	x1, y1 = config.imgLoader.image.size

	#config.workImageDraw = ImageDraw.Draw(config.workImage)
	#config.workImageDraw.rectangle((0,0,256,256), fill=(100,0,0,200))
	#config.workImage = Image.blend(config.workImage,config.imgLoader.image.convert("RGBA"),.5,)

	config.workImage.paste(config.imgLoader.image.convert("RGBA"), (0, 0), config.imgLoader.image.convert("RGBA"))
	
	## RESETS for paused animation
	if config.imgLoader.holdAnimation == True and (config.imgLoader.imageGlitchCount > config.imgLoader.imageGlitchCountLimit or random.random() < config.releasePauseProb):
		config.imgLoader.image = config.imgLoader.imageOriginal.copy()
		config.f.fadingDone = True
		#print(config.glitchCount)
		#print("RESET " + str(config.glitchCount/config.glitchCountRestFactor))
		config.imgLoader.glitchCount = 0
		config.imgLoader.imageGlitchCount = 0
		config.imgLoader.imageGlitchCountLimit = round(random.uniform(2,config.imageGlitchCountLimit))
		config.imgLoader.holdAnimation = False
		config.imgLoader.make(config.imagePath + config.imageList[0], 0, 0, False, config.resizeToFit, False, True)


	

	if random.random() < config.overlayChangeProb:
		if config.verticalOrientation == 0 : 1 
		else : 0


	if random.random() < config.overlayChangeProb:
		#config.colorOverlay = colorutils.getRandomRGB()
		#config.colorOverlay = colorutils.randomColorAlpha(config.brightness * 1.0, 255,255)
		config.colorOverlay = colorutils.getRandomColorHSV(	0,360, .65,1.0, .5,.5, 0,0, 255)


	if random.random() < config.overlayChangeSizeProb:
		config.clrBlkWidth = round(random.uniform(5,config.canvasWidth))
		config.clrBlkHeight = round(random.uniform(5,config.canvasHeight))

	if random.random() < config.overlayChangePosProb:
		config.overlayxPos = round(random.uniform(0,2 * config.canvasWidth/3))
		config.overlayyPos = round(random.uniform(0,2 * config.canvasHeight/3))

	if random.random() < config.overlayChangePosProb/2.0:
		config.overlayxPos = config.overlayxPosOrig
		config.overlayyPos = config.overlayyPosOrig

	colorize(config.colorOverlay)

	if config.useBlanks:
		bads.drawBlanks(None, False)
		if random.random() > 0.99:
			bads.setBlanks()

	'''
	'''

	config.renderImageFull.paste(
		config.workImage, (config.imageXOffset, config.imageYOffset), config.workImage
	)

	#en = ImageEnhance.Brightness(config.renderImageFull)
	#config.renderImageFull = en.enhance(config.brightness)
	#config.renderImageFull.paste(config.renderImageFull)


def iterate(n=0):
	global config, blocks
	global xPos, yPos



	if config.f.fadingDone == True:

		config.renderImageFullOld = config.renderImageFull.copy()
		config.renderImageFull.paste(
			config.workImage,
			(config.imageXOffset, config.imageYOffset),
			config.workImage,
		)
		config.f.xPos = config.imageXOffset
		config.f.yPos = config.imageYOffset

		# config.renderImageFull = config.renderImageFull.convert("RGBA")
		# renderImageFull = renderImageFull.convert("RGBA")

		config.f.setUp(
			config.renderImageFullOld.convert("RGBA"),
			config.workImage.convert("RGBA"),
		)


	performChanges() 
	#config.f.fadeIn()
	#config.render(config.f.blendedImage, 0, 0)
	config.render(config.renderImageFull, 0, 0)

	#config.updateCanvas()


def drawVLine():
	global xPos, yPos
	if random.random() > 0.998:
		pass
		# xPos = int(random.uniform(0,config.screenWidth))
		# yPos = 0 #int(random.uniform(0,config.screenHeight))
	r = 0
	g = 0
	b = 0
	if random.random() > 0.0:
		config.renderDraw.rectangle(
			(xPos, yPos, xPos, config.screenHeight / 2 - 1), fill=(r, g, b)
		)
		config.renderDraw.rectangle(
			(xPos + 1, config.screenHeight / 2, xPos + 1, config.screenHeight),
			fill=(r, g, b),
		)
	xPos -= 1
	if xPos < 0:
		xPos = config.screenWidth


def colorize(clr=(250, 0, 250, 255), recolorize=False):

	# Colorize via overlay etc
	w = config.renderImageFull.size[0]
	h = config.renderImageFull.size[1]

	clrBlock = Image.new(config.workImage.mode, (w, h))
	clrBlockDraw = ImageDraw.Draw(clrBlock)

	# Color overlay on b/w PNG sprite
	#clrBlockDraw.rectangle((0, 0, w, h), fill=(255, 255, 255))
	clrBlockDraw.rectangle(
		(
			config.overlayxPos,
			config.overlayyPos,
			config.clrBlkWidth + config.overlayxPos,
			config.clrBlkHeight + config.overlayyPos,
		),
		fill=clr,
	)
	"""

		ptA = (config.overlayxPos + 10, config.overlayyPos + 20)
		ptB = (config.overlayxPos + config.clrBlkWidth , config.overlayyPos)
		ptC = (config.overlayxPos + config.clrBlkWidth , config.overlayyPos + config.clrBlkHeight + 20)
		ptD = (config.overlayxPos, config.clrBlkHeight + config.overlayyPos)
		clrBlockDraw.polygon([ptA,ptB,ptC,ptD], fill=clr)
		"""
	# config.renderImageFull.paste(clrBlock, (0,0))

	try:
		'''
		if random.random() > .5 :
			config.workImage = ImageChops.add_modulo(clrBlock, config.workImage)
		else :
		'''
		#config.workImage = ImageChops.add_modulo(clrBlock, config.workImage)
		
		imgTemp = ImageChops.darker(clrBlock, config.workImage)
		config.workImage.paste(imgTemp,(0,0), imgTemp)
		#config.workImage = ImageChops.add(clrBlock, config.workImage, .50, 1)
		# imgTemp = imgTemp.convert(config.renderImageFull.mode)
		# print(imgTemp.mode, clrBlock.mode, config.renderImageFull.mode)
		# config.renderImageFull.paste(imgTemp,(0,0,w,h))

	except Exception as e:
		print(e, clrBlock.mode, config.renderImageFull.mode)
		pass


def redrawBackGround():
	config.renderDraw.rectangle(
		(0, 0, config.screenWidth, config.screenHeight), fill=(0, 0, 0)
	)
	# if(random.random() > .99) : gc.collect()
	# if(random.random() > .97) : config.renderImageFull = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	return True


def callBack():
	global config
	return True


#####################
