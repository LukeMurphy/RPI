#!/usr/bin/python
#import modules
# ################################################### #
import os, sys, getopt, time, random, math, datetime, textwrap
from collections import OrderedDict
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageChops, ImageEnhance
from PIL import ImageChops, ImageFilter, ImagePalette
from modules import colorutils, coloroverlay, continuous_scroller

global config


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
## Image manipulations

def glitchBox(img, r1 = -10, r2 = 10, dir = "horizontal") :

	apparentWidth = img.size[0]
	apparentHeight = img.size[1]

	dx = int(random.uniform(r1,r2))
	dy = int(random.uniform(r1,r2))
	
	#dx = 0

	sectionWidth = int(random.uniform(2, apparentWidth - dx))
	sectionHeight = int(random.uniform(2, apparentHeight - dy))
	
	#sectionHeight = apparentWidth

	# 95% of the time they dance together as mirrors
	if(random.random() < .97) :
		if(dir  == "horizontal") :
			cp1 = img.crop((0, dy,  apparentWidth, dy + sectionHeight))
		else :
			cp1 = img.crop((dx, 0, dx + sectionWidth, sectionHeight))

		img.paste( cp1, (int(0 + dx), int(0 + dy)))	

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
## Layer imagery
def makeDaemonMessages(imageRef, direction = 1):
	global config

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

	combination = demonArray[int(math.floor(random.uniform(0, len(demonArray))))]
	arrayToUse = combination[int(math.floor(random.uniform(0, len(combination))))]
	messageString = ""

	if(config.sansSerif) : 
		font = ImageFont.truetype(config.path  + '/assets/fonts/freefont/FreeSansBold.ttf', config.fontSize)
	else :
		font = ImageFont.truetype(config.path  + '/assets/fonts/freefont/FreeSerifBold.ttf', config.fontSize)

	for i in range(0,4) :
		adj = arrayToUse[1][int(math.floor(random.uniform(0,7)))]
		noun = arrayToUse[0][int(math.floor(random.uniform(0,7)))]
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

def makeScrollBlock(imageRef, imageDrawRef, direction):
	global config
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

def remakeScrollBlock(imageRef, direction):
	drawRef = ImageDraw.Draw(imageRef)
	if(random.random() < config.imageBlockRemakeProb) :
		makeScrollBlock(imageRef, drawRef, direction)

def makeArrows(drawRef, direction = 1) :

	rows = config.displayCols * 2
	cols = config.arrowCols * 2

	xDiv = int(config.displayRows * config.windowWidth) / cols 
	yDiv = config.canvasHeight / rows 

	xStart = 0 #config.canvasWidth / 2
	yStart = config.bandHeight / 2 #config.canvasHeight / 2

	bufferDistance = 15
	arrowLength = cols * 2
	blade = cols / 3

	clr  = (int(220 * config.brightness),0,0)

	drawRef.rectangle((0,0,int(config.displayRows * config.windowWidth), config.canvasHeight), fill = config.bgBackGroundColor)

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

def makeMessage(imageRef, messageString = "FooBar", direction = 1):
	global config


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

def remakeMessage(imageRef, messageString = "FooBar", direction = 1) :
	messageString = config.msg1 if random.random() < .5 else config.msg2
	makeMessage(imageRef=imageRef, messageString=messageString, direction=direction)

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def makeBackGround(drawRef, n = 1):
	rows = config.patternRows * 1
	cols = config.patternCols * 1

	xDiv = int(round(config.displayRows * config.windowWidth)) / cols #- config.patternColsOffset
	yDiv = config.canvasHeight / rows / config.displayRows #- config.patternRowsOffset

	xStart = 0
	yStart = 0

	config.arrowBgBackGroundColor = (0,0,0,20) #colorutils.getRandomColor()

	drawRef.rectangle((0,0,int(round(config.displayRows * config.windowWidth)), config.canvasHeight), fill = config.bgBackGroundColor)

	## Chevron pattern
	## config.bgForeGroundColor
	#fillClr = colorutils.getRandomColor(config.brightness/2)
	
	#config.patternColor = config.patternEndColor
	#config.patternEndColor = colorutils.getRandomColor(config.brightness)

	#print(xDiv, yDiv)

	rowMultiplier = 1
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

		rCol  = config.patternColor[0] + rDelta
		gCol  = config.patternColor[1] + gDelta
		bCol  = config.patternColor[2] + bDelta
		config.patternColor = (rCol, gCol, bCol)

		### Because the way the pattern draws the left end is actually the end color
		### so need to reverse the color gradient ....

		fillClr = (
			int(round(config.patternEndColor[0] - rDelta * (c+1))),
			int(round(config.patternEndColor[1] - gDelta * (c+1))),
			int(round(config.patternEndColor[2] - bDelta * (c+1))),
			200)

		#print(c,fillClr)

		for r in range (0, rows) : 
			if(random.random() < config.patternDrawProb) :
				if (config.pattern == "diamonds") :
					poly = []
					poly.append((xStart, yStart + yDiv))
					poly.append((xStart + xDiv, yStart))
					poly.append((xStart + xDiv + xDiv, yStart + yDiv))
					poly.append((xStart + xDiv, yStart + yDiv + yDiv))
					drawRef.polygon(poly, fill = fillClr) 
					#if(n ==2) : color = (100,200,0,255)
				else :
					#if (r%2 > 0):
					length = int(round(random.uniform(1,2 * xDiv)))
					offset = int(round(random.uniform(0,4 * xDiv)))

					if(random.random() < .5) :
						drawRef.rectangle((xStart, yStart, xStart + 2 * xDiv , yStart + yDiv), fill = fillClr, outline=None)
					else:
						drawRef.rectangle((xStart + offset, yStart, xStart + length + offset, yStart + yDiv), fill = fillClr, outline=None)
			yStart += rowMultiplier * yDiv
		xStart += colMultiplier * xDiv
		yStart = 0

	config.patternColor = config.patternEndColor

## Layer imagery callbacks & regeneration functions
def remakePatternBlock(imageRef, direction):
	## Stacking the cards ...
	config.patternColor = config.patternEndColor

	if(random.random() < .3) :
		config.patternEndColor = colorutils.randomColorAlpha(config.brightness)
	if(random.random() < .05) :
		config.patternEndColor = (254,0,254,255)
	if(random.random() < .05) :
		config.patternEndColor = (0,0,250,255)
	if(random.random() < .3) :
		config.patternDrawProb = random.uniform(.08,.12)
	if(random.random() < .3) :
		config.patternRows = int(round(random.uniform(40,80)))
	if(random.random() < .3) :
		config.patternCols = int(round(random.uniform(90,240)))

	drawRef = ImageDraw.Draw(imageRef)
	makeBackGround(drawRef, direction)

## Setup and run functions
def configureBackgroundScrolling():
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
	scrollerRef.canvasWidth = int(config.displayRows * config.canvasWidth)
	scrollerRef.xSpeed = config.patternSpeed
	scrollerRef.setUp()
	direction = 1 if scrollerRef.xSpeed > 0 else -1
	scrollerRef.callBack = {"func" : remakePatternBlock, "direction" : direction}	
	config.patternColor = (50,0,55,50)
	config.patternEndColor = (255,0,255,50)
	makeBackGround(scrollerRef.bg1Draw, 1)
	makeBackGround(scrollerRef.bg2Draw, 1)
	config.scrollArray.append(scrollerRef)

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def configureImageScrolling():
	config.imageSpeed = int(workConfig.get("scroller", 'imageSpeed'))
	config.imageBlockImage = workConfig.get("scroller", 'imageBlockImage')
	config.imageBlockBuffer = int(workConfig.get("scroller", 'imageBlockBuffer'))
	config.imageBlockRemakeProb = float(workConfig.get("scroller", 'imageBlockRemakeProb'))

	arg = config.path + config.imageBlockImage
	config.imageBlockImageLoaded = Image.open(arg , "r")
	config.imageBlockImageLoaded.load()
	config.imageBlockImageLoadedCopy  = config.imageBlockImageLoaded.copy()

	config.scroller5 = continuous_scroller.ScrollObject()
	scrollerRef = config.scroller5
	scrollerRef.canvasWidth = int(config.displayRows * config.canvasWidth)
	#scrollerRef.canvasHeight = int(config.windowHeight)
	scrollerRef.xSpeed = config.imageSpeed
	scrollerRef.setUp()
	direction = 1 if scrollerRef.xSpeed > 0 else -1
	scrollerRef.callBack = {"func" : remakeScrollBlock, "direction" : direction}
	makeScrollBlock(scrollerRef.bg1, scrollerRef.bg1Draw, direction)
	makeScrollBlock(scrollerRef.bg2, scrollerRef.bg2Draw, direction)
	config.scrollArray.append(scrollerRef)
		
def configureArrowScrolling():
	config.arrowCols = int(workConfig.get("scroller", 'arrowCols'))
	config.lineThickness = int(workConfig.get("scroller", 'lineThickness'))
	config.arrowSpeed = int(workConfig.get("scroller", 'arrowSpeed'))
	config.greyLevel = int(workConfig.get("scroller", 'greyLevel'))
	config.redShift = int(workConfig.get("scroller", 'redShift'))
	config.scroller1 = continuous_scroller.ScrollObject()

	scrollerRef = config.scroller1
	scrollerRef.canvasWidth = int(config.displayRows * config.canvasWidth)
	scrollerRef.xSpeed = config.arrowSpeed
	scrollerRef.setUp()
	direction = 1 if scrollerRef.xSpeed > 0 else -1
	scrollerRef.callBack = {"func" : remakeArrowBlock, "direction" : direction}
	makeArrows(scrollerRef.bg1Draw, 1)
	makeArrows(scrollerRef.bg2Draw, 1)
	config.scrollArray.append(scrollerRef)

def configureMessageScrolling():
	config.colorMode = workConfig.get("scroller", 'colorMode')
	config.sansSerif = workConfig.getboolean("scroller", 'sansSerif')
	config.fontSize =  int(workConfig.get("scroller", 'fontSize'))
	config.textVOffest = int(workConfig.get("scroller", 'textVOffest'))
	config.shadowSize = int(workConfig.get("scroller", 'shadowSize'))
	config.textSpeed = int(workConfig.get("scroller", 'textSpeed'))
	config.msg1 = workConfig.get("scroller", 'msg1')
	config.msg2 = workConfig.get("scroller", 'msg2')
	config.msg3 = workConfig.get("scroller", 'msg3')

	config.scroller2 = continuous_scroller.ScrollObject()
	scrollerRef = config.scroller2
	scrollerRef.canvasWidth = int(config.displayRows * config.canvasWidth)
	scrollerRef.xSpeed = -config.textSpeed
	scrollerRef.setUp()
	direction = 1 if scrollerRef.xSpeed > 0 else -1
	makeMessage(scrollerRef.bg1,config.msg1, direction)
	makeMessage(scrollerRef.bg2,config.msg1, direction)
	scrollerRef.callBack = {"func" : remakeMessage, "direction" : direction}
	config.scrollArray.append(scrollerRef)

	config.scroller3 = continuous_scroller.ScrollObject()
	scrollerRef = config.scroller3
	scrollerRef.canvasWidth = int(config.displayRows * config.canvasWidth)
	scrollerRef.xSpeed = config.textSpeed + 1
	scrollerRef.setUp()
	direction = 1 if scrollerRef.xSpeed > 0 else -1
	makeMessage(scrollerRef.bg1,config.msg2, direction)
	makeMessage(scrollerRef.bg2,config.msg2, direction)
	scrollerRef.callBack = {"func" : remakeMessage, "direction" : direction}
	config.scrollArray.append(scrollerRef)

def configureAltTextScrolling() :
	config.colorMode = workConfig.get("scroller", 'colorMode')
	config.sansSerif = workConfig.getboolean("scroller", 'sansSerif')
	config.fontSize =  int(workConfig.get("scroller", 'fontSize'))
	config.textVOffest = int(workConfig.get("scroller", 'textVOffest'))
	config.shadowSize = int(workConfig.get("scroller", 'shadowSize'))
	config.textSpeed = int(workConfig.get("scroller", 'textSpeed'))
	config.scroller6 = continuous_scroller.ScrollObject()
	scrollerRef = config.scroller6
	scrollerRef.canvasWidth = int(config.displayRows * config.canvasWidth)
	scrollerRef.xSpeed = -config.textSpeed
	scrollerRef.setUp()
	direction = 1 if scrollerRef.xSpeed > 0 else -1
	makeDaemonMessages(scrollerRef.bg1, direction)
	makeDaemonMessages(scrollerRef.bg2, direction)
	scrollerRef.callBack = {"func" : remakeDaemonMessages, "direction" : direction}
	config.scrollArray.append(scrollerRef)

def configureImageOverlay():
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
def init() :
	global config
	config.redrawSpeed  = float(workConfig.get("scroller", 'redrawSpeed')) 

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

	config.flip = False
	config.scrollArray = []

	config.useOverLayImage = workConfig.getboolean("scroller", 'useOverLayImage')
	config.useArrows = workConfig.getboolean("scroller", 'useArrows')
	config.useText = workConfig.getboolean("scroller", 'useText')
	config.useImages = workConfig.getboolean("scroller", 'useImages')
	config.useTransparentImages = workConfig.getboolean("scroller", 'useTransparentImages')
	config.useBackground = workConfig.getboolean("scroller", 'useBackground')
	config.useAltText = workConfig.getboolean("scroller", 'useAltText')

	try:
		config.altDirectionScrolling = workConfig.getboolean("scroller", 'altDirectionScrolling')
	except Exception as e:
		print (str(e))
		config.altDirectionScrolling = True

	if(config.useOverLayImage ==  True) :
		configureImageOverlay()

	## Set up the scrolling layers
	if(config.useBackground == True) :
		configureBackgroundScrolling()

	if(config.useArrows == True) :
		configureArrowScrolling()

	if(config.useText == True) :
		configureMessageScrolling()

	if(config.useAltText == True) :
		configureAltTextScrolling()

	if(config.useImages == True) :
		configureImageScrolling()

def runWork():
	global config
	while True:
		iterate()
		time.sleep(config.redrawSpeed)

def iterate() :
	global config

	#config.workImageDraw.rectangle((0,0,config.canvasWidth,config.canvasHeight), fill  = (0,0,0))
	#config.canvasImageDraw.rectangle((0,0,config.canvasWidth*10,config.canvasHeight), fill  = (0,0,0,20))

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
	
	config.renderImageFull.paste(config.workImage, (config.imageXOffset, config.imageYOffset), config.workImage)
	config.render(config.renderImageFull, 0,0)

def main(run = True) :
	global config, threads, thrd
	init()
	
	if(run) : runWork()

### Kick off .......
if __name__ == "__main__":
	__main__()