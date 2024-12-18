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


# config.canvasImage is the final layer or image to be rendered
# everything else gets pasted on to this image layer
# the filtering happens to this canvasImage as well
#----------------------------------------------------##----------------------------------------------------#

class Holder:
    def __init__(self, config):
        self.config = config

#----------------------------------------------------##----------------------------------------------------#
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

#----------------------------------------------------##----------------------------------------------------#
class spriteAnimation():

    frameWidth = 128
    frameHeight = 128
    totalFrames = 24
    frameCols = 4
    frameRows = 5
    sliceCol = 0
    sliceRow = 0

    sliceWidth = 128
    sliceHeight = 128

    sliceXOffset = 0
    sliceYOffset = 0

    startFrame = 0
    endFrame = 24
    currentFrame = 0
    playCount = 0
    step = 1
    animSpeedMin = 2
    animSpeedMax = 4
    
    direction = 1
    reversing = False

    animationRotation = 0
    animationRotationRate = 0

    randomPlacement = True
    resizeAnimationToFit = False
    animationWidth = 256
    animationHeight = 256
    
    name= "default"

    xPos = 0
    yPos = 0

    frameArray = []

    pause = False

    def __init__(self, config):
        self.config = config
        self.imageFrame = Image.new("RGBA", (self.frameWidth, self.frameHeight))

    #----------------------------------------------------##----------------------------------------------------#
    def prepSlices(self):
        frame = 0
        self.frameArray = []
        for r in range(0, self.frameRows):
            for c in range(0, self.frameCols):
                if frame < self.totalFrames:
                    xPos = c * self.frameWidth + self.sliceXOffset
                    yPos = r * self.frameHeight + self.sliceYOffset

                    frameSlice = self.image.crop(
                        (xPos, yPos, xPos + self.sliceWidth, yPos + self.sliceHeight))
                    
                    if self.resizeAnimationToFit == True:
                        frameSlice = frameSlice.resize((self.animationWidth,self.animationHeight))
            
                    if self.animationRotation != 0:
                        frameSlice = frameSlice.rotate(
                            self.animationRotation, 0, 1)

                    if self.config.brightness != 1.0:
                        enhancer = ImageEnhance.Brightness(frameSlice)
                        frameSlice = enhancer.enhance(self.config.brightness)
                    self.frameArray.append(frameSlice)
                    frame += 1
                    

        print("------------  ")
        print(self.name + " prep done")
        print("Number of Frames:" + str(len(self.frameArray)))
        print("------------\n")
        # exit()
    #----------------------------------------------------##----------------------------------------------------#
    def getNextFrame(self):
        # img = self.frameArray[self.currentFrame]
        if self.pause == False :
            self.playCount += self.step
            if self.reversing == True :
                if self.playCount % self.animSpeed == 0:
                        self.currentFrame += self.direction
                    
                if self.currentFrame >= self.endFrame :
                    self.direction *= -1
                    self.currentFrame = self.endFrame - 1
                    
                    # if self.direction > 0 :
                    #     self.currentFrame = self.endFrame
                    
                if self.currentFrame < self.startFrame :
                    self.direction *= -1   
                    self.currentFrame = self.startFrame 
                    # if self.direction < 0 :
                    #     self.currentFrame = self.startFrame
            else :
                if self.playCount % self.animSpeed == 0:
                    self.currentFrame += 1
                    if self.currentFrame >= self.endFrame :
                        self.currentFrame = self.startFrame

    #----------------------------------------------------##----------------------------------------------------#
    def nextFrameImg(self) :
        return self.frameArray[self.currentFrame]
    
#----------------------------------------------------##----------------------------------------------------#
def loadImage(spriteSheet):
    image = Image.open(spriteSheet, "r")
    image.load()
    imgHeight = image.getbbox()[3]
    return image

#----------------------------------------------------##----------------------------------------------------#
def main(run=True):
    global config, workConfig, blocks, simulBlocks, bads
    # gc.enable()

    print("SpriteSheet Player Piece Loaded")
    # config.playSpeed = float(workConfig.get("base-parameters", "playSpeed"))

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

    config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.canvasDraw = ImageDraw.Draw(config.canvasImage)
    
    config.overLayLayer = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.overlayDraw = ImageDraw.Draw(config.overLayLayer)

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
        
        
    try:
        # comment: 
        config.moireXPos = int(workConfig.get("base-parameters", "moireXPos"))
        config.moireYPos = int(workConfig.get("base-parameters", "moireYPos"))
        config.moireXDistance = int(workConfig.get("base-parameters", "moireXDistance"))
        config.moireYDistance = int(workConfig.get("base-parameters", "moireYDistance"))
    except Exception as e:
        print(str(e))
        config.moireXPos = 100
        config.moireYPos = 100
        config.moireXDistance = 100
        config.moireYDistance = 100
        
        
    try:
        # comment: 
        config.setMoireColor = workConfig.getboolean("base-parameters", "setMoireColor")
        config.moireColorAltProb = float(workConfig.get("base-parameters", "moireColorAltProb"))
        config.moireColor = tuple(map(lambda x: int(x), workConfig.get("base-parameters", "moireColor").split(",")))
        config.moireColorAlt = tuple(map(lambda x: int(x), workConfig.get("base-parameters", "moireColorAlt").split(",")))

    except Exception as e:
        print(str(e))
        config.setMoireColor  = False
        
    

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
        aConfig.animationRotation = float(workConfig.get(a, "animationRotation"))
        aConfig.animationImage = Image.new("RGBA", (aConfig.animationWidth, aConfig.animationHeight))
        
        if abs(aConfig.animationRotation) == 90 :
            aConfig.animationImage = Image.new("RGBA", (aConfig.animationHeight, aConfig.animationWidth))
            
        
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
        aConfig.animSpeedMin = float(workConfig.get(a, "animSpeedMin"))
        aConfig.animSpeedMax = float(workConfig.get(a, "animSpeedMax"))
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
        aConfig.bg_alpha = 0
        aConfig.bg_alpha_max = int(workConfig.get(a, "bg_alpha"))

        aConfig.backgroundColorChangeProb = float(workConfig.get(a, "backgroundColorChangeProb"))
        aConfig.changeAnimProb = float(workConfig.get(a, "changeAnimProb"))
        aConfig.pauseProb = float(workConfig.get(a, "pauseProb"))
        aConfig.unPauseProb = float(workConfig.get(a, "unPauseProb"))
        aConfig.freezeGlitchProb = float(workConfig.get(a, "freezeGlitchProb"))
        aConfig.unFreezeGlitchProb = float(workConfig.get(a, "unFreezeGlitchProb"))
        try:
            # comment: 
            aConfig.pauseOnFirstFrameProb = float(workConfig.get(a, "pauseOnFirstFrameProb"))
            aConfig.pauseOnLastFrameProb = float(workConfig.get(a, "pauseOnLastFrameProb"))
        except Exception as e:
            print(str(e))
            aConfig.pauseOnFirstFrameProb = 0.0
            aConfig.pauseOnLastFrameProb = 0.0
        try:
            # comment: 
            aConfig.reversing = workConfig.getboolean(a, "reversing")
        except Exception as e:
            print(str(e))
            aConfig.reversing = False

        
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
        anim.reversing = aConfig.reversing
        anim.currentFrame = 0
        anim.name = aConfig.name

        aConfig.imagePath = config.path + "/assets/imgs/"
        aConfig.imageList = [aConfig.imageToLoad]

        config.animations.append(aConfig)
        reConfigAnimationCell(anim, aConfig)
        anim.prepSlices()
        # aConfig.animationArray.append(anim)
        aConfig.anim = anim

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
        config.clearLastOverlayProb = 0
        
    config.compositionModeChangeProb = float(workConfig.get("base-parameters", "compositionModeChangeProb"))
    config.compositionMode = 1
    
    # if config.compositionMode == 0 :
    #     config.overlayDraw.rectangle((0,0,config.canvasWidth, config.canvasHeight), fill= (0,0,0,255))
    
    try:
        config.animationFrameXOffset = int(workConfig.get("base-parameters", "animationFrameXOffset"))
        config.animationFrameYOffset = int(workConfig.get("base-parameters", "animationFrameYOffset"))
    except Exception as e:
        print(str(e))
        config.animationFrameXOffset = 0
        config.animationFrameYOffset = 0
    # end try
  
    try:
        config.clearLastOverlayProb = float(workConfig.get("base-parameters", "clearLastOverlayProb"))
    except Exception as e:
        print(str(e))
        config.clearLastOverlayProb = 0
  
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


    # config.debugSelf()

    # print(config.__dict__)
    if run:
        runWork()

#----------------------------------------------------##----------------------------------------------------#
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

#----------------------------------------------------##----------------------------------------------------#
def animationBackGroundFadeIn() :
    currentAnimation = config.animations[config.currentAnimationIndex]
    if currentAnimation.bg_alpha <= currentAnimation.bg_alpha_max :
        currentAnimation.bg_alpha += 2

#----------------------------------------------------##----------------------------------------------------#
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
    anim.startFrame = anim.sliceCol + anim.sliceRow * aConfig.frameCols
    anim.startFrame = 0
    anim.endFrame = anim.totalFrames
    anim.playCount = 0
    anim.currentFrame = 0

    # random slicing of section to display
    anim.sliceXOffset = 0  # round(random.random() * anim.frameWidth)
    anim.sliceYOffset = 0  # round(random.random() * anim.frameHeight)
    anim.sliceWidth = round(random.uniform(aConfig.sliceWidthMin, aConfig.sliceWidth))
    anim.sliceHeight = round(random.uniform(aConfig.sliceHeightMin, aConfig.sliceHeight))

    if anim.sliceWidth + anim.sliceXOffset > anim.frameWidth:anim.sliceWidth = anim.frameWidth - anim.sliceXOffset

    if anim.sliceHeight + anim.sliceYOffset > anim.frameHeight:anim.sliceHeight = anim.frameHeight - anim.sliceYOffset

    anim.animationRotationRate = random.uniform(-aConfig.animationRotationRateRange, aConfig.animationRotationRateRange)

#----------------------------------------------------##----------------------------------------------------#
def filterRemapCall(ovrd=False) :
        config.filterRemap = True
        # new version  more control but may require previous pieces to be re-worked
        startX = round(random.uniform(0, config.filterRemapRangeX))
        startY = round(random.uniform(0, config.filterRemapRangeY))
        endX = round(random.uniform(8, config.filterRemapminHoriSize))
        endY = round(random.uniform(8, config.filterRemapminVertSize))
        
        if ovrd == True :
            startX = 0
            startY = 0
            endX = 200
            endY = 200
        config.remapImageBlockSection = [
            startX, startY, startX + endX, startY + endY]
        config.remapImageBlockDestination = [startX, startY]
        # print("swapping" + str(config.remapImageBlockSection))

#----------------------------------------------------##----------------------------------------------------#
def runWork():
    print(bcolors.OKGREEN + "** " + bcolors.BOLD)
    print("Running spritesheet3.py")
    print(bcolors.ENDC)
    # gc.enable()
    while config.isRunning == True:
        config.directorController.checkTime()
        if config.directorController.advance == True:
            iterate()
            time.sleep(config.delay)
        if config.standAlone == False:
            config.callBack()
            
#----------------------------------------------------##----------------------------------------------------#
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

    config.canvasImage.paste(currentAnimation.animationImage, (config.animationFrameXOffset,config.animationFrameYOffset), currentAnimation.animationImage)
    animationBackGroundFadeIn()

    if config.allPause == True:
        if currentAnimation.glitching == True:
            glitchBox()
            if random.random() < currentAnimation.freezeGlitchProb:
                currentAnimation.glitching = False
    else:
        
        # config.canvasDraw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=(bgColor[0], bgColor[1], bgColor[2], config.bg_alpha))
        animationBackGroundFadeIn()
        anim = currentAnimation.anim
        bgColor = (round(config.brightness * bgColor[0]), round(config.brightness * bgColor[1]), round(config.brightness * bgColor[2]), currentAnimation.bg_alpha)
        
        currentAnimation.animationImageDraw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill = bgColor)
        
        if config.drawMoire == True : 
            c1  = (round(config.brightness * 150),round(config.brightness * 50),round(config.brightness * 0),150)
            
            if config.setMoireColor == True :
                c1 = config.moireColor
                
                if random.random() < config.moireColorAltProb :
                    c1 = config.moireColorAlt

            for ii in range (0,2):
                xc = ii * config.moireXDistance + config.moireXPos
                yc = ii * config.moireYDistance + config.moireYPos
                for i in range(0, 180) :
                    w = 800 - i * 6
                    x0 = xc - w / 2
                    y0 = yc - w / 2
                    x1 = xc + w / 2
                    y1 = yc + w / 2
                    
                    if x1 < x0 :
                        x1 = x0 +1
                    if y1 < y0 :
                        y1 = y0 +1
                    currentAnimation.animationImageDraw.ellipse((x0, y0, x1, y1), fill=None, outline=c1)
        
        tempImageRef  = anim.nextFrameImg()
        currentAnimation.animationImage.paste(tempImageRef, (anim.xPos + currentAnimation.animationXOffset, anim.yPos + currentAnimation.animationYOffset), tempImageRef)

        if config.allPause == False :
            
            # doing this 3 times because this was how the v.2 version inadvertently did it - my bad - but also to 
            # improve the smoothness and the way the animation speed values work - i.e. they affect the speed at 
            # at a more granular way
            
            anim.getNextFrame()
            anim.getNextFrame()
            anim.getNextFrame()
            
            if random.random() < currentAnimation.pauseOnFirstFrameProb and anim.currentFrame == anim.startFrame:
                # print("paused at start")
                anim.pause = True
                config.allPause = True
    
            # print(anim.currentFrame,anim.endFrame-1)
            if random.random() < currentAnimation.pauseOnLastFrameProb and anim.currentFrame == anim.endFrame-1:
                # print("paused at end")
                config.allPause = True
                anim.pause = True
                
            if (anim.pause == True or config.allPause == True) and random.random() < currentAnimation.unPauseProb :
                # print("releasing animation")
                anim.pause = False
                config.allPause = False
                
            if random.random() < currentAnimation.pauseProb:
                # print("pausing at frame:" + str(anim.currentFrame) )
                anim.pause = True
                config.allPause = True
                if random.random() < .5 :
                    anim.direction *= -1

                
        anim.pause = config.allPause

        if random.random() < currentAnimation.changeAnimProb:      
            reConfigAnimationCell(anim, currentAnimation)
                
    compositeFinal = config.canvasImage
    # Draws the colored tiles over the animation image - 
    # Note first versions drew this over the animation image but on 10-29-2023 I
    # tested drawing it over the final image layer canvasImage instead - not sure
    # if it really changes anything though
    
    if random.random() < config.useLastOverlayProb and config.useLastOverlay == True and config.allPause == False:
        # config.useLastOverlay = False if config.useLastOverlay == True  else True
        print("lastOVerlay")
        xPos = config.tileSizeWidth * math.floor(random.uniform(0, config.cols))
        yPos = config.tileSizeHeight * math.floor(random.uniform(0, config.rows))
        if random.random() < config.clearLastOverlayProb :
            print("clear lastOVerlay")
            xPos = yPos = 0
            config.lastOverlayBox = (xPos, yPos, xPos + config.canvasWidth, yPos + config.canvasHeight)
            config.lastOverlayFill = (0,0,0,0)
            config.overLayLayer = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
            config.overlayDraw = ImageDraw.Draw(config.overLayLayer)
            
            if config.compositionMode == 0 :
                config.overlayDraw.rectangle((0,0,config.canvasWidth, config.canvasHeight), fill= (255,255,255,255))
                
                
        else :
            config.lastOverlayBox = (xPos, yPos, xPos + config.tileSizeWidth, yPos + config.tileSizeHeight)
            cR = config.lastOverLayColorRange
            # print(cR)
            lastOverlayFill = colorutils.getRandomColorHSV(cR[0],cR[1],cR[2],cR[3],cR[4],cR[5],cR[6],cR[7])
            # print(lastOverlayFill)
            config.lastOverlayFill = (round(config.brightness * lastOverlayFill[0]), round(config.brightness * lastOverlayFill[1]), round(config.brightness * lastOverlayFill[2]), round(random.uniform(config.lastOverlayAlphaRange[0], config.lastOverlayAlphaRange[1])))
            #config.lastOverlayFill = (10, 0, 0, round(random.uniform(5, 50)))
        
        config.overlayDraw.rectangle(config.lastOverlayBox, fill= config.lastOverlayFill)
        # do not delete - see note above
        #currentAnimation.animationImageDraw.rectangle(config.lastOverlayBox, fill= config.lastOverlayFill)
        #config.canvasDraw.rectangle(config.lastOverlayBox, fill= config.lastOverlayFill)
        
    if config.compositionMode == 0 :
        compositeFinal = ImageChops.screen( config.overLayLayer, config.canvasImage)
        
    if config.compositionMode == 1 :
        compositeFinal = ImageChops.add( config.overLayLayer, config.canvasImage,.65, 1)

    if config.compositionMode == 2 :
        compositeFinal = ImageChops.soft_light(config.canvasImage, config.overLayLayer)

    if config.compositionMode == 3 :
        compositeFinal = ImageChops.overlay(config.overLayLayer, config.canvasImage)




    ########### RENDERING AS A MOCKUP OR AS REAL ###########
    if config.useDrawingPoints == True:
        config.panelDrawing.canvasToUse = config.f.blendedImage
        config.panelDrawing.render()
    else:
        # config.render(config.image, 0, 0)
        config.render(compositeFinal, 0, 0, config.canvasWidth, config.canvasHeight)

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
            filterRemapCall()


    if random.random() < config.pixelSortProbOn:
        config.usePixelSort = True

    if random.random() < config.pixelSortProbOff:
        config.usePixelSort = False

    # if random.random() < currentAnimation.pauseProb:
    #     config.allPause = True
    

    if config.allPause == True and random.random() < currentAnimation.unFreezeGlitchProb:
        currentAnimation.glitching = True

    if config.allPause == True and random.random() < currentAnimation.unPauseProb:
        # print("un-pausing")
        config.allPause = False

    # if random.random() < currentAnimation.backgroundColorChangeProb:
    #     # config.bgBackGroundColor = config.bgBackGroundEndColor
    #     print("Setting new BG Color for animation")
    #     # currentAnimation.bgBackGroundEndColor = colorutils.getRandomColorHSV(
    #     #     currentAnimation.bg_minHue, currentAnimation.bg_maxHue,
    #     #     currentAnimation.bg_minSaturation, currentAnimation.bg_maxSaturation,
    #     #     currentAnimation.bg_minValue, currentAnimation.bg_maxValue,
    #     #     currentAnimation.bg_dropHueMinValue, currentAnimation.bg_dropHueMaxValue, 10, config.brightness)
        
    # if random.random() < currentAnimation.backgroundColorChangeProb/2.0:
    #     print("Clearing the canvas")
    #     bgColor = currentAnimation.colOverlay.currentColor
    #     config.canvasDraw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=(
    #         round(config.brightness * bgColor[0]), round(config.brightness * bgColor[1]), round(config.brightness * bgColor[2]), currentAnimation.bg_alpha))

    if random.random() < config.compositionModeChangeProb :
        config.compositionMode = math.floor(random.uniform(0,4))
        print("New composition mode: " + str(config.compositionMode))
        if config.compositionMode == 0 :
            config.overlayDraw.rectangle((0,0,config.canvasWidth, config.canvasHeight), fill= (0,0,0,255))
        if config.compositionMode == 1 :
            config.overlayDraw.rectangle((0,0,config.canvasWidth, config.canvasHeight), fill= (0,0,0,0))
        if config.compositionMode == 2 :
            config.overlayDraw.rectangle((0,0,config.canvasWidth, config.canvasHeight), fill= (0,0,0,0))
        if config.compositionMode == 3 :
            config.overlayDraw.rectangle((0,0,config.canvasWidth, config.canvasHeight), fill= (0,0,0,0))
        
        
        
    
    config.animationController.checkTime()
    if config.animationController.advance == True:
        currentAnimation.glitching = False
        
        if config.playInOrder == True:
            config.currentAnimationIndex += 1
            if config.currentAnimationIndex >= len(config.animations):
                config.currentAnimationIndex = 0
            print("Next Animation : " + str(config.animations[config.currentAnimationIndex].name))
        else :
            choice = math.floor(random.uniform(0,len(config.animations)))
            config.currentAnimationIndex = choice
            print("Next Animation : " + str(config.animations[choice].name))
        
        config.animationController.slotRate = config.playTimes[config.currentAnimationIndex]
        
        currentAnimation = config.animations[config.currentAnimationIndex]
        config.animationController.slotRate = round(random.uniform(currentAnimation.animSpeedMin,currentAnimation.animSpeedMax))
        

        tempTest = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
        tempTestDraw = ImageDraw.Draw(tempTest)
        xPos  = round(random.uniform(0,config.canvasWidth))
        yPos  = round(random.uniform(0,config.canvasHeight))
        xPos2 = round(random.uniform(xPos,config.canvasWidth))
        yPos2 = round(random.uniform(yPos,config.canvasHeight))
        tempTestDraw.rectangle( (xPos,yPos,xPos2,yPos2), fill= (0,255,0,155))
        
        # currentAnimation.anim.imageFrame.paste(tempTest,(0,0), tempTest)
        # config.canvasImage.paste(tempTest,(0,0), tempTest)
        
        currentAnimation.bg_alpha = 10
        config.allPause = False
        currentAnimation.anim.currentFrame = 0
        # config.canvasImage.paste(currentAnimation.animationImage, (0,0), currentAnimation.animationImage)
        # config.render(config.canvasImage, 0, 0, config.canvasWidth, config.canvasHeight)
        
        


        
#----------------------------------------------------##----------------------------------------------------#
def callBack():
    global config
    print("CALLBACK")
    return True


#####################
