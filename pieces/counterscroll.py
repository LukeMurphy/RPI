import time
import random
import textwrap
import math
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageEnhance
from modules import colorutils, badpixels

blocks = []
XOsBlocks = []

# LEFT means text or icon moves to the left (i.e. comes from the right)
# RIGHT means text or icon moves to the right (i.e. comes from the left)
directionOrder = ["LEFT","RIGHT"]

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

class ScrollMessage :

	########################
	#scroll speed and steps per cycle
	scrollSpeed = 0.004
	steps = 1
	fontSize = 14

	def __init__(self, messageString, direction, config, clr='') :
		#print ("init: " + messageString)
		self.messageString = messageString
		self.direction = direction

		self.config = config
		if (clr == '') :
			if(config.colorMode == "getRandomRGB") : self.clr = colorutils.getRandomRGB()
			if(config.colorMode == "randomColor") : self.clr = colorutils.randomColor()
			if(config.colorMode == "getRandomColorWheel") : self.clr = colorutils.getRandomColorWheel()
		else: self.clr = clr
		#self.clr = colorutils.randomColor()
		#self.clr = colorutils.getSunsetColors()
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
			self.xPos += config.steps
		else :
			self.xPos -= config.steps

		#if(self.xPos > self.end) :
		#	self.xPos = self.start = -self.scrollImage.size[0]

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

class XOx :

	########################
	#scroll speed and steps per cycle
	scrollSpeed = 0.004
	steps = 1.5
	lineThickness = 2
	bufferSpacing = 40
	xsWidth = 54
	maxNumXOs = 12
	minNumXOs = 5
	XColor = [255,0,0]
	OColor = [255,0,0] 
	ArrowColor = [255,2,0] 

	def __init__(self, direction, config, n, rng) :
		#print ("init: " + messageString)

		self.direction = direction
		self.config = config
		self.clr = (int(255*config.brightness),0,0)

		self.xsWidth = int(.85 * config.fontSize)
		self.maxNumXOs = int(self.xsWidth / 2)

		self.xoString =  self.makeBlock(config.useArrows)

		prv = n - 1
		nxt = n + 1
		if n < 3 :
			if (prv < 0) : prv = 3 - 1
			if (nxt == 3) : nxt = 0
		else :
			if (prv < 3) : prv = rng - 1
			if (nxt == rng) : nxt = 3

		self.prvBlock = prv
		self.nxtBlock = nxt

	def makeBlock(self, dash=False) :
		strg = ""

		num = int(random.uniform(self.minNumXOs,self.maxNumXOs))
		
		for n in range (0, num) : 
			if (dash) :
				strg += "-"
			else : 
				if (random.random() > .5) : strg += "X"
				else  : strg += "O"

		self.width = n * (self.xsWidth + 8)

		if(self.direction == "RIGHT") :
			self.xPos = self.config.screenWidth + self.config.bufferSpacing
			self.end = - self.width
		else :
			self.xPos = 0
			self.end = self.config.screenWidth * self.config.displayRows
		self.yPos = 0
		
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
				clr  = (int(self.XColor[0] * config.brightness), int(self.XColor[1] * config.brightness), int(self.XColor[2] * config.brightness))
				draw.line((startX, startY, endX, endY), fill = clr, width = self.lineThickness)
				draw.line((endX, startY, startX, endY), fill = clr, width = self.lineThickness)
			elif (self.xoString[n]) ==  "O" :
				clr  = (int(self.OColor[0] * config.brightness), int(self.OColor[1] * config.brightness), int(self.OColor[2] * config.brightness))
				draw.ellipse((startX, startY, endX, endY),  outline=clr)
				draw.ellipse((startX +1, startY+1, endX-1, endY-1),  outline=clr)
			else : 
				clr  = (int(self.ArrowColor[0] * config.brightness), int(self.ArrowColor[1] * config.brightness), int(self.ArrowColor[2] * config.brightness))
				y0 = startY + self.xsWidth/2
				yA = self.xsWidth/4

				if(self.direction == "RIGHT") :
					xA = startX + yA * math.tan(math.pi/4)
					# the horizontal
					draw.line((startX, y0, endX, y0), fill = clr, width = self.lineThickness)
					# the blades
					draw.line((xA, yA, startX, y0), fill = clr, width = self.lineThickness)
					draw.line((xA, yA + self.xsWidth/2 , startX, y0), fill = clr, width = self.lineThickness)				
				else :
					xA = endX - yA * math.tan(math.pi/4)
					# the horizontal
					draw.line((startX, y0, endX, y0), fill = clr, width = self.lineThickness)
					# the blades
					draw.line((xA, yA, endX, y0), fill = clr, width = self.lineThickness)
					draw.line((xA, yA + self.xsWidth/2 , endX, y0), fill = clr, width = self.lineThickness)

			leng += endX - startX
	
		if(self.direction == "RIGHT") : 
			self.xPos -= self.steps
		else :
			self.xPos += self.steps

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def main(run = True) :
	global config, directionOrder
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
	config.counterScrollText = (workConfig.getboolean("scroll", 'counterScrollText'))
	config.useXOs = (workConfig.getboolean("scroll", 'useXOs')) 
	config.useArrows = (workConfig.getboolean("scroll", 'useArrows')) 
	config.sansSerif = (workConfig.getboolean("scroll", 'sansSerif'))
	config.useBlanks = (workConfig.getboolean("scroll", 'useBlanks'))
	config.useThreeD = (workConfig.getboolean("scroll", 'useThreeD'))
	config.directionOrder = (workConfig.get("scroll", 'directionOrder'))
	config.txt1 = " " + (workConfig.get("scroll", 'txt1')) + " " 
	config.txt2 = " " + (workConfig.get("scroll", 'txt2')) + " " 
	config.colorMode = (workConfig.get("scroll", 'colorMode')) 

	# Used to composite XO's and message text
	#config.canvasImage = Image.new("RGBA", (config.canvasImageWidth  , int(config.screenHeight / config.displayRows)))
	config.canvasImage = Image.new("RGBA", (config.canvasImageWidth  , config.canvasImageHeight))

	# Used to be final image sent to renderImageFull after canvasImage has been chopped up and reordered to fit
	config.canvasImageFinal = Image.new("RGBA", (config.canvasWidth , config.canvasHeight))

	#config.drawBeforeConversion = callBack
	config.actualScreenWidth = config.canvasImage.size[0]

	imageWrapLength = config.screenWidth * 50
	config.warpedImage = Image.new("RGBA", (imageWrapLength, config.screenHeight))

	if(config.rotation == -90) :
		imageWrapLength = config.screenWidth * 50
		config.warpedImage = Image.new("RGBA", (imageWrapLength, config.screenWidth))

	if(config.useBlanks) :
		badpixels.numberOfDeadPixels = 50
		badpixels.size = config.canvasImage.size
		badpixels.config = config
		badpixels.setBlanksOnScreen() 

	if(config.directionOrder == "RIGHT-LEFT") : directionOrder = ["RIGHT","LEFT"]

	setUp()

	if(run) : runWork()

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def makeBlock(n, rng = 3, direction = "LEFT", strgArg="") :
	global config
	strg = strgArg

	if(strgArg == "") : 
		#if n in[1,3,5] :
		if n < 3:
			strg = config.txt1 
		else : 
			strg = config.txt2

	clrseq = ((100,0,0),(0,100,0),(0,0,100))
	c = n if n <3 else n-3

	#block = ScrollMessage(makeText(config.usingEmoties, strg), direction ,config, clrseq[c])
	block = ScrollMessage(makeText(config.usingEmoties, strg), direction ,config)

	prv = n - 1
	nxt = n + 1
	if n < 3 :
		if (prv < 0) : prv = 3 - 1
		if (nxt == 3) : nxt = 0
	else :
		if (prv < 3) : prv = rng - 1
		if (nxt == rng) : nxt = 3

	block.prvBlock = prv
	block.nxtBlock = nxt
	block.width = block.scrollImage.size[0]
	block.bufferSpacing = 8

	#print(n, block.prvBlock, block.nxtBlock, block.width, direction, strg)	
	return block

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def makeText(emotis=False, arg = " FEEL BAD ") :
	global config
	space = "  "
	strg = ""
	if(emotis) :
		maxNums = int(config.fontSize / 2)
		num = int(random.uniform(3,maxNums))
		for n in range (0, num) : 
			strg += "(:" + space
			if (random.random() > .5) : strg += "o:" + space
			if (random.random() > .95) : strg += "(;" + space
		#strg ="| oTESTx |"
	else :
		strg = arg
	return strg

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def setUp():
	global config, XOsBlocks, overlayImage, blocks, usingEmoties, directionOrder

	#overlayImage = Image.new("RGBA", (config.actualScreenWidth , config.screenHeight))
	lastWidth = config.canvasImageWidth
	direction = directionOrder[0]

	# Used if there are 2 text statements running against eachother
	rng = 3 if (config.usingEmoties == True or config.counterScrollText == False) else 6

	for n in range (0, rng) :

		if n >= 3 : direction = directionOrder[1]
		if n == 3 : lastWidth = 0
		
		block = makeBlock(n, rng, direction)

		if(block.direction == "RIGHT") : 
			block.start = lastWidth
			block.end = - block.width #- lastWidth -config.screenWidth * config.displayRows 
		elif(block.direction == "LEFT")  :
			block.start = -block.width - lastWidth
			block.end = config.screenWidth * config.displayRows
		
		lastWidth += block.width
		block.xPos = block.start
		blocks.append(block)

	#lastWidth = 0
	#direction = directionOrder[1]

	if(config.useXOs) :
		lastWidth = 0
		direction = directionOrder[1]
		for n in range (0, 3) :
			XOs = XOx(direction, config, n, 3)
			if(XOs.direction == "RIGHT") : 
				XOs.xPos = XOs.start = config.canvasImageWidth + lastWidth
			else :	
				XOs.xPos = XOs.start = - lastWidth - XOs.width
			lastWidth += XOs.width + XOs.bufferSpacing
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

	displayWidth = config.screenWidth * config.displayRows

	''''''''''''

	# Scroll message
	rng = 3 if config.usingEmoties == True or config.counterScrollText == False else 6

	for i in range (0, rng) :

		## This reverses the pasting so the text scrolling from right to left is on top
		## Right to Left scrolling is the normal for readability ....
		if(rng != 3) :
			n = (rng - 1) - i
		else: 
			n = i

		block = blocks[n]
		block.scroll()

		# paste scrollImage into the canvasImage - but eventually chop and flip
		config.canvasImage.paste(block.scrollImage, (block.xPos, config.vOffset), block.scrollImage)

		if(block.xPos > displayWidth and block.direction== "LEFT" ) :
			# a block moves off-screen, possibly change message, then move to back of queue
			if(random.random() > .5 ) :
				strg = config.txt1 if random.random() > .5 else config.txt2
				blocks[n] = makeBlock(n , rng, block.direction, strg)
				block = blocks[n]
				block.end = displayWidth

			nxtBlockStartPoint = blocks[block.prvBlock].xPos
			if ((nxtBlockStartPoint - block.width ) > 0 ):
				block.xPos =  -block.width
			else :
				block.xPos = nxtBlockStartPoint - block.width 

		if(block.xPos < block.end and block.direction== "RIGHT" )  :
			if(random.random() > .5 ) :
				strg = config.txt1 if random.random() > .5 else config.txt2
				blocks[n] = makeBlock(n , rng, block.direction, strg)
				block = blocks[n]
				block.end = - block.width
	
			prevBlockEndPoint = blocks[block.prvBlock].xPos + blocks[block.prvBlock].width
			if (prevBlockEndPoint < displayWidth ):
				block.xPos = config.canvasImageWidth + block.width
			else :
				block.xPos = prevBlockEndPoint + block.bufferSpacing 


	if(config.useBlanks) : badpixels.drawBlanks(config.canvasImage, False)
	if(random.random() > .998 and (config.useBlanks)) : badpixels.setBlanksOnScreen() 

	''''''''''''

	if(config.useXOs) :
		# Add the counter XO's
		
		for n in range (0, 3) :
			XOsBlock = XOsBlocks[n]
			XOsBlock.drawCounterXO()

			if (XOsBlock.xPos  > displayWidth and XOsBlock.direction == "LEFT") :
				if(random.random() > .5 ) : 
					XOsBlocks[n].xoString = XOsBlocks[n].makeBlock(config.useArrows)
					XOsBlock.end = displayWidth

				nxtBlockStartPoint = XOsBlocks[XOsBlock.prvBlock].xPos
				if ((nxtBlockStartPoint - XOsBlock.width ) > 0 ):
					XOsBlock.xPos =  -XOsBlock.width
				else :
					XOsBlock.xPos = nxtBlockStartPoint - XOsBlock.width 

				#print (n,XOsBlock.xPos,XOsBlock.end, XOsBlock.width)
				#XOsBlocks[n].xPos = XOsBlocks[n].start =  XOsBlocks[XOsBlock.prvBlock].xPos - XOsBlock.width - XOsBlock.bufferSpacing
				

			elif(XOsBlocks[n].xPos < -XOsBlocks[n].width and XOsBlocks[n].direction == "RIGHT") :	
				if(random.random() > .5 ) : 
					XOsBlock.xoString = XOsBlock.makeBlock(config.useArrows)
					XOsBlock.end  = -XOsBlock.width

				prevBlockEndPoint = XOsBlocks[XOsBlock.prvBlock].xPos + XOsBlocks[XOsBlock.prvBlock].width
				if (prevBlockEndPoint < displayWidth ):
					XOsBlock.xPos = config.canvasImageWidth + XOsBlock.width
				else :
					XOsBlock.xPos = prevBlockEndPoint + XOsBlock.bufferSpacing 
				#XOsBlock.xPos = XOsBlock.start = XOsBlocks[XOsBlock.prvBlock].xPos + XOsBlocks[XOsBlock.prvBlock].width + XOsBlock.bufferSpacing
				

	''''''''''''

	# Chop up the scrollImage into "rows"
	for n in range(0, config.displayRows) :
		segmentHeight = int(config.canvasHeight / config.displayRows)
		segmentWidth = config.canvasWidth
		segment =  config.canvasImage.crop((n * config.screenWidth, 0, segmentWidth + n * config.screenWidth, segmentHeight))
		
		# At some point go to modulo for even/odd ... but for now not more than 5 rows
		if ((n == 0 or n == 2 or n == 4) and (config.displayRows >  1) ) :
			segment = ImageOps.flip(segment)
			segment = ImageOps.mirror(segment)
		config.canvasImageFinal.paste(segment, (0, n * segmentHeight))

	# Debug geometry for rotation
	#tS = config.canvasImageFinal.size
	#tDraw = ImageDraw.Draw(config.canvasImageFinal)
	#tDraw.rectangle((0,0,tS[0],tS[1]), fill = None, outline=(0,255,0))

	if(config.useThreeD) :
		ThreeD(config.canvasImageFinal)
		config.render(config.warpedImage, 0, 0, config.canvasWidth  , config.canvasHeight, False)
	else : 
		config.render(config.canvasImageFinal, 0, 0, config.canvasWidth  , config.canvasHeight, False)

	
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def ThreeD(imageToRender) :
	numSegments = 64
	dFactor =  1.334
	offset = 0
	angle =  math.pi  / numSegments
	if(config.rotation == -90) :
		numSegments = 32
		dFactor =  1.4
		angle =  math.pi  / numSegments
		width  = config.screenHeight
		height = config.screenWidth
	else: 
		width  = config.screenWidth
		height = config.screenHeight
	segmentWidth = int((width) * math.sin(angle) /3 )
	#stepRange = int(pixLen[0] / stepSize)
	useColorFLicker = False
	placementx = 1

	for n in range(0,numSegments) :
		pCropx = n * segmentWidth + offset
		pWidth  = math.fabs(dFactor * segmentWidth * math.sin(angle * n/1)) + 1
		projectedWidth = int(pWidth)

		segmentImage  = Image.new("RGBA", (projectedWidth, height))
		croppedSegment = imageToRender.crop((pCropx,0, pCropx + segmentWidth, height))
		segmentImage = croppedSegment.resize((projectedWidth,height))
		br = pWidth  / segmentWidth

		if(useColorFLicker) :
			segmentColorizer = Image.new("RGBA", (projectedWidth, height))
			draw = ImageDraw.Draw(segmentColorizer)
			draw.rectangle((0,0,projectedWidth,height), fill = config.randomColor())
			segmentImage = ImageChops.multiply(segmentImage, segmentColorizer)

		enhancer = ImageEnhance.Brightness(segmentImage)
		segmentImage = enhancer.enhance(br)
		#segmentImage = segmentImage.filter(ImageFilter.BLUR)
		#warpedImage.paste(segmentColorizer , (placementx,0))
		config.warpedImage.paste(segmentImage , (placementx,0))
		placementx += projectedWidth

	#config.render(warpedImage,0,0, config.screenWidth, config.screenHeight)

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def callBack() :
	global config, XOs
	return True

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''



