import datetime
import math
import random
import textwrap
import time

from modules import badpixels, coloroverlay, colorutils
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageOps


class unit:
	def __init__(self, config):
		self.config = config
		self.xPos = 0
		self.yPos = 0
		self.image = Image.new("RGBA", (100, 100))
		self.draw = ImageDraw.Draw(self.image)
		self.state = 0

	def update(self):
		self.state = 0 if self.state == 1 else 1

	def render(self, offset=False):

		xPos = self.xPos
		yPos = self.yPos

		if offset == True:
			xPos = self.xPos + self.config.xOffset
			yPos = self.yPos + self.config.yOffset

		box = (
			xPos - self.objWidth,
			yPos - self.objWidth,
			xPos + self.objWidth,
			yPos + self.objWidth,
		)

		fillColor = self.fillColor if self.state == 0 else self.altFillColor
		self.config.draw.ellipse(box, fill=fillColor, outline=fillColor)

	def changeColor(self):
		self.fillColor = colorutils.randomColor(random.random())
		self.outlineColor = colorutils.getRandomRGB()


def main(run=True):
	global config, directionOrder
	print("---------------------")
	print("OPTIC Loaded")
	colorutils.brightness = config.brightness
	config.canvasImageWidth = config.screenWidth
	config.canvasImageHeight = config.screenHeight
	config.canvasImageWidth -= 4
	config.canvasImageHeight -= 4

	config.numUnits = 2

	config.fontColorVals = (workConfig.get("optics", "fontColor")).split(",")
	config.fontColor = tuple(map(lambda x: int(x), config.fontColorVals))

	config.outlineColorVals = (workConfig.get("optics", "outlineColor")).split(",")
	config.outlineColor = tuple(map(lambda x: int(x), config.outlineColorVals))

	config.bgColorVals = (workConfig.get("optics", "bgColor")).split(",")
	config.bgColor = tuple(map(lambda x: int(x), config.bgColorVals))

	config.colorAVals = (workConfig.get("optics", "colorA")).split(",")
	config.colorA = tuple(map(lambda x: int(x), config.colorAVals))

	config.colorBVals = (workConfig.get("optics", "colorB")).split(",")
	config.colorB = tuple(map(lambda x: int(x), config.colorBVals))

	config.xOffset = int(workConfig.get("optics", "xOffset"))
	config.yOffset = int(workConfig.get("optics", "yOffset"))
	config.objWidth = int(workConfig.get("optics", "objWidth"))
	config.containerWidth = int(workConfig.get("optics", "containerWidth"))
	config.transitSpeed = float(workConfig.get("optics", "transitSpeed"))
	config.refreshRate = float(workConfig.get("optics", "refreshRate"))
	config.blinkRate = float(workConfig.get("optics", "blinkRate"))

	"""""" """""" """""" """""" """""" """""" """""" """""" """""" """"""

	config.canvasImage = Image.new(
		"RGBA", (config.canvasImageWidth, config.canvasImageHeight)
	)

	"""""" """""" """""" """""" """""" """""" """""" """""" """""" """"""
	config.unitArray = []
	config.xPositions = [48, 144]
	config.yPositions = [80, 80]

	# config.fills = [(0,0,255),(0,0,255)]
	config.fills = [(0, 0, 0), (255, 255, 255)]
	config.fills = [config.colorA, config.colorB]

	config.timeDelta = 0
	config.t1 = time.time()
	config.t2 = time.time()

	for i in range(0, config.numUnits):
		obj = unit(config)
		obj.fillColor = config.fills[i]
		altFillIndex = 0 if i == 1 else 1
		obj.altFillColor = config.fills[altFillIndex]
		obj.outlineColor = config.fills[i]
		obj.objWidth = config.containerWidth
		obj.xPos = config.xPositions[i]
		obj.yPos = config.yPositions[i]
		config.unitArray.append(obj)

	for i in range(0, config.numUnits):
		obj = unit(config)
		obj.fillColor = config.fills[0]
		obj.outlineColor = config.fills[0]
		altFillIndex = 1
		obj.altFillColor = config.fills[altFillIndex]
		obj.objWidth = config.objWidth
		obj.xPos = config.xPositions[i]
		obj.yPos = config.yPositions[i]
		config.unitArray.append(obj)

	setUp()

	if run:
		runWork()


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
		time.sleep(config.refreshRate)


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def iterate():
	global config

	config.draw.rectangle(
		(0, 0, config.screenWidth - 1, config.screenHeight - 1),
		fill=config.bgColor,
		outline=config.outlineColor,
	)

	config.t2 = time.time()
	delta = config.t2 - config.t1
	config.timeDelta += delta
	config.t1 = config.t2

	config.fills = [config.colorA, config.colorB, config.colorA, config.colorB]

	l = len(config.unitArray)
	for i in range(0, l):
		obj = config.unitArray[i]

		obj.fillColor = config.fills[i]
		altFillIndex = 0 if i == 1 else 1
		obj.altFillColor = config.fills[altFillIndex]
		obj.outlineColor = config.fills[i]

		if i > 1:
			obj.fillColor = config.fills[2]
			obj.outlineColor = config.fills[2]
			altFillIndex = 3

			if config.timeDelta > config.blinkRate:
				obj.update()
			obj.render(True)
		else:
			obj.render()

	config.yOffset -= config.transitSpeed

	if config.yOffset < -config.screenHeight / 2 - config.objWidth:
		config.yOffset = config.screenHeight / 2 + config.objWidth / 2
		config.colorA = colorutils.randomColor(config.brightness)
		config.colorB = colorutils.randomColor(config.brightness)

	config.render(config.image, 0, 0)

	if config.timeDelta > config.blinkRate:
		config.timeDelta = 0


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def callBack():
	global config, XOs
	return True


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
