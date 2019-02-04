import time
import random
import textwrap
import math
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageEnhance, ImageChops
from modules import colorutils, badpixels, coloroverlay
from modules.quilting.colorset import ColorSet
from modules.quilting import createtrianglepieces
from modules.quilting import createpolypieces
from modules.quilting import createstarpieces

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def transformImage(img) :
	width, height = img.size
	m = -0.5
	xshift = abs(m) * 420
	new_width = width + int(round(xshift))

	img = img.transform((new_width, height), Image.AFFINE, (1, m, 0, 0, 1, 0), Image.BICUBIC)
	img = img.transform((new_width, height), Image.PERSPECTIVE, config.transformTuples, Image.BICUBIC)
	return img


# this could be written to use A as the starting point
# for b's range - but this way it makes for some more
# mixed up results
def randomRange(A=0, B=1, rounding=False):
	a = random.uniform(A,B)
	b = random.uniform(A,B)
	if rounding == False :
		return (a,b)
	else :
		return (round(a), round(b))


def restartPiece():
	config.t1  = time.time()
	config.t2  = time.time()


	## The "dark" color to the spokes
	config.c1HueRange = randomRange(0,360,True)
	config.c2SaturationRange = randomRange(.4,.95)
	config.c1ValueRange = randomRange(.3,.5)
	
	# the light color on the 8 spokes / points
	# these ones should always have the maximum variability
	config.c2HueRange = (0,360) #randomRange(0,360,True)
	config.c2SaturationRange = randomRange(.4,1)
	config.c2ValueRange = randomRange(.8,1)

	## The background -- ie the squares etc
	config.c3HueRange = randomRange(0,360,True)
	config.c3SaturationRange = randomRange()
	config.c3ValueRange = randomRange()
	if random.random() < .25 :
		choice = round(random.uniform(1,3))
		print ("Choice {0}".format(choice))
		if choice == 1 :
			# ruby pink bgs
			config.c3HueRange = (350,40)
			config.c3SaturationRange = (.5,1)
			config.c3ValueRange = (.4,1)
		elif choice == 2 :
			# blue bg
			config.c3HueRange = (220,260)
			config.c3SaturationRange = (.9,1)
			config.c3ValueRange = (.3,.95)
		else :
			# saturated 
			config.c3HueRange = (0,360)
			config.c3SaturationRange = (.6,1)
			config.c3ValueRange = (.9,1)

	config.fillColorSet = []
	config.fillColorSet.append (ColorSet(config.c1HueRange, config.c1SaturationRange, config.c1ValueRange))
	config.fillColorSet.append (ColorSet(config.c2HueRange, config.c2SaturationRange, config.c2ValueRange))
	config.fillColorSet.append (ColorSet(config.c3HueRange, config.c3SaturationRange, config.c3ValueRange))

	if random.random() < config.resetSizeProbability  :
		config.rotation = random.uniform(-config.rotationRange,config.rotationRange)
		config.doingRefresh = 0
		config.doingRefreshCount = 100
		
	if random.random() < config.resetSizeProbability  :
		config.blockSize = round(random.uniform(config.blockSizeMin,config.blockSizeMax))
		
		if (config.blockSize >= 11) :
			config.blockCols = config.blockColsMin
			config.blockRows = config.blockRowsMin
		else :
			config.blockCols = config.blockColsMax
			config.blockRows = config.blockRowsMax
		
		config.blockLength = config.blockSize
		config.blockHeight = config.blockSize
		config.doingRefresh = 0
		config.doingRefreshCount = 100
		createpolypieces.createPieces(config, True)

	# poly specific
	if random.random() < config.resetSizeProbability  :
		config.randomness = random.uniform(0,3)
		config.doingRefresh = 0
		config.doingRefreshCount = 100

	createpolypieces.refreshPalette(config)
	setInitialColors(True)


def setInitialColors(refresh=False):
	## Better initial color when piece is turned on
	for i in range(0,len(config.unitArray)):
		obj = config.unitArray[i]
		for c in range(0,len(obj.polys)) :
			colOverlay = obj.polys[c][1]
			colOverlay.colorB = colorutils.randomColor(config.brightness * .8)
			colOverlay.colorA = colorutils.randomColor(config.brightness * .8)
			colOverlay.colorTransitionSetupValues()
		

def main(run = True) :
	global config, directionOrder,workConfig
	print("---------------------")
	print("QUILT Loaded")


	config.brightness = float(workConfig.get("displayconfig", 'brightness')) 
	colorutils.brightness = config.brightness
	config.canvasImageWidth = config.screenWidth
	config.canvasImageHeight = config.screenHeight
	config.canvasImageWidth -= 4
	config.canvasImageHeight -= 4

	config.outlineColorObj = coloroverlay.ColorOverlay()
	config.outlineColorObj.randomRange = (5.0,30.0)

	config.quiltPattern = (workConfig.get("quilt", 'pattern'))

	# these control the timing of the individual color transitions - longer is slower
	config.transitionStepsMin = float(workConfig.get("quilt", 'transitionStepsMin'))
	config.transitionStepsMax = float(workConfig.get("quilt", 'transitionStepsMax'))

	# Some triangles will re-draw like a tick - on triangles quilt
	config.resetTrianglesProb = float(workConfig.get("quilt", 'resetTrianglesProb'))

	# The probability that at the beginning of a new quilt image the size of the
	# elements will change
	config.resetSizeProbability = float(workConfig.get("quilt", 'resetSizeProbability'))

	# the time in seconds given before the quilt image resets to new parameters
	config.timeToComplete = int(workConfig.get("quilt", 'timeToComplete')) 

	config.transformShape  = (workConfig.getboolean("quilt", 'transformShape'))
	transformTuples = workConfig.get("quilt", 'transformTuples').split(",")
	config.transformTuples = tuple([float(i) for i in transformTuples])

	redRange = workConfig.get("quilt", 'redRange').split(",")
	config.redRange = tuple([int(i) for i in redRange])

	# the mins and maxes for the size of the units 
	config.gapSize = int(workConfig.get("quilt", 'gapSize')) 
	config.blockSizeMin = int(workConfig.get("quilt", 'blockSizeMin'))
	config.blockSizeMax = int(workConfig.get("quilt", 'blockSizeMax'))
	config.blockSize = round(random.uniform(config.blockSizeMin,config.blockSizeMax))

	config.blockRowsMin = int(workConfig.get("quilt", 'blockRowsMin')) 
	config.blockRowsMax = int(workConfig.get("quilt", 'blockRowsMax')) 
	config.blockColsMin = int(workConfig.get("quilt", 'blockColsMin')) 
	config.blockColsMax = int(workConfig.get("quilt", 'blockColsMax')) 
	config.blockCols = config.blockColsMax
	config.blockRows = config.blockRowsMax


	# can adjust the quilt image offset
	config.cntrOffsetX = int(workConfig.get("quilt", 'cntrOffsetX')) 
	config.cntrOffsetY = int(workConfig.get("quilt", 'cntrOffsetY')) 

	# frame rate
	config.delay = float(workConfig.get("quilt", 'delay'))
	
	# the probabilty that any triangle will pop to another color
	config.colorPopProb = float(workConfig.get("quilt", 'colorPopProb'))

	config.brightnessFactorDark = float(workConfig.get("quilt", 'brightnessFactorDark'))
	config.brightnessFactorLight = float(workConfig.get("quilt", 'brightnessFactorLight'))
	config.lines  = (workConfig.getboolean("quilt", 'lines'))
	config.patternPrecision  = (workConfig.getboolean("quilt", 'patternPrecision'))
	

	config.activeSet = workConfig.get("quilt","activeSet")

	config.c1HueRange = tuple([float(i) for i in workConfig.get(config.activeSet, 'c1HueRange').split(",")])
	config.c1SaturationRange = tuple([float(i) for i in workConfig.get(config.activeSet, 'c1SaturationRange').split(",")])
	config.c1ValueRange = tuple([float(i) for i in workConfig.get(config.activeSet, 'c1ValueRange').split(",")])
	
	config.c2HueRange = tuple([float(i) for i in workConfig.get(config.activeSet, 'c2HueRange').split(",")])
	config.c2SaturationRange = tuple([float(i) for i in workConfig.get(config.activeSet, 'c2SaturationRange').split(",")])
	config.c2ValueRange = tuple([float(i) for i in workConfig.get(config.activeSet, 'c2ValueRange').split(",")])
	
	config.c3HueRange = tuple([float(i) for i in workConfig.get(config.activeSet, 'c3HueRange').split(",")])
	config.c3SaturationRange = tuple([float(i) for i in workConfig.get(config.activeSet, 'c3SaturationRange').split(",")])
	config.c3ValueRange = tuple([float(i) for i in workConfig.get(config.activeSet, 'c3ValueRange').split(",")])
	

	# for now, all squares 
	config.blockLength = config.blockSize
	config.blockHeight = config.blockSize

	config.canvasImage = Image.new("RGBA", (config.canvasImageWidth, config.canvasImageHeight))

	config.unitArray = []

	config.fillColorSet = []
	config.fillColorSet.append (ColorSet(config.c1HueRange, config.c1SaturationRange, config.c1ValueRange))
	config.fillColorSet.append (ColorSet(config.c2HueRange, config.c2SaturationRange, config.c2ValueRange))
	config.fillColorSet.append (ColorSet(config.c3HueRange, config.c3SaturationRange, config.c3ValueRange))


	try :
		config.rotationRange = float(workConfig.get("quilt", 'rotationRange')) 
	except Exception as e:
		config.rotationRange = 0
		print (e)


	try :
		config.randomness = int(workConfig.get("quilt", 'randomness')) 
	except Exception as e:
		config.randomness = 0
		print (e)



	try :
		drawBlockCoordsRaw = list(list((i).split(',')) for i in workConfig.get("drawBlock", 'drawBlockCoords').split("|"))
		config.drawBlockCoords = []
		for i in drawBlockCoordsRaw :
			coords = tuple(int(ii) for ii in i)
			config.drawBlockCoords.append(coords)
		config.drawBlockCoords = tuple(config.drawBlockCoords)

		config.drawBlockFixedColor = tuple([int(i) for i in workConfig.get("drawBlock", 'drawBlockFixedColor').split(",")])
		config.drawBlock_c1HueRange = tuple([float(i) for i in workConfig.get("drawBlock", 'c1HueRange').split(",")])
		config.drawBlock_c1SaturationRange = tuple([float(i) for i in workConfig.get("drawBlock", 'c1SaturationRange').split(",")])
		config.drawBlock_c1ValueRange = tuple([float(i) for i in workConfig.get("drawBlock", 'c1ValueRange').split(",")])
		config.canvasImageDraw = ImageDraw.Draw(config.canvasImage)
		config.drawBlock = True
		config.drawBlockShape = lambda : config.canvasImageDraw.polygon(config.drawBlockCoords, fill=config.drawBlockFixedColor)
	except Exception as e:
		print (e)
		config.drawBlock = False
		config.drawBlockShape = lambda : True



	createpolypieces.createPieces(config)

	setInitialColors()

	config.t1  = time.time()
	config.t2  = time.time()

	config.doingRefresh = 100
	config.doingRefreshCount = 100

	if(run) : runWork()


def runWork():
	global blocks, config, XOs
	#gc.enable()
	
	while True:
		iterate()
		time.sleep(config.delay)  
	

def iterate() :
	global config
	config.outlineColorObj.stepTransition()

	# Need to do a crossfade 
	if config.doingRefresh < config.doingRefreshCount :
		#print("crossfade...",  config.doingRefresh/config.doingRefreshCount)
		if config.doingRefresh == 0 :
			config.snapShot = config.canvasImage.copy()
		crossFade = Image.blend(config.snapShot, config.canvasImage, config.doingRefresh/config.doingRefreshCount)
		config.drawBlockShape()
		config.render(crossFade, 0,0)
		config.doingRefresh += 1
	else :
		temp = Image.new("RGBA", (config.canvasImageWidth, config.canvasImageWidth))
		temp.paste(config.canvasImage, (0,0), config.canvasImage)
		if(config.transformShape == True) :
			temp = transformImage(temp)
		config.drawBlockShape()
		config.render(temp, 0,0)

	for i in range(0,len(config.unitArray)):
		obj = config.unitArray[i]
		obj.update()
		obj.render()

	config.t2  = time.time()
	delta = config.t2  - config.t1

	if delta > config.timeToComplete :
		restartPiece()
		

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
