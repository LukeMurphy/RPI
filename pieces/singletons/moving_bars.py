import math
import random
import threading
import time
from modules.configuration import bcolors
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
		self.xSpeed = random.uniform(config.xSpeedRangeMin * config.direction, config.xSpeedRangeMax * config.direction)
		self.ySpeed = random.uniform(config.ySpeedRangeMin, config.ySpeedRangeMax)
		self.yPos = round(random.uniform(config.yRangeMin,config.yRangeMax))
		self.xPos = -config.barThicknessMax * 2
		if config.direction == -1 :
			self.xPos = config.canvasWidth + config.barThicknessMax * 2
		self.barThickness = round(random.uniform(config.barThicknessMin, config.barThicknessMax))
		self.barLength = round(random.uniform(config.barLengthMin, config.barLengthMax))
		#self.colorVal = colorutils.randomColorAlpha()
		cset = config.colorSets[config.usingColorSet]

		colorAlpha = config.outlineColorAlpha

		self.colorVal = colorutils.getRandomColorHSV(cset[0], cset[1], cset[2], cset[3], cset[4], cset[5], config.dropHueMax,0, colorAlpha, config.brightness )
		self.outlineColorVal = colorutils.getRandomColorHSV(cset[0], cset[1], cset[2], cset[3], cset[4], cset[5], config.dropHueMax,0, config.outlineColorAlpha, config.brightness )
		self.outlineColorVal = self.colorVal


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
	print(bcolors.OKGREEN + "** " + bcolors.BOLD)
	print("Running moving_bars.py")
	print(bcolors.ENDC)
	while config.isRunning == True:
		iterate()
		time.sleep(config.redrawRate)
		if config.standAlone == False :
			config.callBack()

def iterate():
	global config

	config.draw.rectangle((0,0,400,400), fill=(0,0,0,10))


	for i in range(0, config.numberOfBars):
		bar = config.barArray[i]
		bar.xPos += bar.xSpeed
		bar.yPos += bar.ySpeed

		w = round(math.sqrt(2) * config.barThicknessMax * 1.5)

		angle = 180/math.pi * math.tan(bar.ySpeed/abs(bar.xSpeed))

		temp = Image.new("RGBA", (w, w))
		drw = ImageDraw.Draw(temp)

		if config.tipType == 1 :
			drw.rectangle((0, 0, bar.barThickness, bar.barLength ), fill = bar.colorVal, outline = bar.outlineColorVal)
			drw.rectangle((0, 2, bar.barThickness, bar.barLength+2 ), fill = bar.colorVal, outline = bar.outlineColorVal)
		
		elif config.tipType == 0:
			drw.ellipse((0, 2, bar.barThickness, bar.barLength+2 ), fill = bar.colorVal, outline = bar.outlineColorVal)

		elif config.tipType == 2:
			drw.ellipse((0, 2, bar.barThickness, bar.barThickness), fill = bar.colorVal, outline = bar.outlineColorVal)
		temp = temp.rotate(config.tipAngle - angle)

		config.image.paste(temp,(round(bar.xPos), round(bar.yPos)), temp)

		if bar.xPos > config.canvasWidth + bar.barLength and config.direction == 1:
			bar.remake()
		if bar.xPos < 0 and config.direction == -1:
			bar.remake()


	if random.random() < .002 :
		if config.dropHueMax == 0 :
			config.dropHueMax = 255
		else :
			config.dropHueMax = 0
		#print("Winter... " + str(config.dropHueMax ))

	if random.random() < .003 :
		config.usingColorSet = math.floor(random.uniform(0,config.numberOfColorSets))
		# just in case ....
		if config.usingColorSet == config.numberOfColorSets : 
			config.usingColorSet = config.numberOfColorSets-1
		config.colorAlpha = round(random.uniform(config.leadEdgeAlpahMin,config.leadEdgeAlpahMax))
		config.dropHueMax = 0
		#config.tipType = round(random.random())
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

	config.barLengthMin =  int(workConfig.get("bars", "barLengthMin"))
	config.barLengthMax =  int(workConfig.get("bars", "barLengthMax"))	

	config.direction =  int(workConfig.get("bars", "direction"))	
	yRange =  (workConfig.get("bars", "yRange")).split(",")
	config.yRangeMin = int(yRange[0])	
	config.yRangeMax = int(yRange[1])	

	config.leadEdgeAlpahMin =  int(workConfig.get("bars", "leadEdgeAlpahMin"))
	config.leadEdgeAlpahMax =  int(workConfig.get("bars", "leadEdgeAlpahMax"))
	config.tipAngle =  float(workConfig.get("bars", "tipAngle"))
	
	config.xSpeedRangeMin =  float(workConfig.get("bars", "xSpeedRangeMin"))
	config.xSpeedRangeMax =  float(workConfig.get("bars", "xSpeedRangeMax"))
	config.ySpeedRangeMin =  float(workConfig.get("bars", "ySpeedRangeMin"))
	config.ySpeedRangeMax =  float(workConfig.get("bars", "ySpeedRangeMax"))

	try:
		config.tipType = int(workConfig.get("bars", "tipType"))
	except Exception as e:
		print(str(e))
		config.tipType = 1
	
	config.colorAlpha = round(random.uniform(config.leadEdgeAlpahMin,config.leadEdgeAlpahMax))
	config.outlineColorAlpha = round(random.uniform(config.leadEdgeAlpahMin,config.leadEdgeAlpahMax))
	yPos = 0
	config.barArray = []

	config.colorSets = []
	
	config.colorSetList = list(
		i for i in (workConfig.get("bars", "colorSets").split(","))
	)

	config.numberOfColorSets = len(config.colorSetList)
	for setName in config.colorSetList :
		cset = list(
			float(i) for i in (workConfig.get("bars", setName).split(","))
		)
		config.colorSets.append(cset)


	config.usingColorSet = math.floor(random.uniform(0,config.numberOfColorSets))
	if config.usingColorSet == config.numberOfColorSets : config.usingColorSet = config.numberOfColorSets - 1

	# initialize and place the first set
	for i in range(0, config.numberOfBars):
		bar =  Bar()
		bar.yPos = round(random.uniform(config.yRangeMin,config.yRangeMax))
		bar.xPos = round(random.uniform(0,config.canvasWidth - config.barThicknessMax))
		config.barArray.append(bar)
		#yPos += bar.barThickness



	if run:
		runWork()
