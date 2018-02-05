import os, sys, getopt, time, random, math, datetime, textwrap
import ConfigParser, io
import importlib 
import numpy
import threading
import resource
from collections import OrderedDict
from PIL import ImageFont, Image, ImageDraw, ImageOps, ImageChops, ImageEnhance
from modules import colorutils, coloroverlay
global config

def drawCarcas():
	global config

	gray0 = int(random.uniform(0,config.greyLevel) * config.brightness)
	gray1 = int(random.uniform(0,config.greyLevel) * config.brightness)
	gray2 = int(random.uniform(0,config.greyLevel) * config.brightness)
	redShift = config.redShift

	redShiftToUse = redShift

	## the drawing
	fills = [(gray0 + redShiftToUse,gray1,gray1,255),(gray1 + redShiftToUse,gray1,gray1,255),(gray2 + redShiftToUse,gray2,gray2,255)]
	poly = [403,262,317,251,291,183,277,132,254,69,250,37,246,53,226,33,230,65,241,88,257,162,259,231,258,232,234,300,215,350,219,417,258,484,260,616,283,766,306,908,335,995,336,1046,344,1027,343,1025,345,1015,349,1038,355,1013,356,994,355,990,340,904,346,857,345,898,336,949,364,916,368,985,385,1031,391,1059,414,1067,435,1062,449,1063,447,1028,459,968,454,907,476,918,455,886,435,866,441,859,500,939,518,999,522,1026,529,1014,530,1013,529,998,544,1018,535,993,534,989,529,930,510,875,512,833,506,784,516,753,504,688,500,619,486,523,505,405,473,280,475,279,466,199,475,133,475,130,486,71,496,48,494,19,484,41,471,12,467,48,460,88,446,134,426,197,419,216,402,258]
	
	## randomize the points
	if(random.random() < .01) :
		## Change the amount of random point displacement
		changePigglyWiggle()
		
	polyToUse = [n + random.uniform(-config.pigglyWiggleToUse,config.pigglyWiggleToUse) for n in poly]

	## Clear the drawing
	#config.imageLayerTemp = Image.new("RGBA", (config.canvasWidth * 3, int(config.canvasHeight * 3.4) ))
	config.imageLayerTemp = Image.new("RGBA", (1000, 1060 ))
	config.imageLayerTempDraw = ImageDraw.Draw(config.imageLayerTemp)

	## Draw the figure
	config.imageLayerTempDraw.polygon(polyToUse, fill = fills[0]) #outline = (15,15,15)

	## resize to fit
	config.imageLayerTemp = config.imageLayerTemp.resize((config.canvasWidth, config.canvasHeight))

	## paste to the image layer
	config.imageLayerDraw.rectangle((0,0,config.canvasWidth, config.canvasHeight), fill = (0,0,0,config.alpha))
	config.imageLayer.paste(config.imageLayerTemp, (config.xOffset,config.yOffset), config.imageLayerTemp)

def changePigglyWiggle():
	global config
	config.pigglyWiggleToUse = config.pigglyWiggle + int(random.uniform(0, config.pigglyWiggleVariance))
	pass