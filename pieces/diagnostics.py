import time
import random
import textwrap
import math
import datetime
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageEnhance, ImageChops
from modules import colorutils, badpixels, coloroverlay

class unit:
	def __init__(self, config):
		self.config = config
		self.xPos = 0
		self.yPos = 0
		self.xPosR = self.config.screenWidth/2
		self.yPosR = self.config.screenHeight/2
		self.move = True
		
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

	
	def render(self):
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
	config.delay = .02
	config.numUnits  = 1

	config.fontColorVals = ((workConfig.get("diag", 'fontColor')).split(','))
	config.fontColor = tuple(map(lambda x: int(x) , config.fontColorVals))
	config.outlineColorVals = ((workConfig.get("diag", 'outlineColor')).split(','))
	config.outlineColor = tuple(map(lambda x: int(x) , config.outlineColorVals))


	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

	config.canvasImage = Image.new("RGBA", (config.canvasImageWidth  , config.canvasImageHeight))
	config.fontSize = 14
	config.font = ImageFont.truetype(config.path  + '/assets/fonts/freefont/FreeSansBold.ttf', config.fontSize)
	

	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
	config.unitArrray = []
	for i in range(0,config.numUnits):
		obj = unit(config)
		#obj.move = False
		obj.objWidth = 5
		obj.objWidthMax = 4
		obj.objWidthMin = 3
		config.unitArrray.append(obj)

	setUp()

	if(run) : runWork()


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def setUp():
	global config

	'''
	arg = "./assets/imgs/"
	testImage = Image.open(arg , "r")
		self.image.load()
		self.imgHeight =  self.image.getbbox()[3]
	'''

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
	#config.draw.rectangle((0,0,config.screenWidth, config.screenHeight), fill=(0,0,0), outline=(0,0,0))
	config.draw.rectangle((0,0,config.screenWidth-1, config.screenHeight-1), fill=(0,0,0), outline=config.outlineColor)
	config.draw.text((10,10),"TOP",config.fontColor,font=config.font)
	tm = datetime.datetime.now()
	tm = time.ctime()
	config.draw.text((10,24),tm,config.fontColor,font=config.font)


	
	for i in range(0,config.numUnits):
		obj = 	config.unitArrray[i]
		if(obj.move ==True) : obj.update()
		obj.render()
	
	config.render(config.image, 0,0)
		


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def callBack() :
	global config, XOs
	return True

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''



