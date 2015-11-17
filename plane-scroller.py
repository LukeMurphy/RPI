#!/usr/bin/python

#import modules

from modules import utils, actions,machine,scroll,user,bluescreen ,loader, squares
import Image
import ImageDraw
import time
import random
from rgbmatrix import Adafruit_RGBmatrix
import datetime
import ImageFont
import textwrap
import math
import os

# ################################################### #

matrix = Adafruit_RGBmatrix(32, 8)
image = Image.new("RGBA", (128, 64))
draw  = ImageDraw.Draw(image)
iid = image.im.id
matrix.SetImage(iid, 0, 0)

config = utils
config.matrix = matrix
config.id = id
config.draw = draw
config.image = image
config.Image = Image
config.ImageDraw = ImageDraw
config.ImageFont = ImageFont
config.actions = actions
config.screenWidth = 128
config.screenHeight = 64
config.actualScreenWidth = 256
config.renderImage = Image.new("RGBA", (config.actualScreenWidth, 32))

action = actions
action.config = config

imgLoader = loader
imgLoader.config = config


# ################################################### #


def seq() :
	
	# Get all files in the drawing folder
	path = "./imgs"
	rawList = os.listdir(path)
	imageList = []

	for f in rawList :
		if os.path.isfile(os.path.join(path, f)) and f.startswith("plane") :
			imageList.append(f)

	imageList = ['plane-2b.gif']

	while True:

		seq = int(random.uniform(0,30))

		#seq = 5
		#seq = 18
		seq = 16

		if (seq == 16) :
			imgLoader.debug = False
			imgLoader.action = "pan"
			imgLoader.countLimit = 1
			imgLoader.xOffset =  0
			imgLoader.yOffset = 0
			imgLoader.panRangeLimit = 0 + config.screenWidth
			imgLoader.scrollSpeed = .01
			imgLoader.useJitter =  True
			imgLoader.start(path + "/" + imageList[0], 1 , 0)

seq()


