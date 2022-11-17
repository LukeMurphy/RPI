import math
import random
import threading
import time
from modules.configuration import bcolors
from modules import colorutils
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps


class Fader:
	def __init__(self):
		self.doingRefresh = 0
		self.doingRefreshCount = 50
		self.fadingDone = False
		self.rotation = 0

	def fadeIn(self, config):
		if self.fadingDone == False:
			if self.doingRefresh < self.doingRefreshCount:
				self.blankImage = Image.new("RGBA", (self.width, self.height))
				d = ImageDraw.Draw(self.blankImage)
				d.rectangle((0,0,self.width,self.height), outline=None, fill =(0,0,0,0))
				self.crossFade = Image.blend(
					self.blankImage,
					self.image,
					self.doingRefresh / self.doingRefreshCount,
				)
				cf = self.crossFade.rotate(self.rotation ,0,1)
				config.image.paste(
					cf, (self.xPos, self.yPos), cf
				)
				self.doingRefresh += 1
			else:
				config.image.paste(self.image, (self.xPos, self.yPos), self.image)
				self.fadingDone = True



# Now drawing a gradient with 3 points
def drawBar(width=32, height=32, c1=(0, 0, 0, 0), c2=(0, 0, 0, 0), c3=(255,255,255,255)):
	global config

	gradientImage = Image.new("RGBA", (width, height))
	gradientImageDraw = ImageDraw.Draw(gradientImage)

	# draw box container
	gradientImageDraw.rectangle(
		(0, 0, width, height), outline=None, fill=(config.holderColor)
	)

	# draw bar
	# round this later so we get continuous segments
	steps = (config.steps/2) 
	segmentHeight = (height/2)
	bandHeigth = (segmentHeight / steps)
	arc = (math.pi) / bandHeigth

	if len(c1) == 3:
		dA = 0
	else:
		dA = (c2[3] - c1[3]) / steps

	dR1 = (c2[0] - c1[0]) / steps
	dG1 = (c2[1] - c1[1]) / steps
	dB1 = (c2[2] - c1[2]) / steps
	dA1 = (c2[3] - c1[3]) / steps

	dR2 = (c3[0] - c2[0]) / steps
	dG2 = (c3[1] - c2[1]) / steps
	dB2 = (c3[2] - c2[2]) / steps
	dA2 = (c3[3] - c2[3]) / steps

	rates = [(dR1,dG1,dB1,dA),(dR2,dG2,dB2,dA)]
	startColors = [c1,c2]
	endColors = [c2,c3]

	yPos = 0
	for seg in range(0,2):
		for n in range(0, round(steps)):
			yPos = (n * bandHeigth + seg * segmentHeight)
			yPos2 = (n + 1) * bandHeigth + seg * segmentHeight
			xPos = 0
			xPos2 = width
			#b = math.sin(arc * n)
			#b = n
			rVd = round(startColors[seg][0] + n * rates[seg][0])
			gVd = round(startColors[seg][1] + n * rates[seg][1])
			bVd = round(startColors[seg][2] + n * rates[seg][2])

			if len(startColors[seg]) == 4:
				bAd = round(startColors[seg][3] + (n * rates[seg][3]))
			else:
				bAd = 255
			
			barColorDisplay = (rVd, gVd, bVd, bAd)
			
			gradientImageDraw.rectangle(
				(xPos, yPos, xPos2, yPos2), fill=barColorDisplay, outline=barColorDisplay
			)


	return gradientImage


def reDraw(config):
	for i in range(0, config.rowsShown):

		if random.random() < config.drawBarProb:

			width = round(random.uniform(config.minWidth,config.maxWidth))
			height = round(random.uniform(config.heightMin,config.heightMax))

			xPos = round(random.uniform(0, config.canvasWidth))
			yPos = round(random.uniform(0, config.canvasHeight))

			#yPos = 0

			if config.colorChoice == "manual":
				c1  = colorutils.getRandomColorHSV(hMin=config.c1[0],hMax=config.c1[1],sMin=config.c1[2],sMax=config.c1[3],vMin=config.c1[4],vMax=config.c1[5],dropHueMin=0,dropHueMax=0,a=config.alpha1)
				c2  = colorutils.getRandomColorHSV(hMin=config.c2[0],hMax=config.c2[1],sMin=config.c2[2],sMax=config.c2[3],vMin=config.c2[4],vMax=config.c2[5],dropHueMin=0,dropHueMax=0,a=config.alpha2)
				c3  = colorutils.getRandomColorHSV(hMin=config.c3[0],hMax=config.c3[1],sMin=config.c3[2],sMax=config.c3[3],vMin=config.c3[4],vMax=config.c3[5],dropHueMin=0,dropHueMax=0,a=255)


			elif config.colorChoice == "rgbAlpha":
				c1 = colorutils.randomColorAlpha(
					config.brightness, config.alpha1, config.alpha1
				)
				c2 = colorutils.randomColorAlpha(
					config.brightness, config.alpha2, config.alpha2
				)
				c3  = colorutils.getRandomColorHSV(hMin=190.0,hMax=200.0,sMin=.9,sMax=1.0,vMin=.90,vMax=1.0,dropHueMin=0,dropHueMax=0,a=255)
			elif config.colorChoice == "rgb":
				c1 = colorutils.getRandomRGB(config.brightness)
				c2 = colorutils.getRandomRGB(config.brightness)
				c3 = colorutils.getRandomRGB(config.brightness)
			elif config.colorChoice == "random":
				c1 = colorutils.randomColor(config.brightness)
				c2 = colorutils.randomColor(config.brightness)
				c3 = colorutils.randomColor(config.brightness)
			else:
				c1 = colorutils.getRandomColorWheel(config.brightness)
				c2 = colorutils.getRandomColorWheel(config.brightness)
				c3 = colorutils.getRandomColorWheel(config.brightness)

			#c1  = colorutils.getRandomColorHSV(hMin=30.0,hMax=54.0,sMin=.9,sMax=1.0,vMin=.9,vMax=1.0,dropHueMin=0,dropHueMax=0,a=255)
			#c2  = colorutils.getRandomColorHSV(hMin=190.0,hMax=200.0,sMin=.0,sMax=.0,vMin=1.0,vMax=1.0,dropHueMin=0,dropHueMax=0,a=255)


			if config.fromBlack  == True :
				c1 = (0, 0, 0, 255)
			
			if random.random() < config.blackProb:
				c1 = (0, 0, 0, 255)
				c2 = (0, 0, 0, 255)
				c3 = (0, 0, 0, 255)

			gradientImage = drawBar(width, height, c1, c2, c3)


			fadeIn = Fader()
			# fadeIn.blankImage = Image.new("RGBA", (height, width))
			fadeIn.crossFade = Image.new("RGBA", (height, width))
			fadeIn.image = gradientImage
			fadeIn.xPos = xPos
			fadeIn.yPos = yPos
			fadeIn.height = gradientImage.height
			fadeIn.width = gradientImage.width
			fadeIn.doingRefreshCount = config.fadeInRefreshCount
			fadeIn.rotation = random.uniform(-config.angleRotationRange,config.angleRotationRange)

			config.fadeArray.append(fadeIn)

			# config.image.paste(gradientImage, (xPos,yPos), gradientImage)


def runWork():
	global config
	print(bcolors.OKGREEN + "** " + bcolors.BOLD)
	print("Running gradients.py")
	print(bcolors.ENDC)
	while True:
		iterate()
		time.sleep(config.redrawRate)


def iterate():
	global config
	# Display bar, spinner, message or %
	reDraw(config)

	for i in config.fadeArray:
		i.fadeIn(config)

	# some crude memory management ;)
	if len(config.fadeArray) > 400 :
		config.fadeArray = config.fadeArray[:100]

	if random.random() < config.colorChange:	
		index = math.floor(random.uniform(0,len(config.colorModes)))
		if index == len(config.colorModes) : index = 0
		config.colorChoice = config.colorModes[index]


	# Do the final rendering of the composited image

	temp = config.image.copy()

	if config.rotateDrawing != 0 :
		temp = temp.rotate(config.rotateDrawing)
	config.render(temp, 0, 0, config.screenWidth, config.screenHeight)

	'''
	## Vary the rate of change sometimes after initial startup has filled the frame
	if random.random() < config.probDrawChange:
		config.probDraw = random.uniform(0.001, 0.05)
		config.probDrawChange = 0.001
		# print(config.probDraw)

	if random.random() < .01 :
		config.probDrawEffective = config.probDraw
	'''


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
	config.rowHeight = int(workConfig.get("gradients", "rowHeight"))
	config.angle = float(workConfig.get("gradients", "angle"))
	config.angleRotationRange = float(workConfig.get("gradients", "angle"))
	config.probDraw = float(workConfig.get("gradients", "probDraw"))
	config.blackProb = float(workConfig.get("gradients", "blackProb"))

	try:
		config.drawBarProb = float(workConfig.get("gradients", "drawBarProb"))
	except Exception as e:
		config.drawBarProb = float(workConfig.get("gradients", "blackProb"))
		print(str(e))

	config.heightMin = int(workConfig.get("gradients", "heightMin"))
	config.heightMax = int(workConfig.get("gradients", "heightMax"))
	config.colorChoice = workConfig.get("gradients", "colorChoice")
	
	config.fadeInRefreshCount = int(workConfig.get("gradients", "fadeInRefreshCount"))

	config.probDrawChange = float(workConfig.get("gradients", "probDrawChange"))
	config.probDrawEffective = config.probDrawChange

	config.boxMax = config.screenWidth - 2
	config.boxMaxAlt = config.boxMax + int(random.uniform(10, 30) * config.screenWidth)
	config.boxHeight = config.screenHeight - 3

	config.colorModes = ["rgb", "getRandomColorWheel", "randomColor", "manual"]

	c1 = workConfig.get("gradients", "c1").split(",")
	c2 = workConfig.get("gradients", "c2").split(",")
	c3 = workConfig.get("gradients", "c3").split(",")

	config.c1  = tuple(map(lambda x: float(float(x) * config.brightness), c1))
	config.c2  = tuple(map(lambda x: float(float(x) * config.brightness), c2))
	config.c3  = tuple(map(lambda x: float(float(x) * config.brightness), c3))


	try:
		config.fromBlack = workConfig.getboolean("gradients", "fromBlack")
	except Exception as e:
		print(str(e))
		config.fromBlack = False

	try:
		config.rotateDrawing = float(workConfig.get("gradients", "rotate"))
	except Exception as e:
		print(str(e))
		config.rotateDrawing = 0


	try:
		config.colorChange = float(workConfig.get("gradients", "colorChange"))
	except Exception as e:
		print(str(e))
		config.colorChange = 0


	try:
		config.minWidth = int(workConfig.get("gradients", "minWidth"))
		config.maxWidth = int(workConfig.get("gradients", "maxWidth"))
	except Exception as e:
		print(str(e))
		config.minWidth = 4
		config.maxWidth = 16

	config.xPos = 0
	config.yPos = 0
	config.holderColor = (120, 120, 120, 100)
	config.boxWidth = 200
	config.gradientLevel = 2
	config.barColorStart = (0, 0, 100, 255)
	config.barColorEnd = (255, 0, 0, 255)

	config.fadeArray = []

	config.usedSpots = []

	if run:
		runWork()
