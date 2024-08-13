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

                    if config.brightness != 1.0:
                        enhancer = ImageEnhance.Brightness(frameSlice)
                        frameSlice = enhancer.enhance(config.brightness)
                    self.frameArray.append(frameSlice)
                    frame += 1

    def nextFrame(self):
        xPos = self.sliceCol * self.frameWidth + self.sliceXOffset
        yPos = self.sliceRow * self.frameHeight + self.sliceYOffset

        frameSlice = self.image.crop(
            (xPos, yPos, xPos + self.sliceWidth, yPos + self.sliceHeight))

        if self.resizeAnimationToFit == True:
            frameSlice = frameSlice.resize(
                ( self.animationWidth, self.animationHeight))

        if self.animationRotation != 0:
            frameSlice = frameSlice.rotate(self.animationRotation, 0, 1)

        if config.brightness != 1.0:
            enhancer = ImageEnhance.Brightness(frameSlice)
            frameSlice = enhancer.enhance(config.brightness)

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
    config.playSpeed = float(workConfig.get("images", "playSpeed"))
    
    # managing speed of animation and framerate
    config.directorController = Director(config)

    try:
        config.delay = float(workConfig.get("images", "delay"))
    except Exception as e:
        print(str(e))
        config.delay = 0.02
    try:
        config.directorController.slotRate = float(
            workConfig.get("images", "slotRate"))
    except Exception as e:
        print(str(e))
        print("SHOULD ADJUST TO USE slotRate AS FRAMERATE ")
        config.directorController.slotRate = 0.0
    
    
    
    config.imageToLoad = workConfig.get("images", "i1")

    config.canvasImage = Image.new(
        "RGBA", (config.canvasWidth, config.canvasHeight))
    config.canvasDraw = ImageDraw.Draw(config.canvasImage)

    config.animationWidth = int(workConfig.get("images", "animationWidth"))
    config.animationHeight = int(workConfig.get("images", "animationHeight"))
    config.resizeAnimationToFit = (
        workConfig.getboolean("images", "resizeAnimationToFit"))
    config.animationImage = Image.new(
        "RGBA", (config.animationWidth, config.animationHeight))
    config.animationImageDraw = ImageDraw.Draw(config.animationImage)

    config.animationArray = []
    config.spriteSheet1 = loadImage(config.path + config.imageToLoad)

    config.randomPlacement = (
        workConfig.getboolean("images", "randomPlacement"))
    config.fixedPosition = (workConfig.getboolean("images", "fixedPosition"))
    config.frameWidth = int(workConfig.get("images", "frameWidth"))
    config.frameHeight = int(workConfig.get("images", "frameHeight"))
    config.totalFrames = int(workConfig.get("images", "totalFrames"))
    config.frameCols = int(workConfig.get("images", "frameCols"))
    config.frameRows = int(workConfig.get("images", "frameRows"))
    config.sliceWidth = int(workConfig.get("images", "sliceWidth"))
    config.sliceHeight = int(workConfig.get("images", "sliceHeight"))
    config.sliceWidthMin = int(workConfig.get("images", "sliceWidthMin"))
    config.sliceHeightMin = int(workConfig.get("images", "sliceHeightMin"))
    config.numberOfCells = int(workConfig.get("images", "numberOfCells"))
    config.animSpeedMin = int(workConfig.get("images", "animSpeedMin"))
    config.animSpeedMax = int(workConfig.get("images", "animSpeedMax"))
    config.animationRotation = float(
        workConfig.get("images", "animationRotation"))
    config.animationRotationRateRange = float(
        workConfig.get("images", "animationRotationRateRange"))
    config.animationRotationJitter = float(
        workConfig.get("images", "animationRotationJitter"))
    config.animationXOffset = int(workConfig.get("images", "animationXOffset"))
    config.animationYOffset = int(workConfig.get("images", "animationYOffset"))
    config.randomPlacemnetXRange = int(workConfig.get("images", "randomPlacemnetXRange"))
    config.randomPlacemnetYRange = int(workConfig.get("images", "randomPlacemnetYRange"))

    config.bg_minHue = int(workConfig.get("images", "bg_minHue"))
    config.bg_maxHue = int(workConfig.get("images", "bg_maxHue"))
    config.bg_minSaturation = float(
        workConfig.get("images", "bg_minSaturation"))
    config.bg_maxSaturation = float(
        workConfig.get("images", "bg_maxSaturation"))
    config.bg_minValue = float(workConfig.get("images", "bg_minValue"))
    config.bg_maxValue = float(workConfig.get("images", "bg_maxValue"))
    config.bg_dropHueMinValue = float(
        workConfig.get("images", "bg_dropHueMinValue"))
    config.bg_dropHueMaxValue = float(
        workConfig.get("images", "bg_dropHueMaxValue"))
    config.bg_alpha = int(workConfig.get("images", "bg_alpha"))

    config.backgroundColorChangeProb = float(
        workConfig.get("images", "backgroundColorChangeProb"))
    config.changeAnimProb = float(workConfig.get("images", "changeAnimProb"))
    config.pauseProb = float(workConfig.get("images", "pauseProb"))
    config.unPauseProb = float(workConfig.get("images", "unPauseProb"))
    config.freezeGlitchProb = float(
        workConfig.get("images", "freezeGlitchProb"))
    config.unFreezeGlitchProb = float(
        workConfig.get("images", "unFreezeGlitchProb"))

    config.glitching = True

    config.imageGlitchDisplacementHorizontal = int(
        workConfig.get("images", "imageGlitchDisplacementHorizontal"))
    config.imageGlitchDisplacementVertical = int(
        workConfig.get("images", "imageGlitchDisplacementVertical"))

    # Sets up color transitions
    config.colOverlay = coloroverlay.ColorOverlay()
    config.colOverlay.randomSteps = True
    config.colOverlay.timeTrigger = True
    config.colOverlay.tLimitBase = 5
    config.colOverlay.steps = 10

    config.colOverlay.maxBrightness = config.brightness
    config.colOverlay.minSaturation = config.bg_minSaturation
    config.colOverlay.maxSaturation = config.bg_maxSaturation
    config.colOverlay.minValue = config.bg_minValue
    config.colOverlay.maxValue = config.bg_maxValue
    config.colOverlay.minHue = config.bg_minHue
    config.colOverlay.maxHue = config.bg_maxHue
    config.colOverlay.colorTransitionSetup()

    config.allPause = False

    for i in range(0, config.numberOfCells):
        anim = spriteAnimation(config)

        anim.frameWidth = config.frameWidth
        anim.frameHeight = config.frameHeight
        anim.totalFrames = config.totalFrames
        anim.frameCols = config.frameCols
        anim.frameRows = config.frameRows
        anim.animSpeedMin = config.animSpeedMin
        anim.animSpeedMax = config.animSpeedMax
        anim.animationWidth = config.animationWidth
        anim.animationHeight = config.animationHeight
        anim.resizeAnimationToFit = config.resizeAnimationToFit
        anim.randomPlacement = config.randomPlacement

        reConfigAnimationCell(anim)
        config.animationArray.append(anim)

    try:
        config.filterRemapping = (
            workConfig.getboolean("images", "filterRemapping"))
        config.filterRemappingProb = float(
            workConfig.get("images", "filterRemappingProb"))
        config.filterRemapminHoriSize = int(
            workConfig.get("images", "filterRemapminHoriSize"))
        config.filterRemapminVertSize = int(
            workConfig.get("images", "filterRemapminVertSize"))
    except Exception as e:
        print(str(e))
        config.filterRemapping = False
        config.filterRemappingProb = 0.0
        config.filterRemapminHoriSize = 24
        config.filterRemapminVertSize = 24

    try:
        config.filterRemapRangeX = int(
            workConfig.get("images", "filterRemapRangeX"))
        config.filterRemapRangeY = int(
            workConfig.get("images", "filterRemapRangeY"))
    except Exception as e:
        print(str(e))
        config.filterRemapRangeX = config.canvasWidth
        config.filterRemapRangeY = config.canvasHeight

    try:
        if config.usePixelSort == True:
            config.pixelSortProbOn = float(
                workConfig.get("images", "pixelSortProbOn"))
            config.pixelSortProbOff = float(
                workConfig.get("images", "pixelSortProbOff"))
        else:
            config.pixelSortProbOn = 0
            config.pixelSortProbOff = 0

    except Exception as e:
        print(str(e))
        config.pixelSortProbOn = 0
        config.pixelSortProbOff = 0

    print(bcolors.OKBLUE + "** " + bcolors.BOLD)

    config.fontSize = 8
    config.font = ImageFont.truetype(
        config.path + "/assets/fonts/freefont/FreeSansBold.ttf", config.fontSize)

    config.imagePath = config.path + "/assets/imgs/"
    config.imageList = [config.imageToLoad]

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

    if run:
        runWork()


def glitchBox():

    global config

    apparentWidth = config.canvasImage.size[0]
    apparentHeight = config.canvasImage.size[1]
    apparentWidth = config.animationWidth
    apparentHeight = config.animationWidth
    # config.imageGlitchDisplacementVertical = 32
    # config.imageGlitchDisplacementHorizontal = 32

    dx = round(random.uniform(-config.imageGlitchDisplacementHorizontal,
               config.imageGlitchDisplacementHorizontal))
    dy = round(random.uniform(-config.imageGlitchDisplacementVertical,
               config.imageGlitchDisplacementVertical))

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
            cp1 = config.animationImage.crop((0, 0, cx, cy))
            config.animationImage.paste(cp1, (round(dx), round(dy)))
        # comment:
    except Exception as e:
        print(str(e))
        print(dx + sectionWidth, dy + sectionHeight)
    # end try


def reConfigAnimationCell(anim):
    global config

    anim.animSpeed = round(random.uniform(
        anim.animSpeedMin, anim.animSpeedMax))
    anim.animationRotation = config.animationRotation + \
        random.uniform(-config.animationRotationJitter,
                       config.animationRotationJitter)

    if config.animationRotation != 0:
        maxDim = max(anim.frameHeight, anim.frameWidth)
        anim.imageFrame = Image.new("RGBA", (maxDim, maxDim))

    anim.image = config.spriteSheet1

    # Placement on the canvas
    if anim.randomPlacement == True :
        anim.xPos = round(random.random() * config.randomPlacemnetXRange)
        anim.yPos = round(random.random() * config.randomPlacemnetYRange)

    # if config.fixedPosition == True:
    #     anim.xPos = config.animationXOffset
    #     anim.yPos = config.animationYOffset

    # deprecating for now in favor or repeat frames per cycle etc
    # anim.step = round(random.uniform(1,2))

    # random starting point in animation
    anim.sliceCol = round(random.random() * anim.frameCols)
    anim.sliceRow = round(random.random() * anim.frameRows)
    anim.frameCount = anim.sliceCol + anim.sliceRow * config.frameCols

    # random slicing of section to display
    anim.sliceXOffset = 0  # round(random.random() * anim.frameWidth)
    anim.sliceYOffset = 0  # round(random.random() * anim.frameHeight)
    anim.sliceWidth = round(random.uniform(
        config.sliceWidthMin, config.sliceWidth))
    anim.sliceHeight = round(random.uniform(
        config.sliceHeightMin, config.sliceHeight))

    if anim.sliceWidth + anim.sliceXOffset > anim.frameWidth:
        anim.sliceWidth = anim.frameWidth - anim.sliceXOffset

    if anim.sliceHeight + anim.sliceYOffset > anim.frameHeight:
        anim.sliceHeight = anim.frameHeight - anim.sliceYOffset

    anim.animationRotationRate = random.uniform(
        -config.animationRotationRateRange, config.animationRotationRateRange)


def runWork():
    print(bcolors.OKGREEN + "** " + bcolors.BOLD)
    print("Running image.py")
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

    config.colOverlay.stepTransition()

    bgColor = config.colOverlay.currentColor
    # config.bg_alpha = 255
    # config.canvasDraw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=(
    #         bgColor[0], bgColor[1], bgColor[2], config.bg_alpha))

    config.canvasImage.paste(config.animationImage, (config.animationXOffset,
                             config.animationYOffset), config.animationImage)

    if config.allPause == True:
        if config.glitching == True:
            glitchBox()
            if random.random() < config.freezeGlitchProb:
                config.glitching = False
    else:
        config.animationImageDraw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=(
            bgColor[0], bgColor[1], bgColor[2], config.bg_alpha))
        # config.canvasDraw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=(bgColor[0], bgColor[1], bgColor[2], config.bg_alpha))
        for anim in config.animationArray:
            config.animationImage.paste(
                anim.nextFrame(), (anim.xPos, anim.yPos), anim.nextFrame())
            # config.animationImage.paste(anim.nextFrame(), (0, 0), anim.nextFrame())
            anim.pause = config.allPause

            if random.random() < config.changeAnimProb:
                reConfigAnimationCell(anim)

    ########### RENDERING AS A MOCKUP OR AS REAL ###########
    if config.useDrawingPoints == True:
        config.panelDrawing.canvasToUse = config.f.blendedImage
        config.panelDrawing.render()
    else:
        # config.render(config.image, 0, 0)
        config.render(config.canvasImage, 0, 0,
                      config.canvasWidth, config.canvasHeight)

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

    if random.random() < config.pauseProb:
        config.allPause = True

    if config.allPause == True and random.random() < config.unFreezeGlitchProb:
        config.glitching = True

    if config.allPause == True and random.random() < config.unPauseProb:
        config.allPause = False

    if random.random() < config.backgroundColorChangeProb:
        # config.bgBackGroundColor = config.bgBackGroundEndColor
        config.bgBackGroundEndColor = colorutils.getRandomColorHSV(
            config.bg_minHue, config.bg_maxHue,
            config.bg_minSaturation, config.bg_maxSaturation,
            config.bg_minValue, config.bg_maxValue,
            config.bg_dropHueMinValue, config.bg_dropHueMaxValue, 255, config.brightness)


def callBack():
    global config
    print("CALLBACK")
    return True


#####################
