#!/usr/bin/python
#import modules
from modules import utils, configuration
from modules.imagesprite import ImageSprite
from modules import colorutils

from PIL import Image, ImageDraw, ImageFont
from PIL import ImageFilter
import importlib
import time
import random
from random import shuffle
import datetime
import textwrap
import math
import sys, getopt, os
import ConfigParser, io
import gc
from subprocess import call

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

xPos = 320
yPos = 0
colorModeDirectional = False
colorModes = ["colorWheel","random","colorRGB"]

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def drawVLine() :
	global xPos, yPos
	if(random.random() > .998) :
		pass
		#xPos = int(random.uniform(0,config.screenWidth))
		#yPos = 0 #int(random.uniform(0,config.screenHeight))
	r = 0
	g = 0
	b = 0
	if(random.random() > .0) : 
		config.renderDraw.rectangle((xPos,yPos,xPos, config.screenHeight/2-1), fill = (r,g,b))
		config.renderDraw.rectangle((xPos+1,config.screenHeight/2,xPos+1, config.screenHeight), fill = (r,g,b))
	xPos -= 1
	if(xPos <0):xPos = config.screenWidth

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def redrawBackGround() :
	config.renderDraw.rectangle((0,0,config.screenWidth, config.screenHeight), fill = (0,0,0))
	#config.draw.rectangle((0,0,config.screenWidth, config.screenHeight), fill = (255,0,0))
	#if(random.random() > .99) : gc.collect()
	#if(random.random() > .97) : config.renderImageFull = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	return True

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def main(run = True) :
	global config, workConfig, blocks, simulBlocks, colorModeDirectional
	gc.enable()

	print("Plane Loaded")

	try :
		config.vOffset = int(workConfig.get("images", 'vOffset'))
		config.speed = float(workConfig.get("images", 'redrawSpeed'))
		config.displayRows = int(workConfig.get("images", 'displayRows'))
		config.displayCols = int(workConfig.get("images", 'displayCols'))
		config.unitCount = int(workConfig.get("images", 'unitCount'))
		config.scalingFactor  = float(workConfig.get("images", 'scalingFactor'))
		config.speedFactor  = float(workConfig.get("images", 'speedFactor'))
		config.useJitter  = (workConfig.getboolean("images", 'useJitter'))
		config.jitterRate = float(workConfig.get("images", 'jitterRate'))
		config.useBlink  = (workConfig.getboolean("images", 'useBlink'))
		config.noTrails  = (workConfig.getboolean("images", 'noTrails'))
		config.imageList  = (workConfig.get("images", 'imageList')).split(',')
		config.colorMode  = (workConfig.get("images", 'colorMode'))
		config.randomColorMode  = (workConfig.getboolean("images", 'randomColorMode'))
	except Exception as e: 
		print (str(e))


	#for attr, value in config.__dict__.iteritems():print (attr, value)
	blocks = []
	#for i in range (0,simulBlocks) : makeBlock()

	path = config.path  + "assets/imgs/"
	imageList = config.imageList

	for i in range (0,config.unitCount) :
		dx = 0
		imgLoader = ImageSprite(config)
		imgLoader.debug = True
		imgLoader.action = "pan"
		imgLoader.xOffset = 0
		imgLoader.yOffsetFactor = 0
		imgLoader.endX = config.screenWidth
		imgLoader.endY = config.screenHeight + 32

		imgLoader.scalingFactor = config.scalingFactor
		imgLoader.useJitter =  config.useJitter
		imgLoader.useBlink = config.useBlink
		imgLoader.brightnessFactor = config.brightness * random.random()
		imgLoader.config = config
		imgLoader.colorMode = config.colorMode #"colorRGB" #colorWheel #random #colorRGB
		imgLoader.colorModeDirectional = colorModeDirectional
		if(i == 0) : dx = 0
		# def make(self, img="", setvX = 0, setvY = 0, processImage = True, resizeImage = True, randomizeDirection = True, randomizeColor = True):
		imgLoader.make(path + imageList[i], dx, 0, True, False, False, True)
		imgLoader.yOffsetChange = False
		imgLoader.yOffset = 0
		if(i == 1) : imgLoader.yOffset = 80
		imgLoader.jitterRange = .02
		blocks.append(imgLoader)


	if(run) : runWork()

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def runWork():
	global blocks, config
	#gc.enable()
	print("running work.")
	while True:
		iterate()
		time.sleep(config.speed)	

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def iterate( n = 0) :
	global config, blocks, colorModeDirectional, colorModes
	global xPos, yPos

	# Clear the background and redraw all planes


	if(config.noTrails) : redrawBackGround()

	if(random.random() > .9 and config.randomColorMode == True) :
		index = int(random.uniform(0,3))
		config.colorMode = colorModes[index]

	for n in range (0, len(blocks)) :
		block = blocks[n]
		block.colorMode = config.colorMode
		block.update()
		block.colorModeDirectional = colorModeDirectional
		updateCanvasCall = True if n == 0 else True
		if(random.random() < .001 and n > 0) : 
			clr = colorutils.randomColor(random.random() + .2)
			block.colorize(clr, True)
		if(random.random() < .001 and n == 0) : 
			clr = colorutils.randomColor(random.random() + .2)
			block.colorize(clr, True)
		config.renderImageFull.paste( block.image, (int(block.x), int(block.y)), block.image )


	# Render the final full image
	config.image = config.renderImageFull
	config.render(config.renderImageFull, 0, 0, config.screenWidth, config.screenHeight, False, False, updateCanvasCall)

	# cleanup the list
	#blocks[:] = [block for block in blocks if block.setForRemoval!=True]
	config.updateCanvas()

	if len(blocks) == 0 : exit()

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def callBack() :
	global config
	pass

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
