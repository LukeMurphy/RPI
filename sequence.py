#!/usr/bin/python
#import modules
from modules import utils, actions, machine, scroll, user, bluescreen ,loader, squares
import Image
import ImageDraw
import time
import random
from rgbmatrix import Adafruit_RGBmatrix
import datetime
import ImageFont
import textwrap
import math
import sys, getopt
import ConfigParser, io

def stroopSequence() :
	global group, groups
	global action, scroll, machine, bluescreen, user, imgLoader, concentric, signage
	if(random.random() > .7) :scroll.stroop("YELLOW",(255,0,225),"Top")
	if(random.random() > .7) :scroll.stroop("VIOLET",(230,225,0),"Right")
	if(random.random() > .7) :scroll.stroop("RED",(0,255,0),"Left")
	if(random.random() > .7) :scroll.stroop("BLUE",(225,100,0),"Top")
	if(random.random() > .7) :scroll.stroop("GREEN",(255,0,0),"Left")
	if(random.random() > .7) :scroll.stroop("ORANGE",(0,0,200),"Right")


def seq2() :
	global group, groups
	global action, scroll, machine, bluescreen, user, imgLoader, concentric, signage
	#machine.machineAnimator(130)
	lastAction  = 0

	while True:
		d = int(random.uniform(1,3))
		dir = "Left"
		if (d == 1) : dir = "Left"
		if (d == 2) : dir = "Right"
		if (d == 3) : dir = "Bottom"

		seq = int(random.uniform(0,30))
		while (seq not in group and seq != lastAction) : 
			seq = int(random.uniform(0,30))

		#print (lastAction, seq)
		lastAction = seq
		#seq =4
		#seq = 5
		#concentric
		#seq = 14

		if(seq == 0) : actions.burst(40)
		elif(seq == 1) :
			if(random.random() > .8) :actions.burst(10)
			if(random.random() > .8) :scroll.scrollMessage("** PTGS * GIFS * JPEGS * PTGS * PTGS * CODE **", True, False, "Left")
		elif(seq == 2) :
			if(random.random() > .8) : actions.explosion()
			if(random.random() > .8) : scroll.scrollMessage("** FIGURATIVE ** ABSTRACT ** NO SOFTWARE **", True, False, "Left")
		elif(seq == 3) :
			if(random.random() > .8) : actions.explosion()
			if(random.random() > .8) : scroll.scrollMessage("** All USERS!! **** ALL USERS WELCOME **", True, False, "Left")
			if(random.random() > .8) :
				scroll.scrollMessage("Hey there " + str(int(random.uniform(10000,99999))), True, False, "Left")
				actions.explosion()
		elif(seq == 8) :
			if(random.random() > .8) : 
				actions.explosion()
				scroll.scrollMessage("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$", True, False, dir)
		elif (seq == 9) :
			stroopSequence()
		elif(seq == 11) :
			if(random.random() > .8) : actions.burst(10)
			if(random.random() > .8) : scroll.scrollMessage("** ART ART ART **", True, False, dir)
		elif(seq == 12) :
			if(random.random() > .8) : actions.burst(10)
			if(random.random() > .9) : scroll.scrollMessage("** VAST POTENTIAL **", True, False, "Left")
		elif(seq == 13) :
			if(random.random() > .8) : actions.explosion()
			if(random.random() > .8) : scroll.scrollMessage("% % %%%% HUGE PROBABILITIES %%%% % %", True, False, "Left")
		elif (seq == 10) :
			if(random.random() > .8) : actions.burst(10)
			if(random.random() > .8) : scroll.scrollMessage("<> THOUSANDS of COLORS <> VERY FRESH <>", True, True, "Left")



		elif (seq == 14) :
			if(random.random() > 0) :scroll.scrollMessage(" :)     :)     :)     :)     :)     :)     :o ", True, True, "Left")

		elif(seq == 4) :
			user.userAnimator(24)
		elif(seq == 5) :
			machine.machineAnimator(430)
		elif(seq == 6) :
			bluescreen.draw()
		elif(seq == 7) :
			actions.glitch()
		elif (seq == 20) :
			user.userAnimator(20)
			#machine.machineAnimator(80)
			#user.userAnimator(1)
			#machine.machineAnimator(80)
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



def main():
	global group, groups
	global action, scroll, machine, bluescreen, user, imgLoader, concentric, signage

	baseconfig = ConfigParser.ConfigParser()
	baseconfig.read('/home/pi/RPI/config.cfg')

	config = utils
	config.matrix = Adafruit_RGBmatrix(32, int(baseconfig.get("config", 'matrixTiles')))
	config.screenHeight = int(baseconfig.get("config", 'screenHeight'))
	config.screenWidth =  int(baseconfig.get("config", 'screenWidth'))
	config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	config.draw = ImageDraw.Draw(config.image)

	config.Image = Image
	config.ImageDraw = ImageDraw
	config.ImageFont = ImageFont
	iid = config.image.im.id
	config.matrix.SetImage(iid, 0, 0)
	config.tileSize = (int(baseconfig.get("config", 'tileSizeHeight')),int(baseconfig.get("config", 'tileSizeWidth')))
	config.rows = int(baseconfig.get("config", 'rows'))
	config.cols = int(baseconfig.get("config", 'cols'))

	config.actualScreenWidth  = int(baseconfig.get("config", 'actualScreenWidth'))
	config.useMassager = bool(baseconfig.getboolean("config", 'useMassager'))
	config.renderImage = Image.new("RGBA", (config.actualScreenWidth, 32))
	config.brightness =  float(baseconfig.get("config", 'brightness'))
	config.path = baseconfig.get("config", 'path')

	action = actions
	action.config = config
	config.actions = actions

	scroll = scroll
	scroll.config = config
	scroll.fontSize = int(baseconfig.get("scroll", 'fontSize'))
	scroll.vOffset = int(baseconfig.get("scroll", 'vOffset'))

	machine = machine
	machine.config = config

	bluescreen = bluescreen
	bluescreen.config = config

	user = user
	user.config = config
	user.userCenterx = int(baseconfig.get("user", 'userCenterx'))
	user.userCentery = int(baseconfig.get("user", 'userCentery'))

	imgLoader = loader
	imgLoader.debug = True
	imgLoader.config = config
	imgLoader.yOffset = config.screenHeight

	concentric = squares
	concentric.config = config

	signage = (1,2,3,11,12,13,10,8,9,17,14)
	#signage = (3,3)
	animations = (4,6,7,14,20,17,18)

	groups = [signage,animations]
	group = groups[0]
	group = groups[1]

	try:
		args = sys.argv
		options = ""
		if(len(args) > 1):
			argument =  args[1]
			if(len(args) > 2) : options = args[2]
			if(argument == "explosion") : 
				actions.explosion()
				exit()
			elif(argument == "burst") : 
				actions.burst()
				exit()
			elif(argument == "user") : 
				user.userAnimator(10)
				exit()        	
			elif(argument == "cards") : 
				machine.machineAnimator(10000)
				exit()
			elif(argument == "glitch") : 
				actions.glitch()
				exit()
			elif(argument == "scroll") : 
				scroll.scrollMessage(options, True, False, "Left")
				exit()
			elif(argument == "stroop") : 
				stroopSequence()
				exit()
			elif(argument == "squares") : 
				concentric.colorSwitch = False
				concentric.animator(60, "cols")
				exit()
			elif(argument == "blue") : 
				bluescreen.draw()
				exit()
			elif(argument == "pan") : 
				imgLoader.action = "pan"
				imgLoader.countLimit = 1
				imgLoader.start("",0,-1)
				exit()	
			elif(argument  == "play") :
				imgLoader.action = "play"
				imgLoader.countLimit = 100
				imgLoader.start()
			elif(argument  == "seq") :
				group = groups[int(options)]
				seq2()

		else : seq2()
	except getopt.GetoptError as err:
		# print help information and exit:
		print str(err) # will print something like "option -a not recognized"

if __name__ == "__main__":
    main()



