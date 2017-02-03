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


	config.draw.rectangle((0,0,config.screenWidth,config.screenHeight), fill=(15,15,30,15))

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

	vBuffer = 33
	hBuffer = 30


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



			xPos = 3 + random.uniform(hBuffer,config.screenWidth-hBuffer) 
			yPos = random.uniform(vBuffer/3,config.screenHeight-vBuffer) 

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
			config.fontSize = int(random.uniform(10,30))
			config.font = ImageFont.truetype(config.path  + '/assets/fonts/freefont/FreeSansBold.ttf', config.fontSize)

			xPos = random.random() * config.screenWidth #* 1/3 + config.screenWidth/2
			yPos = random.random() * config.screenHeight #* 1/3 + config.screenHeight/2


			xPos = 3 + random.uniform(hBuffer,config.screenWidth-hBuffer) 
			yPos = random.uniform(vBuffer/3,config.screenHeight-vBuffer) 

			drawText(xPos, yPos, char, False)

			# Draw the scaffold / gallows
			if(len(config.guessed) <= len(config.scaffolding)) : 
				coords = config.scaffolding[len(config.guessed) - 1]
				config.draw.line( tuple(15 * x + config.xOffset for x in coords), fill=(10,10,10))

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

	config.render(config.image, 0, 0, config.screenWidth, config.screenHeight)

	if(config.done == True) :
		init()
		time.sleep(.02)






def main(run = True) :
	global config
	config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	config.draw  = ImageDraw.Draw(config.image)
	config.redrawSpeed  = float(workConfig.get("hang", 'redrawSpeed')) 
	config.fontSize = int(workConfig.get("hang", 'fontSize'))
	config.shadowSize = int(workConfig.get("hang", 'shadowSize'))
	config.font = ImageFont.truetype(config.path  + '/assets/fonts/freefont/FreeSansBold.ttf', config.fontSize)
	config.clr = (255,0,0)
	config.textPosY = 40
	config.textPosX = 120

	config.alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
	config.word = "FEAR"
	colorutils.brightness =  1
	config.messageString = config.word
	config.xOffset = 15
	# (0,10,2,6) (4,10,2,6)
	config.scaffolding = [(2,15,2,10),(2,10,2,6),(2,6,2,2),(2,2,2,0),(2,2,4,0),(2,0,5,0),(5,0,5,1)]
	#config.body = [(4,1,6,2),(5,2,5,3),(5,3,5,5),(5,3,3,3),(5,3,7,3),(5,5,4,7),(5,5,6,7),(5,5,5,6),(5,5,4,4),(5,5,6,6)]
	config.body = [(4,1,6,2),(5,2,5,3),(5,3,5,5),(5,3,3,3),(5,3,7,3),(5,5,4,7),(5,5,6,7)]


	init()
	
	if(run) : runWork()
