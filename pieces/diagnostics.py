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
	
	config.delay = .02


	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

	config.canvasImage = Image.new("RGBA", (config.canvasImageWidth  , config.canvasImageHeight))

	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
	# Used to be final image sent to renderImageFull after canvasImage has been chopped up and reordered to fit
	config.canvasImageFinal = Image.new("RGBA", (config.screenWidth , config.screenHeight))

	
	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
	#config.drawBeforeConversion = callBack
	config.actualScreenWidth = config.canvasImage.size[0]

	imageWrapLength = config.screenWidth * 50
	config.warpedImage = Image.new("RGBA", (imageWrapLength, config.screenHeight))

	if(config.rotation == -90) :
		imageWrapLength = config.screenWidth * 50
		config.warpedImage = Image.new("RGBA", (imageWrapLength, config.screenWidth))

		
	
	config.xPos = 0
	config.yPos = 0
	config.xPosR = 0
	config.yPosR = 0
	

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
	draw.rectangle((0,0,50,50), fill=(50,0,100), outline=(200,200,0))
	
	#draw.rectangle((0,0,192,160), fill=None, outline=(0,255,255))
	
	#draw.rectangle((0,0,1,1), fill=(0,255,255), outline=None)
	#draw.point((0,0), fill=(0,255,255))

	#draw.point((192,160), fill=(0,255,255))
	#draw.point((191,159), fill=(0,255,255))

	config.xPos += 1
	config.yPos += 1
	
	config.xPosR += 1
	config.yPosR += 3

	if(config.xPosR > config.screenWidth) : config.xPosR = -10
	if(config.yPosR > config.screenWidth) : config.yPosR = -10
	
	config.render(config.canvasImageFinal, config.xPosR, config.yPosR, 500, 500)




''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def callBack() :
	global config, XOs
	return True

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''



