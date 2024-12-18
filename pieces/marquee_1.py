# ################################################### #
import math
import random
import time
from modules.configuration import bcolors
from modules import coloroverlay, colorutils
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps


def makeMarquee(p, w, h, mw, step=1):
	perimeter = []
	# mw=0
	o = 0
	for i in range(p[1] + 0, p[1] + h + o, step):
		perimeter.append([p[0] + w, i])
	for i in range(p[0] + w, p[0] - o, -step):
		perimeter.append([i, p[1] + h])
	for i in range(p[1] + h, p[1] - o, -step):
		perimeter.append([p[0], i])
	for i in range(p[0] + 0, p[0] + w + round(step / 2), step):
		perimeter.append([i, p[1]])
	return perimeter


def init():
	global config
	config.alphabetLeft = []
	config.alphabetLeft = [a for a in config.alphabet]
	config.guessed = []
	config.found = []
	config.wordNotFound = True
	config.lost = False
	config.done = False
	angle = random.random() * 22 / 7
	config.draw.rectangle(
		(0, 0, config.screenWidth, config.screenHeight), fill=(0, 0, 0, 255)
	)

	config.bgColor = coloroverlay.ColorOverlay()
	config.bgColor.randomRange = (10.0, config.randomRange / 2)
	config.marquees = []

	marqueeWidth = config.marqueeWidth
	w = config.screenWidth - marqueeWidth
	h = config.screenHeight - marqueeWidth
	pattern = [
		1,
		1,
		1,
		1,
		1,
		1,
		1,
		1,
		1,
		1,
		1,
		1,
		1,
		1,
		1,
		1,
		1,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
	]
	if config.step > 2:
		pattern = [
			1,
			1,
			1,
			1,
			1,
			1,
			1,
			1,
			1,
			1,
			1,
			1,
			1,
			0,
			0,
			0,
			0,
			0,
			0,
			0,
			0,
			0,
			0,
			0,
			0,
			0,
		]
	# pattern = [1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0]
	# pattern = [1,1,1,0,0,0]
	p0 = [0, 0]
	innerWidth = w
	innerHeight = h
	gap = config.gap
	step = config.step
	decrement = config.decrement
	mw = marqueeWidth
	mwPrev = marqueeWidth

	for i in range(0, config.marqueeNum):
		clrs = [colorutils.randomColor(), colorutils.getRandomRGB()]
		colOverlayA = coloroverlay.ColorOverlay()
		colOverlayB = coloroverlay.ColorOverlay()

		colOverlayA.randomRange = (10.0, config.randomRange)
		colOverlayB.randomRange = (10.0, config.randomRange)

		# if(i%2 == 0) : mw = mwPrev - decrement

		if i != 0:
			mw = mwPrev - decrement
		if mw <= 2:
			mw = 2

		# print(i, p0, mw, mwPrev, innerWidth, innerHeight)

		if innerWidth < 32 or i > 6:
			step = 1

		config.marquees.append(
			[
				0,
				pattern,
				makeMarquee((p0[0], p0[1]), innerWidth, innerHeight, mw, step),
				mw,
				clrs,
				colOverlayA,
				colOverlayB,
			]
		)

		# print (config.marquees[i][2])

		p0[0] += mw + gap
		p0[1] += mw + gap
		mwPrev = mw

		innerWidth = innerWidth - 2 * (mw) - gap + decrement
		innerHeight = innerHeight - 2 * (mw) - gap + decrement

		if gap > 0:
			innerWidth -= decrement
			innerHeight -= decrement

		if mw == 2:
			innerWidth -= 1
			innerHeight -= 1

		if len(pattern) >= 4 and random.random() > 0.1:
			pattern = pattern[1:]
			pattern = pattern[0 : len(pattern) - 1]


def drawText(xPos=0, yPos=0, messageString="", crossout=False):
	global config
	# Draw the text with "borders"
	indent = int(0.05 * config.tileSize[0])
	for i in range(1, config.shadowSize):
		config.draw.text((indent + -i, -i), messageString, (0, 0, 0), font=config.font)
		config.draw.text((indent + i, i), messageString, (0, 0, 0), font=config.font)

	config.draw.text((xPos, yPos), messageString, config.clr, font=config.font)
	if crossout == True:
		# config.draw.line((xPos, yPos + config.fontSize, xPos + config.fontSize/1.5, yPos - config.fontSize/8), fill=config.clr)
		config.draw.line(
			(
				xPos,
				yPos + config.fontSize / 1.5,
				xPos + config.fontSize / 1.5,
				yPos + config.fontSize / 1.5,
			),
			fill=config.clr,
		)


def drawMarquee():
	global config
	drawText(10, 10, str(config.offset))
	pass


def drawElement():
	global config
	return True


def redraw():
	global config

	bgColor = tuple(int(c) for c in config.bgColor.currentColor)
	config.draw.rectangle((0, 0, config.screenWidth, config.screenHeight), fill=bgColor)
	config.bgColor.stepTransition()

	mcount = 0
	for m in config.marquees:

		offset = m[0]
		pattern = m[1]
		perimeter = m[2]
		marqueeWidth = m[3]
		l = len(pattern)

		patternA = pattern[0 : (l - offset)]
		patternB = pattern[(l - offset) : l]
		pattern = patternB + patternA

		colOverlayA = m[5]
		colOverlayB = m[6]

		clrA = colOverlayA.currentColor
		clrB = colOverlayB.currentColor

		count = 0

		perim = perimeter
		if mcount % 2 > 0:
			perim = reversed(perimeter)

		for p in perim:
			if pattern[count] == 1:
				config.draw.rectangle(
					(p[0], p[1], p[0] + marqueeWidth - 1, p[1] + marqueeWidth - 1),
					outline=None,
					fill=tuple(int(c) for c in clrA),
				)
			else:
				config.draw.rectangle(
					(p[0], p[1], p[0] + marqueeWidth - 1, p[1] + marqueeWidth - 1),
					outline=None,
					fill=tuple(int(c) for c in clrB),
				)
			count += 1
			if count >= len(pattern):
				count = 0

		m[0] += 1
		if m[0] >= len(pattern):
			m[0] = 0
		mcount += 1

		colOverlayA.stepTransition()
		colOverlayB.stepTransition()


def changeColor():
	pass
	return True


def changeCall():
	pass
	return True


def callBack():
	global config
	pass


def runWork():
	global config
	print(bcolors.OKGREEN + "** " + bcolors.BOLD)
	print("Running marquee_1.py")
	print(bcolors.ENDC)
	while True:
		iterate()
		time.sleep(config.redrawSpeed)
		# time.sleep(random.random() * config.redrawSpeed)


def iterate():
	global config
	redraw()
	config.render(config.image, 0, 0, config.screenWidth, config.screenHeight)


def main(run=True):
	global config
	global workConfig
	config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	config.draw = ImageDraw.Draw(config.image)
	config.redrawSpeed = float(workConfig.get("marquee", "redrawSpeed"))
	config.randomRange = float(workConfig.get("marquee", "randomRange"))
	config.fontSize = int(workConfig.get("marquee", "fontSize"))
	config.marqueeWidth = int(workConfig.get("marquee", "marqueeWidth"))
	config.gap = int(workConfig.get("marquee", "gap"))
	config.step = int(workConfig.get("marquee", "step"))
	config.decrement = int(workConfig.get("marquee", "decrement"))
	config.marqueeNum = int(workConfig.get("marquee", "marqueeNum"))
	config.shadowSize = int(workConfig.get("marquee", "shadowSize"))
	config.font = ImageFont.truetype(
		config.path + "/assets/fonts/freefont/FreeSansBold.ttf", config.fontSize
	)
	config.clr = (255, 0, 0)
	config.textPosY = 40
	config.textPosX = 120

	config.clr = colorutils.randomColor(1)
	config.fontSize = int(random.uniform(10, 50))
	config.fontSize = 10
	config.font = ImageFont.truetype(
		config.path + "/assets/fonts/freefont/FreeSansBold.ttf", config.fontSize
	)

	config.alphabet = [
		"a",
		"b",
		"c",
		"d",
		"e",
		"f",
		"g",
		"h",
		"i",
		"j",
		"k",
		"l",
		"m",
		"n",
		"o",
		"p",
		"q",
		"r",
		"s",
		"t",
		"u",
		"v",
		"w",
		"x",
		"y",
		"z",
	]
	config.word = "FEAR"
	colorutils.brightness = float(workConfig.get("displayconfig", "brightness"))
	config.messageString = config.word
	config.xOffset = 15

	init()

	if run:
		runWork()
