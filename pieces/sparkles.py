import time
import random
import math
import threading
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageEnhance
from modules import colorutils

traces = False

class Sparkles :


	def __init__(self, config):
		self.config = config
		self.x = 0
		self.y = 0
		self.particles = []
		self.done = False

		# Number of sparks
		self.p = int(50 + (random.uniform(20,190)))
		self.angle = 2 * math.pi/self.p

		# initial center position
		self.x = int(random.random()*self.config.screenWidth)
		self.y = int(random.random()*16)

		self.brightness = self.config.brightness
		self.sparkleBrightness = self.config.brightness
		self.brightness = .9
		self.sparkleBrightness = .8

		self.decr = 20
		self.decr = int(random.uniform(1,10))  
		self.deacelleration = random.uniform(.9,.999)
		self.gravity = random.uniform(.03,.1)

	def explosion(self):
		for n in range (0, self.p) :
			# variation in initial velocity
			f = random.random() * 4
			vx = math.cos(self.angle * n) * f
			vy = math.sin(self.angle * n) * f
			r = int(random.uniform(0,255)* self.brightness)
			g = int(random.uniform(0,255)* self.brightness)
			b = int(random.uniform(0,255)* self.brightness)
			self.particles.append({'id':n,'xpos':self.x,'ypos':self.y,'vx':vx,'vy':vy, 'c':[r,g,b], 'd':0})
		
		'''
		if(self.traces == False) : self.config.matrix.Clear()
		'''

		sumOfDone = 0  
		for q in range (0, self.p) :
			sumOfDone += self.particles[q]['d'] 

		if(sumOfDone >= self.p-1) :
			self.done = True

		for q in range (0, self.p) :
			ref = self.particles[q]
			ref['xpos'] = ref['vx'] + ref['xpos']
			ref['ypos'] = ref['vy'] + ref['ypos']

			# deacelleration
			ref['vy'] = ref['vy'] * self.deacelleration
			ref['vx'] = ref['vx'] * .9

			# pseudo gravity
			ref['vy'] = ref['vy'] + self.gravity

			self.particles[q]['c'][0] = self.particles[q]['c'][0] - self.decr
			self.particles[q]['c'][1] = self.particles[q]['c'][1] - self.decr
			self.particles[q]['c'][2] = self.particles[q]['c'][2] - self.decr

			if(self.particles[q]['c'][0] <= 0) : self.particles[q]['c'][0] = 0
			if(self.particles[q]['c'][1] <= 0) : self.particles[q]['c'][1] = 0
			if(self.particles[q]['c'][2] <= 0) : self.particles[q]['c'][2] = 0

			r = self.particles[q]['c'][0]
			g = self.particles[q]['c'][1]
			b = self.particles[q]['c'][2]

			# Sparkles!!
			if(random.random() > .9) :
				r = int(220 * self.sparkleBrightness)
				g = int(220 * self.sparkleBrightness)
				b = int(255 * self.sparkleBrightness)

			#if (q ==0) : print (particles[q]['c'][0])
			xDisplayPos = ref['xpos']
			yDisplayPos = ref['ypos']

			if(xDisplayPos <= self.config.screenWidth and xDisplayPos >= 0 and yDisplayPos >= 0 and yDisplayPos <= config.screenHeight) :
				config.image.putpixel((int(xDisplayPos),int(yDisplayPos)), (r,g,b))
			if(xDisplayPos < 0 or xDisplayPos > config.screenWidth or yDisplayPos > config.screenHeight) :
				self.particles[q]['d'] = 1




def drawElement() :
	global config
	return True

def redraw():
	global config

def changeColor() :
	pass
	return True

def changeCall() :
	pass
	return True

def callBack() :
	global config, sprkl, traces
	if(random.random() > .986) : traces = True
	#if(random.random() > .99) : traces = False
	if (sprkl.done == True) :
		sprkl = Sparkles(config)
		traces = False


def runWork():
	global redrawSpeed
	global sprkl
	redrawSpeed = .01
	while True:
		iterate()
		time.sleep(redrawSpeed)

def setUpDelays() :
	global config


def iterate() :
	global config
	global sprkl, traces
	if(traces != True) : config.draw.rectangle((0,0,config.screenWidth,config.screenHeight), fill=0)
	sprkl.explosion()
	config.render(config.image, 0, 0, config.screenWidth, config.screenHeight)
	callBack()
	count = 0
	# Done

def main(run = True) :
	global config
	global redrawSpeed
	global sprkl

	config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	config.draw  = ImageDraw.Draw(config.image)
	sprkl = Sparkles(config)

	if(run) : runWork()
