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

# ################################################### #


matrix = Adafruit_RGBmatrix(32, 8)
imageTop = Image.new("RGBA", (256, 64))
imageBottom = Image.new("RGBA", (256, 64))

def render(imageTemp):
	global imageTop,imageBottom
	imageTop = imageTemp.crop((0,0,128,32))
	imageBottom = imageTemp.crop((0,32,128,64))
	imageTop.paste(imageBottom, (128,0))
	imageTop.load()

	id1 = imageTop.im.id
	id2 = imageBottom.im.id

	matrix.SetImage(id1, 0, 0)
	matrix.SetImage(id2, 128, 0)



xOffset = 0
yOffset = 0
width = 127
height = 50

imageTemp = Image.new("RGBA", (256, 64))
drawTemp  = ImageDraw.Draw(imageTemp)
drawTemp.rectangle((0,0,31,31), fill=(255,0,0), outline=(0,255,0))
drawTemp.rectangle((31,0,63,63), fill=(255,0,0), outline=(0,255,0))



render(imageTemp)


time.sleep(20)




