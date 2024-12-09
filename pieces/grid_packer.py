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


def newBGClr():
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


def newClr():
    return colorutils.getRandomColorHSV(
        config.clr1_minHue,
        config.clr1_maxHue,
        config.clr1_minSaturation,
        config.clr1_maxSaturation,
        config.clr1_minValue,
        config.clr1_maxValue,
        config.clr1_dropHueMinValue,
        config.clr1_dropHueMaxValue,
        round(random.uniform(config.clr1_minAlpha, config.clr1_maxAlpha)),
    )


def newClr2():
    return colorutils.getRandomColorHSV(
        config.clr2_minHue,
        config.clr2_maxHue,
        config.clr2_minSaturation,
        config.clr2_maxSaturation,
        config.clr2_minValue,
        config.clr2_maxValue,
        config.clr2_dropHueMinValue,
        config.clr2_dropHueMaxValue,
        round(random.uniform(config.clr2_minAlpha, config.clr2_maxAlpha)),
    )

def newClr3():
    return colorutils.getRandomColorHSV(
        config.clr3_minHue,
        config.clr3_maxHue,
        config.clr3_minSaturation,
        config.clr3_maxSaturation,
        config.clr3_minValue,
        config.clr3_maxValue,
        config.clr3_dropHueMinValue,
        config.clr3_dropHueMaxValue,
        round(random.uniform(config.clr3_minAlpha, config.clr3_maxAlpha)),
    )


def generateUnitImage(dims):
    image = Image.new("RGBA", (config.blockWidth, config.blockHeight))
    draw = ImageDraw.Draw(image)

    # if random.SystemRandom().random() < config.drawFullColorUnit :
    #     draw.rectangle((0,0,dims[0], dims[1]), fill=clr)
    # else :
    #     if random.SystemRandom().random() < config.drawLeftTriangle :
    #         draw.polygon(((0,0),(dims[0], dims[1]),(0, dims[1])), fill=clr)
    #         # draw.polygon(((0,0),(dims[0], dims[1]),(0, dims[1])), fill=(255,0,0,200))
    #         if random.SystemRandom().random() < config.drawGreyTriangleUnit :
    #             draw.polygon(((0,0),(dims[0], dims[1]),(dims[0], 0)), fill=clr2)
    #     else :
    #         draw.polygon(((0, dims[1]),(dims[0], 0),(dims[0],dims[1])), fill=clr2)
    #         if random.SystemRandom().random() < config.drawRedTriangleUnit :
    #             draw.polygon(((0, dims[1]),(dims[0], 0),(0,0)), fill=clr3)



    cntrPt = [dims[0]/2, dims[1]/2]


    if random.SystemRandom().random() < config.drawTwoTrianglesProb :

        if random.SystemRandom().random() < config.drawLeftTriangle :
            # triangle slop L to R
            clr_t1 = newClr()

            if random.SystemRandom().random() < config.drawRedTriangleUnit :
                clr_t1 = newClr3()


            clr_t2 = clr_t1
            if random.SystemRandom().random() < config.drawGreyTriangleUnit :
                clr_t3  = newClr2()
            else :
                clr_t3 = newClr()

            clr_t4 = clr_t3
        else :
            # triangle slop R to L
            clr_t1 = newClr()
            clr_t2 = newClr()

            if random.SystemRandom().random() < config.drawRedTriangleUnit :
                clr_t1 = newClr3()



            clr_t3 = clr_t1
            clr_t4 = clr_t2
    else:
        clr_t1 = newClr()
        clr_t2 = newClr()
        clr_t3 = newClr()
        clr_t4 = newClr()

        # butterfly
        clr_t1 = newClr()
        clr_t3 = newClr()

        if random.SystemRandom().random() < config.drawGreyTriangleUnit :
            clr_t3 = newClr2()

        clr_t2 = clr_t3
        clr_t4 = clr_t1

    if random.SystemRandom().random() < config.drawFullColorUnit :
        clr_t2 = clr_t1
        clr_t3 = clr_t1
        clr_t4 = clr_t1



    # t1
    draw.polygon(((0,0),(dims[0], 0),(cntrPt[0], cntrPt[1])), fill=clr_t1)
    # t2
    draw.polygon(((0,0),(cntrPt[0], cntrPt[1]),(0, dims[1])), fill=clr_t2)
    # # t3
    draw.polygon(((dims[0], 0),(cntrPt[0], cntrPt[1]),(dims[0], dims[1])), fill=clr_t3)
    # # t4
    draw.polygon(((0, dims[1]),(cntrPt[0], cntrPt[1]),(dims[0], dims[1])), fill=clr_t4)
    
    
    clr_t1a = newClr()
    # clr_t1a = clr_t2

    if random.SystemRandom().random() < config.drawConcentricEllipse :
        radius = [dims[0],dims[1]]
        for ii in range( 1, 5) :
            radius[0] = 1/8 * ii * dims[0]
            radius[1] = 1/8 * ii * dims[1]
            draw.ellipse(((cntrPt[0]-radius[0], cntrPt[1]-radius[1]),(cntrPt[0] + radius[0], cntrPt[1] + radius[1])), fill=None, outline=clr_t1a, width=3)

    return image


def removeFromAvailable(lastX ,lastY, unitFills):
    for h in range(lastY, lastY+unitFills[1], config.gridSize) :
        for w in range(lastX, lastX+unitFills[0],  config.gridSize) :
            for ii in range(0, len(config.availableSpots)) :
                if config.availableSpots[ii][0] == w and config.availableSpots[ii][1] == h :
                    config.availableSpots[ii][2] = False


def linearPlacer(doSort = False, reversedSort = False):
    if doSort : config.unitFills = sorted(config.unitFills, key=lambda w: w[0] * w[1] , reverse=reversedSort)

    lastX = 0
    lastY = 0
    lastHighest = 0
    for i in range(0, len(config.unitFills)):
        img = generateUnitImage(config.unitFills[i])

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


def simplePlacer(doSort = False, reversedSort = False):
    if doSort : 
        config.unitFills = sorted(config.unitFills, key=lambda w: w[0] * w[1] , reverse=reversedSort)
    lastX = 0
    lastY = 0
    lastHighest = 0

    unitIndex = config.unitIndex
    # for unitIndex in range(0, len(config.unitFills)):
    if unitIndex < len(config.unitFills):
        img = generateUnitImage(config.unitFills[unitIndex])
        # searchRadius = math.ceil(math.sqrt(config.unitFills[i][0]*config.unitFills[i][0] + config.unitFills[i][1]*config.unitFills[i][1]))
        # print(searchRadius)
        insertIndex = 0
        canFit = False
        for s in range(0, len(config.availableSpots)) :
            if config.availableSpots[s][2] :
                sY = config.availableSpots[s][1]
                eY = config.availableSpots[s][1] + config.unitFills[unitIndex][1]
                sX = config.availableSpots[s][0]
                eX = config.availableSpots[s][0] + config.unitFills[unitIndex][0]
                keepGoing = True
                for h in range (sY, eY ,config.gridSize ) :
                    if keepGoing :
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
            removeFromAvailable(config.availableSpots[insertIndex][0] ,config.availableSpots[insertIndex][1], config.unitFills[unitIndex])


def drawGrid():
    # linearPlacer(True)
    # linearPlacer(False)
    # simplePlacer(doSort, reversedSort)

    if config.unitIndex < len(config.unitFills):
        simplePlacer(config.doSort, config.reversedSort)

    config.unitIndex += 1

    # if (config.unitIndex >= len(config.unitFills)) :
    #     config.unitIndex = 0

    # FOR DEBUGGING!
    # for i in range(0, len(config.availableSpots)) :
    #     if(config.availableSpots[i][2]) : 
    #         config.draw.rectangle((config.availableSpots[i][0], config.availableSpots[i][1],config.availableSpots[i][0]+1, config.availableSpots[i][1]+1), fill=(0,0,255))


def reDraw(config):
        rebuildGrid()
        setUp()
        drawGrid()


def iterate():
    global config, expandingRingsRing, lastRate, calibrated, cycleCount
    # config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))

    config.director.checkTime()
    if config.director.advance == True:
        drawGrid()
        # config.draw.rectangle(
        #     (0, 0, config.screenWidth, config.screenHeight), fill=config.backgroundColor
        # )
     
        if random.random() < config.bgFlashRate:
            config.draw.rectangle(
                (0, 0, config.screenWidth, config.screenHeight),
                fill=config.bgColor,
            )
            reDraw(config)
        # Do the final rendering of the composited image
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
    config.bgColor = newBGClr()
    config.availableSpots = []

    for h in range(0, config.canvasHeight, config.gridSize) :
        for w in range(0, config.canvasWidth, config.gridSize) :
            config.availableSpots.append([w,h,True])


def rebuildGrid():
    config.unitFills = []

    for i in range(0,config.unitsToDraw ) :
        config.unitFills.append((round(random.SystemRandom().uniform(config.minW,config.maxW))* config.gridSize, round(random.SystemRandom().uniform(config.minH,config.maxH))* config.gridSize) )

    config.unitIndex = 0

    config.doSort = True if random.SystemRandom().random() < config.doSortProb else False
    config.reversedSort = True if random.SystemRandom().random() < config.reversedSortProb else False

def main(run=True):
    global config
    global expandingRingss
    global workConfig

    expandingRingss = []
    config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.draw = ImageDraw.Draw(config.image)

    config.redrawSpeed = float(workConfig.get("forms", "redrawSpeed"))
    config.slotRate = float(workConfig.get("forms", "slotRate"))

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

    config.clr1_minHue = float(workConfig.get("forms", "clr1_minHue"))
    config.clr1_maxHue = float(workConfig.get("forms", "clr1_maxHue"))
    config.clr1_minSaturation = float(workConfig.get("forms", "clr1_minSaturation"))
    config.clr1_maxSaturation = float(workConfig.get("forms", "clr1_maxSaturation"))
    config.clr1_minValue = float(workConfig.get("forms", "clr1_minValue"))
    config.clr1_maxValue = float(workConfig.get("forms", "clr1_maxValue"))
    config.clr1_dropHueMinValue = float(workConfig.get("forms", "clr1_dropHueMinValue"))
    config.clr1_dropHueMaxValue = float(workConfig.get("forms", "clr1_dropHueMaxValue"))
    config.clr1_minAlpha = float(workConfig.get("forms", "clr1_minAlpha"))
    config.clr1_maxAlpha = float(workConfig.get("forms", "clr1_maxAlpha"))

    config.clr2_minHue = float(workConfig.get("forms", "clr2_minHue"))
    config.clr2_maxHue = float(workConfig.get("forms", "clr2_maxHue"))
    config.clr2_minSaturation = float(workConfig.get("forms", "clr2_minSaturation"))
    config.clr2_maxSaturation = float(workConfig.get("forms", "clr2_maxSaturation"))
    config.clr2_minValue = float(workConfig.get("forms", "clr2_minValue"))
    config.clr2_maxValue = float(workConfig.get("forms", "clr2_maxValue"))
    config.clr2_dropHueMinValue = float( workConfig.get("forms", "clr2_dropHueMinValue"))
    config.clr2_dropHueMaxValue = float(workConfig.get("forms", "clr2_dropHueMaxValue"))
    config.clr2_minAlpha = float(workConfig.get("forms", "clr2_minAlpha"))
    config.clr2_maxAlpha = float(workConfig.get("forms", "clr2_maxAlpha"))

    config.clr3_minHue = float(workConfig.get("forms", "clr3_minHue"))
    config.clr3_maxHue = float(workConfig.get("forms", "clr3_maxHue"))
    config.clr3_minSaturation = float(workConfig.get("forms", "clr3_minSaturation"))
    config.clr3_maxSaturation = float(workConfig.get("forms", "clr3_maxSaturation"))
    config.clr3_minValue = float(workConfig.get("forms", "clr3_minValue"))
    config.clr3_maxValue = float(workConfig.get("forms", "clr3_maxValue"))
    config.clr3_dropHueMinValue = float( workConfig.get("forms", "clr3_dropHueMinValue"))
    config.clr3_dropHueMaxValue = float(workConfig.get("forms", "clr3_dropHueMaxValue"))
    config.clr3_minAlpha = float(workConfig.get("forms", "clr3_minAlpha"))
    config.clr3_maxAlpha = float(workConfig.get("forms", "clr3_maxAlpha"))

    config.bgFlashRate = float(workConfig.get("forms", "bgFlashRate"))
    backgroundFlashcolor = (workConfig.get("forms", "backgroundFlashcolor")).split(",")
    config.backgroundFlashcolor = tuple(int(x) for x in backgroundFlashcolor)

    config.filterPatchProb = float(workConfig.get("forms", "filterPatchProb"))
    config.filterPatchProbOff = float(workConfig.get("forms", "filterPatchProbOff"))

    config.director = Director(config)


    config.gridSize = int(workConfig.get("forms", "gridSize"))
    config.unitsToDraw = int(workConfig.get("forms", "unitsToDraw"))
    config.minW = int(workConfig.get("forms", "minW"))
    config.maxW = int(workConfig.get("forms", "maxW"))
    config.minH = int(workConfig.get("forms", "minH"))
    config.maxH = int(workConfig.get("forms", "maxH"))
    config.doSortProb = float(workConfig.get("forms", "doSortProb"))
    config.reversedSortProb = float(workConfig.get("forms", "reversedSortProb"))

    config.blockWidth = config.maxW * config.gridSize
    config.blockHeight = config.maxH * config.gridSize


    # higher = more full color rectangles
    config.drawFullColorUnit = float(workConfig.get("forms", "drawFullColorUnit"))
    # lower more single color
    config.drawLeftTriangle = float(workConfig.get("forms", "drawLeftTriangle"))
    # lower = more black/bg
    config.drawGreyTriangleUnit = float(workConfig.get("forms", "drawGreyTriangleUnit"))
    # lower = more black/bg on left
    config.drawRedTriangleUnit = float(workConfig.get("forms", "drawRedTriangleUnit"))

    config.drawTwoTrianglesProb = float(workConfig.get("forms", "drawTwoTrianglesProb"))

    config.drawConcentricEllipse = float(workConfig.get("forms", "drawConcentricEllipse"))


    config.unitIndex = 0

    config.doSort = True if random.SystemRandom().random() < config.doSortProb else False
    config.reversedSort = True if random.SystemRandom().random() < config.reversedSortProb else False

    setUp()
    rebuildGrid()
    drawGrid()


def runWork():
    global config
    print(bcolors.OKGREEN + "** " + bcolors.BOLD)
    print("Running slots.py")
    print(bcolors.ENDC)
    while True:
        iterate()
        time.sleep(config.redrawSpeed)
 