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


matrix = Adafruit_RGBmatrix(32, 12)


def render(imageToRender):
	global matrix

	tileSize = (32,64)
	rows = 3
	cols = 2
	imageRows = [] * rows
	
	segmentImage = Image.new("RGBA", (tileSize[1]*cols*rows, 32))
	print("Total segment", segmentImage)

	for n in range(0,rows) :
		segmentWidth = tileSize[1] * cols
		segmentHeight = 32
		xPos = n * segmentWidth
		yPos = n * 32
		segment =  imageToRender.crop((0, yPos, segmentWidth, segmentHeight + yPos))
		print(n, segment)
		segmentImage.paste(segment, (xPos,0,segmentWidth + xPos,segmentHeight))

	iid = segmentImage.im.id
	matrix.SetImage(iid, 0, 0)



# width , height
imageToRender = Image.new("RGBA", (128, 96))
draw  = ImageDraw.Draw(imageToRender)

rows = 3
cols = 4
n = 0
rSizeX = 31
tile =  32

for r in range(0, rows ) :
	for c in range(0, cols ) :	
		xPos  = c * tile
		yPos  = r * 32
		xPos2 = xPos + rSizeX
		yPos2 = 31 + yPos
		draw.rectangle((xPos,yPos,xPos2,yPos2), fill=(255,0,n * 15), outline=(0,255,0))
		n += 1
		print(n, xPos, yPos)


iid = imageToRender.im.id
matrix.SetImage(iid, 0, 0)
print("imageToRender", imageToRender)

#time.sleep(5)
#exit()


render(imageToRender)
time.sleep(5)




