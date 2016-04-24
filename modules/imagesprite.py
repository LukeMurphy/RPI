#!/usr/bin/python
from PIL import Image, ImageDraw,ImageMath, ImageEnhance
# Import the essentials to everything
import time, random, math

class ImageSprite :
	color = (255,0,0)
	bgColor = (0,255,255)
	speed = 2
	speedMultiplier = 4
	x = 0
	y = 0
	dX = -1
	dY = 0
	startX = 0
	startY = 0
	endX = 0
	endY = 0

	reveal = 0
	revealSpeed = 1
	revealSpeedMax = 3
	setForRemoval = False

	r=g=b=0
	xOffset = 0
	yOffset = 0

	count = 0
	frame = 1
	countLimit = 1

	imgHeight = 0
	panRangeLimit = 0
	useJitter = False
	useBlink = False
	presentTime =  10
	brightnessFactor = .5
	rate = 0
	gifPlaySpeed = 0.07
	scrollSpeed = .04
	bgFillColor = 0x000000

	action = "play"
	direction = "right"
	directionStr = "Left"
	brightnessFlux = False
	brightnessFluxRate  = 8 # As a factor or PI/brightnessFluxRate
	resizeToWidth = False

	lastPictureIndex = 0
	debug = False

	def __init__(self, config, iid=0) :
		self.iid = iid
		self.config = config
		pass
		
	def callBack(self, pos, newPos) :
		return True
		

	def make(self, img="", setvX = 0, setvY = 0):

		self.frame = 0
		self.dX = setvX
		self.dY = setvY

		self.debugMessage("Trying to load " + img)	

		if(self.loadImage(img)) :
			# scale to the WIDTH of the screen
			if(self.image.size[0] != self.config.screenWidth and self.resizeToWidth) :
				self.ratio = float(config.screenWidth)/ image.size[0]
				self.image = self.image.resize((self.config.screenWidth,int(self.ratio * self.image.size[1])))

			self.imageCopy = Image.new("RGBA", (self.image.size[0], self.image.size[1]))
			self.imageCopy.paste(self.image, (0, 0), self.image)

			enhancer = ImageEnhance.Brightness(self.imageCopy)
			self.image = enhancer.enhance(self.brightnessFactor)
			self.debugMessage( img + " loaded")
			#init()
		else:
			self.debugMessage ("could not load")

	def remove(self, arrayList) :
		arrayList.remove(self)
		pass

	def move(self) :
		if(self.setForRemoval!=True) :
			#self.image.paste(self.presentationImage, (0,0))

			self.x += self.dX
			self.y += self.dY

			if(self.dY > 0 and self.y >= self.endY) :
				self.callBack(self.y, -self.image.size[1])
				#self.y = -self.image.size[1]

			if(self.dY < 0 and self.y < self.endY) :
				self.callBack(self.y, self.endY)
				#self.y = self.endY

			if(self.dX > 0 and self.x >= self.endX) :
				self.callBack(self.x, -self.image.size[0])
				self.x = -self.image.size[0]

			if(self.dX < 0 and self.x < self.endX) :
				self.callBack(self.x, self.endX)
				self.x = self.endX

	def loadImage(self,arg):
		self.image = Image.open(arg , "r")
		self.image.load()
		self.imgHeight =  self.image.getbbox()[3]
		return True

	def presentImage(self) :
		global frame, count, xOffset, yOffset, dX, dY, image, panRangeLimit, scrollSpeed, useJitter, useBlink, imageCopy, presentTime	
		imageCopyTemp = imageCopy
		enhancer = ImageEnhance.Brightness(imageCopyTemp)
		imageCopyTemp = enhancer.enhance(brightnessFactor)
		config.render(imageCopyTemp, int(xOffset), int(yOffset), imageCopy.size[0], imageCopy.size[1], False)
		config.actions.drawBlanks()
		time.sleep(presentTime)
		
	def panImage(self) :

		self.jitter = False

		'''
		# defaults for vertical image scrolling
		if(self.panRangeLimit == 0) : 
			self.rangeLimit = self.imageCopy.size[1] + self.config.screenHeight
			self.yOffset = self.config.screenHeight
		else : 
			self.rangeLimit = self.panRangeLimit + self.imageCopy.size[1]
			if(self.dY ==0) : self.xOffset = -self.imageCopy.size[1]

		if(self.dY != 0) : 
			self.yOffset = self.config.screenHeight #-image.size[1]
			#xOffset = int((config.screenWidth ) * random.random()) - 20
			#xOffset = 0
		'''

		self.draw = ImageDraw.Draw(self.image)

		# this doesnt work because it just draws to the existing size of the loaded image ... so gets cut off
		#if(random.random() > .9) : draw.rectangle((0,image.size[1] -10,32,image.size[1] + config.screenHeight), fill = (12), outline = (0))

		self.stepSize = 1
		if(abs(self.dY) > 1) : self.stepSize = abs(self.dY)

		if(self.useJitter):
			if(random.random() > .7) : 
				self.jitter = False
				self.dY = 0
				self.y = 0
			if(random.random() > .17) : self.jitter = True
			if(self.jitter) : self.dY = random.uniform(-.3,.3)

		self.move()

		if(self.useBlink == True and random.random() > .9985) :
			self.blink = False
			self.blinkNum = int(random.uniform(7,23))
			for blk in range (0, self.blinkNum) :
				self.imageCopy  = self.image
				self.draw.rectangle((0,0, self.image.size[0] ,self.image.size[1]), fill = (0))
				if(self.blink) :
					#config.render(imageCopy, int(xOffset + x), int(yOffset  + y), image.size[0], image.size[1], False)
					self.blink = False
				else :
					#config.render(image, int(xOffset + x), int(yOffset  + y), image.size[0], image.size[1], False)
					self.blink = True
				time.sleep(.15)	
			self.x += self.image.size[1]
		#else :
			#imageCopyTemp = self.image
			#enhancer = ImageEnhance.Brightness(imageCopyTemp)
			#imageCopyTemp = enhancer.enhance(self.brightnessFactor)
			#self.imageCopy = imageCopyTemp
			#self.config.render(self.image, int(xOffset + x), int(yOffset + y), imageCopy.size[0], imageCopy.size[1], False)
	
	def fillColor(self,force=False) :
		global bgFillColor
		if(random.random() > .8 or force) :
			config.matrix.Fill(bgFillColor)
		else :
			config.matrix.Fill(bgFillColor)
			
	def rotateImage(self,angle) :
		global image, matrix
		image = config.image.resize((32,32))
		image = image.rotate(angle, Image.BICUBIC, 1);		
		config.matrix.Clear()
		config.matrix.SetImage(config.image.im.id, -8, -8)

	def animate(self, randomizeTiming = False, frameLimit = 3) :
		global frame, count, xOffset, yOffset, dX,image, action, gifPlaySpeed, imgHeight, imageCopy, brightnessFactor, brightnessFluxRate, rate

		# This needs fixing  - currently requires extra frame
		# at end of gif  --

		#fillColor(True)
		#config.screenHeight - imgHeight'
		skipTime = False
		#************************************#
		### DRAW THE IMAGE ACROSS ALL PANELS
		#imageCopy = image.point(lambda p: p * 0.19)
		
		imageCopy.paste(image)
		#print(imageCopy,image,xOffset,yOffset)

		if(brightnessFlux) :
			rate+=math.pi/brightnessFluxRate;
			brightnessFactor = (math.sin(rate) + 1) / 2 + .01
			#if(brightnessFactor > 1) : brightnessFactor = 1
			#if(brightnessFactor < 0) : brightnessFactor = .00001
		enhancer = ImageEnhance.Brightness(imageCopy)
		imageCopy = enhancer.enhance(brightnessFactor)
		
		config.render(imageCopy, xOffset, yOffset, config.screenWidth, config.screenHeight)
		config.actions.drawBlanks()
		
		try:
			image.seek(image.tell() + 1)
		except EOFError:
			image.seek(0)
			#print("fail", frame)
			skipTime = True
			pass

		if(skipTime == False) :
			if(randomizeTiming) :
				time.sleep(random.uniform(.02,.08))
				if(random.random() > .98) :
					time.sleep(random.uniform(.05,2))
			else :
				time.sleep(gifPlaySpeed)

		#if (frame == frameLimit):frame = 0
		
	def playImage(self, randomizeTiming = False, frameLimit = 3):
		global config
		animate(randomizeTiming, frameLimit)

	def update(self) :
		self.panImage()
		pass

	def init(self):
		global action, countLimit

		#print(countLimit)
		count = 0
		#fillColor(True)
		# Constantly re-calls the requested action util 
		# the count runs out - for long running plays
		# the countlimit just gets reset 
		while (count < countLimit):
			try:
				if(action == "play"):
					playImage(False, 7)
				elif(action == "pan") : 
					panImage()
				elif(action == "present") :
					presentImage()		
				count += 1
			except KeyboardInterrupt:
				print "Stopping...."
				exit()
				break

	def debugMessage(self,arg) :

		if(self.debug) : print(arg)		

	
	
###############################	