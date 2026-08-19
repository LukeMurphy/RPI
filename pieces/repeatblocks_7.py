# ------------------------------------------##### #
import math
import random
import time
import configparser

from modules.configuration import pieceLogger
from modules.blanks_and_dither_rempping import BlanksAndDitherRemapping
from modules.movieClip import movieClip
from modules import colorutils, panelDrawing, pattern_blocks_v5, disturbance
from modules.holder_director import Holder
from modules.holder_director import Director
from modules.coloroverlay import ColorOverlay
from PIL import Image, ImageDraw, ImageEnhance, ImageOps, ImageChops
from copy import copy

# This version substitutes the overlay disturbance with a slide-repeating of a section

# Adding the wave deformation to get a slightly more organic
# pattern distortion - might be too much, too expected but
# is dreamy  4-3-2024

# major refactoring along with pattern_blocks.py 2025-02-19

# more refactoring including slow scrolling and timing controls


# --------------------- CLASSES     ---------------------

class RepeatedPatterns:
    path = ""
    brightness = 1.0
    setupDeBug = False
    blockWidthMin = 48
    blockWidthMax = 64
    yOffset = 12
    yOffset2 = 13
    blockRotation = 0.0
    canvasRotation = -0.0
    imgcanvasOffsetX = 0
    imgcanvasOffsetY = 0
    pictureWidth = 512
    pictureHeight = 224
    repeatProb = 0.99
    saveImages = False
    outPutPath = ""
    drawBGColorEachCycle = True
    repeatDrawingMode = 1
    loadAnImageProb = 0.0
    imageSources = []
    useBlurSection = False
    blurSectionWidth = 120
    blurSectionHeight = 60
    blurSectionXPos = 220
    blurSectionYPos = 0
    mask_blur_amt = 20
    cp_blur_amt = 3
    resetOverlayProbability = 0.0
    useClipPlayer = True
    clipXPos = 100
    clipYPos = 100
    clipRotate = 90.0
    steps = 2
    fadeThroughIncrement = 0.005
    faderProbDissolve = 0.2
    faderLargeBlockXSections = 10
    faderLargeBlockYSections = 2
    faderSmallBlockXSections = 32
    faderSmallBlockYSections = 64
    sectionDeltaWidth = 20
    sectionDeltaHeight = 5
    faderParallelBlocks = 5
    faderFadeDoingRefreshCountIterations = 1
    faderDissolveDoingRefreshCountIterations = 20
    faderDoingRefreshCountIterationsStartup = 100
    doTransition = True
    doneCount = 0
    faderInit = False
    faderDoingRefreshCountIterations = 100
    fader = None
    usePolygonOverlay = False
    polyOverlay = None
    tileOverlayGridProb = 0.5
    poly_alpha = 255
    useOverlayTileGrid = True
    polyOverlayMode = "overlay"
    polyOverlayChangeProb = 0.001
    tileOverlayGrid = []
    polyBase = []
    patternSequence = []
    slotsToChange = []
    settingUpPattern = True
    lastPatternSelected = ""
    consecutivePatternChoiceCount = 0
    consecutivePatternCount = 0
    rebuildAllSlotsProb = 0.001
    rebuildIndividualSlotProb = 0.9
    chanceRebuildPatternChoosesRandom = 0.2
    rebuildSlotSkipRate = 0.1
    rebuildSlotStartSkipRate = 0.05
    patternModel = None
    rebuildPatternProbability = 0.0004
    probPatternsRebuildAfterNewPalette = 0.99
    changePaletteWhenRebuildProb = 0.25
    patternChangeWhenBuilding = 0.05
    changeFullPaletteWhenChangingPatternProb = 0.5
    changeEachblockWhenChangingPatternProb = 0.95
    changePaletteWhenChangingPatternProb = 0.0
    altColoringProb = 0.5
    popRandomColorProb = False
    blockSizeChangeProb = 0.5
    blockSizeChangeAlwaysUseMax = False
    numScaleRows = 4
    stepsRange = (2, 3)
    ringsRange = (10, 18)
    patternOrientation = -90.0
    numRows = 2
    numRowsRandomize = False
    linesOnly = False
    waveScaleRings = 18
    waveScaleSteps = 2
    usePixelSortRandomize = False
    randomBlockProb = 0.99
    randomBlockWidth = 0
    randomBlockHeight = 0
    decoBoxBandWidth = 3
    diamondUseTriangles = False
    diamondStep = 1
    minnumConcentricBoxes = 2
    maxnumConcentricBoxes = 16
    numShingleRows = 2
    amplitude = 9
    amplitude2 = 9
    shingleVariation = True
    shingleVariationRange = 6
    shingleVariationAmount = 6
    numDotRows = 3
    speedFactor = 1.0
    phaseFactor = 4.0
    xSpeed = 0.8
    ySpeed = 0.1
    ySpeedInit = 0.1
    lineDiff = 2
    useDoubleLine = True
    randomizeSpeed = True
    steps2 = 2
    xIncrementer = 1
    yIncrementer = 1
    combinationSets = []
    changeCombinationAnytimeProb = 0.99
    currentCombinationsetIndex = 7
    numberOfRandomizersUsed = 0
    comboSetDirector = None
    palettesConfigFile = ""
    paletteConfig = None
    palettes = []
    bgColorAlpha = [100, 250]
    allAvailablePalettesList = []
    c1 = None
    c2 = None
    c3 = None
    c4 = None
    currentPaletteIndex = 0
    transformShape = False
    transformTuples = (1.2, 0.0, 1.0, -0.0, 1.0, 0.1, 0.005, 0.0)
    useWaveDistortion = True
    waveAmplitude = 20.0
    waveAmplitudeMax = 40.0
    waveAmplitudeMin = -20.0
    waveAmplitudeSpeed = 0.0001
    wavePeriodMod = 5.0
    wavegridspace = 30
    pNoiseMod = 10.0
    waveDeformXPosRate = 0.001
    waveDeformXPos = 0
    sectionDisturbance = True
    doSectionDisturbance = False
    disturbanceConfigSets = ["heavy"]
    changeDisturbanceSetProb = 0.25
    skipFrames = 0
    skipFramesCount = 0
    disturbanceConfigFile = ""
    disturbanceConfig = None
    baseSectionSpeed = 0.2
    sectionPlacementXRange = (-10, 384)
    sectionPlacementYRange = (-10, 200)
    sectionWidthRange = (88, 180)
    sectionHeightRange = (88, 180)
    numberOfSections = 20
    sectionMovementCountMax = 100
    redoSectionDisturbance = 0.01
    rebuildImmediatelyAfterDone = False
    disturbanceScaleX = 9.0
    disturbanceScaleY = 9.0
    stableSectionsMin = 2
    stableSectionsMax = 3
    stableSectionsMinWidth = 20
    stableSectionsMinHeight = 24
    stableSegments = []
    movingSections = []
    drawingPrinted = False
    blockWidth = 48
    blockHeight = 48
    blockImage = None
    blockDraw = None
    patternBlockCols = 11
    patternBlockRows = 5
    totalSlots = 55
    altLineColoring = True
    numConcentricBoxes = 3
    floral = None
    usedPatterns = []
    initPatternBuild = False
    randomInsertionCount = 0
    useBorderPattern = False
    borderPattern = ""
    patternsInBands = False
    borderDrawn = False
    imageXPOS = 0
    imageYPOS = 0
    XPOSSpeed = 0.0
    YPOSSpeed = 0.0
    useSubPixelSmoothing = True


    filterRemapping = True
    filterRemappingProb = .0005
    filterRemapMinHoriSize = 32
    filterRemapMinVertSize = 32
    filterRemapMaxHoriSize = 256
    filterRemapMaxVertSize = 192
    filterRemapRangeX = 256
    filterRemapRangeY = 192

    rows = 0
    cols = 0
    tileSizeWidth = 0
    tileSizeHeight = 0

    def __init__(self):
        pass

    def debugSelf(self):
        allArgs = self.__dict__
        for element in allArgs:
            print(f"{element} = {allArgs[element]}")

        method_list = [attribute for attribute in dir(self) if callable(getattr(self, attribute)) and attribute.startswith("__") is False]
        # print(f"[RepeatedPatterns] {method_list}")


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
            sectionDeltaWidth = rpO.sectionDeltaWidth
            sectionDeltaHeight = rpO.sectionDeltaHeight
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

        if config.faderInit:
            config.faderInit = False
        else:
            if self.fadeInMode == 0:
                config.faderDoingRefreshCountIterations = config.faderFadeDoingRefreshCountIterations
            if self.fadeInMode == 1:
                config.faderDoingRefreshCountIterations = config.faderDissolveDoingRefreshCountIterations

        pieceLogger(f" >> Fader initialized setup {self.fadeInMode} {config.faderDoingRefreshCountIterations}")

        self.blankImage = Image.new("RGBA", (self.width, self.height))
        self.startingImage = Image.new("RGBA", (self.width, self.height))
        self.endImage = Image.new("RGBA", (self.width, self.height))
        self.crossFadeImage = Image.new("RGBA", (self.width, self.height))
        self.xRange = [0, config.pictureWidth]
        self.yRange = [0, rpO.pictureHeight]

        self.fadeThroughIncrement = config.fadeThroughIncrement
        self.numParallelBlocks = getattr(config, "faderParallelBlocks", 1)

        self.largeBlocks = self.makeSections(0, rpO.pictureWidth, 0, rpO.pictureHeight, config.faderLargeBlockXSections, config.faderLargeBlockYSections, True)
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
        rpO.doTransition = False
        # pieceLogger("=> FADING DONE")

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
            if (self.x + _w) <= self.x:
                # pieceLogger(_w)
                _w = 0

            if (self.y + _h) <= self.y:
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
        pieceLogger(" >> Saving Image...")
        fn = f"{baseName}.png"
        renderImage.save(fn)


def loadImageForBase():
    # image = Image.open("./assets/imgs/drawings/P1060494.jpg", "r")
    # image = Image.open("./assets/imgs/miscl/comp-384.jpg", "r")
    # image = Image.open("./assets/imgs/miscl/lm_a.png", "r")

    i = math.floor(random.random() * len(config.imageSources))
    imagePath = config.imageSources[i]
    pieceLogger(f" >> {imagePath}")
    image = Image.open(imagePath)
    image.load()
    config.canvasImage.paste(image, (0, 0))


def loadClipPlayerConfigs():
    loadConfigValue(rpO, workConfig, "imageSequencePlayer", "useClipPlayer", False, bool)
    loadConfigValue(rpO, workConfig, "imageSequencePlayer", "clipXPos", 1, int)
    loadConfigValue(rpO, workConfig, "imageSequencePlayer", "clipYPos", 1, int)
    loadConfigValue(rpO, workConfig, "imageSequencePlayer", "clipRotate", 0, float)
    loadConfigValue(rpO, workConfig, "imageSequencePlayer", "steps", 1, int)


    try:
        rpO.clipMain = movieClip(rpO)
        rpO.clipMain.clipRotate = rpO.clipRotate
        rpO.clipMain.setUp(workConfig)
    except Exception as e:
        pieceLogger(f" >> {e} \n")
        rpO.useClipPlayer = False


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
        pieceLogger(f"\n >> Config value not loaded:{obj} {workConfig} {section} {option} ==> will be set to {default} \n  {e}", 1)
        setattr(obj, option, default)


# --------------------- PALETTES      ---------------------


def loadAndSetupAllPalettes():
    global workConfig
    """initial palatte setups -- needs to run after combinations are established"""
    rpO.palettesConfigFile = workConfig.get("movingpattern", "palettesConfigFile")

    rpO.paletteConfig = configparser.ConfigParser()
    argument = f"{rpO.path}/configs/{rpO.palettesConfigFile}"

    pieceLogger(f" >> loading from {argument}")
    rpO.paletteConfig.read(argument)

    rpO.palettes = rpO.paletteConfig.get("palettesIncluded", "palettes").replace("\n", "").split(",")
    rpO.paletteConfigs = rpO.paletteConfig.get("palettesIncluded", "palettes").replace("\n", "").split(",")

    bgColorAlpha = (workConfig.get("movingpattern", "bgColorAlpha")).split(",")
    rpO.bgColorAlpha = list(map(lambda x: (int(x)), bgColorAlpha))

    # buildPalette(rpO, 0)

    rpO.allAvailablePalettesList = []
    rpO.c1 = Holder()
    rpO.c2 = Holder()
    rpO.c3 = Holder()
    rpO.c4 = Holder()

    for arg in rpO.paletteConfigs:
        if arg != "":
            loadPalette(arg)

    # rpO.currentPaletteIndex = 0
    rpO.currentPaletteIndex = math.floor(random.uniform(0, len(rpO.combinationSets[rpO.currentCombinationsetIndex].palettes)))
    setPalette(rpO, rpO.currentPaletteIndex)
    # config.borderPalette = changeSinglePalette(rpO.currentCombinationsetIndex)


def loadPalette(palette):
    global config
    # palette = config.palettes[index]

    pieceLogger(f" >> Loading palette {palette}")
    c1 = Holder()
    c2 = Holder()
    c3 = Holder()
    c4 = Holder()

    _noGraysBool = rpO.paletteConfig.getboolean(palette, "noGrays", fallback=False)
    _noGrays = 1.0 if _noGraysBool else 0.0

    # background
    # tLimitBase = int(workConfig.get(palette, "tLimitBase"))
    c1.minHue = float(rpO.paletteConfig.get(palette, "c1_minHue"))
    c1.maxHue = float(rpO.paletteConfig.get(palette, "c1_maxHue"))
    c1.minSaturation = float(rpO.paletteConfig.get(palette, "c1_minSaturation"))
    c1.maxSaturation = float(rpO.paletteConfig.get(palette, "c1_maxSaturation"))
    c1.minValue = float(rpO.paletteConfig.get(palette, "c1_minValue"))
    c1.maxValue = float(rpO.paletteConfig.get(palette, "c1_maxValue"))
    c1.dropHueMin = float(rpO.paletteConfig.get(palette, "c1_dropHueMin", fallback=0))
    c1.dropHueMax = float(rpO.paletteConfig.get(palette, "c1_dropHueMax", fallback=0))
    c1.noGrays = _noGrays
    c1.currentColor = setCurrentColor(c1)

    # color 1
    # tLimitBase = int(rpO.paletteConfig.get(palette, "line_tLimitBase"))
    c2.minHue = float(rpO.paletteConfig.get(palette, "c2_minHue"))
    c2.maxHue = float(rpO.paletteConfig.get(palette, "c2_maxHue"))
    c2.minSaturation = float(rpO.paletteConfig.get(palette, "c2_minSaturation"))
    c2.maxSaturation = float(rpO.paletteConfig.get(palette, "c2_maxSaturation"))
    c2.minValue = float(rpO.paletteConfig.get(palette, "c2_minValue"))
    c2.maxValue = float(rpO.paletteConfig.get(palette, "c2_maxValue"))
    c2.dropHueMin = float(rpO.paletteConfig.get(palette, "c2_dropHueMin", fallback=0))
    c2.dropHueMax = float(rpO.paletteConfig.get(palette, "c2_dropHueMax", fallback=0))
    c2.noGrays = _noGrays
    c2.currentColor = setCurrentColor(c2)
    # color 2
    # tLimitBase = int(rpO.paletteConfig.get(palette, "line2_tLimitBase"))
    c3.minHue = float(rpO.paletteConfig.get(palette, "c3_minHue"))
    c3.maxHue = float(rpO.paletteConfig.get(palette, "c3_maxHue"))
    c3.minSaturation = float(rpO.paletteConfig.get(palette, "c3_minSaturation"))
    c3.maxSaturation = float(rpO.paletteConfig.get(palette, "c3_maxSaturation"))
    c3.minValue = float(rpO.paletteConfig.get(palette, "c3_minValue"))
    c3.maxValue = float(rpO.paletteConfig.get(palette, "c3_maxValue"))
    c3.dropHueMin = float(rpO.paletteConfig.get(palette, "c3_dropHueMin", fallback=0))
    c3.dropHueMax = float(rpO.paletteConfig.get(palette, "c3_dropHueMax", fallback=0))
    c3.noGrays = _noGrays
    c3.currentColor = setCurrentColor(c3)

    c4.minHue = float(rpO.paletteConfig.get(palette, "c4_minHue", fallback=0))
    c4.maxHue = float(rpO.paletteConfig.get(palette, "c4_maxHue", fallback=0))
    c4.minSaturation = float(rpO.paletteConfig.get(palette, "c4_minSaturation", fallback=0))
    c4.maxSaturation = float(rpO.paletteConfig.get(palette, "c4_maxSaturation", fallback=0))
    c4.minValue = float(rpO.paletteConfig.get(palette, "c4_minValue", fallback=0))
    c4.maxValue = float(rpO.paletteConfig.get(palette, "c4_maxValue", fallback=0))
    c4.dropHueMin = float(rpO.paletteConfig.get(palette, "c4_dropHueMin", fallback=0))
    c4.dropHueMax = float(rpO.paletteConfig.get(palette, "c4_dropHueMax", fallback=0))
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

    rpO.allAvailablePalettesList.append(_paletteObj)


def getPaletteObjectByName(_name):
    for _n in rpO.allAvailablePalettesList:
        if _n.paletteName == _name:
            return _n


def changeSinglePalette(index=0):
    # pieceLogger(f"changeSinglePalette  {index}")
    paletteObj = getPaletteObjectByName(rpO.combinationSets[rpO.currentCombinationsetIndex].palettes[index])
    _paletteObjLocal = Holder()
    _paletteObjLocal.paletteName = rpO.combinationSets[rpO.currentCombinationsetIndex].palettes[index]
    _paletteObjLocal.c1 = copy(paletteObj.c1)
    _paletteObjLocal.c1.currentColor = copy(paletteObj.c1.currentColor)
    _paletteObjLocal.c2 = copy(paletteObj.c2)
    _paletteObjLocal.c2.currentColor = copy(paletteObj.c2.currentColor)
    _paletteObjLocal.c3 = copy(paletteObj.c3)
    _paletteObjLocal.c3.currentColor = copy(paletteObj.c3.currentColor)
    _paletteObjLocal.c4 = copy(paletteObj.c4)
    _paletteObjLocal.c4.currentColor = copy(paletteObj.c4.currentColor)

    _paletteObjLocal.c1.currentColor = setCurrentColor(paletteObj.c1, 0, 0, round(random.uniform(rpO.bgColorAlpha[0], rpO.bgColorAlpha[1])))
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
    paletteObj = getPaletteObjectByName(rpO.combinationSets[rpO.currentCombinationsetIndex].palettes[index])

    pieceLogger(
        f"\n >> currentCombinationsetIndex: {rpO.currentCombinationsetIndex} index: {index} rpO.combinationSets[rpO.currentCombinationsetIndex].palettes[index]: {rpO.combinationSets[rpO.currentCombinationsetIndex].palettes[index]}"
    )
    pieceLogger(f" >> Setting a new palette:  {paletteObj.paletteName}")
    rpO.c1.bgColor = setCurrentColor(paletteObj.c1, 0, 0, round(random.uniform(rpO.bgColorAlpha[0], rpO.bgColorAlpha[1])))
    rpO.c1.currentColor = setCurrentColor(paletteObj.c1)
    rpO.c2.currentColor = setCurrentColor(paletteObj.c2)
    rpO.c3.currentColor = setCurrentColor(paletteObj.c3)
    rpO.c4.currentColor = setCurrentColor(paletteObj.c4)

    # if zero palette mixing is desired, force the patterns to rebuild
    # this is a bit of an extreme but was having trouble preventing the
    # palette mixing and making unpleasant combinations

    # if config.changePaletteWhenChangingPatternProb == 0.0:
    # buildPatternSequence(config)


def selectNewPalette(_setPalette=True):

    # rather than favoring a normal distribution, use a list - getting tired of trying to game the randomness by ordering the list of palettes etc
    # rpO.currentPaletteIndex = math.floor(random.uniform(0, len(rpO.combinationSets[rpO.currentCombinationsetIndex].palettes)))
    _listOfIndecies = list(range(len(rpO.combinationSets[rpO.currentCombinationsetIndex].palettes)))
    rpO.currentPaletteIndex = random.choice(_listOfIndecies)

    pieceLogger(
        f" >> Choosing a palette: {rpO.combinationSets[rpO.currentCombinationsetIndex].palettes[rpO.currentPaletteIndex]} in {rpO.combinationSets[rpO.currentCombinationsetIndex].name}",
        2,
        True,
    )
    setPalette(rpO, rpO.currentPaletteIndex)

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
    # loadConfigValue(rpO, workConfig, "movingpattern", "dominantPatternProb", 0, float)

    rpO.patternSequence = []
    rpO.slotsToChange = []
    rpO.settingUpPattern = True
    rpO.lastPatternSelected = ""
    rpO.consecutivePatternChoiceCount = 0
    rpO.consecutivePatternCount = 0

    # when rebuild is called, chance that the full pattern gets rebuilt -
    loadConfigValue(rpO, workConfig, "movingpattern", "rebuildAllSlotsProb", 0.50, float)
    # when rebuild is called and the full rebuild is not called, individual slots can change
    # at this rate
    loadConfigValue(rpO, workConfig, "movingpattern", "rebuildIndividualSlotProb", 0.0, float)
    # at this rate
    loadConfigValue(rpO, workConfig, "movingpattern", "chanceRebuildPatternChoosesRandom", 0.0, float)
    loadConfigValue(rpO, workConfig, "movingpattern", "rebuildSlotSkipRate", 0.1, float)
    loadConfigValue(rpO, workConfig, "movingpattern", "rebuildSlotStartSkipRate", 0.1, float)
    loadConfigValue(rpO, workConfig, "movingpattern", "patternModel", None, str)

    # patternSequence = workConfig.get("movingpattern", "patternSequence").split(",")
    # config.patternSequence = []

    config.rotateAltBlock = 0

    # --------------------- PATTERN CHANGE   ---------------------
    # higher = more variation in patterns
    # e.g. .2 is 20% chance each new block will change to a
    # new pattern

    loadConfigValue(rpO, workConfig, "movingpattern", "rebuildPatternProbability", 0.0, float)
    loadConfigValue(rpO, workConfig, "movingpattern", "probPatternsRebuildAfterNewPalette", 1.0, float)
    loadConfigValue(rpO, workConfig, "movingpattern", "changePaletteWhenRebuildProb", 0.0, float)
    loadConfigValue(rpO, workConfig, "movingpattern", "patternChangeWhenBuilding", 0.0, float)
    loadConfigValue(rpO, workConfig, "movingpattern", "changeFullPaletteWhenChangingPatternProb", 0.0, float)
    loadConfigValue(rpO, workConfig, "movingpattern", "changeEachblockWhenChangingPatternProb", 1.0, float)
    loadConfigValue(rpO, workConfig, "movingpattern", "changePaletteWhenChangingPatternProb", 0.0, float)
    loadConfigValue(rpO, workConfig, "movingpattern", "altColoringProb", 0.0, float)
    loadConfigValue(rpO, workConfig, "movingpattern", "popRandomColorProb", 0.8, float)
    loadConfigValue(rpO, workConfig, "movingpattern", "blockSizeChangeProb", 0.0, float)
    loadConfigValue(rpO, workConfig, "movingpattern", "blockSizeChangeAlwaysUseMax", False, bool)

    try:
        ringsRange = workConfig.get("movingpattern", "ringsRange").split(",")
        stepsRange = workConfig.get("movingpattern", "stepsRange").split(",")
        rpO.numScaleRows = int(workConfig.get("movingpattern", "numScaleRows"))
        rpO.stepsRange = tuple(map(lambda x: int(x), stepsRange))
        rpO.ringsRange = tuple(map(lambda x: int(x), ringsRange))
    except Exception as e:
        pieceLogger(e, 1)
        rpO.stepsRange = (1, 1)
        rpO.ringsRange = (1, 1)
        rpO.numScaleRows = rpO.numShingleRows

    loadConfigValue(rpO, workConfig, "movingpattern", "patternOrientation", 0, float)
    loadConfigValue(rpO, workConfig, "movingpattern", "numRows", 5, int)
    loadConfigValue(rpO, workConfig, "movingpattern", "numRowsRandomize", False, bool)

    # affects patterns to use just lines w/o fills
    loadConfigValue(rpO, workConfig, "movingpattern", "linesOnly", False, bool)

    # try:
    #     config.borderPattern = workConfig.get("movingpattern", "borderPattern")
    #     config.useBorderPattern = workConfig.getboolean("movingpattern", "useBorderPattern")
    # except Exception as e:
    #     print(e)
    #     config.borderPattern = config.patterns[0]
    #     config.useBorderPattern = False
    # end try

    rpO.waveScaleRings = round(random.uniform(rpO.ringsRange[0], rpO.ringsRange[1]))
    rpO.waveScaleSteps = round(random.uniform(rpO.stepsRange[0], rpO.stepsRange[1]))
    # print(config.waveScaleRings, config.waveScaleSteps)
    # end try

    # for the randomizer
    loadConfigValue(rpO, workConfig, "movingpattern", "usePixelSortRandomize", True, bool)
    loadConfigValue(rpO, workConfig, "movingpattern", "randomBlockProb", 0.0, float)
    loadConfigValue(rpO, workConfig, "movingpattern", "randomBlockWidth", 10, int)
    loadConfigValue(rpO, workConfig, "movingpattern", "randomBlockHeight", 10, int)
    loadConfigValue(rpO, workConfig, "movingpattern", "decoBoxBandWidth", 10, int)

    rpO.diamondUseTriangles = False
    loadConfigValue(rpO, workConfig, "movingpattern", "diamondStep", 1, int)
    loadConfigValue(rpO, workConfig, "movingpattern", "minnumConcentricBoxes", 1, int)
    loadConfigValue(rpO, workConfig, "movingpattern", "maxnumConcentricBoxes", 8, int)
    loadConfigValue(rpO, workConfig, "movingpattern", "numShingleRows", 1, int)
    loadConfigValue(rpO, workConfig, "movingpattern", "amplitude", 1, int)
    loadConfigValue(rpO, workConfig, "movingpattern", "amplitude2", 1, int)
    loadConfigValue(rpO, workConfig, "movingpattern", "shingleVariation", False, bool)
    loadConfigValue(rpO, workConfig, "movingpattern", "shingleVariationRange", 1, int)
    rpO.shingleVariationAmount = rpO.shingleVariationRange

    loadConfigValue(rpO, workConfig, "movingpattern", "numDotRows", 1, int)
    loadConfigValue(rpO, workConfig, "movingpattern", "speedFactor", 0.0, float)
    loadConfigValue(rpO, workConfig, "movingpattern", "phaseFactor", 0.0, float)
    loadConfigValue(rpO, workConfig, "movingpattern", "xSpeed", 0.0, float)
    loadConfigValue(rpO, workConfig, "movingpattern", "ySpeed", 0.0, float)
    rpO.ySpeedInit = rpO.ySpeed

    loadConfigValue(rpO, workConfig, "movingpattern", "lineDiff", 1, int)
    loadConfigValue(rpO, workConfig, "movingpattern", "useDoubleLine", False, bool)
    loadConfigValue(rpO, workConfig, "movingpattern", "randomizeSpeed", False, bool)

    # used in pattern_blocks code
    loadConfigValue(rpO, workConfig, "movingpattern", "steps", 1, int)
    loadConfigValue(rpO, workConfig, "movingpattern", "steps2", 1, int)

    loadConfigValue(rpO, workConfig, "movingpattern", "xIncrementer", 1, int)
    loadConfigValue(rpO, workConfig, "movingpattern", "yIncrementer", 1, int)

    config.altLineColoring = False
    stepsRange = workConfig.get("movingpattern", "stepsRange").split(",")

    loadAndSetCombinations()


def loadAndSetCombinations():
    rpO.combinationSets = []
    combinationSets = workConfig.get("movingpattern", "combinationSets").replace("\n", "").split(",")
    rpO.changeCombinationAnytimeProb = float(workConfig.get("movingpattern", "changeCombinationAnytimeProb", fallback=0))
    for combinationSetName in combinationSets:
        comboSet = CombinationSet(combinationSetName)
        comboSet.patterns = workConfig.get(combinationSetName, "patterns").replace("\n", "").split(",")
        comboSet.palettes = workConfig.get(combinationSetName, "palettes").replace("\n", "").split(",")
        comboSet.dominantPatterns = workConfig.get(combinationSetName, "dominantPatterns", fallback="").replace("\n", "").split(",")
        comboSet.dominantPatternProb = float(workConfig.get(combinationSetName, "dominantPatternProb", fallback=0))
        comboSet.borderPattern = workConfig.get(combinationSetName, "borderPattern", fallback="")
        comboSet.useBorderPattern = workConfig.getboolean(combinationSetName, "useBorderPattern", fallback=False)
        comboSet.altColoringProb = float(workConfig.get(combinationSetName, "altColoringProb", fallback=rpO.altColoringProb))
        comboSet.popRandomColorProb = float(workConfig.get(combinationSetName, "popRandomColorProb", fallback=rpO.popRandomColorProb))

        comboSet.usePolygonOverlay = workConfig.getboolean(combinationSetName, "usePolygonOverlay", fallback=rpO.usePolygonOverlay)
        comboSet.tileOverlayGridProb = float(workConfig.get(combinationSetName, "tileOverlayGridProb", fallback=rpO.tileOverlayGridProb))
        comboSet.polyOverlayMode = workConfig.get(combinationSetName, "polyOverlayMode", fallback=rpO.polyOverlayMode)

        comboSet.patternsInBands = workConfig.getboolean(combinationSetName, "patternsInBands", fallback=False)
        comboSet.altBlockRotation = workConfig.getboolean(combinationSetName, "altBlockRotation", fallback=True)

        comboSet.combinationSetsMinTime = float(workConfig.get(combinationSetName, "combinationSetsMinTime", fallback=30))
        comboSet.combinationSetsMaxTime = float(workConfig.get(combinationSetName, "combinationSetsMaxTime", fallback=60))

        comboSet.maxNumberOfRandomizers = int(workConfig.get(combinationSetName, "maxNumberOfRandomizers", fallback=3))
        comboSet.minNumberOfPatternVariations = int(workConfig.get(combinationSetName, "minNumberOfPatternVariations", fallback=0))

        comboSet.randomInsertions = workConfig.get(combinationSetName, "randomInsertions", fallback="0,0").split(",")
        comboSet.randomInsertionInitialProbabilitly = float(workConfig.get(combinationSetName, "randomInsertionInitialProbabilitly", fallback=0.0))
        comboSet.randomInsertionProbabilitly = float(workConfig.get(combinationSetName, "randomInsertionProbabilitly", fallback=0.0))
        comboSet.randomInsertionBaseProbabilitly = float(workConfig.get(combinationSetName, "randomInsertionProbabilitly", fallback=0.0))
        comboSet.borderLeakProb = float(workConfig.get(combinationSetName, "borderLeakProb", fallback=0.0))
        comboSet.randomInsertionMin = int(workConfig.get(combinationSetName, "randomInsertionMin", fallback="0"))
        comboSet.randomInsertionMax = int(workConfig.get(combinationSetName, "randomInsertionMax", fallback="0"))
        config.randomInsertionCount = 0
        if comboSet.randomInsertionMin > 0:
            comboSet.randomInsertionProbabilitly = comboSet.randomInsertionInitialProbabilitly

        rpO.combinationSets.append(comboSet)

    # rpO.currentCombinationsetIndex = 0
    rpO.currentCombinationsetIndex = math.floor(random.uniform(0, len(rpO.combinationSets)))
    rpO.numberOfRandomizersUsed = 0
    rpO.comboSetDirector = Director(config)
    rpO.comboSetDirector.slotRate = int(
        random.uniform(
            rpO.combinationSets[rpO.currentCombinationsetIndex].combinationSetsMinTime, rpO.combinationSets[rpO.currentCombinationsetIndex].combinationSetsMaxTime
        )
    )
    pieceLogger(f" Initial combo set change wait time (slotRate) : {rpO.comboSetDirector.slotRate}")


def handleChangeCurrentCominationSet():

    pieceLogger(" >> Checking combo set")
    disturbancesDone = not rpO.doSectionDisturbance or rpO.doneCount >= rpO.numberOfSections

    if random.random() < rpO.changeCombinationAnytimeProb and rpO.fader.fadingDone and disturbancesDone:
        # rather than favoring a normal distribution, use a list - getting tired of trying to game the randomness by ordering the list of palettes etc
        # rpO.currentCombinationsetIndex = math.floor(random.uniform(0, len(rpO.combinationSets)))
        _listOfIndecies = list(range(len(rpO.combinationSets)))
        rpO.currentCombinationsetIndex = random.choice(_listOfIndecies)
        rpO.currentPaletteIndex = math.floor(random.uniform(0, len(rpO.combinationSets[rpO.currentCombinationsetIndex].palettes)))
        setPalette(rpO, rpO.currentPaletteIndex)
        # {rpO.combinationSets[rpO.currentCombinationsetIndex]}
        # pieceLogger(f" >> _listOfIndecies =   {_listOfIndecies}")
        pieceLogger(
            f" >> =====> Combo changed to {rpO.combinationSets[rpO.currentCombinationsetIndex].name} (index: {rpO.currentCombinationsetIndex})",
            2,
            True,
        )
        rpO.numberOfRandomizersUsed = 0

        # problem the currentPaletteIndex may exceed the number of palettes if the combinationSet has changed
        # rpO.currentPaletteIndex = math.floor(random.uniform(0, len(rpO.combinationSets[rpO.currentCombinationsetIndex].palettes)))

        if random.random() < rpO.changePaletteWhenRebuildProb:
            _listOfIndecies = list(range(len(rpO.combinationSets[rpO.currentCombinationsetIndex].palettes)))
            rpO.currentPaletteIndex = random.choice(_listOfIndecies)

        # turning off to test
        # rpO.settingUpPattern = True
        # selectNewPalette()

        # changing so the transition between a new combo set happens in chunks rather than
        # waves

        # config.patternSequence = []
        # config.rebuildIndividualSlotProb = .1

        rpO.comboSetDirector.slotRate = int(
            random.uniform(
                rpO.combinationSets[rpO.currentCombinationsetIndex].combinationSetsMinTime, rpO.combinationSets[rpO.currentCombinationsetIndex].combinationSetsMaxTime
            )
        )
        rpO.comboSetDirector.reset()

        rpO.settingUpPattern = True
        rpO.rebuildPatternProbability = 1.0
        rpO.rebuildAllSlotsProb = 1.0
        rpO.fader.setUp(rpO)
        # rebuildPatterns()

        handlePatternRebuild()

        drawAndProcessPattern()

    else:
        pieceLogger("\n >> No change")


def resetPatternBlocks():

    tempPalette = changeSinglePalette(rpO.currentPaletteIndex)

    pieceLogger(f" >> config.totalSlots {config.totalSlots}", 4, True)

    for i in range(rpO.totalSlots):
        _patternBlock = rpO.patternSequence[i]
        _patternBlock.hasBeenPainted = False
        _patternBlock.tempPalette = tempPalette

        if random.random() > rpO.changeEachblockWhenChangingPatternProb:
            _patternBlock.tempPalette = getTempPalette(rpO)

        rpO.patternSequence[i] = _patternBlock


def buildPatternSequence(_repeatedPatternsObj):
    pieceLogger(" >> called", 0)

    rpO : RepeatedPatterns = _repeatedPatternsObj
    # rpO.patternSequence = []
    # rpO.usedPatterns = []

    # during a partial rebuild, maybe don't change too much
    # in terms of the block size
    if rpO.settingUpPattern:
        if random.random() < rpO.blockSizeChangeProb:
            if rpO.blockSizeChangeAlwaysUseMax:
                rpO.blockWidth = rpO.blockWidthMax
                rpO.blockHeight = rpO.blockWidthMax
            else:
                rpO.blockWidth = round(random.uniform(rpO.blockWidthMin, rpO.blockWidthMax))
                rpO.blockHeight = rpO.blockWidth
        else:
            rpO.blockWidth = rpO.blockWidthMin
            rpO.blockHeight = rpO.blockWidthMin

        rpO.blockImage = Image.new("RGBA", (rpO.blockWidth, rpO.blockHeight))
        rpO.blockDraw = ImageDraw.Draw(rpO.blockImage)

        rpO.patternBlockCols = math.ceil(rpO.pictureWidth / rpO.blockWidth)
        rpO.patternBlockRows = math.ceil(rpO.pictureHeight / rpO.blockHeight)

        # considering making this be an option to fit exactly the width - i.e. choose the number of columns
        # rather than width or an alogrithm to do the fitting - the problem is that then you lose the
        # ragged edges which are a nice trace of the previous state
        # print(f"rpO.blockWidth {rpO.blockWidth} rpO.patternBlockCols {rpO.patternBlockCols}")

        rpO.totalSlots = rpO.patternBlockRows * rpO.patternBlockCols
        # pieceLogger(f"rpO.totalSlots {rpO.totalSlots}", 4, True)

    rpO.altLineColoring = random.random() < rpO.combinationSets[rpO.currentCombinationsetIndex].altColoringProb
    rpO.popRandomColorProb = random.random() < rpO.combinationSets[rpO.currentCombinationsetIndex].popRandomColorProb

    # print(rpO.altLineColoring)
    rpO.numConcentricBoxes = int(random.uniform(rpO.minnumConcentricBoxes, rpO.maxnumConcentricBoxes))

    pattern_blocks_v5.floralConfig(rpO)
    generatePatternSequence(rpO)

    # _print_pattern_sequence(rpO)
    rpO.borderDrawn = False
    rpO.initPatternBuild = False


def chooseAPattern(limitRandomizers=False, forceDominant=False):
    _patterns = rpO.combinationSets[rpO.currentCombinationsetIndex].patterns
    _dominantPatterns = rpO.combinationSets[rpO.currentCombinationsetIndex].dominantPatterns
    _dominantPatternProb = rpO.combinationSets[rpO.currentCombinationsetIndex].dominantPatternProb

    # due to normal distribution this kind of favors the things in the middle of the list
    # should really convert to a random choice operation rather than just numerical random
    # _patternSelected = _patterns[math.floor(random.uniform(0, len(_patterns)))]
    _patternSelected = random.choice(_patterns)

    if random.random() < _dominantPatternProb or forceDominant:
        _patternSelected = _dominantPatterns[math.floor(random.uniform(0, len(_dominantPatterns)))]

    # need to limit randomizers
    if "randomizer" in _patternSelected:
        if limitRandomizers:
            _patternSelected = rpO.lastPatternSelected
        else:
            if rpO.numberOfRandomizersUsed < rpO.combinationSets[rpO.currentCombinationsetIndex].maxNumberOfRandomizers:
                rpO.numberOfRandomizersUsed += 1
            else:
                chooseAPattern()

    # this catches if the same pattern is selected twice in a sequence
    if _patternSelected == rpO.lastPatternSelected:
        rpO.consecutivePatternCount += 1

    return _patternSelected


# this really needs to change to be more readable and predictable ....
# there are n number of slots, just fill each one and change randomly etc
# as they all get filled up
def generatePatternSequence(rpO):

    # config.patternSequence = []
    rpO.usedPatterns = []
    _baseProb = rpO.patternChangeWhenBuilding * rpO.totalSlots / 100
    _patternSelected = chooseAPattern()
    rpO.lastPatternSelected = _patternSelected
    _tempPalette = getTempPalette(rpO)
    _iterCount = 0
    rpO.initPatternBuild = True
    rpO.randomInsertionCount = 0
    rpO.consecutivePatternChoiceCount = 0

    _combo = rpO.combinationSets[rpO.currentCombinationsetIndex]
    rpO.useBorderPattern = _combo.useBorderPattern
    rpO.borderPattern = _combo.borderPattern
    rpO.usePolygonOverlay = _combo.usePolygonOverlay
    rpO.polyOverlayMode = _combo.polyOverlayMode
    rpO.tileOverlayGridProb = _combo.tileOverlayGridProb
    rpO.patternsInBands = _combo.patternsInBands

    _combo.randomInsertionProbabilitly = _combo.randomInsertionInitialProbabilitly

    _randomInserts = _combo.randomInsertions
    _randomInsertionProb = _combo.randomInsertionProbabilitly
    _randomInsertionMax = _combo.randomInsertionMax

    pieceLogger(f" >> COMBINATION SET: {_combo.name} using colors _tempPalette: {_tempPalette.paletteName}", 2, True)

    def add_pattern_block(c, r):
        nonlocal _patternSelected, _tempPalette, _iterCount, _randomInserts, _randomInsertionProb, _randomInsertionMax
        _isBorder = False

        if random.random() < _baseProb:
            _patternSelected = chooseAPattern()
            _tempPalette = getTempPalette(rpO)

        if _combo.minNumberOfPatternVariations > 0:
            if _patternSelected != rpO.lastPatternSelected:
                rpO.consecutivePatternChoiceCount += 1
                rpO.lastPatternSelected = _patternSelected

            if rpO.consecutivePatternChoiceCount == 0 and _iterCount > (rpO.patternBlockRows * rpO.patternBlockCols - _combo.minNumberOfPatternVariations):
                if _combo.dominantPatternProb > 0 and rpO.lastPatternSelected != _combo.dominantPatterns[0]:
                    _patternSelected = chooseAPattern(False, True)
                else:
                    _patternSelected = chooseAPattern()

                _tempPalette = getTempPalette(rpO)
                pieceLogger(" >> forcing a change in last few slots")

        if "randomizer" in _patternSelected:
            if rpO.numberOfRandomizersUsed >= _combo.maxNumberOfRandomizers:
                # pieceLogger(f"need to limit _patternSelected {_patternSelected} {_iterCount} {rpO.numberOfRandomizersUsed}")
                _patternSelected = chooseAPattern(True)
                _tempPalette = getTempPalette(rpO)
            else:
                rpO.numberOfRandomizersUsed += 1

        _position = _iterCount
        _pattern = _patternSelected

        _rotate = 0 if _patternSelected in (["shingles", "fishScales", "balls", "petals"]) else random.randint(0, 1)
        if not _combo.altBlockRotation:
            _rotate = 0

        if rpO.useBorderPattern and (c == 0 or r == 0 or c == (rpO.patternBlockCols - 1) or r == (rpO.patternBlockRows - 1)) and random.random() > _combo.borderLeakProb:
            _pattern = rpO.borderPattern
            _isBorder = True

        # else:
        #     pieceLogger(f"[generatePatternSequence][add_pattern_block] >> _pattern: {_pattern} _patternSelected: {_patternSelected}\n")

        _patternBlock = PatternBlock()
        _patternBlock.pattern = _pattern
        _patternBlock.position = _position
        _patternBlock.rotate = _rotate
        _patternBlock.tempPalette = _tempPalette
        _patternBlock.col = c
        _patternBlock.row = r
        _patternBlock.rePainting = _patternSelected in ["randomizer4", "randomizer3", "randomizer2", "randomizer", "diamond"]
        _patternBlock.isBorder = rpO.useBorderPattern and (c == 0 or r == 0 or c == (rpO.patternBlockCols - 1) or r == (rpO.patternBlockRows - 1))

        # if config.randomInsertionCount < _randomInsertionMax and not _patternBlock.isBorder:
        if rpO.randomInsertionCount < _randomInsertionMax:
            if random.random() < _randomInsertionProb:
                _patternBlock.pattern = _randomInserts[math.floor(random.uniform(0, len(_randomInserts)))]
                # pieceLogger(f"[generatePatternSequence][add_pattern_block]===== {rpO.randomInsertionCount} / {_randomInsertionMax} {_patternSelected} {_randomInsertionProb}")
                _randomInsertionProb = _combo.randomInsertionBaseProbabilitly
                rpO.randomInsertionCount += 1

        try:
            if rpO.settingUpPattern:
                rpO.patternSequence.append(_patternBlock)
            else:
                if len(rpO.slotsToChange) > 0:
                    if _iterCount in rpO.slotsToChange:
                        rpO.patternSequence[_iterCount] = _patternBlock
                        # pieceLogger(f"_iterCount {_iterCount} {_patternBlock.pattern}")
                elif random.random() < rpO.rebuildIndividualSlotProb:
                    _slot = round(random.uniform(0, len(rpO.patternSequence) - 1))
                    # shouldn't there be a list of slots to change that are somewhat
                    # consecuetive? otherwise just makes the whole thing more patchy?
                    # pieceLogger(f"add_pattern_block: change this slot {_slot}/ {len(rpO.patternSequence)}")
                    rpO.patternSequence[_slot] = _patternBlock
        except Exception as e:
            pieceLogger(f" error {e}", 1)

        # pieceLogger(f"[generatePatternSequence][add_pattern_block] >> _patternBlock.pattern: column:{c} row:{r} rpO.randomInsertionCount {rpO.randomInsertionCount}/{_randomInsertionMax} {_iterCount}: {_patternBlock.pattern}")
        _iterCount += 1

    if rpO.patternsInBands:
        for r in range(rpO.patternBlockRows):
            for c in range(rpO.patternBlockCols):
                add_pattern_block(c, r)
    else:
        for c in range(rpO.patternBlockCols):
            for r in range(rpO.patternBlockRows):
                add_pattern_block(c, r)


def getTempPalette(rpO):

    if random.SystemRandom().random() > rpO.changePaletteWhenChangingPatternProb:
        return getPaletteObjectByName(rpO.combinationSets[rpO.currentCombinationsetIndex].palettes[rpO.currentPaletteIndex])

    if random.SystemRandom().random() <= rpO.changeFullPaletteWhenChangingPatternProb:
        selectNewPalette(False)

    return changeSinglePalette(rpO.currentPaletteIndex)


def _print_pattern_sequence(config):
    print("----------------------------------------------")
    print(("New sequence"))
    print(f"config.totalSlots {config.totalSlots}")
    for s in config.patternSequence:
        print(f"{s[0]} {s[1]} {s[3].linecolOverlay.currentColor} {s[4]} ")
    print(f"Using start pattern {config.patternModel}")
    print("----------------------------------------------")


def rebuildPatterns(arg=0):
    pieceLogger(" >> called")

    if rpO.numRowsRandomize:
        rowsAndDotsSettings()

    # if random.random() < config.changePaletteWhenRebuildProb:
    #     pieceLogger("selectNewPalette called from: rebuildPatterns()")
    #     selectNewPalette()

    buildPatternSequence(rpO)
    disturbance.setupStableSections()
    disturbance.rebuildSections()
    resetCrossFader(False)


def resetCrossFader(_useConfigImage=True):
    # os.system('afplay /System/Library/Sounds/Sosumi.aiff')
    # print(f"DOING NOW  {config.faderDoingRefreshCount}")
    # os.system('say "NOW" &')
    # pieceLogger(f"resetCrossFader called : {_useConfigImage}")
    rpO.repeatDrawingMode = 1
    rpO.fader.fadingDone = False
    rpO.doTransition = True
    rpO.doSectionDisturbance = False
    if _useConfigImage:
        rpO.fader.startingImage = config.image.copy()
    else:
        # config.fader.startingImage = config.canvasImage.copy()
        rpO.fader.startingImage = config.compositeImage.copy()

    # _tempImg  =  Image.new("RGBA", (rpO.pictureWidth, rpO.pictureHeight))
    # _tempDraw = ImageDraw.Draw(_tempImg)
    # _tempDraw.rectangle((0,0,500,500), fill = (255,0,0,255))
    # config.canvasImage.paste(_tempImg, (0,0), _tempImg)

    # NOT WORKING

    # config.fader.endImage = config.canvasImage.copy()
    # config.fader.crossFadeImage = Image.new("RGBA", (rpO.pictureWidth, rpO.pictureHeight))

    # config.fader.totalBlocksToChange = config.faderDoingRefreshCount
    rpO.fader.initialized = True
    # config.debugPause = True


def rowsAndDotsSettings():

    rpO.numRows = round(random.uniform(1, 2))
    rpO.numShingleRows = round(random.uniform(1, 2))
    rpO.numScaleRows = round(random.uniform(1, 2))
    dotRows = [1, 2, 4]
    rpO.numDotRows = dotRows[round(random.uniform(0, 2))]
    rpO.waveScaleRings = round(random.uniform(rpO.ringsRange[0], rpO.ringsRange[1]))
    rpO.waveScaleSteps = round(random.uniform(rpO.stepsRange[0], rpO.stepsRange[1]))


# --------------------- LOOP ACTIONS  ---------------------


def iterate():
    """Performs a single iteration of the animation."""
    global config
    global rpO

    if config.debugPause:
        config.directorController.slotRate = 2.0

    rpO.comboSetDirector.checkTime()
    if rpO.comboSetDirector.advance:
        handleChangeCurrentCominationSet()

    updateBackgroundColor()
    # handleClipPlayer()
    drawAndProcessPattern()
    disturbance.handleDisturbances()
    overlayControls.handleOverlayActions()
    handleFadingAndRebuild()
    disturbance.handleSectionDisturbances()
    disturbance.handleShingleVariation()
    drawBackgroundAndPasteImage()
    renderComposite()

    if rpO.saveImages:
        saveImageIfDone()


def drawRepeatedPatternImage(config, canvasImage):
    """Draws the repeated pattern image onto the canvas."""
    _counter = 0
    extraOverlapx = 0
    extraOverlapy = 0
    # for i in range(len(config.patternSequence)):
    for i in range(rpO.totalSlots):
        _patternBlock = rpO.patternSequence[i]
        # This sets the block image for each unit
        drawBlockWithPattern(i)

        if _patternBlock.hasBeenPainted == False:
            drawIndividualBlock(rpO, canvasImage, _patternBlock.col, _patternBlock.row, i, extraOverlapx, extraOverlapy)
            if not _patternBlock.rePainting or _patternBlock.isBorder:
                _patternBlock.hasBeenPainted = True

    # rpO.patternImage = canvasImage.copy()
    rpO.fader.endImage = config.patternImage.copy()
    # rpO.fader.endImage = rpO.canvasImage.copy()


def drawIndividualBlock(rpO, canvasImage, c, r, _counter, extraOverlapx, extraOverlapy):
    """Draws a single block of the pattern."""

    _temp = rpO.blockImage.copy()
    # _temp = Image.new("RGBA",(rpO.blockWidth, rpO.blockHeight))
    # _tempDraw = ImageDraw.Draw(_temp)
    # _temp.paste(rpO.blockImage, (0,0), rpO.blockImage)
    # _tempDraw.rectangle((0,0,10,10), fill =(random.randint(0,255),random.randint(0,255),random.randint(0,255),255))
    # _temp = _temp.crop((0,0,20,20))
    # disabling for a moment 2023-04-01

    if rpO.patternModel not in ["ropePattern", "littleCones"]:
        _temp = _temp.rotate(90)
    # if rpO.patternModel == "circlesPacked":
    #     extraOverlapx = round(rpO.blockWidth / 8)
    #     extraOverlapy = round(rpO.blockWidth / 8)

    if rpO.patternModel in ["waveScales", "shellScales"]:
        _temp = _temp.rotate(-180)

    if c % 2 != 0 and rpO.rotateAltBlock == 1:
        _temp = _temp.rotate(-90)

    # forces the patterns to align to a certain rotation
    # useful instead of rotation the whole piece etc
    if rpO.patternOrientation != 0:
        _temp = _temp.rotate(rpO.patternOrientation)

    if rpO.blockRotation != 0:
        _temp = _temp.rotate(rpO.blockRotation)

    # _tempDraw = ImageDraw.Draw(canvasImage)
    # _tempDrawB = ImageDraw.Draw(_temp)

    _xPos = c * rpO.blockWidth - c * extraOverlapx
    _yPos = r * rpO.blockHeight - r * extraOverlapy

    canvasImage.paste(_temp, (_xPos, _yPos), _temp)
    config.canvasImage.paste(_temp, (_xPos, _yPos), _temp)


def drawBlockWithPattern(_counter):
    """Applies pattern variations based on the pattern sequence."""
    _patternBlock = rpO.patternSequence[_counter]
    rpO.patternModel = _patternBlock.pattern
    rpO.rotateAltBlock = _patternBlock.rotate
    if not _patternBlock.hasBeenPainted:
        func = eval(f"pattern_blocks_v5.{_patternBlock.pattern}")
        func(rpO, _patternBlock.tempPalette)

    # if not _patternBlock.rePainting:
    #     _patternBlock.hasBeenPainted = True


def updateBackgroundColor():
    """Updates the background color based on current palette."""
    rpO.bgColor = tuple(round(a * config.brightness) for a in rpO.c1.currentColor)


def drawAndProcessPattern():
    """Draws and processes the repeated pattern image."""
    drawRepeatedPatternImage(config, config.patternImage)

    # if config.repeatDrawingMode == 1:
    #     redrawAndLoadImage(config)

    if random.random() < 0.005 and rpO.usePixelSortRandomize:
        config.usePixelSort = not config.usePixelSort  # Toggle pixel sort


def redrawAndLoadImage(config):
    """Redraws the pattern and optionally loads a new image."""

    if random.random() < config.loadAnImageProb:
        loadImageForBase()
    else:
        drawRepeatedPatternImage(config, config.canvasImage)

    config.repeatDrawingMode = 0


# ----------------------------------


def handleFadingAndRebuild():
    """Handles image fading and pattern rebuilding."""
    if rpO.fader.fadingDone:
        # config.fader.fadingDone = False
        # config.fader.startingImage = config.canvasImage

        rpO.fader.totalBlocksToChange = 0
        if rpO.doneCount >= rpO.numberOfSections and rpO.rebuildImmediatelyAfterDone:
            rpO.doSectionDisturbance = False
            pieceLogger("rebuildPatterns called after fading done")
            rebuildPatterns()

    if random.random() < rpO.resetOverlayProbability and rpO.usePolygonOverlay:
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
    disturbancesDone = not rpO.doSectionDisturbance or rpO.doneCount >= rpO.numberOfSections
    if rpO.fader.fadingDone and disturbancesDone:
        # rpO.doSectionDisturbance = False
        # print("\nrebuildPatterns called after fading done 2")

        # selectNewPalette(False)
        if random.random() < rpO.rebuildAllSlotsProb:
            pieceLogger(f"\n >> Rebuiding full : {rpO.combinationSets[rpO.currentCombinationsetIndex].name}")
            rpO.settingUpPattern = True
            rpO.patternSequence = []
            # selectNewPalette(True)
            # selectNewPalette()
        else:
            pieceLogger(f"\n >> Rebuiding parts: {rpO.combinationSets[rpO.currentCombinationsetIndex].name}")
            if random.random() < rpO.chanceRebuildPatternChoosesRandom:
                rpO.slotsToChange = []
            else:
                rpO.slotsToChange = []
                _skip = True
                _chanceNotToSkip = rpO.rebuildSlotSkipRate
                _chanceToSkip = rpO.rebuildSlotStartSkipRate
                for i in range(len(rpO.patternSequence)):
                    if random.random() < _chanceToSkip:
                        _skip = False
                    if random.random() < _chanceNotToSkip:
                        _skip = True
                    if not _skip:
                        rpO.slotsToChange.append(i)
                # pieceLogger(f"handlePatternRebuild:  {rpO.slotsToChange}")

            rpO.settingUpPattern = False
        try:
            pieceLogger(f" >> rpO.settingUpPattern {rpO.settingUpPattern} | color palette : {rpO.palettes[rpO.currentPaletteIndex]}")
        except Exception as e:
            pieceLogger(e)
        # pieceLogger(f"handlePatternRebuild(): rpO.slotsToChange {rpO.slotsToChange}")
        rebuildPatterns()


def drawBackgroundAndPasteImage():
    """Draws the background and pastes the main image."""
    if rpO.doTransition:

        for _ in range(rpO.faderDoingRefreshCountIterations):
            rpO.fader.fadeIn(config)
            for _patch, _px, _py in rpO.fader.crossFadePatches:
                config.compositeImage.paste(_patch, (_px, _py), _patch)

    elif rpO.sectionDisturbance:
        if rpO.doSectionDisturbance:
            config.compositeImage.paste(config.canvasImage, (0, 0), config.canvasImage)
        else:
            config.compositeImage.paste(config.patternImage, (0, 0), config.patternImage)

    """Transforms and renders the final image."""
    if rpO.transformShape:
        config.compositeImage = transformImage(config.compositeImage)

    if rpO.canvasRotation != 0:
        config.compositeImage = config.compositeImage.rotate(rpO.canvasRotation, 3, True)
        config.compositeImage = ImageEnhance.Contrast(config.compositeImage).enhance(1.20)


def renderComposite():
    """FINAL RENDERING CALL"""
    if config.useDrawingPoints == True:
        config.panelDrawing.canvasToUse = config.compositeImage
        config.panelDrawing.render()
    else:
        # if rpO.usePolygonOverlay:
        #     config.compositeImage = shapeOverLayFunction(config.compositeImage)

        # config.compositeImageDraw = ImageDraw.Draw(config.compositeImage)
        # config.destinationImageDraw = ImageDraw.Draw(config.destinationImage)
        # config.compositeImageDraw.rectangle((60,70,128,120), fill = (255,0,0,50))
        # config.patternImageDraw.rectangle((60, 70, 128, 120), fill=(255, 0, 0, 50))

        # config.destinationImage.paste(config.compositeImage, (0, 0), config.compositeImage)

        _xp = int(rpO.imageXPOS)
        _frac = rpO.imageXPOS - _xp
        _yp = int(rpO.imageYPOS)

        if getattr(rpO, "useSubPixelSmoothing", False):
            _BG = rpO.bgColor
            _w, _h = config.scrollBlendFrame0.width, config.scrollBlendFrame0.height
            config.scrollBlendFrame0.paste(_BG, (0, 0, _w, _h))
            config.scrollBlendFrame0.paste(config.compositeImage, (_xp, _yp), config.compositeImage)
            config.scrollBlendFrame0.paste(config.compositeImage, (_xp - rpO.pictureWidth, _yp), config.compositeImage)
            if _frac > 0.05:
                config.scrollBlendFrame1.paste(_BG, (0, 0, _w, _h))
                config.scrollBlendFrame1.paste(config.compositeImage, (_xp + 1, _yp), config.compositeImage)
                config.scrollBlendFrame1.paste(config.compositeImage, (_xp + 1 - rpO.pictureWidth, _yp), config.compositeImage)
                config.destinationImage.paste(Image.blend(config.scrollBlendFrame0, config.scrollBlendFrame1, _frac), (0, 0))
            else:
                config.destinationImage.paste(config.scrollBlendFrame0, (0, 0))
        else:
            config.destinationImage.paste(config.compositeImage, (_xp, _yp), config.compositeImage)
            config.destinationImage.paste(config.compositeImage, (_xp - rpO.pictureWidth, _yp), config.compositeImage)

        rpO.imageXPOS += rpO.XPOSSpeed
        # rpO.imageYPOS += rpO.YPOSSpeed

        if rpO.imageXPOS >= rpO.pictureWidth:
            rpO.imageXPOS = 0

        if rpO.imageYPOS >= rpO.pictureHeight:
            rpO.imageYPOS = 0

        # showDebugCanvases(rpO)
        # # uncomment for all temp canvas layers to show
        if rpO.setupDeBug:
            showDebugCanvases(rpO)

        # this used to occur on the composite layer but was getting jumps when
        # new blocks were added so compromising with wave distortions applied to final
        # image  - smoother and slower
        if rpO.useWaveDistortion:
            config.destinationImage = ImageOps.deform(config.destinationImage, disturbance.WaveDeformer())
            rpO.waveDeformXPos += rpO.waveDeformXPosRate
            if rpO.waveDeformXPos > config.screenWidth:
                rpO.waveDeformXPos = 0

        # Run every cycle:
        global overlayControls
        if overlayControls.usingPanelOverlays:
            overlayControls.targetImageRef = config.destinationImage
            
        if overlayControls.useBlanks:
            config.destinationImageDraw = ImageDraw.Draw(config.destinationImage)
            overlayControls.destinationImageDraw = config.destinationImageDraw

        overlayControls.handleOverlayActions()

        # Special polygon overlay for certain types of framing
        if rpO.usePolygonOverlay:
            config.destinationImage = shapeOverLayFunction(config.destinationImage)

        config.render(config.destinationImage, 0, 0)


def showDebugCanvases(config):
    _w = rpO.pictureWidth
    _h = rpO.pictureHeight

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
    _rpO : RepeatedPatterns = rpO
    temp2 = Image.new("RGBA", (rpO.pictureWidth, rpO.pictureHeight))
    temp2Draw = ImageDraw.Draw(temp2)

    if not _rpO.useOverlayTileGrid:
        _rpO.polyOverlay.stepTransition()
        polyFillaList = [int(a) for a in (_rpO.polyOverlay.currentColor)]
        polyFilla = (polyFillaList[0], polyFillaList[1], polyFillaList[2], _rpO.poly_alpha)
        # actual shape
        if random.random() < _rpO.polyOverlayChangeProb:
            _rpO.polyBase[0][0] += random.uniform(-3, 3)
            _rpO.polyBase[1][0] += random.uniform(-3, 3)
            _rpO.polyBase[2][0] += random.uniform(-3, 3)
            _rpO.polyBase[3][0] += random.uniform(-3, 3)
            _rpO.polyBase[4][0] += random.uniform(-3, 3)
        poly = tuple(map(lambda x: (tuple(x)), _rpO.polyBase))

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
        _overlayFill = tuple(round(a * config.brightness) for a in _rpO.c3.currentColor)
        for _r in range(_rpO.rows):
            for _c in range(_rpO.cols):
                _x0 = _c * _rpO.tileSizeWidth
                _y0 = _r * _rpO.tileSizeHeight
                _x1 = _x0 + _rpO.tileSizeWidth
                _y1 = _y0 + _rpO.tileSizeHeight
                if _count in _rpO.tileOverlayGrid:
                    temp2Draw.rectangle((_x0, _y0, _x1, _y1), fill=_overlayFill)
                # else :
                #     temp2Draw.rectangle((_x0,_y0,_x1,_y1), fill=(200,0,0,0))
                _count += 1

        # removing python 3.10 specific match for the moment ..
        # match config.polyOverlayMode:
        #     case "overaly":
        #         temp1 = ImageChops.overlay(temp1, temp2)
        #     case "subtract_modulo":
        #         temp1 = ImageChops.subtract_modulo(temp1, temp2)
        #     case "soft_light":
        #         temp1 = ImageChops.soft_light(temp1, temp2)
        #     case "lighter":
        #         temp1 = ImageChops.lighter(temp1, temp2)

        if _rpO.polyOverlayMode == "overaly":
            temp1 = ImageChops.overlay(temp1, temp2)
        if _rpO.polyOverlayMode == "subtract_modulo":
            temp1 = ImageChops.subtract_modulo(temp1, temp2)
        if _rpO.polyOverlayMode == "soft_light":
            temp1 = ImageChops.soft_light(temp1, temp2)
        if _rpO.polyOverlayMode == "lighter":
            temp1 = ImageChops.lighter(temp1, temp2)

        if random.random() < _rpO.polyOverlayChangeProb:
            generateOverlayTiles()
        # temp1.paste(temp2, (0, 0), temp2)
    return temp1


def loadPolyOverlaybaseValues():
    try:
        _polyBaseVals = workConfig.get("movingpattern", "polyBaseVals").split("|")
        # print(_polyBaseVals)
        rpO.polyBase = []
        for _a in _polyBaseVals:
            _ps = list(map(lambda x: int(x), _a.split(",")))
            rpO.polyBase.append(_ps)
    except Exception as e:
        pieceLogger(e)
        rpO.polyBase = []


def generateOverlayTiles():
    rpO.tileOverlayGrid = [0]
    for _v in range(config.rows * config.cols):
        if random.random() < rpO.tileOverlayGridProb:
            rpO.tileOverlayGrid.append(_v)


def setupPolyOverlay(): 
    rpO.usePolygonOverlay = False
    try:
        rpO.polyOverlay = ColorOverlay()
        rpO.polyOverlay.randomSteps = True
        rpO.polyOverlay.timeTrigger = True
        rpO.polyOverlay.tLimitBase = int(workConfig.get("movingpattern", "poly_tLimitBase"))
        rpO.polyOverlay.tLimit = int(workConfig.get("movingpattern", "poly_tLimit"))
        rpO.polyOverlay.steps = int(workConfig.get("movingpattern", "poly_steps"))
        rpO.usePolygonOverlay = workConfig.getboolean("movingpattern", "usePolygonOverlay")
        rpO.polyOverlay.minHue = int(workConfig.get("movingpattern", "poly_minHue"))
        rpO.polyOverlay.maxHue = int(workConfig.get("movingpattern", "poly_maxHue"))
        rpO.polyOverlay.minSaturation = float(workConfig.get("movingpattern", "poly_minSaturation"))
        rpO.polyOverlay.maxSaturation = float(workConfig.get("movingpattern", "poly_maxSaturation"))
        rpO.polyOverlay.minValue = float(workConfig.get("movingpattern", "poly_minValue"))
        rpO.polyOverlay.maxValue = float(workConfig.get("movingpattern", "poly_maxValue"))
        rpO.tileOverlayGridProb = float(workConfig.get("movingpattern", "tileOverlayGridProb", fallback=0.0))
        rpO.poly_alpha = int(workConfig.get("movingpattern", "poly_alpha"))
        rpO.useOverlayTileGrid = workConfig.getboolean("movingpattern", "useOverlayTileGrid", fallback=False)
        rpO.polyOverlayMode = workConfig.get("movingpattern", "polyOverlayMode", fallback="soft_light")
        rpO.polyOverlay.setStartColor()
        rpO.polyOverlay.getNewColor()
        rpO.polyOverlay.colorTransitionSetup()
        rpO.polyOverlayChangeProb = float(workConfig.get("movingpattern", "polyOverlayChangeProb", fallback=0.003))

        generateOverlayTiles()
        loadPolyOverlaybaseValues()
        # print(config.polyBase)

    except Exception as e:
        pieceLogger(f" >> Not using custom polygon overlay {e}")
        rpO.usePolygonOverlay = False


# ----------------- INITIAL ACTIONS  ---------------------


def loadAndInitializeCrossFader():

    pieceLogger(" >> Initialize cross fader")
    loadConfigValue(rpO, workConfig, "movingpattern", "fadeThroughIncrement", 0.1, float)
    loadConfigValue(rpO, workConfig, "movingpattern", "faderProbDissolve", 0.5, float)
    loadConfigValue(rpO, workConfig, "movingpattern", "faderLargeBlockXSections", 10, int)
    loadConfigValue(rpO, workConfig, "movingpattern", "faderLargeBlockYSections", 3, int)
    loadConfigValue(rpO, workConfig, "movingpattern", "faderSmallBlockXSections", 40, int)
    loadConfigValue(rpO, workConfig, "movingpattern", "faderSmallBlockYSections", 40, int)
    loadConfigValue(rpO, workConfig, "movingpattern", "sectionDeltaWidth", 0, int)
    loadConfigValue(rpO, workConfig, "movingpattern", "sectionDeltaHeight", 0, int)
    loadConfigValue(rpO, workConfig, "movingpattern", "faderParallelBlocks", 1, int)
    loadConfigValue(rpO, workConfig, "movingpattern", "faderFadeDoingRefreshCountIterations", 20, int)
    loadConfigValue(rpO, workConfig, "movingpattern", "faderDissolveDoingRefreshCountIterations", 100, int)
    loadConfigValue(rpO, workConfig, "movingpattern", "faderDoingRefreshCountIterationsStartup", 500, int)

    rpO.doTransition = True
    rpO.doneCount = 0
    rpO.faderInit = True
    rpO.faderDoingRefreshCountIterations = rpO.faderDoingRefreshCountIterationsStartup
    rpO.fader = Fader()
    rpO.fader.height = rpO.pictureHeight
    rpO.fader.width = rpO.pictureWidth
    rpO.fader.startingImage = Image.new("RGBA", (rpO.pictureWidth, rpO.pictureHeight))
    rpO.fader.endImage = config.canvasImage
    rpO.fader.destinationImage = config.image
    rpO.fader.setUp(rpO)


def createImageHolders():
    # CREATE THE IMAGE HOLDERS
    # canvasImage will get the drawing
    # disturbanceImage will get the disturbance / glitching
    # image will be the final output

    config.image = Image.new("RGBA", (rpO.pictureWidth, rpO.pictureHeight))

    config.patternImage = Image.new("RGBA", (rpO.pictureWidth, rpO.pictureHeight))
    config.patternImageDraw = ImageDraw.Draw(config.patternImage)

    config.canvasImage = Image.new("RGBA", (rpO.pictureWidth, rpO.pictureHeight))
    config.canvasImageDraw = ImageDraw.Draw(config.canvasImage)

    config.nextStateImage = Image.new("RGBA", (rpO.pictureWidth, rpO.pictureHeight))
    config.nextStateImageDraw = ImageDraw.Draw(config.nextStateImage)

    config.destinationImage = Image.new("RGBA", (config.screenWidth, config.screenHeight))
    config.destinationImageDraw = ImageDraw.Draw(config.destinationImage)

    config.compositeImage = Image.new("RGBA", (rpO.pictureWidth, rpO.pictureHeight))

    # For scrolling the entire piece
    config.scrollBlendFrame0 = Image.new("RGBA", (config.screenWidth, config.screenHeight), (0, 0, 0, 255))
    config.scrollBlendFrame1 = Image.new("RGBA", (config.screenWidth, config.screenHeight), (0, 0, 0, 255))

    config.blendSteps = 5
    config.blendStep = 0

    rpO.canvasImage = config.canvasImage
    rpO.patternImage = config.patternImage
    rpO.nextStateImage = config.nextStateImage
    rpO.destinationImage = config.destinationImage
    rpO.compositeImage = config.compositeImage


def main(run=True):
    global config
    global rpO
    rpO = RepeatedPatterns()
    pieceLogger("\n[main] >> called")

    config.debugPause = False

    rpO.path = config.path
    rpO.brightness =  config.brightness
    rpO.config = config
    # for the overlay function when doing
    # strict panels
    rpO.rows = config.rows
    rpO.cols = config.cols
    rpO.tileSizeWidth = config.tileSizeWidth
    rpO.tileSizeHeight = config.tileSizeHeight

    loadConfigValue(rpO, workConfig, "movingpattern", "setupDeBug", False, bool)

    loadConfigValue(rpO, workConfig, "movingpattern", "blockWidthMin", 32, int)
    loadConfigValue(rpO, workConfig, "movingpattern", "blockWidthMax", 32, int)

    loadConfigValue(rpO, workConfig, "movingpattern", "yOffset", 1, int)
    loadConfigValue(rpO, workConfig, "movingpattern", "yOffset2", 1, int)

    loadConfigValue(rpO, workConfig, "movingpattern", "blockRotation", 0.00, float)
    loadConfigValue(rpO, workConfig, "movingpattern", "canvasRotation", 0.00, float)
    loadConfigValue(rpO, workConfig, "movingpattern", "imgcanvasOffsetX", 0, int)
    loadConfigValue(rpO, workConfig, "movingpattern", "imgcanvasOffsetY", 0, int)

    loadConfigValue(rpO, workConfig, "movingpattern", "pictureWidth", config.canvasWidth, int)
    loadConfigValue(rpO, workConfig, "movingpattern", "pictureHeight", config.canvasHeight, int)

    rpO.repeatProb = 0.99

    # if/when saving images
    config.drawingPrinted = True
    loadConfigValue(rpO, workConfig, "movingpattern", "saveImages", False, bool)
    loadConfigValue(rpO, workConfig, "movingpattern", "outPutPath", "", str)
    loadConfigValue(rpO, workConfig, "movingpattern", "drawBGColorEachCycle", True, bool)

    rpO.repeatDrawingMode = 1
    loadConfigValue(rpO, workConfig, "movingpattern", "loadAnImageProb", 0.0, float)
    rpO.imageSources = workConfig.get("movingpattern", "imageSources").split(",")

    # ---------------------------------------------------------------###
    createImageHolders()
    # ---------------------------------------------------------------###

    loadConfigValue(rpO, workConfig, "movingpattern", "useBlurSection", False, bool)
    loadConfigValue(rpO, workConfig, "movingpattern", "blurSectionWidth", 0, int)
    loadConfigValue(rpO, workConfig, "movingpattern", "blurSectionHeight", 0, int)
    loadConfigValue(rpO, workConfig, "movingpattern", "blurSectionXPos", 0, int)
    loadConfigValue(rpO, workConfig, "movingpattern", "blurSectionYPos", 0, int)
    loadConfigValue(rpO, workConfig, "movingpattern", "mask_blur_amt", 0, int)
    loadConfigValue(rpO, workConfig, "movingpattern", "cp_blur_amt", 0, int)

    rpO.mask = Image.new("L", config.canvasImage.size, 0)
    rpO.mask_draw = ImageDraw.Draw(rpO.mask)

    rpO.mask_draw.ellipse(
        (
            rpO.blurSectionXPos,
            rpO.blurSectionYPos,
            rpO.blurSectionXPos + rpO.blurSectionWidth,
            rpO.blurSectionYPos + rpO.blurSectionHeight,
        ),
        fill=255,
    )
    rpO.mask_blur_amt = rpO.mask_blur_amt
    rpO.cp_blur_amt = rpO.cp_blur_amt

    # ---------------------------------------------------------------###

    # loadConfigValue(rpO, workConfig, "movingpattern", "filterRemapping", False, bool)
    # loadConfigValue(rpO, workConfig, "movingpattern", "filterRemappingProb", 0.0, float)
    # loadConfigValue(rpO, workConfig, "movingpattern", "filterRemapMinHoriSize", 1, int)
    # loadConfigValue(rpO, workConfig, "movingpattern", "filterRemapMaxHoriSize", 1, int)
    # loadConfigValue(rpO, workConfig, "movingpattern", "filterRemapMinVertSize", 1, int)
    # loadConfigValue(rpO, workConfig, "movingpattern", "filterRemapMaxVertSize", 1, int)
    # loadConfigValue(rpO, workConfig, "movingpattern", "filterRemapRangeY", 1, int)
    # loadConfigValue(rpO, workConfig, "movingpattern", "filterRemapRangeX", 1, int)

    # ---------------------------------------------------------------###

    loadConfigValue(rpO, workConfig, "movingpattern", "resetOverlayProbability", 0.000, float)

    # --------------------- clip player instert ---------------------#########
    loadClipPlayerConfigs()

    loadAndInitializeCrossFader()

    setupPolyOverlay()

    loadAndSetupPatterns()

    loadAndSetupAllPalettes()

    disturbance.init(rpO, workConfig)
    disturbance.setupDisturbances()

    buildPatternSequence(rpO)

    config.applyDitherBeforeRemapping = True

    # ---------------------------------------------------------------######

    config.directorController = Director(config)
    config.redrawSpeed = float(workConfig.get("movingpattern", "redrawSpeed"))

    rpO.imageXPOS = 0
    rpO.imageYPOS = 0
    rpO.XPOSSpeed = float(workConfig.get("movingpattern", "XPOSSpeed", fallback="0.0"))
    rpO.YPOSSpeed = float(workConfig.get("movingpattern", "YPOSSpeed", fallback="0.0"))
    loadConfigValue(rpO, workConfig, "movingpattern", "useSubPixelSmoothing", False, bool)

    try:
        config.directorController.slotRate = float(workConfig.get("movingpattern", "slotRate"))
    except Exception as e:
        pieceLogger(f"{e} <== adjust config to use slotRate!! <===")
        config.directorController.slotRate = 0.03

    # initiate
    global overlayControls
    overlayControls = BlanksAndDitherRemapping(config, workConfig, "movingpattern")

    # For blanks
    overlayControls.altColor = (0, 0, 0, 15)
    overlayControls.targetImageRef = config.destinationImage
    overlayControls.destinationImageDraw = config.destinationImageDraw

    # for overlay blocks
    overlayControls.overlayImage = config.destinationImage
    overlayControls.overlayImageDraw = config.destinationImageDraw
    overlayControls.setPanelOverlays()

    # for filter remapping


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
    #         #config.render(config.canvasImage, 0, 0, rpO.pictureWidth, rpO.pictureHeight)
    #         #config.render(config.image, 0, 0)
    #         config.render(config.renderImageFull, 0, 0)
    # """

    if rpO.setupDeBug:
        # prints out everything in the config global
        config.debugSelf()

    if run:
        runWork()


def runWork():
    pieceLogger(" >> Running repeatblocks.py", 2)
    _subSteps = getattr(config, "smoothingSteps", 0)

    while config.isRunning:
        config.directorController.checkTime()
        if config.directorController.advance:
            iterate()
        else:
            renderComposite()
        for _ in range(_subSteps):
            renderComposite()
        time.sleep(config.redrawSpeed)
        if not config.standAlone:
            config.callBack()


def _pieceLogger(arg1, arg2=None, arg3=None):
    return True
