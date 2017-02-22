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
		self.redRange = self.config.redRange
		self.greenRange = self.config.greenRange
		self.blueRange = self.config.blueRange

		self.targetColor = tuple(int(i) for i in self.getRandomColorList())
		self.displayCurrentColor = tuple(int(i) for i in self.currentColor)
		
		rate = (.01 * random.random()) / self.speedFactor
		delta = tuple(self.targetColor[i] - self.currentColor[i] for i in range(0,3))
		self.rateOfChange = tuple(i * rate for i in delta)

		#rate = .01
		rate = random.uniform(.2,.5) #/ self.speedFactor
		delta = self.hueTarget - self.hue
		
		fx = 1 #math.exp(math.pow(deltaFromAvg/200,3))/1

		self.hueRateBase = rate * delta * .01
		self.hueRate = self.hueRateBase

		#print(delta,deltaFromAvg,fx,self.config.avgHue,self.hueRate)
		#print(self.hueRate)


	def update(self) :

		self.hue += self.hueRate


		deltaFromAvg = self.config.avgHue - self.hue
		if(abs(deltaFromAvg) > 120 and abs(self.hueRateBase) > .001) : 
			delta = self.hueTarget - self.hue
			self.hueRate = .02 * delta
		else :
			self.hueRate = self.hueRateBase

		#print(self.hue, self.hueRate, deltaFromAvg)

		if(self.hue >= 359 or self.hue <= 0 or abs(deltaFromAvg) >= 358) : 
			self.hue = 0
			self.make()

		#self.currentColor = colorutils.hsv_to_rgb(self.hue, self.sat, self.val)
		self.currentColor = list(colorutils.HSVToRGB(self.hue, self.sat, self.val))

		'''
		if(sum(self.displayCurrentColor) > 1000) :
			self.currentColor[0] = self.targetColor[0]
			self.currentColor[1] = self.targetColor[1]
			self.currentColor[2] = self.targetColor[2]

		if( self.displayCurrentColor[0] <= self.targetColor[0] and self.rateOfChange[0] < 0 ) or (self.displayCurrentColor[0] >= self.targetColor[0]  and  self.rateOfChange[0] > 0) or (self.displayCurrentColor[0] == self.targetColor[0]) :
			self.rateOfChange = (0,self.rateOfChange[1],self.rateOfChange[2])
			self.currentColor[0] = self.targetColor[0]

		if ( self.displayCurrentColor[1] <= self.targetColor[1] and self.rateOfChange[1] < 0 ) or (self.displayCurrentColor[1] >= self.targetColor[1]  and  self.rateOfChange[1] > 0) or (self.displayCurrentColor[1] == self.targetColor[1]) :
			self.rateOfChange = (self.rateOfChange[0],0,self.rateOfChange[2])
			self.currentColor[1] = self.targetColor[1]

		if ( self.displayCurrentColor[2] <= self.targetColor[0] and self.rateOfChange[2] < 0 ) or (self.displayCurrentColor[2] >= self.targetColor[2]  and  self.rateOfChange[2] > 0) or (self.displayCurrentColor[2] == self.targetColor[2]) :
			self.rateOfChange = (self.rateOfChange[0],self.rateOfChange[1],0)
			self.currentColor[2] = self.targetColor[2]

		'''
		self.displayCurrentColor = tuple(int(i) for i in self.currentColor)

		self.config.draw.rectangle((self.x, self.y, self.width + self.x, self.height + self.y), fill = self.displayCurrentColor)

		# ah, nifty Python tricks.....
		if(all(v == 0 for v in self.rateOfChange)) :
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

	#config.avgHue = avgHue / numBlocks

	

	im = config.image.filter(ImageFilter.GaussianBlur(config.blurLevel))
	#im2 = im.filter(ImageFilter.MinFilter(3))
	config.render(im, 0, 0,config.screenWidth,config.screenHeight)

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
