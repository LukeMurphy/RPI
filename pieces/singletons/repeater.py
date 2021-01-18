#!/usr/bin/python
# import modules

import datetime
import getopt
import importlib
import math
import os
import random
import sys
import textwrap
import time
from random import shuffle
from subprocess import call

from modules import configuration
from modules.imagesprite import ImageSprite
from PIL import Image, ImageDraw, ImageFilter, ImageFont

"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

xPos = 320
yPos = 0
colorModeDirectional = True
counter = 0

"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def checkTime():
	config.t2 = time.time()
	delta = config.t2 - config.t1

	if delta > config.timeToComplete:
		config.usePixelSort = False
		# config.rotation = 0


def redrawBackGround():
	config.renderDraw.rectangle(
		(0, 0, config.screenWidth, config.screenHeight), fill=(0, 0, 0)
	)
	# config.draw.rectangle((0,0,config.screenWidth, config.screenHeight), fill = (255,0,0))
	# if(random.random() > .99) : gc.collect()
	# if(random.random() > .97) : config.renderImageFull = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	return True


def kaleidescopic():
	for i in range(1, config.k_rotations):
		img = config.renderImageFull.rotate(config.k_angle * i, expand=False)
		config.renderImageFull.paste(img.convert("RGBA"), (0, 0))


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def main(run=True):
	global config, workConfig, blocks, simulBlocks, colorModeDirectional

	print("REPEATER Loaded")

	config.vOffset = int(workConfig.get("repeater", "vOffset"))
	config.speed = float(workConfig.get("repeater", "scrollSpeed"))
	config.displayRows = int(workConfig.get("repeater", "displayRows"))
	config.displayCols = int(workConfig.get("repeater", "displayCols"))
	config.unitCount = int(workConfig.get("repeater", "unitCount"))
	config.scalingFactor = float(workConfig.get("repeater", "scalingFactor"))
	config.speedFactor = float(workConfig.get("repeater", "speedFactor"))
	config.useJitter = workConfig.getboolean("repeater", "useJitter")
	config.useBlink = workConfig.getboolean("repeater", "useBlink")
	config.noTrails = workConfig.getboolean("repeater", "noTrails")
	config.imageList = workConfig.get("repeater", "imageList")
	config.channelHeight = int(workConfig.get("repeater", "channelHeight"))

	try:
		config.pauseProb = float(workConfig.get("repeater", "pauseProb"))
	except Exception as e:
		config.pauseProb = 0.0
		print(str(e))

	config.t1 = time.time()
	config.t2 = time.time()
	config.timeToComplete = 0

	try:
		config.colorMode = workConfig.get("repeater", "colorMode")
	except Exception as e:
		print(str(e))
		config.colorMode = "randomized"

	try:
		config.kaleidescopicEffect = workConfig.getboolean(
			"repeater", "kaleidescopicEffect"
		)
		config.k_rotations = int(workConfig.get("repeater", "k_rotations"))
		config.k_angle = float(workConfig.get("repeater", "k_angle"))
	except Exception as e:
		print(str(e))
		config.kaleidescopicEffect = False

	try:
		config.resizeMin = float(workConfig.get("repeater", "resizeMin"))
		config.resizeMax = float(workConfig.get("repeater", "resizeMax"))
	except Exception as e:
		print(str(e))
		config.resizeMin = 0.1
		config.resizeMax = 1.2

	# for attr, value in config.__dict__.iteritems():print (attr, value)
	blocks = []
	# for i in range (0,simulBlocks) : makeBlock()

	path = config.path + "/assets/imgs/"

	imageList = []

	for element in config.imageList.split(',') :
		imageList.append(element)


	for i in range(0, config.unitCount):
		imgLoader = ImageSprite(config)
		imgLoader.debug = False
		imgLoader.action = "pan"
		imgLoader.xOffset = 0
		imgLoader.yOffsetFactor = 200
		imgLoader.endX = config.screenWidth
		imgLoader.endY = config.screenHeight + 32
		if config.unitCount == 1:
			imgLoader.scalingFactor = config.scalingFactor
			imgLoader.useJitter = config.useJitter
			imgLoader.useBlink = config.useBlink
			imgLoader.brightnessFactor = config.brightness * random.random()
			imgLoader.config = config
			imgLoader.colorMode = "fixed"  # colorWheel #random #colorRGB
			imgLoader.colorModeDirectional = False
			imgLoader.resizeToHeight = False
			imgLoader.yOffsetChange = False
			# processImage = True, resizeImage = True, randomizeDirection = True, randomizeColor = True
		else:
			imgLoader.scalingFactor = config.scalingFactor
			imgLoader.useJitter = config.useJitter
			imgLoader.useBlink = config.useBlink
			imgLoader.brightnessFactor = config.brightness * random.uniform(.4,1.1)
			imgLoader.config = config
			if config.colorMode == "randomized":
				imgLoader.colorMode = "random"
				if random.random() < 0.5:
					imgLoader.colorMode = "colorRGB"
			else:
				imgLoader.colorMode = config.colorMode
			imgLoader.resizeMin = config.resizeMin
			imgLoader.resizeMax = config.resizeMax
			# colorRGB" #colorWheel #random #colorRGB
			imgLoader.colorModeDirectional = colorModeDirectional
			# imgLoader.make(path + imageList[1], random.uniform(1,2) , 0, False)
			# processImage = True, resizeImage = True, randomizeDirection = True, randomizeColor = True
			""" Speed """
			vX = 1 * config.scalingFactor * 2 * config.speedFactor

			# imgLoader.make(path + imageList[0], vX, 0, True, True, True, True)

			imageListIndex = round(random.uniform(0,len(imageList)-1))
			imgLoader.make(path + imageList[imageListIndex], vX, 0, True, True, True, True)
			# imgLoader.x = imgLoader.xPos = 0 #config.screenWidth/4 * random.random()
			# imgLoader.y = imgLoader.yPos = 10 + i * 10 #config.screenWidth/4 * random.random()
			# print (imgLoader.x, imgLoader.xPos, imgLoader.y, imgLoader.dX, imgLoader.dY)

		blocks.append(imgLoader)
	# Assume single item type display

	if run:
		runWork()


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

def runWork():
	global config
	print(bcolors.OKGREEN + "** " + bcolors.BOLD)
	print("RUNNING REPEATER repeater.py")
	print(bcolors.ENDC)

	while config.isRunning == True:
		iterate()
		time.sleep(config.speed)
		if config.standAlone == False :
			config.callBack()



"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def iterate(n=0):
	global config, blocks, colorModeDirectional
	global xPos, yPos

	# Clear the background and redraw all planes
	if random.random() > 0.9985:
		shuffle(blocks)

	if random.random() > 0.9985:
		colorModeDirectional = False if colorModeDirectional == True else True

	if config.noTrails == True:
		redrawBackGround()



	for n in range(0, len(blocks)):
		block = blocks[n]
		block.update()
		block.colorModeDirectional = colorModeDirectional
		updateCanvasCall = True if n == 0 else True
		config.renderImageFull.paste(
			block.image, (round(block.x), round(block.y)), block.image
		)
		# Never really want to do this as it force sends to the renderer for EACH item - big slowdowns etc
		# config.render(block.image, int(block.x), int(block.y), block.image.size[0], block.image.size[1], False, False, updateCanvasCall)
		pos = round(block.x + block.image.size[0])


	# if(random.random() > .98) : config.renderImageFull = config.renderImageFull.filter(ImageFilter.GaussianBlur(radius=20))
	# if(random.random() > .98) : config.renderImageFull = config.renderImageFull.filter(ImageFilter.UnsharpMask(radius=20, percent=150,threshold=2))
	# if(block.setForRemoval==True) : makeBlock()

	if random.random() < config.pauseProb and config.usePixelSort == False:
		config.usePixelSort = True
		config.t1 = time.time()
		config.timeToComplete = random.uniform(1, 10)

	checkTime()

	if config.kaleidescopicEffect == True:
		config.noTrails = False
		kaleidescopic()

	# Render the final full image
	config.render(
		config.renderImageFull,
		0,
		0,
		config.screenWidth,
		config.screenHeight,
		False,
		False,
		updateCanvasCall,
	)

	# cleanup the list
	# blocks[:] = [block for block in blocks if block.setForRemoval!=True]
	config.updateCanvas()

	if len(blocks) == 0:
		exit()


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def callBack():
	global config
	pass


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
