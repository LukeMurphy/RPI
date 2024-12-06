# ################################################### #
import math
import random
import time
from modules.configuration import bcolors
from modules import coloroverlay, colorutils
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps


class Director:
    """docstring for Director"""

    targetSlotArray = []
    currentSlot = 0
    totalSlots = 0
    slotRate = 0.02
    advance = False
    color = [255, 255, 255]
    direction = 1

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


def newColor():
    return colorutils.getRandomColorHSV(
        config.bg_minHue,
        config.bg_maxHue,
        config.bg_minSaturation,
        config.bg_maxSaturation,
        config.bg_minValue,
        config.bg_maxValue,
        config.bg_dropHueMinValue,
        config.bg_dropHueMaxValue,
        round(random.uniform(config.bg_minAlpha, config.bg_maxAlpha)),
    )


def newColorAlt():
    return colorutils.getRandomColorHSV(
        config.line1_minHue,
        config.line1_maxHue,
        config.line1_minSaturation,
        config.line1_maxSaturation,
        config.line1_minValue,
        config.line1_maxValue,
        config.line1_dropHueMinValue,
        config.line1_dropHueMaxValue,
        round(random.uniform(config.line1_minAlpha, config.line1_maxAlpha)),
    )


def newColorAlt2():
    return colorutils.getRandomColorHSV(
        config.line2_minHue,
        config.line2_maxHue,
        config.line2_minSaturation,
        config.line2_maxSaturation,
        config.line2_minValue,
        config.line2_maxValue,
        config.line2_dropHueMinValue,
        config.line2_dropHueMaxValue,
        round(random.uniform(config.line2_minAlpha, config.line2_maxAlpha)),
    )


def generateInitialImage(dims):
    image = Image.new("RGBA", (config.blockWidth, config.blockHeight))
    draw = ImageDraw.Draw(image)

    clr = colorutils.getRandomColor()
    if random.SystemRandom().random() < .1 :
        # draw.rectangle((0,0,dims[0], dims[1]), fill=(255,0,0,200))
        draw.rectangle((0,0,dims[0], dims[1]), fill=clr)
    else :
        if random.SystemRandom().random() < .55 :
            draw.polygon(((0,0),(dims[0], dims[1]),(0, dims[1])), fill=clr)
            # draw.polygon(((0,0),(dims[0], dims[1]),(0, dims[1])), fill=(255,0,0,200))
            if random.SystemRandom().random() < .95 :
                draw.polygon(((0,0),(dims[0], dims[1]),(dims[0], 0)), fill=(255,255,250,200))
        else :
            draw.polygon(((0, dims[1]),(dims[0], 0),(dims[0],dims[1])), fill=(255,255,255,200))
            if random.SystemRandom().random() < .85 :
                draw.polygon(((0, dims[1]),(dims[0], 0),(0,0)), fill=(255,0,0,200))


    return image

def removeFromAvailable(lastX ,lastY, unitFills):
    for h in range(lastY, lastY+unitFills[1], config.gridSize) :
        for w in range(lastX, lastX+unitFills[0],  config.gridSize) :
            for ii in range(0, len(config.availableSpots)) :
                if config.availableSpots[ii][0] == w and config.availableSpots[ii][1] == h :
                    config.availableSpots[ii][2] = False

def linearPlacer(doSort = False):
    if doSort : config.unitFills = sorted(config.unitFills, key=lambda w: w[0] * w[1] , reverse=False)

    lastX = 0
    lastY = 0
    lastHighest = 0
    for i in range(0, len(config.unitFills)):
        img = generateInitialImage(config.unitFills[i])

        if (lastX + config.unitFills[i][0] + 0) > config.canvasWidth :
            lastX = 0
            lastY += lastHighest
            removeFromAvailable(lastX ,lastY, config.unitFills[i])
            lastHighest = config.unitFills[i][1]
            config.image.paste(img,(lastX ,lastY),img)

            lastX += config.unitFills[i][0] + 0
        else :
            config.image.paste(img,(lastX ,lastY),img)
            removeFromAvailable(lastX ,lastY, config.unitFills[i])
            lastX += config.unitFills[i][0] + 0

        if config.unitFills[i][1] >= lastHighest:
            lastHighest = config.unitFills[i][1]

def simplePlacer(doSort = False):
    if doSort : 
        config.unitFills = sorted(config.unitFills, key=lambda w: w[0] * w[1] , reverse=False)
    lastX = 0
    lastY = 0
    lastHighest = 0
    for i in range(0, len(config.unitFills)):
        img = generateInitialImage(config.unitFills[i])

        # searchRadius = math.ceil(math.sqrt(config.unitFills[i][0]*config.unitFills[i][0] + config.unitFills[i][1]*config.unitFills[i][1]))
        # print(searchRadius)
        insertIndex = 0
        canFit = False
        for s in range(0, len(config.availableSpots)) :
            if config.availableSpots[s][2] :
                sY = config.availableSpots[s][1]
                eY = config.availableSpots[s][1] + config.unitFills[i][1]
                sX = config.availableSpots[s][0]
                eX = config.availableSpots[s][0] + config.unitFills[i][0]
                keepGoing = True
                for h in range (sY, eY ,config.gridSize ) :
                    for w in range (sX, eX,config.gridSize ) :
                        if keepGoing :
                            indx = -1
                            try :
                                indx = config.availableSpots.index([w,h,True])
                            except ValueError :
                                indx = -1
                                # print("not found")
                            if indx != -1 : 
                                canFit = True
                                insertIndex = s
                            else :
                                canFit = False
                                keepGoing = False

                if canFit :
                    break


        if canFit :
            config.image.paste(img,(config.availableSpots[insertIndex][0] ,config.availableSpots[insertIndex][1]),img)
            removeFromAvailable(config.availableSpots[insertIndex][0] ,config.availableSpots[insertIndex][1], config.unitFills[i])


def drawGrid():
    # linearPlacer(True)
    # linearPlacer(False)

    doSort = False if random.SystemRandom().random() < .95 else True
    simplePlacer(doSort)

    # FOR DEBUGGING!
    # for i in range(0, len(config.availableSpots)) :
    #     if(config.availableSpots[i][2]) : 
    #         config.draw.rectangle((config.availableSpots[i][0], config.availableSpots[i][1],config.availableSpots[i][0]+1, config.availableSpots[i][1]+1), fill=(0,0,255))


def reDraw(config):
        if random.SystemRandom().random() < .1:
            rebuildGrid()
        setUp()
        drawGrid()


def iterate():
    global config, expandingRingsRing, lastRate, calibrated, cycleCount
    # config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))

    config.director.checkTime()
    if config.director.advance == True:
        # config.draw.rectangle(
        #     (0, 0, config.screenWidth, config.screenHeight), fill=config.backgroundColor
        # )
     
        # Do the final rendering of the composited image
        if random.random() < config.bgFlashRate:
            config.draw.rectangle(
                (0, 0, config.screenWidth, config.screenHeight),
                fill=config.backgroundFlashcolor,
            )
            reDraw(config)
        config.render(config.image, 0, 0, config.canvasWidth, config.canvasHeight)

    if random.random() < config.filterPatchProb:
        # print("should be remapping")
        config.useFilters = True
        x1 = round(random.uniform(0, config.canvasWidth))
        x2 = round(random.uniform(x1, config.canvasWidth))
        y1 = round(random.uniform(0, config.canvasHeight))
        y2 = round(random.uniform(y1, config.canvasHeight))

        config.remapImageBlock = True
        config.remapImageBlockSection = (x1, y1, x2, y2)
        config.remapImageBlockDestination = (x1, y1)

    # Don't want the patch to always be there - just little interruptions
    if random.random() < config.filterPatchProbOff:
        # print("turning off remapping")
        config.useFilters = False
        x1 = 0
        x2 = 0
        y1 = 0
        y2 = 0

        config.remapImageBlock = True
        config.remapImageBlockSection = (x1, y1, x2, y2)
        config.remapImageBlockDestination = (x1, y1)


def setUp():
    config.blockWidth = round(
        random.uniform(config.blockWidthMin, config.blockWidthMax)
    )
    config.blockHeight = round(
        random.uniform(config.blockHeightMin, config.blockHeightMax)
    )
    config.colGap = round(
        random.uniform(config.blockColSpacingMin, config.blockColSpacingMax)
    )
    config.rowGap = round(
        random.uniform(config.blockRowSpacingMin, config.blockRowSpacingMax)
    )
    config.angle = 0
    config.gridAngleIncrement = random.uniform(
        config.gridAngleIncrementMin, config.gridAngleIncrementMax
    )
    config.spiralAngleIncrement = random.uniform(
        config.spiralAngleIncrementMin, config.spiralAngleIncrementMax
    )
    config.repeatFactor = random.uniform(config.repeatFactorMin, config.repeatFactorMax)

    config.lineAColor = newColor()
    config.lineBColor = newColorAlt()
    config.lineCColor = newColorAlt2()

    config.gridCols = round(config.canvasWidth / config.blockWidth) + 2
    config.gridRows = round(config.canvasHeight / config.blockHeight) + 2

    # config.expandPaste = True if random.random() > .5 else False
    # config.figureType = "boxes" if random.random() > .5 else "lines"
    # config.patternType = "spiral" if random.random() > .5 else "grid"
    # config.elementNumber = round(random.uniform(1,3))
    config.availableSpots = []
    for h in range(0, config.canvasHeight, config.gridSize) :
        for w in range(0, config.canvasWidth, config.gridSize) :
            config.availableSpots.append([w,h,True])


def rebuildGrid():
    config.unitFills = []

    for i in range(0,config.unitsToDraw ) :
        config.unitFills.append((round(random.SystemRandom().uniform(config.minW,config.maxW))* config.gridSize, round(random.SystemRandom().uniform(config.minH,config.maxH))* config.gridSize) )


def main(run=True):
    global config
    global expandingRingss
    global workConfig

    expandingRingss = []
    config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.draw = ImageDraw.Draw(config.image)

    config.redrawSpeed = float(workConfig.get("forms", "redrawSpeed"))

    config.bg_minHue = float(workConfig.get("forms", "bg_minHue"))
    config.bg_maxHue = float(workConfig.get("forms", "bg_maxHue"))
    config.bg_minSaturation = float(workConfig.get("forms", "bg_minSaturation"))
    config.bg_maxSaturation = float(workConfig.get("forms", "bg_maxSaturation"))
    config.bg_minValue = float(workConfig.get("forms", "bg_minValue"))
    config.bg_maxValue = float(workConfig.get("forms", "bg_maxValue"))
    config.bg_dropHueMinValue = float(workConfig.get("forms", "bg_dropHueMinValue"))
    config.bg_dropHueMaxValue = float(workConfig.get("forms", "bg_dropHueMaxValue"))
    config.bg_minAlpha = float(workConfig.get("forms", "bg_minAlpha"))
    config.bg_maxAlpha = float(workConfig.get("forms", "bg_maxAlpha"))

    config.line1_minHue = float(workConfig.get("forms", "line1_minHue"))
    config.line1_maxHue = float(workConfig.get("forms", "line1_maxHue"))
    config.line1_minSaturation = float(workConfig.get("forms", "line1_minSaturation"))
    config.line1_maxSaturation = float(workConfig.get("forms", "line1_maxSaturation"))
    config.line1_minValue = float(workConfig.get("forms", "line1_minValue"))
    config.line1_maxValue = float(workConfig.get("forms", "line1_maxValue"))
    config.line1_dropHueMinValue = float(
        workConfig.get("forms", "line1_dropHueMinValue")
    )
    config.line1_dropHueMaxValue = float(
        workConfig.get("forms", "line1_dropHueMaxValue")
    )
    config.line1_minAlpha = float(workConfig.get("forms", "line1_minAlpha"))
    config.line1_maxAlpha = float(workConfig.get("forms", "line1_maxAlpha"))

    config.line2_minHue = float(workConfig.get("forms", "line2_minHue"))
    config.line2_maxHue = float(workConfig.get("forms", "line2_maxHue"))
    config.line2_minSaturation = float(workConfig.get("forms", "line2_minSaturation"))
    config.line2_maxSaturation = float(workConfig.get("forms", "line2_maxSaturation"))
    config.line2_minValue = float(workConfig.get("forms", "line2_minValue"))
    config.line2_maxValue = float(workConfig.get("forms", "line2_maxValue"))
    config.line2_dropHueMinValue = float(
        workConfig.get("forms", "line2_dropHueMinValue")
    )
    config.line2_dropHueMaxValue = float(
        workConfig.get("forms", "line2_dropHueMaxValue")
    )
    config.line2_minAlpha = float(workConfig.get("forms", "line2_minAlpha"))
    config.line2_maxAlpha = float(workConfig.get("forms", "line2_maxAlpha"))

    config.blockSpeedMultiplier = float(workConfig.get("forms", "blockSpeedMultiplier"))
    config.blockSpeedMin = (
        float(workConfig.get("forms", "blockSpeedMin")) * config.blockSpeedMultiplier
    )
    config.blockSpeedMax = (
        float(workConfig.get("forms", "blockSpeedMax")) * config.blockSpeedMultiplier
    )
    config.blockSpeed2Min = (
        float(workConfig.get("forms", "blockSpeed2Min")) * config.blockSpeedMultiplier
    )
    config.blockSpeed2Max = (
        float(workConfig.get("forms", "blockSpeed2Max")) * config.blockSpeedMultiplier
    )
    config.bgFlashRate = float(workConfig.get("forms", "bgFlashRate"))

    config.blockColSpacingMin = int(workConfig.get("forms", "blockColSpacingMin"))
    config.blockColSpacingMax = int(workConfig.get("forms", "blockColSpacingMax"))
    config.blockRowSpacingMin = int(workConfig.get("forms", "blockRowSpacingMin"))
    config.blockRowSpacingMax = int(workConfig.get("forms", "blockRowSpacingMax"))
    config.blockWidthMin = int(workConfig.get("forms", "blockWidthMin"))
    config.blockWidthMax = int(workConfig.get("forms", "blockWidthMax"))
    config.blockHeightMin = int(workConfig.get("forms", "blockHeightMin"))
    config.blockHeightMax = int(workConfig.get("forms", "blockHeightMax"))

    config.xPosInit = int(workConfig.get("forms", "xPosInit"))
    config.yPosInit = int(workConfig.get("forms", "yPosInit"))

    config.gridAngleIncrementMin = float(
        workConfig.get("forms", "gridAngleIncrementMin")
    )
    config.gridAngleIncrementMax = float(
        workConfig.get("forms", "gridAngleIncrementMax")
    )
    config.spiralAngleIncrementMin = float(
        workConfig.get("forms", "spiralAngleIncrementMin")
    )
    config.spiralAngleIncrementMax = float(
        workConfig.get("forms", "spiralAngleIncrementMax")
    )

    config.repeatFactorMin = float(workConfig.get("forms", "repeatFactorMin"))
    config.repeatFactorMax = float(workConfig.get("forms", "repeatFactorMax"))
    config.expandPaste = workConfig.getboolean("forms", "expandPaste")

    config.sAngleRate = math.pi / float(workConfig.get("forms", "sAngleRate"))
    config.initialRadius = int(workConfig.get("forms", "initialRadius"))
    config.sRadiusRate = float(workConfig.get("forms", "sRadiusRate"))
    config.sRadiusRateChange = float(workConfig.get("forms", "sRadiusRateChange"))
    config.radiusMutiplier = float(workConfig.get("forms", "radiusMutiplier"))

    config.patternType = workConfig.get("forms", "patternType")
    config.figureType = workConfig.get("forms", "figureType")
    config.elementNumber = int(workConfig.get("forms", "elementNumber"))
    config.boxSize = int(workConfig.get("forms", "boxSize"))

    # background color - higher the
    # alpha = less persistent images
    backgroundColor = (workConfig.get("forms", "backgroundColor")).split(",")
    config.backgroundColor = tuple(int(x) for x in backgroundColor)

    backgroundFlashcolor = (workConfig.get("forms", "backgroundFlashcolor")).split(",")
    config.backgroundFlashcolor = tuple(int(x) for x in backgroundFlashcolor)

    config.filterPatchProb = float(workConfig.get("forms", "filterPatchProb"))
    config.filterPatchProbOff = float(workConfig.get("forms", "filterPatchProbOff"))

    config.director = Director(config)
    config.director.slotRate = config.blockSpeedMin


    config.gridSize = 5
    config.unitsToDraw = 250
    config.minW = 1
    config.maxW = 5
    config.minH = 3
    config.maxH = 8


    rebuildGrid()
    setUp()
    drawGrid()


def runWork():
    global config
    print(bcolors.OKGREEN + "** " + bcolors.BOLD)
    print("Running slots.py")
    print(bcolors.ENDC)
    while True:
        iterate()
        time.sleep(config.redrawSpeed)
 