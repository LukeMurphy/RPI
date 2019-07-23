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
	for i in range(0,16):
		for ii in range(0,6):
			height = round(random.uniform(6,96))
			width = 16
			xPos = round(random.uniform(0,config.canvasWidth - width))
			yPos = round(random.uniform(0,config.canvasWidth - 32))
			yPos = i * 16
			angle = random.uniform(0,360)
			angle = 270
			c1 = colorutils.randomColorAlpha(1,50,0)
			c2 = colorutils.randomColorAlpha(1,255,255)
			if random.random() < .1:
				c1 = (0,0,0,55)

			gradientImage = drawBar(width, height, c1,c2)
			gradientImage = gradientImage.rotate(angle, expand=1)
			config.image.paste(gradientImage, (xPos,yPos), gradientImage)


def drawBar(width = 32, height = 32, c1 = (0,0,0,0), c2 =(0,0,0,0)) :
	global config

	gradientImage = Image.new("RGBA", (width, height))
	gradientImageDraw  = ImageDraw.Draw(gradientImage)
	
	# draw box container
	gradientImageDraw.rectangle((0, 0, width, height), outline=None, fill=(config.holderColor) )

	# draw bar
	vLines = round((height)/config.steps) 
	arc = (math.pi) / vLines 
	dR = ((c2[0] - c1[0]))
	dG = ((c2[1] - c1[1]))
	dB = ((c2[2] - c1[2]))
	dA = ((c2[3] - c1[3]))

	for n in range (0, vLines) :
		yPos = n * config.steps
		yPos2 = (n + 1) * config.steps
		xPos = 0
		xPos2 = width
		b = math.sin(arc * n) 
		rVd = int(c1[0] + (b * dR) )
		gVd = int(c1[1] + (b * dG) )
		bVd = int(c1[2] + (b * dB) )
		bAd = int(c1[3] + (b * dA) )
		barColorDisplay = (rVd, gVd, bVd, bAd)
		gradientImageDraw.rectangle((xPos, yPos, xPos2, yPos2), fill=barColorDisplay, outline=None)

	return gradientImage



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
	config.barColorStart = (0,0,100,255)
	config.barColorEnd = (255,0,0,255)


	if(run) : runWork()









