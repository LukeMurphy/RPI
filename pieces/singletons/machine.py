# ################################################### #
import math
import random
import time
from modules.configuration import bcolors
from PIL import Image, ImageDraw

vx = 1
vy = 2
x = 0
y = 0
r = g = b = 125
redrawSpeed = 0.01
boxHeight = 30
boxWidth = 26
smile = -1
count = 0
steps = 0
end = 1


def drawMachine(mDisplacey=-1):
	global config
	global r, g, b
	global x, y
	global boxWidth, boxHeight
	# draw = config.draw
	# id = config.id

	screenWidth = config.screenWidth
	screenHeight = config.screenHeight

	# Used to draw directly onto a larger canvas, vs. sending
	# just the little square to be pasted into the canvas
	xD = x
	yD = y
	xD = yD = 0

	# x1, y1 are inital face points (left eye)
	x1 = 5 + xD
	y1 = 12 + yD
	# d is size of eye X
	d = 4
	# d2 is mouth / right eye
	d2 = 10
	# m1 is left point start, mw is mouth width
	m1 = 6 + xD
	mw = 12
	# Sets a frowm :[ upsidedown :]
	# mDisplacey = -1
	mDisplacex = 0

	# Fill colors
	rf = gf = bf = 0

	# line width
	w = 1

	# First state is  :[ second state is :]
	if r == 0:
		rf = int(255 * config.brightness)
		gf = 0
		r = 0
		g = int(255 * config.brightness)
		b = 0
	else:
		rf = 0
		gf = int(255 * config.brightness)
		r = int(255 * config.brightness)
		g = 0
		b = 0
		w = 2

	# outline
	config.draw.rectangle((xD, yD, boxWidth + xD, boxHeight + yD), fill=(0, 0, 0))
	config.draw.rectangle(
		(1 + xD, 1 + yD, 24 + xD, 28 + yD), fill=(rf, gf, bf), outline=(r, g, b)
	)

	# eyes
	config.draw.line((x1, y1, x1 + d, y1 + d), fill=(r, g, b), width=w)
	config.draw.line((x1, y1 + d, x1 + d, y1), fill=(r, g, b), width=w)

	x1 = x1 + d2

	config.draw.line((x1, y1, x1 + d, y1 + d), fill=(r, g, b), width=w)
	config.draw.line((x1, y1 + d, x1 + d, y1), fill=(r, g, b), width=w)

	# mouth
	x1 = x1 - d2
	y1 = y1 + -1

	# left corner
	# config.draw.line((x1+3,y1+d2,x1+2,y1+d2 +1), fill=(r,g,b), width = w)
	config.draw.line(
		(m1 - mDisplacex, y1 + d2 + mDisplacey, m1, y1 + d2), fill=(r, g, b), width=w
	)
	# center
	config.draw.line((m1, y1 + d2, m1 + mw, y1 + d2), fill=(r, g, b), width=w)
	# rigth corner
	# config.draw.line((x1+d2+1,y1+d2,x1+d2 +2,y1+d2+1), fill=(r,g,b), width = w)
	config.draw.line(
		(m1 + mw, y1 + d2, m1 + mw + mDisplacex, y1 + d2 + mDisplacey),
		fill=(r, g, b),
		width=w,
	)


def redraw():
	global config
	global x, y, vx, vy, boxWidth, boxHeight, smile
	speed = 1

	xMax = config.screenWidth - 12
	yMax = config.screenHeight - 12

	buffer = 12
	x = x + vx
	y = y + vy

	drawMachine(smile)

	# Render using main render function - manages the matrix tiling
	# config.render(config.image,x,y,boxWidth,boxHeight,False)
	# sendToRender(config.image, x,y,boxWidth,boxHeight,False)

	if x > xMax + buffer:
		vx = vx * -1
		changeColor()
		if random.random() > 0.5:
			vx = int(vx * 2 * random.random())
		x = xMax + buffer - 2
		changeSmile()
	if x < 0 - 26 + 1:
		vx = vx * -1
		changeColor()
		if random.random() > 0.5:
			vx = int(vx * 2 * random.random())
		x = -26 + 1
		changeSmile()
	if y > yMax + buffer:
		vy = vy * -1
		changeColor()
		if random.random() > 0.5:
			vx = int(vy * 2 * random.random())
		y = yMax + buffer - 2
		changeSmile()
	if y < 0 - boxHeight:
		vy = vy * -1
		changeColor()
		if random.random() > 0.5:
			vx = int(vy * 2 * random.random())
		y = 0 - boxHeight
		changeSmile()


def changeSmile():
	global smile
	frownProb = 0.85
	if random.random() > frownProb:
		smile = 1
	else:
		smile = -1


def changeColor(rnd=False):
	global r, g, b
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
		r = int(random.uniform(0, 255))
		g = int(random.uniform(0, 255))
		b = int(random.uniform(0, 255))


def callBack():
	global config
	pass



def runWork():
	global redrawSpeed
	global config
	print(bcolors.OKGREEN + "** " + bcolors.BOLD)
	print("RUNNING Machine")
	print(bcolors.ENDC)

	while config.isRunning == True:
		iterate()
		time.sleep(redrawSpeed)
		if config.standAlone == False :
			config.callBack()


def iterate(n=0):
	global config, x, y, wd, ht, dx, dx, start, end, steps, count, boxWidth, boxHeight
	config.render(config.image, x, y, boxWidth, boxHeight)
	redraw()

	count += steps

	if count > abs(end):
		callBack()
		count = 0
		# Done


def main(run=True):
	global config
	global redrawSpeed, x, y, vx, vy
	print("You Win!!! Loaded")

	config.renderImage = Image.new(
		"RGBA", (config.actualScreenWidth, config.screenHeight)
	)
	config.image = Image.new("RGBA", (26, 30))

	config.draw = ImageDraw.Draw(config.image)
	config.id = config.image.im.id

	x = int(random.random() * config.screenWidth)
	y = int(random.random() * config.screenHeight)

	if run:
		runWork()
