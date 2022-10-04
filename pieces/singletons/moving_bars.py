import math
import random
import threading
import time
from modules.configuration import bcolors
from modules import colorutils, coloroverlay
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps


'''
				fadeIn = Fader()
				# fadeIn.blankImage = Image.new("RGBA", (height, width))
				fadeIn.crossFade = Image.new("RGBA", (height, width))
				fadeIn.image = gradientImage
				fadeIn.xPos = xPos
				fadeIn.yPos = yPos
				fadeIn.height = gradientImage.height
				fadeIn.width = gradientImage.width

				config.fadeArray.append(fadeIn)

'''
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


class Fader:
    def __init__(self):
        self.doingRefresh = 0
        self.doingRefreshCount = 50
        self.fadingDone = False

    def fadeIn(self, config):
        if self.fadingDone == False:
            if self.doingRefresh < self.doingRefreshCount:
                self.blankImage = Image.new("RGBA", (self.width, self.height))
                self.crossFade = Image.blend(
                    self.blankImage,
                    self.image,
                    self.doingRefresh / self.doingRefreshCount,
                )
                config.image.paste(
                    self.crossFade, (self.xPos, self.yPos), self.crossFade
                )
                self.doingRefresh += 1
            else:
                config.image.paste(
                    self.image, (self.xPos, self.yPos), self.image)
                self.fadingDone = True


class Bar:
    def __init__(self, config):
        self.config = config
        self.colOverlay = coloroverlay.ColorOverlay()
        self.remake()

    def remake(self):
        self.direction = 1
        if random.random() < .5 : self.direction = -1
        self.xSpeed = random.uniform(
            config.xSpeedRangeMin * self.direction, config.xSpeedRangeMax * self.direction)
        self.ySpeed = random.uniform(
            config.ySpeedRangeMin, config.ySpeedRangeMax)
        self.yPos = round(random.uniform(config.yRangeMin, config.yRangeMax))
        self.xPos = 0  # -config.barThicknessMax * 2
        if self.direction == -1:
            self.xPos = config.canvasWidth  # + config.barThicknessMax * 2

        self.barThickness = round(random.uniform(
            config.barThicknessMin, config.barThicknessMax))

        self.barLength = round(random.uniform(
            config.barLengthMin, config.barLengthMax))


        #self.colorVal = colorutils.randomColorAlpha()
        cset = config.colorSets[config.usingColorSet]

        colorAlpha = config.outlineColorAlpha

        self.colorVal = colorutils.getRandomColorHSV(
            cset[0], cset[1], cset[2], cset[3], cset[4], cset[5], config.dropHueMax, 0, colorAlpha, config.brightness)
        self.outlineColorVal = colorutils.getRandomColorHSV(
            cset[0], cset[1], cset[2], cset[3], cset[4], cset[5], config.dropHueMax, 0, config.outlineColorAlpha, config.brightness)
        self.outlineColorVal = self.colorVal

        self.setColors()
        self.colOverlay.colorTransitionSetup()

    def setColors(self):
        # Sets up color transitions
        cset = config.colorSets[config.usingColorSet]

        self.colOverlay.randomSteps = True
        self.colOverlay.timeTrigger = True
        self.colOverlay.tLimitBase = 12
        self.colOverlay.steps = 10

        self.colOverlay.minHue = cset[0]
        self.colOverlay.maxHue = cset[1]
        self.colOverlay.minSaturation = cset[2]
        self.colOverlay.maxSaturation = cset[3]
        self.colOverlay.minValue = cset[4]
        self.colOverlay.maxValue = cset[5]

        self.colOverlay.colorA = self.colorVal

    def update(self):
        self.colOverlay.stepTransition()
        self.colorVal = (
            int(self.colOverlay.currentColor[0]*self.config.brightness),
            int(self.colOverlay.currentColor[1]*self.config.brightness),
            int(self.colOverlay.currentColor[2]*self.config.brightness),
            self.config.colorAlpha
        )

        if self.colOverlay.complete == True:
            self.setColors()


def transformImage(img):
    width, height = img.size
    new_width = 50
    m = 0.0
    img = img.transform(
        (new_width, height), Image.AFFINE, (1, m, 0, 0, 1, 0), Image.BICUBIC
    )
    return img


def drawBar():
    global config


def reDraw():
    global config


def runWork():
    global config
    print(bcolors.OKGREEN + "** " + bcolors.BOLD)
    print("Running moving_bars.py")
    print(bcolors.ENDC)
    while config.isRunning == True:
        config.directorController.checkTime()
        if config.directorController.advance == True :
            iterate()
        time.sleep(config.redrawRate)
        if config.standAlone == False:
            config.callBack()


def iterate():
    global config

    config.draw.rectangle((0, 0, 400, 400), fill=(0, 0, 0, 1))

    locus = [100,100]

    for i in range(0, config.numberOfBars):
        bar = config.barArray[i]
        bar.xPos += bar.xSpeed
        bar.yPos += bar.ySpeed
        bar.update()

        w = round(math.sqrt(2) * config.barThicknessMax * 1.5)

        angle = math.atan2(bar.ySpeed, bar.xSpeed)

        temp = Image.new("RGBA", (bar.barLength, bar.barLength))
        drw = ImageDraw.Draw(temp)


        dx = bar.xPos - locus[0]
        dy = bar.yPos - locus[1]
        angle = math.atan2(dy, dx)


        if config.tipType == 1:
            drw.rectangle((0, bar.barLength/2, bar.barLength, bar.barLength/2 + bar.barThickness  ),
                          fill=bar.colorVal, outline=bar.outlineColorVal)
            #drw.rectangle((0, 2, bar.barThickness, bar.barLength+2),fill=bar.colorVal, outline=bar.outlineColorVal)

        elif config.tipType == 0:
            drw.ellipse((0, 2, bar.barThickness, bar.barLength+2),
                        fill=bar.colorVal, outline=bar.outlineColorVal)

        elif config.tipType == 2:
            drw.ellipse((0, 2, bar.barThickness, bar.barThickness),
                        fill=bar.colorVal, outline=bar.outlineColorVal)

        temp = temp.rotate( 180 - math.degrees(angle))

        config.image.paste(temp, (round(bar.xPos), round(bar.yPos)), temp)

        if bar.xPos > config.canvasWidth:
            #bar.remake()
            bar.xPos = 0

        if bar.xPos < 0 :
            bar.xPos = config.canvasWidth

        if bar.yPos < 0 :
            bar.yPos = config.canvasHeight

        if bar.yPos > config.canvasHeight :
            bar.yPos = 0
            #bar.remake()

    if random.random() < .002:
        if config.dropHueMax == 0:
            config.dropHueMax = 255
        else:
            config.dropHueMax = 0
        #print("Winter... " + str(config.dropHueMax ))

    if random.random() < config.colorChangeProb:

        config.usingColorSet = math.floor(
            random.uniform(0, config.numberOfColorSets))
        # just in case ....
        if config.usingColorSet == config.numberOfColorSets:
            config.usingColorSet = config.numberOfColorSets-1
        config.colorAlpha = round(random.uniform(
            config.leadEdgeAlpahMin, config.leadEdgeAlpahMax))
        config.dropHueMax = 0


        if random.random() < config.changeShapeProb:
            config.tipType = config.tipTypeAlt
        else:
            config.tipType = config.tipTypeOrig

    config.render(config.image, 0, 0)


def main(run=True):
    global config
    config.redrawRate = .02

    config.image = Image.new("RGBA", (config.screenWidth, config.screenHeight))
    config.draw = ImageDraw.Draw(config.image)
    config.canvasImage = Image.new(
        "RGBA", (config.canvasWidth, config.canvasHeight))
    config.canvasDraw = ImageDraw.Draw(config.canvasImage)

    config.xPos = 0
    config.dropHueMax = 0

    config.numberOfBars = int(workConfig.get("bars", "numberOfBars"))
    config.barThicknessMin = int(workConfig.get("bars", "barThicknessMin"))
    config.barThicknessMax = int(workConfig.get("bars", "barThicknessMax"))

    config.barLengthMin = int(workConfig.get("bars", "barLengthMin"))
    config.barLengthMax = int(workConfig.get("bars", "barLengthMax"))

    config.direction = int(workConfig.get("bars", "direction"))
    yRange = (workConfig.get("bars", "yRange")).split(",")
    config.yRangeMin = int(yRange[0])
    config.yRangeMax = int(yRange[1])

    config.leadEdgeAlpahMin = int(workConfig.get("bars", "leadEdgeAlpahMin"))
    config.leadEdgeAlpahMax = int(workConfig.get("bars", "leadEdgeAlpahMax"))
    config.tipAngle = float(workConfig.get("bars", "tipAngle"))

    config.xSpeedRangeMin = float(workConfig.get("bars", "xSpeedRangeMin"))
    config.xSpeedRangeMax = float(workConfig.get("bars", "xSpeedRangeMax"))
    config.ySpeedRangeMin = float(workConfig.get("bars", "ySpeedRangeMin"))
    config.ySpeedRangeMax = float(workConfig.get("bars", "ySpeedRangeMax"))

    try:
        config.colorChangeProb = float(
            workConfig.get("bars", "colorChangeProb"))
    except Exception as e:
        print(str(e))
        config.colorChangeProb = .003

    try:
        config.changeShapeProb = float(
            workConfig.get("bars", "changeShapeProb"))
    except Exception as e:
        print(str(e))
        config.changeShapeProb = .001

    try:
        config.tipType = int(workConfig.get("bars", "tipType"))
        config.tipTypeOrig = int(workConfig.get("bars", "tipType"))
        config.tipTypeAlt = int(workConfig.get("bars", "tipTypeAlt"))
    except Exception as e:
        print(str(e))
        config.tipType = 1
        config.tipTypeAlt = 1
        config.tipTypeOrig = 1

    config.colorAlpha = round(random.uniform(
        config.leadEdgeAlpahMin, config.leadEdgeAlpahMax))
    config.outlineColorAlpha = round(random.uniform(
        config.leadEdgeAlpahMin/2, config.leadEdgeAlpahMax/2))
    yPos = 0
    config.barArray = []

    config.colorSets = []

    config.colorSetList = list(
        i for i in (workConfig.get("bars", "colorSets").split(","))
    )

    config.numberOfColorSets = len(config.colorSetList)
    for setName in config.colorSetList:
        cset = list(
            float(i) for i in (workConfig.get("bars", setName).split(","))
        )
        config.colorSets.append(cset)

    config.usingColorSet = math.floor(
        random.uniform(0, config.numberOfColorSets))
    if config.usingColorSet == config.numberOfColorSets:
        config.usingColorSet = config.numberOfColorSets - 1

    # initialize and place the first set
    for i in range(0, config.numberOfBars):
        bar = Bar(config)
        bar.yPos = round(random.uniform(config.yRangeMin, config.yRangeMax))
        bar.xPos = round(random.uniform(
            0, config.canvasWidth - 2))
        config.barArray.append(bar)
        #yPos += bar.barThickness

    config.directorController = Director(config)
    config.directorController.slotRate = .03

    if run:
        runWork()
