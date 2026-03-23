# ################################################### #
from ast import Try
import math
import random
import time
import os, sys
import configparser

# from shapely import length
from modules.configuration import bcolors
from modules.configuration import pieceLogger
from modules.movieClip import movieClip
from modules import colorutils, panelDrawing, pattern_blocks_v5, disturbance
from modules.holder_director import Holder
from modules.holder_director import Director
from modules.coloroverlay import ColorOverlay
from PIL import Image, ImageDraw, ImageEnhance, ImageOps, ImageChops
from copy import copy, deepcopy

# This version substitutes the overlay disturbance with a slide-repeating of a section

# Adding the wave deformation to get a slightly more organic
# pattern distortion - might be too much, too expected but
# is dreamy  4-3-2024

# major refactoring along with pattern_blocks.py 2025-02-19


###############################################


# --------------------- CLASSES     ---------------------


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


# --------------------- PALETTES      ---------------------


def loadAndSetupAllPalettes():
    global workConfig
    """initial palatte setups -- needs to run after combinations are established"""
    config.palettesConfigFile = workConfig.get("movingpattern", "palettesConfigFile")

    config.paletteConfig = configparser.ConfigParser()
    argument = f"{config.path}/configs/{config.palettesConfigFile}"

    pieceLogger(f"loadAndSetupAllPalettes: loading from {argument}")
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
        if arg != "":
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
    print(f"Setting a new palette:  {paletteObj.paletteName}")
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

    pieceLogger(
        f"selectNewPalette: Choosing a palette: {config.combinationSets[config.currentCombinationsetIndex].palettes[config.currentPaletteIndex]} in {config.combinationSets[config.currentCombinationsetIndex].name}",
        2,
        True,
    )
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

    config.patternSequence = []
    config.slotsToChange = []
    config.settingUpPattern = True

    # when rebuild is called, chance that the full pattern gets rebuilt -
    loadConfigValue(config, workConfig, "movingpattern", "rebuildAllSlotsProb", 0.50, float)
    # when rebuild is called and the full rebuild is not called, individual slots can change
    # at this rate
    loadConfigValue(config, workConfig, "movingpattern", "rebuildIndividualSlotProb", 0.0, float)
    # at this rate
    loadConfigValue(config, workConfig, "movingpattern", "chanceRebuildPatternChoosesRandom", 0.0, float)
    loadConfigValue(config, workConfig, "movingpattern", "rebuildSlotSkipRate", 0.1, float)
    loadConfigValue(config, workConfig, "movingpattern", "rebuildSlotStartSkipRate", 0.1, float)

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

        comboSet.combinationSetsMinTime = float(workConfig.get(combinationSetName, "combinationSetsMinTime", fallback=30))
        comboSet.combinationSetsMaxTime = float(workConfig.get(combinationSetName, "combinationSetsMaxTime", fallback=60))

        comboSet.maxNumberOfRandomizers = int(workConfig.get(combinationSetName, "maxNumberOfRandomizers", fallback=3))

        config.combinationSets.append(comboSet)
    config.currentCombinationsetIndex = 0
    config.numberOfRandomizersUsed = 0
    config.comboSetDirector = Director(config)
    config.comboSetDirector.slotRate = config.combinationSets[config.currentCombinationsetIndex].combinationSetsMaxTime


def handleChangeCurrentCominationSet():
    pieceLogger("Checking combo set",3)
    disturbancesDone = not config.doSectionDisturbance or config.doneCount >= config.numberOfSections
    if random.random() < config.changeCombinationAnytimeProb and config.fader.fadingDone and disturbancesDone :
        config.currentCombinationsetIndex = math.floor(random.uniform(0, len(config.combinationSets)))
        # {config.combinationSets[config.currentCombinationsetIndex]}
        pieceLogger(f"=====> Combo changed to {config.combinationSets[config.currentCombinationsetIndex].name} (index: {config.currentCombinationsetIndex})\n", 2, True)
        config.numberOfRandomizersUsed = 0

        # turning off to test
        # config.settingUpPattern = True
        # selectNewPalette()

        # changing so the transition between a new combo set happens in chunks rather than
        # waves

        # config.patternSequence = []
        # config.rebuildIndividualSlotProb = .1
        rebuildPatterns()


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
    pieceLogger("Building new pattern sequence : buildPatternSequence called", 0)
    # config.patternSequence = []
    # config.usedPatterns = []

    # during a partial rebuild, maybe don't change too much
    # in terms of the block size
    if config.settingUpPattern:
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

        config.patternBlockCols = round(config.pictureWidth / config.blockWidth)
        config.patternBlockRows = round(config.pictureHeight / config.blockHeight)

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

    if "randomizer" in _patternSelected :
        if config.numberOfRandomizersUsed < config.combinationSets[config.currentCombinationsetIndex].maxNumberOfRandomizers : 
            config.numberOfRandomizersUsed +=1
        else :
            chooseAPattern()
    return _patternSelected


# this really needs to change to be more readable and predictable ....
# there are n number of slots, just fill each one and change randomly etc
# as they all get filled up
def generatePatternSequence(config):

    # config.patternSequence = []
    config.usedPatterns = []
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
            "randomizer4",
            "randomizer3",
            "randomizer2",
            "randomizer",
            "diamond",
        ]
        _patternBlock.isBorder = config.useBorderPattern and (c == 0 or r == 0 or c == (config.patternBlockCols - 1) or r == (config.patternBlockRows - 1))

        try:

            if config.settingUpPattern:
                config.patternSequence.append(_patternBlock)
            else:
                if len(config.slotsToChange) > 0:
                    if _iterCount in config.slotsToChange:
                        config.patternSequence[_iterCount] = _patternBlock
                        # pieceLogger(f"_iterCount {_iterCount} {_patternBlock.pattern}")
                elif random.random() < config.rebuildIndividualSlotProb:
                    _slot = round(random.uniform(0, len(config.patternSequence) - 1))
                    # shouldn't there be a list of slots to change that are somewhat
                    # consecuetive? otherwise just makes the whole thing more patchy?
                    # pieceLogger(f"add_pattern_block: change this slot {_slot}/ {len(config.patternSequence)}")
                    config.patternSequence[_slot] = _patternBlock

            # comment:
        except Exception as e:
            print(e)
        # end try

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
    pieceLogger("rebuildPatterns() called")

    if config.numRowsRandomize:
        rowsAndDotsSettings()

    # if random.random() < config.changePaletteWhenRebuildProb:
    #     pieceLogger("selectNewPalette called from: rebuildPatterns()")
    #     selectNewPalette()

    buildPatternSequence(config)
    disturbance.setupStableSections()
    disturbance.rebuildSections()
    resetCrossFader(False)


def resetCrossFader(_useConfigImage=True):
    # os.system('afplay /System/Library/Sounds/Sosumi.aiff')
    # print(f"DOING NOW  {config.faderDoingRefreshCount}")
    # os.system('say "NOW" &')

    pieceLogger(f"resetCrossFader called : {_useConfigImage}")
    config.repeatDrawingMode = 1
    config.fader.fadingDone = False
    config.doTransition = True
    config.doSectionDisturbance = False
    if _useConfigImage:
        config.fader.startingImage = config.image.copy()
    else:
        # config.fader.startingImage = config.canvasImage.copy()
        config.fader.startingImage = config.compositeImage.copy()

    # _tempImg  =  Image.new("RGBA", (config.pictureWidth, config.pictureHeight))
    # _tempDraw = ImageDraw.Draw(_tempImg)
    # _tempDraw.rectangle((0,0,500,500), fill = (255,0,0,255))
    # config.canvasImage.paste(_tempImg, (0,0), _tempImg)

    # NOT WORKING

    # config.fader.endImage = config.canvasImage.copy()
    # config.fader.crossFadeImage = Image.new("RGBA", (config.pictureWidth, config.pictureHeight))

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
    config.comboSetDirector.checkTime()
    if config.comboSetDirector.advance:
        handleChangeCurrentCominationSet()
    handlePaletteChanges()
    updateBackgroundColor()
    handleClipPlayer()
    drawAndProcessPattern()
    disturbance.handleDisturbances()
    handleFilterRemapping()
    handleFadingAndRebuild()
    handlePatternRebuild()
    disturbance.handleSectionDisturbances()
    disturbance.handleShingleVariation()
    drawBackgroundAndPasteImage()
    renderComposite()
    if config.saveImages:
        saveImageIfDone()


def drawRepeatedPatternImage(config, canvasImage):
    """Draws the repeated pattern image onto the canvas."""
    _counter = 0
    extraOverlapx = 0
    extraOverlapy = 0
    # for i in range(len(config.patternSequence)):
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
    disturbancesDone = not config.doSectionDisturbance or config.doneCount >= config.numberOfSections
    if random.random() < config.rebuildPatternProbability and config.fader.fadingDone and disturbancesDone:
        # config.doSectionDisturbance = False
        # print("\nrebuildPatterns called after fading done 2")

        # selectNewPalette(False)
        if random.random() < config.rebuildAllSlotsProb:
            pieceLogger("\nhandlePatternRebuild(): Rebuiding full")
            config.settingUpPattern = True
            config.patternSequence = []
            # selectNewPalette(True)
            # selectNewPalette()
        else:
            if random.random() < config.chanceRebuildPatternChoosesRandom:
                config.slotsToChange = []
            else:
                config.slotsToChange = []
                _skip = True
                _chanceNotToSkip = config.rebuildSlotSkipRate
                _chanceToSkip = config.rebuildSlotStartSkipRate
                for i in range(len(config.patternSequence)):
                    if random.random() < _chanceToSkip:
                        _skip = False
                    if random.random() < _chanceNotToSkip:
                        _skip = True
                    if not _skip:
                        config.slotsToChange.append(i)
                # pieceLogger(f"handlePatternRebuild:  {config.slotsToChange}")

            config.settingUpPattern = False
        pieceLogger("\nhandlePatternRebuild(): Rebuiding parts")
        pieceLogger(f"handlePatternRebuild(): config.settingUpPattern {config.settingUpPattern}")
        pieceLogger(f"handlePatternRebuild(): config.slotsToChange {config.slotsToChange}")
        rebuildPatterns()


def drawBackgroundAndPasteImage():
    """Draws the background and pastes the main image."""
    if config.doTransition:

        config.fader.fadeIn(config)
        config.compositeImage.paste(config.fader.crossFadeImage, (0, 0), config.fader.crossFadeImage)

    elif config.sectionDisturbance:
        if config.doSectionDisturbance:
            config.compositeImage.paste(config.canvasImage, (0, 0), config.canvasImage)
        else:
            config.compositeImage.paste(config.patternImage, (0, 0), config.patternImage)

    """Transforms and renders the final image."""
    if config.transformShape:
        config.compositeImage = transformImage(config.compositeImage)

    if config.canvasRotation != 0:
        config.compositeImage = config.compositeImage.rotate(config.canvasRotation, 3, True)
        config.compositeImage = ImageEnhance.Contrast(config.compositeImage).enhance(1.20)

    # if config.useWaveDistortion:
    #     config.compositeImage = ImageOps.deform(config.compositeImage, disturbance.WaveDeformer())
    #     config.waveDeformXPos += config.waveDeformXPosRate
    #     if config.waveDeformXPos > config.screenWidth:
    #         config.waveDeformXPos = 0


# def blendStep():
#     f0 = config.scrollBlendFrame0
#     f1 = config.scrollBlendFrame1
#     # config.destinationImage.paste(config.compositeImage, (round(config.imageXPOS), round(config.imageYPOS)), config.compositeImage)
#     # config.destinationImage.paste(config.compositeImage, (round(config.imageXPOS - config.pictureWidth), round(config.imageYPOS)), config.compositeImage)

#     if config.blendStep == 0:
#         # f0.paste(config.compositeImage,(0,0), config.compositeImage)
#         config.destinationImage.paste(f0, (0, 0))

#     if config.blendStep >= config.blendSteps:
#         f0.paste(config.compositeImage, (round(config.imageXPOS), round(config.imageYPOS)), config.compositeImage)
#         f0.paste(config.compositeImage, (round(config.imageXPOS - config.pictureWidth), round(config.imageYPOS)), config.compositeImage)
#         config.blendStep = 0
#         config.imageXPOS += config.XPOSSpeed
#         if config.imageXPOS >= config.pictureWidth:
#             config.imageXPOS = 0

#         f1.paste(config.compositeImage, (round(config.imageXPOS), round(config.imageYPOS)), config.compositeImage)
#         f1.paste(config.compositeImage, (round(config.imageXPOS - config.pictureWidth), round(config.imageYPOS)), config.compositeImage)
#         # config.destinationImage.paste(f1, (0, 0))
#     else:
#         config.blendStep += 1
#         tempImag = Image.new("RGBA", (config.pictureWidth, config.pictureHeight))
#         tempImag.paste(Image.blend(f0, f1, config.blendStep / 5), (0, 0))
#         config.render(tempImag, 0, 0)
#         # config.imageYPOS += config.YPOSSpeed
#         # if config.imageYPOS >= config.pictureHeight:
#         #     config.imageYPOS = 0


def renderComposite():
    """FINAL RENDERING CALL"""
    if config.useDrawingPoints == True:
        config.panelDrawing.canvasToUse = config.compositeImage
        config.panelDrawing.render()
    else:
        if config.usePolygonOverlay:
            config.compositeImage = shapeOverLayFunction(config.compositeImage)

        # x0 = round(math.floor(config.imageXPOS))
        # frac = config.imageXPOS - x0
        # y = round(config.imageYPOS)

        # # Blend between integer pixel positions x0 and x0+1 for smooth sub-pixel scrolling.
        # # Reuse pre-allocated buffers to avoid per-frame allocation and GC pauses.
        # _bg = (0, 0, 0, 255)
        # f0 = config.scrollBlendFrame0
        # f1 = config.scrollBlendFrame1

        # f0.paste(_bg, (0, 0, f0.width, f0.height))
        # f0.paste(config.compositeImage, (x0, y), config.compositeImage)
        # f0.paste(config.compositeImage, (x0 - config.pictureWidth, y), config.compositeImage)

        # f1.paste(_bg, (0, 0, f1.width, f1.height))
        # f1.paste(config.compositeImage, (x0 + 1, y), config.compositeImage)
        # f1.paste(config.compositeImage, (x0 + 1 - config.pictureWidth, y), config.compositeImage)

        # config.destinationImage.paste(Image.blend(f0, f1, frac), (0, 0))
        # original method - only good for whole number jumps
        config.destinationImage.paste(config.compositeImage, (round(config.imageXPOS), round(config.imageYPOS)), config.compositeImage)
        config.destinationImage.paste(config.compositeImage, (round(config.imageXPOS - config.pictureWidth), round(config.imageYPOS)), config.compositeImage)

        config.imageXPOS += config.XPOSSpeed
        # config.imageYPOS += config.YPOSSpeed

        if config.imageXPOS >= config.pictureWidth:
            config.imageXPOS = 0

        if config.imageYPOS >= config.pictureHeight:
            config.imageYPOS = 0

        # # uncomment for all temp canvas layers to show
        if config.setupDeBug:
            showDebugCanvases(config)

        # this used to occur on the composite layer but was getting jumps when
        # new blocks were added so compromising with wave distortions applied to final 
        # image  - smoother and slower
        if config.useWaveDistortion:
            config.destinationImage = ImageOps.deform(config.destinationImage, disturbance.WaveDeformer())
            config.waveDeformXPos += config.waveDeformXPosRate
            if config.waveDeformXPos > config.screenWidth:
                config.waveDeformXPos = 0

        config.render(config.destinationImage, 0, 0)


def showDebugCanvases(config):
    _w = config.pictureWidth
    _h = config.pictureHeight

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
    temp2 = Image.new("RGBA", (config.pictureWidth, config.pictureHeight))
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
    config.fader.height = config.pictureHeight
    config.fader.width = config.pictureWidth
    config.fader.xPos = 0
    config.fader.yPos = 0
    config.fader.setUp()
    config.fader.startingImage = Image.new("RGBA", (config.pictureWidth, config.pictureHeight))
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
        config.filterRemapRangeX = config.pictureWidth
        config.filterRemapRangeY = config.pictureHeight


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

    config.image = Image.new("RGBA", (config.pictureWidth, config.pictureHeight))
    config.patternImage = Image.new("RGBA", (config.pictureWidth, config.pictureHeight))
    config.canvasImage = Image.new("RGBA", (config.pictureWidth, config.pictureHeight))
    config.destinationImage = Image.new("RGBA", (config.screenWidth, config.screenHeight))
    config.compositeImage = Image.new("RGBA", (config.pictureWidth, config.pictureHeight))

    # For scrolling the entire piece
    config.scrollBlendFrame0 = Image.new("RGBA", (config.screenWidth, config.screenHeight), (0, 0, 0, 255))
    config.scrollBlendFrame1 = Image.new("RGBA", (config.screenWidth, config.screenHeight), (0, 0, 0, 255))

    config.blendSteps = 5
    config.blendStep = 0

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

    loadConfigValue(config, workConfig, "movingpattern", "pictureWidth", config.canvasWidth, int)
    loadConfigValue(config, workConfig, "movingpattern", "pictureHeight", config.canvasHeight, int)

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
    setupPolyOverlay()
    loadAndSetupPatterns()
    loadAndSetupAllPalettes()
    disturbance.init(config, workConfig)
    disturbance.setupDisturbances()
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
    #         #config.render(config.canvasImage, 0, 0, config.pictureWidth, config.pictureHeight)
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
