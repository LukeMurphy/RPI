# ################################################### #
import math
import random
import time
from modules.configuration import bcolors
from modules import coloroverlay, colorutils
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps


class Director:
	"""docstring for Director"""

	targetSlotArray = []
	currentSlot = 0
	totalSlots = 0
	slotRate = .02
	advance = False
	color = [255,255,255]
	direction = 1

	def __init__(self, config):
		super(Director, self).__init__()
		self.config = config
		self.tT = time.time()


	def checkTime(self):
		if (time.time() - self.tT) >= self.slotRate :
			self.tT = time.time()
			self.advance = True
		else :
			self.advance = False


	def next(self):

		self.checkTime()
	

def newColor() :
	return colorutils.getRandomColorHSV(
				config.bg_minHue,
				config.bg_maxHue,
				config.bg_minSaturation,
				config.bg_maxSaturation,
				config.bg_minValue,
				config.bg_maxValue,
				config.bg_dropHueMinValue,
				config.bg_dropHueMaxValue,
				round(random.uniform(config.bg_minAlpha, config.bg_maxAlpha))
				)


def newColorAlt() :
	return colorutils.getRandomColorHSV(
				config.line1_minHue,
				config.line1_maxHue,
				config.line1_minSaturation,
				config.line1_maxSaturation,
				config.line1_minValue,
				config.line1_maxValue,
				config.line1_dropHueMinValue,
				config.line1_dropHueMaxValue,
				round(random.uniform(config.line1_minAlpha, config.line1_maxAlpha))
				)

def newColorAlt2() :
	return colorutils.getRandomColorHSV(
				config.line2_minHue,
				config.line2_maxHue,
				config.line2_minSaturation,
				config.line2_maxSaturation,
				config.line2_minValue,
				config.line2_maxValue,
				config.line2_dropHueMinValue,
				config.line2_dropHueMaxValue,
				round(random.uniform(config.line1_minAlpha, config.line1_maxAlpha))
				)

''' ----------------------------------------------------------------------------------- '''
def generateInitialImage():
	image = Image.new("RGBA", (config.blockWidth, config.blockHeight))
	draw = ImageDraw.Draw(image)
	#draw.rectangle((0,0,config.blockWidth/4,config.blockHeight/4), fill=(190,0,255,100))
	draw.line((config.blockWidth,0,0,config.blockHeight), fill=config.lineAColor)
	draw.line((0,0,config.blockWidth,config.blockHeight), fill=config.lineBColor)
	draw.line((0,config.blockHeight/2,config.blockWidth,config.blockHeight/2), fill=config.lineCColor)
	return image

''' ----------------------------------------------------------------------------------- '''


def drawGrid() :
	img  = generateInitialImage()

	i = 0 
	rad = round(360/config.gridRows/config.gridCols/config.repeatFactor)
	for row in range(0, config.gridRows) :
		for col in range(0, config.gridCols) :
			#rotAngle = -config.angle + 360/(config.gridCols * config.repeatFactor ) * i
			rotAngle = -config.angle + rad * i 
			imgTemp = img.rotate(rotAngle, expand=config.expandPaste)
			xPos = col * (config.blockWidth + config.colGap)
			yPos = row * (config.blockHeight + config.rowGap)
			config.image.paste(imgTemp, (xPos, yPos ), imgTemp)
			#config.angle += config.angleIncrement
			i += 1
	config.angle += config.angleIncrement


def drawSpiral() :
	img  = generateInitialImage()

	i = 0 
	rad = round(360/config.gridRows/config.gridCols/config.repeatFactor)
	sAngle = 0
	sAngleRate = config.sAngleRate #math.pi/20
	sRadius = config.initialRadius #5
	sRadiusRate = config.sRadiusRate#.49
	sRadiusRateChange = config.sRadiusRateChange #.998


	numberOfUnits = round(config.gridRows * config.gridCols * config.radiusMutiplier)
	for element in range(0, numberOfUnits) :
		rotAngle = -config.angle + rad * i 
		imgTemp = img.rotate(rotAngle, expand=config.expandPaste)
		xPos = round(config.xPosInit + math.cos(sAngle) * sRadius)
		yPos = round(config.yPosInit + math.sin(sAngle) * sRadius)
		config.image.paste(imgTemp, (xPos, yPos ), imgTemp)
		#config.angle += config.angleIncrement
		i += 1
		sAngle += sAngleRate
		sRadius += sRadiusRate
		sRadiusRate *= sRadiusRateChange
	config.angle += config.angleIncrement


def reDraw(config):
	if config.patternType == "spiral" :
		drawSpiral()
	else :
		drawGrid()

	if random.random() < config.bgFlashRate:
		config.draw.rectangle((0, 0, config.screenWidth, config.screenHeight), fill=config.backgroundFlashcolor)
		setUp()

	
def iterate():
	global config, expandingRingsRing, lastRate, calibrated, cycleCount
	#config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))

	config.director.checkTime()
	if config.director.advance == True :
		config.draw.rectangle((0, 0, config.screenWidth, config.screenHeight), fill=config.backgroundColor)
		reDraw(config)
		# Do the final rendering of the composited image
		config.render(config.image, 0, 0, config.screenWidth, config.screenHeight)

	if random.random() < config.filterPatchProb:
		#print("should be remapping")
		config.useFilters = True
		x1 = round(random.uniform(0,config.canvasWidth))
		x2 = round(random.uniform(x1,config.canvasWidth))
		y1 = round(random.uniform(0,config.canvasHeight))
		y2 = round(random.uniform(y1,config.canvasHeight))

		config.remapImageBlock = True
		config.remapImageBlockSection = (x1, y1, x2, y2)
		config.remapImageBlockDestination = (x1, y1)

	# Don't want the patch to always be there - just little interruptions
	if random.random() < config.filterPatchProbOff :
		#print("turning off remapping")
		config.useFilters = False
		x1 = 0
		x2 = 0
		y1 = 0
		y2 = 0

		config.remapImageBlock = True
		config.remapImageBlockSection = (x1, y1, x2, y2)
		config.remapImageBlockDestination = (x1, y1)


def setUp() :
	config.blockWidth = round(random.uniform(config.blockWidthMin,config.blockWidthMax))
	config.blockHeight = round(random.uniform(config.blockHeightMin,config.blockHeightMax))
	config.colGap = round(random.uniform(config.blockColSpacingMin, config.blockColSpacingMax))
	config.rowGap = round(random.uniform(config.blockRowSpacingMin, config.blockRowSpacingMax))
	config.angle = 0
	config.angleIncrement = random.uniform(config.angleIncrementMin, config.angleIncrementMax)
	config.repeatFactor = random.uniform(config.repeatFactorMin, config.repeatFactorMax)

	config.lineAColor = newColor()
	config.lineBColor = newColorAlt()
	config.lineCColor = newColorAlt2()
	config.patternType = workConfig.get("forms", "patternType")

	config.gridCols = round(config.canvasWidth / config.blockWidth)
	config.gridRows = round(config.canvasHeight / config.blockHeight)

	config.expandPaste = True if random.random() > .5 else False


def main(run=True):
	global config
	global expandingRingss

	expandingRingss = []
	config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.draw = ImageDraw.Draw(config.image)

	config.redrawSpeed = float(workConfig.get("forms", "redrawSpeed"))

	config.bg_minHue = float(workConfig.get("forms", "bg_minHue"))
	config.bg_maxHue = float(workConfig.get("forms", "bg_maxHue"))
	config.bg_minSaturation = float(workConfig.get("forms", "bg_minSaturation"))
	config.bg_maxSaturation = float(workConfig.get("forms", "bg_maxSaturation"))
	config.bg_minValue = float(workConfig.get("forms", "bg_minValue"))
	config.bg_maxValue = float(workConfig.get("forms", "bg_maxValue"))
	config.bg_dropHueMinValue = float(workConfig.get("forms", "bg_dropHueMinValue"))
	config.bg_dropHueMaxValue = float(workConfig.get("forms", "bg_dropHueMaxValue"))
	config.bg_minAlpha= float(workConfig.get("forms", "bg_minAlpha"))
	config.bg_maxAlpha = float(workConfig.get("forms", "bg_maxAlpha"))

	config.line1_minHue = float(workConfig.get("forms", "line1_minHue"))
	config.line1_maxHue = float(workConfig.get("forms", "line1_maxHue"))
	config.line1_minSaturation = float(workConfig.get("forms", "line1_minSaturation"))
	config.line1_maxSaturation = float(workConfig.get("forms", "line1_maxSaturation"))
	config.line1_minValue = float(workConfig.get("forms", "line1_minValue"))
	config.line1_maxValue = float(workConfig.get("forms", "line1_maxValue"))
	config.line1_dropHueMinValue = float(workConfig.get("forms", "line1_dropHueMinValue"))
	config.line1_dropHueMaxValue = float(workConfig.get("forms", "line1_dropHueMaxValue"))
	config.line1_minAlpha= float(workConfig.get("forms", "line1_minAlpha"))
	config.line1_maxAlpha = float(workConfig.get("forms", "line1_maxAlpha"))

	config.line2_minHue = float(workConfig.get("forms", "line2_minHue"))
	config.line2_maxHue = float(workConfig.get("forms", "line2_maxHue"))
	config.line2_minSaturation = float(workConfig.get("forms", "line2_minSaturation"))
	config.line2_maxSaturation = float(workConfig.get("forms", "line2_maxSaturation"))
	config.line2_minValue = float(workConfig.get("forms", "line2_minValue"))
	config.line2_maxValue = float(workConfig.get("forms", "line2_maxValue"))
	config.line2_dropHueMinValue = float(workConfig.get("forms", "line2_dropHueMinValue"))
	config.line2_dropHueMaxValue = float(workConfig.get("forms", "line2_dropHueMaxValue"))
	config.line2_minAlpha= float(workConfig.get("forms", "line2_minAlpha"))
	config.line2_maxAlpha = float(workConfig.get("forms", "line2_maxAlpha"))

	config.blockSpeedMultiplier = float(workConfig.get("forms", "blockSpeedMultiplier"))
	config.blockSpeedMin = float(workConfig.get("forms", "blockSpeedMin")) * config.blockSpeedMultiplier
	config.blockSpeedMax = float(workConfig.get("forms", "blockSpeedMax")) * config.blockSpeedMultiplier
	config.blockSpeed2Min = float(workConfig.get("forms", "blockSpeed2Min")) * config.blockSpeedMultiplier
	config.blockSpeed2Max = float(workConfig.get("forms", "blockSpeed2Max")) * config.blockSpeedMultiplier
	config.bgFlashRate = float(workConfig.get("forms", "bgFlashRate"))

	config.blockColSpacingMin = int(workConfig.get("forms", "blockColSpacingMin"))
	config.blockColSpacingMax = int(workConfig.get("forms", "blockColSpacingMax"))
	config.blockRowSpacingMin = int(workConfig.get("forms", "blockRowSpacingMin"))
	config.blockRowSpacingMax = int(workConfig.get("forms", "blockRowSpacingMax"))
	config.blockWidthMin = int(workConfig.get("forms", "blockWidthMin"))
	config.blockWidthMax = int(workConfig.get("forms", "blockWidthMax"))
	config.blockHeightMin = int(workConfig.get("forms", "blockHeightMin"))
	config.blockHeightMax = int(workConfig.get("forms", "blockHeightMax"))

	config.xPosInit = int(workConfig.get("forms", "xPosInit"))
	config.yPosInit = int(workConfig.get("forms", "yPosInit"))

	config.angleIncrementMin = float(workConfig.get("forms", "angleIncrementMin"))
	config.angleIncrementMax = float(workConfig.get("forms", "angleIncrementMax"))
	config.repeatFactorMin = float(workConfig.get("forms", "repeatFactorMin"))
	config.repeatFactorMax = float(workConfig.get("forms", "repeatFactorMax"))
	config.expandPaste = (workConfig.getboolean("forms", "expandPaste"))

	config.sAngleRate = math.pi / float(workConfig.get("forms", "sAngleRate"))
	config.initialRadius = int(workConfig.get("forms", "initialRadius"))
	config.sRadiusRate = float(workConfig.get("forms", "sRadiusRate"))
	config.sRadiusRateChange = float(workConfig.get("forms", "sRadiusRateChange"))
	config.radiusMutiplier = float(workConfig.get("forms", "radiusMutiplier"))


	# background color - higher the 
	# alpha = less persistent images
	backgroundColor = (workConfig.get("forms", "backgroundColor")).split(",")
	config.backgroundColor = tuple(int(x) for x in backgroundColor)	

	backgroundFlashcolor = (workConfig.get("forms", "backgroundFlashcolor")).split(",")
	config.backgroundFlashcolor = tuple(int(x) for x in backgroundFlashcolor)

	config.filterPatchProb = float(workConfig.get("forms", "filterPatchProb"))
	config.filterPatchProbOff = float(workConfig.get("forms", "filterPatchProbOff"))

	config.director = Director(config)
	config.director.slotRate = config.blockSpeedMin

	setUp()


def runWork():
	global config
	print(bcolors.OKGREEN + "** " + bcolors.BOLD)
	print("Running slots.py")
	print(bcolors.ENDC)
	while True:
		iterate()
		time.sleep(config.redrawSpeed)

