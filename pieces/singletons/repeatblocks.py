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

	config.xIncrementer += 1
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

def repeatImage(config) :
	cntr = 0
	skipBlocks = [ 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
	skipBlocks = [ 200]
	for r in range(0, config.rows):
		for c in range(0, config.cols):
			if cntr in skipBlocks :
				config.canvasDraw.rectangle((c * config.blockWidth, r * config.blockHeight, c * config.blockWidth + config.blockWidth, r * config.blockHeight + config.blockHeight), fill = config.bgColor, outline=config.bgColor)
			else :
				config.canvasImage.paste(config.blockImage, (c * config.blockWidth, r * config.blockHeight), config.blockImage)
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

	if config.useDrawingPoints == True :
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
	config.linecolOverlay2 = getConfigOverlay(tLimitBase,minHue,maxHue,minSaturation,maxSaturation,minValue,maxValue)

	config.useDoubleLine = (workConfig.getboolean("movingpattern", "useDoubleLine"))

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

	#####


	config.tileSizeWidth = int(workConfig.get("displayconfig", "tileSizeWidth"))
	config.tileSizeHeight = int(workConfig.get("displayconfig", "tileSizeHeight"))
	config.panelDrawing = panelDrawing.PanelPathDrawing(config)

	try:
		config.useDrawingPoints = workConfig.getboolean("movingpattern", "useDrawingPoints")
		drawingPathPoints = workConfig.get("movingpattern", "drawingPathPoints").split("|")
		config.panelDrawing.drawingPath = []

		for i in range(0, len(drawingPathPoints)) :
			p = drawingPathPoints[i].split(",")
			config.panelDrawing.drawingPath.append((int(p[0]), int(p[1]), int(p[2])))
	except Exception as e:
		print(str(e))
		config.useDrawingPoints = False


	if run:
		runWork()
