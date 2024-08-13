# dRAWING uSER Class
import math
import random
import time
from modules.configuration import bcolors
import PIL.Image
from PIL import Image, ImageDraw
from modules.holder_director import Holder 
from modules.holder_director import Director 

centerx = 0  # config.screenWidth/2
centery = 0  # 32

# x, y set just for video output - legacy stuff
x = offsety = 0
y = offsetx = 0

userCenterx = 0
userCentery = -0

scale = 1

fixed = True
numUsers = 2
userList = []

count = 0
steps = 1
start = 0
end = 5


def drawUser(n=0):

	global centery, centery, offsetx, offsety, userList, fixed
	global config, scale

	draw = ImageDraw.Draw(config.image)

	userCenterx = userList[n][0]
	userCentery = userList[n][1]

	hw = 18 * scale
	hh = 18 * scale
	mw = 6 * scale
	mh = 4 * scale
	bw = 32 * scale
	bh = 32 * scale

	hx1 = userCenterx + bw / 2 - hw / 2 + offsetx * scale
	hx2 = hx1 + hw
	hy1 = userCentery + offsety * scale
	hy2 = userCentery + hh + offsety * scale

	mx1 = userCenterx - mw / 2 + bw / 2 + offsetx * scale
	mx2 = mx1 + mw
	my1 = userCentery + hw * 2 / 3 + offsety * scale
	my2 = my1

	bx1 = userCenterx + offsetx * scale
	bx2 = bx1 + bw
	by1 = userCentery + hh - 3 + offsety * scale
	by2 = 3 + by1 + bh

	r = int(200 * config.brightness)
	g = int(124 * config.brightness)
	b = int(12 * config.brightness)
	a = 255

	onColor = (0, 0, 100, 255)
	oColor = (
		int(400 * config.brightness),
		int(random.uniform(50, 300) * config.brightness),
		int(0 * config.brightness),
		255,
	)

	# matrix = config.matrix
	# draw  = ImageDraw.Draw(config.image)

	#### BODY
	draw.ellipse((bx1, by1, bx2, by2), fill=(r, g, b, a), outline=1)
	## Cleanup / Outline
	draw.arc(
		(int(bx1 - 1), int(by1 - 1), int(bx2 + 1), int(by2 + 1)), 180, 360, fill=onColor
	)
	#### HEAD
	draw.ellipse((hx1, hy1, hx2, hy2), fill=(r, g, b, a), outline=1)
	## Cleanup / Outline
	draw.arc(
		(int(hx1 - 1), int(hy1 - 1), int(hx2 + 1), int(hy2 + 1)), 130, 420, fill=onColor
	)

	#### MOUTH
	if random.random() > 0.8:

		r = int(random.uniform(0, 255) * config.brightness)
		g = int(random.uniform(0, 255) * config.brightness)
		b = int(random.uniform(0, 255) * config.brightness)
		a = 255
		#### BODY
		draw.ellipse((bx1, by1, bx2, by2), fill=(r, g, b, a), outline=(1))
		## Cleanup / Outline
		draw.arc(
			(int(bx1 - 1), int(by1 - 1), int(bx2 + 1), int(by2 + 1)),
			180,
			360,
			fill=oColor,
		)
		#### HEAD
		draw.ellipse((hx1, hy1, hx2, hy2), fill=(r, g, b, a), outline=1)
		## Cleanup / Outline
		draw.arc(
			(int(hx1 - 1), int(hy1 - 1), int(hx2 + 1), int(hy2 + 1)),
			130,
			420,
			fill=oColor,
		)

		if n != 1 or fixed == True:
			draw.ellipse(
				(mx1, my1 - mh / 2, mx2, my2 + mh / 2),
				fill=(
					int(180 * config.brightness),
					int(80 * config.brightness),
					int(80 * config.brightness),
					a,
				),
				outline=1,
			)

	else:
		if n != 1 or fixed == True:
			draw.line((mx1, my1, mx1 + mw, my2), fill=1)


def userAnimator(*args):
	global config, userList, userCenterx, userCentery, scale, numUsers, fixed

	config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	# numUsers = int(random.uniform(1,3))
	numUsers = 2
	userList = [[0, 0]] * numUsers

	xPosInit = 0
	xMid = int(33 * scale)  # config.screenWidth/config.cols
	for n in range(0, numUsers):
		if fixed == False:
			xPos = int(
				random.uniform(xPosInit + 2, (config.screenWidth - xMid) * 2 / 3)
			)
		else:
			xPos = userCenterx + n * (xMid + userCenterx + 2)

		userList[n] = [xPos + xPosInit, userCentery]


def callBack():
	global config, fixed
	fixed = True if (random.random() > 0.5) else False
	userAnimator()


def runWork():
	# global redrawSpeed
	while True:
		iterate()
		t = random.uniform(0.01, 0.3)
		time.sleep(t)


def iterate(n=0):
	global config, userList, numUsers, userCenterx, userCentery
	global start, end, steps, count, boxWidth, boxHeight

	for n in range(0, numUsers):
		drawUser(n)

	config.render(config.image, 0, 1, 128, 128)

	count += steps
	if count > abs(end):
		count = 0
		callBack()
		# Done


def main(run=True):
	global config, workConfig, scale, userCenterx, userCentery
	scale = float(workConfig.get("user", "scale"))
	userCenterx = int(workConfig.get("user", "userCenterx"))
	userCentery = int(workConfig.get("user", "userCentery"))
	userAnimator()
	if run:
		runWork()
