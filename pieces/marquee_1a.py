# ################################################### #
import time
import random
import math
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageEnhance
from modules import colorutils, coloroverlay

class TimerObj:
	delay = 0
	t1 = 0
	t2 = 0
	done = True

	def __init__(self) :
		self.done =  False
		pass

	def setTimeOut(self, delay , callBack):
		self.callBack = callBack
		self.delay = delay
		self.t1 = time.time()
	
	def checkTime(self):
		self.t2 = time.time()
		if(self.t2 - self.t1 >= self.delay * 1 and self.done == False) :
			self.done = True
			self.t1 = time.time()
			self.callBack["func"]()

def makeMarqueeBar(p,w,h,mw,step=1):
	perimeter = []
	#mw=0
	o = 0
	for i in range (p[1] + 0, p[1] + h + o, step) : perimeter.append([p[0] + w, i])
	return (perimeter)

def init() :
	global config
	config.timerArray = [] 
	config.tmr = TimerObj()
	config.tmr.setTimeOut(2.0, {"func":changeRotation})

	config.draw.rectangle((0,0,config.screenWidth,config.screenHeight), fill=(0,0,0,255))

	config.bgColor = coloroverlay.ColorOverlay()
	config.bgColor.randomRange = (10.0,config.randomRange/2)
	config.marquees = []

	marqueeWidth = config.marqueeWidth
	w = config.screenWidth - marqueeWidth
	h = config.screenHeight - marqueeWidth
	pattern = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	if(config.step > 2) : pattern = [1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0]
	#pattern = [1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0]
	#pattern = [1,1,1,0,0,0]
	p0 = [0,0]
	innerWidth = w
	innerHeight = h
	gap = config.gap 
	step = config.step
	decrement = config.decrement
	mw = marqueeWidth
	mwPrev = marqueeWidth

	for i in range (0, config.marqueeNum):
		clrs = [colorutils.randomColor(),colorutils.getRandomRGB()]
		colOverlayA = coloroverlay.ColorOverlay()
		colOverlayB = coloroverlay.ColorOverlay()

		colOverlayA.randomRange = (10.0, config.randomRange)
		colOverlayB.randomRange = (10.0, config.randomRange)

		#if(i%2 == 0) : mw = mwPrev - decrement

		if (i != 0) : mw = mwPrev - decrement
		if(mw <= 2) : mw = 2

		#print(i, p0, mw, mwPrev, innerWidth, innerHeight)

		if(innerWidth < 32 or i > 6) :
			step = 1

		config.marquees.append([
			0, 
			pattern, 
			makeMarqueeBar(
				(p0[0], 0),
				innerWidth , h, config.marqueeWidth, step
				), 
			config.marqueeWidth, 
			clrs,
			colOverlayA,
			colOverlayB
			 ])

		#print (config.marquees[i][2])

		p0[0] += (mw + gap) 
		p0[1] += (mw + gap) 
		mwPrev = mw

		innerWidth = innerWidth - 2 * (mw ) - gap + decrement
		innerHeight = innerHeight - 2 * (mw ) - gap + decrement


		if(len(pattern) >= 3 ) :
			pattern = pattern[1:]
			pattern = pattern[0:len(pattern)-1]

def changeRotation():
	config.rotation +=90
	if config.rotation > 1000 :
		config.rotation = config.rotationOrig

def redraw():
	global config

	if (config.tmr.done == True) : 
		config.tmr = TimerObj()
		config.tmr.setTimeOut(random.uniform(1,12), {"func":changeRotation})

	bgColor = tuple(int(c) for c in config.bgColor.currentColor)
	config.draw.rectangle((0,0,config.screenWidth,config.screenHeight), fill=bgColor)
	config.bgColor.stepTransition()

	mcount  = 0
	for m in config.marquees :

		offset = m[0]
		pattern = m[1]
		perimeter = m[2]
		marqueeWidth = m[3]
		l = len(pattern)

		patternA = pattern[0 : (l - offset)]
		patternB = pattern[(l - offset): l ]
		pattern = patternB + patternA
		
		colOverlayA = m[5]
		colOverlayB = m[6]

		clrA = colOverlayA.currentColor
		clrB = colOverlayB.currentColor

		count = 0

		perim = perimeter
		#if(mcount%2 > 0 and random.random() > .002) : perim = reversed(perimeter)
		if(mcount%2 > 0 ) : perim = reversed(perimeter)


		for p in (perim ):
			if(pattern[count] == 1) :
				config.draw.rectangle((p[0],p[1], p[0] + config.marqueeWidth - 1, p[1] + config.marqueeWidth - 1), outline=None, fill=tuple(int(c) for c in clrA))
			else:
				config.draw.rectangle((p[0],p[1], p[0] + config.marqueeWidth - 1, p[1] + config.marqueeWidth - 1), outline=None, fill=tuple(int(c) for c in clrB))
			count += 1
			if(count >= len(pattern)) :
				count = 0

		m[0] += 1
		if(m[0] >= len(pattern)) : m[0] =  0 
		mcount += 1

		colOverlayA.stepTransition()
		colOverlayB.stepTransition()

def runWork():
	global config
	while True:
		iterate()
		time.sleep(config.redrawSpeed)

def iterate() :
	global config
	config.tmr.checkTime()
	redraw()
	config.render(config.image, 0, 0, config.screenWidth, config.screenHeight)

def main(run = True) :
	global config
	config.rotationOrig = config.rotation
	config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	config.draw  = ImageDraw.Draw(config.image)
	config.redrawSpeed  = float(workConfig.get("marquee", 'redrawSpeed')) 
	config.randomRange  = float(workConfig.get("marquee", 'randomRange')) 
	config.marqueeWidth = int(workConfig.get("marquee", 'marqueeWidth'))
	config.gap = int(workConfig.get("marquee", 'gap'))
	config.step = int(workConfig.get("marquee", 'step'))
	config.decrement = int(workConfig.get("marquee", 'decrement'))
	config.marqueeNum = int(workConfig.get("marquee", 'marqueeNum'))
	config.clr = colorutils.randomColor(1)
	colorutils.brightness =  float(workConfig.get("displayconfig", 'brightness')) 
	config.xOffset = 15

	init()
	
	if(run) : runWork()
