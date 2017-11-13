import time
import random
import textwrap
import math
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageEnhance, ImageChops
from modules import colorutils, badpixels, coloroverlay

class unit:
	def __init__(self, config):
		self.config = config
		self.xPos = 0
		self.yPos = 0
		self.redraw = False

		#self.image = Image.new("RGBA", (200 , 200))
		#self.imageRotation = 0 #int(random.uniform(0,60))

		self.draw  = ImageDraw.Draw(config.image)

		self.fillColor = colorutils.getRandomRGB()
		self.outlineColor = colorutils.getRandomRGB()
		self.objWidth = 20
		self.speedRange = 1

		blueFactor  =  10
		self.redRange = [(250,0,blueFactor),(200,0,blueFactor),(150,0,blueFactor),(100,0,blueFactor),(50,0,blueFactor),(20,0,blueFactor)]
		self.brightness = 1
		self.fillColorMode = "random"
		self.lineColorMode = "red"
		self.changeColor = True

	def setUp(self, n = 0) :

		self.brightness *= self.config.brightness
		if(n!=0):
			n = int(math.floor(random.uniform(0,len(self.redRange))))
		self.fillColor = tuple(int(a*self.brightness) for a in (self.redRange[n]))
		self.outlineColor = tuple(int(a*self.brightness) for a in (self.redRange[n]))

		
	def update(self):
		self.changeColorFill()

	
	def render(self):

		xPosFinal = self.xPos
		yPosFinal = self.yPos

		self.draw.rectangle(((self.xPos, self.yPos), (self.xPos + self.blockLength, self.yPos + self.blockHeight))
			, fill=self.fillColor, outline=self.outlineColor)

		# rotate brush
		#img = self.image.rotate(self.imageRotation, expand=True)
		
		# paste into image that is final render
		#self.config.image.paste(img, (xPosFinal,yPosFinal), img)

	def changeColorFill(self):
		if(self.changeColor == True) :
			if(self.fillColorMode == "random") :
				self.fillColor = colorutils.randomColor(random.uniform(.01,self.brightness))
				if(self.lineColorMode == "red") :
					n = int(math.floor(random.uniform(0,len(self.redRange))))
					self.outlineColor = tuple(int(a*self.brightness) for a in (self.redRange[n]))
				else :	
					self.outlineColor = colorutils.getRandomRGB(random.uniform(.01,self.brightness))
			else:
				n = int(math.floor(random.uniform(0,len(self.redRange))))
				self.fillColor = tuple(int(a*self.brightness) for a in (self.redRange[n]))
				n = int(math.floor(random.uniform(0,len(self.redRange))))
				self.outlineColor = tuple(int(a*self.brightness) for a in (self.redRange[n]))


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def main(run = True) :
	global config, directionOrder,workConfig
	print("---------------------")
	print("QUILT Loaded")


	config.brightness = float(workConfig.get("displayconfig", 'brightness')) 
	colorutils.brightness = config.brightness
	config.canvasImageWidth = config.screenWidth
	config.canvasImageHeight = config.screenHeight
	config.canvasImageWidth -= 4
	config.canvasImageHeight -= 4


	try :
		config.numUnits = int(workConfig.get("quilt", 'numUnits')) 
		config.speedRange = int(workConfig.get("quilt", 'speedRange')) 
		config.blockLength = int(workConfig.get("quilt", 'blockLength')) 
		config.blockHeight = int(workConfig.get("quilt", 'blockHeight')) 
		config.blockRows = int(workConfig.get("quilt", 'blockRows')) 
		config.blockCols = int(workConfig.get("quilt", 'blockCols')) 
		config.cntrOffsetX = int(workConfig.get("quilt", 'cntrOffsetX')) 
		config.cntrOffsetY = int(workConfig.get("quilt", 'cntrOffsetY')) 
		config.delay = float(workConfig.get("quilt", 'delay')) 

	except Exception as e: 
		print (str(e))


	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

	config.canvasImage = Image.new("RGBA", (config.canvasImageWidth  , config.canvasImageHeight))

	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

	cntrOffset = [config.cntrOffsetX,config.cntrOffsetY]
	reds = [(255,0,0),(180,0,0),(120,0,0),(50,5,5),(100,20,20)]

	config.unitArrray = []

	for rows in range (0,config.blockRows) :
		for cols in range (0,config.blockCols) :
			delta = config.numUnits * config.blockHeight * 2 +  config.blockLength
			cntr = [rows * delta + cntrOffset[0], cols * delta + cntrOffset[1]]		

			obj = unit(config)
			obj.xPos = cntr[0]
			obj.yPos = cntr[1]
			obj.blockLength = config.blockLength
			obj.blockHeight = config.blockHeight
			obj.speedRange = config.speedRange
			obj.colorMode = "red"
			obj.brightness = 1.0
			obj.changeColor = False
			obj.setUp()
			config.unitArrray.append(obj)


			# RIGHT
			for i in range(0,config.numUnits):
				obj = unit(config)
				obj.xPos = cntr[0] - (i) * config.blockLength
				obj.yPos = cntr[1] - (i + 1) * config.blockLength
				obj.blockLength = config.blockLength * (i + 1) * 2
				obj.blockHeight = config.blockHeight
				obj.speedRange = config.speedRange
				obj.fillColorMode = "red"
				obj.brightness = .4
				obj.changeColor = True
				obj.setUp(-1)
				config.unitArrray.append(obj)

			# BOTTOM
			for i in range(0,config.numUnits):
				obj = unit(config)
				obj.xPos = cntr[0] + config.blockLength * (i + 1)
				obj.yPos = cntr[1] - (i ) * config.blockLength
				obj.blockLength = config.blockLength 
				obj.blockHeight = config.blockHeight * (i + 1) * 2
				obj.speedRange = config.speedRange
				obj.fillColorMode = "red"
				obj.brightness = .8
				obj.changeColor = True
				obj.setUp(-1)
				config.unitArrray.append(obj)

			# LEFT
			for i in range(0,config.numUnits):
				obj = unit(config)
				obj.xPos = cntr[0] - config.blockLength * (i + 1 )
				obj.yPos = cntr[1] + (i + 1) * config.blockLength
				obj.blockLength = config.blockLength * (i + 1) * 2
				obj.blockHeight = config.blockHeight
				obj.speedRange = config.speedRange
				obj.fillColorMode = "random"
				obj.brightness = .99
				obj.changeColor = True
				obj.setUp(-1)
				config.unitArrray.append(obj)

			# TOP
			for i in range(0,config.numUnits):
				obj = unit(config)
				obj.xPos = cntr[0] - config.blockLength * (i + 1)
				obj.yPos = cntr[1] - (i + 1) * config.blockLength
				obj.blockLength = config.blockLength 
				obj.blockHeight = config.blockHeight * (i + 1) * 2
				obj.speedRange = config.speedRange
				obj.fillColorMode = "random"
				obj.brightness = .4
				obj.changeColor = True
				obj.setUp(-1)
				config.unitArrray.append(obj)



	config.rectify = True

	setUp()

	if(run) : runWork()


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def setUp():
	global config
	pass



''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def runWork():
	global blocks, config, XOs
	#gc.enable()
	while True:
		iterate()
		time.sleep(config.delay)  

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def iterate() :
	global config

	## No trails 
	#config.draw.rectangle((0,0,config.screenWidth, config.screenHeight), fill=(0,0,0), outline=(0,0,0))


	for i in range(0,len(config.unitArrray)):
		obj = 	config.unitArrray[i]
		obj.update()
		obj.render()

	config.render(config.image, 0,0)
		


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def callBack() :
	global config, XOs
	return True

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
