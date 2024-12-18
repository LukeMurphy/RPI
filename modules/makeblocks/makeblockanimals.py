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


def makeCarcas():
	global config

	if random.random() < config.redrawProbablility:

		config.imageLayerDraw.rectangle(
			(0, 0, config.canvasWidth, config.canvasHeight),
			fill=(config.bgR, config.bgG, config.bgB, config.fade),
		)

		# config.fillColorA = tuple(int (a * config.brightness ) for a in config.colOverlayA.currentColor)
		# config.imageLayerDraw.rectangle((0,0,config.canvasWidth,config.canvasHeight), fill=config.fillColorA)
		# config.imageLayerDraw.rectangle((0,0,config.canvasWidth, config.canvasHeight), fill = (0,0,0,config.alpha))
		config.pixSortXOffset = config.pixSortXOffsetVal

		imgWidth = config.canvasWidth
		imgHeight = config.canvasHeight
		gray0 = 0
		gray1 = 30
		gray2 = 100
		fills = [(gray0, gray0, gray0, 255), (gray1, gray1, gray1, 255)]
		fills = [(gray0, gray0, gray0, 255), (gray2, gray0, gray0, 255)]

		quadBlocks = {
			"tail": {"order": 3, "proportions": [1, 1.5], "coords": []},
			"rl1": {"order": 1, "proportions": [1.8, 3.4], "coords": []},
			"rl2": {"order": 2, "proportions": [1.8, 4], "coords": []},
			"fl1": {"order": 1, "proportions": [2, 3.8], "coords": []},
			"fl2": {"order": 2, "proportions": [1.8, 3.5], "coords": []},
			"head": {"order": 6, "proportions": [3, 3.67], "coords": []},
			"body": {"order": 4, "proportions": [9, 14], "coords": []},
			"cavity": {"order": 5, "proportions": [6, 10], "coords": []},
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

		blockWidth = config.carcasBlockWidth
		wVariance = [imgWidth / 6, imgWidth / 3]
		hVariance = [imgHeight / 6, imgHeight / 2]
		wFactor = 1
		hFactor = 2
		l1Variance = config.l1Variance

		yStart = yPos = config.carcasYOffset
		xStart = xPos = imgWidth / 2 - config.carcasXOffset
		bodyEnd = 0
		bodyStart = 0
		tiedToBottom = 0 if random.random() < 0.5 else 2

		angleRotation = random.uniform(
			-config.angleRotationRange, config.angleRotationRange
		)

		bodyWidth = (
			quadBlocks["body"]["proportions"][0]
			* blockWidth
			* random.uniform(0.9, 1.25)
		)
		bodyLength = (
			quadBlocks["body"]["proportions"][1] * blockWidth * random.uniform(0.9, 1.2)
		)

		tailWidth = (
			quadBlocks["tail"]["proportions"][0] * blockWidth * random.uniform(0.9, 1.2)
		)
		tailLength = (
			quadBlocks["tail"]["proportions"][1] * blockWidth * random.uniform(0.9, 1.2)
		)

		headWidth = (
			quadBlocks["head"]["proportions"][0] * blockWidth * random.uniform(0.9, 1.2)
		)
		headLength = (
			quadBlocks["head"]["proportions"][1] * blockWidth * random.uniform(0.9, 1.2)
		)

		legWidth = (
			quadBlocks["rl1"]["proportions"][0] * blockWidth * random.uniform(0.9, 1.2)
		)
		legLength = (
			quadBlocks["rl1"]["proportions"][1] * blockWidth * random.uniform(0.9, 1.2)
		)

		frontLegWidth = (
			quadBlocks["fl1"]["proportions"][0] * blockWidth * random.uniform(0.9, 1.2)
		)
		frontLegLength = (
			quadBlocks["fl1"]["proportions"][1] * blockWidth * random.uniform(0.9, 1.2)
		)

		cavityLengthRatio = 0.9

		quad = "rl1"
		x1 = xStart * random.uniform(0.9, 1.2)
		y1 = yStart * random.uniform(0.9, 1.2)
		x2 = x1 + legWidth + l1Variance
		y2 = y1 + legLength
		quadBlocks[quad]["coords"] = [x1, y1, x2, y2]

		quad = "rl2"
		x1 = quadBlocks["rl1"]["coords"][0] - l1Variance + bodyWidth - legWidth
		y1 = yStart * random.uniform(0.9, 1.2)
		x2 = x1 + legWidth + l1Variance
		y2 = y1 + legLength
		quadBlocks[quad]["coords"] = [x1, y1, x2, y2]

		quad = "fl1"
		x1 = quadBlocks["rl1"]["coords"][0] - l1Variance
		y1 = (
			quadBlocks["rl1"]["coords"][3]
			+ bodyLength
			- l1Variance * random.uniform(0.9, 1.05)
		)
		x2 = x1 + frontLegWidth + l1Variance
		y2 = y1 + frontLegLength
		quadBlocks[quad]["coords"] = [x1, y1, x2, y2]

		quad = "fl2"
		x1 = quadBlocks["rl1"]["coords"][0] - l1Variance + bodyWidth - legWidth
		y1 = (
			quadBlocks["rl1"]["coords"][3]
			+ bodyLength * random.uniform(0.9, 1.05)
			- l1Variance
		)
		x2 = x1 + frontLegWidth + l1Variance
		y2 = y1 + frontLegLength
		quadBlocks[quad]["coords"] = [x1, y1, x2, y2]

		quad = "tail"
		x1 = quadBlocks["rl1"]["coords"][0] + bodyWidth / 2 - tailWidth / 2 - l1Variance
		y1 = quadBlocks["rl1"]["coords"][3] - tailLength / 4 * random.uniform(1.05, 1.3)
		x2 = x1 + tailWidth
		y2 = y1 + tailLength
		quadBlocks[quad]["coords"] = [x1, y1, x2, y2]

		quad = "body"
		x1 = quadBlocks["rl1"]["coords"][0] - l1Variance
		y1 = quadBlocks["rl1"]["coords"][3]
		x2 = x1 + bodyWidth
		y2 = y1 + bodyLength
		quadBlocks[quad]["coords"] = [x1, y1, x2, y2]

		quad = "cavity"
		x1 = quadBlocks["body"]["coords"][0] - l1Variance + bodyWidth / 4
		y1 = quadBlocks["body"]["coords"][1] + bodyLength * (1 - cavityLengthRatio)
		x2 = x1 + bodyWidth / 2
		y2 = y1 + cavityLengthRatio * bodyLength
		quadBlocks[quad]["coords"] = [x1, y1, x2, y2]

		quad = "head"
		x1 = quadBlocks["body"]["coords"][2] - headWidth / 2 - bodyWidth / 2
		y1 = quadBlocks["body"]["coords"][3] - tailLength / 2 * random.uniform(0.9, 1.2)
		x2 = x1 + headWidth
		y2 = y1 + headLength
		quadBlocks[quad]["coords"] = [x1, y1, x2, y2]

		xOffsetVal = (
			quadBlocks["cavity"]["coords"][0] + bodyWidth / 10
		) * random.uniform(0.9, 1.2)
		config.pixSortXOffset = xOffsetVal

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

			redShiftToUse = redShift
			# This is large red oblong
			if quad == "cavity":
				redShiftToUse = int(120 * (config.brightness))

			fills = [
				(gray0 + redShiftToUse, gray1, gray1, 255),
				(gray1 + redShiftToUse, gray1, gray1, 255),
				(gray2 + redShiftToUse, gray2, gray2, 255),
			]

			temp = Image.new("RGBA", (imgWidth, imgHeight))
			drawtemp = ImageDraw.Draw(temp)
			if n >= len(fills):
				n = 0  # n - len(fills)
			fillIndex = n

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


def makeAnimal():
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
			"tail": {"order": 3, "proportions": [1, 1.5], "coords": []},
			"l1": {"order": 1, "proportions": [3, 2], "coords": []},
			"l2": {"order": 2, "proportions": [3.2, 2], "coords": []},
			"head": {"order": 5, "proportions": [3, 3.67], "coords": []},
			"body": {"order": 4, "proportions": [5.5, 11], "coords": []},
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
		wVariance = [imgWidth / 6, imgWidth / 3]
		hVariance = [imgHeight / 6, imgHeight / 2]
		wFactor = 1
		hFactor = 2
		l1Variance = config.l1Variance

		yStart = yPos = config.yOffset
		xStart = xPos = imgWidth / 2 - config.xOffset
		bodyEnd = 0
		bodyStart = 0
		tiedToBottom = 0 if random.random() < 0.5 else 2

		angleRotation = random.uniform(
			-config.angleRotationRange, config.angleRotationRange
		)

		bodyWidth = (
			quadBlocks["body"]["proportions"][0]
			* blockWidth
			* random.uniform(0.9, 1.25)
		)
		bodyLength = (
			quadBlocks["body"]["proportions"][1] * blockWidth * random.uniform(0.9, 1.2)
		)

		tailWidth = (
			quadBlocks["tail"]["proportions"][0] * blockWidth * random.uniform(0.9, 1.2)
		)
		tailLength = (
			quadBlocks["tail"]["proportions"][1] * blockWidth * random.uniform(0.9, 1.2)
		)

		headWidth = (
			quadBlocks["head"]["proportions"][0] * blockWidth * random.uniform(0.9, 1.2)
		)
		headLength = (
			quadBlocks["head"]["proportions"][1] * blockWidth * random.uniform(0.9, 1.2)
		)

		legWidth = (
			quadBlocks["l1"]["proportions"][0] * blockWidth * random.uniform(0.9, 1.2)
		)
		legLength = (
			quadBlocks["l1"]["proportions"][1] * blockWidth * random.uniform(0.9, 1.2)
		)

		xOffsetVal = random.uniform(0.9, 1.2)

		quad = "l1"
		x1 = xStart * xOffsetVal
		y1 = yStart * random.uniform(0.9, 1.2)
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
