import time
import random
import textwrap
import math
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageEnhance, ImageChops
from modules import colorutils, badpixels, coloroverlay

class unit:
	def __init__(self, config):
		self.config = config
		self.xPos = 0
		self.yPos = 0
		self.xPosR = self.config.screenWidth/2
		self.yPosR = self.config.screenHeight/2
		
		self.dx = random.uniform(-3,3)
		self.dy = random.uniform(-3,3)

		self.image = Image.new("RGBA", (100 , 100))
		self.fillColor = colorutils.getRandomRGB()
		self.outlineColor = colorutils.getRandomRGB()
		self.objWidth = 20
		self.objWidthMax = 26
		self.objWidthMin = 13

		self.draw  = ImageDraw.Draw(self.image)

	def update(self):
		self.xPos += self.dx
		self.yPos += self.dy
		
		self.xPosR += self.dx
		self.yPosR += self.dy

		if(self.xPosR + self.objWidth > self.config.screenWidth) : 
			self.xPosR = self.config.screenWidth - self.objWidth 
			self.xPos = self.config.screenWidth - self.objWidth 
			self.changeColor()
			self.dx *= -1
		if(self.yPosR + self.objWidth> self.config.screenHeight) : 
			self.yPosR = self.config.screenHeight-self.objWidth 
			self.yPos = self.config.screenHeight-self.objWidth 
			self.changeColor()
			self.dy *= -1
		if(self.xPosR < 0) : 
			self.xPosR = 0
			self.xPos = 0
			self.changeColor()
			self.dx*= -1
		if(self.yPosR < 0) : 
			self.yPosR = 0
			self.yPos = 0
			self.changeColor()
			self.dy *= -1

		if(self.dx == 0 and self.dy == 0 ):
			if(random.random() > .5): self.dx = (2 * random.random())
			if(random.random() > .5): self.dy = (2 * random.random())

		xPos = int(self.xPosR)
		yPos = int(self.yPosR)

		self.config.draw.rectangle((xPos, yPos,xPos+ self.objWidth , yPos +self.objWidth ), fill=self.fillColor, outline=self.outlineColor)
	

	def changeColor(self):
		self.fillColor = colorutils.randomColor(random.random())
		self.outlineColor = colorutils.getRandomRGB()
		if(random.random() > .5): self.dx = (4 * random.random() + 2)
		if(random.random() > .5): self.dy = (4 * random.random() + 2)
		if(random.random() > .5): self.objWidth = int(random.uniform(self.objWidthMin,self.objWidthMax))


def main(run = True) :
	global config, directionOrder
	print("---------------------")
	print("Diag Loaded")
	colorutils.brightness = config.brightness
	config.canvasImageWidth = config.screenWidth
	config.canvasImageHeight = config.screenHeight
	config.canvasImageWidth -= 4
	config.canvasImageHeight -= 4
	config.delay = .01
	config.numUnits  = 4

	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

	config.canvasImage = Image.new("RGBA", (config.canvasImageWidth  , config.canvasImageHeight))

	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
	config.unitArrray = []
	for i in range(0,config.numUnits):
		config.unitArrray.append(unit(config))

	setUp()

	if(run) : runWork()


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def setUp():
	global config
	pass



''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def runWork():
	global blocks, config, XOs
	#gc.enable()
	while True:
		iterate()
		time.sleep(config.delay)  

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def iterate() :
	global config
	for i in range(0,config.numUnits):
		config.unitArrray[i].update()


	config.render(config.image, 0,0)
		


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def callBack() :
	global config, XOs
	return True

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''



