import math
import random
import threading
import time

from modules import colorutils
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps, ImageChops


'''
				fadeIn = Fader()
				# fadeIn.blankImage = Image.new("RGBA", (height, width))
				fadeIn.crossFade = Image.new("RGBA", (height, width))
				fadeIn.image = gradientImage
				fadeIn.xPos = xPos
				fadeIn.yPos = yPos
				fadeIn.height = gradientImage.height
				fadeIn.width = gradientImage.width

				config.fadeArray.append(fadeIn)

'''

class Fader:
	def __init__(self):
		self.doingRefresh = 0
		self.doingRefreshCount = 50
		self.fadingDone = False

	def fadeIn(self, config):
		if self.fadingDone == False:
			if self.doingRefresh < self.doingRefreshCount:
				self.blankImage = Image.new("RGBA", (self.width, self.height))
				self.crossFade = Image.blend(
					self.blankImage,
					self.image,
					self.doingRefresh / self.doingRefreshCount,
				)
				config.image.paste(
					self.crossFade, (self.xPos, self.yPos), self.crossFade
				)
				self.doingRefresh += 1
			else:
				config.image.paste(self.image, (self.xPos, self.yPos), self.image)
				self.fadingDone = True


class Bar:
	def __init__(self):
		self.remake()
		self.yPos = 0
		self.xPos = 0


	def remake(self) :
		self.colorSetBeingUsed = config.usingColorSet
		#self.colorVal = colorutils.randomColorAlpha()
		self.verticalLength = random.random() * config.verticalLength
		cset = config.colorSets[config.usingColorSet]
		self.colorVal = colorutils.getRandomColorHSV(cset[0], cset[1], cset[2], cset[3], cset[4], cset[5], config.dropHueMax,0, config.colorAlpha )
		self.outlineColorVal = colorutils.getRandomColorHSV(cset[0], cset[1], cset[2], cset[3], cset[4], cset[5], config.dropHueMax,0, config.outlineColorAlpha )
		self.outlineColorVal = None


def reDraw():
	global config


def runWork():
	global config
	while True:
		iterate()
		time.sleep(config.redrawRate)



def iterate():
	global config

	i = 0
	base = -math.pi/2
	r = config.verticalLength

	

	config.angularOffset = time.time()
	config.angularOffset2 = time.time()*2
	
	'''
	config.angularOffset += config.angularOffsetSpeeed
	config.angularOffset2 += config.angularOffsetSpeeed2
	'''

	config.draw.rectangle((0,0,config.canvasWidth,config.canvasHeight), fill =config.bgColor)

	dx = config.canvasWidth / config.numberOfCols /3 
	dy = config.canvasHeight / config.numberOfRows /8


	for row in range(0, config.numberOfRows):
		for col in range(0, config.numberOfCols):

			bar = config.barArray[i]

			pAx = col * dx * 3 + dx
			pBx = col * dx * 3 * config.colSpacing - dx 
			pCx = col * dx * 3 + dx + dx


			verticalD = math.sin(row * dy + config.angularOffset2) * config.spacing/2

			#pAy = r * math.sin(pAx) + config.spacing/2
			pAy = 5
			pBy = bar.verticalLength * math.sin(pBx * config.period + config.angularOffset) + verticalD + config.spacing
			pCy = bar.verticalLength * math.sin(pCx * config.period + config.angularOffset) + verticalD + config.spacing

			pA = (dx, pAy)
			pB = (0, pBy)
			pC = (2*dx, pCy)

			#making a dart shape
			pD = (dx, pAy + bar.verticalLength)

			w = round(dx * 9)
			temp = Image.new("RGBA", (w, w))

			drw = ImageDraw.Draw(temp)

			drw.polygon((pA,pB,pD,pC), fill = bar.colorVal, outline = bar.outlineColorVal)
			#drw.ellipse((d,pAy,d+2,pAy+2), fill = (255,0,0))
			#drw.ellipse((0,pBy,2,pBy+2), fill = (0,250,0))
			#drw.ellipse((2*d,pCy,2*d+2,pCy+2), fill = (0,100,100))

			#temp = temp.rotate(config.tipAngle - angle)

			config.image.paste(temp,(round(pBx), round(bar.yPos)), temp)
			#config.image = ImageChops.add(config.image, temp)
			i+=1

			if random.random() < .2 and bar.colorSetBeingUsed != config.usingColorSet:
				bar.remake()

	if random.random() < .002 :
		if config.dropHueMax == 0 :
			config.dropHueMax = 255
		else :
			config.dropHueMax = 0
		#print("Winter... " + str(config.dropHueMax ))

	if random.random() < config.colorChangeProb :
		config.usingColorSet = math.floor(random.uniform(0,config.numberOfColorSets))
		# just in case ....
		if config.usingColorSet == config.numberOfColorSets : 
			config.usingColorSet = config.numberOfColorSets-1
		config.colorAlpha = round(random.uniform(config.leadEdgeAlpahMin,config.leadEdgeAlpahMax))
		config.dropHueMax = 0

		if random.random() < config.colorChangeProb * 3 :
			config.bgColor = colorutils.randomColorAlpha(config.brightness, config.bgColorAlpha, config.bgColorAlpha)
		else :
			config.bgColor = config.bgColorInit
		#print("ColorSet: " + str(config.usingColorSet))

	config.render(config.image, 0,0)


def main(run=True):
	global config
	config.redrawRate = .02

	
	config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	config.draw = ImageDraw.Draw(config.image)
	config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.canvasDraw = ImageDraw.Draw(config.canvasImage)


	# --------  Color ------------------#
	config.leadEdgeAlpahMax =  int(workConfig.get("bars", "leadEdgeAlpahMax"))
	config.leadEdgeAlpahMin =  int(workConfig.get("bars", "leadEdgeAlpahMin"))
	config.colorAlpha = config.leadEdgeAlpahMax
	config.outlineColorAlpha = config.leadEdgeAlpahMin
	config.dropHueMax = 0
	config.colorChangeProb =  float(workConfig.get("bars", "colorChangeProb"))
	config.bgColorAlpha =  int(workConfig.get("bars", "bgColorAlpha"))
	config.bgColor = tuple(
		int(i) for i in (workConfig.get("bars", "bgColor").split(","))
	)
	config.bgColorInit = tuple(
		int(i) for i in (workConfig.get("bars", "bgColor").split(","))
	)
	
	config.colorSetList = list(
		i for i in (workConfig.get("bars", "colorSets").split(","))
	)

	config.numberOfColorSets = len(config.colorSetList)
	config.colorSets = []
	for setName in config.colorSetList :
		cset = list(
			float(i) for i in (workConfig.get("bars", setName).split(","))
		)
		config.colorSets.append(cset)


	config.usingColorSet = math.floor(random.uniform(0,config.numberOfColorSets))
	if config.usingColorSet == config.numberOfColorSets : config.usingColorSet = config.numberOfColorSets - 1


	# --------  Space ------------------#
	config.xPos = 0
	config.numberOfRows =  int(workConfig.get("bars", "numberOfRows"))
	config.numberOfCols =  int(workConfig.get("bars", "numberOfCols"))
	config.spacing =  float(workConfig.get("bars", "spacing"))
	config.colSpacing =  float(workConfig.get("bars", "colSpacing"))
	config.rowSpacing =  float(workConfig.get("bars", "rowSpacing"))
	config.colSpacingOffset =  float(workConfig.get("bars", "colSpacingOffset"))
	config.verticalLength =  int(workConfig.get("bars", "verticalLength"))	

	# --------- Movement ---------------#
	config.angularOffsetSpeeed = math.pi / float(workConfig.get("bars", "angularOffsetSpeeed"))
	config.angularOffsetSpeeed2 = math.pi / float(workConfig.get("bars", "angularOffsetSpeeed2"))
	config.angularOffset = 0
	config.angularOffset2 = 0
	config.period = float(workConfig.get("bars", "period"))
	config.periodOffset = float(workConfig.get("bars", "periodOffset"))
	config.barArray = []
	altRowCount = 0
	d = config.canvasWidth / config.numberOfCols /3 
	i = 0
	for row in range(0, config.numberOfRows):
		for col in range(0, config.numberOfCols):
			bar =  Bar()
			bar.xPos = col * d * config.colSpacing
			bar.yPos = row * d * config.rowSpacing
			'''
			altRowCount = 0
			if altRowCount == 0 : bar.colorVal = (255,0,0,125)
			if altRowCount == 1 : bar.colorVal = (0,255,0,125)
			if altRowCount == 2 : bar.colorVal = (0,0,255,125)
			'''
			config.barArray.append(bar)
			i += 1
		altRowCount +=1
		if altRowCount == 3 : altRowCount = 0

	print(i)
			

	if run:
		runWork()
