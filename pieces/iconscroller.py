#!/usr/bin/python
#import modules
# ################################################### #
import os, sys, getopt, time, random, math, datetime, textwrap
import ConfigParser, io
import importlib 
import numpy
import threading
import resource
from collections import OrderedDict
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageChops, ImageEnhance
from modules import colorutils, coloroverlay, continuous_scroller

global thrd, config

def init() :
	global config
	config.redrawSpeed  = float(workConfig.get("scroller", 'redrawSpeed')) 

	config.windowWidth  = float(workConfig.get("displayconfig", 'windowWidth')) 
	config.windowHeight  = float(workConfig.get("displayconfig", 'windowHeight')) 

	config.xOffset = int(workConfig.get("scroller", 'xOffset')) 
	config.yOffset = int(workConfig.get("scroller", 'yOffset')) 

	config.displayRows = int(workConfig.get("scroller", 'displayRows'))
	config.displayCols = int(workConfig.get("scroller", 'displayCols'))

	config.patternRows = int(workConfig.get("scroller", 'patternRows'))
	config.patternCols = int(workConfig.get("scroller", 'patternCols'))
	config.arrowCols = int(workConfig.get("scroller", 'arrowCols'))

	config.lineThickness = int(workConfig.get("scroller", 'lineThickness'))
	config.colorMode = workConfig.get("scroller", 'colorMode')
	config.sansSerif = workConfig.getboolean("scroller", 'sansSerif')
	config.fontSize =  int(workConfig.get("scroller", 'fontSize'))
	config.textVOffest = int(workConfig.get("scroller", 'textVOffest'))
	config.shadowSize = int(workConfig.get("scroller", 'shadowSize'))

	config.patternRows = int(workConfig.get("scroller", 'patternRows'))
	config.patternCols = int(workConfig.get("scroller", 'patternCols'))
	config.patternRowsOffset = int(workConfig.get("scroller", 'patternRowsOffset'))
	config.patternColsOffset = int(workConfig.get("scroller", 'patternColsOffset'))
	config.patternDrawProb = float(workConfig.get("scroller", 'patternDrawProb')) 
	config.bgBackGroundColor = (workConfig.get("scroller", 'bgBackGroundColor').split(","))
	config.bgBackGroundColor = tuple([int(i) for i in config.bgBackGroundColor])
	config.bgForeGroundColor = (workConfig.get("scroller", 'bgForeGroundColor').split(","))
	config.bgForeGroundColor = tuple([int(i) for i in config.bgForeGroundColor])

	config.patternSpeed = int(workConfig.get("scroller", 'patternSpeed'))
	config.textSpeed = int(workConfig.get("scroller", 'textSpeed'))
	config.arrowSpeed = int(workConfig.get("scroller", 'arrowSpeed'))
	config.greyLevel = int(workConfig.get("scroller", 'greyLevel'))
	config.redShift = int(workConfig.get("scroller", 'redShift'))

	config.imageSpeed = int(workConfig.get("scroller", 'imageSpeed'))
	config.flip = False
	config.xVariance = int(workConfig.get("scroller", 'xVariance'))
	config.blockWidth = int(workConfig.get("scroller", 'blockWidth'))
	config.l1Variance = int(workConfig.get("scroller", 'l1Variance'))
	config.angleRotationRange = int(workConfig.get("scroller", 'angleRotationRange'))
	
	config.bgR = int(workConfig.get("scroller", 'bgR'))
	config.bgG = int(workConfig.get("scroller", 'bgG'))
	config.bgB = int(workConfig.get("scroller", 'bgB'))
	config.fade = int(workConfig.get("scroller", 'fade'))

	config.msg1 = workConfig.get("scroller", 'msg1')
	config.msg2 = workConfig.get("scroller", 'msg2')
	config.msg3 = workConfig.get("scroller", 'msg3')

	config.useOverLayImage = workConfig.getboolean("scroller", 'useOverLayImage')
	config.overLayImage = workConfig.get("scroller", 'overLayImage')
	config.overLayXPos = int(workConfig.get("scroller", 'overLayXPos'))
	config.overLayYPos = int(workConfig.get("scroller", 'overLayYPos'))

	config.bandHeight = int(round(config.windowHeight / config.displayRows) )

	#********* HARD CODING VALUES  ***********************
	config.bgBackGroundColor = (0,0,0,0)
	config.arrowBgBackGroundColor = (0,0,0,200)

	config.canvasImage = Image.new("RGBA", (config.canvasWidth * 10, config.canvasHeight))
	config.canvasImageDraw = ImageDraw.Draw(config.canvasImage)	

	config.imageLayer = Image.new("RGBA", (config.canvasWidth , config.canvasHeight))
	config.imageLayerDraw = ImageDraw.Draw(config.canvasImage)

	config.workImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.workImageDraw = ImageDraw.Draw(config.workImage)

	## Set up the scrolling layers
	config.scrollArray = []

	config.scroller4 = continuous_scroller.ScrollObject()
	scrollerRef = config.scroller4
	scrollerRef.canvasWidth = int(config.displayRows * config.windowWidth)
	scrollerRef.xSpeed = config.patternSpeed
	scrollerRef.setUp()
	direction = 1 if scrollerRef.xSpeed > 0 else -1
	scrollerRef.callBack = {"func" : remakePatternBlock, "direction" : direction}
	#makeBackGround(scrollerRef.bg1Draw, 1)
	makeBackGround(scrollerRef.bg2Draw, 1)
	config.scrollArray.append(scrollerRef)

	config.scroller1 = continuous_scroller.ScrollObject()
	scrollerRef = config.scroller1
	scrollerRef.canvasWidth = int(config.displayRows * config.windowWidth)
	scrollerRef.xSpeed = config.arrowSpeed
	scrollerRef.setUp()
	direction = 1 if scrollerRef.xSpeed > 0 else -1
	scrollerRef.callBack = {"func" : remakeArrowBlock, "direction" : direction}
	makeArrows(scrollerRef.bg1Draw, 1)
	makeArrows(scrollerRef.bg2Draw, 1)
	config.scrollArray.append(scrollerRef)

	'''
	config.scroller5 = continuous_scroller.ScrollObject()
	scrollerRef = config.scroller5
	scrollerRef.canvasWidth = int(config.displayRows * config.windowWidth)
	scrollerRef.canvasHeight = int(config.windowHeight)
	scrollerRef.xSpeed = config.imageSpeed
	scrollerRef.setUp()
	direction = 1 if scrollerRef.xSpeed > 0 else -1
	scrollerRef.callBack = {"func" : remakeImageBlock, "direction" : direction}
	#makeAnimal(config.imageLayer,scrollerRef.bg1Draw, 1)
	makeAnimal(config.imageLayer,scrollerRef.bg2Draw, 1)
	config.scrollArray.append(scrollerRef)
	'''

	config.scroller2 = continuous_scroller.ScrollObject()
	scrollerRef = config.scroller2
	scrollerRef.canvasWidth = int(config.displayRows * config.windowWidth)
	scrollerRef.xSpeed = -config.textSpeed
	scrollerRef.setUp()
	direction = 1 if scrollerRef.xSpeed > 0 else -1
	makeMessage(scrollerRef.bg1,config.msg1, direction)
	makeMessage(scrollerRef.bg2,config.msg2, direction)
	scrollerRef.callBack = {"func" : remakeMessage, "direction" : direction}
	config.scrollArray.append(scrollerRef)

	config.scroller3 = continuous_scroller.ScrollObject()
	scrollerRef = config.scroller3
	scrollerRef.canvasWidth = int(config.displayRows * config.windowWidth)
	scrollerRef.xSpeed = config.textSpeed + 1
	scrollerRef.setUp()
	direction = 1 if scrollerRef.xSpeed > 0 else -1
	makeMessage(scrollerRef.bg1,config.msg1, direction)
	makeMessage(scrollerRef.bg2,config.msg2, direction)
	scrollerRef.callBack = {"func" : remakeMessage, "direction" : direction}
	config.scrollArray.append(scrollerRef)

	if(config.useOverLayImage ==  True) :
		arg = "."+config.overLayImage
		config.loadedImage = Image.open(arg , "r")
		config.loadedImage.load()


def remakeMessage(imageRef, messageString = "FooBar", direction = 1) :
	messageString = config.msg1 if random.random() < .5 else config.msg2
	makeMessage(imageRef=imageRef, messageString=messageString, direction=direction)

def remakeArrowBlock(imageRef, direction):
	drawRef = ImageDraw.Draw(imageRef)
	makeArrows(drawRef, direction)

def remakePatternBlock(imageRef, direction):
	drawRef = ImageDraw.Draw(imageRef)
	makeBackGround(drawRef, direction)

def remakeImageBlock(imageRef, direction):
	drawRef = ImageDraw.Draw(imageRef)
	makeAnimal(imageRef, drawRef, direction)

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

def makeAnimal(imageRef, imageDrawRef, direction):
	global config

	#config.imageLayerDraw.rectangle((0,0,config.canvasWidth, config.canvasHeight), fill = (0,0,0,config.alpha))
	imageDrawRef.rectangle((0,0,config.canvasWidth,config.canvasHeight), fill=(config.bgR, config.bgG, config.bgB,config.fade))
	#config.pixSortXOffset = config.pixSortXOffsetVal 

	imgWidth = config.canvasWidth
	imgHeight = config.canvasHeight
	gray0 = 0
	gray1 = 30
	gray2 = 100
	fills = [(gray0,gray0,gray0,255),(gray1,gray1,gray1,255)]
	fills = [(gray0,gray0,gray0,255),(gray2,gray0,gray0,255)]
	
	
	quadBlocks =  {
	"tail":	{"order":3, "proportions":[1,1.5] ,"coords":[]},
	"l1":	{"order":1, "proportions":[3,2] ,"coords":[]},
	"l2":	{"order":2, "proportions":[3.2,2] ,"coords":[]},
	"head":	{"order":5, "proportions":[3,3.67],"coords":[]},
	"body":	{"order":4, "proportions":[5.5,11],"coords":[]},
	}
	quadBlocks = OrderedDict(sorted(quadBlocks.items(), key=lambda t: t[1]))

	numSquarePairs = len(quadBlocks)

	# Choose seam x point  -- ideally about 1/3 from left
	xVariance = config.xVariance
	flip = config.flip
	
	blockWidth = config.blockWidth
	wVariance = [imgWidth/6, imgWidth/3]
	hVariance = [imgHeight/6, imgHeight/2]
	wFactor = 1
	hFactor = 2
	l1Variance = config.l1Variance

	yStart = yPos = config.yOffset
	xStart = xPos = imgWidth/2 - config.xOffset

	bodyEnd = 0
	bodyStart = 0
	tiedToBottom = 0 if random.random() < .5 else 2
	for i in range(0,50) :

		#xStart =  i *30

		angleRotation = random.uniform(-config.angleRotationRange,config.angleRotationRange)

		bodyWidth = quadBlocks["body"]["proportions"][0] * blockWidth * random.uniform(.9,1.25)
		bodyLength = quadBlocks["body"]["proportions"][1] * blockWidth * random.uniform(.9,1.2)

		tailWidth = quadBlocks["tail"]["proportions"][0] * blockWidth * random.uniform(.9,1.2)
		tailLength = quadBlocks["tail"]["proportions"][1] * blockWidth * random.uniform(.9,1.2)

		headWidth = quadBlocks["head"]["proportions"][0] * blockWidth * random.uniform(.9,1.2)
		headLength = quadBlocks["head"]["proportions"][1] * blockWidth * random.uniform(.9,1.2)

		legWidth = quadBlocks["l1"]["proportions"][0] * blockWidth * random.uniform(.9,1.2)
		legLength = quadBlocks["l1"]["proportions"][1] * blockWidth * random.uniform(.9,1.2)

		xOffsetVal = random.uniform(.9,1.2)
		xOffsetVal = 1

		quad = "l1"
		x1 = xStart * xOffsetVal
		y1 = yStart * random.uniform(.9,1.2)
		x2 = x1 + legWidth + l1Variance
		y2 = y1 + legLength
		quadBlocks[quad]["coords"] = [x1,y1,x2,y2]

		#config.pixSortXOffset *= xOffsetVal

		quad = "l2"
		x1 = quadBlocks["l1"]["coords"][0] - l1Variance
		y1 = yStart + bodyLength  - legLength * random.uniform(.9,1.2)
		x2 = x1 + legWidth + l1Variance
		y2 = y1 + legLength 
		quadBlocks[quad]["coords"] = [x1,y1,x2,y2]

		quad = "tail"
		x1 = quadBlocks["l1"]["coords"][2] + bodyWidth - tailWidth - l1Variance
		y1 = yStart * random.uniform(.9,1.2) - tailLength/4 * random.uniform(1.05,1.3)
		x2 = x1 + tailWidth
		y2 = y1 + tailLength
		quadBlocks[quad]["coords"] = [x1,y1,x2,y2]

		quad = "body"
		x1 = quadBlocks["l1"]["coords"][2] - l1Variance
		y1 = quadBlocks["l1"]["coords"][1]
		x2 = x1 + bodyWidth
		y2 = y1 + bodyLength
		quadBlocks[quad]["coords"] = [x1,y1,x2,y2]

		quad = "head"
		x1 = quadBlocks["body"]["coords"][2] - headWidth
		y1 = quadBlocks["body"]["coords"][3] - tailLength/2 * random.uniform(.9,1.2)
		x2 = x1 + headWidth
		y2 = y1 + headLength
		quadBlocks[quad]["coords"] = [x1,y1,x2,y2]

		tempUnit = Image.new("RGBA", (imgWidth, imgHeight))
		n = 0
		for quad in quadBlocks:

			if(random.random() < .5 and quad != "body") : 
				angleRotation = random.uniform(-config.angleRotationRange/2,config.angleRotationRange/2)

			gray0 = int(random.uniform(0,config.greyLevel) * config.brightness)
			gray1 = int(random.uniform(0,config.greyLevel) * config.brightness)
			gray2 = int(random.uniform(0,config.greyLevel) * config.brightness)
			redShift = config.redShift
			fills = [(gray0 + redShift,gray1,gray1,255),(gray1 + redShift,gray1,gray1,255),(gray2 + redShift,gray2,gray2,255)]
			
			#fills = [colorutils.getRandomColor(config.brightness),colorutils.getRandomColor(config.brightness),colorutils.getRandomColor(config.brightness)]

			temp = Image.new("RGBA", (imgWidth, imgHeight))
			drawtemp = ImageDraw.Draw(temp)
			fillIndex = n
			if n >= len(fills) : fillIndex = n - len(fills)

			x1 = quadBlocks[quad]["coords"][0]
			y1 = quadBlocks[quad]["coords"][1]
			x2 = quadBlocks[quad]["coords"][2]
			y2 = quadBlocks[quad]["coords"][3]


			drawtemp.rectangle((x1,y1,x2,y2), fill=fills[fillIndex])
			temp = ScaleRotateTranslate(temp,angleRotation, None, None, None, True)
			#config.workImage.paste(temp, temp)
			tempUnit.paste(temp, temp)
			n += 1

		#tempUnit = ScaleRotateTranslate(tempUnit, 90, None, None, None, True)
		tempUnit = ScaleRotateTranslate(tempUnit, 90, None, None, None, True)
		imageRef.paste(tempUnit,(i * 50,0), tempUnit)
		#config.workImage.paste(temp, temp)
	imageRef = ScaleRotateTranslate(imageRef,90, None, None, None, False)

	if(random.random() < 0) : flip = True
	
	if(flip == True) :
		imageRef = imageRef.transpose(Image.FLIP_TOP_BOTTOM)
		imageRef = imageRef.transpose(Image.ROTATE_180)

def makeArrows(drawRef, direction = 1) :

	rows = config.patternRows * 2
	cols = config.arrowCols * 2

	xDiv = int(config.displayRows * config.windowWidth) / cols 
	yDiv = config.canvasHeight / rows 

	xStart = 0 #config.canvasWidth / 2
	yStart = config.bandHeight / 2 #config.canvasHeight / 2

	bufferDistance = 15
	arrowLength = cols * 2
	blade = cols / 3

	clr  = (200,0,0)

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

def makeMessage(imageRef, messageString = "FooBar", direction = 1):
	global config
	scrollSpeed = 0.004
	steps = 1
	fontSize = 14

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

def makeBackGround(drawRef, n = 1):
	rows = config.patternRows * 2
	cols = config.patternCols * 2

	xDiv = int(round(config.displayRows * config.windowWidth)) / cols #- config.patternColsOffset
	yDiv = config.canvasHeight / rows #- config.patternRowsOffset

	xStart = 0
	yStart = 0

	config.arrowBgBackGroundColor = (0,0,0,220) #colorutils.getRandomColor()

	drawRef.rectangle((0,0,int(round(config.displayRows * config.windowWidth)), config.canvasHeight), fill = config.arrowBgBackGroundColor)

	## Chevron pattern
	## config.bgForeGroundColor
	fillClr = colorutils.getRandomColor(config.brightness/2)
	for r in range (0, rows) : 
		for c in range (0, cols) : 
			poly = []
			poly.append((xStart, yStart + yDiv))
			poly.append((xStart + xDiv, yStart))
			poly.append((xStart + xDiv + xDiv, yStart + yDiv))
			poly.append((xStart + xDiv, yStart + yDiv + yDiv))
			#if(n ==2) : color = (100,200,0,255)
			if(random.random() < config.patternDrawProb) :
				drawRef.polygon(poly, fill = fillClr) #outline = (15,15,15)
			xStart += 2 * xDiv
		xStart = 0
		yStart += 2 * yDiv

def runWork():
	global config
	while True:
		iterate()
		time.sleep(config.redrawSpeed)

def iterate() :
	global config

	config.workImageDraw.rectangle((0,0,config.windowWidth,config.windowHeight), fill  = (0,0,0))
	config.canvasImageDraw.rectangle((0,0,config.windowWidth*10,config.windowHeight), fill  = (0,0,0))

	for scrollerObj in config.scrollArray :
		scrollerObj.scroll()
		config.canvasImage.paste(scrollerObj.canvas, (0,0), scrollerObj.canvas)

	#segmentHeight = int(config.canvasHeight / config.displayRows)
	#segmentWidth = config.canvasWidth	
	# Chop up the scrollImage into "rows"
	for n in range(0, config.displayRows) :
		segment = config.canvasImage.crop((n * config.windowWidth, 0, config.windowWidth + n * config.windowWidth, config.bandHeight))
		# At some point go to modulo for even/odd ... but for now not more than 5 rows
		if ((n == 0 or n == 2 or n == 4) and (config.displayRows >  1) ) :
			segment = ImageOps.flip(segment)
			segment = ImageOps.mirror(segment)
		config.workImage.paste(segment, (0, n * config.bandHeight))

	if(config.useOverLayImage  ==  True) :
		config.workImage.paste(config.loadedImage, (config.overLayXPos, config.overLayYPos), config.loadedImage)
	config.render(config.workImage, 0,0)

def main(run = True) :
	global config, threads, thrd
	init()
	
	if(run) : runWork()

### Kick off .......
if __name__ == "__main__":
	__main__()