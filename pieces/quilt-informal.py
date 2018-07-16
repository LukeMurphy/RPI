import time
import random
import textwrap
import math
from functools import reduce
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageEnhance, ImageChops
from modules import colorutils, badpixels, coloroverlay

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

		self.draw  = ImageDraw.Draw(config.canvasImage)

		## Like the "stiching" color and affects the overall "tone" of the piece
		self.outlineColor = config.outlineColorObj.currentColor
		self.objWidth = 20
		self.outlineRange = [(20,20,250)]
		self.brightness = 1
		self.fillColorMode = "random"
		self.lineColorMode = "red"
		self.changeColor = True
		self.lines = config.lines

	def setUp(self, n = 0) :

		self.outlineColor = tuple(int(a*self.brightness) for a in (self.outlineColorObj.currentColor))

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
		self.colOverlay.randomRange = (self.config.transitionStepsMin,self.config.transitionStepsMax)


		self.fillColor = colorutils.getRandomColorHSV(
			sMin = self.minSaturation, sMax = self.maxSaturation,  
			hMin = self.minHue, hMax  = self.maxHue, 
			vMin = self.minValue, vMax = self.maxValue
			)

		self.colOverlay.colorA = self.fillColor

		self.colOverlay.colorB = colorutils.getRandomColorHSV(
			sMin = self.minSaturation, sMax = self.maxSaturation,  
			hMin = self.minHue, hMax  = self.maxHue, 
			vMin = self.minValue, vMax = self.maxValue
			)
		
		self.outlineColor = tuple(int(a*self.brightness) for a in (self.outlineColorObj.currentColor))


	def update(self):
		#self.fillColorMode == "random" or 
		if(random.random() > config.colorPopProb) :
			self.colOverlay.stepTransition()
			self.fillColor = tuple(int (a * self.brightness ) for a in self.colOverlay.currentColor)
		else :
			self.changeColorFill()

	
	def render(self):

		if (self.fillColorMode == "red") : 
			brightnessFactor = self.config.brightnessFactorDark
		else:
			brightnessFactor = self.config.brightnessFactorLight

		self.outlineColor = tuple(int (a * self.brightness * brightnessFactor) for a in self.outlineColorObj.currentColor)

		if(self.lines == True) :
			self.draw.rectangle(((self.xPos, self.yPos), (self.xPos + self.blockLength, self.yPos + self.blockHeight))
			, fill=self.fillColor, outline=self.outlineColor)
		else:
			self.draw.rectangle(((self.xPos, self.yPos), (self.xPos + self.blockLength, self.yPos + self.blockHeight))
			, fill=self.fillColor, outline=None)


	## Straight color change - deprecated - too blinky
	def changeColorFill(self):

		if(self.changeColor == True) :
			if(self.fillColorMode == "random") :
				self.fillColor = colorutils.randomColor(random.uniform(.01,self.brightness))
				self.outlineColor = colorutils.getRandomRGB(random.uniform(.01,self.brightness))
			else:
				self.fillColor = colorutils.getRandomColorHSV(
					sMin = self.minSaturation, sMax = self.maxSaturation,  
					hMin = self.minHue, hMax  = self.maxHue, 
					vMin = self.minValue, vMax = self.maxValue
					)

				self.colOverlay.colorA = self.fillColor


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def transformImage(img) :
	width, height = img.size
	m = -0.5
	xshift = abs(m) * 420
	new_width = width + int(round(xshift))

	img = img.transform((new_width, height), Image.AFFINE, (1, m, 0, 0, 1, 0), Image.BICUBIC)
	img = img.transform((new_width, height), Image.PERSPECTIVE, config.transformTuples, Image.BICUBIC)
	return img


def main(run = True) :
	global config, directionOrder,workConfig
	print("---------------------")
	print("QUILT Loaded")


	config.brightness = float(workConfig.get("displayconfig", 'brightness')) 
	colorutils.brightness = config.brightness
	config.canvasImageWidth = config.screenWidth
	config.canvasImageHeight = config.screenHeight
	config.canvasImageWidth -= 4
	config.canvasImageHeight -= 4

	config.outlineColorObj = coloroverlay.ColorOverlay()
	config.outlineColorObj.randomRange = (5.0,30.0)

	config.transitionStepsMin = float(workConfig.get("quilt", 'transitionStepsMin'))
	config.transitionStepsMax = float(workConfig.get("quilt", 'transitionStepsMax'))

	config.transformShape  = (workConfig.getboolean("quilt", 'transformShape'))
	transformTuples = workConfig.get("quilt", 'transformTuples').split(",")
	config.transformTuples = tuple([float(i) for i in transformTuples])

	redRange = workConfig.get("quilt", 'redRange').split(",")
	config.redRange = tuple([int(i) for i in redRange])

	config.numUnits = int(workConfig.get("quilt", 'numUnits')) 
	config.gapSize = int(workConfig.get("quilt", 'gapSize')) 
	config.blockSize = int(workConfig.get("quilt", 'blockSize')) 
	config.blockLength = int(workConfig.get("quilt", 'blockLength')) 
	config.blockHeight = int(workConfig.get("quilt", 'blockHeight')) 
	config.blockRows = int(workConfig.get("quilt", 'blockRows')) 
	config.blockCols = int(workConfig.get("quilt", 'blockCols')) 
	config.cntrOffsetX = int(workConfig.get("quilt", 'cntrOffsetX')) 
	config.cntrOffsetY = int(workConfig.get("quilt", 'cntrOffsetY')) 
	config.delay = float(workConfig.get("quilt", 'delay'))
	config.colorPopProb = float(workConfig.get("quilt", 'colorPopProb'))
	config.brightnessFactorDark = float(workConfig.get("quilt", 'brightnessFactorDark'))
	config.brightnessFactorLight = float(workConfig.get("quilt", 'brightnessFactorLight'))
	config.lines  = (workConfig.getboolean("quilt", 'lines'))
	config.patternPrecision  = (workConfig.getboolean("quilt", 'patternPrecision'))

	# for now, all squares 
	config.blockLength = config.blockSize
	config.blockHeight = config.blockSize



	config.canvasImage = Image.new("RGBA", (config.canvasImageWidth  , config.canvasImageHeight))

	#createPieces()

	drawSqareSpiral()

	if(run) : runWork()


def drawSqareSpiral():

	config.unitArrray = []

	draw  = ImageDraw.Draw(config.canvasImage)
	## Archimedes spiral is  r = a + b * theta
	turns = 8
	b = 16
	xOffset = 100
	yOffset = 130
	A = []
	rangeChange = (-10,10)

	for i in range(1,turns):
		x = i * b + xOffset + random.uniform(rangeChange[0],rangeChange[1])
		y = i * b + yOffset + random.uniform(rangeChange[0],rangeChange[1])
		A.append((x,y))

		x = -i * b + xOffset + random.uniform(rangeChange[0],rangeChange[1])
		y = i * b + yOffset + random.uniform(rangeChange[0],rangeChange[1])
		A.append((x,y))

		x = -i * b + xOffset + random.uniform(rangeChange[0],rangeChange[1])
		y = -i * b + yOffset + random.uniform(rangeChange[0],rangeChange[1])
		A.append((x,y))

		x = (i + 1) * b + xOffset + random.uniform(rangeChange[0],rangeChange[1])
		y = -i * b + yOffset + random.uniform(rangeChange[0],rangeChange[1])
		A.append((x,y))


	B = [(item[0] - b ,item[1] ) for item in A]

	n = 1
	for i in range(0, turns):
		try :

			#LEFT
			poly = (B[n+1], A[n+1], A[n+0], B[n+0])
			draw.polygon(poly, fill=colorutils.randomColor(config.brightness/4))

			#BOTTOM
			poly = (B[n+0], A[n-1], B[n+3], A[n+4])
			draw.polygon(poly, fill=colorutils.randomColor())

			#RIGHT
			poly = (B[n+2], A[n+2], A[n+3], B[n+3])
			draw.polygon(poly, fill=colorutils.randomColor(config.brightness * 1.2))

			#TOP
			poly = (B[n+1], A[n+5], B[n+6], A[n+2])
			draw.polygon(poly, fill=colorutils.randomColor(config.brightness/1.5))
			
			n += 4
		except Exception as e :
			print(e)


	
	for i in range(0, len(A) -1):
		draw.line((A[i],A[i+1]), fill=(230,10,0))

	#pointsArray2 = []

	for i in range(0, len(B) -1):
		draw.line((B[i],B[i+1]), fill=(0,0,230))
	


def createPieces() :
	global config
	cntrOffset = [config.cntrOffsetX,config.cntrOffsetY]

	config.unitArrray = []

	
	## Jinky odds/evens alignment setup
	sizeAdjustor = 0
	## Alignment perfect setup
	if(config.patternPrecision == True): sizeAdjustor = 1

	n = 0

	for rows in range (0,config.blockRows) :
		for cols in range (0,config.blockCols) :
			delta = config.numUnits * config.blockHeight * 2 +  config.blockLength + config.gapSize
			cntr = [rows * delta + cntrOffset[0], cols * delta + cntrOffset[1]]	

			outlineColorObj = coloroverlay.ColorOverlay()
			outlineColorObj.randomRange = (5.0,30.0)

			obj = unit(config)
			obj.xPos = cntr[0]
			obj.yPos = cntr[1]
			obj.blockLength = config.blockLength - sizeAdjustor
			obj.blockHeight = config.blockHeight - sizeAdjustor
			obj.fillColorMode = "red"
			obj.changeColor = False
			obj.outlineColorObj	= outlineColorObj

			obj.minSaturation = .8
			obj.maxSaturation = 1
			obj.minValue = .5
			obj.maxValue = .8
			obj.minHue = 350
			obj.maxHue = 10

			obj.setUp(n)
			config.unitArrray.append(obj)

			n+=1

			# RIGHT (or TOP when viewed horizontally -- light reds)
			for i in range(0,config.numUnits):
				obj = unit(config)
				obj.xPos = cntr[0] - (i) * config.blockLength
				obj.yPos = cntr[1] - (i + 1) * config.blockLength
				obj.blockLength = config.blockLength * (i + 1) * 2 - sizeAdjustor
				obj.blockHeight = config.blockHeight - 1
				obj.fillColorMode = "red"
				obj.changeColor = True
				obj.outlineColorObj	= outlineColorObj
				obj.brightness =  config.brightness

				obj.minSaturation = .7
				obj.maxSaturation = .9
				obj.minValue = .5
				obj.maxValue = .9
				obj.minHue = config.redRange[0]
				obj.maxHue = config.redRange[1]

				obj.setUp(n)
				config.unitArrray.append(obj)

			# BOTTOM (or RIGHT when viewed horizontally - bright colors)
			for i in range(0,config.numUnits):
				obj = unit(config)
				obj.xPos = cntr[0] + config.blockLength * (i + 1)
				obj.yPos = cntr[1] - (i ) * config.blockLength
				obj.blockLength = config.blockLength - sizeAdjustor
				obj.blockHeight = config.blockHeight * (i + 1) * 2 - sizeAdjustor
				obj.fillColorMode = "random"
				obj.changeColor = True
				obj.outlineColorObj	= outlineColorObj
				obj.timeTrigger = True
				obj.tLimitBase = 10
				obj.brightness =  config.brightness

				obj.minSaturation = .7
				obj.maxSaturation = .9
				obj.minValue = .5
				obj.maxValue = 1
				obj.minHue = 0
				obj.maxHue = 360

				obj.setUp(n)
				config.unitArrray.append(obj)

			# LEFT (or BOTTOM when viewed horizontally -- darker colors)
			for i in range(0,config.numUnits):
				obj = unit(config)
				obj.xPos = cntr[0] - config.blockLength * (i + 1 ) 
				obj.yPos = cntr[1] + (i + 1) * config.blockLength
				obj.blockLength = config.blockLength * (i + 1) * 2 - sizeAdjustor
				obj.blockHeight = config.blockHeight - sizeAdjustor
				obj.fillColorMode = "random"
				obj.changeColor = True
				obj.outlineColorObj	= outlineColorObj
				obj.timeTrigger = True
				obj.tLimitBase = 10
				obj.brightness =  config.brightness

				obj.minSaturation = .5
				obj.maxSaturation = 1
				obj.minValue = .1
				obj.maxValue = .5
				obj.minHue = 0
				obj.maxHue = 360

				obj.setUp(n)
				config.unitArrray.append(obj)

			# TOP (or LEFT when viewed horizontally -- darker reds)
			for i in range(0,config.numUnits):
				obj = unit(config)
				obj.xPos = cntr[0] - config.blockLength * (i + 1)
				obj.yPos = cntr[1] - (i + 1) * config.blockLength 
				obj.blockLength = config.blockLength - sizeAdjustor
				obj.blockHeight = config.blockHeight * (i + 1) * 2 - sizeAdjustor
				obj.fillColorMode = "red"
				obj.changeColor = True
				obj.outlineColorObj	= outlineColorObj
				obj.brightness =  config.brightness

				obj.minSaturation = .8
				obj.maxSaturation = 1
				obj.minValue = .05
				obj.maxValue = .4
				obj.minHue = config.redRange[0]
				obj.maxHue = config.redRange[1]

				obj.setUp(n)
				config.unitArrray.append(obj)


def runWork():
	global blocks, config, XOs
	#gc.enable()
	while True:
		iterate()
		time.sleep(config.delay)  


def iterate() :
	global config
	config.outlineColorObj.stepTransition()

	for i in range(0,len(config.unitArrray)):
		obj = config.unitArrray[i]
		if(random.random() > .98) : obj.outlineColorObj.stepTransition()
		obj.update()
		obj.render()

	temp = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	temp.paste(config.canvasImage, (0,0), config.canvasImage)
	if(config.transformShape == True) :
		temp = transformImage(temp)
	config.render(temp, 0,0)
		

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
