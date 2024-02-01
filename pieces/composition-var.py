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

"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


class DrawingUnit:
    def __init__(self, config):
        self.config = config
        self.units = []
        self.unitFills = []


def renderCompositions():
    temp = Image.new("RGBA", (config.canvasImageWidth, config.canvasImageHeight))
    drawtemp = ImageDraw.Draw(temp)
    
    for i in range(0, len(config.drawingUnit.units)) :
        # drawtemp.rectangle(config.drawingUnit.units[i], fill=config.drawingUnit.unitFills[i])
        drawtemp.polygon(config.drawingUnit.units[i], fill=config.drawingUnit.unitFills[i])

    
    temp = temp.rotate(config.orientationRotationFinal, expand=1)
    # config.imageLayer.paste(temp, temp)
    
    
    temp2 = Image.new("RGBA", (temp.size[0], temp.size[1]))
    # temp2Draw = ImageDraw.Draw(temp2)
    # temp2Draw.rectangle((0,0,300,300), fill = (0,0,0,0))
    pct = config.pctAlphaNewFigure 
    temp3 = Image.blend(temp2,temp,pct)
    config.imageLayer.paste(temp3, temp3)
    
    if config.pctAlphaNewFigure < 1.0 :
        config.pctAlphaNewFigure += .085
    


    # time.sleep(1)    
    # if config.fader.fadingDone == True :
    #     config.imageLayer.paste(temp, temp)
    
    # # Fade in the paste a bit to soften the appearance
    # if config.fader.fadingDone == False :
    #     if config.fader.doingRefresh == 0 :
    #         config.fader.height = temp.size[1]
    #         config.fader.width = temp.size[0]
    #         config.fader.setUp()
    #         config.fader.image = temp
            
    #     config.fader.fadeIn(config)
    
    # # if config.figureIsFadedIn == False :
    # #     config.figureBlendAlpha +=1
        
    # #     config.imageLayer = Image.blend(config.imageLayer , temp, config.figureBlendAlpha)
        
    # #     if config.figureBlendAlpha >= 255 :
    # #         config.figureIsFadedIn = True
            
    # if config.fader.fadingDone == True :
    #     config.imageLayer.paste(temp, temp)
    # else :
    #     config.imageLayer.paste(config.fader.crossFade, config.fader.crossFade)
        

def drawCompositions():
    print("\n**********************")
    print("Drawing the figure")
    print("**********************")
    

    config.pctAlphaNewFigure = 0
    # config.fader.fadingDone = False
    # config.fader.doingRefreshCount = 40
    

    config.drawingUnit = DrawingUnit(config)

    startx = config.imageWidth / 9
    
    startx = 0
    wVariance = [config.imageWidth / 3, config.imageWidth / 1]
    hVariance = [config.imageHeight / 3, config.imageHeight / 1]
    wFactor = 1
    hFactor = 1
    
    config.orientationRotationFinal = config.orientationRotation + random.uniform(-config.angleRotationRange, config.angleRotationRange)


    # Choose seam x point  -- ideally about 1/3 from left
    # the 100 px spread around the 1/3 width should really be proportional to the overall size
    # xVariance = round(random.uniform(config.canvasWidth - 50, config.canvasWidth + 50) / 3) 
    xVarianceSpread = round(config.canvasWidth/6)
    xVariance = round(random.uniform(config.imageWidth - xVarianceSpread, config.imageWidth + xVarianceSpread) / 3) 
    config.flip = False

    xSeam = round(random.uniform(config.imageWidth * 2 / 3 - xVariance, config.imageWidth * 2 / 3 + xVariance))
    
    config.pixSortXOffset = xSeam
    tiedToBottom = 0 if random.random() < 0.5 else 2

    
    
    # config.imageLayer.paste(temp, temp)
    fills = []
    fills.append([0])
    
    lastBlockY = config.imageHeight
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
        xVar  = round(random.uniform(-config.varX,config.varX))
        yVar  = round(random.uniform(-config.varY,config.varY))
        
        nextBlockHeight = round(random.uniform(config.blockHeightRange[0],config.blockHeightRange[1]))
        nextBlockWidth = round(random.uniform(config.blockWidthRange[0],config.blockWidthRange[1]))
        centerX = round(config.imageWidth/2 + random.uniform(-config.centerRange,config.centerRange))
        x1 = round(centerX - nextBlockWidth/2)
        y1 = lastBlockY
        x2 = round(x1 + nextBlockWidth)
        y2 = y1 - nextBlockHeight
        lastBlockY = y2
        
        
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
    config.orientationRotation = float(workConfig.get("compositions", "orientationRotation"))
    config.orientationRotationFinal = float(workConfig.get("compositions", "orientationRotation"))
    
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
    
        
    config.figureBlendAlpha = 0
    config.figureIsFadedIn = False
    
    # config.fader = Fader()
    # config.fader.height = config.canvasImageHeight
    # config.fader.width = config.canvasImageWidth
    # config.fader.xPos = 0
    # config.fader.yPos = 0
    # config.fader.setUp()
    
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


def drawFigure() :
    # redraw()
    config.t2 = time.time()
    delta = config.t2 - config.t1

    if delta > config.timeToComplete:
        
        print("Starting a new drawing")
        config.snapShot = config.imageLayer.copy()
        config.workImage.paste(config.snapShot, (0, 0), config.snapShot)
        config.imageLayer = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
        config.imageLayerDraw = ImageDraw.Draw(config.imageLayer)
        # config.imageLayer.paste(config.snapShot, (0,0))
                
        if random.random()  < .5 :
            rebuildColorPalette()       
            
        restartDrawing()
        
    renderCompositions()

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
    config.varX = int(workConfig.get("compositions", "varX"))
    config.varY = int(workConfig.get("compositions", "varY"))
    config.angleRotationRange = float(workConfig.get("compositions", "angleRotationRange"))
    
    config.blockWidthRange = workConfig.get("compositions", "blockWidthRange").split(",")
    config.blockWidthRange = tuple([int(i) for i in config.blockWidthRange])
    config.blockHeightRange = workConfig.get("compositions", "blockHeightRange").split(",")
    config.blockHeightRange = tuple([int(i) for i in config.blockHeightRange])
    config.centerRange = int(workConfig.get("compositions", "centerRange"))
    
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
    
    config.yDivHeightAddition = int(workConfig.get("compositions", "yDivHeightAddition"))
    config.xDivWidthAddition = int(workConfig.get("compositions", "xDivWidthAddition"))
    

    config.pixSortXOffsetVal = config.pixSortXOffset
    config.colorTransitionRangeMin = float(workConfig.get("compositions", "colorTransitionRangeMin"))
    config.colorTransitionRangeMax = float(workConfig.get("compositions", "colorTransitionRangeMax"))


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

    
    initCompositions()


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

def rebuildColorPalette():
    config.colorSetInUse  = math.floor(random.uniform(0,len(config.colorSets)))
    c = config.colorSets[config.colorSetInUse]
    print("Changing color to ", c.name)
    config.colOverlayA.minHue = c.bg_minHue
    config.colOverlayA.maxHue = c.bg_maxHue
    config.colOverlayA.minSaturation = c.bg_minSaturation
    config.colOverlayA.maxSaturation = c.bg_maxSaturation
    config.colOverlayA.minValue = c.bg_minValue
    config.colOverlayA.maxValue = c.bg_maxValue
    config.colOverlayA.dropHueMin = c.bg_dropHueMin
    config.colOverlayA.dropHueMax = c.bg_dropHueMax
    config.colOverlayA.colorTransitionSetup()
    
    


    
    

"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

def makeBackGround(drawRef, n=1):
    rows = config.patternRows * 2
    cols = config.patternCols * 2

    xDiv = config.canvasWidth / cols + config.xDivWidthAddition # - config.patternColsOffset
    yDiv = config.canvasHeight / rows + config.yDivHeightAddition # - config.patternRowsOffset

    xStart = 0
    yStart = 0
    
    # config.bgBackGroundColor = (0,255,0,255)

    drawRef.rectangle(
        (0, 0, config.canvasWidth, config.canvasHeight), fill=config.bgBackGroundColor
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
            
            if random.random() < config.patternDrawProb:
                # drawRef.polygon(poly, fill=config.bgForeGroundColor)  # outline = (15,15,15)
                drawRef.line((poly[0],poly[1]), fill = config.bgForeGroundColor)
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
        makeBackGround(leadBGDraw)

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
                (0, 0, config.canvasWidth, config.canvasHeight), fill=(config.fillColorA[0],config.fillColorA[1],config.fillColorA[2],config.fade)
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
