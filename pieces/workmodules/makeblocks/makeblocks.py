# import os, sys, getopt, time, random, math, datetime, textwrap
# import ConfigParser, io
# import importlib
# import numpy
# import threading
# import resource
import random
from collections import OrderedDict

from modules import coloroverlay, colorutils
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFont, ImageOps

global config


def makeComposition():
	global config

	if random.random() < config.redrawProbablility:
		# config.imageLayerDraw.rectangle((0,0,config.canvasWidth, config.canvasHeight), fill = (0,0,0,config.alpha))
		config.imageLayerDraw.rectangle(
			(0, 0, config.canvasWidth, config.canvasHeight),
			fill=(config.bgR, config.bgG, config.bgB, config.fade),
		)

		# config.fillColorA = tuple(int (a * config.brightness ) for a in config.colOverlayA.currentColor)
		# config.imageLayerDraw.rectangle((0,0,config.canvasWidth,config.canvasHeight), fill=config.fillColorA)

		config.pixSortXOffset = config.pixSortXOffsetVal

		imgWidth = config.canvasWidth
		imgHeight = config.canvasHeight
		gray0 = 0
		gray1 = 30
		gray2 = 100
		fills = [(gray0, gray0, gray0, 255), (gray1, gray1, gray1, 255)]
		fills = [(gray0, gray0, gray0, 255), (gray2, gray0, gray0, 255)]

		quadBlocks = {
			"tail": {"order": 3, "proportions": [7, 9], "coords": []},
			"l1": {"order": 1, "proportions": [7, 9], "coords": []},
			"l2": {"order": 2, "proportions": [7, 9], "coords": []},
			"head": {"order": 5, "proportions": [7, 9], "coords": []},
			"body": {"order": 4, "proportions": [7.5, 11], "coords": []},
		}
		quadBlocks = OrderedDict(
			sorted(quadBlocks.items(), key=lambda t: t[1]["order"])
		)

		numSquarePairs = len(quadBlocks)

		# renderImage = Image.new("RGBA", (imgWidth, imgHeight))

		# drawBackGround()

		# Choose seam x point  -- ideally about 1/3 from left
		xVariance = config.xVariance
		flip = config.flip

		blockWidth = config.blockWidth
		wVariance = [imgWidth / 2, imgWidth / 2]
		hVariance = [imgHeight / 2, imgHeight / 2]
		wFactor = 3
		hFactor = 4
		l1Variance = config.l1Variance

		yStart = yPos = config.yOffset
		xStart = xPos = imgWidth / 2 - config.xOffset
		bodyEnd = 0
		bodyStart = 0
		tiedToBottom = 0 if random.random() < 0.5 else 2

		sizeVarianceMin = 0.2
		sizeVarianceMax = 2

		angleRotation = random.uniform(
			-config.angleRotationRange, config.angleRotationRange
		)

		bodyWidth = (
			quadBlocks["body"]["proportions"][0]
			* blockWidth
			* random.uniform(sizeVarianceMin, sizeVarianceMax)
		)
		bodyLength = (
			quadBlocks["body"]["proportions"][1]
			* blockWidth
			* random.uniform(sizeVarianceMin, sizeVarianceMax)
		)

		tailWidth = (
			quadBlocks["tail"]["proportions"][0]
			* blockWidth
			* random.uniform(sizeVarianceMin, sizeVarianceMax)
		)
		tailLength = (
			quadBlocks["tail"]["proportions"][1]
			* blockWidth
			* random.uniform(sizeVarianceMin, sizeVarianceMax)
		)

		headWidth = (
			quadBlocks["head"]["proportions"][0]
			* blockWidth
			* random.uniform(sizeVarianceMin, sizeVarianceMax)
		)
		headLength = (
			quadBlocks["head"]["proportions"][1]
			* blockWidth
			* random.uniform(sizeVarianceMin, sizeVarianceMax)
		)

		legWidth = (
			quadBlocks["l1"]["proportions"][0]
			* blockWidth
			* random.uniform(sizeVarianceMin, sizeVarianceMax)
		)
		legLength = (
			quadBlocks["l1"]["proportions"][1]
			* blockWidth
			* random.uniform(sizeVarianceMin, sizeVarianceMax)
		)

		xOffsetVal = random.uniform(0.1, 2)

		quad = "l1"
		x1 = xStart * xOffsetVal
		y1 = yStart * random.uniform(0.9, 2.8)
		x2 = x1 + legWidth + l1Variance
		y2 = y1 + legLength
		quadBlocks[quad]["coords"] = [x1, y1, x2, y2]

		config.pixSortXOffset *= xOffsetVal

		quad = "l2"
		x1 = quadBlocks["l1"]["coords"][0] - l1Variance
		y1 = yStart + bodyLength - legLength * random.uniform(0.9, 1.2)
		x2 = x1 + legWidth + l1Variance
		y2 = y1 + legLength
		quadBlocks[quad]["coords"] = [x1, y1, x2, y2]

		quad = "tail"
		x1 = quadBlocks["l1"]["coords"][2] + bodyWidth - tailWidth - l1Variance
		y1 = yStart * random.uniform(0.9, 1.2) - tailLength / 4 * random.uniform(
			1.05, 1.3
		)
		x2 = x1 + tailWidth
		y2 = y1 + tailLength
		quadBlocks[quad]["coords"] = [x1, y1, x2, y2]

		quad = "body"
		x1 = quadBlocks["l1"]["coords"][2] - l1Variance
		y1 = quadBlocks["l1"]["coords"][1]
		x2 = x1 + bodyWidth
		y2 = y1 + bodyLength
		quadBlocks[quad]["coords"] = [x1, y1, x2, y2]

		quad = "head"
		x1 = quadBlocks["body"]["coords"][2] - headWidth
		y1 = quadBlocks["body"]["coords"][3] - tailLength / 2 * random.uniform(0.9, 1.2)
		x2 = x1 + headWidth
		y2 = y1 + headLength
		quadBlocks[quad]["coords"] = [x1, y1, x2, y2]

		n = 0
		for quad in quadBlocks:

			if random.random() < 0.5 and quad != "body":
				angleRotation = random.uniform(
					-config.angleRotationRange / 2, config.angleRotationRange / 2
				)

			gray0 = int(random.uniform(0, config.greyLevel) * config.brightness)
			gray1 = int(random.uniform(0, config.greyLevel) * config.brightness)
			gray2 = int(random.uniform(0, config.greyLevel) * config.brightness)
			redShift = config.redShift
			fills = [
				(gray0 + redShift, gray1, gray1, 255),
				(gray1 + redShift, gray1, gray1, 255),
				(gray2 + redShift, gray2, gray2, 255),
			]

			temp = Image.new("RGBA", (imgWidth, imgHeight))
			drawtemp = ImageDraw.Draw(temp)
			fillIndex = n
			if n >= len(fills):
				fillIndex = n - len(fills)

			x1 = quadBlocks[quad]["coords"][0]
			y1 = quadBlocks[quad]["coords"][1]
			x2 = quadBlocks[quad]["coords"][2]
			y2 = quadBlocks[quad]["coords"][3]

			drawtemp.rectangle((x1, y1, x2, y2), fill=fills[fillIndex])
			temp = ScaleRotateTranslate(temp, angleRotation, None, None, None, True)
			# config.workImage.paste(temp, temp)
			config.imageLayer.paste(temp, temp)
			n += 1

		# config.workImage.paste(temp, temp)

		if random.random() < 0:
			flip = True

		if flip == True:
			config.workImage = config.workImage.transpose(Image.FLIP_TOP_BOTTOM)
			config.workImage = config.workImage.transpose(Image.ROTATE_180)

		return True

	else:
		return False
