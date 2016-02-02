#!/usr/bin/python

import Image
import ImageDraw
import ImageMath
import ImageEnhance
# Import the essentials to everything
import time, random, math

# Rows and chain length are both required parameters:
r=g=b=0
xOffset = 0
yOffset = 0
vX = 0
vY = -1
count = 0
frame = 1
countLimit = 1

imgHeight = 0
panRangeLimit = 0
useJitter = False
useBlink = False
presentTime =  10
brightnessFactor = .5
rate = 0
gifPlaySpeed = 0.07
scrollSpeed = .04
bgFillColor = 0x000000

action = "play"
brightnessFlux = False
brightnessFluxRate  = 8 # As a factor or PI/brightnessFluxRate
resizeToWidth = False

lastPictureIndex = 0

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
	global image, imgHeight, imageCopy, resizeToWidth
	image = Image.open(arg , "r")

	#print("loading : ", arg)
	image.load()
	imgHeight =  image.getbbox()[3]

	return True

def presentImage() :
	global frame, count, xOffset, yOffset, vX, vY, image, panRangeLimit, scrollSpeed, useJitter, useBlink, imageCopy, presentTime	
	imageCopyTemp = imageCopy
	enhancer = ImageEnhance.Brightness(imageCopyTemp)
	imageCopyTemp = enhancer.enhance(brightnessFactor)
	config.render(imageCopyTemp, int(xOffset), int(yOffset), imageCopy.size[0], imageCopy.size[1], False)
	time.sleep(presentTime)
	
def panImage() :
	global frame, count, xOffset, yOffset, vX, vY, image, panRangeLimit, scrollSpeed, useJitter, useBlink, imageCopy, brightnessFactor
	jitter = False

	# defaults for vertical image scrolling
	if(panRangeLimit == 0) : 
		rangeLimit = imageCopy.size[1] + config.screenHeight
		yOffset = config.screenHeight
	else : 
		rangeLimit = panRangeLimit + imageCopy.size[1]
		if(vY ==0) : xOffset = -imageCopy.size[1]

	if(vY != 0) : 
		yOffset = config.screenHeight #-image.size[1]
		#xOffset = int((config.screenWidth ) * random.random()) - 20
		#xOffset = 0

	draw = ImageDraw.Draw(image)

	# this doesnt work because it just draws to the existing size of the loaded image ... so gets cut off
	#if(random.random() > .9) : draw.rectangle((0,image.size[1] -10,32,image.size[1] + config.screenHeight), fill = (12), outline = (0))

	xPos = 0
	yPos = 0

	stepSize = 1
	if(abs(vY) > 1) : stepSize = abs(vY)
	for n in range (0, rangeLimit, stepSize):
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
			#imageTemp = imageCopy.rotate(2, expand=1)
			#imageCopy.paste(imageTemp, (-5,0))

			xF = int(xOffset + xPos)
			yF = int(yOffset  + yPos)

			imageCopyTemp = imageCopy
			enhancer = ImageEnhance.Brightness(imageCopyTemp)
			imageCopyTemp = enhancer.enhance(brightnessFactor)
			config.render(imageCopyTemp, xF, yF, imageCopy.size[0], imageCopy.size[1], False)	
		
		time.sleep(scrollSpeed)

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
	global frame, count, xOffset, yOffset, vX,image, action, gifPlaySpeed, imgHeight, imageCopy, brightnessFactor, brightnessFluxRate, rate

	# This needs fixing  - currently requires extra frame
	# at end of gif  --

	#fillColor(True)
	#config.screenHeight - imgHeight'
	skipTime = False
	#************************************#
	### DRAW THE IMAGE ACROSS ALL PANELS
	#imageCopy = image.point(lambda p: p * 0.19)
	imageCopy.paste(image)
	if(brightnessFlux) :
		rate+=math.pi/brightnessFluxRate;
		brightnessFactor = (math.sin(rate) + 1) / 2 + .01
		#if(brightnessFactor > 1) : brightnessFactor = 1
		#if(brightnessFactor < 0) : brightnessFactor = .00001
	enhancer = ImageEnhance.Brightness(imageCopy)
	imageCopy = enhancer.enhance(brightnessFactor)
	
	config.render(imageCopy, xOffset, yOffset, config.screenWidth, config.screenHeight)
	config.actions.drawBlanks()
	
	try:
		image.seek(image.tell() + 1)
	except EOFError:
		image.seek(0)
		#print("fail", frame)
		skipTime = True
		pass

	if(skipTime == False) :
		if(randomizeTiming) :
			time.sleep(random.uniform(.02,.08))
			if(random.random() > .98) :
				time.sleep(random.uniform(.05,2))
		else :
			time.sleep(gifPlaySpeed)

	#if (frame == frameLimit):frame = 0
	
def playImage(randomizeTiming = False, frameLimit = 3):

	animate(randomizeTiming, frameLimit)

def init():
	global action, countLimit

	#print(countLimit)
	count = 0
	fillColor(True)
	while (count < countLimit):
		try:
			if(action == "play"):
				playImage(False, 7)
			elif(action == "pan") : 
				panImage()
			elif(action == "present") :
				presentImage()		
			count += 1
		except KeyboardInterrupt:
			print "Stopping...."
			exit()
			break

def debugMessage(arg) :

	if(debug) : print(arg)		

def start(img="", setvX = 0, setvY = 0):
	global image,frame, action, xOffset, yOffset, vX, vY, imageCopy
	frame = 0

	vX = setvX
	vY = setvY
	
	if (action == "play") : 
		#xOffset = yOffset = 0
		if(img=="") : 
			if(config.screenWidth <= 128 and config.screenHeight == 64) :
				img  = config.path + "/imgs/flames-128x64.gif"
			elif(config.screenHeight == 96) :
				img  = config.path + "/imgs/flames-tilt.gif"
			else  :
				img  = config.path + "/imgs/flames-196x64.gif"
	else :
		if(img=="") : img = config.path + "/imgs/drawings/206_thumbnail25.gif"

	debugMessage("Trying to load " + img)	

	if(loadImage(img)) :
		# scale to the WIDTH of the screen
		if(image.size[0] != config.screenWidth and resizeToWidth) :
			ratio = float(config.screenWidth)/ image.size[0]
			image = image.resize((config.screenWidth,int(ratio * image.size[1])))
		imageCopy = Image.new("RGBA", (image.size[0], image.size[1]))

		imageCopy.paste(image, (0, 0))
		debugMessage( img + " loaded")
		init()
	else:
		debugMessage ("could not load")
	
	
###############################	