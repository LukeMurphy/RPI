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


class Bar:
	def __init__(self):
		self.remake()


	def remake(self) :
		self.speed = random.uniform(.5,3)
		self.speed2 = random.uniform(-.15,.15)
		self.yPos = round(random.uniform(0,96))
		self.xPos = 0
		self.barThickness = round(random.uniform(5,16))
		self.colorVal = colorutils.randomColorAlpha()



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


	for i in range(0, config.numberOfBars):
		bar = config.barArray[i]
		bar.xPos += bar.speed
		bar.yPos += bar.speed2
		config.draw.rectangle((bar.xPos-2, bar.yPos, bar.xPos, bar.yPos + bar.barThickness ), fill = bar.colorVal)

		if bar.xPos > config.canvasWidth :
			bar.remake()



	config.render(config.image, 0,0)



def main(run=True):
	global config
	config.redrawRate = .02

	config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	config.draw = ImageDraw.Draw(config.image)
	config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.canvasDraw = ImageDraw.Draw(config.canvasImage)

	config.xPos = 0

	config.numberOfBars = 20
	yPos = 0
	config.barArray = []
	for i in range(0, config.numberOfBars):
		bar =  Bar()
		bar.yPos = yPos
		config.barArray.append(bar)
		yPos += bar.barThickness




	if run:
		runWork()
