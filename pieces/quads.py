#!/usr/bin/python
#import modules
# ################################################### #
#import os, sys, getopt, time, random, math, datetime, textwrap
#import ConfigParser, io
#import importlib 
import numpy
#import threading
#import resource
import random, time
from collections import OrderedDict
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageChops, ImageEnhance
from modules import colorutils, coloroverlay
from modules.makeblocks import makeblockanimals #, makedrawcarcas

global thrd, config

def init() :
	global config
	config.redrawSpeed  = float(workConfig.get("animals", 'redrawSpeed')) 
	config.redrawProbablility  = float(workConfig.get("animals", 'redrawProbablility')) 
	config.xVariance = float(workConfig.get("animals", 'xVariance')) 
	config.flip = workConfig.getboolean("animals", 'flip')
	config.blockWidth = int(workConfig.get("animals", 'blockWidth')) 
	config.carcasBlockWidth = int(workConfig.get("animals", 'carcasBlockWidth')) 
	config.l1Variance = float(workConfig.get("animals", 'l1Variance')) 
	config.carcas_pixSortYOffset = int(workConfig.get("animals", 'carcas_pixSortYOffset')) 
	config.base_pixSortYOffset = int(workConfig.get("animals", 'base_pixSortYOffset')) 
	config.xOffset = int(workConfig.get("animals", 'xOffset')) 
	config.yOffset = int(workConfig.get("animals", 'yOffset')) 
	config.carcasXOffset = int(workConfig.get("animals", 'carcasXOffset')) 
	config.carcasYOffset = int(workConfig.get("animals", 'carcasYOffset')) 
	config.fade = int(workConfig.get("animals", 'fade')) 
	config.redShift = int(workConfig.get("animals", 'redShift')) 
	config.greyLevel = int(workConfig.get("animals", 'greyLevel')) 
	config.bgR = int(workConfig.get("animals", 'bgR')) 
	config.bgG = int(workConfig.get("animals", 'bgG')) 
	config.bgB = int(workConfig.get("animals", 'bgB'))

	config.useColorOverlayTransitions = workConfig.getboolean("animals", 'useColorOverlayTransitions')
	config.applyColorOverlayToFullImage = workConfig.getboolean("animals", 'applyColorOverlayToFullImage')
	config.useScrollingBackGround = workConfig.getboolean("animals", 'useScrollingBackGround')
	config.patternRows = int(workConfig.get("animals", 'patternRows'))
	config.patternCols = int(workConfig.get("animals", 'patternCols'))
	config.patternRowsOffset = int(workConfig.get("animals", 'patternRowsOffset'))
	config.patternColsOffset = int(workConfig.get("animals", 'patternColsOffset'))
	config.bgYStepSpeed = int(workConfig.get("animals", 'bgYStepSpeed'))
	config.bgXStepSpeed = int(workConfig.get("animals", 'bgXStepSpeed'))
	config.alpha = int(workConfig.get("animals", 'alpha'))
	config.pixSortXOffsetVal = config.pixSortXOffset

	config.colorTransitionRangeMin = float(workConfig.get("animals", 'colorTransitionRangeMin')) 
	config.colorTransitionRangeMax = float(workConfig.get("animals", 'colorTransitionRangeMax')) 
	config.angleRotationRange = float(workConfig.get("animals", 'angleRotationRange')) 
	config.pigglyWiggle = int(workConfig.get("animals", 'pigglyWiggle'))
	config.pigglyWiggleVariance = int(workConfig.get("animals", 'pigglyWiggleVariance'))
	#changePigglyWiggle()

	### Piece is made up of three layers
	### the background layer or moving pattern is drawn to the the 	bgImage layer
	### this is placed first into the workImage 
	### then the imageLayer is created with the figure drawn on it and then pasted 
	### onto the workImage to make the the final composited image and that is rendered
	###

	config.imageLayer = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.imageLayerDraw = ImageDraw.Draw(config.imageLayer)
	
	config.bgImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.bgDraw = ImageDraw.Draw(config.bgImage)

	config.workImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.workImageDraw = ImageDraw.Draw(config.workImage)

	config.clrBlock = Image.new(config.workImage.mode, (config.canvasWidth, config.canvasHeight))
	config.clrBlockDraw = ImageDraw.Draw(config.clrBlock)

	## Set up the scrolling background images
	## patternDrawProb creates the gaps in the pattern
	## the pattern is redrawn every time one of the two panels moves off screen
	config.patternDrawProb = float(workConfig.get("animals", 'patternDrawProb')) 

	config.bgBackGroundColor = (workConfig.get("animals", 'bgBackGroundColor').split(","))
	config.bgBackGroundColor = tuple([int(i) for i in config.bgBackGroundColor])

	config.bgForeGroundColor = (workConfig.get("animals", 'bgForeGroundColor').split(","))
	config.bgForeGroundColor = tuple([int(i) for i in config.bgForeGroundColor])

	config.bg1 = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.bg1Draw = ImageDraw.Draw(config.bg1)
	config.bg1Draw.rectangle((0,0,config.canvasWidth, config.canvasHeight), fill = config.bgBackGroundColor)
	makeBackGround(config.bg1Draw, 1)
	
	config.bg2 = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.bg2Draw = ImageDraw.Draw(config.bg2)
	config.bg2Draw.rectangle((0,0,config.canvasWidth, config.canvasHeight), fill = config.bgBackGroundColor)
	makeBackGround(config.bg2Draw, 2)

	config.leadBG = config.bg1
	config.followBG = config.bg2
	config.leadBGDraw = config.bg1Draw
	config.followBGDraw = config.bg2Draw

	config.bgImage.paste(config.bg1)
	config.bgImage.paste(config.bg2,(0,config.canvasHeight))
	config.bgXpos = 0
	config.bgYpos = 0

	### the overlay color affects the background only in this case
	config.colOverlayA = coloroverlay.ColorOverlay()
	### This is the speed range of transitions in color
	### Higher numbers means more possible steps so slower
	### transitions - 1,10 very blinky, 10,200 very slow
	config.colOverlayA.randomRange = (config.colorTransitionRangeMin,config.colorTransitionRangeMax)
	config.colOverlayA.colorA = tuple(int(a*config.brightness) for a in (colorutils.getRandomColor()))

	config.colOverlayA.randomSteps = True 
	config.colOverlayA.timeTrigger = True 
	config.colOverlayA.steps = 100 
	config.colOverlayA.tLimitBase = 30
	config.colOverlayA.maxBrightness = config.brightness
	config.colOverlayA.colorTransitionSetup()

	makeblockanimals.config = config
	makeblockanimals.drawBackGround = drawBackGround
	makeblockanimals.ScaleRotateTranslate = ScaleRotateTranslate

	#makedrawcarcas.config = config
	#makedrawcarcas.ScaleRotateTranslate = ScaleRotateTranslate

def makeBackGround(drawRef, n = 1):
	rows = config.patternRows * 2
	cols = config.patternCols * 2

	xDiv = config.canvasWidth / cols #- config.patternColsOffset
	yDiv = config.canvasHeight / rows #- config.patternRowsOffset

	xStart = 0
	yStart = 0

	drawRef.rectangle((0,0,config.canvasWidth, config.canvasHeight), fill = config.bgBackGroundColor)

	## Chevron pattern
	for r in range (0, rows) : 
		for c in range (0, cols) : 
			poly = []
			poly.append((xStart, yStart + yDiv))
			poly.append((xStart + xDiv, yStart))
			poly.append((xStart + xDiv + xDiv, yStart + yDiv))
			poly.append((xStart + xDiv, yStart + yDiv + yDiv))
			#if(n ==2) : color = (100,200,0,255)
			if(random.random() < config.patternDrawProb) :
				drawRef.polygon(poly, fill = config.bgForeGroundColor) #outline = (15,15,15)
			xStart += 2 * xDiv
		xStart = 0
		yStart += 2 * yDiv

def drawBackGround():
	global config

	#config.workImageDraw.rectangle((0,0,config.canvasWidth,config.canvasHeight), fill=(config.bgR, config.bgG, config.bgB,config.fade))
	config.workImage.paste(config.leadBG, (config.bgXpos,config.bgYpos))
	config.workImage.paste(config.followBG, (config.bgXpos,config.bgYpos - config.canvasHeight))

	if(config.bgYStepSpeed < 0) :
		config.workImage.paste(config.followBG, (config.bgXpos,config.bgYpos + config.canvasHeight))

	if config.applyColorOverlayToFullImage == True :
		config.workImage.paste(config.imageLayer, (0,0), config.imageLayer)

	if(config.useColorOverlayTransitions == True and config.applyColorOverlayToFullImage == False) :
		# Color overlay on b/w PNG sprite
		#clrBlockDraw.rectangle((0,0, config.canvasWidth, config.canvasHeight), fill=(255,255,255))
		config.clrBlockDraw.rectangle(((0,0,config.canvasWidth,config.canvasHeight)), fill=config.fillColorA)
		try :
			config.workImage = ImageChops.multiply(config.clrBlock, config.workImage)

		except Exception as e: 
			print(e, clrBlock.mode, config.renderImageFull.mode)
			pass

	config.bgYpos += config.bgYStepSpeed
	config.bgXpos += config.bgXStepSpeed
	lead = config.leadBG
	leadBGDraw = config.leadBGDraw
	swap = False

	if (config.bgXpos > config.canvasWidth) : 
		config.bgXpos = -config.canvasWidth

	if (config.bgYpos > 1 * config.canvasHeight and config.bgYStepSpeed > 0) : 
		config.workImage.paste(config.leadBG, (config.bgXpos, -1*config.canvasHeight))
		makeBackGround(leadBGDraw)
		swap = True

	if (config.bgYpos < -1 * config.canvasHeight and config.bgYStepSpeed < 0) : 
		config.workImage.paste(config.leadBG, (config.bgXpos, 1*config.canvasHeight))
		makeBackGround(leadBGDraw)
		swap = True

	if(swap == True):
		config.leadBG = config.followBG
		config.followBG = lead

		config.leadBGDraw = config.followBGDraw
		config.followBGDraw = leadBGDraw
		config.bgYpos = 0

def ScaleRotateTranslate(image, angle, center = None, new_center = None, scale = None,expand=False):
	if center is None:
		return image.rotate(angle)
	angle = -angle/180.0*math.pi
	nx,ny = x,y = center
	sx=sy=1.0
	if new_center:
		(nx,ny) = new_center
	if scale:
		(sx,sy) = scale
	cosine = math.cos(angle)
	sine = math.sin(angle)
	a = cosine/sx
	b = sine/sx
	c = x-nx*a-ny*b
	d = -sine/sy
	e = cosine/sy
	f = y-nx*d-ny*e
	return image.transform(image.size, Image.AFFINE, (a,b,c,d,e,f), resample=Image.BICUBIC)

def callBack() :
	global config
	pass

def runWork():
	global config
	while True:
		iterate()
		#time.sleep(.01)
		#time.sleep(random.random() * config.redrawSpeed)
		time.sleep(config.redrawSpeed)

def iterate() :
	global config

	### In each cycle, the color transition is stepped forward and placed on top of the background
	### If the piece uses the scrolling background, the colorOverlayA.currentColor is used 
	config.colOverlayA.stepTransition()
	config.fillColorA = tuple(int (a * config.brightness ) for a in config.colOverlayA.currentColor)

	if(config.useScrollingBackGround == False):
		if(config.useColorOverlayTransitions == True) :
			config.workImageDraw.rectangle((0,0,config.canvasWidth,config.canvasHeight), fill=config.fillColorA)
		else :
			config.workImageDraw.rectangle((0,0,config.canvasWidth,config.canvasHeight), fill=(config.bgR, config.bgG, config.bgB,config.fade))
		
		config.workImage.paste(config.imageLayer, (0,0), config.imageLayer)
	else :
		drawBackGround()
	

	#drawCarcas()
	
	if(random.random() < .01) :
		config.pixSortprobDraw = random.uniform(0,.01)
	

	if(random.random() < .5) :
		config.pixSortYOffset = config.base_pixSortYOffset
		#print("Animal")
		makeblockanimals.makeAnimal()
	else :
		config.pixSortYOffset = config.carcas_pixSortYOffset
		#print("Carcass")
		makeblockanimals.makeCarcas()

	if(config.useColorOverlayTransitions == True and config.applyColorOverlayToFullImage == True) :
		# Color overlay on b/w PNG sprite
		#clrBlockDraw.rectangle((0,0, config.canvasWidth, config.canvasHeight), fill=(255,255,255))
		config.clrBlockDraw.rectangle(((0,0,config.canvasWidth,config.canvasHeight)), fill=config.fillColorA)
		try :
			config.workImage = ImageChops.multiply(config.clrBlock, config.workImage)

		except Exception as e: 
			print(e, clrBlock.mode, config.renderImageFull.mode)
			pass
	else :
		config.workImage.paste(config.imageLayer, (0,0), config.imageLayer)


	config.render(config.workImage, 0,0)

def main(run = True) :
	global config, threads, thrd
	init()
	
	if(run) : runWork()

### Kick off .......
if __name__ == "__main__":
	__main__()