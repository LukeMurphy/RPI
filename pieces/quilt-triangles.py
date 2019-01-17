import time
import random
import textwrap
import math
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageEnhance, ImageChops
from modules import colorutils, badpixels, coloroverlay
from modules.quilting.colorset import ColorSet
from modules.quilting import createtrianglepieces
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

	newValueRange = randomRange()
	newSaturationRange = randomRange()
	newHueRange = randomRange(0,360,True)

	# triangles: major outline squares and diamonds
	# stars: BASE
	config.c1HueRange = newHueRange
	config.c1ValueRange = newValueRange

	newHueRange = randomRange(0,360,True)
	# triangles:  wings of the 8-point inner starts
	# stars: SQUARE
	if(config.quiltPattern == "stars"): 
		config.c2SaturationRange = randomRange()
		config.c2ValueRange = randomRange()
		config.c2HueRange = randomRange(0,360,True)
	else :
		config.c2HueRange = newHueRange

	# triangles:  the star center diamond
	# stars: CENTER SQUARE
	config.c3HueRange = newHueRange
	if(config.quiltPattern == "stars"): 
		newValueRange = randomRange()
	config.c3ValueRange = newValueRange

	config.fillColorSet = []
	config.fillColorSet.append (ColorSet(config.c1HueRange, config.c1SaturationRange, config.c1ValueRange))
	config.fillColorSet.append (ColorSet(config.c2HueRange, config.c2SaturationRange, config.c2ValueRange))
	config.fillColorSet.append (ColorSet(config.c3HueRange, config.c3SaturationRange, config.c3ValueRange))

	try:
		config.c4HueRange = newHueRange
		config.c5HueRange = newHueRange
		config.fillColorSet.append (ColorSet(config.c4HueRange, config.c4SaturationRange, config.c4ValueRange))
		config.fillColorSet.append (ColorSet(config.c5HueRange, config.c5SaturationRange, config.c5ValueRange))
	except Exception as e:
		print (e)


	if(config.quiltPattern == "triangles"):
		config.blockSize = round(random.uniform(10,28))
		if (config.blockSize >= 16) :
			config.blockRows = 4
			config.blockCols = 3
		else :
			config.blockRows = 7
			config.blockCols = 5
		createtrianglepieces.createPieces(config)
	else :
		config.blockSize = round(random.uniform(8,18))
		if (config.blockSize >= 11) :
			config.blockRows = 10
			config.blockCols = 8
		else :
			config.blockRows = 14
			config.blockCols = 10
		createstarpieces.createPieces(config)

	config.blockLength = config.blockSize
	config.blockHeight = config.blockSize

	config.rotation = random.uniform(-3,3)

	setInitialColors()


def setInitialColors():
	## Better initial color when piece is turned on
	for i in range(0,len(config.unitArray)):
		obj = config.unitArray[i]
		for c in range(0,8) :
			colOverlay = obj.triangles[c][1]
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
	config.transitionStepsMin = float(workConfig.get("quilt", 'transitionStepsMin'))
	config.transitionStepsMax = float(workConfig.get("quilt", 'transitionStepsMax'))
	config.resetTrianglesProd = float(workConfig.get("quilt", 'resetTrianglesProd'))

	config.transformShape  = (workConfig.getboolean("quilt", 'transformShape'))
	transformTuples = workConfig.get("quilt", 'transformTuples').split(",")
	config.transformTuples = tuple([float(i) for i in transformTuples])

	redRange = workConfig.get("quilt", 'redRange').split(",")
	config.redRange = tuple([int(i) for i in redRange])


	config.gapSize = int(workConfig.get("quilt", 'gapSize')) 
	config.blockSize = int(workConfig.get("quilt", 'blockSize')) 

	config.blockRows = int(workConfig.get("quilt", 'blockRows')) 
	config.blockCols = int(workConfig.get("quilt", 'blockCols')) 
	config.cntrOffsetX = int(workConfig.get("quilt", 'cntrOffsetX')) 
	config.cntrOffsetY = int(workConfig.get("quilt", 'cntrOffsetY')) 
	config.delay = float(workConfig.get("quilt", 'delay'))
	config.colorPopProb = float(workConfig.get("quilt", 'colorPopProb'))
	config.brightnessFactorDark = float(workConfig.get("quilt", 'brightnessFactorDark'))
	config.brightnessFactorLight = float(workConfig.get("quilt", 'brightnessFactorLight'))
	config.lines  = (workConfig.getboolean("quilt", 'lines'))
	config.patternPrecision  = (workConfig.getboolean("quilt", 'patternPrecision'))
	config.timeToComplete = int(workConfig.get("quilt", 'timeToComplete')) 

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
	
	try :
		config.c4HueRange = tuple([float(i) for i in workConfig.get(config.activeSet, 'c4HueRange').split(",")])
		config.c4SaturationRange = tuple([float(i) for i in workConfig.get(config.activeSet, 'c4SaturationRange').split(",")])
		config.c4ValueRange = tuple([float(i) for i in workConfig.get(config.activeSet, 'c4ValueRange').split(",")])
		
		config.c5HueRange = tuple([float(i) for i in workConfig.get(config.activeSet, 'c5HueRange').split(",")])
		config.c5SaturationRange = tuple([float(i) for i in workConfig.get(config.activeSet, 'c5SaturationRange').split(",")])
		config.c5ValueRange = tuple([float(i) for i in workConfig.get(config.activeSet, 'c5ValueRange').split(",")])
	except Exception as e:
		print (e)
		
	# for now, all squares 
	config.blockLength = config.blockSize
	config.blockHeight = config.blockSize

	config.canvasImage = Image.new("RGBA", (config.canvasImageWidth  , config.canvasImageHeight))

	config.unitArray = []

	config.fillColorSet = []
	config.fillColorSet.append (ColorSet(config.c1HueRange, config.c1SaturationRange, config.c1ValueRange))
	config.fillColorSet.append (ColorSet(config.c2HueRange, config.c2SaturationRange, config.c2ValueRange))
	config.fillColorSet.append (ColorSet(config.c3HueRange, config.c3SaturationRange, config.c3ValueRange))

	try :
		config.fillColorSet.append (ColorSet(config.c4HueRange, config.c4SaturationRange, config.c4ValueRange))
		config.fillColorSet.append (ColorSet(config.c5HueRange, config.c5SaturationRange, config.c5ValueRange))
	except Exception as e:
		print (e)

	if config.quiltPattern == "triangles" :
		createtrianglepieces.createPieces(config)
	elif config.quiltPattern == "stars" :
		createstarpieces.createPieces(config)

	config.t1  = time.time()
	config.t2  = time.time()


	setInitialColors()

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

	for i in range(0,len(config.unitArray)):

		obj = config.unitArray[i]
		obj.update()
		obj.render()

	temp = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	temp.paste(config.canvasImage, (0,0), config.canvasImage)
	if(config.transformShape == True) :
		temp = transformImage(temp)
	config.render(temp, 0,0)

	config.t2  = time.time()
	delta = config.t2  - config.t1

	if delta > config.timeToComplete :
		restartPiece()
		

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
