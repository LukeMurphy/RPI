#!/usr/bin/python
#import modules
from modules import utils, configuration
from modules.imagesprite import ImageSprite
from configs import localconfig

from PIL import Image, ImageDraw, ImageFont
import importlib
import time
import random
import datetime
import textwrap
import math
import sys, getopt, os
import ConfigParser, io
from subprocess import call


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

	

	path = config.path  + "assets/imgs/"
	imageList = ['plane-2b.gif','plane-2t.png'] 

	imgLoader = ImageSprite(config)
	imgLoader.debug = True
	imgLoader.action = "pan"
	imgLoader.countLimit = 1
	imgLoader.xOffset = 0
	imgLoader.yOffset = 0
	imgLoader.endX = config.screenWidth
	imgLoader.endY = config.screenHeight + 32
	imgLoader.panRangeLimit = 0 + config.screenWidth
	imgLoader.scrollSpeed = .01
	imgLoader.useJitter =  True
	imgLoader.useBlink = False
	imgLoader.brightnessFactor = .85
	imgLoader.config = config
	imgLoader.iid = "one=>"
	imgLoader.make(path  + imageList[1], 2 , 0)

	blocks.append(imgLoader)

	imgLoader = ImageSprite(config)
	imgLoader.debug = True
	imgLoader.action = "pan"
	imgLoader.countLimit = 1
	imgLoader.xOffset = 0
	imgLoader.yOffset = 0
	imgLoader.endX = config.screenWidth
	imgLoader.endY = config.screenHeight + 32
	imgLoader.panRangeLimit = 0 + config.screenWidth
	imgLoader.scrollSpeed = .01
	imgLoader.useJitter =  True
	imgLoader.useBlink = False
	imgLoader.brightnessFactor = .9
	imgLoader.config = config
	imgLoader.iid = "one=>"
	imgLoader.make(path  + imageList[1], 4, 0)
	
	blocks.append(imgLoader)

	imgLoader = ImageSprite(config)
	imgLoader.debug = True
	imgLoader.action = "pan"
	imgLoader.countLimit = 1
	imgLoader.xOffset = 0
	imgLoader.yOffset = 0
	imgLoader.endX = config.screenWidth
	imgLoader.endY = config.screenHeight + 32
	imgLoader.panRangeLimit = 0 + config.screenWidth
	imgLoader.scrollSpeed = .01
	imgLoader.useJitter =  True
	imgLoader.useBlink = False
	imgLoader.brightnessFactor = .9
	imgLoader.config = config
	imgLoader.iid = "one=>"
	imgLoader.make(path  + imageList[1], 3, 0)
	
	blocks.append(imgLoader)

	#if(run) : runWork()

def runWork():
	global blocks, config
	#gc.enable()
	while True:
		iterate()
		time.sleep(config.speed)	

def iterate( n = 0) :
	global config, blocks
	for n in range (0, len(blocks)) :
		block = blocks[n]
		block.update()
		updateCanvasCall = True if n == 0 else True
		config.render(block.image, int(block.x), int(block.y), block.image.size[0], block.image.size[1], False, False, updateCanvasCall)
	#config.render(block.image, int(block.x), int(block.y), block.image.size[0], block.image.size[1], False, False, updateCanvasCall)
		#if(block.setForRemoval==True) : makeBlock()

	# cleanup the list
	#blocks[:] = [block for block in blocks if block.setForRemoval!=True]
	config.updateCanvas()

	if len(blocks) == 0 : exit()

def callBack() :
	global config
	pass











	
#####################


