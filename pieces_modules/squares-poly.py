import math
import random
import textwrap
import time

from modules import badpixels, coloroverlay, colorutils
from modules.quilting import createpolysquarepieces
from modules.quilting.colorset import ColorSet
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFont, ImageOps

"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def transformImage(img):
	width, height = img.size
	m = -0.5
	xshift = abs(m) * 420
	new_width = width + int(round(xshift))

	img = img.transform(
		(new_width, height), Image.AFFINE, (1, m, 0, 0, 1, 0), Image.BICUBIC
	)
	img = img.transform(
		(new_width, height), Image.PERSPECTIVE, config.transformTuples, Image.BICUBIC
	)
	return img


# this could be written to use A as the starting point
# for b's range - but this way it makes for some more
# mixed up results
def randomRange(A=0, B=1, rounding=False):
	a = random.uniform(A, B)
	b = random.uniform(A, B)
	if rounding == False:
		return (a, b)
	else:
		return (round(a), round(b))


def restartPiece(config):
	config.t1 = time.time()
	config.t2 = time.time()


	'''

	## The top / base diamond / square
	c1Range = round(random.uniform(0, 120))
	config.c1HueRange = (c1Range, c1Range + 240)
	config.c1SaturationRange = randomRange(0.4, 0.95)

	vRange = random.uniform(0.2, 0.9)
	config.c1ValueRange = randomRange(vRange, vRange + 0.1)

	# the "Shaded" side
	c2Range = round(random.uniform(0, 140))
	config.c2HueRange = (c2Range, c2Range + 220)
	config.c2SaturationRange = randomRange(0.4, 1)
	config.c2ValueRange = randomRange(0.1, 0.5)

	## The "bright side"
	config.c3HueRange = config.c2HueRange
	config.c3SaturationRange = randomRange(0.4, 0.999)
	config.c3ValueRange = randomRange(0.5, 1)

	'''

	config.fillColorSet = []
	config.fillColorSet.append(
		ColorSet(config.c1HueRange, config.c1SaturationRange, config.c1ValueRange)
	)
	config.fillColorSet.append(
		ColorSet(config.c2HueRange, config.c2SaturationRange, config.c2ValueRange)
	)
	config.fillColorSet.append(
		ColorSet(config.c3HueRange, config.c3SaturationRange, config.c3ValueRange)
	)

	if random.random() < config.resetSizeProbability:
		config.rotation = random.uniform(-config.rotationRange, config.rotationRange)
		config.doingRefresh = 0
		config.doingRefreshCount = 100

	if random.random() < config.resetSizeProbability / 8:
		config.lines = True
	else:
		config.lines = False

	# a lame attempt at "optimizing" the number or rows and cols that are drawn
	# based on the size of the blocks ... ;[

	if random.random() < config.resetSizeProbability:
		config.blockSize = round(
			random.uniform(config.blockSizeMin, config.blockSizeMax)
		)

		if config.blockSize <= 11:
			config.blockCols = config.blockColsMax
			config.blockRows = config.blockRowsMax
		else:
			config.blockCols = config.blockColsMin
			config.blockRows = config.blockRowsMin

		# print(config.blockSize, config.blockCols, config.blockRows)

		config.blockLength = config.blockSize
		config.blockHeight = config.blockSize
		config.doingRefresh = 0
		config.doingRefreshCount = 100
		createpolysquarepieces.createPieces(config, True)

	# poly specific
	if random.random() < config.resetSizeProbability:
		if config.randomness != 0:
			config.randomness = random.uniform(
				config.minRandomness, config.maxRandomness
			)

		# initialize crossfade - in this case 100 steps ...
		config.doingRefresh = 0
		config.doingRefreshCount = 100

	createpolysquarepieces.refreshPalette(config)
	setInitialColors(config, True)


def setInitialColors(config, refresh=False):
	## Better initial color when piece is turned on
	for i in range(0, len(config.unitArray)):
		obj = config.unitArray[i]
		for c in range(0, len(obj.polys)):
			colOverlay = obj.polys[c][1]
			colOverlay.colorB = colorutils.randomColor(config.brightness * 0.8)
			colOverlay.colorA = colorutils.randomColor(config.brightness * 0.8)
			colOverlay.colorTransitionSetup()
			colOverlay.colorTransitionSetupValues()


def main(config, workConfig, run=True):

	print("---------------------")
	print("POLYS Loaded")

	config.brightness = float(workConfig.get("displayconfig", "brightness"))
	colorutils.brightness = config.brightness
	config.canvasImageWidth = config.screenWidth
	config.canvasImageHeight = config.screenHeight
	config.canvasImageWidth -= 4
	config.canvasImageHeight -= 4

	config.outlineColorObj = coloroverlay.ColorOverlay()
	config.outlineColorObj.randomRange = (5.0, 30.0)
	config.outlineColorObj.colorTransitionSetup()

	config.quiltPattern = workConfig.get("quilt", "pattern")

	# these control the timing of the individual color transitions - longer is slower
	config.transitionStepsMin = float(workConfig.get("quilt", "transitionStepsMin"))
	config.transitionStepsMax = float(workConfig.get("quilt", "transitionStepsMax"))

	# Some triangles will re-draw like a tick - on triangles quilt
	config.resetTrianglesProb = float(workConfig.get("quilt", "resetTrianglesProb"))

	# The probability that at the beginning of a new quilt image the size of the
	# elements will change
	config.resetSizeProbability = float(workConfig.get("quilt", "resetSizeProbability"))

	# the time in seconds given before the quilt image resets to new parameters
	config.timeToComplete = int(workConfig.get("quilt", "timeToComplete"))

	config.transformShape = workConfig.getboolean("quilt", "transformShape")
	transformTuples = workConfig.get("quilt", "transformTuples").split(",")
	config.transformTuples = tuple([float(i) for i in transformTuples])

	redRange = workConfig.get("quilt", "redRange").split(",")
	config.redRange = tuple([int(i) for i in redRange])

	# the mins and maxes for the size of the units
	config.gapSize = int(workConfig.get("quilt", "gapSize"))
	config.blockSizeMin = int(workConfig.get("quilt", "blockSizeMin"))
	config.blockSizeMax = int(workConfig.get("quilt", "blockSizeMax"))
	config.blockSize = round(random.uniform(config.blockSizeMin, config.blockSizeMax))

	config.blockRowsMin = int(workConfig.get("quilt", "blockRowsMin"))
	config.blockRowsMax = int(workConfig.get("quilt", "blockRowsMax"))
	config.blockColsMin = int(workConfig.get("quilt", "blockColsMin"))
	config.blockColsMax = int(workConfig.get("quilt", "blockColsMax"))

	# the amount to reduce the "vertical" blocks: allowable values are 1-5
	config.elongation = int(workConfig.get("quilt", "elongation"))
	config.blockCols = config.blockColsMax
	config.blockRows = config.blockRowsMax

	# can adjust the quilt image offset
	config.cntrOffsetX = int(workConfig.get("quilt", "cntrOffsetX"))
	config.cntrOffsetY = int(workConfig.get("quilt", "cntrOffsetY"))

	# frame rate
	config.delay = float(workConfig.get("quilt", "delay"))

	# the probabilty that any triangle will pop to another color
	config.colorPopProb = float(workConfig.get("quilt", "colorPopProb"))

	config.brightnessFactorDark = float(workConfig.get("quilt", "brightnessFactorDark"))
	config.brightnessFactorLight = float(
		workConfig.get("quilt", "brightnessFactorLight")
	)
	config.lines = workConfig.getboolean("quilt", "lines")
	config.patternPrecision = workConfig.getboolean("quilt", "patternPrecision")

	config.activeSet = workConfig.get("quilt", "activeSet")

	config.c1HueRange = tuple(
		[float(i) for i in workConfig.get(config.activeSet, "c1HueRange").split(",")]
	)
	config.c1SaturationRange = tuple(
		[
			float(i)
			for i in workConfig.get(config.activeSet, "c1SaturationRange").split(",")
		]
	)
	config.c1ValueRange = tuple(
		[float(i) for i in workConfig.get(config.activeSet, "c1ValueRange").split(",")]
	)

	config.c2HueRange = tuple(
		[float(i) for i in workConfig.get(config.activeSet, "c2HueRange").split(",")]
	)
	config.c2SaturationRange = tuple(
		[
			float(i)
			for i in workConfig.get(config.activeSet, "c2SaturationRange").split(",")
		]
	)
	config.c2ValueRange = tuple(
		[float(i) for i in workConfig.get(config.activeSet, "c2ValueRange").split(",")]
	)

	config.c3HueRange = tuple(
		[float(i) for i in workConfig.get(config.activeSet, "c3HueRange").split(",")]
	)
	config.c3SaturationRange = tuple(
		[
			float(i)
			for i in workConfig.get(config.activeSet, "c3SaturationRange").split(",")
		]
	)
	config.c3ValueRange = tuple(
		[float(i) for i in workConfig.get(config.activeSet, "c3ValueRange").split(",")]
	)

	# for now, all squares
	config.blockLength = config.blockSize
	config.blockHeight = config.blockSize

	if config.blockSize <= 11:
		config.blockCols = config.blockColsMax
		config.blockRows = config.blockRowsMax
	else:
		config.blockCols = config.blockColsMin
		config.blockRows = config.blockRowsMin

	# print(config.blockSize, config.blockCols, config.blockRows)

	config.canvasImage = Image.new(
		"RGBA", (config.canvasImageWidth, config.canvasImageHeight)
	)

	config.unitArray = []

	config.fillColorSet = []
	config.fillColorSet.append(
		ColorSet(config.c1HueRange, config.c1SaturationRange, config.c1ValueRange)
	)
	config.fillColorSet.append(
		ColorSet(config.c2HueRange, config.c2SaturationRange, config.c2ValueRange)
	)
	config.fillColorSet.append(
		ColorSet(config.c3HueRange, config.c3SaturationRange, config.c3ValueRange)
	)

	config.randomness = 0
	config.minRandomness = 0
	config.maxRandomness = 0

	try:
		config.rotationRange = float(workConfig.get("quilt", "rotationRange"))
	except Exception as e:
		config.rotationRange = 0
		print(e)

	try:
		config.randomness = int(workConfig.get("quilt", "randomness"))
		try:
			config.maxRandomness = int(workConfig.get("quilt", "maxRandomness"))
		except Exception as e:
			config.maxRandomness = config.randomness
			print(e)
	except Exception as e:
		print(e)

	try:
		config.minRandomness = int(workConfig.get("quilt", "minRandomness"))
	except Exception as e:
		config.minRandomness = 0
		print(e)

	## Draws a single colored block ....
	try:
		drawBlockCoordsRaw = list(
			list((i).split(","))
			for i in workConfig.get("drawBlock", "drawBlockCoords").split("|")
		)
		config.drawBlockCoords = []

		for i in drawBlockCoordsRaw:
			coords = tuple(int(ii) for ii in i)
			config.drawBlockCoords.append(coords)
		config.drawBlockCoords = tuple(config.drawBlockCoords)

		config.drawBlockFixedColor = tuple(
			[
				int(i)
				for i in workConfig.get("drawBlock", "drawBlockFixedColor").split(",")
			]
		)
		config.drawBlock_c1HueRange = tuple(
			[float(i) for i in workConfig.get("drawBlock", "c1HueRange").split(",")]
		)
		config.drawBlock_c1SaturationRange = tuple(
			[
				float(i)
				for i in workConfig.get("drawBlock", "c1SaturationRange").split(",")
			]
		)
		config.drawBlock_c1ValueRange = tuple(
			[float(i) for i in workConfig.get("drawBlock", "c1ValueRange").split(",")]
		)
		config.drawBlockColor = coloroverlay.ColorOverlay(False)
		config.drawBlockColor.minHue = config.drawBlock_c1HueRange[0]
		config.drawBlockColor.maxHue = config.drawBlock_c1HueRange[1]
		config.drawBlockColor.minSaturation = config.drawBlock_c1SaturationRange[0]
		config.drawBlockColor.maxSaturation = config.drawBlock_c1SaturationRange[1]
		config.drawBlockColor.minValue = config.drawBlock_c1ValueRange[0]
		config.drawBlockColor.maxValue = config.drawBlock_c1ValueRange[1]
		config.drawBlockColor.colorTransitionSetup()
		config.drawBlockColor.stepTransition()
		config.canvasImageDraw = ImageDraw.Draw(config.canvasImage)
		config.drawBlock = True
		f1 = lambda: config.canvasImageDraw.polygon(
			config.drawBlockCoords,
			fill=tuple(x for x in config.drawBlockColor.currentColor),
		)
		f2 = lambda: config.drawBlockColor.stepTransition()
		config.drawBlockShape = [f1, f2]

	except Exception as e:
		print(e)
		config.drawBlock = False
		config.drawBlockShape = []

	createpolysquarepieces.createPieces(config)

	setInitialColors(config)

	config.t1 = time.time()
	config.t2 = time.time()

	# initial crossfade settings
	config.doingRefresh = 100
	config.doingRefreshCount = 100


def iterate(config):

	config.outlineColorObj.stepTransition()

	# print(config.doingRefresh)

	# Need to do a crossfade
	if config.doingRefresh < config.doingRefreshCount:
		# print("crossfade...",  config.doingRefresh/config.doingRefreshCount)
		if config.doingRefresh == 0:
			config.snapShot = config.canvasImage.copy()
		crossFade = Image.blend(
			config.snapShot,
			config.canvasImage,
			config.doingRefresh / config.doingRefreshCount,
		)
		config.render(crossFade, 0, 0)
		config.doingRefresh += 1
	else:
		temp = Image.new("RGBA", (config.canvasImageWidth, config.canvasImageWidth))
		temp.paste(config.canvasImage, (0, 0), config.canvasImage)
		if config.transformShape == True:
			temp = transformImage(temp)
		config.render(temp, 0, 0)

	for i in range(0, len(config.unitArray)):
		obj = config.unitArray[i]
		obj.update()
		obj.render()

		"""
		if config.doingRefresh < config.doingRefreshCount and random.random() < .1 :
			obj.render()
			config.doingRefresh += 1
		elif config.doingRefresh == config.doingRefreshCount :
			obj.render()
		"""

	# For drawing a single color block or other lambda fcu
	for fcu in config.drawBlockShape:
		fcu()

	config.t2 = time.time()
	delta = config.t2 - config.t1

	if delta > config.timeToComplete:
		restartPiece(config)


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
