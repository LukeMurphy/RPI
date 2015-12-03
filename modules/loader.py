#!/usr/bin/python

import Image
import ImageDraw
import time
import random
#from rgbmatrix import Adafruit_RGBmatrix

# Rows and chain length are both required parameters:
#matrix = Adafruit_RGBmatrix(32, 1)
r=g=b=0
xOffset = yOffset = 0
vX = 0
vY = -1
count = 0
frame = 0
countLimit = 1
action = "play"
gifPlaySpeed = 0.07
scrollSpeed = .04
bgFillColor = 0x000000
imgHeight = 0
panRangeLimit = 0
useJitter = False
useBlink = False

global debug
global draw
global config
global image, imageCopy

debug = False

def setUpNew():
	global image, imageCopy
	image = Image.new("RGBA", (128, 400))
	imageCopy = Image.new("RGBA", (128, 400))

def loadImage(arg):
	global image, imgHeight, imageCopy
	image = Image.open(arg , "r")
	image.load()
	imgHeight =  image.getbbox()[3]
	imageCopy = Image.new("RGBA", (image.size[0], image.size[1]))
	imageCopy.paste(image)
	return True
	
def panImage() :
	global frame, count, xOffset, yOffset, vX, vY, image, panRangeLimit, scrollSpeed, useJitter, useBlink, imageCopy
	jitter = False

	# defaults for vertical image scrolling
	if(panRangeLimit == 0) : 
		rangeLimit = image.size[1] + config.screenHeight
		yOffset = config.screenHeight

	else : 
		rangeLimit = panRangeLimit + image.size[1]
		xOffset = -image.size[1]

	draw = ImageDraw.Draw(image)

	# this doesnt work because it just draws to the existing size of the loaded image ... so gets cut off
	#if(random.random() > .9) : draw.rectangle((0,image.size[1] -10,32,image.size[1] + config.screenHeight), fill = (12), outline = (0))

	xPos = 0
	yPos = 0
	

	for n in range (0, rangeLimit):
		if(useJitter):
			if(random.random() > .7) : 
				jitter = False
				vY = 0
				yPos = 0
			if(random.random() > .17) : jitter = True
			if(jitter) : vY = random.uniform(-.3,.3)
		xPos += vX;
		yPos += vY

		if(useBlink == True and random.random() > .9985) :
			blink = False
			blinkNum = int(random.uniform(7,23))
			for blk in range (0, blinkNum) :
				draw.rectangle((0,0, image.size[0] ,image.size[1]), fill = (0))
				if(blink) :
					config.render(imageCopy, int(xOffset + xPos), int(yOffset  + yPos), image.size[0], image.size[1], False)
					blink = False
				else :
					config.render(image, int(xOffset + xPos), int(yOffset  + yPos), image.size[0], image.size[1], False)
					blink = True
				time.sleep(.15)	
			xPos += image.size[1]
		else :
			config.render(imageCopy, int(xOffset + xPos), int(yOffset  + yPos), image.size[0], image.size[1], False)	
		time.sleep(scrollSpeed)
		#time.sleep(5)
		#exit()

	debugMessage("done pan")

def fillColor(force=False) :
	global bgFillColor
	if(random.random() > .8 or force) :
		config.matrix.Fill(bgFillColor)
	else :
		config.matrix.Fill(bgFillColor)
		
def rotateImage(angle) :
	global image, matrix
	image = config.image.resize((32,32))
	image = image.rotate(angle, Image.BICUBIC, 1);		
	config.matrix.Clear()
	config.matrix.SetImage(config.image.im.id, -8, -8)

def animate(randomizeTiming = False, frameLimit = 3) :
	global frame, count, xOffset, yOffset, vX,image, action, gifPlaySpeed, imgHeight

	#fillColor(True)
	#config.screenHeight - imgHeight'

	#************************************#
	### DRAW THE IMAGE ACROSS ALL PANELS
	config.render(image, 0, 0, config.screenWidth, config.screenHeight )
	config.actions.drawBlanks()
	
	#print(imgHeight, config.screenHeight)
	
	try:
		image.seek(frame)
	except EOFError:
		image.seek(0)
		pass
	
	# forces redraw of next frame  -- must fix this hack sometime ....
	image.rotate(0)
	
	if(randomizeTiming) :
		time.sleep(random.uniform(.02,.08))
		if(random.random() > .98) :
			time.sleep(random.uniform(.05,2))
	else :
		time.sleep(gifPlaySpeed)

	# Advance to next frame
	frame = image.tell() + 1

	if (frame == frameLimit):
		frame = 0
	
def playImage(randomizeTiming = False, frameLimit = 3):
	animate(randomizeTiming, frameLimit)

def init():
	global action
	count = 0
	fillColor(True)
	while (count < countLimit):
		try:
			if(action == "play"):
				playImage(False, 30)
			elif(action == "pan") : 
				panImage()
			
			count += 1
		except KeyboardInterrupt:
			print "Stopping...."
			exit()
			break

def debugMessage(arg) :
	
	if(debug) : print(arg)		

def start(img="", setvX = 0, setvY = 0):
	global image,frame, action,xOffset,yOffset,vX,vY
	frame = 0

	vX = setvX
	vY = setvY
	
	if (action == "play") : 
		xOffset = yOffset = 0
		if(img=="") : 
			if(config.screenWidth <= 128) :
				img  = config.path + "/imgs/flames-128x64.gif"
			elif(config.screenHeight == 96) :
				img  = config.path + "/imgs/flames-tilt.gif"
			elif(config.screenWidth >= 196) :
				img  = config.path + "/imgs/flames-196x64.gif"
	else :
		if(img=="") : img = config.path + "/imgs/drawings/206_thumbnail25.gif"

	debugMessage("Trying to load " + img)	

	if(loadImage(img)) :
		debugMessage( img + " loaded")
		init()
	else:
		debugMessage ("could not load")
	
	
###############################	