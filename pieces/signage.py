import time
import random
import textwrap
import math
import datetime
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageEnhance, ImageChops
from modules import colorutils, badpixels, coloroverlay
import argparse

class unit:
	def __init__(self, config):
		self.config = config
		self.xPos = 0
		self.yPos = 0
		self.xPosR = self.config.screenWidth/2
		self.yPosR = self.config.screenHeight/2
		self.move = True
		
		self.dx = random.uniform(-3,3)
		self.dy = random.uniform(-3,3)

		self.image = Image.new("RGBA", (100 , 100))
		self.fillColor = colorutils.getRandomRGB()
		self.outlineColor = colorutils.getRandomRGB(config.brightness)
		self.objWidth = 20
		self.objWidthMax = 26
		self.objWidthMin = 13

		self.draw  = ImageDraw.Draw(self.image)

	def update(self):
		self.xPos += self.dx
		self.yPos += self.dy
		
		self.xPosR += self.dx
		self.yPosR += self.dy

		if(self.xPosR + self.objWidth > self.config.screenWidth) : 
			self.xPosR = self.config.screenWidth - self.objWidth 
			self.xPos = self.config.screenWidth - self.objWidth 
			self.changeColor()
			self.dx *= -1
		if(self.yPosR + self.objWidth> self.config.screenHeight) : 
			self.yPosR = self.config.screenHeight-self.objWidth 
			self.yPos = self.config.screenHeight-self.objWidth 
			self.changeColor()
			self.dy *= -1
		if(self.xPosR < 0) : 
			self.xPosR = 0
			self.xPos = 0
			self.changeColor()
			self.dx*= -1
		if(self.yPosR < 0) : 
			self.yPosR = 0
			self.yPos = 0
			self.changeColor()
			self.dy *= -1

		if(self.dx == 0 and self.dy == 0 ):
			if(random.random() > .5): self.dx = (2 * random.random())
			if(random.random() > .5): self.dy = (2 * random.random())

	
	def render(self):
		xPos = int(self.xPosR)
		yPos = int(self.yPosR)
		self.config.draw.rectangle((xPos, yPos,xPos+ self.objWidth , yPos +self.objWidth ), fill=self.fillColor, outline=self.outlineColor)


	def changeColor(self):
		self.fillColor = colorutils.randomColor(random.random())
		self.outlineColor = colorutils.getRandomRGB()
		if(random.random() > .5): self.dx = (4 * random.random() + 2)
		if(random.random() > .5): self.dy = (4 * random.random() + 2)
		if(random.random() > .5): self.objWidth = int(random.uniform(self.objWidthMin,self.objWidthMax))



def showGrid():
	global config
	#config.draw.rectangle((0,0,config.screenWidth, config.screenHeight), fill=(0,0,0), outline=(0,0,0))
	config.draw.rectangle((0,0,config.screenWidth-1, config.screenHeight-1), fill=(0,0,0), outline=config.outlineColor)
	config.draw.rectangle((1,1,config.screenWidth-2, config.screenHeight-2), fill=(0,0,0), outline=(0,0,int(220 * config.brightness)))
	

	for row in range (0, config.rows) :
		for col in range (0, config.cols) :
			xPos = col * config.tileSizeWidth
			yPos = row * config.tileSizeHeight
			config.draw.rectangle((xPos,yPos,xPos + config.tileSizeWidth - 1, yPos +  config.tileSizeHeight -1), fill=(0,0,0), outline=config.outlineColor)
			
			displyInfo  =  str(col) + ", " + str(row) + "\n" + str(col * config.tileSizeWidth) + ", " + str(row * config.tileSizeHeight)
			config.draw.text((xPos + 2,yPos - 1),displyInfo,config.fontColor,font=config.font)

	if(config.useOverLayImage  ==  True) :
		config.image.paste(config.loadedImage, (config.overLayXPos, config.overLayYPos), config.loadedImage)
	
	config.render(config.image, 0,0)

def main(run = True) :
	global config, directionOrder
	print("---------------------")
	print("Diag Loaded")


	colorutils.brightness = config.brightness
	config.canvasImageWidth = config.screenWidth
	config.canvasImageHeight = config.screenHeight
	config.canvasImageWidth -= 4
	config.canvasImageHeight -= 4
	config.delay = .005
	config.numUnits  = 1

	config.fontColorVals = ((workConfig.get("signage", 'fontColor')).split(','))
	config.fontColor = tuple(map(lambda x: int(int(x)  * config.brightness), config.fontColorVals))
	config.outlineColorVals = ((workConfig.get("signage", 'outlineColor')).split(','))
	config.outlineColor = tuple(map(lambda x: int(int(x) * config.brightness) , config.outlineColorVals))

	config.useOverLayImage = workConfig.getboolean("signage", 'useOverLayImage')
	config.overLayImage = workConfig.get("signage", 'overLayImage')
	config.overLayXPos = int(workConfig.get("signage", 'overLayXPos'))
	config.overLayYPos = int(workConfig.get("signage", 'overLayYPos'))

	try:
		config.showGrid = workConfig.getboolean("signage","showGrid")
	except Exception as e:
		print (str(e))
		config.showGrid = False

	
	config.tileSizeWidth = int(workConfig.get("displayconfig", 'tileSizeWidth'))
	config.tileSizeHeight = int(workConfig.get("displayconfig", 'tileSizeHeight'))

	if(config.useOverLayImage ==  True) :
		arg = "."+config.overLayImage
		config.loadedImage = Image.open(arg , "r")
		config.loadedImage.load()


	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

	config.canvasImage = Image.new("RGBA", (config.canvasImageWidth  , config.canvasImageHeight))
	config.fontSize = 14
	config.font = ImageFont.truetype(config.path  + '/assets/fonts/freefont/FreeSansBold.ttf', config.fontSize)
	

	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
	config.unitArrray = []
	for i in range(0,config.numUnits):
		obj = unit(config)
		#obj.move = False
		obj.objWidth = 5
		obj.objWidthMax = 4
		obj.objWidthMin = 3
		config.unitArrray.append(obj)

	setUp()

	if(run) : runWork()

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

def setUp():
	global config
	arg = "./assets/imgs/miscl/burst.png"
	config.loadedImage = Image.open(arg , "r")
	config.loadedImage.load()

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def runWork():
	global blocks, config, XOs
	#gc.enable()
	while True:
		iterate()
		time.sleep(config.delay)  

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


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

	
	for i in range(0,config.numUnits):
		obj = 	config.unitArrray[i]
		if(obj.move ==True) : obj.update()
		obj.render()
	
	config.render(config.image, 0,0)

def iterate() :

	global config
	if config.showGrid ==  True :
		showGrid()
	else :		
		displayTest()		


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def callBack() :
	global config, XOs
	return True

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''



