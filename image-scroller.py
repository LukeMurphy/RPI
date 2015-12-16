#!/usr/bin/python

#import modules

from modules import utils, actions,machine,scroll,user,bluescreen ,loader, squares
import Image
import ImageDraw
import time
import random
from rgbmatrix import Adafruit_RGBmatrix
import datetime
import ImageFont
import textwrap
import math
import sys, getopt, os
import ConfigParser, io

# ################################################### #

baseconfig = ConfigParser.ConfigParser()
baseconfig.read('/home/pi/RPI/config.cfg')

config = utils
config.matrix = Adafruit_RGBmatrix(32, int(baseconfig.get("config", 'matrixTiles')))
config.screenHeight = int(baseconfig.get("config", 'screenHeight'))
config.screenWidth =  int(baseconfig.get("config", 'screenWidth'))
config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
config.draw = ImageDraw.Draw(config.image)

config.Image = Image
config.ImageDraw = ImageDraw
config.ImageFont = ImageFont
iid = config.image.im.id
config.matrix.SetImage(iid, 0, 0)
config.tileSize = (int(baseconfig.get("config", 'tileSizeHeight')),int(baseconfig.get("config", 'tileSizeWidth')))
config.rows = int(baseconfig.get("config", 'rows'))
config.cols = int(baseconfig.get("config", 'cols'))

config.actualScreenWidth  = int(baseconfig.get("config", 'actualScreenWidth'))
config.useMassager = bool(baseconfig.getboolean("config", 'useMassager'))
config.renderImage = Image.new("RGBA", (config.actualScreenWidth, 32))
config.brightness =  float(baseconfig.get("config", 'brightness'))
config.path = baseconfig.get("config", 'path')

action = actions
actions.drawBlanksFlag = False
action.config = config
# This is so not good .. so much for avoiding OOP ....
config.actions =  actions

imgLoader = loader
imgLoader.config = config


# ################################################### #


def seq() :
	global group, groups
	global action, scroll, machine, bluescreen, user, imgLoader, concentric, signage
	
	# Get all files in the drawing folder
	path = config.path  + "/imgs/drawings"
	rawList = os.listdir(path)
	imageList = []
	seq = 1

	for f in rawList :
		if os.path.isfile(os.path.join(path, f)) and not f.startswith("._") and not f.startswith(".") :
			imageList.append(f)

	args = sys.argv

	if(len(args) > 1):
		seq =  int(args[2])
		#if(len(args) > 2) : options = args[2]
		#if(len(args) > 3) : options2 = args[3]
		#if(len(args) > 4) : options3 = args[4]

	while True:

		if (seq == 1) :
			imageList = ['plane-2b.gif','paletter3c.gif'] 
			imgLoader.debug = False
			imgLoader.action = "pan"
			imgLoader.countLimit = 1
			imgLoader.xOffset =  0
			imgLoader.yOffset = 0
			imgLoader.panRangeLimit = 0 + config.screenWidth
			imgLoader.scrollSpeed = .01
			imgLoader.useJitter =  True
			imgLoader.useBlink = True
			imgLoader.start(config.path  + "/imgs/" + imageList[0], 1 , 0)

		if (seq == 2) :
			imageList = ['plane-2b.gif','paletter3c.gif'] 
			imgLoader.debug = False
			imgLoader.action = "play"
			imgLoader.countLimit = 5
			imgLoader.gifPlaySpeed = .08
			imgLoader.brightnessFactor  = .2
			imgLoader.brightnessFlux = True
			imgLoader.xOffset =  0
			imgLoader.yOffset = 0
			imgLoader.panRangeLimit = 0 + config.screenWidth
			imgLoader.scrollSpeed = .01
			imgLoader.useJitter =  True
			imgLoader.useBlink = True
			imgLoader.start(config.path  + "/imgs/"  + imageList[1], 0 , 0)

		if(seq == 3) :
			imgLoader.debug = False
			imgLoader.action = "pan"
			imgLoader.countLimit = 2
			imgLoader.xOffset =  0
			imgLoader.yOffset = 0
			imgLoader.panRangeLimit = 0 #+ config.screenWidth
			imgLoader.scrollSpeed = .01
			imgLoader.countLimit = 1
			imgLoader.resizeToWidth = True
			img = int(random.random() *  len(imageList))
			imgLoader.start(path + "/" + imageList[img], 0, -1)

seq()


