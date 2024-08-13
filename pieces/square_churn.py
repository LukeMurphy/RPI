import math
import random
import textwrap
import time
from modules.configuration import bcolors
from modules import badpixels, coloroverlay, colorutils, panelDrawing
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFont, ImageOps

## This quilt supercedes the quilt.py module because it accounts for a zero irregularity
## as well as the infomal bar construction

class SkewedSquareUnit :
    units = []
    speed = 0
    
    rateA = 0
    rateB = 0
    rateC = 0
    rateD = 0

    def __init__(self, config):
        self.config = config
    

class Unit:

    timeTrigger = True
    tLimitBase = 30

    maxBrightness = 1

    minSaturation = 1
    maxSaturation = 1

    minValue = 1
    maxValue = 1

    minHue = 0
    maxHue = 360
    
    varR = 100
    
    redrawBaseImageEachCycle = True

    def __init__(self, config):
        self.config = config
        self.xPos = 0
        self.yPos = 0
        self.redraw = False
  
        self.canvas = Image.new('RGBA', (400,400))
        self.draw = ImageDraw.Draw(self.canvas)

        ## Like the "stiching" color and affects the overall "tone" of the piece
        self.outlineColor = config.outlineColorObj.currentColor
        self.objWidth = 20

        self.outlineRange = [(20, 20, 250)]
        self.brightness = 1
        self.fillColorMode = "random"
        self.lineColorMode = "red"
        self.changeColor = True


    def setUp(self, n=0):

        self.outlineColor = tuple(
            int(a * self.brightness) for a in (self.outlineColorObj.currentColor)
        )

        #### Sets up color transitions
        self.colOverlay = coloroverlay.ColorOverlay()
        self.colOverlay.randomSteps = True
        self.colOverlay.timeTrigger = True
        self.colOverlay.tLimitBase = 5
        self.colOverlay.steps = 10

        self.colOverlay.maxBrightness = self.config.brightness
        self.colOverlay.maxBrightness = self.maxBrightness

        self.colOverlay.minSaturation = self.minSaturation
        self.colOverlay.maxSaturation = self.maxSaturation

        self.colOverlay.minValue = self.minValue
        self.colOverlay.maxValue = self.maxValue

        self.colOverlay.minHue = self.minHue
        self.colOverlay.maxHue = self.maxHue
        
        self.colOverlay.dropHueMin = self.dropHueMin
        self.colOverlay.dropHueMax = self.dropHueMax

        ### This is the speed range of transitions in color
        ### Higher numbers means more possible steps so slower
        ### transitions - 1,10 very blinky, 10,200 very slow
        self.colOverlay.randomRange = (
            self.config.transitionStepsMin,
            self.config.transitionStepsMax,
        )

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
        if random.random() > config.colorPopProb:
            self.colOverlay.stepTransition()
            self.fillColor = tuple(
                int(a * self.brightness) for a in self.colOverlay.currentColor
            )
        else:
            self.changeColorFill()

    
    def makePoly(self) :
        # varR = radius - i * radius/numberOfRings
        parent = self.parent

        A = (parent.centerPoint[0] + round(self.varR * math.cos(parent.angleA)),parent.centerPoint[1] + round(self.varR * math.sin(parent.angleA)))
        B = (parent.centerPoint[0] + round(self.varR * math.cos(parent.angleB)),parent.centerPoint[1] + round(self.varR * math.sin(parent.angleB)))
        C = (parent.centerPoint[0] + round(self.varR * math.cos(parent.angleC)),parent.centerPoint[1] + round(self.varR * math.sin(parent.angleC)))
        D = (parent.centerPoint[0] + round(self.varR * math.cos(parent.angleD)),parent.centerPoint[1] + round(self.varR * math.sin(parent.angleD)))
        E = (parent.centerPoint[0] + round(self.varR * math.cos(parent.angleA)),parent.centerPoint[1] + round(self.varR * math.sin(parent.angleA)))
        # print(A,B,C,D)

        self.poly = (A,B,C,D,E)

   
    def renderPolys(self):
        
        if self.redrawBaseImageEachCycle == True :
            self.canvas = Image.new('RGBA', (400,400))
            self.draw = ImageDraw.Draw(self.canvas)


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
                    random.uniform(0.01, self.brightness)
                )
                self.outlineColor = colorutils.getRandomRGB(
                    random.uniform(0.01, self.brightness)
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

    config.outlineColorObj = coloroverlay.ColorOverlay()
    config.outlineColorObj.randomRange = (5.0, 30.0)
    config.outlineColorObj.colorTransitionSetup()

    config.transitionStepsMin = float(workConfig.get("squarerings", "transitionStepsMin"))
    config.transitionStepsMax = float(workConfig.get("squarerings", "transitionStepsMax"))

    config.transformShape = workConfig.getboolean("squarerings", "transformShape")
    transformTuples = workConfig.get("squarerings", "transformTuples").split(",")
    config.transformTuples = tuple([float(i) for i in transformTuples])

    redRange = workConfig.get("squarerings", "redRange").split(",")
    config.redRange = tuple([int(i) for i in redRange])
    

    try:
        saturationRangeFactorLeft = workConfig.get("squarerings", "saturationRangeFactorLeft").split(",")
        config.saturationRangeFactorLeft = tuple([float(i) for i in saturationRangeFactorLeft])

        saturationRangeFactorRight = workConfig.get("squarerings", "saturationRangeFactorRight").split(",")
        config.saturationRangeFactorRight = tuple([float(i) for i in saturationRangeFactorRight])
    
    except Exception as e:
        print(str(e))
        config.saturationRangeFactorLeft = (1,1)
        config.saturationRangeFactorRight = (1,1)

    backgroundColor = workConfig.get("squarerings", "backgroundColor").split(",")
    config.backgroundColor = tuple([int(i) for i in backgroundColor])
    
    config.minHue = float(workConfig.get("squarerings", "minHue"))
    config.maxHue = float(workConfig.get("squarerings", "maxHue"))
    config.minSaturation = float(workConfig.get("squarerings", "minSaturation"))
    config.maxSaturation = float(workConfig.get("squarerings", "maxSaturation"))
    config.minValue = float(workConfig.get("squarerings", "minValue"))
    config.maxValue = float(workConfig.get("squarerings", "maxValue"))
    config.dropHueMin = float(workConfig.get("squarerings", "dropHueMin"))
    config.dropHueMax = float(workConfig.get("squarerings", "dropHueMax"))
    config.alt_minHue = float(workConfig.get("squarerings", "alt_minHue"))
    config.alt_maxHue = float(workConfig.get("squarerings", "alt_maxHue"))
    config.alt_minSaturation = float(workConfig.get("squarerings", "alt_minSaturation"))
    config.alt_maxSaturation = float(workConfig.get("squarerings", "alt_maxSaturation"))
    config.alt_minValue = float(workConfig.get("squarerings", "alt_minValue"))
    config.alt_maxValue = float(workConfig.get("squarerings", "alt_maxValue"))
    config.alt_dropHueMin = float(workConfig.get("squarerings", "alt_dropHueMin"))
    config.alt_dropHueMax = float(workConfig.get("squarerings", "alt_dropHueMax"))

    config.numUnits = int(workConfig.get("squarerings", "numUnits"))
    config.minRadius = int(workConfig.get("squarerings", "minRadius"))
    config.maxRadius = int(workConfig.get("squarerings", "maxRadius"))
    config.minNumberOfRings = int(workConfig.get("squarerings", "minNumberOfRings"))
    config.maxNumberOfRings = int(workConfig.get("squarerings", "maxNumberOfRings"))
    config.movementRate = float(workConfig.get("squarerings", "movementRate"))
    
    config.redrawBaseImageEachCycle = (workConfig.getboolean("squarerings", "redrawBaseImageEachCycle"))
    config.probredrawBaseImageEachCycle = float(workConfig.get("squarerings", "probredrawBaseImageEachCycle"))

    config.cntrOffsetX = int(workConfig.get("squarerings", "cntrOffsetX"))
    config.cntrOffsetY = int(workConfig.get("squarerings", "cntrOffsetY"))
    config.delay = float(workConfig.get("squarerings", "delay"))
    config.colorPopProb = float(workConfig.get("squarerings", "colorPopProb"))
    config.brightnessFactorDark = float(workConfig.get("squarerings", "brightnessFactorDark"))
    config.brightnessFactorLight = float(workConfig.get("squarerings", "brightnessFactorLight"))

    config.polyDistortion = float(workConfig.get("squarerings", "polyDistortion"))
    config.polyDistortionMin = -config.polyDistortion
    config.polyDistortionMax = config.polyDistortion

    config.polyDistortionChangeRateMin = float(workConfig.get("squarerings", "polyDistortionChangeRateMin"))
    config.polyDistortionChangeRateMax = float(workConfig.get("squarerings", "polyDistortionChangeRateMax"))

    config.canvasImage = Image.new(
        "RGBA", (config.canvasImageWidth, config.canvasImageHeight)
    )
    config.timeToComplete = int(workConfig.get("squarerings", "timeToComplete"))
    # config.timeToComplete = 60 #round(random.uniform(30,220))

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
    drawSqareSpiral()

    if run:
        runWork()


def restartPiece():
    del config.unitArray[:]
    del config.squaresArray[:]
    if random.random() < config.probredrawBaseImageEachCycle :
        if random.random() < .5 :
            config.redrawBaseImageEachCycle = False
        else:
            config.redrawBaseImageEachCycle = True
    drawSqareSpiral()


def drawSqareSpiral():

    global config

    config.t1 = time.time()
    config.t2 = time.time()

    cntrOffset = [config.cntrOffsetX, config.cntrOffsetY]

    config.squaresArray = []
    config.unitArray = []
    
    for n in range (0,config.numUnits) :
        
        skewedSquare = SkewedSquareUnit(config)    
        config.squaresArray.append(skewedSquare)
        skewedSquare.unitArray = []
        skewedSquare.speed = random.uniform(-config.movementRate,config.movementRate)

        skewedSquare.radius = random.uniform(config.minRadius,config.maxRadius)
        skewedSquare.numberOfRings = round(random.uniform(config.minNumberOfRings,config.maxNumberOfRings))

        skewedSquare.angleA = 0 + random.uniform(-math.pi * config.polyDistortion, math.pi*config.polyDistortion)
        skewedSquare.angleB = math.pi / 2 + random.uniform(-math.pi*config.polyDistortion, math.pi*config.polyDistortion)
        skewedSquare.angleC = math.pi / 1 + random.uniform(-math.pi*config.polyDistortion, math.pi*config.polyDistortion)
        skewedSquare.angleD = 3 * math.pi / 2 + random.uniform(-math.pi*config.polyDistortion, math.pi*config.polyDistortion)
        
        skewedSquare.centerPoint = (round(random.uniform(0,config.canvasWidth)),round(random.uniform(0,config.canvasHeight)))
        skewedSquare.xPos = 0
        skewedSquare.yPos = 0
        
        rangeA = config.polyDistortionChangeRateMin
        rangeB = config.polyDistortionChangeRateMax
        
        if random.random() < .3 :
        
            skewedSquare.rateA = math.pi * (random.uniform(rangeA,rangeB))
            if random.random()> .85 : skewedSquare.rateA *= -1
            skewedSquare.rateB = math.pi * (random.uniform(rangeA,rangeB))
            if random.random()> .85 : skewedSquare.rateB *= -1
            skewedSquare.rateC = math.pi * (random.uniform(rangeA,rangeB))
            if random.random()> .85 : skewedSquare.rateC *= -1
            skewedSquare.rateD = math.pi * (random.uniform(rangeA,rangeB))
            if random.random()> .85 : skewedSquare.rateD *= -1
        
        for i in range(1,skewedSquare.numberOfRings) :
            
            outlineColorObj = coloroverlay.ColorOverlay()
            outlineColorObj.randomRange = (5.0, 30.0)
            outlineColorObj.colorTransitionSetup()
            obj = Unit(config)
            obj.fillColorMode = "red"
            obj.changeColor = False
            obj.outlineColorObj = outlineColorObj


            # This is the center square, so should be red, like the hearth it represents
            obj.minHue = config.minHue
            obj.maxHue = config.maxHue
            obj.minSaturation = config.minSaturation
            obj.maxSaturation = config.maxSaturation
            obj.minValue = config.minValue
            obj.maxValue = config.maxValue
            obj.dropHueMin = config.dropHueMin
            obj.dropHueMax = config.dropHueMax
            
            
            if i % 2 == 0 :
                obj.minHue = config.alt_minHue
                obj.maxHue = config.alt_maxHue
                obj.minSaturation = config.alt_minSaturation
                obj.maxSaturation = config.alt_maxSaturation
                obj.minValue = config.alt_minValue
                obj.maxValue = config.alt_maxValue
                obj.dropHueMin = config.alt_dropHueMin
                obj.dropHueMax = config.alt_dropHueMax

                
            obj.varR = skewedSquare.radius - i * skewedSquare.radius/skewedSquare.numberOfRings
            obj.parent = skewedSquare
            obj.redrawBaseImageEachCycle = config.redrawBaseImageEachCycle
            
            obj.makePoly()
            obj.setUp()
            config.unitArray.append(obj)
            skewedSquare.unitArray.append(obj)
    

def runWork():
    global config
    print(bcolors.OKGREEN + "** " + bcolors.BOLD)
    print("RUNNING squarerings-informal.py")
    print(bcolors.ENDC)
    while config.isRunning == True:
        iterate()
        time.sleep(config.delay)
        if config.standAlone == False :
            config.callBack()


def iterate():
    global config
    config.outlineColorObj.stepTransition()

    for u in range(0, len(config.squaresArray)):
        parentRef  = config.squaresArray[u]
        parentRef.angleA += parentRef.rateA
        parentRef.angleB += parentRef.rateB
        parentRef.angleC += parentRef.rateC
        parentRef.angleD += parentRef.rateD
        for i in range(0, len(parentRef.unitArray)):
            obj = parentRef.unitArray[i]
            if random.random() > 0.98:
                obj.outlineColorObj.stepTransition()
            
            obj.update()
            obj.makePoly()
            obj.renderPolys()
            objTmp = (obj.canvas)
            config.canvasImage.paste(objTmp,(round(parentRef.xPos),round(parentRef.yPos)), objTmp)
            
        parentRef.xPos += parentRef.speed  
        if parentRef.xPos < 0 :
            parentRef.xPos = config.canvasWidth
        if parentRef.xPos > config.canvasWidth :
            parentRef.xPos = 0
            
        
    temp = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    tDraw = ImageDraw.Draw(temp)
    
    tDraw.rectangle(
        ((0, 0), (config.screenWidth, config.screenHeight)), fill=config.backgroundColor
    )
    temp.paste(config.canvasImage, (0, 0), config.canvasImage)
    
    if config.transformShape == True:
        temp = transformImage(temp)

    # print("squareringss ",config.render, config.instanceNumber)

    ########### RENDERING AS A MOCKUP OR AS REAL ###########
    if config.useDrawingPoints == True :
        config.panelDrawing.canvasToUse = temp
        config.panelDrawing.render()
    else :
        config.render(temp, 0, 0)


    config.t2 = time.time()
    delta = config.t2 - config.t1

    if delta > config.timeToComplete:
        restartPiece()
