#!/usr/bin/python
#import modules
from Tkinter import *
import PIL.Image
import PIL.ImageTk
from PIL import Image, ImageTk, ImageDraw, ImageFont
from subprocess import call

from configs import configuration
from configs import localconfig
#from cntrlscripts import off_signal

import os, sys, getopt, time, random, math, datetime, textwrap
import sys, getopt, os
import ConfigParser, io
import threading
import tkMessageBox
import importlib 
from Tkinter import *

global thrd, config
global imageTop,imageBottom,image,config,transWiring

## Create a blank dummy object container for now
#config = type('', (object,), {})()

###################################################
# -------   Reads configuration files and sets
# -------   defaults                             *#
###################################################
def configure() :
	#global group, groups, config
	#global action, scroll, machine, bluescreen, user, carouselSign, imgLoader, concentric, flash, blend, sqrs
	global config, path
	try: 
		baseconfig = localconfig
		path = baseconfig.path

		#baseconfig = ConfigParser.ConfigParser()
		#baseconfig.read('localconfig.cfg')
		config = configuration

		# Machine ID
		config.MID = baseconfig.MID
		# Default Work Instance ID
		config.WRKINID = baseconfig.WRKINID
		# Default Local Path
		config.path = baseconfig.path

		# Load the default work
		workconfig = ConfigParser.ConfigParser()
		workconfig.read(config.path  + '/configs/works/' + config.WRKINID + ".cfg")

		config.screenHeight = int(workconfig.get("displayconfig", 'screenHeight'))
		config.screenWidth =  int(workconfig.get("displayconfig", 'screenWidth'))
		config.tileSize = (int(workconfig.get("displayconfig", 'tileSizeHeight')),int(workconfig.get("displayconfig", 'tileSizeWidth')))
		config.rows = int(workconfig.get("displayconfig", 'rows'))
		config.cols = int(workconfig.get("displayconfig", 'cols'))
		config.actualScreenWidth  = int(workconfig.get("displayconfig", 'actualScreenWidth'))
		config.useMassager = bool(workconfig.getboolean("displayconfig", 'useMassager'))
		config.brightness =  float(workconfig.get("displayconfig", 'brightness'))
		config.transWiring = bool(workconfig.getboolean("displayconfig", 'transWiring'))
		config.work = workconfig.get("displayconfig", 'work')
		config.rendering = workconfig.get("displayconfig", 'rendering')

		config.renderImage = PIL.Image.new("RGBA", (config.actualScreenWidth, 32))
		config.renderImageFull = PIL.Image.new("RGBA", (config.screenWidth, config.screenHeight))
		config.image = PIL.Image.new("RGBA", (config.screenWidth, config.screenHeight))
		config.draw = ImageDraw.Draw(config.image)
		config.render = render


		if(config.rendering == "hub") :
			root = Tk()
			w = config.screenWidth + 8
			h = config.screenHeight  + 8
			x = 4
			y = 4
			root.overrideredirect(True)
			root.geometry('%dx%d+%d+%d' % (w, h, x, y))
			cnvs = Canvas(root, width=config.screenWidth + 4, height=config.screenHeight + 4)
			config.cnvs = cnvs
			config.cnvs.pack()
			config.cnvs.create_rectangle(0, 0, config.screenWidth + 8, config.screenHeight + 8, fill="black")
			config.cnvs.update()

		if(config.rendering == "hat") :
			#importlib.import_module('rgbmatrix.Adafruit_RGBmatrix')
			from rgbmatrix import Adafruit_RGBmatrix
			config.matrix = Adafruit_RGBmatrix(32, int(workconfig.get("displayconfig", 'matrixTiles')))

		# Load the work itself
		work = importlib.import_module('modules.'+str(config.work))
		work.config = config
		work.workConfig = workconfig
		work.main()
		return True


	except getopt.GetoptError as err:
		# print help information and exit:
		print ("Error:" + str(err))
		return False

def render(imageToRender,xOffset,yOffset,w=128,h=64,nocrop=False, overlayBottom=False) :
	global config
	if(config.rendering == "hub") :
		renderToHub( imageToRender,xOffset,yOffset,w,h,nocrop, overlayBottom)

	elif (config.rendering == "hat") :
		renderToHat( imageToRender,xOffset,yOffset,w,h,nocrop, overlayBottom)

def renderToHub( imageToRender,xOffset,yOffset,w=128,h=64,nocrop=False, overlayBottom=False) :
	# Render to canvas
	global config
	config.renderImageFull.paste(imageToRender, (xOffset, yOffset))
	temp = PIL.ImageTk.PhotoImage(config.renderImageFull)
	config.cnvs._image_id = config.cnvs.create_image(3, 3, image=temp, anchor='nw')
	config.cnvs.update()

def renderToHat(imageToRender,xOffset,yOffset,w=128,h=64,nocrop=False, overlayBottom=False):

	#global imageTop, imageBottom, screenHeight, screenWidth, panels, 
	#matrix, image, renderImage, tileSize, rows, cols, transWiring
	global config
	segmentImage = []

	# the rendered image is the screen size
	#renderImage = Image.new("RGBA", (screenWidth , 32))
	if(nocrop == True) :
		for n in range(0,rows) :
			segmentWidth = config.tileSize[1] * config.cols
			segmentHeight = 32
			xPos = n * segmentWidth - xOffset
			yPos = n * 32 #- yOffset
			segment =  imageToRender.crop((0, yPos, segmentWidth, segmentHeight + yPos))
			config.renderImage.paste(segment, (xPos,0,segmentWidth + xPos,segmentHeight))

	elif (nocrop == False) :
		segmentWidth = config.tileSize[1] * config.cols
		segmentHeight = 32

		#yOffset = 10
		#xOffset = 100
		# Must crop exactly the overlap and position of the to-be-rendered image with each segment
		#           ________________
		#           |               |
		#           |               |
		#           |    |||||||||  |
		#           -----|||||||||---
		#           |    |||||||||  |
		#           |    |||||||||  |

		
		cropP1 = [0,0]
		cropP2 = [0,0]

		for n in range(0,config.rows) :

			# Crop PLACEMENTS\
			a = max(0, xOffset) + segmentWidth * n
			b = max(0, yOffset - segmentHeight * n)
			c = min(segmentWidth, xOffset + w) + segmentWidth * n
			d = min(segmentHeight, yOffset + h - segmentHeight * n)

			# Cropping
			cropP2 = [  cropP1[0] + c - xOffset, 
						cropP1[1] + min(32, d - yOffset + n * segmentHeight)]

			cropP1 = [max(0 , 0 - xOffset),     max(0, n * segmentHeight - yOffset)]
			cropP2 = [min(w , segmentWidth - xOffset),   min(h, n * segmentHeight + 32 - yOffset)]

			pCrop  = cropP1 + cropP2

			if ((n==0 or n == 2 or n == 4) and (config.transWiring == False) ) : pCrop[1] = 0
			segmentImage.append(imageToRender.crop(pCrop))

			#print(a,b,c,d,cropP1,cropP2)


			# Depending on the cabling, either copy segment laterally - which I think
			# is faster, or transform the segment each time to flip and mirror because
			# the panels are upside down wrt the ones below them
			# Wiring from BACK  **** = ribbon jumper cables
			#           ________________
			#           |               |
			#           |        <--  * |
			#           |           | * |
			#           --------------*--
			#           |             * |
			#           |        ^    * |
			#           |        |-->   |
			#           ________________

			#           ________________
			#           |        ^      |
			#           | *      |-->   |
			#           |    *          |
			#           --------*--------
			#           |          *    |
			#           |        ^    * |
			#           |        |-->   |
			#           ________________


			# Only render if needs be
			if(pCrop[3] - pCrop[1] > 0 ) : 
				if ( pCrop[2] - pCrop[0] > 0) :
					segImg = segmentImage[n]
					if ((n==0 or n == 2 or n == 4) and (config.transWiring == False) ) : 
						# This flips, reveses and places the segment when the row is "upside down" wrt
						# the previous row of panels - this is when transWiring == False - i.e no long transverse cable
						segImg = ImageOps.flip(segImg)
						segImg = ImageOps.mirror(segImg)

						an = segmentWidth - xOffset - w
						if(an < 0) : an = 0

						bn = segmentHeight - yOffset - h
						if(bn < 0) : bn = 0

						config.renderImage.paste( segImg, (an, bn, an + pCrop[2] - pCrop[0], bn + pCrop[3] - pCrop[1]))
					else:
						config.renderImage.paste( segImg, (a, b, a + pCrop[2] - pCrop[0], b + pCrop[3] - pCrop[1]))

	 
			cropP1[1] = cropP2[1]


	if(overlayBottom) :
		config.renderImage = Image.new("RGBA", (w , h))
		config.renderImage.paste(imageToRender, (0,0))
		iid = config.renderImage.im.id
		idtemp = config.image.im.id
		config.matrix.SetImage(iid, xOffset + screenWidth, 0)
	else :
		iid = config.renderImage.im.id
		idtemp = config.image.im.id
		config.matrix.SetImage(iid, 0, 0)

def main():
	global config
	if(configure()) :
		try:
			args = sys.argv


		except getopt.GetoptError as err:
			# print help information and exit:
			print ("Error:" + str(err))

if __name__ == "__main__":
	main()
