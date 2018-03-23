#!/usr/bin/python
#import modules
# ################################################### #
import os, sys, getopt, time, random, math, datetime, textwrap
#import ConfigParser, io
import importlib 
import numpy
import threading
import resource
from collections import OrderedDict
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageChops, ImageEnhance
from modules import colorutils, coloroverlay

global thrd, config

class ScrollObject :

	canvasWidth = 330
	canvasHeight = 64
	windowWidth = 320
	windowHeight = 224
	xPos = 0
	yPos = 0
	xSpeed = 2
	ySpeed = 0
	xOffset = 0
	yOffset = 0
	bgBackGroundColor = (200,0,0)
	callBack = None



	def __init__(self, direction="right-left") :
		print("Scroller Initiated")


	def setUp(self):
		self.canvas = Image.new("RGBA", (self.canvasWidth, self.canvasHeight))
		self.canvasDraw = ImageDraw.Draw(self.canvas)

		self.bg1 = Image.new("RGBA", (self.canvasWidth, self.canvasHeight))
		self.bg1Draw = ImageDraw.Draw(self.bg1)

		self.bg2 = Image.new("RGBA", (self.canvasWidth, self.canvasHeight))
		self.bg2Draw = ImageDraw.Draw(self.bg2)

		self.leadImage = self.bg1
		self.followImage = self.bg2

		#self.bg1Draw.rectangle((0,0,10,100), fill= (100,100,100))
		#self.bg2Draw.rectangle((0,0,10,100), fill= (100,0,255))

		'''
		#self.bg1Draw.rectangle((0,0,self.canvasWidth, self.canvasHeight), fill = self.bgBackGroundColor)
		self.bg1Draw.rectangle((0,0,100,50), fill=(0,200,0))
		self.bg1Draw.rectangle((self.canvasWidth - 20,0,self.canvasWidth,50), fill=(0,200,200))

		#self.bg2Draw.rectangle((0,0,self.canvasWidth, self.canvasHeight), fill = self.bgBackGroundColor)
		self.bg2Draw.rectangle((0,0,100,50), fill=(0,00,200))
		self.bg2Draw.rectangle((self.canvasWidth - 30,0,self.canvasWidth,50), fill=(200,20,200))
		'''

		self.canvas.paste(self.bg1)
		self.canvas.paste(self.bg2,(self.canvasWidth, 0))


	def scroll(self):

		self.xPos += self.xSpeed
		self.yPos += self.ySpeed
		leadImage = self.leadImage
		swap = False

		## Just right-left scrolling for now ...
		self.canvasDraw.rectangle((0,0,self.canvasWidth,self.canvasHeight), fill  = (0,0,0,10))
		self.canvas.paste(self.leadImage, (self.xPos ,self.yPos))
		if (self.xSpeed > 0) : 
			self.canvas.paste(self.followImage, (self.xPos - self.canvasWidth,self.yPos ))
		else :
			self.canvas.paste(self.followImage, (self.xPos + self.canvasWidth,self.yPos ))

		if (self.xPos > 1 * self.canvasWidth and self.xSpeed > 0) : 
			self.canvas.paste(self.leadImage, ( -1 * self.canvasWidth, self.yPos))
			#if self.callBack is not None : self.callBack["func"](imageRef = leadImage, direction = self.callBack["direction"])
			swap = True

		if (self.xPos < -1 * self.canvasWidth and self.xSpeed < 0) : 
			self.canvas.paste(self.leadImage, ( 1 * self.canvasWidth, self.yPos))
			swap = True

		if(swap == True):
			if self.callBack is not None : self.callBack["func"](imageRef = leadImage, direction = self.callBack["direction"])
			self.leadImage = self.followImage
			self.followImage = leadImage
			self.xPos = 0

		self.render()

	def render(self) :
		pass


