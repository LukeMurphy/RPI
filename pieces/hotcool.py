import time  
import random
import PIL.Image, PIL.ImageTk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import textwrap
import math
from modules import colorutils
import gc

########################
#scroll speed and steps per cycle
scrollSpeed = 0.0006
stroopSpeed = 0.1
steps = 2
stroopSteps = 2
stroopFontSize = 30
fontSize = 14
vOffset  = -1
opticalOpposites = True
higherVariability = False
verticalBg = False
verticalBgColor = (0,0,0)
#countLimit = 6
count = 0
blocks = []
simulBlocks = 2
colorMode = True

####################################################################

class Block:

	direction = "down"
	word = "HOT"
	color = (255,0,0)
	bgColor = (0,255,255)
	speed = 2
	speedMultiplier = 1
	x = 0
	y = 0
	dx = -1
	dy = 0
	startx = 0
	starty = 0
	endx = 0
	endy = 0

	reveal = 0
	revealSpeed = 1
	revealSpeedMax = 3

	colorWord = "RED"
	colorOfWord = (0,0,0)
	directionStr = "Left"

	setForRemoval = False

	def __init__(self, iid=0) :
		self.iid = iid
		

	def remove(self, arrayList) :
		arrayList.remove(self)

	def make(self, colorMode=True) :

		config = self.config
		choice = int(random.uniform(1,8))
		brightness = config.brightness
		brightness = random.uniform(self.config.minBrightness,1.1)
		opticalOpposites = False if (random.random() > .5) else True
		self.verticalTileSize = int(config.screenHeight/self.displayRows) if self.displayRows != config.rows else config.tileSize[1]

		if(colorMode != True) : choice = int(random.uniform(8,10))

		#choice = 3 if (random.random() > .5) else 5
		#choice = 4 if (random.random() > .5) else 6
		#choice = 9

		if(choice == 1) :colorWord, colorOfWord = "YELLOW",(255,0,225)
		if(choice == 2) :colorWord, colorOfWord = "VIOLET",(230,225,0)
		if(choice == 3) :colorWord, colorOfWord = "RED",(0,255,0)
		if(choice == 4) :colorWord, colorOfWord = "BLUE",(225,100,0)
		if(choice == 5) :colorWord, colorOfWord = "GREEN",(255,0,0)
		if(choice == 6) :colorWord, colorOfWord = "ORANGE",(0,0,200)
		if(choice == 7) :colorWord, colorOfWord = "GRAY",(50,50,50)
		if(choice == 8) :colorWord, colorOfWord = "BLACK",(0,0,0)
		if(choice >= 9) :colorWord, colorOfWord = "WHITE",(250,250,250)
		

		clr = colorOfWord

		# Draw Background Color
		# Optical (RBY) or RGB opposites
		if(opticalOpposites) :
			if(colorWord == "RED") : bgColor = tuple(int(a*brightness) for a in ((255,0,0)))
			if(colorWord == "GREEN") : bgColor = tuple(int(a*brightness) for a in ((0,255,0)))
			if(colorWord == "BLUE") : bgColor = tuple(int(a*brightness) for a in ((0,0,255)))
			if(colorWord == "YELLOW") : bgColor = tuple(int(a*brightness) for a in ((255,255,0)))
			if(colorWord == "ORANGE") : bgColor = tuple(int(a*brightness) for a in ((255,125,0)))
			if(colorWord == "VIOLET") : bgColor = tuple(int(a*brightness) for a in ((200,0,255)))
			if(colorWord == "BLACK") : bgColor = tuple(int(a*brightness) for a in ((250,250,250)))
			if(colorWord == "WHITE") : bgColor = tuple(int(a*brightness) for a in ((0,0,0)))
			if(colorWord == "GRAY") : bgColor = tuple(int(a*brightness) for a in ((200,200,200)))
		else:
			 bgColor = colorutils.colorCompliment(clr, brightness)

		clr = tuple(int(a*brightness) for a in (clr))

		# Setting 2 fonts - one for the main text and the other for its "border"... not really necessary
		font = ImageFont.truetype(config.path + '/assets/fonts/freefont/FreeSansBold.ttf',self.fontSize)
		font2 = ImageFont.truetype(config.path + '/assets/fonts/freefont/FreeSansBold.ttf',self.fontSize)
		pixLen = config.draw.textsize(colorWord, font = font)

		dims = [pixLen[0],pixLen[1]]
		if(dims[1] < self.verticalTileSize) : dims[1] = self.verticalTileSize + 2

		vPadding = int(.75 * config.tileSize[0])
		self.presentationImage = PIL.Image.new("RGBA", (dims[0]+vPadding,dims[1]))
		self.image = PIL.Image.new("RGBA", (dims[0]+vPadding,0))
		draw  = ImageDraw.Draw(self.presentationImage)
		iid = self.image.im.id
		draw.rectangle((0,0,dims[0]+config.tileSize[0], dims[1]), fill=bgColor)

		# Draw the text with "borders"
		indent = int(.05 * config.tileSize[0])

		for i in range(1, self.shadowSize) :
			draw.text((indent + -i,-i),colorWord,(0,0,0),font=font2)
			draw.text((indent + i,i),colorWord,(0,0,0),font=font2)
		draw.text((indent + 0,0),colorWord,clr,font=font)

		offset = int(random.uniform(1,config.screenWidth-20))
		vOffset = int(random.uniform(0, self.displayRows)) * self.verticalTileSize
		if(higherVariability) : vOffset += int(random.uniform(-config.tileSize[0]/10, config.tileSize[0]/10))

		self.wd = dims[0]
		self.ht = dims[1]
		
		self.y = vOffset
		#self.y = int(random.uniform(0,config.screenHeight))
		self.x  = int(random.uniform(-self.wd,config.screenWidth + self.wd))
		#self.x = config.screenWidth/2
		
		self.startx = self.x
		self.starty = self.y

		self.dx = int(random.uniform(-self.speed,self.speed)) * self.speedMultiplier
		self.dy = int(random.uniform(-self.speed,self.speed)) * self.speedMultiplier
		if(self.dx == 0) : self.dx = -1
		if(self.dy == 0) : self.dy = -1

		self.endx = -self.wd if self.dx < 0 else config.screenWidth
		self.endy = -self.ht if self.dy < 0 else config.screenHeight

		self.revealSpeed = int(random.uniform(1,self.revealSpeedMax))
		#print(self.dx, self.end, self.x)

	def callBack(self) :
		self.setForRemoval = True
		pass

	def move(self) :
		if(self.setForRemoval!=True) :
			self.image.paste(self.presentationImage, (0,0))

			self.x += self.dx
			self.y += self.dy

			if(self.dy > 0 and self.y >= self.endy) :
				self.callBack()
			if(self.dy < 0 and self.y < self.endy) :
				self.callBack()
			if(self.dx > 0 and self.x >= self.endx) :
				self.callBack()
			if(self.dx < 0 and self.x < self.endx) :
				self.callBack()		

	def appear(self) :
		if(self.setForRemoval!=True) :

			dims = self.presentationImage.size
			self.reveal += self.revealSpeed
			self.image = PIL.Image.new("RGBA", (dims[0],self.reveal))

			dr = ImageDraw.Draw(self.image)
			dr.rectangle((0,0,100,5), fill=(0,255,0))
			
			segment = self.presentationImage.crop((0,0,dims[0],self.reveal))
			self.image.paste(segment, (0,0))


			if (self.reveal  > dims[1]) : self.callBack()

	def update(self) :
		self.appear()
		self.move()


####################################################################


def callBack() :
	global config
	pass

def iterate( n = 0) :
	global config, blocks
	for n in range (0, len(blocks)) :
		block = blocks[n]
		config.render(block.image, block.x, block.y, block.image.size[0], block.image.size[1], False, False, False)
		block.update()
		if(block.setForRemoval==True) : makeBlock()

	# cleanup the list
	blocks[:] = [block for block in blocks if block.setForRemoval!=True]
	config.updateCanvas()

	if len(blocks) == 0 : exit()

def runWork():
	global stroopSpeed, blocks, config
	gc.enable()
	while True:
		iterate()
		time.sleep(stroopSpeed)

def makeBlock() :
	global config, workConfig, blocks, stroopSpeed, stroopSteps, displayRows, colorMode
	fontSize = int(workConfig.get("stroop", 'fontSize'))
	vOffset = int(workConfig.get("stroop", 'vOffset'))
	stroopSpeed = float(workConfig.get("stroop", 'stroopSpeed'))
	stroopSteps = float(workConfig.get("stroop", 'stroopSteps'))
	stroopFontSize = int(workConfig.get("stroop", 'stroopFontSize'))
	shadowSize = int(workConfig.get("stroop", 'shadowSize'))
	higherVariability = (workConfig.getboolean("stroop", 'higherVariability'))
	verticalBg = (workConfig.getboolean("stroop", 'verticalBg'))
	displayRows = int(workConfig.get("stroop", 'displayRows'))

	config.opticalOpposites = True

	block = Block()
	block.config = config
	block.fontSize = stroopFontSize
	block.shadowSize = shadowSize
	block.displayRows = displayRows
	block.make(colorMode)
	block.blocksRef = blocks
	blocks.append(block)
	gc.collect()

	if(colorMode == False) :
		if (random.random() > .982) :
			colorMode = True
			print("ColorMode changed back")
	else :
		if(random.random() > .985) :
			colorMode = False
			print("ColorMode change  to b/w")

def main(run = True) :
	global config, workConfig, blocks, simulBlocks
	print("HotCool Loaded")
	#[stroop]

	blocks = []
	for i in range (0,simulBlocks) : makeBlock()

	if(run) : runWork()


def runStroop(run=True) :
	global config, opticalOpposites
	while run:
		numRuns = int(random.uniform(2,6))
		numRuns =  1
		for i in range(0,numRuns) : 
			opticalOpposites = False if (opticalOpposites == True) else True
			stroopSequence()		


def getDirection() :
	d = int(random.uniform(1,4))
	direction = "Left"
	if (d == 1) : direction = "Left"
	if (d == 2) : direction = "Right"
	if (d == 3) : direction = "Bottom"
	return direction










	
#####################


