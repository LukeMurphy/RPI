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
	gc.enable()

	print("Image Piece Loaded")

	config.vOffset = int(workConfig.get("scroll", "vOffset"))
	config.speed = float(workConfig.get("scroll", "scrollSpeed"))
	config.displayRows = int(workConfig.get("scroll", "displayRows"))
	config.displayCols = int(workConfig.get("scroll", "displayCols"))

	config.imageToLoad = workConfig.get("images", "i1")
	config.useBlanks = workConfig.getboolean("images", "useBlanks")
	config.useImageFilter = workConfig.getboolean("images", "useImageFilter")
	config.playSpeed = float(workConfig.get("images", "playSpeed"))

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
	config.overlayChangePosProb = float(
		workConfig.get("images", "overlayChangePosProb")
	)

	config.animateProb = float(workConfig.get("images", "animateProb"))
	config.imageGlitchProb = float(workConfig.get("images", "imageGlitchProb"))
	config.imageGlitchSize = float(workConfig.get("images", "imageGlitchSize"))
	config.imageGlitchDisplacement = int(
		workConfig.get("images", "imageGlitchDisplacement")
	)

	config.workImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.workImageDraw = ImageDraw.Draw(config.workImage)

	## Sets the image size  -- should probably be set to canvasHeight
	config.channelHeight = 256

	## New configs
	config.animateProb = float(workConfig.get("images", "animateProb"))
	config.verticalOrientation = int(workConfig.get("images", "verticalOrientation"))
	config.resetProbability =float(workConfig.get("images", "resetProbability"))

	try:
		config.resizeToFit = workConfig.getboolean("images", "resizeToFit")
	except Exception as e:
		print(str(e))
		config.resizeToFit = False

	try:
		config.glitchCountRestFactor = float(workConfig.get("images", "glitchCountRestFactor"))
	except Exception as e:
		print(str(e))
		config.glitchCountRestFactor = 1000

	try:
		config.forceGlitchFrameCount = int(
			workConfig.get("images", "forceGlitchFrameCount")
		)
	except Exception as e:
		print(str(e))
		config.forceGlitchFrameCount = 220

	try:
		config.doingRefreshCount  = int(
			workConfig.get("images", "doingRefreshCount")
		)
	except Exception as e:
		print(str(e))
		config.doingRefreshCount = 10

	config.colorOverlay = (255, 0, 255)

	# for attr, value in config.__dict__.iteritems():print (attr, value)
	blocks = []
	# for i in range (0,simulBlocks) : makeBlock()

	path = config.path + "/assets/imgs/"
	imageList = [config.imageToLoad]

	if config.useBlanks:
		bads.config = config
		bads.setBlanks = bads.setBlanksOnImage
		bads.numberOfDeadPixels = 5
		bads.probabilityOfBlockBlanks = 0.8
		bads.colsRange = (5, 40)
		bads.rowsRange = (5, 40)
		bads.setBlanks()

	for i in range(0, 1):
		imgLoader = ImageSprite(config)
		imgLoader.debug = True
		imgLoader.action = "play"
		imgLoader.xOffset = 0
		imgLoader.yOffset = 0
		imgLoader.endX = config.screenWidth
		imgLoader.endY = config.screenHeight
		imgLoader.useJitter = True
		imgLoader.useBlink = True
		imgLoader.brightnessFactor = 0.9
		imgLoader.config = config
		# processImage = True, resizeImage = True, randomizeDirection = True, randomizeColor = True
		imgLoader.make(path + imageList[0], 0, 0, False, config.resizeToFit, False, False)
		blocks.append(imgLoader)


	config.canvasImage = Image.new(
		"RGBA", (config.canvasWidth * 10, config.canvasHeight)
	)
	config.canvasImageDraw = ImageDraw.Draw(config.canvasImage)

	config.imageLayer = Image.new(
		"RGBA", (config.canvasWidth * 10, config.canvasHeight)
	)
	config.imageLayerDraw = ImageDraw.Draw(config.canvasImage)

	config.workImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.workImageDraw = ImageDraw.Draw(config.workImage)

	
	config.f = FaderObj()
	config.f.setUp(config.renderImageFull, config.workImage)
	config.f.doingRefreshCount = config.doingRefreshCount
	# config.workImageDraw.rectangle((0,0,100,100), fill=(100,0,0,100))
	config.renderImageFullOld = config.renderImageFull.copy()
	config.fadingDone = True

	config.glitchCount = 0


	if run:
		runWork()


def runWork():
	global blocks, config, bads
	# gc.enable()
	while True:
		iterate()
		time.sleep(config.playSpeed)


def performChanges() :

	if blocks[0].action == "play" and config.animateProb > 0:
		if random.random() < config.animateProb:
			## holdAnimation
			blocks[0].animate(False)
		else:
			blocks[0].animate(True)

	# Clear the background and redraw all planes
	# redrawBackGround()

	# if(random.random() > .98) : config.renderImageFull = config.renderImageFull.filter(ImageFilter.GaussianBlur(radius=20))
	# if(random.random() > .98) : config.renderImageFull = config.renderImageFull.filter(ImageFilter.UnsharpMask(radius=20, percent=150,threshold=2))
	x, y = config.workImage.size
	x1, y1 = blocks[0].image.size

	if random.random() < config.imageGlitchProb:
		blocks[0].glitchBox(
			-config.imageGlitchDisplacement, config.imageGlitchDisplacement
		)
		config.glitchCount += 1
		#config.f.fadingDone = True

	# blocks[0].image = blocks[0].image.convert(config.renderImageFull.mode)
	# config.workImage.paste(blocks[0].image.convert("RGBA"), (0,0,x,y), blocks[0].image.convert("RGBA"))
	config.workImage.paste(
		blocks[0].image.convert("RGBA"), (0, 0), blocks[0].image.convert("RGBA")
	)


	## RESETS
	## config.resetProbability + 
	if random.random() < (config.glitchCount/config.glitchCountRestFactor):
		print("RESET" + str(config.glitchCount/config.glitchCountRestFactor))
		blocks[0].image = blocks[0].imageOriginal.copy()
		blocks[0].process()
		#config.f.fadingDone = True

		#print(config.glitchCount)
		config.glitchCount = 0

	if random.random() < config.overlayChangeProb:
		if config.verticalOrientation == 0 : 1 
		else : 0


	if random.random() < config.overlayChangeProb:
		#config.colorOverlay = colorutils.getRandomRGB()
		config.colorOverlay = colorutils.randomColorAlpha(config.brightness * 2.0, 200,200)
		if random.random() < config.overlayChangePosProb:
			config.overlayyPos = round(random.uniform(0,config.canvasHeight))
			config.overlayxPos = round(random.uniform(0,config.canvasWidth))
		if random.random() < config.overlayChangePosProb:
			config.overlayxPos = config.overlayxPosOrig
			config.overlayyPos = config.overlayyPosOrig

	colorize(config.colorOverlay)

	if config.useBlanks:
		bads.drawBlanks(None, False)
		if random.random() > 0.99:
			bads.setBlanks()

	config.renderImageFull.paste(
		config.workImage, (config.imageXOffset, config.imageYOffset), config.workImage
	)

	en = ImageEnhance.Brightness(config.renderImageFull)
	config.renderImageFull = en.enhance(config.brightness)
	config.renderImageFull.paste(config.renderImageFull)



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
	config.f.fadeIn()
	config.render(config.f.blendedImage, 0, 0)

	'''
	# Render the final full image
	config.render(
		config.renderImageFull,
		0,
		0,
		config.screenWidth,
		config.screenHeight,
		False,
		False,
	)
	'''

	# cleanup the list
	# blocks[:] = [block for block in blocks if block.setForRemoval!=True]
	config.updateCanvas()

	if len(blocks) == 0:
		exit()


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


def colorize(clr=(250, 0, 250), recolorize=False):

	# Colorize via overlay etc
	w = config.renderImageFull.size[0]
	h = config.renderImageFull.size[1]
	clrBlock = Image.new(config.workImage.mode, (w, h))
	clrBlockDraw = ImageDraw.Draw(clrBlock)

	# Color overlay on b/w PNG sprite
	clrBlockDraw.rectangle((0, 0, w, h), fill=(255, 255, 255))
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
		if random.random() > .5 :
			config.workImage = ImageChops.add_modulo(clrBlock, config.workImage)
		else :
			config.workImage = ImageChops.add_modulo(clrBlock, config.workImage)

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
	pass


#####################
