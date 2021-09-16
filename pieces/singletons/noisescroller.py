# ################################################### #
import argparse
import math
import random
import time
import types
import noise
from noise import *
from modules.configuration import bcolors
from modules import badpixels, coloroverlay, colorutils, panelDrawing
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps

import numpy as np

lastRate = 0
colorutils.brightness = 1

def getColor(r,g,b,a) :
	clr = list( round(i * config.brightness) for i in [r,g,b])
	clr.append(a)

	return tuple(clr)


def reDraw():
	if config.function == "wavey" :
		wavey()
	if config.function == "ringLines" :
		ringLines()
	if config.function == "rings" :
		rings()
	if config.function == "waves" :
		waves()


def ringLinesNoLoop():
	global config

	config.draw.rectangle((0,0,500,500), fill=config.bgColor)
	gDelta = 1 + 1/config.rgbSplitFactor
	bDelta = 1 + 1/config.rgbSplitFactor + 1/config.rgbSplitFactor

	lastx = [config.xOffset,config.xOffset,config.xOffset]
	lasty = [config.yOffset,config.yOffset,config.yOffset]


	for row in range(0,config.numRings):
		points = config.pointsMin + row * config.pointsMin
		rads = 2 * math.pi / points
		ra = config.radiusMin * row + config.radiusMin
		for col in range(0,points):
			x = math.cos(col * rads) * ra + config.xOffset
			y = math.sin(col * rads) * ra + config.yOffset

			yChange1 = noise.pnoise2(x/config.rowFactor, (y + config.scroll)/config.colFactor/1, 1) * config.amplitude + row
			yChange2 = noise.pnoise2(x/config.rowFactor, (y + config.scroll)/config.colFactor/gDelta, 1) * config.amplitude + row
			yChange3 = noise.pnoise2(x/config.rowFactor, (y + config.scroll)/config.colFactor/bDelta, 1) * config.amplitude + row
			
			if config.drawOptimize == True :
				doDraw =  False
			else :
				doDraw = True 

			if x > 0  and x < config.canvasWidth-config.xOffset and (y + yChange1)  > 0 and (y + yChange1) <  config.canvasHeight:
				doDraw = True

			if doDraw == True:

				config.draw.line((lastx[0],lasty[0], x, y + yChange1), fill=getColor(255,0,10,250))
				config.draw.line((lastx[0],lasty[0], x, y + yChange2), fill=getColor(200,120,10,255))
				config.draw.line((lastx[0],lasty[0], x, y + yChange3), fill=getColor(52,0,250,155))

				if random.random() < .99:
					config.draw.line((lastx[0],lasty[0], x, y + yChange1), fill=getColor(125,125,125,250))
					config.draw.line((lastx[0],lasty[0], x, y + yChange2), fill=getColor(25,25,25,255))
					config.draw.line((lastx[0],lasty[0], x, y + yChange3), fill=getColor(5,5,5,155))
					
				lastx = [x,x,x]
				lasty = [y + yChange1,y + yChange2,y + yChange3]

		#octv += 1
	config.scroll += config.scrollRate


def ringLines():
	global config
	config.draw.rectangle((0,0,500,500), fill=config.bgColor)
	gDelta = 1 + 1/config.rgbSplitFactor
	bDelta = 1 + 1/config.rgbSplitFactor + 1/config.rgbSplitFactor

	lastx = [config.xOffset,config.xOffset,config.xOffset]
	lasty = [config.yOffset,config.yOffset,config.yOffset]


	config.scrollAngle += config.scrollRate
	if config.scrollAngle >= math.pi * 2 :
		config.scrollAngle = config.scrollRate
		print("now")
		config.draw.rectangle((100,100, 120,120), fill=getColor(0,250,0,255), outline=None)
		#print(lastx[0],lasty[0])

	config.scrollx = config.radiusVal * math.sin(config.scrollAngle)
	config.scrolly = config.radiusVal * math.cos(config.scrollAngle)
	config.frameCount += 1

	#print(config.scrollAngle)


	row = 1
	rads = 2 * math.pi / config.numRings
	ra = config.radiusMin * 1 + config.radiusMin
	for col in range(0,config.numRings):
		x = math.cos(col * rads) * ra + config.xOffset
		#x = col + config.xOffset
		y = math.sin(col * rads) * ra + config.yOffset

		yChange1 = noise.pnoise2(0 + x + config.scrollx, (config.scrolly + y)/1, 1) * config.amplitude + row
		yChange2 = noise.pnoise2(0 + config.scrollx, (0 + config.scrolly)/gDelta, 1) * config.amplitude + row
		yChange3 = noise.pnoise2(0 + config.scrollx, (0 + config.scrolly)/bDelta, 1) * config.amplitude + row

		#yChange1 = 20
		
		if config.drawOptimize == True :
			doDraw =  False
		else :
			doDraw = True 

		if x > 0  and x < config.canvasWidth-config.xOffset and (y + yChange1)  > 0 and (y + yChange1) <  config.canvasHeight:
			doDraw = True

		if doDraw == True:

			xPos = (config.radiusMin + yChange1) * math.cos(col * rads) * 2 + config.xOffset
			yPos = (config.radiusMin + yChange1) * math.sin(col * rads) * 2 + config.yOffset

			if col != 0 :
				config.draw.line((lastx[0],lasty[0], xPos, yPos), fill=getColor(255,100,0,50))
			config.draw.rectangle((xPos-1,yPos-1, xPos + 0,yPos + 0 ), fill=getColor(100,250,0,255), outline=None)
			#config.draw.line((lastx[0],lasty[0], x, y + yChange2), fill=getColor(200,120,10,255))
			#config.draw.line((lastx[0],lasty[0], x, y + yChange3), fill=getColor(52,0,250,155))

			#if random.random() > .99:
				#config.draw.line((lastx[0],lasty[0], x, y + yChange1), fill=getColor(125,125,125,250))
				#config.draw.line((lastx[0],lasty[0], x, y + yChange2), fill=getColor(25,25,25,255))
				#config.draw.line((lastx[0],lasty[0], x, y + yChange3), fill=getColor(5,5,5,155))
			

			lastx = [xPos,xPos,xPos]
			lasty = [yPos,yPos,yPos]




def rings():
	global config
	config.draw.rectangle((0,0,500,500), fill=config.bgColor)
	gDelta = 1 + 1/config.rgbSplitFactor
	bDelta = 1 + 1/config.rgbSplitFactor + 1/config.rgbSplitFactor

	for row in range(0,config.numRings):
		points = config.pointsMin + row * config.pointsMin
		rads = 2 * math.pi / points
		ra = config.radiusMin * row + config.radiusMin
		for col in range(0,points):
			x = math.cos(col * rads) * ra + config.xOffset
			y = math.sin(col * rads) * ra + config.yOffset

			yChange1 = noise.pnoise2(x/config.rowFactor, (y + config.scroll)/config.colFactor/1, 1) * config.amplitude + row
			yChange2 = noise.pnoise2(x/config.rowFactor, (y + config.scroll)/config.colFactor/gDelta, 1) * config.amplitude + row
			yChange3 = noise.pnoise2(x/config.rowFactor, (y + config.scroll)/config.colFactor/bDelta, 1) * config.amplitude + row
			
			if config.drawOptimize == True :
				doDraw =  False
			else :
				doDraw = True 

			if x > 0  and x < config.canvasWidth-config.xOffset and (y + yChange1)  > 0 and (y + yChange1) <  config.canvasHeight:
				doDraw = True

			if doDraw == True:
				if config.markSize == 1 :
					config.draw.rectangle((x, y + yChange1, x+0, y + yChange1 +0), fill=getColor(255,0,100,255), outline=None)
					config.draw.rectangle((x, y + yChange2, x+0, y + yChange2 +0), fill=getColor(0,255,0,255), outline=None)
					config.draw.rectangle((x, y + yChange3, x+0, y + yChange3 +0), fill=getColor(0,0,255,255), outline=None)
				else:
					config.draw.ellipse((x, y + yChange2, x+config.markSize, y + yChange1 +config.markSize), fill=getColor(255,0,0,255), outline=None)
					config.draw.ellipse((x, y + yChange2, x+config.markSize, y + yChange2 +config.markSize), fill=getColor(0,255,0,255), outline=None)
					config.draw.ellipse((x, y + yChange3, x+config.markSize, y + yChange3 +config.markSize), fill=getColor(0,0,255,255), outline=None)
		#octv += 1
	config.scroll += config.scrollRate

def wavey():
	global config
	config.draw.rectangle((0,0,500,500), fill=config.bgColor)
	octv = 1
	lastx = [0,0,0]
	for col in range(0,config.canvasWidth*1,2):
		lasty = [0,0,0]
		for row in range(0,config.canvasHeight,8):
			y = row
			x = round(noise.pnoise2((col +config.scroll)/config.colFactor/3, (y )/config.rowFactor/1, 1) * config.amplitude + col)

			r = round(math.sin((y/config.colFactor)+.1) * 200)
			g = round(math.sin((col/config.rowFactor)+.1) * 100)
			#g = round(math.sin((x/config.rowFactor)+.1) * 200)
			b = round(math.sin((x/config.rowFactor)+.1) * 100)
			#config.draw.rectangle((x, y, x+1, y+1), fill=(r,g,b,150))
			if col != 0 :
				config.draw.line((lastx[0],lasty[0],x,y), fill = getColor(r,g,b,150))
			lastx = [x,x,x]
			lasty = [y,y,y]
		#octv += 1
	config.scroll += config.scrollRate

def waves():
	global config
	config.draw.rectangle((0,0,500,500), fill=config.bgColor)
	octv = 1
	lastx = [0,0,0]
	lasty = [0,0,0]
	for row in range(0,config.canvasHeight,4):
		for col in range(0,config.canvasWidth):
			x = col 
			y = noise.pnoise2(row/config.rowFactor + random.random()*.0, (col+ config.scroll)/config.colFactor + random.random()*.0, octv) * config.amplitude + row

			r = 255
			g = round(math.sin((col/config.rowFactor)+.1) * 200)
			b = 50
			#config.draw.rectangle((x, y, x+1, y+1), fill=(r,g,b,150))
			if col != 0 :
				config.draw.line((lastx[0],lasty[0],x,y), fill = getColor(r,g,b,150))
			lastx = [x,x,x]
			lasty = [y,y,y]
		#octv += 1
	config.scroll += config.scrollRate




def runWork():
	global config
	print(bcolors.OKGREEN + "** " + bcolors.BOLD)
	print("Running woodyscroller.py")
	print(bcolors.ENDC)

	while config.isRunning == True:
		iterate()
		time.sleep(config.redrawSpeed)
		if config.standAlone == False :
			config.callBack()
			

def iterate():
	reDraw()

	########### RENDERING AS A MOCKUP OR AS REAL ###########
	if config.useDrawingPoints == True :
		config.panelDrawing.canvasToUse = config.image
		config.panelDrawing.render()
	else :
		config.render(config.image, 0, 0, config.screenWidth, config.screenHeight)
	# Done


def main(run=True):
	global config
	
	config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.draw = ImageDraw.Draw(config.image)


	config.redrawSpeed = float(workConfig.get("noisescroller", "redrawSpeed"))
	config.amplitude = float(workConfig.get("noisescroller", "amplitude"))
	config.rowFactor = float(workConfig.get("noisescroller", "rowFactor"))
	config.colFactor = float(workConfig.get("noisescroller", "colFactor"))
	config.rgbSplitFactor = float(workConfig.get("noisescroller", "rgbSplitFactor"))

	config.numRings = int(workConfig.get("noisescroller", "numRings"))
	config.pointsMin = int(workConfig.get("noisescroller", "pointsMin"))
	config.xOffset = int(workConfig.get("noisescroller", "xOffset"))
	config.yOffset = int(workConfig.get("noisescroller", "yOffset"))
	config.radiusMin = int(workConfig.get("noisescroller", "radiusMin"))
	config.markSize = int(workConfig.get("noisescroller", "markSize"))
	config.scroll = 0

	config.function = (workConfig.get("noisescroller", "function"))

	config.bgColorVals = (workConfig.get("noisescroller", "bgColor")).split(",")
	config.bgColor = tuple(map(lambda x: round(float(x) * config.brightness), config.bgColorVals))

	config.scrollRate = float(workConfig.get("noisescroller", "scrollRate"))

	config.frames =  300
	config.radiusVal = 1
	config.animationDuration = 6
	config.scrollRate = 2 * math.pi / config.frames
	config.frameCount = 0 
	config.animationRev = 0
	config.scrollAngle = 0


		#octv += 1

	print (config.scrollRate)

	try:
		config.drawOptimize = workConfig.getboolean("noisescroller", "drawOptimize")
	except Exception as e:
		print(str(e))
		config.drawOptimize = False

	### THIS IS USED AS WAY TO MOCKUP A CONFIGURATION OF RECTANGULAR PANELS
	panelDrawing.mockupBlock(config, workConfig)
	#### Need to add something like this at final render call  as well
	''' 
		########### RENDERING AS A MOCKUP OR AS REAL ###########
		if config.useDrawingPoints == True :
			config.panelDrawing.canvasToUse = config.renderImageFull
			config.panelDrawing.render()
		else :
			#config.render(config.canvasImage, 0, 0, config.canvasWidth, config.canvasHeight)
			#config.render(config.image, 0, 0)
			config.render(config.renderImageFull, 0, 0)
	'''

	if run:
		runWork()
