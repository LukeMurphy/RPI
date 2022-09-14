# ################################################### #
import math
import random
import time
from modules.configuration import bcolors
from modules import coloroverlay, colorutils
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps


''' ----------------------------------------------------------------------------------- '''


class SlotMaker:
	"""docstring for SlotMaker"""
	numberOfSlots = 0
	slotHeight = 100
	slotWidth = 4
	slotSpacing = 1 
	xPos = 0
	yPos = 0


	def __init__(self, config):

		super(SlotMaker, self).__init__()
		self.config = config
		self.directorArray = []
		self.angleOffset = 0
		self.angleGap = 1
		self.innerRadius = 10
		self.outerRadius = 100
		self.orientation = 1



	def setUpLinears(self):
		self.slotArray = []
		for i in range(0, self.numberOfSlots) :
			s = Slot()
			self.slotArray.append(s)

		self.setUpPositions()


	def setUpPositions(self) :

		jitterAmount = round(random.uniform(0,config.jitterAmount))
		for i in range(0, len(self.slotArray)) :
			s = self.slotArray[i]
			jitter = 0
			s.width = self.slotWidth
			s.height = self.slotHeight
			spacing = self.slotSpacing

			s.width -= 1
			if i % self.config.jitterFreq == 0 : jitter = jitterAmount
			s.xPos = self.xPos + s.width * i + spacing * i
			s.yPos = self.yPos + jitter

			s.xPos2 = self.xPos + s.width * i + spacing * i + s.width
			s.yPos2 = self.yPos + jitter

			s.xPos3 = self.xPos + s.width * i + spacing * i  + s.width
			s.yPos3 = self.yPos + s.height + jitter

			s.xPos4 = self.xPos + s.width * i + spacing * i
			s.yPos4 = self.yPos + s.height + jitter

			if self.orientation == -1 :
				s.xPos = self.xPos  + jitter
				s.yPos = self.yPos + s.width * i + spacing * i
				s.xPos2 = self.xPos  + jitter
				s.yPos2 = self.yPos + s.width * i + spacing * i + s.width
				s.xPos3 = self.xPos + s.height + jitter
				s.yPos3 = self.yPos + s.width * i + spacing * i  + s.width
				s.xPos4 = self.xPos + s.height + jitter
				s.yPos4 = self.yPos + s.width * i + spacing * i




	def setUpRadials(self):

		rads = 2 * math.pi / self.numberOfSlots
		for i in range(0, self.numberOfSlots) :
			s = Slot()
			s.width = self.slotWidth
			s.height = self.slotHeight
			spacing = self.slotSpacing
			a1 = i * rads + self.angleOffset
			a2 = (i + self.angleGap) * rads + self.angleOffset
			s.xPos = self.xPos + math.cos(a1) * self.innerRadius
			s.yPos = self.yPos + math.sin(a1) * self.innerRadius
			s.xPos2 = self.xPos + math.cos(a1) * self.outerRadius
			s.yPos2 = self.yPos + math.sin(a1) * self.outerRadius

			s.xPos3 = self.xPos + math.cos(a2) * self.outerRadius
			s.yPos3 = self.yPos + math.sin(a2) * self.outerRadius
			s.xPos4 = self.xPos + math.cos(a2) * self.innerRadius
			s.yPos4 = self.yPos + math.sin(a2) * self.innerRadius


			s.angle = i * rads
			self.slotArray.append(s)


''' ----------------------------------------------------------------------------------- '''


class Slot:
	"""docstring for Slot"""

	def __init__(self):

		super(Slot, self).__init__()
		self.xPos = 0
		self.yPos = 0
		self.width = 0
		self.height = 0
		self.backgroundColor = (0,0,0,0)
		self.r = 0
		self.g = 0
		self.b = 0
		self.a = 0

	
	def renderRect(self,ref) :

		self.backgroundColor  = tuple(round(x) for x in [self.r,self.g,self.b,self.a])
		p1 = (self.xPos, self.yPos)
		p2 = (self.xPos + self.width, self.yPos)
		p3 = (self.xPos + self.width, self.yPos + self.height)
		p4 = (self.xPos, self.yPos + self.height)

		ref.polygon((p1,p2,p3,p4), fill = self.backgroundColor)
		#ref.rectangle((self.xPos, self.yPos, self.xPos + self.width, self.yPos + self.height), fill=self.backgroundColor)

	def render(self,ref) :

		self.backgroundColor  = tuple(round(x) for x in [self.r,self.g,self.b,self.a])
		p1 = (self.xPos, self.yPos)
		p2 = (self.xPos2, self.yPos2)
		p3 = (self.xPos3, self.yPos3)
		p4 = (self.xPos4, self.yPos4 )

		ref.polygon((p1,p2,p3,p4), fill = self.backgroundColor)
		#ref.rectangle((self.xPos, self.yPos, self.xPos + self.width, self.yPos + self.height), fill=self.backgroundColor)

''' ----------------------------------------------------------------------------------- '''


class Director:
	"""docstring for Director"""

	targetSlotArray = []
	currentSlot = 0
	totalSlots = 0
	slotRate = .02
	advance = False
	color = [255,255,255]
	direction = 1

	def __init__(self, config):
		super(Director, self).__init__()
		self.config = config
		self.tT = time.time()


	def setUpSlots(self):
		s = SlotMaker(self.config)
		s.numberOfSlots = config.numerOfSlotsMin + round(random.random()*config.numerOfSlotsMax)
		s.slotSpacing = round(random.uniform(config.slotSpacingMin, config.slotSpacingMax))
		s.slotWidth = round(random.uniform(config.slotWidthMin, config.slotWidthMax))
		s.slotHeight = round(random.uniform(config.slotHeightMin, config.slotHeightMax))

		s.orientation = 1 if random.random() > config.orientationProb else -1

		if s.orientation == 1 :
			s.yPos = round(random.random()*config.yRange)
			s.xPos = 0
			s.numberOfSlots = round(config.canvasWidth / (s.slotWidth + s.slotSpacing/2))
		else : 
			s.xPos = round(random.random()*config.xRange)
			s.yPos = 0
			s.numberOfSlots = round(config.canvasHeight / (s.slotWidth + s.slotSpacing/2))

		s.setUpLinears()

		self.slotMakerRef = s
		self.orientation = s.orientation
		self.targetSlotArray = s.slotArray
		self.color = newColor() if self.orientation == 1 else newColorAlt()
		self.direction = 1 if random.random() > .5 else -1
		if self.orientation == 1 :
			self.slotRate = random.uniform(self.config.slotSpeed2Min, self.config.slotSpeed2Max)
		else :
			self.slotRate = random.uniform(self.config.slotSpeedMin, self.config.slotSpeedMax)
		#s.directorArray.append(d)


	def checkTime(self):
		if (time.time() - self.tT) >= self.slotRate :
			self.tT = time.time()
			self.advance = True
		else :
			self.advance = False


	def next(self):

		self.checkTime()

		if self.advance == True :
			#self.targetSlotArray[self.currentSlot].backgroundColor = (0,0,255,255)
			self.currentSlot += self.direction
			reset = False

			if self.currentSlot >= len(self.targetSlotArray) :
				self.currentSlot = 0
				reset = True

			if self.currentSlot < 0:
				self.currentSlot = len(self.targetSlotArray) - 1
				reset = True

			if reset == True :
				if self.orientation == 1 :
					self.slotRate = random.uniform(self.config.slotSpeed2Min, self.config.slotSpeed2Max)
				else :
					self.slotRate = random.uniform(self.config.slotSpeedMin, self.config.slotSpeedMax)
				#self.direction *= -1
				

				if self.orientation == 1 :
					self.color = newColor()  
					self.slotMakerRef.yPos = round(random.random()*self.config.yRange)
					self.slotMakerRef.setUpPositions()
				else:
					self.color = newColorAlt()
					self.slotMakerRef.xPos = round(random.random()*self.config.xRange)
					self.slotMakerRef.setUpPositions()



			self.targetSlotArray[self.currentSlot].r = self.color[0]
			self.targetSlotArray[self.currentSlot].g = self.color[1]
			self.targetSlotArray[self.currentSlot].b = self.color[2]
			self.targetSlotArray[self.currentSlot].a = self.color[3]

			if self.targetSlotArray[self.currentSlot].r >255 : self.targetSlotArray[self.currentSlot].r = 255
			if self.targetSlotArray[self.currentSlot].g >255 : self.targetSlotArray[self.currentSlot].g = 255
			if self.targetSlotArray[self.currentSlot].b >255 : self.targetSlotArray[self.currentSlot].b = 255
			if self.targetSlotArray[self.currentSlot].a >255 : self.targetSlotArray[self.currentSlot].a = 255

		self.targetSlotArray[self.currentSlot].render(self.config.draw)


	

def newColor() :
	return colorutils.getRandomColorHSV(
				config.bg_minHue,
				config.bg_maxHue,
				config.bg_minSaturation,
				config.bg_maxSaturation,
				config.bg_minValue,
				config.bg_maxValue,
				config.bg_dropHueMinValue,
				config.bg_dropHueMaxValue,
				round(random.uniform(config.bg_minAlpha, config.bg_maxAlpha))
				)


def newColorAlt() :
	return colorutils.getRandomColorHSV(
				config.lines_minHue,
				config.lines_maxHue,
				config.lines_minSaturation,
				config.lines_maxSaturation,
				config.lines_minValue,
				config.lines_maxValue,
				config.lines_dropHueMinValue,
				config.lines_dropHueMaxValue,
				round(random.uniform(config.lines_minAlpha, config.lines_maxAlpha))
				)


def main(run=True):
	global config
	global expandingRingss

	expandingRingss = []
	config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.draw = ImageDraw.Draw(config.image)

	config.redrawSpeed = float(workConfig.get("forms", "redrawSpeed"))

	config.bg_minHue = float(workConfig.get("forms", "bg_minHue"))
	config.bg_maxHue = float(workConfig.get("forms", "bg_maxHue"))
	config.bg_minSaturation = float(workConfig.get("forms", "bg_minSaturation"))
	config.bg_maxSaturation = float(workConfig.get("forms", "bg_maxSaturation"))
	config.bg_minValue = float(workConfig.get("forms", "bg_minValue"))
	config.bg_maxValue = float(workConfig.get("forms", "bg_maxValue"))
	config.bg_dropHueMinValue = float(workConfig.get("forms", "bg_dropHueMinValue"))
	config.bg_dropHueMaxValue = float(workConfig.get("forms", "bg_dropHueMaxValue"))
	config.bg_minAlpha= float(workConfig.get("forms", "bg_minAlpha"))
	config.bg_maxAlpha = float(workConfig.get("forms", "bg_maxAlpha"))

	config.lines_minHue = float(workConfig.get("forms", "lines_minHue"))
	config.lines_maxHue = float(workConfig.get("forms", "lines_maxHue"))
	config.lines_minSaturation = float(workConfig.get("forms", "lines_minSaturation"))
	config.lines_maxSaturation = float(workConfig.get("forms", "lines_maxSaturation"))
	config.lines_minValue = float(workConfig.get("forms", "lines_minValue"))
	config.lines_maxValue = float(workConfig.get("forms", "lines_maxValue"))
	config.lines_dropHueMinValue = float(workConfig.get("forms", "lines_dropHueMinValue"))
	config.lines_dropHueMaxValue = float(workConfig.get("forms", "lines_dropHueMaxValue"))
	config.lines_minAlpha= float(workConfig.get("forms", "lines_minAlpha"))
	config.lines_maxAlpha = float(workConfig.get("forms", "lines_maxAlpha"))


	config.orientationProb = float(workConfig.get("forms", "orientationProb"))

	config.slotSpeedMultiplier = float(workConfig.get("forms", "slotSpeedMultiplier"))
	config.slotSpeedMin = float(workConfig.get("forms", "slotSpeedMin")) * config.slotSpeedMultiplier
	config.slotSpeedMax = float(workConfig.get("forms", "slotSpeedMax")) * config.slotSpeedMultiplier
	config.slotSpeed2Min = float(workConfig.get("forms", "slotSpeed2Min")) * config.slotSpeedMultiplier
	config.slotSpeed2Max = float(workConfig.get("forms", "slotSpeed2Max")) * config.slotSpeedMultiplier
	config.bgFlashRate = float(workConfig.get("forms", "bgFlashRate"))

	config.numerOfSlotsMax = int(workConfig.get("forms", "numerOfSlotsMax"))
	config.numerOfSlotsMin = int(workConfig.get("forms", "numerOfSlotsMin"))
	config.jitterAmount = int(workConfig.get("forms", "jitterAmount"))
	config.jitterAmountInit = int(workConfig.get("forms", "jitterAmount"))
	config.jitterFreq = int(workConfig.get("forms", "jitterFreq"))
	config.slotSpacingMin = int(workConfig.get("forms", "slotSpacingMin"))
	config.slotSpacingMax = int(workConfig.get("forms", "slotSpacingMax"))
	config.slotWidthMin = int(workConfig.get("forms", "slotWidthMin"))
	config.slotWidthMax = int(workConfig.get("forms", "slotWidthMax"))
	config.slotHeightMin = int(workConfig.get("forms", "slotHeightMin"))
	config.slotHeightMax = int(workConfig.get("forms", "slotHeightMax"))
	config.innerRadius = int(workConfig.get("forms", "innerRadius"))
	config.outerRadius = int(workConfig.get("forms", "outerRadius"))
	config.linesCreated = int(workConfig.get("forms", "linesCreated"))
	config.yRange = int(workConfig.get("forms", "yRange"))
	config.xRange = int(workConfig.get("forms", "xRange"))

		# background color - higher the 
	# alpha = less persistent images
	backgroundColor = (workConfig.get("forms", "backgroundColor")).split(",")
	config.backgroundColor = tuple(int(x) for x in backgroundColor)	

	backgroundFlashcolor = (workConfig.get("forms", "backgroundFlashcolor")).split(",")
	config.backgroundFlashcolor = tuple(int(x) for x in backgroundFlashcolor)

	config.filterPatchProb = float(workConfig.get("forms", "filterPatchProb"))
	config.filterPatchProbOff = float(workConfig.get("forms", "filterPatchProbOff"))


	config.drawingPaths = []


	for i in range(0, config.linesCreated):
		d = Director(config)
		d.setUpSlots()
		config.drawingPaths.append(d)


	'''
	for i in range(0, config.linesCreated):
		s = SlotMaker(config)
		s.numberOfSlots = config.numerOfSlotsMin + round(random.random()*config.numerOfSlotsMax)
		s.slotSpacing = round(random.uniform(config.slotSpacingMin, config.slotSpacingMax))
		s.slotWidth = round(random.uniform(config.slotWidthMin, config.slotWidthMax))
		s.slotHeight = round(random.uniform(config.slotHeightMin, config.slotHeightMax))
		s.orientation = 1 if random.random() > config.orientationProb else -1
		s.yPos = round(random.random()*config.yRange)
		s.xPos = round(random.random()*config.xRange)

		s.innerRadius = round(random.random()*config.innerRadius)
		s.outerRadius = round(random.random()*config.outerRadius)
		s.angleGap = random.random()
		s.angleOffset = math.pi/4 + math.pi
		s.setUpRadials()

		d = Director(config)
		d.targetSlotArray = s.slotArray
		d.color = newColor()
		d.direction = 1 if random.random() > .5 else -1
		d.slotRate = random.uniform(config.slotSpeedMin, config.slotSpeedMax)
		s.directorArray.append(d)
		#config.slotsArray.append(s)

	Every set of slots is first built or drawn out and then can have 
	any number of directors running its slots

	Each set of slots only has one SlotManager

	Each Director should probably only talk to one SlotManager because the 
	Director has to know how many slots are available etc


	'''


def reDraw(config):
	
	for d in range(0, len(config.drawingPaths)) :
		director = config.drawingPaths[d]
		director.next()

	if random.random() < config.bgFlashRate:
		config.draw.rectangle((0, 0, config.screenWidth, config.screenHeight), fill=config.backgroundFlashcolor)
		for d in range(0, len(config.drawingPaths)) :
			director = config.drawingPaths[d]
			director.currentSlot = 0
		if config.jitterAmount == 0 :
			config.jitterAmount = config.jitterAmountInit 
		else:
			config.jitterAmount = 0


def iterate():
	global config, expandingRingsRing, lastRate, calibrated, cycleCount
	#config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.draw.rectangle((0, 0, config.screenWidth, config.screenHeight), fill=config.backgroundColor)
	
	reDraw(config)

	if random.random() < config.filterPatchProb:
		#print("should be remapping")
		config.useFilters = True
		x1 = round(random.uniform(0,config.canvasWidth))
		x2 = round(random.uniform(x1,config.canvasWidth))
		y1 = round(random.uniform(0,config.canvasHeight))
		y2 = round(random.uniform(y1,config.canvasHeight))

		config.remapImageBlock = True
		config.remapImageBlockSection = (x1, y1, x2, y2)
		config.remapImageBlockDestination = (x1, y1)

	# Don't want the patch to always be there - just little interruptions
	if random.random() < config.filterPatchProbOff :
		#print("turning off remapping")
		config.useFilters = False
		x1 = 0
		x2 = 0
		y1 = 0
		y2 = 0

		config.remapImageBlock = True
		config.remapImageBlockSection = (x1, y1, x2, y2)
		config.remapImageBlockDestination = (x1, y1)

	# Do the final rendering of the composited image
	config.render(config.image, 0, 0, config.screenWidth, config.screenHeight)


def runWork():
	global config
	print(bcolors.OKGREEN + "** " + bcolors.BOLD)
	print("Running slots.py")
	print(bcolors.ENDC)
	while True:
		iterate()
		time.sleep(config.redrawSpeed)


	'''
	s = SlotMaker(config)
	s.numberOfSlots = 180
	s.slotSpacing = 2
	s.slotWidth = 1
	s.slotHeight = 300
	s.xPos = 200
	s.yPos = 200
	s.angleOffset = 0
	s.angleGap = .5
	s.innerRadius = 2
	s.outerRadius = 240
	s.setUp()

	d = Director(config)
	d.targetSlotArray = s.slotArray
	d.color = [255,0,0,255]
	d.direction = 1
	d.currentSlot = len(d.targetSlotArray) - 1
	d.slotRate = .02
	s.directorArray.append(d)

	config.slotsArray.append(s)

	s = SlotMaker(config)
	s.numberOfSlots = 180
	s.slotSpacing = 2
	s.slotWidth = 1
	s.slotHeight = 300
	s.xPos = 200
	s.yPos = 200
	s.angleOffset = math.pi
	s.angleGap = .5
	s.innerRadius = 2
	s.outerRadius = 240
	s.setUp()

	d = Director(config)
	d.targetSlotArray = s.slotArray
	d.color = [255,0,0,255]
	d.direction = 1
	d.currentSlot = len(d.targetSlotArray) - 1
	d.slotRate = .02
	s.directorArray.append(d)

	config.slotsArray.append(s)


	s = SlotMaker(config)
	s.numberOfSlots = 180
	s.slotSpacing = 1
	s.slotWidth = 1
	s.slotHeight = 300
	s.xPos = 208
	s.yPos = 200
	s.angleOffset = -math.pi/100
	s.angleGap = .15
	s.innerRadius = 2
	s.outerRadius = 240
	s.setUp()

	d = Director(config)
	d.targetSlotArray = s.slotArray
	d.color = [100,255,0,155]
	d.direction = 1
	d.slotRate = .03
	s.directorArray.append(d)
	config.slotsArray.append(s)


	s = SlotMaker(config)
	s.numberOfSlots = 180
	s.slotSpacing = 1
	s.slotWidth = 1
	s.slotHeight = 300
	s.xPos = 208
	s.yPos = 200
	s.angleOffset = -math.pi/100 + math.pi
	s.angleGap = .15
	s.innerRadius = 2
	s.outerRadius = 240
	s.setUp()

	d = Director(config)
	d.targetSlotArray = s.slotArray
	d.color = [100,255,0,155]
	d.direction = 1
	d.slotRate = .03
	s.directorArray.append(d)
	config.slotsArray.append(s)




	s = SlotMaker(config)
	s.numberOfSlots = 180
	s.slotSpacing = 1
	s.slotWidth = 1
	s.slotHeight = 300
	s.xPos = 210
	s.yPos = 200
	s.angleOffset = math.pi/4
	s.angleGap = .5
	s.innerRadius = 0
	s.outerRadius = 240
	s.setUp()

	d = Director(config)
	d.targetSlotArray = s.slotArray
	d.color = [0,0,255,255]
	d.direction = -1
	d.slotRate = .03
	s.directorArray.append(d)
	config.slotsArray.append(s)


	s = SlotMaker(config)
	s.numberOfSlots = 180
	s.slotSpacing = 1
	s.slotWidth = 1
	s.slotHeight = 300
	s.xPos = 210
	s.yPos = 200
	s.angleOffset = math.pi/4 + math.pi
	s.angleGap = .5
	s.innerRadius = 0
	s.outerRadius = 240
	s.setUp()

	d = Director(config)
	d.targetSlotArray = s.slotArray
	d.color = [0,0,255,255]
	d.direction = -1
	d.slotRate = .03
	s.directorArray.append(d)
	config.slotsArray.append(s)
	'''
