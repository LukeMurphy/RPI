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
import datetime
import textwrap
import math
import sys, getopt, os
import ConfigParser, io
from subprocess import call

xPos = 320
yPos = 0


def main(run = True) :
	global config, workConfig, blocks, simulBlocks

	print("Plane Loaded")

	config.vOffset = int(workConfig.get("scroll", 'vOffset'))
	config.speed = float(workConfig.get("scroll", 'scrollSpeed'))
	config.displayRows = int(workConfig.get("scroll", 'displayRows'))
	config.displayCols = int(workConfig.get("scroll", 'displayCols'))

	#for attr, value in config.__dict__.iteritems():print (attr, value)
	blocks = []
	#for i in range (0,simulBlocks) : makeBlock()

	

	path = config.path  + "/assets/imgs/"
	imageList = ['plane-2b.gif','plane-2tw.png','plane-2tg.png','plane-2t.png'] 

	for i in range (0,8) :
		imgLoader = ImageSprite(config)
		imgLoader.debug = True
		imgLoader.action = "pan"
		imgLoader.xOffset = 0
		imgLoader.yOffset = 0
		imgLoader.endX = config.screenWidth
		imgLoader.endY = config.screenHeight + 32
		imgLoader.useJitter =  True
		imgLoader.useBlink = True
		imgLoader.brightnessFactor = .9
		imgLoader.config = config
		imgLoader.make(path  + imageList[1], random.uniform(1,2) , 0)

		blocks.append(imgLoader)

	if(run) : runWork()

def runWork():
	global blocks, config
	#gc.enable()
	while True:
		iterate()
		time.sleep(config.speed)	

def iterate( n = 0) :
	global config, blocks
	global xPos, yPos
	for n in range (0, len(blocks)) :
		block = blocks[n]
		block.update()
		updateCanvasCall = True if n == 0 else True
		config.renderImageFull.paste( block.image, (int(block.x), int(block.y)), block.image )
		pos = int(block.x + block.image.size[0])

		'''
		if (  pos == xPos or pos == xPos-1 or pos == xPos-2 or pos == xPos+1 ) : 
			block.blink =  True
			block.blinkNum = int(random.uniform(8,128))
			block.blinkCount = 0
			block.blinkStationary = True if (random.random() > .75) else False
		#config.render(block.image, int(block.x) + block.xOffset, int(block.y) + block.yOffset, block.image.size[0], block.image.size[1], False, False, updateCanvasCall)
		'''



	config.render(config.renderImageFull, 0, 0, config.screenWidth, config.screenHeight, False, False, updateCanvasCall)
	if(random.random() > 1.99) : 
		config.renderImageFull = config.renderImageFull.filter(ImageFilter.GaussianBlur(radius=20))
		config.renderImageFull = config.renderImageFull.filter(ImageFilter.UnsharpMask(radius=20, percent=150,threshold=2))

	redrawBackGround()
	drawVLine()
	#if(block.setForRemoval==True) : makeBlock()

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
	if(random.random() > 1.9) : config.renderImageFull = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	return True

def callBack() :
	global config
	pass











	
#####################


