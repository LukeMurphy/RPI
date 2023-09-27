#!/usr/bin/python
# import modules
import datetime
import gc
import getopt
import importlib
import io
import math
import os
import random
import sys
import textwrap
import time
from random import shuffle
from subprocess import call
from modules.configuration import bcolors
from modules.faderclass import FaderObj
from modules import badpixels, colorutils, coloroverlay, configuration, panelDrawing
from modules.imagesprite import ImageSprite
from PIL import (
    Image,
    ImageChops,
    ImageFont,
    ImageDraw,
    ImageEnhance,
    ImageFilter,
    ImageMath,
    ImagePalette,
)
import numpy as np

xPos = 320
yPos = 0

bads = badpixels


class Holder:
    def __init__(self, config):
        self.config = config


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


class spriteAnimation():

    frameWidth = 128
    frameHeight = 128
    totalFrames = 233
    frameCols = 16
    frameRows = 14
    sliceCol = 0
    sliceRow = 0

    sliceWidth = 128
    sliceHeight = 128

    sliceXOffset = 0
    sliceYOffset = 0

    frameCount = 0
    playCount = 0
    step = 1
    animSpeedMin = 2
    animSpeedMax = 4

    animationRotation = 0
    animationRotationRate = 0

    randomPlacement = True
    resizeAnimationToFit = False
    animationWidth = 256
    animationHeight = 256

    xPos = 0
    yPos = 0

    frameArray = []

    pause = False

    def __init__(self, config):
        self.config = config
        self.imageFrame = Image.new(
            "RGBA", (self.frameWidth, self.frameHeight))

    def prepSlices(self):
        frame = 0
        for c in range(0, self.frameCols):
            for r in range(0, self.frameCols):
                if frame < self.frameCount:
                    xPos = c * self.frameWidth + self.sliceXOffset
                    yPos = r * self.frameHeight + self.sliceYOffset

                    frameSlice = self.image.crop(
                        (xPos, yPos, xPos + self.sliceWidth, yPos + self.sliceHeight))
                    if self.animationRotation != 0:
                        frameSlice = frameSlice.rotate(
                            self.animationRotation, 0, 1)

                    if self.config.brightness != 1.0:
                        enhancer = ImageEnhance.Brightness(frameSlice)
                        frameSlice = enhancer.enhance(self.config.brightness)
                    self.frameArray.append(frameSlice)
                    frame += 1

    def nextFrame(self):
        xPos = self.sliceCol * self.frameWidth + self.sliceXOffset
        yPos = self.sliceRow * self.frameHeight + self.sliceYOffset

        frameSlice = self.image.crop(
            (xPos, yPos, xPos + self.sliceWidth, yPos + self.sliceHeight))

        if self.resizeAnimationToFit == True:
            frameSlice = frameSlice.resize(
                (self.animationHeight, self.animationWidth))

        if self.animationRotation != 0:
            frameSlice = frameSlice.rotate(self.animationRotation, 0, 1)

        if self.config.brightness != 1.0:
            enhancer = ImageEnhance.Brightness(frameSlice)
            frameSlice = enhancer.enhance(self.config.brightness)

        if self.pause == False:
            self.playCount += self.step

            # This fakes the speed by repeating n number of frames per cycle
            # i.e. if the animSpeed == 2, then for each cycle the same frame is
            # shown twice before it advances - this can control smoothness or jittery
            # or staccato as needed

            if self.playCount % self.animSpeed == 0:
                self.sliceCol += self.step
                self.frameCount += self.step
                self.animationRotation += self.animationRotationRate

            if self.sliceCol >= self.frameCols:
                self.sliceRow += 1
                self.sliceCol = 0

            if self.sliceRow >= self.frameRows or self.frameCount > self.totalFrames:
                self.sliceRow = 0
                self.sliceCol = 0
                self.frameCount = 0
                self.playCount = 0

        return frameSlice


def loadImage(spriteSheet):
    image = Image.open(spriteSheet, "r")
    image.load()
    imgHeight = image.getbbox()[3]
    return image


def main(run=True):
    global config, workConfig, blocks, simulBlocks, bads
    # gc.enable()

    print("SpriteSheet Player Piece Loaded")
    config.playSpeed = float(workConfig.get("base-parameters", "playSpeed"))

    # managing speed of animation and framerate
    config.directorController = Director(config)

    try:
        config.delay = float(workConfig.get("base-parameters", "delay"))
    except Exception as e:
        print(str(e))
        config.delay = 0.02
    try:
        config.directorController.slotRate = float(workConfig.get("base-parameters", "slotRate"))
    except Exception as e:
        print(str(e))
        print("SHOULD ADJUST TO USE slotRate AS FRAMERATE ")
        config.directorController.slotRate = 0.0

    try:
        config.filterRemapping = (workConfig.getboolean("base-parameters", "filterRemapping"))
        config.filterRemappingProb = float(workConfig.get("base-parameters", "filterRemappingProb"))
        config.filterRemapminHoriSize = int(workConfig.get("base-parameters", "filterRemapminHoriSize"))
        config.filterRemapminVertSize = int(workConfig.get("base-parameters", "filterRemapminVertSize"))
    except Exception as e:
        print(str(e))
        config.filterRemapping = False
        config.filterRemappingProb = 0.0
        config.filterRemapminHoriSize = 24
        config.filterRemapminVertSize = 24

    try:
        config.filterRemapRangeX = int(workConfig.get("base-parameters", "filterRemapRangeX"))
        config.filterRemapRangeY = int(workConfig.get("base-parameters", "filterRemapRangeY"))
    except Exception as e:
        print(str(e))
        config.filterRemapRangeX = config.canvasWidth
        config.filterRemapRangeY = config.canvasHeight

    try:
        if config.usePixelSort == True:
            config.pixelSortProbOn = float(workConfig.get("base-parameters", "pixelSortProbOn"))
            config.pixelSortProbOff = float(workConfig.get("base-parameters", "pixelSortProbOff"))
        else:
            config.pixelSortProbOn = 0
            config.pixelSortProbOff = 0

    except Exception as e:
        print(str(e))
        config.pixelSortProbOn = 0
        config.pixelSortProbOff = 0

    print(bcolors.OKBLUE + "** " + bcolors.BOLD)

    config.canvasImage = Image.new(
        "RGBA", (config.canvasWidth, config.canvasHeight))
    config.canvasDraw = ImageDraw.Draw(config.canvasImage)

    config.allPause = False

    animationNames = workConfig.get("base-parameters", "animations").split(",")
    playTimes = workConfig.get("base-parameters", "playTimes").split(",")
    config.playInOrder = workConfig.getboolean("base-parameters", "playInOrder")
    try:
        # comment: 
        config.drawMoire = workConfig.getboolean("base-parameters", "drawMoire")
        config.drawMoireProb = float(workConfig.get("base-parameters", "drawMoireProb"))
        config.drawMoireProbOff = float(workConfig.get("base-parameters", "drawMoireProbOff"))
    except Exception as e:
        print(str(e))
        config.drawMoire  = False
        config.drawMoireProb = 0 
        config.drawMoireProbOff = 0 

    config.animationNames = animationNames
    config.animations = []
    config.currentAnimationIndex = 0
    config.animationController = Director(config)

    # ----------------------------------------------------------------------------

    for a in config.animationNames:
        aConfig = Holder(config)
        aConfig.name = a

        aConfig.imageToLoad = workConfig.get(a, "i1")
        aConfig.animationWidth = int(workConfig.get(a, "animationWidth"))
        aConfig.animationHeight = int(workConfig.get(a, "animationHeight"))
        aConfig.resizeAnimationToFit = (workConfig.getboolean(a, "resizeAnimationToFit"))
        aConfig.animationImage = Image.new("RGBA", (aConfig.animationWidth, aConfig.animationHeight))
        aConfig.animationImageDraw = ImageDraw.Draw(aConfig.animationImage)

        aConfig.animationArray = []
        aConfig.spriteSheet1 = loadImage(config.path + aConfig.imageToLoad)

        aConfig.randomPlacement = (workConfig.getboolean(a, "randomPlacement"))
        aConfig.fixedPosition = (workConfig.getboolean(a, "fixedPosition"))
        aConfig.frameWidth = int(workConfig.get(a, "frameWidth"))
        aConfig.frameHeight = int(workConfig.get(a, "frameHeight"))
        aConfig.totalFrames = int(workConfig.get(a, "totalFrames"))
        aConfig.frameCols = int(workConfig.get(a, "frameCols"))
        aConfig.frameRows = int(workConfig.get(a, "frameRows"))
        aConfig.sliceWidth = int(workConfig.get(a, "sliceWidth"))
        aConfig.sliceHeight = int(workConfig.get(a, "sliceHeight"))
        aConfig.sliceWidthMin = int(workConfig.get(a, "sliceWidthMin"))
        aConfig.sliceHeightMin = int(workConfig.get(a, "sliceHeightMin"))
        aConfig.numberOfCells = int(workConfig.get(a, "numberOfCells"))
        aConfig.animSpeedMin = int(workConfig.get(a, "animSpeedMin"))
        aConfig.animSpeedMax = int(workConfig.get(a, "animSpeedMax"))
        aConfig.animationRotation = float(workConfig.get(a, "animationRotation"))
        aConfig.animationRotationRateRange = float(workConfig.get(a, "animationRotationRateRange"))
        aConfig.animationRotationJitter = float(workConfig.get(a, "animationRotationJitter"))
        aConfig.animationXOffset = int(workConfig.get(a, "animationXOffset"))
        aConfig.animationYOffset = int(workConfig.get(a, "animationYOffset"))
        aConfig.randomPlacemnetXRange = int(workConfig.get(a, "randomPlacemnetXRange"))
        aConfig.randomPlacemnetYRange = int(workConfig.get(a, "randomPlacemnetYRange"))

        aConfig.bg_minHue = int(workConfig.get(a, "bg_minHue"))
        aConfig.bg_maxHue = int(workConfig.get(a, "bg_maxHue"))
        aConfig.bg_minSaturation = float(workConfig.get(a, "bg_minSaturation"))
        aConfig.bg_maxSaturation = float(workConfig.get(a, "bg_maxSaturation"))
        aConfig.bg_minValue = float(workConfig.get(a, "bg_minValue"))
        aConfig.bg_maxValue = float(workConfig.get(a, "bg_maxValue"))
        aConfig.bg_dropHueMinValue = float(workConfig.get(a, "bg_dropHueMinValue"))
        aConfig.bg_dropHueMaxValue = float(workConfig.get(a, "bg_dropHueMaxValue"))
        aConfig.bg_alpha = int(workConfig.get(a, "bg_alpha"))

        aConfig.backgroundColorChangeProb = float(workConfig.get(a, "backgroundColorChangeProb"))
        aConfig.changeAnimProb = float(workConfig.get(a, "changeAnimProb"))
        aConfig.pauseProb = float(workConfig.get(a, "pauseProb"))
        aConfig.unPauseProb = float(workConfig.get(a, "unPauseProb"))
        aConfig.freezeGlitchProb = float(workConfig.get(a, "freezeGlitchProb"))
        aConfig.unFreezeGlitchProb = float(workConfig.get(a, "unFreezeGlitchProb"))

        aConfig.glitching = True

        aConfig.imageGlitchDisplacementHorizontal = int(workConfig.get(a, "imageGlitchDisplacementHorizontal"))
        aConfig.imageGlitchDisplacementVertical = int(workConfig.get(a, "imageGlitchDisplacementVertical"))

        # Sets up color transitions
        aConfig.colOverlay = coloroverlay.ColorOverlay()
        aConfig.colOverlay.randomSteps = True
        aConfig.colOverlay.timeTrigger = True
        aConfig.colOverlay.tLimitBase = 5
        aConfig.colOverlay.steps = 10

        aConfig.colOverlay.maxBrightness = config.brightness
        aConfig.colOverlay.minSaturation = aConfig.bg_minSaturation
        aConfig.colOverlay.maxSaturation = aConfig.bg_maxSaturation
        aConfig.colOverlay.minValue = aConfig.bg_minValue
        aConfig.colOverlay.maxValue = aConfig.bg_maxValue
        aConfig.colOverlay.minHue = aConfig.bg_minHue
        aConfig.colOverlay.maxHue = aConfig.bg_maxHue
        aConfig.colOverlay.dropHueMin = aConfig.bg_dropHueMinValue
        aConfig.colOverlay.dropHueMax = aConfig.bg_dropHueMaxValue
        
        aConfig.colOverlay.colorTransitionSetup()

        for i in range(0, aConfig.numberOfCells):
            anim = spriteAnimation(config)

            anim.frameWidth = aConfig.frameWidth
            anim.frameHeight = aConfig.frameHeight
            anim.totalFrames = aConfig.totalFrames
            anim.frameCols = aConfig.frameCols
            anim.frameRows = aConfig.frameRows
            anim.animSpeedMin = aConfig.animSpeedMin
            anim.animSpeedMax = aConfig.animSpeedMax
            anim.animationWidth = aConfig.animationWidth
            anim.animationHeight = aConfig.animationHeight
            anim.resizeAnimationToFit = aConfig.resizeAnimationToFit
            anim.randomPlacement = aConfig.randomPlacement

            reConfigAnimationCell(anim, aConfig)
            aConfig.animationArray.append(anim)

        aConfig.imagePath = config.path + "/assets/imgs/"
        aConfig.imageList = [aConfig.imageToLoad]

        config.animations.append(aConfig)

    try:
        config.lastOverLayColorRange = list(map(lambda x: float(x), workConfig.get("base-parameters", "lastOverLayColorRange").split(",")))
        config.lastOverlayAlphaRange = tuple(map(lambda x: int(x), workConfig.get("base-parameters", "lastOverlayAlphaRange").split(",")))
        config.useLastOverlay = workConfig.getboolean("base-parameters", "forceLastOverlay")
        config.useLastOverlayProb = float(workConfig.get("base-parameters", "useLastOverlayProb"))
        config.lastOverlayBox = tuple(map(lambda x: int(x), workConfig.get("base-parameters", "lastOverlayBox").split(",")))
        config.renderImageFullOverlay = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
        config.renderDrawOver = ImageDraw.Draw(config.renderImageFullOverlay)
        config.lastOverlayBlur = float(workConfig.get("base-parameters", "lastOverlayBlur"))
        config.lastOverlayFill = (0, 0, 0, 0)
        # config.lastOverlayFill = tuple(	map(lambda x: int(x), workConfig.get("base-parameters", "lastOverlayFill").split(",")))
    except Exception as e:
        print(str(e))
        config.lastOverlayBox = (0, 0, 64, 32)
        config.lastOverlayFill = (0, 0, 0, 0)
        config.useLastOverlay = False
        config.useLastOverlayProb = 0
  
  
    config.playTimes = tuple(map(lambda x: int(int(x)), playTimes))
    config.animationController.delay = 1.0
    config.animationController.slotRate = config.playTimes[0]

    # THIS IS USED AS WAY TO MOCKUP A CONFIGURATION OF RECTANGULAR PANELS
    panelDrawing.mockupBlock(config, workConfig)
    # Need to add something like this at final render call  as well
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


    config.debugSelf()

    # print(config.__dict__)
    if run:
        runWork()


def glitchBox():

    global config
    currentAnimation = config.animations[0]
    apparentWidth = config.canvasImage.size[0]
    apparentHeight = config.canvasImage.size[1]
    apparentWidth = currentAnimation.animationWidth
    apparentHeight = currentAnimation.animationWidth
    # currentAnimation.imageGlitchDisplacementVertical = 32
    # currentAnimation.imageGlitchDisplacementHorizontal = 32

    dx = round(random.uniform(-currentAnimation.imageGlitchDisplacementHorizontal,currentAnimation.imageGlitchDisplacementHorizontal))
    dy = round(random.uniform(-currentAnimation.imageGlitchDisplacementVertical,currentAnimation.imageGlitchDisplacementVertical))

    sectionWidth = round(random.uniform(2, apparentWidth - dx))
    sectionHeight = round(random.uniform(2, apparentHeight - dy))

    # 95% of the time they dance together as mirrors
    try:
        if random.random() < 0.97:
            cx = dx + sectionWidth
            cy = dy + sectionHeight

            if cx < 0:
                cx = 32
            if cy < 0:
                cy = 32
            cp1 = currentAnimation.animationImage.crop((0, 0, cx, cy))
            currentAnimation.animationImage.paste(cp1, (round(dx), round(dy)))
        # comment:
    except Exception as e:
        print(str(e))
        print(dx + sectionWidth, dy + sectionHeight)
    # end try


def reConfigAnimationCell(anim, aConfig):
    global config

    anim.animSpeed = round(random.uniform(anim.animSpeedMin, anim.animSpeedMax))
    anim.animationRotation = aConfig.animationRotation + random.uniform(-aConfig.animationRotationJitter,aConfig.animationRotationJitter)

    if aConfig.animationRotation != 0:
        maxDim = max(anim.frameHeight, anim.frameWidth)
        anim.imageFrame = Image.new("RGBA", (maxDim, maxDim))

    anim.image = aConfig.spriteSheet1

    # Placement on the canvas
    if anim.randomPlacement == True:
        anim.xPos = round(random.random() * aConfig.randomPlacemnetXRange)
        anim.yPos = round(random.random() * aConfig.randomPlacemnetYRange)

    # if config.fixedPosition == True:
    #     anim.xPos = config.animationXOffset
    #     anim.yPos = config.animationYOffset

    # deprecating for now in favor or repeat frames per cycle etc
    # anim.step = round(random.uniform(1,2))

    # random starting point in animation
    anim.sliceCol = round(random.random() * anim.frameCols)
    anim.sliceRow = round(random.random() * anim.frameRows)
    anim.frameCount = anim.sliceCol + anim.sliceRow * aConfig.frameCols

    # random slicing of section to display
    anim.sliceXOffset = 0  # round(random.random() * anim.frameWidth)
    anim.sliceYOffset = 0  # round(random.random() * anim.frameHeight)
    anim.sliceWidth = round(random.uniform(aConfig.sliceWidthMin, aConfig.sliceWidth))
    anim.sliceHeight = round(random.uniform(aConfig.sliceHeightMin, aConfig.sliceHeight))

    if anim.sliceWidth + anim.sliceXOffset > anim.frameWidth:anim.sliceWidth = anim.frameWidth - anim.sliceXOffset

    if anim.sliceHeight + anim.sliceYOffset > anim.frameHeight:anim.sliceHeight = anim.frameHeight - anim.sliceYOffset

    anim.animationRotationRate = random.uniform(-aConfig.animationRotationRateRange, aConfig.animationRotationRateRange)


def runWork():
    print(bcolors.OKGREEN + "** " + bcolors.BOLD)
    print("Running spritesheet2.py")
    print(bcolors.ENDC)
    # gc.enable()
    while config.isRunning == True:
        config.directorController.checkTime()
        if config.directorController.advance == True:
            iterate()
            time.sleep(config.delay)
        if config.standAlone == False:
            config.callBack()


def iterate(n=0):
    global config, blocks
    global xPos, yPos

    currentAnimation = config.animations[config.currentAnimationIndex]
    currentAnimation.colOverlay.stepTransition()
    bgColor = currentAnimation.colOverlay.currentColor
    # bgColor = currentAnimation.bgBackGroundEndColor
    # config.bg_alpha = 255
    # config.canvasDraw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=(
    #         bgColor[0], bgColor[1], bgColor[2], currentAnimation.bg_alpha))

    config.canvasImage.paste(currentAnimation.animationImage, (0,0), currentAnimation.animationImage)

    if config.allPause == True:
        if currentAnimation.glitching == True:
            glitchBox()
            if random.random() < currentAnimation.freezeGlitchProb:
                currentAnimation.glitching = False
    else:
        
        # config.canvasDraw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=(bgColor[0], bgColor[1], bgColor[2], config.bg_alpha))
        for anim in currentAnimation.animationArray:
            bgColor = (round(config.brightness * bgColor[0]), round(config.brightness * bgColor[1]), round(config.brightness * bgColor[2]), currentAnimation.bg_alpha)
            currentAnimation.animationImageDraw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=bgColor)
            if config.drawMoire == True : 
                c1  = (round(config.brightness * 150),round(config.brightness * 50),round(config.brightness * 0),150)
                for ii in range (0,2):
                    xc = ii * 20 + 100
                    yc = ii * 20 + 100
                    for i in range(0, 80) :
                        w = 400 - i * 6
                        x0 = xc - w / 2
                        y0 = yc - w / 2
                        x1 = xc + w / 2
                        y1 = yc + w / 2
                        
                        if x1 < x0 :
                            x1 = x0 +1
                        if y1 < y0 :
                            y1 = y0 +1
                        currentAnimation.animationImageDraw.ellipse((x0, y0, x1, y1), fill=None, outline=c1)
            try:
                currentAnimation.animationImage.paste(anim.nextFrame(), (anim.xPos + currentAnimation.animationXOffset, anim.yPos + currentAnimation.animationYOffset), anim.nextFrame())
                # config.animationImage.paste(anim.nextFrame(), (0, 0), anim.nextFrame())
                # comment:
            except Exception as e:
                print(str(e))
            # end try
            anim.pause = config.allPause

            if random.random() < currentAnimation.changeAnimProb:
                reConfigAnimationCell(anim, currentAnimation)
                
                
    if random.random() < config.useLastOverlayProb and config.useLastOverlay == True:
            # config.useLastOverlay = False if config.useLastOverlay == True  else True
            # print("lastOVerlay")
            xPos = config.tileSizeWidth * math.floor(random.uniform(0, config.cols))
            yPos = config.tileSizeHeight * math.floor(random.uniform(0, config.rows))
            config.lastOverlayBox = (xPos, yPos, xPos + config.tileSizeWidth, yPos + config.tileSizeHeight)

            cR = config.lastOverLayColorRange
            # print(cR)
            lastOverlayFill = colorutils.getRandomColorHSV(cR[0],cR[1],cR[2],cR[3],cR[4],cR[5],cR[6],cR[7])
            # print(lastOverlayFill)
            config.lastOverlayFill = (round(config.brightness * lastOverlayFill[0]), round(config.brightness * lastOverlayFill[1]), round(config.brightness * lastOverlayFill[2]), round(random.uniform(config.lastOverlayAlphaRange[0], config.lastOverlayAlphaRange[1])))
            #config.lastOverlayFill = (10, 0, 0, round(random.uniform(5, 50)))
            
            currentAnimation.animationImageDraw.rectangle(config.lastOverlayBox, fill= config.lastOverlayFill)


    ########### RENDERING AS A MOCKUP OR AS REAL ###########
    if config.useDrawingPoints == True:
        config.panelDrawing.canvasToUse = config.f.blendedImage
        config.panelDrawing.render()
    else:
        # config.render(config.image, 0, 0)
        config.render(config.canvasImage, 0, 0,
                      config.canvasWidth, config.canvasHeight)

    if random.random() < config.drawMoireProb:
        config.drawMoire = True
    if random.random() < config.drawMoireProbOff:
        config.drawMoire = False
        
        
    if random.random() < config.filterRemappingProb:
        if random.random() < .5:
            config.filterRemapping == False
        else:
            config.filterRemapping == True

    if random.random() < config.filterRemappingProb:
        if config.useFilters == True and config.filterRemapping == True:
            config.filterRemap = True
            # new version  more control but may require previous pieces to be re-worked
            startX = round(random.uniform(0, config.filterRemapRangeX))
            startY = round(random.uniform(0, config.filterRemapRangeY))
            endX = round(random.uniform(8, config.filterRemapminHoriSize))
            endY = round(random.uniform(8, config.filterRemapminVertSize))
            config.remapImageBlockSection = [
                startX, startY, startX + endX, startY + endY]
            config.remapImageBlockDestination = [startX, startY]
            # print("swapping" + str(config.remapImageBlockSection))

    if random.random() < config.pixelSortProbOn:
        config.usePixelSort = True

    if random.random() < config.pixelSortProbOff:
        config.usePixelSort = False

    if random.random() < currentAnimation.pauseProb:
        config.allPause = True

    if config.allPause == True and random.random() < currentAnimation.unFreezeGlitchProb:
        currentAnimation.glitching = True

    if config.allPause == True and random.random() < currentAnimation.unPauseProb:
        config.allPause = False

    if random.random() < currentAnimation.backgroundColorChangeProb:
        # config.bgBackGroundColor = config.bgBackGroundEndColor
        currentAnimation.bgBackGroundEndColor = colorutils.getRandomColorHSV(
            currentAnimation.bg_minHue, currentAnimation.bg_maxHue,
            currentAnimation.bg_minSaturation, currentAnimation.bg_maxSaturation,
            currentAnimation.bg_minValue, currentAnimation.bg_maxValue,
            currentAnimation.bg_dropHueMinValue, currentAnimation.bg_dropHueMaxValue, 255, config.brightness)
        
    if random.random() < currentAnimation.backgroundColorChangeProb/2.0:
        bgColor = currentAnimation.colOverlay.currentColor
        config.canvasDraw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=(
            bgColor[0], bgColor[1], bgColor[2], currentAnimation.bg_alpha))

    config.animationController.checkTime()
    if config.animationController.advance == True:
        if config.playInOrder == True:
            config.currentAnimationIndex += 1
            if config.currentAnimationIndex >= len(config.animations):
                config.currentAnimationIndex = 0
        else :
            choice = math.floor(random.uniform(0,len(config.animations)))
            config.currentAnimationIndex = choice
        config.animationController.slotRate = config.playTimes[config.currentAnimationIndex]
        
        config.animationController.slotRate = round(random.uniform(5,20))


def callBack():
    global config
    print("CALLBACK")
    return True


#####################
