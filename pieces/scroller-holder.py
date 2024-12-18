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

"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""
## Image manipulations


def glitchBox(img, r1=-10, r2=10, dir="horizontal"):

    apparentWidth = img.size[0]
    apparentHeight = img.size[1]

    dx = int(random.uniform(r1, r2))
    dy = int(random.uniform(r1, r2))

    # dx = 0

    sectionWidth = int(random.uniform(2, apparentWidth - dx))
    sectionHeight = int(random.uniform(2, apparentHeight - dy))

    # sectionHeight = apparentWidth

    # 95% of the time they dance together as mirrors
    if random.random() < 0.97:
        if dir == "horizontal":
            cp1 = img.crop((0, dy, apparentWidth, dy + sectionHeight))
        else:
            cp1 = img.crop((dx, 0, dx + sectionWidth, sectionHeight))

        img.paste(cp1, (int(0 + dx), int(0 + dy)))


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""

## Layer imagery
def makeDaemonMessages(imageRef, direction=1):
    global config

    demonsMale = [
        "Jealousy",
        "Wrath",
        "Tears",
        "Sighing",
        "Suffering",
        "Lamentation",
        "Bitter Weeping",
    ]
    demonsMaleModifier = [
        "Jealous",
        "Wrathful",
        "Tearful",
        "Sighing",
        "Suffering",
        "Lamenting",
        "Embittered Weeping",
    ]

    demonsFemale = [
        "Wrath",
        "Pain",
        "Lust",
        "Sighing",
        "Cursedness",
        "Bitterness",
        "Quarelsomeness",
    ]
    demonsFemaleModifier = [
        "Wrathful",
        "Painful",
        "Lusty",
        "Sighing",
        "Cursed",
        "Bitter",
        "Quarelsome",
    ]

    angelsMale = [
        "Unenviousness",
        "Blessedness",
        "Joy",
        "Truth",
        "Unbegrudgingness",
        "Belovedness",
        "Trustworthyness",
    ]
    angelsMaleModifier = [
        "Unenvious",
        "Blessed",
        "Joyful",
        "True",
        "Unbegrudging",
        "Beloved",
        "Trustworthy",
    ]

    angelsFemale = [
        "Peace",
        "Gladness",
        "Rejoicing",
        "Blessedness",
        "Truth",
        "Love",
        "Faith",
    ]
    angelsFemaleModifier = [
        "Peaceful",
        "Glad",
        "Rejoicing",
        "Blessed",
        "Truthful",
        "Lovely",
        "Faithful",
    ]

    maleDemons = [demonsMale, demonsMaleModifier]
    femaleDemons = [demonsFemale, demonsFemaleModifier]
    maleAngels = [angelsMale, angelsMaleModifier]
    femaleAngels = [angelsFemale, angelsFemaleModifier]

    md_fd = [maleDemons, femaleDemons]
    fd_md = [femaleDemons, maleDemons]

    ma_fa = [maleAngels, femaleAngels]
    fa_ma = [femaleAngels, maleAngels]

    md_fa = [maleDemons, femaleAngels]
    fa_md = [femaleAngels, maleDemons]

    ma_fd = [maleAngels, femaleDemons]
    fd_ma = [femaleDemons, maleAngels]

    demonArray = [md_fd, md_fa, ma_fd, ma_fa, fd_md, fd_ma, fa_md, fa_ma]

    combination = demonArray[int(math.floor(random.uniform(0, len(demonArray))))]
    arrayToUse = combination[int(math.floor(random.uniform(0, len(combination))))]
    messageString = ""

    if config.sansSerif:
        font = ImageFont.truetype(
            config.path + "/assets/fonts/freefont/FreeSansBold.ttf", config.fontSize
        )
    else:
        font = ImageFont.truetype(
            config.path + "/assets/fonts/freefont/FreeSerifBold.ttf", config.fontSize
        )

    for i in range(0, 4):
        adj = arrayToUse[1][int(math.floor(random.uniform(0, 7)))]
        noun = arrayToUse[0][int(math.floor(random.uniform(0, 7)))]
        messageString = messageString + adj.upper() + " " + noun.upper() + "           "

    # print(messageString)

    if random.random() < 0.15:
        messageString = ""
        font = ImageFont.truetype(
            config.path + "/assets/fonts/freefont/FreeSans.ttf", config.fontSize
        )
        for i in range(0, 23):
            xo = "X" if (random.random() < 0.5) else "O"
            messageString = messageString + xo
            messageString = (
                messageString + " " if (random.random() < 0.5) else messageString
            )

    if config.colorMode == "getRandomRGB":
        clr = colorutils.getRandomRGB(config.brightness)
    if config.colorMode == "randomColor":
        clr = colorutils.randomColor(config.brightness)
    if config.colorMode == "getRandomColorWheel":
        clr = colorutils.getRandomColorWheel(config.brightness)

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""
    # draw the message to get its size

    tempImage = Image.new("RGBA", (1200, 196))
    draw = ImageDraw.Draw(tempImage)

    # pixLen = draw.textsize(messageString, font=font)
    
    pixLen = [100,10]
    # For some reason textsize is not getting full height !
    fontHeight = int(pixLen[1] * 1.3)

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""
    # make a new image with the right size
    scrollImage = Image.new("RGBA", (pixLen[0] + 2, fontHeight))
    draw = ImageDraw.Draw(scrollImage)
    iid = scrollImage.im.id

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""
    # Draw the text with "borders"
    indent = int(0.05 * config.tileSize[0])
    for i in range(1, config.shadowSize):
        draw.text((indent + -i, -i), messageString, (0, 0, 0), font=font)
        draw.text((indent + i, i), messageString, (0, 0, 0), font=font)

    draw.text((2, 0), messageString, clr, font=font)

    refDraw = ImageDraw.Draw(imageRef)
    refDraw.rectangle((0, 0, pixLen[0] + 2, fontHeight), fill=config.bgBackGroundColor)
    imageRef.paste(scrollImage, (0, config.textVOffest), scrollImage)


def remakeDaemonMessages(imageRef, direction=1):
    ##
    makeDaemonMessages(imageRef=imageRef, direction=direction)


def makeScrollBlock(imageRef, imageDrawRef, direction):
    global config
    w = imageRef.size[0]
    # config.enhancer = ImageEnhance.Brightness(config.loadedImage)
    # config.loadedImage = config.enhancer.enhance(config.overlayBrightness)

    widthImage = config.imageBlockImageLoaded.size[0]
    heightImage = config.imageBlockImageLoaded.size[1]
    hBuffer = config.imageBlockBuffer
    numberOfUnits = int(round(w / (widthImage + hBuffer)))

    for i in range(0, numberOfUnits):
        x = i * (widthImage + hBuffer)
        y = -5

        tempImage = config.imageBlockImageLoaded.copy()
        tempEnhancer = ImageEnhance.Brightness(tempImage)
        tempImage = tempEnhancer.enhance(config.brightness)

        clrBlock = Image.new("RGBA", (widthImage, heightImage))
        clrBlockDraw = ImageDraw.Draw(clrBlock)

        # Color overlay on b/w PNG sprite
        # EVERYTHING HAS TO BE PNG  / have ALPHA
        if config.useTransparentImages == True:
            clr = colorutils.randomColorAlpha(
                brtns=config.brightness, maxTransparency=200
            )
        else:
            clr = colorutils.randomColor()
        clrBlockDraw.rectangle((0, 0, widthImage, heightImage), fill=clr)

        tempImage = ImageChops.multiply(clrBlock, tempImage)
        imageRef.paste(tempImage, (x, y), tempImage)


def remakeScrollBlock(imageRef, direction):
    drawRef = ImageDraw.Draw(imageRef)
    if random.random() < config.imageBlockRemakeProb:
        makeScrollBlock(imageRef, drawRef, direction)


def makeArrows(drawRef, direction=1):

    rows = config.displayCols * 2
    cols = config.arrowCols * 2

    xDiv = int(config.displayRows * config.windowWidth) / cols
    yDiv = config.canvasHeight / rows

    xStart = 0  # config.canvasWidth / 2
    yStart = config.bandHeight / 2  # config.canvasHeight / 2

    bufferDistance = 15
    arrowLength = cols * 2
    blade = cols / 3

    clr = (int(220 * config.brightness), 0, 0)

    drawRef.rectangle(
        (0, 0, int(config.displayRows * config.windowWidth), config.canvasHeight),
        fill=config.bgBackGroundColor,
    )

    for c in range(0, cols):
        yArrowEnd = yStart  # yStart + arrowLength
        xArrowEnd = xStart + arrowLength

        # the blades
        xDisplace = xArrowEnd - blade
        yDisplace = blade * math.tan(math.pi / 4)
        # the horizontal
        if random.random() < 0.5:
            drawRef.line(
                (xStart, yStart, xArrowEnd, yArrowEnd),
                fill=clr,
                width=config.lineThickness,
            )

            if direction == 1:
                drawRef.line(
                    (xArrowEnd - blade, yArrowEnd - yDisplace, xArrowEnd, yArrowEnd),
                    fill=clr,
                    width=config.lineThickness,
                )
                drawRef.line(
                    (xArrowEnd - blade, yArrowEnd + yDisplace, xArrowEnd, yArrowEnd),
                    fill=clr,
                    width=config.lineThickness,
                )
            else:
                drawRef.line(
                    (xStart + blade, yArrowEnd - yDisplace, xStart, yArrowEnd),
                    fill=clr,
                    width=config.lineThickness,
                )
                drawRef.line(
                    (xStart + blade, yArrowEnd + yDisplace, xStart, yArrowEnd),
                    fill=clr,
                    width=config.lineThickness,
                )

        # yStart += arrowLength + bufferDistance
        xStart += arrowLength + bufferDistance


def remakeArrowBlock(imageRef, direction):
    drawRef = ImageDraw.Draw(imageRef)
    makeArrows(drawRef, direction)


def makeMessage(imageRef, messageString="FooBar", direction=1):
    global config

    if config.colorMode == "getRandomRGB":
        clr = colorutils.getRandomRGB(config.brightness)
    if config.colorMode == "randomColor":
        clr = colorutils.randomColor(config.brightness)
    if config.colorMode == "getRandomColorWheel":
        clr = colorutils.getRandomColorWheel(config.brightness)

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""
    # draw the message to get its size
    if config.sansSerif:
        font = ImageFont.truetype(
            config.path + "/assets/fonts/freefont/FreeSansBold.ttf", config.fontSize
        )
    else:
        font = ImageFont.truetype(
            config.path + "/assets/fonts/freefont/FreeSerifBold.ttf", config.fontSize
        )

    tempImage = Image.new("RGBA", (1200, 196))
    draw = ImageDraw.Draw(tempImage)
    # pixLen = draw.textsize(messageString, font=font)
    pixelLength = int(draw.textlength(messageString, font=font))
    
    print(pixelLength)
    # For some reason textsize is not getting full height !
    pixLen = [pixelLength + 2,config.fontSize]
    fontHeight = int(pixLen[1] * 1.3)
    
    """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""
    # make a new image with the right size
    scrollImage = Image.new("RGBA", (pixLen[0] + 2, fontHeight))
    draw = ImageDraw.Draw(scrollImage)
    iid = scrollImage.im.id

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""
    # Draw the text with "borders"
    indent = int(0.05 * config.tileSize[0])
    for i in range(1, config.shadowSize):
        draw.text((indent + -i, -i), messageString, (0, 0, 0), font=font)
        draw.text((indent + i, i), messageString, (0, 0, 0), font=font)

    print("makeMesage called:" + messageString)
    draw.text((2, 0), messageString, clr, font=font)

    refDraw = ImageDraw.Draw(imageRef)
    # refDraw.rectangle((0, 0, pixLen[0] + 2, fontHeight), fill=None)
    imageRef.paste(scrollImage, (0, config.textVOffest), scrollImage)


def remakeMessage(imageRef, messageString="FooBar", direction=1):
    messageString = config.msg1 if random.random() < 0.5 else config.msg2
    # config.textVOffest = round(random.uniform(-12, -30))
    if random.random() < 0.5:
        config.colorMode = "randomColor"
    else:
        config.colorMode = "getRandomRGB"
    # makeMessage(imageRef=imageRef, messageString=messageString, direction=direction)


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""


def makeBackGround(drawRef, n=1):
    rows = config.patternRows * 1
    cols = config.patternCols * 1

    xDiv = round(
        (config.displayRows * config.canvasWidth) / cols
    )  # - config.patternColsOffset

    xDiv = (
        2 * config.canvasWidth * config.displayCols/ cols 
    ) 

    yDiv = (
        config.canvasHeight / rows
    ) / config.displayRows  # - config.patternRowsOffset


    gap = 0
    steps = cols
    config.arrowBgBackGroundColor = (0, 0, 0, 20)  # colorutils.getRandomColor()
    colorChange = False

    # Background setup
    '''
    '''
    drawRef.rectangle(
        (0, 0, (round(config.displayRows * config.canvasWidth)), config.canvasHeight),
        fill=config.bgBackGroundColor)

    ## The multiplier is actually a factor of the number of rows
    ## but, generally so far only using two rows ....
    rDelta = ((config.bgBackGroundEndColor[0] - config.bgBackGroundColor[0]) / steps)
    gDelta = ((config.bgBackGroundEndColor[1] - config.bgBackGroundColor[1]) / steps)
    bDelta = ((config.bgBackGroundEndColor[2] - config.bgBackGroundColor[2]) / steps)

    xPos = 0 
    transitionCount = 0 
    config.patternLengthTransition = 8
    lengthDelta = round((xDiv - config.currentPatternLength ) / config.patternLengthTransition)
    patternLength = xDiv

    for c in range(0, cols):
        columnOffset = 0

        rCol = config.bgBackGroundColor[0] + rDelta
        gCol = config.bgBackGroundColor[1] + gDelta
        bCol = config.bgBackGroundColor[2] + bDelta
        config.bgBackGroundColor = (rCol, gCol, bCol)

        ### Because the way the pattern draws the left end is actually the end color
        ### so need to reverse the color gradient ....

        fillClr = (
            (round(config.bgBackGroundEndColor[0] - rDelta * (c + 1))),
            (round(config.bgBackGroundEndColor[1] - gDelta * (c + 1))),
            (round(config.bgBackGroundEndColor[2] - bDelta * (c + 1))),
            200,
        )

        w = patternLength

        outline = None
        if c < 0 :
            outline=(255,0,0,200)

        drawRef.rectangle((xPos,0,xPos+w,config.canvasHeight), fill = fillClr, outline=outline)
        xPos += w

        if transitionCount < config.patternLengthTransition-1 : 
            #print(config.currentPatternLength,xDiv,lengthDelta)
            transitionCount += 1
            #patternLength += lengthDelta
        else :
            patternLength = xDiv


    config.bgBackGroundColor = config.bgBackGroundEndColor

    # Foreground setup

    rowMultiplier = 1
    colMultiplier = 1

    if config.pattern == "bricks":
        rowMultiplier = 1
        colMultiplier = 1

    if config.pattern == "regularLines":
        rowMultiplier = 2
        colMultiplier = 1

    if config.pattern == "pluses":
        rowMultiplier = 2
        colMultiplier = 1

    if config.pattern == "diamonds":
        rowMultiplier = 2
        colMultiplier = 2

    
    ## The multiplier is actually a factor of the number of rows
    ## but, generally so far only using two rows ....
    rDelta = ((config.patternEndColor[0] - config.patternColor[0]) / steps)
    gDelta = ((config.patternEndColor[1] - config.patternColor[1]) / steps)
    bDelta = ((config.patternEndColor[2] - config.patternColor[2]) / steps)

    xPos = 0
    xStart = 0
    yStart = 0
    transitionCount = 0 
    config.patternLengthTransition = 8
    lengthDelta = round((xDiv - config.currentPatternLength ) / config.patternLengthTransition)


    for c in range(0, cols+1):
        
        columnOffset = 0

        rCol = config.patternColor[0] + rDelta
        gCol = config.patternColor[1] + gDelta
        bCol = config.patternColor[2] + bDelta
        config.patternColor = (rCol, gCol, bCol)

        ### Because the way the pattern draws the left end is actually the end color
        ### so need to reverse the color gradient ....

        fillClr = (
            (round(config.patternEndColor[0] - rDelta * (c + 1))),
            (round(config.patternEndColor[1] - gDelta * (c + 1))),
            (round(config.patternEndColor[2] - bDelta * (c + 1))),
            225,
        )
        
        #drawRef.rectangle((0, 0, 0 + 1, config.canvasHeight), fill = None, outline = (255,0,0,255))

        # length transition
        patternLength = xDiv

        for r in range(0, rows):
            columnOffset = 0
            if r == 0 or r == 2 or r == 4 or r == 6:
                columnOffset = xDiv

            if r / 2 % 2 == 0:
                columnOffset = xDiv

            if random.random() < config.patternDrawProb or c == 0:

                if config.pattern == "test":
                    drawRef.rectangle((xPos,5,xPos+4,55), fill = fillClr)

                if random.random() < config.redGreenSwapProb: 
                    fillClr = (fillClr[1],fillClr[0],fillClr[2])

                if random.random() < config.redBlueSwapProb: 
                    fillClr = (fillClr[2],fillClr[1],fillClr[0])

                if random.random() < config.greenBlueSwapProb: 
                    fillClr = (fillClr[0],fillClr[2],fillClr[1])

                if config.pattern == "diamonds":
                    poly = []
                    poly.append((xStart, yStart + yDiv))
                    poly.append((xStart + xDiv, yStart))
                    poly.append((xStart + xDiv + xDiv, yStart + yDiv))
                    poly.append((xStart + xDiv, yStart + yDiv + yDiv))
                    drawRef.polygon(poly, fill=fillClr)
                    # if(n ==2) : color = (100,200,0,255)

                if config.pattern == "bricks":
                    length = xDiv
                    #xPos = xStart + columnOffset
                    yPos = yStart
                    drawRef.rectangle(
                        (xPos+ columnOffset, yPos, xPos+ columnOffset + length, yPos + yDiv),
                        fill=fillClr,
                        outline=None,
                    )

                if config.pattern == "pluses":
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
        
                if config.pattern == "regularLines":
                    length = patternLength
                    #xPos = xStart + columnOffset
                    yPos = yStart
                    drawRef.rectangle((xPos+ columnOffset, yPos, xPos + length+ columnOffset, yPos + yDiv), fill = fillClr)

                
                if config.pattern == "lines":
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

        if transitionCount < config.patternLengthTransition-1 : 
            #print(config.currentPatternLength,xDiv,lengthDelta)
            transitionCount += 1
            #patternLength += lengthDelta
        else :
            config.currentPatternLength = xDiv

        
        if config.pattern == "lines":
            xStart += colMultiplier * xDiv
        else:
            xStart += xDiv * 2
        xPos += xDiv
        yStart = 0

    config.patternColor = config.patternEndColor
    config.currentPatternLength = xDiv


## Layer imagery callbacks & regeneration functions
def remakePatternBlock(imageRef, direction):
    #print("remakePatternBlock")
    ## Stacking the cards ...

    '''
    if config.setPatternColor == True :
        config.setPatternEndColor = colorutils.getRandomColorHSV(
                config.fg_minHue, config.fg_maxHue, 
                config.fg_minSaturation, config.fg_maxSaturation, 
                config.fg_minValue, config.fg_maxValue,
                config.fg_dropHueMinValue, config.fg_dropHueMaxValue, 255, config.brightness)
        config.patternEndColor = config.setPatternEndColor
        config.patternColor = config.setPatternEndColor
    '''
    
    if config.alwaysRandomPattern == True :
        if random.random() < .15:
            config.patternDrawProb = random.uniform(0.08, 0.8)

        if random.random() < .15:
            config.patternRows = (round(random.uniform(8, config.canvasHeight)))

        if random.random() < .15:
            config.patternCols = (round(random.uniform(4, config.canvasWidth)))

        if random.random() < .15:
            if random.random() < .5 :
                config.pattern == "lines"
            else:
                config.pattern == "pluses"
    else :
        config.pattern == config.initialPattern 




    config.patternColor = config.patternEndColor
    if random.random() < config.backgroundColorChangeProb :
        config.patternEndColor = colorutils.getRandomColorHSV(
                config.fg_minHue, config.fg_maxHue, 
                config.fg_minSaturation, config.fg_maxSaturation, 
                config.fg_minValue, config.fg_maxValue,
                config.fg_dropHueMinValue, config.fg_dropHueMaxValue, 255, config.brightness)


    config.bgBackGroundColor = config.bgBackGroundEndColor
    if random.random() < config.backgroundColorChangeProb :
        config.bgBackGroundEndColor = colorutils.getRandomColorHSV(
                config.bg_minHue, config.bg_maxHue, 
                config.bg_minSaturation, config.bg_maxSaturation, 
                config.bg_minValue, config.bg_maxValue,
                config.bg_dropHueMinValue, config.bg_dropHueMaxValue,255,config.brightness)


    drawRef = ImageDraw.Draw(imageRef)
    makeBackGround(drawRef, direction)


## Setup and run functions
def configureBackgroundScrolling():
    global workConfig
    print("configureBackgroundScrolling")
    config.patternRows = int(workConfig.get("scroller", "patternRows"))
    config.patternCols = int(workConfig.get("scroller", "patternCols"))
    config.patternRowsOffset = int(workConfig.get("scroller", "patternRowsOffset"))
    config.patternColsOffset = int(workConfig.get("scroller", "patternColsOffset"))
    config.patternDrawProb = float(workConfig.get("scroller", "patternDrawProb"))
    config.bgBackGroundColor = workConfig.get("scroller", "bgBackGroundColor").split(",")
    config.bgBackGroundColor = tuple([int(i) for i in config.bgBackGroundColor])
    config.pattern = workConfig.get("scroller", "pattern")
    config.initialPattern  = workConfig.get("scroller", "pattern")
    config.patternSpeed = float(workConfig.get("scroller", "patternSpeed"))


    if config.useHSV :	

        config.bgBackGroundColor = colorutils.getRandomColorHSV(
                config.bg_minHue, config.bg_maxHue, 
                config.bg_minSaturation, config.bg_maxSaturation, 
                config.bg_minValue, config.bg_maxValue,
                config.bg_dropHueMinValue, config.bg_dropHueMaxValue, 255, config.brightness)

        config.bgBackGroundEndColor = colorutils.getRandomColorHSV(
                config.bg_minHue, config.bg_maxHue, 
                config.bg_minSaturation, config.bg_maxSaturation, 
                config.bg_minValue, config.bg_maxValue,
                config.bg_dropHueMinValue, config.bg_dropHueMaxValue, 255, config.brightness)

        config.patternColor = colorutils.getRandomColorHSV(
                config.fg_minHue, config.fg_maxHue, 
                config.fg_minSaturation, config.fg_maxSaturation, 
                config.fg_minValue, config.fg_maxValue,0,0,255,config.brightness)		

        config.patternEndColor = colorutils.getRandomColorHSV(
                config.fg_minHue, config.fg_maxHue, 
                config.fg_minSaturation, config.fg_maxSaturation, 
                config.fg_minValue, config.fg_maxValue,
                config.fg_dropHueMinValue, config.fg_dropHueMaxValue, 255, config.brightness)
    else :

        config.bgBackGroundColor = colorutils.randomColorAlpha(config.brightness)
        config.bgBackGroundEndColor = colorutils.randomColorAlpha(config.brightness)
        config.patternColor = colorutils.randomColorAlpha(config.brightness)
        config.patternEndColor = colorutils.randomColorAlpha(config.brightness)

        if config.alwaysRandomPatternColor == True:
            config.patternColor = colorutils.randomColorAlpha(config.brightness)
            config.patternEndColor = colorutils.randomColorAlpha(config.brightness)

        if config.setPatternColor == True :
            config.setPatternEndColor = colorutils.getRandomColorHSV(
                    config.fg_minHue, config.fg_maxHue, 
                    config.fg_minSaturation, config.fg_maxSaturation, 
                    config.fg_minValue, config.fg_maxValue,
                    config.bg_dropHueMinValue, config.bg_dropHueMaxValue, 255, config.brightness)
            config.patternColor = config.setPatternEndColor
            config.patternEndColor = config.setPatternEndColor

        
    config.currentPatternLength = 0

    config.scroller4 = continuous_scroller.ScrollObject()
    scrollerRef = config.scroller4
    scrollerRef.typeOfScroller = "bg"
    scrollerRef.canvasWidth = int(config.displayRows * config.canvasWidth)
    scrollerRef.xSpeed = config.patternSpeed
    scrollerRef.setUp()
    direction = 1 if scrollerRef.xSpeed > 0 else -1
    scrollerRef.callBack = {"func": remakePatternBlock, "direction": direction}
    

    try:
        config.maxSpeed = float(workConfig.get("scroller", "maxSpeed"))
    except Exception as e:
        config.maxSpeed = config.patternSpeed
    
    scrollerRef.xMaxSpeed = config.maxSpeed

    try:
        config.changeProb = float(workConfig.get("scroller", "changeProb"))
    except Exception as e:
        config.changeProb = 0.0
        print(str(e))

    try:
        config.changeProbReleaseFactor = float(workConfig.get("scroller", "changeProbReleaseFactor"))
    except Exception as e:
        config.changeProbReleaseFactor = 1.0
        print(str(e))


    makeBackGround(scrollerRef.bg1Draw, 1)
    makeBackGround(scrollerRef.bg2Draw, 1)


    config.t1 = time.time()
    config.t2 = time.time()
    config.timeToComplete = 1
    config.scrollerPauseBool = False

    config.scrollArray.append(scrollerRef)


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""


def configureImageScrolling():
    global workConfig
    config.imageSpeed = float(workConfig.get("scroller", "imageSpeed"))
    config.imageBlockImage = workConfig.get("scroller", "imageBlockImage")
    config.imageBlockBuffer = int(workConfig.get("scroller", "imageBlockBuffer"))
    config.imageBlockRemakeProb = float(
        workConfig.get("scroller", "imageBlockRemakeProb")
    )

    arg = config.path + config.imageBlockImage
    config.imageBlockImageLoaded = Image.open(arg, "r")
    config.imageBlockImageLoaded.load()
    config.imageBlockImageLoadedCopy = config.imageBlockImageLoaded.copy()

    config.scroller5 = continuous_scroller.ScrollObject()
    scrollerRef = config.scroller5
    scrollerRef.canvasWidth = int(config.displayCols * config.canvasWidth)
    # scrollerRef.canvasHeight = int(config.windowHeight)
    scrollerRef.xSpeed = config.imageSpeed
    scrollerRef.setUp()
    direction = 1 if scrollerRef.xSpeed > 0 else -1
    scrollerRef.callBack = {"func": remakeScrollBlock, "direction": direction}
    makeScrollBlock(scrollerRef.bg1, scrollerRef.bg1Draw, direction)
    makeScrollBlock(scrollerRef.bg2, scrollerRef.bg2Draw, direction)
    config.scrollArray.append(scrollerRef)


def configureArrowScrolling():
    global workConfig
    config.arrowCols = int(workConfig.get("scroller", "arrowCols"))
    config.lineThickness = int(workConfig.get("scroller", "lineThickness"))
    config.arrowSpeed = int(workConfig.get("scroller", "arrowSpeed"))
    config.greyLevel = int(workConfig.get("scroller", "greyLevel"))
    config.redShift = int(workConfig.get("scroller", "redShift"))
    config.scroller1 = continuous_scroller.ScrollObject()

    scrollerRef = config.scroller1
    scrollerRef.canvasWidth = int(config.displayRows * config.canvasWidth)
    scrollerRef.xSpeed = config.arrowSpeed
    scrollerRef.setUp()
    direction = 1 if scrollerRef.xSpeed > 0 else -1
    scrollerRef.callBack = {"func": remakeArrowBlock, "direction": direction}
    makeArrows(scrollerRef.bg1Draw, -1)
    makeArrows(scrollerRef.bg2Draw, -1)
    config.scrollArray.append(scrollerRef)


def configureMessageScrolling():
    global workConfig
    config.colorMode = workConfig.get("scroller", "colorMode")
    config.sansSerif = workConfig.getboolean("scroller", "sansSerif")
    config.fontSize = int(workConfig.get("scroller", "fontSize"))
    config.textVOffest = int(workConfig.get("scroller", "textVOffest"))
    config.shadowSize = int(workConfig.get("scroller", "shadowSize"))
    config.textSpeed = float(workConfig.get("scroller", "textSpeed"))
    config.msg1 = workConfig.get("scroller", "msg1")
    config.msg2 = workConfig.get("scroller", "msg2")
    config.msg3 = workConfig.get("scroller", "msg3")

    config.scroller2 = continuous_scroller.ScrollObject()
    scrollerRef = config.scroller2
    scrollerRef.canvasWidth = int(config.displayCols * config.canvasWidth)
    scrollerRef.canvasWidth = int(len(config.msg1) * config.fontSize/2)
    scrollerRef.canvasHeight = 200
    scrollerRef.xSpeed = -config.textSpeed
    scrollerRef.setUp()
    direction = 1 if scrollerRef.xSpeed > 0 else -1
    makeMessage(scrollerRef.bg1, config.msg1, direction)
    makeMessage(scrollerRef.bg2, config.msg1, direction)
    scrollerRef.callBack = {"func": remakeMessage, "direction": direction}
    config.scrollArray.append(scrollerRef)

    config.scroller3 = continuous_scroller.ScrollObject()
    scrollerRef = config.scroller3
    scrollerRef.canvasWidth = int(config.displayCols * config.canvasWidth)
    scrollerRef.canvasWidth = int(len(config.msg2) * config.fontSize/2)
    scrollerRef.xSpeed = config.textSpeed + 0.25
    scrollerRef.setUp()
    direction = 1 if scrollerRef.xSpeed > 0 else -1
    makeMessage(scrollerRef.bg1, config.msg2, direction)
    makeMessage(scrollerRef.bg2, config.msg2, direction)
    scrollerRef.callBack = {"func": remakeMessage, "direction": direction}
    config.scrollArray.append(scrollerRef)


def configureAltTextScrolling():
    global workConfig
    config.colorMode = workConfig.get("scroller", "colorMode")
    config.sansSerif = workConfig.getboolean("scroller", "sansSerif")
    config.fontSize = int(workConfig.get("scroller", "fontSize"))
    config.textVOffest = int(workConfig.get("scroller", "textVOffest"))
    config.shadowSize = int(workConfig.get("scroller", "shadowSize"))
    config.textSpeed = float(workConfig.get("scroller", "textSpeed"))
    config.scroller6 = continuous_scroller.ScrollObject()
    scrollerRef = config.scroller6
    scrollerRef.canvasWidth = int(config.displayRows * config.canvasWidth)
    scrollerRef.xSpeed = -config.textSpeed
    scrollerRef.setUp()
    direction = 1 if scrollerRef.xSpeed > 0 else -1
    makeDaemonMessages(scrollerRef.bg1, direction)
    makeDaemonMessages(scrollerRef.bg2, direction)
    scrollerRef.callBack = {"func": remakeDaemonMessages, "direction": direction}
    config.scrollArray.append(scrollerRef)


def configureImageOverlay():
    global workConfig
    config.overLayImage = workConfig.get("scroller", "overLayImage")
    config.overLayXPos = int(workConfig.get("scroller", "overLayXPos"))
    config.overLayYPos = int(workConfig.get("scroller", "overLayYPos"))
    config.overlayGlitchSize = int(workConfig.get("scroller", "overlayGlitchSize"))
    config.overlayBrightness = float(workConfig.get("scroller", "overlayBrightness"))
    config.overlayGlitchRate = float(workConfig.get("scroller", "overlayGlitchRate"))
    config.overlayResetRate = float(workConfig.get("scroller", "overlayResetRate"))

    arg = config.path + config.overLayImage
    config.loadedImage = Image.open(arg, "r")
    config.loadedImage.load()
    config.loadedImageCopy = config.loadedImage.copy()


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """"""


def init():
    global config
    global workConfig
    print("SINGLETON SCROLLER HOLDER INIT")

    config.redrawSpeed = float(workConfig.get("scroller", "redrawSpeed"))

    config.windowWidth = float(workConfig.get("displayconfig", "windowWidth"))
    config.windowHeight = float(workConfig.get("displayconfig", "windowHeight"))

    config.xOffset = int(workConfig.get("scroller", "xOffset"))
    config.yOffset = int(workConfig.get("scroller", "yOffset"))

    config.displayRows = int(workConfig.get("scroller", "displayRows"))
    config.displayCols = int(workConfig.get("scroller", "displayCols"))

    # ********* HARD CODING VALUES  ***********************

    config.bandHeight = int(round(config.canvasHeight / config.displayRows))
    config.bgBackGroundColor = (0, 0, 0, 0)
    config.arrowBgBackGroundColor = (0, 0, 0, 200)

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

    config.overallBlur = float(
        workConfig.get("scroller", "overallBlur", vars=0, fallback=0)
    )

    config.flip = False
    config.scrollArray = []

    ## Set up the scrolling layer

    config.useBackground = workConfig.getboolean("scroller", "useBackground")

    try:
        config.backgroundColorChangeProb = float(workConfig.get("scroller", "backgroundColorChangeProb"))
    except Exception as e:
        print(str(e))
        config.backgroundColorChangeProb = .5


    try:
        config.setPatternColor = workConfig.getboolean("scroller", "setPatternColor")
        config.setPatternEndColor = list(map(lambda x: int(x), workConfig.get("scroller", "setPatternEndColor").split(",")))
    except Exception as e:
        config.setPatternColor = False
        print(str(e))

    try:
        config.altDirectionScrolling = workConfig.getboolean(
        "scroller", "altDirectionScrolling"
        )
    except Exception as e:
        config.altDirectionScrolling = False
        print(str(e))

    try:
        config.alwaysRandomPatternColor = workConfig.getboolean(
            "scroller", "alwaysRandomPatternColor"
        )
    except Exception as e:
        config.alwaysRandomPatternColor = False
        print(str(e))

    try:
        config.alwaysRandomPattern = workConfig.getboolean(
            "scroller", "alwaysRandomPattern"
        )
    except Exception as e:
        config.alwaysRandomPattern = False
        print(str(e))


    try:
        config.redGreenSwapProb = float(workConfig.get("scroller", "redGreenSwapProb"))
    except Exception as e:
        print(str(e))
        config.redGreenSwapProb = 0
    try:
        config.redBlueSwapProb = float(workConfig.get("scroller", "redBlueSwapProb"))
    except Exception as e:
        print(str(e))
        config.redBlueSwapProb = 0
    try:
        config.greenBlueSwapProb = float(workConfig.get("scroller", "greenBlueSwapProb"))
    except Exception as e:
        print(str(e))
        config.greenBlueSwapProb = 0

    try:
        config.bg_dropHueMinValue = float(workConfig.get("scroller", "bg_dropHueMinValue"))
        config.bg_dropHueMaxValue = float(workConfig.get("scroller", "bg_dropHueMaxValue"))
        config.fg_dropHueMinValue = float(workConfig.get("scroller", "fg_dropHueMinValue"))
        config.fg_dropHueMaxValue = float(workConfig.get("scroller", "fg_dropHueMaxValue"))		
    except Exception as e:
        config.bg_dropHueMinValue = 0
        config.bg_dropHueMaxValue = 0
        config.fg_dropHueMinValue = 0
        config.fg_dropHueMaxValue = 0
        print(str(e))

    try:
        config.useHSV = True

        config.fg_minHue = int(workConfig.get("scroller", "fg_minHue"))
        config.fg_maxHue = int(workConfig.get("scroller", "fg_maxHue"))
        config.fg_minSaturation = float(workConfig.get("scroller", "fg_minSaturation"))
        config.fg_maxSaturation = float(workConfig.get("scroller", "fg_maxSaturation"))
        config.fg_minValue = float(workConfig.get("scroller", "fg_minValue"))
        config.fg_maxValue = float(workConfig.get("scroller", "fg_maxValue"))


        config.bg_minHue = int(workConfig.get("scroller", "bg_minHue"))
        config.bg_maxHue = int(workConfig.get("scroller", "bg_maxHue"))
        config.bg_minSaturation = float(workConfig.get("scroller", "bg_minSaturation"))
        config.bg_maxSaturation = float(workConfig.get("scroller", "bg_maxSaturation"))
        config.bg_minValue = float(workConfig.get("scroller", "bg_minValue"))
        config.bg_maxValue = float(workConfig.get("scroller", "bg_maxValue"))


    except Exception as e:

        print(str(e))
        config.useHSV = False

        config.fg_minHue = 0
        config.fg_maxHue = 360
        config.fg_minSaturation = 1
        config.fg_maxSaturation = 1
        config.fg_minValue = 1
        config.fg_maxValue = 1


        config.bg_minHue = 0
        config.bg_maxHue = 360
        config.bg_minSaturation = 1
        config.bg_maxSaturation = 1
        config.bg_minValue = 1
        config.bg_maxValue = 1
        
        
        
        
        


    if config.useBackground == True:
        configureBackgroundScrolling()


    try:
        config.useText = workConfig.getboolean("scroller", "useText")
        config.useAltText = workConfig.getboolean("scroller", "useAltText")
        if config.useText == True:
            configureMessageScrolling()
        if config.useAltText == True:
            configureAltTextScrolling()
    except Exception as e:
        print(str(e))

    try:
        config.useOverLayImage = workConfig.getboolean("scroller", "useOverLayImage")
        if config.useOverLayImage == True:
            configureImageOverlay()
    except Exception as e:
        config.useOverLayImage = False
        print(str(e))

    try:
        config.useArrows = workConfig.getboolean("scroller", "useArrows")
        if config.useArrows == True:
            configureArrowScrolling()
    except Exception as e:
        print(str(e))

    try:
        config.useUltraSlowSpeed = workConfig.getboolean(
            "scroller", "useUltraSlowSpeed"
        )
    except Exception as e:
        config.useUltraSlowSpeed = False
        print(str(e))

    try:
        config.useImages = workConfig.getboolean("scroller", "useImages")
        config.useTransparentImages = workConfig.getboolean(
            "scroller", "useTransparentImages"
        )
        if config.useImages == True:
            configureImageScrolling()
    except Exception as e:
        print(str(e))

    try:
        config.doingRefreshCount = float(
            workConfig.get("scroller", "doingRefreshCount")
        )
    except Exception as e:
        config.doingRefreshCount = 50
        print(str(e))


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




    config.renderImageFull = config.workImage.copy()
    config.f = FaderObj()
    config.f.setUp(config.renderImageFull, config.workImage)
    config.f.doingRefreshCount = config.doingRefreshCount
    # config.workImageDraw.rectangle((0,0,100,100), fill=(100,0,0,100))
    config.renderImageFullOld = config.renderImageFull.copy()
    config.fadingDone = True

    config.useFadeThruAnimation = True
    config.deltaTimeDone = True

    try:
        config.useFadeThruAnimation = workConfig.getboolean("scroller", "useFadeThruAnimation")
    except Exception as e:
        print(str(e))
        config.useFadeThruAnimation = True


def runWork():
    global config
    print(bcolors.OKGREEN + "** " + bcolors.BOLD)
    print("RUNNING Scroller Holder scroller-holder.py")
    print(bcolors.ENDC)
    while config.isRunning == True:
        iterate()
        time.sleep(config.redrawSpeed)
        if config.standAlone == False :
            config.callBack()


def checkTime(scrollerObj):
    config.t2 = time.time()
    delta = config.t2 - config.t1

    if delta > config.timeToComplete and config.deltaTimeDone == False:

        scrollerObj.xSpeed -= 0.2

        if scrollerObj.xSpeed <= 0.70:
            config.deltaTimeDone = True
            config.useFadeThruAnimation = True
            config.f.fadingDone = True

            # print ("DELTA TIME UP")
            processImageForScrolling()
            if config.useUltraSlowSpeed == True:
                scrollerObj.xSpeed = 1


def processImageForScrolling():
    ## Run through each of the objects being scrolled - text, image, background etc
    for scrollerObj in config.scrollArray:
        scrollerObj.scroll()
        config.canvasImage.paste(scrollerObj.canvas, (0, 0), scrollerObj.canvas)

    # Chop up the scrollImage into "rows"
    for n in range(0, config.displayRows):
        segment = config.canvasImage.crop(
            (
                n * config.canvasWidth,
                0,
                config.canvasWidth + n * config.canvasWidth,
                config.bandHeight,
            )
        )

        if (
            (n % 2 == 0)
            and (config.displayRows > 1)
            and config.altDirectionScrolling == True
        ):
            segment = ImageOps.flip(segment)
            segment = ImageOps.mirror(segment)

        config.workImage.paste(segment, (0, n * config.bandHeight))

    if config.useOverLayImage == True:
        if random.random() < config.overlayGlitchRate:
            glitchBox(
                config.loadedImage, -config.overlayGlitchSize, config.overlayGlitchSize
            )
        if random.random() < config.overlayResetRate:
            config.loadedImage.paste(config.loadedImageCopy)
        config.workImage.paste(
            config.loadedImage,
            (config.overLayXPos, config.overLayYPos),
            config.loadedImage,
        )

    if config.overallBlur != 0:
        config.workImage = config.workImage.filter(
            ImageFilter.GaussianBlur(radius=config.overallBlur)
        )


def iterate():
    global config

    # config.workImageDraw.rectangle((0,0,config.canvasWidth,config.canvasHeight), fill  = (0,0,0))
    # config.canvasImageDraw.rectangle((0,0,config.canvasWidth*10,config.canvasHeight), fill  = (0,0,0,20))

    for scrollerObj in config.scrollArray:
        if scrollerObj.typeOfScroller == "bg":
            if (
                random.random() < config.changeProb * config.changeProbReleaseFactor
                and config.deltaTimeDone == True
                and config.useFadeThruAnimation == True
            ):
                config.useFadeThruAnimation = False
                scrollerObj.xSpeed = random.uniform(0.6, scrollerObj.xMaxSpeed)
                config.deltaTimeDone = False
                config.t1 = time.time()
                config.timeToComplete = random.uniform(3, 10)
            checkTime(scrollerObj)

    if config.useFadeThruAnimation == True and config.useUltraSlowSpeed == True:
        if config.f.fadingDone == True:

            config.renderImageFullOld = config.renderImageFull.copy()
            config.renderImageFull.paste(
                config.workImage,
                (config.imageXOffset, config.imageYOffset),
                config.workImage,
            )
            config.f.xPos = config.imageXOffset
            config.f.yPos = config.imageYOffset
            # config.renderImageFull = config.renderImageFull.convert("RGBA")
            # renderImageFull = renderImageFull.convert("RGBA")
            config.f.setUp(
                config.renderImageFullOld.convert("RGBA"),
                config.workImage.convert("RGBA"),
            )
            processImageForScrolling()

        config.f.fadeIn()
        config.render(config.f.blendedImage, 0, 0)

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
    global config, threads, thrd
    init()

    if run:
        runWork()


### Kick off .......
if __name__ == "__main__":
    main()