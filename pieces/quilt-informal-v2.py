import contextlib
import math
import random
import time
# from noise import *
from threading import Timer
from PIL import Image,  ImageDraw, ImageOps
from modules import distortions
from modules import coloroverlay, colorutils, panelDrawing
from modules.holder_director import Director
from modules.configuration import bcolors, pieceLogger

def setTimeout(fn, ms, *args, **kwargs):
    t = Timer(ms / 1000.0, fn, args=args, kwargs=kwargs)
    t.start()
    return t


## This quilt supercedes the quilt.py module because it accounts for a zero irregularity
## as well as the infomal bar construction

class QuiltManager:
    def __init__(self, config):
        self.config = config

    def setUp(self, workConfig):
        self.canvasImageWidth = self.config.screenWidth
        self.canvasImageHeight = self.config.screenHeight
        # self.canvasImageWidth -= 4
        # self.canvasImageHeight -= 4

        self.outlineColorObj = coloroverlay.ColorOverlay()
        self.outlineColorObj.randomRange = (5.0, 30.0)
        self.outlineColorObj.colorTransitionSetup()

        self.transitionStepsMin = float(
            workConfig.get("quilt-informal", "transitionStepsMin")
        )
        self.transitionStepsMax = float(
            workConfig.get("quilt-informal", "transitionStepsMax")
        )

        self.transformShape = workConfig.getboolean("quilt-informal", "transformShape")
        transformTuples = workConfig.get("quilt-informal", "transformTuples").split(",")
        self.transformTuples = tuple(float(i) for i in transformTuples)

        redRange = workConfig.get("quilt-informal", "redRange").split(",")
        self.redRange = tuple(int(i) for i in redRange)

        try:
            saturationRangeFactorLeft = workConfig.get(
                "quilt-informal", "saturationRangeFactorLeft"
            ).split(",")
            self.saturationRangeFactorLeft = tuple(
                float(i) for i in saturationRangeFactorLeft
            )

            saturationRangeFactorRight = workConfig.get(
                "quilt-informal", "saturationRangeFactorRight"
            ).split(",")
            self.saturationRangeFactorRight = tuple(
                float(i) for i in saturationRangeFactorRight
            )

        except Exception as e:
            pieceLogger(e, 1)
            self.saturationRangeFactorLeft = (1, 1)
            self.saturationRangeFactorRight = (1, 1)

        backgroundColor = workConfig.get("quilt-informal", "backgroundColor").split(",")
        self.backgroundColor = tuple(int(i) for i in backgroundColor)

        self.numUnits = int(workConfig.get("quilt-informal", "numUnits"))
        self.hGapSize = int(workConfig.get("quilt-informal", "hGapSize"))
        self.vGapSize = int(workConfig.get("quilt-informal", "vGapSize"))
        self.blockSize = int(workConfig.get("quilt-informal", "blockSize"))
        self.blockLength = float(workConfig.get("quilt-informal", "blockLength"))
        self.blockHeight = float(workConfig.get("quilt-informal", "blockHeight"))
        self.blockLengthBase = float(workConfig.get("quilt-informal", "blockLength"))
        self.blockHeightBase = float(workConfig.get("quilt-informal", "blockHeight"))
        self.blockRows = int(workConfig.get("quilt-informal", "blockRows"))
        self.blockCols = int(workConfig.get("quilt-informal", "blockCols"))
        self.cntrOffsetX = int(workConfig.get("quilt-informal", "cntrOffsetX"))
        self.cntrOffsetY = int(workConfig.get("quilt-informal", "cntrOffsetY"))
        self.colorPopProb = float(workConfig.get("quilt-informal", "colorPopProb"))
        self.brightnessFactorDark = float(
            workConfig.get("quilt-informal", "brightnessFactorDark")
        )
        self.brightnessFactorLight = float(
            workConfig.get("quilt-informal", "brightnessFactorLight")
        )
        self.lines = workConfig.getboolean("quilt-informal", "lines")
        self.patternPrecision = workConfig.getboolean(
            "quilt-informal", "patternPrecision"
        )

        self.polyDistortion = float(workConfig.get("quilt-informal", "polyDistortion"))
        self.polyDistortionMin = -self.polyDistortion
        self.polyDistortionMax = self.polyDistortion

        # stacking the decks a bit in favor of vertical lightening strike and regular
        try:
            self.opticalPatterns = workConfig.get(
                "quilt-informal", "opticalPatterns"
            ).split(",")
        except Exception as e:
            pieceLogger(e, 1)
            self.opticalPatterns = [
                "Regular",
                "Regular",
                "LighteningStrikeH",
                "LighteningStrikeH",
                "Diagonals",
                "LighteningStrikeH",
            ]

        # Chance that when the Quilt rebuilds the pattern doubles in size
        self.sizeFactorChangeProb = float(
            workConfig.get("quilt-informal", "sizeFactorChangeProb")
        )
        self.baseSizeMultiplier = float(
            workConfig.get("quilt-informal", "baseSizeMultiplier")
        )
        self.extraSizeMultiplier = float(
            workConfig.get("quilt-informal", "extraSizeMultiplier")
        )

        p = math.floor(random.SystemRandom().uniform(0, len(self.opticalPatterns)))
        self.opticalPattern = self.opticalPatterns[p]

        self.timeToComplete = int(workConfig.get("quilt-informal", "timeToComplete"))


class unit:

    timeTrigger = True
    tLimitBase = 30

    maxBrightness = 1

    minSaturation = 1
    maxSaturation = 1

    minValue = 1
    maxValue = 1

    minHue = 0
    maxHue = 360

    def __init__(self, config, qMngr):
        self.config = config
        self.qMngr = qMngr
        self.xPos = 0
        self.yPos = 0
        self.redraw = False

        self.draw = ImageDraw.Draw(config.image)

        ## Like the "stiching" color and affects the overall "tone" of the piece
        self.outlineColor = qMngr.outlineColorObj.currentColor
        self.objWidth = 20

        self.outlineRange = [(20, 20, 250)]
        self.brightness = 1
        self.fillColorMode = "random"
        self.lineColorMode = "red"
        self.changeColor = True
        self.lines = qMngr.lines

    def setUp(self, n=0):

        self.outlineColor = tuple(
            int(a * self.brightness) for a in (self.outlineColorObj.currentColor)
        )

        #### Sets up color transitions
        self.colOverlay = coloroverlay.ColorOverlay()
        self.colOverlay.randomSteps = True
        self.colOverlay.timeTrigger = True
        self.colOverlay.tLimitBase = 5
        self.colOverlay.tLimit = 5
        self.colOverlay.steps = 10

        self.colOverlay.maxBrightness = self.config.brightness
        self.colOverlay.maxBrightness = self.maxBrightness

        self.colOverlay.minSaturation = self.minSaturation
        self.colOverlay.maxSaturation = self.maxSaturation

        self.colOverlay.minValue = self.minValue
        self.colOverlay.maxValue = self.maxValue

        self.colOverlay.minHue = self.minHue
        self.colOverlay.maxHue = self.maxHue

        ### This is the speed range of transitions in color
        ### Higher numbers means more possible steps so slower
        ### transitions - 1,10 very blinky, 10,200 very slow
        self.colOverlay.randomRange = (
            self.qMngr.transitionStepsMin,
            self.qMngr.transitionStepsMax,
        )

        """
        self.fillColor = colorutils.getRandomColorHSV(
            sMin = self.minSaturation, sMax = self.maxSaturation,  
            hMin = self.minHue, hMax  = self.maxHue, 
            vMin = self.minValue, vMax = self.maxValue
            )


        self.colOverlay.colorB = colorutils.getRandomColorHSV(
            sMin = self.minSaturation, sMax = self.maxSaturation,  
            hMin = self.minHue, hMax  = self.maxHue, 
            vMin = self.minValue, vMax = self.maxValue
            )

        self.colOverlay.colorA = self.fillColor
        """

        self.colOverlay.setStartColor()
        self.colOverlay.getNewColor()
        self.colOverlay.colorTransitionSetup()

        self.outlineColor = tuple(
            int(a * self.brightness) for a in (self.outlineColorObj.currentColor)
        )
        self.fillColor = tuple(
            int(a * self.brightness) for a in (self.colOverlay.currentColor)
        )

    def update(self):
        # self.fillColorMode == "random" or
        if random.SystemRandom().random() > qMngr.colorPopProb:
            self.colOverlay.stepTransition()
            self.fillColor = tuple(
                int(a * self.brightness) for a in self.colOverlay.currentColor
            )
        else:
            self.changeColorFill()

    def renderPolys(self):

        if self.fillColorMode == "red":
            brightnessFactor = self.qMngr.brightnessFactorDark
        else:
            brightnessFactor = self.qMngr.brightnessFactorLight

        self.outlineColor = tuple(
            int(a * self.brightness * brightnessFactor)
            for a in self.outlineColorObj.currentColor
        )
        self.fillColor = tuple(
            int(a * self.brightness) for a in (self.colOverlay.currentColor)
        )

        if self.lines :
            self.draw.polygon(self.poly, fill=self.fillColor)
        else:
            self.draw.polygon(self.poly, fill=self.fillColor, outline=None)

    def render(self):

        if self.fillColorMode == "red":
            brightnessFactor = self.qMngr.brightnessFactorDark
        else:
            brightnessFactor = self.qMngr.brightnessFactorLight

        self.outlineColor = tuple(
            int(a * self.brightness * brightnessFactor)
            for a in self.outlineColorObj.currentColor
        )
        self.fillColor = tuple(
            int(a * self.brightness) for a in (self.colOverlay.currentColor)
        )

        if self.lines :
            self.draw.rectangle(
                (
                    (self.xPos, self.yPos),
                    (self.xPos + self.blockLength, self.yPos + self.blockHeight),
                ),
                fill=self.fillColor,
                outline=self.outlineColor,
            )
        else:
            self.draw.rectangle(
                (
                    (self.xPos, self.yPos),
                    (self.xPos + self.blockLength, self.yPos + self.blockHeight),
                ),
                fill=self.fillColor,
                outline=None,
            )

    ## Straight color change - deprecated - too blinky
    def changeColorFill(self):

        if self.changeColor :
            if self.fillColorMode == "random":
                self.fillColor = colorutils.randomColor(
                    random.SystemRandom().uniform(0.01, self.brightness)
                )
                self.outlineColor = colorutils.getRandomRGB(
                    random.SystemRandom().uniform(0.01, self.brightness)
                )
            else:
                self.fillColor = colorutils.getRandomColorHSV(
                    sMin=self.minSaturation,
                    sMax=self.maxSaturation,
                    hMin=self.minHue,
                    hMax=self.maxHue,
                    vMin=self.minValue,
                    vMax=self.maxValue,
                )

                self.colOverlay.colorA = self.fillColor


def drawSquareSpiral():

    global config, qMngr

    qMngr.t1 = time.time()
    qMngr.t2 = time.time()

    setTimeout(resetToAllowDistortion, 3000)

    cntrOffset = [qMngr.cntrOffsetX, qMngr.cntrOffsetY]

    qMngr.unitArray = []

    ## Alignment perfect setup
    # if qMngr.patternPrecision :
    #     sizeAdjustor = 1

    n = 0
    # @todo
    # dark factor should be made into parameters
    darkValues = [0.1 * config.brightness, 0.5 * config.brightness]
    lightValues = [0.5 * config.brightness, 1.0 * config.brightness]

    opticalPattern = qMngr.opticalPattern

    """
    LIGHTENING PATTERN
    dark right dark bottom   dark top. dark right
    dark top  dark left.   dark right. dark bottom

    repeat .....


    """

    for rows in range(qMngr.blockRows):

        for cols in range(qMngr.blockCols):

            if opticalPattern == "Diagonals":
                if cols % 2 > 0 and rows % 2 > 0 or cols % 2 <= 0 and rows % 2 <= 0:
                    topValues = darkValues
                    rightValues = darkValues
                    bottomValues = lightValues
                    leftValues = lightValues
                else:
                    topValues = lightValues
                    rightValues = lightValues
                    bottomValues = darkValues
                    leftValues = darkValues
            elif opticalPattern == "LighteningStrike":
                if cols % 2 > 0:
                    if rows % 2 > 0:
                        topValues = lightValues
                        rightValues = darkValues
                        bottomValues = darkValues
                    else:
                        topValues = darkValues
                        rightValues = darkValues
                        bottomValues = lightValues
                    leftValues = lightValues
                else:
                    if rows % 2 > 0:
                        topValues = darkValues
                        rightValues = lightValues
                        bottomValues = lightValues
                    else:
                        topValues = lightValues
                        rightValues = lightValues
                        bottomValues = darkValues
                    leftValues = darkValues
            elif opticalPattern == "LighteningStrikeH":
                if cols % 2 == 0:
                    if rows % 2 == 0:
                        topValues = lightValues
                        rightValues = darkValues
                        bottomValues = darkValues
                        leftValues = lightValues
                    else:
                        topValues = darkValues
                        rightValues = lightValues
                        bottomValues = lightValues
                        leftValues = darkValues
                elif rows % 2 == 0:
                    topValues = lightValues
                    rightValues = lightValues
                    bottomValues = darkValues
                    leftValues = darkValues
                else:
                    topValues = darkValues
                    rightValues = darkValues
                    bottomValues = lightValues
                    leftValues = lightValues

            else:
                topValues = lightValues
                rightValues = lightValues
                bottomValues = darkValues
                leftValues = darkValues

            hDelta = qMngr.numUnits * qMngr.blockLength * 2 + qMngr.hGapSize
            vDelta = qMngr.numUnits * qMngr.blockHeight * 2 + qMngr.vGapSize

            _center = [cols * hDelta + cntrOffset[0], rows * vDelta + cntrOffset[1]]
            outlineColorObj = coloroverlay.ColorOverlay()
            outlineColorObj.randomRange = (5.0, 30.0)
            outlineColorObj.colorTransitionSetup()

            n += 1

            ## Archimedean spiral is  r = a + b * theta
            turns = qMngr.numUnits + 1
            _blockLength = qMngr.blockLength
            _blockHeight = qMngr.blockHeight

            A = []
            B = []
            rangeChange = (qMngr.polyDistortionMin, qMngr.polyDistortionMax)

            for i in range(1, turns):
                x = (
                    i * _blockLength
                    + _center[0]
                    + random.SystemRandom().uniform(rangeChange[0], rangeChange[1])
                )
                y = (
                    i * _blockHeight + _center[1]
                )  # + random.SystemRandom().uniform(rangeChange[0],rangeChange[1])
                A.append((x, y))

                x = (
                    -i * _blockLength + _center[0]
                )  # + random.SystemRandom().uniform(rangeChange[0],rangeChange[1])
                y = (
                    i * _blockHeight
                    + _center[1]
                    + random.SystemRandom().uniform(rangeChange[0], rangeChange[1])
                )
                A.append((x, y))

                x = (
                    -i * _blockLength
                    + _center[0]
                    + random.SystemRandom().uniform(rangeChange[0], rangeChange[1])
                )
                y = (
                    -i * _blockHeight + _center[1]
                )  # + random.SystemRandom().uniform(rangeChange[0],rangeChange[1])
                A.append((x, y))

                x = (i + 1) * _blockLength + _center[
                    0
                ]  # + random.SystemRandom().uniform(rangeChange[0],rangeChange[1])
                y = (
                    -i * _blockHeight
                    + _center[1]
                    + random.SystemRandom().uniform(rangeChange[0], rangeChange[1])
                )
                A.append((x, y))

            B = [(_item[0] - _blockLength*1.25, _item[1]) for _item in A]

            obj = unit(config, qMngr)
            obj.fillColorMode = "red"
            obj.changeColor = False
            obj.outlineColorObj = outlineColorObj
            obj.poly = (A[2], B[3], A[0], A[1])

            # This is the center square, so should be red, like the hearth it represents
            obj.minSaturation = 0.8
            obj.maxSaturation = 1.0
            obj.minValue = 0.1
            obj.maxValue = 1.0
            obj.minHue = 0
            obj.maxHue = 36

            obj.setUp(n)
            qMngr.unitArray.append(obj)

            n = 1

            for _ in range(turns):
                with contextlib.suppress(Exception):
                    # LEFT
                    # draw.polygon(poly, fill=colorutils.randomColor(config.brightness/4))
                    obj = unit(config, qMngr)
                    obj.poly = (B[n + 1], A[n + 1], A[n + 0], B[n + 0])
                    obj.changeColor = False
                    obj.outlineColorObj = outlineColorObj

                    obj.minHue = qMngr.redRange[0]
                    obj.maxHue = qMngr.redRange[1]
                    obj.minSaturation = 0.5 * qMngr.saturationRangeFactorLeft[0]
                    obj.maxSaturation = 1 * qMngr.saturationRangeFactorLeft[1]
                    obj.minValue = leftValues[0]
                    obj.maxValue = leftValues[1]

                    obj.setUp(n)
                    qMngr.unitArray.append(obj)

                    # BOTTOM
                    obj = unit(config, qMngr)
                    obj.poly = (B[n + 0], A[n - 1], B[n + 3], A[n + 4])
                    obj.changeColor = False
                    obj.outlineColorObj = outlineColorObj

                    obj.minHue = 0
                    obj.maxHue = 360
                    obj.minSaturation = 0.8 * qMngr.saturationRangeFactorLeft[0]
                    obj.maxSaturation = 1 * qMngr.saturationRangeFactorLeft[1]
                    obj.minValue = bottomValues[0]
                    obj.maxValue = bottomValues[1]

                    obj.setUp(n)
                    qMngr.unitArray.append(obj)
                    # draw.polygon(poly, fill=colorutils.randomColor())

                    # RIGHT
                    obj = unit(config, qMngr)
                    obj.poly = (B[n + 2], A[n + 2], A[n + 3], B[n + 3])
                    obj.changeColor = False
                    obj.outlineColorObj = outlineColorObj

                    obj.minHue = 0
                    obj.maxHue = 360
                    obj.minSaturation = 0.7 * qMngr.saturationRangeFactorRight[0]
                    obj.maxSaturation = 0.9 * qMngr.saturationRangeFactorRight[1]
                    obj.minValue = rightValues[0]
                    obj.maxValue = rightValues[1]

                    obj.setUp(n)
                    qMngr.unitArray.append(obj)
                    # draw.polygon(poly, fill=colorutils.randomColor(config.brightness * 1.2))

                    # TOP
                    obj = unit(config, qMngr)
                    obj.poly = (B[n + 1], A[n + 5], B[n + 6], A[n + 2])
                    obj.changeColor = False
                    obj.outlineColorObj = outlineColorObj

                    obj.minHue = qMngr.redRange[0]
                    obj.maxHue = qMngr.redRange[1]
                    obj.minSaturation = 0.7 * qMngr.saturationRangeFactorRight[0]
                    obj.maxSaturation = 0.9 * qMngr.saturationRangeFactorRight[1]
                    obj.minValue = topValues[0]
                    obj.maxValue = topValues[1]

                    obj.setUp(n)
                    qMngr.unitArray.append(obj)
                    # draw.polygon(poly, fill=colorutils.randomColor(config.brightness/1.5))
                    n += 4


def resetToAllowDistortion():
    config.rebuildingPattern = False
    # pieceLogger("restartPiece has finished its call")


def restartPiece():

    config.doSectionDisturbance = False
    config.doingSectionDisturbance = False
    config.rebuildingPattern = True

    qMngr.polyDistortionMin = -random.SystemRandom().uniform(
        1, qMngr.polyDistortion + 1
    )
    qMngr.polyDistortionMax = random.SystemRandom().uniform(
        1, qMngr.polyDistortion + 1
    )

    del qMngr.unitArray[:]

    p = math.floor(random.SystemRandom().uniform(0, len(qMngr.opticalPatterns)))

    qMngr.opticalPattern = qMngr.opticalPatterns[p]

    if random.SystemRandom().random() < qMngr.sizeFactorChangeProb:
        qMngr.sizeFactor = qMngr.extraSizeMultiplier
    else:
        qMngr.sizeFactor = qMngr.baseSizeMultiplier

    qMngr.blockLength = qMngr.blockLengthBase * qMngr.sizeFactor
    qMngr.blockHeight = qMngr.blockHeightBase * qMngr.sizeFactor

    pieceLogger(f"{qMngr.opticalPattern} {str(qMngr.sizeFactor)}")

    drawSquareSpiral()


def transformImage(img):
    width, height = img.size
    m = -0.5
    xshift = abs(m) * 420
    new_width = width + int(round(xshift))

    img = img.transform(
        (new_width, height), Image.AFFINE, (1, m, 0, 0, 1, 0), Image.BICUBIC
    )
    img = img.transform(
        (new_width, height), Image.PERSPECTIVE, qMngr.transformTuples, Image.BICUBIC
    )
    return img


def main(run=True):
    global config, directionOrder, workConfig, qMngr
    pieceLogger("quilt-informal-v2.py Loaded", 2, True)

    config.directorController = Director(config)
    config.redrawSpeed = float(workConfig.get("quilt-informal", "redrawSpeed"))
    config.directorController.slotRate = float(
        workConfig.get("quilt-informal", "slotRate")
    )

    config.brightness = float(workConfig.get("displayconfig", "brightness"))
    colorutils.brightness = config.brightness

    qMngr = QuiltManager(config)
    qMngr.setUp(workConfig)

    config.delay = float(workConfig.get("quilt-informal", "delay"))

    ### THIS IS USED AS WAY TO MOCKUP A CONFIGURATION OF RECTANGULAR PANELS
    panelDrawing.mockupBlock(config, workConfig)
    #### Need to add something like this at final render call  as well
    """ 
        ########### RENDERING AS A MOCKUP OR AS REAL ###########
        if config.useDrawingPoints  :
            config.panelDrawing.canvasToUse = config.renderImageFull
            config.panelDrawing.render()
        else :
            #config.render(config.canvasImage, 0, 0, config.canvasWidth, config.canvasHeight)
            #config.render(config.image, 0, 0)
            config.render(config.renderImageFull, 0, 0)
    """

    # createPieces()

    ########################################################################
    # CREATE THE IMAGE HOLDERS
    # canvasImage will get the drawing
    # disturbanceImage will get the disturbance / glitching
    # image will be the final output

    config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.canvasDraw = ImageDraw.Draw(config.canvasImage)
    config.disturbanceImage = Image.new(
        "RGBA", (config.canvasWidth, config.canvasHeight)
    )
    config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))

    config.doingSectionDisturbance = False
    config.rebuildingPattern = True
    distortions.distortionsConfigs(config, workConfig)

    config.blockImage = Image.new("RGBA", (config.dblockWidth, config.dblockHeight))
    config.blockDraw = ImageDraw.Draw(config.blockImage)

    drawSquareSpiral()

    ########################################################################

    if run:
        runWork()


def runWork():
    pieceLogger("RUNNING quilt-informal-v2.py", 2, True)
    while config.isRunning :
        config.directorController.checkTime()
        if config.directorController.advance :
            iterate()
        time.sleep(config.redrawSpeed)
        if not config.standAlone :
            config.callBack()


def iterate():
    global config, qMngr
    qMngr.outlineColorObj.stepTransition()

    if not config.doingSectionDisturbance :
        for i in range(len(qMngr.unitArray)):
            obj = qMngr.unitArray[i]
            if random.SystemRandom().random() > 0.98:
                obj.outlineColorObj.stepTransition()
            obj.update()
            obj.renderPolys()

    # quilt is rendered to the config.image image each cycle

    temp = Image.new("RGBA", (config.screenWidth, config.screenHeight))
    tDraw = ImageDraw.Draw(temp)
    tDraw.rectangle(
        ((0, 0), (config.screenWidth, config.screenHeight)), fill=qMngr.backgroundColor
    )

    if qMngr.transformShape :
        temp = transformImage(temp)

    if config.sectionDisturbance :
        distortions.iterationFunction(config)

    # previous non-disturbing iteration just rendered the temp image
    # config.render(temp, 0, 0)

    temp1 = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    # temp1Draw = ImageDraw.Draw(temp1)

    config.image.paste(config.canvasImage, (0, 0), config.canvasImage)
    temp1.paste(config.image, (0, 0), config.image)

    if qMngr.transformShape :
        temp1 = transformImage(temp1)

    if config.useWaveDistortion :
        temp1 = ImageOps.deform(temp1, distortions.WaveDeformer(config))
        config.waveDeformXPos += config.waveDeformXPosRate
        if config.waveDeformXPos > config.screenWidth:
            config.waveDeformXPos = 0

    config.render(
        temp1,
        config.imgcanvasOffsetX,
        config.imgcanvasOffsetY,
        config.canvasWidth,
        config.canvasHeight,
    )
    # Done

    qMngr.t2 = time.time()
    delta = qMngr.t2 - qMngr.t1

    if delta > qMngr.timeToComplete:
        if config.sectionDisturbance :
            # these functions are run to restart disturber
            distortions.resetFunction(config)

        restartPiece()
