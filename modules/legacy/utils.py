import math
import random
import sys
import time

# import messenger
from PIL import ImageChops, ImageOps

screenWidth = 128
screenHeight = 64

tileSize = (32, 64)
rows = 2
cols = 1
imageRows = [] * rows
actualScreenWidth = tileSize[1] * cols * rows
path = "/home/pi/rpimain"
useMassager = False
brightness = 1


global imageTop, imageBottom, image, config, transWiring

transWiring = True


def soliloquy(override=False, arg=""):
	global useMassager
	if useMassager:
		messenger.soliloquy(override, arg)


def render(
	imageToRender, xOffset, yOffset, w=128, h=64, nocrop=False, overlayBottom=False
):

	global imageTop, imageBottom, screenHeight, screenWidth, panels, matrix, image, renderImage, tileSize, rows, cols, transWiring

	# w = screenWidth
	# h = screenHeight

	segmentImage = []

	# the rendered image is the screen size
	# renderImage = Image.new("RGBA", (screenWidth , 32))

	if nocrop == True:
		for n in range(0, rows):
			segmentWidth = tileSize[1] * cols
			segmentHeight = 32
			xPos = n * segmentWidth - xOffset
			yPos = n * 32  # - yOffset
			segment = imageToRender.crop((0, yPos, segmentWidth, segmentHeight + yPos))
			renderImage.paste(segment, (xPos, 0, segmentWidth + xPos, segmentHeight))

	elif nocrop == False:
		segmentWidth = tileSize[1] * cols
		segmentHeight = 32

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

		for n in range(0, rows):

			# Crop PLACEMENTS\
			a = max(0, xOffset) + segmentWidth * n
			b = max(0, yOffset - segmentHeight * n)
			c = min(segmentWidth, xOffset + w) + segmentWidth * n
			d = min(segmentHeight, yOffset + h - segmentHeight * n)

			# Cropping
			cropP2 = [
				cropP1[0] + c - xOffset,
				cropP1[1] + min(32, d - yOffset + n * segmentHeight),
			]

			cropP1 = [max(0, 0 - xOffset), max(0, n * segmentHeight - yOffset)]
			cropP2 = [
				min(w, segmentWidth - xOffset),
				min(h, n * segmentHeight + 32 - yOffset),
			]

			pCrop = cropP1 + cropP2

			if (n == 0 or n == 2 or n == 4) and (transWiring == False):
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
					if (n == 0 or n == 2 or n == 4) and (transWiring == False):
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

						renderImage.paste(
							segImg,
							(
								an,
								bn,
								an + pCrop[2] - pCrop[0],
								bn + pCrop[3] - pCrop[1],
							),
						)
					else:
						renderImage.paste(
							segImg,
							(a, b, a + pCrop[2] - pCrop[0], b + pCrop[3] - pCrop[1]),
						)

			cropP1[1] = cropP2[1]

	if overlayBottom:
		renderImage = Image.new("RGBA", (w, h))
		renderImage.paste(imageToRender, (0, 0))
		iid = renderImage.im.id
		idtemp = image.im.id
		matrix.SetImage(iid, xOffset + screenWidth, 0)
	else:
		iid = renderImage.im.id
		idtemp = image.im.id
		matrix.SetImage(iid, 0, 0)

	# DEBUG .....
	# time.sleep(10)
	# exit()
	# ************************************ #

	# print(">>")
	# if(random.random() > .95) : soliloquy()
