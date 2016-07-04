# ################################################### #
import time
import random
import math
from PIL import Image, ImageDraw

vx = 1
vy = 2
xPos = 0
yPos = 0
r=g=b=125
redrawSpeed = .001

boxWidth = boxHeight = 32
bufferX = bufferY = 0

def drawElement() :
	global config
	global r,g,b
	global xPos, yPos
	global boxWidth, boxHeight

	config.draw.rectangle((xPos,yPos,boxWidth+xPos,boxHeight+yPos), outline=(255,0,0), fill=(0,255,0) )


def redraw():
	global config
	global xPos, yPos, vx, vy, boxWidth, boxHeight, xMax, yMax, bufferX, bufferY

	xPos += vx
	yPos += vy

	drawElement()

	# Render using main render function - manages the matrix tiling
	# config.render(config.image,xPos,yPos,boxWidth,boxHeight,False)
	#sendToRender(config.image, xPos,yPos,boxWidth,boxHeight,False)
		
	if (xPos > xMax + bufferX):
		vx = vx * -1
		changeColor()
		if(random.random() > .5): vx = int(vx * 2 * random.random())
		xPos = xMax +  bufferX - 2
		changeCall()
	if (xPos < 0 - boxWidth + 1):
		vx = vx * -1
		changeColor()
		if(random.random() > .5): vx = int(vx * 2 * random.random())
		xPos = -boxWidth + 1
		changeCall()
	if (yPos > yMax + bufferY):
		vy = vy * -1
		changeColor()
		if(random.random() > .5): vx = int(vy * 2 * random.random())
		yPos = yMax + bufferY -  2
		changeCall()
	if(yPos < 0 - boxHeight):
		vy = vy * -1
		changeColor()
		if(random.random() > .5): vx = int(vy * 2 * random.random())
		yPos = 0 - boxHeight
		changeCall()

def changeColor() :
	pass
	return True

def changeCall() :
	if(random.random() >  .5) : vX = random.uniform(1,5)
	if(random.random() >  .5) : vY = random.uniform(1,5)
	return True

def callBack() :
	global config
	pass

def runWork():
	global redrawSpeed
	while True:
		iterate()
		time.sleep(redrawSpeed)

def iterate() :
	global config, xPos, yPos, wd, ht, dx, dx, start, end, steps, count, boxWidth, boxHeight

	config.render(config.image, xPos, yPos, boxWidth, boxHeight)

	redraw()

	callBack()
	count = 0
	# Done

def main(run = True) :
	global config
	global redrawSpeed, xPos, yPos, vx, vy, xMax, yMax 
	print("Template Loaded")

	config.renderImage = Image.new("RGBA", (config.actualScreenWidth, config.screenHeight))
	config.image = Image.new("RGBA", (26, 30))

	config.draw  = ImageDraw.Draw(config.image)
	config.id = config.image.im.id

	xPos = int(random.random() * config.screenWidth)
	yPos = int(random.random() * config.screenHeight)

	xMax = config.screenWidth
	yMax = config.screenHeight

	vx = vy = 2




	if(run) : runWork()
		

	