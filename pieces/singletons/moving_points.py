import math
import random
import threading
import time
from modules.configuration import bcolors
from modules import colorutils, coloroverlay
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps, ImageFilter


'''
				fadeIn = Fader()
				# fadeIn.blankImage = Image.new("RGBA", (height, width))
				fadeIn.crossFade = Image.new("RGBA", (height, width))
				fadeIn.image = gradientImage
				fadeIn.xPos = xPos
				fadeIn.yPos = yPos
				fadeIn.height = gradientImage.height
				fadeIn.width = gradientImage.width

				config.fadeArray.append(fadeIn)

'''


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


class Fader:
	def __init__(self):
		self.doingRefresh = 0
		self.doingRefreshCount = 10
		self.fadingDone = False
		print("Fader")

	def fadeIn(self, config):
		if self.fadingDone == False:
			if self.doingRefresh < self.doingRefreshCount:
				self.blankImage = Image.new("RGBA", (self.width, self.height))
				self.crossFade = Image.blend(
					self.blankImage,
					self.image,
					self.doingRefresh / self.doingRefreshCount,
				)
				config.image.paste(
					self.crossFade, (self.xPos, self.yPos), self.crossFade
				)
				self.doingRefresh += 1
			else:
				config.image.paste(
					self.image, (self.xPos, self.yPos), self.image)
				self.fadingDone = True


class Point:

	remakeOnExit = True

	def __init__(self, config):
		self.config = config
		self.colOverlay = coloroverlay.ColorOverlay()
		self.remake()

	def remake(self):

		self.direction = 1
		if random.random() < .5:
			self.direction = -1
		self.xSpeed = random.uniform(config.xSpeedRangeMin, config.xSpeedRangeMax) * self.direction
		self.ySpeed = random.uniform(config.ySpeedRangeMin, config.ySpeedRangeMax) 

		self.speed = random.uniform(1, config.speedRange) * self.direction

		#self.speed = 3 * self.direction

		self.xSpeedInit = self.xSpeed
		self.ySpeedInit = self.ySpeed

		self.xPos = round(random.uniform(config.xRangeMin, config.xRangeMax))
		self.yPos = round(random.uniform(config.yRangeMin, config.yRangeMax))

		dx = self.xPos - config.locus[0]
		dy = self.yPos - config.locus[1]
		self.angle = math.atan2(dy, dx)


		self.xSpeed = math.cos(self.angle) * self.speed
		self.ySpeed = math.sin(self.angle) * self.speed

		self.growthCount = 0

		#print(self.angle)


		#if self.direction == -1:
		#	self.xPos = config.canvasWidth  # + config.barThicknessMax * 2

		self.finalBarThickness = round(random.uniform(
			config.barThicknessMin, config.barThicknessMax))

		self.finalBarLength = round(random.uniform(
			config.barLengthMin, config.barLengthMax))

		self.barLength = 0
		self.barThickness = 0


		#self.colorVal = colorutils.randomColorAlpha()

		config.usingColorSet = math.floor(random.uniform(0, config.numberOfColorSets))
		cset = config.colorSets[config.usingColorSet]

		self.colorVal = colorutils.getRandomColorHSV(
			cset[0], cset[1], cset[2], cset[3], cset[4], cset[5], config.dropHueMax, 0, config.colorAlpha, config.brightness)

		self.outlineColorVal = colorutils.getRandomColorHSV(
			cset[0], cset[1], cset[2], cset[3], cset[4], cset[5], config.dropHueMax, 0, config.outlineColorAlpha, config.brightness)

		#self.outlineColorVal = self.colorVal

		self.setColors()
		self.colOverlay.colorTransitionSetup()

	def setColors(self):
		# Sets up color transitions
		cset = config.colorSets[config.usingColorSet]

		self.colOverlay.randomSteps = True
		self.colOverlay.timeTrigger = True
		self.colOverlay.tLimitBase = 12
		self.colOverlay.steps = 10

		self.colOverlay.minHue = cset[0]
		self.colOverlay.maxHue = cset[1]
		self.colOverlay.minSaturation = cset[2]
		self.colOverlay.maxSaturation = cset[3]
		self.colOverlay.minValue = cset[4]
		self.colOverlay.maxValue = cset[5]

		self.colOverlay.colorA = self.colorVal

	def update(self):
		self.colOverlay.stepTransition()
		self.colorVal = (
			int(self.colOverlay.currentColor[0]*self.config.brightness),
			int(self.colOverlay.currentColor[1]*self.config.brightness),
			int(self.colOverlay.currentColor[2]*self.config.brightness),
			self.config.colorAlpha
		)

		if self.colOverlay.complete == True:
			self.setColors()

	def render(self, angle=0):
		temp = Image.new("RGBA", ((self.finalBarLength)+1, (self.finalBarLength)+1))
		drw = ImageDraw.Draw(temp)
		xPos = round(self.finalBarLength/2 - self.barLength/2)
		xPos2 = round(self.finalBarLength/2 + self.barLength/2)
		yPos = round(self.finalBarLength/2 - self.barThickness/2)
		yPos2 = round(self.finalBarLength/2 + self.barThickness/2)

		if config.tipType == 1:
			#drw.rectangle((xPos, yPos-1, xPos2, yPos2+1), fill=self.colorVal, outline=self.outlineColorVal)
			#drw.rectangle((0, 0, self.finalBarLength-2, self.finalBarLength-2), outline=(255,0,0), fill=None)
			drw.rectangle((xPos, yPos, xPos2, yPos2), fill=self.colorVal, outline=None)

		elif config.tipType == 2:
			drw.ellipse((xPos, yPos, xPos2, yPos2), fill=self.colorVal, outline=self.outlineColorVal)

		temp = temp.rotate(180 - math.degrees(angle))

		config.image.paste(temp, (round(self.xPos), round(self.yPos)), temp)

		del temp

		if self.growthCount < 10 :
			self.growthCount +=1
			self.barLength += self.finalBarLength / 10
			self.barThickness += self.finalBarThickness / 10


def transformImage(img):
	width, height = img.size
	new_width = 50
	m = 0.0
	img = img.transform(
		(new_width, height), Image.AFFINE, (1, m, 0, 0, 1, 0), Image.BICUBIC
	)
	return img


def runWork():
	global config
	print(bcolors.OKGREEN + "** " + bcolors.BOLD)
	print("Running moving_points.py")
	print(bcolors.ENDC)
	while config.isRunning == True:
		config.directorController.checkTime()
		if config.directorController.advance == True:
			iterate()
		time.sleep(config.redrawRate)
		if config.standAlone == False:
			config.callBack()


def iterate():
	global config

	config.draw.rectangle((0, 0, 400, 400), fill=(
		config.fillColor[0], config.fillColor[1], config.fillColor[2], config.fillColorAlpha))


	## Change the center locus

	config.locus[0] += config.locus[2]
	config.locus[1] += config.locus[3]

	if config.locus[0] > config.canvasWidth:
		#config.locus[0] = 0
		config.locus[0] = config.canvasWidth
		config.locus[2] = config.locus[4] - 2 * random.random() * config.locus[4] *-1
	if config.locus[0] < 0:
		config.locus[0] = 0
		#config.locus[0] = config.canvasWidth
		config.locus[2] = config.locus[4] - 2 * random.random() * config.locus[4]
	if config.locus[1] > config.canvasHeight:
		#config.locus[1] = 0
		config.locus[3] = config.locus[5] - 2 * random.random() * config.locus[5]*-1
	if config.locus[1] < 0:
		config.locus[1] = 0
		config.locus[3] = config.locus[5] - 2 * random.random() * config.locus[5]


	## Run through the elements to update

	for i in range(0, config.numberOfPoints):
		bar = config.barArray[i]

		#w = round(math.sqrt(2) * config.barThicknessMax * 1.5)
		#angle = math.atan2(bar.ySpeed, bar.xSpeed)

		dx = bar.xPos - config.locus[0]
		dy = bar.yPos - config.locus[1]
		d = math.sqrt(dx*dx+dy*dy)
		angle = math.atan2(bar.ySpeed, bar.xSpeed)

		if config.useLocus :
			angle = math.atan2(dy, dx)
			#print(d, angle)


		
		if config.movementModel == "concentric":
			d = 1.5
			if (abs(dx) > bar.barLength*d) and (abs(dy) > bar.barLength*d):
				bar.angle = math.atan2(dy, dx)

			bar.xPos += bar.xSpeedInit * math.cos(bar.angle) * 5
			bar.yPos += bar.xSpeedInit * math.sin(bar.angle) * 5

		if config.movementModel == "linear":
			if config.noXMovement == False:
				bar.xPos += bar.xSpeed
			if config.noYMovement == False:
				bar.yPos += bar.ySpeed


		if config.movementModel == "radiating":
				bar.xPos += bar.xSpeed
				bar.yPos += bar.ySpeed


		bar.update()

		bar.render(angle)

		if bar.xPos > config.canvasWidth + bar.barLength:
			bar.xPos = -bar.barLength
			if bar.remakeOnExit == True:
				bar.remake()

		if bar.xPos < - bar.barLength:
			bar.xPos = config.canvasWidth + bar.barLength
			if bar.remakeOnExit == True:
				bar.remake()

		if bar.yPos < -bar.barLength:
			bar.yPos = config.canvasHeight + bar.barLength
			if bar.remakeOnExit == True:
				bar.remake()

		if bar.yPos > config.canvasHeight + bar.barLength:
			bar.yPos = -bar.barLength
			if bar.remakeOnExit == True:
				bar.remake()
	'''
	if random.random() < .002:
		print("drophue")
		if config.dropHueMax == 0:
			config.dropHueMax = 255
		else:
			config.dropHueMax = 0
		#print("Winter... " + str(config.dropHueMax ))
	'''

	if random.random() < config.colorChangeProb:

		config.usingColorSet = math.floor(random.uniform(0, config.numberOfColorSets))
		# just in case ....
		if config.usingColorSet == config.numberOfColorSets:
			config.usingColorSet = config.numberOfColorSets-1

		config.colorAlpha = round(random.uniform(config.fillAlphaMin, config.fillAlphaMax))
		#config.dropHueMax = 0

		print("change colors " + str(config.usingColorSet) + " " + str(config.numberOfColorSets))


		if random.random() < config.changeShapeProb:
			config.tipType = config.tipTypeAlt
		else:
			config.tipType = config.tipTypeOrig

	if random.random() < config.changeMovementProb:
		print("remaking bars")
		for i in range(0, config.numberOfPoints):
			bar = config.barArray[i]
			bar.remake()


	if random.random() < config.changeMovementProb:
		choice = round(random.uniform(0, 8))
		if choice == 0:
			config.noXMovement = True
			config.noYMovement = False
			config.movementModel = "linear"
		if choice >= 1:
			config.noXMovement = False
			config.noYMovement = True
			config.movementModel = "linear"
		if choice >= 3:
			config.noXMovement = False
			config.noYMovement = False
			config.movementModel = "linear"
		if choice >=4 :
			config.movementModel = "concentric"
			config.useLocus = True
		if choice >=5 :
			config.movementModel = "radiating"
			config.useLocus = True
		print("new Movement: " +  config.movementModel)

	if random.random() < config.filterRemappingProb:

		config.useFilters = True
		config.remapImageBlock = True

		startX = round(random.uniform(0, config.filterRemapRangeX))
		startY = round(random.uniform(0, config.filterRemapRangeY))
		endX = round(random.uniform(128, config.filterRemapminHoriSize))
		endY = round(random.uniform(64, config.filterRemapminVertSize))
		config.remapImageBlockSection = [startX, startY, startX + endX, startY + endY]
		config.remapImageBlockDestination = [startX, startY]

	temp1 = config.image.copy()
	if config.blurRadius != 0 : temp1 = temp1.filter(ImageFilter.GaussianBlur(radius=config.blurRadius))
	config.render(temp1, 0, 0)


def main(run=True):
	global config


	config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	config.draw = ImageDraw.Draw(config.image)
	config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.canvasDraw = ImageDraw.Draw(config.canvasImage)

	config.xPos = 0
	config.dropHueMax = 0

	config.numberOfPoints = int(workConfig.get("Points", "numberOfPoints"))
	config.barThicknessMin = int(workConfig.get("Points", "barThicknessMin"))
	config.barThicknessMax = int(workConfig.get("Points", "barThicknessMax"))

	config.barLengthMin = int(workConfig.get("Points", "barLengthMin"))
	config.barLengthMax = int(workConfig.get("Points", "barLengthMax"))


	yRange = (workConfig.get("Points", "yRange")).split(",")
	config.yRangeMin = int(yRange[0])
	config.yRangeMax = int(yRange[1])
	xRange = (workConfig.get("Points", "xRange")).split(",")
	config.xRangeMin = int(yRange[0])
	config.xRangeMax = int(yRange[1])

	config.locus = list(int(i) for i in (workConfig.get("Points", "locus").split(",")))
	config.useLocus = (workConfig.getboolean("Points", "useLocus"))
	# storing initial values of locus drift
	config.locus.append(config.locus[2])
	config.locus.append(config.locus[3])


	config.edgeAlphaMin = int(workConfig.get("Points", "edgeAlphaMin"))
	config.edgeAlphaMax = int(workConfig.get("Points", "edgeAlphaMax"))
	config.fillAlphaMin = int(workConfig.get("Points", "fillAlphaMin"))
	config.fillAlphaMax = int(workConfig.get("Points", "fillAlphaMax"))

	config.tipAngle = float(workConfig.get("Points", "tipAngle"))

	config.xSpeedRangeMin = float(workConfig.get("Points", "xSpeedRangeMin"))
	config.xSpeedRangeMax = float(workConfig.get("Points", "xSpeedRangeMax"))
	config.ySpeedRangeMin = float(workConfig.get("Points", "ySpeedRangeMin"))
	config.ySpeedRangeMax = float(workConfig.get("Points", "ySpeedRangeMax"))
	config.speedRange = float(workConfig.get("Points", "speedRange"))

	try:
		config.colorChangeProb = float(workConfig.get("Points", "colorChangeProb"))
	except Exception as e:
		print(str(e))
		config.colorChangeProb = .003

	try:
		config.changeShapeProb = float(workConfig.get("Points", "changeShapeProb"))
	except Exception as e:
		print(str(e))
		config.changeShapeProb = .001

	config.movementModel = (workConfig.get("Points", "movementModel"))

	try:
		config.changeMovementProb = float(workConfig.get("Points", "changeMovementProb"))
	except Exception as e:
		print(str(e))
		config.changeMovementProb = .001

	config.noXMovement = False
	config.noYMovement = False

	try:
		config.tipType = int(workConfig.get("Points", "tipType"))
		config.tipTypeOrig = int(workConfig.get("Points", "tipType"))
		config.tipTypeAlt = int(workConfig.get("Points", "tipTypeAlt"))
	except Exception as e:
		print(str(e))
		config.tipType = 1
		config.tipTypeAlt = 1
		config.tipTypeOrig = 1

	config.colorAlpha = round(random.uniform(config.fillAlphaMin, config.fillAlphaMax))
	config.outlineColorAlpha = round(random.uniform(config.edgeAlphaMin, config.edgeAlphaMax))

	config.filterRemappingProb = float(workConfig.get("Points", "filterRemappingProb"))
	config.filterRemapRangeX = int(workConfig.get("Points", "filterRemapRangeX"))
	config.filterRemapRangeY = int(workConfig.get("Points", "filterRemapRangeY"))
	config.filterRemapminHoriSize = int(workConfig.get("Points", "filterRemapminHoriSize"))
	config.filterRemapminVertSize = int(workConfig.get("Points", "filterRemapminVertSize"))
	config.blurRadius = int(workConfig.get("Points", "blurRadius"))

	config.barArray = []
	config.colorSets = []

	config.colorSetList = list(
		i for i in (workConfig.get("Points", "colorSets").split(","))
	)

	config.numberOfColorSets = len(config.colorSetList)
	for setName in config.colorSetList:
		cset = list(
			float(i) for i in (workConfig.get("Points", setName).split(","))
		)
		config.colorSets.append(cset)

	config.usingColorSet = math.floor(
		random.uniform(0, config.numberOfColorSets))
	if config.usingColorSet == config.numberOfColorSets:
		config.usingColorSet = config.numberOfColorSets - 1

	config.fillColorList = list(
		float(i) for i in (workConfig.get("Points", 'fillColor').split(","))
	)

	config.fillColorAlpha = int(workConfig.get("Points", "fillColorAlpha"))
	config.fillColor = colorutils.getRandomColorHSV(
		config.fillColorList[0], config.fillColorList[1], config.fillColorList[2], config.fillColorList[3], config.fillColorList[4], config.fillColorList[5], config.dropHueMax, 0, config.fillColorAlpha, config.brightness)

	# initialize and place the first set
	for i in range(0, config.numberOfPoints):
		bar = Point(config)
		bar.yPos = round(random.uniform(config.yRangeMin, config.yRangeMax))
		bar.xPos = round(random.uniform(
			0, config.canvasWidth - 2))
		config.barArray.append(bar)
		#yPos += bar.barThickness


	config.redrawRate = .03
	config.directorController = Director(config)
	config.directorController.slotRate = .05

	if run:
		runWork()



