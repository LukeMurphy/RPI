# ################################################### #
import time
import random
import math
import PIL.Image
from PIL import Image, ImageDraw
import sys
from modules import colorutils


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

class DiceFactory :

	def __init__(self, config):
		self.config = config
		self.w  = 20
		self.dibit = 5
		self.fill = (200,0,0)
		self.offset = [0,0]
		self.image = Image.new("RGBA", (self.w, self.w))
		self.draw = ImageDraw.Draw(self.image)
		self.offset = []
		self.fills = [(200,0,0), (0,100,80), (0,0,200),(200,150,0), (200,0,100), (0,150,150)]
		f = math.floor(random.uniform(0,6))
		self.fill = self.fills[f]

		


	def createDice(self):

		if random.random() < .5 :
			f = math.floor(random.uniform(0,6))
			self.fill = self.fills[f]

		self.image = Image.new("RGBA", (self.w, self.w))
		self.draw = ImageDraw.Draw(self.image)

		w = self.w
		dibit = self.dibit
		draw = self.draw
		offX = 0 #self.offset[0]
		offY = 0 #self.offset[1]
		draw.rectangle((offX,offY, offX + w , offY + w ), fill = self.fill)

		num = round(random.uniform(1,6))
		#num = 2

		if num == 1 :
			x = w/2
			y = w/2
			draw.ellipse((offX + x-dibit/2, offY + y-dibit/2, offX + x + dibit/2, offY + y + dibit/2), fill = (200,200,200))

		if num == 2 :
			x = w/5
			y = w/5
			draw.ellipse((offX + 1 * x-dibit/2, offY + 1 * y-dibit/2, offX + 1 * x + dibit/2, offY + 1 * y + dibit/2), fill = (200,200,200))
			draw.ellipse((offX + 4 * x-dibit/2, offY + 4 * y-dibit/2, offX + 4 * x + dibit/2, offY + 4 * y + dibit/2), fill = (200,200,200))

		if num == 3 :
			x = w/5
			y = w/5
			draw.ellipse((offX + 1 * x-dibit/2, offY + 1 * y-dibit/2, offX + 1 * x + dibit/2, offY + 1 * y + dibit/2), fill = (200,200,200))
			draw.ellipse((offX + 4 * x-dibit/2, offY + 4 * y-dibit/2, offX + 4 * x + dibit/2, offY + 4 * y + dibit/2), fill = (200,200,200))
			x = w/2
			y = w/2
			draw.ellipse((offX + x-dibit/2, offY + y-dibit/2, offX + x + dibit/2, offY + y + dibit/2), fill = (200,200,200))

		if num == 4 :
			x = w/5
			y = w/5
			draw.ellipse((offX + 1 * x-dibit/2, offY + 1 * y-dibit/2, offX + 1 * x + dibit/2, offY + 1 * y + dibit/2), fill = (200,200,200))
			draw.ellipse((offX + 4 * x-dibit/2, offY + 1 * y-dibit/2, offX + 4 * x + dibit/2, offY + 1 * y + dibit/2), fill = (200,200,200))
			draw.ellipse((offX + 4 * x-dibit/2, offY + 4 * y-dibit/2, offX + 4 * x + dibit/2, offY + 4 * y + dibit/2), fill = (200,200,200))
			draw.ellipse((offX + 1 * x-dibit/2, offY + 4 * y-dibit/2, offX + 1 * x + dibit/2, offY + 4 * y + dibit/2), fill = (200,200,200))

		if num == 5 :
			x = w/5
			y = w/5
			draw.ellipse((offX + 1 * x-dibit/2, offY + 1 * y-dibit/2, offX + 1 * x + dibit/2, offY + 1 * y + dibit/2), fill = (200,200,200))
			draw.ellipse((offX + 4 * x-dibit/2, offY + 1 * y-dibit/2, offX + 4 * x + dibit/2, offY + 1 * y + dibit/2), fill = (200,200,200))
			draw.ellipse((offX + 4 * x-dibit/2, offY + 4 * y-dibit/2, offX + 4 * x + dibit/2, offY + 4 * y + dibit/2), fill = (200,200,200))
			draw.ellipse((offX + 1 * x-dibit/2, offY + 4 * y-dibit/2, offX + 1 * x + dibit/2, offY + 4 * y + dibit/2), fill = (200,200,200))
			x = w/2
			y = w/2
			draw.ellipse((offX + x-dibit/2, y-dibit/2, offX + x + dibit/2, y + dibit/2), fill = (200,200,200))

		if num == 6 :
			x = w/5
			y = w/5
			draw.ellipse((offX + x-dibit/2, offY + y-dibit/2, offX + x + dibit/2, offY + y + dibit/2), fill = (200,200,200))
			draw.ellipse((offX + 4 * x-dibit/2, offY + y-dibit/2, offX + 4 * x + dibit/2, offY + y + dibit/2), fill = (200,200,200))
			draw.ellipse((offX + 4 * x-dibit/2, offY + 4 * y-dibit/2, offX + 4 * x + dibit/2, offY + 4 * y + dibit/2), fill = (200,200,200))
			draw.ellipse((offX + 1 * x-dibit/2, offY + 4 * y-dibit/2, offX + 1 * x + dibit/2, offY + 4 * y + dibit/2), fill = (200,200,200))
			x = w/5
			y = w/2
			draw.ellipse((offX + x-dibit/2, offY + y-dibit/2, offX + x + dibit/2, offY + y + dibit/2), fill = (200,200,200))
			draw.ellipse((offX + 4 * x-dibit/2, offY + y-dibit/2, offX + 4 * x + dibit/2, offY + y + dibit/2), fill = (200,200,200))

		if random.random() < .5 :
			self.image = self.image.rotate(90)

		return self.image



def drawRects():
	global config

	changeColor(config.colorSwitch)

	# For single square dividing, rows = cols all the time
	# But for double square, start with rows, divide columns
	# then divide rows, then repeat

	#if (rows * lineWidth) < config.screenHeight : rows = int(config.screenHeight/lineWidth)
	rHeight = round(config.screenHeight / config.rows)
	squaresToDraw = round(rHeight / 2)

	# if(rows*lineWidth < config.screenHeight)
	additionalRows = 0
	rowDiff = config.screenHeight - config.rows * rHeight

	if(rowDiff > config.lineWidth + 1):
		additionalRows = rowDiff

	for row in range(0, config.rows + additionalRows):

		yOffset = round(row * rHeight)

		for col in range(0, config.cols):
			rWidth = round(config.screenWidth / config.cols)
			xOffset = round(col * rWidth)
			config.colorSwitchMode = round(random.uniform(1, 4))

			for n in range(0, squaresToDraw, config.lineWidth):
				# --------------------------------------------------------------#
				# Alternate Bands of Color, keep to one scheme per set of squares
				changeColor(config.colorSwitch, config.colorSwitchMode)

				xStart = n + xOffset
				xEnd = xOffset + rWidth - n - 1

				yStart = n + yOffset
				yEnd = yOffset + rHeight - n - 1

				#config.draw.rectangle((xStart, yStart, xEnd, yEnd), outline=(r,g,b))

				for l in range(0, config.lineWidth):
					config.draw.rectangle((xStart + l, yStart + l, xEnd - l, yEnd - l), outline=(config.r, config.g, config.b))

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


def changeColor(rnd=False, choice=3):
	global config

	#rnd = True

	if rnd == False and config.rows < 2:
		val = round(255 * config.brightness)
		if(config.r == val):
			config.r = 0
			config.g = val
			config.b = 0
			# Add variant that we pulse red/blue not just red/greeen
			# red/blue makes for pink afterimage so more about excitement
			# than red/green making yellow after image, which feels like it's
			# more about food ...

			if(random.random() > .5):
				config.b = 0
				config.g = val
		else:
			config.r = val
			config.g = 0
			config.b = 0

	else:
		choice = round(random.uniform(1, 8))

		#choice = 3
		if(choice == 1):
			clr = config.colorutil.getRandomColorWheel(config.brightness)

		if(choice == 2):
			clr = config.colorutil.getRandomRGB(config.brightness)

		if(choice >= 3):
			clr = config.colorutil.randomColor(config.brightness)

		if(config.grayMode):
			clr = config.colorutil.randomGray(config.brightness)

		#clr = config.colorutil.getRandomColorWheel(config.brightness)

		config.r = clr[0]
		config.g = clr[1]
		config.b = clr[2]


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


def main(run=True):
	global config, workConfig

	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
	# make script to reduce from one square to 2 to 4 to 8 to 16...
	# Like a frenetic Albers excercise that is more like a sign
	# advertising itself
	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
	config.x = config.y = 0
	config.r = 255
	config.g = config.b = 0
	config.pulseSpeed = .1
	config.colorSwitch = True
	config.countLimit = 10
	config.rHeight = 0
	config.rWidth = 0
	config.rows = 1
	config.cols = 1
	config.lineWidth = 1

	# rows, cols
	config.divisionOfSquares = [1, 1, 2, 2, 4, 4, 8, 8, 16, 16, 32, 32]

	config.colorutil = colorutils

	config.grayMode = False
	config.count = 0
	config.rWidth = config.screenWidth
	config.rHeight = config.screenHeight

	# reseting render image size
	config.renderImage = Image.new("RGBA", (config.actualScreenWidth, 32))
	config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	config.canvasImage = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	config.draw = ImageDraw.Draw(config.image)
	config.id = config.image.im.id

	config.lineWidth = config.lineWidth = int(workConfig.get("dicefactory", 'lineWidth'))
	config.pulseSpeed = float(workConfig.get("dicefactory", 'pulseSpeed'))
	config.pasteDelay = float(workConfig.get("dicefactory", 'pasteDelay'))
	config.mode = (workConfig.get("dicefactory", 'mode'))
	config.countLimit = int(workConfig.get("dicefactory", 'countLimit'))
	config.w = int(workConfig.get("dicefactory", 'w'))
	config.b = int(workConfig.get("dicefactory", 'b'))
	config.dibit = int(workConfig.get("dicefactory", 'dibit'))
	config.rows = int(workConfig.get("dicefactory", 'rows'))
	config.cols = int(workConfig.get("dicefactory", 'cols'))
	config.reRollProb = float(workConfig.get("dicefactory", 'reRollProb'))
	config.reDrawProb = float(workConfig.get("dicefactory", 'reDrawProb'))
	config.alwaysRedrawAfterReRoll = (workConfig.getboolean("dicefactory", 'alwaysRedrawAfterReRoll'))
	config.allChange = (workConfig.getboolean("dicefactory", 'allChange'))

	config.t1  = time.time()
	config.t2  = time.time()
	config.deltaLim = float(workConfig.get("dicefactory", 'deltaLim'))
	config.rowRunning = 0
	config.diceArray = []

	try:
		config.forceHoldDivision = int(workConfig.get("dicefactory", 'forceHoldDivision'))
		config.divisionPosition = config.forceHoldDivision
	except Exception as e:
		config.forceHoldDivision = -1
		config.divisionPosition = 0
		print(e)


	setUp()

	if(run):
		runWork()

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def setUp():

	w = config.w
	dibit = config.dibit
	b = config.b
	rows = config.rows
	cols = config.cols

	## move the creation of the images to the setup and create an array of dice
	## that are updated  - otherwise getting pretty slow
	for col in range(0, cols):
		for row in range(0, rows):
			d = DiceFactory(config)
			d.offset = [col * (w + b), row * (w + b)]
			d.w = w
			d.dibit = dibit
			d.rowNum = row
			d.colNum = col

			config.diceArray.append(d)
			img  = d.createDice()
			config.image.paste(img, (d.offset[0], d.offset[1]))

def iterate():
	global config
	rows = config.rows
	cols = config.cols

	config.draw.rectangle((0,0,config.screenWidth, config.screenHeight), fill = (0,0,0,1))


	for d in config.diceArray :
		if d.rowNum == config.rowRunning or config.allChange == True:
			if random.random() < config.reRollProb :
				img  = d.createDice()
				if config.alwaysRedrawAfterReRoll == True :
					config.image.paste(d.image, (d.offset[0], d.offset[1]))
			if random.random() < config.reDrawProb :
				config.image.paste(d.image, (d.offset[0], d.offset[1]))

		

	'''
	'''
	## Paste an alpha of the next image, wait a few ms 
	## then past a more opaque one again
	## softens the transitions just enough

	mask1 = config.image.point(lambda i: min(i * 1, 50))
	config.canvasImage.paste(config.image, (0,0), mask1)
	config.render(config.canvasImage, 0, 0, config.image)
	
	time.sleep(config.pasteDelay)
	mask2 = config.image.point(lambda i: min(i * 25, 100))
	config.canvasImage.paste(config.image, (0,0), mask2)
	config.render(config.canvasImage, 0, 0, config.image)
	
	time.sleep(config.pasteDelay)
	mask3 = config.image.point(lambda i: min(i * 25, 255))
	config.canvasImage.paste(config.image, (0,0), mask3)
	config.render(config.canvasImage, 0, 0, config.image)

	#config.canvasImage.paste(config.image, (0,0))
	#config.render(config.canvasImage, 0, 0, config.image)


	config.t2 = time.time()
	if config.t2 - config.t1 > config.deltaLim:
		config.rowRunning += 1
		config.t1 = time.time()
		if config.rowRunning >= config.rows :
			config.rowRunning = 0

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def runWork():
	global config
	while True:
		iterate()
		time.sleep(config.pulseSpeed)

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


def reset():
	global config
	config.divisionPosition = 0
	config.countLimit = config.countLimit
	config.lineWidth = int(random.uniform(1, 9))


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def callBack():
	global config
	# animator()

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
