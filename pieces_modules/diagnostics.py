import argparse
import datetime
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

		self.image = Image.new("RGBA", (100, 100))
		self.fillColor = colorutils.getRandomRGB()
		self.outlineColor = colorutils.getRandomRGB(config.brightness)
		self.objWidth = 20
		self.objWidthMax = 26
		self.objWidthMin = 13

		self.draw = ImageDraw.Draw(self.image)

	def update(self):
		self.xPos += self.dx
		self.yPos += self.dy

		self.xPosR += self.dx
		self.yPosR += self.dy

		if self.xPosR + self.objWidth > self.config.screenWidth:
			self.xPosR = self.config.screenWidth - self.objWidth
			self.xPos = self.config.screenWidth - self.objWidth
			self.changeColor()
			self.dx *= -1
		if self.yPosR + self.objWidth > self.config.screenHeight:
			self.yPosR = self.config.screenHeight - self.objWidth
			self.yPos = self.config.screenHeight - self.objWidth
			self.changeColor()
			self.dy *= -1
		if self.xPosR < 0:
			self.xPosR = 0
			self.xPos = 0
			self.changeColor()
			self.dx *= -1
		if self.yPosR < 0:
			self.yPosR = 0
			self.yPos = 0
			self.changeColor()
			self.dy *= -1

		if self.dx == 0 and self.dy == 0:
			if random.random() > 0.5:
				self.dx = 2 * random.random()
			if random.random() > 0.5:
				self.dy = 2 * random.random()

	def render(self):
		xPos = int(self.xPosR)
		yPos = int(self.yPosR)
		self.config.draw.rectangle(
			(xPos, yPos, xPos + self.objWidth, yPos + self.objWidth),
			fill=self.fillColor,
			outline=self.outlineColor,
		)

	def changeColor(self):
		self.fillColor = colorutils.randomColor(random.random())
		self.outlineColor = colorutils.getRandomRGB()
		if random.random() > 0.5:
			self.dx = 4 * random.random() + 2
		if random.random() > 0.5:
			self.dy = 4 * random.random() + 2
		if random.random() > 0.5:
			self.objWidth = int(random.uniform(self.objWidthMin, self.objWidthMax))


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def displayTest(config):
	# global config
	# config.draw.rectangle((0,0,config.screenWidth, config.screenHeight), fill=(0,0,0), outline=(0,0,0))
	config.draw.rectangle(
		(0, 0, config.screenWidth - 1, config.screenHeight - 1),
		fill=(0, 0, 0),
		outline=config.outlineColor,
	)
	config.draw.rectangle(
		(1, 1, config.screenWidth - 2, config.screenHeight - 2),
		fill=(0, 0, 0),
		outline=(0, 0, int(220 * config.brightness)),
	)
	config.draw.text((1, 0), "TOP", config.fontColor, font=config.font)
	config.draw.text(
		(1, config.screenHeight - 15), "BOTTOM", config.fontColor, font=config.font
	)

	tm = datetime.datetime.now()
	tm = time.ctime()
	config.draw.text((10, 24), tm, config.fontColor, font=config.font)

	w = 24
	h = 24
	xp = 10
	yp = 40

	rgbWheel = [
		(255, 0, 0),
		(255, 255, 0),
		(0, 255, 0),
		(0, 255, 255),
		(0, 0, 255),
		(255, 0, 255),
		(255, 255, 255),
	]

	for i in range(0, len(rgbWheel)):
		colorBlock = tuple(map(lambda x: int(int(x) * config.brightness), rgbWheel[i]))
		config.draw.rectangle(
			(xp, yp, xp + w, yp + h), fill=colorBlock, outline=colorBlock
		)
		xp += w

	yp += h
	xp = 10

	for i in range(0, len(rgbWheel)):
		colorBlock = tuple(
			map(lambda x: int(int(x) * config.brightness * 0.5), rgbWheel[i])
		)
		config.draw.rectangle(
			(xp, yp, xp + w, yp + h), fill=colorBlock, outline=colorBlock
		)
		xp += w

	for i in range(0, config.numUnits):
		obj = config.unitArray[i]
		if obj.move == True:
			obj.update()
		obj.render()

	config.render(config.image, 0, 0)


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def showGrid(config):
	# global config

	config.draw.rectangle(
		(0, 0, config.screenWidth, config.screenHeight),
		fill=config.bgColor,
		outline=(0, 0, 0),
	)
	config.canvasDraw.rectangle(
		(0, 0, config.canvasWidth - 1, config.canvasHeight - 1),
		fill=config.bgColor,
		outline=config.outlineColor,
	)
	config.canvasDraw.rectangle(
		(1, 1, config.canvasWidth - 2, config.canvasHeight - 2),
		fill=config.bgColor,
		outline=(0, 0, int(220 * config.brightness)),
	)

	# print(config.imageXOffset)

	for row in range(0, config.rows):
		for col in range(0, config.cols):
			xPos = col * config.tileSizeWidth
			yPos = row * config.tileSizeHeight
			config.canvasDraw.rectangle(
				(
					xPos,
					yPos,
					xPos + config.tileSizeWidth - 1,
					yPos + config.tileSizeHeight - 1,
				),
				fill=config.bgColor,
				outline=config.outlineColor,
			)

			displyInfo = str(col) + ", " + str(row) + ""
			config.canvasDraw.text(
				(xPos + 2, yPos - 1), displyInfo, config.fontColor, font=config.font
			)
			displyInfo = (
				""
				+ str(col * config.tileSizeWidth)
				+ ", "
				+ str(row * config.tileSizeHeight)
			)
			config.canvasDraw.text(
				(xPos + 2, yPos - 1 + config.fontSize), displyInfo, config.fontColor2, font=config.font
			)

	config.image.paste(
		config.canvasImage,
		(config.imageXOffset, config.imageYOffset),
		config.canvasImage,
	)

	# config.draw.rectangle((0,64,8,72), fill=(200,200,0), outline = (0,0,200))

	config.render(config.image, 0, 0)


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def drawPalette(config):
	# global config

	config.draw.rectangle(
		(0, 0, config.screenWidth, config.screenHeight),
		fill=config.bgColor,
		outline=(0, 0, 0),
	)
	config.canvasDraw.rectangle(
		(0, 0, config.canvasWidth - 1, config.canvasHeight - 1),
		fill=config.bgColor,
		outline=config.outlineColor,
	)
	config.canvasDraw.rectangle(
		(1, 1, config.canvasWidth - 2, config.canvasHeight - 2),
		fill=config.bgColor,
		outline=(0, 0, int(220 * config.brightness)),
	)

	# print(config.imageXOffset)

	hues = 360 / config.cols
	vals = 1 / config.rows
	sat = 1  # / config.rows

	for row in range(0, config.rows + 1):
		for col in range(0, config.cols):
			## Draw colors 0 thru 360
			xPos = col * config.tileSizeWidth
			yPos = row * config.tileSizeHeight

			hue = col * hues
			val = row * vals
			# sat = row * vals

			bgColor = colorutils.HSVToRGB(hue, sat, val)
			config.canvasDraw.rectangle(
				(
					xPos,
					yPos,
					xPos + config.tileSizeWidth - 1,
					yPos + config.tileSizeHeight - 1,
				),
				fill=bgColor,
				outline=config.outlineColor,
			)

			displyInfo = str(round(hue)) + "\n " + str(round(val * 10) / 10) + "\n"
			config.canvasDraw.text(
				(xPos + 2, yPos - 1), displyInfo, config.fontColor, font=config.font
			)
			# displyInfo  =  "\n" + str(col * config.tileSizeWidth) + ", " + str(row * config.tileSizeHeight)
			# config.canvasDraw.text((xPos + 2,yPos - 1),displyInfo,config.fontColor2,font=config.font)

	config.image.paste(
		config.canvasImage,
		(config.imageXOffset, config.imageYOffset),
		config.canvasImage,
	)

	# config.draw.rectangle((0,64,8,72), fill=(200,200,0), outline = (0,0,200))

	config.render(config.image, 0, 0)


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def main(config, workConfig, run=True):

	# global config, directionOrder
	print("** ---------------------")
	print("** Diag Loaded **")
	print(config)
	print("** ---------------------")

	colorutils.brightness = config.brightness
	# config.canvasImageWidth = config.screenWidth
	# config.canvasImageHeight = config.screenHeight
	# config.canvasImageWidth -= 4
	# config.canvasImageHeight -= 4
	config.delay = 0.02
	config.numUnits = 1

	config.fontColorVals = (workConfig.get("diag", "fontColor")).split(",")
	config.fontColor = tuple(
		map(lambda x: int(int(x) * config.brightness), config.fontColorVals)
	)
	config.outlineColorVals = (workConfig.get("diag", "outlineColor")).split(",")
	config.outlineColor = tuple(
		map(lambda x: int(int(x) * config.brightness), config.outlineColorVals)
	)
	config.bgColorVals = (workConfig.get("diag", "bgColor")).split(",")
	config.bgColor = tuple(
		map(lambda x: int(int(x) * config.brightness), config.bgColorVals)
	)
	config.useLastOverlay = False

	config.angle = 0

	try:
		config.fontSize = int(workConfig.get("diag", "fontSize"))
	except Exception as e:
		print(str(e))
		config.fontSize = 14
	try:
		config.imageXOffset = int(workConfig.get("displayconfig", "imageXOffset"))
	except Exception as e:
		print(str(e))
		config.imageXOffset = 0
	try:
		config.showGrid = workConfig.getboolean("diag", "showGrid")
	except Exception as e:
		print(str(e))
		config.showGrid = False
	try:
		fontColor2 = workConfig.get("diag", "fontColor2").split(",")
	except Exception as e:
		print(str(e))
		fontColor2 = [0, 200, 0]
	config.fontColor2 = tuple(
		map(lambda x: int(int(x) * config.brightness), fontColor2)
	)

	config.tileSizeWidth = int(workConfig.get("displayconfig", "tileSizeWidth"))
	config.tileSizeHeight = int(workConfig.get("displayconfig", "tileSizeHeight"))

	try:
		config.colorPalette = workConfig.getboolean("diag", "colorPalette")
	except Exception as e:
		print(str(e))
		config.colorPalette = False

	if config.colorPalette == True:
		# config.rows = round(config.canvasHeight / 16)
		# config.cols = round(config.canvasWidth / 16)
		# config.tileSizeWidth = round(config.canvasWidth / 16)
		# config.tileSizeHeight = round(config.canvasHeight / 16)
		pass

	"""""" """""" """""" """""" """""" """""" """""" """""" """""" """"""

	config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	config.draw = ImageDraw.Draw(config.image)
	config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.canvasDraw = ImageDraw.Draw(config.canvasImage)
	config.font = ImageFont.truetype(
		config.path + "/assets/fonts/freefont/FreeSansBold.ttf", config.fontSize
	)

	"""""" """""" """""" """""" """""" """""" """""" """""" """""" """"""
	config.unitArray = []
	for i in range(0, config.numUnits):
		obj = unit(config)
		# obj.move = False
		obj.objWidth = 5
		obj.objWidthMax = 4
		obj.objWidthMin = 3
		config.unitArray.append(obj)

	setUp()

	# if(run) : runWork()


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def setUp():
	pass
	# arg = "./assets/imgs/sks/skull-s2.png"
	# config.loadedImage = Image.open(arg , "r")
	# config.loadedImage.load()


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def runWork(config):
	# global blocks, config, XOs
	print("RUNNING DIAGNOSTICS")
	# gc.enable()

	while True:
		iterate(config)
		time.sleep(config.delay)


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def iterate(config):

	if config.colorPalette == True:
		drawPalette(config)
	else:
		if config.showGrid == True:
			showGrid(config)
		else:
			displayTest(config)


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def callBack():
	# global config, XOs
	return True


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
