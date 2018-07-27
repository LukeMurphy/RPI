import time
import random
import textwrap
import math
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageEnhance, ImageChops
from modules import colorutils, badpixels, coloroverlay

class Unit:

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
	fillColors = []
	triangles = []


	
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

		self.triangles = []
		self.fillColors = []
		## Each of the 8 triangles has a set of coordinates and a color
		#self.triangles = [[[] for i in range(0,2)] for i in range(0,8)]
		self.fillColors = []

		## Pre-fill the triangles list/array with ColorOverlay objects
		self.triangles = [[[],coloroverlay.ColorOverlay(),[]] for i in range(0,8)]



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
		self.colOverlay.colorA = (50,50,50)
		#self.colOverlay.colorB = (50,50,50)

		self.outlineColor = tuple(round(a*self.brightness) for a in (self.outlineColorObj.currentColor))

		self.setupSquares()
		self.setupTriangles()

	def setupFullSquares(self):
		# Square's points made of corners and mid point
		# 	0	1	2
		#	3	4	5
		#	6	7	8

		## e.g. this triangle is 0,4,6

		#	*
		#	* *
		#	*	

		## but dividing into smaller triangles
		## p0,p1,p3

		#	*
		#	* *
		#	

		self.sqrPoints = []

		self.sqrPoints.append( 	(self.xPos, self.yPos))
		self.sqrPoints.append( 	(self.xPos + self.blockLength/2, self.yPos) )				
		self.sqrPoints.append( 	(self.xPos + self.blockLength, self.yPos) )	

		self.sqrPoints.append( 	(self.xPos, self.yPos + self.blockHeight/2) )
		self.sqrPoints.append( 	(self.xPos + self.blockLength/2, self.yPos + self.blockHeight/2))
		self.sqrPoints.append( 	(self.xPos + self.blockLength, self.yPos + self.blockHeight) )

		self.sqrPoints.append( 	(self.xPos, self.yPos + self.blockHeight) )
		self.sqrPoints.append( 	(self.xPos + self.blockLength/2, self.yPos + self.blockHeight))
		self.sqrPoints.append( 	(self.xPos + self.blockLength, self.yPos + self.blockHeight) )

		self.sqrPointsSet = []
		# "TOP"
		self.sqrPointsSet.append((0,4,3))
		self.sqrPointsSet.append((0,1,4))
		self.sqrPointsSet.append((1,2,4))
		self.sqrPointsSet.append((2,4,5))

		self.sqrPointsSet.append((3,4,6))
		self.sqrPointsSet.append((6,4,7))
		self.sqrPointsSet.append((7,5,8))
		self.sqrPointsSet.append((4,5,8))


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
		if(random.random() > self.config.colorPopProb) :
			if self.initialized == True :
				self.initialized = False
			self.colOverlay.stepTransition()
			self.fillColor = tuple(round (a * self.brightness ) for a in self.colOverlay.currentColor)
		else :
			self.changeColorFill()

		if(random.random() > .98) : self.outlineColorObj.stepTransition()

		## Approximating timing so that any one triange changes once every 2 minutes or so
		## e.g. .0005 prob checked every .01 seconds ~ .0005/ .01s = 5% chance per second ...
		
		if(random.random() > self.config.resetTrianglesProd) : self.setupTriangles()

	
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
