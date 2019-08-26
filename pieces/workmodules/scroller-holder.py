#!/usr/bin/python
#import modules
# ################################################### #
import os, sys, getopt, time, random, math, datetime, textwrap
from collections import OrderedDict
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageChops, ImageEnhance
from PIL import ImageChops, ImageFilter, ImagePalette
from modules import colorutils, coloroverlay
from pieces.workmodules import continuous_scroller
from pieces.workmodules.faderclass import FaderObj
#global config


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
## Image manipulations

def glitchBox(img, r1 = -10, r2 = 10, dir = "horizontal") :

	apparentWidth = img.size[0]
	apparentHeight = img.size[1]

	dx = round(random.uniform(r1,r2))
	dy = round(random.uniform(r1,r2))
	
	#dx = 0

	sectionWidth = round(random.uniform(2, apparentWidth - dx))
	sectionHeight = round(random.uniform(2, apparentHeight - dy))
	
	#sectionHeight = apparentWidth

	# 95% of the time they dance together as mirrors
	if(random.random() < .97) :
		if(dir  == "horizontal") :
			cp1 = img.crop((0, dy,  apparentWidth, dy + sectionHeight))
		else :
			cp1 = img.crop((dx, 0, dx + sectionWidth, sectionHeight))

		img.paste( cp1, (round(0 + dx), round(0 + dy)))	

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
## Layer imagery
def makeDaemonMessages(config, imageRef, direction = 1):
	#global config

	demonsMale = ["Jealousy", "Wrath", "Tears", "Sighing", "Suffering", "Lamentation", "Bitter Weeping"]
	demonsMaleModifier = ["Jealous", "Wrathful", "Tearful", "Sighing", "Suffering", "Lamenting", "Embittered Weeping"]

	demonsFemale = ["Wrath", "Pain", "Lust", "Sighing", "Cursedness", "Bitterness", "Quarelsomeness"]
	demonsFemaleModifier = ["Wrathful", "Painful", "Lusty", "Sighing", "Cursed", "Bitter", "Quarelsome"]

	angelsMale = ["Unenviousness", "Blessedness", "Joy", "Truth", "Unbegrudgingness", "Belovedness", "Trustworthyness"]
	angelsMaleModifier = ["Unenvious", "Blessed", "Joyful", "True", "Unbegrudging", "Beloved", "Trustworthy"]

	angelsFemale = ["Peace", "Gladness", "Rejoicing", "Blessedness", "Truth", "Love", "Faith"]
	angelsFemaleModifier = ["Peaceful", "Glad", "Rejoicing", "Blessed", "Truthful", "Lovely", "Faithful"]

	maleDemons = [demonsMale, demonsMaleModifier]
	femaleDemons = [demonsFemale, demonsFemaleModifier]
	maleAngels = [angelsMale, angelsMaleModifier]
	femaleAngels = [angelsFemale, angelsFemaleModifier]


	md_fd = [maleDemons, femaleDemons]
	fd_md = [femaleDemons, maleDemons]

	ma_fa = [maleAngels, femaleAngels]
	fa_ma = [femaleAngels, maleAngels]

	md_fa = [maleDemons, femaleAngels]
	fa_md = [femaleAngels, maleDemons]

	ma_fd = [maleAngels, femaleDemons]
	fd_ma = [femaleDemons, maleAngels]


	demonArray = [
	md_fd, 
	md_fa, 
	ma_fd, 
	ma_fa, 
	fd_md, 
	fd_ma,
	fa_md,
	fa_ma
	]

	combination = demonArray[round(math.floor(random.uniform(0, len(demonArray))))]
	arrayToUse = combination[round(math.floor(random.uniform(0, len(combination))))]
	messageString = ""

	if(config.sansSerif) : 
		font = ImageFont.truetype(config.path  + '/assets/fonts/freefont/FreeSansBold.ttf', config.fontSize)
	else :
		font = ImageFont.truetype(config.path  + '/assets/fonts/freefont/FreeSerifBold.ttf', config.fontSize)

	for i in range(0,4) :
		adj = arrayToUse[1][round(math.floor(random.uniform(0,7)))]
		noun = arrayToUse[0][round(math.floor(random.uniform(0,7)))]
		messageString = messageString + adj.upper() + " " + noun.upper() + "           "

	#print(messageString)

	if (random.random() < .15) :
		messageString = ""
		font = ImageFont.truetype(config.path  + '/assets/fonts/freefont/FreeSans.ttf', config.fontSize)
		for i in range(0,23) :
			xo = "X" if (random.random() < .5) else "O"
			messageString = messageString + xo
			messageString = messageString + " " if (random.random() < .5) else messageString


	if(config.colorMode == "getRandomRGB") : clr = colorutils.getRandomRGB(config.brightness)
	if(config.colorMode == "randomColor") : clr = colorutils.randomColor(config.brightness)
	if(config.colorMode == "getRandomColorWheel") : clr = colorutils.getRandomColorWheel(config.brightness)


	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
	# draw the message to get its size


	tempImage = Image.new("RGBA", (1200,196))
	draw  = ImageDraw.Draw(tempImage)


	pixLen = draw.textsize(messageString, font = font)
	# For some reason textsize is not getting full height !
	fontHeight = int(pixLen[1] * 1.3)

	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
	# make a new image with the right size
	scrollImage = Image.new("RGBA", (pixLen[0] + 2 , fontHeight))
	draw  = ImageDraw.Draw(scrollImage)
	iid = scrollImage.im.id

	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
	# Draw the text with "borders"
	indent = int(.05 * config.tileSize[0])
	for i in range(1, config.shadowSize) :
		draw.text((indent + -i,-i),messageString,(0,0,0),font=font)
		draw.text((indent + i,i),messageString,(0,0,0),font=font)

	draw.text((2,0),messageString, clr ,font=font)

	refDraw = ImageDraw.Draw(imageRef)
	refDraw.rectangle((0,0,pixLen[0] + 2 , fontHeight), fill = config.bgBackGroundColor)
	imageRef.paste(scrollImage,(0,config.textVOffest), scrollImage)


def remakeDaemonMessages(imageRef, direction = 1):
	##
	makeDaemonMessages(imageRef=imageRef, direction=direction)


def makeScrollBlock(config, imageRef, imageDrawRef, direction):
	
	#global config
	w = imageRef.size[0]
	#config.enhancer = ImageEnhance.Brightness(config.loadedImage)
	#config.loadedImage = config.enhancer.enhance(config.overlayBrightness)

	widthImage = config.imageBlockImageLoaded.size[0]
	heightImage = config.imageBlockImageLoaded.size[1]
	hBuffer  = config.imageBlockBuffer
	numberOfUnits = int(round(w / (widthImage + hBuffer)))

	for i in range (0,numberOfUnits):
		x = i * ( widthImage + hBuffer)
		y = -5

		tempImage  = config.imageBlockImageLoaded.copy()
		tempEnhancer = ImageEnhance.Brightness(tempImage)
		tempImage = tempEnhancer.enhance(config.brightness)

		clrBlock = Image.new("RGBA", (widthImage, heightImage))
		clrBlockDraw = ImageDraw.Draw(clrBlock)

		# Color overlay on b/w PNG sprite
		# EVERYTHING HAS TO BE PNG  / have ALPHA 
		if (config.useTransparentImages == True) :
			clr = colorutils.randomColorAlpha(brtns = config.brightness, maxTransparency = 200)
		else :
			clr = colorutils.randomColor()
		clrBlockDraw.rectangle((0,0,widthImage, heightImage), fill=clr)

		tempImage = ImageChops.multiply(clrBlock, tempImage)
		imageRef.paste(tempImage,(x,y),tempImage)


def remakeScrollBlock(config, imageRef, direction):
	drawRef = ImageDraw.Draw(imageRef)
	if(random.random() < config.imageBlockRemakeProb) :
		makeScrollBlock(imageRef, drawRef, direction)


def makeArrows(config, drawRef, direction = 1) :

	rows = config.displayCols * 2
	cols = config.arrowCols * 2

	xDiv = round(config.displayRows * config.windowWidth) / cols 
	yDiv = config.canvasHeight / rows 

	xStart = 0 #config.canvasWidth / 2
	yStart = config.bandHeight / 2 #config.canvasHeight / 2

	bufferDistance = 15
	arrowLength = cols * 2
	blade = cols / 3

	clr  = (round(220 * config.brightness),0,0)

	drawRef.rectangle((0,0,round(config.displayRows * config.windowWidth), config.canvasHeight), fill = config.bgBackGroundColor)

	for c in range (0, cols) : 
		yArrowEnd = yStart #yStart + arrowLength
		xArrowEnd = xStart + arrowLength

		# the blades
		xDisplace = xArrowEnd - blade
		yDisplace = blade * math.tan(math.pi/4)
		# the horizontal
		if(random.random() < .5 ) :
			drawRef.line((xStart, yStart, xArrowEnd, yArrowEnd), fill = clr, width = config.lineThickness)

			if direction == 1 :
				drawRef.line((xArrowEnd - blade, yArrowEnd - yDisplace, xArrowEnd, yArrowEnd), fill = clr, width = config.lineThickness)
				drawRef.line((xArrowEnd - blade, yArrowEnd + yDisplace , xArrowEnd, yArrowEnd), fill = clr, width = config.lineThickness)
			else :
				drawRef.line((xStart + blade, yArrowEnd - yDisplace, xStart, yArrowEnd), fill = clr, width = config.lineThickness)
				drawRef.line((xStart + blade, yArrowEnd + yDisplace , xStart, yArrowEnd), fill = clr, width = config.lineThickness)

	
		#yStart += arrowLength + bufferDistance
		xStart += arrowLength + bufferDistance


def remakeArrowBlock(imageRef, direction):
	drawRef = ImageDraw.Draw(imageRef)
	makeArrows(drawRef, direction)


def makeMessage(config, imageRef, messageString = "FooBar", direction = 1):
	#global config


	if(config.colorMode == "getRandomRGB") : clr = colorutils.getRandomRGB(config.brightness)
	if(config.colorMode == "randomColor") : clr = colorutils.randomColor(config.brightness)
	if(config.colorMode == "getRandomColorWheel") : clr = colorutils.getRandomColorWheel(config.brightness)


	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
	# draw the message to get its size
	if(config.sansSerif) : 
		font = ImageFont.truetype(config.path  + '/assets/fonts/freefont/FreeSansBold.ttf', config.fontSize)
	else :
		font = ImageFont.truetype(config.path  + '/assets/fonts/freefont/FreeSerifBold.ttf', config.fontSize)

	tempImage = Image.new("RGBA", (1200,196))
	draw  = ImageDraw.Draw(tempImage)
	pixLen = draw.textsize(messageString, font = font)
	# For some reason textsize is not getting full height !
	fontHeight = round(pixLen[1] * 1.3)

	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
	# make a new image with the right size
	scrollImage = Image.new("RGBA", (pixLen[0] + 2 , fontHeight))
	draw  = ImageDraw.Draw(scrollImage)
	iid = scrollImage.im.id

	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
	# Draw the text with "borders"
	indent = round(.05 * config.tileSize[0])
	for i in range(1, config.shadowSize) :
		draw.text((indent + -i,-i),messageString,(0,0,0),font=font)
		draw.text((indent + i,i),messageString,(0,0,0),font=font)

	draw.text((2,0),messageString, clr ,font=font)

	refDraw = ImageDraw.Draw(imageRef)
	refDraw.rectangle((0,0,pixLen[0] + 2 , fontHeight), fill = config.bgBackGroundColor)
	imageRef.paste(scrollImage,(0,config.textVOffest), scrollImage)


def remakeMessage(config, imageRef, messageString = "FooBar", direction = 1) :
	messageString = config.msg1 if random.random() < .5 else config.msg2
	config.textVOffest = round(random.uniform(-12,-30))
	if random.random() < .5 :
		config.colorMode = "randomColor"
	else:
		config.colorMode = "getRandomRGB"
	makeMessage(imageRef=imageRef, messageString=messageString, direction=direction)

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def makeBackGround(config, drawRef, n = 1):
	rows = config.patternRows * 1
	cols = config.patternCols * 1

	xDiv = round((config.displayRows * config.windowWidth) / cols) #- config.patternColsOffset
	yDiv = ((config.canvasHeight / rows) / config.displayRows) #- config.patternRowsOffset

	#print(xDiv, yDiv)

	xStart = 0
	yStart = 0

	gap = 0

	config.arrowBgBackGroundColor = (0,0,0,20) #colorutils.getRandomColor()

	drawRef.rectangle((0,0,(round(config.displayRows * config.windowWidth)), config.canvasHeight), fill = config.bgBackGroundColor)

	## Chevron pattern
	## config.bgForeGroundColor
	#fillClr = colorutils.getRandomColor(config.brightness/2)
	
	#config.patternColor = config.patternEndColor
	#config.patternEndColor = colorutils.getRandomColor(config.brightness)

	#print(xDiv, yDiv)

	rowMultiplier = 1
	colMultiplier = 1

	if (config.pattern == "bricks") :
		rowMultiplier = 1
		colMultiplier = 1

	if (config.pattern == "regularLines") :
		rowMultiplier = 2
		colMultiplier = 1		

	if (config.pattern == "pluses") :
		rowMultiplier = 2
		colMultiplier = 1

	if (config.pattern == "diamonds") :
		rowMultiplier = 2
		colMultiplier = 2

	steps =  cols

	## The multiplier is actually a factor of the number of rows 
	## but, generally so far only using two rows ....
	rDelta = colMultiplier * (config.patternEndColor[0] - config.patternColor[0]) / steps
	gDelta = colMultiplier * (config.patternEndColor[1] - config.patternColor[1]) / steps
	bDelta = colMultiplier * (config.patternEndColor[2] - config.patternColor[2]) / steps
	
	for c in range (0, cols) : 
		columnOffset = 0

		rCol  = config.patternColor[0] + rDelta
		gCol  = config.patternColor[1] + gDelta
		bCol  = config.patternColor[2] + bDelta
		config.patternColor = (rCol, gCol, bCol)

		### Because the way the pattern draws the left end is actually the end color
		### so need to reverse the color gradient ....

		fillClr = (
			(round(config.patternEndColor[0] - rDelta * (c+1))),
			(round(config.patternEndColor[1] - gDelta * (c+1))),
			(round(config.patternEndColor[2] - bDelta * (c+1))),
			200)

		#print(c,fillClr)

		for r in range (0, rows) : 
			columnOffset = 0
			if r == 0 or r == 2 or r == 4 or r == 6:
				columnOffset = xDiv

			if r/2%2 == 0 :
				columnOffset = xDiv


			if(random.random() < config.patternDrawProb) :

				if (config.pattern == "diamonds") :
					poly = []
					poly.append((xStart, yStart + yDiv))
					poly.append((xStart + xDiv, yStart))
					poly.append((xStart + xDiv + xDiv, yStart + yDiv))
					poly.append((xStart + xDiv, yStart + yDiv + yDiv))
					drawRef.polygon(poly, fill = fillClr) 
					#if(n ==2) : color = (100,200,0,255)


				if (config.pattern == "bricks") :
					length = xDiv
					xPos = xStart + columnOffset
					yPos = yStart
					drawRef.rectangle((xPos, yPos, xPos + length , yPos + yDiv), fill = fillClr, outline=None)


				if (config.pattern == "pluses") :
					length = xDiv
					height = xDiv/2

					xPos = xStart + columnOffset
					yPos = yStart
					
					xPos2 = xPos + round(length/2 - height/2)
					yPos2 = round(yPos - length/2 + height/2)

					drawRef.rectangle((xPos, yPos, xPos + length , yPos + yDiv), fill = fillClr, outline=None)
					drawRef.rectangle((xPos2, yPos2, xPos2 + height , yPos2 + length), fill = fillClr, outline=None)
					

				if (config.pattern == "regularLines") :
					length = xDiv
					xPos = xStart + columnOffset
					yPos = yStart
					drawRef.rectangle((xPos, yPos, xPos + length , yPos + yDiv), fill = fillClr, outline=None)


				if (config.pattern == "lines")  :
					#if (r%2 > 0):
					length = int(round(random.uniform(1,2 * xDiv)))
					offset = int(round(random.uniform(0,4 * xDiv)))

					if(random.random() < .5) :
						drawRef.rectangle((xStart, yStart, xStart + 2 * xDiv , yStart + yDiv), fill = fillClr, outline=None)
					else:
						drawRef.rectangle((xStart + offset, yStart, xStart + length + offset, yStart + yDiv), fill = fillClr, outline=None)			

			yStart += rowMultiplier * yDiv
		if config.pattern == "lines" :
			xStart += colMultiplier * xDiv
		else :
			xStart += xDiv * 2
		yStart = 0


	config.patternColor = config.patternEndColor

## Layer imagery callbacks & regeneration functions

def remakePatternBlock(config, imageRef, direction):
	## Stacking the cards ...
	config.patternColor = config.patternEndColor

	if(random.random() < .3) :
		config.patternEndColor = colorutils.randomColorAlpha(config.brightness)
	if(random.random() < .05) :
		config.patternEndColor = (254,0,254,255)
	if(random.random() < .05) :
		config.patternEndColor = (0,0,250,255)

	if(config.alwaysRandomPattern == True) :
		if(random.random() < .3) :
			config.patternDrawProb = random.uniform(.08,.12)
		if(random.random() < .3) :
			config.patternRows = (round(random.uniform(40,80)))
		if(random.random() < .3) :
			config.patternCols = (round(random.uniform(90,240)))
	else :
		pass

	if(config.alwaysRandomPatternColor == True) :
		config.patternEndColor = colorutils.randomColorAlpha(config.brightness)

	drawRef = ImageDraw.Draw(imageRef)
	makeBackGround(config,drawRef, direction)

## Setup and run functions

def configureBackgroundScrolling(config, workConfig):
	config.patternRows = int(workConfig.get("scroller", 'patternRows'))
	config.patternCols = int(workConfig.get("scroller", 'patternCols'))
	config.patternRowsOffset = int(workConfig.get("scroller", 'patternRowsOffset'))
	config.patternColsOffset = int(workConfig.get("scroller", 'patternColsOffset'))
	config.patternDrawProb = float(workConfig.get("scroller", 'patternDrawProb')) 
	config.bgBackGroundColor = (workConfig.get("scroller", 'bgBackGroundColor').split(","))
	config.bgBackGroundColor = tuple([int(i) for i in config.bgBackGroundColor])
	config.bgForeGroundColor = (workConfig.get("scroller", 'bgForeGroundColor').split(","))
	config.bgForeGroundColor = tuple([int(i) for i in config.bgForeGroundColor])
	config.pattern = (workConfig.get("scroller", 'pattern'))
	config.patternSpeed = float(workConfig.get("scroller", 'patternSpeed'))

	config.scroller4 = continuous_scroller.ScrollObject()
	scrollerRef = config.scroller4
	scrollerRef.typeOfScroller = "bg"
	scrollerRef.canvasWidth = int(config.displayRows * config.canvasWidth)
	scrollerRef.xSpeed = config.patternSpeed
	scrollerRef.setUp(config)
	direction = 1 if scrollerRef.xSpeed > 0 else -1
	scrollerRef.callBack = {"func" : remakePatternBlock, "direction" : direction}	

	config.patternColor = (50,0,55,50)
	config.patternEndColor = (255,0,255,50)	
	
	try :
		config.useUltraSlowSpeed = (workConfig.getboolean("scroller", 'useUltraSlowSpeed'))
	except Exception as e: 
		config.useUltraSlowSpeed = False
		print (str(e))	

	try :
		config.changeProb = float(workConfig.get("scroller", 'changeProb'))
	except Exception as e: 
		config.changeProb = 0.0
		print (str(e))

	if (config.alwaysRandomPatternColor == True):
		config.patternColor = colorutils.randomColorAlpha(config.brightness)
		config.patternEndColor = colorutils.randomColorAlpha(config.brightness)

	makeBackGround(config,scrollerRef.bg1Draw, 1)
	makeBackGround(config,scrollerRef.bg2Draw, 1)

	config.t1  = time.time()
	config.t2  = time.time()
	config.timeToComplete = 1
	config.scrollerPauseBool = False

	config.scrollArray.append(scrollerRef)

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def configureImageScrolling(config, workConfig):
	config.imageSpeed = float(workConfig.get("scroller", 'imageSpeed'))
	config.imageBlockImage = workConfig.get("scroller", 'imageBlockImage')
	config.imageBlockBuffer = int(workConfig.get("scroller", 'imageBlockBuffer'))
	config.imageBlockRemakeProb = float(workConfig.get("scroller", 'imageBlockRemakeProb'))

	arg = config.path + config.imageBlockImage
	config.imageBlockImageLoaded = Image.open(arg , "r")
	config.imageBlockImageLoaded.load()
	config.imageBlockImageLoadedCopy  = config.imageBlockImageLoaded.copy()

	config.scroller5 = continuous_scroller.ScrollObject()
	scrollerRef = config.scroller5
	scrollerRef.canvasWidth = round(config.displayCols * config.canvasWidth)
	#scrollerRef.canvasHeight = int(config.windowHeight)
	scrollerRef.xSpeed = config.imageSpeed
	scrollerRef.setUp(config)
	direction = 1 if scrollerRef.xSpeed > 0 else -1
	scrollerRef.callBack = {"func" : remakeScrollBlock, "direction" : direction}
	makeScrollBlock(scrollerRef.bg1, scrollerRef.bg1Draw, direction)
	makeScrollBlock(scrollerRef.bg2, scrollerRef.bg2Draw, direction)
	config.scrollArray.append(scrollerRef)
		

def configureArrowScrolling(config, workConfig):
	config.arrowCols = int(workConfig.get("scroller", 'arrowCols'))
	config.lineThickness = int(workConfig.get("scroller", 'lineThickness'))
	config.arrowSpeed = int(workConfig.get("scroller", 'arrowSpeed'))
	config.greyLevel = int(workConfig.get("scroller", 'greyLevel'))
	config.redShift = int(workConfig.get("scroller", 'redShift'))
	config.scroller1 = continuous_scroller.ScrollObject()

	scrollerRef = config.scroller1
	scrollerRef.canvasWidth = round(config.displayRows * config.canvasWidth)
	scrollerRef.xSpeed = config.arrowSpeed
	scrollerRef.setUp(config)
	direction = 1 if scrollerRef.xSpeed > 0 else -1
	scrollerRef.callBack = {"func" : remakeArrowBlock, "direction" : direction}
	makeArrows(scrollerRef.bg1Draw, 1)
	makeArrows(scrollerRef.bg2Draw, 1)
	config.scrollArray.append(scrollerRef)


def configureMessageScrolling(config, workConfig):
	config.colorMode = workConfig.get("scroller", 'colorMode')
	config.sansSerif = workConfig.getboolean("scroller", 'sansSerif')
	config.fontSize =  int(workConfig.get("scroller", 'fontSize'))
	config.textVOffest = int(workConfig.get("scroller", 'textVOffest'))
	config.shadowSize = int(workConfig.get("scroller", 'shadowSize'))
	config.textSpeed = float(workConfig.get("scroller", 'textSpeed'))
	config.msg1 = workConfig.get("scroller", 'msg1')
	config.msg2 = workConfig.get("scroller", 'msg2')
	config.msg3 = workConfig.get("scroller", 'msg3')

	config.scroller2 = continuous_scroller.ScrollObject()
	scrollerRef = config.scroller2
	scrollerRef.canvasWidth = round(config.displayRows * config.canvasWidth)
	scrollerRef.xSpeed = -config.textSpeed
	scrollerRef.setUp(config)
	direction = 1 if scrollerRef.xSpeed > 0 else -1
	makeMessage(scrollerRef.bg1,config.msg1, direction)
	makeMessage(scrollerRef.bg2,config.msg1, direction)
	scrollerRef.callBack = {"func" : remakeMessage, "direction" : direction}
	config.scrollArray.append(scrollerRef)

	config.scroller3 = continuous_scroller.ScrollObject()
	scrollerRef = config.scroller3
	scrollerRef.canvasWidth = round(config.displayRows * config.canvasWidth)
	scrollerRef.xSpeed = config.textSpeed + .25
	scrollerRef.setUp(config)
	direction = 1 if scrollerRef.xSpeed > 0 else -1
	makeMessage(scrollerRef.bg1,config.msg2, direction)
	makeMessage(scrollerRef.bg2,config.msg2, direction)
	scrollerRef.callBack = {"func" : remakeMessage, "direction" : direction}
	config.scrollArray.append(scrollerRef)


def configureAltTextScrolling(config, workConfig) :
	config.colorMode = workConfig.get("scroller", 'colorMode')
	config.sansSerif = workConfig.getboolean("scroller", 'sansSerif')
	config.fontSize =  int(workConfig.get("scroller", 'fontSize'))
	config.textVOffest = int(workConfig.get("scroller", 'textVOffest'))
	config.shadowSize = int(workConfig.get("scroller", 'shadowSize'))
	config.textSpeed = float(workConfig.get("scroller", 'textSpeed'))
	config.scroller6 = continuous_scroller.ScrollObject()
	scrollerRef = config.scroller6
	scrollerRef.canvasWidth = round(config.displayRows * config.canvasWidth)
	scrollerRef.xSpeed = -config.textSpeed
	scrollerRef.setUp(config)
	direction = 1 if scrollerRef.xSpeed > 0 else -1
	makeDaemonMessages(scrollerRef.bg1, direction)
	makeDaemonMessages(scrollerRef.bg2, direction)
	scrollerRef.callBack = {"func" : remakeDaemonMessages, "direction" : direction}
	config.scrollArray.append(scrollerRef)


def configureImageOverlay(config, workConfig):
	config.overLayImage = workConfig.get("scroller", 'overLayImage')
	config.overLayXPos = int(workConfig.get("scroller", 'overLayXPos'))
	config.overLayYPos = int(workConfig.get("scroller", 'overLayYPos'))
	config.overlayGlitchSize = int(workConfig.get("scroller", 'overlayGlitchSize'))
	config.overlayBrightness = float(workConfig.get("scroller", 'overlayBrightness'))
	config.overlayGlitchRate = float(workConfig.get("scroller", 'overlayGlitchRate'))
	config.overlayResetRate = float(workConfig.get("scroller", 'overlayResetRate'))

	arg = config.path + config.overLayImage
	config.loadedImage = Image.open(arg , "r")
	config.loadedImage.load()
	config.loadedImageCopy  = config.loadedImage.copy()

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def init(config, workConfig) :
	#global config

	print("WORKMODULES SCROLLER HOLDER INIT")

	config.redrawSpeed  = float(workConfig.get("scroller", 'redrawSpeed')) 

	try:
		config.delay = float(workConfig.get("scroller", 'delay')) 
	except Exception as e:
		print (str(e))
		config.delay  = float(workConfig.get("scroller", 'redrawSpeed')) 


	config.windowWidth  = float(workConfig.get("displayconfig", 'windowWidth')) 
	config.windowHeight  = float(workConfig.get("displayconfig", 'windowHeight')) 

	config.xOffset = int(workConfig.get("scroller", 'xOffset')) 
	config.yOffset = int(workConfig.get("scroller", 'yOffset')) 

	config.displayRows = int(workConfig.get("scroller", 'displayRows'))
	config.displayCols = int(workConfig.get("scroller", 'displayCols'))

	#********* HARD CODING VALUES  ***********************

	config.bandHeight = int(round(config.canvasHeight / config.displayRows) )
	config.bgBackGroundColor = (0,0,0,0)
	config.arrowBgBackGroundColor = (0,0,0,200)

	config.canvasImage = Image.new("RGBA", (config.canvasWidth * 10, config.canvasHeight))
	config.canvasImageDraw = ImageDraw.Draw(config.canvasImage)	

	config.imageLayer = Image.new("RGBA", (config.canvasWidth * 10, config.canvasHeight))
	config.imageLayerDraw = ImageDraw.Draw(config.canvasImage)

	config.workImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.workImageDraw = ImageDraw.Draw(config.workImage)

	config.overallBlur = float(workConfig.get("scroller", 'overallBlur', vars=0, fallback=0))

	config.flip = False
	config.scrollArray = []

	## Set up the scrolling layer
	
	config.useBackground = workConfig.getboolean("scroller", 'useBackground')
	config.altDirectionScrolling = workConfig.getboolean("scroller", 'altDirectionScrolling')
	config.alwaysRandomPatternColor = workConfig.getboolean("scroller", 'alwaysRandomPatternColor')
	config.alwaysRandomPattern = workConfig.getboolean("scroller", 'alwaysRandomPattern')
	if(config.useBackground == True) :
		configureBackgroundScrolling(config, workConfig)

	try:
		config.minHue = float(workConfig.get("scroller", 'minHue')) 
		config.maxHue = float(workConfig.get("scroller", 'minHue')) 
		config.minSat = float(workConfig.get("scroller", 'minSat')) 
		config.maxSat = float(workConfig.get("scroller", 'maxSat')) 
		config.minVal = float(workConfig.get("scroller", 'minVal')) 
		config.maxVal = float(workConfig.get("scroller", 'maxVal')) 

	except Exception as e:
		print (str(e))
		config.minHue = 0
		config.maxHue = 360
		config.minSat = .1
		config.maxSat = 1.0
		config.minVal = .1
		config.maxVal = .85


	try:
		config.useText = workConfig.getboolean("scroller", 'useText')
		config.useAltText = workConfig.getboolean("scroller", 'useAltText')
		if(config.useText == True) :
			configureMessageScrolling(config, workConfig)
		if(config.useAltText == True) :
			configureAltTextScrolling(config, workConfig)
	except Exception as e:
		print (str(e))

	
	try:
		config.useOverLayImage = workConfig.getboolean("scroller", 'useOverLayImage')
		if(config.useOverLayImage ==  True) :
			configureImageOverlay(config, workConfig)
	except Exception as e:
		config.useOverLayImage = False
		print (str(e))
	

	
	try:
		config.useArrows = workConfig.getboolean("scroller", 'useArrows')
		if(config.useArrows == True) :
			configureArrowScrolling(config, workConfig)
	except Exception as e:
		print (str(e))
	

	
	try:
		config.useImages = workConfig.getboolean("scroller", 'useImages')
		config.useTransparentImages = workConfig.getboolean("scroller", 'useTransparentImages')
		if(config.useImages == True) :
			configureImageScrolling(config, workConfig)
	except Exception as e:
		print (str(e))
	
	
	try:
		config.doingRefreshCount = float(workConfig.get("scroller", 'doingRefreshCount'))
	except Exception as e:
		config.doingRefreshCount = 50
		print (str(e))


	config.f = FaderObj()
	config.f.setUp(config.renderImageFull, config.workImage)
	config.f.doingRefreshCount = config.doingRefreshCount
	#config.workImageDraw.rectangle((0,0,100,100), fill=(100,0,0,100))
	config.renderImageFullOld = config.renderImageFull.copy()
	config.fadingDone = True

	config.useFadeThruAnimation = True
	config.deltaTimeDone = True


def runWork(config):
	#global config
	while True:
		iterate(config)
		time.sleep(config.redrawSpeed)


def checkTime(config, scrollerObj):
	config.t2  = time.time()
	delta = config.t2  - config.t1

	if delta > config.timeToComplete and config.deltaTimeDone == False :
		scrollerObj.xSpeed -= 0.2
		if scrollerObj.xSpeed <= .70 :
			config.deltaTimeDone = True
			config.useFadeThruAnimation = True
			config.f.fadingDone = True 

			#print ("DELTA TIME UP")
			processImageForScrolling(config)
			if config.useUltraSlowSpeed == True :
				scrollerObj.xSpeed = 1 

def processImageForScrolling(config) :

	## Run through each of the objects being scrolled - text, image, background etc
	for scrollerObj in config.scrollArray :
		scrollerObj.scroll()
		config.canvasImage.paste(scrollerObj.canvas, (0,0), scrollerObj.canvas)


	# Chop up the scrollImage into "rows"
	for n in range(0, config.displayRows) :
		segment = config.canvasImage.crop((n * config.canvasWidth, 0, config.canvasWidth + n * config.canvasWidth, config.bandHeight))
		
		if ((n % 2 ==  0) and (config.displayRows >  1) and config.altDirectionScrolling == True) :
			segment = ImageOps.flip(segment)
			segment = ImageOps.mirror(segment)

		config.workImage.paste(segment, (0, n * config.bandHeight))


	if(config.useOverLayImage  ==  True) :
		if(random.random() < config.overlayGlitchRate ) :
			glitchBox(config.loadedImage, -config.overlayGlitchSize, config.overlayGlitchSize)
		if(random.random() < config.overlayResetRate ) :
			config.loadedImage.paste(config.loadedImageCopy)
		config.workImage.paste(config.loadedImage, (config.overLayXPos, config.overLayYPos), config.loadedImage)

	if (config.overallBlur != 0 ) :
		config.workImage = config.workImage.filter(ImageFilter.GaussianBlur(radius=config.overallBlur))


def iterate(config) :

	for scrollerObj in config.scrollArray :
		if scrollerObj.typeOfScroller == "bg" :
			if random.random() < config.changeProb and config.deltaTimeDone == True and config.useFadeThruAnimation == True:
				config.useFadeThruAnimation = False
				scrollerObj.xSpeed = random.uniform(.6,10)
				config.deltaTimeDone = False
				config.t1  = time.time()
				config.timeToComplete = random.uniform(3,10)
			checkTime(config, scrollerObj)

	if config.useFadeThruAnimation == True and config.useUltraSlowSpeed == True:
		if config.f.fadingDone == True :
			config.renderImageFullOld = config.renderImageFull.copy()
			config.renderImageFull.paste(config.workImage, (config.imageXOffset, config.imageYOffset), config.workImage)
			config.f.xPos = config.imageXOffset
			config.f.yPos = config.imageYOffset
			#config.renderImageFull = config.renderImageFull.convert("RGBA")
			#renderImageFull = renderImageFull.convert("RGBA")
			config.f.setUp(config.renderImageFullOld.convert("RGBA"), config.workImage.convert("RGBA") )
			processImageForScrolling(config)

		config.f.fadeIn()
		config.render(config.f.blendedImage, 0,0)

	else :

		processImageForScrolling(config)
		config.renderImageFull.paste(config.workImage, (config.imageXOffset, config.imageYOffset), config.workImage)
		config.render(config.renderImageFull, 0,0)


def main(config, workConfig, run = True) :
	#global config, threads, thrd
	init(config, workConfig)
	
	if(run) : runWork(config)

### Kick off .......
if __name__ == "__main__":
	__main__()