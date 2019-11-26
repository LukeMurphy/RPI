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

def redraw():
	global config

	datab = config.data
	datab = config.mult_a * np.tan(config.mult_b * np.sin(config.mult_c * config.data + config.dpat/config.mult_d) * config.data + config.data * config.mult_e)
	datab = np.roll(datab, round(config.dpat), (0))

	#datab = datab[:, :, [0, 2, 1]]
	config.image = Image.fromarray(datab.astype('uint8'))
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
	config.deltapat = float(workConfig.get("movingpattern", "deltapat"))
	config.baseImage =(workConfig.get("movingpattern", "baseImage"))
	config.mult_a = float(workConfig.get("movingpattern", "mult_a"))
	config.mult_b = float(workConfig.get("movingpattern", "mult_b"))
	config.mult_c = float(workConfig.get("movingpattern", "mult_c"))
	config.mult_d = float(workConfig.get("movingpattern", "mult_d"))
	config.mult_e = float(workConfig.get("movingpattern", "mult_e"))


	im = Image.open(config.baseImage)

	im2arr = np.array(im) # im2arr.shape: height x width x channel
	arr2im = Image.fromarray(im2arr)
	#arr2im.show()

	im = np.array(Image.open(config.baseImage))
	config.data = im

	if run:
		runWork()
