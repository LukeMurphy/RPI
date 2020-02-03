#!/usr/bin/python
# import modules
# ################################################### #
import datetime
import getopt
import math
import os
import random
import sys
import textwrap
import time
from collections import OrderedDict

from modules import coloroverlay, colorutils
from modules.faderclass import FaderObj
from PIL import (
	Image,
	ImageChops,
	ImageDraw,
	ImageEnhance,
	ImageFilter,
	ImageFont,
	ImageOps,
	ImagePalette,
)

global config



"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""


def init():
	global config

	print("SINGLETON Spots HOLDER INIT")

	config.redrawSpeed = float(workConfig.get("spots", "redrawSpeed"))
	config.doingRefreshCount = float(workConfig.get("spots", "doingRefreshCount"))
	config.dotSize = int(workConfig.get("spots", "dotSize"))
	config.spread = int(workConfig.get("spots", "spread"))
	config.packing = int(workConfig.get("spots", "packing"))
	config.dotrows = int(workConfig.get("spots", "rows"))
	config.dotcols = int(workConfig.get("spots", "cols"))
	config.blurRadius = int(workConfig.get("spots", "blurRadius"))
	config.bgColorVals = (workConfig.get("spots", "bgColor"))
	config.bgColor = tuple(int(i) for i in config.bgColorVals.split(','))

	config.clrAVals = (workConfig.get("spots", "clrA"))
	config.clrA = tuple(round(int(i) * config.brightness) for i in config.clrAVals.split(','))

	config.clrBVals = (workConfig.get("spots", "clrB"))
	config.clrB = tuple(round(int(i) * config.brightness) for i in config.clrBVals.split(','))

	config.clrCVals = (workConfig.get("spots", "clrC"))
	config.clrCV = tuple(round(int(i) * config.brightness) for i in config.clrCVals.split(','))

	config.hideDots = (workConfig.get("spots", "hideDots"))
	config.hideDotsList = tuple((int(i)) for i in config.hideDots.split(','))



	config.colsXOffset = int(workConfig.get("spots", "colsXOffset"))
	config.rowsYOffset = int(workConfig.get("spots", "rowsYOffset"))
	config.gridVariation = int(workConfig.get("spots", "gridVariation"))
	config.dotVariation = int(workConfig.get("spots", "dotVariation"))
	config.dotVariationByColor = (workConfig.getboolean("spots", "dotVariationByColor"))
	config.imageXOffset = 0 
	config.imageYOffset = 0


	config.canvasImage = Image.new(
		"RGBA", (config.canvasWidth * 10, config.canvasHeight)
	)
	config.canvasImageDraw = ImageDraw.Draw(config.canvasImage)

	config.imageLayer = Image.new(
		"RGBA", (config.canvasWidth * 10, config.canvasHeight)
	)
	config.imageLayerDraw = ImageDraw.Draw(config.canvasImage)

	config.workImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.workImageDraw = ImageDraw.Draw(config.workImage)
	

	config.spot = Spot()
	config.spot.xOffSet = config.colsXOffset
	config.spot.yOffSet = config.rowsYOffset
	config.spot.colsXOffset = config.colsXOffset
	config.spot.rowsYOffset = config.rowsYOffset
	config.spot.dotSize = config.dotSize
	config.spot.packing = config.packing
	config.spot.spread = config.spread
	config.spot.rows = config.dotrows
	config.spot.cols = config.dotcols
	config.spot.bgColor = config.bgColor
	config.spot.blurRadius =  config.blurRadius
	config.spot.gridVariation =config.gridVariation
	config.spot.dotVariation =config.dotVariation
	config.spot.dotVariationByColor =config.dotVariationByColor
	config.spot.hideDotsList = config.hideDotsList

	config.spot.clrs = [config.clrA, config.clrB, config.clrCV]

	config.spot.setUp()
	config.spot.render()

	config.init = 0
	config.initCount = 1

	config.f = FaderObj()
	config.f.doingRefreshCount = 5
	config.f.setUp(config.renderImageFull, config.workImage)

	config.renderImageFullOld = config.renderImageFull.copy()
	config.fadingDone = True

	config.useFadeThruAnimation = True
	config.deltaTimeDone = True


def runWork():
	global config
	while True:
		iterate()
		time.sleep(config.redrawSpeed)


def checkTime(SpotsObj):
	config.t2 = time.time()
	delta = config.t2 - config.t1

	#if delta > config.timeToComplete and config.deltaTimeDone == False:


class Spot :
	
	def __init__(self):
		self.clrs = [(255,0,0,200), (0,255,0,200), (0,0,255,200)]
		self.spotsArray = list()
		self.width = 256
		self.height = 256

		self.bgColor  = (30,0,100,10)

		self.cols = 4
		self.rows = 8

		self.workImage = Image.new("RGBA", (self.width, self.height))
		self.draw = ImageDraw.Draw(self.workImage)



	def setUp(self) :
		self.draw.rectangle((0,0,256,256), fill=self.bgColor)
		n = 0
		for c in range(0,self.cols):
			for r in range(0,self.rows):
				xVariation = self.gridVariation - 2 * self.gridVariation * random.random()
				yVariation = self.gridVariation - 2 * self.gridVariation * random.random()
				self.spotsArray.append(list())
				if self.dotVariationByColor != True :
					dotVariation = random.random() * self.dotVariation
				for i in range(0,3) :

					d = Dot()
					d.xOffSet = (self.dotSize + self.packing) * c + xVariation * (i-2)*0 + self.colsXOffset
					d.yOffSet = (self.dotSize + self.packing) * r + yVariation * (2-i)*0 + self.rowsYOffset
					d.fillColor = self.clrs[i]
					if self.dotVariationByColor == True :
						dotVariation = random.random() * self.dotVariation
					d.dotSize = self.dotSize + dotVariation
					d.spread = self.spread
					d.setUp()
					if n in self.hideDotsList : 
						d.visible = False
					else :
						d.visible = True
					self.spotsArray[n].append(d)


				n += 1


	def change(self) :

		self.workImage = Image.new("RGBA", (self.width, self.height))
		self.draw = ImageDraw.Draw(self.workImage)

		if random.random() < .05:
			# sets a default that is a dot that doesn't exist so things don't throw an
			# error as per above .....
			self.hideDotsList = [len(self.spotsArray) + 1]

			for i in range (0,len(self.spotsArray)) :
				if random.random() < .15 :
					self.hideDotsList.append(i)



		self.draw.rectangle((0,0,256,256), fill=self.bgColor)
		n = 0
		for c in range(0,self.cols):
			for r in range(0,self.rows):
				xVariation = self.gridVariation - 2 * self.gridVariation * random.random()
				yVariation = self.gridVariation - 2 * self.gridVariation * random.random()

				if self.dotVariationByColor != True :
					dotVariation = random.random() * self.dotVariation
				if random.random() < .5 : 
					for i in range(0,3) :

						d = self.spotsArray[n][i]
						d.xOffSet = (self.dotSize + self.packing) * c + xVariation * (i-2)*0 + self.colsXOffset
						d.yOffSet = (self.dotSize + self.packing) * r + yVariation * (2-i)*0 + self.rowsYOffset
						d.fillColor = self.clrs[i]
						if self.dotVariationByColor == True :
							dotVariation = random.random() * self.dotVariation
						d.dotSize = self.dotSize + dotVariation
						d.spread = self.spread
						d.setUp()
						if n in self.hideDotsList : 
							d.visible = False
						else :
							d.visible = True
				n += 1

		self.render()



	def render(self) :
		for n in range(0,(self.rows*self.cols)):
			for i in range(0,3):
				self.spotsArray[n][i].drawOval()
				#self.spotsArray[i].xPos += i
				self.workImage = ImageChops.add(self.workImage , self.spotsArray[n][2].workImage)
				self.workImage = ImageChops.add(self.workImage , self.spotsArray[n][0].workImage)
				self.workImage = ImageChops.add(self.workImage , self.spotsArray[n][1].workImage)

		self.workImage = self.workImage.filter(ImageFilter.GaussianBlur(radius=self.blurRadius))


class Dot :

	def __init__(self):

		self.xOffSet = 0
		self.yOffSet = 0
		self.fillColor = (255,0,0,255)
		self.outlineColor = None
		self.visible = True

	def setUp(self):
		self.workImage = Image.new("RGBA", (256, 256))
		self.width = self.dotSize
		self.height = self.dotSize
		self.draw = ImageDraw.Draw(self.workImage)
		self.xPos = self.spread + self.spread * random.random()
		self.yPos = self.spread + self.spread * random.random()
		self.xPos += self.xOffSet
		self.yPos += self.yOffSet

	def drawOval(self):
			# self.draw.ellipse((0, 0, round(self.objWidth/2) ,round(self.objHeight/2)),
			#     fill=self.fillColor, outline=self.outlineColor)
			if self.visible == True :
				box = [(self.xPos, self.yPos), (self.xPos + self.width/2 + 1, self.yPos + self.height/2 + 1)]
				self.draw.chord(box, 0, 360, fill=self.fillColor, outline=self.outlineColor)



def processImage():
	## Run through the objects .....
	config.workImageDraw.rectangle((0,0,config.canvasWidth, config.canvasHeight), fill=(0,0,0,200))

	config.spot.change()

	config.workImage.paste(config.spot.workImage, (0,0))
	#config.workImage.paste(config.spot2.workImage, (config.spot2.xOffSet, config.spot2.yOffSet))
	#config.workImage = ImageChops.add(config.spot.workImage,config.workImage)
	#config.workImage = ImageChops.add(config.spot2.workImage, config.workImage)
	
	#config.workImage = ImageChops.add(config.workImage,)




def iterate():
	global config

	# config.workImageDraw.rectangle((0,0,config.canvasWidth,config.canvasHeight), fill  = (0,0,0))
	# config.canvasImageDraw.rectangle((0,0,config.canvasWidth*10,config.canvasHeight), fill  = (0,0,0,20))


	if config.useFadeThruAnimation == True:
		if config.f.fadingDone == True:

			config.renderImageFullOld = config.renderImageFull.copy()
			config.renderImageFull.paste(
				config.workImage,
				(config.imageXOffset, config.imageYOffset),
				config.workImage,
			)
			config.f.xPos = config.imageXOffset
			config.f.yPos = config.imageYOffset
			# config.renderImageFull = config.renderImageFull.convert("RGBA")
			# renderImageFull = renderImageFull.convert("RGBA")
			config.f.setUp(
				config.renderImageFullOld.convert("RGBA"),
				config.workImage.convert("RGBA"),
			)
			processImage()


		config.f.fadeIn()
		config.render(config.f.blendedImage, 0, 0)
		config.init += config.initCount
		
		# This is to get a faster initial fade-in then when done
		# set it to the right fade-through count
		if config.init > 18 and config.initCount > 0 :
			config.f.doingRefreshCount = config.doingRefreshCount
			config.initCount = 0


	else:
		processImage()
		config.renderImageFull.paste(
			config.workImage,
			(config.imageXOffset, config.imageYOffset),
			config.workImage,
		)
		config.render(config.renderImageFull, 0, 0)



def main(run=True):
	global config, threads, thrd
	init()

	if run:
		runWork()


### Kick off .......
if __name__ == "__main__":
	__main__()
