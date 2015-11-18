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


config = utils
config.matrix = Adafruit_RGBmatrix(32, 12)
config.image = Image.new("RGBA", (192, 64))
config.draw = ImageDraw.Draw(config.image)

config.Image = Image
config.ImageDraw = ImageDraw
config.ImageFont = ImageFont
iid = config.image.im.id
config.matrix.SetImage(iid, 0, 0)
config.tileSize = (32,64)
config.rows = 2
config.cols = 3
config.screenHeight =  64
config.screenWidth =  192
config.actualScreenWidth  = 192 * 2
config.useMassager = False
config.renderImage = Image.new("RGBA", (config.actualScreenWidth, 32))
config.brightness =  .25
config.path = "/home/pi/RPI1"


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
	global config
	# Get all files in the drawing folder
	path = config.path + "/imgs/drawings"
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


