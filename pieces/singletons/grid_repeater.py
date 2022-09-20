# ################################################### #
import math
import random
import time
from modules.configuration import bcolors
from modules import coloroverlay, colorutils
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps


''' ----------------------------------------------------------------------------------- '''
def generateInitialImage():
	image = Image.new("RGBA", (config.blockWidth, config.blockHeight))
	draw = ImageDraw.Draw(image)
	#draw.rectangle((0,0,config.blockWidth/4,config.blockHeight/4), fill=(190,0,255,100))
	draw.line((config.blockWidth,0,0,config.blockHeight), fill=(0,180,0))
	draw.line((0,0,config.blockWidth,config.blockHeight), fill=(255,0,0,255))
	draw.line((0,config.blockHeight/2,config.blockWidth,config.blockHeight/2), fill=(0,0,255))
	return image

''' ----------------------------------------------------------------------------------- '''


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
				config.lines_minHue,
				config.lines_maxHue,
				config.lines_minSaturation,
				config.lines_maxSaturation,
				config.lines_minValue,
				config.lines_maxValue,
				config.lines_dropHueMinValue,
				config.lines_dropHueMaxValue,
				round(random.uniform(config.lines_minAlpha, config.lines_maxAlpha))
				)


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

	config.lines_minHue = float(workConfig.get("forms", "lines_minHue"))
	config.lines_maxHue = float(workConfig.get("forms", "lines_maxHue"))
	config.lines_minSaturation = float(workConfig.get("forms", "lines_minSaturation"))
	config.lines_maxSaturation = float(workConfig.get("forms", "lines_maxSaturation"))
	config.lines_minValue = float(workConfig.get("forms", "lines_minValue"))
	config.lines_maxValue = float(workConfig.get("forms", "lines_maxValue"))
	config.lines_dropHueMinValue = float(workConfig.get("forms", "lines_dropHueMinValue"))
	config.lines_dropHueMaxValue = float(workConfig.get("forms", "lines_dropHueMaxValue"))
	config.lines_minAlpha= float(workConfig.get("forms", "lines_minAlpha"))
	config.lines_maxAlpha = float(workConfig.get("forms", "lines_maxAlpha"))


	config.orientationProb = float(workConfig.get("forms", "orientationProb"))

	config.slotSpeedMultiplier = float(workConfig.get("forms", "slotSpeedMultiplier"))
	config.slotSpeedMin = float(workConfig.get("forms", "slotSpeedMin")) * config.slotSpeedMultiplier
	config.slotSpeedMax = float(workConfig.get("forms", "slotSpeedMax")) * config.slotSpeedMultiplier
	config.slotSpeed2Min = float(workConfig.get("forms", "slotSpeed2Min")) * config.slotSpeedMultiplier
	config.slotSpeed2Max = float(workConfig.get("forms", "slotSpeed2Max")) * config.slotSpeedMultiplier
	config.bgFlashRate = float(workConfig.get("forms", "bgFlashRate"))

	config.numerOfSlotsMax = int(workConfig.get("forms", "numerOfSlotsMax"))
	config.numerOfSlotsMin = int(workConfig.get("forms", "numerOfSlotsMin"))
	config.jitterAmount = int(workConfig.get("forms", "jitterAmount"))
	config.jitterAmountInit = int(workConfig.get("forms", "jitterAmount"))
	config.jitterFreq = int(workConfig.get("forms", "jitterFreq"))
	config.slotSpacingMin = int(workConfig.get("forms", "slotSpacingMin"))
	config.slotSpacingMax = int(workConfig.get("forms", "slotSpacingMax"))
	config.slotWidthMin = int(workConfig.get("forms", "slotWidthMin"))
	config.slotWidthMax = int(workConfig.get("forms", "slotWidthMax"))
	config.slotHeightMin = int(workConfig.get("forms", "slotHeightMin"))
	config.slotHeightMax = int(workConfig.get("forms", "slotHeightMax"))
	config.innerRadius = int(workConfig.get("forms", "innerRadius"))
	config.outerRadius = int(workConfig.get("forms", "outerRadius"))
	config.linesCreated = int(workConfig.get("forms", "linesCreated"))
	config.yRange = int(workConfig.get("forms", "yRange"))
	config.xRange = int(workConfig.get("forms", "xRange"))

		# background color - higher the 
	# alpha = less persistent images
	backgroundColor = (workConfig.get("forms", "backgroundColor")).split(",")
	config.backgroundColor = tuple(int(x) for x in backgroundColor)	

	backgroundFlashcolor = (workConfig.get("forms", "backgroundFlashcolor")).split(",")
	config.backgroundFlashcolor = tuple(int(x) for x in backgroundFlashcolor)

	config.filterPatchProb = float(workConfig.get("forms", "filterPatchProb"))
	config.filterPatchProbOff = float(workConfig.get("forms", "filterPatchProbOff"))


	config.blockWidth = 18
	config.blockHeight = 18
	config.colGap = 1
	config.rowGap = 1
	config.angle = 0
	config.angleIncrement = -5
	config.repeatFactor = .01
	config.expandPaste = False

	config.gridCols = round(config.canvasWidth / config.blockWidth)
	config.gridRows = round(config.canvasHeight / config.blockHeight)

	config.director = Director(config)
	config.director.slotRate = .03







	'''

	'''
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
	sAngleRate = math.pi/20
	sRadius = 5
	sRadiusRate = .49
	sRadiusRateChange = .998
	xPosInit = config.canvasWidth/2 - config.blockWidth/2
	yPosInit = config.canvasHeight/2 - config.blockHeight/2
	numberOfUnits = config.gridRows * config.gridCols * 2
	for element in range(0, numberOfUnits) :
		rotAngle = -config.angle + rad * i 
		imgTemp = img.rotate(rotAngle, expand=config.expandPaste)
		xPos = round(xPosInit + math.cos(sAngle) * sRadius)
		yPos = round(yPosInit + math.sin(sAngle) * sRadius)
		config.image.paste(imgTemp, (xPos, yPos ), imgTemp)
		#config.angle += config.angleIncrement
		i += 1
		sAngle += sAngleRate
		sRadius += sRadiusRate
		sRadiusRate *= sRadiusRateChange
	config.angle += config.angleIncrement


def reDraw(config):
	drawSpiral()
	
def iterate():
	global config, expandingRingsRing, lastRate, calibrated, cycleCount
	#config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))

	config.director.checkTime()
	if config.director.advance == True :
		config.draw.rectangle((0, 0, config.screenWidth, config.screenHeight), fill=config.backgroundColor)
		reDraw(config)
		# Do the final rendering of the composited image
		config.render(config.image, 0, 0, config.screenWidth, config.screenHeight)


def runWork():
	global config
	print(bcolors.OKGREEN + "** " + bcolors.BOLD)
	print("Running slots.py")
	print(bcolors.ENDC)
	while True:
		iterate()
		time.sleep(config.redrawSpeed)

