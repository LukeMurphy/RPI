import time
import random
import math
import datetime
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageEnhance, ImageChops
from modules import colorutils, coloroverlay
import argparse



def pentagram(x, y, a = 1, n = 5, offset = 0, turn = 0) :
	pointArray = []
	theta = 2*math.pi / n
	theta2 = 2*math.pi/4 - theta
	angleOffset = 0
	if turn ==0 : 
		angleOffset = theta / (n - 1)

	d = a * math.cos(theta2) / 2
	r = a / (2 * math.cos(theta2))

	for nn in range (0,n) :
		xpt = x + math.cos(nn * theta - angleOffset + offset) * r
		ypt = y + math.sin(nn * theta - angleOffset + offset) * r
		pointArray.append((xpt,ypt))

	return (pointArray,d)



def marker(x, y, draw, f = "red"):
	draw.rectangle((x,y,x+3,y+3), fill=f)


def drawPolygons(start, end, x, y, d, theta, level = 1, parent = 0):
	draw = config.draw
	a = config.a
	offset = 2*math.pi/4 - theta
	theta2 = theta #2*math.pi/4 - config.theta
	for i in range(start, end) :
		theta2 += config.theta

		x1 = x + math.cos(theta2) * d * 2
		y1 = y + math.sin(theta2) * d * 2

		offset = theta2
		box = pentagram(x1, y1, config.a, config.n, offset, 1)
		f = config.colorArray[level]
		draw.polygon(box[0], fill = f)
		marker(x1,y1,draw)
		if i == 0 :
			marker(x1,y1,draw, "blue")

		d = box[1]

		if level < 2 and i < 5:
			_start  = i * 2
			_end = _start + 1
			theta3 = i  * config.theta + (2*math.pi/config.n - theta) - level * config.theta


			if _start == 6 :
				_start = 3
				_end = 5
				theta3 = (i - 5)  * config.theta + (2*math.pi/config.n - theta) - level * config.theta
			drawPolygons(_start, _end, x1, y1, d, theta3, level+1, i)



def drawPattern():

	draw = config.draw


	config.f1.stepTransition()
	config.f2.stepTransition()
	config.f3.stepTransition()
	config.f4.stepTransition()
	config.f5.stepTransition()
	config.f6.stepTransition()

	config.f1t = tuple(config.f1.currentColor)
	config.f2t = tuple(config.f2.currentColor)
	config.f3t = tuple(config.f3.currentColor)
	config.f4t = tuple(config.f4.currentColor)
	config.f5t = tuple(config.f5.currentColor)
	config.f6t = tuple(config.f6.currentColor)

	config.colorArray = [config.f1t,config.f2t,config.f3t,config.f4t,config.f5t,config.f6t]

	rows = config.rows
	cols = config.cols

	base = config.base
	exp = 0

	x = 100
	y = 100
	config.a = 20
	config.n = 5
	offset = 0
	config.theta = 2*math.pi/config.n
	theta2 = 2*math.pi/4 - config.theta

	box = pentagram(x, y, config.a, config.n, offset)
	draw.polygon(box[0], fill = config.f1t)
	#marker(x,y,config.draw)

	d = box[1] 

	offset = 2*math.pi/4 - config.theta

	drawPolygons(0,config.n, x, y, d, theta2)

	
	'''

	for i in range(0,n) :

		x1 = x + math.cos(theta2) * d * 2
		y1 = y + math.sin(theta2) * d * 2

		offset += theta
		theta2 += theta

		f = f2
		if i == 0 : f= f3

		box = pentagram(x1, y1, a, n, offset, 1)
		draw.polygon(box[0], fill = f)
		marker(x1,y1,draw)
		
		theta2b = 2*math.pi/n - theta2
		offset2 = 0

		if i < n :
			start  = i * 2
			end = start + 2
			for ii in range(start, end) :

				offset2 = theta * ii
				theta3 = ii * theta + (2*math.pi/n - theta2)

				x2 = x1 + math.cos(theta3) * d * 2 
				y2 = y1 + math.sin(theta3) * d * 2

				f = f4
				box = pentagram(x2, y2, a, n, offset2, 0)
				draw.polygon(box[0], fill = f)
				fi = "green"
				if ii == 0 : fi = "blue"
				marker(x2,y2,draw,fi)

	'''


	#renderImage.save("pattern.png")
	#print (rows, b17, cols*b17)

def getColorChanger():
	colOverlay = coloroverlay.ColorOverlay()
	colOverlay.randomSteps = False 
	colOverlay.timeTrigger = True 
	colOverlay.tLimitBase = 10 
	colOverlay.maxBrightness = config.brightness
	colOverlay.steps = 50
	return colOverlay


def showGrid():
	global config


	#config.image = config.image.rotate(config.imageRotation, expand=1)

	config.image.paste(config.canvasImage, (0,0), config.canvasImage)
	config.render(config.image, round(config.imageOffsetX), round(config.imageOffsetY))
	#if (random.random() < .02) :
		#config.base = random.uniform(2,5)
	#config.base += .1
	#config.imageOffsetX = -config.base*config.cols
	#config.imageOffsetY = -config.base*config.rows

	#config.imageOffsetX = -0
	#config.imageOffsetY = -0

	#config.imageRotation += .1



def main(run = True) :
	global config, directionOrder
	print("---------------------")
	print("Screen Loaded")

	colorutils.brightness = config.brightness

	config.delay = float(workConfig.get("pattern", 'delay'))
	config.base = float(workConfig.get("pattern", 'base'))
	config.rows = int(workConfig.get("pattern", 'rows'))
	config.cols = int(workConfig.get("pattern", 'cols'))


	config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	config.draw = ImageDraw.Draw(config.image)
	config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.canvasDraw = ImageDraw.Draw(config.canvasImage)

	config.imageOffsetX = 0
	config.imageOffsetY = 0

	config.f1 = getColorChanger()
	config.f2 = getColorChanger()
	config.f3 = getColorChanger()
	config.f4 = getColorChanger()
	config.f5 = getColorChanger()
	config.f6 = getColorChanger()

	config.imageRotation = .0001



	'''
	config.colOverlay.minHue = float(workConfig.get("screenproject", 'minHue'))
	config.colOverlay.maxHue = float(workConfig.get("screenproject", 'maxHue'))
	config.colOverlay.minSaturation = float(workConfig.get("screenproject", 'minSaturation'))
	config.colOverlay.maxSaturation= float(workConfig.get("screenproject", 'maxSaturation'))
	config.colOverlay.minValue = float(workConfig.get("screenproject", 'minValue'))
	config.colOverlay.maxBrightness = float(workConfig.get("screenproject", 'maxBrightness'))
	config.colOverlay.maxValue = float(workConfig.get("screenproject", 'maxValue'))

	config.crackChangeProb = float(workConfig.get("screenproject", 'crackChangeProb'))
	config.imageResetProb = float(workConfig.get("screenproject", 'imageResetProb'))
	'''



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


def callBack() :
	global config
	return True




''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


	




