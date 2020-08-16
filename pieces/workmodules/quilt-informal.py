import math
import random
import textwrap
import time

from modules import badpixels, coloroverlay, colorutils
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFont, ImageOps

## This quilt supercedes the quilt.py module because it accounts for a zero irregularity
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
		self.lineColorMode = "red"
		self.changeColor = True
		self.lines = config.lines

	def setUp(self, n=0):

		self.outlineColor = tuple(
			int(a * self.brightness) for a in (self.outlineColorObj.currentColor)
		)

		#### Sets up color transitions
		self.colOverlay = coloroverlay.ColorOverlay()
		self.colOverlay.randomSteps = True
		self.colOverlay.timeTrigger = True
		self.colOverlay.tLimitBase = 5
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

		"""
		self.fillColor = colorutils.getRandomColorHSV(
			sMin = self.minSaturation, sMax = self.maxSaturation,  
			hMin = self.minHue, hMax  = self.maxHue, 
			vMin = self.minValue, vMax = self.maxValue
			)


		self.colOverlay.colorB = colorutils.getRandomColorHSV(
			sMin = self.minSaturation, sMax = self.maxSaturation,  
			hMin = self.minHue, hMax  = self.maxHue, 
			vMin = self.minValue, vMax = self.maxValue
			)

		self.colOverlay.colorA = self.fillColor
		"""

		self.colOverlay.setStartColor()
		self.colOverlay.getNewColor()
		self.colOverlay.colorTransitionSetup()

		self.outlineColor = tuple(
			int(a * self.brightness) for a in (self.outlineColorObj.currentColor)
		)
		self.fillColor = tuple(
			int(a * self.brightness) for a in (self.colOverlay.currentColor)
		)

	def update(self):
		# self.fillColorMode == "random" or
		if random.random() > self.config.colorPopProb:
			self.colOverlay.stepTransition()
			self.fillColor = tuple(
				int(a * self.brightness) for a in self.colOverlay.currentColor
			)
		else:
			self.changeColorFill()

	def renderPolys(self):

		if self.fillColorMode == "red":
			brightnessFactor = self.config.brightnessFactorDark
		else:
			brightnessFactor = self.config.brightnessFactorLight

		self.outlineColor = tuple(
			int(a * self.brightness * brightnessFactor)
			for a in self.outlineColorObj.currentColor
		)
		self.fillColor = tuple(
			int(a * self.brightness) for a in (self.colOverlay.currentColor)
		)

		if self.lines == True:
			self.draw.polygon(self.poly, fill=self.fillColor)
		else:
			self.draw.polygon(self.poly, fill=self.fillColor, outline=None)

	def render(self):

		if self.fillColorMode == "red":
			brightnessFactor = self.config.brightnessFactorDark
		else:
			brightnessFactor = self.config.brightnessFactorLight

		self.outlineColor = tuple(
			int(a * self.brightness * brightnessFactor)
			for a in self.outlineColorObj.currentColor
		)
		self.fillColor = tuple(
			int(a * self.brightness) for a in (self.colOverlay.currentColor)
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


def main(config, workConfig, run=True):
	# global config, directionOrder,workConfig
	print("---------------------")
	print("QUILT Loaded")

	config.brightness = float(workConfig.get("displayconfig", "brightness"))
	colorutils.brightness = config.brightness
	config.canvasImageWidth = config.screenWidth
	config.canvasImageHeight = config.screenHeight
	# config.canvasImageWidth -= 4
	# config.canvasImageHeight -= 4

	config.outlineColorObj = coloroverlay.ColorOverlay()
	config.outlineColorObj.randomRange = (5.0, 30.0)
	config.outlineColorObj.colorTransitionSetup()

	config.transitionStepsMin = float(workConfig.get("quilt", "transitionStepsMin"))
	config.transitionStepsMax = float(workConfig.get("quilt", "transitionStepsMax"))

	config.transformShape = workConfig.getboolean("quilt", "transformShape")
	transformTuples = workConfig.get("quilt", "transformTuples").split(",")
	config.transformTuples = tuple([float(i) for i in transformTuples])

	redRange = workConfig.get("quilt", "redRange").split(",")
	config.redRange = tuple([int(i) for i in redRange])

	backgroundColor = workConfig.get("quilt", "backgroundColor").split(",")
	config.backgroundColor = tuple([int(i) for i in backgroundColor])

	config.opticalPattern = workConfig.get("quilt", "opticalPattern")
	config.numUnits = int(workConfig.get("quilt", "numUnits"))
	config.hGapSize = int(workConfig.get("quilt", "hGapSize"))
	config.vGapSize = int(workConfig.get("quilt", "vGapSize"))
	config.blockSize = int(workConfig.get("quilt", "blockSize"))
	config.blockLength = float(workConfig.get("quilt", "blockLength"))
	config.blockHeight = float(workConfig.get("quilt", "blockHeight"))
	config.blockRows = int(workConfig.get("quilt", "blockRows"))
	config.blockCols = int(workConfig.get("quilt", "blockCols"))
	config.cntrOffsetX = int(workConfig.get("quilt", "cntrOffsetX"))
	config.cntrOffsetY = int(workConfig.get("quilt", "cntrOffsetY"))
	config.delay = float(workConfig.get("quilt", "delay"))
	config.colorPopProb = float(workConfig.get("quilt", "colorPopProb"))
	config.brightnessFactorDark = float(workConfig.get("quilt", "brightnessFactorDark"))
	config.brightnessFactorLight = float(
		workConfig.get("quilt", "brightnessFactorLight")
	)
	config.lines = workConfig.getboolean("quilt", "lines")
	config.patternPrecision = workConfig.getboolean("quilt", "patternPrecision")

	config.polyDistortion = float(workConfig.get("quilt", "polyDistortion"))
	config.polyDistortionMin = -config.polyDistortion
	config.polyDistortionMax = config.polyDistortion

	config.opticalPatterns = ["Regular", "LighteningStrike", "Diagonals"]
	# "LighteningStrikeH"  aka Charlie Brown sweater ...

	# for now, all squares
	# config.blockLength = config.blockSize
	# config.blockHeight = config.blockSize

	config.canvasImage = Image.new(
		"RGBA", (config.canvasImageWidth, config.canvasImageHeight)
	)
	config.timeToComplete = int(workConfig.get("quilt", "timeToComplete"))
	# config.timeToComplete = 60 #round(random.uniform(30,220))


	# createPieces()
	drawSqareSpiral(config)

	# if(run) : runWork()



def restartPiece(config):

	config.polyDistortionMin = -random.uniform(1, config.polyDistortion + 1)
	config.polyDistortionMax = random.uniform(1, config.polyDistortion + 1)

	del config.unitArray[:]

	p = math.floor(random.uniform(0, len(config.opticalPatterns)))

	config.opticalPattern = config.opticalPatterns[p]

	drawSqareSpiral(config)

	config.canvasOffsetX = round(random.uniform(-config.canvasOffsetX_init,config.canvasOffsetX_init))
	config.canvasOffsetY = round(random.uniform(-config.canvasOffsetY_init,config.canvasOffsetY_init))
	config.canvasRotation = random.uniform(-config.canvasRotation_init,config.canvasRotation_init)


def drawSqareSpiral(config):

	# global config

	config.t1 = time.time()
	config.t2 = time.time()

	cntrOffset = [config.cntrOffsetX, config.cntrOffsetY]

	config.unitArray = []

	## Alignment perfect setup
	if config.patternPrecision == True:
		sizeAdjustor = 1

	n = 0

	darkValues = [0.1 * config.brightness, 0.5 * config.brightness]
	lightValues = [0.5 * config.brightness, 0.99 * config.brightness]

	opticalPattern = config.opticalPattern

	"""
	LIGHTENING PATTERN
	 dark right dark bottom   dark top. dark right
	 dark top  dark left.   dark right. dark bottom

	 repeat .....


	"""

	for rows in range(0, config.blockRows):

		for cols in range(0, config.blockCols):

			if opticalPattern == "LighteningStrike":

				if cols % 2 > 0:
					if rows % 2 > 0:
						topValues = lightValues
						rightValues = darkValues
						bottomValues = darkValues
						leftValues = lightValues
					else:
						topValues = darkValues
						rightValues = darkValues
						bottomValues = lightValues
						leftValues = lightValues
				else:
					if rows % 2 > 0:
						topValues = darkValues
						rightValues = lightValues
						bottomValues = lightValues
						leftValues = darkValues
					else:
						topValues = lightValues
						rightValues = lightValues
						bottomValues = darkValues
						leftValues = darkValues

			elif opticalPattern == "LighteningStrikeH":

				if cols % 2 == 0:
					if rows % 2 == 0:
						topValues = lightValues
						rightValues = darkValues
						bottomValues = darkValues
						leftValues = lightValues
					else:
						topValues = darkValues
						rightValues = lightValues
						bottomValues = lightValues
						leftValues = darkValues
				else:
					if rows % 2 == 0:
						topValues = lightValues
						rightValues = lightValues
						bottomValues = darkValues
						leftValues = darkValues
					else:
						topValues = darkValues
						rightValues = darkValues
						bottomValues = lightValues
						leftValues = lightValues

			elif opticalPattern == "Diagonals":

				if cols % 2 > 0:
					if rows % 2 > 0:
						topValues = darkValues
						rightValues = darkValues
						bottomValues = lightValues
						leftValues = lightValues
					else:
						topValues = lightValues
						rightValues = lightValues
						bottomValues = darkValues
						leftValues = darkValues
				else:
					if rows % 2 > 0:
						topValues = lightValues
						rightValues = lightValues
						bottomValues = darkValues
						leftValues = darkValues
					else:
						topValues = darkValues
						rightValues = darkValues
						bottomValues = lightValues
						leftValues = lightValues
			else:

				topValues = lightValues
				rightValues = lightValues
				bottomValues = darkValues
				leftValues = darkValues

			hDelta = config.numUnits * config.blockLength * 2 + config.hGapSize
			vDelta = config.numUnits * config.blockHeight * 2 + config.vGapSize

			cntr = [cols * hDelta + cntrOffset[0], rows * vDelta + cntrOffset[1]]
			outlineColorObj = coloroverlay.ColorOverlay()
			outlineColorObj.randomRange = (5.0, 30.0)
			outlineColorObj.colorTransitionSetup()

			n += 1

			## Archimedean spiral is  r = a + b * theta
			turns = config.numUnits + 1
			b1 = config.blockLength
			b2 = config.blockHeight

			A = []
			B = []
			rangeChange = (config.polyDistortionMin, config.polyDistortionMax)

			for i in range(1, turns):
				x = i * b1 + cntr[0] + random.uniform(rangeChange[0], rangeChange[1])
				y = i * b2 + cntr[1]  # + random.uniform(rangeChange[0],rangeChange[1])
				A.append((x, y))

				x = -i * b1 + cntr[0]  # + random.uniform(rangeChange[0],rangeChange[1])
				y = i * b2 + cntr[1] + random.uniform(rangeChange[0], rangeChange[1])
				A.append((x, y))

				x = -i * b1 + cntr[0] + random.uniform(rangeChange[0], rangeChange[1])
				y = -i * b2 + cntr[1]  # + random.uniform(rangeChange[0],rangeChange[1])
				A.append((x, y))

				x = (i + 1) * b1 + cntr[
					0
				]  # + random.uniform(rangeChange[0],rangeChange[1])
				y = -i * b2 + cntr[1] + random.uniform(rangeChange[0], rangeChange[1])
				A.append((x, y))

			B = [(item[0] - b1, item[1]) for item in A]

			obj = unit(config)
			obj.fillColorMode = "red"
			obj.changeColor = False
			obj.outlineColorObj = outlineColorObj
			obj.poly = (A[2], B[3], A[0], A[1])

			# This is the center square, so should be red, like the hearth it represents
			obj.minSaturation = 0.8
			obj.maxSaturation = 1
			obj.minValue = 0.1
			obj.maxValue = 0.7
			obj.minHue = 0
			obj.maxHue = 36

			obj.setUp(n)
			config.unitArray.append(obj)

			n = 1

			for i in range(0, turns):
				try:
					# LEFT
					# draw.polygon(poly, fill=colorutils.randomColor(config.brightness/4))
					obj = unit(config)
					obj.poly = (B[n + 1], A[n + 1], A[n + 0], B[n + 0])
					obj.changeColor = False
					obj.outlineColorObj = outlineColorObj

					obj.minSaturation = 0.5
					obj.maxSaturation = 1
					obj.minValue = leftValues[0]
					obj.maxValue = leftValues[1]
					obj.minHue = config.redRange[0]
					obj.maxHue = config.redRange[1]

					obj.setUp(n)
					config.unitArray.append(obj)

					# BOTTOM
					obj = unit(config)
					obj.poly = (B[n + 0], A[n - 1], B[n + 3], A[n + 4])
					obj.changeColor = False
					obj.outlineColorObj = outlineColorObj

					obj.minSaturation = 0.8
					obj.maxSaturation = 1
					obj.minValue = bottomValues[0]
					obj.maxValue = bottomValues[1]
					obj.minHue = 0
					obj.maxHue = 360

					obj.setUp(n)
					config.unitArray.append(obj)
					# draw.polygon(poly, fill=colorutils.randomColor())

					# RIGHT
					obj = unit(config)
					obj.poly = (B[n + 2], A[n + 2], A[n + 3], B[n + 3])
					obj.changeColor = False
					obj.outlineColorObj = outlineColorObj

					obj.minSaturation = 0.7
					obj.maxSaturation = 0.9
					obj.minValue = rightValues[0]
					obj.maxValue = rightValues[1]
					obj.minHue = 0
					obj.maxHue = 360

					obj.setUp(n)
					config.unitArray.append(obj)
					# draw.polygon(poly, fill=colorutils.randomColor(config.brightness * 1.2))

					# TOP
					obj = unit(config)
					obj.poly = (B[n + 1], A[n + 5], B[n + 6], A[n + 2])
					obj.changeColor = False
					obj.outlineColorObj = outlineColorObj

					obj.minSaturation = 0.7
					obj.maxSaturation = 0.9
					obj.minValue = topValues[0]
					obj.maxValue = topValues[1]
					obj.minHue = config.redRange[0]
					obj.maxHue = config.redRange[1]

					obj.setUp(n)
					config.unitArray.append(obj)
					# draw.polygon(poly, fill=colorutils.randomColor(config.brightness/1.5))

					n += 4
				except Exception as e:
					# print(e)
					pass


def runWork(config):
	# global blocks, config, XOs
	# gc.enable()
	# print("quilts ",config.render, config.instanceNumber)
	while True:
		iterate(config)
		time.sleep(config.delay)


def iterate(config):
	# global config
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
		((0, 0), (config.screenWidth, config.screenHeight)), fill=config.backgroundColor
	)
	temp.paste(config.canvasImage, (0, 0), config.canvasImage)
	if config.transformShape == True:
		temp = transformImage(temp)

	# print("quilts ",config.render, config.instanceNumber)
	config.render(temp, 0, 0)

	config.t2 = time.time()
	delta = config.t2 - config.t1

	if delta > config.timeToComplete:
		restartPiece(config)
