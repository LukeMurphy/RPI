import math
import random
import textwrap
import time

from modules import badpixels, coloroverlay, colorutils
from modules.quilting.colorset import ColorSet
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFont, ImageOps


class Unit:

	timeTrigger = True
	tLimitBase = 30

	maxBrightness = 1

	minSaturation = 0.0
	maxSaturation = 0.0

	minValue = 0.0
	maxValue = 0.0

	minHue = 0.0
	maxHue = 0.0

	# Default is square made of 4 triangles
	compositionNumber = 0
	squareNumber = 0

	darkeningFactor = 1.4

	initialized = True

	fillColor = (0, 0, 0, 255)
	fillColors = []
	polys = []
	pointRange = 28

	def __init__(self, config):
		self.config = config
		self.xPos = 0
		self.yPos = 0
		self.redraw = False

		self.draw = ImageDraw.Draw(config.image)

		## Like the "stiching" color and affects the overall "tone" of the piece
		self.outlineColor = config.outlineColorObj.currentColor
		self.objWidth = 20

		self.outlineRange = [(20, 20, 250)]
		self.brightness = 1
		self.fillColorMode = "random"
		self.lineColorMode = "red"
		self.changeColor = True
		self.lines = config.lines

		self.fillColors = []
		## Each of the 8 triangles has a set of coordinates and a color
		# self.triangles = [[[] for i in range(0,2)] for i in range(0,8)]
		self.fillColors = []

		## Pre-fill the triangles list/array with ColorOverlay objects
		self.polys = [
			[[], coloroverlay.ColorOverlay(False), []]
			for i in range(0, self.pointRange)
		]
		# self.triangles = [[[],coloroverlay.ColorOverlay(),[]] for i in range(0,8)]

	def setUp(self, n=0):

		self.outlineColor = tuple(
			int(a * self.brightness) for a in (self.outlineColorObj.currentColor)
		)

		#### Sets up color transitions

		# print ("Running setup: polys= {}".format(len(self.polys)))

		for i in range(0, len(self.polys)):
			colOverlay = self.polys[i][1]

			colOverlay.randomSteps = True
			colOverlay.timeTrigger = True
			colOverlay.tLimitBase = 2
			colOverlay.steps = 10

			# print(self.fillColors[i].valueRange)

			colOverlay.maxBrightness = self.config.brightness
			colOverlay.maxBrightness = self.fillColors[i].valueRange[1]

			colOverlay.minHue = self.fillColors[i].hueRange[0]
			colOverlay.maxHue = self.fillColors[i].hueRange[1]
			colOverlay.minSaturation = self.fillColors[i].saturationRange[0]
			colOverlay.maxSaturation = self.fillColors[i].saturationRange[1]
			colOverlay.minValue = self.fillColors[i].valueRange[0]
			colOverlay.maxValue = self.fillColors[i].valueRange[1]

			### This is the speed range of transitions in color
			### Higher numbers means more possible steps so slower
			### transitions - 1,10 very blinky, 10,200 very slow
			colOverlay.randomRange = (
				self.config.transitionStepsMin,
				self.config.transitionStepsMax,
			)

		self.outlineColor = tuple(
			round(a * self.brightness) for a in (self.outlineColorObj.currentColor)
		)
		# self.outlineColor = (0,0,0,255)
		self.setupSquareWithTriangles()

	def setupSquareWithTriangles(self):
		# Square's points made of corners and mid points
		"""
			 a     b     c     d     e
			f     g     h     i     j
			 k     l     m     n     o
			 p     q     r     s     t
			 u     v     w     x     y
	

		## dividing into polygons
		## b m g

		#      *
		#    * 
		#        *
		"""

		self.sqrPoints = {}
		letters = "abcdefghijklmnopqrstuvwxyz"
		n = 0
		for row in range(0, 5):
			for col in range(0, 5):
				xRnd = round(
					random.uniform(-self.config.randomness, self.config.randomness)
				)
				yRnd = round(
					random.uniform(-self.config.randomness, self.config.randomness)
				)
				self.sqrPoints[letters[n]] = (
					self.xPos + col * self.blockLength + xRnd,
					self.yPos + row * self.blockHeight + yRnd,
				)
				n = n + 1

		# print(self.xPos, self.blockLength)
		# print(self.sqrPoints)
		# print("")

		## All this just creates the sqaures and polygons
		## That make up a single square with an 8 point star
		## that also is divided bilaterally -- like a compass
		## star ... turned 2PI/16

		s = self.sqrPoints

		## "row" 1
		self.polys[0][0] = (s["a"], s["b"], s["g"], s["f"])
		self.polys[1][0] = (s["b"], s["m"], s["g"])
		self.polys[2][0] = (s["b"], s["m"], s["h"])
		self.polys[3][0] = (s["b"], s["c"], s["h"])
		self.polys[4][0] = (s["d"], s["c"], s["h"])
		self.polys[5][0] = (s["d"], s["m"], s["h"])
		self.polys[6][0] = (s["d"], s["i"], s["m"])
		self.polys[7][0] = (s["d"], s["e"], s["j"], s["i"])

		## "row" 2
		self.polys[8][0] = (s["f"], s["l"], s["k"])
		self.polys[9][0] = (s["f"], s["m"], s["l"])
		self.polys[10][0] = (s["f"], s["g"], s["m"])
		self.polys[11][0] = (s["m"], s["i"], s["j"])
		self.polys[12][0] = (s["m"], s["j"], s["n"])
		self.polys[13][0] = (s["j"], s["o"], s["n"])

		## "row" 3
		self.polys[14][0] = (s["k"], s["l"], s["p"])
		self.polys[15][0] = (s["p"], s["l"], s["m"])
		self.polys[16][0] = (s["p"], s["m"], s["q"])
		self.polys[17][0] = (s["q"], s["m"], s["v"])
		self.polys[18][0] = (s["v"], s["m"], s["r"])
		self.polys[19][0] = (s["m"], s["r"], s["x"])
		self.polys[20][0] = (s["m"], s["s"], s["x"])
		self.polys[21][0] = (s["m"], s["n"], s["t"])
		self.polys[22][0] = (s["m"], s["t"], s["s"])
		self.polys[23][0] = (s["n"], s["o"], s["t"])

		## "row" 4
		self.polys[24][0] = (s["p"], s["q"], s["v"], s["u"])
		self.polys[25][0] = (s["v"], s["r"], s["w"])
		self.polys[26][0] = (s["r"], s["x"], s["w"])
		self.polys[27][0] = (s["s"], s["t"], s["y"], s["x"])

		self.pointRange = 28

		# print (self.polys)
		# sys.exit()

	def update(self):
		for i in range(0, self.pointRange):
			if random.random() > self.config.colorPopProb:
				self.polys[i][1].stepTransition()
				self.polys[i][2] = tuple(
					round(a * self.config.brightness)
					for a in self.polys[i][1].currentColor
				)
			else:
				self.changeColorFill(self.polys[i])

	def drawUnitTriangles(self):
		if self.lines == True:
			outline = self.outlineColor
		else:
			outline = None

		for i in range(0, self.pointRange):
			coords = self.polys[i][0]
			fillColor = self.polys[i][2]
			fillColorList = list(round(a * self.config.brightness) for a in fillColor)
			fillColor = (fillColorList[0], fillColorList[1], fillColorList[2], 255)
			self.draw.polygon(coords, fill=fillColor, outline=outline)

	def render(self):

		if self.fillColorMode == "red":
			brightnessFactor = self.config.brightnessFactorDark
		else:
			brightnessFactor = self.config.brightnessFactorLight

		self.outlineColor = tuple(
			int(a * self.config.brightness * brightnessFactor)
			for a in self.outlineColorObj.currentColor
		)

		self.drawUnitTriangles()

	## Straight color change - deprecated - too blinky
	def changeColorFill(self, obj):

		# obj[0] are coordinates
		# obj[1] is the colorOverlay object
		# obj[2] is the fill color

		if self.changeColor == True:
			if self.fillColorMode == "random":
				obj[2] = colorutils.randomColor(random.uniform(0.01, self.brightness))
				self.outlineColor = colorutils.getRandomRGB(
					random.uniform(0.01, self.brightness)
				)
			else:
				newColor = colorutils.getRandomColorHSV(
					hMin=obj[1].minHue,
					hMax=obj[1].maxHue,
					sMin=obj[1].minSaturation,
					sMax=obj[1].maxSaturation,
					vMin=obj[1].minValue,
					vMax=obj[1].maxValue,
				)

				obj[1].colorA = newColor
