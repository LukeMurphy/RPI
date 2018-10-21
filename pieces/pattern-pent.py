import time
import random
import math
import datetime
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageEnhance, ImageChops
from modules import colorutils, coloroverlay
import argparse
from threading import Timer


def marker(x, y, draw, f="red"):
	draw.rectangle((x, y, x + 3, y + 3), fill=f)


def getColorChanger():
	colOverlay = coloroverlay.ColorOverlay()
	colOverlay.randomSteps = False 
	colOverlay.timeTrigger = True 
	colOverlay.tLimitBase = 10 
	colOverlay.maxBrightness = config.brightness
	colOverlay.steps = 50
	return colOverlay


def drawFigure(offset=(0, 0), angleOffset=0, level=0, numChildren=0, fillLevel=0):
	if(level <= 7):
		pointsArray = []
		#marker(offset[0] + config.offset[0],offset[1]+ config.offset[1],config.draw, "yellow")

		#numberChildren = config.n if level < 1 else numChildren

		start = 0
		end = config.n

		if fillLevel >= len(config.colorArray):
			fillLevel = 0

		for i in range(0, config.n):
			angle = config.theta * i + angleOffset
			x = config.r * math.cos(angle) + config.offset[0] + offset[0]
			y = config.r * math.sin(angle) + config.offset[1] + offset[1]

			pointsArray.append((x, y))

			x1 = (config.n - 2) * config.d * math.cos(angle + config.theta / 2) + offset[0]
			y1 = (config.n - 2) * config.d * math.sin(angle + config.theta / 2) + offset[1]
			newOffset = (x1, y1)

			if level % 2 > 0:
				newAngle = angle - config.theta / 2
				alt = 1
			else:
				newAngle = angle + config.theta / 2
				alt = 4

			if (i == 0 or level < 1) and numChildren != -1:
				drawFigure(newOffset, newAngle, level + 1, numChildren, fillLevel + 1)

			if level == 1 and i == 14:
				marker(x, y, config.canvasDraw)
				drawFigure(newOffset, newAngle - config.theta, level + 1, -1, fillLevel + 1)

			if level == 1 and i == 1:
				marker(x, y, config.canvasDraw)
				drawFigure(newOffset, newAngle + 1 * config.theta, level + 1, -1, fillLevel + 1)

		if len(pointsArray) > 0:
			config.draw.polygon(pointsArray, outline="black", fill=config.colorArray[fillLevel])


def drawPattern():

	draw = config.draw
	config.colorArray = []

	for i in config.colorArrayBase :
		i.stepTransition()
		config.colorArray.append(tuple(i.currentColor))

	'''
	rows = config.rows
	cols = config.cols

	base = config.base
	exp = 0
	'''

	# marker(config.offset[0],config.offset[1],draw,"green")
	#drawFigure()

	drawConcentricRings()
	drawTheReal()

	# renderImage.save("pattern.png")



def drawTheReal() :
	x = config.blockDims[0]
	y = config.blockDims[1]
	w = config.blockDims[2] + x
	h = config.blockDims[3] + y
	box = tuple([x, y, w, h])
	config.canvasDraw.rectangle(box, fill = tuple(config.f2.currentColor))


	lines = h - y
	for i in range(0, lines, config.blockSteps)  :
		f =  tuple(config.f1.currentColor)
		if random.random() < .001 :
			f = colorutils.randomColor(1)
			f = tuple(config.f4.currentColor)
		config.canvasDraw.rectangle((x,y+i,w,y+i+config.blockLineHeight) , fill = f)


def resetPause() :
	config.paused = False
	
	#config.turnRateLimPlus = random.uniform(1,3)
	#config.turnRateLimNeg = random.uniform(config.turnRateLimPlus-1 ,config.turnRateLimPlus - 3)


def drawConcentricRings():
	offset = (0, 0)
	angleOffset = 0
	level = 0
	numChildren = 0
	fillLevel = 0

	figs = config.repeatFigures
	config.r = 200

	"Ideally, make the rate of change sinusoidal - i.e. change the rate\
	gradually over time so there are smooth transitions back and forth"

	'''
	config.angle += config.angleIncrement
	if config.angle == 0 or config.angle == math.pi or config.angle == 2*math.pi :
		pass
	else :
		m = 2
		#x = m - abs(i % (2*m) - m)
		#rate = m - abs(math.sin(config.angle) % 2*m - m) + .8
		rate = m - abs((config.angle) % 2*m - m) + .9
	'''

	if random.random() > .99 :
		config.turnRateChange = random.uniform(.5,3) / config.turnRateFactor



	if config.paused == False :
		config.turnRate += config.turnRateChange * config.turnRateDirection
		#config.turnRate = rate 
		
		if config.turnRate > config.turnRateLimPlus :


			config.turnRateDirection = -1
			config.turnRate = config.turnRateLimPlus

			#config.paused = True
			d = random.uniform(.5,2)
			t1 = Timer(d, resetPause)
			#t1.start()

		if config.turnRate < config.turnRateLimNeg:
			config.turnRateDirection = 1

			#config.paused = True
			d = random.uniform(.5,2)
			t = Timer(d,resetPause)
			#t.start()
		


	f = 0
	for figures in range(0, figs):

		figureAngle = 0 * figures 
		figx = 0
		figy = 0
		figureAngleOffset = config.theta/config.turnRate * figures

		config.r*= config.reduceRate/config.phi

		pointsArray = []

		for i in range(0, config.n):
			angle = config.theta * i + figureAngleOffset
			x = config.r * math.cos(angle) + config.offset[0] + figx
			y = config.r * math.sin(angle) + config.offset[1] + figy
			pointsArray.append((x,y))

		config.draw.polygon(pointsArray, outline=None, fill = config.colorArray[f])

		f += 1
		if f >= config.colorRep : f = 0



def drawRings():
	offset = (0, 0)
	angleOffset = 0
	level = 0
	numChildren = 0
	fillLevel = 0

	for ring in range(0, 4):

		if ring == 0 : 
			figs = 1
			figTheta = config.theta
		if ring == 1 : 
			figs = 5
			figTheta = config.theta
		if ring > 1 : 
			figs = 10
			figTheta = config.theta/2

		r = ring * config.d * 3


		for figures in range(0, figs):

			figureAngle = figTheta * figures - config.theta/2 * ring
			figx = r * math.cos(figureAngle)
			figy = r * math.sin(figureAngle)
			figureAngleOffset = config.theta/2 * ring

			pointsArray = []

			for i in range(0, config.n):
				angle = config.theta * i + figureAngleOffset
				x = config.r * math.cos(angle) + config.offset[0] + figx
				y = config.r * math.sin(angle) + config.offset[1] + figy
				pointsArray.append((x,y))

			if ring  == 2 :
				marker(figx + config.offset[0],figy + config.offset[1],config.canvasDraw)
			config.draw.polygon(pointsArray, outline="black", fill = config.colorArray[ring])
	

def showGrid():
	global config

	config.image.paste(config.canvasImage, (0, 0), config.canvasImage)
	config.render(config.image, round(config.imageOffsetX), round(config.imageOffsetY))


def main(run=True):
	global config, directionOrder
	print("---------------------")
	print("Screen Loaded")

	colorutils.brightness = config.brightness

	config.delay = float(workConfig.get("pattern", 'delay'))
	config.base = float(workConfig.get("pattern", 'base'))
	config.rows = int(workConfig.get("pattern", 'rows'))
	config.cols = int(workConfig.get("pattern", 'cols'))


	config.patternSet = workConfig.get("pattern", 'patternSet')

	config.initialRadius = float(workConfig.get(config.patternSet, 'initialRadius'))
	config.nSides = int(workConfig.get(config.patternSet, 'nSides'))
	config.colorRep = int(workConfig.get(config.patternSet, 'colorRep'))
	config.repeatFigures = int(workConfig.get(config.patternSet, 'repeatFigures'))
	config.reduceRate = float(workConfig.get(config.patternSet, 'reduceRate'))
	config.turnRate = float(workConfig.get(config.patternSet, 'turnRate'))
	config.turnRateDirection = 1


	config.turnRateChange = float(workConfig.get("pattern", 'turnRateChange'))
	config.turnRateLimPlus = float(workConfig.get("pattern", 'turnRateLimPlus'))
	config.turnRateLimNeg = float(workConfig.get("pattern", 'turnRateLimNeg'))
	config.turnRateFactor = float(workConfig.get("pattern", 'turnRateFactor'))

	config.xOffset = int(workConfig.get("pattern", 'xOffset'))
	config.yOffset = int(workConfig.get("pattern", 'yOffset'))
	config.imageOffsetY = 0
	config.imageOffsetX = 0

	config.block = ((workConfig.get("pattern", 'block')).split(','))
	config.blockDims = list([int(i) for i in config.block])
	config.blockLineHeight = int(workConfig.get("pattern", 'blockLineHeight'))
	config.blockSteps = int(workConfig.get("pattern", 'blockSteps'))
	config.paused =  False
	config.timeDelay = 5.0


	# Start from center for each polygon
	"sin (theta) = (r + d) / s"
	"s = 2 * r * cos(theta/2)"
	config.n = config.nSides
	config.r = config.initialRadius
	config.offset = (config.xOffset, config.yOffset)

	config.theta = 2 * math.pi / config.n
	config.side = 2 * config.r * math.cos(config.theta / 2)
	config.d = config.side * math.sin(config.theta) - config.r
	config.phi = (1.0 + math.sqrt(5.0))/2

	config.f1 = getColorChanger()
	config.f2 = getColorChanger()
	config.f3 = getColorChanger()
	config.f4 = getColorChanger()
	config.f5 = getColorChanger()
	config.f6 = getColorChanger()

	config.colorArrayBase = [config.f1, config.f2, config.f3, config.f4, config.f5, config.f6]

	for i in range(0,6,2) :
		setColorProperties(config.colorArrayBase[i])

	config.f2.minHue = 90
	config.f2.maxHue = 180
	config.f2.minSaturation = .1
	config.f2.maxSaturation = .3
	config.f2.minValue = .2
	config.f2.maxBrightness = .5
	config.f2.maxValue = .5


	config.angle = 0
	config.angleIncrement = math.pi/1000

	config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	config.draw = ImageDraw.Draw(config.image)
	config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.canvasDraw = ImageDraw.Draw(config.canvasImage)

	setUp()

	#if(run) : runWork()

def setColorProperties(c) :
	c.minHue = float(workConfig.get("pattern", 'minHue'))
	c.maxHue = float(workConfig.get("pattern", 'maxHue'))
	c.minSaturation = float(workConfig.get("pattern", 'minSaturation'))
	c.maxSaturation = float(workConfig.get("pattern", 'maxSaturation'))
	c.minValue = float(workConfig.get("pattern", 'minValue'))
	c.maxBrightness = float(workConfig.get("pattern", 'maxBrightness'))
	c.maxValue = float(workConfig.get("pattern", 'maxValue'))



def setUp():
	global config
	drawPattern()


def runWork():
	global config
	while True:
		iterate()
		time.sleep(config.delay)


def iterate():
	global config
	drawPattern()
	showGrid()


def callBack():
	global config
	return True
