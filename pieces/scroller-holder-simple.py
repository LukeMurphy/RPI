#!/usr/bin/python
# import modules
# ################################################### #
import datetime
import getopt
import math
import os
import random
import sys
import textwrap
import time
from collections import OrderedDict
from modules.configuration import bcolors
from modules import coloroverlay, colorutils, continuous_scroller,  panelDrawing

from modules.faderclass import FaderObj
from PIL import (
    Image,
    ImageChops,
    ImageDraw,
    ImageEnhance,
    ImageFilter,
    ImageFont,
    ImageOps,
    ImagePalette,
)

global config


class ScrollerManager:
    def __init__(self, config):
        self.config = config

    def setUp(self, workConfig):
        config = self.config
        print("SINGLETON SCROLLER HOLDER INIT")

        config.redrawSpeed = float(workConfig.get("scroller", "redrawSpeed"))

        config.windowWidth = float(workConfig.get("displayconfig", "windowWidth"))
        config.windowHeight = float(workConfig.get("displayconfig", "windowHeight"))


        self.displayRows = int(workConfig.get("scroller", "displayRows"))
        self.displayCols = int(workConfig.get("scroller", "displayCols"))

        # ********* HARD CODING VALUES  ***********************
        try:
            self.patternHeight = int(workConfig.get("scroller", "patternHeight"))
        except Exception as e:
            print(str(e))
            self.patternHeight = config.canvasHeight
        self.bandHeight = int(round(self.patternHeight / self.displayRows))
        self.bgBackGroundColor = (0, 0, 0, 0)
        self.arrowBgBackGroundColor = (0, 0, 0, 200)

        config.canvasImage = Image.new(
            "RGBA", (config.canvasWidth * 10, config.canvasHeight)
        )
        config.canvasImageDraw = ImageDraw.Draw(config.canvasImage)

        config.imageLayer = Image.new(
            "RGBA", (config.canvasWidth * 10, config.canvasHeight)
        )
        config.imageLayerDraw = ImageDraw.Draw(config.canvasImage)

        config.workImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
        config.workImageDraw = ImageDraw.Draw(config.workImage)

        self.overallBlur = float(
            workConfig.get("scroller", "overallBlur", vars=0, fallback=0)
        )

        self.flip = False
        self.scrollArray = []

        ## Set up the scrolling layer

        try:
            self.backgroundColorChangeProb = float(workConfig.get("scroller", "backgroundColorChangeProb"))
        except Exception as e:
            print(str(e))
            self.backgroundColorChangeProb = .5

        try:
            self.patternRowChangeProb = float(workConfig.get("scroller", "patternRowChangeProb"))
        except Exception as e:
            print(str(e))
            self.patternRowChangeProb = .15

        try:
            self.patternColChangeProb = float(workConfig.get("scroller", "patternColChangeProb"))
        except Exception as e:
            print(str(e))
            self.patternColChangeProb = .15


        try:
            self.setPatternColor = workConfig.getboolean("scroller", "setPatternColor")
            self.setPatternEndColor = list(map(lambda x: int(x), workConfig.get("scroller", "setPatternEndColor").split(",")))
        except Exception as e:
            self.setPatternColor = False
            print(str(e))

        self.altDirectionScrolling = workConfig.getboolean(
            "scroller", "altDirectionScrolling"
        )
        self.alwaysRandomPatternColor = workConfig.getboolean(
            "scroller", "alwaysRandomPatternColor"
        )
        self.alwaysRandomPattern = workConfig.getboolean(
            "scroller", "alwaysRandomPattern"
        )

        self.maxPatternRows = int(workConfig.get("scroller", "maxPatternRows"))
        self.maxPatternCols = int(workConfig.get("scroller", "maxPatternCols"))
        self.minPatternRows = int(workConfig.get("scroller", "minPatternRows"))
        self.minPatternCols = int(workConfig.get("scroller", "minPatternCols"))
        self.maxDrawProb = float(workConfig.get("scroller", "maxDrawProb"))
        self.minDrawProb = float(workConfig.get("scroller", "minDrawProb"))


        self.fg_minHue = int(workConfig.get("scroller", "fg_minHue"))
        self.fg_maxHue = int(workConfig.get("scroller", "fg_maxHue"))
        self.fg_minSaturation = float(workConfig.get("scroller", "fg_minSaturation"))
        self.fg_maxSaturation = float(workConfig.get("scroller", "fg_maxSaturation"))
        self.fg_minValue = float(workConfig.get("scroller", "fg_minValue"))
        self.fg_maxValue = float(workConfig.get("scroller", "fg_maxValue"))


        self.bg_minHue = int(workConfig.get("scroller", "bg_minHue"))
        self.bg_maxHue = int(workConfig.get("scroller", "bg_maxHue"))
        self.bg_minSaturation = float(workConfig.get("scroller", "bg_minSaturation"))
        self.bg_maxSaturation = float(workConfig.get("scroller", "bg_maxSaturation"))
        self.bg_minValue = float(workConfig.get("scroller", "bg_minValue"))
        self.bg_maxValue = float(workConfig.get("scroller", "bg_maxValue"))


        try :
            self.addrndProb = float(workConfig.get("scroller","addrndProb"))
            self.addrnd_minHue = int(workConfig.get("scroller", "addrnd_minHue"))
            self.addrnd_maxHue = int(workConfig.get("scroller", "addrnd_maxHue"))
            self.addrnd_minSaturation = float(workConfig.get("scroller", "addrnd_minSaturation"))
            self.addrnd_maxSaturation = float(workConfig.get("scroller", "addrnd_maxSaturation"))
            self.addrnd_minValue = float(workConfig.get("scroller", "addrnd_minValue"))
            self.addrnd_maxValue = float(workConfig.get("scroller", "addrnd_maxValue"))
            self.addrnd_dropHueMaxValue = float(workConfig.get("scroller", "addrnd_dropHueMaxValue"))
            self.addrnd_dropHueMinValue = float(workConfig.get("scroller", "addrnd_dropHueMinValue"))
        except Exception as e:
            print(str(e))
            self.addrndProb = 0

        try:
            self.redGreenSwapProb = float(workConfig.get("scroller", "redGreenSwapProb"))
        except Exception as e:
            print(str(e))
            self.redGreenSwapProb = 0
        try:
            self.redBlueSwapProb = float(workConfig.get("scroller", "redBlueSwapProb"))
        except Exception as e:
            print(str(e))
            self.redBlueSwapProb = 0
        try:
            self.greenBlueSwapProb = float(workConfig.get("scroller", "greenBlueSwapProb"))
        except Exception as e:
            print(str(e))
            self.greenBlueSwapProb = 0

        try:
            self.bg_dropHueMinValue = float(workConfig.get("scroller", "bg_dropHueMinValue"))
            self.bg_dropHueMaxValue = float(workConfig.get("scroller", "bg_dropHueMaxValue"))
            self.fg_dropHueMinValue = float(workConfig.get("scroller", "fg_dropHueMinValue"))
            self.fg_dropHueMaxValue = float(workConfig.get("scroller", "fg_dropHueMaxValue"))
        except Exception as e:
            self.bg_dropHueMinValue = 0
            self.bg_dropHueMaxValue = 0
            self.fg_dropHueMinValue = 0
            self.fg_dropHueMaxValue = 0
            print(str(e))


        self._configureBackgroundScrolling(workConfig)


        try:
            self.useOverLayImage = workConfig.getboolean("scroller", "useOverLayImage")
            if self.useOverLayImage == True:
                configureImageOverlay()
        except Exception as e:
            self.useOverLayImage = False
            print(str(e))


        try:
            self.useUltraSlowSpeed = workConfig.getboolean(
                "scroller", "useUltraSlowSpeed"
            )
        except Exception as e:
            self.useUltraSlowSpeed = False
            print(str(e))



        try:
            self.doingRefreshCount = float(
                workConfig.get("scroller", "doingRefreshCount")
            )
        except Exception as e:
            self.doingRefreshCount = 50
            print(str(e))


        self.useBend = False
        config.directorController = Director(config)
        config.directorController.slotRate = .03


        ### THIS IS USED AS WAY TO MOCKUP A CONFIGURATION OF RECTANGULAR PANELS
        panelDrawing.mockupBlock(config, workConfig)
        '''
            ########### Need to add something like this at final render call  as well

            ########### RENDERING AS A MOCKUP OR AS REAL ###########
            if config.useDrawingPoints == True :
                config.panelDrawing.canvasToUse = config.renderImageFull
                config.panelDrawing.render()
            else :
                #config.render(config.canvasImage, 0, 0, config.canvasWidth, config.canvasHeight)
                #config.render(config.image, 0, 0)
                config.render(config.renderImageFull, 0, 0)
        '''



        self.f = FaderObj()
        self.f.setUp(config.renderImageFull, config.workImage)
        self.f.doingRefreshCount = self.doingRefreshCount
        # config.workImageDraw.rectangle((0,0,100,100), fill=(100,0,0,100))
        self.renderImageFullOld = config.renderImageFull.copy()
        self.fadingDone = True

        self.useFadeThruAnimation = True
        self.deltaTimeDone = True

    def _configureBackgroundScrolling(self, workConfig):
        config = self.config
        print("configureBackgroundScrolling")
        self.patternRows = int(workConfig.get("scroller", "patternRows"))
        self.patternCols = int(workConfig.get("scroller", "patternCols"))

        self.patternDrawProb = float(workConfig.get("scroller", "patternDrawProb"))
        self.patternSpeed = float(workConfig.get("scroller", "patternSpeed"))
        self.pattern = workConfig.get("scroller", "pattern")
        self.initialPattern  = workConfig.get("scroller", "pattern")
        self.choiceArray = ["lines","pluses","regularLines","regularLines"]


        self.bgBackGroundColor = colorutils.getRandomColorHSVSaturated(
                self.bg_minHue, self.bg_maxHue,
                self.bg_minSaturation, self.bg_maxSaturation,
                self.bg_minValue, self.bg_maxValue,
                self.bg_dropHueMinValue, self.bg_dropHueMaxValue, 255, config.brightness)

        self.bgBackGroundEndColor = colorutils.getRandomColorHSVSaturated(
                self.bg_minHue, self.bg_maxHue,
                self.bg_minSaturation, self.bg_maxSaturation,
                self.bg_minValue, self.bg_maxValue,
                self.bg_dropHueMinValue, self.bg_dropHueMaxValue, 255, config.brightness)

        self.patternColor = colorutils.getRandomColorHSVSaturated(
                self.fg_minHue, self.fg_maxHue,
                self.fg_minSaturation, self.fg_maxSaturation,
                self.fg_minValue, self.fg_maxValue,0,0,255,config.brightness)

        self.patternEndColor = colorutils.getRandomColorHSVSaturated(
                self.fg_minHue, self.fg_maxHue,
                self.fg_minSaturation, self.fg_maxSaturation,
                self.fg_minValue, self.fg_maxValue,
                self.fg_dropHueMinValue, self.fg_dropHueMaxValue, 255, config.brightness)


        self.currentPatternLength = 0

        self.scroller4 = continuous_scroller.ScrollObject()
        scrollerRef = self.scroller4
        scrollerRef.typeOfScroller = "bg"
        scrollerRef.canvasWidth = int(self.displayRows * config.canvasWidth)
        scrollerRef.xSpeed = self.patternSpeed
        scrollerRef.setUp()
        direction = 1 if scrollerRef.xSpeed > 0 else -1
        scrollerRef.callBack = {"func": remakePatternBlock, "direction": direction}


        try:
            self.maxSpeed = float(workConfig.get("scroller", "maxSpeed"))
        except Exception as e:
            self.maxSpeed = self.patternSpeed

        scrollerRef.xMaxSpeed = self.maxSpeed

        try:
            self.changeProb = float(workConfig.get("scroller", "changeProb"))
        except Exception as e:
            self.changeProb = 0.0
            print(str(e))

        try:
            self.changeProbReleaseFactor = float(workConfig.get("scroller", "changeProbReleaseFactor"))
        except Exception as e:
            self.changeProbReleaseFactor = 1.0
            print(str(e))


        makeBackGround(scrollerRef.bg1Draw, 1)
        makeBackGround(scrollerRef.bg2Draw, 1)


        self.t1 = time.time()
        self.t2 = time.time()
        self.timeToComplete = 1
        self.scrollerPauseBool = False

        self.scrollArray.append(scrollerRef)



class Director:
    """docstring for Director"""

    slotRate = .5

    def __init__(self, config):
        super(Director, self).__init__()
        self.config = config
        self.tT = time.time()


    def checkTime(self):
        if (time.time() - self.tT) >= self.slotRate :
            self.tT = time.time()
            self.advance = True
        else :
            self.advance = False


    def next(self):

        self.checkTime()


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""


def makeBackGround(drawRef, n=1):
    rows = scrllrMngr.patternRows * 1
    cols = scrllrMngr.patternCols * 1

    xDiv = round(
        (scrllrMngr.displayRows * config.canvasWidth) / cols
    )

    xDiv = (
        2 * config.canvasWidth * scrllrMngr.displayCols/ cols
    )

    yDiv = (
        scrllrMngr.patternHeight / rows
    ) / scrllrMngr.displayRows


    gap = 0
    steps = cols
    scrllrMngr.arrowBgBackGroundColor = (0, 0, 0, 20)  # colorutils.getRandomColor()
    colorChange = False

    # Background setup
    '''
    '''
    drawRef.rectangle(
        (0, 0, (round(scrllrMngr.displayRows * config.canvasWidth)), config.canvasHeight),
        fill=scrllrMngr.bgBackGroundColor)

    ## The multiplier is actually a factor of the number of rows
    ## but, generally so far only using two rows ....
    rDelta = ((scrllrMngr.bgBackGroundEndColor[0] - scrllrMngr.bgBackGroundColor[0]) / steps)
    gDelta = ((scrllrMngr.bgBackGroundEndColor[1] - scrllrMngr.bgBackGroundColor[1]) / steps)
    bDelta = ((scrllrMngr.bgBackGroundEndColor[2] - scrllrMngr.bgBackGroundColor[2]) / steps)

    xPos = 0
    transitionCount = 0
    scrllrMngr.patternLengthTransition = 8
    lengthDelta = round((xDiv - scrllrMngr.currentPatternLength ) / scrllrMngr.patternLengthTransition)
    patternLength = xDiv

    for c in range(0, cols):
        columnOffset = 0

        rCol = scrllrMngr.bgBackGroundColor[0] + rDelta
        gCol = scrllrMngr.bgBackGroundColor[1] + gDelta
        bCol = scrllrMngr.bgBackGroundColor[2] + bDelta
        scrllrMngr.bgBackGroundColor = (rCol, gCol, bCol)

        ### Because the way the pattern draws the left end is actually the end color
        ### so need to reverse the color gradient ....

        fillClr = (
            (round(scrllrMngr.bgBackGroundEndColor[0] - rDelta * (c + 1))),
            (round(scrllrMngr.bgBackGroundEndColor[1] - gDelta * (c + 1))),
            (round(scrllrMngr.bgBackGroundEndColor[2] - bDelta * (c + 1))),
            200,
        )

        w = patternLength

        outline = None
        if c < 0 :
            outline=(255,0,0,200)

        drawRef.rectangle((xPos,0,xPos+w,config.canvasHeight), fill = fillClr, outline=outline)
        xPos += w

        if transitionCount < scrllrMngr.patternLengthTransition-1 :
            #print(scrllrMngr.currentPatternLength,xDiv,lengthDelta)
            transitionCount += 1
            #patternLength += lengthDelta
        else :
            patternLength = xDiv


    scrllrMngr.bgBackGroundColor = scrllrMngr.bgBackGroundEndColor

    # Foreground setup

    rowMultiplier = 1
    colMultiplier = 1

    if scrllrMngr.pattern == "bricks":
        rowMultiplier = 1
        colMultiplier = 1

    if scrllrMngr.pattern == "regularLines":
        rowMultiplier = 2
        colMultiplier = 1

    if scrllrMngr.pattern == "pluses":
        rowMultiplier = 2
        colMultiplier = 1

    if scrllrMngr.pattern == "diamonds":
        rowMultiplier = 2
        colMultiplier = 2


    ## The multiplier is actually a factor of the number of rows
    ## but, generally so far only using two rows ....
    rDelta = ((scrllrMngr.patternEndColor[0] - scrllrMngr.patternColor[0]) / steps)
    gDelta = ((scrllrMngr.patternEndColor[1] - scrllrMngr.patternColor[1]) / steps)
    bDelta = ((scrllrMngr.patternEndColor[2] - scrllrMngr.patternColor[2]) / steps)

    xPos = 0
    xStart = 0
    yStart = 0
    transitionCount = 0
    scrllrMngr.patternLengthTransition = 8
    lengthDelta = round((xDiv - scrllrMngr.currentPatternLength ) / scrllrMngr.patternLengthTransition)


    for c in range(0, cols+1):

        columnOffset = 0

        rCol = scrllrMngr.patternColor[0] + rDelta
        gCol = scrllrMngr.patternColor[1] + gDelta
        bCol = scrllrMngr.patternColor[2] + bDelta
        scrllrMngr.patternColor = (rCol, gCol, bCol)

        ### Because the way the pattern draws the left end is actually the end color
        ### so need to reverse the color gradient ....

        fillClr = (
            (round(scrllrMngr.patternEndColor[0] - rDelta * (c + 1))),
            (round(scrllrMngr.patternEndColor[1] - gDelta * (c + 1))),
            (round(scrllrMngr.patternEndColor[2] - bDelta * (c + 1))),
            225,
        )

        if random.random() < scrllrMngr.addrndProb:

            fillClr = colorutils.getRandomColorHSVSaturated(
            scrllrMngr.addrnd_minHue, scrllrMngr.addrnd_maxHue,
            scrllrMngr.addrnd_minSaturation, scrllrMngr.addrnd_maxSaturation,
            scrllrMngr.addrnd_minValue, scrllrMngr.addrnd_maxValue,
            scrllrMngr.addrnd_dropHueMinValue, scrllrMngr.addrnd_dropHueMaxValue, 255, config.brightness)

        #drawRef.rectangle((0, 0, 0 + 1, config.canvasHeight), fill = None, outline = (255,0,0,255))

        # length transition
        patternLength = xDiv

        for r in range(0, rows):
            columnOffset = 0
            if r == 0 or r == 2 or r == 4 or r == 6:
                columnOffset = xDiv

            if r / 2 % 2 == 0:
                columnOffset = xDiv

            if random.random() < scrllrMngr.patternDrawProb or c == 0:

                if scrllrMngr.pattern == "test":
                    drawRef.rectangle((xPos,5,xPos+4,55), fill = fillClr)

                if random.random() < scrllrMngr.redGreenSwapProb:
                    fillClr = (fillClr[1],fillClr[0],fillClr[2])

                if random.random() < scrllrMngr.redBlueSwapProb:
                    fillClr = (fillClr[2],fillClr[1],fillClr[0])

                if random.random() < scrllrMngr.greenBlueSwapProb:
                    fillClr = (fillClr[0],fillClr[2],fillClr[1])

                if scrllrMngr.pattern == "diamonds":
                    poly = []
                    poly.append((xStart, yStart + yDiv))
                    poly.append((xStart + xDiv, yStart))
                    poly.append((xStart + xDiv + xDiv, yStart + yDiv))
                    poly.append((xStart + xDiv, yStart + yDiv + yDiv))
                    drawRef.polygon(poly, fill=fillClr)
                    # if(n ==2) : color = (100,200,0,255)

                if scrllrMngr.pattern == "bricks":
                    length = xDiv
                    #xPos = xStart + columnOffset
                    yPos = yStart
                    drawRef.rectangle(
                        (xPos+ columnOffset, yPos, xPos+ columnOffset + length, yPos + yDiv),
                        fill=fillClr,
                        outline=None,
                    )

                if scrllrMngr.pattern == "pluses":
                    length = xDiv
                    height = xDiv / 2

                    #xPos = xStart + columnOffset
                    yPos = yStart

                    xPos2 = xPos + round(length / 2 - height / 2)
                    yPos2 = round(yPos - length / 2 + height / 2)

                    drawRef.rectangle(
                        (xPos+ columnOffset, yPos, xPos + length+ columnOffset, yPos + yDiv),
                        fill=fillClr,
                        outline=None,
                    )
                    drawRef.rectangle(
                        (xPos2, yPos2, xPos2 + height, yPos2 + length),
                        fill=fillClr,
                        outline=None,
                    )

                if scrllrMngr.pattern == "regularLines":
                    length = patternLength
                    #xPos = xStart + columnOffset
                    yPos = yStart
                    drawRef.rectangle((xPos+ columnOffset, yPos, xPos + length+ columnOffset, yPos + yDiv), fill = fillClr)


                if scrllrMngr.pattern == "lines":
                    # if (r%2 > 0):
                    length = int(round(random.uniform(1, 2 * xDiv)))
                    offset = int(round(random.uniform(0, 4 * xDiv)))

                    if random.random() < 0.5:
                        drawRef.rectangle(
                            (xStart, yStart, xStart + 2 * xDiv, yStart + yDiv),
                            fill=fillClr,
                            outline=None,
                        )
                    else:
                        drawRef.rectangle(
                            (
                                xStart + offset,
                                yStart,
                                xStart + length + offset,
                                yStart + yDiv,
                            ),
                            fill=fillClr,
                            outline=None,
                        )


            yStart += rowMultiplier * yDiv

        if transitionCount < scrllrMngr.patternLengthTransition-1 :
            #print(scrllrMngr.currentPatternLength,xDiv,lengthDelta)
            transitionCount += 1
            #patternLength += lengthDelta
        else :
            scrllrMngr.currentPatternLength = xDiv


        if scrllrMngr.pattern == "lines":
            xStart += colMultiplier * xDiv
        else:
            xStart += xDiv * 2
        xPos += xDiv
        yStart = 0

    scrllrMngr.patternColor = scrllrMngr.patternEndColor
    scrllrMngr.currentPatternLength = xDiv


## Layer imagery callbacks & regeneration functions
def remakePatternBlock(imageRef, direction):


    if scrllrMngr.alwaysRandomPattern == True :
        if random.random() < .15:
            scrllrMngr.patternDrawProb = random.uniform(scrllrMngr.minDrawProb, scrllrMngr.maxDrawProb)

        if random.random() < scrllrMngr.patternRowChangeProb:
            scrllrMngr.patternRows = (round(random.uniform(scrllrMngr.minPatternRows, scrllrMngr.maxPatternRows)))

        if random.random() < scrllrMngr.patternColChangeProb:
            scrllrMngr.patternCols = (round(random.uniform(scrllrMngr.minPatternCols, scrllrMngr.maxPatternCols)))

        if random.random() < .15:
            choice = round(random.uniform(0,len(scrllrMngr.choiceArray)-1))
            scrllrMngr.pattern = scrllrMngr.choiceArray[choice]

        print("New Patterns : {0} {1}".format(scrllrMngr.patternRows, scrllrMngr.patternCols))

    else :
        scrllrMngr.pattern == scrllrMngr.initialPattern


    scrllrMngr.patternColor = scrllrMngr.patternEndColor
    if random.random() < scrllrMngr.backgroundColorChangeProb :
        scrllrMngr.patternEndColor = colorutils.getRandomColorHSVSaturated(
                scrllrMngr.fg_minHue, scrllrMngr.fg_maxHue,
                scrllrMngr.fg_minSaturation, scrllrMngr.fg_maxSaturation,
                scrllrMngr.fg_minValue, scrllrMngr.fg_maxValue,
                scrllrMngr.fg_dropHueMinValue, scrllrMngr.fg_dropHueMaxValue, 255, config.brightness)


    scrllrMngr.bgBackGroundColor = scrllrMngr.bgBackGroundEndColor
    if random.random() < scrllrMngr.backgroundColorChangeProb :
        scrllrMngr.bgBackGroundEndColor = colorutils.getRandomColorHSVSaturated(
                scrllrMngr.bg_minHue, scrllrMngr.bg_maxHue,
                scrllrMngr.bg_minSaturation, scrllrMngr.bg_maxSaturation,
                scrllrMngr.bg_minValue, scrllrMngr.bg_maxValue,
                scrllrMngr.bg_dropHueMinValue, scrllrMngr.bg_dropHueMaxValue,255,config.brightness)


    drawRef = ImageDraw.Draw(imageRef)
    makeBackGround(drawRef, direction)


def runWork():
    global config
    print(bcolors.OKGREEN + "** " + bcolors.BOLD)
    print("RUNNING Scroller Holder scroller-holder.py")
    print(bcolors.ENDC)
    while 1==1 :
        if config.isRunning == True :
            config.directorController.checkTime()
            if config.directorController.advance == True :
                iterate()
        time.sleep(config.redrawSpeed)
        if config.standAlone == False :
            config.callBack()


def checkTime(scrollerObj):
    scrllrMngr.t2 = time.time()
    delta = scrllrMngr.t2 - scrllrMngr.t1

    if delta > scrllrMngr.timeToComplete and scrllrMngr.deltaTimeDone == False:

        scrollerObj.xSpeed -= 0.2

        if scrollerObj.xSpeed <= 0.70:
            scrllrMngr.deltaTimeDone = True
            scrllrMngr.useFadeThruAnimation = True
            scrllrMngr.f.fadingDone = True

            # print ("DELTA TIME UP")
            processImageForScrolling()
            if scrllrMngr.useUltraSlowSpeed == True:
                scrollerObj.xSpeed = 1


def processImageForScrolling():
    ## Run through each of the objects being scrolled - text, image, background etc
    config.workImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    for scrollerObj in scrllrMngr.scrollArray:
        scrollerObj.scroll()
        config.canvasImage.paste(scrollerObj.canvas, (0, 0), scrollerObj.canvas)

    # Chop up the scrollImage into "rows"
    for n in range(0, scrllrMngr.displayRows):
        segment = config.canvasImage.crop(
            (
                n * config.canvasWidth,
                0,
                config.canvasWidth + n * config.canvasWidth,
                scrllrMngr.bandHeight,
            )
        )

        if (
            (n % 2 == 0)
            and (scrllrMngr.displayRows > 1)
            and scrllrMngr.altDirectionScrolling == True
        ):
            segment = ImageOps.flip(segment)
            segment = ImageOps.mirror(segment)

        config.workImage.paste(segment, (0, n * scrllrMngr.bandHeight))

    if scrllrMngr.useOverLayImage == True:
        if random.random() < scrllrMngr.overlayGlitchRate:
            glitchBox(
                scrllrMngr.loadedImage, -scrllrMngr.overlayGlitchSize, scrllrMngr.overlayGlitchSize
            )
        if random.random() < scrllrMngr.overlayResetRate:
            scrllrMngr.loadedImage.paste(scrllrMngr.loadedImageCopy)
        config.workImage.paste(
            scrllrMngr.loadedImage,
            (scrllrMngr.overLayXPos, scrllrMngr.overLayYPos),
            scrllrMngr.loadedImage,
        )

    if scrllrMngr.overallBlur != 0:
        config.workImage = config.workImage.filter(
            ImageFilter.GaussianBlur(radius=scrllrMngr.overallBlur)
        )


    # Create a bend
    if scrllrMngr.useBend  == True :
        workImageTemp = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))

        bendWidth = scrllrMngr.patternHeight
        segments = 22
        bendStart = [200,0]
        centerOfPivot = [round(bendStart[0] + bendWidth/2),round(bendStart[1] + bendWidth/2)]
        bendEnd = [200 + bendWidth, round(bendStart[1] + bendWidth) + 400]
        cropWidth = round(bendWidth/ segments)

        destination = [200, bendWidth]


        crop1 = config.workImage.crop((0,0,bendStart[0],bendWidth))
        workImageTemp.paste(crop1, (0,0), crop1)

        crop3 = config.workImage.crop((bendStart[0] + bendWidth ,0,bendEnd[1],bendStart[1] + bendWidth ))
        crop3 = crop3.rotate(-90, expand=True)
        workImageTemp.paste(crop3, (bendStart[0],bendWidth), crop3)

        for i in range (segments + 1, -1 , -1) :
            cropTemp = config.workImage.crop((bendStart[0] + i*cropWidth, 0, bendStart[0] + (i+1)*cropWidth + 2, bendWidth))
            cropTemp = cropTemp.rotate(i * -90/segments, expand=True, center = None, translate = None, fillcolor = (255,0,0,0))
            xPos = round(centerOfPivot[0] - bendWidth/2)# + i * 20 #- cropWidth * 2 #+ round(crop2a.size[0]/2)
            yPos = round(bendWidth - cropTemp.size[1])
            workImageTemp.paste(cropTemp, (xPos,yPos) , cropTemp)


        config.workImage = workImageTemp


def iterate():
    global config

    # config.workImageDraw.rectangle((0,0,config.canvasWidth,config.canvasHeight), fill  = (0,0,0))
    # config.canvasImageDraw.rectangle((0,0,config.canvasWidth*10,config.canvasHeight), fill  = (0,0,0,20))

    for scrollerObj in scrllrMngr.scrollArray:
        if scrollerObj.typeOfScroller == "bg":
            if (
                random.random() < scrllrMngr.changeProb * scrllrMngr.changeProbReleaseFactor
                and scrllrMngr.deltaTimeDone == True
                and scrllrMngr.useFadeThruAnimation == True
            ):
                scrllrMngr.useFadeThruAnimation = False
                scrollerObj.xSpeed = random.uniform(0.6, scrollerObj.xMaxSpeed)
                scrllrMngr.deltaTimeDone = False
                scrllrMngr.t1 = time.time()
                scrllrMngr.timeToComplete = random.uniform(3, 10)
            checkTime(scrollerObj)

    if scrllrMngr.useFadeThruAnimation == True and scrllrMngr.useUltraSlowSpeed == True:
        if scrllrMngr.f.fadingDone == True:

            scrllrMngr.renderImageFullOld = config.renderImageFull.copy()
            config.renderImageFull.paste(
                config.workImage,
                (config.imageXOffset, config.imageYOffset),
                config.workImage,
            )
            scrllrMngr.f.xPos = config.imageXOffset
            scrllrMngr.f.yPos = config.imageYOffset
            # config.renderImageFull = config.renderImageFull.convert("RGBA")
            # renderImageFull = renderImageFull.convert("RGBA")
            scrllrMngr.f.setUp(
                scrllrMngr.renderImageFullOld.convert("RGBA"),
                config.workImage.convert("RGBA"),
            )
            processImageForScrolling()

        scrllrMngr.f.fadeIn()
        config.render(scrllrMngr.f.blendedImage, 0, 0)

    else:
        processImageForScrolling()
        config.renderImageFull.paste(
            config.workImage,
            (config.imageXOffset, config.imageYOffset),
            config.workImage,
        )

        # RENDERING AS A MOCKUP OR AS REAL
        if config.useDrawingPoints == True :
            config.panelDrawing.canvasToUse = config.renderImageFull
            config.panelDrawing.render()
        else :
            #config.render(config.canvasImage, 0, 0, config.canvasWidth, config.canvasHeight)
            #config.render(config.image, 0, 0)
            config.render(config.renderImageFull, 0, 0)


def main(run=True):
    global config, threads, thrd, scrllrMngr
    scrllrMngr = ScrollerManager(config)
    scrllrMngr.setUp(workConfig)

    if run:
        runWork()


### Kick off .......
if __name__ == "__main__":
    __main__()
