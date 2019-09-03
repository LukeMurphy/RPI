import math
import random
import textwrap
import time

from modules import colorutils
from PIL import ImageFont

########################
# scroll speed and steps per cycle
scrollSpeed = 0.0006
stroopSpeed = 0.0001
steps = 2
stroopSteps = 2
stroopFontSize = 30

fontSize = 14
vOffset = -1
opticalOpposites = True
countLimit = 6
count = 0

# fcu present will start with the opposite
paintColor = "GREEN"

r = g = b = 0


def changeColor(rnd=False):
	global r, g, b, config
	if rnd == False:
		if r == int(255 * config.brightness):
			r = 0
			g = int(255 * config.brightness)
			b = 0
		else:
			g = 0
			r = int(255 * config.brightness)
			b = 0
	else:
		r = int(random.uniform(0, 255) * config.brightness)
		g = int(random.uniform(0, 255) * config.brightness)
		b = int(random.uniform(0, 255) * config.brightness)


def scrollMessage(arg, clrChange=False, adjustLenth=False, direction="Left"):
	global config, scrollSpeed, stroopSpeed, steps, fontSize, vOffset
	changeColor(clrChange)

	# draw the meassage to get its size
	font = config.ImageFont.truetype(
		config.path + "/fonts/freefont/FreeSerifBold.ttf", fontSize
	)
	tempImage = config.Image.new("RGBA", (1200, 196))
	draw = config.ImageDraw.Draw(tempImage)
	pixLen = draw.textsize(arg, font=font)
	# For some reason textsize is not getting full height !
	fontHeight = int(pixLen[1] * 1.3)

	# make a new image with the right size
	config.renderImage = config.Image.new(
		"RGBA", (config.actualScreenWidth, config.screenHeight)
	)
	scrollImage = config.Image.new("RGBA", pixLen)
	draw = config.ImageDraw.Draw(scrollImage)
	iid = scrollImage.im.id

	if direction == "Bottom":
		# The new image is going to be vertically stacked letters so will be
		# roughly as tall as it is long when written out horizontally
		# get average letter width

		letterHeight = pixLen[1] * 5 / 7
		imageHeight = len(arg) * letterHeight

		scrollImage = config.Image.new("RGBA", (pixLen[1], imageHeight))
		draw = config.ImageDraw.Draw(scrollImage)
		iid = scrollImage.im.id
		chars = list(arg)
		count = 0
		xOffset = -int(config.screenWidth / 2 * random.random()) + 10
		vOffset = -1

		for letter in chars:
			draw.text((2, count * letterHeight), letter, (r, g, b), font=font)
			count += 1

		end = scrollImage.size[1]
		start = -64

		for n in range(start, end):
			# fix  config.matrix.SetImage(config.id,xOffset,-n)
			config.render(scrollImage, xOffset, n, pixLen[0], fontHeight)
			time.sleep(scrollSpeed)

	elif direction == "Top":
		imageHeight = pixLen[0]

		print(pixLen, imageHeight, fontHeight)

		scrollImage = config.Image.new("RGBA", (imageHeight, imageHeight))
		draw = config.ImageDraw.Draw(scrollImage)
		draw.text((0, 0), arg, (r, g, b), font=font)
		# scrollImage = scrollImage.rotate(-90)
		# scrollImage.load()
		# print(scrollImage.size)

		xOffset = int(random.random() * (config.screenWidth - fontHeight))

		for n in range(0, pixLen[0] + config.screenHeight):
			config.render(scrollImage, xOffset, -n + pixLen[0], 0, 0)
			time.sleep(0.012)

	else:
		scrollImage = config.Image.new("RGBA", (pixLen[0], fontHeight))
		draw = config.ImageDraw.Draw(scrollImage)
		iid = scrollImage.im.id
		draw.text((0, 0), arg, (r, g, b), font=font)

		start = 0
		end = scrollImage.size[0]
		start = -config.screenWidth
		if direction == "Right":
			start = -end
			end = config.screenWidth

		for n in range(start, end, steps):
			if direction == "Left":
				config.render(scrollImage, -n, vOffset, pixLen[0], fontHeight, False)
				config.actions.drawBlanks()
			else:
				config.actions.drawBlanks()
				config.render(scrollImage, n, vOffset, pixLen[0], fontHeight, False)
				if random.random() > 0.9998:
					config.actions.glitch()
					break
			time.sleep(scrollSpeed)


def present(arg, clr=(250, 150, 150), duration=1, repeat=-1):
	global config, scrollSpeed, steps, fontSize, vOffset, countLimit, count
	global r, g, b, paintColor

	vFactor = 1.5

	try:
		# changeColor(False)
		if paintColor == "RED":
			paintColor = "GREEN"
		else:
			paintColor = "RED"
		# clr = tuple(int(a*config.brightness) for a in (clr))
		paintColorRGB = config.subtractiveColors(paintColor)

		fSize = int(config.screenHeight * vFactor)

		# draw the message to get its size - not very accurate for height tho...
		font = ImageFont.truetype(
			config.path + "/fonts/freefont/FreeSansBold.ttf", fSize
		)
		pixLen = config.draw.textsize(arg, font=font)

		# make a new image with the right size
		scrollImage = config.Image.new("RGBA", (pixLen[0], pixLen[1] + 20))
		draw = config.ImageDraw.Draw(scrollImage)
		xoffRange = 1
		yOffRange = 2

		# Draw the 'shadow' - either the 'optical ' RGB opposite or the RBY paint 'opposite/compliment'
		if random.random() > 0.5:
			draw.text(
				(-xoffRange, yOffRange),
				arg,
				config.colorCompliment(paintColorRGB),
				font=font,
			)
		else:
			draw.text(
				(-xoffRange, yOffRange),
				arg,
				config.colorComplimentRBY(paintColor),
				font=font,
			)

		# Draw the actual text
		draw.text((0, 0), arg, paintColorRGB, font=font)

		# Scale the image to fit the full set of panels (using a rough formula for font offset)
		scaledSize = (
			config.screenWidth,
			int(vFactor * float(config.screenHeight * pixLen[1]) / fSize) + 8,
		)
		# scaledSize = (config.screenWidth , config.screenHeight)
		scrollImage = scrollImage.resize(scaledSize)

		vOffset = -scaledSize[1] / 8
		config.render(
			scrollImage,
			0,
			vOffset + 4,
			config.screenWidth,
			config.screenHeight - vOffset,
		)
		config.actions.drawBlanks()

		time.sleep(duration)

		if count <= countLimit:
			count += 1
			# if countLimit = 0 then assume go on forever ...
			if countLimit == 0:
				count = 0

			if repeat == -1:
				present(arg, paintColorRGB, duration, repeat)
			if repeat > 0:
				present(arg, paintColorRGB, duration, repeat - 1)
			if repeat == 0:
				pass

		# else :
		# pass
		# exit()

	except KeyboardInterrupt:
		# print "Stopping"
		exit()
