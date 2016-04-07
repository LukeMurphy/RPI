#!/usr/bin/python
from modules import utils
#from seqs.dm import dM
import Image
import ImageDraw
import ImageChops
import time
import random
from rgbmatrix import Adafruit_RGBmatrix
import datetime
import ImageFont
import textwrap
import math
import sys, getopt, os
import ConfigParser, io
from subprocess import call
import threading



#matrix = Adafruit_RGBmatrix(32, 12)

image = Image.new("RGBA", (96, 64))
invertedBlock = Image.new("RGBA", (96, 64))
draw  = ImageDraw.Draw(image)
draw2 = ImageDraw.Draw(invertedBlock)
id1 = image.im.id
id2 = invertedBlock.im.id

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
config.transWiring = bool(baseconfig.getboolean("config", 'transWiring'))

config.fontSize = int(baseconfig.get("scroll", 'fontSize'))
config.vOffset = int(baseconfig.get("scroll", 'vOffset'))
config.scrollSpeed = float(baseconfig.get("scroll", 'scrollSpeed'))
config.stroopSpeed = float(baseconfig.get("scroll", 'stroopSpeed'))
config.stroopSteps = float(baseconfig.get("scroll", 'stroopSteps'))

motions = []

def stroop(arg, clr, side = "Left"):
	global config, speed
	fontSize  = 108
	font = ImageFont.truetype(config.path + '/fonts/freefont/FreeSansBold.ttf', fontSize)
	font2 = ImageFont.truetype(config.path + '/fonts/freefont/FreeSansBold.ttf', fontSize)
	pixLen = config.draw.textsize(arg, font = font)

	yOffset = int((pixLen[1] - 26)/4)

	image = Image.new("RGBA", pixLen)
	draw  = ImageDraw.Draw(image)
	clr = tuple(int(a*config.brightness) for a in (clr))

	# If not passed in, make the background the "opposite" color - from the seqs directory
	oppClr  =  config.colorCompliment(clr)
	draw.rectangle((0,0,image.size[0], max(32,pixLen[1])), fill=oppClr)

	# fudged shadow
	draw.text((-1,-1-yOffset),arg,(0,0,0),font=font2)
	draw.text((1,1-yOffset),arg,(0,0,0),font=font2)
	draw.text((0,-yOffset),arg,clr,font=font)
	
	#config.matrix.Clear()
	
	start = 0
	if (side == "Right") : start = config.screenWidth/2
	motions.append([image,0,side,start, config.stroopSteps])
	

def runAnimation(direction="out", stepsSpeed = 1):
	global motions, config
	run = True
	
	dirUnit = 1 * config.stroopSteps
	blockWidth = 1
	blockPos = 0
	blockDir = 1
	panelWidth = config.screenWidth /2
	panelHeight = config.screenHeight
	if (direction == "in") : dirUnit =  -1 * config.stroopSteps

	# need to add each text-image to a single composite
	# but move each side in or out each cycle

	while ( run == True) :
		for i in range(0,2) :
		 
			ref  = motions[i]
			image = ref[0]
			n = ref[1]
			side = ref[2]
			offset = ref[3]
			speed = ref[4]

			if(side == "Left") :
				motions[i][1] = n - dirUnit*config.stroopSteps
				xPos = 0
				xBlock = panelWidth - blockWidth - blockPos*blockDir
			if(side == "Right") :
				motions[i][1] = n + dirUnit*blockDir*config.stroopSteps
				xPos = panelWidth
				xBlock = 0 + blockPos

			# crop and load
			invertedBlock = ImageChops.offset(image,int(n),0)
			invertedBlock = invertedBlock.crop((0,0,panelWidth,panelHeight))
			config.render(invertedBlock,xPos,0,panelWidth,panelHeight,False)

		time.sleep(config.stroopSpeed)
		

# Set up the pair
stroop("  TWO @ ONE TIME  ",[255,255,0],"Left")
stroop(" THINGS OF BEAUTY ",(255,67,0),"Right")


runAnimation("in")

