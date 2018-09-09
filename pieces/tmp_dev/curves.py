#!/usr/bin/python
import PIL.Image
from PIL import Image, ImageDraw, ImageMath, ImageEnhance
from PIL import ImageChops
#from modules import colorutils
# Import the essentials to everything
import time, random, math

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
canvasBase =  dict(width=160,height=160)
origin = [80,80]
pos = 0
lastCoord = [0,0]
nextCoord = [0,0]
v = [0,0]
angle = 0 #math.pi/2
phase = math.pi/4
rotationAngle = 90
currentAngle = 0
runRun = True
d = .5
segments = 80

class Lsys :
	
	n = 5
	c = 0
	recursionLimit = 5
	strg = ""

	useRandom = True
	foliage = False
	incrRange = 6
	incrEnd = 6
	angle = 20
	dFactor = 1
	dFactorMultiplier = .8
	
	s = ""
	incrStart = 0
	instruction = ""
	xPos = 0
	yPos = 0
	origin = dict(xpos=0,ypos=0)
	a = 0
	branchPoint = []
	branch = 0
	segments = 100

	#nodeSpriteContainer:Sprite
	
	def __init__(self, segs) :
		print("Init Lsys")
		incrRange = 100
		incrEnd = 100
		incrStart = 0
		segments = segs
		self.setUpNewDrawingParameters()
		
	
	def setUpNewDrawingParameters(self) :
		self.c = 0
		strgArr = ["F"] * self.segments
		self.strg = str(strgArr)

			
	def setupDrawing(self) :
		self.branchPoint = []
		self.xPos = self.origin['xPos']
		self.yPos = self.origin['yPos']

			

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''
def drawBasic(self):
	listStrg = list(strg)
	for i in range(len(self.strg)):

'''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


def drawLines(arg="F") :
	
	global config, L, origin, lastCoord, nextCoord, angle, currentAngle, v, d, phase

	pi = math.pi
	

	'''
	x	=	16sin^3t	
	y	=	13cost-5cos(2t)-2cos(3t)-cos(4t).
	'''
	#print(v)
	
	currentAngle += angle

	if (arg == "F") :
		
		v = [d * math.sin(currentAngle), d * math.cos(currentAngle)]

		v= [d * math.log1p(math.fabs(currentAngle)) * math.sin(currentAngle) *  math.cos(currentAngle), 
			d * math.sqrt(math.fabs(currentAngle)) * math.cos(currentAngle)]

		a = currentAngle + phase
		v = [16 * d * math.sin(a)* math.sin(a)* math.sin(a), 
			d * (13 * math.cos(a)-5*math.cos(2*a)-2*math.cos(3*a)-math.cos(4*a))]
	
		nextCoord[0] =  v[0]
		nextCoord[1] =  v[1]
		config.draw.line((lastCoord[0] + origin[0],lastCoord[1]+ origin[1], nextCoord[0] + origin[0],nextCoord[1] + origin[1]), fill=(int(config.brightness * 255),0,0))
		lastCoord[0] = nextCoord[0]
		lastCoord[1] = nextCoord[1]
		#print(lastCoord, nextCoord)

	if (arg == "-") :
		currentAngle -= angle

	if (arg == "+") :
		currentAngle += angle

	# reseting render image size
	#print (nextCoord)

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def main(run = True) :
	global config, workConfig
	setUp()
	if(run) : runWork()

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def setUp() :
	global L, config, pos, angle, currentAngle, origin, lastCoord, nextCoord, segments
	config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	config.draw  = ImageDraw.Draw(config.image)
	config.id = config.image.im.id
	L = Lsys(segments)
	angle = math.pi/segments
	lastCoord = [0,0]
	return  True

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def runWork():
	global runRun
	while True:
		iterateAlt()
		time.sleep(.001)

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def iterateAlt() :
	global config, L, pos, runRun, segments, d, currentAngle, phase, origin, rotationAngle
	if pos < 20 :
		for i in range(segments * 2) :
			drawLines(L.strg[i])
		pos += 1
		d += .3
		phase += math.pi/4
		#origin[0] += -5


	else :
		if(runRun) : print("Done!")
		runRun = False
	
	 
	if(runRun) : 
		config.renderImageFull = config.renderImageFull.rotate(rotationAngle)
		config.renderImageFull.paste(config.image,(0,0),config.image)
		config.renderImageFull = config.renderImageFull.rotate(-rotationAngle)
	config.render(config.renderImageFull, 0, 0,192,192)	
	

def iterate() :
	global config, L, pos, runRun
	if pos < len(L.strg) :
		drawLines(L.strg[pos])
		pos += 1
	else :
		if(runRun) : print("Done!")
		runRun = False
	config.render(config.image, 0, 0,192,192)

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def callBack() :
	global config
	pass
	#animator()

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


