# ################################################### #
import math
import random
import time
from modules.configuration import bcolors
from modules import colorutils
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps

colorutils.brightness = 1


class Vertical:

	outerColor = (0, 0, 50)
	innerColor = (130, 30, 0)
	borderColor = (50, 0, 0)

	xPos = 0
	yPos = 0
	vOffset = 0
	boxHeight = 0
	boxWidth = 0
	boxWidthDisplay = 0
	status = 0
	boxMax = 0
	inMotion = False

	def __init__(self, config):

		self.config = config
		self.boxMax = config.canvasWidth
		self.unitImage = Image.new("RGBA", (config.screenWidth, self.config.h))
		self.draw = ImageDraw.Draw(self.unitImage)
		self.BorderWidth = 2
		self.changeAction()

	def changeAction(self):
		self.CenterWidth = int(self.boxMax * config.widthPercentage)
		self.OuterWidth = int(self.boxMax / 2 - self.CenterWidth / 2 - self.BorderWidth)

	def make(self):
		self.changeAction()
		self.outer1 = (
			self.xPos,
			self.yPos,
			int(random.uniform(-self.config.var, self.config.var) + self.OuterWidth)
			+ 1,
			self.yPos + self.config.h,
		)
		self.border1 = (
			self.outer1[2],
			self.yPos,
			self.outer1[2] + int(random.uniform(-1, 1) + self.BorderWidth) + 1,
			self.yPos + self.config.h,
		)
		self.cntr = (
			self.border1[2],
			self.yPos,
			self.border1[2]
			+ int(random.uniform(-self.config.var, +self.config.var) + self.CenterWidth)
			+ 1,
			self.yPos + self.config.h,
		)
		self.border2 = (
			self.cntr[2],
			self.yPos,
			self.cntr[2] + int(random.uniform(0, 2) + self.BorderWidth) + 1,
			self.yPos + self.config.h,
		)
		self.outer2 = (
			self.border2[2],
			self.yPos,
			self.boxMax,
			self.yPos + self.config.h,
		)

	def reDraw(self):
		self.draw.rectangle(self.outer1, fill=self.config.outerColor)
		self.draw.rectangle(self.border1, fill=self.config.borderColor)
		self.draw.rectangle(self.cntr, fill=self.config.innerColor)
		self.draw.rectangle(self.border2, fill=self.config.borderColor)
		self.draw.rectangle(self.outer2, fill=self.config.outerColor)
		config.image.paste(self.unitImage, (0, round(self.vOffset)), self.unitImage)

	def done(self):
		return True


def drawElement():
	global config
	return True


def redraw():
	global config, vertArray
	for i in range(0, len(vertArray)):
		vert = vertArray[i]
		vert.reDraw()
	# This function does the motion and creates
	# new blocks
	reArraynge()

	if config.drawCenteringLines == True:
		drawCenteringLine()


def drawCenteringLine():
	global config

	config.draw.rectangle(
		(0, config.screenHeight / 2, config.screenWidth, config.screenHeight / 2),
		fill=(0, 200, 0),
	)
	config.draw.rectangle(
		(config.screenWidth / 2, 0, config.screenWidth / 2, config.screenHeight),
		fill=(0, 200, 0),
	)


def reArraynge():
	global config, vertArray

	# run through the array and reset each blocks new postition
	# to produce motion animation effect
	for i in range(0, config.layers):
		# vertArray[i].vOffset = i * config.blockHeight
		vertArray[i].vOffset += config.verticalSpeed

	if vertArray[config.layers - 1].vOffset > config.canvasHeight:
		# set the current width
		changeWidth()

		# Pop the last one off the array
		lastElement = vertArray.pop()

		# generate a replacement
		lastElement.changeAction()
		lastElement.make()

		# instert it at the start of the array
		vertArray.insert(0, lastElement)
		lastElement.vOffset = -config.blockHeight


def changeWidth():
	if config.inMotion == True:

		if config.widthPercentage <= config.destinationPercentage:
			config.var = config.varMulitplierWhenChangingUp * config.varBase
			config.multiplier = config.incrRate

		else:
			config.var = config.varMulitplierWhenChangingDown * config.varBase
			config.multiplier = config.reduceRate

		config.widthPercentage = config.widthPercentage * config.multiplier
	else:
		config.var = config.varBase

	if (
		abs(
			(config.widthPercentage - config.destinationPercentage)
			/ config.destinationPercentage
		)
		<= 0.01
		and config.inMotion == True
	):
		config.inMotion = False
		# print("done")

	if random.random() < config.inMotionProbability and config.inMotion == False:
		config.destinationPercentage = random.uniform(
			config.minPercentWidth, config.maxPercentWidth
		)
		config.inMotion = True
		# print ("==>", config.destinationPercentage, config.widthPercentage)


def changeColor():
	pass
	return True


def changeCall():
	pass
	return True


def callBack():
	global config
	pass


def runWork():
	global redrawSpeed
	while True:
		iterate()
		time.sleep(config.redrawSpeed)


def iterate():
	global config, vert, lastRate

	redraw()

	# draw = ImageDraw.Draw(config.image)
	# draw.rectangle((0,0,config.screenWidth-1, config.screenHeight-1),fill=None, outline=(0,255,0))

	config.render(config.image, 0, 0, config.screenWidth, config.screenHeight)

	callBack()
	count = 0
	# Done


def main(run=True):
	global config, workConfig
	global redrawSpeed
	global vert, vertArray
	vertArray = []
	config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	config.draw = ImageDraw.Draw(config.image)
	config.vOffset = int(workConfig.get("vertical", "vOffset"))
	config.drawCenteringLines = workConfig.getboolean("vertical", "drawCenteringLines")

	config.redrawSpeed = float(workConfig.get("vertical", "redrawSpeed"))
	config.blockHeight = int(workConfig.get("vertical", "blockHeight"))
	config.rateMultiplier = float(workConfig.get("vertical", "rateMultiplier"))
	config.rate = config.rateMultiplier * random.random()
	config.h = int(workConfig.get("vertical", "h"))
	config.var = int(workConfig.get("vertical", "var"))
	config.varBase = int(workConfig.get("vertical", "var"))
	config.varMulitplierWhenChangingUp = int(
		workConfig.get("vertical", "varMulitplierWhenChangingUp")
	)
	config.varMulitplierWhenChangingDown = int(
		workConfig.get("vertical", "varMulitplierWhenChangingDown")
	)

	config.destinationPercentage = float(
		workConfig.get("vertical", "destinationPercentage")
	)
	config.widthPercentage = float(workConfig.get("vertical", "widthPercentage"))
	config.multiplier = float(workConfig.get("vertical", "multiplier"))
	config.incrRate = float(workConfig.get("vertical", "incrRate"))
	config.reduceRate = float(workConfig.get("vertical", "reduceRate"))
	config.inMotionProbability = float(
		workConfig.get("vertical", "inMotionProbability")
	)
	config.brightness = float(workConfig.get("vertical", "brightness"))
	config.minPercentWidth = float(workConfig.get("vertical", "minPercentWidth"))
	config.maxPercentWidth = float(workConfig.get("vertical", "maxPercentWidth"))
	config.verticalSpeed = float(workConfig.get("vertical", "verticalSpeed"))

	config.outerColor = (workConfig.get("vertical", "outerColor")).split(",")
	config.outerColor = tuple(
		map(lambda x: int(int(x) * config.brightness), config.outerColor)
	)

	config.innerColor = (workConfig.get("vertical", "innerColor")).split(",")
	config.innerColor = tuple(
		map(lambda x: int(int(x) * config.brightness), config.innerColor)
	)

	config.borderColor = (workConfig.get("vertical", "borderColor")).split(",")
	config.borderColor = tuple(
		map(lambda x: int(int(x) * config.brightness), config.borderColor)
	)

	config.inMotion = False

	config.layers = int(config.canvasHeight / config.blockHeight)

	# print(layers)
	for i in range(0, config.layers):
		vert = Vertical(config)
		vert.make()
		vert.vOffset = i * config.blockHeight
		# print(vert.vOffset, config.blockHeight)
		vertArray.append(vert)
	if run:
		runWork()
