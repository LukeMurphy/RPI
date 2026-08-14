# ################################################### #
import argparse
import math
import random
import time
import types

from modules import badpixels, coloroverlay, colorutils
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps
from modules.configuration import bcolors
from modules.blanks_and_dither_rempping import BlanksAndDitherRemapping
from modules.holder_director import Holder
from modules.holder_director import Director
from modules import distortions

lastRate = 0
colorutils.brightness = 1
shapes = []


# Really no need for a class here - it's always a singleton and besides
# with Python everthing is an object already .... some kind of OOP
# holdover anxiety I guess

#-----------------------------------------------#

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
    alpha = 255
    steps = 20

    def __init__(self, config, clgMngr, i=0):
        # print ("init Fludd", i)

        # self.boxMax = config.screenWidth - 1
        # self.boxMaxAlt = self.boxMax + int(random.uniform(10,30) * config.screenWidth)
        # self.boxHeight = config.screenHeight - 2        #

        self.unitNumber = i
        self.config = config
        self.clgMngr = clgMngr
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
            self.clgMngr.transitionStepsMin,
            self.clgMngr.transitionStepsMax,
        )
        self.colOverlay.colorTransitionSetup()
        self.colOverlay.setStartColor()
        self.colOverlay.getNewColor()

        self.fillColor = tuple(int(a * self.config.brightness) for a in self.colOverlay.currentColor)

        self.widthDelta = 0
        self.heightDelta = 0
        self.xDelta = 0
        self.yDelta = 0
        self.poly = []

        self.setNewBox()

    def changeAction(self):
        return False

    def setNewBox(self):
        self.draw.rectangle((0, 0, self.boxMax, self.boxHeight), fill=(0, 0, 0, 255), outline=None)
        self.poly = []
        for p in self.coords:
            xPos = self.varX + round(p[0] + random.uniform(-self.varX, self.varX))
            yPos = self.varY + round(p[1] + random.uniform(-self.varY, self.varY))
            self.poly.append((xPos, yPos))

    def transition(self):

        self.colOverlay.stepTransition()
        self.fillColor = []
        self.fillColor.extend(
            round(self.colOverlay.currentColor[i] * self.config.brightness)
            for i in range(3)
        )

        self.fillColor.append(self.alpha)
        self.fillColor = tuple(int(a) for a in self.fillColor)

        self.draw.rectangle((0, 0, self.boxMax, self.boxHeight), fill=(0, 0, 0, 10), outline=None)
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


class CollageManager:
    def __init__(self, config):
        self.config = config

    def setUp(self, workConfig):
        config = self.config
        self.t1 = time.time()
        self.t2 = time.time()

        config.doingSectionDisturbance = False
        config.rebuildingPattern = True

        try:
            testForDistortionSetup = workConfig.get("distortionsConfigs", "sectionDisturbance")
            distortions.distortionsConfigs(config, workConfig)
        except Exception as e:
            print(f" ==> No distortionsConfigs or sectionDisturbance: {e}")
            config.sectionDisturbance = False
            config.useWaveDistortion = False
            config.imgcanvasOffsetX = 0
            config.imgcanvasOffsetY = 0

        self.shapeTweening = 0
        self.tweenCount = 0
        self.useBadPixels = False
        self.triggersVals = workConfig.get("collageShapes", "triggers", fallback = "")
        if self.triggersVals == "" :
            self.triggers = []
        else :
            self.triggers = list(map(lambda x: int(x), self.triggersVals.split(",")))


        self.useLastOverlay = workConfig.getboolean("displayconfig", "useLastOverlay", fallback = False)
        self.useVariablePixelSort = workConfig.getboolean("collageShapes", "useVariablePixelSort", fallback = False)
        self.useTransitionCallbacks = workConfig.getboolean("collageShapes", "useTransitionCallbacks", fallback = False)
        self.useTweenTriggers = workConfig.getboolean("collageShapes", "useTweenTriggers", fallback = False)
        self.useTweenTriggers = workConfig.getboolean("collageShapes", "useTweenTriggers", fallback = False)
        self.useVariableFilter = workConfig.getboolean("collageShapes", "useVariableFilter", fallback = False)
            
        self.transitionStepsMin = int(workConfig.get("collageShapes", "transitionStepsMin", fallback = 0))
        self.transitionStepsMax = int(workConfig.get("collageShapes", "transitionStepsMax", fallback = 0))
        self.tweenCountMax = int(workConfig.get("collageShapes", "tweenCountMax", fallback = 0))
        self.colOverlaySteps = int(workConfig.get("collageShapes", "colOverlaySteps", fallback = 0))
        self.colOverlaytLimitBase = int(workConfig.get("collageShapes", "colOverlaytLimitBase", fallback = 0))

        self.changeBoxProb = float(workConfig.get("collageShapes", "changeBoxProb", fallback = 0.0))
        self.redrawSpeed = float(workConfig.get("collageShapes", "redrawSpeed", fallback = 0.0))
        self.useLastOverlayProb = float(workConfig.get("displayconfig", "useLastOverlayProb", fallback = 0.001))
        self.resetProbability = float(workConfig.get("collageShapes", "resetProbability", fallback = 0.0001))
        self.filterPatchProb = float(workConfig.get("collageShapes", "filterPatchProb", fallback = 0.0))
        self.minFilterPatchWidth = float(workConfig.get("collageShapes", "minFilterPatchWidth", fallback = 0.0))
        self.minFilterPatchHeight = float(workConfig.get("collageShapes", "minFilterPatchHeight", fallback = 0.0))
        self.variableFilterProb = float(workConfig.get("collageShapes", "variableFilterProb", fallback = 0.0))
        self.variablePixelProb = float(workConfig.get("collageShapes", "variablePixelProb", fallback = 0.0))
        try:
            self.variablePixelProbOff = float(workConfig.get("collageShapes", "variablePixelProbOff"))
        except Exception as e:
            print(e)
            self.variablePixelProbOff = self.variablePixelProb


        self.shapeSets = list(map(lambda x: x, workConfig.get("collageShapes", "sets").split(",")))
        self.timeBetweenSetChanges = float(workConfig.get("collageShapes", "timeBetweenSetChanges", fallback=60.0))
        self.probablilitySetChanges = float(workConfig.get("collageShapes", "probablilitySetChanges", fallback=0.0))
        # try:


        try:
            badpixels.numberOfDeadPixels = int(workConfig.get("collageShapes", "numberOfDeadPixels"))
            badpixels.config = config
            badpixels.sizeTarget = list(config.image.size)
            badpixels.setBlanksOnScreen()
            self.useBadPixels = True
        except Exception as e:
            print(e)

        #     config.timeBetweenSetChanges = float(workConfig.get("collageShapes", "timeBetweenSetChanges"))
        #     config.probablilitySetChanges = float(workConfig.get("collageShapes", "probablilitySetChanges"))
        # except Exception as e:
        #     config.timeBetweenSetChanges = 60.0
        #     config.probablilitySetChanges = .0
        #     print(e)
        #     print(f"Setting times to {config.timeBetweenSetChanges} {config.probablilitySetChanges}")


        _initialize_shapes(config, self, workConfig)
        _initialize_overlay_settings(config, self, workConfig)


#-----------------------------------------------#

def redraw():
    global config, clgMngr

    shapes = clgMngr.shapeGroups[clgMngr.shapeGroupDisplayed]

    _handle_shape_tweening(config, clgMngr, shapes)

    if clgMngr.shapeTweening == 0:
        _draw_shapes_and_handle_changes(config, clgMngr, shapes)

    _handle_pixel_sort(config, clgMngr)
    _handle_bad_pixels(config, clgMngr)
    _handle_last_overlay(config, clgMngr)
    overlayControls.handleOverlayActions()


def _handle_shape_tweening(config, clgMngr, shapes):
    if clgMngr.shapeTweening == 1:
        clgMngr.shapeTweening = 2
        _generate_transition_state(config, shapes)
        if clgMngr.useTweenTriggers:
            colorTransitionStarted()

    if clgMngr.shapeTweening == 2:
        _perform_tweening(config, clgMngr)


def _generate_transition_state(config, shapes):
    for shapeElement in shapes:
        shapeElement.transition()
        img = shapeElement.tempImage.convert("RGBA")
        config.destinationImage.paste(img, (shapeElement.shapeXPosition, shapeElement.shapeYPosition), img)


def _perform_tweening(config, clgMngr):
    clgMngr.tweenCount += 1
    alpha = clgMngr.tweenCount / clgMngr.tweenCountMax
    composited = Image.blend(config.image, config.destinationImage, alpha=alpha)
    config.image.paste(composited, (0, 0), composited)

    if clgMngr.tweenCount > clgMngr.tweenCountMax / 2:
        clgMngr.tweenCount = 0
        clgMngr.shapeTweening = 0
        if clgMngr.useTweenTriggers:
            colorTransitionDone()


def _draw_shapes_and_handle_changes(config, clgMngr, shapes):
    shapeToChange = -1
    for sCount, shapeElement in enumerate(shapes):
        if random.random() < shapeElement.changeBoxProb:
            shapeToChange = sCount
    for shapeCount, shapeElement in enumerate(shapes):
        shapeElement.transition()
        img = shapeElement.tempImage.convert("RGBA")
        config.image.paste(img, (shapeElement.shapeXPosition, shapeElement.shapeYPosition), img)
        if (shapeElement.varX != 0 or shapeElement.varY != 0) and shapeCount == shapeToChange:
            shapeElement.setNewBox()
            clgMngr.shapeTweening = 1


def _handle_pixel_sort(config, clgMngr):
    if clgMngr.useVariablePixelSort:
        if random.random() < clgMngr.variablePixelProbOff and config.usePixelSort:
            config.usePixelSort = False

        if random.random() < clgMngr.variablePixelProb and not config.usePixelSort:
            config.usePixelSort = True
            if config.usePixelSort:
                config.renderImageFullOverlay = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
                config.renderDrawOver = ImageDraw.Draw(config.renderImageFullOverlay)
            else:
                config.useLastOverlay = True


def _handle_bad_pixels(config, clgMngr):
    if clgMngr.useBadPixels:
        badpixels.drawBlanks(config.image, False)
        if random.random() > 0.999:
            badpixels.setBlanksOnScreen()


# def _handle_filter_patch(config, clgMngr):
#     if random.random() < clgMngr.filterPatchProb:
#         _remap_image_block(config, clgMngr)

#     if random.random() < clgMngr.filterPatchProb * .50 and clgMngr.filterPatchProb > 0.0:
#         _reset_remap_image_block(config)


def _handle_last_overlay(config, clgMngr):
    if random.random() < clgMngr.useLastOverlayProb and config.useLastOverlay:
        _draw_last_overlay(config, clgMngr)


# def _remap_image_block(config, clgMngr):
#     x1 = round(random.uniform(0, config.canvasWidth - + clgMngr.minFilterPatchWidth))
#     x2 = round(random.uniform(x1 + clgMngr.minFilterPatchWidth, config.canvasWidth + clgMngr.minFilterPatchWidth))
#     y1 = round(random.uniform(0, config.canvasHeight - + clgMngr.minFilterPatchHeight))
#     y2 = round(random.uniform(y1 + clgMngr.minFilterPatchHeight, config.canvasHeight + clgMngr.minFilterPatchHeight))

#     config.remapImageBlock = True
#     config.remapImageBlockSection = (x1, y1, x2, y2)
#     config.remapImageBlockDestination = (x1, y1)


# def _reset_remap_image_block(config):
#     config.remapImageBlock = True
#     config.remapImageBlockSection = (0, 0, 0, 0)
#     config.remapImageBlockDestination = (0, 0)


def _draw_last_overlay(config, clgMngr):
    xPos = config.tileSizeWidth * math.floor(random.uniform(0, config.cols))
    yPos = config.tileSizeHeight * math.floor(random.uniform(0, config.rows))
    # config.lastOverlayBox = (xPos, yPos, xPos + config.tileSizeWidth, yPos + config.tileSizeHeight)
    config.lastOverlayBox = (xPos, yPos, xPos + config.lastOverlayBox[0], yPos + config.lastOverlayBox[1])

    cR = clgMngr.lastOverLayColorRange
    lastOverlayFill = colorutils.getRandomColorHSV(cR[0], cR[1], cR[2], cR[3], cR[4], cR[5], cR[6], cR[7])

    config.lastOverlayFill = (
        lastOverlayFill[0],
        lastOverlayFill[1],
        lastOverlayFill[2],
        round(random.uniform(clgMngr.lastOverlayAlphaRange[0], clgMngr.lastOverlayAlphaRange[1])),
    )


def runWork():
    global config, clgMngr
    print(f"{bcolors.OKGREEN}** {bcolors.BOLD}")
    print("RUNNING collage.py")
    print(bcolors.ENDC)
    while config.isRunning == True:
        config.directorController.checkTime()
        if config.directorController.advance == True:
            iterate()
            time.sleep(clgMngr.delay)
        if config.standAlone == False:
            config.callBack()


def iterate():
    global config, clgMngr
    redraw()

    if len(clgMngr.shapeGroups) > 1:
        clgMngr.t1 = time.time()

        if (clgMngr.t1 - clgMngr.t2) > clgMngr.timeBetweenSetChanges:
            ## Beeps ... for debugging
            # print(chr(7))
            clgMngr.t2 = time.time()
            if random.random() < clgMngr.probablilitySetChanges:
                newIndex = math.floor(random.uniform(0, len(clgMngr.shapeGroups)))

                # ensure the next index is different ...
                while newIndex == clgMngr.shapeGroupDisplayed:
                    newIndex = math.floor(random.uniform(0, len(clgMngr.shapeGroups)))
                clgMngr.shapeGroupDisplayed = newIndex
                print(f"--> New Set:{str(newIndex)}")


    if random.random() < clgMngr.blurChangeProb:
        config.sectionBlurRadius = round(random.uniform(1, 3))

    if config.sectionDisturbance == True:
        distortions.iterationFunction(config)

    temp1 = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    temp1Draw = ImageDraw.Draw(temp1)

    config.image.paste(config.canvasImage, (0, 0), config.canvasImage)
    temp1.paste(config.image, (0, 0), config.image)

    if config.useWaveDistortion == True:
        temp1 = ImageOps.deform(temp1, distortions.WaveDeformer(config))
        config.waveDeformXPos += config.waveDeformXPosRate
        if config.waveDeformXPos > config.screenWidth:
            config.waveDeformXPos = 0

    config.render(temp1, config.imgcanvasOffsetX, config.imgcanvasOffsetY, config.canvasWidth, config.canvasHeight)

    if random.random() < clgMngr.resetProbability :
        _imageReset()


def _imageReset():
    img = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    tempDraw = ImageDraw.Draw(img)
    tempDraw.rectangle((0,0,config.canvasWidth, config.canvasHeight), fill=(0,0,0,200))
    config.destinationImage.paste(img, (0, 0), img)
    _initialize_shapes(config, clgMngr, workConfig)
    _initialize_overlay_settings(config, clgMngr, workConfig)


def _newFilterRemapping(config, clgMngr):
    config.filterRemap = True
    # print("Doing remap filter")

    # startX = round(random.uniform(0,config.canvasWidth - config.filterRemapminHoriSize) )
    # startY = round(random.uniform(0,config.canvasHeight - config.filterRemapminVertSize) )
    # endX = round(random.uniform(startX+config.filterRemapminHoriSize,config.canvasWidth) )
    # endY = round(random.uniform(startY+config.filterRemapminVertSize,config.canvasHeight) )
    # new version  more control but may require previous pieces to be re-worked
    startX = round(random.uniform(0, clgMngr.filterRemapRangeX))
    startY = round(random.uniform(0, clgMngr.filterRemapRangeY))
    endX = round(random.uniform(4, clgMngr.filterRemapminHoriSize))
    endY = round(random.uniform(4, clgMngr.filterRemapminVertSize))
    config.remapImageBlockSection = [startX, startY, startX + endX, startY + endY]
    config.remapImageBlockDestination = [startX, startY]
    # Done

    # config.render(config.image, 0, 0, config.screenWidth, config.screenHeight)

    # Done


def colorTransitionDone(arg=None):
    # print("colorTransition   Done ")
    if clgMngr.useTransitionCallbacks == True:
        config.useFilters = False
        config.usePixelSort = True


def colorTransitionStarted(arg=None):
    print("colorTransition   Started ")
    if clgMngr.useTransitionCallbacks == True:
        config.useFilters = True
        config.usePixelSort = False


def main(run=True):
    global config, shapeGroups, workConfig, clgMngr
    print("\n Main Init:")

    clgMngr = CollageManager(config)
    clgMngr.setUp(workConfig)

    config.directorController = Director(config)
    _load_config_value(clgMngr, workConfig, "collageShapes", "delay", 0.03, float)
    _load_config_value(clgMngr, workConfig, "collageShapes", "slotRate", 0.04, float)
    
    config.directorController.delay = clgMngr.delay
    config.directorController.slotRate = config.slotRate

    config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.draw = ImageDraw.Draw(config.image)
    config.destinationImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))

    config.canvasDraw = ImageDraw.Draw(config.canvasImage)
    config.disturbanceImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))

    global overlayControls
    overlayControls = BlanksAndDitherRemapping(config, workConfig, "collageShapes")


    if run:
        runWork()


def _initialize_shapes(config, clgMngr, workConfig):
    clgMngr.shapeGroups = []

    for item in clgMngr.shapeSets:
        shapeSetGroup = list(map(lambda x: x, workConfig.get("collageShapes", item).split(",")))
        shapeGroupList = []

        for i in range(len(shapeSetGroup)):
            shapeDetails = shapeSetGroup[i]
            shape = Shape(config, clgMngr)

            shape.varX = float(workConfig.get(shapeDetails, "varX"))
            shape.varY = float(workConfig.get(shapeDetails, "varY"))

            shapePosition = list(map(lambda x: int(x), workConfig.get(shapeDetails, "position").split(",")))
            shape.shapeXPosition = shapePosition[0]
            shape.shapeYPosition = shapePosition[1]
            shape.name = f"S_{str(i)}"

            shapeCoords = list(map(lambda x: int(x), workConfig.get(shapeDetails, "coords").split(",")))
            shape.coords = []

            shape.coords.extend((shapeCoords[c], shapeCoords[c + 1]) for c in range(0, len(shapeCoords), 2))

            _load_config_value(shape, workConfig, shapeDetails, "minHue", 0, float)
            _load_config_value(shape, workConfig, shapeDetails, "maxHue", 360, float)
            _load_config_value(shape, workConfig, shapeDetails, "maxSaturation", 1, float)
            _load_config_value(shape, workConfig, shapeDetails, "minSaturation", 0.1, float)
            _load_config_value(shape, workConfig, shapeDetails, "maxValue", 1, float)
            _load_config_value(shape, workConfig, shapeDetails, "minValue", 0.1, float)
            _load_config_value(shape, workConfig, shapeDetails, "alpha", 255, float)

            try:
                shape.changeBoxProb = float(workConfig.get(shapeDetails, "changeBoxProb"))
            except Exception as e:
                print(e)
                shape.changeBoxProb = clgMngr.changeBoxProb

            shape.setUp()

            shape.colOverlay.tLimitBase = clgMngr.colOverlaytLimitBase
            shape.colOverlay.steps = clgMngr.colOverlaySteps
            shape.colOverlay.colorTransitionSetupValues()

            if i in clgMngr.triggers:
                shape.colOverlay.setCallBackDoneMethod(colorTransitionDone)
                shape.colOverlay.setCallBackStartedMethod(colorTransitionStarted)

            shape.reDraw()
            shapeGroupList.append(shape)

        clgMngr.shapeGroups.append(shapeGroupList)

    clgMngr.shapeGroupDisplayed = 0


def _initialize_overlay_settings(config, clgMngr, workConfig):
    try:
        clgMngr.lastOverLayColorRange = list(map(lambda x: float(x), workConfig.get("collageShapes", "lastOverLayColorRange").split(",")))
    except Exception as e:
        print(e)
        clgMngr.lastOverLayColorRange = (0, 10, 0.5, 1.0, 0.5, 0.5)

    try:
        clgMngr.lastOverlayAlphaRange = tuple(map(lambda x: int(x), workConfig.get("collageShapes", "lastOverlayAlphaRange").split(",")))
    except Exception as e:
        print(e)
        clgMngr.lastOverlayAlphaRange = (5, 50)

    _load_config_value(clgMngr, workConfig, "collageShapes", "forceLastOverlay", False, bool)
    _load_config_value(clgMngr, workConfig, "collageShapes", "useLastOverlayProb", 0.0, float)

    try:
        config.lastOverlayBox = tuple(map(lambda x: int(x), workConfig.get("collageShapes", "lastOverlayBox").split(",")))
        config.renderImageFullOverlay = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
        config.renderDrawOver = ImageDraw.Draw(config.renderImageFullOverlay)
        config.lastOverlayFill = tuple(map(lambda x: int(x), workConfig.get("collageShapes", "lastOverlayFill").split(",")))
    except Exception as e:
        print(e)
        config.lastOverlayBox = (0, 0, 64, 32)
        config.lastOverlayFill = (0, 0, 0, 0)
        config.useLastOverlay = False

    _load_config_value(clgMngr, workConfig, "collageShapes", "blurChangeProb", 0.0, float)
    _load_config_value(config, workConfig, "collageShapes", "lastOverlayBlur", 0.0, float)


def _load_config_value(obj, workConfig, section, option, default, type_converter):
    try:
        setattr(obj, option, type_converter(workConfig.get(section, option)))
    except Exception as e:
        print(f"=> Failed to set {section}.{option} {e}")
        setattr(obj, option, default)
