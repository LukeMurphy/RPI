import time
import random
import textwrap
import math
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageEnhance, ImageChops
from pieces.workmodules.quilting.colorset import ColorSet
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
	polys = []
	pointRange = 20

	
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

		self.fillColors = []
		## Each of the 8 triangles has a set of coordinates and a color
		#self.triangles = [[[] for i in range(0,2)] for i in range(0,8)]
		self.fillColors = []


		## Pre-fill the triangles list/array with ColorOverlay objects
		self.polys = [[[],coloroverlay.ColorOverlay(False),[]] for i in range(0,self.pointRange)]
		#self.triangles = [[[],coloroverlay.ColorOverlay(),[]] for i in range(0,8)]


	def setUp(self, n = 0) :

		self.outlineColor = tuple(int(a*self.brightness) for a in (self.outlineColorObj.currentColor))

		#### Sets up color transitions

		#print ("Running setup: polys= {}".format(len(self.polys)))

		for i in range(0, len(self.polys)) :
			colOverlay = self.polys[i][1]

			colOverlay.randomSteps = True
			colOverlay.timeTrigger = True 
			colOverlay.tLimitBase = 2
			colOverlay.steps = 10

			#print(self.fillColors[i].valueRange)
					
			colOverlay.maxBrightness = self.config.brightness
			colOverlay.maxBrightness = self.fillColors[i].valueRange[1]

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
		#self.outlineColor = (0,0,0,255)
		self.setupSquareWithTriangles()


	def setupSquareWithTriangles(self):
		# Square's points made of corners and mid points
		'''
		 	a 	b 	c
		 	d 	e	f
		 	g	h	i
		 	j	j	l
		 	m	n	o
		 	p	q	r
		 	s	t	u
		 	v	w	x
		 	y	z	~

		## dividing into polygons
		## a b d

		#	*  *
		#	* 
		#		
		'''

		## This sets up the position of the active points in the grid
		self.sqrPoints = {}
		letters = "abcdefghimnopqrstuyz~"
		n = 0
		rowHeight = 0
		for row in range(0,7):
			if row == 3 or  row == 6 :
				rowHeight += self.blockHeight/self.config.elongation
			else :
				rowHeight += self.blockHeight
			for col in range(0,3):
				xRnd = round(random.uniform(-self.config.randomness,self.config.randomness))
				yRnd = round(random.uniform(-self.config.randomness,self.config.randomness))

				if abs(xRnd) < self.config.minRandomness :
					xRnd = self.config.minRandomness * -1 if xRnd < 0 else self.config.minRandomness
				if abs(xRnd) < self.config.minRandomness :
					yRnd = self.config.minRandomness * -1 if yRnd < 0  else self.config.minRandomness


				self.sqrPoints[letters[n]] = (self.xPos + col * self.blockLength + xRnd, self.yPos + rowHeight  + yRnd)
				n = n+1

		#print(self.xPos, self.blockLength)
		#print(self.sqrPoints)
		#print("")

		## All this just creates the sqaures and polygons
		## That make up a single square with an 8 point star
		## that also is divided bilaterally -- like a compass
		## star ... turned 2PI/16

		s = self.sqrPoints


		## "row" top triangles
		self.polys[0][0] = ( (s["a"], s["d"], s["e"] ) )
		self.polys[1][0] = ( (s["a"], s["b"], s["e"] ) )
		self.polys[2][0] = ( (s["b"], s["e"], s["c"] ) )
		self.polys[3][0] = ( (s["c"], s["f"], s["e"] ) )
		
		self.polys[4][0] = ( (s["g"], s["d"], s["e"] ) )
		self.polys[5][0] = ( (s["g"], s["h"], s["e"] ) )
		self.polys[6][0] = ( (s["h"], s["e"], s["i"] ) )
		self.polys[7][0] = ( (s["i"], s["f"], s["e"] ) )

		# two sides
		self.polys[8][0] = ( (s["g"], s["h"], s["n"], s["m"] ) )
		self.polys[9][0] = ( (s["n"], s["h"], s["i"], s["o"] ) )

		self.polys[10][0] = ( (s["p"], s["m"], s["n"] ) )
		self.polys[11][0] = ( (s["p"], s["q"], s["n"] ) )
		self.polys[12][0] = ( (s["q"], s["n"], s["r"] ) )
		self.polys[13][0] = ( (s["n"], s["o"], s["r"] ) )

		self.polys[14][0] = ( (s["s"], s["p"], s["t"] ) )
		self.polys[15][0] = ( (s["p"], s["q"], s["t"] ) )
		self.polys[16][0] = ( (s["t"], s["q"], s["r"] ) )
		self.polys[17][0] = ( (s["t"], s["r"], s["u"] ) )


		self.polys[18][0] = ( (s["s"], s["t"], s["z"], s["y"] ) )
		self.polys[19][0] = ( (s["z"], s["t"], s["u"], s["~"] ) )

		self.pointRange = len(self.polys)
	

		#print (self.polys)
		#import sys
		#sys.exit()


	def update(self):
		for i in range(0,self.pointRange) :
			if(random.random() > self.config.colorPopProb) :
				self.polys[i][1].stepTransition()
				self.polys[i][2] = tuple(round (a * self.config.brightness ) for a in self.polys[i][1].currentColor)
			else :
				self.changeColorFill(self.polys[i])

	
	def drawUnitTriangles(self):
		if(self.lines == True) :
			outline = self.outlineColor
		else : outline = None
		
		for i in range (0, self.pointRange) :
			coords = self.polys[i][0]
			fillColor = self.polys[i][2]
			fillColorList = (list(round (a * self.config.brightness ) for a in fillColor))
			fillColor = (fillColorList[0],fillColorList[1],fillColorList[2], 255)
			self.draw.polygon(coords, fill=fillColor, outline=outline)



	def render(self):

		if (self.fillColorMode == "red") : 
			brightnessFactor = self.config.brightnessFactorDark
		else:
			brightnessFactor = self.config.brightnessFactorLight

		self.outlineColor = tuple(int (a * self.config.brightness * brightnessFactor) for a in self.outlineColorObj.currentColor)

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

