import math
import random
import threading
import time
from modules.configuration import bcolors
from modules import colorutils
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps


"""
config.percentage will be the global config variable for display of progress

"""


def reDraw():

	"""""" """""" """""" """ BOX AND BAR """ """""" """""" """""" """""" """"""
	drawBar()

	"""""" """""" """""" """ SPINNER """ """""" """""" """""" """""" """"""
	drawSpinner()

	"""""" """""" """""" """ TEXT MESSAGE """ """""" """""" """""" """"""
	drawMessageText()


def drawMessageText():
	global config

	# Set the message to be the % completed
	config.displayPercentage = int(math.floor(config.percentage))
	if config.messageOverrideActive != True and config.firstRun != True:
		config.messageString = str(config.displayPercentage) + "%"

	if config.messageOverrideActive == True:
		config.messageString = config.altStringMessage

	# Draw the message percentage
	indent = 4
	scrollImage = Image.new(
		"RGBA", (config.pixLen[0] + 2 * indent, config.fontHeight + 2 * indent)
	)
	txtdraw = ImageDraw.Draw(scrollImage)
	messageString = config.messageString
	font = config.font
	shadowColor = config.shadowColor

	for i in range(1, config.shadowSize):
		txtdraw.text((indent - i, -i), messageString, shadowColor, font=font)
		txtdraw.text((indent - i, 0), messageString, shadowColor, font=font)
		txtdraw.text((indent - i, +i), messageString, shadowColor, font=font)
		txtdraw.text((indent + 0, -i), messageString, shadowColor, font=font)
		txtdraw.text((indent + 0, 0), messageString, shadowColor, font=font)
		txtdraw.text((indent + 0, +i), messageString, shadowColor, font=font)
		txtdraw.text((indent + i, -i), messageString, shadowColor, font=font)
		txtdraw.text((indent + i, 0), messageString, shadowColor, font=font)
		txtdraw.text((indent + i, +i), messageString, shadowColor, font=font)
	txtdraw.text((indent, 0), messageString, config.messageClr, font=font)

	# Draw a box around message display
	# numXPos = int(xPos2 - 40)
	config.pixLen = config.draw.textsize(messageString, font=font)
	if messageString != config.altStringMessage:
		numXPos = config.boxMax - config.pixLen[0] - 8
	else:
		numXPos = config.boxMax - config.pixLen[0] - 8
	# numXPos = 32
	numYPos = int(config.spinnerCenter[1]- config.fontHeight /2)
	config.spinnerCenter[0] = numXPos - config.spinnerRadius - 0
	# txtdraw.rectangle((0,0,pixLen[0]+indent+2, pixLen[1] + indent-1), outline=(0,100,0))
	config.image.paste(scrollImage, (numXPos, numYPos), scrollImage)


def drawSpinner():
	global config
	"""""" """""" """""" """ SPINNER """ """""" """""" """""" """""" """"""
	# Draw a spinner
	config.spinnerAngle += math.pi / config.spinnerAngleSteps
	if config.spinnerAngle > 2 * math.pi:
		config.spinnerAngle = 0
	config.cwidth = (config.spinnerRadius - config.spinnerInnerRadius) + 4

	for n in range(0, 0):
		r = config.spinnerRadius - n + 2
		config.draw.ellipse(
			(
				config.spinnerCenter[0] - r,
				config.spinnerCenter[1] - r,
				config.spinnerCenter[0] + r,
				config.spinnerCenter[1] + r,
			),
			outline=(10, 10, 10, 40),
		)

	for s in range(0, config.spinnerAngleSteps):
		angle = s * 2 * math.pi / config.spinnerAngleSteps + config.spinnerAngle
		sX0 = config.spinnerInnerRadius * math.sin(angle) + config.spinnerCenter[0]
		sX = config.spinnerRadius * math.sin(angle) + config.spinnerCenter[0]
		sY0 = config.spinnerInnerRadius * math.cos(angle) + config.spinnerCenter[1]
		sY = config.spinnerRadius * math.cos(angle) + config.spinnerCenter[1]
		b = float(s) / float(config.spinnerAngleSteps)
		fillColor = (round(b * 250), round(b * 200), 0, 200)
		# if (b <=.01) : fillColor = barColor
		config.draw.line((sX0, sY0, sX, sY), fill=fillColor)


def drawBar():
	global config

	# Unless overridden, boxWidth is ~ to percentage
	if config.drawBarFill:
		config.boxWidth = round(config.percentage / 100 * config.boxMax)

	# draw box container

	rVd = round(config.barColor[0] * .42)
	gVd = round(config.barColor[1] * .42)
	bVd = round(config.barColor[2] * .42)
	config.draw.rectangle(
		(
			config.xPos - 1,
			config.yPos - 1,
			config.boxMax + 1,
			config.boxHeight + config.yPos + 1,
		),
		outline=(config.outlineColor),
		fill=((rVd,0,bVd)),
	)




	# draw bar
	config.boxWidthDisplay = config.boxWidth
	# draw flat box progress bar
	if config.drawBarFill:
		config.boxWidthDisplay = config.boxWidth
	config.xPos1 = config.xPos
	config.xPos2 = config.boxWidthDisplay + config.xPos
	config.yPos1 = config.yPos
	config.yPos2 = config.boxHeight + config.yPos

	# Draw single left-most black line
	config.draw.rectangle((0, config.yPos1, 1, config.yPos2), fill=(0, 0, 0))

	# draw flat box progress bar - default
	config.draw.rectangle(
		(config.xPos1, config.yPos1, config.xPos2, config.yPos2), fill=(200, 0, 0)
	)

	lines = config.canvasHeight - 2
	if config.gradientLevel == 1:
		arc = math.pi / lines * 1
	else:
		arc = math.pi / lines

	if config.useVerticalColorGradient:
		# Draw vertical shading gradient
		for n in range(0, lines):
			yPos = config.yPos1 + n
			b = math.sin(arc * n) * 1.2
			# b = cyclicalBrightness
			rVd = round(config.barColor[0] * b)
			gVd = round(config.barColor[1] * b)
			bVd = round(config.barColor[2] * b)
			barColorDisplay = (rVd, gVd, bVd)
			config.draw.rectangle(
				(config.xPos1, yPos, config.xPos2, yPos), fill=(barColorDisplay)
			)

	elif config.useHorizontalColorGradient:
		# Draw horizontal color gradient bar
		vLines = round(config.xPos2 - config.xPos1)
		dR = (config.barColorEnd[0] - config.barColorStart[0]) / (vLines + 1)
		dG = (config.barColorEnd[1] - config.barColorStart[1]) / (vLines + 1)
		dB = (config.barColorEnd[2] - config.barColorStart[2]) / (vLines + 1)
		for p in range(0, vLines):
			config.xPos1p = config.xPos1 + p
			config.xPos2p = config.xPos1p + 1
			# cyclicalBrightness = abs(math.sin(cyclicalArc * cyclicalBrightnessPhase * boxMax/vLines))+.1
			# cyclicalBrightness = 1
			# if(config.debug ) : prround(cyclicalBrightness)
			rV = round(config.barColorStart[0] + p * dR)
			gV = round(config.barColorStart[1] + p * dG)
			bV = round(config.barColorStart[2] + p * dB)

			# Draw vertical shading gradient "3D!"
			for n in range(0, lines):
				config.yPos = config.yPos1 + n
				b = math.sin(arc * n)
				# b = cyclicalBrightness
				rVd = round(rV * b)
				gVd = round(gV * b)
				bVd = round(bV * b)
				barColor = (rVd, gVd, bVd)
				config.draw.rectangle(
					(config.xPos1p, config.yPos, config.xPos2p, config.yPos),
					fill=(barColor),
				)


#####################################################


def decisions():
	global config

	if (
		config.percentage >= config.target
		and config.firstRun != True
		and config.completed != True
		and config.goPast != True
	):
		config.t2 = time.time()
		timeToComplete = config.t2 - config.t1
		# config.percentageIncrement = (0.1 + 5 * random.random()) * config.calibratedCycleRate
		config.completed = True
		# config.messageOverrideActive = False
		if config.debug:
			print("Completed progress as far as ")
		startPause(random.uniform(1, 12))

	if config.goPast == True and config.percentage > 150:
		if random.random() < 0.01:
			config.completed = True
			if config.debug:
				print("Completed beyond ")

	if config.goPast == True and config.percentage < 100 and config.percentage > 50:
		if random.random() < 0.1:
			changeRate(3, 8)
		# startPause(random.uniform(1,12))

	if config.paused == False and config.firstRun == False:

		if (
			random.random() < (config.pauseProbability * config.calibratedCycleRate)
			and config.firstRun == False
			and config.percentage >= config.pausePoint
		):
			startPause(random.uniform(1.0, 5.0))
			config.messageOverrideActive = True

		if (
			random.random() < config.changeRateProbability * config.calibratedCycleRate
			or config.percentage < 0
		):
			if config.debug:
				print("Changing rate...")

			if config.percentage < 0:
				if config.debug:
					print("pause on back")
				changeRate(1.0, 4.0)
				startPause(random.uniform(2.0, 8.0))
			else:
				changeRate()
			# don't need to multiply the prob by the calibrated cycle rate as it "inherits" probablity
			# from above
			if random.random() < config.goBackwardsProb and config.hasGoneBack == False:
				# config.percentageIncrement = -(1 + 2 * random.random()) * config.calibratedCycleRate
				if config.debug:
					print("Going back")
				changeRate(1.0, 2.0)
				config.percentageIncrement *= -1
				config.hasGoneBack = True
				config.messageOverrideActive = True

		if random.random() < config.noDoneProb * config.calibratedCycleRate:
			if config.debug:
				print("Done Early")
			config.altStringMessage = "RESTARTING"
			config.completed = True
			startPause(random.uniform(5.0, 5.0))

		elif config.completed == True:
			if config.debug:
				print("Completed")
			done()


def checkPause():
	if config.paused:
		config.pauseTime2 = time.time()
		tD = config.pauseTime2 - config.pauseTime1

		if random.random() > 0.01:
			config.messageOverrideActive = True
		else:
			config.messageOverrideActive = False

		config.messageOverrideActive = True

		# if(config.completed and random.random() < 0) :
		#     config.messageOverrideActive = False

		if tD >= config.timeToPause:
			if config.completed == True:
				done()
			else:
				config.paused = False
				config.hasPaused = True
				# sometimes even the mesaging breaks..
				# if(random.random() > .1) : config.messageOverrideActive = False
				# generally crawls out....
				changeRate(0.01, 0.03)


def startPause(timeToPause):
	if (config.pauseCount < config.pauses and config.paused == False) or (
		config.completed == True
	):
		if config.debug and config.completed == True:
			print(
				"pausing... for:",
				timeToPause,
				config.pauseCount,
				"- out of -- ",
				config.pauses,
			)
		if config.completed != True:
			config.pauseCount += 1
			if config.debug:
				print(
					"pausing... for:",
					timeToPause,
					config.pauseCount,
					"- out of -- ",
					config.pauses,
				)
		config.paused = True
		config.timeToPause = timeToPause
		config.pauseTime1 = time.time()
		config.pauseTime2 = time.time()


#####################################################


def doSomething():
	global config
	advanceBar()


def changeRate(a=0.05, b=1.0):
	global config
	temp = config.percentageIncrement
	config.percentageIncrement = (a + b * random.random()) * config.calibratedCycleRate
	if config.debug:
		print(
			"RATE changed from: ",
			temp,
			" to: ",
			config.percentageIncrement,
			config.target,
		)


def advanceBar():
	global config
	if config.paused != True:
		config.percentage += config.percentageIncrement
		# make sure the % progress shows back up
		if random.random() > 0.94:
			config.messageOverrideActive = False

	if config.percentage <= 1:
		config.messageClr = (255, 0, 0)

	if config.percentage > 2:
		config.messageClr = config.messageClrBase

	if config.percentage >= config.target:
		config.messageClr = (255, 100, 0)

	if random.random() < config.noBarProb * config.calibratedCycleRate:
		config.drawBarFill = False


#####################################################


def calibration():
	"""
	Basic calibration  -- test the speed to try and run 10 percentage points / second with 
	the set delay time per cycle. Find the actual time to complete and set the "processor" 
	factor - i.e. if there were no delays running each cycle then it would be 1. If it's slow
	it will be > 1.

	"""
	global config
	config.percentage += config.percentageIncrement
	config.cycleCount += 1
	if config.percentage >= 100:
		config.t2 = time.time()
		timeToComplete = config.t2 - config.t1
		##########
		timeItShouldHaveTaken = 100 / config.calibrationTest
		config.processorFactor = timeToComplete / timeItShouldHaveTaken
		config.calibratedCycleRate = config.redrawRate * config.processorFactor

		config.percentageIncrement = (
			config.calibrationTest / 10 * config.calibratedCycleRate
		)
		if config.debug:
			print(
				"\n=====>  ",
				timeToComplete,
				timeItShouldHaveTaken,
				config.cycleCount,
				"Processor factor:",
				config.processorFactor,
				"\n",
			)
		config.cycleCount = 0
		config.t1 = time.time()
		config.t2 = time.time()
		config.percentage = 0
		config.firstRun = False
		done()

		# if(config.debug ) : print(config.overrideMessagProb * config.calibratedCycleRate)
		# exit()


def runWork():
	global config
	while True:
		iterate()
		time.sleep(config.redrawRate)


def iterate():
	global config

	if config.firstRun == True:
		calibration()
	else:
		doSomething()

	# Are we waiting?
	checkPause()

	# Do we go on, do we make changes?
	decisions()

	# Display bar, spinner, message or %
	reDraw()

	if random.random() < config.filterRemappingProb:
		if config.useFilters == True and config.filterRemapping == True:
			config.filterRemap = True
			startX = round(random.uniform(0,config.filterRemapRangeX) )
			startY = round(random.uniform(0,config.filterRemapRangeY) )
			endX = round(random.uniform(8, config.filterRemapminHoriSize) )
			endY = round(random.uniform(8, config.filterRemapminVertSize) )
			config.remapImageBlockSection = [startX,startY,startX + endX, startY + endY]
			config.remapImageBlockDestination = [startX,startY]
			#print("swapping" + str(config.remapImageBlockSection))

	# Do the final rendering of the composited image
	config.render(config.image, 0, 0, config.screenWidth, config.screenHeight)

	# Just in case
	callBack()


def main(run=True):
	global config

	config.debug = workConfig.getboolean("progressbar", "debug")

	config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
	config.draw = ImageDraw.Draw(config.image)
	config.fontSize = int(workConfig.get("progressbar", "fontSize"))
	config.vOffset = int(workConfig.get("progressbar", "vOffset"))
	config.steps = int(workConfig.get("progressbar", "steps"))
	config.redrawRate = float(workConfig.get("progressbar", "redrawRate"))

	# config.rateMultiplier = float(workConfig.get("progressbar", 'rateMultiplier'))
	config.shadowSize = int(workConfig.get("progressbar", "shadowSize"))
	config.sansSerif = workConfig.getboolean("progressbar", "sansSerif")

	config.useVerticalColorGradient = workConfig.getboolean(
		"progressbar", "useVerticalColorGradient"
	)
	config.useHorizontalColorGradient = workConfig.getboolean(
		"progressbar", "useHorizontalColorGradient"
	)
	config.boxMax = config.screenWidth - 2
	config.boxMaxAlt = config.boxMax + int(random.uniform(10, 30) * config.screenWidth)
	config.boxHeight = config.canvasHeight - 3
	config.pausePoint = int(random.random() * 100)
	config.cyclicalArc = 4 * math.pi / config.boxMax
	config.cyclicalBrightnessPhase = 0
	config.spinnerCenter = [config.boxMax - 54, config.canvasHeight / 2 + 1]

	config.pauseProbability = (
		float(workConfig.get("progressbar", "pauseProbability")) / 100
	)
	config.goBackwardsProb = (
		float(workConfig.get("progressbar", "goBackwardsProb")) / 100
	)
	config.changeRateProbability = (
		float(workConfig.get("progressbar", "changeRateProbability")) / 100
	)
	config.goPastProb = float(workConfig.get("progressbar", "goPastProb")) / 100

	# chance that a message shows instead of %
	config.messageOverrideProbability = (
		float(workConfig.get("progressbar", "messageOverrideProbability")) / 100
	)
	# chance different message is shown, when shown
	config.overrideMessagProb = (
		float(workConfig.get("progressbar", "overrideMessagProb")) / 100
	)
	config.noBarProb = float(workConfig.get("progressbar", "noBarProb")) / 100
	config.noDoneProb = float(workConfig.get("progressbar", "noDoneProb")) / 100

	try:
		config.filterRemapping = (workConfig.getboolean("progressbar", "filterRemapping"))
		config.filterRemappingProb = float(workConfig.get("progressbar", "filterRemappingProb"))
		config.filterRemapminHoriSize = int(workConfig.get("progressbar", "filterRemapminHoriSize"))
		config.filterRemapminVertSize = int(workConfig.get("progressbar", "filterRemapminVertSize"))
	except Exception as e:
		print(str(e))
		config.filterRemapping = False
		config.filterRemappingProb = 0.0
		config.filterRemapminHoriSize = 24
		config.filterRemapminVertSize = 24

	try:
		config.filterRemapRangeX = int(workConfig.get("progressbar", "filterRemapRangeX"))
		config.filterRemapRangeY = int(workConfig.get("progressbar", "filterRemapRangeY"))
	except Exception as e:
		print(str(e))
		config.filterRemapRangeX = config.canvasWidth
		config.filterRemapRangeY = config.canvasHeight

	init()

	config.processorFactor = 1

	if config.firstRun:
		config.percentageIncrement = (
			config.calibrationTest * config.redrawRate * config.processorFactor
		)
		config.cycleCount = 0
		config.t1 = time.time()
		config.t2 = time.time()
		if config.debug:
			print("=====>  ", config.percentageIncrement)
		config.messageString = "CALIBRATING"

	if run:
		runWork()


def init():
	global config
	if config.debug:
		print("init Progress Bar")

	config.outlineColor = (1, 1, 1)
	config.barColorEnd = (200, 200, 0)
	config.barColorStart = (0, 200, 200)
	config.barColor = (10, 10, 100)
	config.barColorBase = (200, 0, 0)
	config.holderColor = (0, 0, 0)
	config.messageClr = (200, 0, 0)
	config.messageClrBase = (51, 196, 127)
	config.shadowColor = (0, 0, 0)

	config.spinnerAngle = 0
	config.spinnerAngleSteps = 16
	config.spinnerRadius = 9
	config.spinnerInnerRadius = 7

	config.altStringMessage = "PLEASE WAIT"
	colorutils.brightness = 1
	config.gradientLevel = 1

	config.xPos = 1
	config.yPos = 1
	config.status = 0

	config.percentage = 0
	config.target = 99

	config.minSleep = 10
	config.maxSleep = 12

	config.pauses = 3
	config.pauseCount = 0
	config.firstRun = True
	config.completed = False
	config.paused = False
	config.hasPaused = False
	config.pausePoint = 10
	config.goBack = True
	config.hasGoneBack = False
	config.goPast = False
	config.drawBarFill = True
	config.messageOverride = True
	config.messageOverrideActive = False
	config.lastPause = False

	config.calibrationTest = 50

	if config.sansSerif:
		config.font = ImageFont.truetype(
			config.path + "/assets/fonts/freefont/FreeSansBold.ttf", config.fontSize
		)
	else:
		config.font = ImageFont.truetype(
			config.path + "/assets/fonts/freefont/FreeSerifBold.ttf", config.fontSize
		)

	config.messageString = config.altStringMessage
	tempImage = Image.new("RGBA", (1200, 196))
	draw = ImageDraw.Draw(tempImage)
	config.pixLen = draw.textsize(config.messageString, font=config.font)
	# For some reason textsize is not getting full height !
	config.fontHeight = int(config.pixLen[1] * 1.3)
	scrollImage = Image.new("RGBA", (config.pixLen[0] + 2, config.fontHeight))
	config.txtdraw = ImageDraw.Draw(scrollImage)


def done():
	global config

	if config.debug:
		print("Done called.\n")
	config.messageOverrideActive = False
	config.altStringMessage = "PLEASE WAIT"

	if random.random() < config.overrideMessagProb:
		config.altStringMessage = (
			"RESTARTING..." if (random.random() > 0.5) else "UPDATING"
		)
	if config.debug:
		print(config.altStringMessage)

	config.percentage = 0
	# config.barColorStart = config.barColor = colorutils.getRandomRGB(1)
	config.barColorStart = config.barColor = colorutils.randomColor(0.75)
	config.hasPaused = False
	config.paused == False
	config.pauseCount = 0
	config.boxWidth = 1
	config.completed = False
	config.drawBarFill = True
	config.target = random.uniform(95, 99)

	config.goBack = True if (random.random() < config.goBackwardsProb) else False
	config.goPast = True if (random.random() < config.goPastProb) else False
	config.hasGoneBack = False
	if config.goPast:
		config.goBack = False
	config.pausePoint = int(random.random() * 100)
	changeRate()


def callBack():
	global config
	pass
