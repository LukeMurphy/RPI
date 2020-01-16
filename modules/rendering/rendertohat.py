import PIL.Image
import sys, os, threading
from modules.filters import *
from PIL import Image, ImageDraw, ImageFont, ImageOps
#from rgbmatrix import Adafruit_RGBmatrix
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from rgbmatrix import graphics


def setUp():
	# importlib.import_module('rgbmatrix.Adafruit_RGBmatrix')
	#config.matrix = Adafruit_RGBmatrix(32, config.matrixTiles)
	#config.matrix = RGBmatrix(32, config.matrixTiles)

	options = RGBMatrixOptions()

	options.gpio_slowdown = 1
	options.chain_length = 4
	options.rows = 32
	options.cols = 64
	options.hardware_mapping = 'adafruit-hat'
	config.matrix = RGBMatrix(options = options)
	# print(config.renderImage)


def updateCanvas(*args):
	return True


def render(
	imageToRender,
	xOffset,
	yOffset,
	w=128,
	h=64,
	nocrop=False,
	overlayBottom=False,
	updateCanvasCall=True,
):
	# global imageTop, imageBottom, screenHeight, screenWidth, panels,
	# matrix, image, renderImage, tileSize, rows, cols, transWiring
	global config

	if config.useFilters:
		if random.random() < 0.2:
			imageToRender = ditherFilter(imageToRender, xOffset, yOffset, config)

	if config.usePixelSort:
		imageToRender = pixelSort(imageToRender, config)

	segmentImage = []

	# the rendered image is the screen size
	# renderImage = Image.new("RGBA", (screenWidth , 32))

	w=config.tileSize[0] * config.cols
	h=config.tileSize[1] * config.rows

	if nocrop == True:
		for n in range(0, rows):
			segmentWidth = config.tileSize[0] * config.cols
			segmentHeight = config.tileSize[1]
			xPos = n * segmentWidth - xOffset
			yPos = n * config.tileSize[1]  # - yOffset
			segment = imageToRender.crop((0, yPos, segmentWidth, segmentHeight + yPos))
			config.renderImage.paste(
				segment, (xPos, 0, segmentWidth + xPos, segmentHeight)
			)

	elif nocrop == False:
		segmentWidth = config.tileSize[0] * config.cols
		segmentHeight = config.tileSize[1]



		# yOffset = 10
		# xOffset = 100
		# Must crop exactly the overlap and position of the to-be-rendered image with each segment
		#           ________________
		#           |               |
		#           |               |
		#           |    |||||||||  |
		#           -----|||||||||---
		#           |    |||||||||  |
		#           |    |||||||||  |

		cropP1 = [0, 0]
		cropP2 = [0, 0]

		for n in range(0, config.rows):


			# Crop PLACEMENTS\
			a = max(0, xOffset) + segmentWidth * n
			b = max(0, yOffset - segmentHeight * n)
			c = min(segmentWidth, xOffset + w) + segmentWidth * n
			d = min(segmentHeight, yOffset + h - segmentHeight * n)


			# Cropping
			cropP2 = [
				cropP1[0] + c - xOffset,
				cropP1[1] + min(config.tileSize[1], d - yOffset + n * segmentHeight),
			]

			cropP1 = [max(0, 0 - xOffset), max(0, n * segmentHeight - yOffset)]
			cropP2 = [
				min(w, segmentWidth - xOffset),
				min(h, n * segmentHeight + config.tileSize[1] - yOffset),
			]

			pCrop = cropP1 + cropP2

			if (n == 0 or n == 2 or n == 4) and (config.transWiring == False):
				pCrop[1] = 0

			segmentImage.append(imageToRender.crop(pCrop))

			# print(a,b,c,d,cropP1,cropP2)

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
			if pCrop[3] - pCrop[1] > 0:
				if pCrop[2] - pCrop[0] > 0:
					segImg = segmentImage[n]
					if (n == 0 or n == 2 or n == 4) and (config.transWiring == False):
						# This flips, reveses and places the segment when the row is "upside down" wrt
						# the previous row of panels - this is when transWiring == False - i.e no long transverse cable
						segImg = ImageOps.flip(segImg)
						segImg = ImageOps.mirror(segImg)

						an = segmentWidth - xOffset - w
						if an < 0:
							an = 0

						bn = segmentHeight - yOffset - h
						if bn < 0:
							bn = 0

						config.renderImage.paste(
							segImg,
							(
								an,
								bn,
								an + pCrop[2] - pCrop[0],
								bn + pCrop[3] - pCrop[1],
							),
						)
					else:

						## Adding "n" -- because there starts to be a lag as scrolling happens where the top row
						## looks like it's off by one or more pixels, just adding it helps correct
						## only for transwired fast moving things though
						# overriding !!!!!
						n = 0
						config.renderImage.paste(
							segImg,
							(
								a + n,
								b,
								a + n + pCrop[2] - pCrop[0],
								b + pCrop[3] - pCrop[1],
							),
						)

			cropP1[1] = cropP2[1]

	if overlayBottom:
		config.renderImage = Image.new("RGBA", (w, h))
		config.renderImage.paste(imageToRender, (0, 0))
		iid = config.renderImage.im.id
		idtemp = config.image.im.id
		config.matrix.SetImage(iid, xOffset + screenWidth, 0)
	else:
		iid = config.renderImage
		idtemp = config.image.im.id
		#config.matrix.Clear()
		img  = iid.convert('RGB')
		config.matrix.SetImage(img, 0, 0)


#############
