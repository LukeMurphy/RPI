# ################################################### #
import time
import random
import math
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageEnhance
from modules import colorutils

redrawSpeed = .001

class ProgressBar :

	outlineColor = (100,100,100)
	barColor = (0,0,200)
	xPos = 0
	yPos = 0
	boxHeight = 0
	boxWidth = 0
	status = 0
	boxMax = 0
	rate = 2
	pauses = 300
	pauseCount = 0

	def __init__(self, config):
		print ("init PB")
		
		self.boxMax = config.screenWidth - 2
		self.boxHeight = config.screenHeight - 3
		self.holderColor = (5,5,5)
		self.xPos = 1
		self.yPos = 1

		config.fontSize = int(workConfig.get("progressbar", 'fontSize'))
		config.vOffset = int(workConfig.get("progressbar", 'vOffset'))
		config.scrollSpeed = float(workConfig.get("progressbar", 'scrollSpeed'))
		config.steps = int(workConfig.get("progressbar", 'steps'))
		config.shadowSize = int(workConfig.get("progressbar", 'shadowSize'))
		config.sansSerif = (workConfig.getboolean("progressbar", 'sansSerif'))
		if(config.sansSerif) : 
			self.font = ImageFont.truetype(config.path  + '/assets/fonts/freefont/FreeSansBold.ttf', config.fontSize)
		else :
			self.font = ImageFont.truetype(config.path  + '/assets/fonts/freefont/FreeSerifBold.ttf', config.fontSize)
		self.config = config

		self.messageString = "100%"
		tempImage = Image.new("RGBA", (1200,196))
		draw  = ImageDraw.Draw(tempImage)
		self.pixLen = draw.textsize(self.messageString, font = self.font)
		# For some reason textsize is not getting full height !
		self.fontHeight = int(self.pixLen[1] * 1.3)
		self.scrollImage = Image.new("RGBA", (self.pixLen[0] + 2 , self.fontHeight))
		self.txtdraw  = ImageDraw.Draw(self.scrollImage)
		self.clr = (255,255,255)

	def reDraw(self) :

		self.boxWidth += self.rate
		percentage  =  (float(self.boxWidth)/float(self.boxMax)*100)
		pauseProbability = math.exp(percentage/10) / 40000

		displayPercentage  = int(math.ceil(percentage))
		self.messageString = str(displayPercentage) + "%"

		
		if(random.random() < pauseProbability and self.pauseCount < self.pauses) : 
			self.rate = 0
			self.pauseCount += 1
		

		if(random.random() > .95) : self.rate = random.random()
		
		indent  =  0
		# draw box container
		config.draw.rectangle((self.xPos-1, self.yPos-1, self.boxMax+1, self.boxHeight+self.yPos+1), 
			outline=(self.outlineColor), fill=(self.holderColor) )
		# draw bar
		config.draw.rectangle((self.xPos, self.yPos, self.boxWidth+self.xPos, self.boxHeight+self.yPos), 
			 fill=(self.barColor) )

		#self.txtdraw.rectangle((0,0,self.scrollImage.width, self.scrollImage.height), fill=(0,0,0))
		self.scrollImage = Image.new("RGBA", (self.pixLen[0] + 2 , self.fontHeight))
		self.txtdraw  = ImageDraw.Draw(self.scrollImage)
		for i in range(1, self.config.shadowSize + 1) :
			self.txtdraw.text((indent + -i,-i),self.messageString,(0,0,0),font=self.font)
			self.txtdraw.text((indent + i,i),self.messageString,(0,0,0),font=self.font)
			self.txtdraw.text((0,0),self.messageString, self.clr ,font=self.font)
		config.image.paste(self.scrollImage, (self.boxMax - self.pixLen[0] - 4,24), self.scrollImage)

		if(percentage >= 100) :
			time.sleep(int(random.random() * 10))
			self.done()

	def drawBar(self) :
		config = self.config
		config.draw.rectangle((self.xPos,self.yPos,self.boxWidth+self.xPos,self.boxHeight+self.yPos), outline=(self.outlineColor), fill=(self.barColor) )

	def done(self):
		self.pauseCount = 0
		self.boxWidth = 1
		self.rate = 2

def drawElement() :
	global config
	return True


def redraw():
	global config, pBar
	pBar.reDraw()


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
	global config
	redraw()
	config.render(config.image, 0, 0, config.screenWidth, config.screenHeight)
	callBack()
	count = 0
	# Done

def main(run = True) :
	global config
	global redrawSpeed
	global pBar
	pBar = ProgressBar(config)

	print("Template Loaded")
	config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	config.draw  = ImageDraw.Draw(config.image)
	if(run) : runWork()
		

