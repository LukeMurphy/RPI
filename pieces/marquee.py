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
	config.draw.rectangle((0,0,config.screenWidth,config.screenHeight), fill=(15,15,30,5))


	config.perimeter = []

	for i in range (0,config.screenWidth) : config.perimeter.append([i,0])

	for i in range (1,config.screenHeight) : config.perimeter.append([config.screenWidth-1,i])

	for i in range (config.screenWidth-1,0,-1) : config.perimeter.append([i,config.screenHeight-1])
	
	for i in range (config.screenHeight,1,-1) : config.perimeter.append([0,i])

	config.pattern = [0,0,0,0,0,0,0,0,0,0,1,1,1,1]

	config.offset = 0


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

def drawMarquee() :
	drawText(10, 10, "TEST", False)
	pass

def drawElement() :
	global config
	return True

def redraw():
	global config
	drawText(10, 10, "TEST", False)


	patternA = config.pattern[config.offset:]
	patternB = config.pattern[:config.offset]
	config.pattern = patternA + patternB



	count = 0

	for p in config.perimeter :
		if(config.pattern[count] == 1) :
			config.draw.rectangle((p[0],p[1],p[0]+2,p[1]+2), fill=(255,0,0))
		else:
			config.draw.rectangle((p[0],p[1],p[0]+2,p[1]+2), fill=(0,0,0))
		count += 1
		if(count >= len(config.pattern)) :
			count = 0

	config.offset += 1
	if(config.offset >= len(config.pattern)) : 
		config.offset =  0
		#config.pattern = config.pattern[:-1]

	#drawText(10,10, config.messageString)
	

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

	config.render(config.image, 0, 0, config.screenWidth, config.screenHeight)

	if(config.done == True) :
		init()
		time.sleep(config.redrawSpeed)

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

	config.clr = colorutils.randomColor(1)
	config.fontSize = int(random.uniform(10,50))
	config.font = ImageFont.truetype(config.path  + '/assets/fonts/freefont/FreeSansBold.ttf', config.fontSize)

	config.alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
	config.word = "FEAR"
	colorutils.brightness =  1
	config.messageString = config.word
	config.xOffset = 15

	init()
	
	if(run) : runWork()
