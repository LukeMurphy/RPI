import time
import random
import textwrap
import math
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageEnhance, ImageChops
from modules import colorutils, badpixels, coloroverlay

blocks = []
XOsBlocks = []

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# LEFT means text or icon moves to the left (i.e. comes from the right)
# RIGHT means text or icon moves to the right (i.e. comes from the left)
directionOrder = ["LEFT","RIGHT"]

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

class ScrollMessage :

	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
	#scroll speed and steps per cycle
	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
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
		if(config.colorOverlay == True) : self.clr = (200,200,200)

		''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
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

		''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
		# make a new image with the right size
		#self.config.renderImage = Image.new("RGBA", (config.actualScreenWidth , config.screenHeight))
		#self.scrollImage = Image.new("RGBA", pixLen)

		self.scrollImage = Image.new("RGBA", (self.pixLen[0] + 2 , self.fontHeight))
		self.draw  = ImageDraw.Draw(self.scrollImage)
		self.iid = self.scrollImage.im.id

		''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
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


def main(run = True) :
	global config, directionOrder
	print("---------------------")
	print("Diag Loaded")
	colorutils.brightness = config.brightness

	config.displayRows = int(workConfig.get("scroll", 'displayRows'))
	config.displayCols = int(workConfig.get("scroll", 'displayCols'))

	config.canvasImageWidth = config.screenWidth * config.displayRows
	config.canvasImageHeight = config.screenHeight

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
	config.bgColorVals = ((workConfig.get("scroll", 'bgColor')).split(','))
	config.bgColor = tuple(map(lambda x: int(x) , config.bgColorVals))
	config.txt1 = " " + (workConfig.get("scroll", 'txt1')) + " " 
	config.txt2 = " " + (workConfig.get("scroll", 'txt2')) + " " 
	config.txtfile = ""
	try :
		config.txtfile = (workConfig.get("scroll", 'txtfile')) 
	except Exception as e: 
		print (str(e))
	
	config.colorMode = (workConfig.get("scroll", 'colorMode')) 
	config.colorOverlay = (workConfig.getboolean("scroll", 'colorOverlay'))

	
	if (config.colorOverlay == True) :

		config.colorOverlayObjA = coloroverlay.ColorOverlay()
		config.colorOverlayObjB = coloroverlay.ColorOverlay()
		#config.colorA = colorutils.randomColor()
		#config.colorB = colorutils.randomColor()
		#config.currentColor = config.colorA

		#colorTransitionSetup()

	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
	# Used to composite XO's and message text
	#config.canvasImage = Image.new("RGBA", (config.canvasImageWidth  , int(config.screenHeight / config.displayRows)))
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

	if(config.useBlanks) :
		badpixels.numberOfDeadPixels = 20
		badpixels.size = config.canvasImage.size
		badpixels.config = config
		badpixels.setBlanksOnScreen() 

	if(config.directionOrder == "RIGHT-LEFT") : directionOrder = ["RIGHT","LEFT"]

	if(config.txtfile != "") :
		config.textArray = []
		fh = open('./configs/'+config.txtfile,'r')
		lines = fh.readlines()
		config.txt1 = "  "

		''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
		# not really necessary but maybe need some scrubs

		for text in lines :
			#text = fh.readline()
			config.textArray.append(text.replace('\n', ''))
			config.txt1 = config.txt1 + " --> " + text.replace('\n', '')

		config.txt2 = config.txt1
		config.breaksArray = [i for i, ltr in enumerate(config.txt1) if ltr == ">"]



	setUp()

	if(run) : runWork()


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def setUp():
	global config, XOsBlocks, overlayImage, blocks, usingEmoties, directionOrder
	pass



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

	'''
	# Blank out canvases
	draw  = ImageDraw.Draw(config.renderImageFull)
	draw.rectangle((0,0,config.screenWidth, config.screenHeight), fill = (0,0,0))

	draw  = ImageDraw.Draw(config.canvasImage)
	draw.rectangle((0,0,config.canvasImageWidth , config.screenHeight), fill = (config.bgColor))

	displayWidth = config.screenWidth * config.displayRows
	'''

	draw  = ImageDraw.Draw(config.canvasImageFinal)
	draw.rectangle((0,0,191,50), fill=(200,20,0), outline=(0,200,0))
	draw.rectangle((0,51,50,159), fill=(50,0,100), outline=(200,200,0))
	
	draw.rectangle((0,0,192,160), fill=None, outline=(0,255,255))
	draw.rectangle((0,0,1,1), fill=(0,255,255), outline=None)
	draw.point((0,0), fill=(0,255,255))

	draw.point((192,160), fill=(0,255,255))
	draw.point((191,159), fill=(0,255,255))


	config.render(config.canvasImageFinal, 0, 0, config.screenWidth+ config.windowXOffset, config.screenHeight + config.windowYOffset)




''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def callBack() :
	global config, XOs
	return True

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''



