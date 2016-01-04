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

	
	segmentedImage = Image.new("RGBA", (tileSize[1]*cols, 32))
	print("Total segment", segmentedImage)

	for n in range(0,rows) :
		segmentWidth = tileSize[0] * cols
		segmentHeight = 32
		xPos = n * segmentWidth
		yPos = n * segmentHeight
		segment =  imageToRender.crop((0, yPos, segmentWidth, segmentHeight + yPos))
		#print(n, segment, xPos,yPos)
		#segmentedImage.paste(segment, (xPos,0))
		iid = segment.im.id
		matrix.SetImage(iid, xPos, 0)

	#iid = segmentedImage.im.id
	#matrix.SetImage(iid, 0, 0)

def renderManual(imageToRender):
	global matrix
	global rows, cols, tileSize

	pixLen = imageToRender.size

	print(pixLen)

# width , height

matrix = Adafruit_RGBmatrix(32, 12)
# cols, rows
tileSize = (32, 32)
rows = 3
cols = 4
n = clri = 0

# cols, rows
testGrid = (6, 3)
sizeX = int(cols * tileSize[0] / testGrid[0]) - 1
sizeY = int(rows * tileSize[1] / testGrid[1]) - 1

imageToRender = Image.new("RGBA", (tileSize[0]*cols, tileSize[1]*rows))
draw  = ImageDraw.Draw(imageToRender)
print("imageToRender", imageToRender)

 #(0,200,0)
wheel = [   (255,0,0),
            (255,126,0),
            (255,255,0),
            (0,255,0),
            (0,0,255),
            (126,0,255),]

cName1 = wheel[clri]
cName2 = (utils.colorCompliment(cName1))

t1 = time.clock()
t2 = time.clock()

# cols, rows
for r in range(0, testGrid[1] ) :	
	for c in range(0, testGrid[0] ) :
		xPos  = c * sizeX + c -0
		yPos  = r * sizeY + 0
		xPos2 = xPos + sizeX
		yPos2 = yPos + sizeY
		b =  n + 1
		b = 4
		# draw.rectangle((xPos,yPos,xPos2,yPos2), fill=(255,0,n * 15), outline=(0,255,0))
		draw.rectangle((xPos,yPos,xPos2,yPos2), 
			fill=(int(cName1[0]/b),int(cName1[1]/b),int(cName1[2]/b)), 
			outline=(int(cName2[0]/b),int(cName2[1]/b),int(cName2[2]/b)))
		n += 1
		print(n, xPos, yPos, xPos2, yPos2)
		currentName = cName1

		if (clri < len(wheel)-1) :
			clri += 1
		else :
			clri = 0 

		cName1 = wheel[clri]	
		cName2 = utils.closestRBYfromRGB(utils.colorCompliment(cName1))

t2 = time.clock()
print(t2 - t1)
#iid = imageToRender.im.id
#matrix.SetImage(iid, 0, 0)
#print("imageToRender", imageToRender)

#time.sleep(5)
#exit()

#renderManual(imageToRender)
render(imageToRender)

print(time.clock() - t2)
time.sleep(5)





