# ################################################### #
import time
import random
import math
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageEnhance
from modules import colorutils


def guess():
	pass

def init() :
	global config
	config.alphabetLeft = []
	config.alphabetLeft = [ a for a in config.alphabet]
	config.guessed = []
	config.found = []
	config.wordNotFound = True
	config.lost = False
	config.done = False

	angle = random.random() * 22/7
	config.body = [(4,1,6,2),(5,2,5,3),(5,3,5,5),
	(5,3,3,(random.uniform(0,5))),(5,3,7,(random.uniform(0,5))),
	(5,5,4,(random.uniform(7,9))),(5,5,6,(random.uniform(7,9))),
	(5,5,(random.uniform(4,6)),(random.uniform(4,6))),
	(4.7,5,5,5.4),
	(5,5,5.3,5.3)
	]	

	config.body = [(4,1,6,2),(5,2,5,3),(5,3,5,5),
	(5,3,3,(random.uniform(0,5))),(5,3,7,(random.uniform(0,5))),
	(5,5,4,(random.uniform(7,9))),(5,5,6,(random.uniform(7,9)))
	]

	config.draw.rectangle((0,0, config.screenWidth + abs(config.imageXOffset) ,config.screenHeight + abs(config.imageYOffset)), fill=(5,5,5 + int(round(random.random() * 10)),int(round(random.random() * 10))))
	#if(random.random() < .02) :config.draw.rectangle((0,0, config.screenWidth + abs(config.imageXOffset) ,config.screenHeight + abs(config.imageYOffset)), fill=(15,15,35,6))

	gap = 0
	for i in range(0, len(config.word)) :
		startX = config.textPosX + 10*i
		endX = startX + 8
		#config.draw.line((startX, config.textPosY + 20 , endX, config.textPosY + 20), fill=config.clr)


def drawText(xPos=0, yPos=0, messageString = "", crossout=False) :
	global config
	# Draw the text with "borders"
	indent = int(.05 * config.tileSize[0])
	for i in range(1, config.shadowSize) :
		config.draw.text((indent + -i,-i),messageString,(0,0,0),font=config.font)
		config.draw.text((indent + i,i),messageString,(0,0,0),font=config.font)

	config.draw.text((xPos,yPos), messageString, config.clr ,font=config.font)
	if(crossout == True) :
		#config.draw.line((xPos, yPos + config.fontSize, xPos + config.fontSize/1.5, yPos - config.fontSize/8), fill=config.clr)
		config.draw.line((xPos, yPos + config.fontSize/1.5, 
			xPos + config.fontSize/1.5, 
			yPos + config.fontSize/1.5) , fill=config.clr)

def guess():
	global config

	#vBuffer = 33
	#hBuffer = 30

	#config.draw.rectangle((0,0, config.screenWidth + abs(config.imageXOffset) ,config.screenHeight + abs(config.imageYOffset)), fill=(15,15,30,5))

	if (len(config.alphabetLeft) > 0 and config.wordNotFound == True) :
		ran = int(random.uniform(0,len(config.alphabetLeft)))
		char = config.alphabetLeft[ran]

		pos = config.word.lower().find(char)
		if (pos) != -1 :
			## Correct Guess 
			config.found.append(char)
			config.clr = (255,255,0)
			config.clr = colorutils.randomGray()
			config.clr = colorutils.getRandomRGB()
			config.font = ImageFont.truetype(config.path  + '/assets/fonts/freefont/FreeSansBold.ttf', 20)
			#drawText(config.textPosX + pos * 10,config.textPosY, char)
			#drawText(config.textPosX + pos * 10,config.textPosY, "*")

			xPos = config.letterxOffset + random.uniform(config.hBuffer,config.screenWidth-config.hBuffer) 
			yPos = config.letteryOffset + + random.uniform(config.vBuffer/3,config.screenHeight-config.vBuffer) 

			drawText(xPos, yPos, char.upper(), True)

			if(len(config.found) == len(config.word)) :
				config.wordNotFound = False
				config.lost = False
				config.done = True
				#drawText(30, 5, "Computer Wins!", False)

		else :
			## Incorrect - draw letter & part scaffold
			config.guessed.append(char)
			config.clr = colorutils.randomColor(1)
			config.fontSize = int(random.uniform(10,50))
			config.font = ImageFont.truetype(config.path  + '/assets/fonts/freefont/FreeSansBold.ttf', config.fontSize)

			#xPos = random.random() * config.screenWidth #* 1/3 + config.screenWidth/2
			#yPos = random.random() * config.screenHeight #* 1/3 + config.screenHeight/2

			xPos = config.guessxOffset + random.uniform(config.hBuffer,config.screenWidth-config.hBuffer) 
			yPos = config.guessyOffset + random.uniform(config.vBuffer/3,config.screenHeight-config.vBuffer) 

			drawText(xPos, yPos, char, False)

			# Draw the scaffold / gallows
			if(len(config.guessed) <= len(config.scaffolding)) : 
				coords = config.scaffolding[len(config.guessed) - 1]
				config.draw.line( tuple(15 * x + config.xOffset for x in coords), fill=(50,50,50))

				if(len(config.guessed) >= len(config.scaffolding)) :
					config.draw.line( tuple(15 * x + config.xOffset for x in coords), fill=(100,100,100))

			# Draw the body
			elif(len(config.guessed) <= (len(config.scaffolding) + len(config.body))) :
				coords = config.body[len(config.guessed) - len(config.scaffolding) - 1]

				index  = len(config.guessed) - len(config.scaffolding) - 1

				if( index == 0 ) :
					config.draw.arc((tuple(15 * x + config.xOffset for x in coords)),0,360,fill=(255,0,0))
				elif (index >= 8) :
					config.draw.arc((tuple(15 * x + config.xOffset for x in coords)),0,360,fill=(255,0,0))
				else :
					config.draw.line( tuple(15 * x + config.xOffset for x in coords), fill=(255,0,0))

		config.alphabetLeft.remove(char)

		if(len(config.guessed) >= 17) :
			config.lost = True
			config.done = True
			#drawText(32, 5, "You Lose!", False)


def drawElement() :
	global config
	return True

def redraw():
	#drawText(10,10, config.messageString)
	global config

def changeColor() :
	pass
	return True

def changeCall() :
	pass
	return True

def callBack() :
	global config
	pass

def runWork():
	global config
	while True:
		iterate()
		time.sleep(.01)
		#time.sleep(random.random() * config.redrawSpeed)

def iterate() :
	global config
	redraw()
	guess()

	#config.render(config.image, config.imageXOffset, config.imageYOffset,  config.imageXOffset + config.screenWidth, config.imageYOffset + config.screenHeight)
	config.render(config.image, config.imageXOffset, config.imageYOffset,  config.screenWidth, config.screenHeight)

	if(config.done == True) :
		init()
		time.sleep(config.redrawSpeed)


def main(run = True) :
	global config
	config.redrawSpeed  = float(workConfig.get("hang", 'redrawSpeed')) 
	config.fontSize = int(workConfig.get("hang", 'fontSize'))
	config.shadowSize = int(workConfig.get("hang", 'shadowSize'))
	config.xOffset = int(workConfig.get("hang", 'xOffset'))
	config.imageXOffset = int(workConfig.get("hang", 'imageXOffset'))
	config.imageYOffset = int(workConfig.get("hang", 'imageYOffset'))
	config.hBuffer = int(workConfig.get("hang", 'hBuffer'))
	config.vBuffer = int(workConfig.get("hang", 'vBuffer'))
	config.guessxOffset = int(workConfig.get("hang", 'guessxOffset'))
	config.guessyOffset = int(workConfig.get("hang", 'guessyOffset'))	
	config.letterxOffset = int(workConfig.get("hang", 'letterxOffset'))
	config.letteryOffset = int(workConfig.get("hang", 'letteryOffset'))
	
	config.font = ImageFont.truetype(config.path  + '/assets/fonts/freefont/FreeSansBold.ttf', config.fontSize)
	config.image = Image.new("RGBA", (config.screenWidth + abs(config.imageXOffset), config.screenHeight + abs(config.imageYOffset)))
	config.draw  = ImageDraw.Draw(config.image)
	config.clr = (255,0,0)
	config.textPosY = 40
	config.textPosX = 120

	config.alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
	config.word = "FEAR"
	colorutils.brightness =  .9
	config.messageString = config.word
	
	# (0,10,2,6) (4,10,2,6)
	config.scaffolding = [(2,15,2,10),(2,10,2,6),(2,6,2,2),(2,2,2,0),(2,2,4,0),(2,0,5,0),(5,0,5,1)]
	#config.body = [(4,1,6,2),(5,2,5,3),(5,3,5,5),(5,3,3,3),(5,3,7,3),(5,5,4,7),(5,5,6,7),(5,5,5,6),(5,5,4,4),(5,5,6,6)]
	config.body = [(4,1,6,2),(5,2,5,3),(5,3,5,5),(5,3,3,3),(5,3,7,3),(5,5,4,7),(5,5,6,7)]

	init()
	
	if(run) : runWork()
