import time
import random
import textwrap
import math
import datetime
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageEnhance, ImageChops
from modules import colorutils, badpixels, coloroverlay
import argparse
from threading import Timer

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
## Image layers 

class unit :

	xPos = 0
	yPos = 0
	bgColor = (0,0,0)
	outlineColor = (0,0,0)
	tileSizeWidth = 64
	tileSizeHeight = 32
	percentDone = 100.0
	resistance = 50.0


	score = 1


	def __init__(self) :

		self.unHideGrid = False

	
	def createUnitImage(self):
		self.image = Image.new("RGBA", (self.tileSizeWidth  , self.tileSizeHeight))
		self.draw = ImageDraw.Draw(self.image)
	

	def setUp(self):
		self.colOverlay = coloroverlay.ColorOverlay()
		self.colOverlay.randomSteps = True 
		self.colOverlay.steps = self.config.steps
		self.colOverlay.maxBrightness = self.config.brightness
		self.colOverlay.tLimitBase = self.config.tLimitBase

		self.score = 0 if random.random() > .1 else 1

		if self.useFixedPalette == True :

			self.colOverlay.minHue = self.palette[0]
			self.colOverlay.maxHue = self.palette[1]
			self.colOverlay.minSaturation = self.palette[2]
			self.colOverlay.maxSaturation= self.palette[3]
			self.colOverlay.minValue = self.palette[4]
			self.colOverlay.maxValue = self.palette[5]
			self.colOverlay.maxBrightness = self.colOverlay.maxValue

			self.colOverlay.dropHueMin = self.dropHueMin
			self.colOverlay.dropHueMax = self.dropHueMax

			self.colOverlay.colorB = [0,0,0]
			self.colOverlay.colorA = [0,0,0]
			self.colOverlay.currentColor = [0,0,0]
			self.colOverlay.autoChange = False
			self.colOverlay.randomRange = (self.colorStepsRangeMin,self.colorStepsRangeMax)

			self.colOverlay.colorTransitionSetup()

	
	def getNeighbours(self):
		N = []
		previousRow = self.row - 1
		nextRow = self.row + 1
		previousCol = self.col - 1
		nextCol = self.col + 1

		N.append((previousCol, previousRow))
		N.append((self.col, previousRow))
		N.append((nextCol, previousRow))

		N.append((previousCol, self.row))
		N.append((nextCol, self.row))

		N.append((previousCol, nextRow))
		N.append((self.col, nextRow))
		N.append((nextCol, nextRow))

		return N


	def drawUnit(self):

		self.colOverlay.stepTransition()
		self.bgColor  = tuple(int(a*config.brightness) for a in (self.colOverlay.currentColor))

		fontColor = self.bgColor
		fontColor = (0,0,0)
		outlineColor = self.bgColor

		if(self.unHideGrid == True):
			fontColor = config.fontColor
			outlineColor = config.outlineColor

		if self.config.showOutline == False :
			outlineColor = self.bgColor

		'''
		if self.colOverlay.gotoNextTransition == True :
			if self.colOverlay.getPercentageDone() > 50 :
				if random.random() > .1 :
					self.colOverlay.colorTransitionSetup()
		'''
		
		self.draw.rectangle((0,0,self.tileSizeWidth - 1,self.tileSizeHeight -1), 
			fill=self.bgColor,  outline=outlineColor)
		
		#displyInfo = displyInfo.encode('utf-8')
		if self.config.showText == True :
			#u"\u000D"
			displyInfo1  =  str(self.col) + ", " + str(self.row) 
			displyInfo2  =  str(self.col * self.tileSizeWidth) + ", " + str(self.row * self.tileSizeHeight)
			self.draw.text((2,- 1), str(self.unitNumber), fontColor, font=config.font)
			#self.draw.text((2,- 1), (displyInfo1), fontColor, font=config.font)
			#self.draw.text((2,- 1 + config.fontSize), (displyInfo2), fontColor, font=config.font)

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def makeGrid():
	global config
	unitNumber = 1
	config.gridArray = [[[] for i in range(config.rows)] for i in range(config.cols)]

	for row in range (0, config.rows) :
		for col in range (0, config.cols) :
			u = unit()
			u.config = config
			u.tileSizeWidth = config.tileSizeWidth
			u.tileSizeHeight = config.tileSizeHeight
			u.xPos = col * config.tileSizeWidth
			u.yPos = row * config.tileSizeHeight
			u.row = row
			u.col = col
			u.unitNumber = unitNumber
			u.useFixedPalette = config.useFixedPalette
			u.colorStepsRangeMin =config.colorStepsRangeMin
			u.colorStepsRangeMax = config.colorStepsRangeMax

			if(config.useFixedPalette == True) :
				if unitNumber <= config.paletteRange :
					u.palette = config.palette['p'+ str(unitNumber)]
				else :
					u.palette = config.palette['p' + str(config.paletteRange)]
				u.dropHueMin = config.paletteDropHueMin
				u.dropHueMax = config.paletteDropHueMax

			u.createUnitImage()
			if (config.coordinatedColorChange == False ) :
				u.setUp()

			u.drawUnit()
			config.unitArrray.append(u)
			unitNumber +=1
			config.gridArray[col][row] = u


def redrawGrid():

	
	for u in config.unitArrray:
		u.bgColor = tuple(int(a*config.brightness) for a in (config.colOverlay.currentColor))
		u.drawUnit()
		config.image.paste(u.image,(u.xPos + config.imageXOffset,u.yPos), u.image)


		if u.colOverlay.complete == True :
				neighbours = u.getNeighbours()
				u.colOverlay.colorTransitionSetup()
				for unit in neighbours:
					col = unit[0]
					row = unit[1]
					if col >= 0 and col < config.cols and row >= 0 and row < config.rows:
						targetUnit = config.gridArray[col][row]
						if random.random() <= config.propagationProbability  :
							if targetUnit.colOverlay.getPercentageDone() > config.doneThreshold :
								targetUnit.colOverlay.colorTransitionSetup(newColor = u.colOverlay.colorB, steps = round(u.colOverlay.steps/3))


	config.render(config.image, 0,0)


def redrawGrid2():

	
	for u in config.unitArrray:
		u.bgColor = tuple(int(a*config.brightness) for a in (config.colOverlay.currentColor))
		u.drawUnit()
		config.image.paste(u.image,(u.xPos + config.imageXOffset,u.yPos), u.image)


		neighbours = u.getNeighbours()
		u.colOverlay.colorTransitionSetup()

		score = 0
		for unit in neighbours:
			col = unit[0]
			row = unit[1]
			if col >= 0 and col < config.cols and row >= 0 and row < config.rows:
				targetUnit = config.gridArray[col][row]

				if targetUnit.score == 1 :
					score +=1

		if u.score == 1 :
			if score < config.underPopulationThreshold :
				u.score = 0

			## Should be > 3
			if score > config.overCrowdingThreshold :
				u.score = 0

			if score > 1 and score < config.dieThreshold  :
				u.score = 1

		if u.score == 0 :
			if score == config.liveThreshold  :
				u.score = 1


		if u.score == 1 :
			u.colOverlay.colorTransitionSetup(steps = round(u.colOverlay.steps/3))

		if u.score == 0 :
			u.colOverlay.colorTransitionSetup(newColor = (5,5,100))

		if random.random() > config.propagationProbability :
			u.score = 1

	config.render(config.image, 0,0)

## Setup and run functions

def main(run = True) :
	global config, directionOrder
	print("---------------------")
	print("SIGNAGE Loaded")


	colorutils.brightness = config.brightness
	config.canvasImageWidth = config.screenWidth
	config.canvasImageHeight = config.screenHeight
	config.canvasImageWidth -= 4
	config.canvasImageHeight -= 4
	config.delay = float(workConfig.get("signage", 'redrawDelay'))

	config.baseRotation = config.rotation


	config.fontColorVals = ((workConfig.get("signage", 'fontColor')).split(','))
	config.fontColor = tuple(map(lambda x: int(int(x)  * config.brightness), config.fontColorVals))
	config.outlineColorVals = ((workConfig.get("signage", 'outlineColor')).split(','))
	config.outlineColor = tuple(map(lambda x: int(int(x) * config.brightness) , config.outlineColorVals))


	config.coordinatedColorChange = False
	config.propagationProbability = float(workConfig.get("signage", 'propagationProbability'))
	config.doneThreshold = float(workConfig.get("signage", 'doneThreshold'))
	
	config.overCrowdingThreshold = int(workConfig.get("signage","overCrowdingThreshold"))
	config.underPopulationThreshold = int(workConfig.get("signage","underPopulationThreshold"))
	config.liveThreshold = int(workConfig.get("signage","liveThreshold"))
	config.dieThreshold = int(workConfig.get("signage","dieThreshold"))


	config.timeTrigger = workConfig.getboolean("signage", 'timeTrigger')
	config.tLimitBase = int(workConfig.get("signage", 'tLimitBase'))
	config.colOverlay = coloroverlay.ColorOverlay()
	config.colOverlay.randomSteps = False 
	config.colOverlay.timeTrigger = False 
	config.colOverlay.tLimitBase = config.tLimitBase 
	config.colOverlay.maxBrightness = config.brightness
	config.unHideGrid = False
	config.colorStepsRangeMin = int(workConfig.get("signage","colorStepsRangeMin"))
	config.colorStepsRangeMax = int(workConfig.get("signage","colorStepsRangeMax"))
	

	config.unitArrray = []

	try:
		config.randomRotation = workConfig.getboolean("signage","randomRotation")
	except Exception as e:
		print (str(e))
		config.randomRotation = False	

	try:
		config.showText = workConfig.getboolean("signage","showText")
	except Exception as e:
		print (str(e))
		config.showText = True
	
	try:
		config.showOutline = workConfig.getboolean("signage","showOutline")
	except Exception as e:
		print (str(e))
		config.showOutline = True


	try:
		config.steps = int(workConfig.get("signage","steps"))
	except Exception as e:
		print (str(e))
		config.steps = 200
	
	try:
		config.useFixedPalette = workConfig.getboolean("signage","useFixedPalette")
		config.paletteRange = int(workConfig.get("signage","paletteRange"))
		config.palette = {}
		for i in range (0,config.paletteRange) :
			name = "p" + str(i+1)
			vals = ((workConfig.get("signage", name)).split(','))
			config.palette[name] = tuple(map(lambda x: float(x), vals))
		print(config.palette['p1'])
		config.paletteDropHueMin = int(workConfig.get("signage","dropHueMin"))
		config.paletteDropHueMax = int(workConfig.get("signage","dropHueMax"))
			
	except Exception as e:
		print (str(e))
		config.useFixedPalette = False

	config.colOverlay.steps = config.steps 


	config.tileSizeWidth = int(workConfig.get("displayconfig", 'tileSizeWidth'))
	config.tileSizeHeight = int(workConfig.get("displayconfig", 'tileSizeHeight'))

	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

	config.canvasImage = Image.new("RGBA", (config.canvasImageWidth  , config.canvasImageHeight))
	config.fontSize = 14
	config.font = ImageFont.truetype(config.path  + '/assets/fonts/freefont/FreeSansBold.ttf', config.fontSize)
	
	setUp()

	if(run) : runWork()


def setUp():
	global config

	makeGrid()


def runWork():
	global blocks, config, XOs
	#gc.enable()
	while True:
		iterate()
		time.sleep(config.delay)  


def iterate() :

	global config
	redrawGrid2()
	

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''




