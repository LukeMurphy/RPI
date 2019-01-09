#Blanks
import time
import random
import math

blankPixels = []
counterPixels = []
size = []

colsRange = (2,20)
rowsRange = (2,20)

totalCounterWidth = 0
numberOfDeadPixels = 10
probabilityOfBlockBlanks = .9

sizeTarget = [160,48]

def setBlanks() : 
	return None


def setBlanksOnImage() :
	#print("Setting Blanks")
	global config,blankPixels, sizeTarget, numberOfDeadPixels, probabilityOfBlockBlanks
	global colsRange, rowsRange
	blankPixels = []
	count = 0
	

	# scatter 
	for n in range (0, numberOfDeadPixels) :
		x = round(random.random()*sizeTarget[0])
		y = round(random.random()*sizeTarget[1])
		blankPixels.append((x,y))
		if(random.random() > probabilityOfBlockBlanks):
			cols = round(random.uniform(colsRange[0],colsRange[1]))
			rows = round(random.uniform(rowsRange[0],rowsRange[1]))

			for ii in range(0,rows):
				blankPixels.append((x,y + ii))
				for i in range (0,cols) :
					blankPixels.append((x+i,y + ii))



def setBlanksOnScreen() :
	#print("Setting Blanks")
	global config,blankPixels,numberOfDeadPixels, probabilityOfBlockBlanks
	global colsRange, rowsRange, sizeTarget
	blankPixels = []
	count = 0
	
	# scatter horizontally
	for n in range (0, numberOfDeadPixels) :
		x = round(random.random()*config.screenWidth)
		y = round(random.random()*config.screenHeight)
		blankPixels.append((x,y))
		if(random.random() > probabilityOfBlockBlanks):
			cols = round(random.uniform(colsRange[0],colsRange[1]))
			rows = round(random.uniform(rowsRange[0],rowsRange[1]))

			for ii in range(0,rows):
				blankPixels.append((x,y + ii))
				for i in range (0,cols) :
					blankPixels.append((x+i,y + ii))



def drawBlanks(target=None, direct = True) :
	global config, blankPixels,drawBlanksFlag, sizeTarget
	global colsRange, rowsRange
	if(target == None) : 
		target = config.renderImageFull
		sizeTarget = list(config.renderImageFull)

	count = 0
	blankNum = len(blankPixels)

	for n in range (0, blankNum) :
		if(direct) :
			config.matrix.SetPixel(blankPixels[n][0],blankPixels[n][1],0,0,0)
		else :
			if(blankPixels[n][0] < sizeTarget[0] and blankPixels[n][1] < sizeTarget[1]) :
				target.putpixel((blankPixels[n][0],blankPixels[n][1]),(0,0,0))









