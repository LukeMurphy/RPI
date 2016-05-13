#!/usr/bin/python
import PIL.Image
from PIL import Image, ImageDraw, ImageMath, ImageEnhance
from PIL import ImageChops
from modules import colorutils
# Import the essentials to everything
import time, random, math

class ImageSprite :
	color = (255,0,0)
	bgColor = (0,255,255)
	speed = 2
	speedMultiplier = 4
	x = xPos = 0
	y = yPos = 0
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
	yOffsetFactor = 40

	count = 0
	frame = 1
	countLimit = 1
	clrIndex = 0

	imgHeight = 0
	panRangeLimit = 0
	useJitter = False
	useBlink = False
	blink = False
	blinkNum = 0
	blinkCount = 0
	blinkStationary = False

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

	
	processImage = True
	resizeImage = True
	randomizeColor = False
	randomizeDirection = True

	lastPictureIndex = 0
	debug = False

	def __init__(self, config, iid=0) :
		self.iid = iid
		self.config = config

		self.clrUtils = colorutils
		self.clrUtils.brightness = self.config.brightness
		pass
		
	def callBack(self, *args) :

		if(args[0] == True) :
			self.image = self.imageOriginal.copy()
			self.process()

		return True
		

	def make(self, img="", setvX = 0, setvY = 0, processImage = True, resizeImage = True, randomizeDirection = True, randomizeColor = True):

		self.frame = 0
		self.dX = setvX
		self.dY = setvY

		self.processImage = processImage
		self.resizeImage = resizeImage
		self.randomizeColor = randomizeColor
		self.randomizeDirection = randomizeDirection

		if (random.random()> .5 and randomizeDirection) : 
			self.dX *= -1

		self.debugMessage("Trying to load " + img)	

		if(self.loadImage(img)) :
			# scale to the WIDTH of the screen
			if(self.image.size[0] != self.config.screenWidth and self.resizeToWidth) :
				self.ratio = float(config.screenWidth)/ image.size[0]
				self.image = self.image.resize((self.config.screenWidth,int(self.ratio * self.image.size[1])))

			if(self.dX < 0) :
				# Reverse image
				self.image = self.image.rotate(-180)

			self.imageOriginal = self.image.copy()
			self.process()

			self.debugMessage( img + " loaded")
			#init()
		else:
			self.debugMessage ("could not load")

	def process(self) :
		if(self.processImage) :
			if(self.resizeImage) :
				change = random.uniform(.1,1.2)
				newSizeX = change * self.image.size[0]
				newSizeY = change * self.image.size[1]
				self.image = self.image.resize((int(newSizeX), int(newSizeY))) #, Image.ANTIALIAS

			#Colorize via overlay etc
			clrBlock = PIL.Image.new("RGBA", (self.image.size[0], self.image.size[1]))
			clrBlockDraw = ImageDraw.Draw(clrBlock)

			brt = random.random()

			if(self.randomizeColor) :
				r = int(random.uniform(200,255))
				g = int(random.uniform(0,255))
				b = int(random.uniform(0,255))
				clr = self.clrUtils.getRandomColorWheel(brt)
				clrIndex = int(random.random() * 4)

				if (self.dX < 0) : clrIndex  = int(random.uniform(6,9))
				clr = self.clrUtils.wheel[clrIndex]
				self.clrIndex += 1
				if(self.clrIndex == len(self.clrUtils.wheel)) :
					self.clrIndex = 0
			else :
				r = int(random.uniform(200,255))
				g = int(random.uniform(0,255))
				b = int(random.uniform(0,10))
				clr = (r,g,b)

			clrBlockDraw.rectangle((0,0,self.image.size[0], self.image.size[1]), fill=clr)
			self.image =  ImageChops.multiply(clrBlock, self.image)

			self.imageCopy = Image.new("RGBA", (self.image.size[0], self.image.size[1]))
			self.imageCopy.paste(self.image, (0, 0), self.image)

			enhancer = ImageEnhance.Brightness(self.imageCopy)
			self.image = enhancer.enhance(self.brightnessFactor)
			self.imageCopy = enhancer.enhance(self.brightnessFactor)
			self.draw = ImageDraw.Draw(self.image)

			if(self.processImage) : self.yOffset =  int(random.uniform(-self.yOffsetFactor * change, self.yOffsetFactor) )

	def remove(self, arrayList) :
		arrayList.remove(self)
		pass

	def move(self) :
		if(self.setForRemoval!=True) :
			#self.image.paste(self.presentationImage, (0,0))

			self.xPos += self.dX
			self.yPos += self.dY

			if(self.dY > 0 and self.yPos >= self.endY) :
				self.callBack(self.yPos, -self.image.size[1])
				#self.yPos = -self.image.size[1]

			if(self.dY < 0 and self.yPos < 0) :
				self.callBack(self.yPos, self.endY)
				#self.yPos = self.endY

			if(self.dX > 0 and self.xPos >= self.endX) :
				self.callBack(True, self.xPos, -self.image.size[0])
				self.xPos = -self.image.size[0]

			if(self.dX < 0 and self.xPos < -self.image.size[0]) :
				self.callBack(True, self.xPos, self.endX)
				self.xPos = self.endX

			self.x = self.xPos + self.xOffset
			self.y = self.yPos + self.yOffset

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
		# this doesnt work because it just draws to the existing size of the loaded image ... so gets cut off
		#if(random.random() > .9) : draw.rectangle((0,image.size[1] -10,32,image.size[1] + config.screenHeight), fill = (12), outline = (0))

		self.stepSize = 1
		if(abs(self.dY) > 1) : self.stepSize = abs(self.dY)

		if(self.useJitter):
			if(random.random() > .5) : 
				self.jitter = False
				self.dY = 0
				self.yPos = 0
			if(random.random() > .97) : self.jitter = True
			if(self.jitter) : self.dY = random.uniform(-.3,.3)

		self.move()
	
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
		if(self.useBlink == True) :
			if(random.random() > .9998 and self.blink == False) :
				self.blink = True
				self.blinkNum = int(random.uniform(32,256))
				self.blinkCount = 0
				self.blinkStationary = True if (random.random() > .15) else False

			if(self.blink) :
				self.blinkCount += 1
				#self.x -= self.dX
				if(self.blinkCount%8 == 0) :
					self.draw.rectangle((0,0, self.image.size[0] ,self.image.size[1]), fill = (0))
					#self.y = -100
				elif (self.blinkCount%4 == 0) : 
					#self.y = 0
					self.image.paste(self.imageCopy, (0 ,0), self.imageCopy)

				if (self.blinkCount >= self.blinkNum) :
					self.image.paste(self.imageCopy, (0 ,0), self.imageCopy)
					if(random.random() > .5 ) : 
						self.x += self.image.size[1]
					self.blink = False

			if(self.blinkStationary == False) :
				self.panImage()
			elif(random.random() > .995) : 
				self.blinkStationary =  False

		else : self.panImage()

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