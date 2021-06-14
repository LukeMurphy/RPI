import math
import random
import textwrap
import time
from modules.configuration import bcolors
from modules import badpixels, coloroverlay, colorutils, panelDrawing
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
		blockWidth = 128
		blockHeight = 128
		radius = 4
		arc = 2 * math.pi / self.numberOfLeaves
		for i in range(0, self.numberOfLeaves) :
			leaf = Leaf(self.config, self.origin)
			leaf.radius = radius
			leaf.blockWidth = 128
			leaf.blockHeight = 128
			leaf.radians =  arc * i
			#leaf.scaleMax = self.scale
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
			if random.random() <= self.config.leafDrawProb and self.leafArray[i].unit == 0:
				self.leafArray[i].render()
			if random.random() <= self.config.flowerDrawProb and self.leafArray[i].unit == 1:
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
		self.scaleMax = random.uniform(.1, self.config.scaleMax)
		self.scalespeed = random.uniform(.001,.02)

		self.rotation = 0
		self.rotationSpeed = self.config.rotationSpeedMax - random.random() * self.config.rotationSpeedMax * 2

		self.ty = 1
		self.tx = 1



	def getFromBaseImage(self) :

		self.imageElement = self.config.elementArray[self.unit][0]
		self.leafType = self.config.elementArray[self.unit][1]

		# probably not necessary to resize the original element - degrades sometimes
		#self.imageElement = self.imageElement.resize((round(self.blockWidth * self.scale), round(self.blockHeight * self.scale)))


		clrBlock = Image.new("RGBA", (self.blockWidth, self.blockWidth))
		clrBlockDraw = ImageDraw.Draw(clrBlock)

		# Color - Leaves
		if self.leafType == 0 :
			clr = colorutils.getRandomColorHSV(
				hMin=40.0,
				hMax=170.0,
				sMin=.850,
				sMax=1.0,
				vMin=0.150,
				vMax=.50,
				dropHueMin=0,
				dropHueMax=0,
				a=round(random.uniform(200,255)),
			)

			if clr[1] > 100 and clr[0] > 100 :
				clr = (150,255,0,255)
				
		# Color - "flower"
		if self.leafType == 1:
			clr = colorutils.getRandomColorHSV(
				hMin=250.0,
				hMax=350.0,
				sMin=.850,
				sMax=1.0,
				vMin=0.50,
				vMax=1.0,
				dropHueMin=0,
				dropHueMax=0,
				a=round(random.uniform(220,255)),
			)

			if random.random() < .1 :
				clr = colorutils.getRandomColorHSV(
				hMin=350.0,
				hMax=25.0,
				sMin=.850,
				sMax=1.0,
				vMin=0.50,
				vMax=1.0,
				dropHueMin=0,
				dropHueMax=0,
				a=round(random.uniform(220,255)),
				)

		clrBlockDraw.rectangle((0, 0, self.blockWidth, self.blockWidth), fill=clr)
		self.imageElement = ImageChops.multiply(clrBlock, self.imageElement)
		self.rotation = 270 - round(180 / math.pi * self.radians)
		# rotate here or when scaling and rendering each cycle ... not both 
		#self.imageElement = self.imageElement.rotate( self.rotation , center=None, expand=0)
		self.scale = .5


	def setup(self) :
		self.unit = math.floor(random.uniform(0, len(self.config.elementArray)))

		if random.random() <= config.flowerProb : 
			self.unit = 1
		else :
			self.unit = 0


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

		if self.scale <= self.scaleMax and self.unit == 0: 
			self.scale += self.scalespeed
		if self.unit == 1:
			self.scale += self.scalespeed/20.0

		if self.unit == 0 :
			self.tx = self.radius * math.cos(self.radians) 
			self.ty = self.radius * math.sin(self.radians) 
		else :
			self.tx = self.radius * math.cos(self.radians) /50.0
			self.ty -= self.scalespeed *100


		self.loc_x = round(self.tx + self.origin[0] - self.blockWidth * self.scale/2)
		self.loc_y = round(self.ty + self.origin[1] - self.blockHeight * self.scale/2)

		self.rotation += self.rotationSpeed

		if (self.loc_x < 0 - self.blockWidth * self.scale/2 or 
			self.loc_x > self.config.canvasImageWidth +self.blockWidth * self.scale/2 or 
			self.loc_y < 0  -self.blockHeight * self.scale/2 or 
			self.loc_y > self.config.canvasImageHeight + self.blockHeight * self.scale/2) :
			self.radius = 0
			self.setup()
			


	def render(self):
		tempUnit = self.imageElement.resize((round(self.blockWidth * self.scale), round(self.blockHeight * self.scale)))
		tempUnit = tempUnit.rotate(self.rotation, 3, True)
		self.config.canvasImage.paste(tempUnit, (self.loc_x, self.loc_y ), tempUnit)



def iterate():
	global config


	#config.bg.rectangle((0,0, config.canvasImageWidth, config.canvasImageHeight), fill=(200,2,100,100))
	for i in range(0, len(config.Trunk.brandchArray)):
		branch = config.Trunk.brandchArray[i]
		branch.render()

	########### RENDERING AS A MOCKUP OR AS REAL ###########
	if config.useDrawingPoints == True :
		config.panelDrawing.canvasToUse = config.canvasImage
		config.panelDrawing.render()
	else :
		config.render(config.canvasImage, 0, 0)

	config.t2 = time.time()
	delta = config.t2 - config.t1

	if delta > config.timeToComplete:
		restartPiece()


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

	config.spriteSheet = (workConfig.get("leaf-factory", "spriteSheet"))
	path = config.path + config.spriteSheet
	config.spriteSheet = Image.open(path, "r")
	print("loading : ", path)


	config.flowerProb = float(workConfig.get("leaf-factory", "flowerProb"))
	config.drawProb = float(workConfig.get("leaf-factory", "drawProb"))
	config.leafDrawProb = float(workConfig.get("leaf-factory", "leafDrawProb"))
	config.flowerDrawProb = float(workConfig.get("leaf-factory", "flowerDrawProb"))
	config.rotationSpeedMax = float(workConfig.get("leaf-factory", "rotationSpeedMax"))
	config.scaleMax = float(workConfig.get("leaf-factory", "scaleMax"))

	### THIS IS USED AS WAY TO MOCKUP A CONFIGURATION OF RECTANGULAR PANELS
	panelDrawing.mockupBlock(config, workConfig)

	sheet = config.spriteSheet.copy()
	blockWidth = 128
	blockHeight = 128
	scale = 1.0
	config.elementArray = []
	radius = 10
	offSet = [200,200]

	"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""




	count = 0
	for row in  range(0,1):
		for col in range(0,2):
			section = sheet.crop((col*blockWidth, row*blockHeight ,col*blockWidth + blockWidth, row*blockHeight  + blockHeight))
			section = section.resize((round(blockWidth * scale), round(blockHeight * scale)))
			config.elementArray.append([section,col])
			count+=1


	'''
	config.elementArray = []
	for i in range(0,2) :
		cntrMarker = Image.new("RGBA", (40,40))
		cntrMarkerDraw = ImageDraw.Draw(cntrMarker)	
		#cntrMarkerDraw.rectangle((0,0, 0 +20,0 +40), fill=(255,255,255,255))
		poly = ((20,0),(12,10),(11,20),(13,30),(20,40),(27,30),(29,20)) 
		cntrMarkerDraw.polygon(poly, fill=(255,255,255,255))

		config.elementArray.append([cntrMarker,i])
	'''


	config.t1 = time.time()
	config.timeToComplete = 100
	config.delay = .02

	"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
	origins  = [[28,128],[200,200],[200,200],[100,180]]
	#origins  = [[128,128]]
	
	config.Trunk = Trunk(config, origins, 4)
	
	config.Trunk.setup(12, scale)
	
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
	global config
	print(bcolors.OKGREEN + "** " + bcolors.BOLD)
	print("Running leaf-factory.py")
	print(bcolors.ENDC)
	# gc.enable()
	while True:
		iterate()
		time.sleep(config.delay)


