import time
import random
import math
import datetime
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageEnhance, ImageChops
from modules import colorutils, coloroverlay
import argparse


class Unit:

	origin = [64,32]
	points = []
	yVarMin = 1
	yVarMax = 10
	objWidth = 10
	objHeight = 10
	expRate = 1
	x0 = 0
	y0 = 0

	r = 200
	g = 200
	b = 200
	a = 100 #round(random.uniform(1,255))

	alphaInit = 0

	numLines = 60
	angleSpeed = 0
	angle = 0

	def __init__(self, config):
		self.config = config
		self.draw = self.config.canvasDraw

	def setUp(self):
		self.alphaInit = 0
		self.palletteCountOffset = 2
		self.fillColor = tuple((self.r,self.g,self.b))
		self.direction = 1 if random.random() < .5 else -1
		self.angleSpeed = self.direction * math.pi / self.angleRate


	def drawOval(self):
		#self.draw.ellipse((0, 0, round(self.objWidth/2) ,round(self.objHeight/2)), 
		#	fill=self.fillColor, outline=self.outlineColor)	
		self.angleRads  = math.pi/self.numLines	
		self.angle += self.angleSpeed

		pallette = [(255,0,0),(0,255,0),(0,0,255)]
		palletteCount = round(self.palletteCountOffset)

		for i in range (0,self.numLines) :
			xPos = -i*self.expRate + self.x0
			yPos = -i*self.expRate + self.y0

			self.r = round(math.sin(i * self.angleRads + self.angle) * 255)
			self.g = round(math.cos(math.pi + i * self.angleRads + self.angle) * 255)
			self.b = round(math.sin(math.pi + i * self.angleRads + 1 * self.angle) * 255)

			self.r = pallette[palletteCount][0]
			self.g = pallette[palletteCount][1]
			self.b = pallette[palletteCount][2]

			palletteCount += 1

			if palletteCount > 2 :
				palletteCount = 0


			if self.direction == -1 :
				self.a = round( self.alphaInit * (255 - (255 * i/self.numLines)))
			else :
				self.a = round(self.alphaInit * (255 - (255 * i/self.numLines)))
			self.fillColor = tuple((self.r,self.g,self.b,self.a))


			box = [(xPos,yPos),(self.objWidth/2 + i*self.expRate + self.x0, self.objHeight/2 + i*self.expRate + self.y0)] 
			self.draw.chord(box, 0, 360, fill =  None, outline=self.fillColor)

		if self.alphaInit < 1 :
			self.alphaInit += .1

		self.palletteCountOffset += .1
		if (self.palletteCountOffset > 2.5) :
			self.palletteCountOffset = 0
		#print(self.palletteCountOffset)


	
	def drawRectangle(self):
		self.draw.rectangle((0, 0, round(self.objWidth) ,round(self.objHeight)), 
			fill=None, outline=self.fillColor)


def showGrid():
	global config
	config.colOverlay.stepTransition()
	## Force sets the alpha
	config.colOverlay.currentColor[3] = 30

	config.bgColor  = tuple(int(a*config.brightness) for a in (config.colOverlay.currentColor))
	#config.bgColor  = (0,0,0,200)
	config.draw.rectangle((0,0,config.screenWidth, config.screenHeight), fill=config.bgColor, outline=(0,0,0))
	#config.canvasDraw.rectangle((0,0,config.screenWidth, config.screenHeight), fill=config.bgColor, outline=(0,0,0))
	for i in range(0,config.numUnits):
		obj = config.unitArray[i]
		if(random.random() < .000001) :
			obj.x0 = config.canvasWidth * random.random()
			obj.y0 = config.canvasHeight * random.random()
			obj.numLines = round(random.uniform(5,30))
			obj.angleRate = round(random.uniform(20,100))
			obj.expRate = round(random.uniform(2,4))
			obj.setUp()
		obj.drawOval()
	
	config.image.paste(config.canvasImage, (config.imageXOffset, config.imageYOffset), config.canvasImage)
	config.render(config.image, 0,0)


def main(run = True) :
	global config, directionOrder
	print("---------------------")
	print("Concentrics Loaded")

	colorutils.brightness = config.brightness
	config.image = Image.new("RGBA", (config.screenWidth  , config.screenHeight))
	config.draw = ImageDraw.Draw(config.image)
	config.canvasImage = Image.new("RGBA", (config.canvasWidth  , config.canvasHeight))
	config.canvasDraw = ImageDraw.Draw(config.canvasImage)

	config.colOverlay = coloroverlay.ColorOverlay()
	config.colOverlay.randomSteps = False 
	config.colOverlay.timeTrigger = True 
	config.colOverlay.tLimitBase = 5
	config.colOverlay.maxBrightness = config.brightness
	config.colOverlay.steps = 50
	config.delay = float(workConfig.get("concentrics", 'delay'))
	config.numUnits = int(workConfig.get("concentrics", 'numUnits'))
	
	'''
	config.colOverlay.minHue = float(workConfig.get("screenproject", 'minHue'))
	config.colOverlay.maxHue = float(workConfig.get("screenproject", 'maxHue'))
	config.colOverlay.minSaturation = float(workConfig.get("screenproject", 'minSaturation'))
	config.colOverlay.maxSaturation= float(workConfig.get("screenproject", 'maxSaturation'))
	config.colOverlay.minValue = float(workConfig.get("screenproject", 'minValue'))
	config.colOverlay.maxBrightness = float(workConfig.get("screenproject", 'maxBrightness'))
	config.colOverlay.maxValue = float(workConfig.get("screenproject", 'maxValue'))
	'''

	config.unitArray = []
	for i in range(0,config.numUnits):
		obj = Unit(config)

		obj.x0 = config.canvasWidth * random.random()
		obj.y0 = config.canvasHeight * random.random()
		obj.numLines = round(random.uniform(5,30))
		obj.angleRate = round(random.uniform(60,100))
		obj.expRate = round(random.uniform(2,4))
		obj.setUp()
		config.unitArray.append(obj)

	setUp()

	if(run) : runWork()


def setUp():
	global config


def runWork():
	global config
	while True:
		iterate()
		time.sleep(config.delay)  


def iterate() :
	global config
	showGrid()


def callBack() :
	global config
	return True


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


	




