# ################################################### #
import argparse
import math
import random
import time
import types
import noise
from noise import *
from modules.configuration import bcolors
from modules import badpixels, coloroverlay, colorutils, panelDrawing
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps

import numpy as np

lastRate = 0
colorutils.brightness = 1


def reDraw():
	rings()

def rings():
	global config
	config.draw.rectangle((0,0,500,500), fill=(0,0,255,255))

	for row in range(0,config.numRings):
		points = config.pointsMin + row * config.pointsMin
		rads = 2 * math.pi / points
		ra = config.radiusMin * row + config.radiusMin
		for col in range(0,points):
			x = math.cos(col * rads) * ra + config.xOffset
			y = math.sin(col * rads) * ra + config.yOffset
			yChange = noise.pnoise2(x/config.rowFactor, (y+ config.scroll)/config.colFactor, 1) * config.amplitude + row

			r = 255
			g = round(math.sin((col/config.rowFactor)+.1) * 150)
			b = 50

			if config.markSize == 1 :
				config.draw.rectangle((x, y + yChange, x+0, y + yChange +0), fill=(r,g,b,255), outline=None)
			else:
				config.draw.ellipse((x, y + yChange, x+config.markSize, y + yChange +config.markSize), fill=(r,g,b,255), outline=None)
		#octv += 1
	config.scroll += 1

def waves():
	global config
	config.draw.rectangle((0,0,500,500), fill=(0,0,0,55))
	octv = 1
	for row in range(0,420,8):
		for col in range(0,500):
			x = col 
			y = noise.pnoise2(row/config.rowFactor + random.random()*.0, (col+ config.scroll)/config.colFactor + random.random()*.0, octv) * config.amplitude + row

			r = 255
			g = round(math.sin((col/config.rowFactor)+.1) * 200)
			b = 50
			config.draw.rectangle((x, y, x+1, y+1), fill=(r,g,b,150))
		#octv += 1
	config.scroll += 2




def runWork():
	global config
	print(bcolors.OKGREEN + "** " + bcolors.BOLD)
	print("Running woodyscroller.py")
	print(bcolors.ENDC)
	while config.isRunning == True:
		iterate()
		time.sleep(config.redrawSpeed)
		if config.standAlone == False :
			config.callBack()
			

def iterate():
	reDraw()

	########### RENDERING AS A MOCKUP OR AS REAL ###########
	if config.useDrawingPoints == True :
		config.panelDrawing.canvasToUse = config.image
		config.panelDrawing.render()
	else :
		config.render(config.image, 0, 0, config.screenWidth, config.screenHeight)
	# Done


def main(run=True):
	global config
	
	config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.draw = ImageDraw.Draw(config.image)


	config.redrawSpeed = float(workConfig.get("woodyscroller", "redrawSpeed"))
	config.amplitude = float(workConfig.get("woodyscroller", "amplitude"))
	config.rowFactor = float(workConfig.get("woodyscroller", "rowFactor"))
	config.colFactor = float(workConfig.get("woodyscroller", "colFactor"))

	config.numRings = int(workConfig.get("woodyscroller", "numRings"))
	config.pointsMin = int(workConfig.get("woodyscroller", "pointsMin"))
	config.xOffset = int(workConfig.get("woodyscroller", "xOffset"))
	config.yOffset = int(workConfig.get("woodyscroller", "yOffset"))
	config.radiusMin = int(workConfig.get("woodyscroller", "radiusMin"))
	config.markSize = int(workConfig.get("woodyscroller", "markSize"))
	config.scroll = 0

	### THIS IS USED AS WAY TO MOCKUP A CONFIGURATION OF RECTANGULAR PANELS
	panelDrawing.mockupBlock(config, workConfig)
	#### Need to add something like this at final render call  as well
	''' 
		########### RENDERING AS A MOCKUP OR AS REAL ###########
		if config.useDrawingPoints == True :
			config.panelDrawing.canvasToUse = config.renderImageFull
			config.panelDrawing.render()
		else :
			#config.render(config.canvasImage, 0, 0, config.canvasWidth, config.canvasHeight)
			#config.render(config.image, 0, 0)
			config.render(config.renderImageFull, 0, 0)
	'''

	if run:
		runWork()
