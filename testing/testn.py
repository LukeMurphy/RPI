
import sys
#import pyglet
#from pyglet.gl import *
import noise
from noise import *

import PIL.Image
from PIL import Image, ImageDraw, ImageFont
from PIL import ImageChops

import numpy
import os, sys, getopt, time, random, math, datetime, textwrap


def imports():
	import types
	for name, val in globals().items():
		if isinstance(val, types.ModuleType):
			print(val.__name__)

#imports()

def drawTest() :

	points = 80
	span = random.uniform(5.0,15.0)
	span = 5.0
	speed = 1.0
	base = 5
	min = max = 0
	octaves = 1
	xMult = 150
	yMult = 200
	xOffset = 0
	yOffset = 200

	imgWidthFull = 1880
	imgHeightFull = 520


	renderImage = Image.new("RGB", (imgWidthFull, imgHeightFull))
	draw = ImageDraw.Draw(renderImage)
	draw.rectangle((0,0,imgWidthFull,imgHeightFull), fill=(220,220,220,255))
	#draw.rectangle((0,0,100,100), fill=(220,2,2))
	xMult = 5

	for n in range (0,4):

		r = range(points)
		print(xOffset)
		for i in range(0,points):
			x = float(i) * span / points - 0.5 * span
			y = noise.pnoise1(x + base, octaves)
			y2 = noise.pnoise2(x + base, octaves)
			#print(x * 2.0 / span, y, 0)

			xPos = xOffset + i * xMult #round(xOffset + x * xMult)
			yPos = round(yOffset + y * yMult)
			yPos2 = round(yOffset + y2 * yMult)

			draw.rectangle((xPos, yPos, 2 + xPos, 2 +  yPos), fill=(220,2,2))
			#draw.rectangle((xPos, yPos2, 2 + xPos, 2 +  yPos2), fill=(220,20,200))
		#draw.rectangle((xPos, 0, 1 + xPos, 200), fill=(0,2,200))
		xOffset += points * xMult
		base += points-1

	t = 1
	baseName = "./output/comp5_"
	fn = baseName+ str(t)+".jpg"
	renderImage.save(fn)


drawTest()


'''
window = pyglet.window.Window(visible=False, resizable=True)

def on_resize(width, height):
	"""Setup 3D viewport"""
	glViewport(0, 0, width, height)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(70, 1.0*width/height, 0.1, 1000.0)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
window.on_resize = on_resize
window.set_visible()

points = 256
span = 5.0
speed = 1.0

if len(sys.argv) > 1:
	octaves = int(sys.argv[1])
else:
	octaves = 1

base = 0
min = max = 0

@window.event
def on_draw():
	global min,max
	window.clear()
	glLoadIdentity()
	glTranslatef(0, 0, -1)
	r = range(256)
	glBegin(GL_LINE_STRIP)
	for i in r:
		x = float(i) * span / points - 0.5 * span
		y = noise.pnoise1(x + base, octaves)
		glVertex3f(x * 2.0 / span, y, 0)
	glEnd()

def update(dt):
	global base
	base += dt * speed
pyglet.clock.schedule_interval(update, 1.0/30.0)

pyglet.app.run()
'''
