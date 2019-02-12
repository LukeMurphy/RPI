#!/usr/bin/python
#import modules
from modules import configuration
from modules.imagesprite import ImageSprite
from modules import colorutils

from PIL import Image, ImageDraw, ImageFont
from PIL import ImageChops, ImageFilter, ImagePalette
import importlib
import time
import random
from random import shuffle
import datetime
import textwrap
import math
import sys, getopt, os
#import ConfigParser, io
import gc
from subprocess import call

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

xPos = 320
yPos = 0
colorModeDirectional = False
colorModes = ["colorWheel","random","colorRGB"]
glitchRate = .1

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
	global config, workConfig, blocks, simulBlocks, colorModeDirectional, glitchRate
	gc.enable()

	print("Present Loaded")

	try :
		config.vOffset = int(workConfig.get("images", 'vOffset'))
		config.speed = float(workConfig.get("images", 'redrawSpeed'))
		config.displayRows = int(workConfig.get("images", 'displayRows'))
		config.displayCols = int(workConfig.get("images", 'displayCols'))
		config.unitCount = int(workConfig.get("images", 'unitCount'))
		config.scalingFactor  = float(workConfig.get("images", 'scalingFactor'))
		config.speedFactor  = float(workConfig.get("images", 'speedFactor'))
		config.useJitter  = (workConfig.getboolean("images", 'useJitter'))
		config.glitchRate = float(workConfig.get("images", 'glitchRate'))
		config.jitterRange = float(workConfig.get("images", 'jitterRange'))
		config.glitchResetRate = float(workConfig.get("images", 'glitchResetRate'))
		config.glitchModeRate = float(workConfig.get("images", 'glitchModeRate'))
		config.imageGlitchSize = int(workConfig.get("images", 'imageGlitchSize'))
		config.colorChage = float(workConfig.get("images", 'colorChage'))
		config.colorBGChage = float(workConfig.get("images", 'colorBGChage'))
		config.useBlink  = (workConfig.getboolean("images", 'useBlink'))
		config.noTrails  = (workConfig.getboolean("images", 'noTrails'))
		config.imageList  = (workConfig.get("images", 'imageList')).split(',')
		config.colorMode  = (workConfig.get("images", 'colorMode'))
		config.randomColorMode  = (workConfig.getboolean("images", 'randomColorMode'))

		config.clrBlkWidth = int(workConfig.get("filter", 'clrBlkWidth')) 
		config.clrBlkHeight = int(workConfig.get("filter", 'clrBlkHeight')) 
		config.overlayxPosOrig = int(workConfig.get("filter", 'overlayxPos')) 
		config.overlayyPosOrig = int(workConfig.get("filter", 'overlayyPos')) 	
		config.overlayxPos = int(workConfig.get("filter", 'overlayxPos')) 
		config.overlayyPos = int(workConfig.get("filter", 'overlayyPos')) 
		config.overlayChangeProb = float(workConfig.get("filter", 'overlayChangeProb')) 
		config.overlayChangePosProb = float(workConfig.get("filter", 'overlayChangePosProb')) 
		config.colorOverlay  = (255,0,255)

	except Exception as e: 
		print (str(e))


	#for attr, value in config.__dict__.iteritems():print (attr, value)
	blocks = []
	#for i in range (0,simulBlocks) : makeBlock()

	path = config.path  + "assets/imgs/"
	imageList = config.imageList
	glitchRate = config.glitchRate

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
		if(i == 2) : dx = 0
		# def make(self, img="", setvX = 0, setvY = 0, processImage = True, resizeImage = True, randomizeDirection = True, randomizeColor = True):
		imgLoader.make(path + imageList[i], dx, 0, True, False, False, True)
		imgLoader.yOffsetChange = False
		imgLoader.yOffset = 0
		#if(i == 1) : imgLoader.yOffset = 80
		imgLoader.jitterRange = config.jitterRange
		blocks.append(imgLoader)


	print("Running Work...")
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

def dance(): 
	global blocks

	# Jitter a/o glitch 
	# everything is sideways ... width is height etc
	#
	#       "apparentHeight" = width
	# ------------------
	# |                |
	# |                | "apparentWidth"  == height
	# |                |
	# ------------------
	#
	#

	if(len(blocks) > 1) :
		apparentWidth = blocks[1].image.size[1]
		apparentHeight = blocks[1].image.size[0]
		dy = int(random.uniform(-10,10))
		dx = int(random.uniform(1,apparentWidth-2))
		dx = 0

		# really doing "vertical" or y-axis glitching
		# block height is uniform but width is variable

		sectionWidth = int(random.uniform(2,apparentHeight - dx))
		sectionHeight = apparentWidth

		# 95% of the time they dance together as mirrors
		if(random.random() < .97) :
			cp1 = blocks[1].image.crop((dx, 0, dx + sectionWidth, sectionHeight))
			config.renderImageFull.paste( cp1, (int(blocks[1].x + dx), int(blocks[1].y + dy)), cp1)	

		if(len(blocks) >= 3) :
			if(random.random() < .97) :
				cp2 = blocks[2].image.crop((dx, 0, dx + sectionWidth, sectionHeight))
				config.renderImageFull.paste( cp2, (int(blocks[2].x + dx), int(blocks[2].y - dy)), cp2)

		'''	
		# Not sure if this is a useful variation
		if(random.random() < .25) :
			clr = colorutils.randomColor(random.uniform(.1,1))
			blocks[0].colorize(clr, True)
			
		if(random.random() < .1) :
			clr = colorutils.randomColor(random.uniform(.1,1))
			blocks[1].colorize(clr, True)
			clr = colorutils.randomColor(random.uniform(.1,1))
			blocks[2].colorize(clr, True)
		'''

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def glitchBox(img, r1 = -10, r2 = 10) :
	apparentWidth = img.size[1]
	apparentHeight = img.size[0]
	dy = int(random.uniform(r1,r2))
	dx = int(random.uniform(1, config.imageGlitchSize))
	dx = 0

	# really doing "vertical" or y-axis glitching
	# block height is uniform but width is variable

	sectionWidth = int(random.uniform(2, apparentHeight - dx))
	sectionHeight = apparentWidth

	# 95% of the time they dance together as mirrors
	if(random.random() < .97) :
		cp1 = img.crop((dx, 0, dx + sectionWidth, sectionHeight))
		img.paste( cp1, (int(0 + dx), int(0 + dy)))	


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def iterate( n = 0) :
	global config, blocks, colorModeDirectional, colorModes
	global glitchRate

	# Clear the background and redraw all planes
	#if(config.noTrails) : redrawBackGround()
	colorBGChaged = False
	colorChaged = False

	if(random.random() > .9 and config.randomColorMode == True) :
		index = int(random.uniform(0,3))
		config.colorMode = colorModes[index]

	if(random.random() < config.glitchRate) :
		dY = random.uniform(-config.jitterRange,config.jitterRange)
	else :
		dY = 0

	for n in range (0, len(blocks)) :
		block = blocks[n]
		block.colorMode = config.colorMode
		block.colorModeDirectional = colorModeDirectional
		block.update()
		
		### Change the color of the figures
		if(random.random() < config.colorChage and n > 0) : 
			clr = colorutils.randomColor(random.uniform(.1,1))
			block.colorize(clr, True)
			colorBGChaged = True
			for i in range(0,10) : block.glitchBox()
			#config.renderImageFull.paste( block.image, (int(block.x), int(block.y)), block.image )

		### Change the color of the Background -- in configs, BG is first
		if(random.random() < config.colorBGChage and n == 0) : 
			clr = colorutils.randomColor(random.uniform(.4,1))
			block.colorize(clr, True)
			colorBGChaged = True
			for i in range(0,10) : block.glitchBox()
			#config.renderImageFull.paste( block.image, (int(block.x), int(block.y)), block.image )
		
		if(random.random() < .51) : 
			if(n==1) : block.glitchBox(-2,3)
			if(n==2) : block.glitchBox(-3,2)

		config.renderImageFull.paste( block.image, (int(block.x), int(block.y)), block.image )


	if(random.random() < config.glitchResetRate) : 
		glitchRate = config.glitchRate

	if(random.random() < config.glitchModeRate) : 
		glitchRate = .5

	if (random.random() < .1 and colorBGChaged == True):
		for i in range(0,100) : 
			glitchBox(config.renderImageFull,-2,2)

	if(random.random() < glitchRate) : 
		dance()

	# Render the final full image
	#config.image = config.renderImageFull

	if(random.random() < config.overlayChangeProb ) :
		config.colorOverlay = colorutils.getRandomRGB()
		config.colOverlay.colorTransitionSetup()
		#config.colorOverlay = colorutils.getRandomColorWheel()
	if(random.random() < config.overlayChangePosProb ) :
		config.overlayyPos = 100
	if(random.random() < config.overlayChangePosProb ) :
		config.overlayxPos = config.overlayxPosOrig
		config.overlayyPos = config.overlayyPosOrig
	colorize(config.colorOverlay)
	config.render(config.renderImageFull, 0, 0, config.screenWidth, config.screenHeight, False, False, True)


	# cleanup the list
	#blocks[:] = [block for block in blocks if block.setForRemoval!=True]
	config.updateCanvas()

	if len(blocks) == 0 : exit()

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def colorize(clr = (250,0,250), recolorize = False) :

		#Colorize via overlay etc
		w = config.renderImageFull.size[0]
		h = config.renderImageFull.size[1]
		clrBlock = Image.new(config.renderImageFull.mode, (w, h))
		clrBlockDraw = ImageDraw.Draw(clrBlock)

		# Color overlay on b/w PNG sprite
		clrBlockDraw.rectangle((0,0, w, h), fill=(255,255,255))
		clrBlockDraw.rectangle((config.overlayxPos, config.overlayyPos, config.clrBlkWidth + config.overlayxPos, 
								config.clrBlkHeight + config.overlayyPos), fill=clr)
		'''

		ptA = (config.overlayxPos + 10, config.overlayyPos + 20)
		ptB = (config.overlayxPos + config.clrBlkWidth , config.overlayyPos)
		ptC = (config.overlayxPos + config.clrBlkWidth , config.overlayyPos + config.clrBlkHeight + 20)
		ptD = (config.overlayxPos, config.clrBlkHeight + config.overlayyPos)
		clrBlockDraw.polygon([ptA,ptB,ptC,ptD], fill=clr)
		'''
		#config.renderImageFull.paste(clrBlock, (0,0))

		try :
			config.renderImageFull = ImageChops.multiply(clrBlock, config.renderImageFull)
			#imgTemp = imgTemp.convert(config.renderImageFull.mode)
			#print(imgTemp.mode, clrBlock.mode, config.renderImageFull.mode)
			#config.renderImageFull.paste(imgTemp,(0,0,w,h))

		except Exception as e: 
			print(e, clrBlock.mode, config.renderImageFull.mode)
			pass

def callBack() :
	global config
	pass

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
