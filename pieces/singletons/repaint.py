import math
import random
import textwrap
import time

from modules import badpixels, coloroverlay, colorutils
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFont, ImageOps


class unit:
	def __init__(self, config):
		self.config = config
		self.xPos = 0
		self.yPos = 0
		self.xPosR = self.config.screenWidth / 2
		self.yPosR = self.config.screenHeight / 2
		self.move = True

		self.dx = random.uniform(-3, 3)
		self.dy = random.uniform(-3, 3)

		self.image = Image.new("RGBA", (60, 60))
		self.imageRotation = int(random.uniform(0, 60))
		self.draw = ImageDraw.Draw(self.image)

		self.fillColor = colorutils.getRandomRGB()
		self.outlineColor = colorutils.getRandomRGB()
		self.objWidth = 20
		self.objWidthMax = 26
		self.objWidthMin = 13

		self.xBoundry = 16
		self.yBoundry = 54

	def update(self):
		self.xPos += self.dx
		self.yPos += self.dy

		self.xPosR += self.dx
		self.yPosR += self.dy

		# self.objWidth = self.image.width
		# print(self.image.width)

		if self.xPosR + self.xBoundry > self.config.screenWidth:
			self.xPosR = self.config.screenWidth - self.xBoundry
			self.xPos = self.config.screenWidth - self.xBoundry
			self.changeColor()
			self.dx *= -1
		if self.yPosR + self.yBoundry > self.config.screenHeight:
			self.yPosR = self.config.screenHeight - self.yBoundry
			self.yPos = self.config.screenHeight - self.yBoundry
			self.changeColor()
			self.dy *= -1
		if self.xPosR < -self.xBoundry:
			self.xPosR = -self.xBoundry
			self.xPos = -self.xBoundry
			self.changeColor()
			self.dx *= -1
		if self.yPosR < -self.yBoundry:
			self.yPosR = -self.yBoundry
			self.yPos = -self.yBoundry
			self.changeColor()
			self.dy *= -1

		if self.dx == 0 or self.dy == 0:
			if random.random() > 0.5:
				self.dx = 2 * random.random()
			if random.random() > 0.5:
				self.dy = 2 * random.random()

	def render(self):
		xPos = 0
		yPos = self.handle
		xPosFinal = int(self.xPosR)
		yPosFinal = int(self.yPosR)
		"""
		ferrule = 14
		bristle = 19
		handle = 24
		brushWidth = 24
		handleWidth = 6
		holeWidth = 2
		holeHeight = 3
		"""
		shape = [
			xPos,
			yPos,
			xPos,
			yPos + self.ferrule,
			xPos,
			yPos + self.ferrule + self.bristle,
			xPos + self.brushWidth,
			yPos + self.ferrule + self.bristle,
			xPos + self.brushWidth,
			yPos,
			xPos + self.brushWidth / 2 + self.handleWidth / 2,
			yPos,
			xPos + self.brushWidth / 2 + self.handleWidth / 2,
			yPos - self.handle,
			xPos + self.brushWidth / 2 - self.handleWidth / 2,
			yPos - self.handle,
			xPos + self.brushWidth / 2 - self.handleWidth / 2,
			yPos,
			xPos,
			yPos,
		]

		# the brush outline
		self.draw.polygon(shape, fill=self.fillColor, outline=self.outlineColor)

		# the bristles
		self.draw.rectangle(
			(
				(xPos, yPos + self.ferrule),
				(xPos + self.brushWidth, yPos + self.ferrule + self.bristle),
			),
			fill=self.fillColor,
			outline=None,
		)

		# Line demarking bristles
		# self.draw.line(((xPos,yPos + self.ferrule), (xPos + self.brushWidth, yPos + self.ferrule)), fill=self.outlineColor, width=1)

		# hangling hole
		# self.draw.rectangle((xPos + self.brushWidth/2 - self.holeWidth/2, yPos - self.handle + 3, xPos + self.brushWidth/2 + self.holeWidth/2 , yPos - self.handle + 3 + self.holeHeight), fill=(0,0,0), outline=self.outlineColor)

		# rotate brush
		img = self.image.rotate(self.imageRotation, expand=True)

		# paste into image that is final render
		self.config.image.paste(img, (xPosFinal, yPosFinal), img)

	def changeColor(self):
		self.fillColor = colorutils.randomColor(random.uniform(0.2, config.brightness))
		self.outlineColor = colorutils.getRandomRGB(
			random.uniform(0.2, config.brightness)
		)
		if random.random() > 0.5:
			self.dx = random.uniform(-self.speedRange, self.speedRange)
		if random.random() > 0.5:
			self.dy = random.uniform(-self.speedRange, self.speedRange)

		if random.random() < self.orthoProbability and self.imageRotation not in [
			0,
			180,
			-90,
			90,
		]:
			if random.random() > 0.5:
				if random.random() > 0.5:
					self.imageRotation = 0
				else:
					self.imageRotation = 180
			else:
				if random.random() > 0.5:
					self.imageRotation = 90
				else:
					self.imageRotation = -90
		elif random.random() < self.rotationProbability:
			self.imageRotation = int(random.uniform(-60, 60))

		if self.imageRotation in [-90]:
			self.fillColor = (0, 0, 0)

		# if(random.random() > .5): self.objWidth = int(random.uniform(self.objWidthMin,self.objWidthMax))


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def main(run=True):
	global config, directionOrder, workConfig
	print("---------------------")
	print("RE:PAINT Loaded")

	try:
		config.delay = float(workConfig.get("repaint", "repaintDelay"))
		config.randomBrushWidth = workConfig.getboolean("repaint", "randomBrushWidth")
		config.numUnits = int(workConfig.get("repaint", "numBrushes"))
		config.ferrule = int(workConfig.get("repaint", "ferrule"))
		config.bristle = int(workConfig.get("repaint", "bristle"))
		config.handle = int(workConfig.get("repaint", "handle"))
		config.brushWidth = int(workConfig.get("repaint", "brushWidth"))
		config.handleWidth = int(workConfig.get("repaint", "handleWidth"))
		config.holeWidth = int(workConfig.get("repaint", "holeWidth"))
		config.holeHeight = int(workConfig.get("repaint", "holeHeight"))
		config.speedRange = float(workConfig.get("repaint", "speedRange"))
		config.rotationProbability = float(
			workConfig.get("repaint", "rotationProbability")
		)
		config.orthoProbability = float(workConfig.get("repaint", "orthoProbability"))
		config.rectifyProbability = float(
			workConfig.get("repaint", "rectifyProbability")
		)

	except Exception as e:
		print(str(e))

	colorutils.brightness = config.brightness
	config.canvasImageWidth = config.screenWidth
	config.canvasImageHeight = config.screenHeight
	config.canvasImageWidth -= 4
	config.canvasImageHeight -= 4

	"""""" """""" """""" """""" """""" """""" """""" """""" """""" """"""

	config.canvasImage = Image.new(
		"RGBA", (config.canvasImageWidth, config.canvasImageHeight)
	)

	"""""" """""" """""" """""" """""" """""" """""" """""" """""" """"""
	config.unitArray = []
	for i in range(0, config.numUnits):
		obj = unit(config)
		obj.ferrule = config.ferrule
		obj.bristle = config.bristle
		obj.handle = config.handle
		obj.handleWidth = config.handleWidth
		if config.randomBrushWidth == True:
			obj.brushWidth = int(random.uniform(config.handleWidth, config.brushWidth))
		else:
			obj.brushWidth = config.brushWidth
		obj.holeWidth = config.holeWidth
		obj.holeHeight = config.holeHeight
		obj.speedRange = config.speedRange
		obj.rotationProbability = config.rotationProbability
		obj.orthoProbability = config.orthoProbability
		config.unitArray.append(obj)

	config.rectify = True

	setUp()

	if run:
		runWork()


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def setUp():
	global config
	pass


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def runWork():
	global blocks, config, XOs
	# gc.enable()
	while True:
		iterate()
		time.sleep(config.delay)


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def iterate():
	global config

	## No trails
	# config.draw.rectangle((0,0,config.screenWidth, config.screenHeight), fill=(0,0,0), outline=(0,0,0))

	if random.random() < config.rectifyProbability:
		config.rectify = True

	if random.random() < config.rectifyProbability:
		config.rectify = False

	for i in range(0, config.numUnits):
		obj = config.unitArray[i]
		if config.rectify == True:
			obj.orthoProbability = 0.99
		else:
			obj.orthoProbability = config.orthoProbability
		if obj.move == True:
			obj.update()
		obj.render()

	config.render(config.image, 0, 0)


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def callBack():
	global config, XOs
	return True


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
