import time
import random
import math
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageEnhance, ImageChops
from modules import colorutils, badpixels

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
### Colorizing filter that transitions from colorA to colorB ###

class ColorOverlay:

	currentColor = [0,0,0]
	rateOfColorChange = 0
	colorA = colorB = [0,0,0]
	complete =  False
	randomRange = (10.0,100.0)
	randomSteps = True
	steps = 100


	def __init__(self): 
		self.colorTransitionSetup()
		self.colorA = colorutils.randomColor()
		self.colorB = colorutils.randomColor()
		self.colorB = colorutils.getRandomRGB()

	def getNewColor(self):
		self.colorB = colorutils.randomColor()
		if(random.random() > .8) : self.colorB = colorutils.getRandomRGB()


	def colorTransitionSetup(self,steps=0):

		''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
		#### Setting up for color transitions
		self.colorDelta = [0,0,0]
		self.rateOfColorChange = [0,0,0]

		#self.currentColor = self.colorA
		#self.colorA = self.colorB
		self.getNewColor()


		#config.colorDelta = [a - b for a, b in zip(config.colorA, config.colorB)]
		from operator import sub
		self.colorDelta = map(sub, self.colorB, self.currentColor)
		test = [abs(a) for a in self.colorDelta]
		if(steps == 0 or self.randomSteps == True) : 
			self.steps = random.uniform(self.randomRange[0],self.randomRange[1])
		self.rateOfColorChange = [ a/self.steps for a in self.colorDelta]
		self.complete =  False



	def stepTransition(self, autoReset = True) :

		self.currentColor = [
		(self.currentColor[0] + self.rateOfColorChange[0]),
		(self.currentColor[1] + self.rateOfColorChange[1]),
		(self.currentColor[2] + self.rateOfColorChange[2])
		]

		for i in range (0,3):
			#if (self.currentColor[i] - abs(self.rateOfColorChange[i])) <= self.colorB[i] <= (self.currentColor[i] + abs(self.rateOfColorChange[i])) : 
			if (self.currentColor[i] >= self.colorB[i] - abs(self.rateOfColorChange[i])) and  self.currentColor[i] <= (self.colorB[i] + abs(self.rateOfColorChange[i])) :
				self.rateOfColorChange[i] = 0

		
		if(self.rateOfColorChange[0] == 0 and self.rateOfColorChange[1] == 0 and self.rateOfColorChange[2] == 0) : 
				self.complete =  True
				if(autoReset == True) : 
					self.colorTransitionSetup(self.steps)

