# ################################################### #
import argparse
import math
import random
import time
import types
from modules.configuration import bcolors
from modules import badpixels, coloroverlay, colorutils, panelDrawing, pattern_blocks
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps, ImageFilter
import numpy as np


###############################################

class Fader:
	def __init__(self):
		self.doingRefresh = 0
		self.doingRefreshCount = 20
		self.fadingDone = False
		self.testing = True

	def setUp(self):
		self.blankImage = Image.new("RGBA", (self.width, self.height))
		self.image = Image.new("RGBA", (self.width, self.height))
		self.crossFade = Image.new("RGBA", (self.width, self.height))

	def test(self):
		print("test")
		#self.blankImage = Image.new("RGBA", (self.width, self.height))
		draw = ImageDraw.Draw(self.crossFade)
		draw.rectangle((0,0,100,100), fill=(0,0,255,255))
		config.image.paste(
			self.crossFade, (self.xPos, self.yPos), self.crossFade
		)

	def fadeIn(self, config):
		config.fadeThruBlack = False
		if self.fadingDone == False:

			if self.testing == True :
				self.testing = False
				#print(self.fadingDone, self.doingRefresh)

			if self.doingRefresh < self.doingRefreshCount:

				if config.fadeThruBlack == True :
					self.blankImage = Image.new("RGBA", (self.width, self.height))
				percent  = self.doingRefresh / self.doingRefreshCount
				self.crossFade = Image.blend(
					self.blankImage,
					self.image,
					percent,
				)
				config.image.paste(
					self.crossFade, (self.xPos, self.yPos), self.crossFade
				)
				self.doingRefresh += 1
			else:
				config.image.paste(self.image, (self.xPos, self.yPos), self.image)
				self.fadingDone = True
				self.doingRefresh = 0
				self.blankImage = self.image.copy()
				self.testing = True


def redraw(config):

	if config.patternModel == "wavePattern":
		pattern_blocks.wavePattern(config)

	if config.patternModel == "reMove":
		pattern_blocks.reMove(config)

	if config.patternModel == "diagonalMove":
		pattern_blocks.diagonalMove(config)

	if config.patternModel == "randomizer":
		pattern_blocks.randomizer(config)

	if config.patternModel == "runningSpiral":
		pattern_blocks.runningSpiral(config)

	if config.patternModel == "concentricBoxes":
		pattern_blocks.concentricBoxes(config)

	if config.patternModel == "diamond":
		pattern_blocks.diamond(config)

	if config.patternModel == "shingles":
		pattern_blocks.shingles(config)

	if config.patternModel == "balls":
		pattern_blocks.balls(config)

	if config.patternModel == "bars":
		pattern_blocks.bars(config)


def repeatImage(config):
	cntr = 0
	# 2021-06-28 Opted to build the repetition/tiling vertically instead of horizontally
	# to suit the graph piece better and upwards or downwards is better than sideways sometimes
	# so reversed the order of "for c in ..." with "for r in range(..." so builds rows vertically

	# 2022-07-12 Changed my mind because the graph piece is not going to get this code - going for a
	# tower configuration

	#config.transitionImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))

	for c in range(0, config.cols):
		for r in range(0, config.rows):
			if cntr in config.skipBlocks:
				config.canvasDraw.rectangle((c * config.blockWidth, r * config.blockHeight, c * config.blockWidth + config.blockWidth,
											 r * config.blockHeight + config.blockHeight), fill=config.bgColor, outline=config.bgColor)
			else:
				temp = config.blockImage.copy()
				temp = temp.rotate(90)
				if c % 2 != 0 and config.rotateAltBlock == 1:
					temp = temp.rotate(-90)

				config.canvasImage.paste(temp, (c * config.blockWidth-c, r * config.blockHeight-r), temp)
				#config.transitionImage.paste(temp, (c * config.blockWidth-c, r * config.blockHeight-r), temp)

			if config.patternModelVariations == True:
				for s in config.patternSequence:
					if cntr == s[1]:
						config.patternModel = s[0]
						config.rotateAltBlock = s[2]
						func = eval("pattern_blocks." + s[0])
						func(config)

			cntr += 1


def rebuildPatternSequence(config):

	config.patternSequence = []
	numberOfPatterns = round(random.uniform(2, 4))
	config.numConcentricBoxes = round(random.uniform(8, 18))
	lastPosition = 0
	totalSlots = config.rows * config.cols

	if random.random() < .5:
		config.altLineColoring = True
	else:
		config.altLineColoring = False

	# for i in range(0,numberOfPatterns) :
	i = 0
	usedPatterns = []
	while i < numberOfPatterns:
		pattern = config.patterns[math.floor(random.uniform(0, len(config.patterns)))]

		if pattern not in usedPatterns:
			if pattern not in (["shingles", "fishScales", "balls"]):
				rotate = round(random.uniform(0, 1))
			else:
				rotate = 0
			slotsLeft = totalSlots - lastPosition
			position = round(random.uniform(lastPosition, slotsLeft-1))
			config.patternSequence.append([pattern, position, rotate])
			usedPatterns.append(pattern)
			lastPosition = position
			i += 1


def loadImageForBase():
	#image = Image.open("./assets/imgs/drawings/P1060494.jpg", "r")
	#image = Image.open("./assets/imgs/miscl/comp-384.jpg", "r")
	#image = Image.open("./assets/imgs/miscl/lm_a.png", "r")

	i = math.floor(random.random() * len(config.imageSources))
	imagePath  = config.imageSources[i]
	print(imagePath)
	image = Image.open(imagePath)
	image.load()
	config.canvasImage.paste(image, (0, 0))


def getConfigOverlay(tLimitBase, minHue, maxHue, minSaturation, maxSaturation, minValue, maxValue):
	colOverlay = coloroverlay.ColorOverlay()
	colOverlay.randomSteps = False
	colOverlay.timeTrigger = True
	colOverlay.tLimitBase = tLimitBase
	colOverlay.maxBrightness = 1
	colOverlay.steps = 50
	colOverlay.minHue = minHue
	colOverlay.maxHue = maxHue
	colOverlay.minSaturation = minSaturation
	colOverlay.maxSaturation = maxSaturation
	colOverlay.minValue = minValue
	colOverlay.maxValue = maxValue
	colOverlay.colorTransitionSetup()
	return colOverlay


def buildPalette(config, index=0):

	palette = config.palettes[index]

	tLimitBase = int(workConfig.get(palette, "tLimitBase"))
	minHue = float(workConfig.get(palette, "minHue"))
	maxHue = float(workConfig.get(palette, "maxHue"))
	minSaturation = float(workConfig.get(palette, "minSaturation")	)
	maxSaturation = float(workConfig.get(palette, "maxSaturation"))
	minValue = float(workConfig.get(palette, "minValue"))
	maxValue = float(workConfig.get(palette, "maxValue"))
	#config.colOverlay = getConfigOverlay(tLimitBase, minHue, maxHue, minSaturation, maxSaturation, minValue, maxValue)
	config.colOverlay = Holder()
	config.colOverlay.currentColor = [10, 10, 10, 100]
	config.colOverlay.currentColor = colorutils.getRandomColorHSV(minHue, maxHue, minSaturation, maxSaturation, minValue, maxValue, 0, 0,
																  round(random.uniform(config.bgColorAlpha[0], config.bgColorAlpha[1])))
	config.colOverlay.bgColor = colorutils.getRandomColorHSV(
		minHue, maxHue, minSaturation, maxSaturation, minValue, maxValue)

	tLimitBase = int(workConfig.get(palette, "line_tLimitBase"))
	minHue = float(workConfig.get(palette, "line_minHue"))
	maxHue = float(workConfig.get(palette, "line_maxHue"))
	minSaturation = float(workConfig.get(palette, "line_minSaturation")	)
	maxSaturation = float(workConfig.get(palette, "line_maxSaturation"))
	minValue = float(workConfig.get(palette, "line_minValue"))
	maxValue = float(workConfig.get(palette, "line_maxValue"))
	#config.linecolOverlay = getConfigOverlay(tLimitBase, minHue, maxHue, minSaturation, maxSaturation, minValue, maxValue)
	config.linecolOverlay = Holder()
	config.linecolOverlay.currentColor = [200, 10, 10]
	config.linecolOverlay.currentColor = colorutils.getRandomColorHSV(
		minHue, maxHue, minSaturation, maxSaturation, minValue, maxValue)

	tLimitBase = int(workConfig.get(palette, "line2_tLimitBase"))
	minHue = float(workConfig.get(palette, "line2_minHue"))
	maxHue = float(workConfig.get(palette, "line2_maxHue"))
	minSaturation = float(workConfig.get(palette, "line2_minSaturation")	)
	maxSaturation = float(workConfig.get(palette, "line2_maxSaturation"))
	minValue = float(workConfig.get(palette, "line2_minValue"))
	maxValue = float(workConfig.get(palette, "line2_maxValue"))
	#config.linecolOverlay2 = getConfigOverlay(tLimitBase, minHue, maxHue, minSaturation, maxSaturation, minValue, maxValue)
	config.linecolOverlay2 = Holder()
	config.linecolOverlay2.currentColor = [10, 100, 10]
	config.linecolOverlay2.currentColor = colorutils.getRandomColorHSV(
		minHue, maxHue, minSaturation, maxSaturation, minValue, maxValue)

	#config.colOverlay.currentColor = colorutils.getRandomColorHSV(minHue, maxHue, minSaturation, maxSaturation, minValue, maxValue,0,0,200)
	#config.canvasDraw.rectangle((0,0,config.canvasWidth, config.canvasHeight), fill = config.colOverlay.currentColor)
	#config.colOverlay.currentColor = colorutils.getRandomColorHSV(minHue, maxHue, minSaturation, maxSaturation, minValue, maxValue,0,0,10)


def writeImage(baseName, renderImage):
	#baseName = "outputquad3/comp2_"
	if config.saveImages == True :
		fn = baseName+".png"
		renderImage.save(fn)


def rebuildPatterns(arg=0) :

	c = round(random.uniform(1,3))

	if c ==1 :
		if config.numRowsRandomize == True:
			config.numRows = round(random.uniform(1, 2))
			config.numShingleRows = round(random.uniform(1, 2))
			dotRows = [1, 2, 4]
			config.numDotRows = dotRows[round(random.uniform(0, 2))]

	if c == 2 :
		newPalette = math.floor(random.uniform(0, len(config.palettes)))
		if newPalette == len(config.palettes):
			newPalette = 0
		buildPalette(config, newPalette)

	if c == 3 :
		rebuildPatternSequence(config)

	config.repeatDrawingMode = 1
	config.fader.doingRefreshCount = 20
	rebuildSections()

###############################################


def rebuildSections():
	global config

	if random.random() < config.changeDisturbanceSetProb :
		setNumber = math.floor(random.uniform(0,len(config.disturbanceConfigSets)))
		setUpDisturbanceConfigs(config.disturbanceConfigSets[setNumber])
		print("REBUILDSECTIONS RUNNING NOW: " + config.disturbanceConfigSets[setNumber])
		
	if random.random() < .5 :
		config.speedDeAcceleration = config.speedDeAccelerationUpperLimit
	else :
		speedDeAcceleration = config.speedDeAccelerationBase

	baseSpeed = config.baseSectionSpeed
	for i in range(0, config.numberOfSections):
		section = config.movingSections[i]
		section.sectionRotation = random.uniform(-config.sectionRotationRange, config.sectionRotationRange)
		section.sectionPlacement = [round(random.uniform(config.sectionPlacementXRange[0], config.sectionPlacementXRange[1])), round(
			random.uniform(config.sectionPlacementYRange[0], config.sectionPlacementYRange[1]))]
		section.sectionPlacementInit = [section.sectionPlacement[0], section.sectionPlacement[1]]
		section.sectionSize = [round(random.uniform(config.sectionWidthRange[0], config.sectionWidthRange[1])), round(
			random.uniform(config.sectionHeightRange[0], config.sectionHeightRange[1]))]
		section.sectionSpeed = [random.uniform(-baseSpeed, baseSpeed)/config.sectionSpeedFactorHorizontal,
								random.uniform(-baseSpeed, baseSpeed)/config.sectionSpeedFactorVertical]
		section.rotationSpeed = random.uniform(-baseSpeed, baseSpeed)
		section.actionCount = 0
		section.actionCountLimit = round(random.uniform(10, config.sectionMovementCountMax))
		section.done = False
		section.stopProb = random.uniform(0, config.stopProb)
	config.drawingPrinted = False


#############################################


class Holder:
	def __init__(self):
		pass


class Director:
	"""docstring for Director"""

	slotRate = .5

	def __init__(self, config):
		super(Director, self).__init__()
		self.config = config
		self.tT = time.time()

	def checkTime(self):
		if (time.time() - self.tT) >= self.slotRate:
			self.tT = time.time()
			self.advance = True
		else:
			self.advance = False

	def next(self):
		self.checkTime()


def disturber():
	config.doneCount = 0

	if config.doSectionDisturbance == True :
		for i in range(0, config.numberOfSections):
			sectionParams = config.movingSections[i]
			if sectionParams.actionCount >= sectionParams.actionCountLimit:
				#sectionParams.rotationSpeed = 0
				#sectionParams.sectionSpeed[0] = 0
				#sectionParams.sectionSpeed[1] = 0
				config.doneCount += 1
			

			if sectionParams.actionCount < sectionParams.actionCountLimit:

				xPos = round(sectionParams.sectionPlacementInit[0])
				yPos = round(sectionParams.sectionPlacementInit[1])
				section = config.canvasImage.crop(
					(xPos, yPos, xPos + sectionParams.sectionSize[0], yPos + sectionParams.sectionSize[1]))
				'''
				section = section.rotate(sectionParams.sectionRotation, Image.NEAREST, True)
				sectionParams.sectionRotation += sectionParams.rotationSpeed
				'''

				config.canvasImage.paste(section, (round(sectionParams.sectionPlacement[0]), round(
					sectionParams.sectionPlacement[1])), section)

				delta = (sectionParams.actionCountLimit - sectionParams.actionCount)/sectionParams.actionCountLimit
				#rads = (math.pi / 2) / sectionParams.actionCountLimit
				#d = 1.0 - math.sin(sectionParams.actionCount * rads)
				#d = 1.0 - math.pow(3, -.9 * delta)

				d = math.pow(delta,8)
				d =1

				sectionParams.sectionPlacement[0] += sectionParams.sectionSpeed[0] * d
				sectionParams.sectionPlacement[1] += sectionParams.sectionSpeed[1] * d
				sectionParams.sectionSpeed[0] *= config.speedDeAcceleration
				sectionParams.sectionSpeed[1] *= config.speedDeAcceleration

				'''
				if sectionParams.sectionSpeed[0] != 0:
					sectionParams.sectionSpeed[0] = delta/sectionParams.sectionSpeed[0] 
				if sectionParams.sectionSpeed[1] != 0:
					sectionParams.sectionSpeed[1] = delta/sectionParams.sectionSpeed[1] 
				'''

				# add some better easing

				sectionParams.actionCount += 1

				if random.random() < sectionParams.stopProb:
					sectionParams.rotationSpeed = 0
				if random.random() < sectionParams.stopProb:
					sectionParams.sectionSpeed[0] = 0
				if random.random() < sectionParams.stopProb:
					sectionParams.sectionSpeed[1] = 0

def runWork():
	global config
	print(bcolors.OKGREEN + "** " + bcolors.BOLD)
	print("Running repeatblocks.py")
	print(bcolors.ENDC)
	while config.isRunning == True:
		config.directorController.checkTime()
		if config.directorController.advance == True:
			iterate()
		time.sleep(config.redrawSpeed)
		if config.standAlone == False:
			config.callBack()


def iterate():
	global config
	# config.colOverlay.stepTransition()
	# config.linecolOverlay.stepTransition()
	# config.linecolOverlay2.stepTransition()


	config.bgColor = tuple(
		round(a * config.brightness) for a in (config.colOverlay.currentColor)
	)

	#redraw(config)

	#repeatImage(config)

	if config.repeatDrawingMode == 1:
		redraw(config)

		if random.random() < config.loadAnImageProb:
			loadImageForBase()
		else:
			repeatImage(config)

		config.repeatDrawingMode = 0

	if random.random() < .005 and config.usePixelSortRandomize == True:
		config.usePixelSort = False

	if random.random() < .005 and config.usePixelSortRandomize == True:
		config.usePixelSort = True

	if config.randomizeSpeed == True:

		if random.random() < .03:
			config.ySpeed = config.ySpeedInit

		if random.random() < .1:
			config.ySpeed = 0

	if random.random() < .0005:
		config.triangles = True

	if random.random() < .01:
		config.triangles = False


	# paste over a section of the image on to itself and rotate
	if config.sectionDisturbance == True and config.fader.fadingDone == True:
		disturber()

	# a blurred section distrubance
	if config.useBlurSection == True:
		cp = config.canvasImage.copy()
		mask_blur = config.mask.filter(ImageFilter.GaussianBlur(config.mask_blur_amt))
		cp_blur = cp.filter(ImageFilter.GaussianBlur(config.cp_blur_amt))
		config.canvasImage = Image.composite(cp_blur, config.canvasImage, mask_blur)

	if config.fader.fadingDone == True:
		config.fader.fadingDone = False
		config.fader.image = config.canvasImage
		config.fader.doingRefreshCount = 0
		# Rebuild the main pattern, halt any disturbances immediately - i.e. don't wait 
		if config.doneCount >= (config.numberOfSections ) and config.rebuildImmediatelyAfterDone == True:
			config.doSectionDisturbance = False
			rebuildPatterns()
		
	if config.doneCount >= config.numberOfSections and config.drawingPrinted == False and config.saveImages == True :
		config.fader.doingRefreshCount = 40
		config.drawingPrinted = True
		currentTime = time.time()
		baseName = config.outPutPath + str(currentTime)
		writeImage(baseName, renderImage=config.canvasImage)


	# Rebuild the main pattern, halt any disturbances
	if random.random() < config.rebuildPatternProbability:
		config.doSectionDisturbance = False
		rebuildPatterns()	

	# RANDOM OVERLAY REPETITION DISTURBANCE
	if random.random() < config.redoSectionDisturbance and config.sectionDisturbance == True:
		config.doSectionDisturbance = True 
		rebuildSections()

	if config.shingleVariation == True:
		if random.random() < config.redoSectionDisturbance:
			config.shingleVariationAmount = round(random.uniform(0, config.shingleVariationRange))
			config.doSectionDisturbance == True 
			rebuildSections()


	config.fader.fadeIn(config)

	temp1 = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	temp1Draw = ImageDraw.Draw(temp1)
	temp1Draw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=config.colOverlay.bgColor)
	temp1.paste(config.image, (0, 0), config.image)
	config.render(temp1, 0, 0, config.canvasWidth, config.canvasHeight)



	# Done


def setUpDisturbanceConfigs(configSet) :
	config.baseSectionSpeed = float(workConfig.get(configSet, "baseSectionSpeed"))
	config.sectionRotationRange = float(workConfig.get(configSet, "sectionRotationRange"))

	sectionPlacementXRange = workConfig.get(configSet, "sectionPlacementXRange").split(",")
	config.sectionPlacementXRange = tuple(map(lambda x: int(int(x)), sectionPlacementXRange))

	sectionPlacementYRange = workConfig.get(configSet, "sectionPlacementYRange").split(",")
	config.sectionPlacementYRange = tuple(map(lambda x: int(int(x)), sectionPlacementYRange))

	sectionWidthRange = workConfig.get(configSet, "sectionWidthRange").split(",")
	config.sectionWidthRange = tuple(map(lambda x: int(int(x)), sectionWidthRange))

	sectionHeightRange = workConfig.get(configSet, "sectionHeightRange").split(",")
	config.sectionHeightRange = tuple(map(lambda x: int(int(x)), sectionHeightRange))

	config.numberOfSections = int(workConfig.get(configSet, "numberOfSections"))
	config.sectionMovementCountMax = int(workConfig.get(configSet, "sectionMovementCountMax"))

	config.stopProb = float(workConfig.get(configSet, "stopProbMax"))
	config.sectionSpeedFactorHorizontal = float(workConfig.get(configSet, "sectionSpeedFactorHorizontal"))
	config.sectionSpeedFactorVertical = float(workConfig.get(configSet, "sectionSpeedFactorVertical"))
	config.speedDeAcceleration = float(workConfig.get(configSet, "speedDeAcceleration"))
	config.speedDeAccelerationBase = float(workConfig.get(configSet, "speedDeAcceleration"))
	config.redoSectionDisturbance = float(workConfig.get(configSet, "redoSectionDisturbance"))
	config.speedDeAccelerationUpperLimit = float(workConfig.get(configSet, "speedDeAccelerationUpperLimit"))
	config.rebuildImmediatelyAfterDone = (workConfig.getboolean(configSet, "rebuildImmediatelyAfterDone"))


def main(run=True):
	global config
	config.redrawSpeed = float(workConfig.get("movingpattern", "redrawSpeed"))
	config.blockWidth = int(workConfig.get("movingpattern", "blockWidth"))
	config.blockHeight = int(workConfig.get("movingpattern", "blockHeight"))
	config.rows = int(workConfig.get("movingpattern", "rows"))
	config.cols = int(workConfig.get("movingpattern", "cols"))
	config.lineDiff = int(workConfig.get("movingpattern", "lineDiff"))

	config.useDoubleLine = (workConfig.getboolean("movingpattern", "useDoubleLine"))

	config.randomizeSpeed = (workConfig.getboolean("movingpattern", "randomizeSpeed"))

	config.patternModel = (workConfig.get("movingpattern", "patternModel"))
	config.steps = int(workConfig.get("movingpattern", "steps"))
	config.steps2 = int(workConfig.get("movingpattern", "steps2"))
	config.amplitude = int(workConfig.get("movingpattern", "amplitude"))
	config.amplitude2 = int(workConfig.get("movingpattern", "amplitude2"))
	config.yOffset = int(workConfig.get("movingpattern", "yOffset"))
	config.yOffset2 = int(workConfig.get("movingpattern", "yOffset2"))

	config.speedFactor = float(workConfig.get("movingpattern", "speedFactor"))
	config.phaseFactor = float(workConfig.get("movingpattern", "phaseFactor"))
	config.xSpeed = float(workConfig.get("movingpattern", "xSpeed"))
	config.ySpeed = float(workConfig.get("movingpattern", "ySpeed"))
	config.ySpeedInit = float(workConfig.get("movingpattern", "ySpeed"))

	skipBlocks = (workConfig.get("movingpattern", "skipBlocks")).split(",")
	config.skipBlocks = tuple(map(lambda x: int(int(x)), skipBlocks))

	config.diamondUseTriangles = False
	config.diamondStep = int(workConfig.get("movingpattern", "diamondStep"))

	config.numConcentricBoxes = int(workConfig.get("movingpattern", "numConcentricBoxes"))

	config.randomBlockProb = float(workConfig.get("movingpattern", "randomBlockProb"))
	config.randomBlockWidth = int(workConfig.get("movingpattern", "randomBlockWidth"))
	config.randomBlockHeight = int(workConfig.get("movingpattern", "randomBlockHeight"))

	config.repeatProb = .99

	config.xIncrementer = 0
	config.yIncrementer = 0

	config.altLineColoring = True

	config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.canvasDraw = ImageDraw.Draw(config.canvasImage)

	config.blockImage = Image.new("RGBA", (config.blockWidth, config.blockHeight))
	config.blockDraw = ImageDraw.Draw(config.blockImage)

	config.destinationImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.transitionImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))

	config.rotateAltBlock = 0

	try:
		config.numRows = int(workConfig.get("movingpattern", "numRows"))
		config.numRowsRandomize = (workConfig.getboolean("movingpattern", "numRowsRandomize"))
	except Exception as e:
		config.numRows = 1
		config.numRowsRandomize = False
		print(str(e))

	try:
		config.numDotRows = int(workConfig.get("movingpattern", "numDotRows"))
		config.numShingleRows = int(workConfig.get("movingpattern", "numShingleRows"))
	except Exception as e:
		config.numDotRows = config.numRows
		config.numShingleRows = config.numRows
		print(str(e))

	config.rebuildPatternProbability = float(workConfig.get("movingpattern", "rebuildPatternProbability"))
	config.patterns = workConfig.get("movingpattern", "patterns").split(",")

	try:
		config.patternModelVariations = workConfig.getboolean("movingpattern", "patternModelVariations")
		patternSequence = workConfig.get("movingpattern", "patternSequence").split(",")
		config.patternSequence = []
		for i in range(0, len(patternSequence), 3):
			config.patternSequence.append([patternSequence[i], int(patternSequence[i+1]), int(patternSequence[i+2])])
	except Exception as e:
		print(str(e))
		config.patternModelVariations = False
		config.patternSequence = []

	try:
		config.usePixelSortRandomize = (workConfig.getboolean("movingpattern", "usePixelSortRandomize"))
	except Exception as e:
		config.usePixelSortRandomize = False
		print(str(e))

	try:
		config.shingleVariation = (workConfig.getboolean("movingpattern", "shingleVariation"))
		config.shingleVariationRange = int(workConfig.get("movingpattern", "shingleVariationRange"))
		config.shingleVariationAmount = config.shingleVariationRange
	except Exception as e:
		config.shingleVariation = False
		config.shingleVariationRange = 0
		config.shingleVariationAmount = 0
		print(str(e))


	try:
		config.useBlurSection = (workConfig.getboolean("movingpattern", "useBlurSection"))
		config.blurSectionWidth = int(workConfig.get("movingpattern", "blurSectionWidth"))
		config.blurSectionHeight = int(workConfig.get("movingpattern", "blurSectionHeight"))
		config.blurSectionXPos = int(workConfig.get("movingpattern", "blurSectionXPos"))
		config.blurSectionYPos = int(workConfig.get("movingpattern", "blurSectionYPos"))
		config.mask_blur_amt = int(workConfig.get("movingpattern", "mask_blur_amt"))
		config.cp_blur_amt = int(workConfig.get("movingpattern", "cp_blur_amt"))

		config.mask = Image.new("L", config.canvasImage.size, 0)
		config.mask_draw = ImageDraw.Draw(config.mask)

		config.mask_draw.ellipse((config.blurSectionXPos, config.blurSectionYPos, config.blurSectionXPos +
								  config.blurSectionWidth, config.blurSectionYPos + config.blurSectionHeight), fill=255)
		config.mask_blur_amt = config.mask_blur_amt
		config.cp_blur_amt = config.cp_blur_amt
	except Exception as e:
		print(str(e))
		config.useBlurSection = False

	config.palettes = workConfig.get("movingpattern", "palettes").split(",")
	bgColorAlpha = (workConfig.get("movingpattern", "bgColorAlpha")).split(",")
	config.bgColorAlpha = list(map(lambda x: (int(x)), bgColorAlpha))
	buildPalette(config, 0)

	# THIS IS USED AS WAY TO MOCKUP A CONFIGURATION OF RECTANGULAR PANELS
	panelDrawing.mockupBlock(config, workConfig)


	config.sectionDisturbance = (workConfig.getboolean("movingpattern", "sectionDisturbance"))
	config.doSectionDisturbance = False 
	config.disturbanceConfigSets = (workConfig.get("movingpattern", "disturbanceConfigSets")).split(",")
	config.changeDisturbanceSetProb = float(workConfig.get("movingpattern", "changeDisturbanceSetProb"))

	workingDisturbanceSet = config.disturbanceConfigSets[0]

	setUpDisturbanceConfigs(workingDisturbanceSet)



		
	config.movingSections = []
	for i in range(0, config.numberOfSections):
		section = Holder()
		config.movingSections.append(section)
	rebuildSections()

	config.repeatDrawingMode = 1
	config.drawingPrinted = True
	config.saveImages = (workConfig.getboolean("movingpattern", "saveImages"))
	config.outPutPath = workConfig.get("movingpattern", "outPutPath")
	config.loadAnImageProb = float(workConfig.get("movingpattern", "loadAnImageProb"))
	config.imageSources = workConfig.get("movingpattern", "imageSources").split(',')

	config.doneCount = 0

	config.fader = Fader()
	config.fader.height = config.canvasHeight
	config.fader.width = config.canvasWidth
	config.fader.xPos = 0
	config.fader.yPos = 0
	config.fader.setUp()
	config.fader.image = config.canvasImage


	config.directorController = Director(config)
	config.directorController.slotRate = .03

	''' 
		########### Need to add something like this at final render call  as well
			
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


###############################################

