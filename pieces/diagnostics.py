import time
import random
import textwrap
import math
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageEnhance, ImageChops
from modules import colorutils, badpixels, coloroverlay

def main(run = True) :
	global config, directionOrder
	print("---------------------")
	print("Diag Loaded")
	colorutils.brightness = config.brightness



	config.canvasImageWidth = config.screenWidth
	config.canvasImageHeight = config.screenHeight
	config.canvasImageWidth -= 4
	config.canvasImageHeight -= 4
	
	config.delay = .01
	config.objWidth = 20


	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

	config.canvasImage = Image.new("RGBA", (config.canvasImageWidth  , config.canvasImageHeight))

	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
	# Used to be final image sent to renderImageFull after canvasImage has been chopped up and 
	# reordered to fit
	config.canvasImageFinal = Image.new("RGBA", (100 , 100))

	config.fillColor = colorutils.getRandomRGB()
	config.outlineColor = colorutils.getRandomRGB()
	
	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
	#config.drawBeforeConversion = callBack
	
	'''
	config.actualScreenWidth = config.canvasImage.size[0]

	imageWrapLength = config.screenWidth * 50
	config.warpedImage = Image.new("RGBA", (imageWrapLength, config.screenHeight))

	if(config.rotation == -90) :
		imageWrapLength = config.screenWidth * 50
		config.warpedImage = Image.new("RGBA", (imageWrapLength, config.screenWidth))
		
	'''
	
	config.xPos = 0
	config.yPos = 0
	config.xPosR = 0
	config.yPosR = 0
	
	config.dx = 1
	config.dy = 2
	

	setUp()

	if(run) : runWork()


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def setUp():
	global config
	pass



''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def runWork():
	global blocks, config, XOs
	#gc.enable()
	while True:
		iterate()
		time.sleep(config.delay)  

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def iterate() :
	global config

	'''
	# Blank out canvases
	draw  = ImageDraw.Draw(config.renderImageFull)
	draw.rectangle((0,0,config.screenWidth, config.screenHeight), fill = (0,0,0))

	draw  = ImageDraw.Draw(config.canvasImage)
	draw.rectangle((0,0,config.canvasImageWidth , config.screenHeight), fill = (config.bgColor))

	displayWidth = config.screenWidth * config.displayRows
	'''

	draw  = ImageDraw.Draw(config.canvasImageFinal)
	#draw.rectangle((config.xPos,config.yPos,191 + config.xPos,50 + config.yPos), fill=(200,20,0), outline=(0,200,0))

	xPos = int(config.xPosR)
	yPos = int(config.yPosR)

	config.draw.rectangle((xPos, yPos,xPos+ config.objWidth , yPos +config.objWidth ), fill=config.fillColor, outline=config.outlineColor)
	
	#draw.rectangle((0,0,192,160), fill=None, outline=(0,255,255))
	
	#draw.rectangle((0,0,1,1), fill=(0,255,255), outline=None)
	#draw.point((0,0), fill=(0,255,255))

	#draw.point((192,160), fill=(0,255,255))
	#draw.point((191,159), fill=(0,255,255))

	config.xPos += config.dx
	config.yPos += config.dy
	
	config.xPosR += config.dx
	config.yPosR += config.dy

	if(config.xPosR + config.objWidth > config.screenWidth) : 
		config.xPosR = config.screenWidth - config.objWidth 
		config.xPos = config.screenWidth - config.objWidth 
		changeColor()
		config.dx *= -1
	if(config.yPosR + config.objWidth> config.screenHeight) : 
		config.yPosR = config.screenHeight-config.objWidth 
		config.yPos = config.screenHeight-config.objWidth 
		changeColor()
		config.dy *= -1
	if(config.xPosR < 0) : 
		config.xPosR = 0
		config.xPos = 0
		changeColor()
		config.dx*= -1
	if(config.yPosR < 0) : 
		config.yPosR = 0
		config.yPos = 0
		changeColor()
		config.dy *= -1

	if(config.dx == 0 and config.dy == 0 ):
		if(random.random() > .5): config.dx = (2 * random.random())
		if(random.random() > .5): config.dy = (2 * random.random())
	


	config.render(config.image, 0,0)
		
	#print (config.xPosR)
	#config.render(config.canvasImageFinal, 0,0, 500, 500)

def changeColor():
	config.fillColor = colorutils.randomColor(random.random())
	config.outlineColor = colorutils.getRandomRGB()
	if(random.random() > .5): config.dx = (4 * random.random() + 2)
	if(random.random() > .5): config.dy = (4 * random.random() + 2)
	if(random.random() > .5): config.objWidth = int(random.uniform(17,23))


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def callBack() :
	global config, XOs
	return True

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''



