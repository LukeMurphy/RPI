#!/usr/bin/python
# import modules
# ################################################### #
import datetime
import getopt
import math
import os
import random
import sys
import textwrap
import time
from collections import OrderedDict
from modules.configuration import bcolors
from modules import coloroverlay, colorutils, continuous_scroller,  panelDrawing

from modules.faderclass import FaderObj
from PIL import (
	Image,
	ImageChops,
	ImageDraw,
	ImageEnhance,
	ImageFilter,
	ImageFont,
	ImageOps,
	ImagePalette,
)

global config


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""


def makeBackGround(drawRef, n=1):
	rows = config.patternRows * 1
	cols = config.patternCols * 1

	xDiv = round(
		(config.displayRows * config.canvasWidth) / cols
	)  

	xDiv = (
		2 * config.canvasWidth * config.displayCols/ cols 
	) 

	yDiv = (
		config.patternHeight / rows
	) / config.displayRows 


	gap = 0
	steps = cols
	config.arrowBgBackGroundColor = (0, 0, 0, 20)  # colorutils.getRandomColor()
	colorChange = False

	# Background setup
	'''
	'''
	drawRef.rectangle(
		(0, 0, (round(config.displayRows * config.canvasWidth)), config.canvasHeight),
		fill=config.bgBackGroundColor)

	## The multiplier is actually a factor of the number of rows
	## but, generally so far only using two rows ....
	rDelta = ((config.bgBackGroundEndColor[0] - config.bgBackGroundColor[0]) / steps)
	gDelta = ((config.bgBackGroundEndColor[1] - config.bgBackGroundColor[1]) / steps)
	bDelta = ((config.bgBackGroundEndColor[2] - config.bgBackGroundColor[2]) / steps)

	xPos = 0 
	transitionCount = 0 
	config.patternLengthTransition = 8
	lengthDelta = round((xDiv - config.currentPatternLength ) / config.patternLengthTransition)
	patternLength = xDiv

	for c in range(0, cols):
		columnOffset = 0

		rCol = config.bgBackGroundColor[0] + rDelta
		gCol = config.bgBackGroundColor[1] + gDelta
		bCol = config.bgBackGroundColor[2] + bDelta
		config.bgBackGroundColor = (rCol, gCol, bCol)

		### Because the way the pattern draws the left end is actually the end color
		### so need to reverse the color gradient ....

		fillClr = (
			(round(config.bgBackGroundEndColor[0] - rDelta * (c + 1))),
			(round(config.bgBackGroundEndColor[1] - gDelta * (c + 1))),
			(round(config.bgBackGroundEndColor[2] - bDelta * (c + 1))),
			200,
		)

		w = patternLength

		outline = None
		if c < 0 :
			outline=(255,0,0,200)

		drawRef.rectangle((xPos,0,xPos+w,config.canvasHeight), fill = fillClr, outline=outline)
		xPos += w

		if transitionCount < config.patternLengthTransition-1 : 
			#print(config.currentPatternLength,xDiv,lengthDelta)
			transitionCount += 1
			#patternLength += lengthDelta
		else :
			patternLength = xDiv


	config.bgBackGroundColor = config.bgBackGroundEndColor

	# Foreground setup

	rowMultiplier = 1
	colMultiplier = 1

	if config.pattern == "bricks":
		rowMultiplier = 1
		colMultiplier = 1

	if config.pattern == "regularLines":
		rowMultiplier = 2
		colMultiplier = 1

	if config.pattern == "pluses":
		rowMultiplier = 2
		colMultiplier = 1

	if config.pattern == "diamonds":
		rowMultiplier = 2
		colMultiplier = 2

	
	## The multiplier is actually a factor of the number of rows
	## but, generally so far only using two rows ....
	rDelta = ((config.patternEndColor[0] - config.patternColor[0]) / steps)
	gDelta = ((config.patternEndColor[1] - config.patternColor[1]) / steps)
	bDelta = ((config.patternEndColor[2] - config.patternColor[2]) / steps)

	xPos = 0
	xStart = 0
	yStart = 0
	transitionCount = 0 
	config.patternLengthTransition = 8
	lengthDelta = round((xDiv - config.currentPatternLength ) / config.patternLengthTransition)


	for c in range(0, cols+1):
		
		columnOffset = 0

		rCol = config.patternColor[0] + rDelta
		gCol = config.patternColor[1] + gDelta
		bCol = config.patternColor[2] + bDelta
		config.patternColor = (rCol, gCol, bCol)

		### Because the way the pattern draws the left end is actually the end color
		### so need to reverse the color gradient ....

		fillClr = (
			(round(config.patternEndColor[0] - rDelta * (c + 1))),
			(round(config.patternEndColor[1] - gDelta * (c + 1))),
			(round(config.patternEndColor[2] - bDelta * (c + 1))),
			225,
		)

		if random.random() < .5:

			fillClr = (
				round(random.uniform(0,255) * config.brightness),
				round(random.uniform(0,150) * config.brightness),
				round(random.uniform(0,155) * config.brightness),
				255
					)

		#drawRef.rectangle((0, 0, 0 + 1, config.canvasHeight), fill = None, outline = (255,0,0,255))

		# length transition
		patternLength = xDiv

		for r in range(0, rows):
			columnOffset = 0
			if r == 0 or r == 2 or r == 4 or r == 6:
				columnOffset = xDiv

			if r / 2 % 2 == 0:
				columnOffset = xDiv

			if random.random() < config.patternDrawProb or c == 0:

				if config.pattern == "test":
					drawRef.rectangle((xPos,5,xPos+4,55), fill = fillClr)

				if random.random() < config.redGreenSwapProb: 
					fillClr = (fillClr[1],fillClr[0],fillClr[2])

				if random.random() < config.redBlueSwapProb: 
					fillClr = (fillClr[2],fillClr[1],fillClr[0])

				if random.random() < config.greenBlueSwapProb: 
					fillClr = (fillClr[0],fillClr[2],fillClr[1])

				if config.pattern == "diamonds":
					poly = []
					poly.append((xStart, yStart + yDiv))
					poly.append((xStart + xDiv, yStart))
					poly.append((xStart + xDiv + xDiv, yStart + yDiv))
					poly.append((xStart + xDiv, yStart + yDiv + yDiv))
					drawRef.polygon(poly, fill=fillClr)
					# if(n ==2) : color = (100,200,0,255)

				if config.pattern == "bricks":
					length = xDiv
					#xPos = xStart + columnOffset
					yPos = yStart
					drawRef.rectangle(
						(xPos+ columnOffset, yPos, xPos+ columnOffset + length, yPos + yDiv),
						fill=fillClr,
						outline=None,
					)

				if config.pattern == "pluses":
					length = xDiv
					height = xDiv / 2

					#xPos = xStart + columnOffset
					yPos = yStart

					xPos2 = xPos + round(length / 2 - height / 2)
					yPos2 = round(yPos - length / 2 + height / 2)

					drawRef.rectangle(
						(xPos+ columnOffset, yPos, xPos + length+ columnOffset, yPos + yDiv),
						fill=fillClr,
						outline=None,
					)
					drawRef.rectangle(
						(xPos2, yPos2, xPos2 + height, yPos2 + length),
						fill=fillClr,
						outline=None,
					)
		
				if config.pattern == "regularLines":
					length = patternLength
					#xPos = xStart + columnOffset
					yPos = yStart
					drawRef.rectangle((xPos+ columnOffset, yPos, xPos + length+ columnOffset, yPos + yDiv), fill = fillClr)

				
				if config.pattern == "lines":
					# if (r%2 > 0):
					length = int(round(random.uniform(1, 2 * xDiv)))
					offset = int(round(random.uniform(0, 4 * xDiv)))

					if random.random() < 0.5:
						drawRef.rectangle(
							(xStart, yStart, xStart + 2 * xDiv, yStart + yDiv),
							fill=fillClr,
							outline=None,
						)
					else:
						drawRef.rectangle(
							(
								xStart + offset,
								yStart,
								xStart + length + offset,
								yStart + yDiv,
							),
							fill=fillClr,
							outline=None,
						)

				
			yStart += rowMultiplier * yDiv

		if transitionCount < config.patternLengthTransition-1 : 
			#print(config.currentPatternLength,xDiv,lengthDelta)
			transitionCount += 1
			#patternLength += lengthDelta
		else :
			config.currentPatternLength = xDiv

		
		if config.pattern == "lines":
			xStart += colMultiplier * xDiv
		else:
			xStart += xDiv * 2
		xPos += xDiv
		yStart = 0

	config.patternColor = config.patternEndColor
	config.currentPatternLength = xDiv


## Layer imagery callbacks & regeneration functions
def remakePatternBlock(imageRef, direction):

	
	if config.alwaysRandomPattern == True :
		if random.random() < .15:
			config.patternDrawProb = random.uniform(config.minDrawProb, config.maxDrawProb)

		if random.random() < .15:
			config.patternRows = (round(random.uniform(config.minPatternRows, config.maxPatternRows)))

		if random.random() < .15:
			config.patternCols = (round(random.uniform(config.minPatternCols, config.maxPatternCols)))

		if random.random() < .15:
			choice = round(random.uniform(0,len(config.choiceArray)-1))
			config.pattern = config.choiceArray[choice]

	else :
		config.pattern == config.initialPattern 


	config.patternColor = config.patternEndColor
	if random.random() < config.backgroundColorChangeProb :
		config.patternEndColor = colorutils.getRandomColorHSV(
				config.fg_minHue, config.fg_maxHue, 
				config.fg_minSaturation, config.fg_maxSaturation, 
				config.fg_minValue, config.fg_maxValue,
				config.fg_dropHueMinValue, config.fg_dropHueMaxValue, 255, config.brightness)


	config.bgBackGroundColor = config.bgBackGroundEndColor
	if random.random() < config.backgroundColorChangeProb :
		config.bgBackGroundEndColor = colorutils.getRandomColorHSV(
				config.bg_minHue, config.bg_maxHue, 
				config.bg_minSaturation, config.bg_maxSaturation, 
				config.bg_minValue, config.bg_maxValue,
				config.bg_dropHueMinValue, config.bg_dropHueMaxValue,255,config.brightness)


	drawRef = ImageDraw.Draw(imageRef)
	makeBackGround(drawRef, direction)


## Setup and run functions
def configureBackgroundScrolling():
	print("configureBackgroundScrolling")
	config.patternRows = int(workConfig.get("scroller", "patternRows"))
	config.patternCols = int(workConfig.get("scroller", "patternCols"))

	config.patternDrawProb = float(workConfig.get("scroller", "patternDrawProb"))
	config.patternSpeed = float(workConfig.get("scroller", "patternSpeed"))
	config.pattern = workConfig.get("scroller", "pattern")
	config.initialPattern  = workConfig.get("scroller", "pattern")
	config.choiceArray = ["lines","pluses","regularLines","regularLines"]


	config.bgBackGroundColor = colorutils.getRandomColorHSV(
			config.bg_minHue, config.bg_maxHue, 
			config.bg_minSaturation, config.bg_maxSaturation, 
			config.bg_minValue, config.bg_maxValue,
			config.bg_dropHueMinValue, config.bg_dropHueMaxValue, 255, config.brightness)

	config.bgBackGroundEndColor = colorutils.getRandomColorHSV(
			config.bg_minHue, config.bg_maxHue, 
			config.bg_minSaturation, config.bg_maxSaturation, 
			config.bg_minValue, config.bg_maxValue,
			config.bg_dropHueMinValue, config.bg_dropHueMaxValue, 255, config.brightness)

	config.patternColor = colorutils.getRandomColorHSV(
			config.fg_minHue, config.fg_maxHue, 
			config.fg_minSaturation, config.fg_maxSaturation, 
			config.fg_minValue, config.fg_maxValue,0,0,255,config.brightness)		

	config.patternEndColor = colorutils.getRandomColorHSV(
			config.fg_minHue, config.fg_maxHue, 
			config.fg_minSaturation, config.fg_maxSaturation, 
			config.fg_minValue, config.fg_maxValue,
			config.fg_dropHueMinValue, config.fg_dropHueMaxValue, 255, config.brightness)


		
	config.currentPatternLength = 0

	config.scroller4 = continuous_scroller.ScrollObject()
	scrollerRef = config.scroller4
	scrollerRef.typeOfScroller = "bg"
	scrollerRef.canvasWidth = int(config.displayRows * config.canvasWidth)
	scrollerRef.xSpeed = config.patternSpeed
	scrollerRef.setUp()
	direction = 1 if scrollerRef.xSpeed > 0 else -1
	scrollerRef.callBack = {"func": remakePatternBlock, "direction": direction}
	

	try:
		config.maxSpeed = float(workConfig.get("scroller", "maxSpeed"))
	except Exception as e:
		config.maxSpeed = config.patternSpeed
	
	scrollerRef.xMaxSpeed = config.maxSpeed

	try:
		config.changeProb = float(workConfig.get("scroller", "changeProb"))
	except Exception as e:
		config.changeProb = 0.0
		print(str(e))

	try:
		config.changeProbReleaseFactor = float(workConfig.get("scroller", "changeProbReleaseFactor"))
	except Exception as e:
		config.changeProbReleaseFactor = 1.0
		print(str(e))


	makeBackGround(scrollerRef.bg1Draw, 1)
	makeBackGround(scrollerRef.bg2Draw, 1)


	config.t1 = time.time()
	config.t2 = time.time()
	config.timeToComplete = 1
	config.scrollerPauseBool = False

	config.scrollArray.append(scrollerRef)


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""



def init():
	global config

	print("SINGLETON SCROLLER HOLDER INIT")

	config.redrawSpeed = float(workConfig.get("scroller", "redrawSpeed"))

	config.windowWidth = float(workConfig.get("displayconfig", "windowWidth"))
	config.windowHeight = float(workConfig.get("displayconfig", "windowHeight"))


	config.displayRows = int(workConfig.get("scroller", "displayRows"))
	config.displayCols = int(workConfig.get("scroller", "displayCols"))

	# ********* HARD CODING VALUES  ***********************
	try:
		config.patternHeight = int(workConfig.get("scroller", "patternHeight"))
	except Exception as e:
		print(str(e))
		config.patternHeight = config.canvasHeight
	config.bandHeight = int(round(config.patternHeight / config.displayRows))
	config.bgBackGroundColor = (0, 0, 0, 0)
	config.arrowBgBackGroundColor = (0, 0, 0, 200)

	config.canvasImage = Image.new(
		"RGBA", (config.canvasWidth * 10, config.canvasHeight)
	)
	config.canvasImageDraw = ImageDraw.Draw(config.canvasImage)

	config.imageLayer = Image.new(
		"RGBA", (config.canvasWidth * 10, config.canvasHeight)
	)
	config.imageLayerDraw = ImageDraw.Draw(config.canvasImage)

	config.workImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.workImageDraw = ImageDraw.Draw(config.workImage)

	config.overallBlur = float(
		workConfig.get("scroller", "overallBlur", vars=0, fallback=0)
	)

	config.flip = False
	config.scrollArray = []

	## Set up the scrolling layer

	try:
		config.backgroundColorChangeProb = float(workConfig.get("scroller", "backgroundColorChangeProb"))
	except Exception as e:
		print(str(e))
		config.backgroundColorChangeProb = .5


	try:
		config.setPatternColor = workConfig.getboolean("scroller", "setPatternColor")
		config.setPatternEndColor = list(map(lambda x: int(x), workConfig.get("scroller", "setPatternEndColor").split(",")))
	except Exception as e:
		config.setPatternColor = False
		print(str(e))

	config.altDirectionScrolling = workConfig.getboolean(
		"scroller", "altDirectionScrolling"
	)
	config.alwaysRandomPatternColor = workConfig.getboolean(
		"scroller", "alwaysRandomPatternColor"
	)
	config.alwaysRandomPattern = workConfig.getboolean(
		"scroller", "alwaysRandomPattern"
	)

	config.maxPatternRows = int(workConfig.get("scroller", "maxPatternRows"))
	config.maxPatternCols = int(workConfig.get("scroller", "maxPatternCols"))
	config.minPatternRows = int(workConfig.get("scroller", "minPatternRows"))
	config.minPatternCols = int(workConfig.get("scroller", "minPatternCols"))
	config.maxDrawProb = float(workConfig.get("scroller", "maxDrawProb"))
	config.minDrawProb = float(workConfig.get("scroller", "minDrawProb"))


	config.fg_minHue = int(workConfig.get("scroller", "fg_minHue"))
	config.fg_maxHue = int(workConfig.get("scroller", "fg_maxHue"))
	config.fg_minSaturation = float(workConfig.get("scroller", "fg_minSaturation"))
	config.fg_maxSaturation = float(workConfig.get("scroller", "fg_maxSaturation"))
	config.fg_minValue = float(workConfig.get("scroller", "fg_minValue"))
	config.fg_maxValue = float(workConfig.get("scroller", "fg_maxValue"))


	config.bg_minHue = int(workConfig.get("scroller", "bg_minHue"))
	config.bg_maxHue = int(workConfig.get("scroller", "bg_maxHue"))
	config.bg_minSaturation = float(workConfig.get("scroller", "bg_minSaturation"))
	config.bg_maxSaturation = float(workConfig.get("scroller", "bg_maxSaturation"))
	config.bg_minValue = float(workConfig.get("scroller", "bg_minValue"))
	config.bg_maxValue = float(workConfig.get("scroller", "bg_maxValue"))


	try:
		config.redGreenSwapProb = float(workConfig.get("scroller", "redGreenSwapProb"))
	except Exception as e:
		print(str(e))
		config.redGreenSwapProb = 0
	try:
		config.redBlueSwapProb = float(workConfig.get("scroller", "redBlueSwapProb"))
	except Exception as e:
		print(str(e))
		config.redBlueSwapProb = 0
	try:
		config.greenBlueSwapProb = float(workConfig.get("scroller", "greenBlueSwapProb"))
	except Exception as e:
		print(str(e))
		config.greenBlueSwapProb = 0

	try:
		config.bg_dropHueMinValue = float(workConfig.get("scroller", "bg_dropHueMinValue"))
		config.bg_dropHueMaxValue = float(workConfig.get("scroller", "bg_dropHueMaxValue"))
		config.fg_dropHueMinValue = float(workConfig.get("scroller", "fg_dropHueMinValue"))
		config.fg_dropHueMaxValue = float(workConfig.get("scroller", "fg_dropHueMaxValue"))		
	except Exception as e:
		config.bg_dropHueMinValue = 0
		config.bg_dropHueMaxValue = 0
		config.fg_dropHueMinValue = 0
		config.fg_dropHueMaxValue = 0
		print(str(e))


	configureBackgroundScrolling()


	try:
		config.useOverLayImage = workConfig.getboolean("scroller", "useOverLayImage")
		if config.useOverLayImage == True:
			configureImageOverlay()
	except Exception as e:
		config.useOverLayImage = False
		print(str(e))


	try:
		config.useUltraSlowSpeed = workConfig.getboolean(
			"scroller", "useUltraSlowSpeed"
		)
	except Exception as e:
		config.useUltraSlowSpeed = False
		print(str(e))



	try:
		config.doingRefreshCount = float(
			workConfig.get("scroller", "doingRefreshCount")
		)
	except Exception as e:
		config.doingRefreshCount = 50
		print(str(e))


	### THIS IS USED AS WAY TO MOCKUP A CONFIGURATION OF RECTANGULAR PANELS
	panelDrawing.mockupBlock(config, workConfig)
	''' 
		########### Need to add something like this at final render call  as well
			
		########### RENDERING AS A MOCKUP OR AS REAL ###########
		if config.useDrawingPoints == True :
			config.panelDrawing.canvasToUse = config.renderImageFull
			config.panelDrawing.render()
		else :
			#config.render(config.canvasImage, 0, 0, config.canvasWidth, config.canvasHeight)
			#config.render(config.image, 0, 0)
			config.render(config.renderImageFull, 0, 0)
	'''



	config.f = FaderObj()
	config.f.setUp(config.renderImageFull, config.workImage)
	config.f.doingRefreshCount = config.doingRefreshCount
	# config.workImageDraw.rectangle((0,0,100,100), fill=(100,0,0,100))
	config.renderImageFullOld = config.renderImageFull.copy()
	config.fadingDone = True

	config.useFadeThruAnimation = True
	config.deltaTimeDone = True


def runWork():
	global config
	print(bcolors.OKGREEN + "** " + bcolors.BOLD)
	print("RUNNING Scroller Holder scroller-holder.py")
	print(bcolors.ENDC)
	while 1==1 :
		if config.isRunning == True: iterate()
		time.sleep(config.redrawSpeed)
		if config.standAlone == False :
			config.callBack()


def checkTime(scrollerObj):
	config.t2 = time.time()
	delta = config.t2 - config.t1

	if delta > config.timeToComplete and config.deltaTimeDone == False:

		scrollerObj.xSpeed -= 0.2

		if scrollerObj.xSpeed <= 0.70:
			config.deltaTimeDone = True
			config.useFadeThruAnimation = True
			config.f.fadingDone = True

			# print ("DELTA TIME UP")
			processImageForScrolling()
			if config.useUltraSlowSpeed == True:
				scrollerObj.xSpeed = 1


def processImageForScrolling():
	## Run through each of the objects being scrolled - text, image, background etc
	for scrollerObj in config.scrollArray:
		scrollerObj.scroll()
		config.canvasImage.paste(scrollerObj.canvas, (0, 0), scrollerObj.canvas)

	# Chop up the scrollImage into "rows"
	for n in range(0, config.displayRows):
		segment = config.canvasImage.crop(
			(
				n * config.canvasWidth,
				0,
				config.canvasWidth + n * config.canvasWidth,
				config.bandHeight,
			)
		)

		if (
			(n % 2 == 0)
			and (config.displayRows > 1)
			and config.altDirectionScrolling == True
		):
			segment = ImageOps.flip(segment)
			segment = ImageOps.mirror(segment)

		config.workImage.paste(segment, (0, n * config.bandHeight))

	if config.useOverLayImage == True:
		if random.random() < config.overlayGlitchRate:
			glitchBox(
				config.loadedImage, -config.overlayGlitchSize, config.overlayGlitchSize
			)
		if random.random() < config.overlayResetRate:
			config.loadedImage.paste(config.loadedImageCopy)
		config.workImage.paste(
			config.loadedImage,
			(config.overLayXPos, config.overLayYPos),
			config.loadedImage,
		)

	if config.overallBlur != 0:
		config.workImage = config.workImage.filter(
			ImageFilter.GaussianBlur(radius=config.overallBlur)
		)


def iterate():
	global config

	# config.workImageDraw.rectangle((0,0,config.canvasWidth,config.canvasHeight), fill  = (0,0,0))
	# config.canvasImageDraw.rectangle((0,0,config.canvasWidth*10,config.canvasHeight), fill  = (0,0,0,20))

	for scrollerObj in config.scrollArray:
		if scrollerObj.typeOfScroller == "bg":
			if (
				random.random() < config.changeProb * config.changeProbReleaseFactor
				and config.deltaTimeDone == True
				and config.useFadeThruAnimation == True
			):
				config.useFadeThruAnimation = False
				scrollerObj.xSpeed = random.uniform(0.6, scrollerObj.xMaxSpeed)
				config.deltaTimeDone = False
				config.t1 = time.time()
				config.timeToComplete = random.uniform(3, 10)
			checkTime(scrollerObj)

	if config.useFadeThruAnimation == True and config.useUltraSlowSpeed == True:
		if config.f.fadingDone == True:

			config.renderImageFullOld = config.renderImageFull.copy()
			config.renderImageFull.paste(
				config.workImage,
				(config.imageXOffset, config.imageYOffset),
				config.workImage,
			)
			config.f.xPos = config.imageXOffset
			config.f.yPos = config.imageYOffset
			# config.renderImageFull = config.renderImageFull.convert("RGBA")
			# renderImageFull = renderImageFull.convert("RGBA")
			config.f.setUp(
				config.renderImageFullOld.convert("RGBA"),
				config.workImage.convert("RGBA"),
			)
			processImageForScrolling()

		config.f.fadeIn()
		config.render(config.f.blendedImage, 0, 0)

	else:
		processImageForScrolling()
		config.renderImageFull.paste(
			config.workImage,
			(config.imageXOffset, config.imageYOffset),
			config.workImage,
		)

		# RENDERING AS A MOCKUP OR AS REAL
		if config.useDrawingPoints == True :
			config.panelDrawing.canvasToUse = config.renderImageFull
			config.panelDrawing.render()
		else :
			#config.render(config.canvasImage, 0, 0, config.canvasWidth, config.canvasHeight)
			#config.render(config.image, 0, 0)
			config.render(config.renderImageFull, 0, 0)


def main(run=True):
	global config, threads, thrd
	init()

	if run:
		runWork()


### Kick off .......
if __name__ == "__main__":
	__main__()