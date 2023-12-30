import random
import time
import math
from collections import OrderedDict
from modules.configuration import bcolors
import numpy
from modules import coloroverlay, colorutils
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFont, ImageOps

global thrd, config

"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

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

"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


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



"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""



"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

class DrawingUnit:
    def __init__(self, config):
        self.config = config
        self.units = []
        self.unitFills = []


def renderCompositions():
    temp = Image.new("RGBA", (config.imageWidth, config.imageHeight))
    drawtemp = ImageDraw.Draw(temp)
    
    for i in range(0, len(config.drawingUnit.units)) :
        # drawtemp.rectangle(config.drawingUnit.units[i], fill=config.drawingUnit.unitFills[i])
        drawtemp.polygon(config.drawingUnit.units[i], fill=config.drawingUnit.unitFills[i])
        
    config.imageLayer.paste(temp, temp)
        

def drawCompositions():

    config.drawingUnit = DrawingUnit(config)

    startx = config.imageWidth / 9
    wVariance = [config.imageWidth / 3, config.imageWidth / 2]
    hVariance = [config.imageHeight / 2, config.imageHeight / 1]
    wFactor = 1
    hFactor = 2
    starty = 0

    # Choose seam x point  -- ideally about 1/3 from left
    # the 100 px spread around the 1/3 width should really be proportional to the overall size
    # xVariance = round(random.uniform(config.canvasWidth - 50, config.canvasWidth + 50) / 3) 
    xVarianceSpread = round(config.canvasWidth/6)
    xVariance = round(random.uniform(config.imageWidth - xVarianceSpread, config.imageWidth + xVarianceSpread) / 3) 
    config.flip = False

    xSeam = int(
        random.uniform(
            config.imageWidth * 2 / 3 - xVariance, config.imageWidth * 2 / 3 + xVariance
        )
    )
    
    config.pixSortXOffset = xSeam
    tiedToBottom = 0 if random.random() < 0.5 else 2

    angleRotation = random.uniform(-3, 3)
    
    # config.imageLayer.paste(temp, temp)
    fills = []
    fills.append([0])
    
    
    c = config.colorSets[config.colorSetInUse]
    for n in range(0, config.numSquarePairs):
    
        fills = colorutils.getRandomColorHSV(
                                    c.minHue,
                                    c.maxHue,
                                    c.minSaturation,
                                    c.maxSaturation,
                                    c.minValue,
                                    c.maxValue,
                                    c.dropHueMin,
                                    c.dropHueMax,
                                    c.transparency
                                    )
            
        if n == 2:
            wFactor *= 1.5

        if n == 0:
            x1 = round(xSeam)
            x2 = round(random.uniform(x1 + startx, x1 + wVariance[1]))
            y1 = round(random.uniform(hVariance[0], hVariance[1]))
            y2 = round(
                random.uniform(y1 + hVariance[0] * hFactor, y1 + hVariance[1] * hFactor)
            )
            if n == tiedToBottom:
                y2 = config.imageHeight
            starty = round(random.uniform(0, config.imageHeight / 2))

        else:
            x1 = round(
                random.uniform(xSeam - startx * wFactor, xSeam - wVariance[1] * wFactor)
            )
            x2 = round(xSeam)
            y1 = starty
            y2 = round(random.uniform(y1 + hVariance[0], y1 + hVariance[1]))
            if n == tiedToBottom:
                y2 = config.imageHeight
            starty = y2


        rectHeight = y2 - y1

        # temp = Image.new("RGBA", (config.imageWidth, config.imageHeight))
        # drawtemp = ImageDraw.Draw(temp)
        if y2<y1 :
            y2=y1+5
        if x2<x1 :
            x2=x1+5
        # drawtemp.rectangle((x1, y1, x2, y2), fill=fills[n])
        
        # config.drawingUnit.units.append((x1, y1, x2, y2))
        # converted to drawing polygons to add more quandrange variations
        
        poly = []
        xVar  = round(random.uniform(-10,20))
        yVar  = round(random.uniform(-10,20))
        poly.append((x1, y1))
        poly.append((x2 + xVar, y1 + yVar))
        poly.append((x2 + 0, y2 + yVar))
        poly.append((x1, y2))

        config.drawingUnit.units.append(poly)

        
        
        config.drawingUnit.unitFills.append(fills)
  

    if config.flip == True:
        config.imageLayer = config.imageLayer.transpose(Image.FLIP_TOP_BOTTOM)
        config.imageLayer = config.imageLayer.transpose(Image.ROTATE_180)


def initCompositions():
    config.canvasImageWidth = int(workConfig.get("compositions", "canvasImageWidth"))
    config.canvasImageHeight = int(workConfig.get("compositions", "canvasImageHeight"))
    config.refreshCount = int(workConfig.get("compositions", "refreshCount"))
    config.timeToComplete = float(workConfig.get("compositions", "timeToComplete"))
    config.cleanSlateProbability = float(workConfig.get("compositions", "cleanSlateProbability"))
    config.filterPatchProb = float(workConfig.get("compositions", "filterPatchProb"))

    config.imageWidth = config.canvasImageWidth
    config.imageHeight = config.canvasImageHeight

    config.numSquarePairs = int(workConfig.get("compositions", "numSquarePairs"))
 
    config.t1 = time.time()
    config.t2 = time.time()

    # initial crossfade settings
    config.doingRefresh = config.refreshCount
    config.doingRefreshCount = config.refreshCount

    # config.canvasImage = Image.new("RGBA", (config.canvasImageWidth, config.canvasImageHeight))
    # config.draw = ImageDraw.Draw(config.canvasImage)
    # config.draw.rectangle((0, 0, config.imageWidth, config.imageHeight), fill=config.bgColor)

    config.firstRun = True
    config.flip = False
    
    print("Running")
    drawCompositions()
 

def restartDrawing():

    config.flip = True if random.random() < 0.5 else False
    if random.random() < config.cleanSlateProbability or config.firstRun == True:
        # grayLevel = round(random.uniform(20,70))
        # config.bgColor = (grayLevel,grayLevel,grayLevel)
        c = config.colorSets[config.colorSetInUse]
        
        config.bgColor = colorutils.getRandomColorHSVSaturated(
            c.bg_minHue,
            c.bg_maxHue,
            c.bg_minSaturation,
            c.bg_maxSaturation,
            c.bg_minValue,
            c.bg_maxValue,
            c.bg_dropHueMin,
            c.bg_dropHueMax
        )
        # print(config.bgColor)
        # config.bgColor = colorutils.getRandomColorHSV(0,360, .3,.95, .1,.94)
        config.draw.rectangle(
            (0, 0, config.imageWidth, config.imageHeight), fill=config.bgColor
        )
        
        config.firstRun = False
    drawCompositions()

    config.t1 = time.time()
    config.t2 = time.time()
    # initialize crossfade - in this case 100 steps ...
    config.doingRefresh = 0
    config.doingRefreshCount = config.refreshCount



"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""




"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def initShapes() :
   
    config.useTweenTriggers = False    
    config.transitionStepsMin = int(workConfig.get("collageShapes", "transitionStepsMin"))
    config.transitionStepsMax = int(workConfig.get("collageShapes", "transitionStepsMax"))
    config.changeBoxProb = float(workConfig.get("collageShapes", "changeBoxProb"))
    config.colOverlaytLimitBase = int(workConfig.get("collageShapes", "colOverlaytLimitBase"))
    config.colOverlaySteps = int(workConfig.get("collageShapes", "colOverlaySteps"))        
    config.shapeSets = list(map(lambda x: x, workConfig.get("collageShapes", "sets").split(",")))

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

            # shape.callBackDone = types.MethodType(callBackDone, shape)
            shape.reDraw()
            shapeGroupList.append(shape)

        config.shapeGroups.append(shapeGroupList)

    # Always start with the first one, index 0
    config.shapeGroupDisplayed = 0

"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

class ColorSet :
    def __init__(self):
        self.name = "cset"

        
        
def init():
    
    global config, workConfig
    config.redrawSpeed = float(workConfig.get("compositions", "redrawSpeed"))
    config.redrawProbablility = float(workConfig.get("compositions", "redrawProbablility"))
    config.xVariance = float(workConfig.get("compositions", "xVariance"))
    config.xOffset = int(workConfig.get("compositions", "xOffset"))
    config.yOffset = int(workConfig.get("compositions", "yOffset"))
    config.fade = int(workConfig.get("compositions", "fade"))

    config.useColorOverlayTransitions = workConfig.getboolean("compositions", "useColorOverlayTransitions")
    config.applyColorOverlayToFullImage = workConfig.getboolean("compositions", "applyColorOverlayToFullImage")
    config.useScrollingBackGround = workConfig.getboolean("compositions", "useScrollingBackGround")
    config.patternRows = int(workConfig.get("compositions", "patternRows"))
    config.patternCols = int(workConfig.get("compositions", "patternCols"))
    config.patternRowsOffset = int(workConfig.get("compositions", "patternRowsOffset"))
    config.patternColsOffset = int(workConfig.get("compositions", "patternColsOffset"))
    config.bgYStepSpeed = int(workConfig.get("compositions", "bgYStepSpeed"))
    config.bgXStepSpeed = int(workConfig.get("compositions", "bgXStepSpeed"))

    config.pixSortXOffsetVal = config.pixSortXOffset
    config.colorTransitionRangeMin = float(workConfig.get("compositions", "colorTransitionRangeMin"))
    config.colorTransitionRangeMax = float(workConfig.get("compositions", "colorTransitionRangeMax"))
    config.angleRotationRange = float(workConfig.get("compositions", "angleRotationRange"))

    ### """""" """""" """""" """""" """""" """""" """""" """""" ""
    ### """""" """""" """""" """""" """""" """""" """""" """""" ""
    ### """""" """""" """""" """""" """""" """""" """""" """""" ""
    ### Piece is made up of three layers
    ### the background layer or moving pattern is drawn to the the     bgImage layer
    ### this is placed first into the workImage
    ### then the imageLayer is created with the figure drawn on it and then pasted
    ### onto the workImage to make the the final composited image and that is rendered
    ###

    config.imageLayer = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.imageLayerDraw = ImageDraw.Draw(config.imageLayer)

    config.bgImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.bgDraw = ImageDraw.Draw(config.bgImage)

    config.workImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.workImageDraw = ImageDraw.Draw(config.workImage)

    config.clrBlock = Image.new(config.workImage.mode, (config.canvasWidth, config.canvasHeight) )
    config.clrBlockDraw = ImageDraw.Draw(config.clrBlock)
    
    config.destinationImage = config.imageLayer

    ## Set up the scrolling background images
    ## patternDrawProb creates the gaps in the pattern
    ## the pattern is redrawn every time one of the two panels moves off screen
    config.patternDrawProb = float(workConfig.get("compositions", "patternDrawProb"))

    config.bgBackGroundColor = workConfig.get("compositions", "bgBackGroundColor").split(",")
    config.bgBackGroundColor = tuple([int(i) for i in config.bgBackGroundColor])

    config.bgForeGroundColor = workConfig.get("compositions", "bgForeGroundColor").split(",")
    config.bgForeGroundColor = tuple([int(i) for i in config.bgForeGroundColor])

    config.bg1 = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.bg1Draw = ImageDraw.Draw(config.bg1)
    config.bg1Draw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=config.bgBackGroundColor)
    makeBackGround(config.bg1Draw, 1)

    config.bg2 = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.bg2Draw = ImageDraw.Draw(config.bg2)
    config.bg2Draw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=config.bgBackGroundColor)
    makeBackGround(config.bg2Draw, 2)

    config.leadBG = config.bg1
    config.followBG = config.bg2
    config.leadBGDraw = config.bg1Draw
    config.followBGDraw = config.bg2Draw

    config.bgImage.paste(config.bg1)
    config.bgImage.paste(config.bg2, (0, config.canvasHeight))
    config.bgXpos = 0
    config.bgYpos = 0

    ### the overlay color affects the background only in this case
    
    config.colorSets = []
    colorSets = list(map(lambda x: x, workConfig.get("compositions", "colorSetsToUse").split(",")))

    for n in range(0, len(colorSets)):

        colorSetGroup = colorSets[n]        
        c = ColorSet()
        
        colorValsInsets = list(map(lambda x: x, workConfig.get(colorSetGroup, "insets").split(",")))
        colorValsBG = list(map(lambda x: x, workConfig.get(colorSetGroup, "bg").split(",")))

        # for i in range(0, len(colorValsInsets)):
        c.minHue = float(colorValsInsets[0])
        c.maxHue = float(colorValsInsets[1])
        c.minSaturation = float(colorValsInsets[2])
        c.maxSaturation = float(colorValsInsets[3])
        c.minValue = float(colorValsInsets[4])
        c.maxValue = float(colorValsInsets[5])
        c.dropHueMin = float(colorValsInsets[6])
        c.dropHueMax = float(colorValsInsets[7])
        c.transparency = 255
            
        # for i in range(0, len(colorValsBG)):
        c.bg_minHue = float(colorValsBG[0])
        c.bg_maxHue = float(colorValsBG[1])
        c.bg_minSaturation = float(colorValsBG[2])
        c.bg_maxSaturation = float(colorValsBG[3])
        c.bg_minValue = float(colorValsBG[4])
        c.bg_maxValue = float(colorValsBG[5])
        c.bg_dropHueMin = float(colorValsBG[6])
        c.bg_dropHueMax = float(colorValsBG[7])
        c.bgColorTransparency = 255
            
        config.colorSets.append(c)
        
    
    config.colOverlayA = coloroverlay.ColorOverlay()
    ### This is the speed range of transitions in color
    ### Higher numbers means more possible steps so slower
    ### transitions - 1,10 very blinky, 10,200 very slow
    config.colOverlayA.randomRange = (config.colorTransitionRangeMin,config.colorTransitionRangeMax,)
    config.colOverlayA.colorA = tuple(int(a * config.brightness) for a in (colorutils.getRandomColor()))
    
    config.colorSetInUse = 0
    
    c = config.colorSets[config.colorSetInUse]
    
    config.colOverlayA.minHue = c.bg_minHue
    config.colOverlayA.maxHue = c.bg_maxHue
    config.colOverlayA.minSaturation = c.bg_minSaturation
    config.colOverlayA.maxSaturation = c.bg_maxSaturation
    config.colOverlayA.minValue = c.bg_minValue
    config.colOverlayA.maxValue = c.bg_maxValue
    config.colOverlayA.dropHueMin = c.bg_dropHueMin
    config.colOverlayA.dropHueMax = c.bg_dropHueMax

    config.colOverlayA.randomSteps = True
    config.colOverlayA.timeTrigger = True
    config.colOverlayA.steps = 100
    config.colOverlayA.tLimitBase = 30
    config.colOverlayA.maxBrightness = config.brightness
    config.colOverlayA.colorTransitionSetup()
    
    try:
        config.filterPatchProb = float(workConfig.get("compositions", "filterPatchProb"))
    except Exception as e:
        print(e)
        config.filterPatchProb = 0.0
    
    config.directorController = Director(config)
 
    try :
        config.directorController.slotRate = float(workConfig.get("compositions", "slotRate"))
        config.directorController.delay = float(workConfig.get("compositions", "redrawSpeed"))
    except Exception as e:
        print(str(e))
        config.directorController.slotRate = .02
        config.directorController.delay = .02
        
    # initShapes()
    initCompositions()


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

def rebuildColorPalette():
    config.colorSetInUse  = math.floor(random.uniform(0,len(config.colorSets)))
    c = config.colorSets[config.colorSetInUse]
    config.colOverlayA.minHue = c.bg_minHue
    config.colOverlayA.maxHue = c.bg_maxHue
    config.colOverlayA.minSaturation = c.bg_minSaturation
    config.colOverlayA.maxSaturation = c.bg_maxSaturation
    config.colOverlayA.minValue = c.bg_minValue
    config.colOverlayA.maxValue = c.bg_maxValue
    config.colOverlayA.dropHueMin = c.bg_dropHueMin
    config.colOverlayA.dropHueMax = c.bg_dropHueMax
    config.colOverlayA.colorTransitionSetup()
    
    

def drawFigure() :
    # redraw()
    config.t2 = time.time()
    delta = config.t2 - config.t1

    if delta > config.timeToComplete:
        config.snapShot = config.imageLayer.copy()
        config.imageLayer = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
        config.imageLayerDraw = ImageDraw.Draw(config.imageLayer)
        
        if random.random()  < .5 :
            rebuildColorPalette()       
            
        restartDrawing()
        
    renderCompositions()
    
    
def redraw():
    global config, shapeGroups

    shapes = config.shapeGroups[config.shapeGroupDisplayed]
    shapeCount = 0
    
    for shapeElement in shapes:
        shapeElement.transition()
        img = shapeElement.tempImage.convert("RGBA")
        config.imageLayer.paste(
            img, (shapeElement.shapeXPosition, shapeElement.shapeYPosition), img
        )
        
        if random.random() < shapeElement.changeBoxProb :
            shapeElement.setNewBox()


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

def makeBackGround(drawRef, n=1):
    rows = config.patternRows * 2
    cols = config.patternCols * 2

    xDiv = config.canvasWidth / cols  # - config.patternColsOffset
    yDiv = config.canvasHeight / rows  # - config.patternRowsOffset

    xStart = 0
    yStart = 0

    drawRef.rectangle(
        (0, 0, config.canvasWidth, config.canvasHeight), fill=config.bgBackGroundColor
    )

    ## Chevron pattern
    for r in range(0, rows):
        for c in range(0, cols):
            poly = []
            poly.append((xStart, yStart + yDiv))
            poly.append((xStart + xDiv, yStart))
            poly.append((xStart + xDiv + xDiv, yStart + yDiv))
            poly.append((xStart + xDiv, yStart + yDiv + yDiv))
            # if(n ==2) : color = (100,200,0,255)
            if random.random() < config.patternDrawProb:
                drawRef.polygon(
                    poly, fill=config.bgForeGroundColor
                )  # outline = (15,15,15)
            xStart += 2 * xDiv
        xStart = 0
        yStart += 2 * yDiv


def drawBackGround():
    global config

    # config.workImageDraw.rectangle((0,0,config.canvasWidth,config.canvasHeight), fill=(config.bgR, config.bgG, config.bgB,config.fade))
    config.workImage.paste(config.leadBG, (config.bgXpos, config.bgYpos))
    config.workImage.paste(
        config.followBG, (config.bgXpos, config.bgYpos - config.canvasHeight)
    )

    if config.bgYStepSpeed < 0:
        config.workImage.paste(
            config.followBG, (config.bgXpos, config.bgYpos + config.canvasHeight)
        )

    if config.applyColorOverlayToFullImage == True:
        config.workImage.paste(config.imageLayer, (0, 0), config.imageLayer)

    if (
        config.useColorOverlayTransitions == True
        and config.applyColorOverlayToFullImage == False
    ):
        # Color overlay on b/w PNG sprite
        # clrBlockDraw.rectangle((0,0, config.canvasWidth, config.canvasHeight), fill=(255,255,255))
        config.clrBlockDraw.rectangle(
            ((0, 0, config.canvasWidth, config.canvasHeight)), fill=config.fillColorA
        )
        try:
            # ******************************************************************************
            # this puts a color overlay on the grey patterned background that is constantly
            # moving
            config.workImage = ImageChops.multiply(config.clrBlock, config.workImage)

        except Exception as e:
            print(e, config.clrBlock.mode, config.renderImageFull.mode)
            pass

    config.bgYpos += config.bgYStepSpeed
    config.bgXpos += config.bgXStepSpeed
    lead = config.leadBG
    leadBGDraw = config.leadBGDraw
    swap = False

    if config.bgXpos > config.canvasWidth:
        config.bgXpos = -config.canvasWidth

    if config.bgYpos > 1 * config.canvasHeight and config.bgYStepSpeed > 0:
        config.workImage.paste(config.leadBG, (config.bgXpos, -1 * config.canvasHeight))
        makeBackGround(leadBGDraw)
        swap = True

    if config.bgYpos < -1 * config.canvasHeight and config.bgYStepSpeed < 0:
        config.workImage.paste(config.leadBG, (config.bgXpos, 1 * config.canvasHeight))
        makeBackGround(leadBGDraw)
        swap = True

    if swap == True:
        config.leadBG = config.followBG
        config.followBG = lead

        config.leadBGDraw = config.followBGDraw
        config.followBGDraw = leadBGDraw
        config.bgYpos = 0

"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def ScaleRotateTranslate(image, angle, center=None, new_center=None, scale=None, expand=False):
    if center is None:
        return image.rotate(angle)
    angle = -angle / 180.0 * math.pi
    nx, ny = x, y = center
    sx = sy = 1.0
    if new_center:
        (nx, ny) = new_center
    if scale:
        (sx, sy) = scale
    cosine = math.cos(angle)
    sine = math.sin(angle)
    a = cosine / sx
    b = sine / sx
    c = x - nx * a - ny * b
    d = -sine / sy
    e = cosine / sy
    f = y - nx * d - ny * e
    return image.transform(
        image.size, Image.AFFINE, (a, b, c, d, e, f), resample=Image.BICUBIC
    )


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

def callBack():
    global config
    pass


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

def runWork():
    global config
    print(bcolors.OKGREEN + "** " + bcolors.BOLD)
    print("RUNNING compositions3.py")
    print(bcolors.OKGREEN + "** " + bcolors.BOLD)
    print(bcolors.ENDC)
    while config.isRunning == True:
        config.directorController.checkTime()
        if config.directorController.advance == True:
            iterate()
            time.sleep(config.directorController.delay)
        if config.standAlone == False :
            config.callBack()


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def iterate():
    global config

    ### In each cycle, the color transition is stepped forward and placed on top of the background
    ### If the piece uses the scrolling background, the colorOverlayA.currentColor is used
    config.colOverlayA.stepTransition()
    
    config.fillColorA = tuple(
        int(a * config.brightness) for a in config.colOverlayA.currentColor
    )

    if config.useScrollingBackGround == False:
        if config.useColorOverlayTransitions == True:
            config.workImageDraw.rectangle(
                (0, 0, config.canvasWidth, config.canvasHeight), fill=config.fillColorA
            )
        else:
            config.workImageDraw.rectangle(
                (0, 0, config.canvasWidth, config.canvasHeight),
                fill=(config.bgR, config.bgG, config.bgB, config.fade),
            )

        config.workImage.paste(config.imageLayer, (0, 0), config.imageLayer)
    else:
        drawBackGround()

    if random.random() < 0.01:
        config.pixSortprobDraw = random.uniform(0, 0.01)
        
    # *********************  DRAW HERE ******************
    # *********************  DRAW HERE ******************
    # *********************  DRAW HERE ******************
    drawFigure()

    config.workImage.paste(config.imageLayer, (0, 0), config.imageLayer)
    
    if random.random() < config.filterPatchProb:
        #print("should be remapping")
        minWidth = round(random.uniform(60,config.canvasWidth))
        minHeight = round(random.uniform(60,config.canvasHeight))
        x1 = round(random.uniform(0,config.canvasWidth))
        x2 = round(random.uniform(x1 + minWidth ,config.canvasWidth))
        y1 = round(random.uniform(0,config.canvasHeight))
        y2 = round(random.uniform(y1 + minHeight,config.canvasHeight))

        config.remapImageBlock = True
        config.remapImageBlockSection = (x1, y1, x2, y2)
        config.remapImageBlockDestination = (x1, y1)

    config.render(config.workImage, 0, 0)


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

def main(run=True):
    global config, threads, thrd
    init()

    if run:
        runWork()

"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

### Kick off .......
if __name__ == "__main__":
    main()
