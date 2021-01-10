import math
import random
import threading
import time

from modules import colorutils
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps, ImageFilter


class Fader:
	def __init__(self):
		self.doingRefresh = 0
		self.doingRefreshCount = 50
		self.fadingDone = False
		self.testing = True

	def setUp(self):
		self.blankImage = Image.new("RGBA", (self.width, self.height))
		self.image = Image.new("RGBA", (self.width, self.height))
		self.crossFade = Image.new("RGBA", (self.width, self.height))

	def test(self):
		print("test")
		#self.blankImage = Image.new("RGBA", (self.width, self.height))
		draw = ImageDraw.Draw(self.crossFade)
		draw.rectangle((0,0,100,100), fill=(0,0,255,255))
		config.image.paste(
			self.crossFade, (self.xPos, self.yPos), self.crossFade
		)

	def fadeIn(self, config):
		if self.fadingDone == False:

			if self.testing == True :
				self.testing = False
				#print(self.fadingDone, self.doingRefresh)

			if self.doingRefresh < self.doingRefreshCount:

				if config.fadeThruBlack == True :
					self.blankImage = Image.new("RGBA", (self.width, self.height))
				percent  = self.doingRefresh / self.doingRefreshCount
				self.crossFade = Image.blend(
					self.blankImage,
					self.image,
					percent,
				)
				config.image.paste(
					self.crossFade, (self.xPos, self.yPos), self.crossFade
				)
				self.doingRefresh += 1
			else:
				config.image.paste(self.image, (self.xPos, self.yPos), self.image)
				self.fadingDone = True
				self.doingRefresh = 0
				self.blankImage = self.image.copy()
				self.testing = True


class Element:

	def __init__(self):
		self.doingRefresh = 0
		self.doingRefreshCount = 50
		self.fadingDone = False
		self.c1 = (0,0,0,0)
		self.c2 = (0,0,0,0)
		self.grayLevel1 = 0
		self.grayLevel2 = 0

	def setUp(self):
		pass

	def change(self, config):

		if config.colorChoice == "rgbAlpha":
			
			if random.random() < config.grayProb :

				self.grayLevel1 = round(random.uniform(config.grayLevelLower,config.grayLevelUpper))
				self.grayLevel2 = round(random.uniform(config.grayLevelLower,config.grayLevelUpper))

				self.c1 = (self.grayLevel1, self.grayLevel1, self.grayLevel1, 255)
				self.c2 = (self.grayLevel2, self.grayLevel2, self.grayLevel2, 255)

			else :
				self.c1 = colorutils.randomYellowsAlpha(
					config.brightness, config.alpha1, config.alpha1, 0.0, 0.35
				)
				self.c2 = colorutils.randomYellowsAlpha(
					config.brightness, config.alpha2, config.alpha2, 0.0, 0.35
				)

				

		elif config.colorChoice == "rgb":
			self.c1 = colorutils.getRandomRGB(config.brightness)
			self.c2 = colorutils.getRandomRGB(config.brightness)
		else:
			self.c1 = colorutils.getRandomColorWheel(config.brightness)
			self.c2 = colorutils.getRandomColorWheel(config.brightness)

		if random.random() < config.blackProb:
			self.c1 = (0, 0, 0, 55)
			self.c2 = (0, 0, 0, 255)

		#print(self.c1,self.c2)


def transformImage(img):
	width, height = img.size
	new_width = 50
	m = 0.0
	img = img.transform(
		(new_width, height), Image.AFFINE, (1, m, 0, 0, 1, 0), Image.BICUBIC
	)
	return img

def drawCircle(width=32, height=32, c1=(0, 0, 0, 0), c2=(0, 0, 0, 0)):
	global config

	gradientImage = Image.new("RGBA", (width, height))
	gradientImageDraw = ImageDraw.Draw(gradientImage)

	# draw box container
	gradientImageDraw.rectangle(
		(0, 0, width, height), outline=None, fill=(config.holderColor)
	)

	# draw circles
	vLines  = 4;
	arc = (math.pi) / vLines
	dR = c2[0] - c1[0]
	dG = c2[1] - c1[1]
	dB = c2[2] - c1[2]

	if len(c1) == 3:
		dA = 0
	else:
		dA = c2[3] - c1[3]

	mid = width / 2
	for n in range(1, vLines+1):
		boxWidth = width / n
		xPos = math.floor(mid - boxWidth/2)
		xPos2 = math.floor(mid + boxWidth/2)

		yPos = math.floor(mid - boxWidth/2)
		yPos2 = math.floor(mid + boxWidth/2)
		b = math.sin(arc * n)
		b = n/vLines + .2
		rVd = round(c1[0] + (b * dR))
		gVd = round(c1[1] + (b * dG))
		bVd = round(c1[2] + (b * dB))

		if len(c1) == 4:
			bAd = round(c1[3] + (b * dA))
		else:
			bAd = 255

		barColorDisplay = (rVd, gVd, bVd, bAd)
		gradientImageDraw.ellipse((xPos, yPos, xPos2, yPos2), fill=barColorDisplay, outline=None)

	gradientImage = gradientImage.filter(ImageFilter.GaussianBlur(radius=config.dotBlurRadius))

	return gradientImage


def reDraw():
	useRandomPlacement = False
	elementCount = 0
	for i in range(0, config.rowsShown):
		for ii in range(0, config.colsShown):
			width = config.rowHeight
			height = config.heightMax
			xPos = ii * width
			yPos = i * config.rowHeight

			if ii > config.blockYOffset[0] and config.blockYOffset[0] != 0 :
				yPos += config.blockYOffset[1]

			if i > config.blockXOffset[0] and config.blockXOffset[0] != 0 :
				xPos += config.blockXOffset[1]

			if config.initializing == True :
				element = Element()
				element.xPos = xPos
				element.yPos = yPos
				element.width = width
				element.height = height
				element.change(config)
				config.elementsArray.append(element)

				element.gradientImage = drawCircle(width, height, element.c1, element.c2)

				element.fader = Fader()
				element.fader.height = element.gradientImage.height
				element.fader.width = element.gradientImage.width
				element.fader.xPos = xPos
				element.fader.yPos = yPos
				element.fader.setUp()

				element.fader.image = element.gradientImage
				#config.fadeArray.append(fadeIn)
				config.image.paste(element.gradientImage, (element.xPos,element.yPos), element.gradientImage)
			else :
			
				element = config.elementsArray[elementCount]
				if element.fader.fadingDone == True and random.random() < config.probDrawEffective :
					element.fader.fadingDone = False
					element.change(config)
					element.fader.image = element.gradientImage


			if element.fader.fadingDone == True : element.gradientImage = drawCircle(width, height, element.c1, element.c2)
			element.fader.fadeIn(config)
			#config.image.paste(element.gradientImage, (element.xPos,element.yPos), element.gradientImage)
			elementCount+=1



def runWork():
	global config
	while True:
		iterate()
		time.sleep(config.redrawRate)


def iterate():
	global config
	# Display bar, spinner, message or %
	reDraw()

	#for i in config.fadeArray:
	#	i.fadeIn(config)

	# Do the final rendering of the composited image
	config.render(config.image, 0, 0, config.screenWidth, config.screenHeight)

	## Vary the rate of change sometimes after initial startup has filled the frame
	if random.random() < config.probDrawChange:
		config.probDraw = random.uniform(0.001, 0.01)
		config.probDrawChange = 0.001
		# print(config.probDraw)

	if random.random() < .01 :
		config.probDrawEffective = config.probDraw


def main(run=True):
	global config

	config.debug = workConfig.getboolean("gradients", "debug")

	config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	config.draw = ImageDraw.Draw(config.image)

	config.vOffset = int(workConfig.get("gradients", "vOffset"))
	config.steps = int(workConfig.get("gradients", "steps"))
	config.redrawRate = float(workConfig.get("gradients", "redrawRate"))
	config.alpha1 = float(workConfig.get("gradients", "alpha1"))
	config.alpha2 = float(workConfig.get("gradients", "alpha2"))

	config.rowsShown = int(workConfig.get("gradients", "rowsShown"))
	config.colsShown = int(workConfig.get("gradients", "colsShown"))
	config.rowHeight = int(workConfig.get("gradients", "rowHeight"))
	config.angle = float(workConfig.get("gradients", "angle"))
	config.probDraw = float(workConfig.get("gradients", "probDraw"))
	config.blackProb = float(workConfig.get("gradients", "blackProb"))
	config.heightMin = int(workConfig.get("gradients", "heightMin"))
	config.heightMax = int(workConfig.get("gradients", "heightMax"))
	config.colorChoice = workConfig.get("gradients", "colorChoice")
	config.fadeThruBlack = workConfig.getboolean("gradients", "fadeThruBlack")
	config.grayProb = float(workConfig.get("gradients", "grayProb"))

	config.probDrawChange = float(workConfig.get("gradients", "probDrawChange"))
	config.probDrawEffective = 1.0

	config.boxMax = config.screenWidth - 2
	config.boxMaxAlt = config.boxMax + int(random.uniform(10, 30) * config.screenWidth)
	config.boxHeight = config.screenHeight - 3

	config.xPos = 0
	config.yPos = 0

	config.bgColorVals = (workConfig.get("gradients", "bgColor")).split(",")
	config.holderColor = tuple(map(lambda x: int(x), config.bgColorVals))
	config.grayLevelLower = int(workConfig.get("gradients", "grayLevelLower"))
	config.grayLevelUpper = int(workConfig.get("gradients", "grayLevelUpper"))
	config.dotBlurRadius = int(workConfig.get("gradients", "dotBlurRadius"))

	try:
		config.blockXOffset = tuple(map(lambda x: int(x), workConfig.get("gradients", "blockXOffset").split(",")))
		config.blockYOffset = tuple(map(lambda x: int(x), workConfig.get("gradients", "blockYOffset").split(",")))
	except Exception as e:
		print(str(e))
		config.blockXOffset = (0,0)
		config.blockYOffset = (0,0)


	config.boxWidth = 200
	config.gradientLevel = 2


	config.fadeArray = []
	config.elementsArray = []
	config.initializing = True
	reDraw()
	config.initializing = False
	config.probDrawEffective = config.probDraw

	if run:
		runWork()
