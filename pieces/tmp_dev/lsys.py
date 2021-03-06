#!/usr/bin/python
import math
import random
# from modules import colorutils
# Import the essentials to everything
import time

import PIL.Image
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageMath

"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


class Lsys:

	n = 5
	c = 0
	recursionLimit = 8
	strg = ""
	AxiomSelected = "FBF--FF--FF"
	PatternSetSelected = "FF"
	PatternSetSelected2 = "--FBF++FBF++FBF--"

	AxiomSelected = "F-F-F-F"
	PatternSetSelected = "F-F+F+F-F"
	PatternSetSelected2 = ""

	AxiomSelected = "F-F-FF-FF-FFF-FFF-FFFF-FFFF-FFFFF-FFFFF-FFFFFF-FFFFFF-"
	PatternSetSelected = "F"
	PatternSetSelected2 = ""


	PatternSetSelected2 = ""
	PatternSetSelected = "F+F-F-F-F+F+F+F-F"
	PatternSetSelected = "F-F+F+F-F"
	AxiomSelected = "F"



	useRandom = True
	foliage = False
	incrRange = 20
	incrEnd = 20
	angle = 50
	d = 10
	dFactor = 1
	dFactorMultiplier = 0.8

	s = ""
	incrStart = 0
	instruction = ""
	xPos = 0
	yPos = 0
	origin = dict(xpos=0, ypos=0)
	a = 0
	branchPoint = []
	branch = 0

	# nodeSpriteContainer:Sprite

	def __init__(self):
		print("Init Lsys")
		incrRange = 10
		incrEnd = 10
		incrStart = 0
		self.setUpNewDrawingParameters()

	def setUpNewDrawingParameters(self):
		self.c = 0
		self.strg = ""
		if self.PatternSetSelected2 == "":
			self.PatternSetSelected2 = "B"
		self.strg = self.parse(self.AxiomSelected)
		self.strg = self.parse(self.strg)
		self.strg = self.parse(self.strg)
		self.strg = self.parse(self.strg)

		print(self.strg)

	def setupDrawing(self):
		self.branchPoint = []
		self.xPos = self.origin["xPos"]
		self.yPos = self.origin["yPos"]
		# if (s) : canvasBaseHolder.removeChild(s)
		# s = new UIComponent()
		# canvasBaseHolder.addChild(s)
		# s.graphics.moveTo(xPos,yPos)

		# ti =  new Timer(1)
		# ti.addEventListener(TimerEvent.TIMER, redraw)
		# ti.start()

	def redraw(self, e):
		if incrStart < strg.length - incrRange:
			performAction()

	def parse(self, arg):
		finalString = arg
		self.c += 1
		l = len(self.PatternSetSelected2)
		if self.c < self.recursionLimit:
			arg = arg.replace("F", self.PatternSetSelected)
			arg = arg.replace("B", self.PatternSetSelected2)
			return self.parse(arg)
		return arg

	def performAction(self):
		for incr in range(incrStart, incrEnd):
			drawTerminal = false
			instruction = strg.charAt(incr)
			if instruction == "[":
				branchPoint.push({x: xPos, y: yPos, a: a})
				dFactor *= dFactorMultiplier
				if instruction == "]":
					branch = branchPoint.length - 1
				if branch > 0 and useRandom:
					angle += random() - random()

				if branch > 1 and foliage:
					# node = new Sprite()
					# nodeMark = new Sprite()
					node.x = xPos
					node.y = yPos
					# nodeMark.graphics.beginFill(0x000000,.5)

					foliageWidth = branch / dFactor
					foliageHeight = branch * 5 / dFactor

					if foliageWidth > 20:
						foliageWidth = 20
					if foliageHeight > 10:
						foliageHeight = 10

					# nodeMark.graphics.drawEllipse(0,0,foliageWidth,foliageHeight)
					# nodeMark.rotation =  180/Math.PI *  Math.sin(a)
					# nodeMark.graphics.endFill()
					# node.addChild(nodeMark)
					# s.addChild(node)

				xPos = branchPoint[branch].x
				yPos = branchPoint[branch].y
				a = branchPoint[branch].a
				# s.graphics.moveTo(xPos,yPos)
				branchPoint.pop()
				dFactor *= 1 / dFactorMultiplier
				drawTerminal = true
				if instruction == "-" or instruction == "=":
					a += -angle
				if instruction == "+":
					a += angle
				if instruction.toLowerCase() == "f" or instruction.toLowerCase() == "b":
					x1 = Math.cos(a * Math.PI / 180 - Math.PI / 2) * d * dFactor
				if random:
					x1 *= random() * 2
				y1 = Math.sin(a * Math.PI / 180 - PI / 2) * d * dFactor
				xPos += x1
				yPos += y1
				baseColor = 0xCC0000
				f = 1 / branch
				if branch == 0 or isNaN(branch):
					f = 1
				colorOfLine = Math.round(baseColor - baseColor * dFactor * 5)

				# s.graphics.lineStyle(dFactor*3.5,colorOfLine,f)
				# s.graphics.lineTo(xPos,yPos)

				incrStart += incrRange
				incrEnd = incrStart + incrRange


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
"""
def drawBasic(self):
	listStrg = list(strg)
	for i in range(len(self.strg)):

"""
"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
canvasBase = dict(width=500, height=500)
origin = [0, 0]
pos = 0
lastCoord = [2, 400]
nextCoord = [0, 0]
v = [0, 0]
angle = 2 *math.pi / 4.5
currentAngle = 0
runRun = True
d = 2


def drawLines(arg):

	global config, L, lastCoord, nextCoord, angle, currentAngle, v, d

	pi = math.pi

	# print(v)
	if arg == "F" or arg =="B":
		v = [d * math.cos(currentAngle), d * math.sin(currentAngle)]
		nextCoord[0] = lastCoord[0] + v[0]
		nextCoord[1] = lastCoord[1] + v[1]
		config.draw.line(
			(lastCoord[0], lastCoord[1], nextCoord[0], nextCoord[1]), fill=(255, 0, 0)
		)
		lastCoord[0] = nextCoord[0]
		lastCoord[1] = nextCoord[1]
		# print(lastCoord, nextCoord)

	if arg == "-":
		currentAngle -= angle

	if arg == "+":
		currentAngle += angle

	# reseting render image size
	# print (nextCoord)


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def main(run=True):
	global config, workConfig
	setUp()
	if run:
		runWork()


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def setUp():
	global L, config
	config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	config.draw = ImageDraw.Draw(config.image)
	config.id = config.image.im.id
	L = Lsys()
	return True


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def runWork():
	global runRun
	while True:
		iterate()
		#time.sleep(0.001)


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def iterate():
	global config, L, pos, runRun
	r = 4
	if pos < len(L.strg):
		for i in range(pos, pos + r):
			if i < len(L.strg):
				drawLines(L.strg[i])
		pos += r
	else:
		if runRun:
			print("Done!")
		runRun = False
	config.render(config.image, 0, 0, 192, 192)


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def callBack():
	global config
	pass
	# animator()


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
