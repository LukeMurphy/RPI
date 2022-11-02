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


	def setUp(self,paletteArray, linePaletteArray):
		self.blockImage = Image.new("RGBA", (self.blockWidth, self.blockHeight))
		self.blockDraw = ImageDraw.Draw(self.blockImage)

		# [minHue,maxHue,minSaturation,maxSaturation,minValue,maxValue,tLimitBase]

		self.colOverlay = getConfigOverlay(paletteArray)
		self.colOverlay2 = getConfigOverlay(linePaletteArray)


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
			#if self.gap < 3 :
			self.polyDeltaX = round(random.uniform(-self.config.deltaXVal,self.config.deltaXVal))
			self.polyDeltaY = round(random.uniform(-self.config.deltaXVal,self.config.deltaYVal))
			x1 = 0
			y1 = i * (self.barWidth + self.gap) 
			x2 = self.blockWidth-1 + self.polyDeltaX
			y2 = i * (self.barWidth + self.gap) + self.barWidth + self.polyDeltaY


			#self.blockDraw.rectangle((x1,y1,x2,y2),outline=(None), fill=outClr)
			if self.config.drawOutlines == True :
				self.blockDraw.polygon(((x1,y1),(x2,y1),(x2,y2),(x1,y2)),outline=(clr2), fill=outClr)
			else :
				self.blockDraw.polygon(((x1,y1),(x2,y1),(x2,y2),(x1,y2)),outline=None, fill=outClr)
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


	if random.random() < config.filterRemappingProb:

		config.useFilters = True
		config.remapImageBlock = True

		startX = round(random.uniform(0,config.filterRemapRangeX) )
		startY = round(random.uniform(0,config.filterRemapRangeY) )
		endX = round(random.uniform(4, config.filterRemapminHoriSize) )
		endY = round(random.uniform(4, config.filterRemapminVertSize) )
		config.remapImageBlockSection = [startX,startY,startX + endX, startY + endY]
		config.remapImageBlockDestination = [startX,startY]

	if random.random() < config.blurPatchProb:

		x1 = round(random.uniform(0,config.canvasWidth/2))
		x2 = round(random.uniform(x1,config.canvasWidth))
		y1 = round(random.uniform(0,config.canvasHeight/2))
		y2 = round(random.uniform(y1,config.canvasHeight))

		config.useBlur = True
		blurXOffset = x1
		blurYOffset = y1
		blurSectionWidth = x2
		blurSectionHeight = y2
		sectionBlurRadius = 1


def getConfigOverlay(palette):
	colOverlay = coloroverlay.ColorOverlay()
	colOverlay.randomSteps = False
	colOverlay.timeTrigger = True
	colOverlay.maxBrightness = 1
	colOverlay.steps = 50
	colOverlay.minHue = palette[0]
	colOverlay.maxHue = palette[1]
	colOverlay.minSaturation = palette[2]
	colOverlay.maxSaturation = palette[3]
	colOverlay.minValue = palette[4]
	colOverlay.maxValue = palette[5]
	colOverlay.dropHueMin = palette[6]
	colOverlay.dropHueMax = palette[7]
	colOverlay.tLimitBase = palette[8]
	colOverlay.colorTransitionSetup()
	return colOverlay

def getConfigLineOverlay(palette):
	colOverlay = coloroverlay.ColorOverlay()
	colOverlay.randomSteps = False
	colOverlay.timeTrigger = True
	colOverlay.maxBrightness = 1
	colOverlay.steps = 50
	colOverlay.minHue = palette[0]
	colOverlay.maxHue = palette[1]
	colOverlay.minSaturation = palette[2]
	colOverlay.maxSaturation = palette[3]
	colOverlay.minValue = palette[4]
	colOverlay.maxValue = palette[5]
	colOverlay.dropHueMin = palette[6]
	colOverlay.dropHueMax = palette[7]
	colOverlay.tLimitBase = palette[8]
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
	try:
		dropHueMin = float(workConfig.get(palette, "line_dropHueMin"))
		dropHueMax = float(workConfig.get(palette, "line_dropHueMax"))
	except Exception as e:
		print(str(e))
		dropHueMax = 0
		dropHueMin = 0
	return([minHue,maxHue,minSaturation,maxSaturation,minValue,maxValue,dropHueMin,dropHueMax,tLimitBase])


def buildLinePalette(config,index=0):
	palette = config.palettes[index]
	tLimitBase = int(workConfig.get(palette, "line_tLimitBase"))
	minHue = float(workConfig.get(palette, "line_minHue"))
	maxHue = float(workConfig.get(palette, "line_maxHue"))
	minSaturation = float(workConfig.get(palette, "line_minSaturation")	)
	maxSaturation = float(workConfig.get(palette, "line_maxSaturation"))
	minValue = float(workConfig.get(palette, "line_minValue"))
	maxValue = float(workConfig.get(palette, "line_maxValue"))
	try:
		dropHueMin = float(workConfig.get(palette, "line_dropHueMin"))
		dropHueMax = float(workConfig.get(palette, "line_dropHueMax"))
	except Exception as e:
		print(str(e))
		dropHueMax = 0
		dropHueMin = 0
	return([minHue,maxHue,minSaturation,maxSaturation,minValue,maxValue,dropHueMin,dropHueMax,tLimitBase])

# This is not really used - for future use sometime
def buildLinePalette2(config,index=0):
	palette = config.palettes[index]
	try:
		tLimitBase = int(workConfig.get(palette, "line2_tLimitBase"))
		minHue = float(workConfig.get(palette, "line2_minHue"))
		maxHue = float(workConfig.get(palette, "line2_maxHue"))
		minSaturation = float(workConfig.get(palette, "line2_minSaturation"))
		maxSaturation = float(workConfig.get(palette, "line2_maxSaturation"))
		minValue = float(workConfig.get(palette, "line2_minValue"))
		maxValue = float(workConfig.get(palette, "line2_maxValue"))
		dropHueMin = float(workConfig.get(palette, "line2_dropHueMin"))
		dropHueMax = float(workConfig.get(palette, "line2_dropHueMax"))
	except Exception as e:
		print(str(e))
		tLimitBase = 0
		minHue = 0
		maxHue = 0
		minSaturation = 0
		maxSaturation = 0
		minValue = 0
		maxValue = 0
		dropHueMin = 0
		dropHueMax = 0
		dropHueMax = 0
		dropHueMin = 0
	return([minHue,maxHue,minSaturation,maxSaturation,minValue,maxValue,dropHueMin,dropHueMax,tLimitBase])


# Builds flexible grid
def buildGrid(config):

	count = 0
	config.barBlocks = []
	delta = 0 
	sizes = [16,24,32,40,48,56,64,72,80,88,96,104,112,120,128]
	rows = round(config.canvasHeight / config.blockHeight) * 1
	cols = round(config.canvasWidth / config.blockWidth ) 

	if cols > 80 :
		cols = 80


	print("")
	print("----buildGrid --")
	print(rows,cols)
	print("------")
	print("")


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


				paletteIndex = math.floor(random.uniform(0,len(config.palettes)))
				barBlockUnit.setUp(buildPalette(config,paletteIndex), buildLinePalette(config,paletteIndex))

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

		paletteIndex = math.floor(random.uniform(0,len(config.palettes)))
		barBlockUnit.setUp(buildPalette(config,paletteIndex))
		config.barBlocks.append(barBlockUnit)
		count +=1


# Builds uniform grid
def buildUniformGrid(config):

	count = 0
	config.barBlocks = []
	delta = 0 
	index = math.floor(random.uniform(0,len(config.sizeArray)))
	blockWidth = config.sizeArray[index]
	blockHeight = blockWidth

	rows = round(config.canvasHeight / blockHeight) * 2
	cols = round(config.canvasWidth / blockWidth) 

	print("")
	print("---- buildUniformGrid --")
	print(rows,cols,blockWidth,blockHeight)
	print("------")
	print("")


	for r in range(0,rows) :
		lastX = 0
		for c in range(0,cols) :
			barBlockUnit = Block(config,count)
			barBlockUnit.blockWidth = round(random.uniform(blockWidth - delta, blockWidth + delta)) 
			barBlockUnit.blockHeight = barBlockUnit.blockWidth
			barBlockUnit.xPos = lastX #c * barBlockUnit.blockWidth
			lastX += barBlockUnit.blockWidth 
			barBlockUnit.yPos = r * blockHeight

			barBlockUnit.barWidth = round(random.uniform(config.barWidthMin,config.barWidthMax))
			barBlockUnit.gap = round(random.uniform(config.gapWidthMin,config.gapWidthMax))
			if count % 2 != 0 :
				barBlockUnit.rotation = round(random.uniform(90-config.rotationVariation,90+config.rotationVariation))
			else:
				barBlockUnit.rotation = round(random.uniform(-config.rotationVariation,config.rotationVariation))

			paletteIndex = math.floor(random.uniform(0,len(config.palettes)))
			barBlockUnit.setUp(buildPalette(config,paletteIndex), buildLinePalette(config,paletteIndex))
			config.barBlocks.append(barBlockUnit)
			count +=1	


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
			config.deltaXVal = round(random.uniform(0,config.deltaVal ))
			config.deltaYVal = round(random.uniform(0,config.deltaVal ))
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
	config.drawOutlines = (workConfig.getboolean("movingpattern", "drawOutlines"))

	config.blurPatchProb = float(workConfig.get("movingpattern", "blurPatchProb"))

	try:
		config.filterRemapping = (workConfig.getboolean("movingpattern", "filterRemapping"))
		config.filterRemappingProb = float(workConfig.get("movingpattern", "filterRemappingProb"))
		config.filterRemapminHoriSize = int(workConfig.get("movingpattern", "filterRemapminHoriSize"))
		config.filterRemapminVertSize = int(workConfig.get("movingpattern", "filterRemapminVertSize"))
		config.filterRemapRangeX = int(workConfig.get("movingpattern", "filterRemapRangeX"))
		config.filterRemapRangeY = int(workConfig.get("movingpattern", "filterRemapRangeY"))
	except Exception as e:
		print(str(e))
		config.filterRemapping = False
		config.filterRemappingProb = 0.0
		config.filterRemapminHoriSize = 24
		config.filterRemapminVertSize = 24
		config.filterRemapRangeX = config.canvasWidth
		config.filterRemapRangeY = config.canvasHeight



	config.sizeArrayVals = (workConfig.get("movingpattern", "sizeArray"))
	config.sizeArray = config.sizeArrayVals.split(",")
	config.sizeArray = list(
		map(lambda x: int(int(x)), config.sizeArray)
	)


	config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.canvasImage = Image.new(
		"RGBA", (config.canvasWidth, config.canvasHeight))
	config.canvasDraw = ImageDraw.Draw(config.canvasImage)


	config.destinationImage = Image.new(
		"RGBA", (config.canvasWidth, config.canvasHeight)
	)


	try:
		config.deltaXVal = int(workConfig.get("movingpattern", "deltaVal"))
		config.deltaYVal = int(workConfig.get("movingpattern", "deltaVal"))
		config.deltaVal = int(workConfig.get("movingpattern", "deltaVal"))
	except Exception as e:
		print(str(e))
		config.deltaXVal = 1
		config.deltaYVal = 1
		config.deltaVal = 1


	config.gridOptions = ['buildGrid','buildGrid','buildUniformGrid']


	index = math.floor(random.random() * len(config.gridOptions))
	if index > len(config.gridOptions) : index = 0

	config.palettes = workConfig.get("movingpattern", "palettes").split(",")

	# Right now the background is controlled by the first palette in the list of
	# palettes to use
	config.colOverlay = getConfigOverlay(buildPalette(config,0))
	


	print("Running a :" + str(config.gridOptions[index]) )

	eval(config.gridOptions[index])(config)



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
