# ################################################### #
import time
import random
import math
import PIL.Image
from PIL import Image, ImageDraw
import sys
from modules import colorutils

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#make script to reduce from one square to 2 to 4 to 8 to 16...
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
x = y = 0
r=255
g=b=0
pulseSpeed = .1
colorSwitch = False
countLimit = 16
rHeight = 0
rWidth = 0
rows  = 1
cols = 1

lineWidth = 1

divisionOfSquares = [1,1,2,2,4,4,8,8,16,16,32,32,64,64]
divisionPosition = 0
colorutil = colorutils

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def drawRects() :
	global config
	global r,g,b
	global colorSwitch
	global rHeight,rWidth,numSquares
	global rows, cols, lineWidth

	changeColor(colorSwitch)

	# For single square dividing, rows = cols all the time
	# But for double square, start with rows, divide columns
	# then divide rows, then repeat


	for row in range(0, rows):
		rHeight = int(config.screenHeight / rows)
		yOffset = int(row * rHeight)
		squaresToDraw = int(rHeight / 2)

		for col in range(0, cols):
			rWidth = int(config.screenWidth / cols)
			xOffset = int(col* rWidth)
			colorSwitchMode = int(random.uniform(1,4))

			for n in range(0, squaresToDraw, lineWidth):
				# --------------------------------------------------------------#
				# Alternate Bands of Color, keep to one scheme per set of squares
				changeColor(colorSwitch, colorSwitchMode)

				xStart = n + xOffset
				xEnd = xOffset + rWidth - n - 1

				yStart = n + yOffset
				yEnd = yOffset + rHeight - n - 1

				#config.draw.rectangle((xStart, yStart, xEnd, yEnd), outline=(r,g,b))

				for l in range(0,lineWidth) :
					config.draw.rectangle((xStart+l, yStart+l, xEnd - l, yEnd - l ), outline=(r,g,b))
		
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def changeColor( rnd = False, choice = 3) :
	global r,g,b, colorutil       
	if (rnd == False) :
		val  = int(255 * config.brightness)
		if(r == val) :
			r = 0
			g = val
			b = 0
			# Add variant that we pulse red/blue not just red/greeen
			# red/blue makes for pink afterimage so more about excitement
			# than red/green making yellow after image, which feels like it's
			# more about food ...

			if(random.random() > .5) :
				b = val
				g = 0
		else :
			r = val
			g = 0
			b = 0

	else :
		choice = int(random.uniform(1,8))
		#choice = 3
		if(choice == 1) : clr = colorutil.getRandomColorWheel(config.brightness)
		if(choice == 2) : clr = colorutil.getRandomRGB(config.brightness)
		if(choice >= 3) : clr = colorutil.randomColor(config.brightness)
		r = clr[0]
		g = clr[1]
		b = clr[2]	

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def animator() :
	global rHeight,rWidth, numSquares, colorSwitch, pulseSpeed, msg
	global rows, cols, columnLimit, count, mode

	mode = "cols"

	count = 0
	pulseSpeed = .1
	countLimit = 16
	interval = 4
	rWidth = config.screenWidth
	rHeight = config.screenHeight
	
	rows = 1
	cols = 1

	# reseting render image size
	config.renderImage = Image.new("RGBA", (config.actualScreenWidth , 32))
	config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	config.draw  = ImageDraw.Draw(config.image)
	config.id = config.image.im.id

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def main(run = True) :
	global config, workConfig
	setUp()
	if(run) : runWork()

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def setUp() :
	animator()
	retrun True

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def runWork():
	while True:
		iterate()
		time.sleep(.1)

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def iterate() :
	global config, colorSwitch, count, countLimit, divisionPosition, divisionOfSquares
	global rows, cols
	drawRects()
	if(random.random() > .7) : colorSwitch = True
	if(random.random() > .9) : colorSwitch = False
	count += 1

	if (count >= countLimit) :
		divisionPosition += 1

		if(divisionPosition >= len(divisionOfSquares)-1) :
				divisionPosition = 0

		cols = divisionOfSquares[divisionPosition+1]
		rows = divisionOfSquares[divisionPosition]
		count = 0

		countLimit = int(16  *  (2 / rows)) + int(random.uniform(2,10))
		if(random.random() > .7) : colorSwitch = False


	config.render(config.image, 0, 0,128,64)

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def callBack() :
	global config
	#animator()

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
