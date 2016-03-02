#!/usr/bin/python
#import modules
from modules import utils, actions, machine, scroll, user, bluescreen ,loader, squares, flashing, blender, carousel, squaresalt
from cntrlscripts import off_signal
import Image
import ImageDraw
import time
import random
from rgbmatrix import Adafruit_RGBmatrix
import datetime
import ImageFont
import textwrap
import math
import sys, getopt, os
import ConfigParser, io
from subprocess import call
import threading
global thrd

T1 = 0
T2 = 0

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

def imageScrollSeq() :
	global group, groups
	global action, scroll, machine, bluescreen, user, imgLoader, concentric, signage
	global T1, T2

	# Get all files in the drawing folder
	path = config.path  + "/imgs/drawings"
	rawList = os.listdir(path)
	imageList = []
	seq = 1

	for f in rawList :
		if os.path.isfile(os.path.join(path, f)) and not f.startswith("._") and not f.startswith(".") :
			imageList.append(f)

	'''
	try:
		args = sys.argv
		if(len(args) > 1):
			seq =  int(args[2])
			#if(len(args) > 2) : options = args[2]
			#if(len(args) > 3) : options2 = args[3]
			#if(len(args) > 4) : options3 = args[4]
	except getopt.GetoptError as err:
		# print help information and exit:
		print str(err)
	print (seq)
	'''

	while True:
		# --------------------------------------------------------------------------#
		# Force the checking of the status file  -- sometimes the cron does not run
		# probably due to high CPU load etc ...
		# --------------------------------------------------------------------------#
 		T2 = time.time()
                if((T2 - T1) > 15) :
                        threads = []
                        thrd = threading.Thread(target=off_signal.checker)
                        threads.append(thrd)
                        thrd.start()

                        #print(threads)
                        #off_signal.checker()
                        T1 = time.time()		

		if (seq == 1) :
			imageList = ['plane-2b.gif','paletter3c.gif'] 
			imgLoader.debug = False
			imgLoader.action = "pan"
			imgLoader.countLimit = 1
			imgLoader.xOffset =  0
			imgLoader.yOffset = 0
			imgLoader.panRangeLimit = 0 + config.screenWidth
			imgLoader.scrollSpeed = .01
			imgLoader.useJitter =  True
			imgLoader.useBlink = True
			imgLoader.brightnessFactor = .8
			imgLoader.start(config.path  + "/imgs/" + imageList[0], 1 , 0)

		if (seq == 2) :
			imageList = ['plane-2b.gif','paletter3c.gif'] 
			imgLoader.debug = False
			imgLoader.action = "play"
			imgLoader.countLimit = 5
			imgLoader.gifPlaySpeed = .08
			imgLoader.brightnessFactor  = .2
			imgLoader.brightnessFlux = True
			imgLoader.xOffset =  0
			imgLoader.yOffset = 0
			imgLoader.panRangeLimit = 0 + config.screenWidth
			imgLoader.scrollSpeed = .01
			imgLoader.useJitter =  True
			imgLoader.useBlink = True
			imgLoader.start(config.path  + "/imgs/"  + imageList[1], 0 , 0)

		if(seq == 3) :
			imgLoader.debug = False
			imgLoader.action = "pan"
			imgLoader.countLimit = 2
			imgLoader.xOffset =  0
			imgLoader.yOffset = 0
			imgLoader.panRangeLimit = 0 #+ config.screenWidth
			imgLoader.scrollSpeed = .01
			imgLoader.countLimit = 1
			imgLoader.resizeToWidth = True
			img = int(random.random() *  len(imageList))
			imgLoader.start(path + "/" + imageList[img], 0, -1)


###################################################
# -------   Runs the sequences             ------*#
###################################################
def runSequence() :
	global group, groups
	global action, scroll, machine, bluescreen, user, carouselSign, imgLoader, concentric, flash, blend, sqrs
	global T1,T2,thrd
	lastAction  = 0

 	try:

		# If there are more than one set of animations per group e.g. various
		# text sequences, "randomize" the selection and try to avoid repeating
		# the exact same one twice in a row ...

		if(len(group) > 1) :
			seq = int(random.uniform(1,30))
			while (seq not in group and seq != lastAction) : 
				seq = int(random.uniform(1,30))
		else : 
			seq = group[0]
		# try not to repeat
		lastAction = seq
		#print("running", group, len(group))

		# --------------------------------------------------------------------------#
		# Force the checking of the status file  -- sometimes the cron does not run
		# probably it seems due to higher CPU load etc ...
		# --------------------------------------------------------------------------#
		T2 = time.time()
		if((T2 - T1) > 15) :
			threads = []
			thrd = threading.Thread(target=off_signal.checker)
			threads.append(thrd)
			thrd.start()
			
			#print(threads)
			#off_signal.checker()
			T1 = time.time()

		# -------  SCROLL         -------------
		if(seq == 1) :
			if(random.random() > .8) :actions.burst(10)
			scroll.scrollMessage("** PTGS ** GIFS ** JPEGS ** AVIs ** MOVs ** CODEZ ** CRACKS **", True, False, "Left")
		
		# -------  SCROLL         -------------
		elif(seq == 2) :
			if(random.random() > .8) : actions.explosion()
			scroll.scrollMessage("** FIGURATIVE ** ABSTRACT ** NO SOFTWARE **", True, False, "Left")
		
		# -------  SCROLL         -------------
		elif(seq == 3) :
			if(random.random() > .8) : actions.explosion()
			scroll.scrollMessage("** All USERS!! **", True, False, "Left")
			if(random.random() > .8) :
				scroll.scrollMessage("Hey there " + str(int(random.uniform(10000,99999))) + "asdfasdfasdsf", True, False, "Left")
				actions.explosion()
		
		# -------  SCROLL  $$$$   -------------
		elif(seq == 4) :
			if(random.random() > .8) : actions.explosion()
			numDolls = int(random.uniform(3,24))
			strg = ""
			for n in range (3,numDolls) : strg += "$"
			scroll.scrollMessage(strg, True, False, getDirection())
		
		# -------  STROOP STROOP  -------------
		elif (seq == 5) :
			numRuns = int(random.uniform(2,6))
			for i in range(0,numRuns) : 
				if(scroll.opticalOpposites) : 
					scroll.opticalOpposites = False
				else : 
					scroll.opticalOpposites = True
				stroopSequence()
		
		# -------  SCROLL         -------------
		elif (seq == 6) :
			if(random.random() > .8) : actions.burst(10)
			scroll.scrollMessage("<> THOUSANDS of COLORS <>", True, True, "Left")
		
		# -------  SCROLL         -------------
		elif(seq == 7) :
			if(random.random() > .8) : actions.burst(10)
			scroll.scrollMessage("** PTGS PTGS PTGS **", True, False, "Left")
		
		# -------  SCROLL         -------------
		elif(seq == 8) :
			if(random.random() > .8) : actions.burst(10)
			if(random.random() > .8) : actions.explosion()
			scroll.scrollMessage("** COLD AND HOT **", True, False, "Left")
		
		# -------  SCROLL         -------------
		elif(seq == 9) :
			if(random.random() > .8) : actions.explosion()
			scroll.scrollMessage("% % %%%% HUGE PROBABILITIES %%%% % %", True, False, "Left")					
		
		# ------- * EMOTIES       -------------
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
		
		# -------  ASIF SCREEN     -------------
		elif (seq == 11) :
			scroll.countLimit = 5
			scroll.present("ASIF",1)
		
		# -------  ASIF LOVE FEAR CAROUSEL -------	
		elif(seq == 12) :
			clrFlicker = carouselSign.useColorFLicker
			if(random.random() > .95) : carouselSign.useColorFLicker = True
			carouselSign.go("    **** HOT & COLD ****", 0)
			#carouselSign.useColorFlicker = clrFlicker
			carouselSign.useColorFLicker = False
		
		# -------  ASIF LOVE FEAR CAROUSEL noend *	
		elif(seq == 13) :
			if(random.random() > .5) : carouselSign.useColorFLicker = True
			carouselSign.go("       ***** BEEF * CHICKEN * PORK * FISH * LAMB  ****", -1)
			carouselSign.useColorFlicker = False

		# Animation only modules
		
		# -------  USER            -------------
		elif(seq == 14) :
			fixed = False
			duration = int(random.uniform(24,100))
			if(random.random() > .4) : fixed = True
			user.userAnimator(duration, 2, fixed)
		
		# -------  CARDS / MACHINE -------------
		elif(seq == 15) :
			machine.machineAnimator(830) # 430
			if(random.random() > .9) : user.userAnimator(24)
		
		# -------  BLUE SCREEN     -------------
		elif(seq == 16) :
			bluescreen.draw()
		
		# -------  GLITCH SCREEN   -------------
		elif(seq == 17) :
			actions.glitch()
		
		# -------  CONCENTRICS     -------------
		elif (seq == 18) :
			concentric.colorSwitch = False
			concentric.animator(60)
		
		# -------  EXLPOSIONS      -------------
		elif (seq == 19) :
			actions.explosion()

		# -------  BLEND/FLASH     -------------
		elif(seq == 23) : 
			blend.colorSwitch = False
			blend.animator(0)


		# Image Loading Modules	
		
		# -------  DEFAULT PAN     -------------
		elif (seq == 20) :
			imgLoader.action = "pan"
			imgLoader.countLimit = 1
			imgLoader.start("",0,-1)
		
		# -------  DEFAULT PLAY (FLAMES) -------
		elif (seq == 21) :
			imgLoader.action = "play"
			imgLoader.countLimit = 500
			imgLoader.xOffset = 0
			imgLoader.yOffset = 0
			imgLoader.start()
		
		#------ Plane Scrolling --------
		elif (seq == 22) :
			imageScrollSeq()

		#------ Present Bad Pixel --------
		elif (seq == 24 or seq == 25) :
			imageList = ['badpixel.gif'] 
			imgLoader.debug = False
			imgLoader.action = "present"
			imgLoader.countLimit = 1 #int(random.uniform(10,100))
			imgLoader.gifPlaySpeed = int(random.uniform(50,250))
			imgLoader.brightnessFactor  = random.uniform(.25,.75)
			imgLoader.brightnessFlux = True
			imgLoader.brightnessFluxRate = 240
			imgLoader.xOffset = 0
			imgLoader.yOffset = 0
			img = 0
			path = config.path  + "/imgs"
			img = int(random.random() *  len(imageList))
			imgLoader.start(path + "/" + imageList[img],0,-1)

	except Exception, e:
		if(e == "KeyboardInterrupt") :
			print("Stopping")
			exit()
		else :
			# Weak....
			pass  

	time.sleep(.001)
	runSequence()



###################################################
# -------   SETTING UP THE SEQUENCE GROUPS ------*#
###################################################
def setUpSequenceGroups() :
		global group, groups, config
		global action, scroll, machine, bluescreen, user, carouselSign
		global imgLoader, concentric, flash, blend, sqrs

		#signage = (1,2,3,4,6,7,8,9,11,12,21)
		signage = (4,11,12,21)

		# no image panning
		# 16 = blueScreen
		# 17 = glitch
		# 24 = bad pixel
		animations = (17,24,25)

		# just Stroop / colors
		stroopSeq = (5,)

		# just emotis
		emotiSeq = (10,)

		# just concentric squares
		concentricRecs = (18,)

		# just cards & user
		cardsUsers = (15,)

		# Carousel Only
		carouselSolo = (12,)

		# Blend / flashing lights
		flashingBlend = (23,)

		# plane scrolling
		imageScroll = (22,)

		# Users
		users = (14,)

		# start via cmd  sudo python /home/pi/RPI/sequence.py seq 5
		groups = [signage, animations, stroopSeq, emotiSeq, concentricRecs, cardsUsers, carouselSolo, flashingBlend, imageScroll, users]
		group = groups[1]
		options = options2 = options3 = ""


###################################################
# -------   Reads configuration files and sets
# -------   defaults                             *#
###################################################
def configure() :
	global group, groups, config
	global action, scroll, machine, bluescreen, user, carouselSign, imgLoader, concentric, flash, blend, sqrs

	try: 
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
		config.transWiring = bool(baseconfig.getboolean("config", 'transWiring'))

		action = actions
		action.config = config
		config.actions = actions

		scroll = scroll
		scroll.config = config
		scroll.fontSize = int(baseconfig.get("scroll", 'fontSize'))
		scroll.vOffset = int(baseconfig.get("scroll", 'vOffset'))
		scroll.scrollSpeed = float(baseconfig.get("scroll", 'scrollSpeed'))
		scroll.stroopSpeed = float(baseconfig.get("scroll", 'stroopSpeed'))
		scroll.stroopSteps = float(baseconfig.get("scroll", 'stroopSteps'))
		
		machine = machine
		machine.config = config

		bluescreen = bluescreen
		bluescreen.config = config

		user = user
		user.config = config
		user.userCenterx = int(baseconfig.get("user", 'userCenterx'))
		user.userCentery = int(baseconfig.get("user", 'userCentery'))
		user.scale = float(baseconfig.get("user", 'scale'))

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

		sqrs = squaresalt
		sqrs.config = config

		flash = flashing
		flash.config = config

		blend = blender
		blend.config = config
		blend.colorSwitch = False
		blend.boxWidth = 16

		# ---- Call the group-sequence config fcu -----#
		setUpSequenceGroups()

		return True


	except getopt.GetoptError as err:
		# print help information and exit:
		print ("Error:" + str(err))
		return False



def main():
	global group, groups, config
	global action, scroll, machine, bluescreen, user, carouselSign, imgLoader, concentric, flash, blend, sqrs
	
	####################################################################
	################  JUST FOR COMMAND LINE !!!!! ######################
	### Below are used to run individual modules from command line
	# eg ./run.sh explosion or ./run.sh scroll "TEST" 2
	####################################################################

	if(configure()) :
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
					user.userAnimator(250,2,True)
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
				elif(argument == "sqrs") : 
					sqrs.colorSwitch = False
					sqrs.animator(60, "cols")
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
					imgLoader.xOffset = 0
					imgLoader.yOffset = 0
					imgLoader.start()
				elif(argument  == "car") :
					carouselSign.go(options)

				###################################################
				# ----------  Play the group sequence  ---------- #
				###################################################

				elif(argument  == "seq") :
					group = groups[int(options)]
					runSequence()

			else : runSequence()
		except getopt.GetoptError as err:
			# print help information and exit:
			print ("Error:" + str(err))

if __name__ == "__main__":
    main()



