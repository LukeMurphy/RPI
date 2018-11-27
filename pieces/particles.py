import time
import random
import textwrap
import math
import datetime
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageEnhance, ImageChops
from PIL import ImageFilter
from modules import colorutils, coloroverlay
from modules.particles.particle_system import ParticleSystem
from modules.particles.particle import Particle


def main(run = True) :
	global config, directionOrder, ps
	print("---------------------")
	print("Particles Loaded")
	colorutils.brightness = config.brightness
	config.canvasImageWidth = config.canvasWidth
	config.canvasImageHeight = config.canvasHeight
	config.canvasImageWidth -= 4
	config.canvasImageHeight -= 4
	config.delay = .02
	config.numUnits  = 60


	'''
	config.fontColorVals = ((workConfig.get("diag", 'fontColor')).split(','))
	config.fontColor = tuple(map(lambda x: int(int(x)  * config.brightness), config.fontColorVals))
	config.outlineColorVals = ((workConfig.get("diag", 'outlineColor')).split(','))
	config.outlineColor = tuple(map(lambda x: int(int(x) * config.brightness) , config.outlineColorVals))
	'''

	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

	config.canvasImage = Image.new("RGBA", (config.canvasImageWidth  , config.canvasImageHeight))
	config.fontSize = 14
	config.font = ImageFont.truetype(config.path  + '/assets/fonts/freefont/FreeSansBold.ttf', config.fontSize)
	

	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

	ps = ParticleSystem(config)
	ps.unitArray = []

	ps.xGravity = float(workConfig.get("particleSystem", 'xGravity'))
	ps.yGravity = float(workConfig.get("particleSystem", 'yGravity'))
	ps.damping = float(workConfig.get("particleSystem", 'damping'))
	ps.collisionDamping = float(workConfig.get("particleSystem", 'collisionDamping'))
	ps.borderCollisions = (workConfig.getboolean("particleSystem", 'borderCollisions'))    
	ps.ignoreBottom = (workConfig.getboolean("particleSystem", 'ignoreBottom'))    
	ps.expireOnExit = (workConfig.getboolean("particleSystem", 'expireOnExit'))
	ps.changeCohesion = (workConfig.getboolean("particleSystem", 'changeCohesion'))     

	ps.useFlocking = (workConfig.getboolean("particleSystem", 'useFlocking'))
	ps.cohesionDistance = float(workConfig.get("particleSystem", 'cohesionDistance'))
	ps.repelDistance = float(workConfig.get("particleSystem", 'repelDistance'))
	ps.distanceFactor = float(workConfig.get("particleSystem", 'distanceFactor'))
	ps.clumpingFactor = float(workConfig.get("particleSystem", 'clumpingFactor'))
	ps.repelFactor = float(workConfig.get("particleSystem", 'repelFactor'))

	ps.cohesionDegrades = float(workConfig.get("particleSystem", 'cohesionDegrades'))
	ps.speedMin = float(workConfig.get("particleSystem", 'speedMin'))
	ps.speedMax = float(workConfig.get("particleSystem", 'speedMax'))
	ps.numUnits = int(workConfig.get("particleSystem", 'numUnits'))
	config.bgColorVals = ((workConfig.get("particleSystem", 'bgColor')).split(','))
	config.bgColor = tuple(map(lambda x: int(int(x) * config.brightness) , config.bgColorVals))

	ps.centerRangeXMin = int(workConfig.get("particleSystem", 'centerRangeXMin'))
	ps.centerRangeYMin = int(workConfig.get("particleSystem", 'centerRangeYMin'))
	ps.centerRangeXMax = int(workConfig.get("particleSystem", 'centerRangeXMax'))
	ps.centerRangeyMax = int(workConfig.get("particleSystem", 'centerRangeyMax'))

	

	ps.objType = (workConfig.get("particleSystem", 'objType'))

	try :
		ps.meandorFactor = float(workConfig.get("particleSystem", 'meandorFactor'))
	except Exception as e: 
		print (str(e)) 
		ps.meandorFactor = 1.0

	try :
		ps.objTrails = (workConfig.getboolean("particleSystem", 'objTrails'))
	except Exception as e: 
		print (str(e)) 
		ps.objTrails = True

	try :
		config.bgTransitions = (workConfig.getboolean("particleSystem", 'bgTransitions'))
		config.colOverlayA = coloroverlay.ColorOverlay()
		config.bgRangeA = int(workConfig.get("particleSystem", 'bgRangeA'))
		config.bgRangeB = int(workConfig.get("particleSystem", 'bgRangeB'))
		config.colOverlayA.randomRange = (config.bgRangeA,config.bgRangeB)
		#config.colOverlayA.colorA = tuple(int(a*config.brightness) for a in (colorutils.getRandomColor()))
		config.colOverlayA.minHue = int(workConfig.get("particleSystem", 'minHue'))
		config.colOverlayA.maxHue = int(workConfig.get("particleSystem", 'maxHue'))		

		config.colOverlayA.minValue = float(workConfig.get("particleSystem", 'minValue'))
		config.colOverlayA.maxValue = float(workConfig.get("particleSystem", 'maxValue'))

		config.colOverlayA.maxBrightness = float(workConfig.get("particleSystem", 'maxBrightness'))
		config.colOverlayA.bgTransparency = float(workConfig.get("particleSystem", 'bgTransparency'))
		config.colOverlayA.randomSteps = True 
		config.colOverlayA.timeTrigger = True
		config.colOverlayA.tLimitBase = int(workConfig.get("particleSystem", 'tLimitBase'))
		config.colOverlayA.setStartColor()
		config.colOverlayA.getNewColor()
		config.colOverlayA.colorTransitionSetup()


	except Exception as e: 
		print (str(e)) 
		config.bgTransitions = False
	
	try :
		ps.linearMotionAlsoHorizontal = (workConfig.getboolean("particleSystem", 'linearMotionAlsoHorizontal'))
	except Exception as e: 
		print (str(e)) 
		ps.linearMotionAlsoHorizontal = True

	try :
		ps.reEmitNumber = int(workConfig.get("particleSystem", 'reEmitNumber'))
	except Exception as e: 
		print (str(e)) 
		ps.reEmitNumber = 2

	try :
		ps.fixedUnitArray = (workConfig.getboolean("particleSystem", 'fixedUnitArray'))
	except Exception as e: 
		print (str(e)) 
		ps.fixedUnitArray = False

	try :
		ps.transparencyRange = workConfig.get("particleSystem", 'transparencyRange').split(',')
		ps.transparencyRange = tuple(map(lambda x: int(int(x)) , ps.transparencyRange))
	except Exception as e: 
		print (str(e)) 
		ps.transparencyRange = (10,200)

	try :
		config.transformShape = (workConfig.getboolean("particleSystem", 'transformShape'))
		transformTuples = workConfig.get("particleSystem", 'transformTuples').split(",")
		config.transformTuples = tuple([float(i) for i in transformTuples])
	except Exception as e: 
		print (str(e)) 
		config.transformShape = False


	ps.movement = (workConfig.get("particleSystem", 'movement'))
	ps.objColor = (workConfig.get("particleSystem", 'objColor'))
	ps.objWidth = int(workConfig.get("particleSystem", 'objWidth'))
	ps.objHeight = int(workConfig.get("particleSystem", 'objHeight'))
	ps.widthRate = float(workConfig.get("particleSystem", 'widthRate'))
	ps.heightRate = float(workConfig.get("particleSystem", 'heightRate'))
	config.variance = float(workConfig.get("particleSystem", 'variance'))

	config.fillColorVals = ((workConfig.get("particleSystem", 'fillColor')).split(','))
	config.fillColor = tuple(map(lambda x: int(int(x) * config.brightness) , config.fillColorVals))

	config.outlineColorVals = ((workConfig.get("particleSystem", 'outlineColor')).split(','))
	config.outlineColor = tuple(map(lambda x: int(int(x) * config.brightness) , config.outlineColorVals))

	ps.unitBlur = int(workConfig.get("particleSystem", 'unitBlur'))
	config.overallBlur = int(workConfig.get("particleSystem", 'overallBlur'))

	config.useOverLay = (workConfig.getboolean("particleSystem", 'useOverLay'))     
	config.overlayColorVals = ((workConfig.get("particleSystem", 'overlayColor')).split(','))
	config.overlayColor = tuple(map(lambda x: int(int(x) * config.brightness) , config.overlayColorVals))
	config.clrBlkWidth = int(workConfig.get("particleSystem", 'clrBlkWidth')) 
	config.clrBlkHeight = int(workConfig.get("particleSystem", 'clrBlkHeight')) 
	config.overlayxPos = int(workConfig.get("particleSystem", 'overlayxPos')) 
	config.overlayyPos = int(workConfig.get("particleSystem", 'overlayyPos')) 


	for i in range(0, ps.numUnits):
		emitParticle()

	setUp()

	if(run) : runWork()


def emitParticle(i=None):
	global config, ps
	p = Particle(ps)
	p.objWidth = ps.objWidth
	p.objHeight = ps.objHeight
	p.setUpParticle()
	p.xPosR = config.canvasWidth/2 - ps.centerRangeXMin + round(random.random() * ps.centerRangeXMax) - p.objWidth
	p.yPosR = config.canvasHeight/2 - ps.centerRangeYMin + round(random.random() * ps.centerRangeYMax) - p.objHeight
	#variance = math.pi/3
	p.direction = random.uniform(math.pi + math.pi/2 - config.variance, math.pi + math.pi/2 + config.variance)
	p.v = random.uniform(ps.speedMin,ps.speedMax)

	if ps.objColor == "rnd" :
		p.fillColor = colorutils.randomColor(ps.config.brightness)
		p.outlineColor = colorutils.getSunsetColors(ps.config.brightness/2)	

	if ps.objColor == "alphaRandom" :
		p.fillColor = colorutils.randomColorAlpha(ps.config.brightness, int(random.uniform(ps.transparencyRange[0],ps.transparencyRange[1])))
		p.outlineColor = None

	else :
		p.fillColor = config.fillColor #(240,150,0,100)
		p.outlineColor = config.outlineColor #(100,0,0,100)


	if(ps.movement == "linearMotion"):

		p.xPosR = int(random.uniform(0,config.canvasWidth))
		p.yPosR = int(random.uniform(0,config.canvasHeight))
		#config.canvasHeight/3 - p.objHeight/4 #

		directions = [0, math.pi, math.pi/2, -math.pi/2]
		origins = [
			(-p.objWidth, p.yPosR), 
			(config.canvasWidth +  p.objWidth, p.yPosR), 
			(p.xPosR, -p.objHeight), 
			(p.xPosR, config.canvasHeight + p.objHeight)
			]
		dirVal = round(random.uniform(0,1))

		if(ps.linearMotionAlsoHorizontal == True) :
			dirVal = round(random.uniform(0,3))


		p.direction = directions[dirVal]
		p.xPosR = origins[dirVal][0]
		p.yPosR = origins[dirVal][1]
	
	if i != None :
		ps.unitArray[i] = p
	else :
		ps.unitArray.append(p)
	

def transformImage(img) :
	width, height = img.size
	m = -0.5
	xshift = abs(m) * 420
	new_width = width + int(round(xshift))

	img = img.transform((new_width, height), Image.AFFINE, (1, m, 0, 0, 1, 0), Image.BICUBIC)
	img = img.transform((new_width, height), Image.PERSPECTIVE, config.transformTuples, Image.BICUBIC)
	return img
	

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def colorize() :

		#Colorize via overlay etc
		config.clrBlock = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
		clrBlockDraw = ImageDraw.Draw(config.clrBlock)

		# Color overlay on b/w PNG sprite
		#clrBlockDraw.rectangle((0,0, w, h), fill=(255,255,255))
		clrBlockDraw.rectangle((0,0, config.canvasWidth, config.canvasHeight), fill=(255,255,255,255))
		clrBlockDraw.rectangle((0,0, config.clrBlkWidth, config.clrBlkHeight), fill=config.overlayColor)

		'''
		try :
			config.image = ImageChops.multiply(config.clrBlock, config.image)
			#pass
		except Exception as e: 
			print(e, config.image.mode)
			pass
		'''

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def setUp():
	global config
	colorize()
	pass

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def runWork():
	global blocks, config
	#gc.enable()
	while True:
		iterate()
		time.sleep(config.delay)  

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def iterate() :
	global config, ps

	if config.bgTransitions == True :
		config.colOverlayA.stepTransition(alpha=config.colOverlayA.bgTransparency)
		config.bgColor = tuple(int (a * config.brightness ) for a in config.colOverlayA.currentColor)


	## Fade trails or not...
	config.draw.rectangle((0,0,config.screenWidth-1, config.screenHeight-1), fill=config.bgColor, outline=None)

	if config.useOverLay == True :
		#config.image = ImageChops.multiply(config.clrBlock, config.image)
		config.image.paste(config.clrBlock,(config.overlayxPos, config.overlayyPos),config.clrBlock)

	for p in ps.unitArray:
		p.update()
		p.render()

		if(p.remove == True) :
			#print("REMOVING",ps.unitArray.index(p),len(ps.unitArray))

			if(ps.fixedUnitArray == False) :
				ps.unitArray.remove(p)

				if len(ps.unitArray) < config.numUnits + 0 :
					for i in range(0, ps.reEmitNumber):
						emitParticle()
			else :
				emitParticle(i = ps.unitArray.index(p))



	if random.random() < .0005 and ps.changeCohesion == True:
		ps.cohesionDistance = random.uniform(14,30)
		#print(ps.cohesionDistance)

		
	if (config.overallBlur > 0) :
		config.image = config.image.filter(ImageFilter.GaussianBlur(radius=config.overallBlur))
		## This needs to be reset
		config.image = config.image.filter(ImageFilter.UnsharpMask(radius=80,percent=250, threshold=1))
		config.draw = ImageDraw.Draw(config.image)


	if(config.transformShape == True) :
		config.image = transformImage(config.image)

	config.render(config.image, 0,0)
		


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def callBack() :
	global config, XOs
	return True

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''



