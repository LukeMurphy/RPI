import Image
import ImageDraw
import time
import random
from rgbmatrix import Adafruit_RGBmatrix
import datetime
import ImageFont
import textwrap
import math


class dM :
	screenWidth =  128
	screenHeight = 32
	#scroll speed and steps per cycle
	scrollSpeed = 0.01
	steps = 6
	vx = int(random.uniform(1,4))
	vy = int(random.uniform(1,4))
	vx = 1
	vy = 2
	x = y = 3
	speed = 1
	xMax = screenWidth -12
	yMax = 12
	buffer = 12
	matrix=draw=image=id= {}
	

	def __init__(self, arg):
		self.name = "Created: " + arg
		print(self.name)

	def test(self) :
		self.matrix.Fill(244,255,0)

	def change(self) :
		print("")                     

	def changeColor(self, rnd = False) :
			
			if (rnd == False) :
					if(r == 255) :
							r = 0
							g = 255
							b = 0
					else :
							g = 0
							r = 255
							b = 0
			else :
					r = int(random.uniform(0,255))
					g = int(random.uniform(0,255))
					b = int(random.uniform(0,255))



