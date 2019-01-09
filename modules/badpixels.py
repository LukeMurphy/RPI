#Blanks
import time
import random
import math

blankPixels = []
counterPixels = []

colsRange = (2,20)
rowsRange = (2,20)

size = (160,160)

totalCounterWidth = 0
numberOfDeadPixels = 10
probabilityOfBlockBlanks = .9

def setBlanks() : return None

def setBlanksOnImage() :
	#print("Setting Blanks")
	global config,blankPixels, size, numberOfDeadPixels, probabilityOfBlockBlanks
	global colsRange, rowsRange
	blankPixels = []
	count = 0
	size = config.renderImageFull.size
	# scatter horizontally
	for n in range (0, numberOfDeadPixels) :
		x = int(random.random()*size[0])
		y = int(random.random()*size[1])
		blankPixels.append((x,y))
		if(random.random() > probabilityOfBlockBlanks):
			cols = int(random.uniform(colsRange[0],colsRange[1]))
			rows = int(random.uniform(rowsRange[0],rowsRange[1]))

			for ii in range(0,rows):
				blankPixels.append((x,y + ii))
				for i in range (0,cols) :
					blankPixels.append((x+i,y + ii))

def setBlanksOnScreen() :
	#print("Setting Blanks")
	global config,blankPixels,numberOfDeadPixels, probabilityOfBlockBlanks
	global colsRange, rowsRange
	blankPixels = []
	count = 0
	# scatter horizontally
	for n in range (0, numberOfDeadPixels) :
		x = int(random.random()*config.actualScreenWidth)
		y = int(random.random()*48)
		blankPixels.append((x,y))
		if(random.random() > probabilityOfBlockBlanks):
			cols = int(random.uniform(colsRange[0],colsRange[1]))
			rows = int(random.uniform(rowsRange[0],rowsRange[1]))

			for ii in range(0,rows):
				blankPixels.append((x,y + ii))
				for i in range (0,cols) :
					blankPixels.append((x+i,y + ii))
		
def drawBlanks(target=None, direct = True) :
	global config, blankPixels,drawBlanksFlag, size
	global colsRange, rowsRange
	if(target==None) : target = config.renderImageFull
	if (len(blankPixels) == 0): setBlanks()
	count = 0
	blankNum=len(blankPixels)

	for n in range (0, blankNum) :
		if(direct) :
			config.matrix.SetPixel(blankPixels[n][0],blankPixels[n][1],0,0,0)
		else :
			if(blankPixels[n][0] < size[0] and blankPixels[n][1] < size[1]) :
				target.putpixel((blankPixels[n][0],blankPixels[n][1]),(0,0,0))