from modules import colorutils, coloroverlay
from modules.quilting.triangleunit import Unit

def createPieces(config) :

	cntrOffset = [config.cntrOffsetX,config.cntrOffsetY]

	config.unitArray = []
	outlineColorObj = coloroverlay.ColorOverlay()
	outlineColorObj.randomRange = (5.0,30.0)

	## Jinky odds/evens alignment setup
	sizeAdjustor = 0
	## Alignment perfect setup
	if(config.patternPrecision == True): sizeAdjustor = 1

	
	cntr = [0,0]

	pattern = [
	[0,0,0,0,0,0,0,0],
	[1,0,0,0,1,1,1,0],
	[0,0,0,1,0,1,1,1],
	[0,0,0,0,0,0,0,0],
	[0,1,1,1,0,0,0,1],
	[1,1,1,1,1,1,1,1],
	[1,1,1,1,1,1,1,1],
	[1,1,1,0,1,0,0,0],
	[0,0,0,1,0,1,1,1],
	[1,1,1,1,1,1,1,1],
	[1,1,1,1,1,1,1,1],
	[1,0,0,0,1,1,1,0],
	[0,0,0,0,0,0,0,0],
	[1,1,1,0,1,0,0,0],
	[0,1,1,1,0,0,0,1],
	[0,0,0,0,0,0,0,0]
	]

	pattern = [
	[0,0,0,0,0,0,0,0],
	[1,0,0,0,1,1,1,0],
	[0,0,0,1,0,1,1,1],
	[0,0,0,0,0,0,0,0],

	[0,1,1,1,0,0,0,1],
	[1,1,1,2,1,2,2,2],
	[2,1,1,1,2,2,2,1],
	[1,1,1,0,1,0,0,0],

	[0,0,0,1,0,1,1,1],
	[1,2,2,2,1,1,1,2],
	[2,2,2,1,2,1,1,1],
	[1,0,0,0,1,1,1,0],

	[0,0,0,0,0,0,0,0],
	[1,1,1,0,1,0,0,0],
	[0,1,1,1,0,0,0,1],
	[0,0,0,0,0,0,0,0]
	]

	

	# Rows and columns of 9-squares
	for rows in range (0,config.blockRows) :

		rowStart = rows * config.blockHeight * 4 + config.gapSize

		for cols in range (0,config.blockCols) :

			columnStart = cols * config.blockLength * 4 + config.gapSize
			cntrOffset = [config.cntrOffsetX,config.cntrOffsetY]
			cntr = [columnStart, rowStart]

			## Jinky odds/evens alignment setup
			sizeAdjustor = 0
			## Alignment perfect setup
			if(config.patternPrecision == True): sizeAdjustor = 1

			n = 0
			for r in range(0,4):
				for c in range(0,4):
					obj = Unit(config)
					obj.xPos = cntr[0] + c * config.blockLength 
					obj.yPos = cntr[1] + r * config.blockHeight
					obj.blockLength = config.blockLength - sizeAdjustor
					obj.blockHeight = config.blockHeight - sizeAdjustor
					obj.outlineColorObj	= outlineColorObj

					for i in pattern[n] :
						obj.fillColors.append(config.fillColorSet[i])

					obj.setUp()
					config.unitArray.append(obj)
					n+=1
