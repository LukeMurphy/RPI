import time
import random
import textwrap
import math
import datetime
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageEnhance, ImageChops
from modules import colorutils, badpixels, coloroverlay
import argparse

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
## Image layers 

class unit :

	xPos = 0
	yPos = 0
	bgColor = (0,0,0)
	outlineColor = (0,0,0)
	tileSizeWidth = 64
	tileSizeHeight = 32


	def __init__(self) :

		self.image = Image.new("RGBA", (self.tileSizeWidth  , self.tileSizeHeight))
		self.draw = ImageDraw.Draw(self.image)

		self.colOverlay = coloroverlay.ColorOverlay()
		self.colOverlay.randomSteps = True 
		self.colOverlay.steps = 80
		self.unHideGrid = False

		pass

	def drawUnit(self):
		if(self.unHideGrid == False):
			self.colOverlay.stepTransition()

		self.bgColor  = tuple(int(a*config.brightness) for a in (self.colOverlay.currentColor))
		fontColor = self.bgColor
		outlineColor = self.bgColor

		if(self.unHideGrid == True):
			fontColor = config.fontColor
			outlineColor = config.outlineColor
		
		self.draw.rectangle((0,0,self.tileSizeWidth - 1,self.tileSizeHeight -1), 
			fill=self.bgColor,  outline=outlineColor)
		
		#u"\u000D"
		displyInfo1  =  str(self.col) + ", " + str(self.row) 
		displyInfo2  =  str(self.col * self.tileSizeWidth) + ", " + str(self.row * self.tileSizeHeight)

		#displyInfo = displyInfo.encode('utf-8')
		self.draw.text((2,- 1), (displyInfo1), fontColor, font=config.font)
		self.draw.text((2,- 1 + config.fontSize), (displyInfo2), fontColor, font=config.font)

		

def makeGrid():
	global config
	for row in range (0, config.rows) :
		for col in range (0, config.cols) :
			u = unit()
			u.config = config
			u.tileSizeWidth = config.tileSizeWidth
			u.tileSizeHeight = config.tileSizeHeight
			u.xPos = col * config.tileSizeWidth
			u.yPos = row * config.tileSizeHeight
			u.row = row
			u.col = col
			u.drawUnit()
			config.unitArrray.append(u)

def redrawGrid():
	
	if(random.random() < .002):
		config.unHideGrid = True
	if(random.random() < .02):
		config.unHideGrid = False

	for u in config.unitArrray:

		if(random.random() < .02):
			u.unHideGrid = True
		if(random.random() < .02):
			u.unHideGrid = False
		#u.unHideGrid = config.unHideGrid
		u.drawUnit()
		config.image.paste(u.image,(u.xPos,u.yPos), u.image)

	if(random.random() < config.fullimageGiltchRate)  : 
		glitchBox(config.image, -config.imageGlitchSize, config.imageGlitchSize)
	config.render(config.image, 0,0)


def showGrid():
	global config

	#config.draw.rectangle((0,0,config.screenWidth, config.screenHeight), fill=(0,0,0), outline=(0,0,0))
	config.draw.rectangle((0,0,config.screenWidth-1, config.screenHeight-1), fill=(0,0,0), outline=config.outlineColor)
	config.draw.rectangle((1,1,config.screenWidth-2, config.screenHeight-2), fill=(0,0,0), outline=(0,0,int(220 * config.brightness)))

	if(config.unHideGrid == False):
		config.colOverlay.stepTransition()
	config.bgColor  = tuple(int(a*config.brightness) for a in (config.colOverlay.currentColor))
	fontColor = config.bgColor
	outlineColor = config.bgColor

	if(random.random() < .002):
		config.unHideGrid = True
	if(config.unHideGrid == True):
		fontColor = config.fontColor
		outlineColor = config.outlineColor
	if(random.random() < .02):
		config.unHideGrid = False


	for row in range (0, config.rows) :
		for col in range (0, config.cols) :
			xPos = col * config.tileSizeWidth
			yPos = row * config.tileSizeHeight
			config.draw.rectangle((xPos,yPos,xPos + config.tileSizeWidth - 1, yPos +  config.tileSizeHeight -1), 
				fill=config.bgColor,  outline=outlineColor)
			
			#u"\u000D"
			displyInfo1  =  str(col) + ", " + str(row) 
			displyInfo2  =  str(col * config.tileSizeWidth) + ", " + str(row * config.tileSizeHeight)
	
			#displyInfo = displyInfo.encode('utf-8')

			config.draw.text((xPos + 2,yPos - 1), (displyInfo1), fontColor, font=config.font)
			config.draw.text((xPos + 2,yPos - 1 + config.fontSize), (displyInfo2), fontColor, font=config.font)

	# the overlay can fall apart independently of the overall image
	if(config.useOverLayImage  ==  True) :
		if(random.random() < config.overlayGlitchRate ) :
			glitchBox(config.loadedImage, -config.overlayGlitchSize, config.overlayGlitchSize)
		if(random.random() < config.overlayResetRate ) :
			config.loadedImage.paste(config.loadedImageCopy)
		config.image.paste(config.loadedImage, (config.overLayXPos, config.overLayYPos), config.loadedImage)
	
	if(random.random() < config.fullimageGiltchRate)  : 
		glitchBox(config.image, -config.imageGlitchSize, config.imageGlitchSize)
	config.render(config.image, 0,0)

def displayTest():
	global config
	#config.draw.rectangle((0,0,config.screenWidth, config.screenHeight), fill=(0,0,0), outline=(0,0,0))
	config.draw.rectangle((0,0,config.screenWidth-1, config.screenHeight-1), fill=(0,0,0), outline=config.outlineColor)
	config.draw.rectangle((1,1,config.screenWidth-2, config.screenHeight-2), fill=(0,0,0), outline=(0,0,int(220 * config.brightness)))
	config.draw.text((1,0),"TOP",config.fontColor,font=config.font)
	config.draw.text((1,config.screenHeight-15),"BOTTOM",config.fontColor,font=config.font)

	tm = datetime.datetime.now()
	tm = time.ctime()
	config.draw.text((10,24),tm,config.fontColor,font=config.font)

	w = 24
	h = 24
	xp = 10
	yp = 40

	rgbWheel = [(255,0,0),(255,255,0),(0,255,0),(0,255,255),(0,0,255),(255,0,255),(255,255,255)]


	for i in range(0,len(rgbWheel)):
		colorBlock = tuple(map(lambda x: int(int(x)  * config.brightness), rgbWheel[i]))
		config.draw.rectangle((xp,yp,xp + w,yp+h), fill=colorBlock, outline=colorBlock)
		xp += w

	yp+=h 
	xp = 10

	for i in range(0,len(rgbWheel)):
		colorBlock = tuple(map(lambda x: int(int(x)  * config.brightness * .5), rgbWheel[i]))
		config.draw.rectangle((xp,yp,xp + w,yp+h), fill=colorBlock, outline=colorBlock)
		xp += w


	config.render(config.image, 0,0)

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
## Image manipulation functions

def glitchBox(img, r1 = -10, r2 = 10) :
	apparentWidth = img.size[0]
	apparentHeight = img.size[1]
	dy = int(random.uniform(r1,r2))
	dx = int(random.uniform(1, config.imageGlitchSize))
	dx = 0

	# really doing "vertical" or y-axis glitching
	# block height is uniform but width is variable

	sectionHeight= int(random.uniform(2, apparentHeight - dy))
	sectionWidth = apparentWidth

	# 95% of the time they dance together as mirrors
	if(random.random() < .97) :
		cp1 = img.crop((dx, 0, dx + sectionWidth, sectionHeight))
		img.paste( cp1, (int(0 + dx), int(0 + dy)))	

def ScaleRotateTranslate(image, angle, center = None, new_center = None, scale = None,expand=False):
	if center is None:
		return image.rotate(angle)
	angle = -angle/180.0*math.pi
	nx,ny = x,y = center
	sx=sy=1.0
	if new_center:
		(nx,ny) = new_center
	if scale:
		(sx,sy) = scale
	cosine = math.cos(angle)
	sine = math.sin(angle)
	a = cosine/sx
	b = sine/sx
	c = x-nx*a-ny*b
	d = -sine/sy
	e = cosine/sy
	f = y-nx*d-ny*e
	return image.transform(image.size, Image.AFFINE, (a,b,c,d,e,f), resample=Image.BICUBIC)

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
## Setup and run functions

def main(run = True) :
	global config, directionOrder
	print("---------------------")
	print("Diag Loaded")


	colorutils.brightness = config.brightness
	config.canvasImageWidth = config.screenWidth
	config.canvasImageHeight = config.screenHeight
	config.canvasImageWidth -= 4
	config.canvasImageHeight -= 4
	config.delay = float(workConfig.get("signage", 'redrawDelay'))


	config.fontColorVals = ((workConfig.get("signage", 'fontColor')).split(','))
	config.fontColor = tuple(map(lambda x: int(int(x)  * config.brightness), config.fontColorVals))
	config.outlineColorVals = ((workConfig.get("signage", 'outlineColor')).split(','))
	config.outlineColor = tuple(map(lambda x: int(int(x) * config.brightness) , config.outlineColorVals))

	config.useOverLayImage = workConfig.getboolean("signage", 'useOverLayImage')
	config.overLayImage = workConfig.get("signage", 'overLayImage')
	config.overLayXPos = int(workConfig.get("signage", 'overLayXPos'))
	config.overLayYPos = int(workConfig.get("signage", 'overLayYPos'))
	config.imageGlitchSize = int(workConfig.get("signage", 'imageGlitchSize'))
	config.overlayGlitchSize = int(workConfig.get("signage", 'overlayGlitchSize'))
	config.overlayBrightness = float(workConfig.get("signage", 'overlayBrightness'))
	config.overlayGlitchRate = float(workConfig.get("signage", 'overlayGlitchRate'))
	config.fullimageGiltchRate = float(workConfig.get("signage", 'fullimageGiltchRate'))
	config.overlayResetRate = float(workConfig.get("signage", 'overlayResetRate'))


	config.colOverlay = coloroverlay.ColorOverlay()
	config.colOverlay.randomSteps = False 
	config.colOverlay.steps = 200 
	config.unHideGrid = False

	config.unitArrray = []

	try:
		config.showGrid = workConfig.getboolean("signage","showGrid")
	except Exception as e:
		print (str(e))
		config.showGrid = False

	
	config.tileSizeWidth = int(workConfig.get("displayconfig", 'tileSizeWidth'))
	config.tileSizeHeight = int(workConfig.get("displayconfig", 'tileSizeHeight'))

	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

	config.canvasImage = Image.new("RGBA", (config.canvasImageWidth  , config.canvasImageHeight))
	config.fontSize = 14
	config.font = ImageFont.truetype(config.path  + '/assets/fonts/freefont/FreeSansBold.ttf', config.fontSize)
	
	setUp()



	if(run) : runWork()

def setUp():
	global config
	if(config.useOverLayImage ==  True) :
		arg = config.path + config.overLayImage
		config.loadedImage = Image.open(arg , "r")
		config.loadedImage.load()

		config.enhancer = ImageEnhance.Brightness(config.loadedImage)
		config.loadedImage = config.enhancer.enhance(config.overlayBrightness)
		config.loadedImageCopy  = config.loadedImage.copy()
	makeGrid()

def runWork():
	global blocks, config, XOs
	#gc.enable()
	while True:
		iterate()
		time.sleep(config.delay)  

def iterate() :

	global config
	if config.showGrid ==  True :
		#showGrid()
		redrawGrid()
	else :		
		displayTest()		

def callBack() :
	global config, XOs
	return True

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''




