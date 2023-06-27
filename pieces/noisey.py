# ################################################### #
import argparse
import math
import random
import time
import types
import noise
from noise import *
from modules.configuration import bcolors
from modules import badpixels, coloroverlay, colorutils, panelDrawing
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps, ImageFilter 

import numpy as np

lastRate = 0
colorutils.brightness = 1

class WaveDeformer:
    def transform(self, x, y):
        y = y + config.waveAmplitude * math.sin(
            (x + config.waveDeformXPos) / config.wavePeriodMod
        ) * noise.pnoise2(math.sin(x), y / config.pNoiseMod)
        return x, y

    def transform_rectangle(self, x0, y0, x1, y1):
        return (
            *self.transform(x0, y0),
            *self.transform(x0, y1),
            *self.transform(x1, y1),
            *self.transform(x1, y0),
        )

    def getmesh(self, img):
        self.w, self.h = img.size

        target_grid = []
        for x in range(0, self.w, config.wavegridspace):
            for y in range(0, self.h, config.wavegridspace):
                target_grid.append(
                    (x, y, x + config.wavegridspace, y + config.wavegridspace)
                )

        source_grid = [self.transform_rectangle(*rect) for rect in target_grid]

        return [t for t in zip(target_grid, source_grid)]


def getColor(r, g, b, a):
	clr = list(round(i * config.brightness) for i in [r, g, b])
	clr.append(a)

	return tuple(clr)


def reDraw():
	if config.function == "wavey":
		wavey()
	if config.function == "ringLines":
		ringLines()
	if config.function == "ringLinesNoLoop":
		ringLinesNoLoop()
	if config.function == "rings":
		rings()
	if config.function == "waves":
		waves()
	if config.function == "ringScribbles":
		ringScribbles()


def ringLinesNoLoop():
	global config
	config.draw.rectangle((0, 0, 500, 500), fill=config.bgColor)
	config.gDelta = 1 + 1/config.rgbSplitFactor
	config.bDelta = 1 + 1/config.rgbSplitFactor + 1/config.rgbSplitFactor

	config.lastx = [config.xOffset, config.xOffset, config.xOffset]
	config.lasty = [config.yOffset, config.yOffset, config.yOffset]

	config.t2 = time.time()
	tDelta = config.t2-config.t1

	config.scrollAngle += config.scrollRate

	if tDelta >= config.timeToChangeRings:
		# config.scrollAngle = config.scrollRate
		if random.random() < config.changeSizeOfMarkProb:
			# reset it all
			config.scrollAngle = config.scrollRate
			config.markSize = round(random.uniform(0, 2))
			if config.markSize == 0:
				config.brightness = 1.8
				config.redAlpha = config.greenAlpha = config.blueAlpha = 150
			else:
				config.redAlpha = config.redAlphaInit
				config.greenAlpha = config.greenAlphaInit
				config.blueAlpha = config.blueAlphaInit
				config.brightness = config.brightnessInit

		fps = config.frameCount / tDelta
		print("now fps:" + str(fps) + " frameCount: " +
			  str(config.frameCount) + " time-delta: " + str(tDelta))
		config.t1 = config.t2
		config.frameCount = 0
		radius = 300
		config.useFilters = False
		config.draw.ellipse((config.xOffset-radius, config.yOffset-radius, config.xOffset +
							radius, config.yOffset+radius), fill=getColor(250, 250, 250, 255), outline=None)
		if random.random() < .5:
			radius = radius/3
		config.bgColor = colorutils.getRandomColorHSV(config.bg_minHue, config.bg_maxHue, config.bg_minSaturation,
													  config.bg_maxSaturation, config.bg_minValue, config.bg_maxValue, 0, 0, 100, config.brightness)
		bgColor = (config.bgColor[0], config.bgColor[1], config.bgColor[2], 200)
		config.draw.ellipse((config.xOffset-radius, config.yOffset-radius,
							config.xOffset+radius, config.yOffset+radius), fill=bgColor, outline=None)
		if config.timeToChangeRingsProb == 1:
			config.timeToChangeRings = round(random.uniform(1, 32))

	else:
		config.useFilters = True

	renderRingLines()


def ringLines():
	global config
	if config.rendering != "out":
		config.draw.rectangle((0, 0, 500, 500), fill=config.bgColor)
	config.gDelta = 1 + 1/config.rgbSplitFactor
	config.bDelta = 1 + 1/config.rgbSplitFactor + 1/config.rgbSplitFactor

	config.lastx = [config.xOffset, config.xOffset, config.xOffset]
	config.lasty = [config.yOffset, config.yOffset, config.yOffset]

	config.t2 = time.time()
	tDelta = config.t2-config.t1

	config.scrollAngle += config.scrollRate

	if config.scrollAngle >= math.pi * 2:
		config.scrollAngle = config.scrollRate

		fps = config.frameCount / tDelta
		print("now fps:" + str(fps) + " frameCount: " +
			  str(config.frameCount) + " time-delta: " + str(tDelta))
		config.t1 = config.t2
		config.frameCount = 0
		radius = 300

		# config.useFilters = False
		# config.draw.ellipse((config.xOffset-radius,config.yOffset-radius, config.xOffset+radius,config.yOffset+radius), fill=getColor(250,250,250,255), outline=None)
		if random.random() < .5:
			radius = radius/3

		# bgColor = (config.bgColor[0], config.bgColor[1],config.bgColor[2], 200)
		# config.draw.ellipse((config.xOffset-radius,config.yOffset-radius, config.xOffset+radius,config.yOffset+radius), fill=bgColor, outline=None)
	else:
		config.useFilters = True

	renderRingLines()


def renderRingLines():
	config.scrollx = config.radiusVal * math.sin(config.scrollAngle)
	config.scrolly = config.radiusVal * math.cos(config.scrollAngle)
	config.frameCount += 1

	row = 1
	rads = 2 * math.pi / config.numRings
	ra = config.radiusMin * 1 + config.radiusMin
	hMin = config.line_minHue
	hMax = config.line_maxHue
	sMin = config.line_minSaturation
	sMax = config.line_maxSaturation
	vMin = config.line_minValue
	vMax = config.line_maxValue
	dropHueMin = 0
	dropHueMax = 0
	a = 80
	brtns = config.brightness

	for col in range(0, config.numRings):
		x = math.cos(col * rads) * ra + config.xOffset
		# x = col + config.xOffset
		y = math.sin(col * rads) * ra + config.yOffset

		yChange1 = noise.pnoise2(x + config.scrollx, y +
								 config.scrolly) * config.amplitude + row
		yChange2 = noise.pnoise2(
			x + config.scrollx, y + config.scrolly) * config.amplitude/config.gDelta + row
		yChange3 = noise.pnoise2(
			x + config.scrollx, y + config.scrolly) * config.amplitude/config.bDelta + row

		radialFactor = 1
		l1 = math.pi * 1 - config.angle1ForFunnel * math.pi/3
		l2 = math.pi * 1 - config.angle2ForFunnel * math.pi/3
		angle = col * rads
		if angle < l1 and angle > l2:
			radialFactor = config.radialFactor
		xPos = radialFactor * (config.radiusMin + yChange1) * \
							   math.cos(col * rads) * 2 + config.xOffset
		yPos = radialFactor * (config.radiusMin + yChange1) * \
							   math.sin(col * rads) * 2 + config.yOffset

		if col != 0:
			clrToUse = colorutils.getRandomColorHSV(
				hMin, hMax, sMin, sMax, vMin, vMax, dropHueMin, dropHueMax, a, brtns)
			config.draw.line(
				(config.lastx[0], config.lasty[0], xPos, yPos), fill=clrToUse)
		clrToUse2 = colorutils.getRandomColorHSV(
			36, 60, sMin, sMax, vMin, vMax, dropHueMin, dropHueMax, 200, brtns)

		clrToUse2 = (255, 0, 0, config.redAlpha)
		config.draw.rectangle((xPos-config.markSize, yPos-config.markSize,
							  xPos + 0, yPos + 0), fill=clrToUse2, outline=None)

		clrToUse2 = (0, 255, 0, config.greenAlpha)
		xPos = radialFactor * (config.radiusMin + yChange2) * \
							   math.cos(col * rads) * 2 + config.xOffset
		yPos = radialFactor * (config.radiusMin + yChange2) * \
							   math.sin(col * rads) * 2 + config.yOffset
		config.draw.rectangle((xPos-config.markSize, yPos-config.markSize,
							  xPos + 0, yPos + 0), fill=clrToUse2, outline=None)

		clrToUse2 = (0, 0, 255, config.blueAlpha)
		xPos = radialFactor * (config.radiusMin + yChange3) * \
							   math.cos(col * rads) * 2 + config.xOffset
		yPos = radialFactor * (config.radiusMin + yChange3) * \
							   math.sin(col * rads) * 2 + config.yOffset
		config.draw.rectangle((xPos-config.markSize, yPos-config.markSize,
							  xPos + 0, yPos + 0), fill=clrToUse2, outline=None)

		config.lastx = [xPos, xPos, xPos]
		config.lasty = [yPos, yPos, yPos]


def rings():
	global config
	config.draw.rectangle((0, 0, 500, 500), fill=config.bgColor)
	gDelta = 1 + 1/config.rgbSplitFactor
	bDelta = 1 + 1/config.rgbSplitFactor + 1/config.rgbSplitFactor

	for row in range(0, config.numRings):
		points = config.pointsMin + row * config.pointsMin
		rads = 2 * math.pi / points
		ra = config.radiusMin * row + config.radiusMin
		for col in range(0, points):
			x = math.cos(col * rads) * ra + config.xOffset
			y = math.sin(col * rads) * ra + config.yOffset

			yChange1 = noise.pnoise2(x/config.rowFactor, (y + config.scroll) /
									 config.colFactor/1, 1) * config.amplitude + row
			yChange2 = noise.pnoise2(x/config.rowFactor, (y + config.scroll) /
									 config.colFactor/gDelta, 1) * config.amplitude + row
			yChange3 = noise.pnoise2(x/config.rowFactor, (y + config.scroll) /
									 config.colFactor/bDelta, 1) * config.amplitude + row

			if config.drawOptimize == True:
				doDraw = False
			else:
				doDraw = True

			if x > 0 and x < config.canvasWidth-config.xOffset and (y + yChange1) > 0 and (y + yChange1) < config.canvasHeight:
				doDraw = True

			if doDraw == True:
				if config.markSize == 1:
					config.draw.rectangle((x, y + yChange1, x+0, y + yChange1 + 0),
										  fill=getColor(255, 0, 100, 255), outline=None)
					config.draw.rectangle((x, y + yChange2, x+0, y + yChange2 + 0),
										  fill=getColor(0, 255, 0, 255), outline=None)
					config.draw.rectangle((x, y + yChange3, x+0, y + yChange3 + 0),
										  fill=getColor(0, 0, 255, 255), outline=None)
				else:
					config.draw.ellipse((x, y + yChange2, x+config.markSize, y + yChange1 +
										config.markSize), fill=getColor(255, 0, 0, 255), outline=None)
					config.draw.ellipse((x, y + yChange2, x+config.markSize, y + yChange2 +
										config.markSize), fill=getColor(0, 255, 0, 255), outline=None)
					config.draw.ellipse((x, y + yChange3, x+config.markSize, y + yChange3 +
										config.markSize), fill=getColor(0, 0, 255, 255), outline=None)
		# octv += 1
	config.scroll += config.scrollRate


def ringScribbles():

	global config
	config.draw.rectangle((0, 0, 500, 500), fill=config.bgColor)
	config.gDelta = 1 + 1/config.rgbSplitFactor
	config.bDelta = 1 + 1/config.rgbSplitFactor + 1/config.rgbSplitFactor

	config.lastx = [config.xOffset, config.xOffset, config.xOffset]
	config.lasty = [config.yOffset, config.yOffset, config.yOffset]

	config.t2 = time.time()
	tDelta = config.t2-config.t1

	config.scrollAngle += config.scrollRate

	if config.scrollAngle >= math.pi * 2:
		config.scrollAngle = config.scrollRate

		fps = config.frameCount / tDelta
		# print("now fps:" + str(fps) + " frameCount: " + str(config.frameCount) + " time-delta: " + str(tDelta))
		config.t1 = config.t2
		config.frameCount = 0
		radius = 300
		config.useFilters = False
		# config.draw.ellipse((config.xOffset-radius,config.yOffset-radius, config.xOffset+radius,config.yOffset+radius), fill=getColor(250,250,250,255), outline=None)
		if random.random() < .5:
			radius = radius/3

		bgColor = (config.bgColor[0], config.bgColor[1], config.bgColor[2], 200)
		# config.draw.ellipse((config.xOffset-radius,config.yOffset-radius, config.xOffset+radius,config.yOffset+radius), fill=bgColor, outline=None)

		config.lineEcc = random.uniform(config.lineEccMin, config.lineEccMax)
		if config.lineEcc == 0: config.lineEcc = 1
		# if random.random() < .5 : config.lineEcc *= -1

		# config.radiusMin  = random.uniform(config.radiusMinInit,config.radiusMinVar)
		config.angleDecrementBase = random.uniform(0, 3.14)

		# config.angleDecrementRate = random.uniform(-.10,.10)
		if config.radiusMin > config.screenWidth:
			config.angleDecrementRate = -config.screenWidth/config.radiusMin/2
		# config.radialFactor = random.uniform(2,2.2)
		# config.loopIncrease  = random.uniform(-.05,-.2)
		# config.rotationTheta = random.uniform(-math.pi/50,math.pi/50)

		# if (config.angleDecrementBase) < -480 :
		# config.angleDecrementBase = 0

	else:
		config.useFilters = False

	config.scrollx = config.radiusVal * math.sin(config.scrollAngle)
	config.scrolly = config.radiusVal * math.cos(config.scrollAngle)
	config.frameCount += 1

	row = 1
	config.numPointsPerRing = 24
	rads = 2 * math.pi / config.numPointsPerRing
	ra = config.radiusMin * 1 + config.radiusMin

	dropHueMin = 0
	dropHueMax = 0
	a = 80
	brtns = config.brightness
	radialFactor = 1
	radialFactor = config.radialFactor
	radialFactorb = config.radialFactor
	config.lastx = [0, 0, 0]
	config.lasty = [0, 0, 0]

	eRot = math.pi / config.numRings

	rotationTheta = config.rotationTheta

	seed = random.uniform(-.03, .03)
	seed = 0

	loopIncrease = 0
	totalPoints = config.numPointsPerRing * config.numRings

	angleDecrement = config.angleDecrementBase

	for col in range(0, totalPoints):

		x = math.cos(col * rads) * ra + config.xOffset
		# x = col + config.xOffset
		y = math.sin(col * rads) * ra + config.yOffset
		d = round(math.sqrt(x*x + y*y) / 80)
		d = (radialFactorb + radialFactor)/config.lineSizeFactor

		yChange1 = noise.pnoise2(x + config.scrollx, y +
								 config.scrolly) * config.amplitude + loopIncrease
		yChange2 = noise.pnoise2(x + config.scrollx, y + config.scrolly) * \
								 config.amplitude/config.gDelta + loopIncrease
		yChange3 = noise.pnoise2(x + config.scrollx, y + config.scrolly) * \
								 config.amplitude/config.bDelta + loopIncrease

		ns = noise.pnoise2(loopIncrease, 0)
		rotationTheta += ns/config.lineEcc

		l1 = math.pi * 1 - config.angle1ForFunnel * math.pi/3
		l2 = math.pi * 1 - config.angle2ForFunnel * math.pi/3

		'''
		𝑥(𝛼)=𝑅𝑥cos(𝛼)cos(𝜃)−𝑅𝑦sin(𝛼)sin(𝜃)
		𝑦(𝛼)=𝑅𝑥cos(𝛼)sin(𝜃)+𝑅𝑦sin(𝛼)cos(𝜃)
		'''
		Rx = radialFactor * (config.radiusMin + yChange1 + loopIncrease)
		Ry = radialFactorb * (config.radiusMin + yChange1 + loopIncrease)

		# angleDecrement = -config.angleDecrementBase * col/config.numRings * rads
		angleDecrement += config.angleDecrementRate
		# if col < 50 :
		# angleDecrement = 0
		a = col * rads + angleDecrement

		xPos = Rx * math.cos(rotationTheta) * math.cos(a) - Ry * \
							 math.sin(rotationTheta) * math.sin(a) + config.xOffset
		yPos = Ry * math.cos(rotationTheta) * math.sin(a) - Ry * \
							 math.sin(rotationTheta) * math.cos(a) + config.yOffset

		'''
		if col != 0 :
			clrToUse = colorutils.getRandomColorHSV(
				hMin,hMax,sMin,sMax,vMin,vMax,dropHueMin,dropHueMax,a,brtns)
		clrToUse2 = colorutils.getRandomColorHSV(
			36,60,sMin,sMax,vMin,vMax,dropHueMin,dropHueMax,200,brtns)
		'''

		clrToUse2 = (255, 0, 0, config.redAlpha)
		clrToUse2 = colorutils.getRandomColorHSV(config.line_1_minHue, config.line_1_maxHue, config.line_1_minSaturation,
												 config.line_1_maxSaturation, config.line_1_minValue, config.line_1_maxValue, 0, 0, config.redAlpha, brtns)
		config.draw.rectangle((xPos-config.markSize, yPos-config.markSize,
							  xPos + 0, yPos + 0), fill=clrToUse2, outline=None)
		if col != 0:
			config.draw.line(
				(config.lastx[0], config.lasty[0], xPos, yPos), fill=clrToUse2)
			# config.draw.polygon((config.lastx[0],config.lasty[0],config.lastx[0],config.lasty[0]-d,  xPos, yPos-d,  xPos, yPos), fill=clrToUse2)
			# if y > 50 :
			# config.draw.polygon((config.lastx[0],config.lasty[0],config.lastx[0]-d,config.lasty[0],  xPos-d, yPos,  xPos, yPos), fill=clrToUse2)
		config.lastx[0] = (xPos)
		config.lasty[0] = (yPos)

		'''
		clrToUse2 = colorutils.getRandomColorHSV(config.line_2_minHue,config.line_2_maxHue,config.line_2_minSaturation,
												 config.line_2_maxSaturation,config.line_2_minValue,config.line_2_maxValue,0,0,config.greenAlpha,brtns)
		xPos = radialFactor * (config.radiusMin + yChange2) * \
							   math.cos(col * (rads  + config.anlgleOffset)
										) * 2 + config.xOffset
		yPos = radialFactorb * (config.radiusMin + yChange2) * \
								math.sin(col * (rads  + config.anlgleOffset)
										 ) * 2 + config.yOffset

		Rx = radialFactor * (config.radiusMin + yChange2)
		Ry = radialFactorb * (config.radiusMin + yChange2)
		xPos = Rx * math.cos(rotationTheta) * math.cos(a) - Ry * \
							 math.sin(rotationTheta) * math.sin(a) + config.xOffset
		yPos = Ry * math.cos(rotationTheta) * math.sin(a) - Ry * \
							 math.sin(rotationTheta) * math.cos(a)+ config.yOffset

		config.draw.rectangle((xPos-config.markSize,yPos-config.markSize,
							  xPos + 0,yPos + 0 ), fill=clrToUse2, outline=None)
		if col != 0 :
			config.draw.line(
				( config.lastx[1],config.lasty[1] ,xPos,yPos), fill=clrToUse2)
			config.draw.polygon((config.lastx[1],config.lasty[1],config.lastx[1],
								config.lasty[1]-d/2,  xPos, yPos-d/2,  xPos, yPos), fill=clrToUse2)
			if y > 50 :
				config.draw.polygon((config.lastx[1],config.lasty[1],config.lastx[1]- \
									d/2,config.lasty[1],  xPos-d/2, yPos,  xPos, yPos), fill=clrToUse2)
		config.lastx[1] = (xPos)
		config.lasty[1] = (yPos)

		clrToUse2 = colorutils.getRandomColorHSV(config.line_3_minHue,config.line_3_maxHue,config.line_3_minSaturation,
												 config.line_3_maxSaturation,config.line_3_minValue,config.line_3_maxValue,0,0,config.blueAlpha,brtns)
		xPos = radialFactor * (config.radiusMin + yChange3) * \
							   math.cos(col * (rads  + config.anlgleOffset)
										) * 2 + config.xOffset
		yPos = radialFactorb * (config.radiusMin + yChange3) * \
								math.sin(col * (rads  + config.anlgleOffset)
										 ) * 2 + config.yOffset
		Rx = radialFactor * (config.radiusMin + yChange3)
		Ry = radialFactorb * (config.radiusMin + yChange3)
		xPos = Rx * math.cos(rotationTheta) * math.cos(a) - Ry * \
							 math.sin(rotationTheta) * math.sin(a) + config.xOffset
		yPos = Ry * math.cos(rotationTheta) * math.sin(a) - Ry * \
							 math.sin(rotationTheta) * math.cos(a)+ config.yOffset
		config.draw.rectangle((xPos-config.markSize,yPos-config.markSize,
							  xPos + 0,yPos + 0 ), fill=clrToUse2, outline=None)
		if col != 0 :
			config.draw.line(
				(xPos,yPos, config.lastx[2],config.lasty[2] ), fill=clrToUse2)
			config.draw.polygon((config.lastx[2],config.lasty[2],config.lastx[2],
								config.lasty[2]-d/4,  xPos, yPos-d/4,  xPos, yPos), fill=clrToUse2)
			if y > 50 :
				config.draw.polygon((config.lastx[2],config.lasty[2],config.lastx[2]- \
									d/4,config.lasty[2],  xPos-d/4, yPos,  xPos, yPos), fill=clrToUse2)

		config.lastx[2] = (xPos)
		config.lasty[2] = (yPos)
		'''
		radialFactor += config.rIncrease
		radialFactorb += config.raIncrease
		# row += config.loopIncrease
		loopIncrease += config.loopIncrease


def wavey():
	global config
	config.draw.rectangle((0, 0, 500, 500), fill=config.bgColor)
	octv = 1
	lastx = [0, 0, 0]
	for col in range(0, config.canvasWidth*1, 2):
		lasty = [0, 0, 0]
		for row in range(0, config.canvasHeight, 8):
			y = row
			x = round(noise.pnoise2((col + config.scroll)/config.colFactor /
					  3, (y)/config.rowFactor/1, 1) * config.amplitude + col)

			r = round(math.sin((y/config.colFactor)+.1) * 200)
			g = round(math.sin((col/config.rowFactor)+.1) * 100)
			# g = round(math.sin((x/config.rowFactor)+.1) * 200)
			b = round(math.sin((x/config.rowFactor)+.1) * 100)
			# config.draw.rectangle((x, y, x+1, y+1), fill=(r,g,b,150))
			if col != 0:
				config.draw.line((lastx[0], lasty[0], x, y), fill=getColor(r, g, b, 150))
			lastx = [x, x, x]
			lasty = [y, y, y]
		# octv += 1
	config.scroll += config.scrollRate


def waves():
	global config
	config.draw.rectangle(
		(0, 0, config.canvasWidth, config.canvasHeight), fill=config.bgColor)
	octv = 4
	lastx = [0, 0, 0]
	lasty = [0, 0, 0]
	rowRads = 2*math.pi / config.waveLines
	count = 0
	countIncr = 1
	for row in range(0, config.waveLines):
		r = 10
		g = 120
		b = 250
		r = config.lineColors[count][0]
		g = config.lineColors[count][1]
		b = config.lineColors[count][2]

		# if random.random() < .95 :
		# 	r = config.lineColors[count][0]
		# 	g = config.lineColors[count][1]
		# 	b = config.lineColors[count][2]
		# else :
		# 	r = config.assignedLineColors[row][0]
		# 	g = config.assignedLineColors[row][1]
		# 	b = config.assignedLineColors[row][2]

		count += countIncr

		if count >= len(config.lineColors):
			count = 0
			# countIncr = 0

		# alpha = round(255 * abs(math.sin(rowRads * row)))
		# alpha = round(255 * config.waveLines / (5 * row + 1) )
		alpha = 255

		for col in range(0, config.canvasWidth+config.colInterval, config.colInterval):
			x = col
			# moving
			# y = noise.pnoise2(row/config.rowFactor, (col + config.scroll)/config.colFactor, octv) * config.amplitude + 100

			# standing + moving - low scrollrate
			y = noise.pnoise2(
				(row + config.scroll)/config.rowFactor,
				(col + config.travel)/config.colFactor,
				octv,
				.0,
				.0
				) * config.amplitude + config.yOffset + config.lineFactor * (col/20+row)

			# r = 255
			# g = round(math.cos((col/config.rowFactor)+.1) * 200)
			# b = 50

			# config.draw.rectangle((x, y, x+1, y+1), fill=(r,g,b,150))
			if col != 0:
				config.draw.line((lastx[0], lasty[0], x, y), fill=getColor(r, g, b, alpha))
			lastx = [x, x, x]
			lasty = [y, y, y]
		# octv += 1
	config.scroll += config.scrollRate
	config.travel += config.travelRate


def runWork():
	global config
	print(bcolors.OKGREEN + "** " + bcolors.BOLD)
	print("Running noisescroller.py")
	print(bcolors.ENDC)

	config.draw.rectangle(
		(0, 0, config.canvasWidth, config.canvasHeight), fill=config.bgColor)

	while config.isRunning == True:
		iterate()
		time.sleep(config.redrawSpeed)
		if config.standAlone == False:
			config.callBack()


def iterate():

	if random.random() < config.amplitudeChangeProb:
		config.amplitude = random.uniform(config.amplitudeMin, config.amplitudeMax)
	reDraw()

	########### RENDERING AS A MOCKUP OR AS REAL ###########
	if config.useDrawingPoints == True:
		config.panelDrawing.canvasToUse = config.image
		config.panelDrawing.render()
	else:
		if config.useWaveDistortion == True :
			config.waveDeformXPos += config.waveDeformXPosRate
			tempImage  =  config.image.filter(ImageFilter.GaussianBlur(radius=.75))
			config.workImage = ImageOps.deform(tempImage, WaveDeformer())
			tempImage = config.workImage.filter(ImageFilter.SHARPEN())
			config.render(tempImage, 0, 0)
			# config.render(config.workImage, 0, 0)
		else :
			config.render(config.image, 0, 0, config.canvasWidth, config.canvasHeight)
	# Done


def main(run=True):
	global config
	global workConfig
	config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.canvasImage = Image.new(
		"RGBA", (config.canvasWidth, config.canvasHeight))
	config.draw = ImageDraw.Draw(config.image)

	config.redrawSpeed = float(workConfig.get("noisescroller", "redrawSpeed"))
	config.amplitude = float(workConfig.get("noisescroller", "amplitude"))
	config.rowFactor = float(workConfig.get("noisescroller", "rowFactor"))
	config.colFactor = float(workConfig.get("noisescroller", "colFactor"))
	config.rgbSplitFactor = float(
		workConfig.get("noisescroller", "rgbSplitFactor"))

	config.numRings = int(workConfig.get("noisescroller", "numRings"))
	config.pointsMin = int(workConfig.get("noisescroller", "pointsMin"))
	config.xOffset = int(workConfig.get("noisescroller", "xOffset"))
	config.yOffset = int(workConfig.get("noisescroller", "yOffset"))
	config.radiusMin = float(workConfig.get("noisescroller", "radiusMin"))
	config.markSize = int(workConfig.get("noisescroller", "markSize"))
	config.scroll = 0
	config.travel = 0

	config.function = (workConfig.get("noisescroller", "function"))

	config.bgColorVals = (workConfig.get("noisescroller", "bgColor")).split(",")
	config.bgColor = tuple(
		map(lambda x: round(float(x) * config.brightness), config.bgColorVals))

	config.scrollRate = float(workConfig.get("noisescroller", "scrollRate"))

	try:
		config.lineFactor = float(workConfig.get("noisescroller", "lineFactor"))
	except Exception as e:
		print(str(e))
		config.lineFactor = 1

	try:
		config.colInterval = int(workConfig.get("noisescroller", "colInterval"))
	except Exception as e:
		print(str(e))
		config.colInterval = 1

	try:
		config.waveLines = int(workConfig.get("noisescroller", "waveLines"))
	except Exception as e:
		print(str(e))
		config.waveLines = 10

	try:
		config.travelRate = float(workConfig.get("noisescroller", "travelRate"))
	except Exception as e:
		print(str(e))
		config.travelRate = 0.0

	try:
		config.amplitudeChangeProb = float(
			workConfig.get("noisescroller", "amplitudeChangeProb"))
		config.amplitudeMin = float(workConfig.get("noisescroller", "amplitudeMin"))
		config.amplitudeMax = float(workConfig.get("noisescroller", "amplitudeMax"))
	except Exception as e:
		print(str(e))
		config.amplitudeChangeProb = 0.0
		config.amplitudeMin = 0.0
		config.amplitudeMax = 0.0

	if config.function == "ringLines" or config.function == 'ringLinesNoLoop' or config.function == 'ringScribbles':
		config.frames = int(workConfig.get("noisescroller", "frames"))
		config.radiusVal = int(workConfig.get("noisescroller", "radiusVal"))
		config.radialFactor = float(workConfig.get("noisescroller", "radialFactor"))
		config.animationDuration = int(workConfig.get(
			"noisescroller", "animationDuration"))
		config.scrollRate = 2 * math.pi / config.frames
		config.frameCount = 0
		config.animationRev = 0
		config.scrollAngle = 0
		config.t1 = time.time()
		config.t2 = time.time()

		try:
			config.line_minHue = float(workConfig.get("noisescroller", "line_minHue"))
			config.line_maxHue = float(workConfig.get("noisescroller", "line_maxHue"))
			config.line_maxSaturation = float(
				workConfig.get("noisescroller", "line_maxSaturation"))
			config.line_minSaturation = float(
				workConfig.get("noisescroller", "line_minSaturation"))
			config.line_maxValue = float(
				workConfig.get("noisescroller", "line_maxValue"))
			config.line_minValue = float(
				workConfig.get("noisescroller", "line_minValue"))
		except Exception as e:
			print(str(e))

			config.line_1_minHue = float(
				workConfig.get("noisescroller", "line_1_minHue"))
			config.line_1_maxHue = float(
				workConfig.get("noisescroller", "line_1_maxHue"))
			config.line_1_maxSaturation = float(
				workConfig.get("noisescroller", "line_1_maxSaturation"))
			config.line_1_minSaturation = float(
				workConfig.get("noisescroller", "line_1_minSaturation"))
			config.line_1_maxValue = float(
				workConfig.get("noisescroller", "line_1_maxValue"))
			config.line_1_minValue = float(
				workConfig.get("noisescroller", "line_1_minValue"))

			config.line_2_minHue = float(
				workConfig.get("noisescroller", "line_2_minHue"))
			config.line_2_maxHue = float(
				workConfig.get("noisescroller", "line_2_maxHue"))
			config.line_2_maxSaturation = float(
				workConfig.get("noisescroller", "line_2_maxSaturation"))
			config.line_2_minSaturation = float(
				workConfig.get("noisescroller", "line_2_minSaturation"))
			config.line_2_maxValue = float(
				workConfig.get("noisescroller", "line_2_maxValue"))
			config.line_2_minValue = float(
				workConfig.get("noisescroller", "line_2_minValue"))

			config.line_3_minHue = float(
				workConfig.get("noisescroller", "line_3_minHue"))
			config.line_3_maxHue = float(
				workConfig.get("noisescroller", "line_3_maxHue"))
			config.line_3_maxSaturation = float(
				workConfig.get("noisescroller", "line_3_maxSaturation"))
			config.line_3_minSaturation = float(
				workConfig.get("noisescroller", "line_3_minSaturation"))
			config.line_3_maxValue = float(
				workConfig.get("noisescroller", "line_3_maxValue"))
			config.line_3_minValue = float(
				workConfig.get("noisescroller", "line_3_minValue"))

		config.bg_minHue = float(workConfig.get("noisescroller", "bg_minHue"))
		config.bg_maxHue = float(workConfig.get("noisescroller", "bg_maxHue"))
		config.bg_maxSaturation = float(
			workConfig.get("noisescroller", "bg_maxSaturation"))
		config.bg_minSaturation = float(
			workConfig.get("noisescroller", "bg_minSaturation"))
		config.bg_maxValue = float(workConfig.get("noisescroller", "bg_maxValue"))
		config.bg_minValue = float(workConfig.get("noisescroller", "bg_minValue"))

		config.angle1ForFunnel = float(
			workConfig.get("noisescroller", "angle1ForFunnel"))
		config.angle2ForFunnel = float(
			workConfig.get("noisescroller", "angle2ForFunnel"))

		try:
			config.bg_alpha = int(workConfig.get("noisescroller", "bg_alpha"))
		except Exception as e:
			print(str(e))
			config.bg_alpha = 100
		try:
			config.anlgleOffset = float(workConfig.get("noisescroller", "anlgleOffset"))
			config.rIncrease = float(workConfig.get("noisescroller", "rIncrease"))
			config.raIncrease = float(workConfig.get("noisescroller", "raIncrease"))
			config.loopIncrease = float(workConfig.get("noisescroller", "loopIncrease"))
			config.lineSizeFactor = float(
				workConfig.get("noisescroller", "lineSizeFactor"))
			config.lineEcc = float(workConfig.get("noisescroller", "lineEcc"))
			config.angleDecrementRate = float(
				workConfig.get("noisescroller", "angleDecrementRate"))
			config.radiusMinInit = float(workConfig.get("noisescroller", "radiusMin"))
			config.radiusMinVar = float(workConfig.get("noisescroller", "radiusMinVar"))
			config.lineEccMin = float(workConfig.get("noisescroller", "lineEccMin"))
			config.lineEccMax = float(workConfig.get("noisescroller", "lineEccMax"))
			config.rotationTheta = float(
				workConfig.get("noisescroller", "rotationTheta"))
			config.angleDecrementBase = float(
				workConfig.get("noisescroller", "angleDecrementBase"))

		except Exception as e:
			print(str(e))
			config.anlgleOffset = 0
			config.rIncrease = 0
			config.raIncrease = 0
			config.loopIncrease = 0

		config.bgColor = colorutils.getRandomColorHSV(config.bg_minHue, config.bg_maxHue, config.bg_minSaturation,
													  config.bg_maxSaturation, config.bg_minValue, config.bg_maxValue, 0, 0, config.bg_alpha, config.brightness)

		config.timeToChangeRings = int(workConfig.get(
			"noisescroller", "timeToChangeRings"))
		config.timeToChangeRingsProb = 0
		if config.timeToChangeRings == -1:
			config.timeToChangeRingsProb = 1
			config.timeToChangeRings = round(random.uniform(1, 32))
		config.changeSizeOfMarkProb = float(
			workConfig.get("noisescroller", "changeSizeOfMarkProb"))

		config.redAlpha = int(workConfig.get("noisescroller", "redAlpha"))
		config.greenAlpha = int(workConfig.get("noisescroller", "greenAlpha"))
		config.blueAlpha = int(workConfig.get("noisescroller", "blueAlpha"))
		config.redAlphaInit = int(workConfig.get("noisescroller", "redAlpha"))
		config.greenAlphaInit = int(workConfig.get("noisescroller", "greenAlpha"))
		config.blueAlphaInit = int(workConfig.get("noisescroller", "blueAlpha"))
		config.brightnessInit = config.brightness

		# octv += 1

	try:
		lineColors = workConfig.get("noisescroller", "lineColors").split("|")
		config.lineColors = []
		for c in lineColors:
			cArray = c.split(",")
			config.lineColors.append(
				tuple(map(lambda x: round(float(x) * config.brightness), cArray)))

	except Exception as e:
		print(str(e))
		config.lineColors = [(100, 220, 255), (100, 220, 255),
							  (100, 220, 255), (10, 120, 255), (100, 90, 90)]

	config.assignedLineColors = []
	for row in range(0, config.waveLines):
		choice = math.floor(random.uniform(0, len(config.lineColors)))
		if random.random() < .001:
			r = round(random.uniform(0, 255))
			g = round(random.uniform(0, 255))
			b = round(random.uniform(0, 255))
			config.assignedLineColors.append((r, g, b))
		else:
			config.assignedLineColors.append(config.lineColors[choice])


	try:
		config.useWaveDistortion = workConfig.getboolean(
			"noisescroller", "useWaveDistortion"
		)
		config.waveAmplitude = float(workConfig.get("noisescroller", "waveAmplitude"))
		config.wavePeriodMod = float(workConfig.get("noisescroller", "wavePeriodMod"))
		config.wavegridspace = int(workConfig.get("noisescroller", "wavegridspace"))
		config.pNoiseMod = float(workConfig.get("noisescroller", "pNoiseMod"))
		config.waveDeformXPosRate = float(workConfig.get("noisescroller", "waveDeformXPosRate"))
		config.waveDeformXPos = 0
	except Exception as e:
		print(str(e))
		config.useWaveDistortion = False

	try:
		config.drawOptimize = workConfig.getboolean("noisescroller", "drawOptimize")
	except Exception as e:
		print(str(e))
		config.drawOptimize = False

	### THIS IS USED AS WAY TO MOCKUP A CONFIGURATION OF RECTANGULAR PANELS
	panelDrawing.mockupBlock(config, workConfig)
	#### Need to add something like this at final render call  as well
	''' 
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
