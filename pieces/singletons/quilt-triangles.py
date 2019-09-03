import math
import random
import textwrap
import time

from modules import badpixels, coloroverlay, colorutils
from pieces.workmodules.quilting import createstarpieces, createtrianglepieces
from pieces.workmodules.quilting.colorset import ColorSet
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


def restartPiece():
	config.t1 = time.time()
	config.t2 = time.time()

	if config.usePresets == True:

		if config.quiltPattern == "stars":
			newHueRange = randomRange(0, 360, True)
			newSaturationRange = randomRange()
			newValueRange = randomRange()

			"""

			# stars: BASE
			config.c1HueRange = newHueRange
			config.c1ValueRange = newValueRange

			# stars: SQUARE
			config.c2SaturationRange = randomRange()
			config.c2ValueRange = randomRange()
			config.c2HueRange = randomRange(0,360,True)

			"""

			# stars: CENTER SQUARE
			config.c3HueRange = newHueRange
			config.c3ValueRange = randomRange()
			if random.random() < 0.25:
				choice = round(random.uniform(1, 3))
				# print ("Choice {0}".format(choice))
				if choice == 1:
					# yellow centers
					config.c3HueRange = (30, 60)
					config.c3SaturationRange = (0.6, 1)
					config.c3ValueRange = (0.4, 1)
				elif choice == 2:
					# red centers
					config.c3HueRange = (0, 30)
					config.c3SaturationRange = (0.6, 1)
					config.c3ValueRange = (0.4, 1)
				else:
					# yellow centers
					config.c3HueRange = (0, 360)
					config.c3SaturationRange = (0.6, 1)
					config.c3ValueRange = (0.4, 1)

		else:
			newHueRange = (0, 360)  # randomRange(0,360,True)
			newSaturationRange = randomRange(0.2, 1)
			newValueRange = randomRange(0.2, 1)

			# triangles: major outline squares and diamonds
			config.c1HueRange = newHueRange
			config.c1SaturationRange = newSaturationRange
			config.c1ValueRange = newValueRange

			# triangles:  wings of the 8-point inner starts
			newHueRange = randomRange(0, 360, True)
			newSaturationRange = randomRange()
			newValueRange = randomRange()

			config.c2HueRange = newHueRange
			config.c2SaturationRange = newSaturationRange
			config.c2ValueRange = newValueRange

			# triangles:  the star center diamond
			# newHueRange = randomRange(0,360,True)
			if random.random() < 0.5:
				newHueRange = randomRange(0, 360, True)
			newSaturationRange = randomRange()
			newValueRange = randomRange()

			config.c3HueRange = newHueRange
			config.c3SaturationRange = newSaturationRange
			config.c2ValueRange = newValueRange
	else:
		# major outline squares and diamonds
		"""
		config.c1ValueRange = (.3,1.5)
		config.c2ValueRange = (.3,1.5)
		config.c3ValueRange = (.3,1.5)
		config.c1HueRange = (0,360)
		config.c1SaturationRange = (.53,1.81)
		# wings of the 8-point inner starts
		config.c2HueRange = (0,360)
		config.c2SaturationRange = (.53,1.81)
		# the star center diamond
		config.c3HueRange = (0,360)
		config.c3SaturationRange = (.53,1.81)
		"""

	# print(config.c1ValueRange, config.c2ValueRange, config.c3ValueRange)
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
		if config.quiltPattern == "stars":
			config.blockSize = round(
				random.uniform(config.blockSizeMin, config.blockSizeMax)
			)
			if config.blockSize >= 11:
				config.blockCols = config.blockColsMin
				config.blockRows = config.blockRowsMin
				createstarpieces.createPieces(config, True)
			else:
				config.blockCols = config.blockColsMax
				config.blockRows = config.blockRowsMax
				createstarpieces.createPieces(config, False)
		else:
			config.blockSize = round(
				random.uniform(config.blockSizeMin, config.blockSizeMax)
			)
			if config.blockSize >= 16:
				config.blockCols = config.blockColsMin
				config.blockRows = config.blockRowsMin
				createtrianglepieces.createPieces(config, True)
			else:
				config.blockCols = config.blockColsMax
				config.blockRows = config.blockRowsMax
				createtrianglepieces.createPieces(config, False)

		config.blockLength = config.blockSize
		config.blockHeight = config.blockSize
		config.doingRefresh = 0
		config.doingRefreshCount = 100

	if config.quiltPattern == "stars":
		createstarpieces.refreshPalette(config)
	else:
		createtrianglepieces.refreshPalette(config)
		setInitialColors(True)

	if random.random() < 0.5:
		config.rotation = random.uniform(-config.rotationRange, config.rotationRange)


def setInitialColors(refresh=False):
	## Better initial color when piece is turned on

	for i in range(0, len(config.unitArray)):
		obj = config.unitArray[i]
		# print("number of colorOverlay objs {}".format(len(obj.triangles)) )
		for c in range(0, len(obj.triangles)):
			colOverlay = obj.triangles[c][1]
			# colOverlay.colorB = colorutils.randomColorAlpha(config.brightness * .8,0)
			colOverlay.colorA = colorutils.randomColorAlpha(config.brightness * 0.8, 0)
			colOverlay.colorTransitionSetup()
			colOverlay.colorTransitionSetupValues()


def main(run=True):
	global config, directionOrder, workConfig
	print("---------------------")
	print("QUILT TRIANGLES or STARS Loaded")

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

	try:
		config.transformShape = workConfig.getboolean("quilt", "transformShape")
		transformTuples = workConfig.get("quilt", "transformTuples").split(",")
		config.transformTuples = tuple([float(i) for i in transformTuples])

		"""
		e.g.
		#transformTuples_ = .9, 0, 0, -0.05,  .6, 0, -0.001, 0
		#transformTuples__ = 1.2, .5, 0, 0.081,  1, 0, 0.0009, 0.0

		#transformTuples = 1.2, .5, 0, 0.071,  1, 0, 0.0005, 0.0
		## No transform
		transformTuples = 1, .5, 0, 0.0,  1, 0, 0.0, 0.0

		#transformTuples = 1, 0, 0, 0.0,  1, 0, 0, 0.0
		#transformTuples = 0, 0, 0, 0,  0, 0, 0, 0.0
		"""

	except Exception as e:
		print(e)
		config.transformShape = False

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

	config.canvasImage = Image.new(
		"RGBA", (config.canvasImageWidth, config.canvasImageHeight)
	)

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

	config.unitArray = []
	if config.quiltPattern == "triangles":
		createtrianglepieces.createPieces(config)
	elif config.quiltPattern == "stars":
		createstarpieces.createPieces(config)

	try:
		config.usePresets = workConfig.getboolean("quilt", "usePresets")
	except Exception as e:
		print(e)
		config.usePresets = True

	try:
		config.rotationRange = float(workConfig.get("quilt", "rotationRange"))
	except Exception as e:
		config.rotationRange = 0
		print(e)

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
		config.canvasImageDraw = ImageDraw.Draw(config.canvasImage)
		config.drawBlock = True
		config.drawBlockShape = lambda: config.canvasImageDraw.polygon(
			config.drawBlockCoords, fill=config.drawBlockFixedColor
		)
	except Exception as e:
		print(e)
		config.drawBlock = False
		config.drawBlockShape = lambda: True

	setInitialColors()

	config.t1 = time.time()
	config.t2 = time.time()

	config.doingRefresh = 100
	config.doingRefreshCount = 100

	if run:
		runWork()


def runWork():
	global blocks, config, XOs
	# gc.enable()

	while True:
		iterate()
		time.sleep(config.delay)


def iterate():
	global config
	config.outlineColorObj.stepTransition()

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
		config.drawBlockShape()
		config.render(crossFade, 0, 0)
		config.doingRefresh += 1
	else:
		temp = Image.new("RGBA", (config.canvasImageWidth, config.canvasImageHeight))
		temp.paste(config.canvasImage, (0, 0), config.canvasImage)
		if config.transformShape == True:
			temp = transformImage(temp)
		config.drawBlockShape()
		config.render(temp, 0, 0)

	for i in range(0, len(config.unitArray)):
		obj = config.unitArray[i]
		obj.update()
		obj.render()

	config.t2 = time.time()
	delta = config.t2 - config.t1

	if delta > config.timeToComplete:
		restartPiece()


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
