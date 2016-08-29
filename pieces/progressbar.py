import time
import random
import math
import threading
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageEnhance
from modules import colorutils

redrawSpeed = .005
lastRate  = 0 

firstRunCount = 0
completeCount = 0
firstRunCountLim = 0
completeCountLim = 0

class ProgressBar :

	outlineColor = (1,1,1)
	barColorEnd = (200,200,0)
	barColorStart = (0,200,200)
	barColorBase = (200,0,0)
	holderColor = (0,0,0)
	messageClr = (200,0,0)
	shadowColor = (0,0,0)

	spinnerAngle = 0
	spinnerAngleSteps = 16
	spinnerCenter = (11,0)
	spinnerRadius = 9
	spinnerInnerRadius = 7

	xPos = 1
	yPos = 1
	boxHeight = 0
	boxWidth = 0
	boxWidthDisplay = 0
	status = 0
	boxMax = 0

	percentage = 0
	boxMaxAlt = 0
	target = 99

	#### This really controls the progress bar rate
	rateMultiplier = .8
	rate = rateMultiplier * random.random()
	numRate = rate

	completeProbability = 0.1
	completeProbabilityBase = 0.3
	multiplePauseProb = 0.33
	changeProbability = 0.002
	goBackwardsProb = 1
	goFwdProb = 0.5
	overrideMessagProb = 0.04
	messageOverrideProbability = .32
	noBarProb = 0.1
	noDoneProb = 0.3


	minSleep = 10
	maxSleep = 12

	pauses = 3
	pauseCount = 0
	firstRun = True
	complete = False
	paused = False
	hasPaused = False
	gradient = False
	gradientLevel = 1
	pausePoint = 50

	goBack = True
	goPast = False
	drawBarFill = True
	messageOverride = True
	messageOverrideActive = False
	lastPause = False

	altStringMessage = "PLEASE WAIT"
	colorutils.brightness = 1



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
		self.colorGradient = (workConfig.getboolean("progressbar", 'useColorGradient'))
		self.gradient = (workConfig.getboolean("progressbar", 'useThreeD'))
		self.pausePoint = int(random.random() * 100)

		self.cyclicalArc = 4 * math.pi / self.boxMax
		self.cyclicalBrightnessPhase = 0
		self.spinnerCenter = (self.boxMax - 54, self.boxHeight/2 + 3)

		if(config.sansSerif) : 
			self.font = ImageFont.truetype(config.path  + '/assets/fonts/freefont/FreeSansBold.ttf', config.fontSize)
		else :
			self.font = ImageFont.truetype(config.path  + '/assets/fonts/freefont/FreeSerifBold.ttf', config.fontSize)
		self.config = config

		self.messageString = self.altStringMessage
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
			if(random.random() < self.messageOverrideProbability and self.messageOverride) :
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
			barColor = (255,0,0)

		# Get the percentage to display	
		#self.messageClr = (200, int(200 * self.percentage/100), int(200 * self.percentage/100))
		if(self.percentage >= 2) : 
			self.messageClr = (200,200,200)
			barColor = self.barColorStart
		else :
			self.messageClr = (200,0,0)
			barColor = (200,0,0)

		self.displayPercentage = int(math.floor(self.percentage))

		#if(self.complete) : print(self.percentage, self.complete)

		# Set the message to be the % to go
		if(self.messageOverrideActive != True) : 
			self.messageString = str(self.displayPercentage) + "%"


		'''''''''''''''''' ''' BOX AND BAR '''''''''''''''''''''''''''''''''	

		# draw box container
		config.draw.rectangle((self.xPos-1, self.yPos-1, self.boxMax+1, self.boxHeight+self.yPos+1), 
			outline=(self.outlineColor), fill=(self.holderColor) )
		# draw bar
		
		# draw flat box progress bar
		if(self.drawBarFill) : self.boxWidthDisplay = self.boxWidth
		xPos1 = self.xPos
		xPos2 = self.boxWidthDisplay+self.xPos
		yPos1 = self.yPos
		yPos2 = self.boxHeight+self.yPos
		
		# Draw single left-most black line
		config.draw.rectangle((0, yPos1, 1, yPos2), fill=(0,0,0) )
		
		# draw flat box progress bar - default
		config.draw.rectangle((xPos1, yPos1, xPos2, yPos2), fill=(200,0,0) )

		lines = config.screenHeight-2
		if (self.gradientLevel == 1) : arc = math.pi / lines * 1
		else : arc = math.pi / lines 

		if(self.gradient) :
		# Draw vertical shading gradient "3D!"
			for n in range(0, lines) :
				yPos = yPos1 + n
				b = math.sin(arc * n) * 1.2
				#b = cyclicalBrightness
				rVd = int(barColor[0] * b)
				gVd = int(barColor[1] * b)
				bVd = int(barColor[2] * b)
				barColorDisplay = (rVd, gVd, bVd)
				config.draw.rectangle((xPos1, yPos, xPos2, yPos), fill=(barColorDisplay) )
		
		elif(self.colorGradient):
			# Draw horizontal color gradient bar
			vLines = int(xPos2 - xPos1)
			dR = ((self.barColorEnd[0] - self.barColorStart[0])/(vLines+1))
			dG = ((self.barColorEnd[1] - self.barColorStart[1])/(vLines+1))
			dB = ((self.barColorEnd[2] - self.barColorStart[2])/(vLines+1))
			for p in range (0, vLines) :
				xPos1p = xPos1 + p
				xPos2p = xPos1p + 1
				#cyclicalBrightness = abs(math.sin(self.cyclicalArc * self.cyclicalBrightnessPhase * self.boxMax/vLines))+.1
				#cyclicalBrightness = 1
				#print(cyclicalBrightness)
				rV = int(self.barColorStart[0] + p * dR )
				gV = int(self.barColorStart[1] + p * dG )
				bV = int(self.barColorStart[2] + p * dB )

				# Draw vertical shading gradient "3D!"
				for n in range(0, lines) :
					yPos = yPos1 + n
					b = math.sin(arc * n)
					#b = cyclicalBrightness
					rVd = int(rV * b)
					gVd = int(gV * b)
					bVd = int(bV * b)
					barColor = (rVd, gVd, bVd)
					config.draw.rectangle((xPos1p, yPos, xPos2p, yPos), fill=(barColor) )

		'''''''''''''''''' ''' TEXT MESSAGE '''''''''''''''''''''''''''
		self.drawMessageText()

		'''''''''''''''''' ''' SPINNER '''''''''''''''''''''''''''''''''
		self.drawSpinner()
			
	def drawMessageText(self) :
		# Draw the message percentage
		indent  =  4
		self.scrollImage = Image.new("RGBA", (self.pixLen[0] + 2 * indent , self.fontHeight + 2 * indent))
		self.txtdraw  = ImageDraw.Draw(self.scrollImage)
		for i in range(1, self.config.shadowSize ) :
			self.txtdraw.text((indent + -i,-i),self.messageString,self.shadowColor,font=self.font)
			self.txtdraw.text((indent + i,i),self.messageString,self.shadowColor,font=self.font)
		self.txtdraw.text((indent,0),self.messageString, self.messageClr ,font=self.font)

		# Draw a box around message display
		#numXPos = int(xPos2 - 40)
		self.pixLen = config.draw.textsize(self.messageString, font = self.font)
		if (self.messageString != self.altStringMessage) :
			numXPos = self.boxMax - self.pixLen[0] - 8
		else :
			numXPos = self.boxMax - self.pixLen[0] - 8
		#numXPos = 32
		numYPos = 24
		#self.txtdraw.rectangle((0,0,self.pixLen[0]+indent+2, self.pixLen[1] + indent-1), outline=(0,100,0))
		config.image.paste(self.scrollImage, (numXPos, numYPos), self.scrollImage)
		
	def drawSpinner(self) :

		'''''''''''''''''' ''' SPINNER '''''''''''''''''''''''''''''''''	
		# Draw a spinner
		self.spinnerAngle += math.pi / self.spinnerAngleSteps
		if(self.spinnerAngle > 2 * math.pi) : self.spinnerAngle = 0

		for s in range (0, self.spinnerAngleSteps) :
			angle  = s * 2 * math.pi / self.spinnerAngleSteps + self.spinnerAngle
			sX0 = self.spinnerInnerRadius * math.sin(angle) + self.spinnerCenter[0]
			sX = self.spinnerRadius * math.sin(angle) + self.spinnerCenter[0]
			sY0 = self.spinnerInnerRadius * math.cos(angle) + self.spinnerCenter[1]
			sY = self.spinnerRadius * math.cos(angle) + self.spinnerCenter[1]
			b = float(s)/float(self.spinnerAngleSteps)
			fillColor = (int(b * 200),int(b * 200),0)
			#if (b <=.01) : fillColor = barColor
			config.draw.line((sX0, sY0, sX, sY), fill=fillColor )

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
		self.altStringMessage = "PLEASE WAIT" 
		if (random.random() > .05) :
			self.altStringMessage = "RESTARTING..." if (random.random() > .5) else "UPDATING"
		self.pausePoint = int(random.random() * 100)
		self.hasPaused = False
		self.paused = False
		self.barColor = (0,0,200)
		self.barColorStart = colorutils.getRandomRGB(1)
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
	setUpDelays()
	while True:
		iterate()
		time.sleep(redrawSpeed)

def setUpDelays() :
	global firstRunCount, completeCount, firstRunCountLim, completeCountLim
	firstRunCountLim = int(random.uniform(pBar.minSleep,pBar.maxSleep))
	completeCountLim = int(random.uniform(pBar.minSleep,pBar.maxSleep))
	firstRunCount = 0
	completeCount = 0

def iterate() :
	global config, pBar, lastRate
	global firstRunCount, completeCount, firstRunCountLim, completeCountLim
	redraw()
	config.render(config.image, 0, 0, config.screenWidth, config.screenHeight)

	if(pBar.rate != lastRate) :
		#print (pBar.rate)
		lastRate = pBar.rate

	if(pBar.firstRun) :
		#time.sleep(int(random.uniform(pBar.minSleep,pBar.maxSleep)))
		firstRunCount+=config.scrollSpeed
		if(firstRunCount > firstRunCountLim) :
			pBar.firstRun = False


	if(pBar.complete) : 
		#time.sleep(int(random.uniform(pBar.minSleep,pBar.maxSleep)))
		completeCount+=config.scrollSpeed
		if(completeCount > completeCountLim) :
			pBar.done()
			setUpDelays()

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
		

