# ################################################### #
import colorsys
import math
import random
import sys
import time
from modules.configuration import bcolors
import PIL.Image
from modules import colorutils
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps

"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
# make script to subtly shift blue color rectangles slowly
"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


class Fill:

	width = 100
	height = 162
	rows = 1
	cols = 1
	x = y = 0
	currentColor = [0, 0, 0, 255]
	targetColor = [0, 0, 0, 255]
	rangeOfVals = [50, 80]
	rateOfChange = 0

	hue = 180
	hueBase = 180
	hueTarget = 1
	sat = 0.4
	val = 0.4
	hueRate = 0
	hueRateBase = 0

	import colorsys

	def __init__(self, config, col, row, x=0, y=0, width=32, height=32):

		self.config = config
		self.x = x
		self.y = y
		self.height = height
		self.width = width
		self.val = self.config.value
		self.sat = self.config.saturation
		self.rangeOfSpread = self.config.rangeOfSpread
		self.rateOfChange = self.config.rateOfChange
		self.hueBase = self.config.hueBase
		self.col = col
		self.row = row

	def randomize(self):
		self.x = random.random() * self.config.screenWidth
		self.y = random.random() * self.config.screenHeight
		self.width = random.random() * 100 + 5
		self.height = random.random() * 100 + 5

	def make(self):

		rate = random.uniform(self.rateOfChange[0] / 1000, self.rateOfChange[1] / 1000)
		self.hueTarget = random.uniform(
			(self.config.targetHue - self.rangeOfSpread),
			(self.config.targetHue + self.rangeOfSpread),
		)

		# self.hueTarget = 0

		if self.hueTarget > 360:
			self.hueTarget -= 360
		if self.hueTarget < 0:
			self.hueTarget += 360

		self.delta = self.hueTarget - self.hue

		if self.delta > 180:
			self.delta -= 360
		if self.delta < -180:
			self.delta += 360

		# this makes the rate proportional to the delta
		self.hueRateBase = rate * self.delta
		self.hueRate = self.hueRateBase

		# rate *= 20
		# if(self.hueTarget - self.hue < 0) : rate = -rate
		# self.hueRateBase = rate
		# self.hueRate = self.hueRateBase

		# print(self.config.targetHue, self.rangeOfSpread)
		# print(self.row, self.col, self.hue, self.hueTarget , self.hueRate)

	def update(self):

		self.hue += self.hueRate
		self.delta = self.hueTarget - self.hue

		if self.hue > 360:
			self.hue -= 360
		if self.hue < 0:
			self.hue += 360

		# Hue, Saturation, Value
		# self.currentColor = list(colorutils.HSVToRGB(self.hue, self.sat, self.val))

		# Hue, Chroma, Luma
		self.currentColor = list(colorutils.HSLToRGB(self.hue, self.sat, self.val))
		self.displayCurrentColor = tuple((round(i* self.config.brightness)) for i in self.currentColor)
		# if (self.row == 0  and self.col == 0) : print(self.hue, self.displayCurrentColor)
		self.config.draw.rectangle(
			(self.x, self.y, self.width + self.x, self.height + self.y),
			fill=self.displayCurrentColor,
		)

		if abs(self.delta) < 1:
			# self.hue = 0
			self.make()


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def main(run=True):
	global config, workConfig

	config.redrawRate = float(workConfig.get("fills", "redrawRate"))
	config.saturation = float(workConfig.get("fills", "saturation"))
	config.value = float(workConfig.get("fills", "value"))
	config.blurLevel = int(workConfig.get("fills", "blurLevel"))
	config.FillRows = int(workConfig.get("fills", "FillRows"))
	config.FillCols = int(workConfig.get("fills", "FillCols"))
	config.hueBase = int(workConfig.get("fills", "hueBase"))
	config.rangeOfSpread = int(workConfig.get("fills", "rangeOfSpread"))
	config.vval = int(workConfig.get("fills", "vval"))
	config.rateOfChange = workConfig.get("fills", "rateOfChange").split(",")
	config.rateOfChange = [float(i) for i in config.rateOfChange]
	config.vignette = workConfig.getboolean("fills", "vignette")
	config.crossbar = workConfig.getboolean("fills", "crossbar")

	config.transitioning = False
	config.avgHue = 0
	config.targetHue = 230

	# reseting render image size
	config.renderImage = Image.new("RGBA", (config.actualScreenWidth, 32))
	config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	config.draw = ImageDraw.Draw(config.image)
	config.id = config.image.im.id
	config.fill = []

	## Set up the grid
	rows = config.FillRows
	cols = config.FillCols

	colWidth = round(config.screenWidth / cols)
	rowHeight = round(config.screenHeight / rows)
	print(colWidth, rowHeight)
	for col in range(0, cols):
		for row in range(0, rows):
			f = Fill(
				config, col, row, col * colWidth, row * rowHeight, colWidth, rowHeight
			)
			f.make()
			config.fill.append(f)

	config.timerTime = time.time()
	config.timerDelay = 10
	config.timeoutTime = config.timerTime + config.timerDelay

	if run:
		runWork()


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def runWork():
	global config
	print(bcolors.OKGREEN + "** " + bcolors.BOLD)
	print("Running fills.py")
	print(bcolors.ENDC)
	while True:
		iterate()
		time.sleep(config.redrawRate)


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def changeTargetHue():
	change = int(round(random.uniform(-180, 180)))

	config.targetHue = round(config.avgHue + change)

	# the randge has to be 0 - 360
	if config.targetHue > 360:
		config.targetHue = config.targetHue - 360
	if config.targetHue < 0:
		config.targetHue = config.targetHue + 360

	print("new target", config.targetHue)

	# Update all the blocks with their new "target hue"
	numBlocks = len(config.fill)
	for i in range(0, numBlocks):
		config.fill[i].make()


def iterate():
	global config

	# Clear out the image -- not really necessary tho
	config.draw.rectangle(
		(0, 0, config.screenWidth, config.screenHeight), fill=(0, 0, 0, 255)
	)

	# run throught the blocks, update and get average hue
	numBlocks = len(config.fill)
	avgHue = 0
	for i in range(0, numBlocks):
		config.fill[i].update()
		avgHue += config.fill[i].hue
	config.avgHue = avgHue / numBlocks

	# draw the "vignette"
	if config.vignette:
		config.draw.rectangle(
			(0, 0, config.screenWidth - 1, config.screenHeight - 1),
			outline=(config.vval, config.vval, config.vval, 100),
		)
	if config.crossbar:
		config.draw.rectangle(
			(
				config.screenWidth / 2,
				0,
				config.screenWidth / 2 + 2,
				config.screenHeight,
			),
			fill=(config.vval, config.vval, config.vval, 100),
		)

	# Do the blur
	im = config.image.filter(ImageFilter.GaussianBlur(config.blurLevel))

	# Render the image to the screen
	config.render(im, 0, 0, config.screenWidth, config.screenHeight)

	# Decide if the primary target color should shift

	var = 0
	# if (config.avgHue <= config.targetHue + var and config.avgHue >= config.targetHue - var) :
	#     changeTargetHue()

	if time.time() >= config.timeoutTime:
		config.timerTime = time.time()
		config.timerDelay = 10
		config.timeoutTime = config.timerTime + config.timerDelay
		changeTargetHue()


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def callBack():
	global config
	# animator()


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
