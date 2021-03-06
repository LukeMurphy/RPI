#!/usr/bin/python
# import modules
import ConfigParser
import datetime
import getopt
import io
import math
import os
import random
import sys
import textwrap
import time

import Image
import ImageDraw
import ImageFont
from modules import (
    actions,
    blender,
    bluescreen,
    carousel,
    flashing,
    loader,
    machine,
    scroll,
    squares,
    user,
    utils,
)
from rgbmatrix import Adafruit_RGBmatrix

# ################################################### #
global matrix
global rows, cols, tileSize
global r, g, b, boxHeight, boxWidth
global config


def drawMachine(mDisplacey=-1):
	global config
	global r, g, b, boxHeight, boxWidth
	matrix = config.matrix
	draw = config.draw

	screenWidth = config.screenWidth
	screenHeight = config.screenHeight

	# x1, y1 are inital face points (left eye)
	x1 = 5
	y1 = 12
	# d is size of eye X
	d = 4
	# d2 is mouth / right eye
	d2 = 10
	# m1 is left point start, mw is mouth width
	m1 = 6
	mw = 12
	# Sets a frowm :[ upsidedown :]
	# mDisplacey = -1
	mDisplacex = 0

	# Fill colors
	rf = gf = bf = 0

	# line width
	w = 1

	# First state is  :[ second state is :]
	if r == 0:
	    rf = int(255 * config.brightness)
	    gf = 0
	    r = 0
	    g = int(255 * config.brightness)
	    b = 0
	else:
	    rf = 0
	    gf = int(255 * config.brightness)
	    r = int(255 * config.brightness)
	    g = 0
	    b = 0
	    w = 2

	# outline
	config.draw.rectangle(
	    (0, 0, boxWidth - 1, boxHeight - 1), fill=(rf, gf, bf), outline=(r, g, b)
	)

	# eyes
	config.draw.line((x1, y1, x1 + d, y1 + d), fill=(r, g, b), width=w)
	config.draw.line((x1, y1 + d, x1 + d, y1), fill=(r, g, b), width=w)

	x1 = x1 + d2

	config.draw.line((x1, y1, x1 + d, y1 + d), fill=(r, g, b), width=w)
	config.draw.line((x1, y1 + d, x1 + d, y1), fill=(r, g, b), width=w)

	# mouth
	x1 = x1 - d2
	y1 = y1 + -1

	# left corner
	# config.draw.line((x1+3,y1+d2,x1+2,y1+d2 +1), fill=(r,g,b), width = w)
	config.draw.line(
	    (m1 - mDisplacex, y1 + d2 + mDisplacey, m1, y1 + d2), fill=(r, g, b), width=w
	)
	# center
	config.draw.line((m1, y1 + d2, m1 + mw, y1 + d2), fill=(r, g, b), width=w)
	# rigth corner
	# config.draw.line((x1+d2+1,y1+d2,x1+d2 +2,y1+d2+1), fill=(r,g,b), width = w)
	config.draw.line(
	    (m1 + mw, y1 + d2, m1 + mw + mDisplacex, y1 + d2 + mDisplacey),
	    fill=(r, g, b),
	    width=w,
	)


def render(imageToRender):
	global matrix
	global rows, cols, tileSize

	segmentedImage = Image.new("RGBA", (tileSize[1] * cols, 32))
	print("Total segment", segmentedImage)

	for n in range(0, rows):
	    segmentWidth = tileSize[0] * cols
	    segmentHeight = 32
	    xPos = n * segmentWidth
	    yPos = n * segmentHeight
	    segment = imageToRender.crop((0, yPos, segmentWidth, segmentHeight + yPos))
	    # print(n, segment, xPos,yPos)
	    # segmentedImage.paste(segment, (xPos,0))
	    iid = segment.im.id
	    matrix.SetImage(iid, xPos, 0)

	# iid = segmentedImage.im.id
	# matrix.SetImage(iid, 0, 0)


def renderManual(imageToRender):
	global matrix
	global rows, cols, tileSize
	pixLen = imageToRender.size
	print(pixLen)


def configure():
	global config
	baseconfig = ConfigParser.ConfigParser()
	baseconfig.read("/home/pi/RPI/config.cfg")

	config = utils
	config.matrix = Adafruit_RGBmatrix(32, int(baseconfig.get("config", "matrixTiles")))
	config.screenHeight = int(baseconfig.get("config", "screenHeight"))
	config.screenWidth = int(baseconfig.get("config", "screenWidth"))
	config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	config.draw = ImageDraw.Draw(config.image)

	config.Image = Image
	config.ImageDraw = ImageDraw
	config.ImageFont = ImageFont
	iid = config.image.im.id
	# config.matrix.SetImage(iid, 0, 0)

	config.tileSize = (
	    int(baseconfig.get("config", "tileSizeHeight")),
	    int(baseconfig.get("config", "tileSizeWidth")),
	)
	config.rows = int(baseconfig.get("config", "rows"))
	config.cols = int(baseconfig.get("config", "cols"))
	config.matrixTiles = int(baseconfig.get("config", "matrixTiles"))
	config.actualScreenWidth = int(baseconfig.get("config", "actualScreenWidth"))
	config.useMassager = bool(baseconfig.getboolean("config", "useMassager"))
	config.renderImage = Image.new("RGBA", (config.actualScreenWidth, 32))
	config.brightness = float(baseconfig.get("config", "brightness"))
	config.path = baseconfig.get("config", "path")

	config.transWiring = bool(baseconfig.getboolean("config", "transWiring"))


def testPatternBasic(tiles=8, cols=16):
	"""
	This is a raw test so there is only a single line of 32x32 blocks
	"""

	matrix = Adafruit_RGBmatrix(32, tiles)
	# cols, rows
	tileSize = (32, 32)
	sizeX = tileSize[0] * tiles / cols
	sizeY = 32

	# cols = int(tileSize[0] * tiles / sizeX)
	rows = 1

	imageToRender = Image.new("RGBA", (tileSize[0] * tiles, tileSize[1] * rows))
	draw = ImageDraw.Draw(imageToRender)
	print("imageToRender", imageToRender, sizeX)

	# Print tile numbers
	font = ImageFont.truetype("/home/pi/RPI/fonts/freefont/FreeSerifBold.ttf", 30)
	count = 0
	for n in range(0, tiles):
	    xPos = count * 32
	    yPos = -5
	    draw.text((xPos, yPos), str(count), (255, 0, 0), font=font)
	    count = count + 1
	iid = imageToRender.im.id
	matrix.SetImage(iid, 0, 0)
	time.sleep(4)

	# (0,200,0)
	wheel = [
	    (255, 0, 0),
	    (255, 125, 0),
	    (255, 255, 0),
	    (0, 255, 0),
	    (0, 255, 125),
	    (0, 0, 255),
	    (125, 0, 255),
	    (255, 0, 255),
	]

	n = clri = 0
	b = 1
	cName1 = wheel[clri]
	cName2 = (10, 10, 10)

	t1 = time.clock()
	t2 = time.clock()

	for c in range(0, cols):
	    xPos = c * sizeX + 0
	    yPos = 0
	    xPos2 = xPos + sizeX
	    yPos2 = yPos + sizeY
	    b = 1

	    draw.rectangle(
	        (xPos, yPos, xPos2, yPos2),
	        fill=(int(cName1[0] * b), int(cName1[1] * b), int(cName1[2] * b)),
	    )
	    n += 1
	    if n > len(wheel):
	        b *= 0.8
	    # print(n, clri, xPos, yPos, xPos2, yPos2)

	    if clri < len(wheel) - 1:
	        clri += 1
	    else:
	        clri = 0

	    cName1 = wheel[clri]
	    cName2 = (10, 10, 10)

	t2 = time.clock()
	print(t2 - t1)

	iid = imageToRender.im.id
	matrix.SetImage(iid, 0, 0)

	print(time.clock() - t2)
	time.sleep(10)
	draw.rectangle((0, 0, tileSize[0] * cols, tileSize[1] * rows), fill=0, outline=1)
	matrix.SetImage(iid, 0, 0)
	time.sleep(0.1)


def testPatternUsingConfig(t=1):
	global config
	r = g = b = 0
	clr = [
	    (100, 0, 0),
	    (0, 100, 0),
	    (0, 0, 100),
	    (100, 100, 0),
	    (100, 0, 100),
	    (0, 100, 100),
	]
	tmpImage = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	tmpDraw = ImageDraw.Draw(tmpImage)
	for n in range(0, 6):
	    x = 0
	    y = 0
	    boxHeight = config.screenHeight
	    boxWidth = config.screenWidth
	    print(boxHeight, boxWidth)
	    tmpDraw.rectangle((x, y, x + boxWidth, y + boxHeight), fill=clr[n])
	    config.render(tmpImage, x, y, boxWidth, boxHeight, False)
	    time.sleep(t)


def testMachine():
	global r, g, b, boxHeight, boxWidth
	r = g = b = 125
	boxHeight = 24
	boxWidth = 28

	drawMachine()
	x = 0
	y = 0
	count = 160
	while count > 0:
	    config.render(config.image, x, y, boxWidth, boxHeight, False)
	    time.sleep(0.05)
	    y += 2
	    x += 0
	    count -= 1
	    pass


def drawPanelNumbers():
	global config, r, g, b
	r = 100
	g = 0
	b = 0
	font = config.ImageFont.truetype(
	    config.path + "/fonts/freefont/FreeSerifBold.ttf", 30
	)
	totalTiles = config.matrixTiles

	config.image = Image.new("RGBA", (config.actualScreenWidth, 32))
	config.draw = ImageDraw.Draw(config.image)
	iid = config.image.im.id
	config.matrix.SetImage(iid, 0, 0)

	count = 0
	for n in range(0, totalTiles):

	    xPos = count * 32
	    yPos = -5
	    tmpImage = Image.new("RGBA", (32, 32))
	    tmpDraw = ImageDraw.Draw(tmpImage)
	    tmpDraw.text((0, 0), str(count), (r, g, b), font=font)
	    iid = tmpImage.im.id
	    print(count, xPos)
	    config.matrix.SetImage(iid, xPos, yPos)
	    count = count + 1

	time.sleep(1)


def drawPanelNumbersConfig():
	global config, r, g, b
	r = 100
	g = 100
	b = 0
	font = config.ImageFont.truetype(
	    config.path + "/fonts/freefont/FreeSerifBold.ttf", 30
	)
	totalTiles = config.rows * config.cols

	print("total Tiles: " + str(totalTiles))

	config.image = Image.new("RGBA", (config.actualScreenWidth, 32))
	config.draw = ImageDraw.Draw(config.image)
	iid = config.image.im.id
	config.matrix.SetImage(iid, 0, 0)

	tmpImage = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	tmpDraw = ImageDraw.Draw(tmpImage)

	count = 0
	for n in range(0, config.rows):
	    for nn in range(0, config.cols):
	        xPos = nn * 32
	        yPos = -5 + 32 * n
	        tmpDraw.text((xPos, yPos), str(count), (r, g, b), font=font)
	        print(count, xPos, yPos)
	        count = count + 1

	config.render(tmpImage, 0, 0, 128, 160)
	time.sleep(1)


def testConfiged():
	configure()
	drawPanelNumbers()
	drawPanelNumbersConfig()
	testPatternUsingConfig(3)


def testRaw():
	testPatternBasic(8)


def main():
	try:
	    args = sys.argv
	    print(args)
	    if len(args) > 1:
	        argument = args[1]
	        if argument == "raw":
	            testRaw()
	    else:
	        testConfiged()
	except getopt.GetoptError as err:
	    # print help information and exit:
	    print("Error:" + str(err))


if __name__ == "__main__":
	main()
