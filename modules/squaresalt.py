
import time
import random
import math
import Image
import sys
from modules import colorutils


vx = 0
vy = 0
x = y = 0
r=255
g=b=0
pulseSpeed = 1
colorSwitch = True
columnLimit = 16

'''
make script to reduce from one square to 2 to 4 to 8 to 16...
'''

rHeight = 0
rWidth = 0
rows  = 2
cols = 2

lineWidth = 2

colorutil = colorutils


def drawRects() :
	global config
	global r,g,b
	global colorSwitch
	global rHeight,rWidth,numSquares
	global rows, cols, lineWidth

	changeColor(colorSwitch)
	# For single square dividing, rows = cols all the time
	#
	for row in range(0, rows):
		rHeight = int(config.screenHeight / (rows))
		yOffset = int(row * rHeight)
		squaresToDraw = int(rHeight/2)
		if(squaresToDraw <1 ) : squaresToDraw = 1

		for col in range(0, cols):
			rWidth = int(config.screenWidth / (cols))
			xOffset = int(col * rWidth)

			# --------------------------------------------------------------#
			# Alternate Bands of Color, keep to one scheme per set of squares
			colorSwitchMode = int(random.uniform(1,4))
			# --------------------------------------------------------------#

			colorSwitchMode = 4

			for n in range(0,squaresToDraw,lineWidth):				
				changeColor(colorSwitch, colorSwitchMode)
				xStart = n + xOffset
				xEnd = rWidth - n - 1 + xOffset
				yStart = n + yOffset
				yEnd = rHeight - n - 1 + yOffset

				if(squaresToDraw > 0) :
					for l in range(0,lineWidth) :
						config.draw.rectangle((xStart+l, yStart+l, xEnd-l, yEnd-l ),  outline=(r,g,b))
				else :
					config.draw.point((xStart, yStart, xEnd, yEnd ),  fill=(r,g,b))

def drawGradientRects() :
	global config, colorutil
	global r,g,b
	global rHeight,rWidth,numSquares
	global rows, cols, lineWidth
	# For single square dividing, rows = cols all the time
	#
	for row in range(0, rows):
		rHeight = int(config.screenHeight / (rows))
		yOffset = int(row * rHeight)
		squaresToDraw = int(rHeight/2)
		if(squaresToDraw <1 ) : squaresToDraw = 1

		for col in range(0, cols):
			rWidth = int(config.screenWidth / (cols))
			xOffset = int(col * rWidth)
			indx = 0
			for n in range(0,squaresToDraw,lineWidth):		
				val = colorutils.sorted_sunset[indx][0]
				clr = colorutils.sunset[val]
				brtns = config.brightness
				r = int(clr[0] * brtns)
				g = int(clr[1] * brtns)
				b = int(clr[2] * brtns)		

				xStart = n + xOffset
				xEnd = rWidth - n - 1 + xOffset
				yStart = n + yOffset
				yEnd = rHeight - n - 1 + yOffset

				if(squaresToDraw > 0) :
					for l in range(0,lineWidth) :
						config.draw.rectangle((xStart+l, yStart+l, xEnd-l, yEnd-l ),  outline=(r,g,b))
				else :
					config.draw.point((xStart, yStart, xEnd, yEnd ),  fill=(r,g,b))

				indx += 1
				if (indx >= len(colorutils.sorted_sunset)) : indx = 0


def redraw():
	global config, colorSwitch, colorutil
	global x,y,vx,vy
	
	# forces color animation
	# changeColor()
	#drawRects()
	drawGradientRects()

	#config.matrix.SetImage(config.id,x,y)
	config.render(config.image,x,y,config.screenWidth,config.screenHeight, False)

	if(random.random() > .9) : colorSwitch = True
		
def changeColor( rnd = False, colorSwitchMode = 4) :
		global r,g,b     
		global config, colorSwitch, colorutil

		if (rnd == False) :
			if(r == int(255 * config.brightness)) :
				r = 0
				g = int(255 * config.brightness)
				b = 0
			else :
				g = 0
				r = int(255 * config.brightness)
				b = 0
		else :
			#colorSwitchMode = int(random.uniform(1,4))
			if(colorSwitchMode == 1) : clr = colorutil.getRandomColorWheel(config.brightness)
			if(colorSwitchMode == 2) : clr = colorutil.getRandomRGB(config.brightness)
			if(colorSwitchMode == 3) : clr = colorutil.randomColor(config.brightness)
			if(colorSwitchMode == 4) : clr = colorutil.getSunsetColors(config.brightness)
			r = clr[0]
			g = clr[1]
			b = clr[2]	

# adapted to show Soliloguy of The Point
def animator(arg, mode = "cols") :
	global rHeight,rWidth, numSquares, colorSwitch, pulseSpeed, msg
	global rows, cols, columnLimit, lineWidth
	
	rows = 1
	cols = 1

	# reseting render image size
	config.renderImage = Image.new("RGBA", (config.actualScreenWidth , 32))
	config.image = config.Image.new("RGBA", (config.screenWidth, config.screenHeight))
	config.draw  = config.ImageDraw.Draw(config.image)
	config.id = config.image.im.id
	#config.matrix.Clear()

	count = 0
	rWidth = config.screenWidth
	rHeight = config.screenHeight
	
	arg = 20
	pulseSpeed = .1
	countLimit = 165
	interval = 12

	i = 0
	# --------------------------------------------------------------#
	# Squares should divide 1,4,16,64
	while (count < countLimit) :
		#=========  CALL redraw =========
		redraw()
		#================================
		count += 1
		i += 1
		lineWidth = int(random.uniform(1,5))
		#lineWidth = 1
		interval = int(64/rows +  2)
		if(i > interval) : 
			#lineWidth = int(random.uniform(1,5))
			i = 0
			#colorSwitch = False
			cols *= 2
			rows *= 2
			if(rows > config.screenHeight) :
				rows = cols = 1
		time.sleep(pulseSpeed)


	config.matrix.Clear()
	config.matrix.Fill(0)

