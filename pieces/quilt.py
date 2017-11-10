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

		self.image = Image.new("RGBA", (200 , 200))
		self.imageRotation = 0 #int(random.uniform(0,60))
		self.draw  = ImageDraw.Draw(config.image)

		self.fillColor = colorutils.getRandomRGB()
		self.outlineColor = colorutils.getRandomRGB()
		self.objWidth = 20
		self.changeColor = True
		self.speedRange = 1

	def update(self):
		pass
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
			self.fillColor = colorutils.randomColor(random.uniform(.2,config.brightness))
			self.outlineColor = colorutils.getRandomRGB(random.uniform(.2,config.brightness))


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def main(run = True) :
	global config, directionOrder,workConfig
	print("---------------------")
	print("QUILT Loaded")
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
		config.delay = float(workConfig.get("quilt", 'delay')) 

	except Exception as e: 
		print (str(e))


	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

	config.canvasImage = Image.new("RGBA", (config.canvasImageWidth  , config.canvasImageHeight))

	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

	cntr = [0,0]

	config.unitArrray = []

	for rows in range (0,6) :
		for cols in range (0,6) :
			delta = config.numUnits * config.blockHeight * 2
			cntr = [rows * delta, cols * delta]		

			obj = unit(config)
			obj.xPos = cntr[0]
			obj.yPos = cntr[1]
			obj.blockLength = config.blockLength
			obj.blockHeight = config.blockHeight
			obj.speedRange = config.speedRange
			obj.fillColor = (255,0,0)
			obj.outlineColor = (100,100,0)
			obj.changeColor = False
			config.unitArrray.append(obj)

			for i in range(0,config.numUnits):
				obj = unit(config)
				obj.xPos = cntr[0] - (i) * config.blockLength
				obj.yPos = cntr[1] - (i + 1) * config.blockLength
				obj.blockLength = config.blockLength * (i + 1) * 2
				obj.blockHeight = config.blockHeight
				obj.speedRange = config.speedRange
				obj.fillColor = (150,0,0)
				obj.outlineColor = (100,0,0)
				obj.changeColor = False
				config.unitArrray.append(obj)

			for i in range(0,config.numUnits):
				obj = unit(config)
				obj.xPos = cntr[0] + config.blockLength * (i + 1)
				obj.yPos = cntr[1] - (i ) * config.blockLength
				obj.blockLength = config.blockLength 
				obj.blockHeight = config.blockHeight * (i + 1) * 2
				obj.speedRange = config.speedRange
				obj.fillColor = (120,0,0)
				obj.outlineColor = (100,0,0)
				obj.changeColor = False
				config.unitArrray.append(obj)

			for i in range(0,config.numUnits):
				obj = unit(config)
				obj.xPos = cntr[0] - config.blockLength * (i + 1 )
				obj.yPos = cntr[1] + (i + 1) * config.blockLength
				obj.blockLength = config.blockLength * (i + 1) * 2
				obj.blockHeight = config.blockHeight
				obj.speedRange = config.speedRange
				#obj.fillColor = (200,0,0)
				obj.outlineColor = (100,0,0)
				config.unitArrray.append(obj)

			for i in range(0,config.numUnits):
				obj = unit(config)
				obj.xPos = cntr[0] - config.blockLength * (i + 1)
				obj.yPos = cntr[1] - (i + 1) * config.blockLength
				obj.blockLength = config.blockLength 
				obj.blockHeight = config.blockHeight * (i + 1) * 2
				obj.speedRange = config.speedRange
				obj.outlineColor = (100,0,0)
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
