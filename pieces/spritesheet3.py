#!/usr/bin/python
# import modules
import math
import random
import time
from modules.configuration import bcolors
from modules import badpixels, colorutils, coloroverlay, panelDrawing
from PIL import (
    Image,
    ImageDraw,
    ImageEnhance,
)

# import numpy as np
from modules.holder_director import Holder
from modules.holder_director import Director

xPos = 320
yPos = 0
bads = badpixels

# config.canvasImage is the final layer or image to be rendered
# everything else gets pasted on to this image layer
# the filtering happens to this canvasImage as well

# ----------------------------------------------------##----------------------------------------------------#


# ----------------------------------------------------##----------------------------------------------------#
class spriteAnimation:

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

    name = "default"

    xPos = 0
    yPos = 0

    frameArray = []

    pause = False

    def __init__(self, config):
        self.config = config
        self.imageFrame = Image.new("RGBA", (self.frameWidth, self.frameHeight))

    # ----------------------------------------------------##----------------------------------------------------#
    def prepSlices(self):
        frame = 0
        self.frameArray = []
        for r in range(self.frameRows):
            for c in range(self.frameCols):
                if frame < self.totalFrames:
                    xPos = c * self.frameWidth + self.sliceXOffset
                    yPos = r * self.frameHeight + self.sliceYOffset

                    frameSlice = self.image.crop((xPos, yPos, xPos + self.sliceWidth, yPos + self.sliceHeight))

                    if self.resizeAnimationToFit:
                        frameSlice = frameSlice.resize((self.animationWidth, self.animationHeight))

                    if self.animationRotation != 0:
                        frameSlice = frameSlice.rotate(self.animationRotation, 0, 1)

                    if self.config.brightness != 1.0:
                        enhancer = ImageEnhance.Brightness(frameSlice)
                        frameSlice = enhancer.enhance(self.config.brightness)

                    if frame == 0:
                        self.firstFrame = frameSlice.copy()
                    self.frameArray.append(frameSlice)
                    frame += 1

        print("------------  ")
        print(f"{self.name} prep done")
        print(f"Number of Frames:{len(self.frameArray)}")
        print("------------\n")
        # exit()

    # ----------------------------------------------------##----------------------------------------------------#

    def getNextFrame(self):
        # img = self.frameArray[self.currentFrame]

        if self.totalFrames == 1:
            self.currentFrame = 0
        elif not self.pause:
            self.playCount += self.step
            if self.reversing:
                if self.playCount % self.animSpeed == 0:
                    self.currentFrame += self.direction

                if self.currentFrame >= self.endFrame:
                    self.direction *= -1
                    self.currentFrame = self.endFrame - 1

                    # if self.direction > 0 :
                    #     self.currentFrame = self.endFrame

                if self.currentFrame < self.startFrame:
                    self.direction *= -1
                    self.currentFrame = self.startFrame
                    # if self.direction < 0 :
                    #     self.currentFrame = self.startFrame
            elif self.playCount % self.animSpeed == 0:
                self.currentFrame += 1
                if self.currentFrame >= self.endFrame:
                    self.currentFrame = self.startFrame

    # ----------------------------------------------------##----------------------------------------------------#

    def nextFrameImg(self):
        return self.frameArray[self.currentFrame]


# ----------------------------------------------------##----------------------------------------------------#
def loadImage(spriteSheet):
    image = Image.open(spriteSheet, "r")
    image.load()
    # imgHeight = image.getbbox()[3]
    return image


# ----------------------------------------------------##----------------------------------------------------#
def main(run=True):
    global config, workConfig, blocks, simulBlocks, bads
    # gc.enable()

    print("SpriteSheet Player Piece Loaded")
    # config.playSpeed = float(workConfig.get("base-parameters", "playSpeed"))

    # managing speed of animation and framerate
    config.directorController = Director(config)
    config.delay = float(workConfig.get("base-parameters", "delay"))
    config.directorController.slotRate = float(workConfig.get("base-parameters", "slotRate"))

    config.filterRemapping = workConfig.getboolean("base-parameters", "filterRemapping")
    config.filterRemappingProb = float(workConfig.get("base-parameters", "filterRemappingProb"))
    config.filterRemapminHoriSize = int(workConfig.get("base-parameters", "filterRemapminHoriSize"))
    config.filterRemapminVertSize = int(workConfig.get("base-parameters", "filterRemapminVertSize"))
    config.filterRemapRangeX = int(workConfig.get("base-parameters", "filterRemapRangeX"))
    config.filterRemapRangeY = int(workConfig.get("base-parameters", "filterRemapRangeY"))

    try:
        if config.usePixelSort:
            config.pixelSortProbOn = float(workConfig.get("base-parameters", "pixelSortProbOn"))
            config.pixelSortProbOff = float(workConfig.get("base-parameters", "pixelSortProbOff"))
        else:
            config.pixelSortProbOn = 0
            config.pixelSortProbOff = 0

    except Exception as e:
        print(e)
        config.pixelSortProbOn = 0
        config.pixelSortProbOff = 0

    print(f"{bcolors.OKBLUE}** {bcolors.BOLD}")

    config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.canvasDraw = ImageDraw.Draw(config.canvasImage)

    config.underLayer = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.underLayerDraw = ImageDraw.Draw(config.underLayer)

    config.underLayerDraw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=(100, 0, 80, 100))

    config.allPause = False

    animationNames = workConfig.get("base-parameters", "animations").split(",")
    playTimes = workConfig.get("base-parameters", "playTimes").split(",")
    config.playInOrder = workConfig.getboolean("base-parameters", "playInOrder")

    config.drawMoire = workConfig.getboolean("base-parameters", "drawMoire")
    config.drawMoireProb = float(workConfig.get("base-parameters", "drawMoireProb"))
    config.drawMoireProbOff = float(workConfig.get("base-parameters", "drawMoireProbOff"))

    config.moireXPos = int(workConfig.get("base-parameters", "moireXPos"))
    config.moireYPos = int(workConfig.get("base-parameters", "moireYPos"))
    config.moireXDistance = int(workConfig.get("base-parameters", "moireXDistance"))
    config.moireYDistance = int(workConfig.get("base-parameters", "moireYDistance"))
    config.setMoireColor = workConfig.getboolean("base-parameters", "setMoireColor")
    config.moireColorAltProb = float(workConfig.get("base-parameters", "moireColorAltProb"))
    config.moireColor = tuple(map(lambda x: int(x), workConfig.get("base-parameters", "moireColor").split(",")))
    config.moireColorAlt = tuple(
        map(
            lambda x: int(x),
            workConfig.get("base-parameters", "moireColorAlt").split(","),
        )
    )

    config.animationNames = animationNames
    config.animations = []
    config.currentAnimationIndex = 0
    config.animationController = Director(config)

    config.bgBoxColorRange = list(
        map(
            lambda x: float(x),
            workConfig.get("base-parameters", "bgBoxColorRange").split(","),
        )
    )
    config.bgBoxAlphaRange = tuple(
        map(
            lambda x: int(x),
            workConfig.get("base-parameters", "bgBoxAlphaRange").split(","),
        )
    )
    config.usebgBox = workConfig.getboolean("base-parameters", "forcebgBox")
    config.usebgBoxProb = float(workConfig.get("base-parameters", "usebgBoxProb"))
    config.bgBoxBox = tuple(map(lambda x: int(x), workConfig.get("base-parameters", "bgBoxBox").split(",")))
    config.renderImageFullOverlay = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.renderDrawOver = ImageDraw.Draw(config.renderImageFullOverlay)
    config.bgBoxFill = (100, 0, 80, 100)

    config.bgTileSizeWidthMin = float(workConfig.get("base-parameters", "bgTileSizeWidthMin"))
    config.bgTileSizeWidthMax = float(workConfig.get("base-parameters", "bgTileSizeWidthMax"))
    config.bgTileSizeHeightMin = float(workConfig.get("base-parameters", "bgTileSizeHeightMin"))
    config.bgTileSizeHeightMax = float(workConfig.get("base-parameters", "bgTileSizeHeightMax"))
    # config.bgBoxFill = tuple(	map(lambda x: int(x), workConfig.get("base-parameters", "bgBoxFill").split(",")))

    config.animationFrameXOffset = int(workConfig.get("base-parameters", "animationFrameXOffset"))
    config.animationFrameYOffset = int(workConfig.get("base-parameters", "animationFrameYOffset"))

    config.clearbgBoxProb = float(workConfig.get("base-parameters", "clearbgBoxProb"))
    config.bgGlitchCyclesMin = float(workConfig.get("base-parameters", "bgGlitchCyclesMin"))
    config.bgGlitchCyclesMax = float(workConfig.get("base-parameters", "bgGlitchCyclesMax"))
    config.bgGlitchDisplacementHorizontal = float(workConfig.get("base-parameters", "bgGlitchDisplacementHorizontal"))
    config.bgGlitchDisplacementVertical = float(workConfig.get("base-parameters", "bgGlitchDisplacementVertical"))

    config.playTimes = tuple(map(lambda x: int(x), playTimes))
    # config.animationController.delay = 1.0
    config.animationController.slotRate = config.playTimes[0]

    try:
        config.preGlitchNumber = int(workConfig.get("base-parameters", "preGlitchNumber"))
        config.preGlitchNumberMin = int(workConfig.get("base-parameters", "preGlitchNumberMin"))
        config.preGlitchRedo = float(workConfig.get("base-parameters", "preGlitchRedo"))
    except Exception as e:
        print(e)
        config.preGlitchNumberMin = 1
        config.preGlitchNumber = 2
        config.preGlitchRedo = 0.5

    # ----------------------------------------------------------------------------

    for a in config.animationNames:
        aConfig = Holder(config)
        aConfig.name = a

        aConfig.imageToLoad = workConfig.get(a, "i1")
        aConfig.animationWidth = int(workConfig.get(a, "animationWidth"))
        aConfig.animationHeight = int(workConfig.get(a, "animationHeight"))
        aConfig.resizeAnimationToFit = workConfig.getboolean(a, "resizeAnimationToFit")
        aConfig.animationRotation = float(workConfig.get(a, "animationRotation"))
        aConfig.animationImage = Image.new("RGBA", (aConfig.animationWidth, aConfig.animationHeight))

        if abs(aConfig.animationRotation) == 90:
            aConfig.animationImage = Image.new("RGBA", (aConfig.animationHeight, aConfig.animationWidth))

        aConfig.animationImageDraw = ImageDraw.Draw(aConfig.animationImage)

        aConfig.animationArray = []
        aConfig.spriteSheet1 = loadImage(config.path + aConfig.imageToLoad)

        aConfig.randomPlacement = workConfig.getboolean(a, "randomPlacement")
        aConfig.fixedPosition = workConfig.getboolean(a, "fixedPosition")
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
        aConfig.bg_alpha = int(workConfig.get(a, "bg_alpha"))
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
            print(e)
            aConfig.pauseOnFirstFrameProb = 0.0
            aConfig.pauseOnLastFrameProb = 0.0
        try:
            # comment:
            aConfig.reversing = workConfig.getboolean(a, "reversing")
        except Exception as e:
            print(e)
            aConfig.reversing = False

        aConfig.glitching = True
        aConfig.preDistorted = False

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

        aConfig.imagePath = f"{config.path}/assets/imgs/"
        aConfig.imageList = [aConfig.imageToLoad]

        config.animations.append(aConfig)
        reConfigAnimationCell(anim, aConfig)
        anim.prepSlices()
        # aConfig.animationArray.append(anim)
        aConfig.anim = anim

    # THIS IS USED AS WAY TO MOCKUP A CONFIGURATION OF RECTANGULAR PANELS
    panelDrawing.mockupBlock(config, workConfig)
    # Need to add something like this at final render call  as well
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

    # config.debugSelf()

    # print(config.__dict__)

    if config.brightness < 1.0:
        delta = config.ditherFilterBrightness - config.brightness
        config.ditherFilterBrightness -= delta / 4
        print(config.ditherFilterBrightness)

    if run:
        runWork()


# ----------------------------------------------------##----------------------------------------------------#
def glitchBox(
    imageRef,
    apparentWidth,
    apparentHeight,
    imageGlitchDisplacementHorizontal,
    imageGlitchDisplacementVertical,
):

    global config

    apparentWidth = config.canvasImage.size[0]
    apparentHeight = config.canvasImage.size[1]

    dx = round(random.uniform(-imageGlitchDisplacementHorizontal, imageGlitchDisplacementHorizontal))
    dy = round(random.uniform(-imageGlitchDisplacementVertical, imageGlitchDisplacementVertical))

    sectionWidth = round(random.uniform(2, apparentWidth - dx))
    sectionHeight = round(random.uniform(2, apparentHeight - dy))

    # 95% of the time they dance together as mirrors
    try:
        if random.SystemRandom().random() < 0.97:
            cx = dx + sectionWidth
            cy = dy + sectionHeight

            if cx < 0:
                cx = 32
            if cy < 0:
                cy = 32
            cp1 = imageRef.crop((0, 0, cx, cy))
            imageRef.paste(cp1, (round(dx), round(dy)))
        # comment:
    except Exception as e:
        print(e)
        print(dx + sectionWidth, dy + sectionHeight)
    # end try


# ----------------------------------------------------##----------------------------------------------------#
def animationBackGroundFadeIn():
    currentAnimation = config.animations[config.currentAnimationIndex]
    if currentAnimation.bg_alpha <= currentAnimation.bg_alpha_max:
        currentAnimation.bg_alpha += 2


# ----------------------------------------------------##----------------------------------------------------#
def reConfigAnimationCell(anim, aConfig):
    global config

    anim.animSpeed = round(random.uniform(anim.animSpeedMin, anim.animSpeedMax))
    anim.animationRotation = aConfig.animationRotation + random.uniform(-aConfig.animationRotationJitter, aConfig.animationRotationJitter)

    if aConfig.animationRotation != 0:
        maxDim = max(anim.frameHeight, anim.frameWidth)
        anim.imageFrame = Image.new("RGBA", (maxDim, maxDim))

    anim.image = aConfig.spriteSheet1

    # Placement on the canvas
    if anim.randomPlacement:
        anim.xPos = round(random.SystemRandom().random() * aConfig.randomPlacemnetXRange)
        anim.yPos = round(random.SystemRandom().random() * aConfig.randomPlacemnetYRange)

    # if config.fixedPosition :
    #     anim.xPos = config.animationXOffset
    #     anim.yPos = config.animationYOffset

    # deprecating for now in favor or repeat frames per cycle etc
    # anim.step = round(random.uniform(1,2))

    # random starting point in animation
    anim.sliceCol = round(random.SystemRandom().random() * anim.frameCols)
    anim.sliceRow = round(random.SystemRandom().random() * anim.frameRows)
    anim.startFrame = anim.sliceCol + anim.sliceRow * aConfig.frameCols
    anim.startFrame = 0
    anim.endFrame = anim.totalFrames
    anim.playCount = 0
    anim.currentFrame = 0

    # random slicing of section to display
    anim.sliceXOffset = 0  # round(random.SystemRandom().random() * anim.frameWidth)
    anim.sliceYOffset = 0  # round(random.SystemRandom().random() * anim.frameHeight)
    anim.sliceWidth = round(random.uniform(aConfig.sliceWidthMin, aConfig.sliceWidth))
    anim.sliceHeight = round(random.uniform(aConfig.sliceHeightMin, aConfig.sliceHeight))

    if anim.sliceWidth + anim.sliceXOffset > anim.frameWidth:
        anim.sliceWidth = anim.frameWidth - anim.sliceXOffset

    if anim.sliceHeight + anim.sliceYOffset > anim.frameHeight:
        anim.sliceHeight = anim.frameHeight - anim.sliceYOffset

    anim.animationRotationRate = random.uniform(-aConfig.animationRotationRateRange, aConfig.animationRotationRateRange)


# ----------------------------------------------------##----------------------------------------------------#
def filterRemapCall(ovrd=False):
    config.filterRemap = True
    # new version  more control but may require previous pieces to be re-worked
    startX = round(random.uniform(0, config.filterRemapRangeX))
    startY = round(random.uniform(0, config.filterRemapRangeY))
    endX = round(random.uniform(8, config.filterRemapminHoriSize))
    endY = round(random.uniform(8, config.filterRemapminVertSize))

    if ovrd:
        startX = 0
        startY = 0
        endX = 200
        endY = 200
    config.remapImageBlockSection = [startX, startY, startX + endX, startY + endY]
    config.remapImageBlockDestination = [startX, startY]
    # print("swapping" + str(config.remapImageBlockSection))


# ----------------------------------------------------##----------------------------------------------------#
def runWork():
    print(f"{bcolors.OKGREEN} ** {bcolors.BOLD}")
    print("Running spritesheet3.py")
    print(bcolors.ENDC)
    # gc.enable()
    while config.isRunning:
        config.directorController.checkTime()
        if config.directorController.advance:
            iterate()
            time.sleep(config.delay)
        if not config.standAlone:
            config.callBack()


# ----------------------------------------------------##----------------------------------------------------#
def iterate(n=0):
    global config, blocks
    global xPos, yPos

    currentAnimation = config.animations[config.currentAnimationIndex]
    currentAnimation.colOverlay.stepTransition()
    bgColor = currentAnimation.colOverlay.currentColor

    config.canvasImage.paste(
        currentAnimation.animationImage,
        (config.animationFrameXOffset, config.animationFrameYOffset),
        currentAnimation.animationImage,
    )
    animationBackGroundFadeIn()

    if config.allPause:
        if currentAnimation.glitching:
            glitchBox(
                currentAnimation.animationImage,
                currentAnimation.animationWidth,
                currentAnimation.animationHeight,
                currentAnimation.imageGlitchDisplacementHorizontal,
                currentAnimation.imageGlitchDisplacementVertical,
            )
            if random.SystemRandom().random() < currentAnimation.freezeGlitchProb:
                currentAnimation.glitching = False
    else:

        _moireOverLay(currentAnimation, config, bgColor)
    # Draws the colored tiles over the animation image -
    # Note first versions drew this over the animation image but on 10-29-2023 I
    # tested drawing it over the final image layer canvasImage instead - not sure
    # if it really changes anything though

    composite = config.canvasImage

    if random.SystemRandom().random() < config.usebgBoxProb and config.usebgBox and not config.allPause:
        _bgColorsFilling(config)
    if random.SystemRandom().random() < config.clearbgBoxProb:
        config.underLayer = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
        config.underLayerDraw = ImageDraw.Draw(config.underLayer)

    # if config.usebgBox  :
    #     # config.canvasImage.paste(config.underLayer, (0,0), config.underLayer)
    #     composite = ImageChops.screen( config.underLayer, config.canvasImage)

    ########### RENDERING AS A MOCKUP OR AS REAL ###########
    if config.useDrawingPoints:
        config.panelDrawing.canvasToUse = config.f.blendedImage
        config.panelDrawing.render()
    else:
        # config.render(config.image, 0, 0)
        # ===================== RENDERING ================================

        config.render(composite, 0, 0, config.canvasWidth, config.canvasHeight)
        # config.render(config.canvasImage, 0, 0, config.canvasWidth, config.canvasHeight)

        # ===================== RENDERING ================================

    if random.SystemRandom().random() < config.drawMoireProb:
        config.drawMoire = True
    if random.SystemRandom().random() < config.drawMoireProbOff:
        config.drawMoire = False

    # if random.SystemRandom().random() < config.filterRemappingProb:
    #     if random.SystemRandom().random() < 0.5:
    #         not config.filterRemapping
    #     else:
    #         config.filterRemapping

    if random.SystemRandom().random() < config.filterRemappingProb and (config.useFilters and config.filterRemapping):
        filterRemapCall()

    if random.SystemRandom().random() < config.pixelSortProbOn:
        config.usePixelSort = True

    if random.SystemRandom().random() < config.pixelSortProbOff:
        config.usePixelSort = False

    # if random.SystemRandom().random() < currentAnimation.pauseProb:
    #     config.allPause = True

    if config.allPause and random.SystemRandom().random() < currentAnimation.unFreezeGlitchProb:
        # print("glitching")
        currentAnimation.glitching = True

    if config.allPause and random.SystemRandom().random() < currentAnimation.unPauseProb:
        # print("unpausing")
        config.allPause = False

    config.animationController.checkTime()
    if config.animationController.advance:
        _drawNextFrames(currentAnimation, config)


def _drawNextFrames(currentAnimation, config):
    currentAnimation.glitching = False

    if config.playInOrder:
        config.currentAnimationIndex += 1
        if config.currentAnimationIndex >= len(config.animations):
            config.currentAnimationIndex = 0
        # print("Next Animation : " + str(config.animations[config.currentAnimationIndex].name))
    else:
        choice = math.floor(random.uniform(0, len(config.animations)))
        config.currentAnimationIndex = choice
        # print("Next Animation : " + str(config.animations[choice].name))

    config.animationController.slotRate = config.playTimes[config.currentAnimationIndex]
    currentAnimation = config.animations[config.currentAnimationIndex]
    currentAnimation.preDistorted = False

    if currentAnimation.totalFrames == 1:
        if random.SystemRandom().random() < 0.5:
            # print("Repasting in the original")
            currentAnimation.anim.frameArray[0] = currentAnimation.anim.firstFrame.copy()

        tempImageRef = currentAnimation.anim.nextFrameImg()
        # currentAnimation.anim.currentFrame = tempImageRef
        # print("Should be reset")
        glitchyCycles = random.SystemRandom().randrange(config.preGlitchNumberMin, config.preGlitchNumber)
        # print(glitchyCycles)
        for _ in range(glitchyCycles):
            glitchBox(
                tempImageRef,
                currentAnimation.animationWidth,
                currentAnimation.animationHeight,
                currentAnimation.imageGlitchDisplacementHorizontal,
                currentAnimation.imageGlitchDisplacementVertical,
            )

        if random.SystemRandom().random() < config.preGlitchRedo:
            # print("second round")
            for _ in range(glitchyCycles):
                glitchBox(
                    tempImageRef,
                    currentAnimation.animationWidth,
                    currentAnimation.animationHeight,
                    currentAnimation.imageGlitchDisplacementHorizontal,
                    currentAnimation.imageGlitchDisplacementVertical,
                )

    currentAnimation.preDistorted = True
    # config.animationController.slotRate = round(random.uniform(currentAnimation.animSpeedMin,currentAnimation.animSpeedMax))

    currentAnimation.bg_alpha = 10
    config.allPause = False
    currentAnimation.anim.currentFrame = 0


def _bgColorsFilling(config):
    # config.usebgBox = False if config.usebgBox   else True
    # print("bgBox")
    # xPos = config.tileSizeWidth * math.floor(random.uniform(0, config.cols))
    # yPos = config.tileSizeHeight * math.floor(random.uniform(0, config.rows))

    xPos = math.floor(random.uniform(0, config.canvasWidth))
    yPos = math.floor(random.uniform(0, config.canvasHeight))

    config.tileSizeWidth = round(random.uniform(config.bgTileSizeWidthMin, config.bgTileSizeWidthMax))
    config.tileSizeHeight = round(random.uniform(config.bgTileSizeHeightMin, config.bgTileSizeHeightMax))

    if random.SystemRandom().random() < config.clearbgBoxProb:
        xPos = yPos = 0
        config.bgBoxBox = (
            xPos,
            yPos,
            xPos + config.canvasWidth,
            yPos + config.canvasHeight,
        )
        config.bgBoxFill = (0, 0, 0, 0)
    else:
        config.bgBoxBox = (
            xPos,
            yPos,
            xPos + config.tileSizeWidth,
            yPos + config.tileSizeHeight,
        )
        cR = config.bgBoxColorRange
        # print(cR)
        bgBoxFill = colorutils.getRandomColorHSV(cR[0], cR[1], cR[2], cR[3], cR[4], cR[5], cR[6], cR[7])
        # print(bgBoxFill)
        config.bgBoxFill = (
            round(config.brightness * bgBoxFill[0]),
            round(config.brightness * bgBoxFill[1]),
            round(config.brightness * bgBoxFill[2]),
            round(random.uniform(config.bgBoxAlphaRange[0], config.bgBoxAlphaRange[1])),
        )

    config.underLayerDraw.rectangle(config.bgBoxBox, fill=config.bgBoxFill)

    glitchIterations = round(random.uniform(config.bgGlitchCyclesMin, config.bgGlitchCyclesMax))
    for _ in range(glitchIterations):
        glitchBox(
            config.underLayer,
            config.canvasWidth,
            config.canvasHeight,
            config.bgGlitchDisplacementHorizontal,
            config.bgGlitchDisplacementVertical,
        )



def _moireOverLay(currentAnimation, config, bgColor):
    """Applies moire pattern and animates the current animation."""
    _draw_background(currentAnimation, config, bgColor)
    _draw_moire_pattern(currentAnimation, config)
    _paste_animation_frame(currentAnimation)

    if not config.allPause:
        _animate(currentAnimation.anim, currentAnimation, config)

    currentAnimation.anim.pause = config.allPause

    if random.SystemRandom().random() < currentAnimation.changeAnimProb:
        reConfigAnimationCell(currentAnimation.anim, currentAnimation)


def _draw_background(currentAnimation, config, bgColor):
    """Draws the background color on the animation image."""
    bgColor = (
        round(config.brightness * bgColor[0]),
        round(config.brightness * bgColor[1]),
        round(config.brightness * bgColor[2]),
        currentAnimation.bg_alpha,
    )
    currentAnimation.animationImageDraw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=bgColor)

    if config.usebgBox:
        currentAnimation.animationImage.paste(config.underLayer, (0, 0), config.underLayer)


def _draw_moire_pattern(currentAnimation, config):
    """Draws the moire pattern if enabled."""
    if not config.drawMoire:
        return

    c1 = (round(config.brightness * 150), round(config.brightness * 50), 0, 150)
    if config.setMoireColor:
        c1 = config.moireColor
        if random.SystemRandom().random() < config.moireColorAltProb:
            c1 = config.moireColorAlt

    for ii in range(2):
        xc = ii * config.moireXDistance + config.moireXPos
        yc = ii * config.moireYDistance + config.moireYPos
        for i in range(1200):
            w = 3 * config.canvasWidth - i * 6
            if w > 1:
                x0 = xc - w / 2
                y0 = yc - w / 2
                x1 = xc + w / 2
                y1 = yc + w / 2

                x1 = max(x0 + 1, x1)
                y1 = max(y0 + 1, y1)

                currentAnimation.animationImageDraw.ellipse((x0, y0, x1, y1), fill=None, outline=c1)


def _paste_animation_frame(currentAnimation):
    """Pastes the current animation frame onto the animation image."""
    anim = currentAnimation.anim
    tempImageRef = anim.nextFrameImg()
    currentAnimation.animationImage.paste(
        tempImageRef,
        (anim.xPos + currentAnimation.animationXOffset, anim.yPos + currentAnimation.animationYOffset),
        tempImageRef,
    )


def _animate(anim, currentAnimation, config):
    # doing this 3 times because this was how the v.2 version inadvertently did it - my bad - but also to
    # improve the smoothness and the way the animation speed values work - i.e. they affect the speed at
    # at a more granular way

    # print("fetching")
    anim.getNextFrame()
    anim.getNextFrame()
    anim.getNextFrame()

    if random.SystemRandom().random() < currentAnimation.pauseOnFirstFrameProb and anim.currentFrame == anim.startFrame:
        # print("paused at start")
        anim.pause = True
        config.allPause = True

    # print(anim.currentFrame,anim.endFrame-1)
    if random.SystemRandom().random() < currentAnimation.pauseOnLastFrameProb and anim.currentFrame == anim.endFrame - 1:
        # print("paused at end")
        config.allPause = True
        anim.pause = True

    if (anim.pause or config.allPause) and random.SystemRandom().random() < currentAnimation.unPauseProb:
        # print("releasing animation")
        anim.pause = False
        config.allPause = False

    if random.SystemRandom().random() < currentAnimation.pauseProb:
        # print("pausing at frame:" + str(anim.currentFrame) + " prob: " + str(currentAnimation.pauseProb))
        anim.pause = True
        config.allPause = True
        if random.SystemRandom().random() < 0.5:
            anim.direction *= -1
        # config.canvasImage.paste(currentAnimation.animationImage, (0,0), currentAnimation.animationImage)
        # config.render(config.canvasImage, 0, 0, config.canvasWidth, config.canvasHeight)
        # currentAnimation.glitching = True
        # config.allPause = True


# ----------------------------------------------------##----------------------------------------------------#
def callBack():
    global config
    print("CALLBACK")
    return True


#####################
