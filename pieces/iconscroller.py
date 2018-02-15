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

	config.msg1 = workConfig.get("scroller", 'msg1')
	config.msg2 = workConfig.get("scroller", 'msg2')
	config.msg3 = workConfig.get("scroller", 'msg3')

	config.bandHeight = int(round(config.windowHeight / config.displayRows) )

	#********* HARD CODING VALUES  ***********************
	config.bgBackGroundColor = (0,0,0,0)
	config.arrowBgBackGroundColor = (0,0,0,200)

	config.canvasImage = Image.new("RGBA", (config.canvasWidth * 10, config.canvasHeight))
	config.canvasImageDraw = ImageDraw.Draw(config.canvasImage)

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


def remakeMessage(imageRef, messageString = "FooBar", direction = 1) :
	messageString = config.msg1 if random.random() < .5 else config.msg2
	makeMessage(imageRef=imageRef, messageString=messageString, direction=direction)

def remakeArrowBlock(imageRef, direction):
	drawRef = ImageDraw.Draw(imageRef)
	makeArrows(drawRef, direction)

def remakePatternBlock(imageRef, direction):
	drawRef = ImageDraw.Draw(imageRef)
	makeBackGround(drawRef, direction)

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

	config.render(config.workImage, 0,0)

def main(run = True) :
	global config, threads, thrd
	init()
	
	if(run) : runWork()

### Kick off .......
if __name__ == "__main__":
	__main__()