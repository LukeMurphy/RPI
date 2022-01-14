import argparse
import datetime
import math
import random
import time
from modules.configuration import bcolors
from modules import coloroverlay, colorutils
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFont, ImageOps


class Line:

	pointArray = []
	stepSize = 5

	lastPoint = [0, 0]
	nextPoint = [0, 0]

	done = False
	branchCount = 0

	lineColor = (200, 200, 200)

	lineNumber = 0

	# widthMultiplier = 18

	def __init__(self, config, setLineAttributes=True):

		self.config = config
		self.segmentLength = self.config.segmentLength
		self.direction = -2 if random.random() > 0.5 else 2
		#self.direction = 2
		self.pointArray = [[0, 0]]
		self.widthMultiplier = self.config.widthMultiplier
		if setLineAttributes == True:
			self.setLineAttributes()

	def reset(self):
		self.done = False
		self.pointArray = [[0, 0]]
		self.setLineAttributes()


	def setLineAttributes(self):
		# print("new")
		self.angle = random.uniform(-math.pi / 2, math.pi/2)

		if self.config.angleIncrement == 0:
			self.angleIncrement = 0
		else:
			angleIncrementDirection = 1 if random.random() > 0.5 else -1
			self.angleIncrement = (
				angleIncrementDirection * math.pi / self.config.angleIncrement
			)

		side = -1

		self.branchCount = 0

		x = random.uniform(0, config.canvasWidth)
		y = random.uniform(0, config.canvasHeight)


		r = round(random.uniform(0, 3))
		while side == r:
			r = round(random.uniform(0, 3))

		side = r

		'''
		# TOP BOTTOM RIGHT LEFT
		if side == 0:
			y = 0 - self.widthMultiplier + 2
		if side == 1:
			y = self.config.canvasHeight + self.widthMultiplier - 2

		if side == 2:
			x = self.config.canvasWidth + self.widthMultiplier - 2

		if side == 3:
			x = 0 - self.widthMultiplier + 2
		'''

		self.lastPoint = [x, y]
		self.nextPoint = [x, y]

	def calculateNextPoint(self):
		self.nextPoint[0] = (
			self.lastPoint[0]
			+ self.segmentLength * math.cos(self.angle) * self.direction
		)
		self.nextPoint[1] = (
			self.lastPoint[1]
			+ self.segmentLength * math.sin(self.angle) * self.direction
		)
		self.angle += self.angleIncrement

	def drawLine(self):

		if self.done == False:

			x0 = self.lastPoint[0]
			y0 = self.lastPoint[1]

			self.calculateNextPoint()

			x1 = self.nextPoint[0]
			y1 = self.nextPoint[1]

						

		#if self.done == False:

		"********************************************************************"
		s = 2
		dx = x1 - x0
		dy = y1 - y0
		l = math.sqrt(dx * dx + dy * dy)
		s = l * self.widthMultiplier / (self.branchCount / 2 + 1)

		if s < 4:
			s = 4

		#self.config.canvasDraw.rectangle((x0,y0,x1 + s,y1 + s), fill=self.lineColor)
		'''
		self.config.canvasDraw.ellipse(
			(x0, y0, x0 + s, y0 + s), fill=self.lineColor
		)
		'''
		#self.config.canvasDraw.line((x0,y0,x1,y1), fill=self.lineColor)
		w = (config.initWidth -  self.branchCount) * .75


		if w <= 1 : w = 1
		angle = math.atan2(dy,dx)
		angle2 = -math.pi/2 + angle
		x0b = x0 + w * math.cos(angle2) * w
		y0b = y0 + w * math.sin(angle2) * w
		
		x1b = x1 + w * math.cos(angle2) * w
		y1b = y1 + w * math.sin(angle2) * w
		

		tempImage = Image.new("RGBA", (config.screenWidth, config.screenHeight))
		tempImageDraw = ImageDraw.Draw(tempImage)
		tempImageDraw.polygon(((x0,y0),(x1,y1),(x1b,y1b),(x0b,y0b)), outline=None, fill= self.lineColor)

		config.canvasImage.paste(tempImage,(0,0), tempImage)
		"********************************************************************"

		p = [round(self.lastPoint[0]), round(self.lastPoint[1])]
		#if p not in self.pointArray:
		self.pointArray.append(p)


		self.lastPoint = self.nextPoint

		if (
			x1 > self.config.canvasWidth + self.widthMultiplier + 3
			or x1 < 0 - self.widthMultiplier - 3
		):
			self.done = True
		if (
			y1 > self.config.canvasHeight + self.widthMultiplier + 3
			or y1 < 0 - self.widthMultiplier - 3
		):
			self.done = True

		if len(self.pointArray) > 3:
			rng = self.segmentLength / 1
			xNP = self.nextPoint[0]
			yNP = self.nextPoint[1]

			for i in self.config.pointArray:
				x = i[0]
				y = i[1]

				if (
					xNP > x - rng
					and xNP < x + rng
					and yNP > y - rng
					and yNP < y + rng
				):
					# if xNP in range(x - rng, x + rng) and yNP in range(y - rng, y + rng):
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

	numberOfLines =  len(config.linesArray)
	newLines = []

	for i in range(0, numberOfLines):
		ref = config.linesArray[i]

		if ref.done == False:
			ref.drawLine()

			if len(ref.pointArray) < config.activeLineInterceptLimit:
				for p in ref.pointArray:
					pr = [round(p[0]), round(p[1])]
					if pr not in config.pointArray:
						config.pointArray.append(pr)


	for i in range(0, numberOfLines):
		ref = config.linesArray[i]
		currentAngle = ref.angle


		# Branch a line
		if ref.done == True and ref.branchCount < config.branchCountLimit:
			l = len(ref.pointArray)
			if l >=1 :
				point = round(l / 2)
				midPoint = ref.pointArray[point]
				lastPoint = ref.pointArray[l-1]

				ref.pointArray = []

				#if random.random() < config.branchAtTipProb :
				#	midPoint = lastPoint

				# inherited line now starts at mid point
				if random.random() < config.branchProb:
					# split off at right angle
					'''
					'''
					ref.angle = currentAngle + math.pi/2  + random.uniform(-math.pi / 8,math.pi / 8)
					if random.random() < .5 :
						ref.angle = currentAngle - math.pi/2  + random.uniform(-math.pi / 8,math.pi / 8)
					ref.lastPoint = midPoint
					ref.nextPoint = midPoint
					ref.done = False
					ref.lineNumber = ref.lineNumber + 1
					ref.lineColor = ref.lineColor
					ref.branchCount = ref.branchCount + 1
					config.lineCount += 1
					if random.random() < config.doubleBranchProb and len(config.linesArray) < config.simultaneousLines:

						newLines.append([currentAngle - math.pi / 2,lastPoint,ref.lineColor,ref.branchCount + 1,ref.lineNumber + 1,2])
					#newLines.append([currentAngle - math.pi /2,midPoint,ref.lineColor,ref.branchCount + 2,ref.lineNumber + 2,2])


			# start anew line altogether
			if ref.branchCount >= config.branchCountLimit:
				ref.reset()
				ref.lineColor = colorutils.randomColorAlpha(1.0,50,255)
				config.lineCount += 1
				# config.stop = True

	for l in newLines :
		newLine = Line(config, False)
		newLine.setLineAttributes()
		newLine.angle = l[0]
		newLine.lastPoint = l[1]
		newLine.nextPoint = l[1]
		newLine.done = False
		newLine.lineNumber = l[4]
		newLine.lineColor = l[2]
		newLine.branchCount = l[3]
		newLine.direction = l[5]
		config.linesArray.append(newLine)
		config.lineCount += 1


	config.image.paste(config.canvasImage, (0, 0), config.canvasImage)
	config.render(config.image, round(config.imageOffsetX), round(config.imageOffsetY))

	n=0
	for l in config.linesArray:
		if l.done == True :
			config.linesArray.pop(n)
		n+=1

	'''
	if numberOfLines >= config.trimLimit:
		for i in range(0, config.trim):
			config.linesArray.pop()
	'''
	if config.lineCount > config.lineCountLimit:
		config.stop = True


def main(run=True):
	global config, directionOrder
	print("---------------------")
	print("Lines Loaded")

	colorutils.brightness = config.brightness

	config.delay = float(workConfig.get("lines", "delay"))
	config.base = float(workConfig.get("lines", "base"))
	config.widthMultiplier = float(workConfig.get("lines", "widthMultiplier"))
	config.rows = int(workConfig.get("lines", "rows"))
	config.cols = int(workConfig.get("lines", "cols"))
	config.bgColorVals = (workConfig.get("lines", "bgColor")).split(",")
	config.bgColor = tuple(
		map(lambda x: int(int(x) * config.brightness), config.bgColorVals)
	)

	config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	config.draw = ImageDraw.Draw(config.image)
	config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.canvasDraw = ImageDraw.Draw(config.canvasImage)

	config.imageOffsetX = 0
	config.imageOffsetY = 0

	config.trim = int(workConfig.get("lines", "trim"))
	config.trimLimit = int(workConfig.get("lines", "trimLimit"))
	config.branchProb = float(workConfig.get("lines", "branchProb"))
	config.branchAtTipProb = float(workConfig.get("lines", "branchAtTipProb"))
	config.doubleBranchProb =float(workConfig.get("lines", "doubleBranchProb"))
	config.angleIncrementMin = int(workConfig.get("lines", "angleIncrementMin"))
	config.angleIncrementMax = int(workConfig.get("lines", "angleIncrementMax"))
	config.activeLineInterceptLimit = int(workConfig.get("lines", "activeLineInterceptLimit"))
	config.lineCountLimit = int(workConfig.get("lines", "lineCountLimit"))
	config.segmentLength = float(workConfig.get("lines", "segmentLength"))
	config.branchCountLimit = int(workConfig.get("lines", "branchCountLimit"))
	config.simultaneousLines = int(workConfig.get("lines", "simultaneousLines"))
	config.initWidth = int(workConfig.get("lines", "initWidth"))

	config.f1 = getColorChanger()
	config.f2 = getColorChanger()
	config.f3 = getColorChanger()
	config.f4 = getColorChanger()
	config.f5 = getColorChanger()
	config.f6 = getColorChanger()

	config.imageRotation = 0.0001

	setUp()


def setUp():
	global config

	config.lineCount = 0
	config.canvasDraw.rectangle(
		(0, 0, config.canvasWidth, config.canvasHeight), fill=config.bgColor
	)
	config.pointArray = [[0, 0]]
	config.linesArray = []
	config.stop = False

	config.angleIncrement = random.uniform(config.angleIncrementMax, config.angleIncrementMax)

	# print(config.linesArray)

	for i in range(0, config.simultaneousLines):
		l = Line(config, False)
		l.lineNumber = i
		l.lineColor = colorutils.randomColorAlpha(1.0,50,255)
		l.segmentLength = config.segmentLength
		l.widthMultiplier = config.widthMultiplier
		l.setLineAttributes()
		# print(l.lastPoint)
		config.linesArray.append(l)
		config.lineCount += 1

	#config.draw.rectangle((0,0,config.canvasWidth,config.canvasHeight), fill = config.bgColor)
	#config.canvasDraw.rectangle((0,0,config.canvasWidth,config.canvasHeight), fill = config.bgColor)

def runWork():
	global config
	while True:
		iterate()
		time.sleep(config.delay)


def iterate():
	global config
	if config.stop == False:
		showLines()
	else:
		setUp()


def callBack():
	global config
	return True


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
