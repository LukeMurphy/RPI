# ################################################### #
import time
import random
import math
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageEnhance
from modules import colorutils


def makeMarquee(p,w,h):
	perimeter = []
	for i in range (p[0], p[0] + w) : perimeter.append([i, p[1]])
	for i in range (p[1], p[1] + h) : perimeter.append([p[0] + w, i])
	for i in range (p[0] + w - 1, p[0], -1) : perimeter.append([i, p[1] + h])
	for i in range (p[1] + h - 1, p[1], -1) : perimeter.append([p[0], i])
	return (perimeter)



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
	config.draw.rectangle((0,0,config.screenWidth,config.screenHeight), fill=(0,0,0,255))


	config.marquees = []
	offset = 0
	marqueeWidth = 6
	w = config.screenWidth - marqueeWidth
	h = config.screenHeight - marqueeWidth

	pattern = [1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0]
	clrs = [(255,0,0),(0,255,0)]
	config.marquees.append([0, pattern, makeMarquee((0,0),w,h), marqueeWidth , clrs])
	pattern = [0,0,0,0,0,0,0,0,1,1,1,1,1,1]
	clrs = [(255,0,0),(0,255,0)]
	config.marquees.append([0, pattern, makeMarquee((marqueeWidth,marqueeWidth),w-marqueeWidth * 2,h-marqueeWidth * 2), marqueeWidth, clrs ])
	
	
	pattern = [1,1,1,0,0,0,0,0]
	clrs = [(0,0,255),(255,255,0)]
	config.marquees.append([0, pattern, makeMarquee((marqueeWidth * 2,marqueeWidth * 2),w-marqueeWidth * 4,h-marqueeWidth * 4), marqueeWidth, clrs ])
	pattern = [1,1,1,1,0,0,0]
	clrs = [(255,0,255),(0,255,0)]
	config.marquees.append([0, pattern, makeMarquee((marqueeWidth * 3,marqueeWidth * 3),w-marqueeWidth * 6,h-marqueeWidth * 6), marqueeWidth, clrs ])
	

	gap = 0

	for i in range(0, len(config.word)) :
		startX = config.textPosX + 10 * i
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
	global config
	drawText(10, 10, str(config.offset))
	pass

def drawElement() :
	global config
	return True

def redraw():
	global config
	config.draw.rectangle((0,0,config.screenWidth,config.screenHeight), fill=(0,0,0,255))

	for m in config.marquees :

		offset = m[0]
		pattern = m[1]
		perimeter = m[2]
		marqueeWidth = m[3]
		l = len(pattern)

		patternA = pattern[0 : (l - offset)]
		patternB = pattern[(l - offset): l ]
		pattern = patternB + patternA
		clrA = m[4][0]
		clrB = m[4][1]

		count = 0

		for p in reversed(perimeter):
			if(pattern[count] == 1) :
				config.draw.rectangle((p[0],p[1],p[0] + marqueeWidth, p[1] + marqueeWidth), fill=clrA)
			else:
				config.draw.rectangle((p[0],p[1],p[0] + marqueeWidth, p[1] + marqueeWidth), fill=clrB)
			count += 1
			if(count >= len(pattern)) :
				count = 0

		m[0] += 1
		if(m[0] >= len(pattern)) : m[0] =  0 


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
		time.sleep(.005)
		#time.sleep(random.random() * config.redrawSpeed)

def iterate() :
	global config
	redraw()

	config.render(config.image, 0, 0, config.screenWidth, config.screenHeight)

	if(config.done == True) :
		#init()
		#time.sleep(config.redrawSpeed)
		pass

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
	config.fontSize = 10
	config.font = ImageFont.truetype(config.path  + '/assets/fonts/freefont/FreeSansBold.ttf', config.fontSize)

	config.alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
	config.word = "FEAR"
	colorutils.brightness =  1
	config.messageString = config.word
	config.xOffset = 15

	config.marqueeWidth = 3

	init()
	
	if(run) : runWork()
