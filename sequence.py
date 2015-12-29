#!/usr/bin/python
#import modules
from modules import utils, actions, machine, scroll, user, bluescreen ,loader, squares, flashing, blender, carousel
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
	directionStr = getDirection()
	if(random.random() > .7) :scroll.stroop("YELLOW",(255,0,225),directionStr)
	if(random.random() > .7) :scroll.stroop("VIOLET",(230,225,0),directionStr)
	if(random.random() > .7) :scroll.stroop("RED",(0,255,0),directionStr)
	if(random.random() > .7) :scroll.stroop("BLUE",(225,100,0),directionStr)
	if(random.random() > .7) :scroll.stroop("GREEN",(255,0,0),directionStr)
	if(random.random() > .7) :scroll.stroop("ORANGE",(0,0,200),directionStr)

def getDirection() :
	d = int(random.uniform(1,4))
	direction = "Left"
	if (d == 1) : direction = "Left"
	if (d == 2) : direction = "Right"
	if (d == 3) : direction = "Bottom"
	return direction

def runSequence() :
	global group, groups
	global action, scroll, machine, bluescreen, user, carouselSign, imgLoader, concentric, flash, blend
	lastAction  = 0

	print("running", group)
	try:
		while True:

			if(len(group) > 1) :
				seq = int(random.uniform(1,30))
				while (seq not in group and seq != lastAction) : 
					seq = int(random.uniform(1,30))
			else : 
					seq = group[0]
			# try not to repeat
			lastAction = seq
			#seq = 18
			#******* SCROLL         ***************
			if(seq == 1) :
				if(random.random() > .8) :actions.burst(10)
				scroll.scrollMessage("** PTGS ** GIFS ** JPEGS ** AVIs ** MOVs ** CODEZ ** CRACKS **", True, False, "Left")
			#******* SCROLL         ***************
			elif(seq == 2) :
				if(random.random() > .8) : actions.explosion()
				scroll.scrollMessage("** FIGURATIVE ** ABSTRACT ** NO SOFTWARE **", True, False, "Left")
			#******* SCROLL         ***************
			elif(seq == 3) :
				if(random.random() > .8) : actions.explosion()
				scroll.scrollMessage("** All USERS!! **", True, False, "Left")
				if(random.random() > .8) :
					scroll.scrollMessage("Hey there " + str(int(random.uniform(10000,99999))) + "asdfasdfasdsf", True, False, "Left")
					actions.explosion()
			#******* SCROLL  $$$$   ***************
			elif(seq == 4) :
				if(random.random() > .8) : actions.explosion()
				numDolls = int(random.uniform(3,24))
				strg = ""
				for n in range (3,numDolls) : strg += "$"
				scroll.scrollMessage(strg, True, False, getDirection())
			#******* STROOP STROOP  ***************
			elif (seq == 5) :
				numDolls = int(random.uniform(2,6))
				for i in range(0,numDolls) : 
					if(scroll.opticalOpposites) : 
						scroll.opticalOpposites = False
					else : 
						scroll.opticalOpposites = True
					stroopSequence()
			#******* SCROLL         ***************
			elif (seq == 6) :
				if(random.random() > .8) : actions.burst(10)
				scroll.scrollMessage("<> THOUSANDS of COLORS <>", True, True, "Left")
			#******* SCROLL         ***************
			elif(seq == 7) :
				if(random.random() > .8) : actions.burst(10)
				scroll.scrollMessage("** PTGS PTGS PTGS **", True, False, "Left")
			#******* SCROLL         ***************
			elif(seq == 8) :
				if(random.random() > .8) : actions.burst(10)
				scroll.scrollMessage("** VAST POTENTIAL **", True, False, "Left")
			#******* SCROLL         ***************
			elif(seq == 9) :
				if(random.random() > .8) : actions.explosion()
				scroll.scrollMessage("% % %%%% HUGE PROBABILITIES %%%% % %", True, False, "Left")					
			#******** EMOTIES       ***************
			elif (seq == 10) :
				# reset blanks
				if (random.random() > .5) : actions.setBlanks()
				numDolls = int(random.uniform(30,60))
				strg = ""
				scroll.fontSize -= 6
				actions.drawCounterXOsFlag = True
				space = "  "
				for n in range (2, numDolls) : 
					strg += ":)"+space
					if (random.random() > .95) : strg += ":o"+space
					if (random.random() > .95) : strg += ";)"+space
				scroll.scrollMessage(strg, True, True, "Left")

				# After completition reset for other runs
				scroll.fontSize += 6
				actions.drawCounterXOsFlag = False
			#******* ASIF SCREEN     ***************
			elif (seq == 11) :
				scroll.countLimit = 5
				scroll.present("ASIF",1)
			#******* ASIF LOVE FEAR CAROUSEL *******	
			elif(seq == 12) :
				clrFlicker = carouselSign.useColorFLicker
				carouselSign.useColorFLicker = False
				carouselSign.go("    ****  ASIF * LOVE & FEAR ****", 0)
				carouselSign.useColorFlicker = clrFlicker
			#******* ASIF LOVE FEAR CAROUSEL noend *	
			elif(seq == 13) :
				if(random.random() > .5) : carouselSign.useColorFLicker = True
				carouselSign.go("    ****  ASIF * LOVE & FEAR ****", -1)
				carouselSign.useColorFlicker = False

			# Animation only modules
			#******* USER            ***************
			elif(seq == 14) :
				user.userAnimator(24)
			#******* CARDS / MACHINE ***************
			elif(seq == 15) :
				machine.machineAnimator(830) # 430
				if(random.random() > .9) : user.userAnimator(24)
			#******* BLUE SCREEN     ***************
			elif(seq == 16) :
				bluescreen.draw()
			#******* GLITCH SCREEN   ***************
			elif(seq == 17) :
				actions.glitch()
			#******* CONCENTRICS     ***************
			elif (seq == 18) :
				concentric.colorSwitch = False
				concentric.animator(60)
			#******* EXLPOSIONS      ***************
			elif (seq == 19) :
				actions.explosion()

			# Image Loading Modules	
			#******* DEFAULT PAN     ***************
			elif (seq == 20) :
				imgLoader.action = "pan"
				imgLoader.countLimit = 1
				imgLoader.start("",0,-1)
			#******* DEFAULT PLAY (FLAMES) *********
			elif (seq == 21) :
				imgLoader.action = "play"
				imgLoader.countLimit = 20
				imgLoader.start()


	except KeyboardInterrupt:
		print "Stopping"
		exit()    

def main():
	global group, groups, config
	global action, scroll, machine, bluescreen, user, carouselSign, imgLoader, concentric, flash, blend

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
	scroll.scrollSpeed = float(baseconfig.get("scroll", 'scrollSpeed'))

	machine = machine
	machine.config = config

	bluescreen = bluescreen
	bluescreen.config = config

	user = user
	user.config = config
	user.userCenterx = int(baseconfig.get("user", 'userCenterx'))
	user.userCentery = int(baseconfig.get("user", 'userCentery'))

	carouselSign = carousel
	carouselSign.config = config
	carouselSign.fontSize = int(baseconfig.get("scroll", 'fontSize'))
	carouselSign.vOffset = int(baseconfig.get("scroll", 'vOffset'))
	carouselSign.useColorFLicker = bool(baseconfig.getboolean("scroll", 'useColorFLicker'))
	#carouselSign.clr = (120,120,120)

	imgLoader = loader
	imgLoader.debug = True
	imgLoader.config = config
	imgLoader.yOffset = config.screenHeight

	concentric = squares
	concentric.config = config

	flash = flashing
	flash.config = config

	blend = blender
	blend.config = config
	blend.boxWidth = 16




	#*******  SETTING UP THE SEQUENCE GROUPS *********#
	signage = (1,2,3,4,6,7,8,9,11,12,21)

	# no image panning
	animations = (14,16,17,18, 19, 21)

	# just Stroop / colors
	stroopSeq = (5,)

	# just emotis
	emotiSeq = (10,)

	# just concentric squares
	concentricRecs = (18,)

	# just cards & user
	cardsUsers = (15,)

	# Carousel Only
	carouselSolo = (13,)

	# start via cmd  sudo python /home/pi/RPI/sequence.py seq 5
	groups = [signage, animations, stroopSeq, emotiSeq, concentricRecs, cardsUsers, carouselSolo]
	group = groups[0]
	group = groups[1]
	options = options2 = options3 = ""

	################  JUST FOR COMMAND LINE !!!!! ######################
	### Below are used to run individual modules from command line
	# eg ./run.sh explosion or ./run.sh scroll "TEST"

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
			elif(argument == "blend") : 
				blend.colorSwitch = False
				blend.animator(100)
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
			elif(argument  == "car") :
				carouselSign.go(options)

		else : runSequence()
	except getopt.GetoptError as err:
		# print help information and exit:
		print str(err)

if __name__ == "__main__":
    main()



