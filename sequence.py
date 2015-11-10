#!/usr/bin/python

#import modules

from modules import utils, actions,machine,scroll,user,bluescreen ,loader, squares
import Image
import ImageDraw
import time
import random
from rgbmatrix import Adafruit_RGBmatrix
import datetime
import ImageFont
import textwrap
import math

# ################################################### #

matrix = Adafruit_RGBmatrix(32, 8)
image = Image.new("RGBA", (128, 64))
draw  = ImageDraw.Draw(image)
iid = image.im.id
matrix.SetImage(iid, 0, 0)

config = utils
config.matrix = matrix
config.id = id
config.draw = draw
config.image = image
config.Image = Image
config.ImageDraw = ImageDraw
config.ImageFont = ImageFont
config.actions = actions

config.imageTop = Image.new("RGBA", (28, 30))
config.imageBottom = Image.new("RGBA", (28, 30))
config.renderImage = Image.new("RGBA", (config.screenWidth * config.panels , 32))

action = actions
action.config = config
scroll = scroll
scroll.config = config
machine = machine
machine.config = config
bluescreen = bluescreen
bluescreen.config = config
user = user
user.config = config
imgLoader = loader
imgLoader.config = config
concentric = squares
concentric.config = config

#machine.machineAnimator(300)
#exit()


# ################################################### #


def stroopSequence() :
	if(random.random() > .7) :scroll.stroop("YELLOW",(255,0,225),"Top")
	if(random.random() > .7) :scroll.stroop("VIOLET",(230,225,0),"Right")
	if(random.random() > .7) :scroll.stroop("RED",(0,255,0),"Left")
	if(random.random() > .7) :scroll.stroop("BLUE",(225,100,0),"Top")
	if(random.random() > .7) :scroll.stroop("GREEN",(255,0,0),"Left")
	if(random.random() > .7) :scroll.stroop("ORANGE",(0,0,200),"Right")


def seq2() :

	while True:
		d = int(random.uniform(1,3))
		dir = "Left"
		if (d == 1) : dir = "Left"
		if (d == 2) : dir = "Right"
		if (d == 3) : dir = "Bottom"
		seq = int(random.uniform(0,30))

		#seq = 5
		#seq = 18

		if(seq == 0) : actions.burst(40)
		elif(seq == 1) :
			if(random.random() > .8) : actions.burst(20)
			if(random.random() > .8) :scroll.scrollMessage("** PAINTINGS ** GIFS ** JPEGS ** AVIs ** MOVs ** CODE **", True, False, "Left")
		elif(seq == 2) :
			if(random.random() > .8) : actions.explosion()
			if(random.random() > .8) :scroll.scrollMessage("** FIGURATIVE ** ABSTRACT ** NO SOFTWARE **", True, False, "Left")
		elif(seq == 3) :
			if(random.random() > .8) : actions.explosion()
			if(random.random() > .8) :scroll.scrollMessage("** All USERS!! **", True, False, dir)
		elif(seq == 11) :
			if(random.random() > .8) : actions.burst(20)
			if(random.random() > .8) :scroll.scrollMessage("** ART ART ART **", True, False, dir)
		elif(seq == 12) :
			if(random.random() > .8) : actions.burst(20)
			if(random.random() > .9) :scroll.scrollMessage("** VAST POTENTIAL **", True, False, dir)
		elif(seq == 13) :
			if(random.random() > .8) : actions.explosion()
			if(random.random() > .8) :scroll.scrollMessage("% % % % % % % % HUGE PROBABILITIES % % % % % % % %", True, False, dir)
		elif (seq == 10) :
			if(random.random() > .8) : actions.burst(20)
			if(random.random() > .8) :scroll.scrollMessage("> THOUSANDS of COLORS <", True, True, dir)
		elif(seq == 4) :
			user.userAnimator(24)
		elif(seq == 5) :
			machine.machineAnimator(100)
		elif(seq == 6) :
			bluescreen.draw()
		elif(seq == 7) :
			actions.glitch()
		elif(seq == 8) :
			scroll.scrollMessage("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$", True, False, dir)
		elif (seq == 9) :
			stroopSequence()
		elif (seq == 14) :
			if(random.random() > .8) :scroll.scrollMessage(" :)     :)     :)     :)     :)     :)     :o ", True, True, "Top")
		elif (seq == 20) :
			user.userAnimator(12)
			machine.machineAnimator(30)
			user.userAnimator(1)
			machine.machineAnimator(30)
			actions.burst(20)
			actions.explosion()
		elif (seq == 16) :
			imgLoader.action = "pan"
			imgLoader.countLimit = 1
			imgLoader.start()
		elif (seq == 17) :
			imgLoader.action = "play"
			imgLoader.countLimit = 100
			imgLoader.start()
		elif (seq == 18) :
			concentric.colorSwitch = False
			concentric.animator(60)


#actions.explosion()
#stroop("M86 CROSSTOWN",(255,100,0, 100),"Left")
#exit()
seq2()


