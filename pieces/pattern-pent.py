import time
import random
import math
import datetime
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageEnhance, ImageChops
from modules import colorutils, coloroverlay
import argparse



def marker(x, y, draw, f = "red"):
	draw.rectangle((x,y,x+3,y+3), fill=f)


def drawFigure(offset=(0,0), angleOffset=0, level = 0, numChildren=0, fillLevel = 0):
	if(level <= 7) :
		pointsArray = []
		#marker(offset[0] + config.offset[0],offset[1]+ config.offset[1],config.draw, "yellow")
		
		#numberChildren = config.n if level < 1 else numChildren

		start = 0
		end = config.n
		
		if fillLevel >= len(config.colorArray): fillLevel = 0

		for i in range(0, config.n) :
			angle = config.theta * i + angleOffset
			x = config.r * math.cos(angle) + config.offset[0] + offset[0]
			y = config.r * math.sin(angle) + config.offset[1] + offset[1]

			pointsArray.append((x,y))

			x1 = (config.n - 2) * config.d * math.cos(angle + config.theta/2) + offset[0]
			y1 = (config.n - 2) * config.d * math.sin(angle + config.theta/2) + offset[1]
			newOffset = (x1,y1)
			

			if level %2 > 0 :
				newAngle = angle - config.theta/2 	
				alt = 1		
			else :
				newAngle = angle + config.theta/2 
				alt = 4
			
			if (i == 0 or level < 1) and numChildren != -1:
				drawFigure(newOffset, newAngle, level + 1, numChildren, fillLevel+1)

			if level == 1 and i == 14:
				marker(x , y, config.canvasDraw)
				drawFigure(newOffset, newAngle - config.theta, level + 1, -1, fillLevel+1)

			if level == 1 and i == 1:
				marker(x , y, config.canvasDraw)
				drawFigure(newOffset, newAngle + 1 *config.theta, level + 1, -1, fillLevel+1)


		if len(pointsArray) > 0:
			config.draw.polygon(pointsArray, outline="black", fill = config.colorArray[fillLevel])


def drawPattern():

	draw = config.draw


	config.f1.stepTransition()
	config.f2.stepTransition()
	config.f3.stepTransition()
	config.f4.stepTransition()
	config.f5.stepTransition()
	config.f6.stepTransition()

	config.f1t = tuple(config.f1.currentColor)
	config.f2t = tuple(config.f2.currentColor)
	config.f3t = tuple(config.f3.currentColor)
	config.f4t = tuple(config.f4.currentColor)
	config.f5t = tuple(config.f5.currentColor)
	config.f6t = tuple(config.f6.currentColor)

	config.colorArray = [config.f1t,config.f2t,config.f3t,config.f4t,config.f5t,config.f6t]

	rows = config.rows
	cols = config.cols

	base = config.base
	exp = 0

	config.n = 5
	config.r = 12
	config.offset = (100,100)

	## Start from center for each polygon
	"sin (theta) = (r + d) / s"
	"s = 2 * r * cos(theta/2)"
	
	config.theta = 2*math.pi/config.n
	config.side = 2 * config.r * math.cos(config.theta/2)
	config.d = config.side * math.sin(config.theta) - config.r
	
	#marker(config.offset[0],config.offset[1],draw,"green")
	#drawFigure()

	drawRing()

	#renderImage.save("pattern.png")
	#print (rows, b17, cols*b17)


def drawRing():
	offset=(0,0)
	angleOffset = 0
	level = 0
	numChildren=0
	fillLevel = 0
	pointsArray = []

	for i in range(0, config.n) :
		angle = config.theta * i + angleOffset
		x = config.r * math.cos(angle) + config.offset[0] + offset[0]
		y = config.r * math.sin(angle) + config.offset[1] + offset[1]
		pointsArray.append((x,y))
	
	config.draw.polygon(pointsArray, outline="black", fill = config.colorArray[fillLevel])

def getColorChanger():
	colOverlay = coloroverlay.ColorOverlay()
	colOverlay.randomSteps = False 
	colOverlay.timeTrigger = True 
	colOverlay.tLimitBase = 10 
	colOverlay.maxBrightness = config.brightness
	colOverlay.steps = 50
	return colOverlay


def showGrid():
	global config

	config.image.paste(config.canvasImage, (0,0), config.canvasImage)
	config.render(config.image, round(config.imageOffsetX), round(config.imageOffsetY))



def main(run = True) :
	global config, directionOrder
	print("---------------------")
	print("Screen Loaded")

	colorutils.brightness = config.brightness

	config.delay = float(workConfig.get("pattern", 'delay'))
	config.base = float(workConfig.get("pattern", 'base'))
	config.rows = int(workConfig.get("pattern", 'rows'))
	config.cols = int(workConfig.get("pattern", 'cols'))


	config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	config.draw = ImageDraw.Draw(config.image)
	config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.canvasDraw = ImageDraw.Draw(config.canvasImage)

	config.imageOffsetX = 0
	config.imageOffsetY = 0

	config.f1 = getColorChanger()
	config.f2 = getColorChanger()
	config.f3 = getColorChanger()
	config.f4 = getColorChanger()
	config.f5 = getColorChanger()
	config.f6 = getColorChanger()

	config.imageRotation = .0001



	'''
	config.colOverlay.minHue = float(workConfig.get("screenproject", 'minHue'))
	config.colOverlay.maxHue = float(workConfig.get("screenproject", 'maxHue'))
	config.colOverlay.minSaturation = float(workConfig.get("screenproject", 'minSaturation'))
	config.colOverlay.maxSaturation= float(workConfig.get("screenproject", 'maxSaturation'))
	config.colOverlay.minValue = float(workConfig.get("screenproject", 'minValue'))
	config.colOverlay.maxBrightness = float(workConfig.get("screenproject", 'maxBrightness'))
	config.colOverlay.maxValue = float(workConfig.get("screenproject", 'maxValue'))

	config.crackChangeProb = float(workConfig.get("screenproject", 'crackChangeProb'))
	config.imageResetProb = float(workConfig.get("screenproject", 'imageResetProb'))
	'''



	setUp()

	#if(run) : runWork()


def setUp():
	global config
	drawPattern()


def runWork():
	global config
	while True:
		iterate()
		time.sleep(config.delay)  


def iterate() :
	global config
	drawPattern()
	showGrid()


def callBack() :
	global config
	return True




''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


	




