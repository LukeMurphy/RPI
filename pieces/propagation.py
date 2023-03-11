import argparse
import datetime
import math
import random
import textwrap
import time
from threading import Timer

from modules import badpixels, coloroverlay, colorutils
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFont, ImageOps

"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
## Image layers


class unit:

	xPos = 0
	yPos = 0
	bgColor = (0, 0, 0)
	outlineColor = (0, 0, 0)
	tileSizeWidth = 64
	tileSizeHeight = 32
	percentDone = 100.0
	resistance = 50.0
	score = 0

	def __init__(self):

		self.unHideGrid = False

	def createUnitImage(self):
		self.image = Image.new("RGBA", (self.tileSizeWidth, self.tileSizeHeight))
		self.draw = ImageDraw.Draw(self.image)

	def setUp(self):
		self.colOverlay = coloroverlay.ColorOverlay()
		self.colOverlay.randomSteps = True
		self.colOverlay.steps = self.config.steps
		self.colOverlay.maxBrightness = self.config.brightness
		self.colOverlay.tLimitBase = self.config.tLimitBase

		# self.score = 0 if random.random() > .5 else 1

		if self.useFixedPalette == True:

			self.colOverlay.minHue = self.palette[0]
			self.colOverlay.maxHue = self.palette[1]
			self.colOverlay.minSaturation = self.palette[2]
			self.colOverlay.maxSaturation = self.palette[3]
			self.colOverlay.minValue = self.palette[4]
			self.colOverlay.maxValue = self.palette[5]
			self.colOverlay.maxBrightness = self.colOverlay.maxValue

			self.colOverlay.dropHueMin = self.dropHueMin
			self.colOverlay.dropHueMax = self.dropHueMax

			self.colOverlay.colorB = [0, 0, 0]
			self.colOverlay.colorA = [0, 0, 0]
			self.colOverlay.currentColor = [0, 0, 0]
			self.colOverlay.autoChange = False
			self.colOverlay.randomRange = (
				self.colorStepsRangeMin,
				self.colorStepsRangeMax,
			)

			self.colOverlay.colorTransitionSetup()

	def getNeighbours(self):
		N = []
		previousRow = self.row - 1
		nextRow = self.row + 1
		previousCol = self.col - 1
		nextCol = self.col + 1

		N.append((previousCol, previousRow))
		N.append((self.col, previousRow))
		N.append((nextCol, previousRow))

		N.append((previousCol, self.row))
		N.append((nextCol, self.row))

		N.append((previousCol, nextRow))
		N.append((self.col, nextRow))
		N.append((nextCol, nextRow))

		return N

	def drawUnit(self):

		self.colOverlay.stepTransition()
		self.bgColor = tuple(
			int(a * config.brightness) for a in (self.colOverlay.currentColor)
		)

		fontColor = self.bgColor
		fontColor = (0, 0, 0)
		outlineColor = self.bgColor

		if self.unHideGrid == True:
			fontColor = config.fontColor
			outlineColor = config.outlineColor

		if self.config.showOutline == False:
			outlineColor = self.bgColor

		"""
		if self.colOverlay.gotoNextTransition == True :
			if self.colOverlay.getPercentageDone() > 50 :
				if random.random() > .1 :
					self.colOverlay.colorTransitionSetup()
		"""

		self.draw.rectangle(
			(0, 0, self.tileSizeWidth - 1, self.tileSizeHeight - 1),
			fill=self.bgColor,
			outline=outlineColor,
		)

		# displyInfo = displyInfo.encode('utf-8')
		if self.config.showText == True:
			# u"\u000D"
			displyInfo1 = str(self.col) + ", " + str(self.row)
			displyInfo2 = (
				str(self.col * self.tileSizeWidth)
				+ ", "
				+ str(self.row * self.tileSizeHeight)
			)
			self.draw.text((2, -1), str(self.unitNumber), fontColor, font=config.font)
			# self.draw.text((2,- 1), (displyInfo1), fontColor, font=config.font)
			# self.draw.text((2,- 1 + config.fontSize), (displyInfo2), fontColor, font=config.font)


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def makeGrid():
	global config
	unitNumber = 1
	config.unitArray = []
	del config.unitArray[:]
	config.gridArray = []
	config.gridArray = [[[] for i in range(config.rows)] for i in range(config.cols)]

	config.t1 = time.time()
	config.t2 = time.time()
	config.timeToComplete = round(random.uniform(120, 220))

	for row in range(0, config.rows):
		for col in range(0, config.cols):
			u = unit()
			u.config = config
			u.tileSizeWidth = config.tileSizeWidth
			u.tileSizeHeight = config.tileSizeHeight
			u.xPos = col * config.tileSizeWidth
			u.yPos = row * config.tileSizeHeight
			u.row = row
			u.col = col
			u.unitNumber = unitNumber
			u.useFixedPalette = config.useFixedPalette
			u.colorStepsRangeMin = config.colorStepsRangeMin
			u.colorStepsRangeMax = config.colorStepsRangeMax

			if config.useFixedPalette == True:
				if unitNumber <= config.paletteRange:
					u.palette = config.palette["p" + str(unitNumber)]
				else:
					u.palette = config.palette["p" + str(config.paletteRange)]
				u.dropHueMin = config.paletteDropHueMin
				u.dropHueMax = config.paletteDropHueMax

			u.createUnitImage()
			if config.coordinatedColorChange == False:
				u.setUp()

			u.bgColor = tuple(
				int(a * config.brightness) for a in (config.colOverlay.currentColor)
			)
			u.drawUnit()
			config.image.paste(u.image, (u.xPos + config.imageXOffset, u.yPos), u.image)

			config.unitArray.append(u)
			unitNumber += 1
			config.gridArray[col][row] = u


# "Conway Game of Life Like Redraw"
"Conway Game of Life Like Redraw"


def redrawGrid1():

	for u in config.unitArray:
		u.bgColor = tuple(
			int(a * config.brightness) for a in (config.colOverlay.currentColor)
		)
		u.drawUnit()
		config.image.paste(u.image, (u.xPos + config.imageXOffset, u.yPos), u.image)

		if u.colOverlay.complete == True:
			neighbours = u.getNeighbours()
			u.colOverlay.colorTransitionSetup()
			for unit in neighbours:
				col = unit[0]
				row = unit[1]
				if col >= 0 and col < config.cols and row >= 0 and row < config.rows:
					targetUnit = config.gridArray[col][row]
					if random.random() <= config.propagationProbability:
						if (
							targetUnit.colOverlay.getPercentageDone()
							> config.doneThreshold
						):
							targetUnit.colOverlay.colorTransitionSetup(
								newColor=u.colOverlay.colorB,
								steps=round(u.colOverlay.steps / 3),
							)

	config.render(config.image, 0, 0)


def redrawGrid2():

	for u in config.unitArray:
		u.bgColor = tuple(
			int(a * config.brightness) for a in (config.colOverlay.currentColor)
		)
		u.drawUnit()
		config.image.paste(u.image, (u.xPos + config.imageXOffset, u.yPos), u.image)

		neighbours = u.getNeighbours()
		u.colOverlay.colorTransitionSetup()

		score = 0

		## Count how many live neighbors there are out of 8 unless at edge (5) or corner (3)
		for unit in neighbours:
			col = unit[0]
			row = unit[1]
			if col >= 0 and col < config.cols and row >= 0 and row < config.rows:
				try:
					targetUnit = config.gridArray[col][row]

					if targetUnit.score == 1:
						score += 1
				except Exception as e:
					print(e, len(config.unitArray), unit, col, row)

		## If the cell is alive check if it's being overcrowded
		## or has too few neighbors to survive
		if u.score == 1:
			if score < config.underPopulationThreshold:
				u.score = 0

			## Should be > 3
			if score > config.overCrowdingThreshold:
				u.score = 0

			# if score > 1 and score < config.dieThreshold  :
			#     u.score = 1

		if u.score == 0:
			if score == config.liveThreshold:
				u.score = 1

		if u.score == 1:
			u.colOverlay.colorTransitionSetup(steps=round(u.colOverlay.steps / 3))

		if u.score == 0:
			u.colOverlay.colorTransitionSetup(newColor=(config.deadColor))

		if random.random() > config.propagationProbability:
			u.score = 1

	config.render(config.image, 0, 0)

	config.t2 = time.time()
	delta = config.t2 - config.t1

	if delta > config.timeToComplete:
		setUp()


## Setup and run functions
def main(run=True):
	global config, directionOrder
	global workConfig
	print("---------------------")
	print("propagation Loaded")

	colorutils.brightness = config.brightness
	config.canvasImageWidth = config.screenWidth
	config.canvasImageHeight = config.screenHeight
	config.canvasImageWidth -= 4
	config.canvasImageHeight -= 4
	config.delay = float(workConfig.get("propagation", "redrawDelay"))

	config.baseRotation = config.rotation

	config.fontColorVals = (workConfig.get("propagation", "fontColor")).split(",")
	config.fontColor = tuple(
		map(lambda x: int(int(x) * config.brightness), config.fontColorVals)
	)
	config.outlineColorVals = (workConfig.get("propagation", "outlineColor")).split(",")
	config.outlineColor = tuple(
		map(lambda x: int(int(x) * config.brightness), config.outlineColorVals)
	)

	config.coordinatedColorChange = False
	config.propagationProbability = float(
		workConfig.get("propagation", "propagationProbability")
	)
	config.doneThreshold = float(workConfig.get("propagation", "doneThreshold"))

	config.overCrowdingThreshold = int(
		workConfig.get("propagation", "overCrowdingThreshold")
	)
	config.underPopulationThreshold = int(
		workConfig.get("propagation", "underPopulationThreshold")
	)
	config.liveThreshold = int(workConfig.get("propagation", "liveThreshold"))
	# config.dieThreshold = int(workConfig.get("propagation","dieThreshold"))

	config.timeTrigger = workConfig.getboolean("propagation", "timeTrigger")
	config.tLimitBase = int(workConfig.get("propagation", "tLimitBase"))
	config.colOverlay = coloroverlay.ColorOverlay()
	config.colOverlay.randomSteps = False
	config.colOverlay.timeTrigger = False
	config.colOverlay.tLimitBase = config.tLimitBase
	config.colOverlay.maxBrightness = config.brightness
	config.unHideGrid = False
	config.colorStepsRangeMin = int(workConfig.get("propagation", "colorStepsRangeMin"))
	config.colorStepsRangeMax = int(workConfig.get("propagation", "colorStepsRangeMax"))

	config.rows = int(workConfig.get("propagation", "rows"))
	config.cols = int(workConfig.get("propagation", "cols"))

	deadColor = (workConfig.get("propagation", "deadColor")).split(",")
	config.deadColor = tuple(map(lambda x: float(x), deadColor))

	try:
		config.randomRotation = workConfig.getboolean("propagation", "randomRotation")
	except Exception as e:
		print(str(e))
		config.randomRotation = False

	try:
		config.showText = workConfig.getboolean("propagation", "showText")
	except Exception as e:
		print(str(e))
		config.showText = True

	try:
		config.showOutline = workConfig.getboolean("propagation", "showOutline")
	except Exception as e:
		print(str(e))
		config.showOutline = True

	try:
		config.steps = int(workConfig.get("propagation", "steps"))
	except Exception as e:
		print(str(e))
		config.steps = 200

	try:
		config.useFixedPalette = workConfig.getboolean("propagation", "useFixedPalette")
		config.paletteRange = int(workConfig.get("propagation", "paletteRange"))
		config.palette = {}
		for i in range(0, config.paletteRange):
			name = "p" + str(i + 1)
			vals = (workConfig.get("propagation", name)).split(",")
			config.palette[name] = tuple(map(lambda x: float(x), vals))
		# print(config.palette['p1'])
		config.paletteDropHueMin = int(workConfig.get("propagation", "dropHueMin"))
		config.paletteDropHueMax = int(workConfig.get("propagation", "dropHueMax"))

	except Exception as e:
		print(str(e))
		config.useFixedPalette = False

	config.colOverlay.steps = config.steps

	config.tileSizeWidth = int(workConfig.get("propagation", "tileSizeWidth"))
	config.tileSizeHeight = int(workConfig.get("propagation", "tileSizeHeight"))

	"""""" """""" """""" """""" """""" """""" """""" """""" """""" """"""

	config.canvasImage = Image.new(
		"RGBA", (config.canvasImageWidth, config.canvasImageHeight)
	)
	config.fontSize = 14
	config.font = ImageFont.truetype(
		config.path + "/assets/fonts/freefont/FreeSansBold.ttf", config.fontSize
	)

	setUp()

	if run:
		runWork()


def setUp():
	global config

	makeGrid()


def runWork():
	global blocks, config, XOs
	# gc.enable()
	while True:
		iterate()
		time.sleep(config.delay)


def iterate():

	global config
	redrawGrid2()


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
