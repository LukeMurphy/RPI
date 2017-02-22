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


	hue = 0
	hueTarget = 359
	sat = 1
	val = 1
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

		rate = random.uniform(.1,.75) #/ self.speedFactor
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
	config.targetHue = 70

	c = int(random.uniform(0, 3))
	c = 2
	setColor(config.models[c])

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

	

	im = config.image.filter(ImageFilter.GaussianBlur(config.blurLevel))
	#im2 = im.filter(ImageFilter.MinFilter(3))
	config.render(im, 0, 0,config.screenWidth,config.screenHeight)


	if (config.avgHue <= config.targetHue + 1 and config.avgHue >= config.targetHue - 1) :
		config.targetHue = int(round(random.uniform(0,359)))
		print("new target", config.targetHue)
		for i in range (0,numBlocks) :
			config.fill[i].make()



	'''

	# Change dominant color
	if(random.random() < .0005 and config.fill[0].speedFactor != 20) :
		c = int(random.uniform(0, 3))
		if config.models[c] != config.clr :
			setColor(config.models[c], True)
			config.transitioning = True
			for i in range (0,numBlocks) :
				config.fill[i].speedFactor = 20
				config.fill[i].make()

	# After the transition is complete, normal slow variations
	if(config.fill[0].speedFactor == 20 and random.random() < .01 and config.transitioning == True) :
		setColor(config.clr)
		config.transitioning = False
		for i in range (0,numBlocks) :
			config.fill[i].speedFactor = config.speedFactor
			config.fill[i].make()
	'''

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def callBack() :
	global config
	#animator()

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
