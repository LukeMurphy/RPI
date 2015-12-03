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





def render(imageToRender):
	global matrix
	global rows, cols, tileSize

	
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
tileSize = (32,32)
matrix = Adafruit_RGBmatrix(32, 2)
imageToRender = Image.new("RGBA", (64, 32))
draw  = ImageDraw.Draw(imageToRender)

rows = 1
cols = 2
n = 0
sizeX = 31 
sizeY = 31

cName1 = (0,200,0)
cName2 = utils.opp(cName1) #(0,200,0)


imageRows = [] * rows

for r in range(0, rows ) :
	for c in range(0, cols ) :	
		xPos  = c * sizeX + c
		yPos  = r * sizeY
		xPos2 = xPos + sizeX
		yPos2 = yPos + sizeY
		b =  n + 1
		b = 1
		# draw.rectangle((xPos,yPos,xPos2,yPos2), fill=(255,0,n * 15), outline=(0,255,0))
		draw.rectangle((xPos,yPos,xPos2,yPos2), fill=(int(cName1[0]/b),int(cName1[1]/b),int(cName1[2]/b)), outline=cName1)
		n += 1
		print(n, xPos, yPos, xPos2, yPos2)
		currentName = cName1
		cName1 = cName2	
		cName2 = currentName
	currentName = cName1
	cName1 = cName2	
	cName2 = currentName

iid = imageToRender.im.id
#matrix.SetImage(iid, 0, 0)
print("imageToRender", imageToRender)

#time.sleep(5)
#exit()


render(imageToRender)
time.sleep(5)




