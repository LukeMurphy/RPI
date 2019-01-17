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


	if(config.quiltPattern == "stars"): 
		newHueRange = randomRange(0,360,True)
		newSaturationRange = randomRange()
		newValueRange = randomRange()

		# stars: BASE
		config.c1HueRange = newHueRange
		config.c1ValueRange = newValueRange

		# stars: SQUARE
		config.c2SaturationRange = randomRange()
		config.c2ValueRange = randomRange()
		config.c2HueRange = randomRange(0,360,True)
		
		# stars: CENTER SQUARE
		config.c3HueRange = newHueRange
		config.c3ValueRange = randomRange()
	
	else :
		newHueRange = randomRange(0,360,True)
		newSaturationRange = randomRange(.2,1)
		newValueRange = randomRange(.2,1)
		
		# triangles: major outline squares and diamonds
		config.c1HueRange = newHueRange
		config.c1SaturationRange = newSaturationRange
		config.c1ValueRange = newValueRange

		# triangles:  wings of the 8-point inner starts
		newHueRange = randomRange(0,360,True)
		newSaturationRange = randomRange()
		newValueRange = randomRange()
		
		config.c2HueRange = newHueRange
		config.c2SaturationRange = newSaturationRange
		config.c2ValueRange = newValueRange

		# triangles:  the star center diamond
		#newHueRange = randomRange(0,360,True)
		newHueRange = randomRange(0,360,True)
		newSaturationRange = randomRange()
		newValueRange = randomRange()

		#print(newHueRange,newSaturationRange,newValueRange)

		config.c3HueRange = newHueRange
		config.c3SaturationRange = newSaturationRange
		config.c2ValueRange = newValueRange




	'''

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
	'''



	config.fillColorSet = []
	config.fillColorSet.append (ColorSet(config.c1HueRange, config.c1SaturationRange, config.c1ValueRange))
	config.fillColorSet.append (ColorSet(config.c2HueRange, config.c2SaturationRange, config.c2ValueRange))
	config.fillColorSet.append (ColorSet(config.c3HueRange, config.c3SaturationRange, config.c3ValueRange))



	if(config.quiltPattern == "stars"):
		config.blockSize = round(random.uniform(8,18))
		if (config.blockSize >= 11) :
			config.blockRows = 10
			config.blockCols = 8
		else :
			config.blockRows = 14
			config.blockCols = 10
		createstarpieces.createPieces(config)
	else :
		config.blockSize = round(random.uniform(10,28))
		if (config.blockSize >= 16) :
			config.blockRows = 7
			config.blockCols = 5
		else :
			config.blockRows = 7
			config.blockCols = 5

		'''
		'''
		if random.random() < 1 :
			createtrianglepieces.createPieces(config, True)
		setInitialColors(True)

	config.blockLength = config.blockSize
	config.blockHeight = config.blockSize

	config.rotation = random.uniform(-3,3)

	


def setInitialColors(refresh=False):
	## Better initial color when piece is turned on
	if refresh == True:
		createtrianglepieces.refreshPalette(config)
	for i in range(0,len(config.unitArray)):
		obj = config.unitArray[i]
		for c in range(0,8) :
			colOverlay = obj.triangles[c][1]
			#colOverlay.colorB = colorutils.randomColorAlpha(config.brightness * .8,0)
			colOverlay.colorA = colorutils.randomColorAlpha(config.brightness * .8,0)
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
	
		
	# for now, all squares 
	config.blockLength = config.blockSize
	config.blockHeight = config.blockSize

	config.canvasImage = Image.new("RGBA", (config.canvasImageWidth  , config.canvasImageHeight))


	config.fillColorSet = []
	config.fillColorSet.append (ColorSet(config.c1HueRange, config.c1SaturationRange, config.c1ValueRange))
	config.fillColorSet.append (ColorSet(config.c2HueRange, config.c2SaturationRange, config.c2ValueRange))
	config.fillColorSet.append (ColorSet(config.c3HueRange, config.c3SaturationRange, config.c3ValueRange))


	config.unitArray = []
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
		if random.random() < .1 :
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
