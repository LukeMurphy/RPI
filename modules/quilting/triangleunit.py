import time
import random
import textwrap
import math
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageEnhance, ImageChops
from modules.quilting.colorset import ColorSet
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

	triangleUnits = 7


	
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
		self.fillColors = []

		## Each of the 8 triangles has a set of coordinates and a color]
		## Pre-fill the triangles list/array with ColorOverlay objects
		self.triangles = [[[],coloroverlay.ColorOverlay(False),[]] for i in range(0,8)]




	def setUp(self, n = 0) :

		self.outlineColor = tuple(int(a*self.brightness) for a in (self.outlineColorObj.currentColor))

		#### Sets up color transitions

		for i in range(0,8) :
			colOverlay = self.triangles[i][1]

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


		self.outlineColor = tuple(round(a*self.brightness) for a in (self.outlineColorObj.currentColor))
		self.outlineColor = (0,0,0,255)

		self.setupSquareWithTriangles()


	def setupSquareWithTriangles(self):
		# Square's points made of corners and mid point
		# 	0	1	2
		#	3	4	5
		#	6	7	8

		## dividing into 8 smaller triangles
		## p0,p1,p3

		#	*
		#	* *
		#	
		jumble = random.uniform(0,10)
		xRan = random.random() * jumble
		yRan = random.random() * jumble

		self.sqrPoints = []

		self.sqrPoints.append( 	(self.xPos + xRan, self.yPos + yRan))
		self.sqrPoints.append( 	(self.xPos + xRan + self.blockLength/2, self.yPos + yRan) )				
		self.sqrPoints.append( 	(self.xPos + xRan + self.blockLength, self.yPos + yRan) )	


		xRan = random.random() * jumble
		yRan = random.random() * jumble

		self.sqrPoints.append( 	(self.xPos + xRan, self.yPos + self.blockHeight/2 + yRan) )
		self.sqrPoints.append( 	(self.xPos + xRan + self.blockLength/2, self.yPos + self.blockHeight/2 + yRan))
		self.sqrPoints.append( 	(self.xPos + xRan + self.blockLength, self.yPos + self.blockHeight + yRan) )

		xRan = random.random() * jumble
		yRan = random.random() * jumble

		self.sqrPoints.append( 	(self.xPos + xRan, self.yPos + self.blockHeight + yRan) )
		self.sqrPoints.append( 	(self.xPos + xRan + self.blockLength/2, self.yPos + self.blockHeight + yRan))
		self.sqrPoints.append( 	(self.xPos + xRan + self.blockLength, self.yPos + self.blockHeight + yRan) )


		# "TOP"
		self.triangles[0][0] = ((self.sqrPoints[0],self.sqrPoints[4],self.sqrPoints[3]))
		self.triangles[1][0] = ((self.sqrPoints[0],self.sqrPoints[4],self.sqrPoints[1]))
		self.triangles[2][0] = ((self.sqrPoints[1],self.sqrPoints[4],self.sqrPoints[2]))
		self.triangles[3][0] = ((self.sqrPoints[2],self.sqrPoints[4],self.sqrPoints[5]))

		self.triangles[4][0] = ((self.sqrPoints[3],self.sqrPoints[4],self.sqrPoints[6]))
		self.triangles[5][0] = ((self.sqrPoints[6],self.sqrPoints[4],self.sqrPoints[7]))
		self.triangles[6][0] = ((self.sqrPoints[7],self.sqrPoints[4],self.sqrPoints[8]))
		# This last triange turns out to be a dup because the 4th triangle actually spans
		# two rows
		self.triangles[7][0] = ((self.sqrPoints[8],self.sqrPoints[4],self.sqrPoints[5]))


	def update(self):
		for i in range(0,self.triangleUnits) :
			if(random.random() > self.config.colorPopProb) :
				self.triangles[i][1].stepTransition()
				self.triangles[i][2] = tuple(round (a * self.brightness ) for a in self.triangles[i][1].currentColor)
			else :
				self.changeColorFill(self.triangles[i])

	
	def drawUnitTriangles(self):
		if(self.lines == True) :
			outline = self.outlineColor
		else : 
			outline = None

		#outline = (0,0,0,255)
		
		for i in range (0,self.triangleUnits) :
			coords = self.triangles[i][0]
			fillColor = self.triangles[i][2]
			fillColorList = (list(round (a * self.config.brightness ) for a in fillColor))
			fillColor = (fillColorList[0],fillColorList[1],fillColorList[2],255)
			self.draw.polygon(coords, fill=fillColor, outline=outline)


	def render(self):

		if (self.fillColorMode == "red") : 
			brightnessFactor = self.config.brightnessFactorDark
		else:
			brightnessFactor = self.config.brightnessFactorLight

		self.outlineColor = tuple(int (a * self.brightness * brightnessFactor) for a in self.outlineColorObj.currentColor)

		self.drawUnitTriangles()


	## Straight color change - deprecated - too blinky
	def changeColorFill(self, obj):

		# obj[0] are coordinates
		# obj[1] is the colorOverlay object
		# obj[2] is the fill color

		if(self.changeColor == True) :
			if(self.fillColorMode == "random") :
				obj[2] = colorutils.randomColor(random.uniform(.01,self.brightness))
				self.outlineColor = colorutils.getRandomRGB(random.uniform(.01,self.brightness))
			else:
				newColor = colorutils.getRandomColorHSV(
					hMin = obj[1].minHue, hMax  = obj[1].maxHue, 
					sMin = obj[1].minSaturation, sMax = obj[1].maxSaturation,  
					vMin = obj[1].minValue, vMax = obj[1].maxValue
					)

				obj[1].colorA = newColor

