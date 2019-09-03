# ################################################### #
import math
import random
import time

from modules import coloroverlay, colorutils
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps


class MarqueeBlock:

	velocity = [0, 0]
	position = [0, 0]

	def __init__(self):
		pass

	def setUp(self):
		pass


class Marquee:

	perimeter = []
	initPoints = [0, 0]
	innerWidth = 100
	innerHeight = 100
	marqueeBlockCount = 10
	gap = 0
	randomRange = 255
	pattern = []
	rightMessUpFactor = 1
	alt = False
	marqueeBlocks = []
	direction = 1

	def __init__(self):
		print("New Marquee")

	def setUp(self):
		self.colOverlayA = coloroverlay.ColorOverlay()
		self.colOverlayB = coloroverlay.ColorOverlay()
		self.colOverlayA.randomRange = (10.0, self.randomRange)
		self.colOverlayB.randomRange = (10.0, self.randomRange)
		self.perimeter = []

		w = self.innerWidth
		h = self.innerHeight

		self.marqueeBlockLength = round(w / self.marqueeBlockCount)

		self.speed = 0.3

		# self.marqueeBlockCount = round(self.innerWidth / self.marqueeWidth)

		# for i in range (self.initPoints[1], self.initPoints[1] + round(h/self.step)) :
		#     self.perimeter.append([self.initPoints[0] + w, i * self.step])

		## adding vert and horizontal velocity

		# RiGHT
		for i in range(0, self.marqueeBlockCount * 2 + 1):
			marqueeBlock = MarqueeBlock()
			marqueeBlock.initPosition = (self.initPoints[0] + w, self.initPoints[1])
			marqueeBlock.velocity = [0, self.speed * self.direction]
			marqueeBlock.position = [
				self.initPoints[0] + w,
				self.initPoints[1] + i * self.marqueeBlockLength,
			]
			marqueeBlock.blockWidth = self.marqueeWidth
			marqueeBlock.blockHeight = self.marqueeBlockLength
			if i % 2 > 0:
				marqueeBlock.clr = self.colOverlayB
			else:
				marqueeBlock.clr = self.colOverlayA

			self.perimeter.append(marqueeBlock)

		# LEFT
		for i in range(0, self.marqueeBlockCount * 2 + 1):
			marqueeBlock = MarqueeBlock()
			marqueeBlock.initPosition = (self.initPoints[0], self.initPoints[1])
			marqueeBlock.velocity = [0, -self.speed * self.direction]
			marqueeBlock.position = [
				self.initPoints[0],
				self.initPoints[1] + i * self.marqueeBlockLength,
			]
			marqueeBlock.blockWidth = self.marqueeWidth
			marqueeBlock.blockHeight = self.marqueeBlockLength
			if i % 2 > 0:
				marqueeBlock.clr = self.colOverlayB
			else:
				marqueeBlock.clr = self.colOverlayA

			self.perimeter.append(marqueeBlock)

		# TOP
		for i in range(0, self.marqueeBlockCount * 2 + 1):
			marqueeBlock = MarqueeBlock()
			marqueeBlock.initPosition = (self.initPoints[0], self.initPoints[1])
			marqueeBlock.position = [
				self.initPoints[0] + i * self.marqueeBlockLength,
				self.initPoints[1],
			]
			marqueeBlock.velocity = [self.speed * self.direction, 0]
			marqueeBlock.blockWidth = self.marqueeBlockLength
			marqueeBlock.blockHeight = self.marqueeWidth
			if i % 2 > 0:
				marqueeBlock.clr = self.colOverlayB
			else:
				marqueeBlock.clr = self.colOverlayA

			self.perimeter.append(marqueeBlock)

		for i in range(0, self.marqueeBlockCount * 2 + 1):
			marqueeBlock = MarqueeBlock()
			marqueeBlock.initPosition = (self.initPoints[0], self.initPoints[1] + h)
			marqueeBlock.position = [
				self.initPoints[0] + i * self.marqueeBlockLength,
				self.initPoints[1] + h,
			]
			marqueeBlock.velocity = [-self.speed * self.direction, 0]
			marqueeBlock.blockWidth = self.marqueeBlockLength
			marqueeBlock.blockHeight = self.marqueeWidth
			if i % 2 > 0:
				marqueeBlock.clr = self.colOverlayB
			else:
				marqueeBlock.clr = self.colOverlayA

			self.perimeter.append(marqueeBlock)


def init():
	global config

	config.draw.rectangle(
		(0, 0, config.screenWidth, config.screenHeight), fill=(0, 0, 0, 255)
	)

	config.bgColor = coloroverlay.ColorOverlay()
	config.bgColor.randomRange = (10.0, config.randomRange / 2)
	config.marquees = []

	marqueeWidth = config.marqueeWidth
	mwPrev = marqueeWidth
	innerWidth = config.screenWidth - marqueeWidth
	innerHeight = config.screenHeight - marqueeWidth
	p0 = [0, 0]

	for i in range(0, config.marqueeNum):
		clrs = [colorutils.randomColor(), colorutils.getRandomRGB()]
		colOverlayA = coloroverlay.ColorOverlay()
		colOverlayB = coloroverlay.ColorOverlay()

		colOverlayA.randomRange = (10.0, config.randomRange)
		colOverlayB.randomRange = (10.0, config.randomRange)

		# if(i%2 == 0) : mw = mwPrev - decrement

		if i != 0:
			marqueeWidth = round(mwPrev - config.decrement)

		if marqueeWidth <= 2:
			marqueeWidth = 2

		if innerWidth < 32 or i > 6:
			config.step = config.step

		marquee = Marquee()
		marquee.offSet = 0
		marquee.config = config
		marquee.initPoints = p0
		marquee.innerWidth = innerWidth
		marquee.innerHeight = innerHeight
		marquee.marqueeWidth = marqueeWidth

		marquee.marqueeBlockCount = 10 - i
		marquee.step = config.step
		marquee.clrs = clrs
		if i % 2 > 0:
			marquee.direction = -1
		marquee.setUp()

		config.marquees.append(marquee)

		## This creates the total points
		p0[0] += marqueeWidth + config.gap
		p0[1] += marqueeWidth + config.gap
		mwPrev = marqueeWidth

		innerWidth = innerWidth - 2 * (marqueeWidth) - config.gap + config.decrement
		innerHeight = innerHeight - 2 * (marqueeWidth) - config.gap + config.decrement

		if config.gap > 0:
			innerWidth -= config.decrement
			innerHeight -= config.decrement

		if marqueeWidth == 2:
			innerWidth -= 1
			innerHeight -= 1


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

		l = len(m.pattern)
		patternA = m.pattern[0 : (l - m.offSet)]
		patternB = m.pattern[(l - m.offSet) : l]
		pattern = patternB + patternA

		perim = m.perimeter

		if mcount % 2 > 0:
			perim = reversed(m.perimeter)

		count = 0
		for p in perim:

			clr = p.clr.currentColor
			x = p.position[0]
			y = p.position[1]
			blockWidth = p.blockWidth
			blockHeight = p.blockHeight

			config.draw.rectangle(
				(x, y, round(x + blockWidth), round(y + blockHeight)),
				outline=None,
				fill=tuple(int(c) for c in clr),
			)

			p.position[0] += p.velocity[0]
			p.position[1] += p.velocity[1]

			if p.position[1] > m.innerHeight + p.blockHeight:
				p.position[1] = p.initPosition[1] - m.marqueeWidth

			if p.position[1] < p.initPosition[1] - p.blockHeight:
				p.position[1] = m.innerHeight

			if p.position[0] > m.innerWidth + p.blockWidth:
				p.position[0] = p.initPosition[0] - m.marqueeWidth

			if p.position[0] < p.initPosition[0]:
				p.position[0] = m.innerWidth  # - p.blockWidth

		p.clr.stepTransition()


def runWork():
	global config
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
	config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	config.draw = ImageDraw.Draw(config.image)
	config.redrawSpeed = float(workConfig.get("marquee", "redrawSpeed"))
	config.randomRange = float(workConfig.get("marquee", "randomRange"))
	config.fontSize = int(workConfig.get("marquee", "fontSize"))
	config.marqueeWidth = int(workConfig.get("marquee", "marqueeWidth"))
	config.gap = int(workConfig.get("marquee", "gap"))
	config.step = float(workConfig.get("marquee", "step"))
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
