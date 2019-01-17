from modules import colorutils, coloroverlay
from modules.quilting.polyunit import Unit

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


	# the pattern array chooses which color each triangle is meant to be
	# each star unit is comprised of 4 rows and 4 columns of sqaures that 
	# are each divided into  smaller triangles
	# the rows are different lengths becasue of how I divided up each "row"
	# e.g. the last row is just the left box/square, the middle tqo triangles
	# and the lower right square/box

	## In this, the 3rd group of color settings (index = 2) is the negative or
	## background color

	pattern = [
	[2,1,0,2,2,1,0,2],
	[2,1,0,1,0,2],
	[2,0,1,0,1,0,1,1,0,2],
	[2,2,2,2]
	]

	

	# Rows and columns of 9-squares
	for rows in range (0,config.blockRows) :

		rowStart = rows * config.blockHeight * 3 + config.gapSize

		for cols in range (0,config.blockCols) :

			columnStart = cols * config.blockLength * 3 + config.gapSize
			cntrOffset = [config.cntrOffsetX,config.cntrOffsetY]
			cntr = [columnStart, rowStart]

			## Jinky odds/evens alignment setup
			sizeAdjustor = 0
			## Alignment perfect setup
			if(config.patternPrecision == True): sizeAdjustor = 0

			n = 0

			obj = Unit(config)
			obj.xPos = cntr[0] + cols * config.blockLength 
			obj.yPos = cntr[1] + rows * config.blockHeight
			obj.blockLength = config.blockLength - sizeAdjustor
			obj.blockHeight = config.blockHeight - sizeAdjustor
			obj.outlineColorObj	= outlineColorObj

			for n in range(0,4):
				for i in pattern[n] :
					obj.fillColors.append(config.fillColorSet[i])

			obj.setUp()
			config.unitArray.append(obj)
			#n+=1







