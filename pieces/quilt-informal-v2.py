import math
import random
import textwrap
import time
import noise
from noise import *
from modules.configuration import bcolors
from modules import badpixels, coloroverlay, colorutils, panelDrawing
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFont, ImageOps

## This quilt supercedes the quilt.py module because it accounts for a zero irregularity
## as well as the infomal bar construction

from modules import distortions

"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

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

    def __init__(self, config):
        self.config = config
        self.xPos = 0
        self.yPos = 0
        self.redraw = False

        self.draw = ImageDraw.Draw(config.image)

        ## Like the "stiching" color and affects the overall "tone" of the piece
        self.outlineColor = config.outlineColorObj.currentColor
        self.objWidth = 20

        self.outlineRange = [(20, 20, 250)]
        self.brightness = 1
        self.fillColorMode = "random"
        self.lineColorMode = "red"
        self.changeColor = True
        self.lines = config.lines

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
            self.config.transitionStepsMin,
            self.config.transitionStepsMax,
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
        if random.SystemRandom().random() > config.colorPopProb:
            self.colOverlay.stepTransition()
            self.fillColor = tuple(
                int(a * self.brightness) for a in self.colOverlay.currentColor
            )
        else:
            self.changeColorFill()

    def renderPolys(self):

        if self.fillColorMode == "red":
            brightnessFactor = self.config.brightnessFactorDark
        else:
            brightnessFactor = self.config.brightnessFactorLight

        self.outlineColor = tuple(
            int(a * self.brightness * brightnessFactor)
            for a in self.outlineColorObj.currentColor
        )
        self.fillColor = tuple(
            int(a * self.brightness) for a in (self.colOverlay.currentColor)
        )

        if self.lines == True:
            self.draw.polygon(self.poly, fill=self.fillColor)
        else:
            self.draw.polygon(self.poly, fill=self.fillColor, outline=None)

    def render(self):

        if self.fillColorMode == "red":
            brightnessFactor = self.config.brightnessFactorDark
        else:
            brightnessFactor = self.config.brightnessFactorLight

        self.outlineColor = tuple(
            int(a * self.brightness * brightnessFactor)
            for a in self.outlineColorObj.currentColor
        )
        self.fillColor = tuple(
            int(a * self.brightness) for a in (self.colOverlay.currentColor)
        )

        if self.lines == True:
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

        if self.changeColor == True:
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


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

def drawSquareSpiral():

    global config

    config.t1 = time.time()
    config.t2 = time.time()

    cntrOffset = [config.cntrOffsetX, config.cntrOffsetY]

    config.unitArray = []

    ## Alignment perfect setup
    if config.patternPrecision == True:
        sizeAdjustor = 1

    n = 0
    # @todo
    # dark factor should be made into parameters
    darkValues = [0.1 * config.brightness, 0.5 * config.brightness]
    lightValues = [0.5 * config.brightness, 1.0 * config.brightness]

    opticalPattern = config.opticalPattern

    """
    LIGHTENING PATTERN
     dark right dark bottom   dark top. dark right
     dark top  dark left.   dark right. dark bottom

     repeat .....


    """

    for rows in range(0, config.blockRows):

        for cols in range(0, config.blockCols):

            if opticalPattern == "LighteningStrike":

                if cols % 2 > 0:
                    if rows % 2 > 0:
                        topValues = lightValues
                        rightValues = darkValues
                        bottomValues = darkValues
                        leftValues = lightValues
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
                        leftValues = darkValues
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
                else:
                    if rows % 2 == 0:
                        topValues = lightValues
                        rightValues = lightValues
                        bottomValues = darkValues
                        leftValues = darkValues
                    else:
                        topValues = darkValues
                        rightValues = darkValues
                        bottomValues = lightValues
                        leftValues = lightValues

            elif opticalPattern == "Diagonals":

                if cols % 2 > 0:
                    if rows % 2 > 0:
                        topValues = darkValues
                        rightValues = darkValues
                        bottomValues = lightValues
                        leftValues = lightValues
                    else:
                        topValues = lightValues
                        rightValues = lightValues
                        bottomValues = darkValues
                        leftValues = darkValues
                else:
                    if rows % 2 > 0:
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

            hDelta = config.numUnits * config.blockLength * 2 + config.hGapSize
            vDelta = config.numUnits * config.blockHeight * 2 + config.vGapSize

            cntr = [cols * hDelta + cntrOffset[0], rows * vDelta + cntrOffset[1]]
            outlineColorObj = coloroverlay.ColorOverlay()
            outlineColorObj.randomRange = (5.0, 30.0)
            outlineColorObj.colorTransitionSetup()

            n += 1

            ## Archimedean spiral is  r = a + b * theta
            turns = config.numUnits + 1
            b1 = config.blockLength
            b2 = config.blockHeight

            A = []
            B = []
            rangeChange = (config.polyDistortionMin, config.polyDistortionMax)

            for i in range(1, turns):
                x = i * b1 + cntr[0] + random.SystemRandom().uniform(rangeChange[0], rangeChange[1])
                y = i * b2 + cntr[1]  # + random.SystemRandom().uniform(rangeChange[0],rangeChange[1])
                A.append((x, y))

                x = -i * b1 + cntr[0]  # + random.SystemRandom().uniform(rangeChange[0],rangeChange[1])
                y = i * b2 + cntr[1] + random.SystemRandom().uniform(rangeChange[0], rangeChange[1])
                A.append((x, y))

                x = -i * b1 + cntr[0] + random.SystemRandom().uniform(rangeChange[0], rangeChange[1])
                y = -i * b2 + cntr[1]  # + random.SystemRandom().uniform(rangeChange[0],rangeChange[1])
                A.append((x, y))

                x = (i + 1) * b1 + cntr[
                    0
                ]  # + random.SystemRandom().uniform(rangeChange[0],rangeChange[1])
                y = -i * b2 + cntr[1] + random.SystemRandom().uniform(rangeChange[0], rangeChange[1])
                A.append((x, y))

            B = [(item[0] - b1, item[1]) for item in A]

            obj = unit(config)
            obj.fillColorMode = "red"
            obj.changeColor = False
            obj.outlineColorObj = outlineColorObj
            obj.poly = (A[2], B[3], A[0], A[1])

            # This is the center square, so should be red, like the hearth it represents
            obj.minSaturation = 0.8
            obj.maxSaturation = 1
            obj.minValue = 0.1
            obj.maxValue = 0.9
            obj.minHue = 0
            obj.maxHue = 36

            obj.setUp(n)
            config.unitArray.append(obj)

            n = 1


            for i in range(0, turns):
                try:
                    # LEFT
                    # draw.polygon(poly, fill=colorutils.randomColor(config.brightness/4))
                    obj = unit(config)
                    obj.poly = (B[n + 1], A[n + 1], A[n + 0], B[n + 0])
                    obj.changeColor = False
                    obj.outlineColorObj = outlineColorObj

                    obj.minHue = config.redRange[0]
                    obj.maxHue = config.redRange[1]
                    obj.minSaturation = 0.5 * config.saturationRangeFactorLeft[0]
                    obj.maxSaturation = 1 * config.saturationRangeFactorLeft[1]
                    obj.minValue = leftValues[0]
                    obj.maxValue = leftValues[1]

                    obj.setUp(n)
                    config.unitArray.append(obj)

                    # BOTTOM
                    obj = unit(config)
                    obj.poly = (B[n + 0], A[n - 1], B[n + 3], A[n + 4])
                    obj.changeColor = False
                    obj.outlineColorObj = outlineColorObj

                    obj.minHue = 0
                    obj.maxHue = 360
                    obj.minSaturation = 0.8 * config.saturationRangeFactorLeft[0]
                    obj.maxSaturation = 1 * config.saturationRangeFactorLeft[1]
                    obj.minValue = bottomValues[0]
                    obj.maxValue = bottomValues[1]

                    obj.setUp(n)
                    config.unitArray.append(obj)
                    # draw.polygon(poly, fill=colorutils.randomColor())

                    # RIGHT
                    obj = unit(config)
                    obj.poly = (B[n + 2], A[n + 2], A[n + 3], B[n + 3])
                    obj.changeColor = False
                    obj.outlineColorObj = outlineColorObj

                    obj.minHue = 0
                    obj.maxHue = 360
                    obj.minSaturation = 0.7 * config.saturationRangeFactorRight[0]
                    obj.maxSaturation = 0.9 * config.saturationRangeFactorRight[1]
                    obj.minValue = rightValues[0]
                    obj.maxValue = rightValues[1]

                    obj.setUp(n)
                    config.unitArray.append(obj)
                    # draw.polygon(poly, fill=colorutils.randomColor(config.brightness * 1.2))

                    # TOP
                    obj = unit(config)
                    obj.poly = (B[n + 1], A[n + 5], B[n + 6], A[n + 2])
                    obj.changeColor = False
                    obj.outlineColorObj = outlineColorObj

                    obj.minHue = config.redRange[0]
                    obj.maxHue = config.redRange[1]
                    obj.minSaturation = 0.7 * config.saturationRangeFactorRight[0]
                    obj.maxSaturation = 0.9 * config.saturationRangeFactorRight[1]
                    obj.minValue = topValues[0]
                    obj.maxValue = topValues[1]

                    obj.setUp(n)
                    config.unitArray.append(obj)
                    # draw.polygon(poly, fill=colorutils.randomColor(config.brightness/1.5))

                    n += 4
                except Exception as e:
                    # print(e)
                    pass


def restartPiece():

    config.polyDistortionMin = -random.SystemRandom().uniform(1, config.polyDistortion + 1)
    config.polyDistortionMax = random.SystemRandom().uniform(1, config.polyDistortion + 1)

    del config.unitArray[:]

    p = math.floor(random.SystemRandom().uniform(0, len(config.opticalPatterns)))

    config.opticalPattern = config.opticalPatterns[p]
 
    if random.SystemRandom().random() < config.sizeFactorChangeProb :
        config.sizeFactor = 2.0
    else :
        config.sizeFactor = 1.0
    
    config.blockLength = config.blockLengthBase * config.sizeFactor
    config.blockHeight = config.blockHeightBase * config.sizeFactor
        

    #print(config.opticalPattern)

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
        (new_width, height), Image.PERSPECTIVE, config.transformTuples, Image.BICUBIC
    )
    return img


def main(run=True):
    global config, directionOrder, workConfig
    print("---------------------")
    print("QUILT Loaded")

    config.brightness = float(workConfig.get("displayconfig", "brightness"))
    colorutils.brightness = config.brightness
    config.canvasImageWidth = config.screenWidth
    config.canvasImageHeight = config.screenHeight
    # config.canvasImageWidth -= 4
    # config.canvasImageHeight -= 4

    config.outlineColorObj = coloroverlay.ColorOverlay()
    config.outlineColorObj.randomRange = (5.0, 30.0)
    config.outlineColorObj.colorTransitionSetup()

    config.transitionStepsMin = float(workConfig.get("quilt-informal", "transitionStepsMin"))
    config.transitionStepsMax = float(workConfig.get("quilt-informal", "transitionStepsMax"))

    config.transformShape = workConfig.getboolean("quilt-informal", "transformShape")
    transformTuples = workConfig.get("quilt-informal", "transformTuples").split(",")
    config.transformTuples = tuple([float(i) for i in transformTuples])

    redRange = workConfig.get("quilt-informal", "redRange").split(",")
    config.redRange = tuple([int(i) for i in redRange])

    try:
        saturationRangeFactorLeft = workConfig.get("quilt-informal", "saturationRangeFactorLeft").split(",")
        config.saturationRangeFactorLeft = tuple([float(i) for i in saturationRangeFactorLeft])

        saturationRangeFactorRight = workConfig.get("quilt-informal", "saturationRangeFactorRight").split(",")
        config.saturationRangeFactorRight = tuple([float(i) for i in saturationRangeFactorRight])
    
    except Exception as e:
        print(str(e))
        config.saturationRangeFactorLeft = (1,1)
        config.saturationRangeFactorRight = (1,1)

    backgroundColor = workConfig.get("quilt-informal", "backgroundColor").split(",")
    config.backgroundColor = tuple([int(i) for i in backgroundColor])

    config.numUnits = int(workConfig.get("quilt-informal", "numUnits"))
    config.hGapSize = int(workConfig.get("quilt-informal", "hGapSize"))
    config.vGapSize = int(workConfig.get("quilt-informal", "vGapSize"))
    config.blockSize = int(workConfig.get("quilt-informal", "blockSize"))
    config.blockLength = float(workConfig.get("quilt-informal", "blockLength"))
    config.blockHeight = float(workConfig.get("quilt-informal", "blockHeight"))
    config.blockLengthBase = float(workConfig.get("quilt-informal", "blockLength"))
    config.blockHeightBase = float(workConfig.get("quilt-informal", "blockHeight"))
    config.blockRows = int(workConfig.get("quilt-informal", "blockRows"))
    config.blockCols = int(workConfig.get("quilt-informal", "blockCols"))
    config.cntrOffsetX = int(workConfig.get("quilt-informal", "cntrOffsetX"))
    config.cntrOffsetY = int(workConfig.get("quilt-informal", "cntrOffsetY"))
    config.delay = float(workConfig.get("quilt-informal", "delay"))
    config.colorPopProb = float(workConfig.get("quilt-informal", "colorPopProb"))
    config.brightnessFactorDark = float(workConfig.get("quilt-informal", "brightnessFactorDark"))
    config.brightnessFactorLight = float(
        workConfig.get("quilt-informal", "brightnessFactorLight")
    )
    config.lines = workConfig.getboolean("quilt-informal", "lines")
    config.patternPrecision = workConfig.getboolean("quilt-informal", "patternPrecision")

    config.polyDistortion = float(workConfig.get("quilt-informal", "polyDistortion"))
    config.polyDistortionMin = -config.polyDistortion
    config.polyDistortionMax = config.polyDistortion

    # stacking the decks a bit in favor of vertical lightening strike and regular
    try:
        config.opticalPatterns = workConfig.get("quilt-informal","opticalPatterns").split(",")
    except Exception as e:
        print(str(e))
        config.opticalPatterns = ["Regular" , "Regular", "LighteningStrikeH", "LighteningStrikeH", "Diagonals", "LighteningStrikeH"]
    
    # Chance that when the Quilt rebuilds the pattern doubles in size 
    try:
        config.sizeFactorChangeProb = float(workConfig.get("quilt-informal","sizeFactorChangeProb"))
    except Exception as e:
        print(str(e))
        config.sizeFactorChangeProb = 0.0
    # "LighteningStrikeH"  aka Charlie Brown sweater ...

    # for now, all squares
    # config.blockLength = config.blockSize
    # config.blockHeight = config.blockSize

    p = math.floor(random.SystemRandom().uniform(0, len(config.opticalPatterns)))
    config.opticalPattern = config.opticalPatterns[p]


    config.timeToComplete = int(workConfig.get("quilt-informal", "timeToComplete"))
    # config.timeToComplete = 60 #round(random.SystemRandom().uniform(30,220))

    ### THIS IS USED AS WAY TO MOCKUP A CONFIGURATION OF RECTANGULAR PANELS
    panelDrawing.mockupBlock(config, workConfig)
    #### Need to add something like this at final render call  as well
    ''' 
        ########### RENDERING AS A MOCKUP OR AS REAL ###########
        if config.useDrawingPoints == True :
            config.panelDrawing.canvasToUse = config.renderImageFull
            config.panelDrawing.render()
        else :
            #config.render(config.canvasImage, 0, 0, config.canvasWidth, config.canvasHeight)
            #config.render(config.image, 0, 0)
            config.render(config.renderImageFull, 0, 0)
    '''

    # createPieces()
    
    ########################################################################
    # CREATE THE IMAGE HOLDERS
    # canvasImage will get the drawing
    # disturbanceImage will get the disturbance / glitching
    # image will be the final output

    config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.canvasDraw = ImageDraw.Draw(config.canvasImage)
    config.disturbanceImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    
    distortions.additonalSetup(config, workConfig)
    
    config.blockImage = Image.new("RGBA", (config.dblockWidth, config.dblockHeight))
    config.blockDraw = ImageDraw.Draw(config.blockImage)
    
    drawSquareSpiral()

    ########################################################################

    if run:
        runWork()

        
def runWork():
    global config
    print(bcolors.OKGREEN + "** " + bcolors.BOLD)
    print("RUNNING quilt-informal.py")
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
    config.outlineColorObj.stepTransition()

    for i in range(0, len(config.unitArray)):
        obj = config.unitArray[i]
        if random.SystemRandom().random() > 0.98:
            obj.outlineColorObj.stepTransition()
        obj.update()
        obj.renderPolys()
        
    # quilt is rendered to the config.image image each cycle
    
    temp = Image.new("RGBA", (config.screenWidth, config.screenHeight))
    tDraw = ImageDraw.Draw(temp)
    tDraw.rectangle(((0, 0), (config.screenWidth, config.screenHeight)), fill=config.backgroundColor)

    if config.transformShape == True:
        temp = transformImage(temp)
        
    if config.sectionDisturbance == True :
        distortions.iterationFunction(config)
        
    # previous non-disturbing iteration just rendered the temp image
    # config.render(temp, 0, 0)
    
    temp1 = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    temp1Draw = ImageDraw.Draw(temp1)

    config.image.paste(config.canvasImage, (0, 0), config.canvasImage)
    temp1.paste(config.image, (0, 0), config.image)
    
    if config.transformShape == True :
        temp1 = transformImage(temp1)
    
    
    if config.useWaveDistortion == True:
        temp1 = ImageOps.deform(temp1, distortions.WaveDeformer(config))
        config.waveDeformXPos += config.waveDeformXPosRate
        if config.waveDeformXPos > config.screenWidth :
            config.waveDeformXPos = 0
    
    config.render(temp1, config.imgcanvasOffsetX, config.imgcanvasOffsetY, config.canvasWidth, config.canvasHeight)
    # Done

    config.t2 = time.time()
    delta = config.t2 - config.t1

    if delta > config.timeToComplete:
        if config.sectionDisturbance == True :
            # these functions are run to restart disturber
            distortions.resetFunction(config)

        restartPiece()
