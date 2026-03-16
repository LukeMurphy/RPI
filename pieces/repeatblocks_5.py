# ################################################### #
import itertools
import math
import random
import time
import noise
import os, sys
import configparser
from modules.configuration import bcolors
from modules.configuration import pieceLogger
from modules.movieClip import movieClip
from modules import colorutils, panelDrawing, pattern_blocks_v5
from modules.holder_director import Holder
from modules.holder_director import Director
from modules.coloroverlay import ColorOverlay
from PIL import Image, ImageDraw, ImageEnhance, ImageOps, ImageFilter, ImageChops
from copy import copy, deepcopy

# This version substitutes the overlay disturbance with a slide-repeating of a section

# Adding the wave deformation to get a slightly more organic
# pattern distortion - might be too much, too expected but
# is dreamy  4-3-2024

# major refactoring along with pattern_blocks.py 2025-02-19


###############################################


# --------------------- CLASSES     ---------------------
class WaveDeformer:
    def transform(self, x, y):
        y = y + config.waveAmplitude * math.sin((x + config.waveDeformXPos) / config.wavePeriodMod) * noise.pnoise2(math.sin(x), y / config.pNoiseMod)
        return x, y

    def transform_rectangle(self, x0, y0, x1, y1):
        return (
            *self.transform(x0, y0),
            *self.transform(x0, y1),
            *self.transform(x1, y1),
            *self.transform(x1, y0),
        )

    def getmesh(self, img):
        self.w, self.h = img.size

        target_grid = [
            (x, y, x + config.wavegridspace, y + config.wavegridspace)
            for x, y in itertools.product(
                range(0, self.w, config.wavegridspace),
                range(0, self.h, config.wavegridspace),
            )
        ]
        source_grid = [self.transform_rectangle(*rect) for rect in target_grid]

        return list(zip(target_grid, source_grid))


class Fader:

    def __init__(self):
        self.doingRefresh = 0
        self.doingRefreshCount = 20
        self.fadingDone = False
        self.testing = True
        self.fadeThruBlack = False
        self.destinationImage = None
        self.initialized = False

    def setUp(self):
        self.blankImage = Image.new("RGBA", (self.width, self.height))
        self.startingImage = Image.new("RGBA", (self.width, self.height))
        self.endImage = Image.new("RGBA", (self.width, self.height))
        self.crossFadeImage = Image.new("RGBA", (self.width, self.height))

    def test(self):
        pieceLogger("test")
        # self.blankImage = Image.new("RGBA", (self.width, self.height))
        tDraw1 = ImageDraw.Draw(self.startingImage)
        tDraw1.rectangle((0, 0, 100, 100), fill=(0, 255, 255, 200))

        tDraw2 = ImageDraw.Draw(self.crossFadeImage)
        tDraw2.rectangle((100, 0, 200, 100), fill=(0, 0, 255, 200))

        tDraw3 = ImageDraw.Draw(self.destinationImage)
        tDraw3.rectangle((200, 0, 300, 100), fill=(0, 255, 0, 255))

        tDraw4 = ImageDraw.Draw(config.patternImage)
        tDraw4.rectangle((0, 100, 100, 200), fill=(255, 255, 0, 255))

        tDraw5 = ImageDraw.Draw(config.canvasImage)
        tDraw5.rectangle((100, 100, 200, 200), fill=(255, 0, 255, 255))

        tDraw6 = ImageDraw.Draw(config.compositeImage)
        tDraw6.rectangle((0, 200, 0, 300), fill=(255, 250, 255, 255))

    def fadeIn(self, config):
        if self.doingRefreshCount >= 0 and not self.fadingDone:

            if self.initialized:
                # print(self.fadingDone, self.doingRefresh)
                self.initialized = False

            if self.testing:
                self.testing = False

            if self.doingRefresh <= self.doingRefreshCount:

                if self.fadeThruBlack:
                    self.blankImage = Image.new("RGBA", (self.width, self.height))
                    self.blankImageDraw = ImageDraw.Draw(self.blankImage)
                    self.blankImageDraw.rectangle((0, 0, self.width, self.height), fill=(0, 0, 0, 255))

                percent = self.doingRefresh / self.doingRefreshCount
                self.crossFadeImage = Image.blend(
                    self.startingImage,
                    self.endImage,
                    percent,
                )

                # self.test()
                self.destinationImage.paste(self.crossFadeImage, (self.xPos, self.yPos), self.crossFadeImage)
                self.doingRefresh += 1
            else:
                # self.destinationImage.paste(self.startingImage, (self.xPos, self.yPos), self.startingImage)
                self.fadingDone = True
                self.doingRefresh = 0
                # self.blankImage = self.startingImage.copy()
                self.testing = True
                config.doTransition = False
                # print("\n ======> FADING DONE")
        else:
            self.fadingDone = True
            self.initialized = False


class PatternBlock:
    def __init__(self):
        self.hasBeenPainted = False
        self.rePainting = False


class CombinationSet:
    def __init__(self, _name="default"):
        self.name = _name


# --------------------- UTILS       ---------------------
def transformImage(img):
    width, height = img.size
    m = -0.0
    xshift = abs(m) * 420
    new_width = width + int(round(xshift))

    # img = img.transform(
    # 	(new_width, height), Image.AFFINE, (1, -0.1, 0.0, -0.5, 1, 1), Image.BICUBIC
    # )
    img = img.transform((new_width, height), Image.PERSPECTIVE, config.transformTuples, Image.BICUBIC)
    return img


def writeImage(baseName, renderImage):
    # baseName = "outputquad3/comp2_"
    if config.saveImages and not config.drawingPoints:
        pieceLogger("Saving Image...")
        fn = f"{baseName}.png"
        renderImage.save(fn)


def loadImageForBase():
    # image = Image.open("./assets/imgs/drawings/P1060494.jpg", "r")
    # image = Image.open("./assets/imgs/miscl/comp-384.jpg", "r")
    # image = Image.open("./assets/imgs/miscl/lm_a.png", "r")

    i = math.floor(random.random() * len(config.imageSources))
    imagePath = config.imageSources[i]
    pieceLogger(imagePath)
    image = Image.open(imagePath)
    image.load()
    config.canvasImage.paste(image, (0, 0))


def loadClipPlayerConfigs():
    loadConfigValue(config, workConfig, "imageSequencePlayer", "useClipPlayer", False, bool)
    loadConfigValue(config, workConfig, "imageSequencePlayer", "clipXPos", 1, int)
    loadConfigValue(config, workConfig, "imageSequencePlayer", "clipYPos", 1, int)
    loadConfigValue(config, workConfig, "imageSequencePlayer", "clipRotate", 0, float)
    loadConfigValue(config, workConfig, "imageSequencePlayer", "steps", 1, int)
    loadConfigValue(config, workConfig, "imageSequencePlayer", "steps", 1, int)

    try:
        config.clipMain = movieClip(config)
        config.clipMain.clipRotate = config.clipRotate
        config.clipMain.setUp(workConfig)
    except Exception as e:
        pieceLogger(f"{e} \n")
        config.useClipPlayer = False


def handleClipPlayer():
    """Loads and pastes a frame from the clip player if enabled."""
    if not config.useClipPlayer:
        return
    config.clipMain.loadFrame()
    temp = config.clipMain.canvasImage.resize((config.clipMain.clipWidth, config.clipMain.clipHeight))
    temp = temp.rotate(config.clipRotate, expand=True)
    config.image.paste(temp, (config.clipXPos, config.clipYPos), mask=config.clipMain.removalMask)


# --------------------- DISTURBANCES  ---------------------
# loads the disturbance configs and calls the disturbance
# setup functions
def setupDisturbances():

    try:
        config.transformShape = workConfig.getboolean("movingpattern", "transformShape")
        transformTuples = workConfig.get("movingpattern", "transformTuples").split(",")
        config.transformTuples = tuple(float(i) for i in transformTuples)
    except Exception as e:
        print(e)
        config.transformShape = False
    # end try

    try:
        setWaveDistortionParams()
    except Exception as e:
        print(e)
        config.useWaveDistortion = False

    config.sectionDisturbance = workConfig.getboolean("movingpattern", "sectionDisturbance")
    config.doSectionDisturbance = False
    config.disturbanceConfigSets = (workConfig.get("movingpattern", "disturbanceConfigSets")).split(",")
    config.changeDisturbanceSetProb = float(workConfig.get("movingpattern", "changeDisturbanceSetProb"))
    workingDisturbanceSet = config.disturbanceConfigSets[0]
    config.skipFrames = 0
    config.skipFramesCount = 0
    setUpDisturbanceConfigs(workingDisturbanceSet)

    config.stableSectionsMin = int(workConfig.get("movingpattern", "stableSectionsMin"))
    config.stableSectionsMax = int(workConfig.get("movingpattern", "stableSectionsMax"))
    config.stableSectionsMinWidth = int(workConfig.get("movingpattern", "stableSectionsMinWidth"))
    config.stableSectionsMinHeight = int(workConfig.get("movingpattern", "stableSectionsMinHeight"))
    config.stableSectionsChangeProb = float(workConfig.get("movingpattern", "stableSectionsChangeProb"))
    setupStableSections()

    config.movingSections = []
    for _ in range(config.numberOfSections):
        section = Holder()
        config.movingSections.append(section)
    rebuildSections()


def setWaveDistortionParams():
    config.useWaveDistortion = workConfig.getboolean("movingpattern", "useWaveDistortion")
    config.waveAmplitude = float(workConfig.get("movingpattern", "waveAmplitude"))
    config.wavePeriodMod = float(workConfig.get("movingpattern", "wavePeriodMod"))
    config.wavegridspace = int(workConfig.get("movingpattern", "wavegridspace"))
    config.pNoiseMod = float(workConfig.get("movingpattern", "pNoiseMod"))
    config.waveDeformXPosRate = float(workConfig.get("movingpattern", "waveDeformXPosRate"))
    config.waveDeformXPos = 0


# loads the disturbance configs
def setUpDisturbanceConfigs(configSet):

    config.disturbanceConfigFile = workConfig.get("movingpattern", "disturbancesConfigs")
    config.disturbanceConfig = configparser.ConfigParser()
    argument = f"{config.path}/configs/{config.disturbanceConfigFile}"
    config.disturbanceConfig.read(argument)

    config.baseSectionSpeed = float(config.disturbanceConfig.get(configSet, "baseSectionSpeed"))
    config.sectionRotationRange = float(config.disturbanceConfig.get(configSet, "sectionRotationRange"))

    sectionPlacementXRange = config.disturbanceConfig.get(configSet, "sectionPlacementXRange").split(",")
    config.sectionPlacementXRange = tuple(map(lambda x: int(x), sectionPlacementXRange))

    sectionPlacementYRange = config.disturbanceConfig.get(configSet, "sectionPlacementYRange").split(",")
    config.sectionPlacementYRange = tuple(map(lambda x: int(x), sectionPlacementYRange))

    sectionWidthRange = config.disturbanceConfig.get(configSet, "sectionWidthRange").split(",")
    config.sectionWidthRange = tuple(map(lambda x: int(x), sectionWidthRange))

    sectionHeightRange = config.disturbanceConfig.get(configSet, "sectionHeightRange").split(",")
    config.sectionHeightRange = tuple(map(lambda x: int(x), sectionHeightRange))

    config.numberOfSections = int(config.disturbanceConfig.get(configSet, "numberOfSections"))
    config.sectionMovementCountMax = int(config.disturbanceConfig.get(configSet, "sectionMovementCountMax"))

    config.stopProb = float(config.disturbanceConfig.get(configSet, "stopProbMax"))
    config.sectionSpeedFactorHorizontal = float(config.disturbanceConfig.get(configSet, "sectionSpeedFactorHorizontal"))
    config.sectionSpeedFactorVertical = float(config.disturbanceConfig.get(configSet, "sectionSpeedFactorVertical"))
    config.speedDeAcceleration = float(config.disturbanceConfig.get(configSet, "speedDeAcceleration"))
    config.speedDeAccelerationBase = float(config.disturbanceConfig.get(configSet, "speedDeAcceleration"))
    config.redoSectionDisturbance = float(config.disturbanceConfig.get(configSet, "redoSectionDisturbance"))
    config.speedDeAccelerationUpperLimit = float(config.disturbanceConfig.get(configSet, "speedDeAccelerationUpperLimit"))
    config.rebuildImmediatelyAfterDone = config.disturbanceConfig.getboolean(configSet, "rebuildImmediatelyAfterDone")

    try:
        # comment:
        config.diagonalMovement = config.disturbanceConfig.getboolean(configSet, "diagonalMovement")
    except Exception as e:
        print(e)
        config.diagonalMovement = False
    # end try

    try:
        config.randomDiagonal = config.disturbanceConfig.getboolean(configSet, "randomDiagonal")
        config.diagonalFixedAngle = float(config.disturbanceConfig.get(configSet, "diagonalFixedAngle"))
    except Exception as e:
        print(e)
        config.randomDiagonal = True


def setupStableSections():
    # print("New stable sections")
    config.stableSegments = []
    n = round(random.uniform(config.stableSectionsMin, config.stableSectionsMax))
    minWidth = config.stableSectionsMinWidth
    minHeight = config.stableSectionsMinHeight
    for _ in range(n):
        xPos = round(random.uniform(0, config.canvasWidth))
        xPos2 = round(random.uniform(xPos + minWidth, config.canvasWidth))
        yPos = round(random.uniform(0, config.canvasHeight))
        yPos2 = round(random.uniform(yPos + minHeight, config.canvasHeight))
        config.stableSegments.append([xPos, yPos, xPos2, yPos2])


# changes what disturbance sections are doing
def rebuildSections():
    global config

    if random.random() < config.changeDisturbanceSetProb:
        setNumber = math.floor(random.uniform(0, len(config.disturbanceConfigSets)))
        setUpDisturbanceConfigs(config.disturbanceConfigSets[setNumber])
        # print("REBUILDSECTIONS RUNNING NOW: " + config.disturbanceConfigSets[setNumber])

    if random.random() < 0.5:
        config.speedDeAcceleration = config.speedDeAccelerationUpperLimit
    if not config.diagonalMovement:
        sectionDisturbanceDirection = 1 if random.random() < 0.5 else 0

    baseSpeed = config.baseSectionSpeed

    for i in range(config.numberOfSections):

        if i < len(config.movingSections):
            section = config.movingSections[i]
            section.sectionRotation = random.uniform(-config.sectionRotationRange, config.sectionRotationRange)
            section.sectionPlacement = [
                round(random.uniform(config.sectionPlacementXRange[0], config.sectionPlacementXRange[1])),
                round(random.uniform(config.sectionPlacementYRange[0], config.sectionPlacementYRange[1])),
            ]
            section.sectionPlacementInit = [
                section.sectionPlacement[0],
                section.sectionPlacement[1],
            ]
            section.sectionSize = [
                round(random.uniform(config.sectionWidthRange[0], config.sectionWidthRange[1])),
                round(random.uniform(config.sectionHeightRange[0], config.sectionHeightRange[1])),
            ]
            section.sectionSpeed = [
                random.uniform(-baseSpeed, baseSpeed) / config.sectionSpeedFactorHorizontal,
                random.uniform(-baseSpeed, baseSpeed) / config.sectionSpeedFactorVertical,
            ]

            if not config.diagonalMovement:
                if sectionDisturbanceDirection == 1:
                    section.sectionSpeed = [
                        random.uniform(-baseSpeed, baseSpeed) / config.sectionSpeedFactorHorizontal,
                        0,
                    ]
                else:
                    section.sectionSpeed = [
                        0,
                        random.uniform(-baseSpeed, baseSpeed) / config.sectionSpeedFactorVertical,
                    ]

            if not config.randomDiagonal and config.diagonalMovement:
                speed = random.uniform(-baseSpeed, baseSpeed) / config.sectionSpeedFactorHorizontal

                hComponent = math.cos(config.diagonalFixedAngle) * speed
                vComponent = math.sin(config.diagonalFixedAngle) * speed
                section.sectionSpeed = [hComponent, vComponent]

            section.rotationSpeed = random.uniform(-baseSpeed, baseSpeed)
            section.actionCount = 0
            section.actionCountLimit = round(random.uniform(10, config.sectionMovementCountMax))
            section.done = False
            section.stopProb = random.uniform(0, config.stopProb)

    config.drawingPrinted = False


# performs the disturbances
def disturber():
    """Applies disturbances to the canvas image based on configuration."""
    """This function applies "disturbances" to a canvas image, either by 
    disturbing specific sections or (in commented code) by repeating a pattern image. 
    It also pastes stable (undisturbed) sections back onto the canvas. Thanks AI!"""
    config.doneCount = 0

    if config.doSectionDisturbance:
        disturbSections()

        # Paste stable sections onto the canvas
        for s in config.stableSegments:
            tempCrop = config.patternImage.crop((s[0], s[1], s[2], s[3]))
            config.canvasImage.paste(tempCrop, (s[0], s[1]), tempCrop)

    # else:
    #     drawRepeatedPatternImage(config, config.patternImage)
    # config.canvasImage.paste(config.patternImage, (0, 0), config.patternImage)


def disturbSections():
    """Disturbs individual sections of the canvas image."""
    if config.skipFramesCount >= config.skipFrames:
        config.skipFramesCount = 0

        for i in range(config.numberOfSections):
            sectionParams = config.movingSections[i]

            if sectionParams.actionCount >= sectionParams.actionCountLimit:
                config.doneCount += 1
            else:
                disturbSingleSection(sectionParams)
    else:
        config.skipFramesCount += 1


def disturbSingleSection(sectionParams):
    """Disturbs a single section of the canvas image."""

    xPos = round(sectionParams.sectionPlacementInit[0])
    yPos = round(sectionParams.sectionPlacementInit[1])
    section = config.canvasImage.crop(
        (
            xPos,
            yPos,
            xPos + sectionParams.sectionSize[0],
            yPos + sectionParams.sectionSize[1],
        )
    )

    config.canvasImage.paste(
        section,
        (
            round(sectionParams.sectionPlacement[0]),
            round(sectionParams.sectionPlacement[1]),
        ),
        section,
    )

    delta = (sectionParams.actionCountLimit - sectionParams.actionCount) / sectionParams.actionCountLimit
    d = math.pow(delta, 8)
    d = 1  # what is this doing here?

    sectionParams.sectionPlacement[0] += sectionParams.sectionSpeed[0] * d
    sectionParams.sectionPlacement[1] += sectionParams.sectionSpeed[1] * d
    sectionParams.sectionSpeed[0] *= config.speedDeAcceleration
    sectionParams.sectionSpeed[1] *= config.speedDeAcceleration

    sectionParams.actionCount += 1

    if random.random() < sectionParams.stopProb:
        sectionParams.rotationSpeed = 0
    if random.random() < sectionParams.stopProb:
        sectionParams.sectionSpeed[0] = 0
    if random.random() < sectionParams.stopProb:
        sectionParams.sectionSpeed[1] = 0


# --------------------- PALETTES      ---------------------


def loadAndSetupAllPalettes():
    global workConfig
    """initial palatte setups -- needs to run after combinations are established"""
    config.palettesConfigFile = workConfig.get("movingpattern", "palettesConfigFile")

    config.paletteConfig = configparser.ConfigParser()
    argument = f"{config.path}/configs/{config.palettesConfigFile}"
    config.paletteConfig.read(argument)

    config.palettes = config.paletteConfig.get("palettesIncluded", "palettes").replace("\n", "").split(",")
    config.paletteConfigs = config.paletteConfig.get("palettesIncluded", "palettes").replace("\n", "").split(",")

    bgColorAlpha = (workConfig.get("movingpattern", "bgColorAlpha")).split(",")
    config.bgColorAlpha = list(map(lambda x: (int(x)), bgColorAlpha))

    # buildPalette(config, 0)

    config.allAvailablePalettesList = []
    config.c1 = Holder()
    config.c2 = Holder()
    config.c3 = Holder()
    config.c4 = Holder()

    for arg in config.paletteConfigs:
        loadPalette(arg)

    config.currentPaletteIndex = 0
    setPalette(config, config.currentPaletteIndex)
    # config.borderPalette = changeSinglePalette(config.currentCombinationsetIndex)


def loadPalette(palette):
    global config
    # palette = config.palettes[index]

    pieceLogger(f"Loading palette {palette}")
    c1 = Holder()
    c2 = Holder()
    c3 = Holder()
    c4 = Holder()

    _noGraysBool = config.paletteConfig.getboolean(palette, "noGrays", fallback=False)
    _noGrays = 1.0 if _noGraysBool else 0.0

    # background
    # tLimitBase = int(workConfig.get(palette, "tLimitBase"))
    c1.minHue = float(config.paletteConfig.get(palette, "c1_minHue"))
    c1.maxHue = float(config.paletteConfig.get(palette, "c1_maxHue"))
    c1.minSaturation = float(config.paletteConfig.get(palette, "c1_minSaturation"))
    c1.maxSaturation = float(config.paletteConfig.get(palette, "c1_maxSaturation"))
    c1.minValue = float(config.paletteConfig.get(palette, "c1_minValue"))
    c1.maxValue = float(config.paletteConfig.get(palette, "c1_maxValue"))
    c1.dropHueMin = float(config.paletteConfig.get(palette, "c1_dropHueMin", fallback=0))
    c1.dropHueMax = float(config.paletteConfig.get(palette, "c1_dropHueMax", fallback=0))
    c1.noGrays = _noGrays
    c1.currentColor = setCurrentColor(c1)

    # color 1
    # tLimitBase = int(config.paletteConfig.get(palette, "line_tLimitBase"))
    c2.minHue = float(config.paletteConfig.get(palette, "c2_minHue"))
    c2.maxHue = float(config.paletteConfig.get(palette, "c2_maxHue"))
    c2.minSaturation = float(config.paletteConfig.get(palette, "c2_minSaturation"))
    c2.maxSaturation = float(config.paletteConfig.get(palette, "c2_maxSaturation"))
    c2.minValue = float(config.paletteConfig.get(palette, "c2_minValue"))
    c2.maxValue = float(config.paletteConfig.get(palette, "c2_maxValue"))
    c2.dropHueMin = float(config.paletteConfig.get(palette, "c2_dropHueMin", fallback=0))
    c2.dropHueMax = float(config.paletteConfig.get(palette, "c2_dropHueMax", fallback=0))
    c2.noGrays = _noGrays
    c2.currentColor = setCurrentColor(c2)
    # color 2
    # tLimitBase = int(config.paletteConfig.get(palette, "line2_tLimitBase"))
    c3.minHue = float(config.paletteConfig.get(palette, "c3_minHue"))
    c3.maxHue = float(config.paletteConfig.get(palette, "c3_maxHue"))
    c3.minSaturation = float(config.paletteConfig.get(palette, "c3_minSaturation"))
    c3.maxSaturation = float(config.paletteConfig.get(palette, "c3_maxSaturation"))
    c3.minValue = float(config.paletteConfig.get(palette, "c3_minValue"))
    c3.maxValue = float(config.paletteConfig.get(palette, "c3_maxValue"))
    c3.dropHueMin = float(config.paletteConfig.get(palette, "c3_dropHueMin", fallback=0))
    c3.dropHueMax = float(config.paletteConfig.get(palette, "c3_dropHueMax", fallback=0))
    c3.noGrays = _noGrays
    c3.currentColor = setCurrentColor(c3)

    c4.minHue = float(config.paletteConfig.get(palette, "c4_minHue", fallback=0))
    c4.maxHue = float(config.paletteConfig.get(palette, "c4_maxHue", fallback=0))
    c4.minSaturation = float(config.paletteConfig.get(palette, "c4_minSaturation", fallback=0))
    c4.maxSaturation = float(config.paletteConfig.get(palette, "c4_maxSaturation", fallback=0))
    c4.minValue = float(config.paletteConfig.get(palette, "c4_minValue", fallback=0))
    c4.maxValue = float(config.paletteConfig.get(palette, "c4_maxValue", fallback=0))
    c4.dropHueMin = float(config.paletteConfig.get(palette, "c4_dropHueMin", fallback=0))
    c4.dropHueMax = float(config.paletteConfig.get(palette, "c4_dropHueMax", fallback=0))
    c4.noGrays = _noGrays
    c4.currentColor = setCurrentColor(c4)

    _paletteObj = Holder()
    _paletteObj.paletteName = palette
    _paletteObj.c1 = c1
    _paletteObj.c2 = c2
    _paletteObj.c3 = c3
    _paletteObj.c4 = c4
    _paletteObj.noGrays = _noGrays

    # print(f"Palette Loaded: {palette}")

    config.allAvailablePalettesList.append(_paletteObj)


def getPaletteObjectByName(_name):
    for _n in config.allAvailablePalettesList:
        if _n.paletteName == _name:
            return _n


def changeSinglePalette(index=0):
    # pieceLogger(f"changeSinglePalette  {index}")
    paletteObj = getPaletteObjectByName(config.combinationSets[config.currentCombinationsetIndex].palettes[index])
    _paletteObjLocal = Holder()
    _paletteObjLocal.paletteName = config.combinationSets[config.currentCombinationsetIndex].palettes[index]
    _paletteObjLocal.c1 = copy(paletteObj.c1)
    _paletteObjLocal.c1.currentColor = copy(paletteObj.c1.currentColor)
    _paletteObjLocal.c2 = copy(paletteObj.c2)
    _paletteObjLocal.c2.currentColor = copy(paletteObj.c2.currentColor)
    _paletteObjLocal.c3 = copy(paletteObj.c3)
    _paletteObjLocal.c3.currentColor = copy(paletteObj.c3.currentColor)
    _paletteObjLocal.c4 = copy(paletteObj.c4)
    _paletteObjLocal.c4.currentColor = copy(paletteObj.c4.currentColor)

    _paletteObjLocal.c1.currentColor = setCurrentColor(paletteObj.c1, 0, 0, round(random.uniform(config.bgColorAlpha[0], config.bgColorAlpha[1])))
    _paletteObjLocal.c2.currentColor = setCurrentColor(paletteObj.c2)
    _paletteObjLocal.c3.currentColor = setCurrentColor(paletteObj.c3)
    _paletteObjLocal.c4.currentColor = setCurrentColor(paletteObj.c4)
    _paletteObjLocal.noGrays = paletteObj.noGrays
    return _paletteObjLocal


def setCurrentColor(palettObjValsRef, dropHueMin=0, dropHueMax=0, alpha=255):
    return colorutils.getRandomColorHSV(
        palettObjValsRef.minHue,
        palettObjValsRef.maxHue,
        palettObjValsRef.minSaturation,
        palettObjValsRef.maxSaturation,
        palettObjValsRef.minValue,
        palettObjValsRef.maxValue,
        palettObjValsRef.dropHueMin,
        palettObjValsRef.dropHueMax,
        alpha,
        config.brightness,
        palettObjValsRef.noGrays,
    )


def setPalette(config, index=0):
    paletteObj = getPaletteObjectByName(config.combinationSets[config.currentCombinationsetIndex].palettes[index])
    # print(f"Setting a new palette:  {paletteObj.paletteName}")
    config.c1.bgColor = setCurrentColor(paletteObj.c1, 0, 0, round(random.uniform(config.bgColorAlpha[0], config.bgColorAlpha[1])))
    config.c1.currentColor = setCurrentColor(paletteObj.c1)
    config.c2.currentColor = setCurrentColor(paletteObj.c2)
    config.c3.currentColor = setCurrentColor(paletteObj.c3)
    config.c4.currentColor = setCurrentColor(paletteObj.c4)

    # if zero palette mixing is desired, force the patterns to rebuild
    # this is a bit of an extreme but was having trouble preventing the
    # palette mixing and making unpleasant combinations

    # if config.changePaletteWhenChangingPatternProb == 0.0:
    # buildPatternSequence(config)


def selectNewPalette(_setPalette=True):
    # config.currentPaletteIndex = math.floor(random.uniform(0, len(config.palettes)))
    config.currentPaletteIndex = math.floor(random.uniform(0, len(config.combinationSets[config.currentCombinationsetIndex].palettes)))
    # if config.currentPaletteIndex == len(config.palettes):
    #     config.currentPaletteIndex = 0

    pieceLogger(f"selectNewPalette: Choosing a palette: {config.combinationSets[config.currentCombinationsetIndex].palettes[config.currentPaletteIndex]}", 2, True)
    setPalette(config, config.currentPaletteIndex)

    if _setPalette:
        rebuildPatterns()
        resetPatternBlocks()
        # resetCrossFader()

    # if random.random() < config.probPatternsRebuildAfterNewPalette:
    #     rebuildPatterns()
    # else:
    #     resetPatternBlocks()
    #     resetCrossFader()


# --------------------- PATTERNS     ---------------------


def loadAndSetupPatterns():
    # config.patterns = workConfig.get("movingpattern", "patterns").split(",")
    # config.dominantPatterns =  workConfig.get("movingpattern", "dominantPatterns", fallback="").split(",")
    # loadConfigValue(config, workConfig, "movingpattern", "dominantPatternProb", 0, float)

    loadConfigValue(config, workConfig, "movingpattern", "patternModelVariations", True, bool)
    loadConfigValue(config, workConfig, "movingpattern", "patternModel", None, str)

    # patternSequence = workConfig.get("movingpattern", "patternSequence").split(",")
    # config.patternSequence = []

    loadConfigValue(config, workConfig, "movingpattern", "patternSequenceMax", 2, int)
    loadConfigValue(config, workConfig, "movingpattern", "patternSequenceMin", 5, int)

    config.rotateAltBlock = 0

    # --------------------- PATTERN CHANGE   ---------------------
    # higher = more variation in patterns
    # e.g. .2 is 20% chance each new block will change to a
    # new pattern

    loadConfigValue(config, workConfig, "movingpattern", "rebuildPatternProbability", 0.0, float)
    loadConfigValue(config, workConfig, "movingpattern", "probPatternsRebuildAfterNewPalette", 1.0, float)
    loadConfigValue(config, workConfig, "movingpattern", "changePaletteWhenRebuildProb", 0.0, float)
    loadConfigValue(config, workConfig, "movingpattern", "changePaletteAnytimeProb", 0.0, float)
    loadConfigValue(config, workConfig, "movingpattern", "patternChangeWhenBuilding", 0.0, float)
    loadConfigValue(config, workConfig, "movingpattern", "changeFullPaletteWhenChangingPatternProb", 0.0, float)
    loadConfigValue(config, workConfig, "movingpattern", "changeEachblockWhenChangingPatternProb", 1.0, float)
    loadConfigValue(config, workConfig, "movingpattern", "changePaletteWhenChangingPatternProb", 0.0, float)
    loadConfigValue(config, workConfig, "movingpattern", "altColoringProb", 0.0, float)
    loadConfigValue(config, workConfig, "movingpattern", "popRandomColorProb", 0.8, float)
    loadConfigValue(config, workConfig, "movingpattern", "blockSizeChangeProb", 0.0, float)
    loadConfigValue(config, workConfig, "movingpattern", "blockSizeChangeAlwaysUseMax", False, bool)

    try:
        ringsRange = workConfig.get("movingpattern", "ringsRange").split(",")
        stepsRange = workConfig.get("movingpattern", "stepsRange").split(",")
        config.numScaleRows = int(workConfig.get("movingpattern", "numScaleRows"))
        config.stepsRange = tuple(map(lambda x: int(x), stepsRange))
        config.ringsRange = tuple(map(lambda x: int(x), ringsRange))
    except Exception as e:
        pieceLogger(e, 1)
        config.stepsRange = (1, 1)
        config.ringsRange = (1, 1)
        config.numScaleRows = config.numShingleRows

    loadConfigValue(config, workConfig, "movingpattern", "patternOrientation", 0, float)
    loadConfigValue(config, workConfig, "movingpattern", "numRows", 5, int)
    loadConfigValue(config, workConfig, "movingpattern", "numRowsRandomize", False, bool)

    # affects patterns to use just lines w/o fills
    loadConfigValue(config, workConfig, "movingpattern", "linesOnly", False, bool)

    # try:
    #     config.borderPattern = workConfig.get("movingpattern", "borderPattern")
    #     config.useBorderPattern = workConfig.getboolean("movingpattern", "useBorderPattern")
    # except Exception as e:
    #     print(e)
    #     config.borderPattern = config.patterns[0]
    #     config.useBorderPattern = False
    # end try

    config.waveScaleRings = round(random.uniform(config.ringsRange[0], config.ringsRange[1]))
    config.waveScaleSteps = round(random.uniform(config.stepsRange[0], config.stepsRange[1]))
    # print(config.waveScaleRings, config.waveScaleSteps)
    # end try

    # for the randomizer
    loadConfigValue(config, workConfig, "movingpattern", "usePixelSortRandomize", True, bool)
    loadConfigValue(config, workConfig, "movingpattern", "randomBlockProb", 0.0, float)
    loadConfigValue(config, workConfig, "movingpattern", "randomBlockWidth", 10, int)
    loadConfigValue(config, workConfig, "movingpattern", "randomBlockHeight", 10, int)
    loadConfigValue(config, workConfig, "movingpattern", "decoBoxBandWidth", 10, int)

    config.diamondUseTriangles = False
    loadConfigValue(config, workConfig, "movingpattern", "diamondStep", 1, int)
    loadConfigValue(config, workConfig, "movingpattern", "minnumConcentricBoxes", 1, int)
    loadConfigValue(config, workConfig, "movingpattern", "maxnumConcentricBoxes", 8, int)
    loadConfigValue(config, workConfig, "movingpattern", "numShingleRows", 1, int)
    loadConfigValue(config, workConfig, "movingpattern", "amplitude", 1, int)
    loadConfigValue(config, workConfig, "movingpattern", "amplitude2", 1, int)
    loadConfigValue(config, workConfig, "movingpattern", "shingleVariation", False, bool)
    loadConfigValue(config, workConfig, "movingpattern", "shingleVariationRange", 1, int)
    config.shingleVariationAmount = config.shingleVariationRange

    loadConfigValue(config, workConfig, "movingpattern", "numDotRows", 1, int)
    loadConfigValue(config, workConfig, "movingpattern", "speedFactor", 0.0, float)
    loadConfigValue(config, workConfig, "movingpattern", "phaseFactor", 0.0, float)
    loadConfigValue(config, workConfig, "movingpattern", "xSpeed", 0.0, float)
    loadConfigValue(config, workConfig, "movingpattern", "ySpeed", 0.0, float)
    config.ySpeedInit = config.ySpeed

    loadConfigValue(config, workConfig, "movingpattern", "lineDiff", 1, int)
    loadConfigValue(config, workConfig, "movingpattern", "useDoubleLine", False, bool)
    loadConfigValue(config, workConfig, "movingpattern", "randomizeSpeed", False, bool)

    # used in pattern_blocks code
    loadConfigValue(config, workConfig, "movingpattern", "steps", 1, int)
    loadConfigValue(config, workConfig, "movingpattern", "steps2", 1, int)

    loadConfigValue(config, workConfig, "movingpattern", "xIncrementer", 1, int)
    loadConfigValue(config, workConfig, "movingpattern", "yIncrementer", 1, int)

    config.altLineColoring = False
    stepsRange = workConfig.get("movingpattern", "stepsRange").split(",")

    loadAndSetCombinations()


def loadAndSetCombinations():
    config.combinationSets = []
    combinationSets = workConfig.get("movingpattern", "combinationSets").replace("\n", "").split(",")
    config.changeCombinationAnytimeProb = float(workConfig.get("movingpattern", "changeCombinationAnytimeProb", fallback=0))
    for combinationSetName in combinationSets:
        comboSet = CombinationSet(combinationSetName)
        comboSet.patterns = workConfig.get(combinationSetName, "patterns").replace("\n", "").split(",")
        comboSet.palettes = workConfig.get(combinationSetName, "palettes").replace("\n", "").split(",")
        comboSet.dominantPatterns = workConfig.get(combinationSetName, "dominantPatterns", fallback="").replace("\n", "").split(",")
        comboSet.dominantPatternProb = float(workConfig.get(combinationSetName, "dominantPatternProb", fallback=0))
        comboSet.borderPattern = workConfig.get(combinationSetName, "borderPattern", fallback="")
        comboSet.useBorderPattern = workConfig.getboolean(combinationSetName, "useBorderPattern", fallback=False)
        comboSet.altColoringProb = float(workConfig.get(combinationSetName, "altColoringProb", fallback=config.altColoringProb))
        comboSet.popRandomColorProb = float(workConfig.get(combinationSetName, "popRandomColorProb", fallback=config.popRandomColorProb))

        comboSet.usePolygonOverlay = workConfig.getboolean(combinationSetName, "usePolygonOverlay", fallback=config.usePolygonOverlay)
        comboSet.tileOverlayGridProb = float(workConfig.get(combinationSetName, "tileOverlayGridProb", fallback=config.tileOverlayGridProb))
        comboSet.polyOverlayMode = workConfig.get(combinationSetName, "polyOverlayMode", fallback=config.polyOverlayMode)

        comboSet.patternsInBands = workConfig.getboolean(combinationSetName, "patternsInBands", fallback=False)
        comboSet.altBlockRotation = workConfig.getboolean(combinationSetName, "altBlockRotation", fallback=True)

        config.combinationSets.append(comboSet)
    config.currentCombinationsetIndex = 0


def handleChangeCurrentCominationSet():
    if random.random() < config.changeCombinationAnytimeProb and config.fader.fadingDone:
        config.currentCombinationsetIndex = math.floor(random.uniform(0, len(config.combinationSets)))
        # {config.combinationSets[config.currentCombinationsetIndex]}
        pieceLogger(f"=====> Combo changed to {config.combinationSets[config.currentCombinationsetIndex].name} (index: {config.currentCombinationsetIndex})\n", 2, True)
        selectNewPalette()
        # rebuildPatterns()


def resetPatternBlocks():

    tempPalette = changeSinglePalette(config.currentPaletteIndex)

    for i in range(config.totalSlots):
        _patternBlock = config.patternSequence[i]
        _patternBlock.hasBeenPainted = False
        _patternBlock.tempPalette = tempPalette

        if random.random() > config.changeEachblockWhenChangingPatternProb:
            # _patternBlock.tempPalette = config.allAvailablePalettesList[config.currentPaletteIndex]
            _patternBlock.tempPalette = getTempPalette(config)
        # else :
        #     _patternBlock.tempPalette = getPaletteObjectByName(config.combinationSets[config.currentCombinationsetIndex].palettes[config.currentPaletteIndex])

        config.patternSequence[i] = _patternBlock


def buildPatternSequence(config):
    pieceLogger("Building new pattern sequence", 0)
    config.patternSequence = []
    config.usedPatterns = []

    if random.random() < config.blockSizeChangeProb:
        if config.blockSizeChangeAlwaysUseMax:
            config.blockWidth = config.blockWidthMax
            config.blockHeight = config.blockWidthMax
        else:
            config.blockWidth = round(random.uniform(config.blockWidthMin, config.blockWidthMax))
            config.blockHeight = config.blockWidth
    else:
        config.blockWidth = config.blockWidthMin
        config.blockHeight = config.blockWidthMin

    config.blockImage = Image.new("RGBA", (config.blockWidth, config.blockHeight))
    config.blockDraw = ImageDraw.Draw(config.blockImage)

    config.patternBlockCols = round(config.canvasWidth / config.blockWidth)
    config.patternBlockRows = round(config.canvasHeight / config.blockHeight)

    # considering making this be an option to fit exactly the width - i.e. choose the number of columns
    # rather than width or an alogrithm to do the fitting - the problem is that then you lose the
    # ragged edges which are a nice trace of the previous state
    # print(f"config.blockWidth {config.blockWidth} config.patternBlockCols {config.patternBlockCols}")

    config.totalSlots = config.patternBlockRows * config.patternBlockCols
    config.altLineColoring = random.random() < config.combinationSets[config.currentCombinationsetIndex].altColoringProb
    config.popRandomColorProb = random.random() < config.combinationSets[config.currentCombinationsetIndex].popRandomColorProb

    # print(config.altLineColoring)
    config.numConcentricBoxes = round(random.uniform(config.minnumConcentricBoxes, config.maxnumConcentricBoxes))

    pattern_blocks_v5.floralConfig(config)
    generatePatternSequence(config)

    # _print_pattern_sequence(config)
    config.borderDrawn = False
    config.initPatternBuild = False


def chooseAPattern():
    _patterns = config.combinationSets[config.currentCombinationsetIndex].patterns
    _dominantPatterns = config.combinationSets[config.currentCombinationsetIndex].dominantPatterns
    _dominantPatternProb = config.combinationSets[config.currentCombinationsetIndex].dominantPatternProb

    _patternSelected = _patterns[math.floor(random.uniform(0, len(_patterns)))]
    if random.random() < _dominantPatternProb:
        _patternSelected = _dominantPatterns[math.floor(random.uniform(0, len(_dominantPatterns)))]
    return _patternSelected


# this really needs to change to be more readable and predictable ....
# there are n number of slots, just fill each one and change randomly etc
# as they all get filled up
def generatePatternSequence(config):
    _baseProb = config.patternChangeWhenBuilding * config.totalSlots / 100
    _patternSelected = chooseAPattern()
    _tempPalette = getTempPalette(config)
    _iterCount = 0
    config.initPatternBuild = True
    combo = config.combinationSets[config.currentCombinationsetIndex]
    config.useBorderPattern = combo.useBorderPattern
    config.borderPattern = combo.borderPattern
    config.usePolygonOverlay = combo.usePolygonOverlay
    config.polyOverlayMode = combo.polyOverlayMode
    config.tileOverlayGridProb = combo.tileOverlayGridProb
    config.patternsInBands = combo.patternsInBands

    def add_pattern_block(c, r):
        nonlocal _patternSelected, _tempPalette, _iterCount
        if random.random() < _baseProb:
            _patternSelected = chooseAPattern()
            _tempPalette = getTempPalette(config)
        _rotate = 0 if _patternSelected in (["shingles", "fishScales", "balls", "petals"]) else random.randint(0, 1)
        if not combo.altBlockRotation:
            _rotate = 0
        _position = _iterCount
        _pattern = _patternSelected
        if config.useBorderPattern and (c == 0 or r == 0 or c == (config.patternBlockCols - 1) or r == (config.patternBlockRows - 1)):
            _pattern = config.borderPattern
        _patternBlock = PatternBlock()
        _patternBlock.pattern = _pattern
        _patternBlock.position = _position
        _patternBlock.rotate = _rotate
        _patternBlock.tempPalette = _tempPalette
        _patternBlock.col = c
        _patternBlock.row = r
        _patternBlock.rePainting = _patternSelected in [
            "randomizer3",
            "randomizer2",
            "randomizer",
            "diamond",
        ]
        _patternBlock.isBorder = config.useBorderPattern and (c == 0 or r == 0 or c == (config.patternBlockCols - 1) or r == (config.patternBlockRows - 1))
        config.patternSequence.append(_patternBlock)
        _iterCount += 1

    if config.patternsInBands:
        for r in range(config.patternBlockRows):
            for c in range(config.patternBlockCols):
                add_pattern_block(c, r)
    else:
        for c in range(config.patternBlockCols):
            for r in range(config.patternBlockRows):
                add_pattern_block(c, r)


def getTempPalette(config):
    if random.SystemRandom().random() > config.changePaletteWhenChangingPatternProb:
        # return config.allAvailablePalettesList[config.currentPaletteIndex]
        return getPaletteObjectByName(config.combinationSets[config.currentCombinationsetIndex].palettes[config.currentPaletteIndex])
    if random.SystemRandom().random() <= config.changeFullPaletteWhenChangingPatternProb:
        # print("seledtNewPalette called from: getTempPalette()")
        selectNewPalette(False)
    return changeSinglePalette(config.currentPaletteIndex)


def _print_pattern_sequence(config):
    print("----------------------------------------------")
    print(("New sequence"))
    print(f"config.totalSlots {config.totalSlots}")
    for s in config.patternSequence:
        print(f"{s[0]} {s[1]} {s[3].linecolOverlay.currentColor} {s[4]} ")
    print(f"Using start pattern {config.patternModel}")
    print("----------------------------------------------")


def rebuildPatterns(arg=0):
    pieceLogger("rebuildPattern called")

    if config.numRowsRandomize:
        rowsAndDotsSettings()

    # if random.random() < config.changePaletteWhenRebuildProb:
    #     pieceLogger("selectNewPalette called from: rebuildPatterns()")
    #     selectNewPalette()

    buildPatternSequence(config)

    setupStableSections()

    rebuildSections()

    resetCrossFader(False)


def resetCrossFader(_useConfigImage=True):
    # os.system('afplay /System/Library/Sounds/Sosumi.aiff')
    # print(f"DOING NOW  {config.faderDoingRefreshCount}")
    # os.system('say "NOW" &')

    pieceLogger(f"resetCrossFader called : {_useConfigImage}")
    config.repeatDrawingMode = 1
    config.fader.fadingDone = False
    config.doTransition = True
    if _useConfigImage:
        config.fader.startingImage = config.image.copy()
    else:
        # config.fader.startingImage = config.canvasImage.copy()
        config.fader.startingImage = config.compositeImage.copy()

    # _tempImg  =  Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    # _tempDraw = ImageDraw.Draw(_tempImg)
    # _tempDraw.rectangle((0,0,500,500), fill = (255,0,0,255))
    # config.canvasImage.paste(_tempImg, (0,0), _tempImg)

    # NOT WORKING

    # config.fader.endImage = config.canvasImage.copy()
    # config.fader.crossFadeImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))

    config.fader.doingRefreshCount = config.faderDoingRefreshCount
    config.fader.initialized = True
    # config.debugPause = True


def rowsAndDotsSettings():

    config.numRows = round(random.uniform(1, 2))
    config.numShingleRows = round(random.uniform(1, 2))
    config.numScaleRows = round(random.uniform(1, 2))
    dotRows = [1, 2, 4]
    config.numDotRows = dotRows[round(random.uniform(0, 2))]
    config.waveScaleRings = round(random.uniform(config.ringsRange[0], config.ringsRange[1]))
    config.waveScaleSteps = round(random.uniform(config.stepsRange[0], config.stepsRange[1]))


# --------------------- LOOP ACTIONS  ---------------------


def iterate():
    """Performs a single iteration of the animation."""
    global config

    if config.debugPause:
        config.directorController.slotRate = 2.0
    handleChangeCurrentCominationSet()
    handlePaletteChanges()
    updateBackgroundColor()
    handleClipPlayer()
    drawAndProcessPattern()
    handleDisturbances()
    handleFilterRemapping()
    handleFadingAndRebuild()
    handlePatternRebuild()
    handleSectionDisturbances()
    handleShingleVariation()
    drawBackgroundAndPasteImage()
    renderComposite()
    if config.saveImages:
        saveImageIfDone()


def drawRepeatedPatternImage(config, canvasImage):
    """Draws the repeated pattern image onto the canvas."""
    _counter = 0
    extraOverlapx = 0
    extraOverlapy = 0
    for i in range(config.totalSlots):
        _patternBlock = config.patternSequence[i]
        # This sets the block image for each unit
        if config.patternModelVariations:
            drawBlockWithPattern(config, i)

        if _patternBlock.hasBeenPainted == False:
            drawIndividualBlock(config, canvasImage, _patternBlock.col, _patternBlock.row, i, extraOverlapx, extraOverlapy)
            if not _patternBlock.rePainting or _patternBlock.isBorder:
                _patternBlock.hasBeenPainted = True

    updateFaderEndpoint()


def drawIndividualBlock(config, canvasImage, c, r, _counter, extraOverlapx, extraOverlapy):
    """Draws a single block of the pattern."""

    _temp = config.blockImage.copy()
    # _temp = Image.new("RGBA",(config.blockWidth, config.blockHeight))
    # _tempDraw = ImageDraw.Draw(_temp)
    # _temp.paste(config.blockImage, (0,0), config.blockImage)
    # _tempDraw.rectangle((0,0,10,10), fill =(random.randint(0,255),random.randint(0,255),random.randint(0,255),255))
    # _temp = _temp.crop((0,0,20,20))
    # disabling for a moment 2023-04-01

    if config.patternModel not in ["ropePattern", "littleCones"]:
        _temp = _temp.rotate(90)
    # if config.patternModel == "circlesPacked":
    #     extraOverlapx = round(config.blockWidth / 8)
    #     extraOverlapy = round(config.blockWidth / 8)

    if config.patternModel in ["waveScales", "shellScales"]:
        _temp = _temp.rotate(-180)

    if c % 2 != 0 and config.rotateAltBlock == 1:
        _temp = _temp.rotate(-90)

    # forces the patterns to align to a certain rotation
    # useful instead of rotation the whole piece etc
    if config.patternOrientation != 0:
        _temp = _temp.rotate(config.patternOrientation)

    if config.blockRotation != 0:
        _temp = _temp.rotate(config.blockRotation)

    # _tempDraw = ImageDraw.Draw(canvasImage)
    # _tempDrawB = ImageDraw.Draw(_temp)

    _xPos = c * config.blockWidth - c * extraOverlapx
    _yPos = r * config.blockHeight - r * extraOverlapy

    canvasImage.paste(_temp, (_xPos, _yPos), _temp)
    config.canvasImage.paste(_temp, (_xPos, _yPos), _temp)


def updateFaderEndpoint():
    # config.patternImage = canvasImage.copy()
    config.fader.endImage = config.patternImage.copy()
    # config.fader.endImage = config.canvasImage.copy()


# ------------------------------------------------
def drawBlockWithPattern(config, _counter):
    """Applies pattern variations based on the pattern sequence."""
    _patternBlock = config.patternSequence[_counter]
    config.patternModel = _patternBlock.pattern
    config.rotateAltBlock = _patternBlock.rotate
    if not _patternBlock.hasBeenPainted:
        func = eval(f"pattern_blocks_v5.{_patternBlock.pattern}")
        func(config, _patternBlock.tempPalette)

    # if not _patternBlock.rePainting:
    #     _patternBlock.hasBeenPainted = True


def updateBackgroundColor():
    """Updates the background color based on current palette."""
    config.bgColor = tuple(round(a * config.brightness) for a in config.c1.currentColor)


def handlePaletteChanges():
    if random.random() < config.changePaletteAnytimeProb and config.fader.fadingDone:
        print("selectPaletted called from handlePaletteChanges()")
        selectNewPalette(True)
        # rebuildSections()
        # resetCrossFader(False)


def drawAndProcessPattern():
    """Draws and processes the repeated pattern image."""
    drawRepeatedPatternImage(config, config.patternImage)

    # if config.repeatDrawingMode == 1:
    #     redrawAndLoadImage(config)

    if random.random() < 0.005 and config.usePixelSortRandomize:
        config.usePixelSort = not config.usePixelSort  # Toggle pixel sort


def redrawAndLoadImage(config):
    """Redraws the pattern and optionally loads a new image."""

    if random.random() < config.loadAnImageProb:
        loadImageForBase()
    else:
        drawRepeatedPatternImage(config, config.canvasImage)

    config.repeatDrawingMode = 0


def handleDisturbances():
    """Handles various image disturbances and effects."""
    if config.randomizeSpeed:
        if random.random() < 0.03:
            config.ySpeed = config.ySpeedInit
        if random.random() < 0.1:
            config.ySpeed = 0

    if random.random() < 0.0005:
        config.triangles = True

    if random.random() < 0.01:
        config.triangles = False

    if config.sectionDisturbance and config.fader.fadingDone:
        disturber()

    if config.useBlurSection:
        cp = config.canvasImage.copy()
        mask_blur = config.mask.filter(ImageFilter.GaussianBlur(config.mask_blur_amt))
        cp_blur = cp.filter(ImageFilter.GaussianBlur(config.cp_blur_amt))
        config.canvasImage = Image.composite(cp_blur, config.canvasImage, mask_blur)


def handleFilterRemapping():
    """Handles filter remapping if enabled."""
    # print(f"config.useFilters {config.useFilters}  config.filterRemapping {config.filterRemapping} config.filterRemappingProb {config.filterRemappingProb}")
    if random.random() < config.filterRemappingProb and (config.useFilters and config.filterRemapping):
        remapFilter(config)


def remapFilter(config):
    """Remaps the filter block section."""
    config.filterRemap = True
    startX = round(random.uniform(0, config.filterRemapRangeX))
    startY = round(random.uniform(0, config.filterRemapRangeY))
    endX = round(random.uniform(config.filterRemapMinHoriSize, config.filterRemapMaxHoriSize))
    endY = round(random.uniform(config.filterRemapMinVertSize, config.filterRemapMaxVertSize))
    config.remapImageBlockSection = [startX, startY, startX + endX, startY + endY]
    config.remapImageBlockDestination = [startX, startY]


def handleFadingAndRebuild():
    """Handles image fading and pattern rebuilding."""
    if config.fader.fadingDone:
        # config.fader.fadingDone = False
        # config.fader.startingImage = config.canvasImage

        config.fader.doingRefreshCount = 0
        if config.doneCount >= config.numberOfSections and config.rebuildImmediatelyAfterDone:
            config.doSectionDisturbance = False
            pieceLogger("rebuildPatterns called after fading done")
            rebuildPatterns()

    if random.random() < config.resetOverlayProbability and config.usePolygonOverlay:
        loadPolyOverlaybaseValues()


def saveImageIfDone():
    """Saves the image if all sections are done and not already saved."""
    if config.doneCount >= config.numberOfSections and not config.drawingPrinted:
        config.fader.doingRefreshCount = 40
        config.drawingPrinted = True
        currentTime = time.time()
        baseName = config.outPutPath + str(currentTime)
        if not config.useDrawingPoints:
            writeImage(baseName, renderImage=config.canvasImage)


def handlePatternRebuild():
    """Handles rebuilding the pattern based on probability."""
    if random.random() < config.rebuildPatternProbability and config.fader.fadingDone:
        # config.doSectionDisturbance = False
        # print("\nrebuildPatterns called after fading done 2")
        rebuildPatterns()


def handleSectionDisturbances():
    """Handles random overlay repetition disturbance."""
    if random.random() < config.redoSectionDisturbance and config.sectionDisturbance and config.fader.fadingDone:
        config.doSectionDisturbance = True
        rebuildSections()


def handleShingleVariation():
    """Handles shingle variation if enabled."""
    if config.shingleVariation and random.random() < config.redoSectionDisturbance:
        config.shingleVariationAmount = round(random.uniform(0, config.shingleVariationRange))
        rebuildSections()


def drawBackgroundAndPasteImage():
    """Draws the background and pastes the main image."""
    if config.doTransition:

        config.fader.fadeIn(config)
        config.compositeImage.paste(config.fader.crossFadeImage, (0, 0), config.fader.crossFadeImage)

    elif config.sectionDisturbance:
        config.compositeImage.paste(config.canvasImage, (0, 0), config.canvasImage)

    """Transforms and renders the final image."""
    if config.transformShape:
        config.compositeImage = transformImage(config.compositeImage)

    if config.canvasRotation != 0:
        config.compositeImage = config.compositeImage.rotate(config.canvasRotation, 3, True)
        config.compositeImage = ImageEnhance.Contrast(config.compositeImage).enhance(1.20)

    if config.useWaveDistortion:
        config.compositeImage = ImageOps.deform(config.compositeImage, WaveDeformer())
        config.waveDeformXPos += config.waveDeformXPosRate
        if config.waveDeformXPos > config.screenWidth:
            config.waveDeformXPos = 0


def renderComposite():
    """FINAL RENDERING CALL"""
    if config.useDrawingPoints == True:
        config.panelDrawing.canvasToUse = config.compositeImage
        config.panelDrawing.render()
    else:
        if config.usePolygonOverlay:
            config.compositeImage = shapeOverLayFunction(config.compositeImage)

        config.destinationImage.paste(config.compositeImage, (round(config.imageXPOS), round(config.imageYPOS)), config.compositeImage)
        config.destinationImage.paste(config.compositeImage, (round(config.imageXPOS - config.canvasWidth), round(config.imageYPOS)), config.compositeImage)
        
        config.imageXPOS += config.XPOSSpeed
        # config.imageYPOS += config.YPOSSpeed

        if config.imageXPOS >= config.canvasWidth:
            config.imageXPOS = 0

        if config.imageYPOS >= config.canvasHeight:
            config.imageYPOS = 0
        # config.destinationImage.paste(config.compositeImage, (0, 0), config.compositeImage)

        # # uncomment for all temp canvas layers to show
        if config.setupDeBug:
            showDebugCanvases(config)
        config.render(config.destinationImage, 0, 0)


def showDebugCanvases(config):
    _w = config.canvasWidth
    _h = config.canvasHeight

    patternCoord = (1 * (_w + 20), 0)
    canvasImageCoord = (1 * (_w + 20), _h * 2 + 40)
    startingImageCoord = (0, _h + 20)
    crossFadeImageCoord = (1 * (_w + 20), _h + 20)
    endImageCoord = (2 * (_w + 20), _h + 20)

    hilitCor = patternCoord
    hilit = (hilitCor[0] - 1, hilitCor[1] - 1, hilitCor[0] + _w + 1, hilitCor[1] + _h + 1)
    config.destinationImageDraw.rectangle(hilit, fill=None, outline=(255, 0, 255, 200))
    hilitCor = canvasImageCoord
    hilit = (hilitCor[0] - 1, hilitCor[1] - 1, hilitCor[0] + _w + 1, hilitCor[1] + _h + 1)
    config.destinationImageDraw.rectangle(hilit, fill=None, outline=(0, 255, 0, 200))

    config.destinationImage.paste(config.patternImage, patternCoord, config.patternImage)
    config.destinationImage.paste(config.canvasImage, canvasImageCoord, config.canvasImage)
    config.destinationImage.paste(config.fader.startingImage, startingImageCoord, config.fader.startingImage)
    config.destinationImage.paste(config.fader.crossFadeImage, crossFadeImageCoord, config.fader.crossFadeImage)
    config.destinationImage.paste(config.fader.endImage, endImageCoord, config.fader.endImage)


# ----------------- OVERLAY ACTIONS  ---------------------


def shapeOverLayFunction(temp1):
    temp2 = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    temp2Draw = ImageDraw.Draw(temp2)

    if not config.useOverlayTileGrid:
        config.polyOverlay.stepTransition()
        polyFillaList = [int(a) for a in (config.polyOverlay.currentColor)]
        polyFilla = (polyFillaList[0], polyFillaList[1], polyFillaList[2], config.poly_alpha)
        # actual shape
        if random.random() < config.polyOverlayChangeProb:
            config.polyBase[0][0] += random.uniform(-3, 3)
            config.polyBase[1][0] += random.uniform(-3, 3)
            config.polyBase[2][0] += random.uniform(-3, 3)
            config.polyBase[3][0] += random.uniform(-3, 3)
            config.polyBase[4][0] += random.uniform(-3, 3)
        poly = tuple(map(lambda x: (tuple(x)), config.polyBase))

        # outline outside shape
        # poly = ((11,20),(24,160),(300,160),(300,200),(0,200),(0,0),(300,0),(200,12),(20,20))

        # polyFilla =  config.linecolOverlay.currentColor
        # polyFilla =  config.colOverlay.currentColor
        # polyFilla =  (config.colOverlay.currentColor[1], config.colOverlay.currentColor[0],config.colOverlay.currentColor[3], config.poly_alpha)
        # polyFilla = (config.colOverlay.currentColor[0], config.colOverlay.currentColor[1], config.colOverlay.currentColor[2], 1)

        temp2Draw.polygon(poly, fill=polyFilla)
        temp1.paste(temp2, (0, 0), temp2)
    else:
        _count = 0
        _overlayFill = tuple(round(a * config.brightness) for a in config.c3.currentColor)
        for _r in range(config.rows):
            for _c in range(config.cols):
                _x0 = _c * config.tileSizeWidth
                _y0 = _r * config.tileSizeHeight
                _x1 = _x0 + config.tileSizeWidth
                _y1 = _y0 + config.tileSizeHeight
                if _count in config.tileOverlayGrid:
                    temp2Draw.rectangle((_x0, _y0, _x1, _y1), fill=_overlayFill)
                # else :
                #     temp2Draw.rectangle((_x0,_y0,_x1,_y1), fill=(200,0,0,0))
                _count += 1

        match (config.polyOverlayMode):
            case "overaly":
                temp1 = ImageChops.overlay(temp1, temp2)
            case "subtract_modulo":
                temp1 = ImageChops.subtract_modulo(temp1, temp2)
            case "soft_light":
                temp1 = ImageChops.soft_light(temp1, temp2)
            case "lighter":
                temp1 = ImageChops.lighter(temp1, temp2)

        if random.random() < config.polyOverlayChangeProb:
            generateOverlayTiles()
        # temp1.paste(temp2, (0, 0), temp2)
    return temp1


def loadPolyOverlaybaseValues():
    try:
        _polyBaseVals = workConfig.get("movingpattern", "polyBaseVals").split("|")
        # print(_polyBaseVals)
        config.polyBase = []
        for _a in _polyBaseVals:
            _ps = list(map(lambda x: int(x), _a.split(",")))
            config.polyBase.append(_ps)
    except Exception as e:
        pieceLogger(e)
        config.polyBase = []


def generateOverlayTiles():
    config.tileOverlayGrid = [0]
    for _v in range(config.rows * config.cols):
        if random.random() < config.tileOverlayGridProb:
            config.tileOverlayGrid.append(_v)


def setupPolyOverlay():  # sourcery skip: extract-method
    config.usePolygonOverlay = False
    try:
        config.polyOverlay = ColorOverlay()
        config.polyOverlay.randomSteps = True
        config.polyOverlay.timeTrigger = True
        config.polyOverlay.tLimitBase = int(workConfig.get("movingpattern", "poly_tLimitBase"))
        config.polyOverlay.tLimit = int(workConfig.get("movingpattern", "poly_tLimit"))
        config.polyOverlay.steps = int(workConfig.get("movingpattern", "poly_steps"))
        config.usePolygonOverlay = workConfig.getboolean("movingpattern", "usePolygonOverlay")
        config.polyOverlay.minHue = int(workConfig.get("movingpattern", "poly_minHue"))
        config.polyOverlay.maxHue = int(workConfig.get("movingpattern", "poly_maxHue"))
        config.polyOverlay.minSaturation = float(workConfig.get("movingpattern", "poly_minSaturation"))
        config.polyOverlay.maxSaturation = float(workConfig.get("movingpattern", "poly_maxSaturation"))
        config.polyOverlay.minValue = float(workConfig.get("movingpattern", "poly_minValue"))
        config.polyOverlay.maxValue = float(workConfig.get("movingpattern", "poly_maxValue"))
        config.tileOverlayGridProb = float(workConfig.get("movingpattern", "tileOverlayGridProb", fallback=0.0))
        config.poly_alpha = int(workConfig.get("movingpattern", "poly_alpha"))
        config.useOverlayTileGrid = workConfig.getboolean("movingpattern", "useOverlayTileGrid", fallback=False)
        config.polyOverlayMode = workConfig.get("movingpattern", "polyOverlayMode", fallback="soft_light")
        config.polyOverlay.setStartColor()
        config.polyOverlay.getNewColor()
        config.polyOverlay.colorTransitionSetup()
        config.polyOverlayChangeProb = float(workConfig.get("movingpattern", "polyOverlayChangeProb", fallback=0.003))

        generateOverlayTiles()
        loadPolyOverlaybaseValues()
        # print(config.polyBase)
    except Exception as e:
        pieceLogger(f" ==> Not using custom polygon overlay {e}")
        config.usePolygonOverlay = False


# ----------------- INITIAL ACTIONS  ---------------------


def initializeCrossFader():

    config.doTransition = True
    config.doneCount = 0
    config.fader = Fader()
    config.fader.height = config.canvasHeight
    config.fader.width = config.canvasWidth
    config.fader.xPos = 0
    config.fader.yPos = 0
    config.fader.setUp()
    config.fader.startingImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.fader.endImage = config.canvasImage
    config.fader.destinationImage = config.image
    loadConfigValue(config, workConfig, "movingpattern", "faderDoingRefreshCount", 5, int)


def loadFilterRemapping():
    try:
        loadFilterRemappingConfigs()
    except Exception as e:
        pieceLogger(e)
        config.filterRemapping = False
        config.filterRemappingProb = 0.0
        config.filterRemapMinHoriSize = 24
        config.filterRemapMinVertSize = 24
        config.filterRemapMaxHoriSize = 24
        config.filterRemapMaxVertSize = 24
        config.filterRemapRangeX = config.canvasWidth
        config.filterRemapRangeY = config.canvasHeight


def loadFilterRemappingConfigs():
    loadConfigValue(config, workConfig, "movingpattern", "filterRemapping", False, bool)
    loadConfigValue(config, workConfig, "movingpattern", "filterRemappingProb", 0.0, float)
    loadConfigValue(config, workConfig, "movingpattern", "filterRemapMinHoriSize", 1, int)
    loadConfigValue(config, workConfig, "movingpattern", "filterRemapMaxHoriSize", 1, int)
    loadConfigValue(config, workConfig, "movingpattern", "filterRemapMinVertSize", 1, int)
    loadConfigValue(config, workConfig, "movingpattern", "filterRemapMaxVertSize", 1, int)
    loadConfigValue(config, workConfig, "movingpattern", "filterRemapRangeY", 1, int)
    loadConfigValue(config, workConfig, "movingpattern", "filterRemapRangeX", 1, int)


def createImageHolders():
    ########################################################################
    # CREATE THE IMAGE HOLDERS
    # canvasImage will get the drawing
    # disturbanceImage will get the disturbance / glitching
    # image will be the final output

    config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.patternImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.destinationImage = Image.new("RGBA", (config.screenWidth, config.screenHeight))
    config.compositeImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))

    config.canvasImageDraw = ImageDraw.Draw(config.canvasImage)
    config.destinationImageDraw = ImageDraw.Draw(config.destinationImage)


def main(run=True):
    global config
    pieceLogger("\n main() called")

    config.debugPause = False

    loadConfigValue(config, workConfig, "movingpattern", "setupDeBug", False, bool)

    loadConfigValue(config, workConfig, "movingpattern", "blockWidthMin", 32, int)
    loadConfigValue(config, workConfig, "movingpattern", "blockWidthMax", 32, int)

    loadConfigValue(config, workConfig, "movingpattern", "yOffset", 1, int)
    loadConfigValue(config, workConfig, "movingpattern", "yOffset2", 1, int)
    loadConfigValue(config, workConfig, "movingpattern", "", 1, int)
    loadConfigValue(config, workConfig, "movingpattern", "", 1, int)

    loadConfigValue(config, workConfig, "movingpattern", "blockRotation", 0.00, float)
    loadConfigValue(config, workConfig, "movingpattern", "canvasRotation", 0.00, float)
    loadConfigValue(config, workConfig, "movingpattern", "imgcanvasOffsetX", 0, int)
    loadConfigValue(config, workConfig, "movingpattern", "imgcanvasOffsetY", 0, int)

    config.repeatProb = 0.99

    # if/when saving images
    config.drawingPrinted = True
    loadConfigValue(config, workConfig, "movingpattern", "saveImages", False, bool)
    loadConfigValue(config, workConfig, "movingpattern", "outPutPath", "", str)
    loadConfigValue(config, workConfig, "movingpattern", "drawBGColorEachCycle", True, bool)

    config.repeatDrawingMode = 1
    loadConfigValue(config, workConfig, "movingpattern", "loadAnImageProb", 0.0, float)
    config.imageSources = workConfig.get("movingpattern", "imageSources").split(",")

    ########################################################################
    createImageHolders()
    ########################################################################

    loadConfigValue(config, workConfig, "movingpattern", "useBlurSection", False, bool)
    loadConfigValue(config, workConfig, "movingpattern", "blurSectionWidth", 0, int)
    loadConfigValue(config, workConfig, "movingpattern", "blurSectionHeight", 0, int)
    loadConfigValue(config, workConfig, "movingpattern", "blurSectionXPos", 0, int)
    loadConfigValue(config, workConfig, "movingpattern", "blurSectionYPos", 0, int)
    loadConfigValue(config, workConfig, "movingpattern", "mask_blur_amt", 0, int)
    loadConfigValue(config, workConfig, "movingpattern", "cp_blur_amt", 0, int)

    config.mask = Image.new("L", config.canvasImage.size, 0)
    config.mask_draw = ImageDraw.Draw(config.mask)

    config.mask_draw.ellipse(
        (
            config.blurSectionXPos,
            config.blurSectionYPos,
            config.blurSectionXPos + config.blurSectionWidth,
            config.blurSectionYPos + config.blurSectionHeight,
        ),
        fill=255,
    )
    config.mask_blur_amt = config.mask_blur_amt
    config.cp_blur_amt = config.cp_blur_amt

    loadConfigValue(config, workConfig, "movingpattern", "resetOverlayProbability", 0.000, float)

    loadFilterRemapping()

    # ####################### clip player instert ################################
    loadClipPlayerConfigs()

    # ###########################################################################

    initializeCrossFader()

    # ###########################################################################
    setupPolyOverlay()
    loadAndSetupPatterns()
    loadAndSetupAllPalettes()
    setupDisturbances()
    buildPatternSequence(config)

    # ###########################################################################

    config.directorController = Director(config)
    config.redrawSpeed = float(workConfig.get("movingpattern", "redrawSpeed"))

    config.imageXPOS = 0
    config.imageYPOS = 0
    config.XPOSSpeed = float(workConfig.get("movingpattern", "XPOSSpeed", fallback="0.0"))
    config.YPOSSpeed = float(workConfig.get("movingpattern", "YPOSSpeed", fallback="0.0"))

    try:
        config.directorController.slotRate = float(workConfig.get("movingpattern", "slotRate"))
    except Exception as e:
        pieceLogger(f"{e} <== adjust config to use slotRate!! <===")
        config.directorController.slotRate = 0.03

    # THIS IS USED AS WAY TO MOCKUP A CONFIGURATION OF RECTANGULAR PANELS
    panelDrawing.mockupBlock(config, workConfig)

    # """
    # # THIS IS USED AS WAY TO MOCKUP A CONFIGURATION OF RECTANGULAR PANELS
    # panelDrawing.mockupBlock(config, workConfig)
    #     ########### Need to add something like this at final render call  as well

    #     ########### RENDERING AS A MOCKUP OR AS REAL ###########
    #     if config.useDrawingPoints  :
    #         config.panelDrawing.canvasToUse = config.renderImageFull
    #         config.panelDrawing.render()
    #     else :
    #         #config.render(config.canvasImage, 0, 0, config.canvasWidth, config.canvasHeight)
    #         #config.render(config.image, 0, 0)
    #         config.render(config.renderImageFull, 0, 0)
    # """

    if config.setupDeBug:
        # prints out everything in the config global
        config.debugSelf()

    if run:
        runWork()


def runWork():
    global config
    pieceLogger("Running repeatblocks.py", 2)
    while config.isRunning:
        config.directorController.checkTime()
        if config.directorController.advance:
            iterate()
        time.sleep(config.redrawSpeed)
        if not config.standAlone:
            config.callBack()


def loadConfigValue(obj, workConfig, section, option, default, type_converter):
    try:
        if type_converter == bool:
            setattr(obj, option, type_converter(workConfig.getboolean(section, option)))
        else:
            setattr(obj, option, type_converter(workConfig.get(section, option)))
    except Exception as e:
        pieceLogger(f" ==> Config value not loaded: {option} ==> will be set to {default} \n  {e}", 1)
        setattr(obj, option, default)


###############################################
