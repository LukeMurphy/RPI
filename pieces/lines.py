import time
import random
import math
import datetime
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageEnhance, ImageChops
from modules import colorutils, coloroverlay
import argparse

class Line:
	
	pointArray = []
	stepSize = 5

	lastPoint  = [0,0]
	nextPoint  = [0,0]

	done = False
	branchCount = 0

	lineColor = (200,200,200)

	lineNumber  = 0


	def __init__(self, config, setLineAttributes = True):

		self.config = config
		self.segmentLength = 2
		self.direction = -1 if random.random() > .5 else 1
		self.direction = 1
		self.pointArray = [[0,0]]
		if setLineAttributes == True : self.setLineAttributes()

	def reset(self):
		self.done = False
		self.pointArray = [[0,0]]
		self.setLineAttributes()

	def setLineAttributes(self):
		#print("new")
		self.angle = random.uniform(0,math.pi * 2)

		if self.config.angleIncrement == 0 :
			self.angleIncrement = 0
		else :
			angleIncrementDirection = 1 if random.random() > .5 else -1
			self.angleIncrement = angleIncrementDirection * math.pi/ self.config.angleIncrement


		side = -1

		self.branchCount = 0

		x = (random.uniform(0, config.canvasWidth))
		y = (random.uniform(0, config.canvasHeight))

		r = round(random.uniform(0,3))
		while side == r :
			r = round(random.uniform(0,3))

		side = r

		# TOP BOTTOM RIGHT LEFT
		if side == 0 :
			y = 0
		if side == 1 :
			y = self.config.canvasHeight			

		if side == 2 :
			x = self.config.canvasWidth

		if side == 3 :
			x = 0

		self.lastPoint = [x,y]
		self.nextPoint = [x,y]



	def calculateNextPoint(self):
		self.nextPoint[0] = (self.lastPoint[0] + self.segmentLength * math.cos(self.angle) * self.direction);
		self.nextPoint[1] = (self.lastPoint[1] + self.segmentLength * math.sin(self.angle) * self.direction);
		self.angle += self.angleIncrement

	def drawLine(self):

		if self.done == False:
			
			x0 = self.lastPoint[0]
			y0 = self.lastPoint[1]

			self.calculateNextPoint()

			x1 = self.nextPoint[0]
			y1 = self.nextPoint[1]

			if len(self.pointArray) > 3:
				rng = self.segmentLength/2
				xNP = self.nextPoint[0]
				yNP = self.nextPoint[1]

				for i in self.config.pointArray :
					x = i[0] 
					y = i[1]

					if xNP > x - rng and xNP < x + rng and yNP > y - rng and yNP < y + rng :
					#if xNP in range(x - rng, x + rng) and yNP in range(y - rng, y + rng):
						self.done = True
						break


			if self.done  ==  False :	

				"********************************************************************"
				#self.config.canvasDraw.line((x0,y0,x1,y1), fill=self.lineColor)
				s = 2
				dx = x1 - x0
				dy = y1 - y0
				l = math.sqrt(dx*dx + dy*dy)
				s = l + 100
				
				self.config.canvasDraw.rectangle((x0,y0,x1 + s,y1 + s), fill=self.lineColor)
				self.config.canvasDraw.ellipse((x0,y0,x0 + s,y0 + s), fill=self.lineColor)


				"********************************************************************"

				p = [(self.lastPoint[0]), (self.lastPoint[1])]
				if p not in self.pointArray :
					self.pointArray.append(p)
				self.lastPoint = self.nextPoint

			if x1 > self.config.canvasWidth or x1 < 0 :
				self.done = True
			if y1 > self.config.canvasHeight or y1 < 0 :
				self.done = True



def getColorChanger():
	colOverlay = coloroverlay.ColorOverlay()
	colOverlay.randomSteps = False 
	colOverlay.timeTrigger = True 
	colOverlay.tLimitBase = 10 
	colOverlay.maxBrightness = config.brightness
	colOverlay.steps = 50
	return colOverlay


def showLines():
	global config

	for i in range(0, len(config.linesArray)) :

		ref = config.linesArray[i]

		if ref.done == False :
			ref.drawLine()

			if len(ref.pointArray) > config.activeLineInterceptLimit :
				for p in ref.pointArray:
					pr = [round(p[0]), round(p[1])]
					if pr not in config.pointArray : config.pointArray.append(pr)
		else :
			
			# it's done, so add the points it has traced to the global "used" points array
			for p in ref.pointArray:
				pr = [round(p[0]), round(p[1])]
				if pr not in config.pointArray : config.pointArray.append(pr)

			# start anew line altogether
			if ref.branchCount > config.branchCountLimit : 
				config.linesArray[i].reset()
				config.linesArray[i].lineColor = colorutils.randomColor()
				config.lineCount += 1
				#config.stop = True

			# Branch a line
			else:
				point =  (round(len(ref.pointArray)/2))
				currentAngle = ref.angle
				midPoint = config.linesArray[i].pointArray[point]
				
				# inherited line
				if random.random() < config.branchProb :
					config.linesArray[i].angle = currentAngle - math.pi/2
					config.linesArray[i].lastPoint = midPoint
					config.linesArray[i].done = False
					config.linesArray[i].lineNumber = ref.lineNumber
					config.linesArray[i].lineColor = ref.lineColor
					config.linesArray[i].branchCount = ref.branchCount + 1
					config.lineCount += 1

				if len(config.linesArray) < config.trimLimit and random.random() < config.doubleBranchProb:
					newLine = Line(config)
					newLine.angle = currentAngle + math.pi/2
					newLine.lastPoint = midPoint
					newLine.done = False
					#newLine.lineNumber = ref.lineNumber
					newLine.lineColor = ref.lineColor
					newLine.branchCount = ref.branchCount + 2
					config.linesArray.append(newLine)
					config.lineCount += 1


	config.image.paste(config.canvasImage, (0,0), config.canvasImage)
	config.render(config.image, round(config.imageOffsetX), round(config.imageOffsetY))

	if len(config.linesArray) >= config.trimLimit :
		for i in range(0, config.trim) :
			config.linesArray.pop()

	if config.lineCount > config.lineCountLimit :
		config.stop = True




def main(run = True) :
	global config, directionOrder
	print("---------------------")
	print("Screen Loaded")

	colorutils.brightness = config.brightness

	config.delay = float(workConfig.get("lines", 'delay'))
	config.base = float(workConfig.get("lines", 'base'))
	config.rows = int(workConfig.get("lines", 'rows'))
	config.cols = int(workConfig.get("lines", 'cols'))


	config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	config.draw = ImageDraw.Draw(config.image)
	config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.canvasDraw = ImageDraw.Draw(config.canvasImage)

	config.imageOffsetX = 0
	config.imageOffsetY = 0

	config.trim = 4
	config.trimLimit = 10
	config.branchProb = .1
	config.doubleBranchProb = .1
	config.angleIncrement = 900
	config.activeLineInterceptLimit = 500
	config.lineCountLimit = 200
	config.segmentLength = 2
	config.branchCountLimit = 3

	config.f1 = getColorChanger()
	config.f2 = getColorChanger()
	config.f3 = getColorChanger()
	config.f4 = getColorChanger()
	config.f5 = getColorChanger()
	config.f6 = getColorChanger()

	config.imageRotation = .0001


	setUp()


def setUp():
	global config

	config.lineCount = 0
	#config.canvasDraw.rectangle((0,0,config.canvasWidth, config.canvasHeight), fill =(50,0,100,100))
	config.pointArray = [[0,0]]
	config.linesArray = []
	config.stop = False

	config.angleIncrement = random.uniform(0,2000)

	#print(config.linesArray)

	for i in range(0,3):
		l = Line(config, False)
		l.lineNumber = i
		l.lineColor = colorutils.randomColor()
		l.segmentLength = config.segmentLength
		l.setLineAttributes()
		#print(l.lastPoint)
		config.linesArray.append(l)
		config.lineCount += 1
	
def runWork():
	global config
	while True:
		iterate()
		time.sleep(config.delay)  


def iterate() :
	global config
	if config.stop == False :
		showLines()
	else :
		setUp()


def callBack() :
	global config
	return True




''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


	




