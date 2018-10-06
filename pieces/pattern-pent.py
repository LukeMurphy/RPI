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

def pentagram(x, y, a = 1, n = 5, offset = 0, turn = 0) :
	pointArray = []
	theta = 2*math.pi / n
	theta2 = 2*math.pi/4 - theta
	angleOffset = 0
	if turn ==0 : angleOffset = theta/ (n - 1)

	d = a * math.cos(theta2) / 2
	r = a / (2 * math.cos(theta2))

	for nn in range (0,n) :
		xpt = x + math.cos(nn * theta - angleOffset + offset) * r
		ypt = y + math.sin(nn * theta - angleOffset + offset) * r
		pointArray.append((xpt,ypt))

	return (pointArray,d)






def drawPattern():

	draw = config.draw


	config.f1.stepTransition()
	config.f2.stepTransition()
	config.f3.stepTransition()
	config.f4.stepTransition()
	config.f5.stepTransition()
	config.f6.stepTransition()

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

	x = 100
	y = 100
	a = 50
	n = 5
	offset = 0
	theta = 2*math.pi/n
	theta2 = 2*math.pi/4 - theta

	box = pentagram(x, y, a, n, offset)
	draw.polygon(box[0], fill = f1)

	d = box[1] 

	offset = 2*math.pi/4 - theta
	for i in range(0,n) :

		x1 = x + math.cos(theta2) * d * 2
		y1 = y + math.sin(theta2) * d * 2

		offset += theta
		theta2 += theta

		f = f2
		if i == 0 : f= f3

		box = pentagram(x1, y1, a, n, offset, 1)
		draw.polygon(box[0], fill = f)
		draw.rectangle((x,y,x+3,y+3), fill="red")
		
		offset2 = math.pi/n + offset
		theta2b = 2*math.pi/4 - theta2

		if i == 1 :
			for ii in range(i,n) :

				x2 = x1 + math.cos(theta2b) * d * 2 
				y2 = y1 + math.sin(theta2b) * d * 2

				offset2 += theta
				theta2b += theta

				f = f4
				#if ii == 0 : f= f5

				box = pentagram(x2, y2, a, n, offset2, 0)
				#draw.polygon(box[0], fill = f)
				draw.rectangle((x2,y2,x2+3,y2+3), fill="red")

	'''
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


	




