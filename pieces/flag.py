# ################################################### #
import time
import random
import math
import datetime
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageEnhance, ImageChops
from modules import colorutils, coloroverlay, badpixels
import argparse


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


def main(run=True):
	global config, workConfig

	config.delay = float(workConfig.get("flag", 'delay'))
	config.whiteBrightness = float(workConfig.get("flag", 'whiteBrightness'))
	config.starBrightness = float(workConfig.get("flag", 'starBrightness'))
	config.colorBrightness = float(workConfig.get("flag", 'colorBrightness'))

	config.image = Image.new("RGBA", (config.screenWidth  , config.screenHeight))
	config.draw = ImageDraw.Draw(config.image)

	config.canvasImage = Image.new("RGBA", (config.canvasWidth  , config.canvasHeight))
	config.canvasDraw = ImageDraw.Draw(config.canvasImage)

	colorutils.brightness = config.brightness
	config.colOverlay = coloroverlay.ColorOverlay()
	config.colOverlay.randomSteps = False 
	config.colOverlay.timeTrigger = True 
	config.colOverlay.tLimitBase = 5
	config.colOverlay.maxBrightness = config.brightness
	config.colOverlay.steps = 50


	config.stripeHeight = config.canvasHeight / 13
	config.redVal = (120,0,0,255)
	config.whtVal = (220,220,220,255)
	config.starWhtVal = (220,220,220,255)
	config.blueVal = (0,0,120,255)

	config.starHDis = 0.063 * config.canvasHeight
	config.starVDis = 0.054 * config.canvasHeight
	config.starDiam = 0.036 * config.canvasHeight
	config.blueWidth = config.canvasHeight * 0.76 * .8
	config.blueHeight = config.canvasHeight * 0.5385

	config.starPointsAngle = 2*math.pi/5
	config.radius = config.starDiam/2


	badpixels.numberOfDeadPixels = int(workConfig.get("flag", 'numberOfDeadPixels'))
	badpixels.config = config
	badpixels.sizeTarget = list(config.canvasImage.size)
	badpixels.setBlanksOnScreen() 
	

	if(run):
		runWork()

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def drawRects() :

	starWhtVal = tuple(round(c * config.starBrightness) for c in config.starWhtVal)
	blueVal = tuple(round(c * config.colorBrightness) for c in config.blueVal)
	redVal = tuple(round(c * config.colorBrightness) for c in config.redVal)
	whtVal = tuple(round(c * config.whiteBrightness) for c in config.whtVal)

	for s in range(0,13) :
		fillVal = redVal
		if s % 2 > 0 :
			fillVal = whtVal
		config.canvasDraw.rectangle((0, config.stripeHeight * s, config.canvasWidth, config.stripeHeight * s + config.stripeHeight), fill=fillVal)

	config.canvasDraw.rectangle((0,0,config.blueWidth,config.blueHeight), fill=blueVal)

	for r in range(0,7) :
		starsNum = 6
		offset = 0
		if r%2 > 0 :
			starsNum = 5
			offset = config.starHDis
		for s in range(0, starsNum):
			xPos = offset + config.starHDis/1.5 + (config.starHDis + config.starDiam) * s
			yPos = config.starVDis + (config.starVDis/1.5 + config.starDiam) * r
			starPoints = []
			for i in range(0,5) :
				xP = xPos + config.radius * math.cos(i * config.starPointsAngle)
				yP = yPos + config.radius * math.sin(i * config.starPointsAngle)
				starPoints.append((xP,yP))
			#config.canvasDraw.rectangle(xPos, yPos,xPos + starDiam,yPos + starDiam), fill=whtVal)
			#config.canvasDraw.chord((xPos, yPos,xPos + starDiam,yPos + starDiam),0,360, fill=whtVal)
			config.canvasDraw.polygon((starPoints[0],starPoints[2],starPoints[4],starPoints[1],starPoints[3]), 
				fill=starWhtVal)



''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


def iterate():
	global config

	drawRects()

	#config.canvasImage.paste(config.image, (0,0), config.image)
	badpixels.drawBlanks(config.canvasImage, False)
	if random.random() > .998 : badpixels.setBlanksOnScreen() 
	config.render(config.canvasImage, 0, 0, config.canvasImage)


	#config.render(config.canvasImage, 0, 0, config.image)

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def runWork():
	global config
	while True:
		iterate()
		time.sleep(config.delay)

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


def reset():
	global config

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def callBack():
	global config

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
