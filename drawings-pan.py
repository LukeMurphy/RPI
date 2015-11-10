#!/usr/bin/python

#import modules

from modules import utils, loader
import Image
import ImageDraw
import time
import random
from rgbmatrix import Adafruit_RGBmatrix
import datetime
import ImageFont
import textwrap
import math

# ################################################### #

matrix = Adafruit_RGBmatrix(32, 4)
image = Image.new("RGBA", (128, 32))
draw  = ImageDraw.Draw(image)
id = image.im.id
matrix.SetImage(id, 0, 0)

config = utils
config.matrix = matrix
config.id = id
config.draw = draw
config.image = image
config.Image = Image
config.ImageDraw = ImageDraw
config.ImageFont = ImageFont
config.matrix.Clear()

imgLoader = loader
imgLoader.config = config

imgLoader.action = "pan"
imgLoader.countLimit = 1
imgLoader.setUpNew()

imgLoader.start("./imgs/Studio-ii_27.gif",0,-1)

imgLoader.start("./imgs/Studio-ii_28.gif",0,-1)

#imgLoader.start("./imgs/Studio-ii_2.gif",0,-1)

#imgLoader.start("./imgs/Studio-ii_3.gif",0,-1)

exit()

# 206_thumbnail25.jpg
'''
0004.gif
00united_states-onbla.gif
00united_states-onblu.gif
206_thumbnail25.gif
206_thumbnail25.jpg
415.gif
Studio-ii_2.gif
Studio-ii_27.gif
Studio-ii_28.gif
Studio-ii_3.gif
Untitled-1x-600.gif
anim.gif
candle.gif
chained-64x64.jpg
electrical.gif
flame-b.gif
flame-blu.gif
flame-blub.gif
flames-1b.gif
flames-1b2.gif
hub75.jpg
iu.gif
list.txt
monkey.gif
pixelpusher-vid.jpg
plugs.gif
rad.gif
running-vid.jpg
shane1.gif
shane2.gif
shane3.gif
shane3b.gif
skull.gif
skullb.gif
skullib.gif
time-display.jpg

'''
