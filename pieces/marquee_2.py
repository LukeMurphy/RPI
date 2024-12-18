# ################################################### #
import math
import random
import sys
import time
from modules.configuration import bcolors
from modules import coloroverlay, colorutils
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps


class Marquee:

	pattern = []
	perimeter = []
	clrs = []
	p0 = []

	innerWidth = 0
	innerHeight = 0
	marqueeWidth = 0
	step = 1
	offset = 0

	reverse = False

	# colOverlayA = coloroverlay.ColorOverlay()
	# colOverlayB = coloroverlay.ColorOverlay()

	def __init__(self):
		self.p0 = []
		pass

	def setUp(self):
		pass

	## Creates a series of little boxes -- not efficient but useful if you wanted to make some kind of chasing
	## gradient marquee and better to get animation travel speed down as slow as possible

	def makeMarquee(self):

		o = 0
		self.perimeter = []
		self.stepSize = round(self.marqueeWidth / self.step)
		if self.stepSize == 0:
			self.stepSize = 1
		self.stepSize = 1

		# Right
		for i in range(
			self.p0[1], self.p0[1] + self.innerHeight + self.marqueeWidth, self.stepSize
		):
			self.perimeter.append(
				[self.p0[0] + self.innerWidth, i, self.marqueeWidth, self.stepSize]
			)

		# Bottom
		for i in range(
			self.p0[0] + self.innerWidth - 1, self.p0[0] - 1, -self.stepSize
		):
			self.perimeter.append(
				[i, self.p0[1] + self.innerHeight, self.stepSize, self.marqueeWidth]
			)

		# Left
		for i in range(self.p0[1] + self.innerHeight, self.p0[1], -self.stepSize):
			self.perimeter.append([self.p0[0], i, self.marqueeWidth, self.stepSize])

		# Top
		for i in range(
			self.p0[0], self.p0[0] + self.innerWidth + self.marqueeWidth, self.stepSize
		):
			self.perimeter.append([i, self.p0[1], self.stepSize, self.marqueeWidth])

	def advance(self):
		l = len(self.pattern)

		patternA = self.pattern[0 : (l - self.offset)]
		patternB = self.pattern[(l - self.offset) : l]
		pattern = patternB + patternA

		count = 0

		perim = self.perimeter
		if self.reverse == True:
			perim = reversed(self.perimeter)

		try:
			for p in perim:
				if pattern[count] == 1:
					self.configDraw.rectangle(
						(p[0], p[1], p[0] + p[2], p[1] + p[3]),
						outline=None,
						fill=tuple(round(c) for c in self.colOverlayA.currentColor),
					)
				else:
					self.configDraw.rectangle(
						(p[0], p[1], p[0] + p[2], p[1] + p[3]),
						outline=None,
						fill=tuple(round(c) for c in self.colOverlayB.currentColor),
					)
				count += 1
				if count >= len(pattern):
					count = 0
		except Exception as e:
			print(e)
			print(self.colOverlayA.currentColor, self.colOverlayB.currentColor)
			sys.exit()

		self.offset += 1
		if self.offset >= len(pattern):
			self.offset = 0

		self.colOverlayA.stepTransition()
		self.colOverlayB.stepTransition()


def setTwoColors():
	colOverlayA = coloroverlay.ColorOverlay()
	colOverlayB = coloroverlay.ColorOverlay()

	colOverlayA.minHue = config.palettes[config.usePalette][0]
	colOverlayA.maxHue = config.palettes[config.usePalette][1]
	colOverlayB.minHue = config.palettes[config.usePalette][2]
	colOverlayB.maxHue = config.palettes[config.usePalette][3]

	colOverlayA.randomRange = (config.randomRangeMin, config.randomRangeMax)
	colOverlayB.randomRange = (config.randomRangeMin, config.randomRangeMax)

	colOverlayA.steps = 250
	colOverlayA.tLimit = 25
	colOverlayA.tLimitBase = 25
	colOverlayB.steps = 250
	colOverlayB.tLimit = 20
	colOverlayB.tLimitBase = 20

	colOverlayA.colorTransitionSetup()
	colOverlayB.colorTransitionSetup()

	return (colOverlayA, colOverlayB)


def init():
	global config

	config.draw.rectangle(
		(0, 0, config.screenWidth, config.screenHeight), fill=(0, 0, 0, 255)
	)
	config.bgColor = coloroverlay.ColorOverlay()
	config.bgColor.randomRange = (config.randomRangeMin, config.randomRangeMax)
	config.bgColor.colorTransitionSetup()

	## The pattern controls the dash size - each 1 or 0 represents the width of one small
	## building block for the two-color dash

	# pattern = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	# if(config.step > 2) : pattern = [1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0]
	# pattern = [1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0]
	# pattern = [1,1,1,0,0,0]
	# pattern = [1,0,1,0,0,1,0,0,1,0,1]

	pattern = []
	pattern.extend((1 for i in range(0, config.baseDashSize)))
	pattern.extend((0 for i in range(0, config.baseDashSize)))

	p0 = [config.imageXOffset, config.imageYOffset]
	marqueeWidth = config.marqueeWidth
	innerWidth = config.screenWidth - marqueeWidth
	innerHeight = config.screenHeight - marqueeWidth
	marqueeWidthPrev = marqueeWidth

	step = config.step
	decrement = config.decrement

	config.marquees = []

	unitColors = setTwoColors()

	for i in range(0, config.marqueeNum):

		clrs = [colorutils.randomColor(), colorutils.randomColorAlpha(255, 255)]

		if config.mulitColor == True:
			unitColors = setTwoColors()

		if i != 0:
			marqueeWidth = marqueeWidthPrev - decrement

		if marqueeWidth <= 2:
			marqueeWidth = 2

		if innerWidth < 32 or i > 6:
			step = 1

		mq = Marquee()
		mq.pattern = pattern
		mq.p0 = p0
		mq.innerWidth = innerWidth
		mq.innerHeight = innerHeight
		mq.marqueeWidth = marqueeWidth
		mq.step = step
		mq.clrs = clrs
		mq.colOverlayA = unitColors[0]
		mq.colOverlayB = unitColors[1]
		mq.configDraw = config.draw
		mq.reverse = True if (i % 2 > 0) else False

		mq.makeMarquee()
		config.marquees.append(mq)

		p0[0] += marqueeWidth + config.gap
		p0[1] += marqueeWidth + config.gap
		marqueeWidthPrev = marqueeWidth + 1

		# If this is 1 then offsets the gap...
		eveningGap = 2

		innerWidth = (
			innerWidth - 2 * (marqueeWidth) - config.gap * eveningGap + decrement
		)
		innerHeight = (
			innerHeight - 2 * (marqueeWidth) - config.gap * eveningGap + decrement
		)

		if config.gap > 0:
			innerWidth -= decrement
			innerHeight -= decrement

		if marqueeWidth == 2:
			innerWidth -= 1
			innerHeight -= 1

		if len(pattern) >= 4 and random.random() > 0.1:
			pattern = pattern[1:]
			pattern = pattern[0 : len(pattern) - 1]


def redraw():
	global config

	bgColor = tuple(round(c) for c in config.bgColor.currentColor)

	try:
		config.draw.rectangle(
			(0, 0, config.screenWidth, config.screenHeight), fill=bgColor
		)
		config.bgColor.stepTransition()
	except Exception as e:
		print(e)
		print(bgColor, config.bgColor.currentColor)
		sys.exit()

	mcount = 0
	for mq in config.marquees:
		mq.advance()


def runWork():
	global config
	print(bcolors.OKGREEN + "** " + bcolors.BOLD)
	print("Running marquee_2.py")
	print(bcolors.ENDC)

	while config.isRunning == True:
		iterate()
		time.sleep(config.redrawSpeed)
		if config.standAlone == False :
			config.callBack()


def iterate():
	global config
	redraw()
	config.render(config.image, 0, 0, config.screenWidth, config.screenHeight)

	checkTime()

	if config.marqueeTimerDelta > config.changePaletteInterval:
		if random.random() < 0.5:
			palette = math.floor(random.uniform(0, len(list(config.palettes.keys()))))
			config.usePalette = list(config.palettes.keys())[palette]
			# print("New Palette:{}".format(config.usePalette))
		config.marqueeTimerDelta = 0
		config.marqueeTimer1 = time.time()


def main(run=True):
	global config
	global workConfig
	config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	config.draw = ImageDraw.Draw(config.image)
	config.redrawSpeed = float(workConfig.get("marquee", "redrawSpeed"))
	config.marqueeWidth = int(workConfig.get("marquee", "marqueeWidth"))
	config.baseDashSize = int(workConfig.get("marquee", "baseDashSize"))
	config.gap = int(workConfig.get("marquee", "gap"))
	config.step = int(workConfig.get("marquee", "step"))
	config.changePaletteInterval = int(
		workConfig.get("marquee", "changePaletteInterval")
	)
	config.decrement = int(workConfig.get("marquee", "decrement"))
	config.marqueeNum = int(workConfig.get("marquee", "marqueeNum"))
	try:
		config.randomRangeMin = int(workConfig.get("marquee", "randomRangeMin"))
		config.randomRangeMax = int(workConfig.get("marquee", "randomRangeMax"))
	except Exception as e:
		print(e)
		config.randomRangeMin = 200
		config.randomRangeMax = 400

	try:
		config.mulitColor = workConfig.getboolean("marquee", "mulitColor")
	except Exception as e:
		print(e)
		config.mulitColor = True

	colorutils.brightness = float(workConfig.get("displayconfig", "brightness"))
	config.xOffset = 15

	config.palettes = {
		"all": [0, 360, 0, 360],
		"all2": [0, 180, 180, 360],
		"warm-cool": [0, 40, 140, 180],
		"desert": [0, 40, 40, 80],
		"winter": [180, 200, 200, 240],
		"winter2": [190, 210, 210, 230],
		"wintersun": [30, 50, 180, 240],
	}

	if config.mulitColor == False:
		# Only two colors so the palettes are not really applicable
		config.palettes = {"all": [0, 360, 0, 360], "all2": [0, 180, 180, 360]}

	config.usePalette = list(config.palettes.keys())[1]

	config.marqueeTimerDelta = 0
	config.marqueeTimer1 = time.time()

	init()

	if run:
		runWork()


def checkTime():
	global config
	t = time.time()
	config.marqueeTimerDelta = t - config.marqueeTimer1


#########
