# ################################################### #
import argparse
import math
import random
import time
import types
from modules.configuration import bcolors
from modules import badpixels, coloroverlay, colorutils, panelDrawing
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps
import numpy as np

def runningSpiral(config):
	# 16px grid box spiral for now
	w = 4
	h = 4
	x = config.xIncrementer
	y = config.yIncrementer
	config.bgColor = tuple(
		int(a * config.brightness) for a in (config.colOverlay.currentColor)
	)

	clr = tuple(
		int(a * config.brightness) for a in (config.linecolOverlay.currentColor)
	)

	clr2 = tuple(
		int(a * config.brightness) for a in (config.linecolOverlay2.currentColor)
	)

	config.blockDraw.rectangle((0,0,config.blockWidth, config.blockHeight), fill = config.bgColor, outline=None)

	lineMult = config.lineDiff  * 2
	numLines = round(config.blockWidth / config.lineDiff  * 2)
	
	d = 2
	direction = 1
	distance = 1

	p1 =  [config.blockWidth/2, config.blockHeight/2]
	p2 =  [config.blockWidth/2, config.blockHeight/2]


	for i in range (0,numLines):
		distance += d
		p2[0] = p2[0] + distance * direction
		config.blockDraw.line( (p1[0],p1[1],p2[0],p2[1]), fill=clr)
		p1[0] = p2[0]
		distance += d
		p2[1] = p2[1] + distance * direction
		config.blockDraw.line( (p1[0],p1[1],p2[0],p2[1]), fill=clr)
		direction *= -1
		p1[1] = p2[1]


	direction = -1
	distance = 1

	p1 =  [config.blockWidth/2-0, config.blockHeight/2+2]
	p2 =  [config.blockWidth/2-0, config.blockHeight/2+2]


	for i in range (0,numLines):
		distance += d
		p2[0] = p2[0] + distance * direction
		config.blockDraw.line( (p1[0],p1[1],p2[0],p2[1]), fill=clr2)
		p1[0] = p2[0]
		distance += d
		p2[1] = p2[1] + distance * direction
		config.blockDraw.line( (p1[0],p1[1],p2[0],p2[1]), fill=clr2)
		direction *= -1
		p1[1] = p2[1]


def shingles(config):
	clr = config.lineColor
	w = 4
	h = 4
	x = config.xIncrementer
	y = config.yIncrementer
	config.bgColor = tuple(
		int(a * config.brightness) for a in (config.colOverlay.currentColor)
	)

	clr = tuple(
		int(a * config.brightness) for a in (config.linecolOverlay.currentColor)
	)
	clr2 = tuple(
		int(a * config.brightness) for a in (config.linecolOverlay2.currentColor)
	)
	config.blockDraw.rectangle((0,0,config.blockWidth, config.blockHeight), fill = clr2, outline=None)

	numRows = 2
	boxWidth = config.blockWidth
	
	for i in range(0,2):
		config.blockDraw.ellipse((
			i * boxWidth - boxWidth/2, 
			-2, 
			i * boxWidth + boxWidth - boxWidth/2,
			-2 + boxWidth ), 
			outline=(clr), fill = clr2)

	config.blockDraw.ellipse((
		0, 
		-2 -boxWidth/2, 
		0 + boxWidth,
		-2 + boxWidth/2), 
		outline=(clr), fill = clr2)


def circles(config):
	clr = config.lineColor
	w = 4
	h = 4
	x = config.xIncrementer
	y = config.yIncrementer
	config.bgColor = tuple(
		int(a * config.brightness) for a in (config.colOverlay.currentColor)
	)

	clr = tuple(
		int(a * config.brightness) for a in (config.linecolOverlay.currentColor)
	)
	clr2 = tuple(
		int(a * config.brightness) for a in (config.linecolOverlay2.currentColor)
	)
	config.blockDraw.rectangle((0,0,config.blockWidth, config.blockHeight), fill = config.bgColor, outline=None)

	numLines = 1
	for i in range (0,numLines) :
		config.blockDraw.ellipse((
			i-1, 
			i-1, 
			config.blockWidth-1*i,
			config.blockHeight-1*i), 
			outline=(clr), fill = clr2)
		

def concentricBoxes(config):
	clr = config.lineColor

	config.bgColor = tuple(
		int(a * config.brightness) for a in (config.colOverlay.currentColor)
	)

	clr = tuple(
		int(a * config.brightness) for a in (config.linecolOverlay.currentColor)
	)

	config.blockDraw.rectangle((0,0,config.blockWidth, config.blockHeight), fill = config.bgColor, outline=None)


	for i in range (0,config.numConcentricBoxes,2) :
		config.blockDraw.rectangle((
			i-1, 
			i-1, 
			config.blockWidth-1*i,
			config.blockHeight-1*i), 
			outline=(clr), fill = None)
		

def randomizer(config) :

	w = config.randomBlockWidth
	h = config.randomBlockHeight

	config.bgColor = tuple(
		int(a * config.brightness) for a in (config.colOverlay.currentColor)
	)
	config.blockDraw.rectangle((0,0,config.blockWidth, config.blockHeight), fill = config.bgColor, outline=None)

	rows = config.blockHeight
	cols = config.blockWidth
	for r in range(0,rows, h):
		for c in range(0, cols, w):
			clr = colorutils.getRandomRGB()
			if random.random() < config.randomBlockProb :
				config.blockDraw.rectangle((c,r,w+c,h+r), fill=(clr), outline=None)


def diamond(config) :
	clr = (255,0,0,210)

	x = config.xIncrementer
	y = config.yIncrementer

	# needs to be in odd grid

	config.bgColor = tuple(
		int(a * config.brightness) for a in (config.colOverlay.currentColor)
	)

	config.blockDraw.rectangle((0,0,config.blockWidth, config.blockHeight), fill = config.bgColor, outline=None)
	step = config.diamondStep
	row = 1
	delta = 0
	w = 0
	h = 0
	mid = config.blockWidth/2

	

	for i in range(0,config.blockHeight,step*2) :
		for r in range(0,row, 1):
			x =  r  + mid -  row/2
			y = i + config.yIncrementer

			if y >= config.blockHeight :
				y -= config.blockHeight

			if (r % 2) !=1 :
				config.blockDraw.rectangle((x,y,w+x,h+y), fill=(clr), outline=None)
		if config.diamondUseTriangles == False :
			row = 2 * i + step  +  delta
			if i > (config.blockHeight/2):
				row = round(2 * (config.blockHeight-i) )+  delta
				#delta += -2
		else:
			row =  i + step

	'''
	imgPart1  = config.blockImage.crop((config.blockWidth-1, 0, config.blockWidth, config.blockHeight))
	imgPart2  = config.blockImage.crop((0, 0, config.blockWidth-1, config.blockHeight))

	config.blockImage.paste(imgPart2, (1,0), imgPart2)
	config.blockImage.paste(imgPart1, (0,0), imgPart1)
	'''


	config.yIncrementer += config.ySpeed

	if config.yIncrementer >= config.blockHeight:
		config.yIncrementer = 0


def diagonalMove(config) :
	clr = (255,0,0,210)
	w = 4
	h = 4
	x = config.xIncrementer
	y = config.yIncrementer

	config.blockDraw.rectangle((0,0,config.blockWidth, config.blockHeight), fill = config.bgColor, outline=None)
	config.blockDraw.rectangle((x,y,w+x,h+y), fill=(clr), outline=None)
	config.xIncrementer += 1
	config.yIncrementer += 1

	if config.xIncrementer >= config.blockWidth -4:
		config.xIncrementer = 0
	if config.yIncrementer >= config.blockHeight -4:
		config.yIncrementer = 0


def reMove(config) :

	clr = config.lineColor
	w = 4
	h = 4
	x = config.xIncrementer
	y = config.yIncrementer
	config.bgColor = tuple(
		int(a * config.brightness) for a in (config.colOverlay.currentColor)
	)

	clr = tuple(
		int(a * config.brightness) for a in (config.linecolOverlay.currentColor)
	)

	config.blockDraw.rectangle((0,0,config.blockWidth, config.blockHeight), fill = config.bgColor, outline=None)

	lineMult = config.lineDiff  * 2
	numLines = round(config.blockWidth / config.lineDiff  * 2)

	for i in range (0,numLines) :
		config.blockDraw.line((-2*config.blockWidth + config.xIncrementer + i * lineMult, 0, -2*config.blockWidth + config.blockWidth + config.xIncrementer+ i * lineMult,config.blockHeight), fill=(clr))
		if config.useDoubleLine == True : config.blockDraw.line((-2*config.blockWidth + config.xIncrementer + i * lineMult + 1, 0, -2*config.blockWidth + config.blockWidth + config.xIncrementer+ i * lineMult + 1,config.blockHeight), fill=(clr))

	config.xIncrementer += config.xSpeed
	config.yIncrementer += 0

	if config.xIncrementer >= config.blockWidth * 1:
		config.xIncrementer = -0
	if config.yIncrementer >= config.blockHeight -4:
		config.yIncrementer = 0


def wavePattern(config) :
	clr = config.lineColor
	w = 4
	h = 4
	x = config.xIncrementer
	y = config.yIncrementer


	config.bgColor = tuple(
		int(a * config.brightness) for a in (config.colOverlay.currentColor)
	)

	clr = tuple(
		int(a * config.brightness) for a in (config.linecolOverlay.currentColor)
	)
	clr2 = tuple(
		int(a * config.brightness) for a in (config.linecolOverlay2.currentColor)
	)	

	config.blockDraw.rectangle((0,0,config.blockWidth, config.blockHeight), fill = config.bgColor, outline=config.bgColor)

	numPoints = round(config.blockWidth)
	amplitude = config.amplitude
	yOffset = config.yOffset
	amplitude2 = config.amplitude2
	yOffset2 = config.yOffset2
	steps = config.steps
	steps2 = config.steps2
	rads = 2 * 22/7/ numPoints


	for i in range (0,numPoints, steps) :
		angle = (i + config.xIncrementer) * rads
		angle2 = (i+ config.xIncrementer + steps) * rads
		a = (i, math.sin(angle) * amplitude + yOffset)
		b = (i + steps, math.sin(angle) * amplitude + yOffset)
		c = (i + steps, math.sin(angle2) * amplitude + yOffset)

		if c[1] < a[1] :
			b = (i, math.sin(angle2) * amplitude + yOffset)
		config.blockDraw.polygon((a,b,c,a), fill = clr, outline=None)

	phase = round(config.blockWidth/config.phaseFactor)
	for i in range (0,numPoints, steps2) :
		angle = (i - config.speedFactor*config.xIncrementer + phase) * rads
		angle2 = (i - config.speedFactor*config.xIncrementer + phase + steps2) * rads
		a = (i, math.cos(angle) * amplitude2 + yOffset2)
		b = (i + steps2, math.cos(angle) * amplitude2 + yOffset2)
		c = (i + steps2, math.cos(angle2) * amplitude2 + yOffset2)

		if c[1] < a[1] :
			b = (i, math.cos(angle2) * amplitude2 + yOffset2)
		config.blockDraw.polygon((a,b,c,a), fill = clr2, outline=None)


	config.xIncrementer += config.xSpeed
	config.yIncrementer += config.ySpeed

	if config.xIncrementer >= config.blockWidth * 1:
		config.xIncrementer = -0
	if config.yIncrementer >= config.blockHeight -4:
		config.yIncrementer = 0


def redraw(config):
	if config.patternModel == "waves" :
		wavePattern(config)

	if config.patternModel == "reMove" :
		reMove(config)

	if config.patternModel == "diagonalMove" :
		diagonalMove(config)

	if config.patternModel == "randomizer" :
		randomizer(config)

	if config.patternModel == "runningSpiral" :
		runningSpiral(config)

	if config.patternModel == "concentricBoxes" :
		concentricBoxes(config)

	if config.patternModel == "diamond" :
		diamond(config)

	if config.patternModel == "shingles" :
		shingles(config)


def repeatImage(config) :
	cntr = 0
	for r in range(0, config.rows):
		for c in range(0, config.cols):
			if cntr in config.skipBlocks :
				config.canvasDraw.rectangle((c * config.blockWidth, r * config.blockHeight, c * config.blockWidth + config.blockWidth, r * config.blockHeight + config.blockHeight), fill = config.bgColor, outline=config.bgColor)
			else :
				config.canvasImage.paste(config.blockImage, (c * config.blockWidth-c, r * config.blockHeight-r), config.blockImage)

			if cntr == 2 :
				diamond(config)
			if cntr == 22 :
				runningSpiral(config)
			if cntr == 40 :
				reMove(config)

			if cntr == 63 :
				concentricBoxes(config)
			cntr += 1


def runWork():
	global config
	print(bcolors.OKGREEN + "** " + bcolors.BOLD)
	print("Running repeatblocks.py")
	print(bcolors.ENDC)
	while config.isRunning == True:
		iterate()
		time.sleep(config.redrawSpeed)
		if config.standAlone == False :
			config.callBack()
			

def iterate():
	global config
	config.colOverlay.stepTransition()
	config.linecolOverlay.stepTransition()
	config.linecolOverlay2.stepTransition()

	redraw(config)

	repeatImage(config)


	if config.randomizeSpeed == True :

		if random.random() < .03 :
			config.ySpeed = config.ySpeedInit

		if random.random() < .1 :
			config.ySpeed = 0


	if random.random() < .0005 :
		config.triangles = True

	if random.random() < .01 :
		config.triangles = False

	if config.useDrawingPoints == True :
		config.panelDrawing.canvasToUse = config.canvasImage
		config.panelDrawing.render()
	else :
		config.render(config.canvasImage, 0, 0, config.canvasWidth, config.canvasHeight)
	# Done


def getConfigOverlay(tLimitBase,minHue,maxHue,minSaturation,maxSaturation,minValue,maxValue):
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


def main(run=True):
	global config
	config.redrawSpeed = float(workConfig.get("movingpattern", "redrawSpeed"))
	config.blockWidth = int(workConfig.get("movingpattern", "blockWidth"))
	config.blockHeight = int(workConfig.get("movingpattern", "blockHeight"))
	config.rows = int(workConfig.get("movingpattern", "rows"))
	config.cols = int(workConfig.get("movingpattern", "cols"))
	config.lineDiff = int(workConfig.get("movingpattern", "lineDiff"))

	config.bgColorVals = (workConfig.get("movingpattern", "bgColor")).split(",")
	config.bgColor = tuple(
		map(lambda x: int(int(x)), config.bgColorVals)
	)
	config.lineColorVals = (workConfig.get("movingpattern", "lineColor")).split(",")
	config.lineColor = tuple(
		map(lambda x: int(int(x)), config.lineColorVals)
	)

	config.lineColorVals = (workConfig.get("movingpattern", "lineColor")).split(",")
	config.lineColor2 = tuple(
		map(lambda x: int(int(x)), config.lineColorVals)
	)

	tLimitBase = int(workConfig.get("movingpattern", "tLimitBase"))
	minHue = float(workConfig.get("movingpattern", "minHue"))
	maxHue = float(workConfig.get("movingpattern", "maxHue"))
	minSaturation = float(workConfig.get("movingpattern", "minSaturation")	)
	maxSaturation = float(workConfig.get("movingpattern", "maxSaturation"))
	minValue = float(workConfig.get("movingpattern", "minValue"))
	maxValue = float(workConfig.get("movingpattern", "maxValue"))
	config.colOverlay = getConfigOverlay(tLimitBase,minHue,maxHue,minSaturation,maxSaturation,minValue,maxValue)

	tLimitBase = int(workConfig.get("movingpattern", "line_tLimitBase"))
	minHue = float(workConfig.get("movingpattern", "line_minHue"))
	maxHue = float(workConfig.get("movingpattern", "line_maxHue"))
	minSaturation = float(workConfig.get("movingpattern", "line_minSaturation")	)
	maxSaturation = float(workConfig.get("movingpattern", "line_maxSaturation"))
	minValue = float(workConfig.get("movingpattern", "line_minValue"))
	maxValue = float(workConfig.get("movingpattern", "line_maxValue"))
	config.linecolOverlay = getConfigOverlay(tLimitBase,minHue,maxHue,minSaturation,maxSaturation,minValue,maxValue)


	tLimitBase = int(workConfig.get("movingpattern", "line2_tLimitBase"))
	minHue = float(workConfig.get("movingpattern", "line2_minHue"))
	maxHue = float(workConfig.get("movingpattern", "line2_maxHue"))
	minSaturation = float(workConfig.get("movingpattern", "line2_minSaturation")	)
	maxSaturation = float(workConfig.get("movingpattern", "line2_maxSaturation"))
	minValue = float(workConfig.get("movingpattern", "line2_minValue"))
	maxValue = float(workConfig.get("movingpattern", "line2_maxValue"))
	config.linecolOverlay2 = getConfigOverlay(tLimitBase,minHue,maxHue,minSaturation,maxSaturation,minValue,maxValue)

	config.useDoubleLine = (workConfig.getboolean("movingpattern", "useDoubleLine"))

	config.randomizeSpeed = (workConfig.getboolean("movingpattern", "randomizeSpeed"))

	config.patternModel = (workConfig.get("movingpattern", "patternModel"))
	config.steps = int(workConfig.get("movingpattern", "steps"))
	config.steps2 = int(workConfig.get("movingpattern", "steps2"))
	config.amplitude = int(workConfig.get("movingpattern", "amplitude"))
	config.amplitude2 = int(workConfig.get("movingpattern", "amplitude2"))
	config.yOffset = int(workConfig.get("movingpattern", "yOffset"))
	config.yOffset2 = int(workConfig.get("movingpattern", "yOffset2"))

	config.speedFactor = float(workConfig.get("movingpattern", "speedFactor"))
	config.phaseFactor = float(workConfig.get("movingpattern", "phaseFactor"))
	config.xSpeed = float(workConfig.get("movingpattern", "xSpeed"))
	config.ySpeed = float(workConfig.get("movingpattern", "ySpeed"))
	config.ySpeedInit = float(workConfig.get("movingpattern", "ySpeed"))

	skipBlocks = (workConfig.get("movingpattern", "skipBlocks")).split(",")
	config.skipBlocks = tuple(
		map(lambda x: int(int(x)), skipBlocks)
	)
	
	config.diamondUseTriangles = False
	config.diamondStep = int(workConfig.get("movingpattern", "diamondStep"))

	config.numConcentricBoxes = int(workConfig.get("movingpattern", "numConcentricBoxes"))

	config.randomBlockProb = float(workConfig.get("movingpattern", "randomBlockProb"))
	config.randomBlockWidth = int(workConfig.get("movingpattern", "randomBlockWidth"))
	config.randomBlockHeight = int(workConfig.get("movingpattern", "randomBlockHeight"))

	config.repeatProb = .99

	config.xIncrementer = 0
	config.yIncrementer = 0

	config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.canvasDraw = ImageDraw.Draw(config.canvasImage)

	config.blockImage = Image.new("RGBA", (config.blockWidth, config.blockHeight))
	config.blockDraw = ImageDraw.Draw(config.blockImage)

	config.destinationImage = Image.new(
		"RGBA", (config.canvasWidth, config.canvasHeight)
	)

	### THIS IS USED AS WAY TO MOCKUP A CONFIGURATION OF RECTANGULAR PANELS
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
