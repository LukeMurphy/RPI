#!/usr/bin/python
import PIL.Image
from PIL import Image, ImageDraw, ImageMath, ImageEnhance
from PIL import ImageChops, ImageFilter, ImagePalette
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
	xOffset = 0
	yOffset = 0
	yOffsetFactor = 40

	reveal = 0
	revealSpeed = 1
	revealSpeedMax = 3
	setForRemoval = False

	r=g=b=0
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
	gifPlaySpeed = 0.03
	scrollSpeed = .04
	bgFillColor = 0x000000

	action = "play"
	direction = "right"
	directionStr = "Left"
	brightnessFlux = False
	brightnessFluxRate  = 8 # As a factor or PI/brightnessFluxRate
	resizeToWidth = False
	resizeToHeight = False
	
	processImage = True
	resizeImage = True
	randomizeColor = False
	randomizeDirection = True
	colorMode = "random" 
	colorModeDirectional = True
	yOffsetChange = True

	lastPictureIndex = 0
	debug = False

	tempClrCount = 60
	frameCount = 1

	def __init__(self, config, iid=0) :
		self.iid = iid
		self.config = config

		self.clrUtils = colorutils
		self.clrUtils.brightness = self.config.brightness
		pass

	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''	
	## This is called every time an object moves off the screen
	## can update color, size etc
	def callBack(self, *args) :

		if(args[0] == True) :
			self.image = self.imageOriginal.copy()
			self.process()

			# This turns out to be less interesting - somehow the uniformity of speed
			# is a better counter point to the randomness of color and scale - 6-24-16
			'''
			if(random.random() > .8) : 
				speedMultiplier = random.uniform(1,10)
				self.dX *= speedMultiplier 
			'''

		return True
		
	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
	
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
		print("-----------\n")
		self.debugMessage("Trying to load " + img + "\n\n")	
		print("-----------\n")

		if(self.loadImage(img)) :
			# scale to the WIDTH of the screen
			if(self.image.size[0] != self.config.screenWidth and self.resizeToWidth) :
				self.ratio = float(self.config.screenWidth) / self.image.size[0]
				self.image = self.image.resize((self.config.screenWidth, int(self.ratio * self.image.size[1])))

			if(self.image.size[1] != self.config.screenHeight and self.resizeToHeight) :
				self.ratio = float(self.config.screenHeight) / self.image.size[1]
				self.image = self.image.resize((int(self.ratio * self.image.size[0]), self.config.screenHeight))

			if(self.dX < 0) :
				# Reverse image
				self.image = self.image.rotate(-180)
			#print("-----------\n")
			#print(self.image.info)
			#print("-----------\n")

			self.imageOriginal = self.image.copy()
			self.process()

			self.imageCopy = Image.new("RGBA", (self.config.screenWidth, self.config.screenHeight))
			self.imageCopy.paste(self.image, (0, 0))

			self.debugMessage( img + " loaded")
			#init()
		else:
			self.debugMessage ("could not load")
	
	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
	
	def process(self) :
		change = 1

		if(self.processImage) :
			if(self.resizeImage) :
				change = random.uniform(.1,1.2) * self.scalingFactor
				newSizeX = change * self.image.size[0]
				newSizeY = change * self.image.size[1]
				self.image = self.image.resize((int(newSizeX), int(newSizeY))) #, Image.ANTIALIAS

			brt = random.random()

			# This was really just set up for the multiple-planes piece
			if(self.randomizeColor) :

				# "Optical" or RBY Color Wheel
				if(self.colorMode == "colorWheel") : 
					clrIndex = int(random.random() * len(self.clrUtils.colorWheel))
					if(self.colorModeDirectional) :
						# Ones from LEFT are different
						if (self.dX < 0) : 
							clrIndex  = int(random.uniform(6,len(self.clrUtils.colorWheel)))
						else :
							clrIndex  = int(random.uniform(0,5))
					clr = self.clrUtils.wheel[clrIndex]

				# RGB Color Wheel
				if(self.colorMode == "colorRGB") : 
					clrIndex = int(random.random() * len(self.clrUtils.rgbColorWheel))
					if(self.colorModeDirectional) :
						# Ones from LEFT are different
						if (self.dX < 0) : 
							clrIndex  = int(random.uniform(3,len(self.clrUtils.rgbColorWheel)))
						else :
							clrIndex  = int(random.uniform(0,3))
					clr = self.clrUtils.rgbWheel[clrIndex]

				'''
				# Progressive color change - not used
				self.clrIndex += 1
				if(self.clrIndex == len(self.clrUtils.wheel)) :
					self.clrIndex = 0
				'''

				# Any RGB color
				if(self.colorMode == "random") : 
					clr = self.clrUtils.randomColor(brt)

			else :
				r = int(random.uniform(200,255))
				g = int(random.uniform(0,100))
				b = int(random.uniform(0,10))
				clr = (r,g,b)

			self.colorize(clr)

			# Not so great - yOffset is rendered useless by this  ....
			if(self.processImage and self.yOffsetChange) : 
				self.yOffset = int(random.uniform(self.config.screenHeight/2-self.yOffsetFactor * change, self.config.screenHeight/2 + self.yOffsetFactor) )
	
	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
	
	def colorize(self, clr) :

			#Colorize via overlay etc
			clrBlock = PIL.Image.new("RGBA", (self.image.size[0], self.image.size[1]))
			clrBlockDraw = ImageDraw.Draw(clrBlock)

			# Color overlay on b/w PNG sprite
			clrBlockDraw.rectangle((0,0,self.image.size[0], self.image.size[1]), fill=clr)
			self.image =  ImageChops.multiply(clrBlock, self.image)

			self.imageCopy = Image.new("RGBA", (self.image.size[0], self.image.size[1]))
			self.imageCopy.paste(self.image, (0, 0), self.image)

			enhancer = ImageEnhance.Brightness(self.imageCopy)
			self.image = enhancer.enhance(self.brightnessFactor)
			self.imageCopy = enhancer.enhance(self.brightnessFactor)
			self.draw = ImageDraw.Draw(self.image)
	
	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
	def filterize(self) :
		

		# Create a box and crop
		''''''''''''''''''''''''''''''
		lines = self.config.lines
		boxHeight = self.config.boxHeight
		boxWidth = self.config.boxWidth
		xPos1 = self.config.xPos1
		yPosBase = self.config.yPosBase
		targetClrs = self.config.targetClrs
		imageFilterProb = self.config.imageFilterProb
		bgFilterProb = self.config.bgFilterProb

		for n in range(0,lines,boxHeight) :
			
			yPos1 = yPosBase + n
			xPos2 = xPos1 + boxWidth
			yPos2 = yPos1 + boxHeight
			box = (xPos1, yPos1, xPos2, yPos2)
			region = self.image.crop(box)

			# Do geometry manips HERE
			''''''''''''''''''''''''''''''
			#region = region.transpose(Image.ROTATE_180)
			
			''''''''''''''''''''''''''''''
			##############################
			#region = region.convert("RGB")
			##############################

			# Do RGB Things HERE
			''''''''''''''''''''''''''''''
			#r, g, b, a = region.split()
			#region = Image.merge("RGBA", (r, g, b, a))
			#region = region.filter(ImageFilter.BLUR)
			#region = region.filter(ImageFilter.EDGE_ENHANCE_MORE)
			#region = region.filter(ImageFilter.MinFilter(size=3))

			'''
			self.image.copy()
			sharpener = ImageEnhance.Sharpness(self.image)
			sharpened = sharpener.enhance(2.0)
			# PIL.ImageFilter.ModeFilter(size=3)
			#im1 = self.image.filter(ImageFilter.BLUR)
			#f = self.image.ImageFilter.ModeFilter(size=3)
			'''

			#enh = ImageEnhance.Color(region)
			#enh = enh.enhance(0.0)

			#print(list(region.getdata()))

			
			if(random.random() > imageFilterProb) :
				ran = random.random() * 64
				#ran = 206.5
				region = region.point(lambda i: i - ran if (i > 116 and i < 128) else i)
				
				#exit()
			if(random.random() > bgFilterProb) :
				tartClr = targetClrs[int(random.random()*6)]
				#print(tartClr)
				region = region.point(lambda i: tartClr  if (i >= 0 and i < 10 ) else i)
			''''''''''''''''''''''''''''''
			#region = region.convert("P")
			self.image.paste(region, box)



	def augment(self) :
			if(self.frameCount > 39) :
				#print(self.tempClrCount)
				self.tempClrCount += 1
				self.frameCount = 0

	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
	
	def remove(self, arrayList) :
		arrayList.remove(self)
		pass
	
	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
	
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
	
	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
	
	def loadImage(self,arg):
		self.image = Image.open(arg , "r")
		self.image.load()
		self.imgHeight =  self.image.getbbox()[3]
		return True
	
	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

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

	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

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
	
	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

	def debugMessage(self,arg) :

		if(self.debug) : print(arg)		

	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
	
	def presentImage(self) :
		global frame, count, xOffset, yOffset, dX, dY, image, panRangeLimit, scrollSpeed, useJitter, useBlink, imageCopy, presentTime	
		imageCopyTemp = imageCopy
		enhancer = ImageEnhance.Brightness(imageCopyTemp)
		imageCopyTemp = enhancer.enhance(brightnessFactor)
		config.render(imageCopyTemp, int(xOffset), int(yOffset), imageCopy.size[0], imageCopy.size[1], False)
		config.actions.drawBlanks()
		time.sleep(presentTime)
	
	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

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
	
	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
	
	def fillColor(self,force=False) :
		global bgFillColor
		if(random.random() > .8 or force) :
			config.matrix.Fill(bgFillColor)
		else :
			config.matrix.Fill(bgFillColor)
	
	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

	def rotateImage(self,angle) :
		global image, matrix
		image = config.image.resize((32,32))
		image = image.rotate(angle, Image.BICUBIC, 1);		
		config.matrix.Clear()
		config.matrix.SetImage(config.image.im.id, -8, -8)

	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
	
	def animate(self, randomizeTiming = False, frameLimit = 3) :

		# This needs fixing  - currently requires extra frame
		# at end of gif  --

		skipTime = False
		#************************************#
		### DRAW THE IMAGE ACROSS ALL PANELS
		#imageCopy = image.point(lambda p: p * 0.19)
		'''
		self.imageCopy.paste(self.image)
		#print(imageCopy,image,xOffset,yOffset)

		if(self.brightnessFlux) :
			rate+=math.pi/self.brightnessFluxRate;
			brightnessFactor = (math.sin(rate) + 1) / 2 + .01
			#if(brightnessFactor > 1) : brightnessFactor = 1
			#if(brightnessFactor < 0) : brightnessFactor = .00001
		enhancer = ImageEnhance.Brightness(self.imageCopy)
		imageCopy = enhancer.enhance(self.brightnessFactor)
		'''
		
		try:
			self.image.seek(self.image.tell() + 1)
		except EOFError:
			self.image.seek(0)
			#print("fail", frame)
			skipTime = True
			pass

		self.frameCount += 1

		if (self.config.useImageFilter) : self.filterize()
		self.augment()

		'''
		if(skipTime == False) :
			if(randomizeTiming) :
				time.sleep(random.uniform(.02,.08))
				if(random.random() > .98) :
					time.sleep(random.uniform(.05,2))
			else :
				time.sleep(self.gifPlaySpeed)
		'''
		#if (frame == frameLimit):frame = 0
		
	def playImage(self, randomizeTiming = False, frameLimit = 3):
		global config
		animate(randomizeTiming, frameLimit)

	
	
###############################	