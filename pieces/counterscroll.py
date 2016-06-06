import time
import random
import textwrap
import math
from PIL import ImageFont, Image, ImageDraw
from modules import colorutils, badpixels


class ScrollMessage :

	########################
	#scroll speed and steps per cycle
	scrollSpeed = 0.0006
	steps = 4
	fontSize = 14


	def __init__(self, messageString, direction, config) :
		#print ("init: " + messageString)
		self.messageString = messageString
		self.direction = direction

		config.fontSize = int(workConfig.get("stroop", 'fontSize'))
		config.vOffset = int(workConfig.get("scroll", 'vOffset'))
		config.scrollSpeed = float(workConfig.get("scroll", 'scrollSpeed'))
		config.shadowSize = int(workConfig.get("stroop", 'shadowSize'))

		self.config = config
		self.clr = colorutils.getRandomRGB()

		# draw the message to get its size
		font = ImageFont.truetype(config.path  + '/assets/fonts/freefont/FreeSerifBold.ttf', config.fontSize)
		tempImage = Image.new("RGBA", (1200,196))
		draw  = ImageDraw.Draw(tempImage)
		self.pixLen = draw.textsize(self.messageString, font = font)
		# For some reason textsize is not getting full height !
		self.fontHeight = int(self.pixLen[1] * 1.3)

		# make a new image with the right size
		self.config.renderImage = Image.new("RGBA", (config.actualScreenWidth , config.screenHeight))
		#self.scrollImage = Image.new("RGBA", pixLen)

		self.scrollImage = Image.new("RGBA", (self.pixLen[0] + 2 , self.fontHeight))
		self.draw  = ImageDraw.Draw(self.scrollImage)
		self.iid = self.scrollImage.im.id
		
		#self.draw.rectangle((0,0,self.pixLen[0]+4, self.pixLen[1]), fill = (0,0,0))
		self.draw.text((2,0),self.messageString, self.clr ,font=font)

		self.xPos = 0
		self.yPos = config.vOffset

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

class XOx :

	########################
	#scroll speed and steps per cycle
	scrollSpeed = 0.0006
	steps = 4
	lineThickness = 8
	bufferSpacing = 40
	xsWidth = 75

	def __init__(self, direction, config) :
		#print ("init: " + messageString)

		self.direction = direction
		config.scrollSpeed = float(workConfig.get("scroll", 'scrollSpeed'))

		self.config = config
		self.clr = (255,0,0)

		self.xoString =  self.makeBlock()

	def makeBlock(self) :
		strg = ""
		self.xPos = config.screenWidth + self.bufferSpacing
		self.yPos = 0

		num = int(random.uniform(3,10))
		for n in range (0, num) : 
			if (random.random() > .5) : strg += "X"
			else  : strg += "O"

		self.messageLength = n * self.xsWidth + self.bufferSpacing

		return strg

	def drawCounterXO(self) :
		## Try with drawing xo's first then by pasting block ..

		draw  = ImageDraw.Draw(self.config.renderImageFull)

		for n in range (0, len(self.xoString)):
			startX = self.xPos + n * self.xsWidth + 8
			endX = self.xPos + n * self.xsWidth + self.xsWidth
			startY = 0
			endY = self.xsWidth

			if (self.xoString[n]) ==  "X" :
				draw.line((startX, startY, endX, endY), fill = self.clr, width = self.lineThickness)
				draw.line((endX, startY, startX, endY), fill = self.clr, width = self.lineThickness)
			else :
				draw.ellipse((startX, startY, endX, endY),  outline=self.clr)
				draw.ellipse((startX +1, startY+1, endX-1, endY-1),  outline=self.clr)

		self.xPos -= 4


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def callBack() :
	global config, XOs, scroll
	XOs.drawCounterXO()
	if(XOs.xPos < -XOs.messageLength - XOs.bufferSpacing) :
		if(random.random() > .8 ) :
			XOs.xoString = XOs.makeBlock()
		else :
			XOs.xPos = config.screenWidth + XOs.bufferSpacing


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def makeBlock() :
	space = "  "
	strg = ""
	num = int(random.uniform(2,10))
	for n in range (0, num) : 
		strg += ":)"+space
		if (random.random() > .95) : strg += ":o"+space
		if (random.random() > .95) : strg += ";)"+space
	return strg


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def main(run = True) :
	global config, scroll, XOs

	print("CounterScroll Loaded")
	colorutils.brightness = config.brightness
	badpixels.config = config
	XOs = XOx("RIGHT", config)

	print (config.render)
	config.drawBeforeConversion = callBack

	setUp()
	if(run) : runWork()

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def setUp():
	global config, scroll, XOs, overlayImage

	#overlayImage = Image.new("RGBA", (config.actualScreenWidth , config.screenHeight))

	scroll = ScrollMessage(makeBlock(),"LEFT",config)
	scroll.end = config.screenWidth #+ scroll.scrollImage.size[0]
	scroll.start = -scroll.scrollImage.size[0]

	if(scroll.direction == "Right") : 
		scroll.start = -end
		scroll.end = config.screenWidth

	scroll.xPos = scroll.start

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def runWork():
	global blocks, config, scroll, XOs
	#gc.enable()
	while True:
		iterate()
		time.sleep(scroll.scrollSpeed)  

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def iterate() :
	global config, blocks, x, y, scroll
	if(scroll.direction == "Left") :
		scroll.xPos -= scroll.steps
	else :
		scroll.xPos += scroll.steps
	draw  = ImageDraw.Draw(config.renderImageFull)
	draw.rectangle((0,0,config.screenWidth, config.screenHeight), fill = 0)
	config.render(scroll.scrollImage, scroll.xPos, config.vOffset, scroll.pixLen[0], scroll.fontHeight, False)
	badpixels.drawBlanks()
	#config.updateCanvas()
	
	if(scroll.xPos > scroll.end) :
		if(random.random() > .5) :
			setUp()
		else :
			scroll.xPos = scroll.start = -scroll.scrollImage.size[0]

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''




