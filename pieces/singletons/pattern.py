import time
import random
import math
import datetime
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageEnhance, ImageChops
from modules import colorutils, coloroverlay
import argparse


def cross(x, y, l = 1, w = 1) :
	# 12 points

	a = (x, y)
	b = (x + l, y)
	c = (x + l, y - l)
	d = (x + l + w, y - l)
	e = (x + l + w, y )
	f = (x + l + w + l, y )
	g = (x + l + w + l, y + w)
	h = (x + l + w, y + w)
	i = (x + l + w, y + l + w )
	j = (x + l, y + l + w )
	k = (x + l, y +  w)
	m = (x, y + w)

	return [a,b,c,d,e,f,g,h,i,j,k,m]


def drawPatternBlock(rows, cols, f1, f2, l, w, draw, offsetX0, offsetY0, 
	colrule=None, rowrule=None, interstitial = 0, intrastitial = 0 ):
	rCount = 0
	cCount = 0
	for r in range (0, rows) :
		offsetY = offsetY0 + r * (l+w+ interstitial) 
		for c in range (0,cols) :
			offsetX = offsetX0 +  c * (l + w + interstitial) 
			f = f1
			if c%2 > 0:
				f = f2
			box = cross(offsetX + c * (l+w) + c * interstitial , 
						offsetY + (l+w) * r + r * interstitial , 
						l, w)

			if colrule is not None :
				if r in rowrule :
					if rCount%2 > 0:
						f = f1
					else :
						f = f2
					rCount+=1
				if c in colrule :
					if cCount%2 > 0:
						f = f1
					else :
						f = f2
					cCount+=1
					draw.polygon(box, fill = f)
			else :
				draw.polygon(box, fill = f)


def drawPattern():

	draw = config.draw

	config.f1.stepTransition()
	config.f2.stepTransition()
	config.f3.stepTransition()
	config.f4.stepTransition()
	config.f5.stepTransition()
	config.f6.stepTransition()

	config.colorArrayBase = [config.f1, config.f2, config.f3, config.f4, config.f5, config.f6]
	config.colorArray = []

	#for i in range(0,6) :
	#	setColorProperties(config.colorArrayBase[i])

	for i in config.colorArrayBase :
		i.stepTransition()
		config.colorArray.append(tuple(i.currentColor))

	f1 = tuple(config.f1.currentColor)
	f2 = tuple(config.f2.currentColor)
	f3 = tuple(config.f3.currentColor)
	f4 = tuple(config.f4.currentColor)
	f5 = tuple(config.f5.currentColor)
	f6 = tuple(config.f6.currentColor)

	rows = config.rows
	cols = config.cols

	base = config.base
	exp = 0

	b0 = 0
	b1 = 1 * base
	b3 = 3 * base
	b4 = 4 * base
	b5 = 5 * base
	b7 = 7 * base
	b8 = 8 * base
	b9 = 9 * base
	b11 = 11 * base
	b12 = 12 * base
	b13 = 13 * base
	b17 = 17 * base
	patternXOffset = config.patternXOffset
	#b7

	draw.rectangle((0,0,config.canvasWidth,config.canvasHeight), fill=f6)

	inter = 0 + exp
	drawPatternBlock(rows, cols, config.colorArray[1], config.colorArray[0], b3, b5, draw, b1 + patternXOffset, b7, None, None, inter)
	drawPatternBlock(rows, cols, config.colorArray[1], config.colorArray[0], b5, b3, draw, b0 + patternXOffset, b8, None, None, inter)

	l = base
	w = base 

	inter = 6 * base  + exp
	# Top
	drawPatternBlock(rows, cols, config.colorArray[1], config.colorArray[0], l, w, draw, b5 + patternXOffset, b1, None, None, inter)
	
	# Right
	drawPatternBlock(rows, cols, config.colorArray[1], config.colorArray[0], l, w, draw, b11 + patternXOffset , b9, None, None, inter)
	# Left
	drawPatternBlock(rows, cols, config.colorArray[1], config.colorArray[0], l, w, draw, -b1 + patternXOffset , b9, None, None, inter)

	
	# Bottom
	drawPatternBlock(rows, cols, config.colorArray[1], config.colorArray[0], l, w, draw, b5 + patternXOffset, b17, None, None, inter)
	
	# 3x3 grid
	for ii in range(0,round(rows), 1) :
		yOffset = ii * base * 16
		for i in range(0,round(rows), 2) :
			xOffset = i * base * 16
			drawPatternBlock(3, 3, config.colorArray[1], config.colorArray[1], l, w, draw, b1 + patternXOffset + xOffset, b5 + yOffset, None,None, 0)
			drawPatternBlock(3, 3, config.colorArray[0], config.colorArray[0], l, w, draw, b17 + patternXOffset + xOffset, b5 + yOffset, None,None, 0)

	# interior x
	drawPatternBlock(rows, cols, config.colorArray[3], config.colorArray[4], l, w, draw, b5 + patternXOffset, b5, None, None, inter)
	drawPatternBlock(rows, cols, config.colorArray[3], config.colorArray[4], l, w, draw, b5 + patternXOffset, b13, None, None, inter)
	drawPatternBlock(rows, cols, config.colorArray[3], config.colorArray[4], l, w, draw, b1 + patternXOffset, b9, None, None, inter)
	drawPatternBlock(rows, cols, config.colorArray[3], config.colorArray[4], l, w, draw, b9 + patternXOffset, b9, None, None, inter)
	# larger center x
	drawPatternBlock(rows, cols, config.colorArray[3], config.colorArray[4], b1, b3, draw, b4 + patternXOffset, 8 * base, None, None,  b4 + exp)
	# Center
	drawPatternBlock(rows, cols, config.colorArray[4], config.colorArray[3], l, w, draw, b5 + patternXOffset, b9, None, None, inter)

	# interior off- x
	drawPatternBlock(rows* 2, cols, config.colorArray[3], config.colorArray[4], l, w, draw, b9 + patternXOffset, b1, None, None, inter)
	drawPatternBlock(rows* 2, cols, config.colorArray[3], config.colorArray[4], l, w, draw, b17 + patternXOffset, b1, None, None, inter)
	drawPatternBlock(rows* 1, cols, config.colorArray[3], config.colorArray[4], l, w, draw, b13 + patternXOffset, b13, None, None, inter)
	drawPatternBlock(rows* 2, cols, config.colorArray[3], config.colorArray[4], l, w, draw, b13 + patternXOffset, b5, None, None, inter)
	# larger center x
	drawPatternBlock(rows * 2, cols, config.colorArray[3], config.colorArray[4], b1, b3, draw, b12 + patternXOffset, 0 * base, None, None,  b4 + exp)
	# Center
	drawPatternBlock(rows * 2, cols, config.colorArray[1], config.colorArray[0], l, w, draw, b13 + patternXOffset, b1, None, None, inter)
	'''
	'''
	#renderImage.save("pattern.png")

	#print (rows, b17, cols*b17)


def getColorChanger(n=0):
	colOverlay = coloroverlay.ColorOverlay()
	colOverlay.randomSteps = False 
	colOverlay.timeTrigger = True 
	colOverlay.tLimitBase = round(random.uniform(18,20))
	colOverlay.tLimit = round(random.uniform(18,20))
	colOverlay.maxBrightness = config.brightness
	colOverlay.steps = round(random.uniform(15,22))
	setColorProperties(colOverlay, n)
	return colOverlay

def setColorProperties(c, n = 0) :
	c.minHue = float(workConfig.get("pattern", 'minHue'))
	c.maxHue = float(workConfig.get("pattern", 'maxHue'))
	c.minSaturation = float(workConfig.get("pattern", 'minSaturation'))
	c.maxSaturation = float(workConfig.get("pattern", 'maxSaturation'))
	c.minValue = float(workConfig.get("pattern", 'minValue'))
	c.maxBrightness = float(workConfig.get("pattern", 'maxBrightness'))
	c.maxValue = float(workConfig.get("pattern", 'maxValue'))

	# cross shape 1
	if n == 5 :
		c.minHue = 0
		c.maxHue = 30
		c.minSaturation = .99
		c.maxSaturation = .99
		c.minValue = .5
		c.maxValue = .9

	# outer cross shape 1
	if n == 1 :
		c.minHue = 0
		c.maxHue = 30
		c.minSaturation = .99
		c.maxSaturation = .99
		c.minValue = .5
		c.maxValue = .9

	# outer cross shape 2
	if n == 2 :
		c.minHue = 30
		c.maxHue = 45
		c.minSaturation = .99
		c.maxSaturation = .99
		c.minValue = .5
		c.maxValue = .9

	# outline of cross shapes
	if n == 6 :
		c.minHue = 0
		c.maxHue = 50
		c.minSaturation = .99
		c.maxSaturation = .99
		c.minValue = .5
		c.maxValue = .9

	# Not used it seems ???
	if n == 3 :
		c.minHue = 200
		c.maxHue = 245
		c.minSaturation = .99
		c.maxSaturation = .99
		c.minValue = .5
		c.maxValue = .9

	# secondary crosss shape
	if n == 4 :
		c.minHue = 200
		c.maxHue = 300
		c.minSaturation = .99
		c.maxSaturation = .99
		c.minValue = .5
		c.maxValue = .9



	c.colorTransitionSetup()


def drawTheReal() :
	x = 150
	y = 128
	w = 120 + x
	h = 80 + y
	box = tuple([x, y, w, h])
	config.canvasDraw.rectangle(box, fill = tuple(config.f6.currentColor))

	lines = h - y
	for i in range(0, lines, 5)  :
		f =  tuple(config.f1.currentColor)
		if random.random() < .01 :
			f = colorutils.randomColor(1)
		config.canvasDraw.rectangle((x,y+i,w,y+i+2) , fill = f)


def showGrid():
	global config
	config.image.paste(config.canvasImage, (0,0), config.canvasImage)
	config.render(config.image, round(config.imageOffsetX), round(config.imageOffsetY))


def main(run = True) :
	global config, directionOrder
	print("---------------------")
	print("Screen Loaded")

	colorutils.brightness = config.brightness

	config.delay = float(workConfig.get("pattern", 'delay'))
	config.base = float(workConfig.get("pattern", 'base'))
	config.rows = int(workConfig.get("pattern", 'rows'))
	config.cols = int(workConfig.get("pattern", 'cols'))
	config.patternXOffset = int(workConfig.get("pattern", 'patternXOffset'))

	config.delay = float(workConfig.get("pattern", 'delay'))


	config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	config.draw = ImageDraw.Draw(config.image)
	config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.canvasDraw = ImageDraw.Draw(config.canvasImage)

	config.imageOffsetX = 0
	config.imageOffsetY = 0

	config.f1 = getColorChanger(1)
	config.f2 = getColorChanger(2)
	config.f3 = getColorChanger(3)
	config.f4 = getColorChanger(4)
	config.f5 = getColorChanger(5)
	config.f6 = getColorChanger(6)

	config.imageRotation = .0001




	setUp()

	if(run) : runWork()


def setUp():
	global config
	drawPattern()


def runWork():
	global config
	while True:
		iterate()
		time.sleep(config.delay)  


def iterate() :
	global config
	drawPattern()
	showGrid()
	#drawTheReal()





''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


	




