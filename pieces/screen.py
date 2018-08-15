import time
import random
import math
import datetime
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageEnhance, ImageChops
from modules import colorutils, coloroverlay
import argparse


class Crack:

	origin = [0,0]
	pointsCount = 5
	points = []
	yVarMin = 1
	yVarMax = 10

	def __init__(self, config):
		self.config = config
		self.fillColor = colorutils.getRandomRGB()
		self.crackColor = (200,200,200,100)


	def setUp(self):
		self.crackColor = self.config.bgColor

		# Draw from the origin
		lastPoint = self.origin
		self.points = []
		self.slopes = []
		self.points.append([self.origin[0],self.origin[1]])

		xRange = self.config.canvasWidth/self.pointsCount

		a = 0
		slope = 0

		for i in range (0, self.pointsCount):
			x = round(self.origin[0] + xRange * i - round(random.uniform(-xRange/2,xRange/2)))
			y = round(self.origin[1] + round(random.uniform(self.yVarMin * (i+1), self.yVarMax * (i +1))))

			if x < 0 :
				x = 0

			self.points.append([x,y])

			dx = lastPoint[0] - x
			dy = lastPoint[1] - y

			if dx != 0 :
				slope = dy/dx
			else :
				slope = 0

			self.slopes.append(slope)

			lastPoint[0] = x
			lastPoint[1] = y

		#print (self.points)
			
	
	def render(self):
		for i in range (0, self.pointsCount - 1):
			self.config.canvasDraw.line((self.points[i][0], self.points[i][1], self.points[i+1][0], self.points[i+1][1] ), fill=self.crackColor)


def showGrid():
	global config


	config.colOverlay.stepTransition()
	config.bgColor  = tuple(int(a*config.brightness) for a in (config.colOverlay.currentColor))

	if random.random() < .000001 :
		config.draw.rectangle((0,0,config.screenWidth, config.screenHeight), fill=config.bgColor, outline=(0,0,0))
	
	for row in range (0, config.rows) :
		for col in range (0, config.cols) :
			xPos = col * config.tileSizeWidth 
			yPos = row * config.tileSizeHeight
			#config.canvasDraw.rectangle((xPos,yPos,xPos + config.tileSizeWidth - 1, yPos +  config.tileSizeHeight -1), fill=config.bgColor, outline=config.outlineColor)
			config.canvasDraw.rectangle((xPos,yPos,xPos + config.tileSizeWidth - 1, yPos +  config.tileSizeHeight -1), fill=config.bgColor, outline=None)
			

	config.sampleVariationX = 5
	config.sampleVariationY = 0
	for i in range(0, len(config.crackArray)):
		config.crackArray[i].render()

		## Draw vertical lines from one line to the next
		if i < len(config.crackArray) - 1 :
			for p in range(0, config.pointsCount-1):
				startX = config.crackArray[i].points[p][0]
				endX = config.crackArray[i].points[p+1][0]
				aVal =  0
				#config.canvasDraw.line((startX, 0, startX, config.crackArray[i].points[p][1]), fill=(0, 0, 200,200))
				for x in range( startX, endX, 1) :
					y =  (x - startX) * config.crackArray[i].slopes[p] + config.crackArray[i].points[p][1]
					y2 =  (x - startX) * config.crackArray[i+1].slopes[p] + config.crackArray[i+1].points[p][1]
					#config.canvasDraw.rectangle((x, y, x+1, y+1), fill=(200, 0, 0))
					#y2 = config.crackArray[i].points[p][1]
					if i > 0 and random.random() < .5:
						xSample = x - round(random.uniform(-config.sampleVariationX ,config.sampleVariationX ))
						ySample = y - round(random.uniform(-config.sampleVariationY ,config.sampleVariationY ))
						if xSample < 0 : xSample = 0
						if xSample > config.canvasWidth : xSample = config.canvasWidth 
						if ySample < 0 : ySample = 0
						if ySample > config.canvasHeight : ySample = config.canvasHeight

						samplePoint = ( xSample, ySample )
						# Just make sure the sample point is actually within the bounds of the image
						if(samplePoint[0] < config.canvasWidth and samplePoint[1] < config.canvasHeight and samplePoint[0] > 0 and samplePoint[1] > 0):
							colorSample = config.canvasImage.getpixel(samplePoint)

							#randomize brightness a little
							colorSampleColor = tuple(int(round(c * random.uniform(.1,1))) for c in colorSample)

							# Once in a little while, the color is just random
							if(random.random() < config.randomColorSampleProb) : 
								colorSampleColor = colorutils.getRandomRGB(random.random())

							config.canvasDraw.line((x, y, x, y2), fill=colorSampleColor)


	
	config.image.paste(config.canvasImage, (config.imageXOffset, config.imageYOffset), config.canvasImage)
	config.render(config.image, 0,0)



def main(run = True) :
	global config, directionOrder
	print("---------------------")
	print("Diag Loaded")

	colorutils.brightness = config.brightness
	

	try:
		config.imageXOffset = int(workConfig.get("displayconfig","imageXOffset"))
	except Exception as e:
		print (str(e))
		config.imageXOffset = 0
	
	config.outlineColorVals = ((workConfig.get("screenproject", 'outlineColor')).split(','))
	config.outlineColor = tuple(map(lambda x: int(int(x) * config.brightness) , config.outlineColorVals))	
	config.bgColorVals = ((workConfig.get("screenproject", 'bgColor')).split(','))
	config.bgColor = tuple(map(lambda x: int(int(x) * config.brightness) , config.bgColorVals))	
	config.crackColorVals = ((workConfig.get("screenproject", 'crackColor')).split(','))
	config.crackColor = tuple(map(lambda x: int(int(x) * config.brightness) , config.crackColorVals))
	
	config.tileSizeWidth = int(workConfig.get("displayconfig", 'tileSizeWidth'))
	config.tileSizeHeight = int(workConfig.get("displayconfig", 'tileSizeHeight'))
	config.delay = float(workConfig.get("screenproject", 'delay'))
	
	config.numCracks = int(workConfig.get("screenproject", 'numCracks'))
	config.pointsCount = int(workConfig.get("screenproject", 'pointsCount'))

	config.randomColorSampleProb = float(workConfig.get("screenproject", 'randomColorSampleProb'))
	config.yVarMin = int(workConfig.get("screenproject", 'yVarMin'))
	config.yVarMax = int(workConfig.get("screenproject", 'yVarMax'))

	config.tLimitBase = int(workConfig.get("screenproject", 'tLimitBase'))
	config.timeTrigger = (workConfig.getboolean("screenproject", 'timeTrigger'))




	config.image = Image.new("RGBA", (config.screenWidth  , config.screenHeight))
	config.draw = ImageDraw.Draw(config.image)
	config.canvasImage = Image.new("RGBA", (config.canvasWidth  , config.canvasHeight))
	config.canvasDraw = ImageDraw.Draw(config.canvasImage)


	config.colOverlay = coloroverlay.ColorOverlay()
	config.colOverlay.randomSteps = False 
	config.colOverlay.timeTrigger = True 
	config.colOverlay.tLimitBase = config.tLimitBase 
	config.colOverlay.maxBrightness = config.brightness
	config.colOverlay.steps = 100

	config.crackArray = []
	for i in range(0,config.numCracks):
		obj = Crack(config)
		obj.origin = [config.canvasWidth, config.canvasHeight]
		obj.origin = [0,0]
		obj.pointsCount = config.pointsCount
		obj.crackColor = config.crackColor
		obj.yVarMin = config.yVarMin
		obj.yVarMax = config.yVarMax
		obj.setUp()
		config.crackArray.append(obj)

	setUp()

	if(run) : runWork()


def setUp():
	global config


def runWork():
	global config
	while True:
		iterate()
		time.sleep(config.delay)  


def iterate() :
	global config
	showGrid()


	if random.random() < .01 :
		c = math.floor(random.uniform(0,len(config.crackArray)))
		#print (c,len(config.crackArray))
		config.crackArray[c].origin = [0,0]
		config.crackArray[c].setUp()


def callBack() :
	global config
	return True




''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


	




