import time
import random
import textwrap
import math
from PIL import ImageFont, Image, ImageDraw, ImageOps
from modules import colorutils, badpixels

blocks = []
XOsBlocks = []

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

class ScrollMessage :

	########################
	#scroll speed and steps per cycle
	scrollSpeed = 0.004
	steps = 1
	fontSize = 14

	def __init__(self, messageString, direction, config) :
		#print ("init: " + messageString)
		self.messageString = messageString
		self.direction = direction

		self.config = config
		self.clr = colorutils.getRandomRGB()
		self.clr = colorutils.randomColor()
		#self.clr = (0,0,0)

		# draw the message to get its size
		if(config.sansSerif) : 
			font = ImageFont.truetype(config.path  + '/assets/fonts/freefont/FreeSansBold.ttf', config.fontSize)
		else :
			font = ImageFont.truetype(config.path  + '/assets/fonts/freefont/FreeSerifBold.ttf', config.fontSize)
		tempImage = Image.new("RGBA", (1200,196))
		draw  = ImageDraw.Draw(tempImage)
		self.pixLen = draw.textsize(self.messageString, font = font)
		# For some reason textsize is not getting full height !
		self.fontHeight = int(self.pixLen[1] * 1.3)

		# make a new image with the right size
		#self.config.renderImage = Image.new("RGBA", (config.actualScreenWidth , config.screenHeight))
		#self.scrollImage = Image.new("RGBA", pixLen)

		self.scrollImage = Image.new("RGBA", (self.pixLen[0] + 2 , self.fontHeight))
		self.draw  = ImageDraw.Draw(self.scrollImage)
		self.iid = self.scrollImage.im.id
		
		#self.draw.rectangle((0,0,self.pixLen[0]+4, self.pixLen[1]), fill = (0,0,0))
		# Draw the text with "borders"
		indent = int(.05 * config.tileSize[0])
		for i in range(1, config.shadowSize) :
			self.draw.text((indent + -i,-i),self.messageString,(0,0,0),font=font)
			self.draw.text((indent + i,i),self.messageString,(0,0,0),font=font)
		self.draw.text((2,0),self.messageString, self.clr ,font=font)




		self.xPos = 0
		self.yPos = config.vOffset

		#self.end = config.screenWidth * config.displayRows

	def scroll(self) :
		if(self.direction == "LEFT") :
			self.xPos += self.steps
		else :
			self.xPos -= self.steps

		#if(self.xPos > self.end) :
		#	self.xPos = self.start = -self.scrollImage.size[0]

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

class XOx :

	########################
	#scroll speed and steps per cycle
	scrollSpeed = 0.004
	steps = 1
	lineThickness = 2
	bufferSpacing = 40
	xsWidth = 54
	maxNumXOs = 10

	def __init__(self, direction, config) :
		#print ("init: " + messageString)

		self.direction = direction
		config.scrollSpeed = float(workConfig.get("scroll", 'scrollSpeed'))

		self.config = config
		self.clr = (int(255*config.brightness),0,0)

		self.xsWidth = int(.85 * config.fontSize)
		self.maxNumXOs = int(self.xsWidth / 2)

		self.xoString =  self.makeBlock()

	def makeBlock(self) :
		strg = ""
		self.xPos = config.screenWidth + self.bufferSpacing
		self.yPos = 0

		num = int(random.uniform(3,self.maxNumXOs))
		
		for n in range (0, num) : 
			if (random.random() > .5) : strg += "X"
			else  : strg += "O"

		self.messageLength = n * (self.xsWidth + 8)

		return strg

	def drawCounterXO(self) :
		## Try with drawing xo's first then by pasting block ..

		#draw  = ImageDraw.Draw(self.config.renderImageFull)
		draw  = ImageDraw.Draw(self.config.canvasImage)
		leng = 0 
		for n in range (0, len(self.xoString)):
			startX = self.xPos + n * self.xsWidth + 8
			endX = self.xPos + n * self.xsWidth + self.xsWidth
			startY = 0
			endY = self.xsWidth

			if (self.xoString[n]) ==  "X" :
				draw.line((startX, startY, endX, endY), fill = self.clr, width = self.lineThickness)
				draw.line((endX, startY, startX, endY), fill = self.clr, width = self.lineThickness)
			else :
				draw.ellipse((startX, startY, endX, endY),  outline=self.clr)
				draw.ellipse((startX +1, startY+1, endX-1, endY-1),  outline=self.clr)

			leng += endX - startX
	
		self.xPos -= config.steps

		'''
		if(self.xPos < -self.messageLength - self.bufferSpacing) :
			if(random.random() > .8 ) :
				self.xoString = self.makeBlock()
			else :
				self.xPos = config.canvasImageWidth  + self.bufferSpacing
		'''

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def makeBlock(emotis=False, arg = " FEEL BAD ") :
	global config
	space = "  "
	strg = ""
	if(emotis) :
		maxNums = int(config.fontSize / 2)
		num = int(random.uniform(3,maxNums))
		for n in range (0, num) : 
			strg += ":)"+space
			if (random.random() > .5) : strg += ":o"+space
			if (random.random() > .95) : strg += ";)"+space
		#strg ="| oTESTx |"
	else :
		strg = arg
	return strg


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def main(run = True) :
	global config
	print("---------------------")
	print("CounterScroll Loaded")
	colorutils.brightness = config.brightness

	config.displayRows = int(workConfig.get("scroll", 'displayRows'))
	config.displayCols = int(workConfig.get("scroll", 'displayCols'))
	config.canvasImageWidth = config.canvasWidth * config.displayRows
	config.canvasImageHeight = config.canvasHeight

	config.fontSize = int(workConfig.get("scroll", 'fontSize'))
	config.vOffset = int(workConfig.get("scroll", 'vOffset'))
	config.scrollSpeed = float(workConfig.get("scroll", 'scrollSpeed'))
	config.steps = int(workConfig.get("scroll", 'steps'))
	config.shadowSize = int(workConfig.get("scroll", 'shadowSize'))

	config.usingEmoties = (workConfig.getboolean("scroll", 'usingEmoties'))
	config.useXOs = (workConfig.getboolean("scroll", 'useXOs'))
	config.sansSerif = (workConfig.getboolean("scroll", 'sansSerif'))
	config.txt1 = " " + (workConfig.get("scroll", 'txt1')) + " " 
	config.txt2 = " " + (workConfig.get("scroll", 'txt2')) + " " 

	# Used to composite XO's and message text
	#config.canvasImage = Image.new("RGBA", (config.canvasImageWidth  , int(config.screenHeight / config.displayRows)))
	config.canvasImage = Image.new("RGBA", (config.canvasImageWidth  , config.canvasImageHeight))

	# Used to be final image sent to renderImageFull after canvasImage has been chopped up and reordered to fit
	config.canvasImageFinal = Image.new("RGBA", (config.canvasWidth , config.canvasHeight))

	#config.drawBeforeConversion = callBack
	config.actualScreenWidth = config.canvasImage.size[0]
	badpixels.numberOfDeadPixels = 50
	badpixels.size = config.canvasImage.size
	badpixels.config = config
	badpixels.setBlanksOnScreen() 

	setUp()

	if(run) : runWork()

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def setUp():
	global config, XOsBlocks, overlayImage, blocks, usingEmoties

	#overlayImage = Image.new("RGBA", (config.actualScreenWidth , config.screenHeight))
	lastWidth = 0
	direction = "LEFT"
	rng = 3 if config.usingEmoties == True else 6
	for n in range (0, rng) :
		#scroll = ScrollMessage(makeBlock(),"LEFT",config)
		strg = config.txt1 if n in[1,3,5] else config.txt2
		if n == 3 :
			direction = "RIGHT"
			lastWidth = 0
		scroll = ScrollMessage(makeBlock(config.usingEmoties, strg), direction ,config)
	
		if(scroll.direction == "RIGHT") : 
			scroll.start = lastWidth + config.canvasImageWidth
			scroll.end = -config.screenWidth * config.displayRows
		else :
			scroll.start = -scroll.scrollImage.size[0] - lastWidth
			scroll.end = config.screenWidth * config.displayRows

		lastWidth += scroll.scrollImage.size[0]
		scroll.xPos = scroll.start
		blocks.append(scroll)

	lastWidth = 0

	if(config.useXOs) :
		for n in range (0, 3) :
			XOs = XOx("RIGHT", config)
			XOs.xPos = XOs.start = config.canvasImageWidth + lastWidth
			lastWidth += XOs.messageLength + XOs.bufferSpacing
			XOsBlocks.append(XOs)

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def runWork():
	global blocks, config, XOs
	#gc.enable()
	while True:
		iterate()
		time.sleep(config.scrollSpeed)  

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def iterate() :
	global config, blocks, x, y, XOsBlocks, usingEmoties

	# Blank out canvases
	draw  = ImageDraw.Draw(config.renderImageFull)
	draw.rectangle((0,0,config.screenWidth, config.screenHeight), fill = 0)

	draw  = ImageDraw.Draw(config.canvasImage)
	draw.rectangle((0,0,config.canvasImageWidth , config.screenHeight), fill = 0)

	# Scroll message
	rng = 3 if config.usingEmoties == True else 6
	for n in range (0, rng) :
		scroll = blocks[n]
		scroll.scroll()
		# paste scrollImage into the canvasImage - but eventually chop and flip
		config.canvasImage.paste(scroll.scrollImage, (scroll.xPos, config.vOffset), scroll.scrollImage)

		# previous block
		p = n -1 if (n != 0) else 2

		# a block moves off-screen, possibly change message, then move to back of queue
		if(scroll.xPos > scroll.end and scroll.direction== "LEFT" ) :
			if(random.random() > .5) :
				strg = config.txt1 if n in[1,3,5] else config.txt2
				direction = blocks[n].direction
				blocks[n] = ScrollMessage(makeBlock(config.usingEmoties, strg), direction,config)
				scroll = blocks[n]
			scroll.xPos = scroll.start = -scroll.scrollImage.size[0] + blocks[p].xPos
			scroll.end = config.screenWidth * config.displayRows
		if(scroll.xPos < scroll.end and scroll.direction== "RIGHT" )  :
			scroll.xPos = scroll.start = scroll.scrollImage.size[0] + config.screenWidth
			scroll.end = -config.screenWidth * config.displayRows


	badpixels.drawBlanks(config.canvasImage, False)
	if(random.random() > .998) : badpixels.setBlanksOnScreen() 

	if(config.useXOs) :
		# Add the counter XO's
		for n in range (0, 3) :
			XOs = XOsBlocks[n]
			XOs.drawCounterXO()

			# previous block
			p = n -1 if (n != 0) else 2

			if(XOs.xPos < -XOs.messageLength) :
				if(random.random() > .5 ) :
					XOsBlocks[n].xoString = XOs.makeBlock()
				XOs.xPos = XOsBlocks[p].xPos + XOsBlocks[p].messageLength + XOs.bufferSpacing if (XOsBlocks[p].xPos + XOsBlocks[p].messageLength >= config.canvasImageWidth) else config.canvasImageWidth

	# Chop up the scrollImage into "rows"
	for n in range(0, config.displayRows) :
		segmentHeight = int(config.canvasHeight / config.displayRows)
		segmentWidth = config.canvasWidth
		segment =  config.canvasImage.crop((n * config.screenWidth, 0, segmentWidth + n * config.screenWidth, segmentHeight))
		
		# At some point go to modulo for even/odd ... but for now not more than 5 rows
		if (n == 1 or n == 3) :
			segment = ImageOps.flip(segment)
			segment = ImageOps.mirror(segment)

		config.canvasImageFinal.paste(segment, (0, n * segmentHeight))

	# Debug geometry for rotation
	#tS = config.canvasImageFinal.size
	#tDraw = ImageDraw.Draw(config.canvasImageFinal)
	#tDraw.rectangle((0,0,tS[0],tS[1]), fill = None, outline=(0,255,0))

	config.render(config.canvasImageFinal, 0, 0, config.canvasWidth  , config.canvasHeight, False)


	'''''''''''''' #FIX THIS !!!!
	#badpixels.drawBlanks()

	#config.updateCanvas()

	#time.sleep(1)
	
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def callBack() :
	global config, XOs
	return True

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''



