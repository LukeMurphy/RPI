from modules import colorutils, coloroverlay
from modules.quilting.polysquaresunit import Unit

	# the pattern array chooses which color each triangle is meant to be
polyPattern =  [
	[0,1,2,0],
	[0,2,1,0],
	[2,1],
	[2,0,0,1],
	[1,0,0,2],
	[1,2],
	]

def createPieces(config, refresh = False) :

	cntrOffset = [config.cntrOffsetX,config.cntrOffsetY]

	if refresh == False :
		config.unitArray = []
	outlineColorObj = coloroverlay.ColorOverlay()
	outlineColorObj.randomRange = (5.0,30.0)

	## Jinky odds/evens alignment setup
	sizeAdjustor = 0
	## Alignment perfect setup
	if(config.patternPrecision == True): sizeAdjustor = 1

	cntr = [0,0]

	# Rows and columns of 9-squares
	itemCount = 0
	for rows in range (0,config.blockRows) :
		mult = 0
		if config.elongation == 1 : mult = 0
		if config.elongation == 2 : mult = 3
		if config.elongation == 3 : mult = 4
		if config.elongation == 4 : mult = 6
		if config.elongation == 5 : mult = 9

		rowStart = rows * config.blockHeight * 3 + rows * config.gapSize - rows * mult * config.blockHeight/config.elongation - config.blockHeight

		for cols in range (0,config.blockCols) :

			columnStart = cols * config.blockLength * 2 + cols * config.gapSize
			cntrOffset = [config.cntrOffsetX,config.cntrOffsetY]
			cntr = [columnStart, rowStart]

			## Jinky odds/evens alignment setup
			sizeAdjustor = 0
			## Alignment perfect setup
			if(config.patternPrecision == True): 
				sizeAdjustor = 0
			try :
				if refresh == True :
					obj = config.unitArray[itemCount]
				else :
					obj = Unit(config)
					obj.fillColors = []
				obj.xPos = cntr[0] #+ cols * config.blockLength 
				obj.yPos = cntr[1] + rows * 3*config.blockHeight
				obj.blockLength = config.blockLength - sizeAdjustor
				obj.blockHeight = config.blockHeight - sizeAdjustor
				obj.outlineColorObj	= outlineColorObj
				obj.lines = config.lines

				for n in range(0,len(polyPattern)):
					for i in polyPattern[n] :
						obj.fillColors.append(config.fillColorSet[i])

				obj.setUp()
				if refresh == False : config.unitArray.append(obj)
				itemCount += 1
			except Exception as e:
				print(e)
				continue


def refreshPalette(config):
	itemCount = 0
	for rows in range (0,config.blockRows) :
		for cols in range (0,config.blockCols) :
			obj = config.unitArray[itemCount]
			obj.fillColors = []
			for n in range(0,len(polyPattern)):
				for i in polyPattern[n] :
					obj.fillColors.append(config.fillColorSet[i])
				#obj.fillColors = fillColors
			obj.lines = config.lines
			obj.setUp()
			itemCount+=1






