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

		# Number of sparks
		self.p = int(5 + (random.uniform(config.minParticles, config.maxParticles)))
		self.angle = 2 * math.pi / self.p

		config.numberDone = round(self.p / 5)

		# Speed factor
		self.fFactor = int(random.uniform(15, 65))

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
		self.decr_g = round(random.uniform(.25, 1))
		self.decr_b = round(random.uniform(.25, 1))

		# vertical deacelleration
		self.deacelleration = random.uniform(0.8, 0.99)

		# horizontal deacelleration
		self.deacellerationx = random.uniform(0.8, 0.95)

		# pseudo gravity deacelleration
		self.gravity = random.uniform(0.1, 1.52)

		for n in range(0, self.p):
			# variation in initial velocity
			fx = random.random() * self.fFactor
			fy = random.random() * self.fFactor
			vx = math.cos(self.angle * n) * fx
			vy = math.sin(self.angle * n) * fy
			r = int(random.uniform(0, 255) * self.brightness)
			g = int(random.uniform(0, 255) * self.brightness)
			b = int(random.uniform(0, 255) * self.brightness)
			self.particles.append(
				{
					"id": n,
					"xpos": self.x,
					"ypos": self.y,
					"vx": vx,
					"vy": vy,
					"clr": [r, g, b],
					"done": 0,
					"gravity": random.uniform(0.51, 1.52)
				}
			)

	def explosion(self):
		"""
		if(self.traces == False) : self.config.matrix.Clear()
		"""
		sumOfDone = 0
		for q in range(0, self.p):
			sumOfDone += self.particles[q]["done"]

		if sumOfDone >= self.p - config.numberDone:
			self.done = True

		if random.random() > 0.996 and self.config.sideWind == True:
			config.vx = round(2 - random.random() * 4)
			# useSideWind = True

		for q in range(0, self.p):
			ref = self.particles[q]
			ref["xpos"] += ref["vx"]
			ref["ypos"] += ref["vy"]

			# deacelleration / damping
			ref["vx"] = ref["vx"] * self.deacellerationx
			ref["vy"] = ref["vy"] * self.deacelleration

			# pseudo gravity
			ref["vy"] = ref["vy"] + ref["gravity"] * math.sin(config.systemRotation * math.pi/180)  # self.gravity
			ref["vx"] = ref["vx"] + ref["gravity"] * math.cos(config.systemRotation * math.pi/180)  # self.gravity

			self.particles[q]["clr"][0] = self.particles[q]["clr"][0] - self.decr_r
			self.particles[q]["clr"][1] = self.particles[q]["clr"][1] - self.decr_g
			self.particles[q]["clr"][2] = self.particles[q]["clr"][2] - self.decr_b

			if self.particles[q]["clr"][0] <= 0:
				self.particles[q]["clr"][0] = 0
			if self.particles[q]["clr"][1] <= 0:
				self.particles[q]["clr"][1] = 0
			if self.particles[q]["clr"][2] <= 0:
				self.particles[q]["clr"][2] = 0

			r = self.particles[q]["clr"][0]
			g = self.particles[q]["clr"][1]
			b = self.particles[q]["clr"][2]

			sumOfClrs = (
				self.particles[q]["clr"][0]
				+ self.particles[q]["clr"][1]
				+ self.particles[q]["clr"][2]
			)

			'''
			# a pixel wind changes the cascade
			if self.config.sideWind and sumOfClrs > 100:
				config.vx = round(2 - random.random() * 4)
				ref["vx"] = config.vx
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
			xDisplayPos = ref["xpos"]
			yDisplayPos = ref["ypos"]

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

			if (
				xDisplayPos < 0
				or xDisplayPos > config.canvasWidth
				or yDisplayPos > config.canvasHeight
			):
				self.particles[q]["done"] = 1


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


def callBack():
	global config, sprkl

	if random.random() > 0.8:
		config.traces = True
	if random.random() > 0.99:
		config.traces = False
	if sprkl.done == True:
		config.draw.rectangle(
			(0, 0, config.canvasWidth, config.canvasHeight), fill=(0, 0, 0, 20)
		)
		if random.random() > 0.5:
			config.draw.rectangle(
				(0, 0, config.canvasWidth, config.canvasHeight), fill=(0, 0, 0, 255)
			)
		config.render(config.image, 0, 0, config.canvasWidth, config.canvasHeight)
		sprkl = Sparkles(config)
		sprkl.setUp()
		config.traces = False
		config.sideWind = False


def runWork():
	global redrawSpeed
	global sprkl
	redrawSpeed = 0.01
	while True:
		config.directorController.checkTime()
		if config.directorController.advance == True:
			iterate()
		time.sleep(redrawSpeed)


def setUpDelays():
	global config
	##


def iterate():
	global config
	global sprkl
	config.vx = 0

	if random.random() > 0.995 and config.traces == True:
		config.sideWind = True

	# Fade out the sparkle
	if config.traces != True:
		config.draw.rectangle(
			(0, 0, config.canvasWidth, config.canvasHeight),
			fill=(0, 0, 0, config.fadeRate),
		)
		config.sideWind = False
		config.vx = 0
	sprkl.explosion()
	config.render(config.image, 0, 0, config.canvasWidth, config.canvasHeight)
	callBack()
	count = 0
	# Done


def main(run=True):
	global config
	global redrawSpeed
	global sprkl

	config.traces = False
	config.sideWind = False
	config.fadeRate = 15

	config.minParticles = 1000
	config.maxParticles = 12000
	config.numberDone = 10

	config.systemRotation = 200

	config.initXRangeMin = 100
	config.initXRangeMax = 380
	config.initYRangeMin = 100
	config.initYRangeMax = 380

	config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.draw = ImageDraw.Draw(config.image)
	sprkl = Sparkles(config)
	sprkl.setUp()

		# managing speed of animation and framerate
	config.directorController = Director(config)
	config.directorController.slotRate  = .03

	if run:
		runWork()
