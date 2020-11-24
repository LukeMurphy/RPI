import math
import random
import threading
import time

from modules import colorutils
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps


'''
				fadeIn = Fader()
				# fadeIn.blankImage = Image.new("RGBA", (height, width))
				fadeIn.crossFade = Image.new("RGBA", (height, width))
				fadeIn.image = gradientImage
				fadeIn.xPos = xPos
				fadeIn.yPos = yPos
				fadeIn.height = gradientImage.height
				fadeIn.width = gradientImage.width

				config.fadeArray.append(fadeIn)

'''

class Fader:
	def __init__(self):
		self.doingRefresh = 0
		self.doingRefreshCount = 50
		self.fadingDone = False

	def fadeIn(self, config):
		if self.fadingDone == False:
			if self.doingRefresh < self.doingRefreshCount:
				self.blankImage = Image.new("RGBA", (self.width, self.height))
				self.crossFade = Image.blend(
					self.blankImage,
					self.image,
					self.doingRefresh / self.doingRefreshCount,
				)
				config.image.paste(
					self.crossFade, (self.xPos, self.yPos), self.crossFade
				)
				self.doingRefresh += 1
			else:
				config.image.paste(self.image, (self.xPos, self.yPos), self.image)
				self.fadingDone = True


class Block:
	def __init__(self):
		self.unitArray = []
		self.on = True




class UnitX:
	def __init__(self):
		self.remake()
		self.on = True
		self.yPos = 0
		self.xPos = 0

	def remake(self) :
		self.colorVal = (240,200,0)
		self.outlineColorVal = (240,200,0)
		self.barThickness = 1
		self.w = 3
		self.on = True

		self.unitImage = Image.new("RGBA", (self.w, self.w))
		drw = ImageDraw.Draw(self.unitImage)
		
		if random.random() < config.lineDrawProb :
			drw.line((0, 0, 2, 2 ), fill = self.outlineColorVal)


		if random.random() < config.lineDrawProb:
			drw.line((0, 2, 2, 0 ), fill = self.outlineColorVal)



def transformImage(img):
	width, height = img.size
	new_width = 50
	m = 0.0
	img = img.transform(
		(new_width, height), Image.AFFINE, (1, m, 0, 0, 1, 0), Image.BICUBIC
	)
	return img


def drawBar():
	global config


def reDraw():
	global config


def runWork():
	global config
	while True:
		iterate()
		time.sleep(config.redrawRate)


def iterate():
	global config

	'''
	for i in range(0, config.numberOfUnitXs):
		unit = config.unitArray[i]
		if random.random() < .99 and unit.on == True:
			config.image.paste(unit.unitImage,(round(unit.xPos), round(unit.yPos)), unit.unitImage)
		else :
			config.image.paste(config.blankUnit,(round(unit.xPos), round(unit.yPos)), config.blankUnit)
			unit.on = False

			if random.random() < .03 :
				unit.remake()
	'''

	numLargeBlocks = len(config.blockArray)
	for n in range(0, numLargeBlocks) :
		b = config.blockArray[n]
		if random.random() < .9999 and b.on == True :
			for i in range(0, len(b.unitArray)):
				unit = b.unitArray[i]
				if random.random() < .999 and unit.on == True:
					config.image.paste(unit.unitImage,(round(unit.xPos), round(unit.yPos)), unit.unitImage)
				else :
					config.image.paste(config.blankUnit,(round(unit.xPos), round(unit.yPos)), config.blankUnit)
					unit.on = False
					if random.random() < .03 :
						unit.remake()
		else :
			config.image.paste(config.blankBlock,(round(b.unitArray[0].xPos), round(b.unitArray[0].yPos)), config.blankBlock)
			b.on = False
			if random.random() < .01 :
				b.on = True



	config.render(config.image, 0,0)


def main(run=True):
	global config
	config.redrawRate = .02

	config.lineDrawProb = 1.0

	config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	config.draw = ImageDraw.Draw(config.image)
	config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.canvasDraw = ImageDraw.Draw(config.canvasImage)

	config.numberOfUnitXs =  int(workConfig.get("units", "numberOfUnitXs"))
	config.unitArray = []

	config.blankUnit = Image.new("RGBA", (3, 3))
	config.blankUnitDraw = ImageDraw.Draw(config.blankUnit)
	config.blankUnitDraw.rectangle((0,0,3,3), fill = (0,0,100,10))

	config.blankBlock = Image.new("RGBA", (32, 32))
	config.blankBlockDraw = ImageDraw.Draw(config.blankBlock)
	config.blankBlockDraw.rectangle((0,0,32,32), fill = (0,0,0,10))

	config.blockArray = []

	for r in range(0, 4):
		for c in range(0, 3):

			b = Block()

			for i in range(0, 8):
				u =  UnitX()
				u.xPos = i * 4 + c * 64
				u.yPos = i * 4 + r * 64
				config.unitArray.append(u)
				b.unitArray.append(u)
			for i in range(0, 8):
				u =  UnitX()
				u.xPos = 28 - i * 4 + c * 64
				u.yPos = i * 4 + r * 64
				config.unitArray.append(u)	
				b.unitArray.append(u)

			config.blockArray.append(b)

	config.numberOfUnitXs = len(config.unitArray)


	if run:
		runWork()
