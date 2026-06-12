import math
import random
import threading
import time
from modules.configuration import bcolors, pieceLogger
from modules import colorutils
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps
from modules.holder_director import Holder
from modules.holder_director import Director

"""
config.percentage will be the global config variable for display of progress

"""


class Holder:
    def __init__(self, config):
        self.config = config


# ----------------------------------------------------##----------------------------------------------------#
class Director:
    """docstring for Director"""

    animaRate = 0.5

    def __init__(self, config):
        super(Director, self).__init__()
        self.config = config
        self.tT = time.time()

    def checkTime(self):
        if (time.time() - self.tT) >= self.animaRate:
            self.tT = time.time()
            self.advance = True
        else:
            self.advance = False

    def next(self):
        self.checkTime()


def reDraw():

    """""" """""" """""" """ BOX AND BAR """ """""" """""" """""" """""" """"""
    drawBar()

    """""" """""" """""" """ TEXT MESSAGE """ """""" """""" """""" """"""
    drawMessageText()

    """""" """""" """""" """ SPINNER """ """""" """""" """""" """""" """"""
    if config.paused == True or config.percentage <= 1:
        drawSpinner()


def drawMessageText():
    global config

    # Set the message to be the % completed
    config.displayPercentage = int(math.floor(config.percentage))
    pre = ""
    if config.displayPercentage > 0 and config.displayPercentage <= 9:
        pre = ""
    if config.messageOverrideActive != True and config.firstRun != True:
        config.messageString = f"{pre}{config.displayPercentage}%"

    if config.messageOverrideActive == True:
        config.messageString = f"{pre}{config.displayPercentage}% {config.altStringMessage}"

    # Draw the message percentage
    indent = config.indent
    yindent = config.yindent
    scrollImage = Image.new("RGBA", (config.pixLen[0] + 2 * indent, config.fontHeight + 2 * indent))
    txtdraw = ImageDraw.Draw(scrollImage)
    txtdraw = config.draw
    messageString = config.messageString
    font = config.font
    shadowColor = config.shadowColor

    for i in range(1, config.shadowSize):
        txtdraw.text((indent - i, yindent - i), text=messageString, fill=shadowColor, font=font)
        txtdraw.text((indent - i, yindent), text=messageString, fill=shadowColor, font=font)
        txtdraw.text((indent - i, yindent + i), text=messageString, fill=shadowColor, font=font)
        txtdraw.text((indent + 0, yindent - i), text=messageString, fill=shadowColor, font=font)
        txtdraw.text((indent + 0, yindent), text=messageString, fill=shadowColor, font=font)
        txtdraw.text((indent + 0, yindent + i), text=messageString, fill=shadowColor, font=font)
        txtdraw.text((indent + i, yindent - i), text=messageString, fill=shadowColor, font=font)
        txtdraw.text((indent + i, yindent), text=messageString, fill=shadowColor, font=font)
        txtdraw.text((indent + i, yindent + i), text=messageString, fill=shadowColor, font=font)

    # Draw a box around message display
    # numXPos = int(xPos2 - 40)
    config.draw.text((indent, yindent), fill=config.messageClr, text=messageString, font=font)

    config.pixLen = [1200, 100]
    if messageString != config.altStringMessage:
        numXPos = config.boxMax - config.pixLen[0] - 8
    else:
        numXPos = config.boxMax - config.pixLen[0] - 8
    # numXPos = 32
    numYPos = int(config.spinnerCenter[1] - config.fontHeight / 2)
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

    config.spinnerCenter = [int(config.canvasWidth - 4 * config.spinnerRadius), int(config.boxHeight / 2)]

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
        if s % config.spinnerMarkSteps == 0:
            config.draw.line((sX0, sY0, sX, sY), fill=fillColor, width=config.spinnerLineWidth)


def drawBar():
    global config

    # Unless overridden, boxWidth is ~ to percentage
    if config.drawBarFill:
        config.boxWidth = round(config.percentage / 100 * config.boxMax)

    # draw box container

    rVd = round(config.barColor[0] * 0.1)
    gVd = round(config.barColor[1] * 0.1)
    bVd = round(config.barColor[2] * 0.1)

    config.draw.rectangle(
        (
            config.xPos - 1,
            config.yPos - 1,
            config.boxMax + 1,
            config.boxHeight + config.yPos + 1,
        ),
        outline=(config.outlineColor),
        fill=((rVd, gVd, bVd)),
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
    # config.draw.rectangle(
    #     (config.xPos1, config.yPos1, max(config.xPos1, config.xPos2), max(config.yPos2, config.yPos1)), fill=(config.barColor[0], config.barColor[1], config.barColor[2])
    # )

    lines = config.boxHeight
    if config.gradientLevel == 1:
        arc = math.pi / lines * 1
    else:
        arc = math.pi / lines

    if config.useVerticalColorGradient:
        # Draw vertical shading gradient
        for n in range(0, lines):
            yPos = config.yPos1 + n
            b = math.sin(arc * n) * config.brightness + 0.3
            # b = cyclicalBrightness
            # if b < .75 : b = .75
            rVd = round(config.barColor[0] * b)
            gVd = round(config.barColor[1] * b)
            bVd = round(config.barColor[2] * b)
            barColorDisplay = (rVd, gVd, bVd)
            config.draw.rectangle((config.xPos1, yPos, max(config.xPos2, config.xPos1), yPos), fill=(barColorDisplay))

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
def changeAltMessage():
    if random.random() < config.overrideMessagProb:
        msgIndex = random.choice(config.messageStrings)
        config.altStringMessage = msgIndex


def decisions():
    global config

    # if random.random() > 0.94:
    #     config.messageOverrideActive = False

    if config.percentage <= 1:
        config.messageClr = (255, 0, 0, 100)

    if config.percentage > 2:
        config.messageClr = config.messageClrBase

    if config.percentage >= config.target:
        config.messageClr = (255, 10, 0, 100)

    if config.percentage >= config.pausePoint:
        config.messageClr = (255, 100, 0, 100)

    if random.random() < config.noBarProb * config.processorFactor:
        config.drawBarFill = False
        pieceLogger("No bar fill called")

    if config.percentage >= config.target and not config.completed and not config.goPast and not config.hasGoneBack:
        # config.completed = True
        pieceLogger(f"Completed progress as far as {config.target} completed: {config.completed}")
        config.percentageIncrement *= -2
        config.hasGoneBack = True
        config.messageOverrideActive = True
        config.negativePercentageDone = 0
        startPause(random.uniform(2, 7))

    if config.goPast:
        if config.percentage > 150:
            if random.random() < 0.01:
                config.completed = True
                pieceLogger("Completed beyond ")

        if config.percentage < 100 and config.percentage > 50:
            if random.random() < 0.1:
                changeRate()

    # to catch the negative
    if config.percentage <= config.negativePercentageDone and config.percentageIncrement < 0:
        config.complete = True
        pieceLogger("Completed")
        config.messageOverrideActive = True
        startPause(random.uniform(2, 7))
        done()

    # to catch the overage
    if config.percentage > 107 and config.percentageIncrement > 0:
        config.complete = True
        pieceLogger("Completed")
        config.messageOverrideActive = True
        startPause(random.uniform(2, 7))
        done()

    if not config.paused and config.percentage >= config.pausePoint:

        if random.random() < (config.pauseProbability * config.calibratedCycleRate):
            pieceLogger("pause called")
            startPause(random.uniform(2, 7))
            if random.random() > 0.5:
                config.messageOverrideActive = True
            else:
                config.messageOverrideActive = False

        # config.messageOverrideActive = True
        # config.completed = True

        if random.random() < config.changeRateProbability * config.calibratedCycleRate:
            # sometimes even the messaging breaks..
            # if(random.random() > .1) : config.messageOverrideActive = False
            # generally crawls out....
            pieceLogger("Slow rate")
            changeRate(0.01, 0.03)

        if random.random() < config.changeRateProbability * config.calibratedCycleRate:
            if config.percentage < 0:
                pieceLogger("pause on back")
                if config.percentage <= config.negativePercentageDone:
                    done()
                changeRate()
                startPause(random.uniform(2, 7))
            else:
                changeRate()

        if random.random() < config.goBackwardsProb * config.calibratedCycleRate and not config.hasGoneBack:
            # config.percentageIncrement = -(1 + 2 * random.random()) * config.calibratedCycleRate
            pieceLogger("Going back")
            changeRate()
            config.percentageIncrement *= -1
            config.hasGoneBack = True
            if random.random() > 0.5:
                config.messageOverrideActive = True
            else:
                config.messageOverrideActive = False

        if random.random() < config.noDoneProb * config.calibratedCycleRate:
            pieceLogger("Done Early")
            config.altStringMessage = "PAUSING"
            config.completed = False
            config.percentageIncrement *= -1
            config.hasGoneBack = True
            startPause(random.uniform(2, 7))

        elif config.completed:
            pieceLogger("Completed")
            done()


def checkPause():
    if config.paused:
        config.pauseTime2 = time.time()
        tD = config.pauseTime2 - config.pauseTime1

        if tD >= config.timeToPause:
            config.paused = False
            config.hasPaused = True
            config.messageOverrideActive = False
            changeAltMessage()


def startPause(timeToPause):
    if (config.pauseCount < config.pauses and not config.paused) or (config.completed):
        if config.completed:
            config.pauseCount += 1
            pieceLogger(f"pausing... for: {timeToPause} {config.pauseCount} - out of -- {config.pauses}")
        config.paused = True
        config.timeToPause = timeToPause
        config.pauseTime1 = time.time()
        config.pauseTime2 = time.time()


#####################################################


def doSomething():
    global config
    advanceBar()


def changeRate(a=0, b=0):
    global config
    temp = config.percentageIncrement
    if a == b == 0:
        a = config.rateMin
        b = config.rateMax

    config.percentageIncrement = max(0.01, (random.uniform(a, b)) * config.processorFactor)
    pieceLogger(f"RATE changed from: {temp}  to: {config.percentageIncrement} {config.target}", 5)


def advanceBar():
    global config
    if not config.paused:
        config.percentage += config.percentageIncrement


def done():
    global config
    pieceLogger("Done called.\n")
    config.messageOverrideActive = False
    config.altStringMessage = "PLEASE WAIT"
    changeAltMessage()

    # if random.random() < 0.1:
    #     config.altStringMessage = "PLEASE WAIT - RECALCULATING."

    # if random.random() < 0.1:
    #     config.altStringMessage = "COMPLETE"

    # if random.random() < 0.1:
    #     config.altStringMessage = "COMPLETED."

    # if random.random() < config.overrideMessagProb:
    #     config.altStringMessage = "RESTARTING." if (random.random() > 0.5) else "UPDATING."

    pieceLogger(f"altStringMessage set to: {config.altStringMessage}", 2)

    config.percentage = 0
    # config.barColorStart = config.barColor = colorutils.getRandomRGB(1)
    # config.barColorStart = config.barColor = colorutils.randomColor(config.brightness)
    config.barColorStart = config.barColor = colorutils.getRandomColorHSV(0, 360, 0.5, 1.0, 0.5, 1.0)
    config.hasPaused = False
    config.paused == False
    config.pauseCount = 0
    config.boxWidth = 1
    config.completed = False
    config.drawBarFill = True

    config.goBack = True if (random.random() < config.goBackwardsProb) else False
    config.goPast = True if (random.random() < config.goPastProb) else False
    config.hasGoneBack = False
    if config.goPast:
        config.goBack = False

    config.negativePercentageDone = random.uniform(5, -99)
    config.target = random.uniform(89, 99)
    config.pausePoint = 20 + round(random.random() * 79)

    pieceLogger(
        f"config.pausePoint = {config.pausePoint} target = {config.target}",
    )

    changeRate()


#####################################################


def runWork():
    global config
    while True:
        time.sleep(config.cycleDelay)
        config.director.checkTime()
        if config.director.advance:
            iterate()


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
            startX = round(random.uniform(0, config.filterRemapRangeX))
            startY = round(random.uniform(0, config.filterRemapRangeY))
            endX = round(random.uniform(8, config.filterRemapminHoriSize))
            endY = round(random.uniform(8, config.filterRemapminVertSize))
            config.remapImageBlockSection = [startX, startY, startX + endX, startY + endY]
            config.remapImageBlockDestination = [startX, startY]
            # pieceLogger("swapping" + str(config.remapImageBlockSection))

    # Do the final rendering of the composited image
    config.render(config.image, 0, 0, config.screenWidth, config.screenHeight)

    # Just in case
    callBack()


def main(run=True):
    global config
    global workConfig
    config.debug = workConfig.getboolean("progressbar", "debug")

    config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
    config.draw = ImageDraw.Draw(config.image)
    config.fontSize = int(workConfig.get("progressbar", "fontSize"))
    config.indent = int(workConfig.get("progressbar", "indent", fallback=0))
    config.yindent = int(workConfig.get("progressbar", "yindent", fallback=0))
    config.vOffset = int(workConfig.get("progressbar", "vOffset"))
    config.steps = int(workConfig.get("progressbar", "steps"))

    config.rateMin = float(workConfig.get("progressbar", "rateMin"))
    config.rateMax = float(workConfig.get("progressbar", "rateMax"))

    # config.rateMultiplier = float(workConfig.get("progressbar", 'rateMultiplier'))
    config.shadowSize = int(workConfig.get("progressbar", "shadowSize"))
    config.sansSerif = workConfig.getboolean("progressbar", "sansSerif")

    config.useVerticalColorGradient = workConfig.getboolean("progressbar", "useVerticalColorGradient")
    config.useHorizontalColorGradient = workConfig.getboolean("progressbar", "useHorizontalColorGradient")
    config.boxMax = config.screenWidth - 2
    config.boxMaxAlt = config.boxMax + int(random.uniform(10, 30) * config.screenWidth)
    # config.boxHeight = config.canvasHeight - 3
    config.boxHeight = int(workConfig.get("progressbar", "progressbarHeight", fallback=(config.canvasHeight - 3)))
    config.pausePoint = round(random.random() * 99)
    config.cyclicalArc = 4 * math.pi / config.boxMax
    config.cyclicalBrightnessPhase = 0

    config.pauseProbability = float(workConfig.get("progressbar", "pauseProbability"))
    config.goBackwardsProb = float(workConfig.get("progressbar", "goBackwardsProb"))
    config.changeRateProbability = float(workConfig.get("progressbar", "changeRateProbability"))
    config.goPastProb = float(workConfig.get("progressbar", "goPastProb"))

    # chance that a message shows instead of %
    config.messageOverrideProbability = float(workConfig.get("progressbar", "messageOverrideProbability"))
    # chance different message is shown, when shown
    config.overrideMessagProb = float(workConfig.get("progressbar", "overrideMessagProb"))
    config.noBarProb = float(workConfig.get("progressbar", "noBarProb"))
    config.noDoneProb = float(workConfig.get("progressbar", "noDoneProb"))

    config.spinnerAngleSteps = int(workConfig.get("progressbar", "spinnerAngleSteps", fallback=16))
    config.spinnerRadius = int(workConfig.get("progressbar", "spinnerRadius", fallback=12))
    config.spinnerInnerRadius = int(workConfig.get("progressbar", "spinnerInnerRadius", fallback=8))
    config.spinnerLineWidth = int(workConfig.get("progressbar", "spinnerLineWidth", fallback=1))
    config.spinnerMarkSteps = int(workConfig.get("progressbar", "spinnerMarkSteps", fallback=2))

    config.spinnerCenter = [config.boxMax - 54, config.boxHeight / 2 + 1]
    try:
        config.filterRemapping = workConfig.getboolean("progressbar", "filterRemapping")
        config.filterRemappingProb = float(workConfig.get("progressbar", "filterRemappingProb"))
        config.filterRemapminHoriSize = int(workConfig.get("progressbar", "filterRemapminHoriSize"))
        config.filterRemapminVertSize = int(workConfig.get("progressbar", "filterRemapminVertSize"))
    except Exception as e:
        pieceLogger(str(e))
        config.filterRemapping = False
        config.filterRemappingProb = 0.0
        config.filterRemapminHoriSize = 24
        config.filterRemapminVertSize = 24

    try:
        config.filterRemapRangeX = int(workConfig.get("progressbar", "filterRemapRangeX"))
        config.filterRemapRangeY = int(workConfig.get("progressbar", "filterRemapRangeY"))
    except Exception as e:
        pieceLogger(str(e))
        config.filterRemapRangeX = config.canvasWidth
        config.filterRemapRangeY = config.canvasHeight

    config.outlineColor = (1, 1, 1)
    config.barColorEnd = (200, 200, 0)
    config.barColorStart = (0, 200, 200)
    config.barColor = (10, 10, 100)
    config.barColorBase = (200, 0, 0)
    config.holderColor = (0, 0, 0)
    config.messageClr = (255, 255, 255, 100)
    config.messageClrBase = (255, 255, 255, 100)
    config.shadowColor = (0, 0, 0, 100)

    config.spinnerAngle = 0
    config.messageStrings = [
        "PLEASE WAIT",
        "PLEASE WAIT",
        "RECALCULATING.",
        "COMPLETE",
        "COMPLETED.",
        "RESTARTING",
        "RELOADING",
        "PAUSED",
        "UDATING",
        "LOAD WARNING",
        "ERROR 49",
    ]
    config.altStringMessage = "PLEASE WAIT"
    colorutils.brightness = 1
    config.gradientLevel = 1

    config.xPos = 1
    config.yPos = 1
    config.percentage = 0
    config.pauses = 3

    config.cycleDelay = float(workConfig.get("progressbar", "cycleDelay", fallback=0.01))
    config.animaRate = float(workConfig.get("progressbar", "animaRate", fallback=0.02))
    config.director = Director(config)
    config.director.animaRate = config.animaRate

    init()

    config.processorFactor = 1
    config.calibrationCyclesPerSecond = 1 / config.animaRate

    if config.firstRun:
        config.percentageIncrement = 1.0
        config.cycleCount = 0
        config.t1 = time.time()
        config.t2 = time.time()

        pieceLogger(f"=====>   {config.percentageIncrement} config.calibrationCyclesPerSecond : {config.calibrationCyclesPerSecond }")
        config.messageString = "CALIBRATING"

    if run:
        runWork()


def init():
    global config
    pieceLogger("init Progress Bar")

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
    config.negativePercentageDone = -3

    if config.sansSerif:
        config.font = ImageFont.truetype(config.path + "/assets/fonts/freefont/FreeSansBold.ttf", config.fontSize)
    else:
        config.font = ImageFont.truetype(config.path + "/assets/fonts/freefont/FreeSerifBold.ttf", config.fontSize)

    config.messageString = config.altStringMessage
    tempImage = Image.new("RGBA", (1200, 196))
    draw = ImageDraw.Draw(tempImage)
    # config.pixLen = draw.text((0,0),text=config.messageString, font=config.font)
    config.pixLen = [1200, 100]

    # For some reason textsize is not getting full height !
    config.fontHeight = int(config.pixLen[1] * 1.3)
    scrollImage = Image.new("RGBA", (config.pixLen[0] + 2, config.fontHeight))
    config.txtdraw = ImageDraw.Draw(scrollImage)


"""
Basic calibration  -- test the speed to try and run 20 percentage points / 2 seconds with
the set delay time per cycle. Find the actual time to complete and set the "processor"
factor - i.e. if there were no delays running each cycle then it would be 1. If it's slow
it will be > 1.

"""


def calibration():
    global config
    config.percentage += config.percentageIncrement
    config.cycleCount += 1
    # pieceLogger(f"{config.percentage} {config.calibrationCyclesPerSecond} {config.cycleDelay * config.calibrationCyclesPerSecond}")
    if config.percentage >= 100:
        config.t2 = time.time()
        timeToComplete = config.t2 - config.t1
        timeItShouldHaveTaken = (100 / config.percentageIncrement) * config.animaRate
        config.processorFactor = timeToComplete / timeItShouldHaveTaken
        config.calibratedCycleRate = config.cycleDelay * config.processorFactor

        # config.calibratedCycleRate = 1.0
        # config.percentageIncrement = config.calibrationCyclesPerSecond / 10 * config.calibratedCycleRate

        pieceLogger(f"\n=====>  timeToComplete:{timeToComplete} timeItShouldHaveTaken:{timeItShouldHaveTaken}")
        pieceLogger(f"=====>  cycleCount:{config.cycleCount} Processor factor:{config.processorFactor}\n")
        config.cycleCount = 0
        config.t1 = time.time()
        config.t2 = time.time()
        config.percentage = 0
        config.firstRun = False
        done()

        # if(config.debug ) : pieceLogger(config.overrideMessagProb * config.calibratedCycleRate)
        # exit()


def callBack():
    global config
    pass
