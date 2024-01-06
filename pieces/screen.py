import argparse
import datetime
import math
import random
import time
from modules.configuration import bcolors
from modules import coloroverlay, colorutils
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFont, ImageOps


#----------------------------------------------------##----------------------------------------------------#

class Holder:
    def __init__(self, config):
        self.config = config

#----------------------------------------------------##----------------------------------------------------#
class Director:
    """docstring for Director"""

    slotRate = 0.5

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

class Crack:

    origin = [64, 32]
    pointsCount = 5
    points = []
    yVarMin = 1
    yVarMax = 10

    def __init__(self, config):
        self.config = config
        self.fillColor = colorutils.getRandomRGB()
        self.crackColor = (200, 200, 200, 100)

    def setUp(self):
        self.crackColor = self.config.bgColor
        self.crackColor = self.config.colOverlay.colorB

        # Draw from the origin
        lastPoint = self.origin
        self.points = []
        self.slopes = []
        self.points.append([self.origin[0], self.origin[1]])

        xRange = self.config.canvasWidth / self.pointsCount

        a = 0
        slope = 0

        for i in range(0, self.pointsCount):
            x = round(
                self.origin[0]
                + xRange * i
                - round(random.uniform(-xRange / 2, xRange / 2))
            )
            y = round(
                self.origin[1]
                + round(random.uniform(self.yVarMin * (i + 1), self.yVarMax * (i + 1)))
            )

            if x < 0:
                x = 0

            if i == self.pointsCount - 2:
                x = self.config.canvasWidth + round(
                    random.uniform(-xRange / 8, xRange / 4)
                )
                y = self.config.canvasHeight + round(
                    random.uniform(-xRange / 8, xRange / 4)
                )

            self.points.append([x, y])

            dx = lastPoint[0] - x
            dy = lastPoint[1] - y

            if dx != 0:
                slope = dy / dx
            else:
                slope = 0

            self.slopes.append(slope)

            lastPoint[0] = x
            lastPoint[1] = y

        # print (self.points)

    def render(self):
        for i in range(0, self.pointsCount - 1):
            self.config.canvasDraw.line(
                (
                    self.points[i][0],
                    self.points[i][1],
                    self.points[i + 1][0],
                    self.points[i + 1][1],
                ),
                fill=self.crackColor,
            )


#----------------------------------------------------##----------------------------------------------------#
def filterRemapCall(ovrd=False) :
        config.filterRemap = True
        # new version  more control but may require previous pieces to be re-worked
        startX = round(random.uniform(0, config.filterRemapRangeX))
        startY = round(random.uniform(0, config.filterRemapRangeY))
        endX = round(random.uniform(8, config.filterRemapminHoriSize))
        endY = round(random.uniform(8, config.filterRemapminVertSize))
        
        if ovrd == True :
            startX = 0
            startY = 0
            endX = 200
            endY = 200
        config.remapImageBlockSection = [
            startX, startY, startX + endX, startY + endY]
        config.remapImageBlockDestination = [startX, startY]
        # print("swapping" + str(config.remapImageBlockSection))

def showGrid():
    global config

    config.colOverlay.stepTransition()

    ## Force sets the alpha
    config.colOverlay.currentColor[3] = 30

    config.bgColor = tuple(
        int(a * config.brightness) for a in (config.colOverlay.currentColor))

    config.draw.rectangle(
        (0, 0, config.screenWidth, config.screenHeight),
        fill=config.bgColor,
        outline=(0, 0, 0),)
    if config.bgImage is not None:
        config.image.paste(config.bgImage, (0, 0), config.bgImage)

    ##This leaves more trails --- but loses smooth transition to next background color...
    if random.random() < config.imageResetProb:
        config.canvasDraw.rectangle(
            (0, 0, config.screenWidth, config.screenHeight),
            fill=config.bgColor,
            outline=(0, 0, 0),
        )

        if config.bgImage is not None:
            config.image.paste(config.bgImage, (0, 0), config.bgImage)
            if random.random() < config.imageResetProb:
                config.canvasImage.paste(config.bgImage, (0, 0), config.bgImage)

    """
    ## Draw the background grid
    for row in range (0, config.rows) :
        for col in range (0, config.cols) :
            xPos = col * config.tileSizeWidth 
            yPos = row * config.tileSizeHeight
            #config.canvasDraw.rectangle((xPos,yPos,xPos + config.tileSizeWidth - 1, yPos +  config.tileSizeHeight -1), fill=(0,0,0,2), outline=config.outlineColor)
            config.draw.rectangle((xPos,yPos,xPos + config.tileSizeWidth - 1, yPos +  config.tileSizeHeight -1), fill=config.bgColor, outline=None)
    """

    config.sampleVariationX = 5
    config.sampleVariationY = 0
    for i in range(0, len(config.crackArray)):
        if i < 3 and config.drawCracks == True:
            config.crackArray[i].render()

        ## Draw vertical lines from one line to the next
        if i < len(config.crackArray) - 1:
            for p in range(0, config.pointsCount - 1):
                startX = config.crackArray[i].points[p][0]
                endX = config.crackArray[i].points[p + 1][0]

                # config.canvasDraw.line((startX, 0, startX, config.crackArray[i].points[p][1]), fill=(0, 0, 200,200))
                for x in range(startX, endX, 1):
                    y = (x - startX) * config.crackArray[i].slopes[
                        p
                    ] + config.crackArray[i].points[p][1]
                    y2 = (x - startX) * config.crackArray[i + 1].slopes[
                        p
                    ] + config.crackArray[i + 1].points[p][1]

                    if config.crackArray[i + 1].slopes[p] == 0:
                        x2 = 0
                    else:
                        x2 = y2 / config.crackArray[i + 1].slopes[p]
                    # config.canvasDraw.rectangle((x, y, x+1, y+1), fill=(200, 0, 0))
                    # y2 = config.crackArray[i].points[p][1]
                    if (
                        i > 0
                        and random.random()
                        < config.probDrawLines * config.probabilityMultiplier
                    ):
                        xSample = x - round(
                            random.uniform(
                                -config.sampleVariationX, config.sampleVariationX
                            )
                        )
                        ySample = y - round(
                            random.uniform(
                                -config.sampleVariationY, config.sampleVariationY
                            )
                        )
                        if xSample < 0:
                            xSample = 0
                        if xSample > config.canvasWidth:
                            xSample = config.canvasWidth
                        if ySample < 0:
                            ySample = 0
                        if ySample > config.canvasHeight:
                            ySample = config.canvasHeight

                        samplePoint = (xSample, ySample)
                        # Just make sure the sample point is actually within the bounds of the image
                        if (
                            samplePoint[0] < config.canvasWidth
                            and samplePoint[1] < config.canvasHeight
                            and samplePoint[0] > 0
                            and samplePoint[1] > 0
                        ):
                            colorSample = config.canvasImage.getpixel(samplePoint)

                            # randomize brightness a little
                            colorSampleColor = tuple(
                                int(round(c * random.uniform(0.1, 1.8)))
                                for c in colorSample
                            )

                            # Once in a little while, the color is just random
                            if random.random() < config.randomColorSampleProb:
                                colorSampleColor = colorutils.getRandomRGB(
                                    random.random()
                                )

                            if (
                                random.random()
                                < config.probDrawPerpLines
                                * config.probabilityMultiplier
                            ):
                                if i == 2:
                                    # Draw perpendicular light lines
                                    # config.canvasDraw.line((x, y, x, config.canvasHeight), fill=colorSampleColor)
                                    
                                    config.canvasDraw.line(
                                        (x, y, x2, y), fill=colorSampleColor
                                    )
                                else:
                                    config.canvasDraw.line(
                                        (x, y, config.canvasWidth, y),
                                        fill=colorSampleColor,
                                    )

                            if (
                                random.random()
                                < config.probDrawVertLines
                                * config.probabilityMultiplier
                            ):
                                if x2 < x : x2 = x + 10
                                if y2 < y : y2 = y + 10
                                config.canvasDraw.line(
                                    (x, y, x, y2), fill=colorSampleColor
                                )

                            if (
                                random.random()
                                < config.probDrawBoxes * config.probabilityMultiplier
                            ):

                                if x2 < x : x2 = x + 10
                                if y2 < y : y2 = y + 10
                                

                                config.canvasDraw.rectangle(
                                    (x, y, x2, y2),
                                    fill=colorSampleColor,
                                    outline=colorSampleColor,
                                )

    if config.pausing == False:
        config.image.paste(
            config.canvasImage,
            (config.imageXOffset, config.imageYOffset),
            config.canvasImage,
        )
    config.render(config.image, 0, 0)


def main(run=True):
    global config, directionOrder
    global workConfig
    print("---------------------")
    print("Screen Loaded")

    colorutils.brightness = config.brightness

    try:
        config.imageXOffset = int(workConfig.get("displayconfig", "imageXOffset"))
    except Exception as e:
        print(str(e))
        config.imageXOffset = 0

    config.outlineColorVals = (workConfig.get("screenproject", "outlineColor")).split(",")
    config.outlineColor = tuple(map(lambda x: int(int(x) * config.brightness), config.outlineColorVals))
    config.bgColorVals = (workConfig.get("screenproject", "bgColor")).split(",")
    config.bgColor = tuple(map(lambda x: int(int(x) * config.brightness), config.bgColorVals))
    config.crackColorVals = (workConfig.get("screenproject", "crackColor")).split(",")
    config.crackColor = tuple(map(lambda x: int(int(x) * config.brightness), config.crackColorVals))

    config.tileSizeWidth = int(workConfig.get("displayconfig", "tileSizeWidth"))
    config.tileSizeHeight = int(workConfig.get("displayconfig", "tileSizeHeight"))
    config.delay = float(workConfig.get("screenproject", "delay"))

    config.numCracks = int(workConfig.get("screenproject", "numCracks"))
    config.pointsCount = int(workConfig.get("screenproject", "pointsCount"))

    config.randomColorSampleProb = float(workConfig.get("screenproject", "randomColorSampleProb"))
    config.probDrawLines = float(workConfig.get("screenproject", "probDrawLines"))
    config.probDrawPerpLines = float(workConfig.get("screenproject", "probDrawPerpLines"))
    config.probDrawBoxes = float(workConfig.get("screenproject", "probDrawBoxes"))
    config.yVarMin = int(workConfig.get("screenproject", "yVarMin"))
    config.yVarMax = int(workConfig.get("screenproject", "yVarMax"))
    config.drawCracks = workConfig.getboolean("screenproject", "drawCracks")

    config.tLimitBase = int(workConfig.get("screenproject", "tLimitBase"))
    config.timeTrigger = workConfig.getboolean("screenproject", "timeTrigger")

    config.originVals = (workConfig.get("screenproject", "origin")).split(",")
    config.origin = tuple(map(lambda x: int(int(x) * config.brightness), config.originVals))

    config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
    config.draw = ImageDraw.Draw(config.image)
    config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.canvasDraw = ImageDraw.Draw(config.canvasImage)

    config.colOverlay = coloroverlay.ColorOverlay()
    config.colOverlay.randomSteps = False
    config.colOverlay.timeTrigger = True
    config.colOverlay.tLimitBase = config.tLimitBase
    config.colOverlay.maxBrightness = config.brightness
    config.colOverlay.steps = 50
    config.colOverlay.minHue = float(workConfig.get("screenproject", "minHue"))
    config.colOverlay.maxHue = float(workConfig.get("screenproject", "maxHue"))
    config.colOverlay.minSaturation = float(workConfig.get("screenproject", "minSaturation"))
    config.colOverlay.maxSaturation = float(workConfig.get("screenproject", "maxSaturation"))
    config.colOverlay.minValue = float(workConfig.get("screenproject", "minValue"))
    config.colOverlay.maxBrightness = float(workConfig.get("screenproject", "maxBrightness"))
    config.colOverlay.maxValue = float(workConfig.get("screenproject", "maxValue"))

    try:
        config.colOverlay.dropHueMin = float(workConfig.get("screenproject", "dropHueMin"))
        config.colOverlay.dropHueMax = float(workConfig.get("screenproject", "dropHueMax"))
    except Exception as e:
            print(str(e))

    config.colOverlay.colorTransitionSetup()

    config.crackChangeProb = float(workConfig.get("screenproject", "crackChangeProb"))
    config.imageResetProb = float(workConfig.get("screenproject", "imageResetProb"))

    try:
        # if it's set, will act as a range and turn on the setting
        config.probabilityMultiplierRange = float(workConfig.get("screenproject", "probabilityMultiplierRange"))
        config.probabilityMultiplier = 1.0
    except Exception as e:
        config.probabilityMultiplierRange = 1.0
        config.probabilityMultiplier = 1.0
        print(str(e))

    try:
        config.probDrawVertLines = float(
            workConfig.get("screenproject", "probDrawVertLines")
        )
    except Exception as e:
        config.probDrawVertLines = 0.9
        print(str(e))

    try:
        config.pauseProb = float(workConfig.get("screenproject", "pauseProb"))
        config.unpauseProb = float(workConfig.get("screenproject", "unpauseProb"))
        config.usePause = True
        config.pausing = False

    except Exception as e:
        config.usePause = False
        print(str(e))

    try:
        arg = workConfig.get("screenproject", "bgImage")
        path = config.path + arg
        config.bgImage = Image.open(path, "r")
        print("loading : ", path)
        if config.bgImage.load():
            config.bgImage = config.bgImage.convert("RGBA")
        imgHeight = config.bgImage.getbbox()[3]
    except Exception as e:
        print(str(e))
        config.bgImage = None

    # managing speed of animation and framerate
    config.directorController = Director(config)

    try:
        config.delay = float(workConfig.get("screenproject", "delay"))
    except Exception as e:
        print(str(e))
        config.delay = 0.02
    try:
        config.directorController.slotRate = float(workConfig.get("screenproject", "slotRate"))
    except Exception as e:
        print(str(e))
        print("SHOULD ADJUST TO USE slotRate AS FRAMERATE ")
        config.directorController.slotRate = 0.0

    try:
        config.filterRemapping = (workConfig.getboolean("screenproject", "filterRemapping"))
        config.filterRemappingProb = float(workConfig.get("screenproject", "filterRemappingProb"))
        config.filterRemapminHoriSize = int(workConfig.get("screenproject", "filterRemapminHoriSize"))
        config.filterRemapminVertSize = int(workConfig.get("screenproject", "filterRemapminVertSize"))
        config.filterRemapRangeX = int(workConfig.get("screenproject", "filterRemapRangeX"))
        config.filterRemapRangeY = int(workConfig.get("screenproject", "filterRemapRangeY"))
    except Exception as e:
        print(str(e))
        config.filterRemapping = False
        config.filterRemappingProb = 0.0
        config.filterRemapminHoriSize = 24
        config.filterRemapminVertSize = 24
        config.filterRemapRangeX = config.canvasWidth
        config.filterRemapRangeY = config.canvasHeight

    try:
        if config.usePixelSort == True:
            config.pixelSortProbOn = float(workConfig.get("screenproject", "pixelSortProbOn"))
            config.pixelSortProbOff = float(workConfig.get("screenproject", "pixelSortProbOff"))
        else:
            config.pixelSortProbOn = 0
            config.pixelSortProbOff = 0

    except Exception as e:
        print(str(e))
        config.pixelSortProbOn = 0
        config.pixelSortProbOff = 0

    config.crackArray = []
    for i in range(0, config.numCracks):
        obj = Crack(config)
        obj.origin = [config.canvasWidth, config.canvasHeight]
        obj.origin = [config.origin[0], config.origin[1]]
        obj.pointsCount = config.pointsCount
        obj.crackColor = config.crackColor
        obj.yVarMin = config.yVarMin
        obj.yVarMax = config.yVarMax
        obj.setUp()
        config.crackArray.append(obj)

    setUp()

    if run:
        runWork()


def setUp():
    global config
    pass
    

def runWork():
    global config
    print(bcolors.OKGREEN + "** " + bcolors.BOLD)
    print("RUNNING Screen.py")
    print(bcolors.ENDC)
    while config.isRunning == True:
        config.directorController.checkTime()
        if config.directorController.advance == True:
            iterate()
            time.sleep(config.delay)
        if config.standAlone == False:
            config.callBack()


def iterate():
    global config

    ## reuse the pause prob
    if (
        random.random() < config.unpauseProb / 2
        and config.probabilityMultiplierRange > 1
        and config.pausing == False
    ):
        config.probabilityMultiplier = random.uniform(
            1.1, config.probabilityMultiplierRange
        )

    if random.random() < config.pauseProb * 4:
        config.probabilityMultiplier = 1

    if random.random() < config.pauseProb and config.usePause == True:
        config.pausing = True
        showGrid()
    elif config.pausing == False:
        showGrid()

    if random.random() < config.unpauseProb and config.pausing == True:
        config.pausing = False

    if config.usePause == False:
        showGrid()

    if random.random() < config.crackChangeProb:
        c = math.floor(random.uniform(0, len(config.crackArray)))
        # print (c,len(config.crackArray))
        config.crackArray[c].origin = [config.origin[0], config.origin[1]]
        config.crackArray[c].setUp()
        
    if random.random() < config.filterRemappingProb:
        if random.random() < .5:
            config.filterRemapping == False
        else:
            config.filterRemapping == True

    if random.random() < config.filterRemappingProb:
        if config.useFilters == True and config.filterRemapping == True:
            filterRemapCall()


    if random.random() < config.pixelSortProbOn:
        config.usePixelSort = True
        config.pixSortprobGetNextColor = random.random()
        config.randomColorProbabilty = random.uniform(.01,.2)
        config.pixSortXOffset = round(random.uniform(0,config.canvasWidth))
        config.pixSortboxWidth = round(random.uniform(1,50))
        config.pixSortprobDraw = random.random()
        

    if random.random() < config.pixelSortProbOff:
        config.usePixelSort = False


def callBack():
    global config
    return True


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
