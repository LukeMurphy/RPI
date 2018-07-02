import time
import random
import math
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageEnhance, ImageChops
from modules import colorutils

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
### Colorizing filter that transitions from colorA to colorB ###

class ColorOverlay:

	currentColor = [0,0,0]
	rateOfColorChange = 0
	colorA = colorB = [0,0,0]
	randomRange = (10.0,100.0)
	complete =  False
	tDelta = 0
	timeTrigger = False
	gotoNextTransition = False
	autoChange = True
	t1 = 0

	## "Public" variables that can be set
	randomSteps = True
	steps = 100
	tLimit = 10
	tLimitBase = 10

	maxBrightness = 1

	minValue = .1
	maxValue = 1

	minSaturation = 0.1
	maxSaturation= 1
	
	minHue = 1
	maxHue = 360

	dropHueMin = 0
	dropHueMax = 0

	def __init__(self): 
		self.colorTransitionSetup()
		#self.colorA = colorutils.randomColor()
		#self.colorB = colorutils.randomColor()
		#self.colorB = colorutils.getRandomRGB()
		self.t1 = time.time()
		self.timeTrigger = False

	
	def checkTime(self):
		t = time.time()
		self.tDelta = (t - self.t1)

	
	def setStartColor(self):
		self.colorA = colorutils.getRandomColorHSV(
			hMin=self.minHue, hMax=self.maxHue, 
			sMin=self.minSaturation, sMax=self.maxSaturation,
			vMin=self.minValue, vMax=self.maxValue,
			dropHueMin = self.dropHueMin, dropHueMax = self.dropHueMax)
		#print("New Color A", self.colorA)

	
	def getNewColor(self):
		#self.colorB = colorutils.randomColor()
		## Vaguely more control of the color parameters ... 
		#if(random.random() > .8) : self.colorB = colorutils.getRandomRGB()

		## LEGACY --- If the maxbrightness is being set to something other than the default
		## set the maxValue to the maxBrightness 
		if(self.maxBrightness != 1 ) :
			self.maxValue = self.maxBrightness

		#print(self.minHue,self.maxHue,self.minValue,self.maxValue,self.minSaturation,self.maxSaturation)

		self.colorB = colorutils.getRandomColorHSV(
			hMin=self.minHue, hMax=self.maxHue, 
			sMin=self.minSaturation, sMax=self.maxSaturation,
			vMin=self.minValue, vMax=self.maxValue,
			dropHueMin = self.dropHueMin, dropHueMax = self.dropHueMax)

		'''
		print("New Color B", self.minHue, self.maxHue, 
			self.minSaturation, self.maxSaturation,
			self.minValue, self.maxValue)
		'''

	
	def colorTransitionSetup(self,steps=0, newColor = None):

		#self.timeTrigger = False
		self.gotoNextTransition = False

		''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
		#### Setting up for color transitions
		self.colorDelta = [0,0,0]
		self.rateOfColorChange = [0,0,0]

		#self.currentColor = self.colorA
		#self.colorA = self.colorB
		if newColor == None :
			self.getNewColor()
		else :
			self.colorB = newColor


		#config.colorDelta = [a - b for a, b in zip(config.colorA, config.colorB)]
		from operator import sub
		self.colorDelta = list(map(sub, self.colorB, self.currentColor))
		test = [abs(a) for a in self.colorDelta]
		if(steps == 0 or self.randomSteps == True) : 
			self.steps = random.uniform(self.randomRange[0],self.randomRange[1])

		self.tLimit = round(random.uniform(self.tLimitBase/2, self.tLimitBase * 1.5))+ 1
		self.rateOfColorChange = [ a/self.steps for a in self.colorDelta]
		self.complete =  False
		self.t1 = time.time()

	
		#print("New transition started...", self.colorB, self.tLimitBase, self.tLimit)


	def stepTransition(self, autoReset = False, alpha = 255) :
		self.currentColor = [
		round(self.currentColor[0] + self.rateOfColorChange[0]),
		round(self.currentColor[1] + self.rateOfColorChange[1]),
		round(self.currentColor[2] + self.rateOfColorChange[2]),
		alpha
		]

		self.checkTime()

		## Always change to the next color based on TIME
		if (self.tDelta > self.tLimit and self.gotoNextTransition == False) :
			#self.timeTrigger = True
			#and self.complete == True

			#print("Timesup", self.tDelta, self.tLimit)
			self.gotoNextTransition = True
			self.complete =  True
			self.t1 = time.time()
			if self.autoChange == True :
				self.colorTransitionSetup(self.steps)

		for i in range (0,3):
			#if (self.currentColor[i] - abs(self.rateOfColorChange[i])) <= self.colorB[i] <= (self.currentColor[i] + abs(self.rateOfColorChange[i])) : 
			#if (self.currentColor[i] >= (self.colorB[i] - abs(self.rateOfColorChange[i]))) and  self.currentColor[i] <= (self.colorB[i] + abs(self.rateOfColorChange[i])) :
			lowerRange = self.colorB[i] - abs(self.rateOfColorChange[i])
			upperRange = self.colorB[i] + abs(self.rateOfColorChange[i])
			if (self.currentColor[i] >= (lowerRange) and  self.currentColor[i] <= (upperRange) ) :
				self.rateOfColorChange[i] = 0
				#print("Color reached", i)
		
		if(self.rateOfColorChange[0] == 0 and self.rateOfColorChange[1] == 0 and self.rateOfColorChange[2] == 0) : 
				self.complete =  True
				#print("Transition complete.")
				#if(autoReset == True or self.gotoNextTransition == True) : 
				#	self.colorTransitionSetup(self.steps)


	def getPercentageDone(self):
		diff = 0 
		for i in range (0,3):
			d = abs(self.colorB[i] - self.currentColor[i])/255 
			if d < diff : diff = d 
		return diff



