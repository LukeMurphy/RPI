import math
import random
import threading
import time

from modules import colorutils
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps

class Director:
	"""docstring for Director"""

	slotRate = .5

	def __init__(self, config):
		super(Director, self).__init__()
		self.config = config
		self.tT = time.time()

	def checkTime(self):
		if (time.time() - self.tT) >= self.slotRate:
			self.tT = time.time()
			self.advance = True
		else:
			self.advance = False

	def next(self):

		self.checkTime()


class ParticleDot:
	def __init__(self):
		pass

	def setUp(self,p,n):
		# variation in initial velocity
		direction = 1 if p.directionProb < .5 else -1
		orbit = True if p.orbitProb > .5 else False
		fx = random.random() * p.fFactor + 1
		fy = random.random() * p.fFactor + 1
		vx = math.cos(p.angle * n) * fx * direction
		vy = math.sin(p.angle * n) * fy * direction
		r = int(random.uniform(0, 255) * p.brightness)
		g = int(random.uniform(0, 200) * p.brightness)
		b = int(random.uniform(0, 255) * p.brightness)
		radius = random.uniform(1,p.maxRadius)
		rSpeed = random.uniform(100,200)/radius/10.0

		xPos = p.x
		yPos = p.y
		angle = p.angle * n

		if direction == -1 :
			xPos = round(random.uniform(0, config.canvasWidth))
			yPos = round(random.uniform(0, config.canvasHeight))
			angle = math.atan2(yPos - p.y ,xPos - p.x)
			vx = math.cos(angle) * fx * direction
			vy = math.sin(angle) * fy * direction

		self.id = n
		self.xPos = xPos
		self.yPos = yPos
		self.vx = vx
		self.vy = vy
		self.clr = [r, g, b]
		self.done = 0
		self.angle = angle
		self.radius = radius
		self.rSpeed = rSpeed
		self.mode = 1
		self.gravity = random.uniform(0.51, 1.52)
		self.orbit = orbit


class Sparkles:
	def __init__(self, config):
		self.config = config
		self.x = 0
		self.y = 0
		self.particles = []
		self.done = False
		self.orientation = 1
		self.initXRange = [config.initXRangeMin, config.initXRangeMax]
		self.initYRange = [config.initYRangeMin, config.initYRangeMax]

	def setUp(self):


		self.directionProb = random.random()
		self.orbitProb = random.random()
		# Number of sparks
		self.p = int(5 + (random.uniform(config.minParticles, config.maxParticles)))
		self.angle = 2 * math.pi / self.p

		config.numberDone = round(self.p / 5)

		# Speed factor
		self.fFactor = int(random.uniform(1, 6))

		# initial center position
		self.x = round(random.uniform(self.initXRange[0], self.initXRange[1]))
		self.y = round(random.uniform(self.initYRange[0], self.initYRange[1]))
		'''
		if config.rotation != 0:
			approxVisibleArea = self.config.canvasWidth * 0.6
			ran = random.random() * approxVisibleArea
			ran = 64 + random.uniform(-96, 96)
			self.x = int(ran + self.config.canvasWidth / 2)
		'''

		# print (int(self.config.canvasWidth/2 + approxVisibleArea/2), self.x)

		self.brightness = self.config.brightness
		self.sparkleBrightness = self.config.brightness
		self.brightness = 0.9
		self.sparkleBrightness = 0.8

		# speed that each light fades to black / sparkle

		self.decr_r = round(random.uniform(.25, 1))
		self.decr_g = round(random.uniform(.5, 1))
		self.decr_b = round(random.uniform(.25, 1))

		# vertical deacelleration
		self.deacelleration = random.uniform(0.8, 0.99)

		# horizontal deacelleration
		self.deacellerationx = random.uniform(0.8, 0.95)

		# pseudo gravity deacelleration
		self.gravity = random.uniform(0.1, 1.52)

		dx = config.canvasWidth - self.x
		dy = config.canvasHeight - self.y
		self.maxRadius = math.sqrt( config.canvasWidth*config.canvasWidth + config.canvasHeight*config.canvasHeight) * 2.5

		for n in range(0, self.p):
			pDot = ParticleDot()
			pDot.setUp(self,n)
			self.particles.append(pDot)


	def move(self):
		"""
		if(self.traces == False) : self.config.matrix.Clear()
		"""
		sumOfDone = 0
		for q in range(0, self.p):
			sumOfDone += self.particles[q].done

		if sumOfDone >= self.p - config.numberDone:
			self.done = True

		if random.random() > 0.996 and self.config.sideWind == True:
			pass
			#config.vx = round(2 - random.random() * 4)
			# useSideWind = True

		for q in range(0, self.p):
			ref = self.particles[q]

			'''
			# deacelleration / damping
			ref.vx = ref.vx * self.deacellerationx
			ref.vy = ref.vy * self.deacelleration

			# pseudo gravity
			ref.vy = ref.vy + ref.gravity * math.sin(config.systemRotation * math.pi/180)  # self.gravity
			ref.vx = ref.vx + ref.gravity * math.cos(config.systemRotation * math.pi/180)  # self.gravity
			'''

			if ref.mode == 1 :
				ref.xPos += ref.vx
				ref.yPos += ref.vy

				dx = ref.xPos - self.x
				dy = ref.yPos - self.y

				r = round(math.sqrt(dx*dx + dy*dy))

				if r > ref.radius  and ref.orbit == True :
					#print(r, ref.radius)
					ref.mode = 0

			else :
				ref.xPos = self.x + ref.radius  * math.cos(ref.angle) * .2
				ref.yPos = self.y + ref.radius  * math.sin(ref.angle) * .2
				ref.angle += ref.rSpeed


			'''
			'''

			self.particles[q].clr[0] = self.particles[q].clr[0] - self.decr_r
			self.particles[q].clr[1] = self.particles[q].clr[1] - self.decr_g
			self.particles[q].clr[2] = self.particles[q].clr[2] - self.decr_b

			if self.particles[q].clr[0] <= 0:
				self.particles[q].clr[0] = 0
			if self.particles[q].clr[1] <= 0:
				self.particles[q].clr[1] = 0
			if self.particles[q].clr[2] <= 0:
				self.particles[q].clr[2] = 0

			r = self.particles[q].clr[0]
			g = self.particles[q].clr[1]
			b = self.particles[q].clr[2]

			sumOfClrs = (
				self.particles[q].clr[0]
				+ self.particles[q].clr[1]
				+ self.particles[q].clr[2]
			)

			'''
			# a pixel wind changes the cascade
			if self.config.sideWind and sumOfClrs > 100:
				config.vx = round(2 - random.random() * 4)
				ref.vx = config.vx
				self.deacellerationx = 0.75
			'''

			if sumOfClrs < 10 and random.random() > 0.95:
				self.config.traces = False

			# Sparkles!!
			if random.random() < 0.1:
				r = int(220 * self.sparkleBrightness)
				g = int(220 * self.sparkleBrightness)
				b = int(255 * self.sparkleBrightness)

			# if (q ==0) : print (particles[q]['c'][0])
			xDisplayPos = ref.xPos
			yDisplayPos = ref.yPos

			if (
				xDisplayPos < self.config.canvasWidth
				and xDisplayPos > 0
				and yDisplayPos > 0
				and yDisplayPos <= config.canvasHeight
			):
				try:
					config.image.putpixel((int(xDisplayPos), int(yDisplayPos)), (r, g, b))
				except Exception as e:
					print(str(e))

			'''
			'''
			if (
	
				xDisplayPos > config.canvasWidth
				or yDisplayPos > config.canvasHeight
				or yDisplayPos < 0
				or xDisplayPos < 0
			):
				ref.setUp(self, ref.id)


			if random.random() < .05 :
				ref.setUp(self, ref.id)


				#print(ref.xPos,ref.yPos,ref.done,ref.mode)



def drawElement():
	global config
	return True


def redraw():
	#
	global config


def changeColor():
	pass
	return True


def changeCall():
	pass
	return True


def runWork():
	global redrawSpeed
	global sprkl
	redrawSpeed = 0.02
	while True:
		config.directorController.checkTime()
		if config.directorController.advance == True:
			iterate()
		time.sleep(redrawSpeed)



def iterate():
	global config
	global sprkl
	config.vx = 0

	if random.random() > 0.995 and config.traces == True:
		config.sideWind = True

	# Fade out the sparkle

	config.draw.rectangle(
		(0, 0, config.canvasWidth, config.canvasHeight),
		fill=(config.bgColor[0],config.bgColor[1],config.bgColor[2], round(config.fadeRate)),
	)
	w = 190
	x0 = sprkl.x - w/2
	y0 = sprkl.y - w/2
	x1 = sprkl.x + w/2
	y1 = sprkl.y + w/2

	a = round(config.fadeRate + 90) if config.fadeRate > 90 else config.fadeRate

	config.draw.ellipse((x0,y0,x1,y1), fill =(4,4,10,round(a) ))



	w = 160
	x0 = sprkl.x - w/2
	y0 = sprkl.y - w/2
	x1 = sprkl.x + w/2
	y1 = sprkl.y + w/2

	a = round(config.fadeRate + 100) if config.fadeRate > 100 else config.fadeRate

	config.draw.ellipse((x0,y0,x1,y1), fill =(4,4,30,round(a) ))


	w = 130
	x0 = sprkl.x - w/2
	y0 = sprkl.y - w/2
	x1 = sprkl.x + w/2
	y1 = sprkl.y + w/2
	a = round(config.fadeRate + 120) if config.fadeRate > 120 else config.fadeRate

	config.draw.ellipse((x0,y0,x1,y1), fill =(4,4,20,round(a) ))

	w = 100
	x0 = sprkl.x - w/2
	y0 = sprkl.y - w/2
	x1 = sprkl.x + w/2
	y1 = sprkl.y + w/2
	a = round(config.fadeRate + 140) if config.fadeRate > 140 else config.fadeRate

	config.draw.ellipse((x0,y0,x1,y1), fill =(4,4,10,round(a) ))


	config.sideWind = False


	sprkl.move()

	config.fadeRate += config.fadeRateDelta
	if random.random() < .001 :
		print("now")
		#config.fadeRate = 250
		#config.fadeRateDelta = 0
		#config.draw.rectangle((0, 0, config.canvasWidth, config.canvasHeight),fill=(config.bgColor[0],config.bgColor[1],config.bgColor[2], 255))
		sprkl.setUp()



	if config.fadeRate > 255 :
		config.fadeRate = 30
		config.fadeRateDelta = random.uniform(.1,5) 
	config.render(config.image, 0, 0, config.canvasWidth, config.canvasHeight)


	# Done


def main(run=True):
	global config
	global redrawSpeed
	global sprkl

	config.traces = False
	config.sideWind = False

	config.minParticles = 2000
	config.maxParticles = 2000
	config.numberDone = 1

	config.initXRangeMin = 220
	config.initXRangeMax = 220
	config.initYRangeMin = 120
	config.initYRangeMax = 120

	config.action = "other"
	config.systemRotation = 200

	config.bgColor = [1, 1, 2]
	config.fadeRate = 90
	config.fadeRateDelta = 1.0

	config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.draw = ImageDraw.Draw(config.image)
	sprkl = Sparkles(config)
	sprkl.setUp()

		# managing speed of animation and framerate
	config.directorController = Director(config)
	config.directorController.slotRate  = .03

	if run:
		runWork()
