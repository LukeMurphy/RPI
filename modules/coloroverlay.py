import math
import random
import time
from operator import sub

from modules import colorutils
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFont, ImageOps

"""""" """""" """""" """""" """""" """""" """""" """""" """""" """"""
### Colorizing filter that transitions from colorA to colorB ###


class ColorOverlay:

	currentColor = [0, 0, 0, 0]
	currentColorRaw = [0, 0, 0, 0]
	colorA = colorB = [0, 0, 0, 0]
	rateOfColorChange = 0
	randomRange = (10.0, 100.0)
	complete = False
	tDelta = 0
	timeTrigger = False
	gotoNextTransition = False
	autoChange = True
	t1 = 0

	## "Public" variables that can be set
	randomSteps = True
	steps = 200
	step = 1
	tLimit = 20
	tLimitBase = 20

	maxBrightness = 1

	minValue = 0.1
	maxValue = 1

	minSaturation = 0.1
	maxSaturation = 1

	minHue = 1
	maxHue = 360

	dropHueMin = 0
	dropHueMax = 0

	configRef = None

	def __init__(self, randomColorInit=False):
		# self.colorTransitionSetup()
		# self.colorA = colorutils.randomColor()
		# self.colorB = colorutils.randomColor()
		# self.colorB = colorutils.getRandomRGB()
		self.t1 = time.time()
		self.timeTrigger = False

		if randomColorInit == True:
			self.currentColor = list(colorutils.randomColorAlpha(0.5, 0))
			self.currentColorRaw = list(colorutils.randomColorAlpha(0.5, 255))
			self.colorA = self.colorB = list(colorutils.randomColorAlpha(0.5, 0))

			# print(self.currentColorRaw)

	def checkTime(self):
		t = time.time()
		self.tDelta = t - self.t1

	def setStartColor(self):
		self.colorA = colorutils.getRandomColorHSV(
			hMin=self.minHue,
			hMax=self.maxHue,
			sMin=self.minSaturation,
			sMax=self.maxSaturation,
			vMin=self.minValue,
			vMax=self.maxValue,
			dropHueMin=self.dropHueMin,
			dropHueMax=self.dropHueMax,
		)

		"""
		print("New Color A", self.colorA)
		"""

	def getNewColor(self):
		# self.colorB = colorutils.randomColor()
		## Vaguely more control of the color parameters ...
		# if(random.random() > .8) : self.colorB = colorutils.getRandomRGB()

		## LEGACY --- If the maxbrightness is being set to something other than the default
		## set the maxValue to the maxBrightness
		"""
		if(self.maxBrightness != 1 ) :
			self.maxValue = self.maxBrightness
		"""

		# print(self.minHue,self.maxHue,self.minValue,self.maxValue,self.minSaturation,self.maxSaturation)

		self.colorB = colorutils.getRandomColorHSV(
			hMin=self.minHue,
			hMax=self.maxHue,
			sMin=self.minSaturation,
			sMax=self.maxSaturation,
			vMin=self.minValue,
			vMax=self.maxValue,
			dropHueMin=self.dropHueMin,
			dropHueMax=self.dropHueMax,
		)

		"""
		print("New Color B", self.colorB,  self.colorA)
		print("New Color B", self.minHue, self.maxHue, 
			self.minSaturation, self.maxSaturation,
			self.minValue, self.maxValue)
		"""

	## Transition starts
	def colorTransitionSetup(self, steps=0, newColor=None):

		"""
		print("\nNew transition started...")

		try :
			for ii in range (0,3):
				print(ii, " current:", self.currentColorRaw[ii], " old destination:",self.colorB[ii]," old rate:", self.rateOfColorChange[ii])
		except:
			pass
		"""

		if newColor == None:
			self.getNewColor()
		else:
			self.colorB = newColor

		self.colorTransitionSetupValues(steps)

	def colorTransitionSetupValues(self, steps=0):
		#### Setting up for color transitions
		self.gotoNextTransition = False
		self.colorDelta = [0, 0, 0, 0]
		self.rateOfColorChange = [0, 0, 0, 0]

		# config.colorDelta = [a - b for a, b in zip(config.colorA, config.colorB)]

		self.colorDelta = list(map(sub, list(self.colorB), self.currentColorRaw))

		if len(self.colorDelta) == 3:
			self.colorDelta.append(0.1)

		# print(self.colorB, self.currentColorRaw)

		# Create random number of transition steps
		# if(steps == 0 or self.randomSteps == True) :
		self.steps = round(random.uniform(self.randomRange[0], self.randomRange[1]))

		self.tLimit = (
			round(random.uniform(self.tLimitBase / 2, self.tLimitBase * 1.5)) + 1
		)
		self.rateOfColorChange = [x / self.steps for x in self.colorDelta]
		self.complete = False
		self.step = 1
		self.t1 = time.time()

		rounding = 0.001

		if abs(self.rateOfColorChange[0]) < rounding:
			self.rateOfColorChange[0] = 0
		if abs(self.rateOfColorChange[1]) < rounding:
			self.rateOfColorChange[1] = 0
		if abs(self.rateOfColorChange[2]) < rounding:
			self.rateOfColorChange[2] = 0
		if abs(self.rateOfColorChange[3]) < rounding:
			self.rateOfColorChange[3] = 0

		###===========> NEED TO FIX THIS - stopping any alpha transition because
		###===========> NEED TO FIX THIS - stopping any alpha transition because
		###===========> NEED TO FIX THIS - stopping any alpha transition because
		###===========> NEED TO FIX THIS - stopping any alpha transition because
		###===========> NEED TO FIX THIS - stopping any alpha transition because
		###===========> NEED TO FIX THIS - stopping any alpha transition because
		## was throwing errors
		# self.rateOfColorChange[3] = 0

		self.lowerRange = list(
			map(
				lambda x, y: round(x - abs(y)) - 0.5,
				self.colorB,
				self.rateOfColorChange,
			)
		)
		self.upperRange = list(
			map(
				lambda x, y: round(x + abs(y)) + 0.5,
				self.colorB,
				self.rateOfColorChange,
			)
		)

		# print("New destination: ",self.colorB)
		# print(" NEW RATE: ", self.rateOfColorChange)

		self.callBackStarted()

	## Transition ends
	def stopTransition(self):
		# print ("Transition stopped")
		self.gotoNextTransition = True
		self.complete = True
		self.t1 = time.time()
		# self.callBackDone()

	
	def setCallBackDoneMethod(self, method, configRef=None):
		self.callBackDoneMethod = method
		self.configRef = configRef

	
	def setCallBackStartedMethod(self, method, configRef=None):
		self.callBackStartedMethod = method
		self.configRef = configRef

	
	def callBackDone(self):
		if self.complete == True:
			try:
				if self.configRef != None:
					self.callBackDoneMethod(self.configRef)
				else:
					self.callBackDoneMethod()

			except AttributeError as e:
				pass

	def callBackStarted(self):
		try:
			if self.configRef != None:
				self.callBackStartedMethod(self.configRef)
			else:
				self.callBackStartedMethod()
		except AttributeError as e:
			pass

	def stepTransition(self, autoReset=False, alpha=255):

		self.currentColorRaw = [
			self.currentColorRaw[0] + self.rateOfColorChange[0],
			self.currentColorRaw[1] + self.rateOfColorChange[1],
			self.currentColorRaw[2] + self.rateOfColorChange[2],
			self.currentColorRaw[3] + self.rateOfColorChange[3],
		]

		if self.currentColorRaw[3] > 255:
			self.currentColorRaw[3] = 255
			self.rateOfColorChange[3] = 0
		if self.currentColorRaw[3] < 0:
			self.currentColorRaw[3] = 0
			self.rateOfColorChange[3] = 0

		self.currentColor = [
			round(self.currentColorRaw[0]),
			round(self.currentColorRaw[1]),
			round(self.currentColorRaw[2]),
			round(self.currentColorRaw[3]),
		]

		self.step += 1
		self.checkTime()

		## Always change to the next color based on TIME
		# if (self.tDelta > self.tLimit and self.gotoNextTransition == False) :
		if self.tDelta > self.tLimit and self.step >= self.steps:
			self.stopTransition()
			if self.autoChange == True:
				self.colorTransitionSetup(self.steps)

		for i in range(0, 3):

			if (
				self.currentColor[i] >= self.lowerRange[i]
				and self.currentColor[i] <= self.upperRange[i]
				and self.rateOfColorChange[i] != 0
			):
				self.rateOfColorChange[i] = 0
				# print("Color reached", i)
				# self.currentColor[i] = self.colorB[i]
				"""
				print("Color reached", i)
				for ii in range (0,3):
					print(ii, " current:", self.currentColorRaw[ii], " destination:",self.colorB[ii]," rate:", self.rateOfColorChange[ii])
				"""

		if (
			self.rateOfColorChange[0] == 0
			and self.rateOfColorChange[1] == 0
			and self.rateOfColorChange[2] == 0
			and self.complete == False
		):
			self.complete = True
			self.callBackDone()
			# print("Transition complete.")
			# if(autoReset == True or self.gotoNextTransition == True) :
			#     self.colorTransitionSetup(self.steps)

	def getPercentageDone(self):
		return self.step / self.steps
