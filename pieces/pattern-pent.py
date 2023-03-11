import argparse
import datetime
import math
import random
import time
from threading import Timer
from modules.configuration import bcolors
from modules import coloroverlay, colorutils
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFont, ImageOps


def marker(x, y, draw, f="red"):
	draw.rectangle((x, y, x + 3, y + 3), fill=f)


def getColorChanger():
	global workConfig
	colOverlay = coloroverlay.ColorOverlay(False)
	colOverlay.randomSteps = False
	colOverlay.timeTrigger = True
	colOverlay.tLimitBase = round(random.uniform(10,50))
	colOverlay.maxBrightness = config.brightness
	colOverlay.steps = round(random.uniform(20,60))
	colOverlay.minHue = float(workConfig.get("pattern", "minHue"))
	colOverlay.maxHue = float(workConfig.get("pattern", "maxHue"))
	colOverlay.minSaturation = float(workConfig.get("pattern", "minSaturation"))
	colOverlay.maxSaturation = float(workConfig.get("pattern", "maxSaturation"))
	colOverlay.minValue = float(workConfig.get("pattern", "minValue"))
	colOverlay.maxValue = float(workConfig.get("pattern", "maxValue"))
	config.randomRangeMin = int(workConfig.get("pattern", "randomRangeMin"))
	config.randomRangeMax = int(workConfig.get("pattern", "randomRangeMax"))
	colOverlay.randomRange = (config.randomRangeMin, config.randomRangeMax)
	return colOverlay


def setColorProperties(c):
	# c.maxBrightness = float(workConfig.get("pattern", 'maxBrightness'))
	c.colorTransitionSetup()
	c.getNewColor()
	c.setStartColor()
	c.stepTransition()
	pass


def drawPattern():

	draw = config.draw
	config.colorArray = []

	for i in config.colorArrayBase:
		i.stepTransition()
		config.colorArray.append(tuple(i.currentColor))

	drawConcentricRings()



def resetPause():
	config.paused = False

	# config.turnRateLimPlus = random.uniform(1,3)
	# config.turnRateLimNeg = random.uniform(config.turnRateLimPlus-1 ,config.turnRateLimPlus - 3)


def drawConcentricRings():
	offset = (0, 0)
	angleOffset = 0
	level = 0
	numChildren = 0
	fillLevel = 0

	figs = config.repeatFigures
	config.r = config.initialRadius

	"Ideally, make the rate of change sinusoidal - i.e. change the rate\
	gradually over time so there are smooth transitions back and forth"

	"""
	config.angle += config.angleIncrement
	if config.angle == 0 or config.angle == math.pi or config.angle == 2*math.pi :
		pass
	else :
		m = 2
		#x = m - abs(i % (2*m) - m)
		#rate = m - abs(math.sin(config.angle) % 2*m - m) + .8
		rate = m - abs((config.angle) % 2*m - m) + .9

	if random.random() > .99 :
		config.turnRateChange = random.uniform(.5,3) / config.turnRateFactor
	"""

	if config.paused == False and config.turnRateBase != 0:
		config.turnRate += config.turnRateChange * config.turnRateDirection
		# config.turnRate = rate

		if random.random() < config.pauseProb:
			config.paused = True
			d = random.uniform(.1, config.maxPauseTime)
			t1 = Timer(d, resetPause)
			t1.start()

		if config.turnRate > config.turnRateLimPlus:

			config.turnRateDirection = -1
			config.turnRate = config.turnRateLimPlus

			# config.paused = True
			d = random.uniform(5, 20)
			t1 = Timer(d, resetPause)
			# t1.start()

		if config.turnRate < config.turnRateLimNeg:
			config.turnRateDirection = 1

			# config.paused = True
			d = random.uniform(5, 20)
			t = Timer(d, resetPause)
			# t.start()

	f = 0
	for figures in range(0, figs):

		figureAngle = 0 * figures
		figx = 0
		figy = 0

		if config.turnRate == 0:
			delta = 0
		else:
			delta = config.theta / config.turnRate * figures

		# figureAngleOffset = math.pi/4 + delta
		figureAngleOffset = config.figureRotationBase + delta

		config.r *= config.reduceRate / config.phi

		pointsArray = []

		for i in range(0, config.n):
			angle = config.theta * i + figureAngleOffset
			x = (
				config.r * math.cos(angle)
				+ config.offset[0]
				+ config.figureDistortions[figures][i]
			)
			y = (
				config.r * math.sin(angle)
				+ config.offset[1]
				+ config.figureDistortions[figures][i]
			)
			pointsArray.append((x, y))

		if config.showLines == True:
			config.draw.polygon(
				pointsArray, outline=config.colorArray[0], fill=config.colorArray[f]
			)
		else:
			config.draw.polygon(pointsArray, outline=None, fill=config.colorArray[f])

		f += 1
		if f >= config.colorRep:
			f = 0


def showGrid():
	global config

	config.image.paste(config.canvasImage, (0, 0), config.canvasImage)
	config.render(config.image, round(config.imageOffsetX), round(config.imageOffsetY))


def main(run=True):
	global config, directionOrder
	global workConfig
	print("---------------------")
	print("Screen Loaded")

	colorutils.brightness = config.brightness

	config.delay = float(workConfig.get("pattern", "delay"))

	config.patternSet = workConfig.get("pattern", "patternSet")
	config.showLines = workConfig.getboolean("pattern", "showLines")

	config.initialRadius = float(workConfig.get(config.patternSet, "initialRadius"))
	config.nSides = int(workConfig.get(config.patternSet, "nSides"))
	config.colorRep = int(workConfig.get(config.patternSet, "colorRep"))
	config.repeatFigures = int(workConfig.get(config.patternSet, "repeatFigures"))
	config.reduceRate = float(workConfig.get(config.patternSet, "reduceRate"))
	config.pointVariation = float(workConfig.get("pattern", "pointVariation"))
	config.figureRotationBaseDegrees = float(
		workConfig.get("pattern", "figureRotationBaseDegrees")
	)
	config.figureRotationBase = config.figureRotationBaseDegrees * math.pi / 180

	config.turnRateChange = float(workConfig.get("pattern", "turnRateChange"))
	config.turnRateLimPlus = float(workConfig.get("pattern", "turnRateLimPlus"))
	config.turnRateLimNeg = float(workConfig.get("pattern", "turnRateLimNeg"))
	config.turnRateFactor = float(workConfig.get("pattern", "turnRateFactor"))
	config.pauseProb = float(workConfig.get("pattern", "pauseProb"))
	config.maxPauseTime = float(workConfig.get("pattern", "maxPauseTime"))
	config.turnRateBase = float(workConfig.get(config.patternSet, "turnRateBase"))
	config.turnRateDirection = 1
	config.turnRate = config.turnRateBase

	config.xOffset = int(workConfig.get("pattern", "xOffset"))
	config.yOffset = int(workConfig.get("pattern", "yOffset"))
	config.imageOffsetY = 0
	config.imageOffsetX = 0


	config.paused = False

	# Start from center for each polygon
	"sin (theta) = (r + d) / s"
	"s = 2 * r * cos(theta/2)"
	config.n = config.nSides
	config.r = config.initialRadius
	config.offset = (config.xOffset, config.yOffset)

	config.theta = 2 * math.pi / config.n
	config.side = 2 * config.r * math.cos(config.theta / 2)
	config.d = config.side * math.sin(config.theta) - config.r
	config.phi = (1.0 + math.sqrt(5.0)) / 2

	config.f1 = getColorChanger()
	config.f2 = getColorChanger()
	config.f3 = getColorChanger()
	config.f4 = getColorChanger()
	config.f5 = getColorChanger()
	config.f6 = getColorChanger()

	config.colorArrayBase = [
		config.f1,
		config.f2,
		config.f3,
		config.f4,
		config.f5,
		config.f6,
	]

	for i in range(0, 6):
		setColorProperties(config.colorArrayBase[i])

	config.figureDistortions = []

	var = config.pointVariation
	for i in range(0, config.repeatFigures):
		polyDist = []
		varToUse = var - var * i / config.repeatFigures
		# print (varToUse)
		for ii in range(0, config.n):
			# polyDist.append(var  - random.random() * 2 * var)
			polyDist.append(varToUse - random.random() * 2 * varToUse)

		config.figureDistortions.append(polyDist)

	"""
	config.f2.minHue = config.f1.minHue #90
	config.f2.maxHue = config.f1.maxHue #180
	config.f2.minSaturation = config.f1.minSaturation #.1
	config.f2.maxSaturation = config.f1.maxSaturation #.3
	config.f2.minValue = config.f1.minValue #.2
	config.f2.maxValue = config.f1.maxValue #.5
	config.f2.maxBrightness = config.f1.maxBrightness #.5

	config.f3.minHue = config.f1.minHue #90
	config.f3.maxHue = config.f1.maxHue #180
	config.f3.minSaturation = config.f1.minSaturation #.1
	config.f3.maxSaturation = config.f1.maxSaturation #.3
	config.f3.minValue = config.f1.minValue #.2
	config.f3.maxValue = config.f1.maxValue #.5
	config.f3.maxBrightness = config.f1.maxBrightness #.5
	"""

	config.angle = 0
	config.angleIncrement = math.pi / 1000

	config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	config.draw = ImageDraw.Draw(config.image)
	config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.canvasDraw = ImageDraw.Draw(config.canvasImage)

	setUp()

	# if(run) : runWork()


def setUp():
	global config
	drawPattern()


def runWork():
	global config
	print("RUNNING Pattern Pent")
	while config.isRunning == True:
		iterate()
		time.sleep(config.delay)
		if config.standAlone == False :
			config.callBack()	
			

def iterate():
	global config
	drawPattern()
	showGrid()


def callBack():
	global config
	return True
