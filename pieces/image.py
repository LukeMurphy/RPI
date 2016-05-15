#!/usr/bin/python
#import modules
from modules import utils, configuration, badpixels
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

bads = badpixels


def main(run = True) :
	global config, workConfig, blocks, simulBlocks, bads
	gc.enable()

	print("Plane Loaded")

	config.vOffset = int(workConfig.get("scroll", 'vOffset'))
	config.speed = float(workConfig.get("scroll", 'scrollSpeed'))
	config.displayRows = int(workConfig.get("scroll", 'displayRows'))
	config.displayCols = int(workConfig.get("scroll", 'displayCols'))
	config.imageToLoad = (workConfig.get("images", 'i1'))

	#for attr, value in config.__dict__.iteritems():print (attr, value)
	blocks = []
	#for i in range (0,simulBlocks) : makeBlock()

	path = config.path  + "/assets/imgs/"
	imageList = [config.imageToLoad] 

	bads.config = config
	bads.setBlanks = bads.setBlanksOnImage
	bads.numberOfDeadPixels = 200
	bads.probabilityOfBlockBlanks = .99
	bads.setBlanks()

	for i in range (0,1) :
		imgLoader = ImageSprite(config)
		imgLoader.debug = True
		imgLoader.action = "present"
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
		time.sleep(config.speed)	

def iterate( n = 0) :
	global config, blocks
	global xPos, yPos

	# Clear the background and redraw all planes
	#redrawBackGround()

	#if(random.random() > .98) : config.renderImageFull = config.renderImageFull.filter(ImageFilter.GaussianBlur(radius=20))
	#if(random.random() > .98) : config.renderImageFull = config.renderImageFull.filter(ImageFilter.UnsharpMask(radius=20, percent=150,threshold=2))
	config.renderImageFull.paste(blocks[0].image)

	bads.drawBlanks(None, False)
	if(random.random() > .2) : bads.setBlanks()
	
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

def redrawBackGround() :	
	config.renderDraw.rectangle((0,0,config.screenWidth, config.screenHeight), fill = (0,0,0))
	#if(random.random() > .99) : gc.collect()
	#if(random.random() > .97) : config.renderImageFull = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	return True

def callBack() :
	global config
	pass











	
#####################