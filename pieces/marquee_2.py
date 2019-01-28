# ################################################### #
import time
import random
import math, sys
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageEnhance
from modules import colorutils, coloroverlay

class Marquee :

	pattern = []
	perimeter = []
	clrs = []
	p0 = []
	
	innerWidth = 0
	innerHeight = 0
	marqueeWidth = 0
	step = 1
	offset = 0

	reverse = False
	
	colOverlayA = coloroverlay.ColorOverlay()
	colOverlayB = coloroverlay.ColorOverlay()

	def __init__(self):
		self.p0 = []
		pass

	def setUp(self):
		pass

	## Creates a series of little boxes -- not efficient but useful if you wanted to make some kind of chasing
	## gradient marquee and better to get animation travel speed down as slow as possible

	def makeMarquee(self):

		o = 0
		self.perimeter = []
		self.stepSize = round(self.marqueeWidth/self.step)
		if self.stepSize == 0 : self.stepSize = 1
		self.stepSize = 1

		# Right
		for i in range (self.p0[1], self.p0[1] + self.innerHeight + o + self.marqueeWidth, self.stepSize) : 
			self.perimeter.append([self.p0[0] + self.innerWidth, i, self.marqueeWidth, self.stepSize])

		# Bottom
		for i in range (self.p0[0] + self.innerWidth - 1, self.p0[0] - 1, -self.stepSize) : 
			self.perimeter.append([i, self.p0[1] + self.innerHeight, self.stepSize, self.marqueeWidth])

		# Left
		for i in range (self.p0[1] + self.innerHeight + self.marqueeWidth - 2, self.p0[1] - o, -self.stepSize) : 
			self.perimeter.append([self.p0[0], i, self.marqueeWidth, self.stepSize])

		# Top
		for i in range (self.p0[0] + 0, self.p0[0] + self.innerWidth, 
			self.stepSize) : self.perimeter.append([i, self.p0[1], self.stepSize, self.marqueeWidth])


	def advance(self):
		l = len(self.pattern)


		patternA = self.pattern[0 : (l - self.offset)]
		patternB = self.pattern[(l - self.offset): l ]
		pattern = patternB + patternA
	
		count = 0

		perim = self.perimeter
		if(self.reverse == True ) : 
			perim = reversed(self.perimeter)


		try:

			for p in (perim ):
				if(pattern[count] == 1) :
					self.configDraw.rectangle((p[0], p[1], p[0] + p[2], p[1] + p[3]), 
						outline=None, fill=tuple(round(c) for c in self.colOverlayA.currentColor))
				else:
					self.configDraw.rectangle((p[0],p[1],p[0] + p[2], p[1] + p[3]), 
						outline=None, fill=tuple(round(c) for c in self.colOverlayB.currentColor))
				count += 1
				if(count >= len(pattern)) :
					count = 0
		except Exception as e :
			print(e)
			print(self.colOverlayA.currentColor, self.colOverlayB.currentColor)
			sys.exit()


		self.offset += 1
		if(self.offset >= len(pattern)) : 
			self.offset =  0 

		self.colOverlayA.stepTransition()
		self.colOverlayB.stepTransition()


def init() :
	global config

	config.draw.rectangle((0,0,config.screenWidth,config.screenHeight), fill=(0,0,0,255))
	config.bgColor = coloroverlay.ColorOverlay()
	config.bgColor.randomRange = (10.0,config.randomRange/2)



	## The pattern controls the dash size - each 1 or 0 represents the width of one small
	## building block for the two-color dash

	#pattern = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	#if(config.step > 2) : pattern = [1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0]
	#pattern = [1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0]
	#pattern = [1,1,1,0,0,0]
	#pattern = [1,0,1,0,0,1,0,0,1,0,1]
	

	pattern = []
	pattern.extend((1 for i in range(0,config.baseDashSize)))
	pattern.extend((0 for i in range(0,config.baseDashSize)))

	p0 = [config.imageXOffset,config.imageYOffset]
	marqueeWidth = config.marqueeWidth
	innerWidth = config.screenWidth - marqueeWidth
	innerHeight = config.screenHeight - marqueeWidth
	marqueeWidthPrev = marqueeWidth
	
	step = config.step
	decrement = config.decrement

	config.marquees = []

	for i in range (0, config.marqueeNum):
	
		clrs = [colorutils.randomColor(),colorutils.randomColorAlpha(255,255)]
		colOverlayA = coloroverlay.ColorOverlay()
		colOverlayB = coloroverlay.ColorOverlay()

		colOverlayA.randomRange = (10.0, config.randomRange)
		colOverlayB.randomRange = (10.0, config.randomRange)

		if (i != 0) : 
			marqueeWidth = marqueeWidthPrev - decrement

		if(marqueeWidth <= 2) : 
			marqueeWidth = 2

		if(innerWidth < 32 or i > 6) :
			step = 1

		mq = Marquee()
		mq.pattern = pattern
		mq.p0 = p0
		mq.innerWidth = innerWidth
		mq.innerHeight = innerHeight
		mq.marqueeWidth = marqueeWidth
		mq.step = step
		mq.clrs = clrs
		mq.colOverlayA = colOverlayA
		mq.colOverlayB = colOverlayB
		mq.configDraw = config.draw
		mq.reverse = True if(i%2 > 0 ) else False

		mq.makeMarquee()
		config.marquees.append(mq)

		p0[0] += (marqueeWidth + config.gap) 
		p0[1] += (marqueeWidth + config.gap) 
		marqueeWidthPrev = marqueeWidth

		# If this is 1 then offsets the gap...
		eveningGap = 2

		innerWidth = innerWidth - 2 * (marqueeWidth ) - config.gap * eveningGap + decrement
		innerHeight = innerHeight - 2 * (marqueeWidth ) - config.gap * eveningGap + decrement

		if (config.gap > 0) :
			innerWidth -=decrement
			innerHeight -=decrement

		if(marqueeWidth == 2) :
			innerWidth -=1
			innerHeight -=1

		if(len(pattern) >= 4 and random.random() > .1) :
			pattern = pattern[1:]
			pattern = pattern[0:len(pattern)-1]


def redraw():
	global config

	bgColor = tuple(round(c) for c in config.bgColor.currentColor)

	try :
		config.draw.rectangle((0,0,config.screenWidth,config.screenHeight), fill=bgColor)
		config.bgColor.stepTransition()
	except Exception as e :
		print (e)
		print(bgColor, config.bgColor.currentColor)
		sys.exit()

	mcount  = 0
	for mq in config.marquees :
		mq.advance()



def runWork():
	global config
	while True:
		iterate()
		time.sleep(config.redrawSpeed)


def iterate() :
	global config
	redraw()
	config.render(config.image, 0, 0, config.screenWidth, config.screenHeight)


def main(run = True) :
	global config
	config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	config.draw  = ImageDraw.Draw(config.image)
	config.redrawSpeed  = float(workConfig.get("marquee", 'redrawSpeed')) 
	config.randomRange  = float(workConfig.get("marquee", 'randomRange')) 
	config.marqueeWidth = int(workConfig.get("marquee", 'marqueeWidth'))
	config.baseDashSize = int(workConfig.get("marquee", 'baseDashSize'))
	config.gap = int(workConfig.get("marquee", 'gap'))
	config.step = int(workConfig.get("marquee", 'step'))
	config.decrement = int(workConfig.get("marquee", 'decrement'))
	config.marqueeNum = int(workConfig.get("marquee", 'marqueeNum'))
	colorutils.brightness =  float(workConfig.get("displayconfig", 'brightness')) 
	config.xOffset = 15

	init()
	
	if(run) : runWork()







#########

