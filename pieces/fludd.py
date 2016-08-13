# ################################################### #
import time
import random
import math
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageEnhance
from modules import colorutils

redrawSpeed = .005
lastRate  = 0 

class Fludd :

	outlineColor = (1,1,1)
	barColor = (200,200,000)
	barColorStart = (0,200,200)
	holderColor = (0,0,0)
	messageClr = (200,0,0)
	shadowColor = (0,0,0)

	spinnerAngle = 0
	spinnerAngleSteps = 16
	spinnerCenter = (0,0)
	spinnerRadius = 8
	spinnerInnerRadius = 5

	xPos = 1
	yPos = 1
	boxHeight = 0
	boxWidth = 0
	boxWidthDisplay = 0
	status = 0
	boxMax = 0
	rateMultiplier = .1
	rate = rateMultiplier * random.random()
	numRate = rate
	percentage = 0
	boxMaxAlt = 0


	def __init__(self, config):
		print ("init PB")
		
		self.boxMax = config.screenWidth - 2
		self.boxMaxAlt = self.boxMax + int(random.uniform(10,30) * config.screenWidth)
		self.boxHeight = config.screenHeight - 3
		self.spinnerCenter = (self.boxMax - 60, self.boxHeight/2 + 4)
		self.config = config

		tempImage = Image.new("RGBA", (1200,196))
		draw  = ImageDraw.Draw(tempImage)
		self.mainImage = Image.new("RGBA", (config.screenWidth, config.screenHeight))
		
	def changeAction(self):
		return False


	def reDraw(self) :

		xPos1 = 0
		yPos1 = 100
		xPos2 = 0
		yPos2 = 100

		# Draw single left-most black line
		config.draw.rectangle((0, yPos1, 1, yPos2), fill=(0,0,0) )
		
		# draw flat box progress bar - default
		config.draw.rectangle((xPos1, yPos1, xPos2, yPos2), fill=(200,0,0) )

		# Finally composite full image
		config.image.paste(self.scrollImage, (numXPos, numYPos), self.scrollImage)


	def drawBar(self) :
		config = self.config
		config.draw.rectangle((self.xPos,self.yPos,self.boxWidth+self.xPos,self.boxHeight+self.yPos), outline=(self.outlineColor), fill=(self.barColor) )

	def done(self): 
		return True


def drawElement() :
	global config
	return True

def redraw():
	global config, pBar
	fluddSquare.reDraw()

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
	global config, fluddSquare, lastRate
	
	redraw()
	config.render(config.image, 0, 0, config.screenWidth, config.screenHeight)

	callBack()
	count = 0
	# Done

def main(run = True) :
	global config
	global redrawSpeed
	global fluddSquare

	fluddSquare = ProgressBar(config)
	config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	config.draw  = ImageDraw.Draw(config.image)
	if(run) : runWork()
		

