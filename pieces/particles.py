import time
import random
import textwrap
import math
import datetime
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageEnhance, ImageChops
from PIL import ImageFilter
from modules import colorutils, badpixels, coloroverlay
from modules.particle_system import ParticleSystem
from modules.particle import Particle




def main(run = True) :
	global config, directionOrder, ps
	print("---------------------")
	print("Particles Loaded")
	colorutils.brightness = config.brightness
	config.canvasImageWidth = config.screenWidth
	config.canvasImageHeight = config.screenHeight
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


	for i in range(0,ps.numUnits):
		emitParticle()

	setUp()

	if(run) : runWork()


def emitParticle():
	global config, ps
	p = Particle(ps)
	p.objWidth = ps.objWidth
	p.objHeight = ps.objHeight
	p.xPosR = config.screenWidth/2 - ps.centerRangeXMin + round(random.random() * ps.centerRangeXMax) - p.objWidth
	p.yPosR = config.screenHeight/2 + ps.centerRangeYMin - round(random.random() * ps.centerRangeYMax)
	#variance = math.pi/3
	p.direction = random.uniform(math.pi + math.pi/2 - config.variance, math.pi + math.pi/2 + config.variance)
	p.v = random.uniform(ps.speedMin,ps.speedMax)

	if ps.objColor == "rnd" :
		p.fillColor = colorutils.randomColor(ps.config.brightness)
		p.outlineColor = colorutils.getSunsetColors(ps.config.brightness/2)
	else :
		p.fillColor = config.fillColor #(240,150,0,100)
		p.outlineColor = config.outlineColor #(100,0,0,100)

	p.setUpParticle()
	ps.unitArray.append(p)

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def setUp():
	global config
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
	## Fade trails or not...
	config.draw.rectangle((0,0,config.screenWidth-1, config.screenHeight-1), fill=config.bgColor, outline=None)

	for p in ps.unitArray:
		p.update()
		p.render()

		if(p.remove == True) :
			ps.unitArray.remove(p)
			if len(ps.unitArray) < config.numUnits + 5 :
				emitParticle()
				emitParticle()
				emitParticle()

	if random.random() < .0005 and ps.changeCohesion == True:
		ps.cohesionDistance = random.uniform(8,30)
		#print(ps.cohesionDistance)

	if (config.overallBlur > 0) :
		config.image = config.image.filter(ImageFilter.GaussianBlur(radius=config.overallBlur))
	config.render(config.image, 0,0)
		


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def callBack() :
	global config, XOs
	return True

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''



