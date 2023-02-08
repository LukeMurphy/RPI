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

class Director:
	"""docstring for Director"""

	slotRate = .5

	def __init__(self, config):
		super(Director, self).__init__()
		self.config = config
		self.tT = time.time()
		self.slotRate = config.redrawSpeed

	def checkTime(self):
		if (time.time() - self.tT) >= self.slotRate:
			self.tT = time.time()
			self.advance = True
		else:
			self.advance = False

	def next(self):

		self.checkTime()

"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""
class DotGrid :
	
	def __init__(self):
		self.clrs = [(255,0,0,255), (0,255,0,255), (0,0,255,255)]
		self.dotGridsArray = list()
		self.width = 256
		self.height = 256

		self.bgColor  = (30,0,100,10)
		self.bgColor  = (0,0,0,255)

		self.cols = 1
		self.rows = 1



	def setUp(self) :
		self.dotGridsArray = list()
		self.workImage = Image.new("RGBA", (self.width, self.height))
		self.draw = ImageDraw.Draw(self.workImage)
		#self.draw.rectangle((0,0,self.width,self.height), fill=self.bgColor)


		self.dotImage1 = Image.new("RGBA", (self.width, self.height))
		self.dotImage2 = Image.new("RGBA", (self.width, self.height))
		self.dotImage3 = Image.new("RGBA", (self.width, self.height))

		self.dotImageArray = [self.dotImage1, self.dotImage2, self.dotImage3]
		self.hideDotRate = 0

		for i in range(0,3) :
			n = 0
			workImage = self.dotImageArray[i]
			draw = ImageDraw.Draw(workImage)
			for c in range(0,self.cols):
				for r in range(0,self.rows):
					xVariation = self.gridVariation - 2 * self.gridVariation * random.random()
					yVariation = self.gridVariation - 2 * self.gridVariation * random.random()
					#self.dotGridsArray.append(list())
					#if self.dotVariationByColor != True :
					dotVariation = random.random() * self.dotVariation
					d = Dot()
					d.workImage = workImage
					d.draw = draw
					d.xOffSet = (self.dotSize + self.packing) * c + xVariation * (i-2) * 1 + self.colsXOffset
					d.yOffSet = (self.dotSize + self.packing) * r + yVariation * (2-i) * 1 + self.rowsYOffset
					d.fillColor = self.clrs[i]
					d.bgColor = self.bgColor

					if self.dotVariationByColor == True :
						dotVariation = random.random() * self.dotVariation
					d.dotSize = self.dotSize + dotVariation
					d.spreadX = self.spreadX #+ i * 5
					d.spreadY = self.spreadY
	
					if n in self.hideDotsList : 
						d.visible = False
					else :
						d.visible = True
					d.setUp()
					d.drawOval()
					self.dotGridsArray.append(d)
					n += 1


	def change(self) :

		self.workImage = Image.new("RGBA", (self.width, self.height))
		self.draw = ImageDraw.Draw(self.workImage)
		#self.draw.rectangle((0,0,self.width,self.height), fill=self.bgColor)
		self.dotImage1 = Image.new("RGBA", (self.width, self.height))
		self.dotImage2 = Image.new("RGBA", (self.width, self.height))
		self.dotImage3 = Image.new("RGBA", (self.width, self.height))

		self.dotImageArray = [self.dotImage1, self.dotImage2, self.dotImage3]
		self.hideDotRate = 0

		dNum  = 0
		for i in range(0,3) :
			n = 0
			workImage = self.dotImageArray[i]
			draw = ImageDraw.Draw(workImage)
			for c in range(0,self.cols):
				for r in range(0,self.rows):
					d = self.dotGridsArray[dNum]
					d.workImage = workImage
					d.draw = draw

					if random.random() < self.changeDotRate :
						xVariation = self.gridVariation - 2 * self.gridVariation * random.random()
						yVariation = self.gridVariation - 2 * self.gridVariation * random.random()
						dotVariation = random.random() * self.dotVariation
						d.xOffSet = (self.dotSize + self.packing) * c + xVariation * (i-2) * 1 + self.colsXOffset
						d.yOffSet = (self.dotSize + self.packing) * r + yVariation * (2-i) * 1 + self.rowsYOffset
						d.dotSize = self.dotSize + dotVariation
						d.spreadX = self.spreadX #+ i * 5
						d.spreadY = self.spreadY
						d.setUp()

					d.drawOval()

					dNum+= 1

		self.workImage = ImageChops.add_modulo(self.workImage , self.dotImageArray[0])
		self.workImage = ImageChops.add_modulo(self.workImage , self.dotImageArray[1])
		self.workImage = ImageChops.add_modulo(self.workImage , self.dotImageArray[2])
		self.workImage = self.workImage.filter(ImageFilter.GaussianBlur(radius=self.blurRadius))



class Dot :

	def __init__(self):

		self.xOffSet = 0
		self.yOffSet = 0
		self.fillColor = (255,255,255,255)
		self.outlineColor = None
		self.visible = True

	def setUp(self):
		#self.workImage = Image.new("RGBA", (256, 256))
		#self.draw = ImageDraw.Draw(self.workImage)
		self.width = self.dotSize
		self.height = self.dotSize
		self.xPos = self.spreadX + self.spreadX * random.random()
		self.yPos = self.spreadY + self.spreadY * random.random()
		self.xPos += self.xOffSet
		self.yPos += self.yOffSet

	def drawOval(self):
			# self.draw.ellipse((0, 0, round(self.objWidth/2) ,round(self.objHeight/2)),
			#     fill=self.fillColor, outline=self.outlineColor)
			self.draw.rectangle((self.xPos, self.yPos,self.xPos+self.width, self.yPos+self.height), fill= self.bgColor)
			if self.visible == True :
				box = [(self.xPos, self.yPos), (self.xPos + self.width/2 + 1, self.yPos + self.height/2 + 1)]
				self.draw.chord(box, 0, 360, fill=self.fillColor, outline=self.outlineColor)



def processImage():
	## Run through the objects .....
	#config.workImageDraw.rectangle((0,0,config.canvasWidth, config.canvasHeight), fill=(0,0,0,200))

	config.dotGrid.change()
	#config.draw.rectangle((0,0,200,200), fill=config.bgColor)

	config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.canvasImageDraw = ImageDraw.Draw(config.canvasImage)
	config.canvasImage.paste(config.dotGrid.workImage, (0,0))


def getColor(r,g,b,a) :
	clr = list( round(i * config.brightness) for i in [r,g,b])
	clr.append(a)
	return tuple(clr)

def iterate():
	global config

	# config.workImageDraw.rectangle((0,0,config.canvasWidth,config.canvasHeight), fill  = (0,0,0))
	# config.canvasImageDraw.rectangle((0,0,config.canvasWidth*10,config.canvasHeight), fill  = (0,0,0,20))

	
	if config.useFadeThruAnimation == True:
		if config.f.fadingDone == True:

			config.renderImageFullOld = config.renderImageFull.copy()
			config.renderImageFull.paste(
				config.canvasImage,
				(config.imageXOffset, config.imageYOffset),
				config.canvasImage,
			)
			config.f.xPos = config.imageXOffset
			config.f.yPos = config.imageYOffset
			# config.renderImageFull = config.renderImageFull.convert("RGBA")
			# renderImageFull = renderImageFull.convert("RGBA")
			config.f.setUp(
				config.renderImageFullOld.convert("RGBA"),
				config.canvasImage.convert("RGBA"),
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
			config.canvasImage,
			(config.imageXOffset, config.imageYOffset),
			config.canvasImage,
		)
		config.render(config.renderImageFull, 0, 0)
		'''
		config.render(config.canvasImage, 0, 0)
		'''

	if random.random() < config.dotVariationChangeProb:
		config.dotVariation = random.uniform(0,config.dotVariationMax)
		config.dotGrid.dotVariation = config.dotVariation
		#print(config.dotVariation)
		config.dotGrid.setUp()


def init():
	global config

	print("SINGLETON dotGrids HOLDER INIT")

	config.redrawSpeed = float(workConfig.get("spots", "redrawSpeed"))
	config.doingRefreshCount = float(workConfig.get("spots", "doingRefreshCount"))
	config.dotSize = int(workConfig.get("spots", "dotSize"))
	config.spreadX = int(workConfig.get("spots", "spreadX"))
	config.spreadY = int(workConfig.get("spots", "spreadY"))
	config.packing = float(workConfig.get("spots", "packing"))
	config.dotrows = int(workConfig.get("spots", "rows"))
	config.dotcols = int(workConfig.get("spots", "cols"))
	config.blurRadius = int(workConfig.get("spots", "blurRadius"))
	config.bgColorVals = (workConfig.get("spots", "bgColor"))
	config.bgColor = tuple(round(float(i) * config.brightness) for i in config.bgColorVals.split(','))

	config.clrAVals = (workConfig.get("spots", "clrA"))
	config.clrA = tuple(round(int(i) * config.brightness) for i in config.clrAVals.split(','))

	config.clrBVals = (workConfig.get("spots", "clrB"))
	config.clrB = tuple(round(int(i) * config.brightness) for i in config.clrBVals.split(','))

	config.clrCVals = (workConfig.get("spots", "clrC"))
	config.clrCV = tuple(round(int(i) * config.brightness) for i in config.clrCVals.split(','))

	config.hideDots = (workConfig.get("spots", "hideDots"))
	config.hideDotsList = tuple((int(i)) for i in config.hideDots.split(','))
	config.hideDotRate = float(workConfig.get("spots", "hideDotRate"))
	config.changeDotRate = float(workConfig.get("spots", "changeDotRate"))


	config.colsXOffset = int(workConfig.get("spots", "colsXOffset"))
	config.rowsYOffset = int(workConfig.get("spots", "rowsYOffset"))
	config.gridVariation = float(workConfig.get("spots", "gridVariation"))
	config.dotVariationMax = float(workConfig.get("spots", "dotVariationMax"))
	config.dotVariation = float(workConfig.get("spots", "dotVariation"))
	config.dotVariationChangeProb = float(workConfig.get("spots", "dotVariationChangeProb"))
	config.dotVariationByColor = (workConfig.getboolean("spots", "dotVariationByColor"))
	config.imageXOffset = 0 
	config.imageYOffset = 0


	config.canvasImage = Image.new("RGBA", (config.canvasWidth , config.canvasHeight))
	config.canvasImageDraw = ImageDraw.Draw(config.canvasImage)


	config.dotGrid = DotGrid()
	config.dotGrid.xOffSet = config.colsXOffset
	config.dotGrid.yOffSet = config.rowsYOffset
	config.dotGrid.colsXOffset = config.colsXOffset
	config.dotGrid.rowsYOffset = config.rowsYOffset
	config.dotGrid.dotSize = config.dotSize
	config.dotGrid.packing = config.packing
	config.dotGrid.spreadX = config.spreadX
	config.dotGrid.spreadY = config.spreadY
	config.dotGrid.rows = config.dotrows
	config.dotGrid.cols = config.dotcols
	config.dotGrid.bgColor = config.bgColor
	config.dotGrid.blurRadius =  config.blurRadius
	config.dotGrid.gridVariation = config.gridVariation
	config.dotGrid.dotVariation = config.dotVariation
	config.dotGrid.dotVariationByColor = config.dotVariationByColor
	config.dotGrid.hideDotsList = config.hideDotsList
	config.dotGrid.hideDotRate = config.hideDotRate
	config.dotGrid.changeDotRate = config.changeDotRate
	config.dotGrid.width = config.canvasWidth
	config.dotGrid.height = config.canvasHeight
	config.dotGrid.clrs = [config.clrA, config.clrB, config.clrCV]

	config.dotGrid.setUp()


	config.init = 0
	config.initCount = 1

	config.redrawSpeed = float(workConfig.get("spots", "redrawSpeed"))
	config.refreshSpeed = float(workConfig.get("spots", "refreshSpeed"))
	config.directorController = Director(config)

	config.f = FaderObj()
	config.f.doingRefreshCount = 2
	config.f.setUp(config.renderImageFull, config.canvasImage)


	config.renderImageFullOld = config.renderImageFull.copy()
	config.fadingDone = True

	config.useFadeThruAnimation = True
	config.deltaTimeDone = True




def runWork():
	global config
	while True:
		config.directorController.checkTime()
		if config.directorController.advance == True:
			iterate()
		time.sleep(config.refreshSpeed)


def checkTime(dotGridsObj):
	config.t2 = time.time()
	delta = config.t2 - config.t1

	#if delta > config.timeToComplete and config.deltaTimeDone == False:

def main(run=True):
	global config, threads, thrd
	init()

	if run:
		runWork()


### Kick off .......
if __name__ == "__main__":
	__main__()
