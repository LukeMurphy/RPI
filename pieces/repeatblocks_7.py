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
        self.blocksChanged = 0
        self.totalBlocksToChange = 0

        self.subsectionsChanged = 0
        self.totalSubSectionsToChange = 0

        self.fadeThroughAmount = 0
        self.fadeThroughIncrement = 0.1

        self.blocksRefreshed = 0
        self.fadingDone = False
        self.testing = True
        self.fadeThruBlack = False
        self.destinationImage = None
        self.initialized = False

        self.fadeInMode = 1
        self.numParallelBlocks = 1
        self.activeFades = []
        self.activeDissolves = []
        self.pendingLargeBlocks = []
        self.pendingFadeBlockIndices = []
        self.crossFadePatches = []

    def makeSections(self, initalX, sectionWidth, initalY, sectionHeight, x_sections, y_sections, variations=False):
        baseSectionWidth = math.ceil(sectionWidth / (x_sections))
        baseSectionHeight = math.ceil(sectionHeight / (y_sections))
        # variations = False

        if variations:
            sectionDeltaWidth = config.sectionDeltaWidth
            sectionDeltaHeight = config.sectionDeltaHeight
        else:
            sectionDeltaWidth = 0
            sectionDeltaHeight = 0

        _cumulativeWidth = initalX
        sections = []

        for _x in range(x_sections):
            _sectionWidth = random.randint(baseSectionWidth - sectionDeltaWidth, baseSectionWidth + sectionDeltaWidth)
            # pieceLogger((_sectionWidth))
            if _x == x_sections - 1 and variations and sectionDeltaWidth > 0:
                _sectionWidth = sectionWidth - _cumulativeWidth

            _cumulativeHeight = initalY
            for _y in range(y_sections):
                _sectionHeight = random.randint(baseSectionHeight - sectionDeltaHeight, baseSectionHeight + sectionDeltaHeight)
                if _y == y_sections - 1 and variations and sectionDeltaHeight > 0:
                    _sectionHeight = sectionHeight - _cumulativeHeight
                sections.append([_cumulativeWidth, _sectionWidth, _cumulativeHeight, _sectionHeight])
                _cumulativeHeight += _sectionHeight
            _cumulativeWidth += _sectionWidth

        return sections

    def setUp(self, config):
        # self.fadeInMode = config.faderMode
        self.fadeInMode = 1 if random.random() < config.faderProbDissolve else 0

        if config.faderInit :
            config.faderInit = False
        else :
            if self.fadeInMode == 0 :
                config.faderDoingRefreshCountIterations = config.faderFadeDoingRefreshCountIterations
            if self.fadeInMode == 1:
                config.faderDoingRefreshCountIterations = config.faderDissolveDoingRefreshCountIterations

        pieceLogger(f"=> Fader initialized setup {self.fadeInMode} {config.faderDoingRefreshCountIterations}")

        self.blankImage = Image.new("RGBA", (self.width, self.height))
        self.startingImage = Image.new("RGBA", (self.width, self.height))
        self.endImage = Image.new("RGBA", (self.width, self.height))
        self.crossFadeImage = Image.new("RGBA", (self.width, self.height))
        self.xRange = [0, config.pictureWidth]
        self.yRange = [0, config.pictureHeight]

        self.fadeThroughIncrement = config.fadeThroughIncrement
        self.numParallelBlocks = getattr(config, "faderParallelBlocks", 1)

        self.largeBlocks = self.makeSections(0, config.pictureWidth, 0, config.pictureHeight, config.faderLargeBlockXSections, config.faderLargeBlockYSections, True)
        random.shuffle(self.largeBlocks)

        if self.fadeInMode == 1:
            # now create grids of little blocks
            self.fadeBlocks = []
            for b in self.largeBlocks:
                initX = b[0]
                finalX = b[1]
                initY = b[2]
                finalY = b[3]
                subsectionGroup = self.makeSections(initX, finalX, initY, finalY, config.faderSmallBlockXSections, config.faderSmallBlockYSections)
                random.shuffle(subsectionGroup)
                self.fadeBlocks.append(subsectionGroup)

            self.blocksChanged = 0
            self.totalBlocksToChange = len(self.largeBlocks)

            self.fadingInSection = self.fadeBlocks[self.blocksChanged]
            self.totalSubSectionsToChange = len(self.fadingInSection)
            self.subsectionsChanged = 0
            self.pendingFadeBlockIndices = list(range(len(self.largeBlocks)))
            self.activeDissolves = []
        else:
            self.blocksChanged = 0
            self.totalBlocksToChange = len(self.largeBlocks)

            self.fadingInSection = self.largeBlocks[self.blocksChanged]
            self.totalSubSectionsToChange = len(self.fadingInSection)
            self.subsectionsChanged = 0
            self.pendingLargeBlocks = list(self.largeBlocks)
            self.activeFades = []


    def fadeIn(self, config):
        if self.fadeInMode == 1:
            self.dissolveIn()
        else:
            self.crossFadeIn()


    def dissolveIn(self):
        if self.fadingDone:
            self.initialized = False
            return

        if self.initialized:
            self.initialized = False
        if self.testing:
            self.testing = False

        # Seed active dissolves up to numParallelBlocks
        while len(self.activeDissolves) < self.numParallelBlocks and self.pendingFadeBlockIndices:
            _index = self.pendingFadeBlockIndices.pop(0)
            self.activeDissolves.append({"fadeBlock": self.fadeBlocks[_index], "subsectionIndex": 0})

        if not self.activeDissolves:
            self.endFades()
            return

        self.crossFadePatches = []
        dissolvesDone = []

        for dissolve in self.activeDissolves:
            _fadeBlock = dissolve["fadeBlock"]
            _subsectionIndex = dissolve["subsectionIndex"]
            if _subsectionIndex < len(_fadeBlock):
                self.x = _fadeBlock[_subsectionIndex][0]
                _w = _fadeBlock[_subsectionIndex][1]
                self.y = _fadeBlock[_subsectionIndex][2]
                _h = _fadeBlock[_subsectionIndex][3]
                patch = self.endImage.crop((self.x, self.y, max(self.x + _w, self.x), max(self.y + _h, self.y)))
                self.crossFadePatches.append((patch, self.x, self.y))
                self.crossFadeImage = patch
                dissolve["subsectionIndex"] += 1
            else:
                dissolvesDone.append(dissolve)
                self.blocksChanged += 1

        for d in dissolvesDone:
            self.activeDissolves.remove(d)

        if not self.activeDissolves and not self.pendingFadeBlockIndices:
            self.endFades()


    def endFades(self):
        self.fadingDone = True
        self.blocksChanged = 0
        self.fadeThroughAmount = 0
        config.doTransition = False
        pieceLogger("=> FADING DONE")


    def crossFadeIn(self):
        if self.fadingDone:
            self.endFades()
            return

        if self.initialized:
            self.initialized = False
        if self.testing:
            self.testing = False

        # Seed active fades up to numParallelBlocks
        while len(self.activeFades) < self.numParallelBlocks and self.pendingLargeBlocks:
            section = self.pendingLargeBlocks.pop(0)
            self.activeFades.append({"section": section, "amount": 0.0})

        if not self.activeFades:
            self.endFades()
            return

        self.crossFadePatches = []
        fadesDone = []

        for fade in self.activeFades:
            s = fade["section"]
            self.x = s[0]
            _w = s[1]
            self.y = s[2]
            _h = s[3]
            amt = min(fade["amount"], 1.0)
            if  (self.x + _w) <= self.x :
                # pieceLogger(_w)
                _w = 0

            if  (self.y + _h)<= self.y :
                # pieceLogger(_h)
                _h = 0
            _tempEnd = self.endImage.crop((self.x, self.y, self.x + _w, self.y + _h))
            _tempStart = self.startingImage.crop((self.x, self.y, self.x + _w, self.y + _h))
            blended = Image.blend(_tempStart, _tempEnd, amt)
            self.crossFadePatches.append((blended, self.x, self.y))
            self.crossFadeImage = blended

            if fade["amount"] >= 1.0:
                fadesDone.append(fade)
                self.blocksChanged += 1
            else:
                fade["amount"] += self.fadeThroughIncrement

        for fade in fadesDone:
            self.activeFades.remove(fade)

        if not self.activeFades and not self.pendingLargeBlocks:
            self.endFades()


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


def loadConfigValue(obj, workConfig, section, option, default, type_converter):
    try:
        if type_converter == bool:
            setattr(obj, option, type_converter(workConfig.getboolean(section, option)))
        else:
            setattr(obj, option, type_converter(workConfig.get(section, option)))
    except Exception as e:
        pieceLogger(f" ==> Config value not loaded: {option} ==> will be set to {default} \n  {e}", 1)
        setattr(obj, option, default)


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

    # config.currentPaletteIndex = 0
    config.currentPaletteIndex = math.floor(random.uniform(0, len(config.combinationSets[config.currentCombinationsetIndex].palettes)))
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

    # rather than favoring a normal distribution, use a list - getting tired of trying to game the randomness by ordering the list of palettes etc
    # config.currentPaletteIndex = math.floor(random.uniform(0, len(config.combinationSets[config.currentCombinationsetIndex].palettes)))
    _listOfIndecies = list(range(len(config.combinationSets[config.currentCombinationsetIndex].palettes)))
    config.currentPaletteIndex = random.choice(_listOfIndecies)

    pieceLogger(
        f"selectNewPalette: Choosing a palette: {config.combinationSets[config.currentCombinationsetIndex].palettes[config.currentPaletteIndex]} in {config.combinationSets[config.currentCombinationsetIndex].name}",
        2,
        True,
    )
    setPalette(config, config.currentPaletteIndex)

    if _setPalette:
        rebuildPatterns()
        resetCrossFader()
        resetPatternBlocks()

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
    # config.currentCombinationsetIndex = 0
    config.currentCombinationsetIndex = math.floor(random.uniform(0, len(config.combinationSets)))
    config.numberOfRandomizersUsed = 0
    config.comboSetDirector = Director(config)
    config.comboSetDirector.slotRate = config.combinationSets[config.currentCombinationsetIndex].combinationSetsMaxTime


def handleChangeCurrentCominationSet():
    pieceLogger("Checking combo set", 3)
    disturbancesDone = not config.doSectionDisturbance or config.doneCount >= config.numberOfSections
    if random.random() < config.changeCombinationAnytimeProb and config.fader.fadingDone and disturbancesDone:

        # rather than favoring a normal distribution, use a list - getting tired of trying to game the randomness by ordering the list of palettes etc
        # config.currentCombinationsetIndex = math.floor(random.uniform(0, len(config.combinationSets)))

        _listOfIndecies = list(range(len(config.combinationSets)))
        config.currentPalecurrentCombinationsetIndextteIndex = random.choice(_listOfIndecies)

        # {config.combinationSets[config.currentCombinationsetIndex]}
        pieceLogger(f"=====> Combo changed to {config.combinationSets[config.currentCombinationsetIndex].name} (index: {config.currentCombinationsetIndex})\n", 2, True)
        config.numberOfRandomizersUsed = 0

        # problem the currentPaletteIndex may exceed the number of palettes if the combinationSet has changed
        # config.currentPaletteIndex = math.floor(random.uniform(0, len(config.combinationSets[config.currentCombinationsetIndex].palettes)))

        if random.random() < config.changePaletteWhenRebuildProb:
            _listOfIndecies = list(range(len(config.combinationSets[config.currentCombinationsetIndex].palettes)))
            config.currentPaletteIndex = random.choice(_listOfIndecies)

        # turning off to test
        # config.settingUpPattern = True
        # selectNewPalette()

        # changing so the transition between a new combo set happens in chunks rather than
        # waves

        # config.patternSequence = []
        # config.rebuildIndividualSlotProb = .1

        config.settingUpPattern = True
        config.rebuildPatternProbability = 1.0
        config.rebuildAllSlotsProb = 1.0
        config.fader.setUp(config)
        # rebuildPatterns()

        handlePatternRebuild()

        drawAndProcessPattern()


def resetPatternBlocks():

    tempPalette = changeSinglePalette(config.currentPaletteIndex)

    pieceLogger(f"resetPatternBlocks() : config.totalSlots {config.totalSlots}", 4, True)

    for i in range(config.totalSlots):
        _patternBlock = config.patternSequence[i]
        _patternBlock.hasBeenPainted = False
        _patternBlock.tempPalette = tempPalette

        if random.random() > config.changeEachblockWhenChangingPatternProb:
            _patternBlock.tempPalette = getTempPalette(config)

        config.patternSequence[i] = _patternBlock


def buildPatternSequence(config):
    pieceLogger("buildPatternSequence(config) called", 0)
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

        config.patternBlockCols = math.ceil(config.pictureWidth / config.blockWidth)
        config.patternBlockRows = math.ceil(config.pictureHeight / config.blockHeight)

        # considering making this be an option to fit exactly the width - i.e. choose the number of columns
        # rather than width or an alogrithm to do the fitting - the problem is that then you lose the
        # ragged edges which are a nice trace of the previous state
        # print(f"config.blockWidth {config.blockWidth} config.patternBlockCols {config.patternBlockCols}")

        config.totalSlots = config.patternBlockRows * config.patternBlockCols
        # pieceLogger(f"config.totalSlots {config.totalSlots}", 4, True)

    config.altLineColoring = random.random() < config.combinationSets[config.currentCombinationsetIndex].altColoringProb
    config.popRandomColorProb = random.random() < config.combinationSets[config.currentCombinationsetIndex].popRandomColorProb

    # print(config.altLineColoring)
    config.numConcentricBoxes = round(random.uniform(config.minnumConcentricBoxes, config.maxnumConcentricBoxes))

    pattern_blocks_v5.floralConfig(config)
    generatePatternSequence(config)

    # _print_pattern_sequence(config)
    config.borderDrawn = False
    config.initPatternBuild = False


def chooseAPattern(limitRandomizers=False):
    _patterns = config.combinationSets[config.currentCombinationsetIndex].patterns
    _dominantPatterns = config.combinationSets[config.currentCombinationsetIndex].dominantPatterns
    _dominantPatternProb = config.combinationSets[config.currentCombinationsetIndex].dominantPatternProb

    # due to normal distribution this kind of favors the things in the middle of the list
    # should really convert to a random choice operation rather than just numerical random
    # _patternSelected = _patterns[math.floor(random.uniform(0, len(_patterns)))]
    _patternSelected = random.choice(_patterns)

    if random.random() < _dominantPatternProb:
        _patternSelected = _dominantPatterns[math.floor(random.uniform(0, len(_dominantPatterns)))]

    # need to limit randomizers
    if "randomizer" in _patternSelected:
        if limitRandomizers:
            # chooseAPattern(True)
            _patternSelected = config.lastPatternSelected
        else:
            if config.numberOfRandomizersUsed < config.combinationSets[config.currentCombinationsetIndex].maxNumberOfRandomizers:
                config.numberOfRandomizersUsed += 1
            else:
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
    config.lastPatternSelected = _patternSelected
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

    pieceLogger(f"generatePatternSequence(config) called: {config.combinationSets[config.currentCombinationsetIndex].name} using _tempPalette: {_tempPalette.paletteName}")

    def add_pattern_block(c, r):
        nonlocal _patternSelected, _tempPalette, _iterCount
        if random.random() < _baseProb:
            _patternSelected = chooseAPattern()
            _tempPalette = getTempPalette(config)
        if "randomizer" in _patternSelected:
            if config.numberOfRandomizersUsed >= config.combinationSets[config.currentCombinationsetIndex].maxNumberOfRandomizers:
                # pieceLogger(f"need to limit _patternSelected {_patternSelected} {_iterCount} {config.numberOfRandomizersUsed}")
                _patternSelected = chooseAPattern(True)
                _tempPalette = getTempPalette(config)
            else:
                config.numberOfRandomizersUsed += 1

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
        except Exception as e:
            print(e)

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

        return getPaletteObjectByName(config.combinationSets[config.currentCombinationsetIndex].palettes[config.currentPaletteIndex])

    if random.SystemRandom().random() <= config.changeFullPaletteWhenChangingPatternProb:

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
    # pieceLogger(f"resetCrossFader called : {_useConfigImage}")
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

    # config.fader.totalBlocksToChange = config.faderDoingRefreshCount
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
    handleFilterRemapping()

    if config.debugPause:
        config.directorController.slotRate = 2.0

    config.comboSetDirector.checkTime()
    if config.comboSetDirector.advance:
        handleChangeCurrentCominationSet()

    # handlePaletteChanges()

    updateBackgroundColor()

    # handleClipPlayer()

    drawAndProcessPattern()

    disturbance.handleDisturbances()


    handleFadingAndRebuild()

    # handlePatternRebuild()

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

    # config.patternImage = canvasImage.copy()
    config.fader.endImage = config.patternImage.copy()
    # config.fader.endImage = config.canvasImage.copy()


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


# def handlePaletteChanges():
#     if random.random() < config.changePaletteAnytimeProb and config.fader.fadingDone:
#         print("selectPaletted called from handlePaletteChanges()")
#         selectNewPalette(True)
#         # rebuildSections()
#         # resetCrossFader(False)


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

# ---- dither remapping ------------

def loadFilterRemapping():
    loadConfigValue(config, workConfig, "movingpattern", "filterRemapping", False, bool)
    loadConfigValue(config, workConfig, "movingpattern", "filterRemappingProb", 0.0, float)
    loadConfigValue(config, workConfig, "movingpattern", "filterRemapMinHoriSize", 1, int)
    loadConfigValue(config, workConfig, "movingpattern", "filterRemapMaxHoriSize", 1, int)
    loadConfigValue(config, workConfig, "movingpattern", "filterRemapMinVertSize", 1, int)
    loadConfigValue(config, workConfig, "movingpattern", "filterRemapMaxVertSize", 1, int)
    loadConfigValue(config, workConfig, "movingpattern", "filterRemapRangeY", 1, int)
    loadConfigValue(config, workConfig, "movingpattern", "filterRemapRangeX", 1, int)
    loadConfigValue(config, workConfig, "movingpattern", "contractXSpeed", 2, int)
    loadConfigValue(config, workConfig, "movingpattern", "contractYSpeed", 2, int)
    loadConfigValue(config, workConfig, "movingpattern", "expandXSpeed", 2, int)
    loadConfigValue(config, workConfig, "movingpattern", "expandYSpeed", 2, int)
    config.filterRemapContracting = 0
    config.basefilterRemappingProb = config.filterRemappingProb


def handleFilterRemapping():
    """Handles filter remapping if enabled."""
    # print(f"config.useFilters {config.useFilters}  config.filterRemapping {config.filterRemapping} config.filterRemappingProb {config.filterRemappingProb}")
    if random.random() < config.filterRemappingProb and (config.useFilters and config.filterRemapping):
        remapFilter(config)


def expandFilterRemap():

    _pos = list(config.remapImageBlockSection)
    # pieceLogger(_pos)
    _pos[0] = max(_pos[0] - config.expandXSpeed, config.newFilterStartX)
    _pos[2] += config.expandXSpeed
    # _pos[1] -= 2
    # _pos[3] += 2
    # or _pos[1] <= (config.newFilterStartY)
    if _pos[0] <= (config.newFilterStartX) :
        config.filterRemappingProb = config.basefilterRemappingProb
        config.remapImageBlockSection = (_pos[0], _pos[1], _pos[2], _pos[3])
        config.remapImageBlockDestination = [_pos[0], _pos[1]]
        config.filterRemapContracting = 1
        pieceLogger(f"Expanidng done {config.newFilterStartX}")
    else:
        config.filterRemappingProb = 1.0
        config.remapImageBlockSection = (_pos[0], _pos[1], _pos[2], _pos[3])
        config.remapImageBlockDestination = [_pos[0], _pos[1]]
        config.filterRemappingProb = 1.0


def contractFilterRemap():
    _pos = list(config.remapImageBlockSection)
    # pieceLogger(_pos)
    # _pos[0] += config.contractXSpeed
    # _pos[2] -= config.contractXSpeed
    # _pos[1] += config.contractYSpeed
    _pos[3] -= config.contractYSpeed

    if _pos[0] >= _pos[2] or _pos[1] >= _pos[3]:
        config.filterRemappingProb = config.basefilterRemappingProb
        config.filterRemapContracting = 0
        config.remapImageBlockSection = (_pos[2],_pos[3],_pos[2],_pos[3])
        config.remapImageBlockDestination = [_pos[0], _pos[1]]
        pieceLogger(f"contracting done {_pos} {config.filterRemapContracting} {config.filterRemappingProb}")
    else:
        # pieceLogger(_pos)
        config.filterRemappingProb = 1.0
        config.remapImageBlockSection = tuple(_pos)
        config.remapImageBlockDestination = [_pos[0], _pos[1]]
        config.filterRemappingProb = 1.0


def remapFilter(config):
    """Remaps the filter block section."""
    config.filterRemap = True
    if config.filterRemappingProb != 1.0 and config.filterRemapContracting == 0:
        config.filterRemapContracting = 2
        config.newFilterStartX = round(random.uniform(0, config.filterRemapRangeX))
        config.newFilterStartY = round(random.uniform(0, config.filterRemapRangeY))
        config.newFilterEndX = round(random.uniform(config.filterRemapMinHoriSize, config.filterRemapMaxHoriSize))
        config.newFilterEndY = round(random.uniform(config.filterRemapMinVertSize, config.filterRemapMaxVertSize))
        config.remapImageBlockSection = (config.newFilterStartX + config.newFilterEndX, 
                                         config.newFilterStartY, 
                                         config.newFilterStartX + config.newFilterEndX, 
                                         config.newFilterStartY + config.newFilterEndY)
        pieceLogger("Resetting to expand")
        # pieceLogger(f"{config.newFilterStartX} {config.newFilterStartY} {config.newFilterEndX + config.newFilterStartX} {config.newFilterEndY}")

    if config.filterRemapContracting == 1:
        # pieceLogger("Resetting to contract")
        contractFilterRemap()

    if config.filterRemapContracting == 2:
        expandFilterRemap()


# ----------------------------------

def handleFadingAndRebuild():
    """Handles image fading and pattern rebuilding."""
    if config.fader.fadingDone:
        # config.fader.fadingDone = False
        # config.fader.startingImage = config.canvasImage

        config.fader.totalBlocksToChange = 0
        if config.doneCount >= config.numberOfSections and config.rebuildImmediatelyAfterDone:
            config.doSectionDisturbance = False
            pieceLogger("rebuildPatterns called after fading done")
            rebuildPatterns()

    if random.random() < config.resetOverlayProbability and config.usePolygonOverlay:
        loadPolyOverlaybaseValues()


def saveImageIfDone():
    """Saves the image if all sections are done and not already saved."""
    if config.doneCount >= config.numberOfSections and not config.drawingPrinted:
        config.fader.totalBlocksToChange = 40
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
            pieceLogger(f"\nhandlePatternRebuild(): Rebuiding full : {config.combinationSets[config.currentCombinationsetIndex].name}")
            config.settingUpPattern = True
            config.patternSequence = []
            # selectNewPalette(True)
            # selectNewPalette()
        else:
            pieceLogger(f"\nhandlePatternRebuild(): Rebuiding parts: {config.combinationSets[config.currentCombinationsetIndex].name}")
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
        try:
            pieceLogger(f"handlePatternRebuild(): config.settingUpPattern {config.settingUpPattern} | color palette : {config.palettes[config.currentPaletteIndex]}")
        except Exception as e:
            pieceLogger(e)
        # pieceLogger(f"handlePatternRebuild(): config.slotsToChange {config.slotsToChange}")
        rebuildPatterns()


def drawBackgroundAndPasteImage():
    """Draws the background and pastes the main image."""
    if config.doTransition:

        for _ in range(config.faderDoingRefreshCountIterations):
            config.fader.fadeIn(config)
            for _patch, _px, _py in config.fader.crossFadePatches:
                config.compositeImage.paste(_patch, (_px, _py), _patch)

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


def renderComposite():
    """FINAL RENDERING CALL"""
    if config.useDrawingPoints == True:
        config.panelDrawing.canvasToUse = config.compositeImage
        config.panelDrawing.render()
    else:
        if config.usePolygonOverlay:
            config.compositeImage = shapeOverLayFunction(config.compositeImage)

        # config.compositeImageDraw = ImageDraw.Draw(config.compositeImage)
        # config.destinationImageDraw = ImageDraw.Draw(config.destinationImage)
        # config.compositeImageDraw.rectangle((60,70,128,120), fill = (255,0,0,50))
        # config.patternImageDraw.rectangle((60, 70, 128, 120), fill=(255, 0, 0, 50))

        # config.destinationImage.paste(config.compositeImage, (0, 0), config.compositeImage)
        
        config.destinationImage.paste(config.compositeImage, (round(config.imageXPOS), round(config.imageYPOS)), config.compositeImage)
        config.destinationImage.paste(config.compositeImage, (round(config.imageXPOS - config.pictureWidth), round(config.imageYPOS)), config.compositeImage)

        config.imageXPOS += config.XPOSSpeed
        # config.imageYPOS += config.YPOSSpeed

        if config.imageXPOS >= config.pictureWidth:
            config.imageXPOS = 0

        if config.imageYPOS >= config.pictureHeight:
            config.imageYPOS = 0

        # showDebugCanvases(config)
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
        
        # config.image = config.destinationImage.copy()
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
    # config.destinationImage.paste(config.canvasImage, canvasImageCoord, config.canvasImage)
    # config.destinationImage.paste(config.fader.startingImage, startingImageCoord, config.fader.startingImage)
    # config.destinationImage.paste(config.fader.crossFadeImage, crossFadeImageCoord, config.fader.crossFadeImage)
    # config.destinationImage.paste(config.fader.endImage, endImageCoord, config.fader.endImage)


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


def loadAndInitializeCrossFader():

    pieceLogger("Initialize cross fader")
    loadConfigValue(config, workConfig, "movingpattern", "fadeThroughIncrement", 0.1, float)
    loadConfigValue(config, workConfig, "movingpattern", "faderProbDissolve", .5, float)
    loadConfigValue(config, workConfig, "movingpattern", "faderLargeBlockXSections", 10, int)
    loadConfigValue(config, workConfig, "movingpattern", "faderLargeBlockYSections", 3, int)
    loadConfigValue(config, workConfig, "movingpattern", "faderSmallBlockXSections", 40, int)
    loadConfigValue(config, workConfig, "movingpattern", "faderSmallBlockYSections", 40, int)
    loadConfigValue(config, workConfig, "movingpattern", "sectionDeltaWidth", 0, int)
    loadConfigValue(config, workConfig, "movingpattern", "sectionDeltaHeight", 0, int)
    loadConfigValue(config, workConfig, "movingpattern", "faderParallelBlocks", 1, int)
    loadConfigValue(config, workConfig, "movingpattern", "faderFadeDoingRefreshCountIterations", 20, int)
    loadConfigValue(config, workConfig, "movingpattern", "faderDissolveDoingRefreshCountIterations", 100, int)
    loadConfigValue(config, workConfig, "movingpattern", "faderDoingRefreshCountIterationsStartup", 500, int)

    config.doTransition = True
    config.doneCount = 0
    config.faderInit = True
    config.faderDoingRefreshCountIterations = config.faderDoingRefreshCountIterationsStartup
    config.fader = Fader()
    config.fader.height = config.pictureHeight
    config.fader.width = config.pictureWidth
    config.fader.startingImage = Image.new("RGBA", (config.pictureWidth, config.pictureHeight))
    config.fader.endImage = config.canvasImage
    config.fader.destinationImage = config.image
    config.fader.setUp(config)


def createImageHolders():
    ########################################################################
    # CREATE THE IMAGE HOLDERS
    # canvasImage will get the drawing
    # disturbanceImage will get the disturbance / glitching
    # image will be the final output

    config.image = Image.new("RGBA", (config.pictureWidth, config.pictureHeight))
    config.patternImage = Image.new("RGBA", (config.pictureWidth, config.pictureHeight))
    config.patternImageDraw = ImageDraw.Draw(config.patternImage)
    config.canvasImage = Image.new("RGBA", (config.pictureWidth, config.pictureHeight))
    config.nextStateImage = Image.new("RGBA", (config.pictureWidth, config.pictureHeight))
    config.nextStateImageDraw = ImageDraw.Draw(config.nextStateImage)

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
    loadAndInitializeCrossFader()
    setupPolyOverlay()
    loadAndSetupPatterns()
    loadAndSetupAllPalettes()
    disturbance.init(config, workConfig)
    disturbance.setupDisturbances()
    buildPatternSequence(config)

    config.applyDitherBeforeRemapping = True

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


###############################################
