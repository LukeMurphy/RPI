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
	minSaturation = .25
	maxSaturation = 1
	minValue = .1
	maxValue = 1

	def __init__(self, config):
		self.config = config
		self.xPos = 0
		self.yPos = 0
		self.redraw = False

		self.draw  = ImageDraw.Draw(config.canvasImage)

		#self.fillColor = colorutils.getRandomRGB()
		#self.outlineColor = colorutils.getRandomRGB()

		#### Sets up color transitions
		self.colOverlay = coloroverlay.ColorOverlay()
		self.colOverlay.randomSteps = True
		self.colOverlay.timeTrigger = True 
		self.colOverlay.tLimitBase = 20
		self.colOverlay.maxBrightness = .5
		self.colOverlay.steps = 30


		### This is the speed range of transitions in color
		### Higher numbers means more possible steps so slower
		### transitions - 1,10 very blinky, 10,200 very slow
		self.colOverlay.randomRange = (5.0,30.0)

		### This changes each cycle - incrementing towards next target color
		self.fillColor = self.colOverlay.currentColor

		self.colOverlay.maxBrightness = self.maxBrightness
		self.colOverlay.minSaturation = self.minSaturation
		self.colOverlay.maxSaturation = self.maxSaturation
		self.colOverlay.minValue = self.minValue
		self.colOverlay.maxValue = self.maxValue

		
		## Like the "stiching" color and affects the overall "tone" of the piece
		self.outlineColor = config.outlineColorObj.currentColor
		self.objWidth = 20

		blueFactor  =  config.blueFactor
		greenFactor  =  config.greenFactor
		self.redRange = [(250,greenFactor,blueFactor),
						(200,greenFactor,blueFactor),
						(150,greenFactor,blueFactor),
						(100,greenFactor,blueFactor),
						(50,greenFactor,blueFactor),
						(20,greenFactor,blueFactor)]
		self.outlineRange = [(20,20,250)]
		self.brightness = 1
		self.fillColorMode = "random"
		self.lineColorMode = "red"
		self.changeColor = True
		self.lines = config.lines

	def setUp(self, n = 0) :

		self.brightness *= self.config.brightness
		if(n!=0):
			n = int(math.floor(random.uniform(0,len(self.redRange))))
		self.fillColor = tuple(int(a*self.brightness) for a in (self.redRange[n]))

		self.colOverlay.colorA = tuple(int(a*self.brightness) for a in (self.redRange[n]))
		self.colOverlay.colorB = tuple(int(a*self.brightness) for a in (self.redRange[n]))

		#n = int(math.floor(random.uniform(0,len(self.outlineRange))))
		#self.outlineColor = tuple(int(a*self.brightness) for a in (self.outlineRange[n]))
		self.outlineColor = tuple(int(a*self.brightness) for a in (self.outlineColorObj.currentColor))

		if (self.fillColorMode == "red") :
			self.colOverlay.getNewColor = self.getNewColor

	def getNewColor(self):
		n = int(math.floor(random.uniform(0,len(self.redRange))))
		self.colOverlay.colorB = tuple(int(a*self.brightness) for a in (self.redRange[n]))

		
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
				if(self.lineColorMode == "red") :
					n = int(math.floor(random.uniform(0,len(self.redRange))))
					self.outlineColor = tuple(int(a*self.brightness) for a in (self.redRange[n]))
				else :	
					self.outlineColor = colorutils.getRandomRGB(random.uniform(.01,self.brightness))
			else:
				n = int(math.floor(random.uniform(0,len(self.redRange))))
				self.fillColor = tuple(int(a*self.brightness) for a in (self.redRange[n]))
				#n = int(math.floor(random.uniform(0,len(self.outlineRange))))
				#self.outlineColor = tuple(int(a*self.brightness) for a in (self.outlineRange[n]))


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def transformImage(img) :
	width, height = img.size
	m = -0.5
	xshift = abs(m) * 420
	new_width = width + int(round(xshift))

	img = img.transform((new_width, height), Image.AFFINE, (1, m, 0, 0, 1, 0), Image.BICUBIC)
	img = img.transform((new_width, height), Image.PERSPECTIVE, config.transformTuples, Image.BICUBIC)
	return img


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

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

	config.transformShape  = (workConfig.getboolean("quilt", 'transformShape'))
	transformTuples = workConfig.get("quilt", 'transformTuples').split(",")
	config.transformTuples = tuple([float(i) for i in transformTuples])

	try :
		config.numUnits = int(workConfig.get("quilt", 'numUnits')) 
		config.gapSize = int(workConfig.get("quilt", 'gapSize')) 
		config.blockSize = int(workConfig.get("quilt", 'blockSize')) 
		config.blockLength = int(workConfig.get("quilt", 'blockLength')) 
		config.blockHeight = int(workConfig.get("quilt", 'blockHeight')) 
		config.blockRows = int(workConfig.get("quilt", 'blockRows')) 
		config.blockCols = int(workConfig.get("quilt", 'blockCols')) 
		config.cntrOffsetX = int(workConfig.get("quilt", 'cntrOffsetX')) 
		config.cntrOffsetY = int(workConfig.get("quilt", 'cntrOffsetY')) 
		config.blueFactor = int(workConfig.get("quilt", 'blueFactor')) 
		config.greenFactor = int(workConfig.get("quilt", 'greenFactor')) 
		config.delay = float(workConfig.get("quilt", 'delay'))
		config.colorPopProb = float(workConfig.get("quilt", 'colorPopProb'))
		config.brightnessFactorDark = float(workConfig.get("quilt", 'brightnessFactorDark'))
		config.brightnessFactorLight = float(workConfig.get("quilt", 'brightnessFactorLight'))
		config.lines  = (workConfig.getboolean("quilt", 'lines'))
		config.patternPrecision  = (workConfig.getboolean("quilt", 'patternPrecision'))

		# for now, all squares 
		config.blockLength = config.blockSize
		config.blockHeight = config.blockSize
	except Exception as e: 
		print (str(e))


	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

	config.canvasImage = Image.new("RGBA", (config.canvasImageWidth  , config.canvasImageHeight))

	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

	cntrOffset = [config.cntrOffsetX,config.cntrOffsetY]

	config.unitArrray = []

	
	## Jinky odds/evens alignment setup
	sizeAdjustor = 0
	## Alignment perfect setup
	if(config.patternPrecision == True): sizeAdjustor = 1


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
			obj.brightness = 1.0
			obj.changeColor = False
			obj.outlineColorObj	= outlineColorObj
			obj.setUp()
			config.unitArrray.append(obj)

			# RIGHT
			for i in range(0,config.numUnits):
				obj = unit(config)
				obj.xPos = cntr[0] - (i) * config.blockLength
				obj.yPos = cntr[1] - (i + 1) * config.blockLength
				obj.blockLength = config.blockLength * (i + 1) * 2 - sizeAdjustor
				obj.blockHeight = config.blockHeight - 1
				obj.fillColorMode = "red"
				obj.brightness = .8
				obj.changeColor = True
				obj.outlineColorObj	= outlineColorObj
				obj.setUp(-1)
				config.unitArrray.append(obj)

			# BOTTOM
			for i in range(0,config.numUnits):
				obj = unit(config)
				obj.xPos = cntr[0] + config.blockLength * (i + 1)
				obj.yPos = cntr[1] - (i ) * config.blockLength
				obj.blockLength = config.blockLength - sizeAdjustor
				obj.blockHeight = config.blockHeight * (i + 1) * 2 - sizeAdjustor
				obj.fillColorMode = "random"
				obj.brightness = .99
				obj.changeColor = True
				obj.outlineColorObj	= outlineColorObj

				obj.timeTrigger = True
				obj.tLimitBase = 30
				obj.minSaturation = .25
				obj.maxSaturation = 1
				obj.minValue = .9
				obj.maxBrightness = 1
				obj.setUp(-1)
				config.unitArrray.append(obj)

			# LEFT
			for i in range(0,config.numUnits):
				obj = unit(config)
				obj.xPos = cntr[0] - config.blockLength * (i + 1 ) 
				obj.yPos = cntr[1] + (i + 1) * config.blockLength
				obj.blockLength = config.blockLength * (i + 1) * 2 - sizeAdjustor
				obj.blockHeight = config.blockHeight - sizeAdjustor
				obj.fillColorMode = "random"
				obj.brightness = .4
				obj.changeColor = True
				obj.outlineColorObj	= outlineColorObj

				obj.timeTrigger = True
				obj.tLimitBase = 30
				obj.minValue = .3
				obj.maxBrightness = .4
				obj.minSaturation = .25
				obj.maxSaturation = 1
				obj.setUp(-1)
				config.unitArrray.append(obj)

			# TOP
			for i in range(0,config.numUnits):
				obj = unit(config)
				obj.xPos = cntr[0] - config.blockLength * (i + 1)
				obj.yPos = cntr[1] - (i + 1) * config.blockLength 
				obj.blockLength = config.blockLength - sizeAdjustor
				obj.blockHeight = config.blockHeight * (i + 1) * 2 - sizeAdjustor
				obj.fillColorMode = "red"
				obj.brightness = .4
				obj.changeColor = True
				obj.outlineColorObj	= outlineColorObj
				obj.setUp(-1)
				config.unitArrray.append(obj)


	setUp()

	if(run) : runWork()

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def setUp():
	global config

	pass


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def runWork():
	global blocks, config, XOs
	#gc.enable()
	while True:
		iterate()
		time.sleep(config.delay)  

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def iterate() :
	global config
	config.outlineColorObj.stepTransition()

	for i in range(0,len(config.unitArrray)):
		obj = config.unitArrray[i]
		if(random.random() > .98) :obj.outlineColorObj.stepTransition()
		obj.update()
		obj.render()

	temp = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	temp.paste(config.canvasImage, (0,0), config.canvasImage)
	if(config.transformShape == True) :
		temp = transformImage(temp)
	config.render(temp, 0,0)
		

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def callBack() :
	global config, XOs
	return True

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
