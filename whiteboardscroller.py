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

matrix = Adafruit_RGBmatrix(32, 12)
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
config.renderImage = Image.new("RGBA", (32*4*3,32))
config.screenHeight = 96
config.screenWidth  = 128
config.actualScreenWidth = 32*4*3


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
		if os.path.isfile(os.path.join(path, f)) and not f.startswith("._") and not f.startswith(".") :
			imageList.append(f)

	print(imageList)
	while True:
		seq = int(random.uniform(0,30))

		#seq = 5
		#seq = 18
		seq = 16

		if (seq == 16) :
			imgLoader.action = "pan"
			imgLoader.countLimit = 1
			img = int(random.random() *  len(imageList))
			imgLoader.start(path + "/" + imageList[img], 0, -1)
		elif (seq == 17) :
			imgLoader.action = "play"
			imgLoader.countLimit = 100
			imgLoader.start()



#actions.explosion()
#stroop("M86 CROSSTOWN",(255,100,0, 100),"Left")
#exit()
seq()


