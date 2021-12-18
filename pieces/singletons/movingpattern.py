# ################################################### #
import argparse
import math
import random
import time
import types
import numpy as np
from modules.configuration import bcolors
from modules import badpixels, coloroverlay, colorutils
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps


lastRate = 0
colorutils.brightness = 1


# Really no need for a class here - it's always a singleton and besides
# with Python everthing is an object already .... some kind of OOP
# holdover anxiety I guess


def vary1(data, config):
	data = config.mult_a * (config.mult_b * np.sin(config.mult_c * config.data + 
			config.dpatColor/config.mult_d) * config.data + config.data * config.mult_e)
	return data


def vary2(data, config):
	data = config.mult_a * (config.mult_b * np.cos(config.mult_c * config.data + 
			config.dpatColor/config.mult_d) )
	return data


def redraw():
	global config


	if random.random() < .01 :
		config.step = round(random.uniform(5,16))	
	if random.random() < .01 :
		config.redrawSpeed = random.uniform(.01,.1)
	if random.random() < .01 :
		config.grout = round(random.uniform(0,4))
	if random.random() < .01 :
		xPos = round(random.uniform(0,config.screenWidth))
		yPos = round(random.uniform(0,config.screenHeight))
		config.remapImageBlockSection = (xPos,yPos,xPos + round(random.uniform(xPos,config.screenWidth)), yPos + round(random.uniform(yPos,config.screenHeight)))
		config.remapImageBlockDestination = (xPos,yPos)

	# Scroll the image
	if config.scrollDirection == 0 :
		crop1 = config.bufferImage.crop((0,0,config.colStop,config.scrollStep)).convert('RGBA')
		crop2 = config.bufferImage.crop((0,config.scrollStep, config.colStop, config.rowStop)).convert('RGBA')
		config.canvasImage.paste(crop2, (0,0), crop2)
		config.canvasImage.paste(crop1, (0,config.rowStop - config.scrollStep), crop1)
	else :
		crop1 = config.bufferImage.crop((0,0,config.scrollStep,config.rowStop)).convert('RGBA')
		crop2 = config.bufferImage.crop((config.scrollStep,0, config.colStop, config.rowStop)).convert('RGBA')
		config.canvasImage.paste(crop2, (0,0), crop2)
		config.canvasImage.paste(crop1, (config.colStop - config.scrollStep, 0), crop1)


	config.bufferImage = config.canvasImage


	for row in range(0,config.rowStop,config.step) :
		for col in range(0,config.colStop,config.step) :
			crop = config.canvasImage.crop((col,row,col+config.step,row+config.step)).convert('RGBA')
			x = math.floor(random.uniform(0,config.step))
			y = math.floor(random.uniform(0,config.step))
			pix = crop.getpixel((x,y))
			drawPix = (pix[0], pix[1], pix[2], round(random.uniform(10,config.mosaicAlpha)))

			config.draw.rectangle((col,row,col + config.step - config.grout,row + config.step - config.grout), fill = drawPix)






def redrawUsingArray():

	global config

	if random.random() < config.changeProb :
		config.datab = vary1(config.datab, config)
		config.dpatColor += config.deltapatColor
	
	config.datab = config.datab[:, :, [0, 1, 0]]
	datac = np.roll(config.datab, round(config.dpat), (0))
	datac = config.data

	config.image = Image.fromarray(datac.astype('uint8'))


	#print(math.floor(config.dpat))
	#print(len(config.datab[0][0]))



	config.dpat += config.deltapat


	if config.dpat >= len(config.datab[0]) :
		print(config.dpat)
		config.dpat = 2

	if config.dpat >= config.limUp or config.dpat <= config.limDown :
		config.deltapat *= -1



def runWork():
	global config
	print(bcolors.OKGREEN + "** " + bcolors.BOLD)
	print("Running movingpattern.py")
	print(bcolors.ENDC)
	while config.isRunning == True:
		iterate()
		time.sleep(config.redrawSpeed)
		if config.standAlone == False :
			config.callBack()


def rgbSep() :
	im = np.array(config.image)
	im_R = np.array(config.image)

	rads = math.pi / im.shape[0]

	startx = 50
	starty = 50
	width = 20
	height = 100
	for c in range(startx, width + startx - 3, 1):
		for r in range(starty, height + starty - 3, 3):
			rVal = round(abs(math.cos(c * rads * .5)) * r)
			cVal = round(abs(math.sin(r * rads * .75)) * c)
			#im_R[c,r] = im[cVal,rVal]

			rVal = im[c,r][0]
			gVal = im[c,r][1]
			bVal = im[c,r][2]

			im_R[c,r+0] = [rVal,0,0,255]
			im_R[c,r+1] = [0,gVal,0,255]
			im_R[c,r+2] = [0,0,bVal,255]

	config.finalImage = Image.fromarray(im_R)		

def iterate():
	global config
	redraw()
	rgbSep()
	config.render(config.finalImage, 0, 0, config.screenWidth, config.screenHeight)
	# Done


def main(run=True):
	global config
	
	config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.bufferImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.draw = ImageDraw.Draw(config.image)

	config.destinationImage = Image.new(
		"RGBA", (config.canvasWidth, config.canvasHeight)
	)

	config.redrawSpeed = float(workConfig.get("movingpattern", "redrawSpeed"))
	config.limUp = int(workConfig.get("movingpattern", "limUp"))
	config.limDown = int(workConfig.get("movingpattern", "limDown"))
	config.dpat = float(workConfig.get("movingpattern", "dpat"))
	config.dpatColor = float(workConfig.get("movingpattern", "dpatColor"))
	config.deltapat = float(workConfig.get("movingpattern", "deltapat"))
	config.deltapatColor = float(workConfig.get("movingpattern", "deltapatColor"))
	config.baseImage =(workConfig.get("movingpattern", "baseImage"))
	config.mult_a = float(workConfig.get("movingpattern", "mult_a"))
	config.mult_b = float(workConfig.get("movingpattern", "mult_b"))
	config.mult_c = float(workConfig.get("movingpattern", "mult_c"))
	config.mult_d = float(workConfig.get("movingpattern", "mult_d"))
	config.mult_e = float(workConfig.get("movingpattern", "mult_e"))
	config.changeProb = float(workConfig.get("movingpattern", "changeProb"))


	im = Image.open(config.baseImage)


	config.rowStop = im.height
	config.colStop = im.width
	config.scrollStep = int(workConfig.get("movingpattern", "scrollStep"))
	config.step =int(workConfig.get("movingpattern", "step"))
	config.grout = int(workConfig.get("movingpattern", "grout"))
	config.scrollDirection = int(workConfig.get("movingpattern", "scrollDirection"))
	config.mosaicAlpha = int(workConfig.get("movingpattern", "mosaicAlpha"))

	config.bufferImage =  im
	config.canvasImage =  im
	#config.image =  im

	im2arr = np.array(im) # im2arr.shape: height x width x channel
	arr2im = Image.fromarray(im2arr)
	#arr2im.show()

	im = np.array(Image.open(config.baseImage))
	config.data = im
	config.datab = config.data

	if run:
		runWork()
