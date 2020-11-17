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
		self.speed1 = random.uniform(config.speed1RangeMin, config.speed1RangeMax)
		self.speed2 = random.uniform(config.speed2RangeMin, config.speed2RangeMax)
		self.yPos = round(random.uniform(0,96))
		self.xPos = 0
		self.barThickness = round(random.uniform(config.barThicknessMin, config.barThicknessMax))
		#self.colorVal = colorutils.randomColorAlpha()
		cset = config.colorSets[config.usingColorSet]
		self.colorVal = colorutils.getRandomColorHSV(cset[0], cset[1], cset[2], cset[3], cset[4], cset[5], config.dropHueMax,0,config.colorAlpha )



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
		bar.xPos += bar.speed1
		bar.yPos += bar.speed2

		w = round(math.sqrt(2) * config.barThicknessMax * 1.5)

		angle = 180/math.pi * math.tan(bar.speed2/bar.speed1)

		temp = Image.new("RGBA", (w, w))
		drw = ImageDraw.Draw(temp)
		#drw.rectangle((bar.xPos-1, bar.yPos, bar.xPos, bar.yPos + bar.barThickness ), fill = bar.colorVal)
		drw.rectangle((0, 0, bar.barThickness, bar.barThickness ), fill = bar.colorVal)
		drw.rectangle((0, 2, bar.barThickness, bar.barThickness+2 ), fill = bar.colorVal)
		temp = temp.rotate(config.tipAngle - angle)

		config.image.paste(temp,(round(bar.xPos), round(bar.yPos)), temp)

		if bar.xPos > config.canvasWidth :
			bar.remake()


	if random.random() < .002 :
		if config.dropHueMax == 0 :
			config.dropHueMax = 255
		else :
			config.dropHueMax = 0
		#print("Winter... " + str(config.dropHueMax ))

	if random.random() < .003 :
		config.usingColorSet = math.floor(random.uniform(0,4))
		# just in case ....
		if config.usingColorSet == 4 : 
			config.usingColorSet = 3
		config.colorAlpha = round(random.uniform(config.leadEdgeAlpahMin,config.leadEdgeAlpahMax))
		config.dropHueMax = 0
		#print("ColorSet: " + str(config.usingColorSet))

	config.render(config.image, 0,0)




def main(run=True):
	global config
	config.redrawRate = .02

	config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	config.draw = ImageDraw.Draw(config.image)
	config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.canvasDraw = ImageDraw.Draw(config.canvasImage)

	config.xPos = 0
	config.dropHueMax = 0

	config.numberOfBars =  int(workConfig.get("bars", "numberOfBars"))
	config.barThicknessMin =  int(workConfig.get("bars", "barThicknessMin"))
	config.barThicknessMax =  int(workConfig.get("bars", "barThicknessMax"))	

	config.leadEdgeAlpahMin =  int(workConfig.get("bars", "leadEdgeAlpahMin"))
	config.leadEdgeAlpahMax =  int(workConfig.get("bars", "leadEdgeAlpahMax"))
	config.tipAngle =  float(workConfig.get("bars", "tipAngle"))
	
	config.speed1RangeMin =  float(workConfig.get("bars", "speed1RangeMin"))
	config.speed1RangeMax =  float(workConfig.get("bars", "speed1RangeMax"))
	config.speed2RangeMin =  float(workConfig.get("bars", "speed2RangeMin"))
	config.speed2RangeMax =  float(workConfig.get("bars", "speed2RangeMax"))
	
	config.colorAlpha = config.leadEdgeAlpahMin
	yPos = 0
	config.barArray = []

	config.colorSets = []
	# reds of fall
	cset1 = (350,50,.5,1,.3,.8)
	# yellow greens of spring
	cset2 = (50,180,.5,1,.3,.8)
	# winter water
	cset3 = (180,270,.5,1,.3,.8)
	# psychadelic summer dream 
	cset4 = (270,350,.5,1,.3,.8)

	config.colorSets.append(cset1)
	config.colorSets.append(cset2)
	config.colorSets.append(cset3)
	config.colorSets.append(cset4)

	config.usingColorSet = math.floor(random.uniform(0,4))
	if config.usingColorSet == 4 : config.usingColorSet = 3

	for i in range(0, config.numberOfBars):
		bar =  Bar()
		bar.yPos = yPos
		config.barArray.append(bar)
		yPos += bar.barThickness



	if run:
		runWork()
