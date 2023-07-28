#!/usr/bin/python
import argparse
import math
import random
import time
import types
from modules.configuration import bcolors
from modules import badpixels, coloroverlay, colorutils, panelDrawing
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps, ImageFilter
import numpy as np


def runningSpiral(config):
    # 16px grid box spiral for now
    w = 4
    h = 4
    x = config.xIncrementer
    y = config.yIncrementer

    clr = tuple(
        int(a * config.brightness) for a in (config.linecolOverlay.currentColor)
    )

    clr2 = tuple(
        int(a * config.brightness) for a in (config.linecolOverlay2.currentColor)
    )

    config.blockDraw.rectangle(
        (0, 0, config.blockWidth, config.blockHeight), fill=config.bgColor, outline=None)

    lineMult = config.lineDiff * 2
    numLines = round(config.blockWidth / config.lineDiff * 2)

    d = 3
    direction = 1
    distance = 1

    mid = [config.blockWidth/2-1, config.blockHeight/2-1]

    p1 = [mid[0], mid[1]]
    p2 = [mid[0], mid[1]]

    # clr = (0,255,255)

    for i in range(0, numLines):
        distance += d
        p2[0] = p2[0] + distance * direction
        config.blockDraw.line((p1[0], p1[1], p2[0], p2[1]), fill=clr)
        p1[0] = p2[0]
        distance += d
        p2[1] = p2[1] + distance * direction
        config.blockDraw.line((p1[0], p1[1], p2[0], p2[1]), fill=clr)
        direction *= -1
        p1[1] = p2[1]

    direction = -1
    distance = 1

    p1 = [mid[0] + 1, mid[1] + 3]
    p2 = [mid[0] + 1, mid[1] + 3]

    # clr2 = (255,0,255)
    for i in range(0, numLines):
        distance += d
        p2[0] = p2[0] + distance * direction
        config.blockDraw.line((p1[0], p1[1], p2[0], p2[1]), fill=clr2)
        p1[0] = p2[0]
        distance += d
        p2[1] = p2[1] + distance * direction
        config.blockDraw.line((p1[0], p1[1], p2[0], p2[1]), fill=clr2)
        direction *= -1
        p1[1] = p2[1]


def balls(config):
    w = 4
    h = 4
    x = config.xIncrementer
    y = config.yIncrementer

    clr = tuple(
        int(a * config.brightness) for a in (config.linecolOverlay.currentColor)
    )

    clr2 = tuple(
        int(a * config.brightness) for a in (config.linecolOverlay2.currentColor)
    )

    config.blockDraw.rectangle(
        (0, 0, config.blockWidth, config.blockHeight), fill=config.bgColor, outline=None)

    numRows = config.numDotRows
    boxWidth = config.blockWidth
    density = numRows * 4
    dotWidth = boxWidth/2/numRows - 2
    outline = None

    for r in range(0, numRows):

        for i in range(0, density):
            yPos = r * (dotWidth * 2) + r * 4
            config.blockDraw.ellipse((
                i * 2 * boxWidth/density - boxWidth/density,
                yPos,
                i * 2 * boxWidth/density - boxWidth/density + dotWidth,
                yPos + dotWidth),
                outline=(outline), fill=clr)

        for i in range(0, density):
            config.blockDraw.ellipse((
                i * 2 * boxWidth/density,
                yPos + 2 * boxWidth/density,
                i * 2 * boxWidth/density + dotWidth,
                yPos + 2 * boxWidth/density + dotWidth),
                outline=(outline), fill=clr)


def circlesPacked(config):
    config.circlesPackedSize = 1
    clr = tuple(
        int(a * config.brightness) for a in (config.linecolOverlay.currentColor)
    )

    clr2 = tuple(
        int(a * config.brightness) for a in (config.linecolOverlay2.currentColor)
    )
    

    # config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=config.bgColor, outline=clr)

    numRows = config.numDotRows
    boxWidth = round(config.blockWidth * config.circlesPackedSize)
    dotWidth = boxWidth/2
    outline = clr
    steps=2
    yPos = 0
    numLines = config.blockWidth - 1
    for i in range(0, 4):
        xPos = i * dotWidth * 1 - dotWidth/2
        for r in range(0,numLines,steps):
            config.blockDraw.ellipse((
                r-1 + xPos,
                r-1 + yPos,
                xPos + dotWidth -1*r,
                yPos + dotWidth-1*r),
                outline=(outline), fill=config.bgColor)

    yPos = 2 * dotWidth/2 * math.sin(2 * math.pi / 6) + 2

    for i in range(0, 4):
        xPos = i * dotWidth * 1
        for r in range(0,numLines,steps):
            config.blockDraw.ellipse((
                r-1 + xPos,
                r-1 + yPos,
                xPos + dotWidth -1*r,
                yPos + dotWidth-1*r),
                outline=(outline), fill=config.bgColor)


def fishScales(config):
    w = 4
    h = 4
    x = config.xIncrementer
    y = config.yIncrementer

    clr = tuple(
        int(a * config.brightness) for a in (config.linecolOverlay.currentColor)
    )

    clr2 = tuple(
        int(a * config.brightness) for a in (config.linecolOverlay2.currentColor)
    )

    clr3 = config.colOverlay.currentColor

    config.blockDraw.rectangle(
        (0, 0, config.blockWidth, config.blockHeight), fill=clr3, outline=None)

    numRows = config.numShingleRows
    boxWidth = config.blockWidth/numRows

    for r in range(numRows, -1, -1):
        yPos = -2 + r * boxWidth
        for i in range(0, 3):
            config.blockDraw.ellipse((
                i * boxWidth - boxWidth/2,
                yPos,
                i * boxWidth + boxWidth - boxWidth/2,
                yPos + boxWidth),
                outline=(clr), fill=clr3)

        for i in range(0, 2):
            config.blockDraw.ellipse((
                i * boxWidth,
                yPos - boxWidth/2,
                i * boxWidth + boxWidth,
                yPos + boxWidth/2),
                outline=(clr), fill=clr3)


def waveScales(config):

    clr = tuple(
        int(a * config.brightness) for a in (config.linecolOverlay.currentColor)
    )

    clr2 = tuple(
        int(a * config.brightness) for a in (config.linecolOverlay2.currentColor)
    )

    clr3 = config.colOverlay.currentColor


    config.blockDraw.rectangle(
        (0, 0, config.blockWidth, config.blockHeight), fill=clr3, outline=None)

    numRows = config.numScaleRows
    numRows = 2
    boxWidth = 2*config.blockWidth/numRows

    rings = config.waveScaleRings 
    step = config.waveScaleSteps

    patternRows = numRows + 1
    startFirstSet = 0
    
    if config.linesOnly == True :
        config.altLineColoring = False
    # step= 5
    if config.altLineColoring == True and step != 2 :
        lineToUse =  clr
        startFirstSet = 1
    else :
        lineToUse = clr
    
    # lineToUse = clr
    # lineToUse = (255,0,0,204)
    # print(lineToUse,clr, clr2, clr3,config.altLineColoring,step,rings)
    
    # print(config.altLineColoring)
    for r in range(patternRows, -patternRows, -1):
        yPos = -2 + r * boxWidth
        xOffSet = -boxWidth/2
        yOffSet = boxWidth
        y = boxWidth/4 - r * boxWidth/2
        for i in range(0, 3):
            xSizeOfBox = i * boxWidth
            
            for n in range(startFirstSet, rings*step, step):
                if config.altLineColoring == True :
                    eo = n % 2
                    if eo  == 1 :
                        clrToUse = clr3
                    else :
                        clrToUse = clr2
                else :
                        clrToUse = clr3
                x0  =  xSizeOfBox + xOffSet + n   
                x1  =  xSizeOfBox + xOffSet + boxWidth - n
                y0 = yPos + 0 + n + y
                y1 = yPos + yOffSet - n  + y
                
                if y1 < y0 :
                    y1=y0
                
                if x1 < x0 :
                    x1 = x0   
                config.blockDraw.ellipse((
                    x0,
                    y0,
                    x1,
                    y1),
                    outline=(lineToUse), fill=clrToUse)

        xOffSet = 0
        yOffSet = yOffSet / 2
        y = boxWidth/2 - r * boxWidth/2

        for i in range(0, 2):
            xSizeOfBox = i * boxWidth
            for n in range(0, rings*step, step):
                if config.altLineColoring == True :
                    eo = n % 2
                    if eo  == 1 :
                        clrToUse = clr3
                    else :
                        clrToUse = clr2
                else :
                        clrToUse = clr3
                        
                x0 = xSizeOfBox + xOffSet + n
                x1 = xSizeOfBox + xOffSet + boxWidth - n
                y0 = yPos - yOffSet + n + y
                y1 = yPos + yOffSet - n + y
                
                if x1 < x0 :
                    x1 = x0
                
                if y1 < y0 :
                    y1= y0
                    
                config.blockDraw.ellipse((
                    x0,
                    y0,
                    x1,
                    y1),
                    outline=(lineToUse), fill=clrToUse)
                

def shingles(config):
    w = 4
    h = 4
    x = config.xIncrementer
    y = config.yIncrementer

    clr = tuple(
        int(a * config.brightness) for a in (config.linecolOverlay.currentColor)
    )

    clr2 = tuple(
        int(a * config.brightness) for a in (config.linecolOverlay2.currentColor)
    )

    clr2 = config.bgColor

    config.blockDraw.rectangle(
        (0, 0, config.blockWidth, config.blockHeight), fill=clr2, outline=None)

    numRows = config.numShingleRows
    boxWidth = config.blockWidth/numRows
    shingleWidth = config.blockWidth/numRows - config.shingleVariationAmount

    for r in range(numRows, -1, -1):
        yPos = -1 + r * boxWidth

        for i in range(0, 3):
            config.blockDraw.rectangle((
                i * boxWidth - boxWidth/2,
                yPos,
                i * boxWidth + shingleWidth - boxWidth/2,
                yPos + boxWidth-1),
                outline=(clr), fill=clr2)
        for i in range(0, 2):
            config.blockDraw.rectangle((
                i * boxWidth,
                yPos - boxWidth/2,
                i * boxWidth + shingleWidth,
                yPos + boxWidth/2 - 1),
                outline=(clr), fill=clr2)


def circles(config):
    w = 4
    h = 4
    x = config.xIncrementer
    y = config.yIncrementer

    clr = tuple(
        int(a * config.brightness) for a in (config.linecolOverlay.currentColor)
    )
    clr2 = tuple(
        int(a * config.brightness) for a in (config.linecolOverlay2.currentColor)
    )
    config.blockDraw.rectangle(
        (0, 0, config.blockWidth, config.blockHeight), fill=config.bgColor, outline=None)

    numLines = config.blockWidth - 1
    steps = 3
    for c in range(0,2):
        for r in range(0,2):
            xOff = c * config.blockWidth - config.blockWidth/2
            yOff = r * config.blockHeight - config.blockHeight/2
        
            for i in range(0, numLines, steps):
                config.blockDraw.ellipse((
                    i-1 + xOff,
                    i-1 + yOff,
                    config.blockWidth-1*i + xOff,
                    config.blockHeight-1*i + yOff),
                    outline=(clr), fill=None)


def compass(config):

    clr = tuple(
        int(a * config.brightness) for a in (config.linecolOverlay.currentColor)
    )
    clr2 = tuple(
        int(a * config.brightness) for a in (config.linecolOverlay2.currentColor)
    )

    config.blockDraw.rectangle(
        (0, 0, config.blockWidth, config.blockHeight), fill=config.bgColor, outline=None)

    count = 0
    barWidth = 4
    grid = round(config.blockWidth/16)
    len1 = 5
    len2 = 2
    
    origins  = ((0,0),
                (config.blockWidth,0),
                (round(config.blockWidth/2),round(config.blockWidth/2)),
                (0,config.blockWidth),
                (config.blockWidth,config.blockWidth),
                )
    
    outlineClr = None
    outlineClr = clr2
    for i in range(0,5) :

        midx = origins[i][0]
        midy = origins[i][1]
        
        isoTriangle  =  ((midx - grid,midy),
                        (midx,midy - len1 * grid),
                        (midx + grid,midy),
                        (midx, midy + len1 * grid),
                        (midx - grid,midy),
                        )
        config.blockDraw.polygon(isoTriangle, fill = clr, outline=outlineClr)
        isoTriangle  =  ((midx - grid * len1,midy),
                        (midx,midy - grid),
                        (midx + grid *len1,midy),
                        (midx,midy + grid),
                        (midx - grid * len1,midy),
                        )
        config.blockDraw.polygon(isoTriangle, fill = clr, outline=outlineClr)
        isoTriangle  =  ((midx - grid * len2, midy - grid * len2),
                        (midx, midy - grid),
                        (midx + grid *len2, midy - grid * len2),
                        (midx + grid, midy),
                        (midx + grid * len2, midy + grid * len2),
                        (midx, midy + grid),
                        (midx - grid * len2, midy + grid * len2),
                        (midx - grid, midy),
                        )
        config.blockDraw.polygon(isoTriangle, fill = clr, outline=outlineClr)
        

def bars(config):

    clr = tuple(
        int(a * config.brightness) for a in (config.linecolOverlay.currentColor)
    )
    clr2 = tuple(
        int(a * config.brightness) for a in (config.linecolOverlay2.currentColor)
    )

    config.blockDraw.rectangle(
        (0, 0, config.blockWidth, config.blockHeight), fill=config.bgColor, outline=None)

    count = 0
    barWidth = 4
    for i in range(0, config.numConcentricBoxes, 2):

        if config.altLineColoring == True:
            outClr = clr2
            if count % 2 == 0:
                outClr = clr
        else:
            outClr = clr
        config.blockDraw.rectangle((
            0,
            i * barWidth,
            config.blockWidth-1,
            i * barWidth),
            outline=(outClr), fill=None)
        count += 1


def concentricBoxes(config):

    clr = tuple(
        int(a * config.brightness) for a in (config.linecolOverlay.currentColor)
    )
    clr2 = tuple(
        int(a * config.brightness) for a in (config.linecolOverlay2.currentColor)
    )

    config.blockDraw.rectangle(
        (0, 0, config.blockWidth, config.blockHeight), fill=config.bgColor, outline=None)

    count = 0

    for i in range(0, config.numConcentricBoxes, 2):

        if config.altLineColoring == True:
            outClr = clr2
            if count % 2 == 0:
                outClr = clr
        else:
            outClr = clr
        config.blockDraw.rectangle((
            i-1,
            i-1,
            config.blockWidth-1*i,
            config.blockHeight-1*i),
            outline=(outClr), fill=None)
        count += 1


def decoBoxes(config):

    clr = tuple(
        int(a * config.brightness) for a in (config.linecolOverlay2.currentColor)
    )
    clr2 = tuple(
        int(a * config.brightness) for a in (config.linecolOverlay.currentColor)
    )

    config.blockDraw.rectangle(
        (0, 0, config.blockWidth, config.blockHeight), fill=config.bgColor, outline=None)

    clr = config.bgColor
    # clr = (50,50,50)
    # clr2 = (250,250,250)
    count = 0
    numConcentricBoxes = config.blockWidth+1
    altLineColoring = True
    w = round(random.uniform(2, 5))
    w = config.decoBoxBandWidth
    width = config.blockWidth

    blockWidth = width
    blockHeight = width
    halfSide = width/2

    diagonal = round(math.sqrt(halfSide*halfSide*2))
    diagonal = width

    temp = Image.new("RGBA", (width*3, width*3))
    tempDraw = ImageDraw.Draw(temp)

    temp2 = Image.new("RGBA", (width, width))
    temp2Draw = ImageDraw.Draw(temp2)

    # print(diagonal)

    for i in range(1, numConcentricBoxes, 1):

        if altLineColoring == True:
            outClr = clr2
            if count % 2 == 0:
                outClr = clr
        else:
            outClr = clr
         
        x1 = width-w*i   
        y1 = width-w*i
        
        if y1 < 0 :
            y1 = 0

        if x1 < 0 :
            x1 = 0
        temp2Draw.rectangle((
            0,
            0,
            x1,
            y1),
            outline=(None), fill=outClr)
        count += 1

    for c in range(0, 4):
        for r in range(0, 4):
            # temp = temp.rotate(-45)
            xOff = c*w
            yOff = r*w
            temp.paste(temp2, (c * diagonal - xOff, r * diagonal-yOff), temp2)

    szFactor = 1/3
    temp = temp.rotate(135, expand=True,)
    # print(temp)
    ex = 12
    temp = temp.resize((round(width/szFactor)+ex, round(width/szFactor)+ex))

    # print(temp)
    # print('')

    xOff = -round(width/1)
    yOff = -round(width/1)

    config.blockImage.paste(temp, (xOff, yOff), temp)


def randomizer(config):

    w = config.randomBlockWidth
    h = config.randomBlockHeight

    config.blockDraw.rectangle(
        (0, 0, config.blockWidth, config.blockHeight), fill=config.bgColor, outline=None)

    rows = config.blockHeight
    cols = config.blockWidth

    step = w
    hStep = h

    if w == 0:
        step = 1
    if h == 0:
        hStep = 1

    for r in range(0, rows, hStep):
        for c in range(0, cols, step):
            clr = colorutils.getRandomRGB(config.brightness/2)
            if random.random() < config.randomBlockProb:
                config.blockDraw.rectangle(
                    (c, r, w+c, h+r), fill=(clr), outline=None)


def diamond(config):
    clr = tuple(
        int(a * config.brightness) for a in (config.linecolOverlay.currentColor))

    x = config.xIncrementer
    y = config.yIncrementer

    # needs to be in odd grid
    config.blockDraw.rectangle(
        (0, 0, config.blockWidth, config.blockHeight), fill=config.bgColor, outline=None)

    step = config.diamondStep
    row = 1
    delta = 0
    w = 0
    h = 0
    rows = config.numRows
    blockHeight = round(config.blockHeight/rows)
    mid = round(blockHeight/2)

    for rw in range(0, rows):
        for c in range(0, rows):
            for i in range(0, blockHeight, step*2):
                for r in range(0, row, 1):
                    x = r + mid - row/2 + c * blockHeight
                    y = i + config.yIncrementer + rw * blockHeight

                    if y >= blockHeight*rows:
                        y -= blockHeight*rows

                    if (r % 2) != 1:
                        config.blockDraw.rectangle(
                            (x, y, w+x, h+y), fill=(clr), outline=None)
                if config.diamondUseTriangles == False:
                    row = 2 * i + step + delta
                    if i > (blockHeight/2):
                        row = round(2 * (blockHeight-i)) + delta
                        # delta += -2
                else:
                    row = i + step

    '''
	imgPart1  = config.blockImage.crop((config.blockWidth-1, 0, config.blockWidth, config.blockHeight))
	imgPart2  = config.blockImage.crop((0, 0, config.blockWidth-1, config.blockHeight))

	config.blockImage.paste(imgPart2, (1,0), imgPart2)
	config.blockImage.paste(imgPart1, (0,0), imgPart1)
	'''

    config.yIncrementer += config.ySpeed

    if config.yIncrementer >= blockHeight*2:
        config.yIncrementer = 0


def diagonalMove(config):
    clr = (255, 0, 0, 210)
    w = 4
    h = 4
    x = config.xIncrementer
    y = config.yIncrementer

    config.blockDraw.rectangle(
        (0, 0, config.blockWidth, config.blockHeight), fill=config.bgColor, outline=None)
    config.blockDraw.rectangle((x, y, w+x, h+y), fill=(clr), outline=None)
    config.xIncrementer += 1
    config.yIncrementer += 1

    if config.xIncrementer >= config.blockWidth - 4:
        config.xIncrementer = 0
    if config.yIncrementer >= config.blockHeight - 4:
        config.yIncrementer = 0


def reMove(config):

    w = 4
    h = 4
    x = config.xIncrementer
    y = config.yIncrementer

    bgColor = (config.bgColor[0], config.bgColor[1], config.bgColor[3], 255)

    clr = tuple(
        int(a * config.brightness) for a in (config.linecolOverlay.currentColor)
    )
    clr2 = tuple(
        int(a * config.brightness) for a in (config.linecolOverlay2.currentColor)
    )

    config.blockDraw.rectangle(
        (0, 0, config.blockWidth, config.blockHeight), fill=config.bgColor, outline=None)

    lineMult = config.lineDiff * 2
    numLines = round(config.blockWidth / config.lineDiff * 2)

    for i in range(0, numLines):

        x1 = -2*config.blockWidth + config.xIncrementer + i * lineMult
        y1 = 0
        x2 = -2*config.blockWidth + config.blockWidth + config.xIncrementer + i * lineMult
        y2 = config.blockHeight

        config.blockDraw.line((x1, y1, x2, y2), fill=(clr))
        if config.useDoubleLine == True:
            config.blockDraw.line((-2*config.blockWidth + config.xIncrementer + i * lineMult + 1, 0, -2*config.blockWidth +
                                   config.blockWidth + config.xIncrementer + i * lineMult + 1, config.blockHeight), fill=(clr2))

    config.xIncrementer += 0  # config.xSpeed
    config.yIncrementer += 0

    '''
	'''
    if config.xIncrementer > (config.blockWidth + 0):
        config.xIncrementer = -config.xSpeed
    if config.yIncrementer >= config.blockHeight - 4:
        config.yIncrementer = 0


def wavePattern(config):
    w = 4
    h = 4
    x = config.xIncrementer
    y = config.yIncrementer

    clr = tuple(
        int(a * config.brightness) for a in (config.linecolOverlay.currentColor)
    )
    clr2 = tuple(
        int(a * config.brightness) for a in (config.linecolOverlay2.currentColor)
    )

    config.blockDraw.rectangle(
        (0, 0, config.blockWidth, config.blockHeight), fill=config.bgColor, outline=config.bgColor)

    numPoints = round(config.blockWidth)
    amplitude = config.amplitude
    yOffset = config.yOffset
    amplitude2 = config.amplitude2
    yOffset2 = config.yOffset2
    steps = config.steps
    steps2 = config.steps2
    rads = 2 * 22/7 / numPoints

    for i in range(0, numPoints, steps):
        angle = (i + config.xIncrementer) * rads
        angle2 = (i + config.xIncrementer + steps) * rads
        a = (i, math.sin(angle) * amplitude + yOffset)
        b = (i + steps, math.sin(angle) * amplitude + yOffset)
        c = (i + steps, math.sin(angle2) * amplitude + yOffset)

        if c[1] < a[1]:
            b = (i, math.sin(angle2) * amplitude + yOffset)
        config.blockDraw.polygon((a, b, c, a), fill=clr, outline=None)

    phase = round(config.blockWidth/config.phaseFactor)
    for i in range(0, numPoints, steps2):
        angle = (i - config.speedFactor*config.xIncrementer + phase) * rads
        angle2 = (i - config.speedFactor *
                  config.xIncrementer + phase + steps2) * rads
        a = (i, math.cos(angle) * amplitude2 + yOffset2)
        b = (i + steps2, math.cos(angle) * amplitude2 + yOffset2)
        c = (i + steps2, math.cos(angle2) * amplitude2 + yOffset2)

        if c[1] < a[1]:
            b = (i, math.cos(angle2) * amplitude2 + yOffset2)
        config.blockDraw.polygon((a, b, c, a), fill=clr2, outline=None)

    config.xIncrementer += config.xSpeed
    config.yIncrementer += config.ySpeed

    if config.xIncrementer >= config.blockWidth * 1:
        config.xIncrementer = -0
    if config.yIncrementer >= config.blockHeight - 4:
        config.yIncrementer = 0
