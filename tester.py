#!/usr/bin/python
#import modules
from modules import utils, actions, machine, scroll, user, bluescreen ,loader, squares, flashing, blender, carousel
import Image
import ImageDraw
import time
import random
from rgbmatrix import Adafruit_RGBmatrix
import datetime
import ImageFont
import textwrap
import math
import sys, getopt, os
import ConfigParser, io

# ################################################### #
global matrix
global rows, cols, tileSize
global r,g,b,boxHeight,boxWidth
global config


def drawMachine(mDisplacey = -1) :
        global config
        global r,g,b, boxHeight, boxWidth
        matrix = config.matrix
        draw = config.draw

        screenWidth = config.screenWidth
        screenHeight = config.screenHeight
        
        # x1, y1 are inital face points (left eye)
        x1 = 5
        y1 = 12
        # d is size of eye X
        d = 4
        # d2 is mouth / right eye
        d2 = 10
        # m1 is left point start, mw is mouth width
        m1 = 6
        mw = 12
        # Sets a frowm :[ upsidedown :]
        #mDisplacey = -1
        mDisplacex = 0

        # Fill colors
        rf = gf = bf = 0

        # line width
        w = 1

        # First state is  :[ second state is :]
        if (r == 0 ):
                rf = int(255 * config.brightness)
                gf = 0
                r = 0
                g = int(255 * config.brightness)
                b = 0
        else :
                rf = 0
                gf = int(255 * config.brightness)
                r = int(255 * config.brightness)
                g = 0
                b = 0
                w = 2

        # outline
        config.draw.rectangle((0,0,boxWidth-1,boxHeight-1), fill=(rf,gf,bf), outline=(r,g,b))
        
        # eyes
        config.draw.line((x1,y1,x1+d,y1+d), fill=(r,g,b), width = w)
        config.draw.line((x1,y1+d,x1+d,y1), fill=(r,g,b), width = w)

        x1 = x1 + d2

        config.draw.line((x1,y1,x1+d,y1+d), fill=(r,g,b), width = w)
        config.draw.line((x1,y1+d,x1+d,y1), fill=(r,g,b), width = w)

        # mouth
        x1 = x1 - d2
        y1 = y1 + -1

        #left corner
        #config.draw.line((x1+3,y1+d2,x1+2,y1+d2 +1), fill=(r,g,b), width = w)
        config.draw.line((m1 - mDisplacex, y1 + d2 + mDisplacey, m1, y1 + d2), fill=(r,g,b), width = w)
        #center
        config.draw.line((m1, y1 + d2, m1 + mw, y1 + d2), fill=(r,g,b), width = w)
        #rigth corner
        #config.draw.line((x1+d2+1,y1+d2,x1+d2 +2,y1+d2+1), fill=(r,g,b), width = w)
        config.draw.line((m1 + mw, y1 + d2, m1 + mw + mDisplacex, y1 + d2 + mDisplacey), fill=(r,g,b), width = w)

def render(imageToRender):
	global matrix
	global rows, cols, tileSize

	segmentedImage = Image.new("RGBA", (tileSize[1]*cols, 32))
	print("Total segment", segmentedImage)

	for n in range(0,rows) :
		segmentWidth = tileSize[0] * cols
		segmentHeight = 32
		xPos = n * segmentWidth
		yPos = n * segmentHeight
		segment =  imageToRender.crop((0, yPos, segmentWidth, segmentHeight + yPos))
		#print(n, segment, xPos,yPos)
		#segmentedImage.paste(segment, (xPos,0))
		iid = segment.im.id
		matrix.SetImage(iid, xPos, 0)

	#iid = segmentedImage.im.id
	#matrix.SetImage(iid, 0, 0)

def renderManual(imageToRender):
	global matrix
	global rows, cols, tileSize

	pixLen = imageToRender.size

	print(pixLen)

def configure() :
	global config
	baseconfig = ConfigParser.ConfigParser()
	baseconfig.read('/home/pi/RPI/config.cfg')

	config = utils
	config.matrix = Adafruit_RGBmatrix(32, int(baseconfig.get("config", 'matrixTiles')))
	config.screenHeight = int(baseconfig.get("config", 'screenHeight'))
	config.screenWidth =  int(baseconfig.get("config", 'screenWidth'))
	config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	config.draw = ImageDraw.Draw(config.image)

	config.Image = Image
	config.ImageDraw = ImageDraw
	config.ImageFont = ImageFont
	iid = config.image.im.id
	#config.matrix.SetImage(iid, 0, 0)

	config.tileSize = (int(baseconfig.get("config", 'tileSizeHeight')),int(baseconfig.get("config", 'tileSizeWidth')))
	config.rows = int(baseconfig.get("config", 'rows'))
	config.cols = int(baseconfig.get("config", 'cols'))

	config.actualScreenWidth  = int(baseconfig.get("config", 'actualScreenWidth'))
	config.useMassager = bool(baseconfig.getboolean("config", 'useMassager'))
	config.renderImage = Image.new("RGBA", (config.actualScreenWidth, 32))
	config.brightness =  float(baseconfig.get("config", 'brightness'))
	config.path = baseconfig.get("config", 'path')

	config.transWiring = False

def testPatternBasic() :
	global matrix
	global rows, cols, tileSize

	matrix = Adafruit_RGBmatrix(32, 1)
	# cols, rows
	tileSize = (32, 32)
	rows = 1
	cols = 1
	n = clri = 0

	# cols, rows
	testGrid = (2, 2)
	sizeX = int(cols * tileSize[0] / testGrid[0]) - 1
	sizeY = int(rows * tileSize[1] / testGrid[1]) - 1

	imageToRender = Image.new("RGBA", (tileSize[0]*cols, tileSize[1]*rows))
	draw  = ImageDraw.Draw(imageToRender)
	print("imageToRender", imageToRender)

	 #(0,200,0)
	wheel = [   (255,0,0),
	            (255,126,0),
	            (255,255,0),
	            (0,255,0),
	            (0,0,255),
	            (126,0,255),]

	cName1 = wheel[clri]
	cName2 = (utils.colorCompliment(cName1))

	t1 = time.clock()
	t2 = time.clock()

	# cols, rows
	for r in range(0, testGrid[1] ) :	
		for c in range(0, testGrid[0] ) :
			xPos  = c * sizeX + c -0
			yPos  = r * sizeY + 0
			xPos2 = xPos + sizeX
			yPos2 = yPos + sizeY
			b =  n + 1
			b = 1
			# draw.rectangle((xPos,yPos,xPos2,yPos2), fill=(255,0,n * 15), outline=(0,255,0))
			draw.rectangle((xPos,yPos,xPos2,yPos2), 
				fill=(int(cName1[0]/b),int(cName1[1]/b),int(cName1[2]/b)), 
				outline=(int(cName2[0]/b),int(cName2[1]/b),int(cName2[2]/b)))
			n += 1
			print(n, xPos, yPos, xPos2, yPos2)
			currentName = cName1

			if (clri < len(wheel)-1) :
				clri += 1
			else :
				clri = 0 

			cName1 = wheel[clri]	
			cName2 = utils.closestRBYfromRGB(utils.colorCompliment(cName1))

	t2 = time.clock()
	print(t2 - t1)
	#iid = imageToRender.im.id
	#matrix.SetImage(iid, 0, 0)
	#print("imageToRender", imageToRender)

	#time.sleep(5)
	#exit()

	#renderManual(imageToRender)
	render(imageToRender)

	print(time.clock() - t2)
	time.sleep(5)

def testPatternUsingConfig() :
	global config
	r=g=b=0
	rf=gf=bf=0
	if (r == 0 ):
		rf = int(255 * config.brightness)
		gf = 0
		r = 0
		g = int(255 * config.brightness)
		b = 0
	else :
		rf = 0
		gf = int(255 * config.brightness)
		r = int(255 * config.brightness)
		g = 0
		b = 0

	x = 0
	y = 1
	boxHeight = 38
	boxWidth = 65
	config.draw.rectangle((x,y,x+boxWidth,y+boxHeight), fill=(rf,gf,bf))
	config.render(config.image,x,y,boxWidth,boxHeight,False)

	time.sleep(5)

def testMachine() :
	global r,g,b,boxHeight,boxWidth
	r=g=b=125
	boxHeight = 24
	boxWidth = 28

	drawMachine()
	x = 0
	y = 32
	count = 32
	while (count > 0) :
		config.render(config.image,x,y,boxWidth,boxHeight,False)
		time.sleep(1)
		y += -2
		x += 0
		count -= 1
		pass


#testPatternBasic()

configure()

testPatternUsingConfig()
testMachine() 
#testPatternBasic()



