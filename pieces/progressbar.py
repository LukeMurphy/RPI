# ################################################### #
import time
import random
import math
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageEnhance
from modules import colorutils

redrawSpeed = .005
lastRate  = 0 

class ProgressBar :

	outlineColor = (1,1,1)
	barColor = (0,0,200)
	holderColor = (0,0,0)
	messageClr = (200,200,200)
	shadowColor = (0,0,50)

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
	target = 99

	completeProbability = 0.1
	completeProbabilityBase = 0.3
	multiplePauseProb = 0.33
	changeProbability = 0.002
	goBackwardsProb = 1
	goFwdProb = 0.5
	overrideMessagProb = 0.001
	noBarProb = 0.1
	noDoneProb = 0.3

	minSleep = 2
	maxSleep = 6

	pauses = 3
	pauseCount = 0
	firstRun = True
	complete = False
	paused = False
	hasPaused = False
	gradient = False
	gradientLevel = 2
	pausePoint = 50

	goBack = True
	goPast = False
	drawBarFill = True
	messageOverride = True
	messageOverrideActive = False
	lastPause = False

	altStringMessage = "PLEASE WAIT"

	def __init__(self, config):
		print ("init PB")
		
		self.boxMax = config.screenWidth - 2
		self.boxMaxAlt = self.boxMax + int(random.uniform(10,30) * config.screenWidth)
		self.boxHeight = config.screenHeight - 3

		config.fontSize = int(workConfig.get("progressbar", 'fontSize'))
		config.vOffset = int(workConfig.get("progressbar", 'vOffset'))
		config.scrollSpeed = float(workConfig.get("progressbar", 'scrollSpeed'))
		config.steps = int(workConfig.get("progressbar", 'steps'))
		config.shadowSize = int(workConfig.get("progressbar", 'shadowSize'))
		config.sansSerif = (workConfig.getboolean("progressbar", 'sansSerif'))

		self.pausePoint = int(random.random() * 100)

		if(config.sansSerif) : 
			self.font = ImageFont.truetype(config.path  + '/assets/fonts/freefont/FreeSansBold.ttf', config.fontSize)
		else :
			self.font = ImageFont.truetype(config.path  + '/assets/fonts/freefont/FreeSerifBold.ttf', config.fontSize)
		self.config = config

		self.messageString = "PLEASE WAIT. UPDATING"
		tempImage = Image.new("RGBA", (1200,196))
		draw  = ImageDraw.Draw(tempImage)
		self.pixLen = draw.textsize(self.messageString, font = self.font)
		# For some reason textsize is not getting full height !
		self.fontHeight = int(self.pixLen[1] * 1.3)
		self.scrollImage = Image.new("RGBA", (self.pixLen[0] + 2 , self.fontHeight))
		self.txtdraw  = ImageDraw.Draw(self.scrollImage)
		
	def changeAction(self):
		self.rate = random.random() * self.rateMultiplier
		# Chance that the rate changes and things start moving again
		if(self.hasPaused == True):
			self.paused = False

			# Chance things might go backwards
			if(self.goBack and random.random() < self.goBackwardsProb) : 
				self.rate *= -1

			# chance there will be yet another pause ....
			if(random.random() < self.multiplePauseProb) :
				timeLeft = 100 - self.pausePoint
				if (timeLeft >=1) :
					self.hasPaused = False
					self.pausePoint = self.pausePoint + int(random.uniform(1,timeLeft-1))

			# Chance bar will stop being displayed
			if(random.random() < self.noBarProb) :
				self.drawBarFill = False
				self.target = 100
				self.rate = 2 * random.random()

			# Chance that it will never get any further
			c = random.uniform(.001,1)
			if(c < self.completeProbability):
				#print("setting complete1", c, self.completeProbability)
				self.complete = True

	def reDraw(self) :
		'''
		pauseProbability = math.exp(self.percentage/10) / 40000
		pauseProbability = .99 if (pauseProbability < .7) else pauseProbability
		if(random.random() < pauseProbability  and self.rate != 0) : #and self.pauseCount < self.pauses
			self.rate = 0
			self.pauseCount += 1
		'''
		
		# Chance that someting changes
		if(random.random() < self.changeProbability) : 
			self.changeAction()

		# will not go backwards for long
		if(self.rate < 0 and random.random() < self.goFwdProb) :
			self.rate = random.random() * self.rateMultiplier
			#self.completeProbability = .9

		# Increment the bar width
		if(self.paused != True) :
			self.boxWidth += self.rate
			self.percentage  =  (float(self.boxWidth)/float(self.boxMax)*100)

		# Enact the pause
		if(self.percentage >= self.pausePoint and self.hasPaused == False) :
			self.paused = True
			
			if(self.pauseCount >= self.pauses) :
				self.hasPaused = True
			else :
				self.rate = 0
				self.pauseCount += 1

			# Chance the message will say something besides the percentage
			if(random.random() > .9 and self.messageOverride) :
				self.messageString = self.altStringMessage
				self.messageOverrideActive = True

		# Things have gone as far as they are going to go
		if(self.percentage >= self.target and self.goPast != True) : 
			if(random.random() < self.noDoneProb) :
				#print("not done...")
				self.changeAction()
			else :
				self.boxWidth = self.boxMax - 2
				#print("setting complete2")
				self.complete = True
			# Chance the bar changes color
			if(random.random() > .80) : 
				self.barColor = (0,200,0)
		# If it goes past
		elif(self.percentage >= 100 and self.goPast and self.boxWidth >= self.boxMaxAlt) :
			#print("setting complete3")
			self.complete = True
		elif(self.percentage >= 100 and self.goPast) :
			self.rate = 10

		# At or below zero
		if(self.rate < 0 and self.percentage <= 0 and self.paused != True) :
			#print("setting complete4")
			self.complete = True
			self.rate = 0
			self.percentage = 0
			self.boxWidth = 1
			self.barColor = (255,0,0)

		# Get the percentage to display	
		self.displayPercentage = int(math.floor(self.percentage))

		#if(self.complete) : print(self.percentage, self.complete)

		# Set the message to be the % to go
		if(self.messageOverrideActive != True) : 
			self.messageString = str(self.displayPercentage) + "%"

		indent  =  0
		# draw box container
		config.draw.rectangle((self.xPos-1, self.yPos-1, self.boxMax+1, self.boxHeight+self.yPos+1), 
			outline=(self.outlineColor), fill=(self.holderColor) )
		# draw bar
		
		# draw "gradient"
		if(self.drawBarFill) : self.boxWidthDisplay = self.boxWidth
		xPos1 = self.xPos
		xPos2 = self.boxWidthDisplay+self.xPos
		yPos1 = self.yPos
		yPos2 = self.boxHeight+self.yPos

		config.draw.rectangle((xPos1, yPos1, xPos2, yPos2), fill=(self.barColor) )
		lines = config.screenHeight-2
		

		if (self.gradientLevel == 1) : arc = math.pi / lines * .6 
		else : arc = math.pi / lines 

		if(self.gradient):
			for n in range(0, lines) :
				yPos = yPos1 + n
				b = math.sin(arc * n)
				barColor = (int(self.barColor[0] * b), int(self.barColor[1] * b), int(self.barColor[2] * b))
				config.draw.rectangle((xPos1, yPos, xPos2, yPos), fill=(barColor) )


		#self.txtdraw.rectangle((0,0,self.scrollImage.width, self.scrollImage.height), fill=(0,0,0))
		self.scrollImage = Image.new("RGBA", (self.pixLen[0] + 2 , self.fontHeight))
		self.txtdraw  = ImageDraw.Draw(self.scrollImage)
		for i in range(1, self.config.shadowSize ) :
			self.txtdraw.text((indent + -i,-i),self.messageString,self.shadowColor,font=self.font)
			self.txtdraw.text((indent + i,i),self.messageString,self.shadowColor,font=self.font)
		self.txtdraw.text((0,0),self.messageString, self.messageClr ,font=self.font)

		#numXPos = config.screenWidth - self.pixLen[0] - 4
		#
		numXPos = 32
		numYPos = 24
		#numXPos = int(xPos2 - 40)

		config.image.paste(self.scrollImage, (numXPos, numYPos), self.scrollImage)


	def drawBar(self) :
		config = self.config
		config.draw.rectangle((self.xPos,self.yPos,self.boxWidth+self.xPos,self.boxHeight+self.yPos), outline=(self.outlineColor), fill=(self.barColor) )

	def done(self):
		self.pauseCount = 0
		self.boxWidth = 1
		self.rate = self.rateMultiplier * random.random()
		self.numRate = self.rate
		self.firstRun = True
		self.lastPause = False
		self.complete = False
		self.completeProbability = self.completeProbabilityBase
		self.drawBarFill = True
		self.target = 99

		self.goBack = True if (random.random() > .9) else False
		self.goPast = True if (random.random() > .98) else False
		self.messageOverride = True if (random.random() < .1) else False
		self.messageOverrideActive = False
		self.altStringMessage = "PLEASE WAIT" if (random.random() > .5) else "UPDATING"
		self.pausePoint = int(random.random() * 100)
		self.hasPaused = False
		self.paused = False
		self.barColor = (0,0,200)
		if(self.goPast) : self.goBack = False


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
	global config, pBar, lastRate
	
	redraw()
	config.render(config.image, 0, 0, config.screenWidth, config.screenHeight)

	if(pBar.rate != lastRate) :
		#print (pBar.rate)
		lastRate = pBar.rate

	if(pBar.firstRun) :
		time.sleep(int(random.uniform(pBar.minSleep,pBar.maxSleep)))
		pBar.firstRun = False

	if(pBar.complete) : 
		time.sleep(int(random.uniform(pBar.minSleep,pBar.maxSleep)))
		pBar.done()

	callBack()
	count = 0
	# Done

def main(run = True) :
	global config
	global redrawSpeed
	global pBar

	pBar = ProgressBar(config)
	config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	config.draw  = ImageDraw.Draw(config.image)
	if(run) : runWork()
		

