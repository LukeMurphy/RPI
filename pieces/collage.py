# ################################################### #
import argparse
import math
import random
import time
import types

from modules import badpixels, coloroverlay, colorutils
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps
from modules.configuration import bcolors
from modules.holder_director import Holder 
from modules.holder_director import Director 

lastRate = 0
colorutils.brightness = 1
shapes = []


# Really no need for a class here - it's always a singleton and besides
# with Python everthing is an object already .... some kind of OOP
# holdover anxiety I guess


class Shape:

    outlineColor = (1, 1, 1)
    barColor = (200, 200, 000)
    barColorStart = (0, 200, 200)
    holderColor = (0, 0, 0)
    messageClr = (200, 0, 0)
    shadowColor = (0, 0, 0)
    centerColor = (0, 0, 0)

    shapeXPosition = 0
    shapeYPosition = 0

    xPos = 1
    xPos1 = 1
    yPos = 1
    yPos1 = 1
    boxHeight = 100
    boxMax = 100
    status = 0
    rateMultiplier = 0.1
    rate = rateMultiplier * random.random()
    numRate = rate
    percentage = 0
    var = 10

    nothingLevel = 10
    nothingChangeProbability = 0.02

    borderModel = "prism"
    nothing = "void"
    varianceMode = "independent"
    prisimBrightness = 0.5

    steps = 20

    def __init__(self, config, i=0):
        # print ("init Fludd", i)

        # self.boxMax = config.screenWidth - 1
        # self.boxMaxAlt = self.boxMax + int(random.uniform(10,30) * config.screenWidth)
        # self.boxHeight = config.screenHeight - 2        #

        self.unitNumber = i
        self.config = config
        self.colOverlay = coloroverlay.ColorOverlay()

    def setUp(self):

        xCoords = []
        yCoords = []
        for i in self.coords:
            xCoords.append(i[0])
            yCoords.append(i[1])

        self.boxMax = round(max(xCoords) + 2 * self.varX)
        self.boxHeight = round(max(yCoords) + 2 * self.varY)

        self.tempImage = Image.new("RGBA", (self.boxMax, self.boxHeight))

        self.draw = ImageDraw.Draw(self.tempImage)
        #### Sets up color transitions
        self.colOverlay.randomSteps = False
        self.colOverlay.timeTrigger = True
        # self.colOverlay.tLimitBase = 15
        # self.colOverlay.steps = 120

        # This will force the overlay color transition functions to use the
        # configs for HSV
        # print("\n--- New Colors --- ")
        # print(self.minHue,self.maxHue)
        self.colOverlay.maxBrightness = 1
        self.colOverlay.minHue = self.minHue
        self.colOverlay.maxHue = self.maxHue
        self.colOverlay.minSaturation = self.minSaturation
        self.colOverlay.maxSaturation = self.maxSaturation
        self.colOverlay.minValue = self.minValue
        self.colOverlay.maxValue = self.maxValue

        ### This is the speed range of transitions in color
        ### Higher numbers means more possible steps so slower
        ### transitions - 1,10 very blinky, 10,200 very slow
        self.colOverlay.randomRange = (
            self.config.transitionStepsMin,
            self.config.transitionStepsMax,
        )
        self.colOverlay.colorTransitionSetup()
        self.colOverlay.setStartColor()
        self.colOverlay.getNewColor()

        self.fillColor = tuple(
            int(a * self.config.brightness) for a in self.colOverlay.currentColor
        )

        self.widthDelta = 0
        self.heightDelta = 0
        self.xDelta = 0
        self.yDelta = 0
        self.poly = []

        self.setNewBox()

    def changeAction(self):
        return False

    def setNewBox(self):
        self.draw.rectangle(
            (0, 0, self.boxMax, self.boxHeight), fill=(0, 0, 0, 255), outline=None
        )
        self.poly = []
        for p in self.coords:
            xPos = self.varX + round(p[0] + random.uniform(-self.varX, self.varX))
            yPos = self.varY + round(p[1] + random.uniform(-self.varY, self.varY))
            self.poly.append((xPos, yPos))

    def transition(self):

        self.colOverlay.stepTransition()
        self.fillColor = []
        for i in range(0, 3):
            self.fillColor.append(
                round(self.colOverlay.currentColor[i] * self.config.brightness)
            )
        self.fillColor.append(255)
        self.fillColor = tuple(int(a) for a in self.fillColor)

        self.draw.rectangle(
            (0, 0, self.boxMax, self.boxHeight), fill=(0, 0, 0, 10), outline=None
        )
        if self.varX == -1:
            self.draw.ellipse(
                (self.poly[0][0], self.poly[0][1], self.poly[2][0], self.poly[2][1]),
                fill=self.fillColor,
                outline=None,
            )
        self.draw.polygon(self.poly, fill=self.fillColor, outline=None)

    def reDraw(self):
        # self.draw.rectangle((0,0,self.boxMax, self.boxHeight), fill=self.fillColor, outline=None)
        self.draw.polygon(self.poly, fill=self.fillColor, outline=None)

    def done(self):
        return True


def redraw():
    global config, shapeGroups



    ## Each Fludd-square is generated as an image and then pasted into its correct
    ## place in the grid - or off-grid maybe sometime

    """
    config.draw.rectangle((0,0,config.canvasWidth, config.canvasHeight), fill=(0,0,0,10), outline=None)
    for shapeElement in shapes:
        shapeElement.transition()
        img = shapeElement.tempImage.convert("RGBA")
        config.destinationImage.paste(img, (shapeElement.shapeXPosition, shapeElement.shapeYPosition), img)
        config.image.paste(config.destinationImage, (0,0), config.destinationImage)
        if random.random() < config.changeBoxProb:
            if shapeElement.varX == 0 and shapeElement.varY == 0 :
                pass
            else :
                shapeElement.setNewBox()
                #print("new box: " + shapeElement.name)
    """
    shapes = config.shapeGroups[config.shapeGroupDisplayed]

    if config.shapeTweening == 1:
        config.shapeTweening = 2

        ## Generate state to transition to...
        for shapeElement in shapes:
            shapeElement.transition()
            img = shapeElement.tempImage.convert("RGBA")
            config.destinationImage.paste(
                img, (shapeElement.shapeXPosition, shapeElement.shapeYPosition), img
            )

        if config.useTweenTriggers == True:
            colorTransitionStarted()

    if config.shapeTweening == 2:
        config.tweenCount += 1
        config.destinationImage
        alpha = config.tweenCount / config.tweenCountMax
        composited = Image.blend(config.image, config.destinationImage, alpha=alpha)
        config.image.paste(composited, (0, 0), composited)

        # Really an alpha of .5 is good enough to allow full redraw
        if config.tweenCount > config.tweenCountMax / 2:
            config.tweenCount = 0
            config.shapeTweening = 0
            if config.useTweenTriggers == True:
                colorTransitionDone()
            # print("Tweening Done")
            # print("")

    if config.shapeTweening == 0:
        shapeToChange = -1

        sCount = 0
        for shapeElement in shapes:
            if random.random() < shapeElement.changeBoxProb:
                shapeToChange = sCount
            sCount += 1
            #print(shapeToChange)

        shapeCount = 0
        for shapeElement in shapes:
            shapeElement.transition()
            img = shapeElement.tempImage.convert("RGBA")
            config.image.paste(
                img, (shapeElement.shapeXPosition, shapeElement.shapeYPosition), img
            )
            if (
                (shapeElement.varX != 0
                or shapeElement.varY != 0)
                and shapeCount == shapeToChange
            ):
                shapeElement.setNewBox()
                # print("new box: " + shapeElement.name)
                config.shapeTweening = 1
            shapeCount += 1

    '''
    # Disabling in favor of patched dithering
    if config.useVariableFilter == True:
        if random.random() < config.variableFilterProb:
            config.useFilters = False if config.useFilters == True else True
    '''

    if config.useVariablePixelSort == True:

        if (
            random.random() < config.variablePixelProbOff
            and config.usePixelSort == True
        ):
            config.usePixelSort = False

        if random.random() < config.variablePixelProb and config.usePixelSort == False:
            # config.usePixelSort = False if config.usePixelSort == True else True
            config.usePixelSort = True
            if config.usePixelSort == True:
                # config.useLastOverlay = False
                config.renderImageFullOverlay = Image.new(
                    "RGBA", (config.canvasWidth, config.canvasHeight)
                )
                config.renderDrawOver = ImageDraw.Draw(config.renderImageFullOverlay)
            else:
                config.useLastOverlay = True

    if config.useBadPixels == True:
        badpixels.drawBlanks(config.image, False)
        if random.random() > 0.999:
            badpixels.setBlanksOnScreen()

    if random.random() < config.filterPatchProb:
        #print("should be remapping")
        x1 = round(random.uniform(0,config.canvasWidth))
        x2 = round(random.uniform(x1,config.canvasWidth))
        y1 = round(random.uniform(0,config.canvasHeight))
        y2 = round(random.uniform(y1,config.canvasHeight))

        config.remapImageBlock = True
        config.remapImageBlockSection = (x1, y1, x2, y2)
        config.remapImageBlockDestination = (x1, y1)

    # Don't want the patch to always be there - just little interruptions
    if random.random() < config.filterPatchProb * 1.0 and config.filterPatchProb > 0.0 :
        #print("turning off remapping")
        x1 = 0
        x2 = 0
        y1 = 0
        y2 = 0

        config.remapImageBlock = True
        config.remapImageBlockSection = (x1, y1, x2, y2)
        config.remapImageBlockDestination = (x1, y1)

    if random.random() < config.useLastOverlayProb and config.useLastOverlay == True:
        # config.useLastOverlay = False if config.useLastOverlay == True  else True
        #print("lastOVerlay")
        xPos = config.tileSizeWidth * math.floor(random.uniform(0, config.cols))
        yPos = config.tileSizeHeight * math.floor(random.uniform(0, config.rows))
        config.lastOverlayBox = (xPos, yPos, xPos + config.tileSizeWidth, yPos + config.tileSizeHeight)

        cR = config.lastOverLayColorRange
        lastOverlayFill = colorutils.getRandomColorHSV(cR[0],cR[1],cR[2],cR[3],cR[4],cR[5],cR[6],cR[7])
        #print(lastOverlayFill)
        config.lastOverlayFill = (lastOverlayFill[0], lastOverlayFill[1], lastOverlayFill[2], round(random.uniform(config.lastOverlayAlphaRange[0], config.lastOverlayAlphaRange[1])))
        #config.lastOverlayFill = (10, 0, 0, round(random.uniform(5, 50)))


def runWork():
    global config
    print(bcolors.OKGREEN + "** " + bcolors.BOLD)
    print("RUNNING collage.py")
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
    redraw()

    if len(config.shapeGroups) > 1 :
        config.t1 = time.time()

        if (config.t1 - config.t2) > config.timeBetweenSetChanges :
            ## Beeps ... for debugging
            #print(chr(7))
            config.t2 = time.time()
            if random.random() < config.probablilitySetChanges:
                newIndex = math.floor(random.uniform(0,len(config.shapeGroups)))

                # ensure the next index is different ...
                while newIndex == config.shapeGroupDisplayed :
                    newIndex = math.floor(random.uniform(0,len(config.shapeGroups)))
                config.shapeGroupDisplayed = newIndex
                print("--> New Set:" + str(newIndex))

    """
    ## Paste an alpha of the next image, wait a few ms 
    ## then past a more opaque one again
    ## softens the transitions just enough

    config.pasteDelay = .02

    mask1 = config.image.point(lambda i: min(i * 1, 50))
    config.canvasImage.paste(config.image, (0,0), mask1)
    config.render(config.canvasImage, 0, 0, config.image)
    
    time.sleep(config.pasteDelay)
    mask2 = config.image.point(lambda i: min(i * 25, 100))
    config.canvasImage.paste(config.image, (0,0), mask2)
    config.render(config.canvasImage, 0, 0, config.image)
    
    time.sleep(config.pasteDelay)
    mask3 = config.image.point(lambda i: min(i * 25, 255))
    config.canvasImage.paste(config.image, (0,0), mask3)
    config.render(config.canvasImage, 0, 0, config.image)
    """


    if random.random() < config.blurChangeProb:
        config.sectionBlurRadius = round(random.uniform(1,3))


    if random.random() < config.filterRemappingProb:
        if config.useFilters == True and config.filterRemapping == True:
            config.filterRemap = True
            #print("Doing remap filter")

            #startX = round(random.uniform(0,config.canvasWidth - config.filterRemapminHoriSize) )
            #startY = round(random.uniform(0,config.canvasHeight - config.filterRemapminVertSize) )
            #endX = round(random.uniform(startX+config.filterRemapminHoriSize,config.canvasWidth) )
            #endY = round(random.uniform(startY+config.filterRemapminVertSize,config.canvasHeight) )
            # new version  more control but may require previous pieces to be re-worked
            startX = round(random.uniform(0,config.filterRemapRangeX) )
            startY = round(random.uniform(0,config.filterRemapRangeY) )
            endX = round(random.uniform(4, config.filterRemapminHoriSize) )
            endY = round(random.uniform(4, config.filterRemapminVertSize) )
            config.remapImageBlockSection = [startX,startY,startX + endX, startY + endY]
            config.remapImageBlockDestination = [startX,startY]



    config.render(config.image, 0, 0, config.screenWidth, config.screenHeight)

    # Done


def colorTransitionDone(arg=None):
    # print("colorTransition   Done ")
    if config.useTransitionCallbacks == True:
        config.useFilters = False
        config.usePixelSort = True


def colorTransitionStarted(arg=None):
    # print("colorTransition   Started ")
    if config.useTransitionCallbacks == True:
        config.useFilters = True
        config.usePixelSort = False


def main(run=True):
    global config
    global shapeGroups
    global workConfig

    config.t1 = time.time()
    config.t2 = time.time()
    
    # managing speed of animation and framerate
    config.directorController = Director(config)
    try :
        config.delay = float(workConfig.get("collageShapes", "delay"))
        config.directorController.slotRate = float(workConfig.get("collageShapes", "slotRate"))
    except Exception as e:
        print(e)
        config.delay = .03
        config.directorController.slotRate = .04
        
        

    config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.draw = ImageDraw.Draw(config.image)
    config.destinationImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))

    try:
        config.useLastOverlay = workConfig.getboolean("displayconfig", "useLastOverlay")
        config.useLastOverlayProb = float(
            workConfig.get("displayconfig", "useLastOverlayProb")
        )
    except Exception as e:
        print(e)
        config.useLastOverlay = False
        config.useLastOverlayProb = 0.001

    config.transitionStepsMin = int(
        workConfig.get("collageShapes", "transitionStepsMin")
    )
    config.transitionStepsMax = int(
        workConfig.get("collageShapes", "transitionStepsMax")
    )
    config.changeBoxProb = float(workConfig.get("collageShapes", "changeBoxProb"))
    config.redrawSpeed = float(workConfig.get("collageShapes", "redrawSpeed"))
    config.shapeTweening = 0
    config.tweenCount = 0
    config.tweenCountMax = int(workConfig.get("collageShapes", "tweenCountMax"))
    config.colOverlaytLimitBase = int(
        workConfig.get("collageShapes", "colOverlaytLimitBase")
    )
    config.colOverlaySteps = int(workConfig.get("collageShapes", "colOverlaySteps"))
    config.useBadPixels = False

    try:
        config.useTransitionCallbacks = workConfig.getboolean(
            "collageShapes", "useTransitionCallbacks"
        )
    except Exception as e:
        print(e)
        config.useTransitionCallbacks = False

    try:
        config.useTweenTriggers = workConfig.getboolean(
            "collageShapes", "useTweenTriggers"
        )
    except Exception as e:
        print(e)
        config.useTweenTriggers = False

    try:
        config.triggersVals = workConfig.get("collageShapes", "triggers")
        config.triggers = list(
            map(
                lambda x: int(x), workConfig.get("collageShapes", "triggers").split(",")
            )
        )
    except Exception as e:
        print(e)
        config.triggers = []

    try:
        badpixels.numberOfDeadPixels = int(
            workConfig.get("collageShapes", "numberOfDeadPixels")
        )
        badpixels.config = config
        badpixels.sizeTarget = list(config.image.size)
        badpixels.setBlanksOnScreen()
        config.useBadPixels = True
    except Exception as e:
        print(e)

    try:
        config.filterPatchProb = float(workConfig.get("collageShapes", "filterPatchProb"))
    except Exception as e:
        print(e)
        config.filterPatchProb = 0.0
    

    try:
        config.useVariableFilter = workConfig.getboolean("collageShapes", "useVariableFilter")
        config.variableFilterProb = float(workConfig.get("collageShapes", "variableFilterProb"))
        # config.useFilters = True
        # config.usePixelSort = True
    except Exception as e:
        print(e)
        config.useVariableFilter = False

    try:
        config.useVariablePixelSort = workConfig.getboolean(
            "collageShapes", "useVariablePixelSort"
        )
        config.variablePixelProb = float(
            workConfig.get("collageShapes", "variablePixelProb")
        )
        try:
            config.variablePixelProbOff = float(
                workConfig.get("collageShapes", "variablePixelProbOff")
            )
        except Exception as e:
            print(e)
            config.variablePixelProbOff = config.variablePixelProb
        # config.useFilters = True
        # config.usePixelSort = True
    except Exception as e:
        print(e)
        config.useVariablePixelSort = False




    # If there are multiple collage shape sets this sets the time between changes and probability that happens
    try:
        config.timeBetweenSetChanges = float(workConfig.get("collageShapes", "timeBetweenSetChanges"))
        config.probablilitySetChanges = float(workConfig.get("collageShapes", "probablilitySetChanges"))
    except Exception as e:
        config.timeBetweenSetChanges = 60.0
        config.probablilitySetChanges = 1.0 
        print(e)
        print("Setting times to " + str(config.timeBetweenSetChanges) + " " + str(config.probablilitySetChanges ))


    config.shapeSets = list(
        map(lambda x: x, workConfig.get("collageShapes", "sets").split(","))
    )

    config.shapeGroups = []


    for n in range(0, len(config.shapeSets)):

        shapeSetGroup = list(
            map(lambda x: x, workConfig.get("collageShapes", config.shapeSets[n]).split(","))
        )

        shapeGroupList = []

        for i in range(0, len(shapeSetGroup)):

            shapeDetails = shapeSetGroup[i]
            shape = Shape(config)

            shape.varX = float(workConfig.get(shapeDetails, "varX"))
            shape.varY = float(workConfig.get(shapeDetails, "varY"))

            shapePosition = list(
                map(lambda x: int(x), workConfig.get(shapeDetails, "position").split(","))
            )
            shape.shapeXPosition = shapePosition[0]
            shape.shapeYPosition = shapePosition[1]
            shape.name = "S_" + str(i)

            shapeCoords = list(
                map(lambda x: int(x), workConfig.get(shapeDetails, "coords").split(","))
            )
            shape.coords = []

            for c in range(0, len(shapeCoords), 2):
                shape.coords.append((shapeCoords[c], shapeCoords[c + 1]))

            try:
                shape.minHue = float(workConfig.get(shapeDetails, "minHue"))
                shape.maxHue = float(workConfig.get(shapeDetails, "maxHue"))
                shape.maxSaturation = float(workConfig.get(shapeDetails, "maxSaturation"))
                shape.minSaturation = float(workConfig.get(shapeDetails, "minSaturation"))
                shape.maxValue = float(workConfig.get(shapeDetails, "maxValue"))
                shape.minValue = float(workConfig.get(shapeDetails, "minValue"))

            except Exception as e:
                print(e)
                shape.minHue = 0
                shape.maxHue = 360
                shape.maxSaturation = 1
                shape.minSaturation = 0.1
                shape.maxValue = 1
                shape.minValue = 0.1

            # addding individual change probabilities to each shape
            try:
                shape.changeBoxProb  = float(workConfig.get(shapeDetails, "changeBoxProb"))
            except Exception as e:
                print(str(e))
                shape.changeBoxProb  = config.changeBoxProb

            shape.setUp()

            # A couple overrides ...
            shape.colOverlay.tLimitBase = config.colOverlaytLimitBase
            shape.colOverlay.steps = config.colOverlaySteps
            shape.colOverlay.colorTransitionSetupValues()

            if i in config.triggers:
                shape.colOverlay.setCallBackDoneMethod(colorTransitionDone)
                shape.colOverlay.setCallBackStartedMethod(colorTransitionStarted)

            # shape.callBackDone = types.MethodType(callBackDone, shape)
            shape.reDraw()
            shapeGroupList.append(shape)

        config.shapeGroups.append(shapeGroupList)

    # Always start with the first one, index 0
    config.shapeGroupDisplayed = 0

    try:
        config.lastOverLayColorRange = list(
            map(lambda x: float(x), workConfig.get("collageShapes", "lastOverLayColorRange").split(","))
        )
    except Exception as e:
        print(str(e))
        config.lastOverLayColorRange = (0,10,.5,1.0,.5,.5)

    try:
        config.lastOverlayAlphaRange = tuple(map(lambda x: int(x), workConfig.get("collageShapes", "lastOverlayAlphaRange").split(",")))
    except Exception as e:
        print(str(e))
        config.lastOverlayAlphaRange = (5,50)

    try:
        config.useLastOverlay = workConfig.getboolean("collageShapes", "forceLastOverlay")
        config.useLastOverlayProb = float(workConfig.get("collageShapes", "useLastOverlayProb"))
        config.useLastOverlayProb = float(workConfig.get("collageShapes", "useLastOverlayProb"))
        config.lastOverlayBox = tuple(map(lambda x: int(x), workConfig.get("collageShapes", "lastOverlayBox").split(",")))
        config.renderImageFullOverlay = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
        config.renderDrawOver = ImageDraw.Draw(config.renderImageFullOverlay)
        config.lastOverlayFill = tuple(	map(lambda x: int(x), workConfig.get("collageShapes", "lastOverlayFill").split(",")))
    except Exception as e:
        print(str(e))
        config.lastOverlayBox = (0, 0, 64, 32)
        config.lastOverlayFill = (0, 0, 0, 0)
        config.useLastOverlay = False

    try:
        config.blurChangeProb = float(workConfig.get("collageShapes", "blurChangeProb"))
    except Exception as e:
        config.blurChangeProb = 0.0
        print(e)

    try:
        config.lastOverlayBlur = float(workConfig.get("collageShapes", "lastOverlayBlur"))
    except Exception as e:
        config.lastOverlayBlur = 0.0
        print(e)


    

    if run:
        runWork()
