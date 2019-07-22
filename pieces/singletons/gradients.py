import time
import random
import math
import threading
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageEnhance
from modules import colorutils

'''
config.percentage will be the global config variable for display of progress

'''
def reDraw() :
	drawBar()


def drawBar() :
	global config
	
	# draw box container
	config.draw.rectangle((config.xPos-1, config.yPos-1, config.boxMax+1, config.boxHeight+config.yPos+1), outline=None, fill=(config.holderColor) )
	# draw bar
	config.boxWidthDisplay = config.boxWidth

	config.xPos1 = config.xPos
	config.xPos2 = config.boxWidthDisplay+config.xPos
	config.yPos1 = config.yPos
	config.yPos2 = config.boxHeight+config.yPos
	

	vLines = round((config.canvasHeight)/config.steps)
	arc = math.pi  / vLines
	dR = ((config.barColorEnd[0] - config.barColorStart[0])/(vLines+1))
	dG = ((config.barColorEnd[1] - config.barColorStart[1])/(vLines+1))
	dB = ((config.barColorEnd[2] - config.barColorStart[2])/(vLines+1))

	for n in range (0, vLines) :
		yPos = config.yPos1 + (n * config.steps)
		yPos2 = yPos + ((n + 1) * config.steps)
		xPos = config.xPos1
		xPos2 = config.xPos2
		b = math.sin(arc * n) * n
		rVd = int(config.barColorStart[0] + (b * dR) )
		gVd = int(config.barColorStart[1] + (b * dG) )
		bVd = int(config.barColorStart[2] + (b * dB) )
		barColorDisplay = (rVd, gVd, bVd)

		if n < 100 :
			config.draw.rectangle((xPos, yPos, xPos2, yPos2), fill=barColorDisplay, outline=None)



def runWork():
	global config
	while True:
		iterate()
		time.sleep(config.redrawRate)

def iterate() :
	global config
	# Display bar, spinner, message or %
	reDraw()

	# Do the final rendering of the composited image
	config.render(config.image, 0, 0, config.screenWidth, config.screenHeight)



def main(run = True) :
	global config

	config.debug = (workConfig.getboolean("gradients", 'debug'))

	config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	config.draw  = ImageDraw.Draw(config.image)

	config.vOffset = int(workConfig.get("gradients", 'vOffset'))
	config.steps = int(workConfig.get("gradients", 'steps'))
	config.redrawRate = float(workConfig.get("gradients", 'redrawRate'))


	config.useVerticalColorGradient = (workConfig.getboolean("gradients", 'useVerticalColorGradient'))
	config.useHorizontalColorGradient = (workConfig.getboolean("gradients", 'useHorizontalColorGradient'))
	config.boxMax = config.screenWidth - 2
	config.boxMaxAlt = config.boxMax + int(random.uniform(10,30) * config.screenWidth)
	config.boxHeight = config.screenHeight - 3

	config.xPos = 0
	config.yPos = 0
	config.holderColor = (0,100,0,100)
	config.boxWidth = 200
	config.gradientLevel = 2
	config.barColorStart = (0,0,100,100)
	config.barColorEnd = (255,0,0,100)




	if(run) : runWork()









