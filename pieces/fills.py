# ################################################### #
import time
import random
import math
import PIL.Image
import colorsys
import sys
from PIL import Image, ImageDraw
from PIL import ImageFilter, ImageOps, ImageEnhance
from modules import colorutils



import cv2
import numpy as np



''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#make script to subtly shift blue color rectangles slowly
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
class Fill :

	width = 100
	height = 162
	rows  = 1
	cols = 1
	x = y = 0
	currentColor = [80,80,80]
	targetColor = [80,80,80]
	rangeOfVals = [50,80]
	rateOfChange = 0
	redRange = [0,60]
	greenRange = [60,120]
	blueRange = [190,300]
	speedFactor = 250


	hue = 120
	hueTarget = 220
	sat = .4
	val = .4
	hueRate = 0
	hueRateBase = 0
	

	import colorsys

	def __init__(self, config, x= 0 , y =0, width = 32, height = 32) :
		self.config = config
		self.x = x
		self.y = y
		self.height = height
		self.width = width
		#val = random.uniform(self.rangeOfVals[0], self.rangeOfVals[1])
		#self.currentColor = [val,val,val]
		self.speedFactor = self.config.speedFactor
		#self.currentColor = self.getRandomColorList()

	def getRandomColorList(self) :
		col = []
		col.append(random.uniform(self.redRange[0],self.redRange[1]))
		col.append(random.uniform(self.greenRange[0],self.greenRange[1]))
		col.append(random.uniform(self.blueRange[0],self.blueRange[1]))
		return col

	def random(self) :
		self.x  = random.random() *  self.config.screenWidth
		self.y  = random.random() *  self.config.screenHeight
		self.width = random.random() * 100 + 5
		self.height = random.random() * 100 + 5

	def make(self):

		rate = random.uniform(.05,.2) #/ self.speedFactor
		rangeOfSpread = 20
		self.hueTarget = random.uniform(self.config.targetHue-rangeOfSpread,self.config.targetHue+rangeOfSpread)
		self.delta = self.hueTarget - self.hue

		self.hueRateBase = rate * self.delta * .01
		self.hueRate = self.hueRateBase

		#print(self.hue, self.hueTarget, self.hueRate, self.delta)


	def update(self) :

		self.hue += self.hueRate
		self.delta = self.hueTarget - self.hue
		self.currentColor = list(colorutils.HSVToRGB(self.hue, self.sat, self.val))
		self.displayCurrentColor = tuple(int(i) for i in self.currentColor)
		self.config.draw.rectangle((self.x, self.y, self.width + self.x, self.height + self.y), fill = self.displayCurrentColor)

		if(abs(self.delta) <= 1) : 
			#self.hue = 0
			self.make()


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


def setColor(clr="blue", dominant=False) :
	print(clr)
	global config
	config.clr = clr
	if (clr == "red") :
		config.redRange = [config.redModel[0], config.redModel[1]] #if dominant == False else [10,10]
		config.greenRange = [config.redModel[2], config.redModel[3]]# if dominant == False else [0,0]
		config.blueRange = [config.redModel[4], config.redModel[5]] #if dominant == False else [0,0]
	if (clr == "green") :
		config.redRange = [config.greenModel[0], config.greenModel[1]] #if dominant == False else [10,10]
		config.greenRange = [config.greenModel[2], config.greenModel[3]]# if dominant == False else [8,8]
		config.blueRange = [config.greenModel[4], config.greenModel[5]] #if dominant == False else [0,0]
	if (clr == "blue") :
		config.redRange = [config.blueModel[0], config.blueModel[1]] #if dominant == False else [0,0]
		config.greenRange = [config.blueModel[2], config.blueModel[3]] #if dominant == False else [0,0]
		config.blueRange = [config.blueModel[4], config.blueModel[5]] #if dominant == False else [10,10]


def main(run = True) :
	global config

	config.redrawRate = float(workConfig.get("fills", 'redrawRate'))
	config.mode = (workConfig.get("fills", 'mode'))

	config.speedFactor = float(workConfig.get("fills", 'speedFactor'))
	config.blurLevel = int(workConfig.get("fills", 'blurLevel'))

	config.redModel = ((workConfig.get("fills", 'redModel')).split(','))
	config.redModel = map(lambda x: int(x), config.redModel)
	config.greenModel = ((workConfig.get("fills", 'greenModel')).split(','))
	config.greenModel = map(lambda x: int(x), config.greenModel)
	config.blueModel = ((workConfig.get("fills", 'blueModel')).split(','))
	config.blueModel = map(lambda x: int(x), config.blueModel)
	config.models =["red","green","blue"]
	config.clr = "blue"
	config.transitioning = False
	config.avgHue = 0
	config.targetHue = 220

	c = int(random.uniform(0, 3))
	c = 2
	setColor(config.models[c])

	# reseting render image size
	config.renderImage = Image.new("RGBA", (config.actualScreenWidth , 32))
	config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	config.draw  = ImageDraw.Draw(config.image)
	config.id = config.image.im.id

	config.fill = []

	rows = config.rows / 5
	cols = config.cols * 2

	colWidth = config.screenWidth / cols
	rowHeight = config.screenHeight / rows
	for col in range (0,cols) :
		for row in range (0,rows) :
			f  = Fill(config, col * colWidth, row * rowHeight, colWidth, rowHeight)
			f.make()
			config.fill.append(f)


	if(run) : runWork()

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def runWork():
	global config
	while True:
		iterate()
		time.sleep(config.redrawRate)


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def iterate() :
	global config

	config.draw.rectangle((0,0,config.screenWidth,config.screenHeight), fill=(0,0,0,100))
	numBlocks = len(config.fill)
	avgHue = 0
	for i in range (0,numBlocks) :
		config.fill[i].update()
		avgHue += config.fill[i].hue

	config.avgHue = avgHue / numBlocks



	config.draw.rectangle((0,0,config.screenWidth-1,config.screenHeight-1), outline=(0,0,0,100))

	im = config.image.filter(ImageFilter.GaussianBlur(config.blurLevel))

	config.render(im, 0, 0,config.screenWidth,config.screenHeight)

	var  = 10
	if (config.avgHue <= config.targetHue + var and config.avgHue >= config.targetHue - var) :
		
		#config.targetHue = int(round(random.uniform(0,359)))

		change = int(round(random.uniform(-60,60)))


		if(config.targetHue != 200) : 
			config.targetHue = 200
		else :
			config.targetHue = config.avgHue + change


		if(config.targetHue >= 360) :
			config.targetHue = config.targetHue - 360
		if(config.targetHue < 0) :
			config.targetHue = config.targetHue + 360

		print("new target", config.targetHue)
		for i in range (0,numBlocks) :
			config.fill[i].make()


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def callBack() :
	global config
	#animator()

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
