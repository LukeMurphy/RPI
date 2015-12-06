#!/usr/bin/python
#import modules
from modules import utils, actions, machine, scroll, user, bluescreen ,loader, squares, flashing
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

def getDirection() :
	d = int(random.uniform(1,3))
	direction = "Left"
	if (d == 1) : direction = "Left"
	if (d == 2) : direction = "Right"
	if (d == 3) : direction = "Bottom"
	return direction

def runSequence() :
	global group, groups
	global action, scroll, machine, bluescreen, user, imgLoader, concentric, signage

	lastAction  = 0

	print("running")
	try:
		while True:
			seq = int(random.uniform(1,30))
			while (seq not in group and seq != lastAction) : 
				seq = int(random.uniform(1,30))

			# try not to repeat
			lastAction = seq
			#seq = 18

			if(seq == 1) :
				if(random.random() > .8) :actions.burst(10)
				if(random.random() > .8) :scroll.scrollMessage("** PTGS ** GIFS ** JPEGS ** AVIs ** MOVs ** CODEZ ** CRACKS **", True, False, "Left")
			elif(seq == 2) :
				if(random.random() > .8) : actions.explosion()
				if(random.random() > .8) : scroll.scrollMessage("** FIGURATIVE ** ABSTRACT ** NO SOFTWARE **", True, False, "Left")
			elif(seq == 3) :
				if(random.random() > .8) : actions.explosion()
				if(random.random() > .8) : scroll.scrollMessage("** All USERS!! **** ALL USERS WELCOME **", True, False, "Left")
				if(random.random() > .8) :
					scroll.scrollMessage("Hey there " + str(int(random.uniform(10000,99999))) + "asdfasdfasdsf", True, False, "Left")
					actions.explosion()
			elif(seq == 4) :
				if(random.random() > .8) : 
					actions.explosion()
					numDolls = int(random.uniform(3,24))
					strg = ""
					for n in range (3,numDolls) : strg += "$"
					scroll.scrollMessage(strg, True, False, getDirection())
			elif (seq == 5) :
				numDolls = int(random.uniform(2,6))
				for i in range(0,numDolls) : 
					if(scroll.opticalOpposites) : 
						scroll.opticalOpposites = False
					else : 
						scroll.opticalOpposites = True
					stroopSequence()
			elif (seq == 6) :
				if(random.random() > .8) : actions.burst(10)
				if(random.random() > .8) : scroll.scrollMessage("<> THOUSANDS of COLORS <> VERY FRESH <>", True, True, "Left")
			elif(seq == 7) :
				if(random.random() > .8) : actions.burst(10)
				if(random.random() > .8) : scroll.scrollMessage("** PTGS PTGS PTGS **", True, False, getDirection())
			elif(seq == 8) :
				if(random.random() > .8) : actions.burst(10)
				if(random.random() > .9) : scroll.scrollMessage("** VAST POTENTIAL **", True, False, "Left")
			elif(seq == 9) :
				if(random.random() > .8) : actions.explosion()
				if(random.random() > .8) : scroll.scrollMessage("% % %%%% HUGE PROBABILITIES %%%% % %", True, False, "Left")					
			elif (seq == 10) :
				if(random.random() > .8) :
					numDolls = int(random.uniform(2,6))
					strg = ""
					for n in range (2,numDolls) : 
						strg += "     :)"
						if (random.random() > .95) : strg += "     :o"
						if (random.random() > .95) : strg += "     ;)"
					scroll.scrollMessage(strg, True, True, "Left")
			elif (seq == 11) :
				if(random.random() > .8) :
					scroll.countLimit = 5
					scroll.present("ASIF",1)
			

			# Animation only modules

			elif(seq == 14) :
				user.userAnimator(24)
			elif(seq == 15) :
				machine.machineAnimator(430) # 430
			elif(seq == 16) :
				bluescreen.draw()
			elif(seq == 17) :
				actions.glitch()
			elif (seq == 18) :
				imgLoader.action = "pan"
				imgLoader.countLimit = 1
				imgLoader.start("",0,-1)
			elif (seq == 19) :
				imgLoader.action = "play"
				imgLoader.countLimit = 100
				imgLoader.start()
			elif (seq == 20) :
				concentric.colorSwitch = False
				concentric.animator(60)
			elif (seq == 21) :
				user.userAnimator(12)
				machine.machineAnimator(80)
				user.userAnimator(1)
				machine.machineAnimator(80)
				actions.burst(20)
				actions.explosion()
	
	except KeyboardInterrupt:
		print "Stopping"
		exit()    


def main():
	global group, groups
	global action, scroll, machine, bluescreen, user, imgLoader, concentric, signage, flash

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

	flash = flashing
	flash.config = config


	#*******  SETTING UP THE SEQUENCE GROUPS *********#
	signage = (1,2,3,4,5,6,7,8,9,10,11,19)
	animations = (14,15,16,17,18,19,20,21)

	# no image panning
	animations = (14,15,16,17,19,20,21)
	#debug animations = (14,15)


	groups = [signage,animations]
	group = groups[0]
	group = groups[1]
	options = options2 = options3 = ""

	try:
		args = sys.argv
		#print(args)
		if(len(args) > 1):
			argument =  args[1]
			if(len(args) > 2) : options = args[2]
			if(len(args) > 3) : options2 = args[3]
			if(len(args) > 4) : options3 = args[4]
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
				if (options2 != "") : scroll.steps = int(options2)
				actions.drawBlanksFlag = False
				scroll.scrollMessage(options, True, False, "Left")
				exit()
			elif(argument == "present") : 
				# e.g. spy sequence.py present "ASIF" 1 0
				if (options2 != "") : dur = int(options2)
				if (options3 != "") : scroll.countLimit = int(options3)
				actions.drawBlanksFlag = False
				scroll.present(options,(), dur)
				exit()
			elif(argument == "stroop") : 
				for i in range(0,10) : 
					if(scroll.opticalOpposites) : 
						scroll.opticalOpposites = False
					else : 
						scroll.opticalOpposites = True
					stroopSequence()
				exit()
			elif(argument == "squares") : 
				concentric.colorSwitch = False
				concentric.animator(60, "cols")
				exit()
			elif(argument == "flash") : 
				flash.colorSwitch = False
				flash.animator(100)
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
				runSequence()

		else : runSequence()
	except getopt.GetoptError as err:
		# print help information and exit:
		print str(err)

if __name__ == "__main__":
    main()



