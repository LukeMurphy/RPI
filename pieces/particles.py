import time
import random
import textwrap
import math
import datetime
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageEnhance, ImageChops
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

	config.fontColorVals = ((workConfig.get("diag", 'fontColor')).split(','))
	config.fontColor = tuple(map(lambda x: int(int(x)  * config.brightness), config.fontColorVals))
	config.outlineColorVals = ((workConfig.get("diag", 'outlineColor')).split(','))
	config.outlineColor = tuple(map(lambda x: int(int(x) * config.brightness) , config.outlineColorVals))


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
	ps.borderCollisions = (workConfig.getboolean("particleSystem", 'borderCollisions'))
	ps.cohesionDistance = float(workConfig.get("particleSystem", 'cohesionDistance'))
	ps.repelDistance = float(workConfig.get("particleSystem", 'repelDistance'))

	ps.distanceFactor = float(workConfig.get("particleSystem", 'distanceFactor'))
	ps.clumpingFactor = float(workConfig.get("particleSystem", 'clumpingFactor'))
	ps.repelFactor = float(workConfig.get("particleSystem", 'repelFactor'))

	ps.cohesionDegrades = float(workConfig.get("particleSystem", 'cohesionDegrades'))
	ps.speedMin = float(workConfig.get("particleSystem", 'speedMin'))
	ps.speedMax = float(workConfig.get("particleSystem", 'speedMax'))
	ps.numUnits = int(workConfig.get("particleSystem", 'numUnits'))
	config.trailingFade = int(workConfig.get("particleSystem", 'trailingFade'))

	for i in range(0,ps.numUnits):
		p = Particle(ps)
		p.xPosR = config.screenWidth - 40
		p.yPosR = config.screenHeight/2 + random.uniform(-40,40)
		variance = math.pi/3
		p.direction = random.uniform(math.pi + math.pi/2 - variance, math.pi + math.pi/2 + variance)
		p.v = random.uniform(ps.speedMin,ps.speedMax)
		ps.unitArray.append(p)

	setUp()

	if(run) : runWork()


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def setUp():
	global config
	pass

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def runWork():
	global blocks, config, XOs
	#gc.enable()
	while True:
		iterate()
		time.sleep(config.delay)  

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def iterate() :
	global config, ps
	## Fade trails or not...
	config.draw.rectangle((0,0,config.screenWidth-1, config.screenHeight-1), fill=(0,0,0,config.trailingFade), outline=None)

	for p in ps.unitArray:
		p.update()
		p.render()

	if random.random() < .0005 :
		#ps.cohesionDistance = random.uniform(8,30)
		print(ps.cohesionDistance)
		print(config.trailingFade)

	config.render(config.image, 0,0)
		


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def callBack() :
	global config, XOs
	return True

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''



