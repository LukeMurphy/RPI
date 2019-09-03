#####
# import Image
# import ImageDraw
# from rgbmatrix import Adafruit_RGBmatrix
import math
import random
import time

blankPixels = []
counterPixels = []

cols = int(random.uniform(2, 20))
rows = int(random.uniform(2, 20))
drawBlanksFlag = True
drawCounterXOsFlag = False
counterXpos = 0
totalCounterWidth = 0


def explosion():
	global config

	if config.useMassager == True:
		messenger.soliloquy(True)

	# image = Image.new("RGBA", (32, 32))
	# draw  = ImageDraw.Draw(image)

	## Uses the same "global" image to draw to
	image = config.image
	# config.matrix.SetImage(image.im.id, 0,0)
	particles = []
	# Traces / no traces
	traces = False
	if random.random() > 0.98:
		traces = True
	# Number of sparks
	p = int(50 + (random.uniform(10, 90)))
	angle = 2 * math.pi / p

	# initial center position
	x = int(random.random() * config.screenWidth)
	y = int(random.random() * 16)

	brightness = config.brightness
	sparkleBrightness = config.brightness
	brightness = 0.9
	sparkleBrightness = 0.8

	for n in range(0, p):
		# variation in initial velocity
		f = random.random() * 4
		vx = math.cos(angle * n) * f
		vy = math.sin(angle * n) * f
		r = int(random.uniform(0, 255) * brightness)
		g = int(random.uniform(0, 255) * brightness)
		b = int(random.uniform(0, 255) * brightness)
		particles.append(
			{"id": n, "xpos": x, "ypos": y, "vx": vx, "vy": vy, "c": [r, g, b]}
		)

	for i in range(0, 50):
		if traces == False:
			config.matrix.Clear()
		# config.matrix.SetImage(config.image.im.id, 0,0)
		if random.random() > 0.98:
			traces = True
		decr = 20
		decr = int(random.uniform(1, 15))

		for q in range(0, p):
			ref = particles[q]
			ref["xpos"] = ref["vx"] + ref["xpos"]
			ref["ypos"] = ref["vy"] + ref["ypos"]

			# deacelleration
			ref["vy"] = ref["vy"] * 0.9
			ref["vx"] = ref["vx"] * 0.9

			# pseudo gravity
			ref["vy"] = ref["vy"] + 0.1

			particles[q]["c"][0] = particles[q]["c"][0] - decr
			particles[q]["c"][1] = particles[q]["c"][1] - decr
			particles[q]["c"][2] = particles[q]["c"][2] - decr

			if particles[q]["c"][0] <= 0:
				particles[q]["c"][0] = 0
			if particles[q]["c"][1] <= 0:
				particles[q]["c"][1] = 0
			if particles[q]["c"][2] <= 0:
				particles[q]["c"][2] = 0

			r = particles[q]["c"][0]
			g = particles[q]["c"][1]
			b = particles[q]["c"][2]

			# Sparkles!!
			if random.random() > 0.9:
				r = int(220 * sparkleBrightness)
				g = int(220 * sparkleBrightness)
				b = int(255 * sparkleBrightness)

			# if (q ==0) : print (particles[q]['c'][0])
			xDisplayPos = ref["xpos"]
			yDisplayPos = ref["ypos"]

			if xDisplayPos > config.screenWidth:
				xDisplayPos += config.screenWidth

			if yDisplayPos > 32 and yDisplayPos < 64:
				yDisplayPos -= 32
				xDisplayPos += config.screenWidth
			if yDisplayPos > 64:
				yDisplayPos -= 64
				xDisplayPos += config.screenWidth * 2

			config.matrix.SetPixel(int(xDisplayPos), int(yDisplayPos), r, g, b)

		time.sleep(0.015)
	if random.random() > 0.8:
		explosion()


def burst(a=10):
	global config
	config.matrix.Clear()
	count = 0
	stars = False
	p = 20
	actualScreenWidth = config.actualScreenWidth
	if random.random() > 0.5:
		stars = True
		p = 10
	while count < a:
		config.matrix.Clear
		for n in range(0, p):
			r = int(random.uniform(0, 255) * config.brightness)
			g = int(random.uniform(0, 255) * config.brightness)
			b = int(random.uniform(0, 255) * config.brightness)
			x = int(random.random() * actualScreenWidth)
			y = int(random.random() * 31)

			rn = random.random()
			v = int(200 * config.brightness)
			if rn > 0.3 and rn < 0.6:
				r = 0
				g = 0
				b = v  # int(200 * config.brightness)
			elif rn > 0.6 and rn < 0.9:
				r = v  # int(255 * config.brightness)
				g = 0
				b = 0
			else:
				True
				# r = g = b = 0

			config.matrix.SetPixel(x, y, r, g, b)
			if stars:
				(rx, gx, bx) = config.colorCompliment((r, g, b))
				if random.random() > 0.5:
					(rx, gx, bx) = (r, g, b)
				config.matrix.SetPixel(x + 1, y, rx, gx, bx)
				config.matrix.SetPixel(x - 1, y, rx, gx, bx)
				config.matrix.SetPixel(x, y + 1, rx, gx, bx)
				config.matrix.SetPixel(x, y - 1, rx, gx, bx)
		time.sleep(0.08)
		count += 1
	if random.random() > 0.5:
		burst()


def glitch(a=10):
	global config
	count = 0
	setBlanks()
	while count < a:
		yStart = int(random.uniform(0, 8))
		for n in range(0, 30):
			r = int(random.uniform(0, 255) * config.brightness)
			g = int(random.uniform(0, 255) * config.brightness)
			b = int(random.uniform(0, 255) * config.brightness)
			x = int(random.random() * config.screenWidth)

			yEnd = yStart + int(random.uniform(24, 42))
			y = int(random.uniform(yStart, yEnd))

			lineStart = int(random.uniform(0, 64))
			lineLength = int(random.random() * config.actualScreenWidth * 2 / 3)
			for xpos in range(0, lineLength):
				config.matrix.SetPixel(lineStart + xpos, y, r, g, b)
			for xpos in range(lineLength, config.screenWidth):
				config.matrix.SetPixel(xpos, y, 0, 0, 0)

		drawBlanks()
		time.sleep(0.01)
		count += 1
	time.sleep(int(random.uniform(0.1, 4)))
	# exit()


def setBlanks():
	# print("Setting Blanks")
	global config, blankPixels, cols, rows
	blankPixels = []
	count = 0
	# scatter horizontally
	for n in range(0, 10):
		x = int(random.random() * config.actualScreenWidth)
		y = int(random.random() * 32)
		blankPixels.append((x, y))
		if random.random() > 0.9:
			cols = int(random.uniform(2, 20))
			rows = int(random.uniform(2, 20))

			for ii in range(0, rows):
				blankPixels.append((x, y + ii))
				for i in range(0, cols):
					blankPixels.append((x + i, y + ii))


def drawBlanks():
	global config, blankPixels, rows, cols, drawBlanksFlag
	if len(blankPixels) == 0:
		setBlanks()
	count = 0
	blankNum = len(blankPixels)
	if drawBlanksFlag:
		for n in range(0, blankNum):
			config.matrix.SetPixel(blankPixels[n][0], blankPixels[n][1], 0, 0, 0)
	if drawBlanksFlag:
		drawCounterX0()


def transition():
	global config, blankPixels, rows, cols
	# TODO
	# Create diamond transisitons


# Creates primitive XOs to run counter to the LEFT direction of any scroll
def setCounterXO():
	global config, counterPixels, totalCounterWidth
	counterPixels = []
	count = 0
	# scatter horizontally
	rng = config.screenHeight
	radi = rng / 2.25
	theta = 2 * math.pi / rng
	lastx = 0
	numXOs = int(random.uniform(2, 5))

	for XOs in range(0, numXOs):
		if random.random() > 0.5:
			# Draw X
			for n in range(0, rng):
				x = n + lastx
				y = n
				counterPixels.append((x, y))
				counterPixels.append((x + 1, y))
				counterPixels.append((x, rng - y))
				counterPixels.append((x + 1, rng - y))
			lastx += rng + 1
		else:
			# Draw O
			for n in range(0, rng):
				x = int(math.cos(n * theta) * radi + radi) + lastx
				y = int(math.sin(n * theta) * radi) + config.screenHeight / 2
				counterPixels.append((x, y))
				counterPixels.append((x + 1, y))
				counterPixels.append((x - 1, y))
				counterPixels.append((x, y + 1))
				counterPixels.append((x, y - 1))
			lastx += rng + 1
	totalCounterWidth = lastx


def drawCounterX0():
	global config, counterPixels, counterXpos, totalCounterWidth
	if len(counterPixels) == 0:
		setCounterXO()
		counterXpos = 0
	count = 0
	blankNum = len(counterPixels)

	# counterXpos is the "starting" point for drawing the XOXO's
	# it's travelling from left to right so increments by +1 each cycle
	counterXpos += 1

	if drawCounterXOsFlag:
		for n in range(0, blankNum):
			xPos = counterPixels[n][0] + counterXpos
			yPos = counterPixels[n][1]
			lim = config.screenWidth + totalCounterWidth
			limb = config.screenWidth

			if yPos < 32 and xPos < limb:
				config.matrix.SetPixel(
					xPos, yPos, int(255 * (config.brightness + 0.25)), 0, 0
				)

			elif yPos < 32 and xPos > limb:
				xPos = xPos - config.screenWidth
				config.matrix.SetPixel(
					xPos, yPos, 0, 0, int(255 * (config.brightness + 0.25))
				)

			elif yPos > 32 and xPos < lim:
				xPos = xPos + config.screenWidth
				yPos = yPos - 32
				config.matrix.SetPixel(
					xPos, yPos, 0, int(255 * (config.brightness + 0.25)), 0
				)

			elif yPos > 32 and xPos > lim:
				xPos = xPos  # - config.screenWidth
				yPos = yPos - 32
				config.matrix.SetPixel(
					xPos, yPos, 0, int(255 * (config.brightness + 0.25)), 0
				)

			# For now, always pure RED
			# config.matrix.SetPixel(xPos, yPos, int(255 * (config.brightness + .25)),0,0)

	# Wrap the pixels around ...
	if counterXpos > config.screenWidth:
		counterXpos = -totalCounterWidth
		# counterXpos = 1

		# Create a new group of XO's
		if random.random() > 0.2:
			setCounterXO()
