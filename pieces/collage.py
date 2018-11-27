# ################################################### #
import time
import random
import math
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageEnhance
from modules import colorutils, coloroverlay

lastRate  = 0 
colorutils.brightness =  1
shapes = []


# Really no need for a class here - it's always a singleton and besides
# with Python everthing is an object already .... some kind of OOP
# holdover anxiety I guess


class Shape :

	outlineColor = (1,1,1)
	barColor = (200,200,000)
	barColorStart = (0,200,200)
	holderColor = (0,0,0)
	messageClr = (200,0,0)
	shadowColor = (0,0,0)
	centerColor = (0,0,0)

	shapeXPosition  = 0
	shapeYPosition  = 0


	xPos = 1
	xPos1 = 1
	yPos = 1
	yPos1 = 1
	boxHeight = 100
	boxMax = 100
	status = 0
	rateMultiplier = .1
	rate = rateMultiplier * random.random()
	numRate = rate
	percentage = 0
	var = 10

	nothingLevel = 10
	nothingChangeProbability = .02

	usedFixedCenterColor = True

	borderModel = "prism"
	nothing = "void"
	varianceMode = "independent"
	prisimBrightness = .5

	steps = 20

	def __init__(self, config, i=0):
		#print ("init Fludd", i)
		
		#self.boxMax = config.screenWidth - 1
		#self.boxMaxAlt = self.boxMax + int(random.uniform(10,30) * config.screenWidth)
		#self.boxHeight = config.screenHeight - 2		#

		self.unitNumber  = i
		self.config = config


	def setUp(self):

		xCoords = []
		yCoords = []
		for i in self.coords:
			xCoords.append(i[0])
			yCoords.append(i[1])

		self.boxMax = round(max(xCoords) + 2 * self.varX)
		self.boxHeight = round(max(yCoords) + 2 * self.varY)

		self.tempImage = Image.new("RGBA", (self.boxMax, self.boxHeight))


		self.draw  = ImageDraw.Draw(self.tempImage)
		#### Sets up color transitions
		self.colOverlay = coloroverlay.ColorOverlay()
		self.colOverlay.randomSteps = True
		self.colOverlay.timeTrigger = True 
		self.colOverlay.tLimitBase = 10
		self.colOverlay.steps = 100
		
		self.colOverlay.maxBrightness = self.config.brightness
		self.colOverlay.maxBrightness = self.config.brightness

		self.colOverlay.minHue = 0
		self.colOverlay.maxHue = 360
		self.colOverlay.minSaturation = .1
		self.colOverlay.maxSaturation = 1
		self.colOverlay.minValue = .1
		self.colOverlay.maxValue = 1

		### This is the speed range of transitions in color
		### Higher numbers means more possible steps so slower
		### transitions - 1,10 very blinky, 10,200 very slow
		self.colOverlay.randomRange = (self.config.transitionStepsMin, self.config.transitionStepsMax)
		self.fillColor = tuple(int (a * self.config.brightness ) for a in self.colOverlay.currentColor)

		self.widthDelta = 0
		self.heightDelta = 0
		self.xDelta = 0
		self.yDelta = 0
		self.poly = []

		self.setNewBox()
		

	def changeAction(self):
		return False

	def setNewBox(self):
		self.draw.rectangle((0,0,self.boxMax, self.boxHeight), fill=(0,0,0,255), outline=None)
		self.poly  = []
		for p in self.coords:
			xPos = self.varX + round(p[0] + random.uniform(-self.varX, self.varX))
			yPos = self.varY + round(p[1] + random.uniform(-self.varY, self.varY))
			self.poly.append((xPos, yPos))


		
	def transition(self):
		if self.usedFixedCenterColor == True :
			self.fillColor = self.fixedCenterColor
		else :
			self.colOverlay.stepTransition()
			self.fillColor = []
			for i in range(0,3) :
				self.fillColor.append(round(self.colOverlay.currentColor[i] * self.config.brightness ))
			self.fillColor.append(255)
			self.fillColor = tuple(int(a) for a in self.fillColor)

		self.draw.rectangle((0,0,self.boxMax, self.boxHeight), fill=(0,0,0,10), outline=None)
		self.draw.polygon(self.poly, fill=self.fillColor , outline = None)


	def reDraw(self) :
		self.draw.polygon(self.poly, fill=self.fillColor , outline = None)


	def done(self): 
		return True



def redraw():
	global config, shapes 

	## Each Fludd-square is generated as an image and then pasted into its correct
	## place in the grid - or off-grid maybe sometime

	#config.draw.rectangle((0,0,config.canvasWidth, config.canvasHeight), fill=(0,0,0,10), outline=None)

	for shapeElement in shapes:
			shapeElement.transition()

	if config.shapeTweening == 1 :
		config.shapeTweening = 2

		## Generate state to transition to...
		for shapeElement in shapes:
			#shapeElement.transition()
			img = shapeElement.tempImage.convert("RGBA")
			config.destinationImage.paste(img, (shapeElement.shapeXPosition, shapeElement.shapeYPosition), img)

	if config.shapeTweening == 2:
			config.tweenCount += 1
			config.destinationImage
			composited = Image.blend(config.image, config.destinationImage, alpha = config.tweenCount/config.tweenCountMax)
			config.image.paste(composited, (0,0), composited)

			if config.tweenCount > config.tweenCountMax :
				config.tweenCount = 0
				config.shapeTweening = 0

	
	if config.shapeTweening == 0 :
		for shapeElement in shapes:
				#shapeElement.transition()
				img = shapeElement.tempImage.convert("RGBA")
				config.image.paste(img, (shapeElement.shapeXPosition, shapeElement.shapeYPosition), img)
				if random.random() < config.changeBoxProb:
					if shapeElement.varX == 0 and shapeElement.varY == 0 :
						pass
					else :
						shapeElement.setNewBox()
						print("new box: " + shapeElement.name)
						config.shapeTweening = 1


def runWork():
	global config
	while True:
		iterate()
		time.sleep(config.redrawSpeed)


def iterate() :
	global config
	redraw()



	## Paste an alpha of the next image, wait a few ms 
	## then past a more opaque one again
	## softens the transitions just enough

	config.pasteDelay = .02

	mask1 = config.image.point(lambda i: min(i * 1, 50))
	config.canvasImage.paste(config.image, (0,0), mask1)
	config.render(config.canvasImage, 0, 0, config.image)
	
	time.sleep(config.pasteDelay)
	mask2 = config.image.point(lambda i: min(i * 25, 100))
	config.canvasImage.paste(config.image, (0,0), mask2)
	config.render(config.canvasImage, 0, 0, config.image)
	
	time.sleep(config.pasteDelay)
	mask3 = config.image.point(lambda i: min(i * 25, 255))
	config.canvasImage.paste(config.image, (0,0), mask3)
	config.render(config.canvasImage, 0, 0, config.image)

	#config.render(config.image, 0, 0, config.screenWidth, config.screenHeight)

	# Done


def main(run = True) :
	global config
	global shapes
	shapes = []
	config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.draw  = ImageDraw.Draw(config.image)

	config.destinationImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))


	config.transitionStepsMin = int(workConfig.get("collageShapes", 'transitionStepsMin'))
	config.transitionStepsMax = int(workConfig.get("collageShapes", 'transitionStepsMax'))
	config.changeBoxProb = float(workConfig.get("collageShapes", 'changeBoxProb'))

	config.fixedCenterColorVals = ((workConfig.get("collageShapes", 'fixedCenterColor')).split(','))
	config.fixedCenterColor = tuple(map(lambda x: int(int(x) * config.brightness) , config.fixedCenterColorVals))
	config.usedFixedCenterColor = (workConfig.getboolean("collageShapes", 'usedFixedCenterColor'))

	config.redrawSpeed  = float(workConfig.get("collageShapes", 'redrawSpeed')) 
	config.shapeSets = list(map(lambda x: x, workConfig.get("collageShapes", 'sets').split(',')))

	config.shapeTweening = 0
	config.tweenCount = 0
	config.tweenCountMax = 100


	for i in  range(0, len(config.shapeSets)):

		shapeDetails = config.shapeSets[i]
		shape = Shape(config)
		# Prism is all colors, Plenum is white

		shape.varianceMode  = workConfig.get("collageShapes", 'varianceMode')
		shape.prisimBrightness  = float(workConfig.get("collageShapes", 'prisimBrightness')) 
		shape.usedFixedCenterColor = workConfig.getboolean(shapeDetails, 'usedFixedCenterColor')
		shape.fixedCenterColorVals = workConfig.get(shapeDetails, 'fixedCenterColor').split(',')
		shape.fixedCenterColor = tuple(map(lambda x: int(int(x) * config.brightness) , shape.fixedCenterColorVals))

		shape.varX  = float(workConfig.get(shapeDetails, 'varX'))
		shape.varY  = float(workConfig.get(shapeDetails, 'varY'))

		shapePosition = list(map(lambda x: int(x), workConfig.get(shapeDetails, 'postion').split(",")))
		shape.shapeXPosition = shapePosition[0]
		shape.shapeYPosition = shapePosition[1]
		shape.name = "S_"+str(i)

		shapeCoords = list(map(lambda x: int(x), workConfig.get(shapeDetails, 'coords').split(",")))
		shape.coords = []

		for c in range(0, len(shapeCoords), 2):
			shape.coords.append((shapeCoords[c], shapeCoords[c+1]))

		shape.setUp()
		shape.reDraw()
		shapes.append(shape)


	
	if(run) : runWork()
		

