# ################################################### #
import math
import random
import time
from modules.configuration import bcolors
from modules import coloroverlay, colorutils
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps


class Fader:
	def __init__(self):
		self.doingRefresh = 1
		self.doingRefreshCount = 50
		self.fadingDone = False
		self.mode = "reveal"

	def fadeIn(self, config):
		if self.mode == "reveal" :
			self.reveal(config)
		else :
			self.faderize(config)


	def reveal(self, config):
		if self.fadingDone == False:
			if self.doingRefresh <= self.doingRefreshCount:

				'''
				self.blankImage = Image.new("RGBA", (self.width, self.height))
				d = ImageDraw.Draw(self.blankImage)
				d.rectangle((0, 0, self.width, self.height),
							outline=None, fill=(10,0,100,0))
				self.crossFade = Image.blend(
					self.blankImage,
					self.image,
					self.doingRefresh / self.doingRefreshCount,
				)
				'''
				revealedWidth =  self.width * self.doingRefresh / self.doingRefreshCount 
				revealedHeight = self.height * self.doingRefresh / self.doingRefreshCount

				cX  = round( (self.width - revealedWidth )/2)
				cY  = round( (self.height - revealedHeight )/2)
				box = (cX, cY, cX + revealedWidth, cY + revealedHeight)
				img = self.image.crop(box)
				config.image.paste(
					img, (round(self.xPos - revealedWidth/2), round(self.yPos - revealedHeight/2)), img
				)
				self.doingRefresh += 1
			
			else:
				#config.image.paste(self.image, (self.xPos, self.yPos), self.image)
				self.fadingDone = True
			



	def faderize(self, config):
		if self.fadingDone == False:
			if self.doingRefresh < self.doingRefreshCount:
				self.blankImage = Image.new("RGBA", (self.width, self.height))
				d = ImageDraw.Draw(self.blankImage)
				d.rectangle((0, 0, self.width, self.height),
							outline=None, fill=(10,0,100,0))
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
				config.image.paste(
					self.image, (self.xPos, self.yPos), self.image)
				self.fadingDone = True


def drawLine(*kwargs):
	lineColor = (255, 0, 0, 255)

	rounds = round(random.uniform(4, config.roundsMax))

	l = 1
	d = .5
	h = w = 0

	'''
	'''
	if random.random() < .1:
		h = round(random.uniform(0, 2*rounds))
	else:
		w = round(random.uniform(0, 2*rounds))

	unitImage = Image.new("RGBA", (round(rounds)*2 + w, round(rounds )*2  + h))
	unitImageDraw = ImageDraw.Draw(unitImage)
	#unitImageDraw.rectangle((0,0,unitImage.width,unitImage.height), fill = (255,0,0))

	xStart = round(rounds )
	yStart = round(rounds )
	#unitImageDraw.rectangle((xStart,yStart,xStart+10,yStart+10), fill = (0,250,0))

	widthLine = 0


	p0 = (xStart, yStart)
	p1 = (xStart, yStart)

	randomizeLevel = 1

	brightness = .2
	brightnessDelta = (1 - brightness) / rounds

	
	for i in range(0, rounds):
		lineColor = colorutils.getRandomColorHSV(config.lines_minHue, config.lines_maxHue, config.lines_minSaturation,
												 config.lines_maxSaturation, config.lines_minValue, config.lines_maxValue, 0, 0, 255, brightness)

		p0 = p1
		p1 = (p0[0]+l+w, p0[1])
		if random.random() < randomizeLevel:
			l += d
		unitImageDraw.line((p0, p1), fill=lineColor, width=widthLine)

		p0 = p1
		p1 = (p0[0], p0[1]+l+h)
		if random.random() < randomizeLevel:
			l += d
		unitImageDraw.line((p0, p1), fill=lineColor, width=widthLine)

		p0 = p1
		p1 = (p0[0]-l-w, p0[1])
		if random.random() < randomizeLevel:
			l += d
		unitImageDraw.line((p0, p1), fill=lineColor, width=widthLine)

		p0 = p1
		p1 = (p0[0], p0[1]-l-h)
		if random.random() < randomizeLevel:
			l += d
		unitImageDraw.line((p0, p1), fill=lineColor, width=widthLine)

		p0 = p1

		brightness += brightnessDelta
	
	return unitImage


''' ----------------------------------------------------------------------------------- '''


def reDraw(config):
	for i in range(0, config.simultaneousDraws):

		if random.random() < .1:

			xPos = round(random.uniform(0, config.canvasWidth))
			yPos = round(random.uniform(0, config.canvasHeight))

			unitImage = drawLine(config)

			fadeIn = Fader()
			# fadeIn.blankImage = Image.new("RGBA", (height, width))
			fadeIn.crossFade = Image.new("RGBA", (unitImage.width, unitImage.height))

			fadeIn.image = unitImage
			fadeIn.xPos = xPos
			fadeIn.yPos = yPos
			fadeIn.width = unitImage.width
			fadeIn.height = unitImage.height
			fadeIn.doingRefreshCount = config.fadeInRefreshCount

			config.fadeArray.append(fadeIn)
			# config.image.paste(unitImage, (xPos,yPos), unitImage)


def iterate():
	global config, expandingRingsRing, lastRate, calibrated, cycleCount
	#config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.draw.rectangle(
		(0, 0, config.screenWidth, config.screenHeight), fill=config.backgroundColor)

	reDraw(config)

	for i in config.fadeArray:
		i.fadeIn(config)

	if len(config.fadeArray) > 400:
		config.fadeArray = config.fadeArray[:200]

	# Do the final rendering of the composited image
	config.render(config.image, 0, 0, config.screenWidth, config.screenHeight)


def main(run=True):
	global config
	global expandingRingss

	expandingRingss = []
	config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.draw = ImageDraw.Draw(config.image)

	config.redrawSpeed = float(workConfig.get("forms", "redrawSpeed"))

	config.bg_minHue = float(workConfig.get("forms", "bg_minHue"))
	config.bg_maxHue = float(workConfig.get("forms", "bg_maxHue"))
	config.bg_minSaturation = float(
		workConfig.get("forms", "bg_minSaturation"))
	config.bg_maxSaturation = float(
		workConfig.get("forms", "bg_maxSaturation"))
	config.bg_minValue = float(workConfig.get("forms", "bg_minValue"))
	config.bg_maxValue = float(workConfig.get("forms", "bg_maxValue"))

	config.lines_minHue = float(workConfig.get("forms", "lines_minHue"))
	config.lines_maxHue = float(workConfig.get("forms", "lines_maxHue"))
	config.lines_minSaturation = float(
		workConfig.get("forms", "lines_minSaturation"))
	config.lines_maxSaturation = float(
		workConfig.get("forms", "lines_maxSaturation"))
	config.lines_minValue = float(workConfig.get("forms", "lines_minValue"))
	config.lines_maxValue = float(workConfig.get("forms", "lines_maxValue"))
	config.modeChangeProb = .01

	config.roundsMax = int(workConfig.get("forms", "roundsMax"))
	config.simultaneousDraws = int(workConfig.get("forms", "simultaneousDraws"))
	config.fadeInRefreshCount = int(workConfig.get("forms", "fadeInRefreshCount"))
	backgroundColor = (workConfig.get("forms", "backgroundColor")).split(",")
	config.backgroundColor = tuple(int(x) for x in backgroundColor)

	config.unitBlockSize = [400, 400]
	config.fadeArray = []



def runWork():
	global config
	print(bcolors.OKGREEN + "** " + bcolors.BOLD)
	print("Running bismuth.py")
	print(bcolors.ENDC)
	while True:
		iterate()
		time.sleep(config.redrawSpeed)
