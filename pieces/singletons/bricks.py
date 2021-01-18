import math
import random
import textwrap
import time

from modules import badpixels, coloroverlay, colorutils
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFont, ImageOps

## This bricks supercedes the bricks.py module because it accounts for a zero irregularity
## as well as the infomal bar construction


class unit:

	timeTrigger = True
	tLimitBase = 30

	maxBrightness = 1

	minSaturation = 1
	maxSaturation = 1

	minValue = 1
	maxValue = 1

	minHue = 0
	maxHue = 360

	def __init__(self, config):
		self.config = config
		self.xPos = 0
		self.yPos = 0
		self.redraw = False

		self.draw = ImageDraw.Draw(config.canvasImage)

		## Like the "stiching" color and affects the overall "tone" of the piece
		self.outlineColor = config.outlineColorObj.currentColor
		self.objWidth = 20

		self.outlineRange = [(20, 20, 250)]
		self.brightness = 1
		self.fillColorMode = "random"
		self.fillColorMode = "red"
		self.lineColorMode = "red"
		self.changeColor = True
		self.lines = config.lines

	def setUp(self, n=0):

		# self.outlineColor = tuple(int(a*self.brightness) for a in (self.outlineColorObj.currentColor))

		#### Sets up color transitions
		self.colOverlay = coloroverlay.ColorOverlay()
		self.colOverlay.randomSteps = True
		self.colOverlay.timeTrigger = True
		self.colOverlay.tLimitBase = 20
		self.colOverlay.steps = 10

		self.colOverlay.maxBrightness = self.config.brightness
		self.colOverlay.maxBrightness = self.maxBrightness

		self.colOverlay.minSaturation = self.minSaturation
		self.colOverlay.maxSaturation = self.maxSaturation

		self.colOverlay.minValue = self.minValue
		self.colOverlay.maxValue = self.maxValue

		self.colOverlay.minHue = self.minHue
		self.colOverlay.maxHue = self.maxHue

		### This is the speed range of transitions in color
		### Higher numbers means more possible steps so slower
		### transitions - 1,10 very blinky, 10,200 very slow
		self.colOverlay.randomRange = (
			self.config.transitionStepsMin,
			self.config.transitionStepsMax,
		)

		self.fillColor = colorutils.getRandomColorHSV(
			sMin=self.minSaturation,
			sMax=self.maxSaturation,
			hMin=self.minHue,
			hMax=self.maxHue,
			vMin=self.minValue,
			vMax=self.maxValue,
		)

		self.colOverlay.colorA = self.fillColor

		self.colOverlay.colorB = colorutils.getRandomColorHSV(
			sMin=self.minSaturation,
			sMax=self.maxSaturation,
			hMin=self.minHue,
			hMax=self.maxHue,
			vMin=self.minValue,
			vMax=self.maxValue,
		)

		# self.outlineColor = tuple(int(a*self.brightness) for a in (self.outlineColorObj.currentColor))
		self.colOverlay.colorTransitionSetup()

	def update(self):
		# self.fillColorMode == "random" or
		if random.random() > config.colorPopProb:
			self.colOverlay.stepTransition()
			self.outlineColorObj.stepTransition()
			self.fillColor = tuple(
				int(a * self.brightness) for a in self.colOverlay.currentColor
			)
		else:
			self.changeColorFill()

	def renderPolys(self):
		poly = ()
		for i in self.poly:
			i[0] += self.config.scrollSpeed
			poly += tuple(i)

		if self.poly[0][0] > self.config.screenWidth + self.blockLength:
			for i in range(0, 4):
				self.poly[i][0] = self.initPoly[i][0] + self.blockLength

		if self.fillColorMode == "red":
			brightnessFactor = self.config.brightnessFactorDark
		else:
			brightnessFactor = self.config.brightnessFactorLight

		self.outlineColor = tuple(
			int(a * self.brightness * brightnessFactor)
			for a in self.outlineColorObj.currentColor
		)

		if self.lines == True:
			# self.draw.polygon(poly, fill=self.fillColor,  outline=self.outlineColor)
			# self.draw.rectangle( (poly[0] + self.xOffsetInit ,poly[1], poly[4] + self.xOffsetInit,poly[5]), fill=self.fillColor,  outline=self.outlineColor)
			self.draw.rectangle(
				(
					poly[0] + self.xOffsetInit - self.config.hGapSize / 2,
					poly[1] - self.config.vGapSize / 2 + self.yOffsetInit,
					poly[4] + self.xOffsetInit + self.config.hGapSize / 2,
					poly[5] + self.config.vGapSize / 2 + self.yOffsetInit,
				),
				fill=self.outlineColor,
				outline=None,
			)
			self.draw.rectangle(
				(
					poly[0] + self.xOffsetInit,
					poly[1] + self.yOffsetInit,
					poly[4] + self.xOffsetInit,
					poly[5] + self.yOffsetInit,
				),
				fill=self.fillColor,
				outline=None,
			)
		else:
			self.draw.polygon(poly, fill=self.fillColor, outline=None)

	def render(self):

		if self.fillColorMode == "red":
			brightnessFactor = self.config.brightnessFactorDark
		else:
			brightnessFactor = self.config.brightnessFactorLight

		self.outlineColor = tuple(
			int(a * self.brightness * brightnessFactor)
			for a in self.outlineColorObj.currentColor
		)

		if self.lines == True:
			self.draw.rectangle(
				(
					(self.xPos, self.yPos),
					(self.xPos + self.blockLength, self.yPos + self.blockHeight),
				),
				fill=self.fillColor,
				outline=self.outlineColor,
			)
		else:
			self.draw.rectangle(
				(
					(self.xPos, self.yPos),
					(self.xPos + self.blockLength, self.yPos + self.blockHeight),
				),
				fill=self.fillColor,
				outline=None,
			)

	## Straight color change - deprecated - too blinky
	def changeColorFill(self):

		if self.changeColor == True:
			if self.fillColorMode == "random":
				self.fillColor = colorutils.randomColor(
					random.uniform(0.01, self.brightness)
				)
				self.outlineColor = colorutils.getRandomRGB(
					random.uniform(0.01, self.brightness)
				)
			else:
				self.fillColor = colorutils.getRandomColorHSV(
					sMin=self.minSaturation,
					sMax=self.maxSaturation,
					hMin=self.minHue,
					hMax=self.maxHue,
					vMin=self.minValue,
					vMax=self.maxValue,
				)

				self.colOverlay.colorA = self.fillColor


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def transformImage(img):
	width, height = img.size
	m = -0.5
	xshift = abs(m) * 420
	new_width = width + int(round(xshift))

	img = img.transform(
		(new_width, height), Image.AFFINE, (1, m, 0, 0, 1, 0), Image.BICUBIC
	)
	img = img.transform(
		(new_width, height), Image.PERSPECTIVE, config.transformTuples, Image.BICUBIC
	)
	return img


def main(run=True):
	global config, directionOrder, workConfig
	print("---------------------")
	print("BRICKS Loaded")

	config.brightness = float(workConfig.get("displayconfig", "brightness"))
	colorutils.brightness = config.brightness
	config.canvasImageWidth = config.screenWidth
	config.canvasImageHeight = config.screenHeight

	config.outlineColorObj = coloroverlay.ColorOverlay()
	config.outlineColorObj.randomRange = (5.0, 30.0)

	config.transitionStepsMin = float(workConfig.get("bricks", "transitionStepsMin"))
	config.transitionStepsMax = float(workConfig.get("bricks", "transitionStepsMax"))

	config.transformShape = workConfig.getboolean("bricks", "transformShape")
	transformTuples = workConfig.get("bricks", "transformTuples").split(",")
	config.transformTuples = tuple([float(i) for i in transformTuples])

	redRange = workConfig.get("bricks", "redRange").split(",")
	config.redRange = tuple([int(i) for i in redRange])

	config.numUnits = int(workConfig.get("bricks", "numUnits"))
	config.hGapSize = int(workConfig.get("bricks", "hGapSize"))
	config.vGapSize = int(workConfig.get("bricks", "vGapSize"))
	config.blockSize = int(workConfig.get("bricks", "blockSize"))
	config.blockLength = float(workConfig.get("bricks", "blockLength"))
	config.blockHeight = float(workConfig.get("bricks", "blockHeight"))
	config.blockRows = int(workConfig.get("bricks", "blockRows"))
	config.blockCols = int(workConfig.get("bricks", "blockCols"))
	config.cntrOffsetX = int(workConfig.get("bricks", "cntrOffsetX"))
	config.cntrOffsetY = int(workConfig.get("bricks", "cntrOffsetY"))
	config.delay = float(workConfig.get("bricks", "delay"))
	config.colorPopProb = float(workConfig.get("bricks", "colorPopProb"))
	config.scrollSpeed = float(workConfig.get("bricks", "scrollSpeed"))
	config.brightnessFactorDark = float(
		workConfig.get("bricks", "brightnessFactorDark")
	)
	config.brightnessFactorLight = float(
		workConfig.get("bricks", "brightnessFactorLight")
	)
	config.lines = workConfig.getboolean("bricks", "lines")
	config.patternPrecision = workConfig.getboolean("bricks", "patternPrecision")

	config.polyDistortion = float(workConfig.get("bricks", "polyDistortion"))
	config.polyDistortionMin = -config.polyDistortion
	config.polyDistortionMax = config.polyDistortion

	config.canvasImage = Image.new(
		"RGBA", (config.canvasImageWidth, config.canvasImageHeight)
	)

	config.timeToComplete = int(workConfig.get("bricks", "timeToComplete"))
	# config.timeToComplete = 60 #round(random.uniform(30,220))

	# createPieces()
	drawSqareSpiral()

	if run:
		runWork()


def restartPiece():

	config.polyDistortionMin = -random.uniform(1, config.polyDistortion + 1)
	config.polyDistortionMax = random.uniform(1, config.polyDistortion + 1)

	del config.unitArray[:]

	drawSqareSpiral()


def drawSqareSpiral():

	global config

	config.t1 = time.time()
	config.t2 = time.time()

	config.unitArray = []

	hDelta = config.blockLength + config.hGapSize
	vDelta = config.blockHeight + config.vGapSize

	cntrOffset = [config.cntrOffsetX, config.cntrOffsetY]

	xOffsetCalculated = config.screenWidth - config.blockCols * hDelta
	cntrOffset[0] = xOffsetCalculated

	config.xOffsetCalculated = xOffsetCalculated

	xOffset = cntrOffset[0]
	yOffset = cntrOffset[1]

	n = 0

	for rows in range(0, config.blockRows):

		if rows % 2 > 0:
			xOffset = -config.blockLength / 2
		else:
			xOffset = 0

		for cols in range(0, config.blockCols):

			if cols % 2 > 0:
				yOffset = -config.blockHeight / 2
			else:
				yOffset = 0

			cntr = [cols * hDelta + cntrOffset[0], rows * vDelta + cntrOffset[1]]

			b1 = config.blockLength
			b2 = config.blockHeight

			A = []
			B = []
			rangeChange = (config.polyDistortionMin, config.polyDistortionMax)

			x = cntr[0] + random.uniform(rangeChange[0], rangeChange[1])
			y = cntr[1]  # + random.uniform(rangeChange[0],rangeChange[1])
			A.append([x, y])

			x = cntr[0] + b1 + random.uniform(rangeChange[0], rangeChange[1])
			y = cntr[1]  # + random.uniform(rangeChange[0],rangeChange[1])
			A.append([x, y])

			x = cntr[0] + b1 + random.uniform(rangeChange[0], rangeChange[1])
			y = cntr[1] + b2  # + random.uniform(rangeChange[0],rangeChange[1])
			A.append([x, y])

			x = cntr[0] + random.uniform(rangeChange[0], rangeChange[1])
			y = cntr[1] + b2  # + random.uniform(rangeChange[0],rangeChange[1])
			A.append([x, y])

			if cols == 0:
				initPoly = tuple([tuple(A[0]), tuple(A[1]), tuple(A[2]), tuple(A[3])])

			obj = unit(config)
			obj.changeColor = False
			obj.poly = [A[0], A[1], A[2], A[3]]
			obj.initPoly = initPoly

			if config.rotation == 180:
				xOffset = 0

			if config.rotation == 0:
				yOffset = 0

			obj.xOffsetInit = xOffset
			obj.yOffsetInit = yOffset

			obj.minHue = 350
			obj.maxHue = 10
			obj.minSaturation = 0.2
			obj.maxSaturation = 1
			obj.minValue = 0.2
			obj.maxValue = 0.5
			obj.blockLength = config.blockLength

			outlineColorObj = coloroverlay.ColorOverlay()
			# outlineColorObj.randomRange = (5.0,300.0)
			outlineColorObj.minHue = 10
			outlineColorObj.maxHue = 20
			outlineColorObj.minSaturation = 0.1
			outlineColorObj.maxSaturation = 0.1
			outlineColorObj.minValue = 2
			outlineColorObj.maxValue = 2
			outlineColorObj.maxBrightness = 2
			obj.outlineColorObj = outlineColorObj

			obj.setUp(n)
			config.unitArray.append(obj)

			n += 1

			# if cols == 0 : print(obj.poly)


def runWork():
	global config
	print(bcolors.OKGREEN + "** " + bcolors.BOLD)
	print("RUNNING bricks.py")
	print(bcolors.ENDC)
	while True:
		iterate()
		time.sleep(config.delay)


def iterate():
	global config
	config.outlineColorObj.stepTransition()

	for i in range(0, len(config.unitArray)):
		obj = config.unitArray[i]
		if random.random() > 0.98:
			obj.outlineColorObj.stepTransition()
		obj.update()
		obj.renderPolys()

	temp = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	tDraw = ImageDraw.Draw(temp)
	tDraw.rectangle(
		((0, 0), (config.screenWidth, config.screenHeight)), fill=(100, 50, 0)
	)
	temp.paste(config.canvasImage, (0, 0), config.canvasImage)
	if config.transformShape == True:
		temp = transformImage(temp)
	config.render(temp, 0, 0)

	config.t2 = time.time()
	delta = config.t2 - config.t1

	if delta > config.timeToComplete:
		restartPiece()
