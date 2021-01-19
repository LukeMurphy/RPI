import gc
import math
import random
import textwrap
import time
from modules.configuration import bcolors
import PIL.Image
import PIL.ImageTk
from modules import colorutils
from PIL import Image, ImageDraw, ImageFont, ImageTk

"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

# scroll speed and steps per cycle
scrollSpeed = 0.0006
stroopSpeed = 0.1
steps = 2
stroopSteps = 2
stroopFontSize = 30
fontSize = 14
vOffset = -1
opticalOpposites = True
higherVariability = False
verticalBg = False
verticalBgColor = (0, 0, 0)
# countLimit = 6
count = 0
blocks = []

# Number of blocks that can chage at once
simulBlocks = 6

# B/W or COLOR
colorMode = True

# To produce cascade effect
nextRow = 0

# For video out
x = y = 0

"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


class Block:

	direction = "down"
	color = (255, 0, 0)
	bgColor = (0, 255, 255)
	speed = 2
	speedMultiplier = 4
	x = 0
	y = 0
	dx = -1
	dy = 0
	startx = 0
	starty = 0
	endx = 0
	endy = 0

	reveal = 0
	revealSpeed = 3
	revealSpeedMax = 6
	revealSpeedMin = 6

	colorWord = "RED"
	colorOfWord = (0, 0, 0)
	directionStr = "Left"

	setForRemoval = False

	## Options are reveal, revealmove, move
	movementMode = "reveal"

	def __init__(self, iid=0):
		self.iid = iid

	def remove(self, arrayList):
		arrayList.remove(self)

	def make(self, colorMode=True, nextRow=-1):

		config = self.config
		choice = int(random.uniform(1, 7))
		brightness = config.brightness
		brightness = random.uniform(
			self.config.minBrightness, self.config.brightness + 0.1
		)
		opticalOpposites = False if (random.random() > 0.5) else True
		self.verticalTileSize = (
			int(config.screenHeight / self.displayRows)
			if self.displayRows != config.rows
			else config.tileSize[1]
		)

		if colorMode != True:
			choice = int(random.uniform(8, 10))

		# choice = 3 if (random.random() > .5) else 5
		# choice = 4 if (random.random() > .5) else 6
		# choice = 9

		if choice == 1:
			colorWord, colorOfWord = "YELLOW", (255, 0, 225)
		if choice == 2:
			colorWord, colorOfWord = "VIOLET", (230, 225, 0)
		if choice == 3:
			colorWord, colorOfWord = "RED", (0, 255, 0)
		if choice == 4:
			colorWord, colorOfWord = "BLUE", (225, 100, 0)
		if choice == 5:
			colorWord, colorOfWord = "GREEN", (255, 0, 0)
		if choice == 6:
			colorWord, colorOfWord = "ORANGE", (0, 0, 200)
		if choice == 7:
			colorWord, colorOfWord = "GRAY", (50, 50, 50)
		if choice == 8:
			colorWord, colorOfWord = "BLACK", (255, 255, 255)
		if choice >= 9:
			colorWord, colorOfWord = "WHITE", (0, 0, 0)

		self.colorWord = colorWord

		clr = colorOfWord

		# Draw Background Color
		# Optical (RBY) or RGB opposites
		if opticalOpposites:
			if colorWord == "RED":
				bgColor = tuple(int(a * brightness) for a in ((255, 0, 0)))
			if colorWord == "GREEN":
				bgColor = tuple(int(a * brightness) for a in ((0, 255, 0)))
			if colorWord == "BLUE":
				bgColor = tuple(int(a * brightness) for a in ((0, 0, 255)))
			if colorWord == "YELLOW":
				bgColor = tuple(int(a * brightness) for a in ((255, 255, 0)))
			if colorWord == "ORANGE":
				bgColor = tuple(int(a * brightness) for a in ((255, 125, 0)))
			if colorWord == "VIOLET":
				bgColor = tuple(int(a * brightness) for a in ((200, 0, 255)))
			if colorWord == "BLACK":
				bgColor = tuple(int(a * brightness) for a in ((0, 0, 0)))
			if colorWord == "WHITE":
				bgColor = tuple(int(a * brightness) for a in ((250, 250, 250)))
			if colorWord == "GRAY":
				bgColor = tuple(int(a * brightness) for a in ((200, 200, 200)))
		else:
			bgColor = colorutils.colorCompliment(clr, brightness)

		clr = tuple(int(a * brightness) for a in (clr))

		# Setting 2 fonts - one for the main text and the other for its "border"... not really necessary
		font = ImageFont.truetype(
			config.path + "/assets/fonts/freefont/FreeSansBold.ttf", self.fontSize
		)
		font2 = ImageFont.truetype(
			config.path + "/assets/fonts/freefont/FreeSansBold.ttf", self.fontSize
		)
		pixLen = config.draw.textsize(colorWord, font=font)

		dims = [pixLen[0], pixLen[1]]
		if dims[1] < self.verticalTileSize:
			dims[1] = self.verticalTileSize + 2

		vPadding = int(0.75 * config.tileSize[1])
		self.presentationImage = PIL.Image.new("RGBA", (dims[0] + vPadding, dims[1]))
		self.image = PIL.Image.new("RGBA", (dims[0] + vPadding, 1))
		draw = ImageDraw.Draw(self.presentationImage)
		iid = self.image.im.id
		draw.rectangle((0, 0, dims[0] + config.tileSize[0], dims[1]), fill=bgColor)

		# Draw the text with "borders"
		indent = int(0.05 * config.tileSize[0])

		for i in range(1, self.shadowSize):
			draw.text((indent + -i, -i), colorWord, (0, 0, 0), font=font2)
			draw.text((indent + i, i), colorWord, (0, 0, 0), font=font2)
		draw.text((indent + 0, 0), colorWord, clr, font=font)

		if nextRow == -1:
			vOffset = int(random.uniform(0, self.displayRows)) * self.verticalTileSize
		else:
			vOffset = nextRow * self.verticalTileSize
			
		if config.higherVariability:
			vOffset += round(
				random.uniform(-config.tileSize[0] * 2, config.tileSize[0] * 2)
			)
			vOffset = round(random.uniform(0,config.screenHeight))		if config.higherVariability:
			vOffset += round(
				random.uniform(-config.tileSize[0] * 2, config.tileSize[0] * 2)
			)
			vOffset = round(random.uniform(0,config.screenHeight))

		self.wd = dims[0]
		self.ht = dims[1]

		self.y = vOffset
		# self.y = int(random.uniform(0,config.screenHeight))
		self.x = int(random.uniform(-self.wd / 2, config.screenWidth - self.wd / 2))
		# self.x = config.screenWidth/2

		self.startx = self.x
		self.starty = self.y

		self.dx = int(random.uniform(-self.speed, self.speed)) * self.speedMultiplier
		self.dy = int(random.uniform(-self.speed, self.speed)) * self.speedMultiplier

		if self.dx == 0:
			self.dx = -1
		if self.dy == 0:
			self.dy = -1

		self.endx = -self.wd if self.dx < 0 else config.screenWidth
		self.endy = -self.ht if self.dy < 0 else config.screenHeight

		self.revealSpeed = int(random.uniform(self.revealSpeedMin, self.revealSpeedMax))

	def callBack(self):
		self.setForRemoval = True
		pass

	def move(self):
		if self.setForRemoval != True:
			self.image.paste(self.presentationImage, (0, 0))

			self.x += self.dx
			self.y += self.dy

			if self.dy > 0 and self.y >= self.endy:
				self.callBack()
			if self.dy < 0 and self.y < self.endy:
				self.callBack()
			if self.dx > 0 and self.x >= self.endx:
				self.callBack()
			if self.dx < 0 and self.x < self.endx:
				self.callBack()

	def appear(self):
		dims = self.presentationImage.size
		if self.setForRemoval != True:
			self.reveal += self.revealSpeed
			self.image = PIL.Image.new("RGBA", (dims[0], self.reveal))

			# dr = ImageDraw.Draw(self.image)
			# dr.rectangle((0,0,100,5), fill=(0,255,0))

			segment = self.presentationImage.crop((0, 0, dims[0], self.reveal))
			self.image.paste(segment, (0, 0), segment)

			if self.reveal > dims[1]:
				self.callBack()
				# print(self.colorWord, self.reveal, self.revealSpeed, self.image.size, dims)

	def update(self):
		if self.movementMode == "reveal" or self.movementMode == "revealmove":
			self.appear()
		if self.movementMode == "move" or self.movementMode == "revealmove":
			self.move()


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

# Create each display block and add to the global array of blocks
def makeBlock():
	global config, workConfig, blocks, colorMode, nextRow

	if random.random() < config.moveProbability:
		config.movementMode = "revealmove"
	if random.random() > 0.95:
		config.movementMode = "reveal"

	config.opticalOpposites = True

	block = Block()
	block.config = config
	block.fontSize = config.stroopFontSize
	block.shadowSize = config.shadowSize
	block.displayRows = config.displayRows
	block.displayCols = config.displayCols
	block.movementMode = config.movementMode
	block.speedMultiplier = config.speedMultiplier
	block.revealSpeedMin = config.revealSpeedMin
	block.revealSpeedMax = config.revealSpeedMax
	block.make(colorMode, nextRow)
	block.blocksRef = blocks

	blocks.append(block)

	nextRow = nextRow + 1 if (nextRow <= config.displayRows) else 0

	# Not really sure the garbage collection works ...
	gc.collect()

	if colorMode == False:
		if random.random() < config.colorProbabilityReturn:  # .92
			colorMode = True
			# print("ColorMode changed back")
	else:
		if random.random() < config.colorProbability:  # .985
			colorMode = False
			# print("ColorMode change  to b/w")


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def runStroop(run=True):
	global config, opticalOpposites
	while run:
		numRuns = int(random.uniform(2, 6))
		numRuns = 1
		for i in range(0, numRuns):
			opticalOpposites = False if (opticalOpposites == True) else True
			stroopSequence()


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def getDirection():
	d = int(random.uniform(1, 4))
	direction = "Left"
	if d == 1:
		direction = "Left"
	if d == 2:
		direction = "Right"
	if d == 3:
		direction = "Bottom"
	return direction


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def main(run=True):
	global config, workConfig, blocks, simulBlocks

	print("Stroop2 What Color Loaded")
	simulBlocks = int(workConfig.get("stroop", "simulBlocks"))
	config.fontSize = int(workConfig.get("stroop", "fontSize"))
	config.vOffset = int(workConfig.get("stroop", "vOffset"))
	config.stroopSpeed = float(workConfig.get("stroop", "stroopSpeed"))
	config.stroopSteps = float(workConfig.get("stroop", "stroopSteps"))
	config.stroopFontSize = int(workConfig.get("stroop", "stroopFontSize"))
	config.shadowSize = int(workConfig.get("stroop", "shadowSize"))
	config.higherVariability = workConfig.getboolean("stroop", "higherVariability")
	config.verticalBg = workConfig.getboolean("stroop", "verticalBg")
	config.displayRows = int(workConfig.get("stroop", "displayRows"))
	config.displayCols = int(workConfig.get("stroop", "displayCols"))
	config.movementMode = workConfig.get("stroop", "movementMode")
	config.speedMultiplier = int(workConfig.get("stroop", "speedMultiplier"))
	config.revealSpeedMax = int(workConfig.get("stroop", "revealSpeedMax"))
	config.revealSpeedMin = int(workConfig.get("stroop", "revealSpeedMin"))
	config.moveProbability = float(workConfig.get("stroop", "moveProbability"))
	config.colorProbability = float(workConfig.get("stroop", "colorProbability"))
	config.colorProbabilityReturn = float(
		workConfig.get("stroop", "colorProbabilityReturn")
	)

	config.brightness = float(workConfig.get("displayconfig", "brightness"))
	config.minBrightness = float(workConfig.get("displayconfig", "minBrightness"))

	# for attr, value in config.__dict__.iteritems():print (attr, value)
	blocks = []
	for i in range(0, simulBlocks):
		makeBlock()

	if run:
		runWork()


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

def runWork():
	global config
	print(bcolors.OKGREEN + "** " + bcolors.BOLD)
	print("RUNNING Stroop2.py")
	print(bcolors.ENDC)
	while config.isRunning == True:
		iterate()
		time.sleep(config.stroopSpeed)
		if config.standAlone == False :
			config.callBack()

"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def iterate(n=0):
	global config, blocks, x, y
	for n in range(0, len(blocks)):
		block = blocks[n]
		config.render(
			block.image,
			block.x,
			block.y,
			block.image.size[0],
			block.image.size[1],
			False,
			False,
			False,
		)

		if config.rendering == "out":
			# config.image = block.image.copy()
			try:
				config.image.paste(block.image, (block.x, block.y), block.image)
			except:
				config.image.paste(block.image, (block.x, block.y))

		# config.image = PIL.Image.new("RGBA", (block.image.size[0], block.image.size[1]))
		# config.image.paste(block.image, (0,0), block.image)
		# x = block.x
		# y = block.y

		block.update()
		if block.setForRemoval == True:
			block.update()
			makeBlock()

	# cleanup the list
	blocks[:] = [block for block in blocks if block.setForRemoval != True]
	if config.rendering == "hub":
		config.updateCanvas()
	# if(config.rendering == "out") : config.image = config.renderImageFull.copy()

	if len(blocks) == 0:
		exit()


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def callBack():
	global config
	pass


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
