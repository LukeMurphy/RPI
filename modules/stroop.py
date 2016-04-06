import time
import random
import PIL.Image, PIL.ImageTk
from PIL import ImageDraw, ImageFont
import textwrap
import math
from modules import colorutils

########################
#scroll speed and steps per cycle
scrollSpeed = 0.0006
stroopSpeed = 0.0001
steps = 2
stroopSteps = 2
stroopFontSize = 30

fontSize = 14
vOffset  = -1
opticalOpposites = True
countLimit = 6
count = 0

# fcu present will start with the opposite
paintColor = "GREEN"

r = g = b = 0
x = y = wd = ht = 0
dx = dy = 0
start = end = count = 0

colorWord = "RED"
colorOfWord = (0,0,0)
directionStr = "Left"


def iterate(n = 0) :
	global config, x, y, wd, ht, dx, dx, start, end, steps, count
	sendToRender(config.image,x, y, wd, ht)
	x += dx
	y += dy

	count+= steps

	if(count > abs(end)) :
		config.opticalOpposites = False if config.opticalOpposites == False else True
		stroopSequence()
		stroop()
		count = 0
		# Done

def sendToRender(img, xP, yP, wD, hT, c = False) :
	global config, x, y, wd, ht
	x, y, wd, ht = xP, yP, wD, hT
	config.render(img, xP, yP, wD, hT)
	
def main(run = True) :
	global config, workConfig
	global fontSize,vOffset,scrollSpeed,stroopSpeed,stroopSteps,stroopFontSize,useColorFlicker
	global config, x, y, wd, ht, dx, dx, start, end, steps, count
	print("Stroop Loaded")
	#[stroop]

	fontSize = int(workConfig.get("stroop", 'fontSize'))
	vOffset = int(workConfig.get("stroop", 'vOffset'))
	scrollSpeed = float(workConfig.get("stroop", 'scrollSpeed'))
	stroopSpeed = float(workConfig.get("stroop", 'stroopSpeed'))
	stroopSteps = float(workConfig.get("stroop", 'stroopSteps'))
	stroopFontSize = int(workConfig.get("stroop", 'stroopFontSize'))
	config.opticalOpposites = True

	stroopSequence() 
	stroop()

	if(run) :
		while True:
			iterate()
			time.sleep(stroopSpeed)

# This sets up the color and direction
def stroopSequence() :
	global  colorWord, colorOfWord, directionStr
	directionStr = getDirection()
	choice = int(random.uniform(0,7))
	colorWord, colorOfWord, directionStr = "ORANGE",(0,0,200),directionStr
	if(choice <= 1) :colorWord, colorOfWord, directionStr = "YELLOW",(255,0,225),directionStr
	if(choice == 2) :colorWord, colorOfWord, directionStr = "VIOLET",(230,225,0),directionStr
	if(choice == 3) :colorWord, colorOfWord, directionStr = "RED",(0,255,0),directionStr
	if(choice == 4) :colorWord, colorOfWord, directionStr = "BLUE",(225,100,0),directionStr
	if(choice == 5) :colorWord, colorOfWord, directionStr = "GREEN",(255,0,0),directionStr
	if(choice == 6) :colorWord, colorOfWord, directionStr = "ORANGE",(0,0,200),directionStr

def getDirection() :
	d = int(random.uniform(1,4))
	direction = "Left"
	if (d == 1) : direction = "Left"
	if (d == 2) : direction = "Right"
	if (d == 3) : direction = "Bottom"
	return direction

def runStroop(run=True) :
	global config
	while run:
		numRuns = int(random.uniform(2,6))
		numRuns =  1
		for i in range(0,numRuns) : 
			if(config.opticalOpposites) : 
				config.opticalOpposites = False
			else : 
				config.opticalOpposites = True
			stroopSequence()

def stroop() :

	global  colorWord, colorOfWord, directionStr
	global r,g,b,config, opticalOpposites, stroopSpeed, stroopSteps, stroopFontSize
	global x, y, wd, ht, dx, dy, start, end, steps

	x = y = 0

	direction = directionStr
	clr = colorOfWord

	brightness = config.brightness
	brightness = random.random()

	clr = tuple(int(a*brightness) for a in (clr))

	# Setting 2 fonts - one for the main text and the other for its "border"... not really necessary
	font = ImageFont.truetype( config.path + '/assets/fonts/freefont/FreeSansBold.ttf',stroopFontSize)
	font2 = ImageFont.truetype(config.path + '/assets/fonts/freefont/FreeSansBold.ttf',stroopFontSize)
	pixLen = config.draw.textsize(colorWord, font = font)

	dims = [pixLen[0],pixLen[1]]
	if(dims[1] < 32) : dims[1] = 34

	# Draw Background Color
	# Optical (RBY) or RGB opposites

	if(opticalOpposites) :
		if(colorWord == "RED") : bgColor = tuple(int(a*brightness) for a in ((255,0,0)))
		if(colorWord == "GREEN") : bgColor = tuple(int(a*brightness) for a in ((0,255,0)))
		if(colorWord == "BLUE") : bgColor = tuple(int(a*brightness) for a in ((0,0,255)))
		if(colorWord == "YELLOW") : bgColor = tuple(int(a*brightness) for a in ((255,255,0)))
		if(colorWord == "ORANGE") : bgColor = tuple(int(a*brightness) for a in ((255,125,0)))
		if(colorWord == "VIOLET") : bgColor = tuple(int(a*brightness) for a in ((200,0,255)))
	else:
		 bgColor = colorutils.colorCompliment(clr, brightness)

	
	counter =  0

	if(direction == "Top" or direction == "Bottom") :
		#config.image = config.Image.new("RGBA", (dims[1], dims[0]*2))
		vPadding = 42
		config.image = PIL.Image.new("RGBA", (dims[1],dims[0]+vPadding))
		config.draw  = ImageDraw.Draw(config.image)
		config.id = config.image.im.id
		bgColorV = (0,0,0)
		config.draw.rectangle((0,0,config.image.size[1], dims[0] + vPadding), fill=bgColorV)

		chars = list(colorWord)
		end = config.image.size[1]
		
		# Generate vertical text
		for letter in chars :
				# rough estimate to create vertical text
				xD = 2
				# "kerning ... hahhaha ;) "
				if (letter == "I") : xD = 7
				config.draw.text((xD, counter * (stroopFontSize - 5)),letter,clr,font=font)
				counter += 1

		offset = int(random.uniform(1,config.screenWidth-20))
		steps = int(stroopSteps)
		x = offset
		dx = 0

		wd = dims[1]
		ht = dims[0]*2

		if(direction == "Bottom") :
			start = config.screenHeight
			end =  int(random.uniform( -ht/2 ,  -ht))
			dy = -steps
			y = start

			#print("==>", x, y, dx, dy, start, end, steps)



	if(direction == "Left" or direction == "Right") :
		# Left Scroll
		config.image = PIL.Image.new("RGBA", (dims[0],dims[1]))
		config.draw  = ImageDraw.Draw(config.image)
		config.id = config.image.im.id
		config.draw.rectangle((0,0,config.image.size[0]+32, config.screenHeight), fill=bgColor)

		# Draw the text with "borders"
		config.draw.text((-1,-1),colorWord,(0,0,0),font=font2)
		config.draw.text((1,1),colorWord,(0,0,0),font=font2)
		config.draw.text((0,0),colorWord,clr,font=font)

		offset = int(random.uniform(1,config.screenWidth-20))
		vOffset = int(random.uniform(0,config.rows)) * 32

		steps = int(stroopSteps)
		dy = 0
		y = vOffset
		wd = dims[0]
		ht = dims[1]

		if(direction == "Right") :
			start = -config.image.size[0]
			end = int(random.uniform(config.screenWidth/2, wd + config.screenWidth))
			dx = steps
			x = start

		if(direction == "Left") :
			start = config.screenWidth
			end  = config.screenWidth - int(random.uniform(-wd/2,wd)) #+ config.image.size[0] 
			dx = -steps
			x = start

	
#####################


