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


	config.actualScreenWidth = 256


	badpixels.numberOfDeadPixels = 10
	badpixels.size = (256,256)
	badpixels.config = config
	badpixels.setBlanksOnScreen() 
	

	if(run):
		runWork()

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def drawRects() :
	stripeHeight = config.canvasHeight / 13
	redVal = (120,0,0,255)
	whtVal = (220,220,220,255)
	starWhtVal = (220,220,220,255)
	blueVal = (0,0,120,255)

	starHDis = 0.063 * config.canvasHeight
	starVDis = 0.054 * config.canvasHeight
	starDiam = 0.036 * config.canvasHeight
	blueWidth = config.canvasHeight * 0.76 * .8
	blueHeight = config.canvasHeight * 0.5385

	starPointsAngle = 2*math.pi/5
	radius = starDiam/2


	for s in range(0,13) :
		fillVal = redVal
		if s % 2 > 0 :
			fillVal = whtVal
		config.canvasDraw.rectangle((0, stripeHeight * s, config.canvasWidth, stripeHeight * s + stripeHeight), fill=fillVal)

	config.canvasDraw.rectangle((0,0,blueWidth,blueHeight), fill=blueVal)

	for r in range(0,7) :
		starsNum = 6
		offset = 0
		if r%2 > 0 :
			starsNum = 5
			offset = starHDis
		for s in range(0, starsNum):
			xPos = offset + starHDis/1.5 + (starHDis + starDiam) * s
			yPos = starVDis + (starVDis/1.5 + starDiam) * r
			starPoints = []
			for i in range(0,5) :
				xP = xPos + radius * math.cos(i * starPointsAngle)
				yP = yPos + radius * math.sin(i * starPointsAngle)
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
