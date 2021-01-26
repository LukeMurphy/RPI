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

	def fadeIn(self, config):
		if self.fadingDone == False:
			if self.doingRefresh < self.doingRefreshCount:
				self.blankImage = Image.new("RGBA", (self.width, self.height))
				d = ImageDraw.Draw(self.blankImage)
				d.rectangle((0,0,self.width,self.height), outline=None, fill =(100,0,0,0))
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

	# draw bar
	vLines = round((height) / config.steps)

	vLines  = 4;
	arc = (math.pi) / vLines
	dR = c2[0] - c1[0]
	dG = c2[1] - c1[1]
	dB = c2[2] - c1[2]

	if len(c1) == 3:
		dA = 0
	else:
		dA = c2[3] - c1[3]

	for n in range(0, vLines):
		xPos = 0
		xPos2 = width/4 * n
		yPos = n * config.steps
		yPos2 = width/4 * n
		b = math.sin(arc * n)
		rVd = int(c1[0] + (b * dR))
		gVd = int(c1[1] + (b * dG))
		bVd = int(c1[2] + (b * dB))

		if len(c1) == 4:
			bAd = int(c1[3] + (b * dA))
		else:
			bAd = 255
		barColorDisplay = (rVd, gVd, bVd, bAd)
		gradientImageDraw.ellipse((xPos, yPos, xPos2, yPos2), fill=barColorDisplay, outline=None)

	return gradientImage


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
	steps = round(config.steps/2)
	segmentHeight = round(height/2)
	bandHeigth = round(segmentHeight / steps)
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


	for seg in range(0,2):
		for n in range(0, steps):
			yPos = n * bandHeigth + seg * segmentHeight
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
				(xPos, yPos, xPos2, yPos2), fill=barColorDisplay, outline=None
			)
	if random.random() < .95 :
		pass
		#gradientImage = gradientImage.rotate(180 * random.random())

	return gradientImage


def reDraw(
	rows=16, rowHeight=16, angle=90, prob=0.08, blackProb=0.5, heightRange=(6, 96)
):
	for i in range(0, rows):

		if random.random() < prob:
			#height = round(random.uniform(heightRange[0], heightRange[1]))
			#width = height

			width = round(random.uniform(4,100))
			height = heightRange[1]
			height = rowHeight
			xPos = round(random.uniform(0, config.canvasWidth - width))
			yPos = round(random.uniform(0, config.canvasHeight - 32))

			#yPos = i * rowHeight
			# angle = random.uniform(0,360)
			#

			if config.colorChoice == "rgbAlpha":
				c1 = colorutils.randomColorAlpha(
					config.brightness, config.alpha1, config.alpha1
				)
				c2 = colorutils.randomColorAlpha(
					config.brightness, config.alpha2, config.alpha2
				)
			elif config.colorChoice == "rgb":
				c1 = colorutils.getRandomRGB(config.brightness)
				c2 = colorutils.getRandomRGB(config.brightness)
			else:
				c1 = colorutils.getRandomColorWheel(config.brightness)
				c2 = colorutils.getRandomColorWheel(config.brightness)

			c1  = colorutils.getRandomColorHSV(hMin=30.0,hMax=54.0,sMin=.9,sMax=1.0,vMin=.9,vMax=1.0,dropHueMin=0,dropHueMax=0,a=255)
			c2  = colorutils.getRandomColorHSV(hMin=190.0,hMax=200.0,sMin=.0,sMax=.0,vMin=1.0,vMax=1.0,dropHueMin=0,dropHueMax=0,a=255)
			c3  = colorutils.getRandomColorHSV(hMin=190.0,hMax=200.0,sMin=.9,sMax=1.0,vMin=.90,vMax=1.0,dropHueMin=0,dropHueMax=0,a=255)

			#print(c1,c2)

			if random.random() < blackProb:
				c1 = (0, 0, 0, 255)
				c2 = (0, 0, 0, 255)

			gradientImage = drawBar(width, height, c1, c2, c3)

			#gradientImage = drawCircle(width, height, c1, c2)
			
			#gradientImage = gradientImage.rotate(angle, expand=1)

			# gradientImage = transformImage(gradientImage)

			fadeIn = Fader()
			# fadeIn.blankImage = Image.new("RGBA", (height, width))
			fadeIn.crossFade = Image.new("RGBA", (height, width))
			fadeIn.image = gradientImage
			fadeIn.xPos = xPos
			fadeIn.yPos = yPos
			fadeIn.height = gradientImage.height
			fadeIn.width = gradientImage.width
			fadeIn.doingRefreshCount = config.fadeInRefreshCount

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
	reDraw(
		config.rowsShown,
		config.rowHeight,
		config.angle,
		config.probDrawEffective,
		config.blackProb,
		(config.heightMin, config.heightMax),
	)

	for i in config.fadeArray:
		i.fadeIn(config)

	# Do the final rendering of the composited image
	config.render(config.image, 0, 0, config.screenWidth, config.screenHeight)

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
	config.probDraw = float(workConfig.get("gradients", "probDraw"))
	config.blackProb = float(workConfig.get("gradients", "blackProb"))
	config.heightMin = int(workConfig.get("gradients", "heightMin"))
	config.heightMax = int(workConfig.get("gradients", "heightMax"))
	config.colorChoice = workConfig.get("gradients", "colorChoice")
	
	config.fadeInRefreshCount = int(workConfig.get("gradients", "fadeInRefreshCount"))

	config.probDrawChange = float(workConfig.get("gradients", "probDrawChange"))
	config.probDrawEffective = config.probDrawChange

	config.boxMax = config.screenWidth - 2
	config.boxMaxAlt = config.boxMax + int(random.uniform(10, 30) * config.screenWidth)
	config.boxHeight = config.screenHeight - 3

	config.xPos = 0
	config.yPos = 0
	config.holderColor = (0, 100, 0, 100)
	config.boxWidth = 200
	config.gradientLevel = 2
	config.barColorStart = (0, 0, 100, 255)
	config.barColorEnd = (255, 0, 0, 255)

	config.fadeArray = []

	if run:
		runWork()
