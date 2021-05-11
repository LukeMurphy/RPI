# ################################################### #
import argparse
import math
import random
import time
import types
from modules.configuration import bcolors
from modules import badpixels, coloroverlay, colorutils
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps
import numpy as np


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


def redraw(config):
	reMove(config)


def repeatImage(config) :
	for c in range(0, config.cols):
		for r in range(0, config.rows):
			config.canvasImage.paste(config.blockImage, (c * config.blockWidth, r * config.blockHeight), config.blockImage)


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
	redraw(config)
	repeatImage(config)
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

	config.useDoubleLine = (workConfig.getboolean("movingpattern", "useDoubleLine"))

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




	if run:
		runWork()
