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
	complete = False
	percentage = 0
	boxMaxAlt = 0 

	def __init__(self, config):
		print ("init PB")
		
		self.boxMax = config.screenWidth - 2
		self.boxMaxAlt = self.boxMax + int(random.uniform(1,3) * config.screenWidth)
		self.boxHeight = config.screenHeight - 3
		self.holderColor = (5,5,5)
		self.xPos = 1
		self.yPos = 1
		self.lastPause = False

		config.fontSize = int(workConfig.get("progressbar", 'fontSize'))
		config.vOffset = int(workConfig.get("progressbar", 'vOffset'))
		config.scrollSpeed = float(workConfig.get("progressbar", 'scrollSpeed'))
		config.steps = int(workConfig.get("progressbar", 'steps'))
		config.shadowSize = int(workConfig.get("progressbar", 'shadowSize'))
		config.sansSerif = (workConfig.getboolean("progressbar", 'sansSerif'))
		self.pauseAt99 = False
		self.pauseAt100 = False
		self.goBack = False
		self.goPast = False
		self.messageOverride = True
		self.messageOverrideActive = False

		if(config.sansSerif) : 
			self.font = ImageFont.truetype(config.path  + '/assets/fonts/freefont/FreeSansBold.ttf', config.fontSize)
		else :
			self.font = ImageFont.truetype(config.path  + '/assets/fonts/freefont/FreeSerifBold.ttf', config.fontSize)
		self.config = config

		self.messageString = "PLEASE WAIT. UPDATING..."
		tempImage = Image.new("RGBA", (1200,196))
		draw  = ImageDraw.Draw(tempImage)
		self.pixLen = draw.textsize(self.messageString, font = self.font)
		# For some reason textsize is not getting full height !
		self.fontHeight = int(self.pixLen[1] * 1.3)
		self.scrollImage = Image.new("RGBA", (self.pixLen[0] + 2 , self.fontHeight))
		self.txtdraw  = ImageDraw.Draw(self.scrollImage)
		self.clr = (255,255,255)

	def reDraw(self) :
		pauseProbability = math.exp(self.percentage/10) / 40000
		if(random.random() < pauseProbability and self.pauseCount < self.pauses) : 
			self.rate = 0
			self.pauseCount += 1
		
		if(random.random() > .98) : 
			self.rate = random.random() * 2

		if(self.goBack and random.random() > .98) :
			self.rate *= -1

		self.boxWidth += self.rate
		self.percentage  =  (float(self.boxWidth)/float(self.boxMax)*100)

		if(self.percentage >= 100 and self.goPast != True) : 
			self.boxWidth = self.boxMax - 1
			self.complete = True
		elif(self.percentage >= 100 and self.goPast and self.boxWidth >= self.boxMaxAlt) :
			self.complete = True

		self.displayPercentage = int(math.floor(self.percentage))
		if(self.messageOverrideActive != True) : self.messageString = str(self.displayPercentage) + "%"

		if(random.random() > .9 and self.messageOverride) :
			self.rate = 0
			self.messageString = "PLEASE WAIT. UPDATING..."
			self.messageOverrideActive = True

		if(random.random() > .999 ) : 
			self.messageOverride = False
			self.messageOverrideActive = False
			

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
		for i in range(1, self.config.shadowSize ) :
			self.txtdraw.text((indent + -i,-i),self.messageString,(0,0,0),font=self.font)
			self.txtdraw.text((indent + i,i),self.messageString,(0,0,0),font=self.font)
		self.txtdraw.text((0,0),self.messageString, self.clr ,font=self.font)

		numXPos = self.boxMax - self.pixLen[0] - 4

		numXPos = 32
		numYPos = 24

		config.image.paste(self.scrollImage, (numXPos, numYPos), self.scrollImage)


	def drawBar(self) :
		config = self.config
		config.draw.rectangle((self.xPos,self.yPos,self.boxWidth+self.xPos,self.boxHeight+self.yPos), outline=(self.outlineColor), fill=(self.barColor) )

	def done(self):
		self.pauseCount = 0
		self.boxWidth = 1
		self.rate = 2
		self.lastPause = False
		self.complete = False

		self.pauseAt99 = True if (random.random() > .8) else False
		self.pauseAt100 = True if (random.random() > .9) else False
		self.goBack = True if (random.random() > .9) else False
		self.goPast = True if (random.random() > .9) else False
		self.messageOverride = True if (random.random() > .98) else False
		self.messageOverrideActive = False

		if(self.goPast) : 
			self.pauseAt100 = False
			self.pauseAt99 = True
			self.goBack = False

		print(self.pauseAt100,self.pauseAt99,self.goBack,self.goPast)



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
	global config, pBar
	
	redraw()
	config.render(config.image, 0, 0, config.screenWidth, config.screenHeight)

	if(pBar.complete) : 
		if(pBar.pauseAt100) : time.sleep(int(random.uniform(3,10)))
		time.sleep(2)
		pBar.done()

	if(pBar.percentage >= 99 and pBar.percentage < 100 and pBar.pauseAt99 and pBar.pauseCount < pBar.pauses) :
		time.sleep(int(random.uniform(3,10)))
		pBar.pauseCount = pBar.pauses

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
		

