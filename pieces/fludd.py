# ################################################### #
import time
import random
import math
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageEnhance
from modules import colorutils

redrawSpeed = .005
lastRate  = 0 
colorutils.brightness =  1

class Fludd :

	outlineColor = (1,1,1)
	barColor = (200,200,000)
	barColorStart = (0,200,200)
	holderColor = (0,0,0)
	messageClr = (200,0,0)
	shadowColor = (0,0,0)


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
	var = 10

	nothingLevel = 10
	nothingChangeProbability = .02

	borderModel = "prism"
	nothing = "void"
	varianceMode = "independent"
	prisimBrightness = .5


	def __init__(self, config):
		print ("init PB")
		
		self.boxMax = config.screenWidth - 1
		self.boxMaxAlt = self.boxMax + int(random.uniform(10,30) * config.screenWidth)
		self.boxHeight = config.screenHeight - 2
		self.config = config

		tempImage = Image.new("RGBA", (640,640))
		draw  = ImageDraw.Draw(tempImage)
		self.mainImage = Image.new("RGBA", (config.screenWidth, config.screenHeight))

		
	def changeAction(self):
		return False


	def reDraw(self) :
		var = self.var

		gray = 126
		brightness = self.config.brightness * random.random()
		light = int(brightness*self.nothingLevel)

		if self.nothing == "void" :
			gray = 0
		else :
			gray = int(self.config.brightness * random.random()*self.nothingLevel/2)
			light = 0


		config.draw.rectangle((0,0,self.boxMax,self.boxHeight), fill = (0,0,0))
		#config.draw.rectangle((0,0,self.boxMax,self.boxHeight), fill = (light,light,light))
		if(self.borderModel == "prism"):
			outerBorder = colorutils.randomColor(self.prisimBrightness)
		else :
			outerBorder = (light,light,light)

		config.draw.rectangle((0,0,self.boxMax,self.boxHeight), fill = outerBorder)

		if(self.varianceMode == "independent") : 
			xPos1 = random.uniform(-var/2,var)
			yPos1 = random.uniform(-var/2,var)

			xPos2 = random.uniform(self.boxMax-var,self.boxMax+var)
			yPos2 = random.uniform(-var/2,var)	

			xPos3 = random.uniform(self.boxMax-var,self.boxMax+var)
			yPos3 = random.uniform(self.boxHeight-var,self.boxHeight+var)

			xPos4 = random.uniform(-var/2,var)
			yPos4 = random.uniform(self.boxHeight-var,self.boxHeight+var)

			config.draw.polygon((xPos1, yPos1, xPos2, yPos2, xPos3, yPos3, xPos4, yPos4), fill=(gray, gray, gray) )

		elif(self.varianceMode == "symmetrical"):
			svar = random.uniform(0, var)
			symBoxWidth = self.boxMax - svar
			symBoxHeight = self.boxHeight - svar
			xy0 = svar
			
			config.draw.rectangle((xy0,xy0,symBoxWidth,symBoxHeight), fill=(gray, gray, gray) )
	
		elif(self.varianceMode == "asymmetrical"):
			svarw = random.uniform(0, var)
			svarh = random.uniform(0, var)
			symBoxWidth = self.boxMax - svarw
			symBoxHeight = self.boxHeight - svarh
			xPos1 = (self.boxMax - symBoxWidth)
			yPos1 = (self.boxHeight  - symBoxHeight)
			config.draw.rectangle((xPos1,yPos1,symBoxWidth,symBoxHeight), fill=(gray, gray, gray) )

		if(random.random() < self.nothingChangeProbability) : self.nothingLevel = random.uniform(0,255)

		# Finally composite full image
		#config.image.paste(self.mainImage, (numXPos, numYPos), self.scrollImage)


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
	config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	config.draw  = ImageDraw.Draw(config.image)
	fluddSquare = Fludd(config)
	# Prism is all colors, Plenum is white
	fluddSquare.borderModel  = workConfig.get("fludd", 'borderModel')
	fluddSquare.nothing  = workConfig.get("fludd", 'nothing')
	fluddSquare.var  = int(workConfig.get("fludd", 'var'))
	fluddSquare.varianceMode  = workConfig.get("fludd", 'varianceMode')
	fluddSquare.prisimBrightness  = float(workConfig.get("fludd", 'prisimBrightness'))

	# var sets the points offset from the corners - i.e. the larger var is, the wider the borders
	'''
	************
	*           *
	 *           *
	  *          * 
	   ***********
        
	'''
	
	if(run) : runWork()
		

