#!/usr/bin/python
#import modules
from modules import utils, configuration, colorutils
from modules.imagesprite import ImageSprite
from configs import localconfig

from PIL import Image, ImageDraw, ImageMath, ImageEnhance, ImageFont
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


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def main(run = True) :
	global config, workConfig, blocks, simulBlocks, bads
	gc.enable()

	print("Screensaver Loaded")
	config.imageToLoad = (workConfig.get("images", 'i1'))
	config.playSpeed = float(workConfig.get("images", 'playspeed'))
	config.fontSize = int(workConfig.get("txtdisplay", 'fontSize'))

	config.xbuffer = int(workConfig.get("txtdisplay", 'xbuffer'))
	config.ybuffer = int(workConfig.get("txtdisplay", 'ybuffer'))

	config.xMin = int(workConfig.get("txtdisplay", 'xMin'))
	config.yMin = int(workConfig.get("txtdisplay", 'yMin'))

	config.xMax = int(workConfig.get("txtdisplay", 'xMax'))
	config.yMax = int(workConfig.get("txtdisplay", 'yMax'))

	config.txtBoxHtMultuiplier = float(workConfig.get("txtdisplay", 'txtBoxHtMultuiplier'))
	config.txtStringL1 = (workConfig.get("txtdisplay", 'txt1'))
	config.txtStringL2 = (workConfig.get("txtdisplay", 'txt2'))
	config.txtStringL3 = (workConfig.get("txtdisplay", 'txt3'))

	config.xPos  =  0
	config.yPos = 0
	config.vx = 2
	config.vy = 1

	path = config.path  + "/assets/imgs/"
	imageList = [config.imageToLoad] 

	config.renderImage = Image.new("RGBA", (128, 128))
	config.renderDraw = ImageDraw.Draw(config.renderImage)
	config.textImage = Image.new("RGBA", (128, 128))
	config.textDraw = ImageDraw.Draw(config.textImage)
	
	config.iconImage = Image.open((path + imageList[0]) , "r")
	config.iconImage.load()
	config.iconImage = config.iconImage.resize((48,48))
	config.iconImage = config.iconImage.rotate(90,expand=True)
	config.iconImageHeight =  config.iconImage.getbbox()[3]


	# Setting 2 fonts - one for the main text and the other for its "border"... not really necessary
	config.font1 = ImageFont.truetype(config.path + '/assets/fonts/freefont/FreeSerifBold.ttf',config.fontSize )
	config.font2 = ImageFont.truetype(config.path + '/assets/fonts/freefont/Comic Sans MS Bold.ttf',config.fontSize )
	config.font3 = ImageFont.truetype(config.path + '/assets/fonts/freefont/FreeSansBold.ttf',config.fontSize )
	config.pixLen = config.textDraw.textsize(config.txtStringL1, font = config.font2)

	print(config.pixLen)

	config.txtColor = (255,200,0)
	config.txtBoxWd = config.pixLen[0]
	config.txtBoxHt = config.pixLen[1] * config.txtBoxHtMultuiplier

	###### These will be "reversed" if the images are rotated - e.g. verical screen
	'''
	config.xbuffer = config.pixLen[1]
	config.ybuffer = config.pixLen[1] * 4

	config.yMin = -32
	config.yMax = config.screenHeight - config.pixLen[0]/2
	
	config.xMin = -38
	config.xMax = config.screenWidth  - config.pixLen[1]
	'''

	if(run) : runWork()

def runWork():
	global blocks, config, bads
	#gc.enable()
	while True:
		iterate()
		time.sleep(config.playSpeed)	

def randomizeVelocities() :
	if(random.random() > .5): config.vx = int(5 * random.random())
	if(random.random() > .5): config.vy = int(5 * random.random())
	

def iterate( n = 0) :
	global config

	config.xPos += config.vx
	config.yPos += config.vy


	if(random.random() > .98) : config.txtColor = colorutils.getRandomRGB()

	if(config.vx == 0 and config.vy == 0) : randomizeVelocities() 
	change = False

	if (config.xPos + config.xbuffer  > config.xMax ):
		config.vx = config.vx * -1
		config.xPos = config.xMax - config.xbuffer
		change = True

	if (config.xPos  <  config.xMin ):
		config.vx = config.vx * -1
		config.xPos = config.xMin
		change = True

	if (config.yPos + config.ybuffer > config.yMax ):
		config.vy = config.vy * -1
		config.yPos = config.yMax - config.ybuffer
		change = True

	if(config.yPos < config.yMin ):
		config.vy = config.vy * -1
		config.yPos = config.yMin
		change = True
		
	
	if (change == True):
		randomizeVelocities() 
		config.txtColor = colorutils.getRandomRGB()
		config.txtColor = colorutils.randomColor()
		if(random.random() > .95) : redrawBackGround() 




	###### the higher the alpha value, the less messy the trails are - more black 
	config.textDraw.rectangle((0,32,config.txtBoxWd,config.txtBoxHt), fill=(0,0,0,120))

	#config.textDraw.text((3,0), str(config.xPos), (255,200,0,200), font=config.font2)
	#config.textDraw.text((29,0), str(config.yPos), (255,200,200), font=config.font2)

	fontToUse = config.font2

	config.textDraw.text((1,32), config.txtStringL1, (0,0,0), font=fontToUse)
	config.textDraw.text((1,46), config.txtStringL2, (0,0,0), font=fontToUse)
	config.textDraw.text((1,56), config.txtStringL3, (0,0,0), font=fontToUse)	

	config.textDraw.text((1,32 + 1), config.txtStringL1, (0,0,0), font=fontToUse)
	config.textDraw.text((1,46 + 1), config.txtStringL2, (0,0,0), font=fontToUse)
	config.textDraw.text((1,56 + 1), config.txtStringL3, (0,0,0), font=fontToUse)	

	config.textDraw.text((0,32 + 1), config.txtStringL1, (0,0,0), font=fontToUse)
	config.textDraw.text((0,46 + 1), config.txtStringL2, (0,0,0), font=fontToUse)
	config.textDraw.text((0,56 + 1), config.txtStringL3, (0,0,0), font=fontToUse)	


	config.textDraw.text((0,32), config.txtStringL1, config.txtColor, font=fontToUse)
	config.textDraw.text((0,46), config.txtStringL2, config.txtColor, font=fontToUse)
	config.textDraw.text((0,56), config.txtStringL3, config.txtColor, font=fontToUse)

	imgText = config.textImage.rotate(90)

	###### Paste in image
	config.renderImage.paste(config.iconImage , (0,60), config.iconImage)
	###### Paste in rotated text
	config.renderImage.paste(imgText, (0,0), imgText)
	
	###### Render the final full image
	config.render(config.renderImage, config.xPos, config.yPos, config.screenWidth, config.screenHeight, False, False)


	config.updateCanvas()



def redrawBackGround() :	
	config.renderDraw.rectangle((0,0,config.screenWidth, config.screenHeight), fill = (0,0,0,10))
	#config.renderDraw.rectangle((0,0,4,2), fill=(255,0,0))
	#if(random.random() > .99) : gc.collect()
	#if(random.random() > .97) : config.renderImageFull = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	return True

def callBack() :
	global config
	pass











	
#####################