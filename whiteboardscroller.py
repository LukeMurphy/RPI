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

config.imageTop = Image.new("RGBA", (28, 30))
config.imageBottom = Image.new("RGBA", (28, 30))
config.renderImage = Image.new("RGBA", (config.screenWidth * config.panels , 32))

action = actions
action.config = config
scroll = scroll
scroll.config = config
machine = machine
machine.config = config
user = user
user.config = config
imgLoader = loader
imgLoader.config = config


# ################################################### #


def seq() :
	
	# Get all files in the drawing folder
	path = "./imgs/drawings"
	rawList = os.listdir(path)
	imageList = []

	for f in rawList :
		if os.path.isfile(os.path.join(path, f)) and not f.startswith("._") :
			imageList.append(f)


	while True:
		d = int(random.uniform(1,3))
		dir = "Left"
		if (d == 1) : dir = "Left"
		if (d == 2) : dir = "Right"
		if (d == 3) : dir = "Bottom"
		seq = int(random.uniform(0,30))

		#seq = 5
		#seq = 18
		seq = 16

		if (seq == 16) :
			imgLoader.action = "pan"
			imgLoader.countLimit = 1
			img = int(random.random() *  len(imageList))
			imgLoader.start(path + "/" + imageList[img])
		elif (seq == 17) :
			imgLoader.action = "play"
			imgLoader.countLimit = 100
			imgLoader.start()



#actions.explosion()
#stroop("M86 CROSSTOWN",(255,100,0, 100),"Left")
#exit()
seq()


