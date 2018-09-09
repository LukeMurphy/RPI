#!/usr/bin/python
#import modules
from modules import configuration, colorutils
from modules.imagesprite import ImageSprite
#from configs import localconfig

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
#import ConfigParser, io
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
	
	## Often the presentation is on a set of panels or screen that is sideways
	## so that the whole piece needs to be rotated - so the orientation of the 
	## display may mean the work has to be also oriented that way
	

	config.windowOrientation = (workConfig.get("txtdisplay", 'windowOrientation'))
	

	config.xbuffer = int(workConfig.get("txtdisplay", 'xbuffer'))
	config.ybuffer = int(workConfig.get("txtdisplay", 'ybuffer'))

	config.xMin = int(workConfig.get("txtdisplay", 'xMin'))
	config.yMin = int(workConfig.get("txtdisplay", 'yMin'))

	config.xMax = int(workConfig.get("txtdisplay", 'xMax'))
	config.yMax = int(workConfig.get("txtdisplay", 'yMax'))

	config.crawlHeight = int(workConfig.get("txtdisplay", 'crawlHeight'))
	config.crawlPositionX = int(workConfig.get("txtdisplay", 'crawlPositionX'))
	config.crawlPositionY = int(workConfig.get("txtdisplay", 'crawlPositionY'))
	config.crawlRepeatDistanceFactor = float(workConfig.get("txtdisplay", 'crawlRepeatDistanceFactor'))

	config.txtBoxHtMultuiplier = float(workConfig.get("txtdisplay", 'txtBoxHtMultuiplier'))
	config.txtStringL1 = (workConfig.get("txtdisplay", 'txt1')).replace("'","")
	config.txtStringL2 = (workConfig.get("txtdisplay", 'txt2')).replace("'","")
	config.txtStringL3 = (workConfig.get("txtdisplay", 'txt3')).replace("'","")
	config.crawlText = (workConfig.get("txtdisplay", 'crawlText'))

	fontColor1 = workConfig.get("txtdisplay", 'fontColor1').split(",")
	config.fontColor1 = tuple([int(i) for i in fontColor1])
	fontColor2 = workConfig.get("txtdisplay", 'fontColor2').split(",")
	config.fontColor2 = tuple([int(i) for i in fontColor2])
	fontColor3 = workConfig.get("txtdisplay", 'fontColor3').split(",")
	config.fontColor3 = tuple([int(i) for i in fontColor3])	
	txtBackgroundColor = workConfig.get("txtdisplay", 'txtBackgroundColor').split(",")
	config.txtBackgroundColor = tuple([int(i) for i in txtBackgroundColor])
	backgroundColor = workConfig.get("txtdisplay", 'backgroundColor').split(",")
	config.backgroundColor = tuple([int(i) for i in backgroundColor])


	config.xPos  =  0
	config.yPos = 0
	config.vx = 0
	config.vy = 0

	config.crawlPosx = 0 
	config.crawlPosy = 0 
	
	config.imageXOffset = 0
	config.imageYOffset = 0

	path = config.path  + "/assets/imgs/"
	imageList = [config.imageToLoad] 

	dim1 = config.screenWidth
	dim2 = config.screenHeight

	if(config.screenWidth > config.screenHeight) : 
		config.screenHeight = config.screenWidth
	else : 
		config.screenWidth = config.screenHeight


	config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	config.draw = ImageDraw.Draw(config.image)

	config.renderImage = Image.new("RGBA", (128, 128))
	config.renderDraw = ImageDraw.Draw(config.renderImage)

	config.textImage = Image.new("RGBA", (128, 128))
	config.textDraw = ImageDraw.Draw(config.textImage)

	config.textCrawl = Image.new("RGBA", (config.screenHeight, config.screenHeight))
	config.crawlDraw = ImageDraw.Draw(config.textCrawl)
	
	config.iconImage = Image.open((path + imageList[0]) , "r")
	config.iconImage.load()
	
	#config.iconImage = config.iconImage.resize((48,48))

	config.iconImageHeight =  config.iconImage.getbbox()[3]


	# Setting 2 fonts - one for the main text and the other for its "border"... not really necessary
	config.font1 = ImageFont.truetype(config.path + '/assets/fonts/freefont/FreeSerifBold.ttf',config.fontSize )
	config.font2 = ImageFont.truetype(config.path + '/assets/fonts/freefont/ComicSansMSBold.ttf',config.fontSize )
	config.font3 = ImageFont.truetype(config.path + '/assets/fonts/freefont/FreeSansBold.ttf',config.fontSize )
	config.pixLen = config.textDraw.textsize(config.txtStringL1, font = config.font3)

	#print(config.pixLen)

	config.txtColor = (255,200,0)
	config.txtBoxWd = config.pixLen[0] + 10
	config.txtBoxHt = config.pixLen[1] * config.txtBoxHtMultuiplier +2

	config.crawlLen = config.crawlDraw.textsize(config.crawlText, font = config.font3)
	###### These will be "reversed" if the images are rotated - e.g. verical screen
	
	config.xVelocityRange = 2
	config.yVelocityRange = 2
	
	
	
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
	if(random.random() > .5): config.vx = int(config.xVelocityRange * random.random())
	if(random.random() > .5): config.vy = int(config.yVelocityRange * random.random())
	if(random.random() > .95): config.xPos = -32

def iterate( n = 0) :
	global config

	'''
	### pseudo gravity

	if(config.windowOrientation == "horizontal"):
		if(config.vx >= 0) : 
			config.vx += .12
			config.vx *= 1.04
		else :
			config.vx += .12
			config.vx *= .96
	else :
		if(config.vy >= 0) : 
			config.vy += .12
			config.vy *= 1.04
		else :
			config.vy += .12
			config.vy *= .96
	'''

	config.xPos += config.vx
	config.yPos += config.vy


	if(random.random() > .98) : config.txtColor = colorutils.getRandomRGB()

	if(config.vx == 0 and config.vy == 0) : randomizeVelocities() 
	if(config.vy == 0) : randomizeVelocities() 

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
	config.textDraw.rectangle((0,128,config.txtBoxWd,config.txtBoxHt), fill=(0,0,10,10))

	#config.textDraw.text((3,0), str(config.xPos), (255,200,0,200), font=config.font2)
	#config.textDraw.text((29,0), str(config.yPos), (255,200,200), font=config.font2)

	fontToUse = config.font3

	'''
	config.textDraw.text((1,32), config.txtStringL1, (0,0,0), font=fontToUse)
	config.textDraw.text((1,46), config.txtStringL2, (0,0,0), font=fontToUse)
	config.textDraw.text((1,56), config.txtStringL3, (0,0,0), font=fontToUse)	

	config.textDraw.text((1,32 + 1), config.txtStringL1, (0,0,0), font=fontToUse)
	config.textDraw.text((1,46 + 1), config.txtStringL2, (0,0,0), font=fontToUse)
	config.textDraw.text((1,56 + 1), config.txtStringL3, (0,0,0), font=fontToUse)	

	config.textDraw.text((0,32 + 1), config.txtStringL1, (0,0,0), font=fontToUse)
	config.textDraw.text((0,46 + 1), config.txtStringL2, (0,0,0), font=fontToUse)
	config.textDraw.text((0,56 + 1), config.txtStringL3, (0,0,0), font=fontToUse)	
	'''

	config.textDraw.text((0,0), config.txtStringL1, config.txtColor, font=fontToUse)
	config.textDraw.text((0,14), config.txtStringL2, config.txtColor, font=fontToUse)
	config.textDraw.text((0,28), config.txtStringL3, config.txtColor, font=fontToUse)


	imgText = config.textImage

	fontToUse = config.font3
	config.crawlDraw.rectangle((0,0,config.screenHeight,config.crawlHeight), fill=config.txtBackgroundColor)
	#config.crawlDraw.text((config.crawlPosx,config.crawlPosy + 1), config.crawlText, (0,0,0), font=fontToUse)
	#config.crawlDraw.text((config.crawlPosx + 1 ,config.crawlPosy), config.crawlText, (0,0,0), font=fontToUse)
	#config.crawlDraw.text((config.crawlPosx + 1,config.crawlPosy + 1), config.crawlText, (0,0,0), font=fontToUse)	
	config.crawlDraw.text((config.crawlPosx, config.crawlPosy), config.crawlText, config.fontColor1, font=fontToUse)
	
	imgCrawl = config.textCrawl
	
	config.crawlPosx -= 1

	if(config.crawlPosx < -config.crawlLen[0] * config.crawlRepeatDistanceFactor) :
		config.crawlPosx = config.screenWidth

	# background fill and fade
	config.draw.rectangle((0, 0, config.screenWidth, config.screenHeight), fill=config.backgroundColor)


	###### Paste in image
	#config.renderImage.paste(config.iconImage , (config.imageXOffset,config.imageYOffset), config.iconImage)
	
	###### Paste in rotated text
	#config.renderImage.paste(imgText, (0,0), imgText)	
	#config.image.paste(config.renderImage, (int(config.xPos), int(config.yPos)), config.renderImage)
	
	###### Paste in crawl
	config.image.paste(imgCrawl,(config.crawlPositionX , config.crawlPositionY), imgCrawl)
	
	###### Render the final full image
	#config.render(config.renderImage, config.xPos, config.yPos, config.screenWidth, config.screenHeight, False, False)

	if (config.windowOrientation == "horizontal"):
		img = config.image.rotate(90, expand=True)
	else:
		img = config.image

	config.render(img, 0, -32, config.screenWidth, config.screenHeight, True, False)

	config.updateCanvas()

def redrawBackGround() :	
	config.renderDraw.rectangle((0,0,config.screenWidth, config.screenHeight), fill = config.backgroundColor)
	#config.renderDraw.rectangle((0,0,4,2), fill=(255,0,0))
	#if(random.random() > .99) : gc.collect()
	#if(random.random() > .97) : config.renderImageFull = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	return True

def callBack() :
	global config
	pass











	
#####################
