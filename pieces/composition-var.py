import random
import time
import math
from collections import OrderedDict
from modules.configuration import bcolors
import numpy
from modules import coloroverlay, colorutils
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFont, ImageOps
from modules.holder_director import Holder 
from modules.holder_director import Director 

global thrd, config


# ------------------------------------------------------------------ #

class Fader:
    def __init__(self):
        self.doingRefresh = 0
        self.doingRefreshCount = 20
        self.fadingDone = False
        self.testing = True

    def setUp(self):
        self.blankImage = Image.new("RGBA", (self.width, self.height))
        self.image = Image.new("RGBA", (self.width, self.height))
        self.crossFade = Image.new("RGBA", (self.width, self.height))

    def test(self):
        print("test")
        # self.blankImage = Image.new("RGBA", (self.width, self.height))
        draw = ImageDraw.Draw(self.crossFade)
        draw.rectangle((0, 0, 100, 100), fill=(0, 0, 255, 255))
        config.image.paste(
            self.crossFade, (self.xPos, self.yPos), self.crossFade
        )

    def fadeIn(self, config):
        config.fadeThruBlack = False
        if self.doingRefreshCount >= 0 and self.fadingDone == False:

            if self.testing == True:
                self.testing = False
                # print(self.fadingDone, self.doingRefresh)

            if self.doingRefresh < self.doingRefreshCount:

                if config.fadeThruBlack == True:
                    self.blankImage = Image.new(
                        "RGBA", (self.width, self.height))
                percent = self.doingRefresh / self.doingRefreshCount
                self.crossFade = Image.blend(
                    self.blankImage,
                    self.image,
                    percent,
                )
                config.image.paste(
                    self.crossFade, (self.xPos, self.yPos), self.crossFade
                )
                self.doingRefresh += 1
            else:
                # config.image.paste(self.image, (self.xPos, self.yPos), self.image)
                self.fadingDone = True
                self.doingRefresh = 0
                self.blankImage = self.image.copy()
                self.testing = True                
                # print("Fade done")
                # time.sleep(5)
                
        else :
            self.fadingDone =  True


class DrawingUnit:
    def __init__(self, config):
        self.config = config
        self.units = []
        self.unitFills = []


class ColorSet :
    def __init__(self):
        self.name = "cset"


class CompositionManager:
    def __init__(self, config):
        self.config = config

    def setUp(self, workConfig):
        config = self.config
        config.redrawSpeed = float(workConfig.get("compositions", "redrawSpeed"))
        self.redrawProbablility = float(workConfig.get("compositions", "redrawProbablility"))
        self.xVariance = float(workConfig.get("compositions", "xVariance"))
        self.xOffset = int(workConfig.get("compositions", "xOffset"))
        self.yOffset = int(workConfig.get("compositions", "yOffset"))
        self.varX = int(workConfig.get("compositions", "varX"))
        self.varY = int(workConfig.get("compositions", "varY"))
        self.angleRotationRange = float(workConfig.get("compositions", "angleRotationRange"))

        self.blockWidthRange = workConfig.get("compositions", "blockWidthRange").split(",")
        self.blockWidthRange = tuple([int(i) for i in self.blockWidthRange])
        self.blockHeightRange = workConfig.get("compositions", "blockHeightRange").split(",")
        self.blockHeightRange = tuple([int(i) for i in self.blockHeightRange])
        self.centerRange = int(workConfig.get("compositions", "centerRange"))

        self.fade = int(workConfig.get("compositions", "fade"))

        self.useColorOverlayTransitions = workConfig.getboolean("compositions", "useColorOverlayTransitions")
        self.applyColorOverlayToFullImage = workConfig.getboolean("compositions", "applyColorOverlayToFullImage")
        self.useScrollingBackGround = workConfig.getboolean("compositions", "useScrollingBackGround")
        self.patternRows = int(workConfig.get("compositions", "patternRows"))
        self.patternCols = int(workConfig.get("compositions", "patternCols"))
        self.patternRowsOffset = int(workConfig.get("compositions", "patternRowsOffset"))
        self.patternColsOffset = int(workConfig.get("compositions", "patternColsOffset"))
        self.bgYStepSpeed = int(workConfig.get("compositions", "bgYStepSpeed"))
        self.bgXStepSpeed = int(workConfig.get("compositions", "bgXStepSpeed"))

        self.yDivHeightAddition = int(workConfig.get("compositions", "yDivHeightAddition"))
        self.xDivWidthAddition = int(workConfig.get("compositions", "xDivWidthAddition"))

        self.pixSortXOffsetVal = config.pixSortXOffset
        self.colorTransitionRangeMin = float(workConfig.get("compositions", "colorTransitionRangeMin"))
        self.colorTransitionRangeMax = float(workConfig.get("compositions", "colorTransitionRangeMax"))

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
        self.patternDrawProb = float(workConfig.get("compositions", "patternDrawProb"))

        self.bgBackGroundColor = workConfig.get("compositions", "bgBackGroundColor").split(",")
        self.bgBackGroundColor = tuple([int(i) for i in self.bgBackGroundColor])

        self.bgForeGroundColor = workConfig.get("compositions", "bgForeGroundColor").split(",")
        self.bgForeGroundColor = tuple([int(i) for i in self.bgForeGroundColor])

        config.bg1 = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
        config.bg1Draw = ImageDraw.Draw(config.bg1)
        config.bg1Draw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=self.bgBackGroundColor)
        makeBackGround(config.bg1Draw, 1)

        config.bg2 = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
        config.bg2Draw = ImageDraw.Draw(config.bg2)
        config.bg2Draw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=self.bgBackGroundColor)
        makeBackGround(config.bg2Draw, 2)

        self.leadBG = config.bg1
        self.followBG = config.bg2
        self.leadBGDraw = config.bg1Draw
        self.followBGDraw = config.bg2Draw

        config.bgImage.paste(config.bg1)
        config.bgImage.paste(config.bg2, (0, config.canvasHeight))
        self.bgXpos = 0
        self.bgYpos = 0

        ### the overlay color affects the background only in this case

        self.colorSets = []
        colorSets = list(map(lambda x: x, workConfig.get("compositions", "colorSetsToUse").split(",")))

        for n in range(0, len(colorSets)):

            colorSetGroup = colorSets[n]
            c = ColorSet()


            c.name = colorSetGroup

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

            self.colorSets.append(c)


        self.colOverlayA = coloroverlay.ColorOverlay()
        ### This is the speed range of transitions in color
        ### Higher numbers means more possible steps so slower
        ### transitions - 1,10 very blinky, 10,200 very slow
        self.colOverlayA.randomRange = (self.colorTransitionRangeMin,self.colorTransitionRangeMax,)
        self.colOverlayA.colorA = tuple(int(a * config.brightness) for a in (colorutils.getRandomColor()))

        self.colorSetInUse = 0

        c = self.colorSets[self.colorSetInUse]

        self.colOverlayA.minHue = c.bg_minHue
        self.colOverlayA.maxHue = c.bg_maxHue
        self.colOverlayA.minSaturation = c.bg_minSaturation
        self.colOverlayA.maxSaturation = c.bg_maxSaturation
        self.colOverlayA.minValue = c.bg_minValue
        self.colOverlayA.maxValue = c.bg_maxValue
        self.colOverlayA.dropHueMin = c.bg_dropHueMin
        self.colOverlayA.dropHueMax = c.bg_dropHueMax

        self.colOverlayA.randomSteps = True
        self.colOverlayA.timeTrigger = True
        self.colOverlayA.steps = 100
        self.colOverlayA.tLimitBase = 30
        self.colOverlayA.maxBrightness = config.brightness
        self.colOverlayA.colorTransitionSetup()

        try:
            self.filterPatchProb = float(workConfig.get("compositions", "filterPatchProb"))
        except Exception as e:
            print(e)
            self.filterPatchProb = 0.0
        try:
            self.filterPatchMinWidth = float(workConfig.get("compositions", "filterPatchMinWidth"))
            self.filterPatchMinHeight = float(workConfig.get("compositions", "filterPatchMinHeight"))
        except Exception as e:
            print(e)
            self.filterPatchMinWidth = 60
            self.filterPatchMinHeight = 60

        config.directorController = Director(config)

        try :
            config.directorController.slotRate = float(workConfig.get("compositions", "slotRate"))
            config.directorController.delay = float(workConfig.get("compositions", "redrawSpeed"))
        except Exception as e:
            print(str(e))
            config.directorController.slotRate = .02
            config.directorController.delay = .02


        initCompositions()


# ------------------------------------------------------------------ #

def renderCompositions():
    temp = Image.new("RGBA", (cmpMngr.canvasImageWidth, cmpMngr.canvasImageHeight))
    drawtemp = ImageDraw.Draw(temp)

    for i in range(0, len(cmpMngr.drawingUnit.units)) :
        # drawtemp.rectangle(cmpMngr.drawingUnit.units[i], fill=cmpMngr.drawingUnit.unitFills[i])
        drawtemp.polygon(cmpMngr.drawingUnit.units[i], fill=cmpMngr.drawingUnit.unitFills[i])


    temp = temp.rotate(cmpMngr.orientationRotationFinal, expand=1)
    # config.imageLayer.paste(temp, temp)


    temp2 = Image.new("RGBA", (temp.size[0], temp.size[1]))
    # temp2Draw = ImageDraw.Draw(temp2)
    # temp2Draw.rectangle((0,0,300,300), fill = (0,0,0,0))
    pct = cmpMngr.pctAlphaNewFigure
    temp3 = Image.blend(temp2,temp,pct)
    config.imageLayer.paste(temp3, temp3)

    if cmpMngr.pctAlphaNewFigure < 1.0 :
        cmpMngr.pctAlphaNewFigure += .085



    # time.sleep(1)
    # if cmpMngr.fader.fadingDone == True :
    #     config.imageLayer.paste(temp, temp)

    # # Fade in the paste a bit to soften the appearance
    # if cmpMngr.fader.fadingDone == False :
    #     if cmpMngr.fader.doingRefresh == 0 :
    #         cmpMngr.fader.height = temp.size[1]
    #         cmpMngr.fader.width = temp.size[0]
    #         cmpMngr.fader.setUp()
    #         cmpMngr.fader.image = temp

    #     cmpMngr.fader.fadeIn(config)

    # # if cmpMngr.figureIsFadedIn == False :
    # #     cmpMngr.figureBlendAlpha +=1

    # #     config.imageLayer = Image.blend(config.imageLayer , temp, cmpMngr.figureBlendAlpha)

    # #     if cmpMngr.figureBlendAlpha >= 255 :
    # #         cmpMngr.figureIsFadedIn = True

    # if cmpMngr.fader.fadingDone == True :
    #     config.imageLayer.paste(temp, temp)
    # else :
    #     config.imageLayer.paste(cmpMngr.fader.crossFade, cmpMngr.fader.crossFade)


def drawCompositions():
    print("\n**********************")
    print("Drawing the figure")
    print("**********************")


    cmpMngr.pctAlphaNewFigure = 0
    # cmpMngr.fader.fadingDone = False
    # cmpMngr.fader.doingRefreshCount = 40


    cmpMngr.drawingUnit = DrawingUnit(config)

    startx = cmpMngr.imageWidth / 9

    startx = 0
    wVariance = [cmpMngr.imageWidth / 3, cmpMngr.imageWidth / 1]
    hVariance = [cmpMngr.imageHeight / 3, cmpMngr.imageHeight / 1]
    wFactor = 1
    hFactor = 1

    cmpMngr.orientationRotationFinal = cmpMngr.orientationRotation + random.uniform(-cmpMngr.angleRotationRange, cmpMngr.angleRotationRange)


    # Choose seam x point  -- ideally about 1/3 from left
    # the 100 px spread around the 1/3 width should really be proportional to the overall size
    # xVariance = round(random.uniform(config.canvasWidth - 50, config.canvasWidth + 50) / 3)
    xVarianceSpread = round(config.canvasWidth/6)
    xVariance = round(random.uniform(cmpMngr.imageWidth - xVarianceSpread, cmpMngr.imageWidth + xVarianceSpread) / 3)
    cmpMngr.flip = False

    xSeam = round(random.uniform(cmpMngr.imageWidth * 2 / 3 - xVariance, cmpMngr.imageWidth * 2 / 3 + xVariance))

    config.pixSortXOffset = xSeam
    tiedToBottom = 0 if random.random() < 0.5 else 2

    # config.imageLayer.paste(temp, temp)
    fills = []
    fills.append([0])

    lastBlockY = cmpMngr.imageHeight
    c = cmpMngr.colorSets[cmpMngr.colorSetInUse]
    for n in range(0, cmpMngr.numSquarePairs):
    
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
        ''' 
        if n == 2:
            wFactor *= 1.5
            # fills = (0,255,0,255)

        if n == 0:
            x1 = round(xSeam)
            x2 = round(random.uniform(x1 + startx, x1 + wVariance[1]))
            y1 = round(random.uniform(hVariance[0], hVariance[1]))
            y2 = round(random.uniform(y1 + hVariance[0] * hFactor, y1 + hVariance[1] * hFactor))
            if n == tiedToBottom:
                y2 = config.imageHeight
            starty = round(random.uniform(0, config.imageHeight / 2)) + config.yOffset
            

        else:
            x1 = round(random.uniform(xSeam - startx * wFactor, xSeam - wVariance[1] * wFactor))
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
        '''
        poly = []
        xVar  = round(random.uniform(-cmpMngr.varX,cmpMngr.varX))
        yVar  = round(random.uniform(-cmpMngr.varY,cmpMngr.varY))
        
        nextBlockHeight = round(random.uniform(cmpMngr.blockHeightRange[0],cmpMngr.blockHeightRange[1]))
        nextBlockWidth = round(random.uniform(cmpMngr.blockWidthRange[0],cmpMngr.blockWidthRange[1]))
        centerX = round(cmpMngr.imageWidth/2 + random.uniform(-cmpMngr.centerRange,cmpMngr.centerRange))
        x1 = round(centerX - nextBlockWidth/2)
        y1 = lastBlockY
        x2 = round(x1 + nextBlockWidth)
        y2 = y1 - nextBlockHeight
        lastBlockY = y2
        
        
        poly.append((x1, y1))
        poly.append((x2 + xVar, y1 + yVar))
        poly.append((x2 + 0, y2 + yVar))
        poly.append((x1, y2))

        cmpMngr.drawingUnit.units.append(poly)
        cmpMngr.drawingUnit.unitFills.append(fills)


    if cmpMngr.flip == True:
        config.imageLayer = config.imageLayer.transpose(Image.FLIP_TOP_BOTTOM)
        config.imageLayer = config.imageLayer.transpose(Image.ROTATE_180)
        

def initCompositions():
    cmpMngr.canvasImageWidth = int(workConfig.get("compositions", "canvasImageWidth"))
    cmpMngr.canvasImageHeight = int(workConfig.get("compositions", "canvasImageHeight"))
    cmpMngr.orientationRotation = float(workConfig.get("compositions", "orientationRotation"))
    cmpMngr.orientationRotationFinal = float(workConfig.get("compositions", "orientationRotation"))

    cmpMngr.refreshCount = int(workConfig.get("compositions", "refreshCount"))
    cmpMngr.timeToComplete = float(workConfig.get("compositions", "timeToComplete"))
    cmpMngr.cleanSlateProbability = float(workConfig.get("compositions", "cleanSlateProbability"))
    cmpMngr.filterPatchProb = float(workConfig.get("compositions", "filterPatchProb"))

    cmpMngr.imageWidth = cmpMngr.canvasImageWidth
    cmpMngr.imageHeight = cmpMngr.canvasImageHeight

    cmpMngr.numSquarePairs = int(workConfig.get("compositions", "numSquarePairs"))

    cmpMngr.t1 = time.time()
    cmpMngr.t2 = time.time()

    # initial crossfade settings
    cmpMngr.doingRefresh = cmpMngr.refreshCount
    cmpMngr.doingRefreshCount = cmpMngr.refreshCount

    # config.canvasImage = Image.new("RGBA", (cmpMngr.canvasImageWidth, cmpMngr.canvasImageHeight))
    # config.draw = ImageDraw.Draw(config.canvasImage)
    # config.draw.rectangle((0, 0, cmpMngr.imageWidth, cmpMngr.imageHeight), fill=cmpMngr.bgColor)

    cmpMngr.firstRun = True
    cmpMngr.flip = False


    cmpMngr.figureBlendAlpha = 0
    cmpMngr.figureIsFadedIn = False

    # cmpMngr.fader = Fader()
    # cmpMngr.fader.height = cmpMngr.canvasImageHeight
    # cmpMngr.fader.width = cmpMngr.canvasImageWidth
    # cmpMngr.fader.xPos = 0
    # cmpMngr.fader.yPos = 0
    # cmpMngr.fader.setUp()

    print("Running")
    drawCompositions()


def restartDrawing():

    cmpMngr.flip = True if random.random() < 0.5 else False
    if random.random() < cmpMngr.cleanSlateProbability or cmpMngr.firstRun == True:
        # grayLevel = round(random.uniform(20,70))
        # cmpMngr.bgColor = (grayLevel,grayLevel,grayLevel)
        c = cmpMngr.colorSets[cmpMngr.colorSetInUse]

        cmpMngr.bgColor = colorutils.getRandomColorHSVSaturated(
            c.bg_minHue,
            c.bg_maxHue,
            c.bg_minSaturation,
            c.bg_maxSaturation,
            c.bg_minValue,
            c.bg_maxValue,
            c.bg_dropHueMin,
            c.bg_dropHueMax
        )
        # print(cmpMngr.bgColor)
        # cmpMngr.bgColor = colorutils.getRandomColorHSV(0,360, .3,.95, .1,.94)
        config.draw.rectangle(
            (0, 0, cmpMngr.imageWidth, cmpMngr.imageHeight), fill=cmpMngr.bgColor
        )

        cmpMngr.firstRun = False
    drawCompositions()

    cmpMngr.t1 = time.time()
    cmpMngr.t2 = time.time()
    # initialize crossfade - in this case 100 steps ...
    cmpMngr.doingRefresh = 0
    cmpMngr.doingRefreshCount = cmpMngr.refreshCount


def drawFigure() :
    # redraw()
    cmpMngr.t2 = time.time()
    delta = cmpMngr.t2 - cmpMngr.t1

    if delta > cmpMngr.timeToComplete:

        print("Starting a new drawing")
        cmpMngr.snapShot = config.imageLayer.copy()
        config.workImage.paste(cmpMngr.snapShot, (0, 0), cmpMngr.snapShot)
        config.imageLayer = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
        config.imageLayerDraw = ImageDraw.Draw(config.imageLayer)
        # config.imageLayer.paste(cmpMngr.snapShot, (0,0))

        if random.random()  < .5 :
            rebuildColorPalette()

        restartDrawing()

    renderCompositions()

# ------------------------------------------------------------------ #


def rebuildColorPalette():
    cmpMngr.colorSetInUse  = math.floor(random.uniform(0,len(cmpMngr.colorSets)))
    c = cmpMngr.colorSets[cmpMngr.colorSetInUse]
    print("Changing color to ", c.name)
    cmpMngr.colOverlayA.minHue = c.bg_minHue
    cmpMngr.colOverlayA.maxHue = c.bg_maxHue
    cmpMngr.colOverlayA.minSaturation = c.bg_minSaturation
    cmpMngr.colOverlayA.maxSaturation = c.bg_maxSaturation
    cmpMngr.colOverlayA.minValue = c.bg_minValue
    cmpMngr.colOverlayA.maxValue = c.bg_maxValue
    cmpMngr.colOverlayA.dropHueMin = c.bg_dropHueMin
    cmpMngr.colOverlayA.dropHueMax = c.bg_dropHueMax
    cmpMngr.colOverlayA.colorTransitionSetup()
    
    
# ------------------------------------------------------------------ #

def makeBackGround(drawRef, n=1):
    rows = cmpMngr.patternRows * 2
    cols = cmpMngr.patternCols * 2

    xDiv = config.canvasWidth / cols + cmpMngr.xDivWidthAddition # - cmpMngr.patternColsOffset
    yDiv = config.canvasHeight / rows + cmpMngr.yDivHeightAddition # - cmpMngr.patternRowsOffset

    xStart = 0
    yStart = 0

    # cmpMngr.bgBackGroundColor = (0,255,0,255)

    drawRef.rectangle(
        (0, 0, config.canvasWidth, config.canvasHeight), fill=cmpMngr.bgBackGroundColor
    )


    ## Chevron pattern
    for r in range(0, rows):
        # this is to get a little random overlap, less regular
        nDisplace = round(random.uniform(-10,10))
        zDisplace = round(random.uniform(-0,0))
        for c in range(0, cols):
            poly = []
            poly.append((xStart, yStart + yDiv))
            poly.append((xStart + xDiv, yStart))
            poly.append((xStart + xDiv + xDiv, yStart + yDiv))
            poly.append((xStart + xDiv, yStart + yDiv + yDiv))
            # if(n ==2) : color = (100,200,0,255)

            if c % 2 > 0 :
                poly = []
                poly.append((xStart + zDisplace, yStart  + nDisplace * c))
                poly.append((xStart + zDisplace + xDiv , yStart  + nDisplace * c + yDiv + yDiv))
                poly.append((xStart + zDisplace + xDiv  + 1 , yStart  + nDisplace * c + yDiv + yDiv))
                poly.append((xStart + zDisplace + 1, yStart  + nDisplace * c))
            else :
                poly = []
                poly.append((xStart + zDisplace  + xDiv, yStart  + nDisplace * c))
                poly.append((xStart + zDisplace   , yStart  + nDisplace * c + yDiv + yDiv))
                poly.append((xStart + zDisplace    + 1 , yStart  + nDisplace * c + yDiv + yDiv))
                poly.append((xStart + zDisplace + xDiv + 1, yStart  + nDisplace * c))

            if random.random() < cmpMngr.patternDrawProb:
                # drawRef.polygon(poly, fill=cmpMngr.bgForeGroundColor)  # outline = (15,15,15)
                drawRef.line((poly[0],poly[1]), fill = cmpMngr.bgForeGroundColor)
            xStart += 2 * xDiv
        xStart = 0
        yStart += 2 * yDiv


def drawBackGround():
    global config

    # config.workImageDraw.rectangle((0,0,config.canvasWidth,config.canvasHeight), fill=(config.bgR, config.bgG, config.bgB,cmpMngr.fade))
    config.workImage.paste(cmpMngr.leadBG, (cmpMngr.bgXpos, cmpMngr.bgYpos))
    config.workImage.paste(
        cmpMngr.followBG, (cmpMngr.bgXpos, cmpMngr.bgYpos - config.canvasHeight)
    )

    if cmpMngr.bgYStepSpeed < 0:
        config.workImage.paste(
            cmpMngr.followBG, (cmpMngr.bgXpos, cmpMngr.bgYpos + config.canvasHeight)
        )

    if cmpMngr.applyColorOverlayToFullImage == True:
        config.workImage.paste(config.imageLayer, (0, 0), config.imageLayer)

    if (
        cmpMngr.useColorOverlayTransitions == True
        and cmpMngr.applyColorOverlayToFullImage == False
    ):
        # Color overlay on b/w PNG sprite
        # clrBlockDraw.rectangle((0,0, config.canvasWidth, config.canvasHeight), fill=(255,255,255))
        config.clrBlockDraw.rectangle(
            ((0, 0, config.canvasWidth, config.canvasHeight)), fill=cmpMngr.fillColorA
        )
        try:
            # ******************************************************************************
            # this puts a color overlay on the grey patterned background that is constantly
            # moving
            config.workImage = ImageChops.multiply(config.clrBlock, config.workImage)

        except Exception as e:
            print(e, config.clrBlock.mode, config.renderImageFull.mode)
            pass

    cmpMngr.bgYpos += cmpMngr.bgYStepSpeed
    cmpMngr.bgXpos += cmpMngr.bgXStepSpeed
    lead = cmpMngr.leadBG
    leadBGDraw = cmpMngr.leadBGDraw
    swap = False

    if cmpMngr.bgXpos > config.canvasWidth:
        cmpMngr.bgXpos = -config.canvasWidth
        makeBackGround(leadBGDraw)

    if cmpMngr.bgYpos > 1 * config.canvasHeight and cmpMngr.bgYStepSpeed > 0:
        config.workImage.paste(cmpMngr.leadBG, (cmpMngr.bgXpos, -1 * config.canvasHeight))
        makeBackGround(leadBGDraw)
        swap = True

    if cmpMngr.bgYpos < -1 * config.canvasHeight and cmpMngr.bgYStepSpeed < 0:
        config.workImage.paste(cmpMngr.leadBG, (cmpMngr.bgXpos, 1 * config.canvasHeight))
        makeBackGround(leadBGDraw)
        swap = True

    if swap == True:
        cmpMngr.leadBG = cmpMngr.followBG
        cmpMngr.followBG = lead

        cmpMngr.leadBGDraw = cmpMngr.followBGDraw
        cmpMngr.followBGDraw = leadBGDraw
        cmpMngr.bgYpos = 0

# ------------------------------------------------------------------ #


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


# ------------------------------------------------------------------ #

def callBack():
    global config
    pass


# ------------------------------------------------------------------ #

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


# ------------------------------------------------------------------ #


def iterate():
    global config

    ### In each cycle, the color transition is stepped forward and placed on top of the background
    ### If the piece uses the scrolling background, the colorOverlayA.currentColor is used
    cmpMngr.colOverlayA.stepTransition()

    cmpMngr.fillColorA = tuple(
        int(a * config.brightness) for a in cmpMngr.colOverlayA.currentColor
    )

    if cmpMngr.useScrollingBackGround == False:
        if cmpMngr.useColorOverlayTransitions == True:
            config.workImageDraw.rectangle(
                (0, 0, config.canvasWidth, config.canvasHeight), fill=(cmpMngr.fillColorA[0],cmpMngr.fillColorA[1],cmpMngr.fillColorA[2],cmpMngr.fade)
            )
        else:
            config.workImageDraw.rectangle(
                (0, 0, config.canvasWidth, config.canvasHeight),
                fill=(config.bgR, config.bgG, config.bgB, cmpMngr.fade),
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



    if random.random() < cmpMngr.filterPatchProb:
        #print("should be remapping")
        minWidth = round(random.uniform(cmpMngr.filterPatchMinWidth,config.canvasWidth))
        minHeight = round(random.uniform(cmpMngr.filterPatchMinHeight,config.canvasHeight))
        x1 = round(random.uniform(0,config.canvasWidth))
        x2 = round(random.uniform(x1 + minWidth ,config.canvasWidth))
        y1 = round(random.uniform(0,config.canvasHeight))
        y2 = round(random.uniform(y1 + minHeight,config.canvasHeight))

        config.remapImageBlock = True
        config.remapImageBlockSection = (x1, y1, x2, y2)
        config.remapImageBlockDestination = (x1, y1)

    config.render(config.workImage, 0, 0)


# ------------------------------------------------------------------ #

def main(run=True):
    global config, threads, thrd, cmpMngr, workConfig
    cmpMngr = CompositionManager(config)
    cmpMngr.setUp(workConfig)

    if run:
        runWork()

# ------------------------------------------------------------------ #

### Kick off .......
if __name__ == "__main__":
    main()
