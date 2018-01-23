import time
import random
import textwrap
import math
import datetime
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageEnhance, ImageChops
from modules import colorutils

class Particle(object):
	

	vx = 0
	vy = 0
	vz = 0
	
	x = 0
	y = 0
	z = 0

	direction = 0
	angle = 0

	dxIncremental = 0
	dyIncremental = 0
	directionIncrement = 0


	changeColorOnChange = False

	def __init__(self, particleSystemRef):
		super(Particle, self).__init__()
		self.ps = particleSystemRef
		self.xPos = 0
		self.yPos = 0

		self.xPosR = 0 #self.ps.config.screenWidth/2
		self.yPosR = 0 #self.ps.config.screenHeight/2
		self.move = True
		
		self.dx = 0
		self.dy = 0

		self.v = random.uniform(1,3)
		self.direction = 0

		self.objWidth = 2
		self.objHeight = 5

		self.image = Image.new("RGBA", (self.objWidth , self.objHeight))
		self.draw = ImageDraw.Draw(self.image)
		self.fillColor = colorutils.getRandomRGB()
		self.outlineColor = colorutils.getRandomRGB(self.ps.config.brightness)
		self.fillColor = colorutils.getSunsetColors(self.ps.config.brightness)
		self.outlineColor = colorutils.getSunsetColors(self.ps.config.brightness)

	def update(self):

		self.direction += self.directionIncrement * self.ps.clumpingFactor

		self.dx = self.v * math.sin(self.direction)
		self.dy = self.v * math.cos(self.direction)

		self.xPos += self.dx
		self.yPos += self.dy
		
		self.xPosR += self.dx
		self.yPosR += self.dy

		#self.directionIncrement *= self.ps.cohesionDegrades
		

		if(self.ps.borderCollisions ==  True) :

			if(self.xPosR + self.objWidth > self.ps.config.screenWidth) : 
				self.xPosR = self.ps.config.screenWidth - self.objWidth 
				self.xPos = self.ps.config.screenWidth - self.objWidth 
				self.changeColor()
				self.direction -= math.pi
			if(self.yPosR + self.objWidth> self.ps.config.screenHeight) : 
				self.yPosR = self.ps.config.screenHeight-self.objWidth 
				self.yPos = self.ps.config.screenHeight-self.objWidth 
				self.changeColor()
				self.direction -= math.pi
			if(self.xPosR < 0) : 
				self.xPosR = 0
				self.xPos = 0
				self.changeColor()
				self.direction -= math.pi
			if(self.yPosR < 0) : 
				self.yPosR = 0
				self.yPos = 0
				self.changeColor()
				self.direction -= math.pi
		else :
			if(self.xPosR  > self.ps.config.screenWidth) : 
				self.xPosR = 0
				self.xPos = 0
				self.changeColor()
			if(self.yPosR > self.ps.config.screenHeight) : 
				self.yPosR = 0 
				self.yPos = 0 
				self.changeColor()

			if(self.xPosR < 0) : 
				self.xPosR = self.ps.config.screenWidth
				self.xPos = self.ps.config.screenWidth
				self.changeColor()

			if(self.yPosR < 0) : 
				self.yPosR = self.ps.config.screenHeight
				self.yPos = self.ps.config.screenHeight
				self.changeColor()

		
		self.v *= self.ps.damping
		self.dx += self.ps.xGravity
		self.dy += self.ps.yGravity	

		self.checkMyBuddies()

	def render(self):
		xPos = int(self.xPosR)
		yPos = int(self.yPosR)

		if(self.dy == 0) :
			self.angle = 0
		else :
			self.angle = self.dx/self.dy
		#self.direction = math.atan(self.angle) * 180 / math.pi

		'''
		self.ps.config.draw.rectangle((xPos, yPos,xPos+ self.objHeight , yPos +self.objWidth ), 
			fill=self.fillColor, outline=self.outlineColor)
		'''
		self.draw.rectangle((0, 0, self.objWidth ,self.objHeight), 
			fill=self.fillColor, outline=self.outlineColor)
		imageToPaste = self.image.rotate(self.direction * 180/math.pi, expand=True)
		self.ps.config.image.paste(imageToPaste, (xPos,yPos))


	def changeColor(self):
		if(self.changeColorOnChange == True) :
			self.fillColor = colorutils.randomColor(random.random())
			self.outlineColor = colorutils.getRandomRGB()
			#if(random.random() > .5): self.dx = (4 * random.random() + 2)
			#if(random.random() > .5): self.dy = (4 * random.random() + 2)
			#if(random.random() > .5): self.objWidth = int(random.uniform(self.objWidthMin,self.objWidthMax)) 

	def checkMyBuddies(self):

		total = len(self.ps.unitArray)
		dxTotal = self.dx
		dyTotal = self.dy
		directionTotal = self.direction
		count = 1
		ps = self.ps
		distance = 0
		centerX = self.xPosR
		centerY = self.yPosR

		for pal in (ps.unitArray):
			if self != pal :
				dx  = self.xPosR - pal.xPosR
				dy  = self.yPosR - pal.yPosR
				distance = math.sqrt(dx*dx + dy*dy)
				if(distance < ps.cohesionDistance) :
					## Find center of pals
					centerX += pal.xPosR
					centerY += pal.yPosR
					count += 1
					distianceProportion = 1 #( distance/ps.cohesionDistance) 
					## Get your pals average direction
					if(distance < ps.cohesionDistance and distance > ps.repelDistance) :
						directionTotal += pal.direction * distianceProportion
					## Get your pals average direction but back off 
					if(distance < ps.cohesionDistance and distance < ps.repelDistance ) :
						directionTotal -= pal.direction * distianceProportion * ps.repelFactor

		if(count > 1) :
			directionTotal = directionTotal / count
			self.directionIncrement = (directionTotal - self.direction) 

		if(count == 1) :
			self.directionIncrement *= ps.cohesionDegrades

		if(count > 5) :
			dx = self.xPosR - centerX / count
			dy = self.yPosR - centerY / count

			if(dx == 0) :
				angle = -self.direction
			else :
				angle = math.atan(dy/dx)

			#self.directionIncrement += (angle - self.direction) / ps.clumpingFactor * 10












