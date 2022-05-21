#!/usr/bin/python
# import modules
import datetime
import gc
import getopt
import importlib
import io
import math
import os
import random
import sys
import textwrap
import time
from random import shuffle
from subprocess import call
from modules.configuration import bcolors
from modules.faderclass import FaderObj
from modules import badpixels, colorutils, configuration, panelDrawing
from modules.imagesprite import ImageSprite
from PIL import (
	Image,
	ImageChops,
	ImageFont,
	ImageDraw,
	ImageEnhance,
	ImageFilter,
	ImageMath,
	ImagePalette,
)
import numpy as np

xPos = 320
yPos = 0

bads = badpixels

class spriteAnimation() :

	frameWidth = 128
	frameHeight = 128
	totalFrames = 233
	frameCols = 16
	frameRows = 14
	sliceCol = 0
	sliceRow = 0

	sliceWidth = 128
	sliceHeight = 128

	sliceXOffset = 0
	sliceYOffset = 0

	frameCount = 0
	step = 1

	def __init__(self,config):
		self.config = config
		self.imageFrame = Image.new("RGBA", (self.frameWidth, self.frameHeight))


	def nextFrame(self):
		xPos = self.sliceCol * self.frameWidth + self.sliceXOffset
		yPos = self.sliceRow * self.frameWidth + self.sliceYOffset
		frameSlice = self.image.crop((xPos, yPos, xPos + self.sliceWidth, yPos + self.sliceHeight))

		self.sliceCol += self.step
		self.frameCount += self.step

		if self.sliceCol >= self.frameCols :
			self.sliceRow += 1
			self.sliceCol = 0

		if self.sliceRow >= self.frameRows or self.frameCount > self.totalFrames:
			self.sliceRow = 0
			self.sliceCol = 0
			self.frameCount = 0


		return frameSlice



def loadImage(spriteSheet):
	image = Image.open(spriteSheet, "r")
	image.load()
	imgHeight = image.getbbox()[3]
	return image

def main(run=True):
	global config, workConfig, blocks, simulBlocks, bads
	# gc.enable()

	print("SpriteSheet Player Piece Loaded")
	config.playSpeed = float(workConfig.get("images", "playSpeed"))
	config.imageToLoad = workConfig.get("images", "i1")

	config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
	config.canvasDraw = ImageDraw.Draw(config.canvasImage)


	config.animationArray = []
	config.spriteSheet1 = loadImage(config.imageToLoad)


	for i in range(0,1000) :
		anim = spriteAnimation(config)
		anim.image = config.spriteSheet1
		anim.xPos = round(random.random() * config.canvasWidth)
		anim.yPos = round(random.random() * config.canvasHeight)

		anim.step = round(random.uniform(1,2))

		anim.sliceCol = round(random.random() * anim.frameCols)
		anim.sliceRow = round(random.random() * anim.frameRows)
		anim.sliceXOffset = round(random.random() * anim.frameWidth)
		anim.sliceYOffset = round(random.random() * anim.frameHeight)

		anim.sliceWidth = round(random.random() * (anim.frameWidth - anim.sliceXOffset))
		anim.sliceHeight = round(random.random() * (anim.frameHeight - anim.sliceYOffset))

		config.animationArray.append(anim)

	
			
	try:
		config.filterRemapping = (workConfig.getboolean("images", "filterRemapping"))
		config.filterRemappingProb = float(workConfig.get("images", "filterRemappingProb"))
		config.filterRemapminHoriSize = int(workConfig.get("images", "filterRemapminHoriSize"))
		config.filterRemapminVertSize = int(workConfig.get("images", "filterRemapminVertSize"))
	except Exception as e:
		print(str(e))
		config.filterRemapping = False
		config.filterRemappingProb = 0.0
		config.filterRemapminHoriSize = 24
		config.filterRemapminVertSize = 24

	try:
		config.filterRemapRangeX = int(workConfig.get("images", "filterRemapRangeX"))
		config.filterRemapRangeY = int(workConfig.get("images", "filterRemapRangeY"))
	except Exception as e:
		print(str(e))
		config.filterRemapRangeX = config.canvasWidth
		config.filterRemapRangeY = config.canvasHeight

	try:
		if config.usePixelSort == True :
			config.pixelSortProbOn = float(workConfig.get("images", "pixelSortProbOn"))
			config.pixelSortProbOff = float(workConfig.get("images", "pixelSortProbOff"))
		else :
			config.pixelSortProbOn = 0
			config.pixelSortProbOff = 0

	except Exception as e:
		print(str(e))
		config.pixelSortProbOn = 0
		config.pixelSortProbOff = 0


		
	print(bcolors.OKBLUE + "** " + bcolors.BOLD)

	config.fontSize = 8
	config.font = ImageFont.truetype(config.path + "/assets/fonts/freefont/FreeSansBold.ttf", config.fontSize)

	config.imagePath = config.path + "/assets/imgs/"
	config.imageList = [config.imageToLoad]

	

	### THIS IS USED AS WAY TO MOCKUP A CONFIGURATION OF RECTANGULAR PANELS
	panelDrawing.mockupBlock(config, workConfig)
	#### Need to add something like this at final render call  as well
	''' 
		########### RENDERING AS A MOCKUP OR AS REAL ###########
		if config.useDrawingPoints == True :
			config.panelDrawing.canvasToUse = config.renderImageFull
			config.panelDrawing.render()
		else :
			#config.render(config.canvasImage, 0, 0, config.canvasWidth, config.canvasHeight)
			#config.render(config.image, 0, 0)
			config.render(config.renderImageFull, 0, 0)
	'''

	if run:
		runWork()


def runWork():
	print(bcolors.OKGREEN + "** " + bcolors.BOLD)
	print("Running image.py")
	print(bcolors.ENDC)
	# gc.enable()

	while config.isRunning == True:
		iterate()
		time.sleep(config.playSpeed)
		if config.standAlone == False:
			config.callBack()



def iterate(n=0):
	global config, blocks
	global xPos, yPos


	config.canvasDraw.rectangle((0,0,config.canvasWidth,config.canvasHeight), fill=(0,0,0,100))
	for anim in config.animationArray:
		config.canvasImage.paste(anim.nextFrame(), (anim.xPos, anim.yPos), anim.nextFrame())

	########### RENDERING AS A MOCKUP OR AS REAL ###########
	if config.useDrawingPoints == True :
		config.panelDrawing.canvasToUse = config.f.blendedImage
		config.panelDrawing.render()
	else :
		#config.render(config.image, 0, 0)
		config.render(config.canvasImage, 0, 0, config.canvasWidth, config.canvasHeight)



	if random.random() < config.filterRemappingProb:
		if random.random() <  .5 :
			config.filterRemapping == False
		else :
			config.filterRemapping == True


	if random.random() < config.filterRemappingProb:
		if config.useFilters == True and config.filterRemapping == True:
			config.filterRemap = True
			# new version  more control but may require previous pieces to be re-worked
			startX = round(random.uniform(0,config.filterRemapRangeX) )
			startY = round(random.uniform(0,config.filterRemapRangeY) )
			endX = round(random.uniform(8, config.filterRemapminHoriSize) )
			endY = round(random.uniform(8, config.filterRemapminVertSize) )
			config.remapImageBlockSection = [startX,startY,startX + endX, startY + endY]
			config.remapImageBlockDestination = [startX,startY]
			#print("swapping" + str(config.remapImageBlockSection))

	if random.random() < config.pixelSortProbOn :
		config.usePixelSort = True

	if random.random() < config.pixelSortProbOff :
		config.usePixelSort = False




def callBack():
	global config
	print("CALLBACK")
	return True


#####################
