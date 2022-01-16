# ################################################### #
import argparse
import math
import random
import time
import types
from modules.configuration import bcolors
from modules import badpixels, coloroverlay, colorutils, panelDrawing
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps, ImageFilter
import numpy as np


class Block:

	def __init__(self, config, i):
		# print ("init Fludd", i)

		# self.boxMax = config.screenWidth - 1
		# self.boxMaxAlt = self.boxMax + int(random.uniform(10,30) * config.screenWidth)
		# self.boxHeight = config.screenHeight - 2        #

		self.unitNumber = i
		self.config = config

		self.xPos = 0
		self.yPos = 0
		self.blockWidth = 128
		self.blockHeight = 128
		self.barWidth = 4
		self.gap = 0
		self.rotation = 0
		self.polyDeltaX = 0
		self.polyDeltaY = 0


	def setUp(self):
		self.blockImage = Image.new("RGBA", (self.blockWidth, self.blockHeight))
		self.blockDraw = ImageDraw.Draw(self.blockImage)

		tLimitBase = 12
		minHue = 0
		maxHue = 360 
		minSaturation= .99
		maxSaturation= .6
		minValue = .1
		maxValue = .99

		self.colOverlay = getConfigOverlay(tLimitBase, minHue, maxHue, minSaturation, maxSaturation, minValue, maxValue)
		self.colOverlay2 = getConfigOverlay(tLimitBase, minHue, maxHue, minSaturation, maxSaturation, minValue, maxValue)


	def bars(self):


		clr = tuple(
			round(a * self.config.brightness) for a in (self.colOverlay.currentColor)
		)
		clr2 = tuple(
			round(a * self.config.brightness) for a in (self.colOverlay2.currentColor)
		)

		self.blockDraw.rectangle(
			(0, 0, self.blockWidth, self.blockHeight), fill=self.config.bgColor, outline=None)

		count  = 0
		numBars = round(self.blockHeight/self.barWidth)
		for i in range(0, numBars):
			outClr = clr2
			if count % 2 == 0 :
				outClr = clr
			if self.gap < 3 :
				self.polyDeltaX = round(random.uniform(-self.config.deltaXVal,self.config.deltaXVal))
				self.polyDeltaY = round(random.uniform(-self.config.deltaXVal,self.config.deltaYVal))
			x1 = 0
			y1 = i * (self.barWidth + self.gap) 
			x2 = self.blockWidth-1 + self.polyDeltaX
			y2 = i * (self.barWidth + self.gap) + self.barWidth + self.polyDeltaY


			#self.blockDraw.rectangle((x1,y1,x2,y2),outline=(None), fill=outClr)
			self.blockDraw.polygon(((x1,y1),(x2,y1),(x2,y2),(x1,y2)),outline=(None), fill=outClr)
			count += 1


def redraw(config):

	config.canvasDraw.rectangle(
			(0, 0, config.canvasWidth, config.canvasHeight), fill=config.bgColor, outline=None)

	for b in (config.barBlocks) :
		b.bars()
		temp = b.blockImage.copy()
		if b.rotation != 0 :
			temp = temp.rotate(b.rotation,0,True)
		config.canvasImage.paste(temp, (b.xPos, b.yPos), temp)
		b.colOverlay.stepTransition()
		b.colOverlay2.stepTransition()


def iterate():
	global config
	config.colOverlay.stepTransition()

	config.bgColor = tuple(
		round(a * config.brightness) for a in (config.colOverlay.currentColor)
	)

	redraw(config)

	if random.random() < config.changeGridProb:
		index = math.floor(random.random() * len(config.gridOptions))
		if index > len(config.gridOptions) : index = 0
		print("Running a :" + str(config.gridOptions[index]) )
		eval(config.gridOptions[index])(config)

	if random.random() < config.changeQuiverProb:
		if random.random() < .75 :
			config.deltaXVal = round(random.uniform(0,1))
			config.deltaYVal = round(random.uniform(0,1))
		else :
			# a bit more often, things just go still
			config.deltaXVal = config.deltaYVal = 0

	if config.useDrawingPoints == True:
		config.panelDrawing.canvasToUse = config.canvasImage
		config.panelDrawing.render()
	else:
		config.render(config.canvasImage, 0, 0,
					  config.canvasWidth, config.canvasHeight)
	# Done


def runWork():
	global config
	print(bcolors.OKGREEN + "** " + bcolors.BOLD)
	print("Running barblocks.py")
	print(bcolors.ENDC)
	while config.isRunning == True:
		iterate()
		time.sleep(config.redrawSpeed)
		if config.standAlone == False:
			config.callBack()


def getConfigOverlay(tLimitBase, minHue, maxHue, minSaturation, maxSaturation, minValue, maxValue):
	colOverlay = coloroverlay.ColorOverlay()
	colOverlay.randomSteps = False
	colOverlay.timeTrigger = True
	colOverlay.tLimitBase = tLimitBase
	colOverlay.maxBrightness = 1
	colOverlay.steps = 50
	colOverlay.minHue = minHue
	colOverlay.maxHue = maxHue
	colOverlay.minSaturation = minSaturation
	colOverlay.maxSaturation = maxSaturation
	colOverlay.minValue = minValue
	colOverlay.maxValue = maxValue
	colOverlay.colorTransitionSetup()
	return colOverlay


def buildPalette(config,index=0):
	palette = config.palettes[index]

	tLimitBase = int(workConfig.get(palette, "tLimitBase"))
	minHue = float(workConfig.get(palette, "minHue"))
	maxHue = float(workConfig.get(palette, "maxHue"))
	minSaturation = float(workConfig.get(palette, "minSaturation")	)
	maxSaturation = float(workConfig.get(palette, "maxSaturation"))
	minValue = float(workConfig.get(palette, "minValue"))
	maxValue = float(workConfig.get(palette, "maxValue"))
	config.colOverlay = getConfigOverlay(
		tLimitBase, minHue, maxHue, minSaturation, maxSaturation, minValue, maxValue)


# Builds flexible grid
def buildGrid(config):

	count = 0
	config.barBlocks = []
	delta = 0 
	sizes = [16,24,32,40,48,56,64,72,80,88,96,104,112,120,128]
	rows = round(config.canvasHeight / config.blockHeight) * 1
	cols = round(config.canvasWidth / config.blockWidth) * 2

	gridSize = 8
	availableCoords = []
	for r in range(0,rows) :
		availableCoords.append([])
		for c in range(0,cols) :
			availableCoords[r].append( [c * gridSize, r * gridSize, 0])


	#first one is upper left
	for row in range(0,len(availableCoords)-2):
		for col in range(0,len(availableCoords[row])):
			if availableCoords[row][col][2] == 0 and availableCoords[row+1][col][2] == 0 and availableCoords[row+2][col][2] == 0 :

				# set size of patch
				index = math.floor(random.uniform(0,len(config.sizeArray)))
				blockWidth = config.sizeArray[index]

				# see if the width is too wide sometimes
				removedPointsSize = round(blockWidth/gridSize)
				if removedPointsSize + col < len(availableCoords[row]) :
					if availableCoords[row][col + removedPointsSize][2] == 1 :
						#reduce size

						newIndex = math.floor(random.uniform(0,3))
						blockWidth = config.sizeArray[newIndex]
	

				blockHeight = blockWidth

				barBlockUnit = Block(config,count)
				barBlockUnit.blockWidth = round(random.uniform(blockWidth - delta, blockWidth + delta)) 
				barBlockUnit.blockHeight = blockHeight

				barBlockUnit.xPos = availableCoords[row][col][0]
				barBlockUnit.yPos = availableCoords[row][col][1]

				barBlockUnit.barWidth = round(random.uniform(config.barWidthMin,config.barWidthMax))
				barBlockUnit.gap = round(random.uniform(config.gapWidthMin,config.gapWidthMax))
				if count % 2 != 0 :
					barBlockUnit.rotation = round(random.uniform(90-config.rotationVariation,90+config.rotationVariation))
				else:
					barBlockUnit.rotation = round(random.uniform(-config.rotationVariation,config.rotationVariation))

				barBlockUnit.setUp()
				config.barBlocks.append(barBlockUnit)
				count +=1

				removedPointsSize = round(blockWidth/gridSize)
				#print(removedPointsSize, len(availableCoords))

				for r in range(0,removedPointsSize):
					for c in range(0,removedPointsSize):
						if (col + c) < len(availableCoords[row]) and (row + r) < len(availableCoords):
							availableCoords[row + r][col + c][2] = 1


# Builds overlapped grid
def buildOverlapGrid(config):

	count = 0
	config.barBlocks = []
	delta = 0 

	rows = 7
	cols = 7

	gridSize = 32
	availableCoords = []
	for r in range(0,rows) :
		for c in range(0,cols) :
			availableCoords.append([c * gridSize, r * gridSize])


	#first one is upper left
	for i in range(0,len(availableCoords)) :
		index = math.floor(random.uniform(0,len(config.sizeArray)))
		blockWidth = config.sizeArray[index]
		blockHeight = config.blockWidth
		barBlockUnit = Block(config,count)
		barBlockUnit.blockWidth = round(random.uniform(blockWidth - delta, blockWidth + delta)) 
		barBlockUnit.blockHeight = barBlockUnit.blockWidth
		barBlockUnit.xPos = availableCoords[i][0]
		barBlockUnit.yPos = availableCoords[i][1]

		barBlockUnit.barWidth = round(random.uniform(config.barWidthMin,config.barWidthMax))
		barBlockUnit.gap = round(random.uniform(config.gapWidthMin,config.gapWidthMax))
		if count % 2 != 0 :
			barBlockUnit.rotation = round(random.uniform(90-config.rotationVariation,90+config.rotationVariation))
		else:
			barBlockUnit.rotation = round(random.uniform(-config.rotationVariation,config.rotationVariation))

		barBlockUnit.setUp()
		config.barBlocks.append(barBlockUnit)
		count +=1


# Builds uniform grid
def buildUniformGrid(config):

	count = 0
	config.barBlocks = []
	delta = 0 
	index = math.floor(random.uniform(0,len(config.sizeArray)))
	config.blockWidth = config.sizeArray[index]
	config.blockHeight = config.blockWidth

	rows = round(config.canvasHeight / config.blockHeight) * 2
	cols = round(config.canvasWidth / config.blockWidth) * 2


	for r in range(0,rows) :
		lastX = 0
		for c in range(0,cols) :
			barBlockUnit = Block(config,count)
			barBlockUnit.blockWidth = round(random.uniform(config.blockWidth - delta, config.blockWidth + delta)) 
			barBlockUnit.blockHeight = barBlockUnit.blockWidth
			barBlockUnit.xPos = lastX #c * barBlockUnit.blockWidth
			lastX += barBlockUnit.blockWidth 
			barBlockUnit.yPos = r * config.blockHeight

			barBlockUnit.barWidth = round(random.uniform(config.barWidthMin,config.barWidthMax))
			barBlockUnit.gap = round(random.uniform(config.gapWidthMin,config.gapWidthMax))
			if count % 2 != 0 :
				barBlockUnit.rotation = round(random.uniform(90-config.rotationVariation,90+config.rotationVariation))
			else:
				barBlockUnit.rotation = round(random.uniform(-config.rotationVariation,config.rotationVariation))

			barBlockUnit.setUp()
			config.barBlocks.append(barBlockUnit)
			count +=1	


def main(run=True):
	global config
	config.redrawSpeed = float(workConfig.get("movingpattern", "redrawSpeed"))
	config.changeGridProb = float(workConfig.get("movingpattern", "changeGridProb"))
	config.changeQuiverProb = float(workConfig.get("movingpattern", "changeQuiverProb"))
	config.rotationVariation = float(workConfig.get("movingpattern", "rotationVariation"))
	config.blockWidth = int(workConfig.get("movingpattern", "blockWidth"))
	config.blockHeight = int(workConfig.get("movingpattern", "blockHeight"))
	config.rows = int(workConfig.get("movingpattern", "rows"))
	config.cols = int(workConfig.get("movingpattern", "cols"))
	config.barWidthMin = int(workConfig.get("movingpattern", "barWidthMin"))
	config.barWidthMax = int(workConfig.get("movingpattern", "barWidthMax"))
	config.gapWidthMin = int(workConfig.get("movingpattern", "gapWidthMin"))
	config.gapWidthMax = int(workConfig.get("movingpattern", "gapWidthMax"))


	config.sizeArrayVals = (workConfig.get("movingpattern", "sizeArray"))
	config.sizeArray = config.sizeArrayVals.split(",")
	config.sizeArray = list(
		map(lambda x: int(int(x)), config.sizeArray)
	)

	print(config.sizeArray)

	config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.canvasImage = Image.new(
		"RGBA", (config.canvasWidth, config.canvasHeight))
	config.canvasDraw = ImageDraw.Draw(config.canvasImage)


	config.destinationImage = Image.new(
		"RGBA", (config.canvasWidth, config.canvasHeight)
	)

	config.deltaXVal = 1
	config.deltaYVal = 1

	config.gridOptions = ['buildGrid','buildGrid','buildUniformGrid']


	index = math.floor(random.random() * len(config.gridOptions))
	if index > len(config.gridOptions) : index = 0


	print("Running a :" + str(config.gridOptions[index]) )
	eval(config.gridOptions[index])(config)

	

	config.palettes = workConfig.get("movingpattern", "palettes").split(",")
	buildPalette(config,0)

	# THIS IS USED AS WAY TO MOCKUP A CONFIGURATION OF RECTANGULAR PANELS
	panelDrawing.mockupBlock(config, workConfig)

	''' 
		########### Need to add something like this at final render call  as well
			
		########### RENDERING AS A MOCKUP OR AS REAL ###########
		if config.useDrawingPoints == True :
			config.panelDrawing.canvasToUse = config.renderImageFull
			config.panelDrawing.render()
		else :
			#config.render(config.canvasImage, 0, 0, config.canvasWidth, config.canvasHeight)
			#config.render(config.image, 0, 0)
			config.render(config.renderImageFull, 0, 0)
	'''

	if run:
		runWork()
