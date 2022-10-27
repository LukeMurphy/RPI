# ################################################### #
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

    #clr = (0,255,255)

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

    #clr2 = (255,0,255)
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

    clr2 = config.bgColor

    config.blockDraw.rectangle(
        (0, 0, config.blockWidth, config.blockHeight), fill=clr2, outline=None)

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
                outline=(clr), fill=clr2)

        for i in range(0, 2):
            config.blockDraw.ellipse((
                i * boxWidth,
                yPos - boxWidth/2,
                i * boxWidth + boxWidth,
                yPos + boxWidth/2),
                outline=(clr), fill=clr2)


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

    numLines = 1
    for i in range(0, numLines):
        config.blockDraw.ellipse((
            i-1,
            i-1,
            config.blockWidth-1*i,
            config.blockHeight-1*i),
            outline=(clr), fill=clr2)


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
                        #delta += -2
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

    bgColor = (config.bgColor[0], config.bgColor[1], config.bgColor[2], 255)

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


###############################################

def redraw(config):

    if config.patternModel == "wavePattern":
        wavePattern(config)

    if config.patternModel == "reMove":
        reMove(config)

    if config.patternModel == "diagonalMove":
        diagonalMove(config)

    if config.patternModel == "randomizer":
        randomizer(config)

    if config.patternModel == "runningSpiral":
        runningSpiral(config)

    if config.patternModel == "concentricBoxes":
        concentricBoxes(config)

    if config.patternModel == "diamond":
        diamond(config)

    if config.patternModel == "shingles":
        shingles(config)

    if config.patternModel == "balls":
        balls(config)

    if config.patternModel == "bars":
        bars(config)


def repeatImage(config):
    cntr = 0
    # 2021-06-28 Opted to build the repetition/tiling vertically instead of horizontally
    # to suit the graph piece better and upwards or downwards is better than sideways sometimes
    # so reversed the order of "for c in ..." with "for r in range(..." so builds rows vertically

    # 2022-07-12 Changed my mind because the graph piece is not going to get this code - going for a
    # tower configuration

    for c in range(0, config.cols):
        for r in range(0, config.rows):
            if cntr in config.skipBlocks:
                config.canvasDraw.rectangle((c * config.blockWidth, r * config.blockHeight, c * config.blockWidth + config.blockWidth,
                                             r * config.blockHeight + config.blockHeight), fill=config.bgColor, outline=config.bgColor)
            else:
                temp = config.blockImage.copy()
                temp = temp.rotate(90)
                if c % 2 != 0 and config.rotateAltBlock == 1:
                    temp = temp.rotate(-90)

                config.canvasImage.paste(temp, (c * config.blockWidth-c, r * config.blockHeight-r), temp)

            if config.patternModelVariations == True:
                for s in config.patternSequence:
                    if cntr == s[1]:
                        config.patternModel = s[0]
                        config.rotateAltBlock = s[2]
                        func = eval(s[0])
                        func(config)

            cntr += 1


def rebuildSections():
    global config

    #print("REBUILDSECTIONS RUNNING NOW")

    for i in range(0, config.numberOfSections):
        section = config.movingSections[i]
        section.sectionRotation = random.uniform(-config.sectionRotationRange, config.sectionRotationRange)
        section.sectionPlacement = [round(random.uniform(config.sectionPlacementXRange[0], config.sectionPlacementXRange[1])), round(
            random.uniform(config.sectionPlacementYRange[0], config.sectionPlacementYRange[1]))]
        section.sectionPlacementInit = [section.sectionPlacement[0], section.sectionPlacement[1]]
        section.sectionSize = [round(random.uniform(config.sectionWidthRange[0], config.sectionWidthRange[1])), round(
            random.uniform(config.sectionHeightRange[0], config.sectionHeightRange[1]))]
        section.sectionSpeed = [random.uniform(-.1, .1)/config.sectionSpeedFactorHorizontal,
                                random.uniform(-.1, .1)/config.sectionSpeedFactorVertical]
        section.rotationSpeed = random.uniform(-.1, .1)
        section.actionCount = 0
        section.actionCountLimit = round(random.uniform(10, config.sectionMovementCountMax))
        section.done = False
        section.stopProb = random.uniform(0, config.stopProb)
    config.drawingPrinted = False


def rebuildPatternSequence(config):

    config.patternSequence = []
    numberOfPatterns = round(random.uniform(2, 4))
    config.numConcentricBoxes = round(random.uniform(8, 18))
    lastPosition = 0
    totalSlots = config.rows * config.cols

    if random.random() < .5:
        config.altLineColoring = True
    else:
        config.altLineColoring = False

    # for i in range(0,numberOfPatterns) :
    i = 0
    usedPatterns = []
    while i < numberOfPatterns:
        pattern = config.patterns[math.floor(random.uniform(0, len(config.patterns)))]

        if pattern not in usedPatterns:
            if pattern not in (["shingles", "fishScales", "balls"]):
                rotate = round(random.uniform(0, 1))
            else:
                rotate = 0
            slotsLeft = totalSlots - lastPosition
            position = round(random.uniform(lastPosition, slotsLeft-1))
            config.patternSequence.append([pattern, position, rotate])
            usedPatterns.append(pattern)
            lastPosition = position
            i += 1


def loadImageForBase():
    #image = Image.open("./assets/imgs/drawings/P1060494.jpg", "r")
    #image = Image.open("./assets/imgs/miscl/comp-384.jpg", "r")
    #image = Image.open("./assets/imgs/miscl/lm_a.png", "r")

    i = math.floor(random.random() * len(config.imageSources))
    imagePath  = config.imageSources[i]
    print(imagePath)
    image = Image.open(imagePath)
    image.load()
    config.canvasImage.paste(image, (0, 0))


def getConfigOverlay(tLimitBase, minHue, maxHue, minSaturation, maxSaturation, minValue, maxValue):
    colOverlay = coloroverlay.ColorOverlay()
    colOverlay.randomSteps = False
    colOverlay.timeTrigger = True
    colOverlay.tLimitBase = tLimitBase
    colOverlay.maxBrightness = 1
    colOverlay.steps = 50
    colOverlay.minHue = minHue
    colOverlay.maxHue = maxHue
    colOverlay.minSaturation = minSaturation
    colOverlay.maxSaturation = maxSaturation
    colOverlay.minValue = minValue
    colOverlay.maxValue = maxValue
    colOverlay.colorTransitionSetup()
    return colOverlay


def buildPalette(config, index=0):

    palette = config.palettes[index]

    tLimitBase = int(workConfig.get(palette, "tLimitBase"))
    minHue = float(workConfig.get(palette, "minHue"))
    maxHue = float(workConfig.get(palette, "maxHue"))
    minSaturation = float(workConfig.get(palette, "minSaturation")	)
    maxSaturation = float(workConfig.get(palette, "maxSaturation"))
    minValue = float(workConfig.get(palette, "minValue"))
    maxValue = float(workConfig.get(palette, "maxValue"))
    #config.colOverlay = getConfigOverlay(tLimitBase, minHue, maxHue, minSaturation, maxSaturation, minValue, maxValue)
    config.colOverlay = Holder()
    config.colOverlay.currentColor = [10, 10, 10, 100]
    config.colOverlay.currentColor = colorutils.getRandomColorHSV(minHue, maxHue, minSaturation, maxSaturation, minValue, maxValue, 0, 0,
                                                                  round(random.uniform(config.bgColorAlpha[0], config.bgColorAlpha[1])))
    config.colOverlay.bgColor = colorutils.getRandomColorHSV(
        minHue, maxHue, minSaturation, maxSaturation, minValue, maxValue)

    tLimitBase = int(workConfig.get(palette, "line_tLimitBase"))
    minHue = float(workConfig.get(palette, "line_minHue"))
    maxHue = float(workConfig.get(palette, "line_maxHue"))
    minSaturation = float(workConfig.get(palette, "line_minSaturation")	)
    maxSaturation = float(workConfig.get(palette, "line_maxSaturation"))
    minValue = float(workConfig.get(palette, "line_minValue"))
    maxValue = float(workConfig.get(palette, "line_maxValue"))
    #config.linecolOverlay = getConfigOverlay(tLimitBase, minHue, maxHue, minSaturation, maxSaturation, minValue, maxValue)
    config.linecolOverlay = Holder()
    config.linecolOverlay.currentColor = [200, 10, 10]
    config.linecolOverlay.currentColor = colorutils.getRandomColorHSV(
        minHue, maxHue, minSaturation, maxSaturation, minValue, maxValue)

    tLimitBase = int(workConfig.get(palette, "line2_tLimitBase"))
    minHue = float(workConfig.get(palette, "line2_minHue"))
    maxHue = float(workConfig.get(palette, "line2_maxHue"))
    minSaturation = float(workConfig.get(palette, "line2_minSaturation")	)
    maxSaturation = float(workConfig.get(palette, "line2_maxSaturation"))
    minValue = float(workConfig.get(palette, "line2_minValue"))
    maxValue = float(workConfig.get(palette, "line2_maxValue"))
    #config.linecolOverlay2 = getConfigOverlay(tLimitBase, minHue, maxHue, minSaturation, maxSaturation, minValue, maxValue)
    config.linecolOverlay2 = Holder()
    config.linecolOverlay2.currentColor = [10, 100, 10]
    config.linecolOverlay2.currentColor = colorutils.getRandomColorHSV(
        minHue, maxHue, minSaturation, maxSaturation, minValue, maxValue)

    #config.colOverlay.currentColor = colorutils.getRandomColorHSV(minHue, maxHue, minSaturation, maxSaturation, minValue, maxValue,0,0,200)
    #config.canvasDraw.rectangle((0,0,config.canvasWidth, config.canvasHeight), fill = config.colOverlay.currentColor)
    #config.colOverlay.currentColor = colorutils.getRandomColorHSV(minHue, maxHue, minSaturation, maxSaturation, minValue, maxValue,0,0,10)


def writeImage(baseName, renderImage):
    #baseName = "outputquad3/comp2_"
    if config.saveImages == True :
    	fn = baseName+".png"
    	renderImage.save(fn)


###############################################


class Holder:
    def __init__(self):
        pass


class Director:
    """docstring for Director"""

    slotRate = .5

    def __init__(self, config):
        super(Director, self).__init__()
        self.config = config
        self.tT = time.time()

    def checkTime(self):
        if (time.time() - self.tT) >= self.slotRate:
            self.tT = time.time()
            self.advance = True
        else:
            self.advance = False

    def next(self):
        self.checkTime()


def runWork():
    global config
    print(bcolors.OKGREEN + "** " + bcolors.BOLD)
    print("Running repeatblocks.py")
    print(bcolors.ENDC)
    while config.isRunning == True:
        config.directorController.checkTime()
        if config.directorController.advance == True:
            iterate()
        time.sleep(config.redrawSpeed)
        if config.standAlone == False:
            config.callBack()


def iterate():
    global config
    # config.colOverlay.stepTransition()
    # config.linecolOverlay.stepTransition()
    # config.linecolOverlay2.stepTransition()

    config.bgColor = tuple(
        round(a * config.brightness) for a in (config.colOverlay.currentColor)
    )

    if config.repeatDrawingMode == 1:
        redraw(config)

        if random.random() < config.loadAnImageProb:
            loadImageForBase()
        else:
            repeatImage(config)

        config.repeatDrawingMode = 0

    if random.random() < .005 and config.usePixelSortRandomize == True:
        config.usePixelSort = False
    if random.random() < .005 and config.usePixelSortRandomize == True:
        config.usePixelSort = True

    if config.randomizeSpeed == True:

        if random.random() < .03:
            config.ySpeed = config.ySpeedInit

        if random.random() < .1:
            config.ySpeed = 0

    if random.random() < .0005:
        config.triangles = True

    if random.random() < .01:
        config.triangles = False

    if random.random() < config.rebuildPatternProbability:
        rebuildPatternSequence(config)
        config.repeatDrawingMode = 1
        rebuildSections()

    if random.random() < config.rebuildPatternProbability:
        newPalette = math.floor(random.uniform(0, len(config.palettes)))
        if newPalette == len(config.palettes):
            newPalette = 0
        buildPalette(config, newPalette)
        config.repeatDrawingMode = 1
        rebuildSections()

    if random.random() < config.rebuildPatternProbability:
        if config.numRowsRandomize == True:
            config.numRows = round(random.uniform(1, 2))
            config.numShingleRows = round(random.uniform(1, 2))
            dotRows = [1, 2, 4]
            config.numDotRows = dotRows[round(random.uniform(0, 2))]
        config.repeatDrawingMode = 1
        rebuildSections()

    # RANDOM OVERLAY REPETITION DISTURBANCE
    if random.random() < config.rebuildPatternProbability and config.sectionDisturbance == True:
        rebuildSections()

    if config.shingleVariation == True:
        if random.random() < config.rebuildPatternProbability:
            config.shingleVariationAmount = round(random.uniform(0, config.shingleVariationRange))
            rebuildSections()

    if config.useDrawingPoints == True:
        config.panelDrawing.canvasToUse = config.canvasImage
        config.panelDrawing.render()
    else:

        # paste over a section of the image on to itself and rotate
        if config.sectionDisturbance == True:
            doneCoount = 0
            for i in range(0, config.numberOfSections):
                sectionParams = config.movingSections[i]
                if sectionParams.actionCount > sectionParams.actionCountLimit:
                    #sectionParams.rotationSpeed = 0
                    #sectionParams.sectionSpeed[0] = 0
                    #sectionParams.sectionSpeed[1] = 0
                    doneCoount += 1
                #else:

                xPos = round(sectionParams.sectionPlacementInit[0])
                yPos = round(sectionParams.sectionPlacementInit[1])
                section = config.canvasImage.crop(
                    (xPos, yPos, xPos + sectionParams.sectionSize[0], yPos + sectionParams.sectionSize[1]))
                '''
				section = section.rotate(sectionParams.sectionRotation, Image.NEAREST, True)
				sectionParams.sectionRotation += sectionParams.rotationSpeed
				'''

                config.canvasImage.paste(section, (round(sectionParams.sectionPlacement[0]), round(
                    sectionParams.sectionPlacement[1])), section)

                sectionParams.sectionPlacement[0] += sectionParams.sectionSpeed[0]
                sectionParams.sectionSpeed[0] *= .9

                sectionParams.sectionPlacement[1] += sectionParams.sectionSpeed[1]
                sectionParams.sectionSpeed[1] *= .9

                sectionParams.actionCount += 1

                if random.random() < sectionParams.stopProb:
                    sectionParams.rotationSpeed = 0
                if random.random() < sectionParams.stopProb:
                    sectionParams.sectionSpeed[0] = 0
                if random.random() < sectionParams.stopProb:
                    sectionParams.sectionSpeed[1] = 0

            if doneCoount >= config.numberOfSections and config.drawingPrinted == False:
                config.drawingPrinted = True
                currentTime = time.time()
                baseName = config.outPutPath + str(currentTime)
                writeImage(baseName, renderImage=config.canvasImage)

            #if doneCoount >= (config.numberOfSections ):
            #    rebuildSections()

        # a blurred section distrubance
        if config.useBlurSection == True:
            cp = config.canvasImage.copy()
            mask_blur = config.mask.filter(ImageFilter.GaussianBlur(config.mask_blur_amt))
            cp_blur = cp.filter(ImageFilter.GaussianBlur(config.cp_blur_amt))
            config.canvasImage = Image.composite(cp_blur, config.canvasImage, mask_blur)

        temp1 = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
        temp1Draw = ImageDraw.Draw(temp1)
        temp1Draw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=config.colOverlay.bgColor)
        temp1.paste(config.canvasImage, (0, 0), config.canvasImage)
        config.render(temp1, 0, 0, config.canvasWidth, config.canvasHeight)
    # Done


def main(run=True):
    global config
    config.redrawSpeed = float(workConfig.get("movingpattern", "redrawSpeed"))
    config.blockWidth = int(workConfig.get("movingpattern", "blockWidth"))
    config.blockHeight = int(workConfig.get("movingpattern", "blockHeight"))
    config.rows = int(workConfig.get("movingpattern", "rows"))
    config.cols = int(workConfig.get("movingpattern", "cols"))
    config.lineDiff = int(workConfig.get("movingpattern", "lineDiff"))

    config.useDoubleLine = (workConfig.getboolean("movingpattern", "useDoubleLine"))

    config.randomizeSpeed = (workConfig.getboolean("movingpattern", "randomizeSpeed"))

    config.patternModel = (workConfig.get("movingpattern", "patternModel"))
    config.steps = int(workConfig.get("movingpattern", "steps"))
    config.steps2 = int(workConfig.get("movingpattern", "steps2"))
    config.amplitude = int(workConfig.get("movingpattern", "amplitude"))
    config.amplitude2 = int(workConfig.get("movingpattern", "amplitude2"))
    config.yOffset = int(workConfig.get("movingpattern", "yOffset"))
    config.yOffset2 = int(workConfig.get("movingpattern", "yOffset2"))

    config.speedFactor = float(workConfig.get("movingpattern", "speedFactor"))
    config.phaseFactor = float(workConfig.get("movingpattern", "phaseFactor"))
    config.xSpeed = float(workConfig.get("movingpattern", "xSpeed"))
    config.ySpeed = float(workConfig.get("movingpattern", "ySpeed"))
    config.ySpeedInit = float(workConfig.get("movingpattern", "ySpeed"))

    skipBlocks = (workConfig.get("movingpattern", "skipBlocks")).split(",")
    config.skipBlocks = tuple(map(lambda x: int(int(x)), skipBlocks))

    config.diamondUseTriangles = False
    config.diamondStep = int(workConfig.get("movingpattern", "diamondStep"))

    config.numConcentricBoxes = int(workConfig.get("movingpattern", "numConcentricBoxes"))

    config.randomBlockProb = float(workConfig.get("movingpattern", "randomBlockProb"))
    config.randomBlockWidth = int(workConfig.get("movingpattern", "randomBlockWidth"))
    config.randomBlockHeight = int(workConfig.get("movingpattern", "randomBlockHeight"))

    config.repeatProb = .99

    config.xIncrementer = 0
    config.yIncrementer = 0

    config.altLineColoring = True

    config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.canvasDraw = ImageDraw.Draw(config.canvasImage)

    config.blockImage = Image.new("RGBA", (config.blockWidth, config.blockHeight))
    config.blockDraw = ImageDraw.Draw(config.blockImage)

    config.destinationImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight)
                                        )

    config.rotateAltBlock = 0

    try:
        config.numRows = int(workConfig.get("movingpattern", "numRows"))
        config.numRowsRandomize = (workConfig.getboolean("movingpattern", "numRowsRandomize"))
    except Exception as e:
        config.numRows = 1
        config.numRowsRandomize = False
        print(str(e))

    try:
        config.numDotRows = int(workConfig.get("movingpattern", "numDotRows"))
        config.numShingleRows = int(workConfig.get("movingpattern", "numShingleRows"))
    except Exception as e:
        config.numDotRows = config.numRows
        config.numShingleRows = config.numRows
        print(str(e))

    config.rebuildPatternProbability = float(workConfig.get("movingpattern", "rebuildPatternProbability"))
    config.patterns = workConfig.get("movingpattern", "patterns").split(",")

    try:
        config.patternModelVariations = workConfig.getboolean("movingpattern", "patternModelVariations")
        patternSequence = workConfig.get("movingpattern", "patternSequence").split(",")
        config.patternSequence = []
        for i in range(0, len(patternSequence), 3):
            config.patternSequence.append([patternSequence[i], int(patternSequence[i+1]), int(patternSequence[i+2])])
    except Exception as e:
        print(str(e))
        config.patternModelVariations = False
        config.patternSequence = []

    try:
        config.usePixelSortRandomize = (workConfig.getboolean("movingpattern", "usePixelSortRandomize"))
    except Exception as e:
        config.usePixelSortRandomize = False
        print(str(e))

    try:
        config.shingleVariation = (workConfig.getboolean("movingpattern", "shingleVariation"))
        config.shingleVariationRange = int(workConfig.get("movingpattern", "shingleVariationRange"))
        config.shingleVariationAmount = config.shingleVariationRange
    except Exception as e:
        config.shingleVariation = False
        config.shingleVariationRange = 0
        config.shingleVariationAmount = 0
        print(str(e))

    try:
        config.sectionDisturbance = (workConfig.getboolean("movingpattern", "sectionDisturbance"))

        config.sectionRotationRange = float(workConfig.get("movingpattern", "sectionRotationRange"))

        sectionPlacementXRange = workConfig.get("movingpattern", "sectionPlacementXRange").split(",")
        config.sectionPlacementXRange = tuple(map(lambda x: int(int(x)), sectionPlacementXRange))

        sectionPlacementYRange = workConfig.get("movingpattern", "sectionPlacementYRange").split(",")
        config.sectionPlacementYRange = tuple(map(lambda x: int(int(x)), sectionPlacementYRange))

        sectionWidthRange = workConfig.get("movingpattern", "sectionWidthRange").split(",")
        config.sectionWidthRange = tuple(map(lambda x: int(int(x)), sectionWidthRange))

        sectionHeightRange = workConfig.get("movingpattern", "sectionHeightRange").split(",")
        config.sectionHeightRange = tuple(map(lambda x: int(int(x)), sectionHeightRange))

        config.numberOfSections = int(workConfig.get("movingpattern", "numberOfSections"))
        config.sectionMovementCountMax = int(workConfig.get("movingpattern", "sectionMovementCountMax"))

        config.stopProb = float(workConfig.get("movingpattern", "stopProbMax"))
        config.sectionSpeedFactorHorizontal = float(workConfig.get("movingpattern", "sectionSpeedFactorHorizontal"))
        config.sectionSpeedFactorVertical = float(workConfig.get("movingpattern", "sectionSpeedFactorVertical"))
        config.movingSections = []
        for i in range(0, config.numberOfSections):
            section = Holder()
            config.movingSections.append(section)
        rebuildSections()

    except Exception as e:
        config.sectionDisturbance = False
        print(str(e))

    try:
        config.useBlurSection = (workConfig.getboolean("movingpattern", "useBlurSection"))
        config.blurSectionWidth = int(workConfig.get("movingpattern", "blurSectionWidth"))
        config.blurSectionHeight = int(workConfig.get("movingpattern", "blurSectionHeight"))
        config.blurSectionXPos = int(workConfig.get("movingpattern", "blurSectionXPos"))
        config.blurSectionYPos = int(workConfig.get("movingpattern", "blurSectionYPos"))
        config.mask_blur_amt = int(workConfig.get("movingpattern", "mask_blur_amt"))
        config.cp_blur_amt = int(workConfig.get("movingpattern", "cp_blur_amt"))

        config.mask = Image.new("L", config.canvasImage.size, 0)
        config.mask_draw = ImageDraw.Draw(config.mask)

        config.mask_draw.ellipse((config.blurSectionXPos, config.blurSectionYPos, config.blurSectionXPos +
                                  config.blurSectionWidth, config.blurSectionYPos + config.blurSectionHeight), fill=255)
        config.mask_blur_amt = config.mask_blur_amt
        config.cp_blur_amt = config.cp_blur_amt
    except Exception as e:
        print(str(e))
        config.useBlurSection = False

    config.palettes = workConfig.get("movingpattern", "palettes").split(",")
    bgColorAlpha = (workConfig.get("movingpattern", "bgColorAlpha")).split(",")
    config.bgColorAlpha = list(map(lambda x: (int(x)), bgColorAlpha))
    buildPalette(config, 0)

    # THIS IS USED AS WAY TO MOCKUP A CONFIGURATION OF RECTANGULAR PANELS
    panelDrawing.mockupBlock(config, workConfig)

    config.repeatDrawingMode = 1
    config.drawingPrinted = True
    config.saveImages = (workConfig.getboolean("movingpattern", "saveImages"))
    config.outPutPath = workConfig.get("movingpattern", "outPutPath")
    config.loadAnImageProb = float(workConfig.get("movingpattern", "loadAnImageProb"))
    config.imageSources = workConfig.get("movingpattern", "imageSources").split(',')

    config.directorController = Director(config)
    config.directorController.slotRate = .03

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


    if run:
        runWork()


###############################################

