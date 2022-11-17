import random

from modules import coloroverlay, colorutils
from modules.quilting.triangleunit import Unit

polyPattern_ = [
	[0, 0, 0, 1, 0, 0, 0, 1],
	[1, 1, 1, 1, 1, 1, 1, 1],
	[1, 1, 1, 1, 1, 1, 1, 1],
	[1, 1, 1, 1, 1, 1, 1, 1],
	[1, 1, 1, 1, 1, 1, 1, 1],
	[1, 1, 1, 1, 1, 1, 1, 1],
	[1, 1, 1, 1, 1, 1, 1, 1],
	[1, 1, 1, 1, 1, 1, 1, 1],
	[1, 1, 1, 1, 1, 1, 1, 1],
	[1, 1, 1, 1, 1, 1, 1, 1],
	[1, 1, 1, 1, 1, 1, 1, 1],
	[1, 1, 1, 1, 1, 1, 1, 1],
	[1, 1, 1, 1, 1, 1, 1, 1],
	[1, 1, 1, 1, 1, 1, 1, 1],
	[1, 1, 1, 1, 1, 1, 1, 1],
	[1, 1, 1, 1, 1, 1, 1, 1],
]


# the pattern array chooses which color each triangle is meant to be
# each star unit is comprised of 4 rows and 4 columns of sqaures that
# are each divided into 4 smaller triangles

polyPattern = [
	[0, 0, 0, 0, 0, 0, 0, 0],
	[1, 0, 0, 0, 1, 1, 1, 0],
	[0, 0, 0, 1, 0, 1, 1, 1],
	[0, 0, 0, 0, 0, 0, 0, 0],
	[0, 1, 1, 1, 0, 0, 0, 1],
	[1, 1, 1, 2, 1, 2, 2, 2],
	[2, 1, 1, 1, 2, 2, 2, 1],
	[1, 1, 1, 0, 1, 0, 0, 0],
	[0, 0, 0, 1, 0, 1, 1, 1],
	[1, 2, 2, 2, 1, 1, 1, 2],
	[2, 2, 2, 1, 2, 1, 1, 1],
	[1, 0, 0, 0, 1, 1, 1, 0],
	[0, 0, 0, 0, 0, 0, 0, 0],
	[1, 1, 1, 0, 1, 0, 0, 0],
	[0, 1, 1, 1, 0, 0, 0, 1],
	[0, 0, 0, 0, 0, 0, 0, 0],
]


def createPieces(config, refresh=False):

	cntrOffset = [config.cntrOffsetX, config.cntrOffsetY]

	if refresh == False:
		config.unitArray = []

	outlineColorObj = coloroverlay.ColorOverlay()
	outlineColorObj.randomRange = (5.0, 30.0)

	## Jinky odds/evens alignment setup
	sizeAdjustor = 0
	## Alignment perfect setup
	if config.patternPrecision == True:
		sizeAdjustor = 1
	cntr = [0, 0]

	# Rows and columns of 9-squares
	itemCount = 0

	# This will be different for each quilt type and if the dimensions change
	# doing this to conserve some CPU ....
	config.unitArrayLimit = config.blockRows * config.blockCols * 16

	if len(config.unitArray) > config.unitArrayLimit:
		config.unitArray = config.unitArray[: config.unitArrayLimit]

	jumble = 0
	for rows in range(0, config.blockRows):

		rowStart = rows * config.blockHeight * 4 + config.gapSize

		for cols in range(0, config.blockCols):

			columnStart = cols * config.blockLength * 4 + config.gapSize
			cntrOffset = [config.cntrOffsetX, config.cntrOffsetY]
			cntr = [columnStart, rowStart]

			## Jinky odds/evens alignment setup
			sizeAdjustor = 0
			## Alignment perfect setup
			if config.patternPrecision == True:
				sizeAdjustor = 1

			n = 0
			for r in range(0, 4):
				for c in range(0, 4):
					if itemCount < config.unitArrayLimit:
						try:
							if refresh == True:
								obj = config.unitArray[itemCount]
							else:
								obj = Unit(config)

							xRan = random.random() * jumble
							yRan = random.random() * jumble
							obj.xPos = cntr[0] + c * (config.blockLength + xRan)
							obj.yPos = cntr[1] + r * (config.blockHeight + yRan)
							obj.blockLength = config.blockLength - sizeAdjustor + xRan
							obj.blockHeight = config.blockHeight - sizeAdjustor + yRan
							obj.outlineColorObj = outlineColorObj

							for i in polyPattern[n]:
								if refresh == True:
									obj.fillColors[i] = config.fillColorSet[i]
								else:
									obj.fillColors.append(config.fillColorSet[i])

							obj.outlineColorObj.currentColor = [0, 0, 0, 255]
							obj.setUp()

							if refresh == False:
								config.unitArray.append(obj)
							n += 1
							itemCount += 1
						except Exception as e:
							print(
								e,
								itemCount,
								len(config.unitArray),
								config.unitArrayLimit,
							)
							pass


def refreshPalette(config):
	itemCount = 0
	config.unitArrayLimit = config.blockRows * config.blockCols * 16
	for rows in range(0, config.blockRows):
		for cols in range(0, config.blockCols):
			n = 0
			for r in range(0, 4):
				for c in range(0, 4):
					if itemCount < config.unitArrayLimit:
						obj = config.unitArray[itemCount]
						fillColors = []
						for i in polyPattern[n]:
							fillColors.append(config.fillColorSet[i])
							# print(config.fillColorSet[i].valueRange)
						n += 1
						obj.fillColors = fillColors
						obj.outlineColorObj.currentColor = [0, 0, 0, 255]
						obj.setUp()
						itemCount += 1
