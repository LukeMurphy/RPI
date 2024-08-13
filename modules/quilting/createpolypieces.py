from modules import coloroverlay, colorutils
from modules.quilting.polyunit import Unit

# the pattern array chooses which color each triangle is meant to be
# each star unit is comprised of 4 rows and 4 columns of sqaures that
# are each divided into  smaller triangles
# the rows are different lengths becasue of how I divided up each "row"
# e.g. the last row is just the left box/square, the middle tqo triangles
# and the lower right square/box

## In this, the 3rd group of color settings (index = 2) is the negative or
## background color
polyPattern = [
	[2, 1, 0, 2, 2, 1, 0, 2],
	[2, 1, 0, 1, 0, 2],
	[2, 0, 1, 0, 1, 0, 1, 1, 0, 2],
	[2, 2, 2, 2],
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
	for rows in range(0, config.blockRows):

		rowStart = rows * config.blockHeight * 3 + config.gapSize

		for cols in range(0, config.blockCols):

			columnStart = cols * config.blockLength * 3 + config.gapSize
			cntrOffset = [config.cntrOffsetX, config.cntrOffsetY]
			cntr = [columnStart, rowStart]

			## Jinky odds/evens alignment setup
			sizeAdjustor = 0
			## Alignment perfect setup
			if config.patternPrecision == True:
				sizeAdjustor = 0

			if refresh == True:
				obj = config.unitArray[itemCount]
			else:
				obj = Unit(config)
				obj.fillColors = []
			obj.xPos = cntr[0] + cols * config.blockLength
			obj.yPos = cntr[1] + rows * config.blockHeight
			obj.blockLength = config.blockLength - sizeAdjustor
			obj.blockHeight = config.blockHeight - sizeAdjustor
			obj.outlineColorObj = outlineColorObj

			for n in range(0, 4):
				for i in polyPattern[n]:
					obj.fillColors.append(config.fillColorSet[i])

			obj.setUp()
			if refresh == False:
				config.unitArray.append(obj)
			itemCount += 1


def refreshPalette(config):
	itemCount = 0
	for rows in range(0, config.blockRows):
		for cols in range(0, config.blockCols):
			obj = config.unitArray[itemCount]
			obj.fillColors = []
			for n in range(0, 4):
				for i in polyPattern[n]:
					obj.fillColors.append(config.fillColorSet[i])
				# obj.fillColors = fillColors
			obj.setUp()
			itemCount += 1
