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
global image, draw
global config
global image2
action = "play"

def loadImage(arg):
	global image2
	image2 = Image.new("RGBA", (40, 32))
	image2 = Image.open(arg , "r")
	image2.load()
	#config.draw  = ImageDraw.Draw(image2)
	#image2 = image2.resize((32,32))
	return True
	
def panImage() :
	global frame, count, xOffset, yOffset, vX, vY
	for n in range (0, image2.size[1] - config.screenHeight):
		xOffset += vX;
		yOffset += vY
		# forces redraw of next frame  -- must fix this hack sometime ....
		image2.rotate(0)
		if(random.random() > .1) : config.matrix.Clear()
		config.matrix.SetImage(image2.im.id, xOffset, yOffset)
		time.sleep(.02)
	#if (xOffset > config.image.size[0] -63 or xOffset < -config.image.size[0]+42) :
		#vX *= -1
	#config.matrix.SetImage(config.image.im.id, xOffset, yOffset)
		
def fillColor() :
	if(random.random() > .99) :
		config.matrix.Fill(0xff0000)
	else :
		config.matrix.Fill(0x0000ff)
		
def rotateImage(angle) :
	global image, matrix
	image2 = config.image.resize((32,32))
	image2 = image2.rotate(angle, Image.BICUBIC, 1);		
	config.matrix.Clear()
	config.matrix.SetImage(config.image2.im.id, -8, -8)
   
		
def testImage():
	global image, matrix
	count = 0
	while (count < 700) :
		#rotateImage(random.uniform(-180, 180))
		rotateImage(count)
		count+=2
		time.sleep(.02)

def animate(randomizeTiming = False, frameLimit = 3) :
	global frame, count, xOffset, yOffset, vX,image2, action
	#config.matrix.Clear()

	fillColor()
	config.matrix.SetImage(image2.im.id, xOffset, yOffset)
	if(action == "play") : config.matrix.SetImage(image2.im.id, 60, yOffset)

	try:
		image2.seek(frame)
	except EOFError:
		image2.seek(0)
		pass
	
	# forces redraw of next frame  -- must fix this hack sometime ....
	image2.rotate(0)
	
	if(randomizeTiming) :
		time.sleep(random.uniform(.02,.08))
		if(random.random() > .98) :
			time.sleep(random.uniform(.05,2))
	else :
		time.sleep(.08)

	# Advance to next frame
	frame = image2.tell() + 1

	if (frame == frameLimit):
		frame = 0

#################################	

def playImage(randomizeTiming = False, frameLimit = 3):
	animate(randomizeTiming, frameLimit)


#################################	
def init():
	global action
	count = 0
	while (count < countLimit):
		try:
			if(action == "play"):
				playImage(False, 30)
			else : 
				panImage()
			#
			count += 1
		except KeyboardInterrupt:
			print "Stopping...."
			break
		
################################

def start():
	global image2,frame, action,xOffset,yOffset
	frame = xOffset = yOffset = 0
	img = "./imgs/shane3.gif"
	img  = "./imgs/00united_states-onblu.gif"
	img  = "./imgs/flame-blub.gif"

	if (action == "play") : 
		img  = "./imgs/flames-1b2.gif"
	else :
		img = "./imgs/206_thumbnail25.gif"

	if(loadImage(img)) :
		print( img + " loaded")
		init()
	else:
		print "could not load"
	
	
###############################	