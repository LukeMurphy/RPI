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
				d.rectangle((0,0,self.width,self.height), outline=None, fill =(5,20,140,2))
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



# Now drawing a gradient with 3 points
def drawBar(config):

	gradientImage = Image.new("RGBA", (200, 200))
	gradientImageDraw = ImageDraw.Draw(gradientImage)

	rings = 14
	radiusBase = round(random.uniform(1,4))
	for r in range(rings,0,-1):
		radius = r * radiusBase
		spokes = 60
		steps = 2*math.pi/spokes 
		a = 50 - round(50 * r/rings)
		for i in range(0,spokes):
			angle = i * steps
			x = 50 + math.cos(angle) * radius
			y = 50 + math.sin(angle) * radius
			# draw box container
			gradientImageDraw.rectangle(
				(x, y, x + 3, y +3), outline=None, fill=(160,160,160,a)
			)

	
	return gradientImage


def reDraw(config):
	for i in range(0, 15):

		if random.random() < .1:

			xPos = round(random.uniform(0, config.canvasWidth)) - 50
			yPos = round(random.uniform(0, config.canvasHeight)) - 50			

			gradientImage = drawBar(config)


			fadeIn = Fader()
			# fadeIn.blankImage = Image.new("RGBA", (height, width))
			fadeIn.crossFade = Image.new("RGBA", (200, 200))
			fadeIn.image = gradientImage
			fadeIn.xPos = xPos
			fadeIn.yPos = yPos
			fadeIn.height = 200
			fadeIn.width = 200
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
	reDraw(config)

	for i in config.fadeArray:
		i.fadeIn(config)


	if len(config.fadeArray) > 400 :
		config.fadeArray = config.fadeArray[:100]

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

	config.debug = workConfig.getboolean("clouds", "debug")

	config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	config.draw = ImageDraw.Draw(config.image)

	config.vOffset = int(workConfig.get("clouds", "vOffset"))
	config.steps = int(workConfig.get("clouds", "steps"))
	config.redrawRate = float(workConfig.get("clouds", "redrawRate"))
	config.alpha1 = float(workConfig.get("clouds", "alpha1"))
	config.alpha2 = float(workConfig.get("clouds", "alpha2"))

	config.rowsShown = int(workConfig.get("clouds", "rowsShown"))
	config.rowHeight = int(workConfig.get("clouds", "rowHeight"))
	config.angle = float(workConfig.get("clouds", "angle"))
	config.probDraw = float(workConfig.get("clouds", "probDraw"))
	config.blackProb = float(workConfig.get("clouds", "blackProb"))
	config.heightMin = int(workConfig.get("clouds", "heightMin"))
	config.heightMax = int(workConfig.get("clouds", "heightMax"))
	config.colorChoice = workConfig.get("clouds", "colorChoice")
	
	config.fadeInRefreshCount = int(workConfig.get("clouds", "fadeInRefreshCount"))

	config.probDrawChange = float(workConfig.get("clouds", "probDrawChange"))
	config.probDrawEffective = config.probDrawChange

	config.boxMax = config.screenWidth - 2
	config.boxMaxAlt = config.boxMax + int(random.uniform(10, 30) * config.screenWidth)
	config.boxHeight = config.screenHeight - 3

	config.xPos = 0
	config.yPos = 0
	config.holderColor = (0, 0, 500, 100)
	config.boxWidth = 200
	config.gradientLevel = 2
	config.barColorStart = (0, 0, 100, 255)
	config.barColorEnd = (0, 0, 200, 255)

	config.fadeArray = []

	config.usedSpots = []

	if run:
		runWork()
