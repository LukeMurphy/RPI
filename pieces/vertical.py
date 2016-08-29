# ################################################### #
import time
import random
import math
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageEnhance
from modules import colorutils

redrawSpeed = .005
lastRate  = 0 
colorutils.brightness =  1
blockHeight = 8 

class Vertical :

	outerColor = (0,0,50)
	innerColor = (180,50,000)
	borderColor = (50,0,0)

	xPos = 0
	yPos = 0
	vOffset = 0
	boxHeight = 0
	boxWidth = 0
	boxWidthDisplay = 0
	status = 0
	boxMax = 0
	rateMultiplier = .1
	rate = rateMultiplier * random.random()
	h = 8
	var = 2

	def __init__(self, config):

		self.boxMax = config.screenWidth - 1
		self.boxMaxAlt = self.boxMax + int(random.uniform(10,30) * config.screenWidth)
		self.boxHeight = config.screenHeight - 2
		self.config = config
		self.h = config.blockHeight

		#self.borderModel = workConfig.get("fludd", 'borderModel')

		self.unitImage = Image.new("RGBA", (config.screenWidth,self.h))
		self.draw  = ImageDraw.Draw(self.unitImage)

		self.CenterWidth = int(self.boxMax * config.widthPercentage)
		self.BorderWidth = 2
		self.OuterWidth = int(self.boxMax/2 - self.CenterWidth/2 - self.BorderWidth)

	def changeAction(self):
		return False

	def make(self):
		self.outer1 = (self.xPos,self.yPos, int(random.uniform(-self.var,+self.var) + self.OuterWidth) + 1, self.yPos + self.h)
		self.border1 = (self.outer1[2],self.yPos, self.outer1[2] + int(random.uniform(-1,1) + self.BorderWidth) + 1, self.yPos + self.h)
		self.cntr = (self.border1[2],self.yPos, self.border1[2] + int(random.uniform(-self.var,+self.var) + self.CenterWidth)  + 1, self.yPos + self.h)
		self.border2 = (self.cntr[2],self.yPos, self.cntr[2] + int(random.uniform(0,2) + self.BorderWidth) + 1, self.yPos + self.h)
		self.outer2= (self.border2[2],self.yPos, self.boxMax, self.yPos + self.h)

	def reDraw(self) :
		self.draw.rectangle(self.outer1, fill = self.outerColor)
		self.draw.rectangle(self.border1, fill = self.borderColor)
		self.draw.rectangle(self.cntr, fill = self.innerColor)
		self.draw.rectangle(self.border2, fill = self.borderColor)
		self.draw.rectangle(self.outer2, fill = self.outerColor)
		config.image.paste(self.unitImage, (0, self.vOffset), self.unitImage )


	def done(self): 
		return True


def drawElement() :
	global config
	return True

def redraw():
	global config, vertArray
	for i in range(0,len(vertArray)):
		vert = vertArray[i]
		vert.reDraw()
	reArraynge()

def reArraynge():
	global config, vertArray
	lastElement = vertArray.pop()
	lastElement.make()
	vertArray.insert(0,lastElement)
	layers = int(config.screenHeight / config.blockHeight)
	for i in range (0,layers):
		vertArray[i].vOffset = i * config.blockHeight

def changeColor() :
	pass
	return True

def changeCall() :
	pass
	return True

def callBack() :
	global config
	pass

def runWork():
	global redrawSpeed
	while True:
		iterate()
		time.sleep(redrawSpeed)

def iterate() :
	global config, vert, lastRate
	
	redraw()
	config.render(config.image, 0, 0, config.screenWidth, config.screenHeight)

	callBack()
	count = 0
	# Done

def main(run = True) :
	global config, workConfig
	global redrawSpeed
	global vert, vertArray
	vertArray = []
	config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	config.draw  = ImageDraw.Draw(config.image)
	config.blockHeight = 8
	config.vOffset = int(workConfig.get("vertical", 'vOffset'))
	config.widthPercentage = float(workConfig.get("vertical", 'widthPercentage'))

	layers = int(config.screenHeight / config.blockHeight)
	for i in range (0,layers):
		vert = Vertical(config)
		vert.make()
		vert.vOffset = i * config.blockHeight
		vertArray.append(vert)
	if(run) : runWork()
		

