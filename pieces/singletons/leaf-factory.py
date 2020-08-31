import math
import random
import textwrap
import time

from modules import badpixels, coloroverlay, colorutils
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFont, ImageOps




"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

class Trunk:

	def __init__(self, config, origins=[[0,0]], numberOfFactories=1,):
		self.config = config
		self.xPos = 0
		self.yPos = 0
		self.redraw = False
		self.draw = ImageDraw.Draw(config.canvasImage)
		self.brandchArray = []
		self.numberOfFactories = numberOfFactories
		self.origins = origins

	def setup(self, numberOfLeavesPerFactory, scale):
		for i in range(0, self.numberOfFactories) :

			if i > len(self.origins) - 1 :
				origin = self.origins[0]
			else :
				origin = self.origins[i]
			branch = LeafFactory(self.config, numberOfLeavesPerFactory, origin, scale)
			self.brandchArray.append(branch)
			branch.setup()



"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

class LeafFactory():

	def __init__(self, config, numberOfLeaves, origin, scale):
		self.config = config
		self.xPos = 0
		self.yPos = 0
		self.redraw = False
		self.draw = ImageDraw.Draw(config.canvasImage)
		self.leafArray = []
		self.numberOfLeaves = numberOfLeaves
		self.origin = origin
		self.scale = scale

	def setup(self):
		blockWidth = 256
		blockHeight = 256
		radius = 4
		arc = 2 * math.pi / self.numberOfLeaves
		for i in range(0, self.numberOfLeaves) :
			leaf = Leaf(self.config, self.origin)
			leaf.radius = radius
			leaf.blockWidth = 256
			leaf.blockHeight = 256
			leaf.radians =  arc * i
			leaf.scaleMax = self.scale
			leaf.scale = self.scale

			self.leafArray.append(leaf)
			leaf.setup()
			leaf.render()

	def render(self):
		if random.random() > .9999 :
			self.origin[0] = round(random.uniform(50, self.config.canvasImageWidth))
			self.origin[1] = round(random.uniform(50, self.config.canvasImageHeight))

		for i in range(0, self.numberOfLeaves) :
			self.leafArray[i].move()
			self.leafArray[i].render()


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

class Leaf():

	def __init__(self, config, origin):
		self.config = config
		self.xPos = 0
		self.yPos = 0
		self.redraw = False
		self.draw = ImageDraw.Draw(config.canvasImage)
		self.origin = origin

		self.angle = 0
		self.unit = 0
		self.scaleMax = 1.0
		self.scalespeed = .05



	def getFromBaseImage(self) :

		self.imageElement = self.config.elementArray[self.unit]
		self.imageElement = self.imageElement.resize((round(self.blockWidth * self.scale), round(self.blockHeight * self.scale)))


		clrBlock = Image.new("RGBA", (self.blockWidth, self.blockWidth))
		clrBlockDraw = ImageDraw.Draw(clrBlock)
		clr = colorutils.getRandomColorHSV(
			hMin=30.0,
			hMax=160.0,
			sMin=.850,
			sMax=1.0,
			vMin=0.150,
			vMax=.50,
			dropHueMin=0,
			dropHueMax=0,
			a=round(random.uniform(200,255)),
		)

		if random.random() > .9 :
			clr = colorutils.getRandomColorHSV(
				hMin=300.0,
				hMax=360.0,
				sMin=.850,
				sMax=1.0,
				vMin=0.850,
				vMax=1.0,
				dropHueMin=0,
				dropHueMax=0,
				a=round(random.uniform(220,255)),
			)

		clrBlockDraw.rectangle((0, 0, self.blockWidth, self.blockWidth), fill=clr)
		self.imageElement = ImageChops.multiply(clrBlock, self.imageElement)
		self.rotation = 270 - round(180 / math.pi * self.radians)
		self.imageElement = self.imageElement.rotate( self.rotation , center=None, expand=0)
		self.scale = .1


	def setup(self) :
		self.unit = math.floor(random.uniform(0, len(self.config.elementArray)))

		#if random.random() > .5 : self.unit = 0

		self.getFromBaseImage()

		self.tx = self.radius * math.cos(self.radians) 
		self.ty = self.radius * math.sin(self.radians) 


		self.loc_x = round(self.tx + self.origin[0] - self.blockWidth * self.scale/2)
		self.loc_y = round(self.ty + self.origin[1] - self.blockHeight * self.scale/2)

		self.speed = 1 + random.random() * 1

		
		#self.section = self.config.elementArray[i].rotate(math.pi * 180 * random.random())
		#self.config.canvasImage.paste(self.section,(self.origin[0],self.origin[1]), self.section)
		

	def move(self):
		self.radius += self.speed

		if self.scale <= self.scaleMax : 
			self.scale += self.scalespeed


		self.tx = self.radius * math.cos(self.radians) 
		self.ty = self.radius * math.sin(self.radians) 

		self.loc_x = round(self.tx + self.origin[0] - self.blockWidth * self.scale/2)
		self.loc_y = round(self.ty + self.origin[1] - self.blockHeight * self.scale/2)

		if (self.loc_x < 0 - self.blockWidth * self.scale/2 or 
			self.loc_x > self.config.canvasImageWidth +self.blockWidth * self.scale/2 or 
			self.loc_y < 0  -self.blockHeight * self.scale/2 or 
			self.loc_y > self.config.canvasImageHeight + self.blockHeight * self.scale/2) :
			self.radius = 0
			self.setup()
			


	def render(self):
		tempUnit = self.imageElement.resize((round(self.blockWidth * self.scale), round(self.blockHeight * self.scale)))
		self.config.canvasImage.paste(tempUnit, (self.loc_x, self.loc_y ), tempUnit)





"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""




def main(run=True):
	global config, directionOrder, workConfig
	print("---------------------")
	print("leaf-factory Loaded")

	config.brightness = float(workConfig.get("displayconfig", "brightness"))
	colorutils.brightness = config.brightness
	config.canvasImageWidth = config.screenWidth
	config.canvasImageHeight = config.screenHeight

	config.canvasImage = Image.new(
		"RGBA", (config.canvasImageWidth, config.canvasImageHeight)
	)

	config.bg = ImageDraw.Draw(config.canvasImage)	
	config.bg.rectangle((0,0, config.canvasImageWidth, config.canvasImageHeight), fill=(100,100,100,255))
	#config.canvasImage.paste(bg, (0,0), bg)

	path = config.path + "assets/imgs/drawings/21-2.png"
	config.spriteSheet = Image.open(path, "r")
	print("loading : ", path)

	sheet = config.spriteSheet.copy()
	blockWidth = 256
	blockHeight = 256
	scale = .41
	config.elementArray = []
	radius = 10
	offSet = [200,200]

	"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
	count = 0
	for row in  range(0,4):
		for col in range(0,6):
			section = sheet.crop((col*blockWidth, row*blockHeight ,col*blockWidth + blockWidth, row*blockHeight  + blockHeight))
			section = section.resize((round(blockWidth * scale), round(blockHeight * scale)))
			config.elementArray.append(section)
			count+=1


	'''

	arc = 2 * math.pi / len(config.elementArray)

	for i in range(0,len(config.elementArray)) :
		section = config.elementArray[i]
		radians =  arc * i
		rotation = 270 - round(180 / math.pi * radians)
		tx = radius * math.cos(radians) 
		ty = radius * math.sin(radians) 

		loc_x = round(tx + offSet[0] - blockWidth * scale/2)
		loc_y = round(ty + offSet[1] - blockHeight * scale/2)

		section = section.rotate( rotation , center=None, expand=0)
		config.canvasImage.paste(section, (loc_x, loc_y ), section)


		test = Image.new("RGBA", (blockWidth,blockHeight))
		testDraw = ImageDraw.Draw(test)	
		testDraw.rectangle((blockWidth/2, blockHeight/2, blockWidth/2 +4, blockHeight/2 +4), fill=(255,0,0,255))
		test = test.resize((round(blockWidth * scale), round(blockHeight * scale)))
		config.canvasImage.paste(test,  (loc_x, loc_y ), test)

	'''
	


	config.t1 = time.time()
	config.timeToComplete = 100
	config.delay = .02

	"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
	origins  = [[128,128],[200,200],[200,200],[100,180]]
	
	config.Trunk = Trunk(config, origins, 4)
	
	config.Trunk.setup(24, scale)
	
	"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

	cntrMarker = Image.new("RGBA", (256,256))
	cntrMarkerDraw = ImageDraw.Draw(cntrMarker)	
	cntrMarkerDraw.rectangle((0,0, 0 +10,0 +10), fill=(255,230,0,255))
	#config.canvasImage.paste(cntrMarker, (origins[0][0]-5, origins[0][1]-5), cntrMarker)
	

	if run:
		runWork()

def restartPiece() :
	config.t1 = time.time()


def runWork():
	global blocks, config, XOs
	# gc.enable()
	while True:
		iterate()
		time.sleep(config.delay)


def iterate():
	global config


	config.bg.rectangle((0,0, config.canvasImageWidth, config.canvasImageHeight), fill=(2,200,10,100))
	for i in range(0, len(config.Trunk.brandchArray)):
		branch = config.Trunk.brandchArray[i]
		branch.render()

	config.render(config.canvasImage, 0, 0)

	config.t2 = time.time()
	delta = config.t2 - config.t1

	if delta > config.timeToComplete:
		restartPiece()
