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
	yPos = 1
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
		self.tempImage = Image.new("RGBA", (self.boxMax, self.boxHeight))
		self.draw  = ImageDraw.Draw(self.tempImage)
		#### Sets up color transitions
		self.colOverlay = coloroverlay.ColorOverlay()
		self.colOverlay.randomSteps = True
		self.colOverlay.timeTrigger = True 
		self.colOverlay.tLimitBase = 25
		self.colOverlay.steps = 20
		
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
		self.colOverlay.randomRange = (self.config.transitionStepsMin,self.config.transitionStepsMax)
		self.fillColor = tuple(int (a * self.config.brightness ) for a in self.colOverlay.currentColor)



		## Used for the center if fixedColorCenter is not chosen ....

		self.colOverlay2 = coloroverlay.ColorOverlay()
		self.colOverlay2.randomSteps = True
		self.colOverlay2.timeTrigger = True 
		self.colOverlay2.tLimitBase = 25
		self.colOverlay2.steps = 20
		
		self.colOverlay2.maxBrightness = self.config.brightness
		self.colOverlay2.maxBrightness = self.config.brightness

		self.colOverlay2.minHue = 0
		self.colOverlay2.maxHue = 360
		self.colOverlay2.minSaturation = .1
		self.colOverlay2.maxSaturation = 1
		self.colOverlay2.minValue = .1
		self.colOverlay2.maxValue = 1

		### This is the speed range of transitions in color
		### Higher numbers means more possible steps so slower
		### transitions - 1,10 very blinky, 10,200 very slow
		self.colOverlay2.randomRange = (self.config.transitionStepsMin,self.config.transitionStepsMax)

		self.widthDelta = 0
		self.heightDelta = 0
		self.xDelta = 0
		self.yDelta = 0
		

		if self.usedFixedCenterColor == True:
			self.centerColor = self.fixedCenterColor
		else:
			self.centerColor = tuple(int (a * self.config.brightness ) for a in self.colOverlay2.currentColor)



	def changeAction(self):
		return False

	def setNewBox(self):
		svarwNew = random.uniform(0, self.varX)
		svarhNew = random.uniform(0, self.varY)
		
		self.symBoxWidthNew = self.boxMax - svarwNew
		self.symBoxHeightNew = self.boxHeight - svarhNew

		self.xPos1New = (self.boxMax - self.symBoxWidthNew)
		self.yPos1New = (self.boxHeight  - self.symBoxHeightNew)

		self.widthDelta = (self.symBoxWidthNew - self.symBoxWidth) / self.config.transitionStepsMax
		self.heightDelta = (self.symBoxHeightNew - self.symBoxHeight) / self.config.transitionStepsMax

		self.xDelta = (self.xPos1New - self.xPos1) / self.config.transitionStepsMax
		self.yDelta = (self.yPos1New - self.yPos1) / self.config.transitionStepsMax

		#print (self.symBoxWidth,self.symBoxWidthNew)
		#print (self.symBoxHeight,self.symBoxHeightNew)

		self.symBoxWidth = self.symBoxWidthNew
		self.xPos1 = self.xPos1New
		self.widthDelta = 0
		self.xDelta = 0

		self.symBoxHeight = self.symBoxHeightNew
		self.yPos1 = self.yPos1New
		self.heightDelta = 0
		self.yDelta = 0

		self.config.shapeTweening = 1


	def transitionBox(self):

		if abs(math.floor(self.symBoxWidth)) != math.floor(self.symBoxWidthNew) and abs(self.symBoxWidth) < self.boxMax and self.symBoxWidth > 0:
			self.symBoxWidth += self.widthDelta
			self.xPos1 += self.xDelta
		else :
			self.symBoxWidth = self.symBoxWidthNew
			self.xPos1 = self.xPos1New
			self.widthDelta = 0
			self.xDelta = 0

		if abs(math.floor(self.symBoxHeight)) != math.floor(self.symBoxHeightNew)  and abs(self.symBoxHeight) < self.boxHeight and self.symBoxHeight > 0 :
			self.symBoxHeight += self.heightDelta
			self.yPos1 += self.yDelta
		else :
			self.symBoxHeight = self.symBoxHeightNew
			self.yPos1 = self.yPos1New
			self.heightDelta = 0
			self.yDelta = 0

		if self.varianceMode == "symmetrical" :
			self.yPos1 = self.xPos1
			self.symBoxHeight = self.symBoxWidth



	def transition(self):

		## This was making the brightness affect transparency!!!!
		#self.fillColor = tuple(int (a * self.config.brightness ) for a in self.colOverlay.currentColor)
		
		fillColor = []
		for i in range(0,3) :
			fillColor.append(round(self.colOverlay.currentColor[i] * self.config.brightness ))
		fillColor.append(255)
		self.fillColor = tuple(int(a) for a in fillColor)
		self.draw.rectangle((0,0, self.boxMax, self.boxHeight), fill = self.fillColor, outline = None)
		self.draw.rectangle((round(self.xPos1), round(self.yPos1), round(self.symBoxWidth), round(self.symBoxHeight)), fill = self.centerColor , outline = None)
		self.colOverlay.stepTransition()

		if self.usedFixedCenterColor == False :
			#self.centerColor = tuple(int (a * self.config.brightness ) for a in self.colOverlay2.currentColor)
			centerColor = []
			for i in range(0,3) :
				centerColor.append(round(self.colOverlay2.currentColor[i] * self.config.brightness ))
			centerColor.append(255)
			self.centerColor = tuple(int(a) for a in centerColor)
			self.colOverlay2.stepTransition()

		#self.transitionBox()


	def reDraw(self) :
		varX = self.varX
		varY = self.varY

		gray = 126
		brightness = self.config.brightness * random.random()
		light = int(brightness*self.nothingLevel)

		if self.nothing == "void" :
			gray = 0
		else :
			gray = int(self.config.brightness * random.random()*self.nothingLevel/2)
			light = 0


		self.draw.rectangle((0,0,self.boxMax,self.boxHeight), fill = (0,0,0), outline = None)
		#config.draw.rectangle((0,0,self.boxMax,self.boxHeight), fill = (light,light,light))
		if(self.borderModel == "prism"):
			outerBorder = colorutils.randomColor(self.prisimBrightness)

		else :
			outerBorder = (light,light,light)

		self.draw.rectangle((0,0, self.boxMax, self.boxHeight), fill = outerBorder, outline = None)

		if(self.varianceMode == "independent") : 
			xPos1 = random.uniform(-varX/2,varX)
			yPos1 = random.uniform(-varY/2,varY)

			xPos2 = random.uniform(self.boxMax-varX,self.boxMax+varX)
			yPos2 = random.uniform(-varY/2,varY)	

			xPos3 = random.uniform(self.boxMax-varX,self.boxMax+varX)
			yPos3 = random.uniform(self.boxHeight-varY,self.boxHeight+varY)

			xPos4 = random.uniform(-varX/2,varX)
			yPos4 = random.uniform(self.boxHeight-varY,self.boxHeight+varY)

			self.draw.polygon((xPos1, yPos1, xPos2, yPos2, xPos3, yPos3, xPos4, yPos4), fill=(gray, gray, gray) , outline = None)

		elif(self.varianceMode == "symmetrical"):
			svar = random.uniform(0, varX)
			self.symBoxWidth = self.boxMax - svar
			self.symBoxHeight = self.boxHeight - svar
			xy0 = svar
			self.xPos1 = xy0
			self.yPos1 = xy0
			self.draw.rectangle((xy0,xy0,self.symBoxWidth,self.symBoxHeight), fill=(gray, gray, gray) , outline = None)
			self.setNewBox()
	
		elif(self.varianceMode == "asymmetrical"):
			self.svarw = random.uniform(0, varX)
			self.svarh = random.uniform(0, varY)
			self.symBoxWidth = self.boxMax - self.svarw
			self.symBoxHeight = self.boxHeight - self.svarh
			self.xPos1 = (self.boxMax - self.symBoxWidth)
			self.yPos1 = (self.boxHeight  - self.symBoxHeight)
			self.draw.rectangle((self.xPos1, self.yPos1, self.symBoxWidth, self.symBoxHeight), fill=self.config.fixedCenterColor , outline = None)
			self.setNewBox()
		

		if(random.random() < self.nothingChangeProbability) : self.nothingLevel = random.uniform(0,255)

		# Finally composite full image
		#config.image.paste(self.mainImage, (numXPos, numYPos), self.scrollImage)


	def change(self) :
		if (self.varianceMode == "independent") :
			self.varianceMode = "symmetrical"
		elif(self.varianceMode == "symmetrical") :
			self.varianceMode = "asymmetrical"		
		elif(self.varianceMode == "asymmetrical") :
			self.varianceMode = "independent"

		if (self.borderModel == "prism") :
			self.borderModel = "plenum"
		else : self.borderModel = "prism"

		print(self.varianceMode)
		#if(self.config.demoMode != 0) : print(self.varianceMode, self.borderModel)


	def done(self): 
		return True



def redraw():
	global config, shapes 

	## Each Fludd-square is generated as an image and then pasted into its correct
	## place in the grid - or off-grid maybe sometime


	if config.shapeTweening == 1 :
		config.shapeTweening = 2

		## Generate state to transition to...
		for shapeElement in shapes:
			shapeElement.transition()
			img = shapeElement.tempImage.convert("RGBA")
			config.destinationImage.paste(img, (shapeElement.shapeXPosition, shapeElement.shapeYPosition), img)

	if config.shapeTweening == 2:
			config.tweenCount += 1
			config.destinationImage

			composited = Image.blend(config.image, config.destinationImage, alpha = config.tweenCount/300)
			config.image.paste(composited, (0,0), composited)

			if config.tweenCount > 300 :
				config.tweenCount = 0
				config.shapeTweening = 0


	if config.shapeTweening == 0 :
		for shapeElement in shapes:
				shapeElement.transition()
				img = shapeElement.tempImage.convert("RGBA")
				config.image.paste(img, (shapeElement.shapeXPosition, shapeElement.shapeYPosition), img)
				if random.random() < config.changeBoxProb :
					shapeElement.setNewBox()


def runWork():
	global config
	while True:
		iterate()
		time.sleep(config.redrawSpeed)


def iterate() :
	global config
	redraw()
	config.render(config.image, 0, 0, config.screenWidth, config.screenHeight)

	# Done


def main(run = True) :
	global config
	global shapes
	shapes = []
	config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.destinationImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.draw  = ImageDraw.Draw(config.image)

	config.rowsOfSquares = int(workConfig.get("collageShapes", 'rowsOfSquares'))
	config.colsOfSquares = int(workConfig.get("collageShapes", 'colsOfSquares'))
	config.numberOfSquares = config.rowsOfSquares * config.colsOfSquares

	config.boxWidth = int(round(config.canvasWidth / config.colsOfSquares))
	config.boxHeight = int(round(config.canvasHeight / config.rowsOfSquares))
	config.transitionStepsMin = int(workConfig.get("collageShapes", 'transitionStepsMin'))
	config.transitionStepsMax = int(workConfig.get("collageShapes", 'transitionStepsMax'))
	config.changeBoxProb = float(workConfig.get("collageShapes", 'changeBoxProb'))

	config.fixedCenterColorVals = ((workConfig.get("collageShapes", 'fixedCenterColor')).split(','))
	config.fixedCenterColor = tuple(map(lambda x: int(int(x) * config.brightness) , config.fixedCenterColorVals))
	config.usedFixedCenterColor = (workConfig.getboolean("collageShapes", 'usedFixedCenterColor'))

	config.shapeSets = list(map(lambda x: x, workConfig.get("collageShapes", 'sets').split(',')))
	config.shapeVariants = list(map(lambda x: x, workConfig.get("collageShapes", 'setsVariants').split(',')))





	# print(config.boxWidth, config.boxHeight)

	squareCount  = 0

	for i in  range(0, len(config.shapeSets)):

		shape = Shape(config)
		# Prism is all colors, Plenum is white


		shapeVariants = list(map(lambda x: int(x), workConfig.get("collageShapes", config.shapeVariants[i]).split(',')))
		shape.varX  = shapeVariants[0]
		shape.varY  = shapeVariants[1]
		shape.varianceMode  = workConfig.get("collageShapes", 'varianceMode')
		shape.prisimBrightness  = float(workConfig.get("collageShapes", 'prisimBrightness')) 
		shape.usedFixedCenterColor = config.usedFixedCenterColor
		shape.fixedCenterColor = config.fixedCenterColor

		shapeCoords = list(map(lambda x: int(x), workConfig.get("collageShapes", config.shapeSets[i]).split(",")))
		shape.shapeXPosition = shapeCoords[0]
		shape.shapeYPosition = shapeCoords[1]
		shape.boxMax = shapeCoords[2]
		shape.boxHeight = shapeCoords[3]

		shape.setUp()
		shape.reDraw()
		config.redrawSpeed  = float(workConfig.get("collageShapes", 'redrawSpeed')) 
		shapes.append(shape)
		squareCount+=1
	
	config.cycleTiming = 1
	config.t1  = time.time()
	config.t2  = time.time()

	config.cycleCount = 0
	config.calibrationCount = 500

	config.shapeTweening = 0
	config.tweenCount = 0



	config.count =  0
	

	# var sets the points offset from the corners - i.e. the larger var is, the wider the borders
	'''
	************
	*           *
	 *           *
	  *          * 
	   ***********
        
	'''
	
	if(run) : runWork()
		

