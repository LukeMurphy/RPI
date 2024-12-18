import datetime
import math
import random
import textwrap
import time

import noise
from noise import *

from modules import colorutils
from PIL import (
	Image,
	ImageChops,
	ImageDraw,
	ImageEnhance,
	ImageFilter,
	ImageFont,
	ImageOps,
)


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
	remove = False
	objWidth = 2
	objHeight = 6
	unitBlur = 0
	meanderFactor = 4
	meanderFactor2 = 90
	meanderDirection = 1
	changeColorOnChange = False
	xWind = 0

	particleWinkOutXMin = 4
	particleWinkOutYMin = 4

	greyRate = 100.0
	greyDeltaRate = [0, 0, 0]
	greyCount = 0
	pixelsGoGray = False
	fillColorRawValues = (0, 0, 0, 0)
	outlineColorRawValues = (0, 0, 0, 0)
	extraOutlineColor = None

	# gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

	def __init__(self, particleSystemRef):
		super(Particle, self).__init__()
		self.ps = particleSystemRef
		self.xPos = 0
		self.yPos = 0

		self.xPosR = 0  # self.ps.config.canvasWidth/2
		self.yPosR = 0  # self.ps.config.canvasHeight/2
		self.move = True

		self.dx = 0
		self.dy = 0

		self.v = random.uniform(1, 3)
		self.direction = 0

		"""
		self.fillColor = colorutils.getSunsetColors(self.ps.config.brightness)
		self.outlineColor = colorutils.getSunsetColors(self.ps.config.brightness)
		

		self.fillColor = (round(random.uniform(200,250)), round(random.uniform(15,195)), round(random.uniform(15,155)))
		self.outlineColor = (round(random.uniform(200,250)), round(random.uniform(15,195)), round(random.uniform(15,155)))
		
		self.fillColor = colorutils.getRandomRGB()
		"""
		self.fillColor = colorutils.randomColor(self.ps.config.brightness)
		self.outlineColor = colorutils.getSunsetColors(self.ps.config.brightness / 2)
		self.imageDrawn = False

		# if(random.random() < .2) : self.fillColor = (100,10,0)

	def setUpParticle(self):


		rndSize = random.uniform(self.ps.rndSizeFactorMin, self.ps.rndSizeFactorMax)

		self.objWidth = round(self.objWidth * rndSize)
		self.objHeight = round(self.objHeight * rndSize)

		self.unitBlur = self.ps.unitBlur

		self.meanderFactor = random.uniform(.1, 1.0) * self.ps.meanderFactor
		self.meanderFactor2 = random.uniform(.1, 1.0) * self.ps.meanderFactor2

		self.remove = False

		self.greyCount = 0

		if self.ps.objType == "image":
			if self.ps.objImageColorize == True:
				overlayImage = Image.new(
					"RGBA",
					(self.ps.loadedImageCopy.width, self.ps.loadedImageCopy.height),
				)
				overlayImageDraw = ImageDraw.Draw(overlayImage)
				overlayImageDraw.rectangle(
					(
						0,
						0,
						self.ps.loadedImageCopy.width,
						self.ps.loadedImageCopy.height,
					),
					fill=colorutils.randomColorAlpha(self.ps.config.brightness),
				)

				"""
				This variant is interesting - puts a few rectangles with faded thumbsup image and more grayscale - slightly less pretty

				self.baseImage = Image.blend(self.ps.loadedImageCopy.convert("RGBA"), overlayImage, alpha = random.random())

				an alpha value of .25 makes for a more early italian renaissance kind of look
				"""
				self.baseImage = Image.blend(
					self.ps.loadedImageCopy,
					overlayImage,
					alpha=self.ps.objImageAlphaBlend,
				)
			else:
				self.baseImage = self.ps.loadedImageCopy.copy()

			if random.random() < self.ps.objImageFlipRate:
				self.baseImage = self.baseImage.transpose(Image.FLIP_LEFT_RIGHT)

			if random.random() < self.ps.objImageRotateRate:
				self.baseImage = self.baseImage.rotate(180)

		self.createParticleImage()

	def createParticleImage(self):

		self.image = Image.new(
			"RGBA", (round(self.objWidth) + 2, round(self.objHeight) + 2)
		)
		self.draw = ImageDraw.Draw(self.image)
		self.imageDrawn = True


	def travel(self):
		self.direction += self.directionIncrement * self.ps.clumpingFactor

		self.dy = self.v * math.sin(self.direction)
		self.dx = self.v * math.cos(self.direction)

		vy = self.v * math.sin(self.direction)
		vx = self.v * math.cos(self.direction)

		vy += self.ps.yGravity
		vx += self.ps.xGravity

		newV = math.sqrt(vx * vx + vy * vy)

		newDirection = math.atan2(vy, vx)

		if self.ps.useFlocking == False:
			self.direction = newDirection

		self.xPos += self.dx
		self.yPos += self.dy

		self.xPosR += self.dx
		self.yPosR += self.dy


	def linearMotion(self):

		self.dy = self.v * math.sin(self.direction)
		self.dx = self.v * math.cos(self.direction)

		vy = self.v * math.sin(self.direction)
		vx = self.v * math.cos(self.direction)

		self.xPos += self.dx
		self.yPos += self.dy

		self.xPosR += self.dx
		self.yPosR += self.dy


	def meander(self):

		self.direction += self.directionIncrement * self.ps.clumpingFactor


		if self.ps.meanderDirection == 1 :
			self.dx = self.v * math.cos(self.direction)
			# self.dx = self.v * math.cos(self.direction)

			self.dy = (
				
				self.meanderFactor
				* noise.pnoise1(self.ps.config.canvasWidth-self.xPos / self.meanderFactor2, 1)
				+ self.xWind
			)
		else :
			self.dy = self.v * math.sin(self.direction)
			# self.dx = self.v * math.cos(self.direction)

			self.dx = (
				
				self.meanderFactor
				* noise.pnoise1(self.yPos / self.meanderFactor2, 1)
				+ self.xWind
			)

		vy = self.v * math.sin(self.direction)
		vx = self.v * math.cos(self.direction)

		vy += self.ps.yGravity
		# vx += self.ps.xGravity

		newV = math.sqrt(vx * vx + vy * vy)

		newDirection = math.atan2(vy, vx)

		if self.ps.useFlocking == False:
			self.direction = newDirection

		self.xPos += self.dx
		self.yPos += self.dy

		self.xPosR += self.dx
		self.yPosR += self.dy


	def checkForBorderCollisions(self):
		if self.ps.borderCollisions == True:
			collide = False

			if self.xPosR > self.ps.config.canvasWidth + self.objWidth:
				self.v *= self.ps.collisionDamping
				self.changeColor()
				if self.ps.useFlocking == True:
					self.direction -= math.pi
				else:
					self.direction = math.pi - self.direction
				if self.ps.expireOnExit == True:
					self.remove = True
				else:
					self.xPosR = self.ps.config.canvasWidth - self.objWidth
					self.xPos = self.ps.config.canvasWidth - self.objWidth

			if self.xPosR < -3 * self.objWidth:
				self.v *= self.ps.collisionDamping
				self.changeColor()
				if self.ps.useFlocking == True:
					self.direction -= math.pi
				else:
					self.direction = math.pi - self.direction
				if self.ps.expireOnExit == True:
					self.remove = True
				else:
					self.xPosR = 0
					self.xPos = 0

			if (
				self.yPosR > self.ps.config.canvasHeight + self.objHeight
				and self.ps.ignoreBottom == False
			):
				self.v *= self.ps.collisionDamping
				self.changeColor()
				if self.ps.useFlocking == True:
					self.direction -= math.pi
				else:
					self.direction = 2 * math.pi - self.direction
				if self.ps.expireOnExit == True:
					self.remove = True
				else:
					self.yPosR = self.ps.config.canvasHeight - self.objHeight
					self.yPos = self.ps.config.canvasHeight - self.objHeight

			if self.yPosR < -1 * self.objHeight:  # -3 * self.objHeight
				self.v *= self.ps.collisionDamping
				self.changeColor()
				if self.ps.useFlocking == True:
					self.direction -= math.pi
				else:
					self.direction = 2 * math.pi - self.direction
				if self.ps.expireOnExit == True:
					self.remove = True
				else:
					self.yPosR = 0
					self.yPos = 0

		else:
			if self.xPosR > self.ps.config.canvasWidth:
				self.xPosR = 0
				self.xPos = 0
				self.changeColor()
			if self.yPosR > self.ps.config.canvasHeight:
				self.yPosR = 0
				self.yPos = 0
				self.changeColor()

			if self.xPosR < 0:
				self.xPosR = self.ps.config.canvasWidth
				self.xPos = self.ps.config.canvasWidth
				self.changeColor()

			if self.yPosR < 0:
				self.yPosR = self.ps.config.canvasHeight
				self.yPos = self.ps.config.canvasHeight
				self.changeColor()


	def update(self):

		if self.ps.movement == "travel":
			self.travel()

		if self.ps.movement == "fire":
			self.meander()

		if self.ps.movement == "linearMotion":
			self.linearMotion()

		self.checkForBorderCollisions()

		if self.ps.movement != "linearMotion":
			self.directionIncrement *= self.ps.cohesionDegrades
			self.v *= self.ps.damping

		if self.ps.movement == "fire":
			self.objWidth *= self.ps.widthRate
			self.objHeight *= self.ps.heightRate

			if self.objWidth < self.particleWinkOutXMin:
				self.objWidth = 0
				self.objHeight = 0
				self.remove = True
			if self.objHeight < self.particleWinkOutYMin:
				self.objHeight = 0
				self.objWidth = 0
				self.remove = True

		if self.ps.useFlocking == True:
			self.checkMyBuddies()




	def isBetween(self, n, a, b, d=0) :
		if n >= (a - d) and n <= (b + d) :
			return True
		else :
			return False


	def render(self):
		if self.remove != True:
			xPos = int(self.xPosR - self.image.size[0] / 2)
			yPos = int(self.yPosR - self.image.size[1] / 2)

			self.createParticleImage()

			if self.pixelsGoGray == True:

				'''
				# REALLY this should be outlineColorRawValues being changed
				# but it seems to look better like this

				self.OutlineR += self.outlineGreyRate[0]
				self.OutlineG += self.outlineGreyRate[1]
				self.OutlineB += self.outlineGreyRate[2]

				#outlineColorRawValues = (r, g, b, self.fillColor[3])
				
				self.outlineColor = (
					round(self.OutlineR),
					round(self.OutlineG),
					round(self.OutlineB),
					self.outlineColor[3],
				)

				self.FillR += self.fillGreyRate[0]
				self.FillG += self.fillGreyRate[1]
				self.FillB += self.fillGreyRate[2]
				
				#fillColorRawValues = (r, g, b, self.fillColor[3])
				
				self.fillColor = (round(self.FillR), round(self.FillG), round(self.FillB), self.fillColor[3])
				'''


				# REALLY this should be outlineColorRawValues being changed
				# but it seems to look better like this

				gr_o = round(self.outlineGrey)
				r_o = self.outlineColor[0] + self.outlineGreyRate[0]
				g_o = self.outlineColor[1] + self.outlineGreyRate[1]
				b_o = self.outlineColor[2] + self.outlineGreyRate[2]

				rr_o = round(r_o)
				rb_o = round(b_o)
				rg_o = round(g_o)


				if self.isBetween(rr_o, gr_o, gr_o, abs(round(self.outlineGreyRate[0]))) : self.outlineGreyRate[0] = 0
				if self.isBetween(rg_o, gr_o, gr_o, abs(round(self.outlineGreyRate[1]))) : self.outlineGreyRate[1] = 0
				if self.isBetween(rb_o, gr_o, gr_o, abs(round(self.outlineGreyRate[2]))) : self.outlineGreyRate[2] = 0


				gr = round(self.fillGrey)
				r = self.fillColorRawValues[0] + self.fillGreyRate[0]
				g = self.fillColorRawValues[1] + self.fillGreyRate[1]
				b = self.fillColorRawValues[2] + self.fillGreyRate[2]

				rr = round(r)
				rb = round(b)
				rg = round(g)


				if self.isBetween(rr, gr, gr, abs(round(self.fillGreyRate[0]))) : self.fillGreyRate[0] = 0
				if self.isBetween(rg, gr, gr, abs(round(self.fillGreyRate[1]))) : self.fillGreyRate[1] = 0
				if self.isBetween(rb, gr, gr, abs(round(self.fillGreyRate[2]))) : self.fillGreyRate[2] = 0


				#if self.jumpToGray == False : 
				self.outlineColorRawValues = (r_o, g_o, b_o, self.outlineColor[3])
				self.outlineColor = (rr_o, rg_o, rb_o, self.outlineColor[3])

				#if self.jumpToGray == False : 
				self.fillColorRawValues = (r, g, b, self.fillColor[3])
				self.fillColor = ( rr, rg, rb, self.fillColor[3])

				'''
				if self.fillGreyRate[0] == 0 and self.fillGreyRate[1] == 0 and self.fillGreyRate[2] == 0 :
					print("d0ne", self.fillGrey)
					self.outlineColor = (
						round(self.outlineGrey),
						round(self.outlineGrey),
						round(self.outlineGrey),
						self.outlineColor[3],
					)
					self.fillColor = (
						round(self.fillGrey),
						round(self.fillGrey),
						round(self.fillGrey),
						self.fillColor[3],
					)
				'''

			if self.ps.objType == "poly":
				xPos = int(self.xPosR - self.image.size[0] / 1.5)
				yPos = int(self.yPosR - self.image.size[1] / 2)
				self.drawPoly()

			elif self.ps.objType == "ellipse":
				self.drawOval()

			elif self.ps.objType == "image":
				self.drawImage()

			else:
				self.drawRectangle()

			imageToPaste = self.image

			if self.ps.movement == "travel" and self.ps.objType != "other":

				angle = 180
				imageToPaste = self.image.rotate(angle, expand=True)
				angle = 90 - math.degrees(self.direction)
				imageToPaste = self.image.rotate(angle, expand=True)

			if self.ps.unitBlur > 0:
				imageToPaste = imageToPaste.filter(
					ImageFilter.GaussianBlur(radius=round(self.unitBlur))
				)
                # This should be optional
				# self.unitBlur += 1

			### This produces trails
			if self.ps.objTrails == True:
				self.ps.config.image.paste(imageToPaste, (xPos, yPos))
			else:
				self.ps.config.image.paste(imageToPaste, (xPos, yPos), imageToPaste)

	def drawPoly(self):

		h = self.objWidth
		b = self.objWidth
		c = self.objHeight  # "height"

		poly = []
		poly.append((round(h) - 0, 0))
		poly.append((round(h) - 4, round(c / 4)))
		poly.append((round(h) - 6, round(c / 3)))
		poly.append((round(h) - 4, round(c / 2)))
		poly.append((round(h) - 0, round(c / 2)))
		poly.append((round(h) + 4, round(c / 3)))
		poly.append((round(h) + 6, round(c / 4)))
		poly.append((round(h) + 4, round(c / 2)))
		self.draw.polygon(poly, fill=self.fillColor, outline=self.outlineColor)

		poly2 = []
		poly2.append((round(h) + -0, 0))
		poly2.append((round(h) + 4, -8))
		poly2.append((round(h) + 4, 8))
		self.draw.polygon(poly2, fill=self.fillColor, outline=None)

		# self.draw.rectangle((0, 0, round(self.objWidth) ,round(self.objHeight)), fill=self.fillColor, outline=self.outlineColor)

	def drawImage(self):
		img = self.baseImage.resize((round(self.objWidth), round(self.objHeight)))
		self.image.paste(img, (0, 0), img)

	def drawOval(self):
		# self.draw.ellipse((0, 0, round(self.objWidth/2) ,round(self.objHeight/2)),
		#     fill=self.fillColor, outline=self.outlineColor)
		box = [(0, 0), (self.objWidth / 2 + 1, self.objHeight / 2 + 1)]
		self.draw.chord(box, 0, 360, fill=self.fillColor, outline=self.outlineColor)

	def drawRectangle(self):
		
		self.draw.rectangle(
			(0, 0, round(self.objWidth), round(self.objHeight)),
			fill=self.fillColor,
			outline=self.outlineColor,
		)
		
		if self.extraOutlineColor != None :
			self.draw.rectangle(
				(1, 1, round(self.objWidth-1), round(self.objHeight-1)),
				fill=None,
				outline=self.extraOutlineColor,
			)

	def changeColor(self):
		if self.changeColorOnChange == True:
			self.fillColor = colorutils.randomColor(random.random())
			self.outlineColor = colorutils.getRandomRGB()
			# if(random.random() > .5): self.dx = (4 * random.random() + 2)
			# if(random.random() > .5): self.dy = (4 * random.random() + 2)
			# if(random.random() > .5): self.objWidth = int(random.uniform(self.objWidthMin,self.objWidthMax))

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

		for pal in ps.unitArray:
			if self != pal:
				dx = self.xPosR - pal.xPosR
				dy = self.yPosR - pal.yPosR
				distance = math.sqrt(dx * dx + dy * dy)
				if distance < ps.cohesionDistance:
					## Find center of pals
					centerX += pal.xPosR
					centerY += pal.yPosR
					count += 1
					distianceProportion = 1  # ( distance/ps.cohesionDistance)
					#distianceProportion = 1 - distance / ps.cohesionDistance 
					## Get your pals average direction
					if distance < ps.cohesionDistance and distance > ps.repelDistance:
						directionTotal += pal.direction * distianceProportion
					## Get your pals average direction but back off
					if distance < ps.cohesionDistance and distance < ps.repelDistance:
						directionTotal -= (
							pal.direction * distianceProportion * ps.repelFactor
						)

		if count > 1:
			directionTotal = directionTotal / count
			self.directionIncrement = directionTotal - self.direction

		if count == 1:
			self.directionIncrement *= ps.cohesionDegrades


		if random.random() < .01 :
			self.direction = random.uniform(-math.pi,math.pi)

		'''
		if count > 20:
			dx = self.xPosR - centerX / count
			dy = self.yPosR - centerY / count

			if dx == 0:
				angle = -self.direction
			else:
				angle = math.atan(dy / dx)
		'''

			# self.directionIncrement += (angle - self.direction) / ps.clumpingFactor * 10
