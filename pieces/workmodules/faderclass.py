#!/usr/bin/python
import time
import random
import math
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageEnhance

print("Fader Class Loaded")

class FaderObj:

	def __init__(self, targetImage, blendImage):
		self.doingRefresh =  0
		self.doingRefreshCount = 50
		self.fadingDone = False
		self.targetImage = targetImage
		self.blendImage = blendImage
		# targetImage = config.image


	def fadeIn(self) :
		if self.fadingDone == False :
			if self.doingRefresh < self.doingRefreshCount :	
				# self.blendImage = Image.new("RGBA", (self.width, self.height))	
				self.crossFade = Image.blend(self.blankImage, self.image, self.doingRefresh/self.doingRefreshCount)
				self.targeImage.paste(self.crossFade, (self.xPos,self.yPos), self.crossFade)
				self.doingRefresh += 1
			else :
				self.targeImage.paste(self.image, (self.xPos,self.yPos), self.image)
				self.fadingDone = True