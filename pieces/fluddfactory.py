# ################################################### #
import math
import random
import time
from modules.configuration import bcolors
from modules import coloroverlay, colorutils
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps

lastRate = 0
colorutils.brightness = 1
fludds = []


# Really no need for a class here - it's always a singleton and besides
# with Python everthing is an object already .... some kind of OOP
# holdover anxiety I guess


class Fludd:

	outlineColor = (1, 1, 1)
	barColor = (200, 200, 000)
	barColorStart = (0, 200, 200)
	holderColor = (0, 0, 0)
	messageClr = (200, 0, 0)
	shadowColor = (0, 0, 0)
	centerColor = (0, 0, 0)

	xPos = 1
	yPos = 1
	boxHeight = 100
	boxMax = 100
	status = 0
	rateMultiplier = 0.1
	rate = rateMultiplier * random.random()
	numRate = rate
	percentage = 0
	var = 10

	nothingLevel = 10
	nothingChangeProbability = 0.02

	usedFixedCenterColor = True

	borderModel = "prism"
	nothing = "void"
	varianceMode = "independent"
	prisimBrightness = 0.5

	steps = 20

	def __init__(self, config, i):
		# print ("init Fludd", i)

		# self.boxMax = config.screenWidth - 1
		# self.boxMaxAlt = self.boxMax + int(random.uniform(10,30) * config.screenWidth)
		# self.boxHeight = config.screenHeight - 2        #

		self.unitNumber = i
		self.config = config

	def done1(self):

		self.colOverlay = coloroverlay.ColorOverlay()
		self.colOverlay.randomSteps = True
		self.colOverlay.timeTrigger = True
		self.colOverlay.tLimitBase = self.config.tLimitBase
		self.colOverlay.steps = 10

		self.colOverlay.minHue = 0
		self.colOverlay.maxHue = 360
		self.colOverlay.minSaturation = 0.1
		self.colOverlay.maxSaturation = 1
		self.colOverlay.minValue = 0.1
		self.colOverlay.maxValue = 1

		self.colOverlay.randomRange = (
			self.config.transitionStepsMin,
			self.config.transitionStepsMax,
		)

		self.colOverlay.colorTransitionSetup()
		self.fillColor = tuple(
			round(a * self.config.brightness) for a in self.colOverlay.currentColor
		)

	def done2(self):
		## Used for the center if fixedColorCenter is not chosen ....
		self.colOverlay2 = coloroverlay.ColorOverlay()
		self.colOverlay2.randomSteps = True
		self.colOverlay2.timeTrigger = True
		self.colOverlay2.tLimitBase = self.config.tLimitBase
		self.colOverlay2.steps = 10

		self.colOverlay2.minHue = 0
		self.colOverlay2.maxHue = 360
		self.colOverlay2.minSaturation = 0.1
		self.colOverlay2.maxSaturation = 1
		self.colOverlay2.minValue = 0.1
		self.colOverlay2.maxValue = 1

		### This is the speed range of transitions in color
		### Higher numbers means more possible steps so slower
		### transitions - 1,10 very blinky, 10,200 very slow
		self.colOverlay2.randomRange = (
			self.config.transitionStepsMin,
			self.config.transitionStepsMax,
		)
		self.colOverlay2.colorTransitionSetup()

	def setUp(self):

		self.tempImage = Image.new("RGBA", (self.boxMax, self.boxHeight))
		self.draw = ImageDraw.Draw(self.tempImage)
		#### Sets up color transitions

		"""
			colOverlay.randomSteps = True
			colOverlay.timeTrigger = True 
			colOverlay.tLimitBase = 2
			colOverlay.steps = 10
					
			colOverlay.maxBrightness = self.config.brightness
			colOverlay.maxBrightness = self.fillColors[i].valueRange[0]

			colOverlay.minHue = self.fillColors[i].hueRange[0]
			colOverlay.maxHue = self.fillColors[i].hueRange[1]                
			colOverlay.minSaturation = self.fillColors[i].saturationRange[0]
			colOverlay.maxSaturation = self.fillColors[i].saturationRange[1]
			colOverlay.minValue = self.fillColors[i].valueRange[0]
			colOverlay.maxValue = self.fillColors[i].valueRange[1]


			### This is the speed range of transitions in color
			### Higher numbers means more possible steps so slower
			### transitions - 1,10 very blinky, 10,200 very slow
			colOverlay.randomRange = (self.config.transitionStepsMin,self.config.transitionStepsMax)
		"""

		self.colOverlay = coloroverlay.ColorOverlay(True)
		self.colOverlay.randomSteps = True
		self.colOverlay.timeTrigger = True
		self.colOverlay.tLimitBase = self.config.tLimitBase
		self.colOverlay.steps = 10

		self.colOverlay.minHue = 0
		self.colOverlay.maxHue = 360
		self.colOverlay.minSaturation = 0.1
		self.colOverlay.maxSaturation = 1
		self.colOverlay.minValue = 0.1
		self.colOverlay.maxValue = 1
		# self.colOverlay.callBackDoneMethod = self.done

		### This is the speed range of transitions in color
		### Higher numbers means more possible steps so slower
		### transitions - 1,10 very blinky, 10,200 very slow
		self.colOverlay.randomRange = (
			self.config.transitionStepsMin,
			self.config.transitionStepsMax,
		)
		self.colOverlay.colorTransitionSetup()

		self.fillColor = tuple(
			round(a * self.config.brightness) for a in self.colOverlay.currentColor
		)

		## Used for the center if fixedColorCenter is not chosen ....
		self.colOverlay2 = coloroverlay.ColorOverlay(True)
		self.colOverlay2.randomSteps = True
		self.colOverlay2.timeTrigger = True
		self.colOverlay2.tLimitBase = self.config.tLimitBase
		self.colOverlay2.steps = 10

		self.colOverlay2.minHue = 0
		self.colOverlay2.maxHue = 360
		self.colOverlay2.minSaturation = 0.1
		self.colOverlay2.maxSaturation = 1
		self.colOverlay2.minValue = 0.1
		self.colOverlay2.maxValue = 1
		# self.colOverlay2.callBackDoneMethod = self.done2

		### This is the speed range of transitions in color
		### Higher numbers means more possible steps so slower
		### transitions - 1,10 very blinky, 10,200 very slow
		self.colOverlay2.randomRange = (
			self.config.transitionStepsMin,
			self.config.transitionStepsMax,
		)
		self.colOverlay2.colorTransitionSetup()

		self.widthDelta = 0
		self.heightDelta = 0
		self.xDelta = 0
		self.yDelta = 0

		if self.usedFixedCenterColor == True:
			self.centerColor = self.fixedCenterColor
		else:
			centerColorTemp = tuple(
				round(a * self.config.brightness) for a in self.colOverlay2.currentColor
			)
			self.centerColor = (
				round(centerColorTemp[0] * self.config.redBoost),
				round(centerColorTemp[1] * self.config.greenBoost),
				round(centerColorTemp[2] * self.config.blueBoost),
				centerColorTemp[3],
			)

	def changeAction(self):
		return False

	def setNewBox(self):
		svarwNew = random.uniform(0, self.varX)
		svarhNew = random.uniform(0, self.varY)

		self.symBoxWidthNew = self.boxMax - svarwNew
		self.symBoxHeightNew = self.boxHeight - svarhNew

		self.xPos1New = self.boxMax - self.symBoxWidthNew
		self.yPos1New = self.boxHeight - self.symBoxHeightNew

		self.widthDelta = (
			self.symBoxWidthNew - self.symBoxWidth
		) / self.config.transitionStepsMax
		self.heightDelta = (
			self.symBoxHeightNew - self.symBoxHeight
		) / self.config.transitionStepsMax

		self.xDelta = (self.xPos1New - self.xPos1) / self.config.transitionStepsMax
		self.yDelta = (self.yPos1New - self.yPos1) / self.config.transitionStepsMax

		# print (self.symBoxWidth,self.symBoxWidthNew)
		# print (self.symBoxHeight,self.symBoxHeightNew)

	def transitionBox(self):

		if (
			abs(math.floor(self.symBoxWidth)) != math.floor(self.symBoxWidthNew)
			and abs(self.symBoxWidth) < self.boxMax
			and self.symBoxWidth > 0
		):
			self.symBoxWidth += self.widthDelta
			self.xPos1 += self.xDelta
		else:
			self.symBoxWidth = self.symBoxWidthNew
			self.xPos1 = self.xPos1New
			self.widthDelta = 0
			self.xDelta = 0

		if (
			abs(math.floor(self.symBoxHeight)) != math.floor(self.symBoxHeightNew)
			and abs(self.symBoxHeight) < self.boxHeight
			and self.symBoxHeight > 0
		):
			self.symBoxHeight += self.heightDelta
			self.yPos1 += self.yDelta
		else:
			self.symBoxHeight = self.symBoxHeightNew
			self.yPos1 = self.yPos1New
			self.heightDelta = 0
			self.yDelta = 0

		if self.varianceMode == "symmetrical":
			self.yPos1 = self.xPos1
			self.symBoxHeight = self.symBoxWidth

	def transition(self):
		self.fillColor = tuple(
			round(a * self.config.brightness) for a in self.colOverlay.currentColor
		)
		fillColorTemp = tuple(
			round(a * self.config.brightness) for a in self.colOverlay.currentColor
		)
		self.fillColor = (
			round(fillColorTemp[0] * self.config.redBoost),
			round(fillColorTemp[1] * self.config.greenBoost),
			round(fillColorTemp[2] * self.config.blueBoost),
			fillColorTemp[3],
		)
		# print(fillColorTemp, self.fillColor)

		try:
			# self.fillColor = (100,50,50)
			self.draw.rectangle(
				(0, 0, self.boxMax, self.boxHeight), fill=self.fillColor, outline=None
			)
			self.draw.rectangle(
				(
					round(self.xPos1),
					round(self.yPos1),
					round(self.symBoxWidth),
					round(self.symBoxHeight),
				),
				fill=self.centerColor,
				outline=None,
			)
			self.colOverlay.stepTransition()

			if self.usedFixedCenterColor == False:
				self.colOverlay2.stepTransition()
				self.centerColor = tuple(
					round(a * self.config.brightness)
					for a in self.colOverlay2.currentColor
				)
				centerColorTemp = tuple(
					round(a * self.config.brightness)
					for a in self.colOverlay2.currentColor
				)
				self.centerColor = (
					round(centerColorTemp[0] * self.config.redBoost),
					round(centerColorTemp[1] * self.config.greenBoost),
					round(centerColorTemp[2] * self.config.blueBoost),
					centerColorTemp[3],
				)

			self.transitionBox()
		except Exception as e:
			print(e, self.fillColor)

	def reDraw(self):
		varX = self.varX
		varY = self.varY

		gray = 126
		brightness = self.config.brightness * random.random()
		light = round(brightness * self.nothingLevel)

		if self.nothing == "void":
			gray = 0
		else:
			gray = round(
				self.config.brightness * random.random() * self.nothingLevel / 2
			)
			light = 0

		self.draw.rectangle(
			(0, 0, self.boxMax, self.boxHeight), fill=(0, 0, 0), outline=None
		)
		# config.draw.rectangle((0,0,self.boxMax,self.boxHeight), fill = (light,light,light))
		if self.borderModel == "prism":
			outerBorder = colorutils.randomColor(self.prisimBrightness)
		else:
			outerBorder = (light, light, light)

		self.draw.rectangle(
			(0, 0, self.boxMax, self.boxHeight), fill=outerBorder, outline=None
		)

		if self.varianceMode == "independent":
			xPos1 = random.uniform(-varX / 2, varX)
			yPos1 = random.uniform(-varY / 2, varY)

			xPos2 = random.uniform(self.boxMax - varX, self.boxMax + varX)
			yPos2 = random.uniform(-varY / 2, varY)

			xPos3 = random.uniform(self.boxMax - varX, self.boxMax + varX)
			yPos3 = random.uniform(self.boxHeight - varY, self.boxHeight + varY)

			xPos4 = random.uniform(-varX / 2, varX)
			yPos4 = random.uniform(self.boxHeight - varY, self.boxHeight + varY)

			self.draw.polygon(
				(xPos1, yPos1, xPos2, yPos2, xPos3, yPos3, xPos4, yPos4),
				fill=(gray, gray, gray),
				outline=None,
			)

		elif self.varianceMode == "symmetrical":
			svar = random.uniform(0, varX)
			self.symBoxWidth = self.boxMax - svar
			self.symBoxHeight = self.boxHeight - svar
			xy0 = svar
			self.xPos1 = xy0
			self.yPos1 = xy0
			self.draw.rectangle(
				(xy0, xy0, self.symBoxWidth, self.symBoxHeight),
				fill=(gray, gray, gray),
				outline=None,
			)
			self.setNewBox()

		elif self.varianceMode == "asymmetrical":
			self.svarw = random.uniform(0, varX)
			self.svarh = random.uniform(0, varY)
			self.symBoxWidth = self.boxMax - self.svarw
			self.symBoxHeight = self.boxHeight - self.svarh
			self.xPos1 = self.boxMax - self.symBoxWidth
			self.yPos1 = self.boxHeight - self.symBoxHeight
			self.draw.rectangle(
				(self.xPos1, self.yPos1, self.symBoxWidth, self.symBoxHeight),
				fill=self.config.fixedCenterColor,
				outline=None,
			)
			self.setNewBox()

		if random.random() < self.nothingChangeProbability:
			self.nothingLevel = random.uniform(0, 255)

		# Finally composite full image
		# config.image.paste(self.mainImage, (numXPos, numYPos), self.scrollImage)

	def change(self):
		if self.varianceMode == "independent":
			self.varianceMode = "symmetrical"
		elif self.varianceMode == "symmetrical":
			self.varianceMode = "asymmetrical"
		elif self.varianceMode == "asymmetrical":
			self.varianceMode = "independent"

		if self.borderModel == "prism":
			self.borderModel = "plenum"
		else:
			self.borderModel = "prism"

		print(self.varianceMode)
		# if(self.config.demoMode != 0) : print(self.varianceMode, self.borderModel)

	def done(self):
		return True


def drawElement():
	global config
	return True


def redraw():
	global config, fludds
	squareCount = 0

	## Each Fludd-square is generated as an image and then pasted into its correct
	## place in the grid - or off-grid maybe sometime

	for r in range(0, config.rowsOfSquares):
		for c in range(0, config.colsOfSquares):
			fluddSquare = fludds[squareCount]
			fluddSquare.transition()
			config.image.paste(
				fluddSquare.tempImage,
				(c * config.boxWidth, r * config.boxHeight),
				fluddSquare.tempImage,
			)
			squareCount += 1

			if random.random() < config.changeBoxProb:
				fluddSquare.setNewBox()


def runWork():
	global config
	print(bcolors.OKGREEN + "** " + bcolors.BOLD)
	print ("Running fluddfactory.py")
	print(bcolors.ENDC)
	while True:
		iterate()
		time.sleep(config.redrawSpeed)


def iterate():
	global config, fluddSquare, lastRate, calibrated, cycleCount

	if config.calibrated == True:
		redraw()
		config.render(config.image, 0, 0, config.screenWidth, config.screenHeight)

		if config.demoMode != 0:
			config.count += 1

			if config.count > config.countMax:
				config.count = 0
				config.t2 = time.time()
				config.timeToComplete = config.t2 - config.t1
				print(config.timeToComplete)
				config.t1 = time.time()
				config.t2 = time.time()
				for i in range(0, config.numberOfSquares):
					fludds[i].change()
	else:
		config.cycleCount += 1
		redraw()
		config.render(config.image, 0, 0, config.screenWidth, config.screenHeight)
		if config.cycleCount > config.calibrationCount:
			config.t2 = time.time()
			config.timeToComplete = config.t2 - config.t1
			config.timeItShouldHaveTaken = config.calibrationCount * config.redrawSpeed

			config.cycleTiming = config.timeToComplete / config.timeItShouldHaveTaken

			config.countMax = (
				config.demoMode * config.calibrationCount / config.timeToComplete
			)
			config.calibrated = True

			print(
				"config.timeItShouldHaveTaken, config.timeToComplete, config.countMax"
			)
			print(config.timeItShouldHaveTaken, config.timeToComplete, config.countMax)

			config.t1 = time.time()
			config.t2 = time.time()

	# Done


def main(run=True):
	global config
	global fludds
	global workConfig
	fludds = []
	config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.draw = ImageDraw.Draw(config.image)

	config.rowsOfSquares = int(workConfig.get("fludd", "rowsOfSquares"))
	config.colsOfSquares = int(workConfig.get("fludd", "colsOfSquares"))
	config.numberOfSquares = config.rowsOfSquares * config.colsOfSquares

	config.boxWidth = int(round(config.canvasWidth / config.colsOfSquares))
	config.boxHeight = int(round(config.canvasHeight / config.rowsOfSquares))
	config.tLimitBase = int(workConfig.get("fludd", "tLimitBase"))
	config.transitionStepsMin = int(workConfig.get("fludd", "transitionStepsMin"))
	config.transitionStepsMax = int(workConfig.get("fludd", "transitionStepsMax"))
	config.changeBoxProb = float(workConfig.get("fludd", "changeBoxProb"))

	config.fixedCenterColorVals = (workConfig.get("fludd", "fixedCenterColor")).split(
		","
	)
	config.fixedCenterColor = tuple(
		map(lambda x: int(int(x) * config.brightness), config.fixedCenterColorVals)
	)
	config.usedFixedCenterColor = workConfig.getboolean("fludd", "usedFixedCenterColor")

	try:
		config.varianceX = int(workConfig.get("fludd", "varianceX"))
		config.varianceY = int(workConfig.get("fludd", "varianceY"))

	except Exception as e:

		config.varianceX = int(workConfig.get("fludd", "var"))
		config.varianceY = int(workConfig.get("fludd", "var"))
		print(str(e))

	# print(config.boxWidth, config.boxHeight)

	squareCount = 0

	for r in range(0, config.rowsOfSquares):
		for c in range(0, config.colsOfSquares):
			fluddSquare = Fludd(config, squareCount)
			# Prism is all colors, Plenum is white
			fluddSquare.borderModel = workConfig.get("fludd", "borderModel")
			fluddSquare.nothing = workConfig.get("fludd", "nothing")
			fluddSquare.varX = config.varianceX
			fluddSquare.varY = config.varianceY
			fluddSquare.varianceMode = workConfig.get("fludd", "varianceMode")
			fluddSquare.prisimBrightness = float(
				workConfig.get("fludd", "prisimBrightness")
			)
			fluddSquare.boxMax = config.boxWidth
			fluddSquare.boxHeight = config.boxHeight
			fluddSquare.usedFixedCenterColor = config.usedFixedCenterColor
			fluddSquare.fixedCenterColor = config.fixedCenterColor

			fluddSquare.setUp()
			fluddSquare.reDraw()
			config.redrawSpeed = float(workConfig.get("fludd", "redrawSpeed"))
			fludds.append(fluddSquare)
			squareCount += 1

	config.cycleTiming = 1
	config.t1 = time.time()
	config.t2 = time.time()

	config.calibrated = True
	config.cycleCount = 0
	config.calibrationCount = 500

	## -----------------------------------------------------------------------
	## Demo mode means the piece cycles through its 6 base
	## variation plenum | prism  X  independent | asymmetrical | symmetrical
	## -----------------------------------------------------------------------

	config.demoMode = float(workConfig.get("fludd", "demoMode"))
	config.count = 0

	# var sets the points offset from the corners - i.e. the larger var is, the wider the borders
	"""
	************
	*           *
	 *           *
	  *          * 
	   ***********
		
	"""

	if run:
		runWork()
