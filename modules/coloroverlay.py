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


	def __init__(self): 
		self.colorTransitionSetup()
		self.colorA = colorutils.randomColor()
		self.colorB = colorutils.randomColor()


	def colorTransitionSetup(self,steps=0):

		''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
		#### Setting up for color transitions
		self.colorDelta = [0,0,0]
		self.rateOfColorChange = [0,0,0]

		self.colorA = self.colorB
		self.currentColor = self.colorA
		self.colorB = colorutils.randomColor()

		#config.colorDelta = [a - b for a, b in zip(config.colorA, config.colorB)]
		from operator import sub
		self.colorDelta = map(sub, self.colorB, self.colorA)
		test = [abs(a) for a in self.colorDelta]
		if(steps == 0) : steps = random.uniform(10.0,500.0)
		self.rateOfColorChange = [ a/steps for a in self.colorDelta]
		self.complete =  False



	def stepTransition(self, autoReset = True) :

		self.currentColor = [
		(self.currentColor[0] + self.rateOfColorChange[0]),
		(self.currentColor[1] + self.rateOfColorChange[1]),
		(self.currentColor[2] + self.rateOfColorChange[2])
		]

		for i in range (0,3):
			if (self.currentColor[i] - abs(self.rateOfColorChange[i])) <= self.colorB[i] <= (self.currentColor[i] + abs(self.rateOfColorChange[i])) : 
				self.rateOfColorChange[i] = 0


		
		if(self.rateOfColorChange[0] == 0 and self.rateOfColorChange[1] == 0 and self.rateOfColorChange[2] == 0) : 
				self.complete =  True
				if(autoReset == True) : self.colorTransitionSetup()

