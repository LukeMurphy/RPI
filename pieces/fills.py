# ################################################### #
import time
import random
import math
import PIL.Image
from PIL import Image, ImageDraw
from PIL import ImageFilter, ImageOps, ImageEnhance

import sys
from modules import colorutils

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#make script to subtly shift blue color rectangles slowly
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
class Fill :

	width = 100
	height = 162
	rows  = 1
	cols = 1
	lineWidth = 1
	x = y = 0
	currentColor = [0,0,0]
	targetColor = [0,0,0]
	rateOfChange = 0
	rangeOfVals = [50,80]
	redRange = [10,50]
	greenRange = [10,20]
	blueRange = [50,60]
	speedFactor = 250

	def __init__(self, config, x= 0 , y =0, width = 32, height = 32) :
		self.config = config
		self.x = x
		self.y = y
		self.height = height
		self.width = width
		val = random.uniform(self.rangeOfVals[0], self.rangeOfVals[1])
		self.currentColor = [val,val,val]


		self.currentColor = self.getRandomColorList()

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
		val = random.uniform(self.rangeOfVals[0], self.rangeOfVals[1])
		self.targetColor = [val,val,val]
		self.targetColor = self.getRandomColorList()
		
		self.displayTargetColor = tuple(int(i) for i in self.targetColor)
		self.displayCurrentColor = tuple(int(i) for i in self.currentColor)
		
		rate = random.random()/self.speedFactor
		delta = tuple(self.targetColor[i] - self.currentColor[i] for i in range(0,3))
		self.rateOfChange = tuple(i * rate for i in delta)


	def update(self) :
		color = []
		for i in range(0,3):
			color.append(self.currentColor[i] + self.rateOfChange[i]) 

		self.currentColor = color
		self.displayCurrentColor = tuple(int(i) for i in self.currentColor)
		self.config.draw.rectangle((self.x, self.y, self.width + self.x, self.height + self.y), fill = self.displayCurrentColor)
		
		if(self.displayCurrentColor == self.displayTargetColor or self.displayCurrentColor >= (255,255,255) or self.displayCurrentColor <= (0,0,0)) :
			#print("*************")
			self.make()



''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


def main(run = True) :
	global config
	config.lineWidth = int(workConfig.get("fills", 'lineWidth'))
	config.pulseSpeed = float(workConfig.get("fills", 'pulseSpeed'))
	config.mode = (workConfig.get("fills", 'mode'))
	config.countLimit = int(workConfig.get("fills", 'countLimit'))


	# reseting render image size
	config.renderImage = Image.new("RGBA", (config.actualScreenWidth , 32))
	config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	config.draw  = ImageDraw.Draw(config.image)
	config.id = config.image.im.id


	config.fill = []

	for col in range (0,config.cols) :
		for row in range (0,config.rows) :
			f  = Fill(config, col * 32, row * 32)
			f.make()
			config.fill.append(f)


	if(run) : runWork()

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def runWork():
	global config
	while True:
		iterate()
		time.sleep(config.pulseSpeed)


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def iterate() :
	global config

	config.draw.rectangle((0,0,config.screenWidth,config.screenHeight), fill=(0,0,0,100))
	numBlocks = len(config.fill)
	for i in range (0,numBlocks) :
		config.fill[i].update()

	im = config.image.filter(ImageFilter.GaussianBlur(12))
	#im2 = im.filter(ImageFilter.MinFilter(3))
	config.render(im, 0, 0,config.screenWidth,config.screenHeight)


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def callBack() :
	global config
	#animator()

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
