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

	config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.canvasImageDraw = ImageDraw.Draw(config.canvasImage)

	config.workImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.workImageDraw = ImageDraw.Draw(config.workImage)

	config.scroller1 = continuous_scroller.ScrollObject()
	makeArrows(config.scroller1.bg1Draw)


	config.scroller2 = continuous_scroller.ScrollObject()
	config.scroller2.xSpeed = -4


def makeArrows(drawRef, n =1) :

	rows = config.patternRows * 2
	cols = config.patternCols * 2

	xDiv = config.canvasWidth / cols 
	yDiv = config.canvasHeight / rows 

	xStart = config.canvasWidth / 2
	yStart = config.canvasHeight / 2

	arrowLength = cols
	blade = cols / 3
	bufferDistance = cols - 5

	clr  = (200,0,0)

	drawRef.rectangle((0,0,config.canvasWidth, config.canvasHeight), fill = config.bgBackGroundColor)

	for c in range (0, cols) : 
		yArrowEnd = 0 #yStart + arrowLength
		xArrowEnd = xStart + arrowLength

		# the horizontal
		drawRef.line((xStart, yStart, xStart, yArrowEnd), fill = clr, width = config.lineThickness)
		# the blades
		xDisplace = 0 #blade * math.tan(math.pi/4)
		yDisplace = blade * math.tan(math.pi/4)

		#drawRef.line((xStart - xDisplace, yArrowEnd - blade, xStart, yArrowEnd), fill = clr, width = config.lineThickness)
		#drawRef.line((xStart + xDisplace, yArrowEnd - blade , xStart, yArrowEnd), fill = clr, width = config.lineThickness)
		drawRef.line((xStart - xDisplace, yArrowEnd - blade, xStart, yArrowEnd), fill = clr, width = config.lineThickness)
		drawRef.line((xStart + xDisplace, yArrowEnd - blade , xStart, yArrowEnd), fill = clr, width = config.lineThickness)
	
		#yStart += arrowLength + bufferDistance
		xStart += arrowLength + bufferDistance

def callBack() :
	global config
	pass

def runWork():
	global config
	while True:
		iterate()
		time.sleep(config.redrawSpeed)

def iterate() :
	global config

	config.workImageDraw.rectangle((0,0,config.windowWidth,config.windowHeight), fill  = (0,0,0))
	
	config.scroller1.scroll()
	config.workImage.paste(config.scroller1.canvas, (0,0), config.scroller1.canvas)

	config.scroller2.scroll()
	config.workImage.paste(config.scroller2.canvas, (0,0), config.scroller2.canvas)

	config.render(config.workImage, 0,0)

def main(run = True) :
	global config, threads, thrd
	init()
	
	if(run) : runWork()

### Kick off .......
if __name__ == "__main__":
	__main__()