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
vX = 1
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

global debug
global draw
global config
global image

debug = False

def setUpNew():
	global image
	image = Image.new("RGBA", (128, 400))

def loadImage(arg):
	global image, imgHeight
	image = Image.open(arg , "r")
	image.load()
	imgHeight =  image.getbbox()[3]
	return True
	
def panImage() :
	global frame, count, xOffset, yOffset, vX, vY, image, panRangeLimit, scrollSpeed, useJitter

	jitter = False

	# defaults for vertical image scrolling
	if(panRangeLimit == 0) : 
		rangeLimit = image.size[1] + config.screenHeight
		yOffset = -config.screenHeight
	else : 
		rangeLimit = panRangeLimit

	#gray = 175
	draw = ImageDraw.Draw(image)
	# this doesnt work because it just draws to the existing size of the loaded image ... so gets cut off
	if(random.random() > .9) : draw.rectangle((0,image.size[1] -10,32,image.size[1] + config.screenHeight), fill = (12), outline = (0))

	xPos = 0
	yPos = 0
	for n in range (0, rangeLimit):
		if(useJitter):
			if(random.random() > .99) : 
				jitter = False
				vY = 0
				yPos = 0
			if(random.random() > .99) : jitter = True
			if(jitter) : vY = random.uniform(-.3,.3)
		xPos -= vX;
		yPos -= vY
		# older methods
		#config.matrix.Fill(gray,gray,gray)
		#config.matrix.SetImage(image.im.id, xOffset, yOffset)

		config.render(image, int(xOffset + xPos), int(yOffset + yPos))
		time.sleep(scrollSpeed)

	debugMessage("done pan")

def fillColor() :
	global bgFillColor
	if(random.random() > .99) :
		config.matrix.Fill(0xff0000)
	else :
		config.matrix.Fill(bgFillColor)
		
def rotateImage(angle) :
	global image, matrix
	image = config.image.resize((32,32))
	image = image.rotate(angle, Image.BICUBIC, 1);		
	config.matrix.Clear()
	config.matrix.SetImage(config.image.im.id, -8, -8)
   
def testImage():
	global image, matrix
	count = 0
	while (count < 700) :
		#rotateImage(random.uniform(-180, 180))
		rotateImage(count)
		count+=2
		time.sleep(.02)

def animate(randomizeTiming = False, frameLimit = 3) :
	global frame, count, xOffset, yOffset, vX,image, action, gifPlaySpeed, imgHeight

	fillColor()

	config.render(image, 0, imgHeight - config.screenHeight)
	
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

def start(img="", setvX = 0, setvY = -1):
	global image,frame, action,xOffset,yOffset,vX,vY
	frame = 0

	vX = setvX
	vY = setvY
	
	if (action == "play") : 
		xOffset = yOffset = 0
		if(img=="") : img  = "./imgs/flames-1c.gif"
	else :
		if(img=="") : img = "./imgs/drawings/206_thumbnail25.gif"

	debugMessage("Trying to load " + img)	

	if(loadImage(img)) :
		debugMessage( img + " loaded")
		init()
	else:
		debugMessage ("could not load")
	
	
###############################	