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
import sys, getopt, os
import ConfigParser, io

# ################################################### #

baseconfig = ConfigParser.ConfigParser()
baseconfig.read('/home/pi/RPI/config.cfg')

config = utils
config.matrix = Adafruit_RGBmatrix(32, int(baseconfig.get("config", 'matrixTiles')))
config.screenHeight = int(baseconfig.get("config", 'screenHeight'))
config.screenWidth =  int(baseconfig.get("config", 'screenWidth'))
config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
config.draw = ImageDraw.Draw(config.image)

config.Image = Image
config.ImageDraw = ImageDraw
config.ImageFont = ImageFont
iid = config.image.im.id
config.matrix.SetImage(iid, 0, 0)
config.tileSize = (int(baseconfig.get("config", 'tileSizeHeight')),int(baseconfig.get("config", 'tileSizeWidth')))
config.rows = int(baseconfig.get("config", 'rows'))
config.cols = int(baseconfig.get("config", 'cols'))

config.actualScreenWidth  = int(baseconfig.get("config", 'actualScreenWidth'))
config.useMassager = bool(baseconfig.getboolean("config", 'useMassager'))
config.renderImage = Image.new("RGBA", (config.actualScreenWidth, 32))
config.brightness =  float(baseconfig.get("config", 'brightness'))
config.path = baseconfig.get("config", 'path')


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


