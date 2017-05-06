#!/usr/bin/python
#import modules
from modules import utils, configuration, badpixels, colorutils
from modules.imagesprite import ImageSprite

from PIL import Image, ImageDraw, ImageMath, ImageEnhance
from PIL import ImageChops, ImageFilter, ImagePalette
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

bads = badpixels


def main(run = True) :
	global config, workConfig, blocks, simulBlocks, bads
	gc.enable()

	print("Image Loaded")

	config.vOffset = int(workConfig.get("scroll", 'vOffset'))
	config.speed = float(workConfig.get("scroll", 'scrollSpeed'))
	config.displayRows = int(workConfig.get("scroll", 'displayRows'))
	config.displayCols = int(workConfig.get("scroll", 'displayCols'))

	config.imageToLoad = (workConfig.get("images", 'i1'))
	config.useBlanks = (workConfig.getboolean("images", 'useBlanks'))
	config.useImageFilter = (workConfig.getboolean("images", 'useImageFilter'))
	config.playSpeed = float(workConfig.get("images", 'playSpeed'))

	config.lines = int(workConfig.get("filter", 'lines'))
	config.boxHeight = int(workConfig.get("filter", 'boxHeight'))
	config.boxWidth = int(workConfig.get("filter", 'boxWidth')) 
	config.xPos1 = int(workConfig.get("filter", 'xPos1'))
	config.yPosBase = int(workConfig.get("filter", 'yPosBase'))
	config.targetClrs = ((workConfig.get("filter", 'targetClrs')).split(','))
	config.targetClrs = map(lambda x: int(x) ,config.targetClrs)
	config.imageFilterProb = float(workConfig.get("filter", 'imageFilterProb'))
	config.bgFilterProb = float(workConfig.get("filter", 'bgFilterProb'))
	config.targetPalette = (workConfig.get("filter", 'targetPalette'))


	config.clrBlkWidth = int(workConfig.get("filter", 'clrBlkWidth')) 
	config.clrBlkHeight = int(workConfig.get("filter", 'clrBlkHeight')) 
	config.overlayxPos = int(workConfig.get("filter", 'overlayxPos')) 
	config.overlayyPos = int(workConfig.get("filter", 'overlayyPos')) 
	config.overlayChangeProb = float(workConfig.get("filter", 'overlayChangeProb')) 

	config.animateProb = float(workConfig.get("filter", 'animateProb')) 
	config.imageGlitchProb = float(workConfig.get("filter", 'imageGlitchProb')) 
	config.imageGlitchSize = float(workConfig.get("filter", 'imageGlitchSize')) 

	config.colorOverlay  = (255,0,255)

	#for attr, value in config.__dict__.iteritems():print (attr, value)
	blocks = []
	#for i in range (0,simulBlocks) : makeBlock()

	path = config.path  + "/assets/imgs/"
	imageList = [config.imageToLoad] 

	if(config.useBlanks) :
		bads.config = config
		bads.setBlanks = bads.setBlanksOnImage
		bads.numberOfDeadPixels = 5
		bads.probabilityOfBlockBlanks = .8
		bads.colsRange = (5,40)
		bads.rowsRange = (5,40)
		bads.setBlanks()

	for i in range (0,1) :
		imgLoader = ImageSprite(config)
		imgLoader.debug = True
		imgLoader.action = "play"
		imgLoader.xOffset = 0
		imgLoader.yOffset = 0
		imgLoader.endX = config.screenWidth
		imgLoader.endY = config.screenHeight
		imgLoader.useJitter =  True
		imgLoader.useBlink = True
		imgLoader.brightnessFactor = .9
		imgLoader.config = config
		# processImage = True, resizeImage = True, randomizeDirection = True, randomizeColor = True
		imgLoader.make(path + imageList[0], 0 , 0, False, False, False, False)
		blocks.append(imgLoader)

	if(run) : runWork()

def runWork():
	global blocks, config, bads
	#gc.enable()
	while True:
		iterate()
		time.sleep(config.playSpeed)	

def iterate( n = 0) :
	global config, blocks
	global xPos, yPos

	if (blocks[0].action == "play") : 
		if(random.random() < config.animateProb ) :
			## holdAnimation
			blocks[0].animate(False)
		else: 
			blocks[0].animate(True)

	# Clear the background and redraw all planes
	#redrawBackGround()

	#if(random.random() > .98) : config.renderImageFull = config.renderImageFull.filter(ImageFilter.GaussianBlur(radius=20))
	#if(random.random() > .98) : config.renderImageFull = config.renderImageFull.filter(ImageFilter.UnsharpMask(radius=20, percent=150,threshold=2))
	x, y = config.renderImageFull.size
	x1, y1  = blocks[0].image.size
	
	if(random.random() < config.imageGlitchProb ) :
		blocks[0].glitchBox()


	#blocks[0].image = blocks[0].image.convert(config.renderImageFull.mode)
	
	config.renderImageFull.paste(blocks[0].image, (0,0,x,y))

	if(random.random() < config.overlayChangeProb ) :
		config.colorOverlay = colorutils.getRandomRGB()
		#config.colorOverlay = colorutils.getRandomColorWheel()
	colorize(config.colorOverlay)


	if(config.useBlanks) :
		bads.drawBlanks(None, False)
		if(random.random() > .99) : bads.setBlanks()
	

	# Render the final full image
	config.render(config.renderImageFull, 0, 0, config.screenWidth, config.screenHeight, False, False)

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

def colorize(clr = (250,0,250), recolorize = False) :

		#Colorize via overlay etc
		w = config.renderImageFull.size[0]
		h = config.renderImageFull.size[1]
		clrBlock = Image.new(config.renderImageFull.mode, (w, h))
		clrBlockDraw = ImageDraw.Draw(clrBlock)

		# Color overlay on b/w PNG sprite
		clrBlockDraw.rectangle((0,0, w, h), fill=(255,255,255))
		clrBlockDraw.rectangle((config.overlayxPos, config.overlayyPos, config.clrBlkWidth + config.overlayxPos, config.clrBlkHeight + config.overlayyPos), fill=clr)
		#config.renderImageFull.paste(clrBlock, (0,0))

		try :
			config.renderImageFull = ImageChops.multiply(clrBlock, config.renderImageFull)
			#imgTemp = imgTemp.convert(config.renderImageFull.mode)
			#print(imgTemp.mode, clrBlock.mode, config.renderImageFull.mode)
			#config.renderImageFull.paste(imgTemp,(0,0,w,h))

		except Exception as e: 
			print(e, clrBlock.mode, config.renderImageFull.mode)
			pass





def redrawBackGround() :	
	config.renderDraw.rectangle((0,0,config.screenWidth, config.screenHeight), fill = (0,0,0))
	#if(random.random() > .99) : gc.collect()
	#if(random.random() > .97) : config.renderImageFull = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	return True

def callBack() :
	global config
	pass











	
#####################