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
		self.triangles = [[[],coloroverlay.ColorOverlay(),[]] for i in range(0,8)]



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
			colOverlay.maxBrightness = self.fillColors[i][2][0]

			colOverlay.minHue = self.fillColors[i][0][0]
			colOverlay.maxHue = self.fillColors[i][0][1]
			colOverlay.minSaturation = self.fillColors[i][1][0]
			colOverlay.maxSaturation = self.fillColors[i][1][1]
			colOverlay.minValue = self.fillColors[i][2][0]
			colOverlay.maxValue = self.fillColors[i][2][1]


			### This is the speed range of transitions in color
			### Higher numbers means more possible steps so slower
			### transitions - 1,10 very blinky, 10,200 very slow
			colOverlay.randomRange = (self.config.transitionStepsMin,self.config.transitionStepsMax)

			colOverlay.colorA = colorutils.getRandomColorHSV(
				hMin = colOverlay.minHue, hMax  = colOverlay.maxHue, 
				sMin = colOverlay.minSaturation, sMax = colOverlay.maxSaturation,  
				vMin = colOverlay.minValue, vMax = colOverlay.maxValue
				)

			colOverlay.colorB = colorutils.getRandomColorHSV(
				hMin = colOverlay.minHue, hMax  = colOverlay.maxHue, 
				sMin = colOverlay.minSaturation, sMax = colOverlay.maxSaturation,  
				vMin = colOverlay.minValue, vMax = colOverlay.maxValue
				)
			colOverlay.colorA = (50,50,50)
			#self.colOverlay.colorB = (50,50,50)

		self.outlineColor = tuple(round(a*self.brightness) for a in (self.outlineColorObj.currentColor))

		self.setupSquares()


	def setupSquares(self):
		# Square's points made of corners and mid point
		# 	0	1	2
		#	3	4	5
		#	6	7	8

		## dividing into 8 smaller triangles
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


		# "TOP"
		self.triangles[0][0] = ((self.sqrPoints[0],self.sqrPoints[4],self.sqrPoints[3]))
		self.triangles[1][0] = ((self.sqrPoints[0],self.sqrPoints[4],self.sqrPoints[1]))
		self.triangles[2][0] = ((self.sqrPoints[1],self.sqrPoints[4],self.sqrPoints[2]))
		self.triangles[3][0] = ((self.sqrPoints[2],self.sqrPoints[4],self.sqrPoints[5]))

		self.triangles[4][0] = ((self.sqrPoints[3],self.sqrPoints[4],self.sqrPoints[6]))
		self.triangles[5][0] = ((self.sqrPoints[6],self.sqrPoints[4],self.sqrPoints[7]))
		self.triangles[6][0] = ((self.sqrPoints[7],self.sqrPoints[4],self.sqrPoints[8]))
		self.triangles[7][0] = ((self.sqrPoints[8],self.sqrPoints[4],self.sqrPoints[5]))


	def update(self):
		for i in range(0,8) :
			if(random.random() > config.colorPopProb) :
				self.triangles[i][1].stepTransition()
				self.triangles[i][2] = tuple(round (a * self.brightness ) for a in self.triangles[i][1].currentColor)
			else :
				self.changeColorFill(self.triangles[i])

	def drawUnitTriangles(self):
		if(self.lines == True) :
			outline = self.outlineColor
		else : outline = None
		
		for i in range (0,8) :
			coords = self.triangles[i][0]
			fillColor = self.triangles[i][2]
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

	config.c1HueRange = tuple([float(i) for i in workConfig.get(config.activeSet, 'c1HueRange').split(",")])
	config.c1SaturationRange = tuple([float(i) for i in workConfig.get(config.activeSet, 'c1SaturationRange').split(",")])
	config.c1ValueRange = tuple([float(i) for i in workConfig.get(config.activeSet, 'c1ValueRange').split(",")])
	
	config.c2HueRange = tuple([float(i) for i in workConfig.get(config.activeSet, 'c2HueRange').split(",")])
	config.c2SaturationRange = tuple([float(i) for i in workConfig.get(config.activeSet, 'c2SaturationRange').split(",")])
	config.c2ValueRange = tuple([float(i) for i in workConfig.get(config.activeSet, 'c2ValueRange').split(",")])
	
	config.c3HueRange = tuple([float(i) for i in workConfig.get(config.activeSet, 'c3HueRange').split(",")])
	config.c3SaturationRange = tuple([float(i) for i in workConfig.get(config.activeSet, 'c3SaturationRange').split(",")])
	config.c3ValueRange = tuple([float(i) for i in workConfig.get(config.activeSet, 'c3ValueRange').split(",")])
	
	config.c4HueRange = tuple([float(i) for i in workConfig.get(config.activeSet, 'c4HueRange').split(",")])
	config.c4SaturationRange = tuple([float(i) for i in workConfig.get(config.activeSet, 'c4SaturationRange').split(",")])
	config.c4ValueRange = tuple([float(i) for i in workConfig.get(config.activeSet, 'c4ValueRange').split(",")])
	
	config.c5HueRange = tuple([float(i) for i in workConfig.get(config.activeSet, 'c5HueRange').split(",")])
	config.c5SaturationRange = tuple([float(i) for i in workConfig.get(config.activeSet, 'c5SaturationRange').split(",")])
	config.c5ValueRange = tuple([float(i) for i in workConfig.get(config.activeSet, 'c5ValueRange').split(",")])

	# for now, all squares 
	config.blockLength = config.blockSize
	config.blockHeight = config.blockSize

	config.canvasImage = Image.new("RGBA", (config.canvasImageWidth  , config.canvasImageHeight))



	config.unitArrray = []
	config.fillColorSet = []
	config.fillColorSet.append ([config.c1HueRange, config.c1SaturationRange, config.c1ValueRange])
	config.fillColorSet.append ([config.c2HueRange, config.c2SaturationRange, config.c2ValueRange])
	config.fillColorSet.append ([config.c3HueRange, config.c3SaturationRange, config.c3ValueRange])
	config.fillColorSet.append ([config.c4HueRange, config.c4SaturationRange, config.c4ValueRange])
	config.fillColorSet.append ([config.c5HueRange, config.c5SaturationRange, config.c5ValueRange])
	
	createPieces()

	if(run) : runWork()


def createPieces() :
	global config
	cntrOffset = [config.cntrOffsetX,config.cntrOffsetY]

	config.unitArrray = []
	outlineColorObj = coloroverlay.ColorOverlay()
	outlineColorObj.randomRange = (5.0,30.0)

	## Jinky odds/evens alignment setup
	sizeAdjustor = 0
	## Alignment perfect setup
	if(config.patternPrecision == True): sizeAdjustor = 1

	
	cntr = [0,0]

	pattern = [
	[0,0,0,0,0,0,0,0],
	[1,0,0,0,1,1,1,0],
	[0,0,0,1,0,1,1,1],
	[0,0,0,0,0,0,0,0],
	[0,1,1,1,0,0,0,1],
	[1,1,1,1,1,1,1,1],
	[1,1,1,1,1,1,1,1],
	[1,1,1,0,1,0,0,0],
	[0,0,0,1,0,1,1,1],
	[1,1,1,1,1,1,1,1],
	[1,1,1,1,1,1,1,1],
	[1,0,0,0,1,1,1,0],
	[0,0,0,0,0,0,0,0],
	[1,1,1,0,1,0,0,0],
	[0,1,1,1,0,0,0,1],
	[0,0,0,0,0,0,0,0]
	]

	# Rows and columns of 9-squares
	for rows in range (0,config.blockRows) :

		rowStart = rows * config.blockHeight * 4 + config.gapSize

		for cols in range (0,config.blockCols) :

			columnStart = cols * config.blockLength * 4 + config.gapSize
			cntrOffset = [config.cntrOffsetX,config.cntrOffsetY]
			cntr = [columnStart, rowStart]

			## Jinky odds/evens alignment setup
			sizeAdjustor = 0
			## Alignment perfect setup
			if(config.patternPrecision == True): sizeAdjustor = 1

			n = 0
			for r in range(0,4):
				for c in range(0,4):
					obj = unit(config)
					obj.xPos = cntr[0] + c * config.blockLength 
					obj.yPos = cntr[1] + r * config.blockHeight
					obj.blockLength = config.blockLength - sizeAdjustor
					obj.blockHeight = config.blockHeight - sizeAdjustor
					obj.outlineColorObj	= outlineColorObj

					for i in pattern[n] :
						obj.fillColors.append(config.fillColorSet[i])

					obj.setUp()
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

		#if(random.random() > .98) : obj.outlineColorObj.stepTransition()

		## Approximating timing so that any one triange changes once every 2 minutes or so
		## e.g. .0005 prob checked every .01 seconds ~ .0005/ .01s = 5% chance per second ...
		
		#if(random.random() > config.resetTrianglesProd) : obj.setupTriangles()

		obj.update()
		obj.render()

	temp = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	temp.paste(config.canvasImage, (0,0), config.canvasImage)
	if(config.transformShape == True) :
		temp = transformImage(temp)
	config.render(temp, 0,0)
		

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
