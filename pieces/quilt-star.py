import time
import random
import textwrap
import math
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageEnhance, ImageChops
from modules import colorutils, badpixels, coloroverlay

class unit:

	timeTrigger = True
	tLimitBase = 30

	maxBrightness = 1

	minSaturation = 0.0
	maxSaturation = 0.0

	minValue = 0.0
	maxValue = 0.0

	minHue = 0.0
	maxHue = 0.0

	# Default is square made of 4 triangles
	compositionNumber = 0
	squareNumber = 0

	darkeningFactor = 1.4

	initialized = True

	fillColor = (0,0,0,255)
	
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
		self.colOverlay.tLimitBase = 2
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


		self.colOverlay.colorA = colorutils.getRandomColorHSV(
			sMin = self.minSaturation, sMax = self.maxSaturation,  
			hMin = self.minHue, hMax  = self.maxHue, 
			vMin = self.minValue, vMax = self.maxValue
			)

		self.colOverlay.colorB = colorutils.getRandomColorHSV(
			sMin = self.minSaturation, sMax = self.maxSaturation,  
			hMin = self.minHue, hMax  = self.maxHue, 
			vMin = self.minValue, vMax = self.maxValue
			)

		self.outlineColor = tuple(round(a*self.brightness) for a in (self.outlineColorObj.currentColor))

		self.setupSquares()
		self.setupTriangles()


	def setupSquares(self):
		# Square's points made of corners and mid point
		# 	0		1
		#		2	
		#	3		4

		## e.g. this triangle is 0,2,3

		#	*
		#	* *
		#	*	

		self.sqrPoints = []

		self.sqrPoints.append( 	(self.xPos, self.yPos))
		self.sqrPoints.append( 	(self.xPos + self.blockLength, self.yPos) )				
		self.sqrPoints.append( 	(self.xPos + self.blockLength/2, self.yPos + self.blockHeight/2) )
		self.sqrPoints.append( 	(self.xPos, self.yPos + self.blockHeight))
		self.sqrPoints.append( 	(self.xPos + self.blockLength, self.yPos + self.blockHeight) )

		self.sqrPointsSet = []
		# "TOP"
		self.sqrPointsSet.append((0,1,2))
		# "LEFT"
		self.sqrPointsSet.append((0,2,3))
		# "RIGHT"
		self.sqrPointsSet.append((1,2,4))
		# "BOTTOM"
		self.sqrPointsSet.append((3,2,4))


	def setupTriangles(self):
		# Square's points made of corners and mid points
		# 	0	1	2
		#	3		4
		#	5	6	7

		## e.g. this triangle is 0,1,5

		#	****
		#	* *
		#	*	

		self.starPoints = []

		# 	0	1	2
		self.starPoints.append( 	(self.xPos, self.yPos))
		self.starPoints.append( 	(self.xPos + random.uniform(self.blockLength/4,3 * self.blockLength/4), self.yPos))
		self.starPoints.append( 	(self.xPos + self.blockLength, self.yPos) )
								
		#	3		4
		self.starPoints.append( 	(self.xPos, self.yPos + random.uniform(self.blockLength/4,3 * self.blockLength/4)))
		self.starPoints.append( 	(self.xPos + self.blockLength, self.yPos + random.uniform(self.blockLength/4,3 * self.blockLength/4)) )						
		
		#	5	6	7
		self.starPoints.append( 	(self.xPos, self.yPos + self.blockHeight))
		self.starPoints.append( 	(self.xPos + random.uniform(self.blockLength/4,3 * self.blockLength/4), self.yPos + self.blockHeight)) 
		self.starPoints.append( 	(self.xPos + self.blockLength, self.yPos + self.blockHeight) )

		self.pointsSet = []
		# "TOP"
		self.pointsSet.append(((5,0,6),(6,2,7),(0,6,2)))
		# "LEFT"
		self.pointsSet.append(((0,2,4),(4,5,7),(0,4,5)))
		# "RIGHT"
		self.pointsSet.append(((0,2,3),(3,5,7),(2,3,7)))
		# "BOTTOM"
		self.pointsSet.append(((0,1,5),(1,2,7),(5,1,7)))


	def update(self):
		#self.fillColorMode == "random" or 
		if(random.random() > config.colorPopProb) :
			if self.initialized == True :
				self.initialized = False
			self.colOverlay.stepTransition()
			self.fillColor = tuple(round (a * self.brightness ) for a in self.colOverlay.currentColor)
		else :
			self.changeColorFill()

	
	def drawUnit(self) :
		if(self.lines == True) :
			self.draw.rectangle(((self.xPos, self.yPos), (self.xPos + self.blockLength, self.yPos + self.blockHeight))
			, fill=self.fillColor, outline=self.outlineColor)
		else:
			self.draw.rectangle(((self.xPos, self.yPos), (self.xPos + self.blockLength, self.yPos + self.blockHeight))
			, fill=self.fillColor, outline=None)

	
	def drawUnitTriangles(self, orientation = 0) :
		if(self.lines == True) :
			outline = self.outlineColor
		else : outline = None

		# Draw 4 triangles 
		c  = 0

		for side in range(0,4):
			square = self.sqrPointsSet[side]
			poly = []
			for triangle in square :
				poly.append(self.sqrPoints[triangle])

			fillColor = self.fillColor
			if self.squareNumber == 0 :
				if c == 0 or c == 1 :  
					fillColor = tuple([round(i/self.darkeningFactor) for i in fillColor])
			if self.squareNumber == 1 :
				if c == 0 or c == 2 :  
					fillColor = tuple([round(i/self.darkeningFactor) for i in fillColor])
			if self.squareNumber == 3 :
				if c == 1 or c == 3 :  
					fillColor = tuple([round(i/self.darkeningFactor) for i in fillColor])
			if self.squareNumber == 4 :
				if c == 3 or c == 2 :  
					fillColor = tuple([round(i/self.darkeningFactor) for i in fillColor])
			self.draw.polygon(poly, fill=fillColor, outline=outline)
			c+=1
	
	
	def drawUnitStar(self, starOrientation) :
		if(self.lines == True) :
			outline = self.outlineColor
		else : outline = None

		c  = 0
		for square in self.pointsSet[starOrientation]:
			poly = []
			for triangle in square :
				poly.append(self.starPoints[triangle])

			fillColor = self.fillColor
			if c == 2 :  
				fillColor = tuple([round(i/self.darkeningFactor) for i in fillColor])
			self.draw.polygon(poly, fill=fillColor, outline=outline)
			c+=1
				

	def render(self):

		if (self.fillColorMode == "red") : 
			brightnessFactor = self.config.brightnessFactorDark
		else:
			brightnessFactor = self.config.brightnessFactorLight

		self.outlineColor = tuple(int (a * self.brightness * brightnessFactor) for a in self.outlineColorObj.currentColor)

		
		if(self.compositionNumber == 0) :
			self.drawUnitTriangles(self.compositionNumber-1)
		else :
			self.drawUnitStar(self.compositionNumber-1)


	## Straight color change - deprecated - too blinky
	def changeColorFill(self):

		if(self.changeColor == True) :
			if(self.fillColorMode == "random") :
				self.fillColor = colorutils.randomColor(random.uniform(.01,self.brightness))
				self.outlineColor = colorutils.getRandomRGB(random.uniform(.01,self.brightness))
			else:
				newColor = colorutils.getRandomColorHSV(
					sMin = self.minSaturation, sMax = self.maxSaturation,  
					hMin = self.minHue, hMax  = self.maxHue, 
					vMin = self.minValue, vMax = self.maxValue
					)

				self.colOverlay.colorA = newColor


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
	config.resetTrianglesProd = float(workConfig.get("quilt", 'resetTrianglesProd'))

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

	config.activeSet = workConfig.get("quilt","activeSet")

	config.baseHueRange = tuple([float(i) for i in workConfig.get(config.activeSet, 'baseHueRange').split(",")])
	config.baseSaturationRange = tuple([float(i) for i in workConfig.get(config.activeSet, 'baseSaturationRange').split(",")])
	config.baseValueRange = tuple([float(i) for i in workConfig.get(config.activeSet, 'baseValueRange').split(",")])
	config.squareHueRange = tuple([float(i) for i in workConfig.get(config.activeSet, 'squareHueRange').split(",")])
	config.squareSaturationRange = tuple([float(i) for i in workConfig.get(config.activeSet, 'squareSaturationRange').split(",")])
	config.squareValueRange = tuple([float(i) for i in workConfig.get(config.activeSet, 'squareValueRange').split(",")])
	config.centerHueRange = tuple([float(i) for i in workConfig.get(config.activeSet, 'centerHueRange').split(",")])
	config.centerValueRange = tuple([float(i) for i in workConfig.get(config.activeSet, 'centerValueRange').split(",")])
	config.centerSaturationRange = tuple([float(i) for i in workConfig.get(config.activeSet, 'centerSaturationRange').split(",")])

	# for now, all squares 
	config.blockLength = config.blockSize
	config.blockHeight = config.blockSize

	config.canvasImage = Image.new("RGBA", (config.canvasImageWidth  , config.canvasImageHeight))

	createPieces()

	if(run) : runWork()


def createPieces() :
	global config
	cntrOffset = [config.cntrOffsetX,config.cntrOffsetY]

	config.unitArrray = []

	## Jinky odds/evens alignment setup
	sizeAdjustor = 0
	## Alignment perfect setup
	if(config.patternPrecision == True): sizeAdjustor = 1

	n = 0

	pattern = [(0,1,0),(2,0,3),(0,4,0)]

	# Rows and columns of 9-squares
	for rows in range (0,config.blockRows) :

		rowStart = rows * config.blockHeight * 3 + config.gapSize

		for cols in range (0,config.blockCols) :

			columnStart = cols * config.blockLength * 3 + config.gapSize

			# Three rows of three squares
			squareNumber = 0
			for unitRow in range (0,len(pattern)):
				rowDelta  =  unitRow * config.blockHeight

				# Each square is either divided in to 4 or 3 triangles
				for unitBlock in range(0, len(pattern[unitRow])):
					colDelta  =  unitBlock * config.blockHeight
					cntr = [columnStart + cntrOffset[0] + colDelta, rowStart  + cntrOffset[1] + rowDelta]	

					outlineColorObj = coloroverlay.ColorOverlay()
					outlineColorObj.randomRange = (5.0,30.0)

					obj = unit(config)
					obj.xPos = cntr[0]
					obj.yPos = cntr[1]
					obj.fillColorMode = "red"
					obj.blockLength = config.blockLength - sizeAdjustor
					obj.blockHeight = config.blockHeight - sizeAdjustor
					obj.outlineColorObj	= outlineColorObj

					obj.minHue = config.baseHueRange[0]
					obj.maxHue = config.baseHueRange[1]				
					obj.minSaturation = config.baseSaturationRange[0]
					obj.maxSaturation = config.baseSaturationRange[1]
					obj.minValue = config.baseValueRange[0]
					obj.maxValue = config.baseValueRange[1]

					obj.compositionNumber = pattern[unitRow][unitBlock]

					
					"The squares"
					if obj.compositionNumber == 0 :
						obj.minHue = config.squareHueRange[0]
						obj.maxHue = config.squareHueRange[1]				
						obj.minSaturation = config.squareSaturationRange[0]
						obj.maxSaturation = config.squareSaturationRange[1]
						obj.minValue = config.squareValueRange[0]
						obj.maxValue = config.squareValueRange[1]

						obj.squareNumber = squareNumber
						squareNumber += 1

					"The center block"
					if obj.compositionNumber == 0 and unitRow == 1 :
						obj.minHue = config.centerHueRange[0]
						obj.maxHue = config.centerHueRange[1]				
						obj.minSaturation = config.centerSaturationRange[0]
						obj.maxSaturation = config.centerSaturationRange[1]
						obj.minValue = config.centerValueRange[0]
						obj.maxValue = config.centerValueRange[1]
					

					obj.setUp(n)
					config.unitArrray.append(obj)

			n+=1


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

		## Approximating timing so that any one triange changes once every 2 minutes or so
		## e.g. .0005 prob checked every .01 seconds ~ .0005/ .01s = 5% chance per second ...
		
		if(random.random() > config.resetTrianglesProd) : obj.setupTriangles()

		obj.update()
		obj.render()

	temp = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	temp.paste(config.canvasImage, (0,0), config.canvasImage)
	if(config.transformShape == True) :
		temp = transformImage(temp)
	config.render(temp, 0,0)
		

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
