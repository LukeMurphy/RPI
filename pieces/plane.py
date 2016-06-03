#!/usr/bin/python
#import modules
from modules import utils, configuration
from modules.imagesprite import ImageSprite
from configs import localconfig

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

xPos = 320
yPos = 0
colorModeDirectional = False


def main(run = True) :
	global config, workConfig, blocks, simulBlocks, colorModeDirectional
	gc.enable()

	print("Plane Loaded")

	config.vOffset = int(workConfig.get("plane", 'vOffset'))
	config.speed = float(workConfig.get("plane", 'scrollSpeed'))
	config.displayRows = int(workConfig.get("plane", 'displayRows'))
	config.displayCols = int(workConfig.get("plane", 'displayCols'))
	config.unitCount = int(workConfig.get("plane", 'unitCount'))
	config.scalingFactor  = float(workConfig.get("plane", 'scalingFactor'))
	config.useJitter  = bool(workConfig.get("plane", 'useJitter'))
	config.useBlink  = bool(workConfig.get("plane", 'useBlink'))
	config.noTrails  = bool(workConfig.get("plane", 'noTrails'))


	#for attr, value in config.__dict__.iteritems():print (attr, value)
	blocks = []
	#for i in range (0,simulBlocks) : makeBlock()

	path = config.path  + "/assets/imgs/"
	imageList = ['plane-2b.gif','plane-2tw.png','plane-2tg.png','plane-2t.png'] 

	for i in range (0,config.unitCount) :
		imgLoader = ImageSprite(config)
		imgLoader.debug = True
		imgLoader.action = "pan"
		imgLoader.xOffset = 0
		imgLoader.yOffsetFactor = 200
		imgLoader.endX = config.screenWidth
		imgLoader.endY = config.screenHeight + 32
		if(config.unitCount == 1) :
			imgLoader.scalingFactor = config.scalingFactor
			imgLoader.useJitter =  config.useJitter
			imgLoader.useBlink = config.useBlink
			imgLoader.brightnessFactor = config.brightness * random.random()
			imgLoader.config = config
			imgLoader.colorMode = "fixed" #colorWheel #random #colorRGB
			imgLoader.colorModeDirectional = False
			imgLoader.resizeToHeight = False
			imgLoader.yOffsetChange = False
			# processImage = True, resizeImage = True, randomizeDirection = True, randomizeColor = True
			imgLoader.make(path + imageList[3], 1 * config.scalingFactor * 2 , 0, True, False, False, False)

		else :
			imgLoader.scalingFactor = config.scalingFactor
			imgLoader.useJitter =  config.useJitter
			imgLoader.useBlink = config.useBlink
			imgLoader.brightnessFactor = config.brightness * random.random()
			imgLoader.config = config
			imgLoader.colorMode = "colorRGB" #colorWheel #random #colorRGB
			imgLoader.colorModeDirectional = colorModeDirectional
			#imgLoader.make(path + imageList[1], random.uniform(1,2) , 0, False)
			# processImage = True, resizeImage = True, randomizeDirection = True, randomizeColor = True
			imgLoader.make(path + imageList[1], 1 * config.scalingFactor * 2 , 0, True, True, True, True)
		blocks.append(imgLoader)
	# Assume single plane type display


	if(run) : runWork()

def runWork():
	global blocks, config
	#gc.enable()
	print("running work.")
	while True:
		iterate()
		time.sleep(config.speed)	

def iterate( n = 0) :
	global config, blocks, colorModeDirectional
	global xPos, yPos

	# Clear the background and redraw all planes
	if(random.random() > .998) : shuffle(blocks)
	if(random.random() > .9985) : colorModeDirectional = False if colorModeDirectional == True else True

	if(config.noTrails) : redrawBackGround()

	for n in range (0, len(blocks)) :
		block = blocks[n]
		block.update()
		block.colorModeDirectional = colorModeDirectional
		updateCanvasCall = True if n == 0 else True
		config.renderImageFull.paste( block.image, (int(block.x), int(block.y)), block.image )
		# Never really want to do this as it force sends to the renderer for EACH item - big slowdowns etc
		#config.render(block.image, int(block.x), int(block.y), block.image.size[0], block.image.size[1], False, False, updateCanvasCall)
		pos = int(block.x + block.image.size[0])

	#if(random.random() > .98) : config.renderImageFull = config.renderImageFull.filter(ImageFilter.GaussianBlur(radius=20))
	#if(random.random() > .98) : config.renderImageFull = config.renderImageFull.filter(ImageFilter.UnsharpMask(radius=20, percent=150,threshold=2))
	
	#drawVLine()
	#if(block.setForRemoval==True) : makeBlock()
	
	# Render the final full image
	config.image = config.renderImageFull
	config.render(config.renderImageFull, 0, 0, config.screenWidth, config.screenHeight, False, False, updateCanvasCall)


	# cleanup the list
	#blocks[:] = [block for block in blocks if block.setForRemoval!=True]
	config.updateCanvas()

	if len(blocks) == 0 : exit()

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

def redrawBackGround() :
	config.renderDraw.rectangle((0,0,config.screenWidth, config.screenHeight), fill = (0,0,0))
	#config.draw.rectangle((0,0,config.screenWidth, config.screenHeight), fill = (255,0,0))
	#if(random.random() > .99) : gc.collect()
	#if(random.random() > .97) : config.renderImageFull = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	return True

def callBack() :
	global config
	pass











	
#####################