# ################################################### #
import argparse
import math
import random
import time
import types

from modules import badpixels, coloroverlay, colorutils
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps

import numpy as np

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

	if random.random() < config.changeProb :
		config.datab = vary1(config.datab, config)
		config.dpatColor += config.deltapatColor
	
	#config.datab = config.datab[:, :, [0, 1, 0]]
	datac = np.roll(config.datab, round(config.dpat), (0))
	#datac = config.data

	config.image = Image.fromarray(datac.astype('uint8'))
	#a.renderImageFull.convert('RGBA')
	config.dpat += config.deltapat

	if config.dpat >= config.limUp or config.dpat <= config.limDown :
		config.deltapat *= -1



def runWork():
	global config
	while True:
		iterate()
		time.sleep(config.redrawSpeed)


def iterate():
	global config
	redraw()
	config.render(config.image, 0, 0, config.screenWidth, config.screenHeight)
	# Done


def main(run=True):
	global config
	
	config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
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

	im2arr = np.array(im) # im2arr.shape: height x width x channel
	arr2im = Image.fromarray(im2arr)
	#arr2im.show()

	im = np.array(Image.open(config.baseImage))
	config.data = im
	config.datab = config.data

	if run:
		runWork()
