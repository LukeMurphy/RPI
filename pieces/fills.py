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
	currentColor = [80,80,80,255]
	targetColor = [80,80,80,255]
	rangeOfVals = [50,80]
	rateOfChange = 0

	hue = 200
	hueBase = 240
	hueTarget = 240
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
		self.val = self.config.value
		self.sat = self.config.saturation
		self.rangeOfSpread = self.config.rangeOfSpread
		self.rateOfChange = self.config.rateOfChange
		self.hueBase = self.config.hueBase

	def random(self) :
		self.x  = random.random() *  self.config.screenWidth
		self.y  = random.random() *  self.config.screenHeight
		self.width = random.random() * 100 + 5
		self.height = random.random() * 100 + 5

	def make(self):

		rate = random.uniform(self.rateOfChange[0]/1000,self.rateOfChange[1]/1000) 
		self.hueTarget = random.uniform( (self.config.targetHue - self.rangeOfSpread) , (self.config.targetHue + self.rangeOfSpread))

		if(self.hueTarget > 360) : self.hueTarget -= 360
		if(self.hueTarget < 0) : self.hueTarget += 360

		self.delta = self.hueTarget - self.hue

		if (self.delta > 180 ) : self.delta -= 360
		if (self.delta < -180 ) : self.delta += 360

		self.hueRateBase = rate * self.delta
		self.hueRate = self.hueRateBase

		#print(self.config.targetHue, self.rangeOfSpread)
		#print(self.hue, self.hueTarget , self.hueRate)

	def update(self) :

		self.hue += self.hueRate

		if (self.hue > 360) :
			self.hue = 0
		if(self.hue < 0) :
			self.hue = 360

		self.delta = self.hueTarget - self.hue

		# Hue, Saturation, Value
		#self.currentColor = list(colorutils.HSVToRGB(self.hue, self.sat, self.val))

		# Hue, Chroma, Luma
		self.currentColor = list(colorutils.HCLToRGB(self.hue, self.sat, self.val))
		self.displayCurrentColor = tuple(int(i) for i in self.currentColor)
		self.config.draw.rectangle((self.x, self.y, self.width + self.x, self.height + self.y), fill = self.displayCurrentColor)

		if(abs(self.delta) <= 1) : 
			#self.hue = 0
			self.make()


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


def main(run = True) :
	global config

	config.redrawRate = float(workConfig.get("fills", 'redrawRate'))
	config.saturation = float(workConfig.get("fills", 'saturation'))
	config.value = float(workConfig.get("fills", 'value'))
	config.blurLevel = int(workConfig.get("fills", 'blurLevel'))
	config.FillRows = int(workConfig.get("fills", 'FillRows'))
	config.FillCols = int(workConfig.get("fills", 'FillCols'))
	config.hueBase = int(workConfig.get("fills", 'hueBase'))
	config.rangeOfSpread = int(workConfig.get("fills", 'rangeOfSpread'))
	config.vval = int(workConfig.get("fills", 'vval'))
	config.rateOfChange = (workConfig.get("fills", 'rateOfChange').split(","))
	config.rateOfChange = [float(i) for i in config.rateOfChange]
	config.vignette = (workConfig.getboolean("fills", 'vignette'))
	config.crossbar = (workConfig.getboolean("fills", 'crossbar'))

	config.transitioning = False
	config.avgHue = 0
	config.targetHue = 230

	# reseting render image size
	config.renderImage = Image.new("RGBA", (config.actualScreenWidth , 32))
	config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	config.draw  = ImageDraw.Draw(config.image)
	config.id = config.image.im.id
	config.fill = []

	## Set up the grid
	rows = config.FillRows
	cols = config.FillCols

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

	# Clear out the image -- not really necessary tho
	config.draw.rectangle((0,0,config.screenWidth,config.screenHeight), fill=(0,0,0,255))

	# run throught the blocks, update and get average hue
	numBlocks = len(config.fill)
	avgHue = 0
	for i in range (0,numBlocks) :
		config.fill[i].update()
		avgHue += config.fill[i].hue
	config.avgHue = avgHue / numBlocks

	# draw the "vignette"
	if(config.vignette) :
		config.draw.rectangle((0, 0, config.screenWidth-1, config.screenHeight-1), outline=(config.vval,config.vval,config.vval,100))
	if(config.crossbar) :
		config.draw.rectangle((config.screenWidth/2, 0, config.screenWidth/2 + 2, config.screenHeight), fill=(config.vval,config.vval,config.vval,100))

	# Do the blur
	im = config.image.filter(ImageFilter.GaussianBlur(config.blurLevel))

	# Render the image to the screen
	config.render(im, 0, 0,config.screenWidth,config.screenHeight)

	# Decide if the primary target color should shift
	var  = 1
	if (config.avgHue <= config.targetHue + var and config.avgHue >= config.targetHue - var) :
		
		change = int(round(random.uniform(-180,180)))

		'''
		if(config.targetHue != config.hueBase) : 
			config.targetHue = config.hueBase
		else :
			config.targetHue = config.avgHue + change
		'''

		config.targetHue = round(config.avgHue + change)

		# the randge has to be 0 - 360
		if(config.targetHue > 360) :
			config.targetHue = config.targetHue - 360
		if(config.targetHue < 0) :
			config.targetHue = config.targetHue + 360

		print("new target", config.targetHue)

		# Update all the blocks with their new "target hue"
		for i in range (0,numBlocks) :
			config.fill[i].make()


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def callBack() :
	global config
	#animator()

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
