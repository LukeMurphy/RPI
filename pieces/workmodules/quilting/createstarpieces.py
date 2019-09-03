from modules import coloroverlay, colorutils
from pieces.workmodules.quilting.starunit import Unit

polyPattern = [[0, 1, 0], [2, 0, 3], [0, 4, 0]]


def createPieces(config, refresh=False):
	# global config
	cntrOffset = [config.cntrOffsetX, config.cntrOffsetY]

	if refresh == False:
		config.unitArray = []

	## Jinky odds/evens alignment setup
	sizeAdjustor = 0
	## Alignment perfect setup
	if config.patternPrecision == True:
		sizeAdjustor = 1

	n = 0
	itemCount = 0
	# This will be different for each quilt type and if the dimensions change
	# doing this to conserve some CPU ....
	config.unitArrayLimit = config.blockRows * config.blockCols * 8

	if len(config.unitArray) > config.unitArrayLimit:
		config.unitArray = config.unitArray[: config.unitArrayLimit]

	# Rows and columns of 9-squares
	for rows in range(0, config.blockRows):

		rowStart = rows * config.blockHeight * 3 + config.gapSize

		for cols in range(0, config.blockCols):

			columnStart = cols * config.blockLength * 3 + config.gapSize

			# Three rows of three squares
			squareNumber = 0
			for unitRow in range(0, len(polyPattern)):
				rowDelta = unitRow * config.blockHeight

				# Each square is either divided in to 4 or 3 triangles
				for unitBlock in range(0, len(polyPattern[unitRow])):
					colDelta = unitBlock * config.blockHeight
					cntr = [
						columnStart + cntrOffset[0] + colDelta,
						rowStart + cntrOffset[1] + rowDelta,
					]

					outlineColorObj = coloroverlay.ColorOverlay()
					outlineColorObj.randomRange = (5.0, 30.0)
					if itemCount < config.unitArrayLimit:
						if refresh == True:
							obj = config.unitArray[itemCount]
						else:
							obj = Unit(config)

						obj.xPos = cntr[0]
						obj.yPos = cntr[1]
						obj.fillColorMode = "red"
						obj.blockLength = config.blockLength - sizeAdjustor
						obj.blockHeight = config.blockHeight - sizeAdjustor
						obj.outlineColorObj = outlineColorObj

						obj.minHue = config.fillColorSet[0].hueRange[0]
						obj.maxHue = config.fillColorSet[0].hueRange[1]
						obj.minSaturation = config.fillColorSet[0].saturationRange[0]
						obj.maxSaturation = config.fillColorSet[0].saturationRange[1]
						obj.minValue = config.fillColorSet[0].valueRange[0]
						obj.maxValue = config.fillColorSet[0].valueRange[1]

						obj.compositionNumber = polyPattern[unitRow][unitBlock]

						"The squares"
						if obj.compositionNumber == 0:
							obj.minHue = config.fillColorSet[1].hueRange[0]
							obj.maxHue = config.fillColorSet[1].hueRange[1]
							obj.minSaturation = config.fillColorSet[1].saturationRange[
								0
							]
							obj.maxSaturation = config.fillColorSet[1].saturationRange[
								1
							]
							obj.minValue = config.fillColorSet[1].valueRange[0]
							obj.maxValue = config.fillColorSet[1].valueRange[1]

							obj.squareNumber = squareNumber
							squareNumber += 1

						"The center block"
						if obj.compositionNumber == 0 and unitRow == 1:
							obj.minHue = config.fillColorSet[2].hueRange[0]
							obj.maxHue = config.fillColorSet[2].hueRange[1]
							obj.minSaturation = config.fillColorSet[2].saturationRange[
								0
							]
							obj.maxSaturation = config.fillColorSet[2].saturationRange[
								1
							]
							obj.minValue = config.fillColorSet[2].valueRange[0]
							obj.maxValue = config.fillColorSet[2].valueRange[1]

						obj.setUp(n)
						itemCount += 1
						if refresh == False:
							config.unitArray.append(obj)

			n += 1


def refreshPalette(config):
	itemCount = 0
	n = 0
	config.unitArrayLimit = config.blockRows * config.blockCols * 8
	# Rows and columns of 9-squares
	for rows in range(0, config.blockRows):
		for cols in range(0, config.blockCols):
			# Three rows of three squares
			squareNumber = 0
			for unitRow in range(0, len(polyPattern)):
				# Each square is either divided in to 4 or 3 triangles
				for unitBlock in range(0, len(polyPattern[unitRow])):
					if itemCount < config.unitArrayLimit:
						obj = config.unitArray[itemCount]
						obj.minHue = config.fillColorSet[0].hueRange[0]
						obj.maxHue = config.fillColorSet[0].hueRange[1]
						obj.minSaturation = config.fillColorSet[0].saturationRange[0]
						obj.maxSaturation = config.fillColorSet[0].saturationRange[1]
						obj.minValue = config.fillColorSet[0].valueRange[0]
						obj.maxValue = config.fillColorSet[0].valueRange[1]
						obj.compositionNumber = polyPattern[unitRow][unitBlock]

						"The squares"
						if obj.compositionNumber == 0:
							obj.minHue = config.fillColorSet[1].hueRange[0]
							obj.maxHue = config.fillColorSet[1].hueRange[1]
							obj.minSaturation = config.fillColorSet[1].saturationRange[
								0
							]
							obj.maxSaturation = config.fillColorSet[1].saturationRange[
								1
							]
							obj.minValue = config.fillColorSet[1].valueRange[0]
							obj.maxValue = config.fillColorSet[1].valueRange[1]

							obj.squareNumber = squareNumber
							squareNumber += 1

						"The center block"
						if obj.compositionNumber == 0 and unitRow == 1:
							obj.minHue = config.fillColorSet[2].hueRange[0]
							obj.maxHue = config.fillColorSet[2].hueRange[1]
							obj.minSaturation = config.fillColorSet[2].saturationRange[
								0
							]
							obj.maxSaturation = config.fillColorSet[2].saturationRange[
								1
							]
							obj.minValue = config.fillColorSet[2].valueRange[0]
							obj.maxValue = config.fillColorSet[2].valueRange[1]

						obj.setUp(n)
						itemCount += 1
			n += 1


def _refreshPalette(config):
	itemCount = 0
	for rows in range(0, config.blockRows):
		for cols in range(0, config.blockCols):
			n = 0
			for r in range(0, 4):
				for c in range(0, 4):
					obj = config.unitArray[itemCount]
					fillColors = []
					for i in polyPattern[n]:
						fillColors.append(config.fillColorSet[i])
					n += 1
					obj.fillColors = fillColors
					obj.setUp()
					itemCount += 1
