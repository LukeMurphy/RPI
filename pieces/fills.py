# ################################################### #
import time
import random
import math
import PIL.Image
from PIL import Image, ImageDraw
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
	currentColor = [0,0,255,20]
	targetColor = [0,0,0,20]
	rateOfChange = 0

	def __init__(self, config) :
		self.config = config
		self.currentColor = [0,0,int(random.uniform(0,255)),20]
		self.x  = random.random() *  self.config.screenWidth
		self.y  = random.random() *  self.config.screenHeight
		self.width = random.random() * 100 + 5
		self.height = random.random() * 100 + 5


	def make(self):
		self.targetColor = [0,0,int(random.uniform(0,255)),int(random.uniform(0,255))]

		delta = self.targetColor[2] - self.currentColor[2]
		direction = -1 if delta < 0 else 1

		self.rateOfChange = direction * random.random()


	def update(self) :
		self.currentColor[2] = self.currentColor[2] + self.rateOfChange
		color  = tuple(int(i) for i in self.currentColor)
		self.config.draw.rectangle((self.x, self.y, self.width + self.x, self.height + self.y), fill = color)
		
		if(int(self.currentColor[2]) ==int(self.targetColor[2])) :
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

	for i in range (0,150) :
		f  = Fill(config)
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
	for i in range (0,150) :
		config.fill[i].update()
	config.render(config.image, 0, 0,config.screenWidth,config.screenHeight)

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def callBack() :
	global config
	#animator()

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
