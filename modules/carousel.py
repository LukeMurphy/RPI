#carousel
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFilter
from PIL import ImageFont
from PIL import ImageEnhance
from PIL import ImageChops
import time
import random
import datetime
import textwrap
import math
import sys, getopt

print( "carousel loaded")

global imageWrapLength, imageToRender, warpedImage, draw, font, angle, segmentWidth, fontSize, useColorFLicker


dFactor  =  1.2
numSegments = 38
stepSize = 4
clr = (150,150,150)
fontSize = 60
vOffset = 0
useColorFLicker = False


def go(arg = "* * * LOVE & PEACE OR *** ") :
	global offset, fontSize, vOffset
	global imageWrapLength, imageToRender, warpedImage, draw, font, angle, segmentWidth, stepSize, clr,useColorFLicker

	# Generally this is set up for paneled screens 196x64
	offset = 10
	argToUse = "          " + arg
	imageWrapLength = config.screenWidth * 50
	imageToRender = Image.new("RGBA", (imageWrapLength, config.screenHeight))
	warpedImage = Image.new("RGBA", (imageWrapLength, config.screenHeight))
	draw  = ImageDraw.Draw(imageToRender)
	font = ImageFont.truetype('/home/pi/RPI/fonts/freefont/FreeSerifBold.ttf',fontSize)

	if(useColorFLicker!=True) : clr = config.getRandomRGB()


	draw.text((0,vOffset),argToUse,clr,font=font)
	pixLen = draw.textsize(argToUse, font = font)

	# n * 2 * r * sin(theta) = curcumfrnace of polygon 
	# where theta = 2 * PI/n  where n = number of faces
	# segment width = d * sin(theta)
	# Cut the text-image into segments and place them as if in a circle
	# then take their projected width onto the screen and force-fit each segment to that
	# so-called projected width
	# change brightness to add to carousel effect - illusion, I know, I said no
	# illusions, just this one - it's 3D!
	
	angle =  math.pi  / numSegments
	segmentWidth = int((config.screenWidth) * math.sin(angle))/2 
	stepRange = int(pixLen[0] / stepSize)

	for n in range(0, stepRange):
		try:
			render()
			offset+=stepSize
			time.sleep(.001)
		except KeyboardInterrupt, e:
			exit()
	go(arg)
	


def render():
	global offset
	global imageWrapLength, imageToRender, warpedImage, draw, numSegments, angle, segmentWidth, useColorFLicker

	placementx = 3

	for n in range(0,numSegments) :
	        pCropx = n * segmentWidth + offset
	        pWidth  = math.fabs(dFactor * segmentWidth * math.sin(angle * n))
	        projectedWidth = int(pWidth)
	        segmentImage  = Image.new("RGBA", (projectedWidth, config.screenHeight))
	        croppedSegment = imageToRender.crop((pCropx,0, pCropx+ segmentWidth, config.screenHeight))
	        segmentImage = croppedSegment.resize((projectedWidth,config.screenHeight))
	        br = pWidth  / segmentWidth

	        if(useColorFLicker) :
		        segmentColorizer = Image.new("RGBA", (projectedWidth, config.screenHeight))
		        draw = ImageDraw.Draw(segmentColorizer)
		        draw.rectangle((0,0,projectedWidth,config.screenHeight), fill = config.randomColor())
		        segmentImage = ImageChops.multiply(segmentImage, segmentColorizer)

	        enhancer = ImageEnhance.Brightness(segmentImage)
	        segmentImage = enhancer.enhance(br)
	        #segmentImage = segmentImage.filter(ImageFilter.BLUR)
	        #warpedImage.paste(segmentColorizer , (placementx,0))
	        warpedImage.paste(segmentImage , (placementx,0))
	        placementx += projectedWidth

	config.render(warpedImage,0,0, config.screenWidth, config.screenHeight)











