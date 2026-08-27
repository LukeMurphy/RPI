import math
import random
import time
import configparser
import re
from tkinter import NO

from matplotlib.pyplot import pie
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

# from scipy.spatial import Voronoi
from scipy.interpolate import splprep, splev
from modules.holder_director import Director
from modules.configuration import ArtWorkConfig, pieceLogger
from modules import colorutils
from modules.rendering.render import saveImageToFile
from modules.blanks_and_dither_rempping import BlanksAndDitherRemapping

"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
"""""" """""" """ This version uses bundles of marks and textures             """
"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


# ----------------------------------------------------#
class MarksManager:
    ''' Holds all the defaults and variables distinct from the main config'''
    def __init__(self, config):
        self.config = config
        self.activePalette = None

    def setUp(self, workConfig):
        '''Loads the piece settings and all the palettes'''
        # ---- bundle path ----
        self.drawingBundle = workConfig.get("drawingField", "drawingBundle")
        self.assetPath = self.config.path
        if self.assetPath[-1] != "/":
            self.assetPath = f"{self.config.path}/"
        self.assetPath = f"{self.assetPath}configs/{self.drawingBundle}"
        if self.assetPath[-1] != "/":
            self.assetPath = f"{self.assetPath}/"

        # ---- texture models ----
        self.useTextureLayer = True
        self.textureSetNames = workConfig.get("drawingField", "textureSets", fallback="texture1").split(",")
        self.textureSets = []
        for _t in self.textureSetNames:
            _tex = _load_texture_values(_t)
            self.textureSets.append(_tex)

        # ---- image layers ----
        self.pictureWidth = int(workConfig.get("drawingField", "pictureWidth", fallback=self.config.canvasWidth))
        self.pictureHeight = int(workConfig.get("drawingField", "pictureHeight", fallback=self.config.canvasHeight))
        createImageLayers()

        # ---- drawing / color configs ----
        self.usebgBox = workConfig.getboolean("drawingField", "forcebgBox")
        self.bgTileSizeWidthMin = float(workConfig.get("drawingField", "bgTileSizeWidthMin"))
        self.bgTileSizeWidthMax = float(workConfig.get("drawingField", "bgTileSizeWidthMax"))
        self.bgTileSizeHeightMin = float(workConfig.get("drawingField", "bgTileSizeHeightMin"))
        self.bgTileSizeHeightMax = float(workConfig.get("drawingField", "bgTileSizeHeightMax"))
        # self.bgBoxFill = tuple(	map(lambda x: int(x), workConfig.get("drawingField", "bgBoxFill").split(",")))

        self.clearbgBoxProb = float(workConfig.get("drawingField", "clearbgBoxProb"))

        # jitter and roughing
        self.doJitterProb = float(workConfig.get("drawingField", "doJitterProb", fallback=0.0))
        self.doJitterAfterLineUseProb = float(workConfig.get("drawingField", "doJitterAfterLineUseProb", fallback=1.0))
        self.doProgressiveJitterProb = float(workConfig.get("drawingField", "doProgressiveJitterProb", fallback=0.50))
        self.doJitterWhenAddingBGUseProb = float(workConfig.get("drawingField", "doJitterWhenAddingBGUseProb", fallback=1.0))
        self.doJitterEventPerCyleProb = float(workConfig.get("drawingField", "doJitterEventPerCyleProb", fallback=1.0))
        self.jitterIterationsMaxAfterDraw = workConfig.getint("drawingField", "jitterIterationsMax", fallback=10)
        self.jitterIterationsMin = workConfig.getint("drawingField", "jitterIterationsMin", fallback=1)
        self.jitterIterationsMax = workConfig.getint("drawingField", "jitterIterationsMax", fallback=10)
        self.jitterDisplacementHorizontal = float(workConfig.get("drawingField", "jitterDisplacementHorizontal", fallback=1))
        self.jitterDisplacementVertical = float(workConfig.get("drawingField", "jitterDisplacementVertical", fallback=1))
        self.jitterIterationsMin_roughing = workConfig.getint("drawingField", "jitterIterationsMin_roughing", fallback=1)
        self.jitterIterationsMax_roughing = workConfig.getint("drawingField", "jitterIterationsMax_roughing", fallback=10)
        self.jitterDisplacementHorizontal_roughing = float(workConfig.get("drawingField", "jitterDisplacementHorizontal_roughing", fallback=2))
        self.jitterDisplacementVertical_roughing = float(workConfig.get("drawingField", "jitterDisplacementVertical_roughing", fallback=2))
        self.jitterIterations = 0

        self.penAlpha = int(workConfig.get("drawingField", "penAlpha", fallback=200))
        self.bgColorAlpha = int(workConfig.get("drawingField", "bgColorAlpha", fallback=2))

        self.noPenGrays = 0.0
        self.nobgGrays = 0.0
        self.linesDrawnCountMinBase = workConfig.getint("drawingField", "linesDrawnCountMinBase", fallback=1)

        self.drawLineAsEnvelope = workConfig.getboolean("drawingField", "drawLineAsEnvelope", fallback=False)

        self.paletteSets = []
        paletteSets = workConfig.get("drawingField", "paletteSets").split(",")

        self.loadPalettesFromCfgFiles = workConfig.getboolean("drawingField", "loadPalettesFromCfgFiles", fallback=False)

        for _pRaw in paletteSets:
            palette = Palette()
            _paletteCFGParser = workConfig
            _p = _pRaw.replace("\n", "")


            if self.loadPalettesFromCfgFiles :
                _paletteCFGParser = configparser.ConfigParser()
                _cfgFile = f"{self.assetPath}palettes/{_p}.cfg"
                pieceLogger(_cfgFile)
                _paletteCFGParser.read(_cfgFile)


            palette.bgBoxAlphaRange = tuple(
                map(
                    lambda x: int(x),
                    _paletteCFGParser.get(_p, "bgBoxAlphaRange").split(","),
                )
            )

            _bgColorSetsRaw = _paletteCFGParser.get(_p, "bgColorSets")
            _bgColorSetsRaw = re.sub(r"[\(\)]", "", _bgColorSetsRaw)
            _bgColorSetsRaw = _bgColorSetsRaw.split("|")
            palette.bgColorSets = []
            palette.bgColorSets.extend(tuple(map(lambda x: float(x), _set.split(","))) for _set in _bgColorSetsRaw)

            _penColorSetsRaw = _paletteCFGParser.get(_p, "penColorSets")
            _penColorSetsRaw = re.sub(r"[\(\)]", "", _penColorSetsRaw)
            _penColorSetsRaw = _penColorSetsRaw.split("|")
            palette.penColorSets = []
            palette.penColorSets.extend(tuple(map(lambda x: float(x), _set.split(","))) for _set in _penColorSetsRaw)

            _bgBoxColorSetsRaw = _paletteCFGParser.get(_p, "bgBoxColorSets")
            _bgBoxColorSetsRaw = re.sub(r"[\(\)]", "", _bgBoxColorSetsRaw)
            _bgBoxColorSetsRaw = _bgBoxColorSetsRaw.split("|")
            palette.bgBoxColorSets = []
            palette.bgBoxColorSets.extend(tuple(map(lambda x: float(x), _set.split(","))) for _set in _bgBoxColorSetsRaw)

            palette.bgBoxRange = list(
                map(
                    lambda x: int(x),
                    _paletteCFGParser.get(_p, "bgBoxRange", fallback=f"0,0,0,0").split(","),
                )
            )

            if palette.bgBoxRange == [0, 0, 0, 0]:
                palette.bgBoxRange = [0, self.pictureWidth, 0, self.pictureHeight]

            palette.noPenGrays = float(_paletteCFGParser.get(_p, "noPenGrays", fallback=0))

            palette.pens = _paletteCFGParser.get(_p, "penNames").split(",")
            palette.name = _p
            palette.textureName = _paletteCFGParser.get(_p, "texture")

            palette.usebgBoxProb = float(_paletteCFGParser.get(_p, "usebgBoxProb", fallback=".01"))
            palette.blendLevelRateBase = float(_paletteCFGParser.get(_p, "blendLevelRateBase", fallback=".01"))
            palette.clearCurrentDrawingProb = float(_paletteCFGParser.get(_p, "clearCurrentDrawingProb", fallback=".0001"))

            # when set to 1.0 and startNewLineDelayRange is set
            # then the new line starts as soon as the random delay
            # ends - since drawing is a major event and changes the
            # attention of the viewer, controlling when it happens
            # is probably better left to timing than just cycle-based
            # probability
            palette.startNewLineProb = float(_paletteCFGParser.get(_p, "startNewLineProb", fallback=".01"))
            palette.startNewLineDelayRange = list(map(lambda x: float(x), _paletteCFGParser.get(_p, "startNewLineDelayRange", fallback="1,10").split(",")))

            # jitter and roughing palette overrides
            palette.doJitterProb = float(_paletteCFGParser.get(_p, "doJitterProb", fallback=self.doJitterProb))
            palette.doJitterAfterLineUseProb = float(_paletteCFGParser.get(_p, "doJitterAfterLineUseProb", fallback=self.doJitterAfterLineUseProb))
            palette.doJitterWhenAddingBGUseProb = float(_paletteCFGParser.get(_p, "doJitterWhenAddingBGUseProb", fallback=self.doJitterWhenAddingBGUseProb))
            palette.doJitterEventPerCyleProb = float(_paletteCFGParser.get(_p, "doJitterEventPerCyleProb", fallback=self.doJitterEventPerCyleProb))
            palette.doProgressiveJitterProb = float(_paletteCFGParser.get(_p, "doProgressiveJitterProb", fallback=self.doProgressiveJitterProb))
            palette.jitterIterationsMaxAfterDraw = _paletteCFGParser.getint(_p, "jitterIterationsMax", fallback=self.jitterIterationsMaxAfterDraw)
            palette.jitterIterationsMin = _paletteCFGParser.getint(_p, "jitterIterationsMin", fallback=mrksMngr.jitterIterationsMin)
            palette.jitterIterationsMax = _paletteCFGParser.getint(_p, "jitterIterationsMax", fallback=self.jitterIterationsMax)
            palette.jitterDisplacementHorizontal = float(_paletteCFGParser.get(_p, "jitterDisplacementHorizontal", fallback=self.jitterDisplacementHorizontal))
            palette.jitterDisplacementVertical = float(_paletteCFGParser.get(_p, "jitterDisplacementVertical", fallback=self.jitterDisplacementVertical))
            palette.jitterIterationsMin_roughing = _paletteCFGParser.getint(_p, "jitterIterationsMin", fallback=self.jitterIterationsMin_roughing)
            palette.jitterIterationsMax_roughing = _paletteCFGParser.getint(_p, "jitterIterationsMax", fallback=self.jitterIterationsMax_roughing)
            palette.jitterDisplacementHorizontal_roughing = float(_paletteCFGParser.get(_p, "jitterDisplacementHorizontal", fallback=self.jitterDisplacementHorizontal_roughing))
            palette.jitterDisplacementVertical_roughing = float(_paletteCFGParser.get(_p, "jitterDisplacementVertical", fallback=self.jitterDisplacementVertical_roughing))
            palette.linesDrawnCountMin = _paletteCFGParser.getint(_p, "linesDrawnCountMin", fallback=mrksMngr.linesDrawnCountMinBase)

            palette.penSpeedMinVal = float(_paletteCFGParser.get(_p, "penSpeedMinVal", fallback=1))
            palette.penSpeedMaxVal = float(_paletteCFGParser.get(_p, "penSpeedMaxVal", fallback=8))

            palette.xOffsetRange = list(
                map(
                    lambda x: float(x),
                    _paletteCFGParser.get(_p, "xOffsetRange", fallback=f"0,{self.pictureWidth}").split(","),
                )
            )
            palette.yOffsetRange = list(
                map(
                    lambda x: float(x),
                    _paletteCFGParser.get(_p, "yOffsetRange", fallback=f"0,{self.pictureHeight}").split(","),
                )
            )
            palette.penAlphaRange = list(
                map(
                    lambda x: float(x),
                    _paletteCFGParser.get(_p, "penAlphaRange", fallback=f"{self.penAlpha},{self.penAlpha}").split(","),
                )
            )

            palette.changePenColorWhileDrawingProb = float(_paletteCFGParser.get(_p, "changePenColorWhileDrawingProb", fallback=0.01))
            palette.drawLineAsEnvelope = _paletteCFGParser.getboolean(_p, "drawLineAsEnvelope", fallback=self.drawLineAsEnvelope)
            palette.outlineStroke = _paletteCFGParser.getboolean(_p, "outlineStroke", fallback=False)
            palette.outlineStrokeColor = tuple(map(lambda x: int(x), _paletteCFGParser.get(_p, "outlineStrokeColor", fallback="0,0,0,200").split(",")))

            palette.dripWidthMax = float(_paletteCFGParser.get(_p, "dripWidthMax", fallback=0.0))
            palette.dripLengthMax = float(_paletteCFGParser.get(_p, "dripLengthMax", fallback=0.0))
            palette.dripProbablility = float(_paletteCFGParser.get(_p, "dripProbablility", fallback=0.0))
            palette.dripSpeedMin = float(_paletteCFGParser.get(_p, "dripSpeedMin", fallback=0.0))
            palette.dripSpeedMax = float(_paletteCFGParser.get(_p, "dripSpeedMax", fallback=0.0))

            pieceLogger(f"===> Loading palette: {palette.name}  Using enveloped line: {palette.drawLineAsEnvelope}")
            self.paletteSets.append(palette)

        self.activePalette = random.choice(self.paletteSets)
        pieceLogger(f"===> New Palette : {self.activePalette.name} Using enveloped line:{palette.drawLineAsEnvelope}", 4, True)

        setBGColor()

        # ---- pen config ----
        self.penNames = workConfig.get("drawingField", "penNames").split(",")
        self.marksPalette = []

        for _penConfigName in self.penNames:
            _mark = _load_single_pen(_penConfigName)
            self.marksPalette.append(_mark)

        # ---- system init ----
        self.changeBGColorProb = float(workConfig.get("drawingField", "changeBGColorProb", fallback=0.001))
        self.totalResetTime = workConfig.getint("drawingField", "totalResetTime", fallback=33)
        self.totalResetTimeMaxMultiplier = float(workConfig.get("drawingField", "totalResetTimeMaxMultiplier", fallback=1.0))
        self.changeDrawingModeTime = float(workConfig.get("drawingField", "changeDrawingModeTime", fallback=100.0))

        self.blendLevelRateBase = float(workConfig.get("drawingField", "blendLevelRateBase", fallback=0.01))
        self.totalRandomPenColorProb = float(workConfig.get("drawingField", "totalRandomPenColorProb", fallback=0.0))
        self.totalRandomBGBoxColorProb = float(workConfig.get("drawingField", "totalRandomBGBoxColorProb", fallback=0.0))
        self.debugMode = workConfig.getboolean("drawingField", "debugMode", fallback=False)

        self.changeColorSetTime = float(workConfig.get("drawingField", "changeColorSetTime", fallback=0))
        self.changeColorSetTimeMaxMultiplier = float(workConfig.get("drawingField", "changeColorSetTimeMaxMultiplier", fallback=1))

        self.justHitPauseProb = float(workConfig.get("drawingField", "justHitPauseProb", fallback=0.0))
        self.releaseFromJustHitPauseProb = float(workConfig.get("drawingField", "releaseFromJustHitPauseProb", fallback=1.0))
        self.justHitPause = False

        if self.changeColorSetTime > 0:
            self.paletteController = Director(self.config)
            self.paletteController.slotRate = self.changeColorSetTime
            self.changeColorSetTimeToUse = self.changeColorSetTime

        if self.changeDrawingModeTime > 0:
            self.changeTimeController = Director(self.config)
            self.changeTimeController.slotRate = self.changeDrawingModeTime

        self.config.slotRate = float(workConfig.get("drawingField", "slotRate", fallback=0.03))
        self.config.redrawSpeed = float(workConfig.get("drawingField", "redrawSpeed", fallback=0.03))

        self.config.directorController = Director(self.config)
        self.config.directorController.slotRate = self.config.slotRate

        self.drawingController = Director(self.config)
        self.drawingController.slotRate = 10

        self.stateReportController = Director(self.config)
        self.stateReportController.slotRate = 25

        self.canDraw = True
        self.doingDrawing = False
        self.doingJitter = False
        self.stoppedAndWaitingToDraw = False
        self.linesDrawnCount = 0
        self.jitterIterations = 0

        self.penArray = []
        self.drawingMode = 1

        self.dripsArray = []
        initDrawings()

        self.blendLevel = 0.0
        self.blendLevelRate = self.blendLevelRateBase

        self.fadeThruToNew = 255
        self.fadeThruToNewDone = True

        self.transitionStateHandler = TransitionStates(self.config)
        self.transitionStateHandler.sourceImage = self.config.finalCompositeLayer
        self.transitionStateHandler.targetImage = self.config.finalCompositeLayer
        self.inTransition = False

        # self.config.underLayerDraw.rectangle((0, 0, self.pictureWidth, self.pictureHeight), fill=(100, 0, 80, 100))


class Palette:
    ''' The colors, jitter, speed, outline, drip characteristics of the drawing painting'''
    bgBoxAlphaRange = ()
    bgColorSets = []
    penColorSets = []
    bgBoxColorSets = []
    bgBoxRange = []
    noPenGrays = 0
    pens = []
    name = ""
    textureName = ""

    usebgBoxProb = .01
    blendLevelRateBase = .01
    clearCurrentDrawingProb = .0001
    startNewLineProb = .01
    startNewLineDelayRange = [1,10]

    # jitter and roughing palette overrides
    doJitterProb = 0.0
    doJitterAfterLineUseProb = 0.0
    doJitterWhenAddingBGUseProb = 0.0
    doJitterEventPerCyleProb = 0.0
    doProgressiveJitterProb = 0.0
    jitterIterationsMaxAfterDraw = 0
    jitterIterationsMin = 1
    jitterIterationsMax = 1
    jitterDisplacementHorizontal = 0.0
    jitterDisplacementVertical = 0.0
    jitterIterationsMin_roughing = 1
    jitterIterationsMax_roughing = 1
    jitterDisplacementHorizontal_roughing = 0.0
    jitterDisplacementVertical_roughing = 0.0
    linesDrawnCountMin = 1

    penSpeedMinVal = 1.0
    penSpeedMaxVal = 8.0

    xOffsetRange = [0,0]
    yOffsetRange = [0,0]
    penAlphaRange = [100,200]

    changePenColorWhileDrawingProb = 0.01
    drawLineAsEnvelope = True
    outlineStroke = False
    outlineStrokeColor = (0,0,0,200)

    dripWidthMax = 0.0
    dripLengthMax = 0.0
    dripProbablility =0.0
    dripSpeedMin =0.0
    dripSpeedMax =0.0


    def __init__(self):
        pass


class Pen:
    ''' The active drawing pen or brush or stylus'''
    def __init__(self):
        pass


class Mark:
    ''' The shape or character that the pen will draw or paint'''
    lastAngle = 0
    angleDiffMax = 70

    def __init__(self):
        pass


class Texture:
    def __init__(self):
        pass


class TransitionStates:
    rate = 0.02
    count = 0
    countMax = 20
    inTransition = False
    chunckSize = 140

    def __init__(self, config):
        self.transitionController = Director(config)
        self.transitionController.slotRate = self.rate

    def initiateTransition(self):
        self.inTransition = True
        self.count = 0

        self.destinationImage = Image.new("RGBA", (mrksMngr.pictureWidth, mrksMngr.pictureHeight))
        self.intermediateImage = Image.new("RGBA", (mrksMngr.pictureWidth, mrksMngr.pictureHeight))

        self.destinationImageDraw = ImageDraw.Draw(self.destinationImage)
        self.destinationImageDraw.rectangle((0, 0, 50, 50), fill=(200, 0, 0, 200))

    def transition(self):
        self.transitionController.checkTime()
        if self.transitionController.advance:
            self.stepThru()

    def stepThru(self):

        # pieceLogger(self.count)
        if self.count < self.countMax:
            _x = round(random.uniform(-self.chunckSize / 2, mrksMngr.pictureWidth))
            _y = round(random.uniform(-self.chunckSize / 2, mrksMngr.pictureHeight))
            _part = self.sourceImage.crop((_x, _y, _x + self.chunckSize, _y + self.chunckSize))
            self.intermediateImage.paste(_part, (_x, _y), _part)
            self.count += 1
        else:
            self.inTransition = False


# ----------------------------------------------------##----------------------------------------------------#


def chaikins_corner_cutting(coords, refinements=2, ratio=0.75):
    # https://stackoverflow.com/questions/47068504/where-to-find-python-implementation-of-chaikins-corner-cutting-algorithm
    coords = np.array(coords)

    for _ in range(refinements):
        L = coords.repeat(2, axis=0)
        R = np.empty_like(L)
        R[0] = L[0]
        R[2::2] = L[1:-1:2]
        R[1:-1:2] = L[2::2]
        R[-1] = L[-1]
        coords = L * ratio + R * (1.00 - ratio)

    return coords


def catmull_rom(p0, p1, p2, p3, t):
    t2 = t * t
    t3 = t2 * t

    return 0.5 * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3)


def R(a, b, rounded=False):
    if not rounded:
        return random.uniform(a, b)
    else:
        return round(random.uniform(a, b))


# ----------------------------------------------------##----------------------------------------------------#


def changeDrawing(args):
    global config
    pieceLogger("CHANGE DRAWING/PAINTING", 2)
    createImageLayers()
    changePalettes()
    initDrawings()

    mrksMngr.systemController = Director(config)
    _newTime = round(random.uniform(mrksMngr.totalResetTime, round(float(mrksMngr.totalResetTime) * mrksMngr.totalResetTimeMaxMultiplier)))
    mrksMngr.systemController.slotRate = _newTime

    # config.underLayerDraw.rectangle((0, 0, mrksMngr.pictureWidth, mrksMngr.pictureHeight), fill=mrksMngr.bgColor)
    # config.finalCompositeLayerDraw.rectangle((0, 0, mrksMngr.pictureWidth, mrksMngr.pictureHeight), fill=mrksMngr.bgColor)
    mrksMngr.fadeThruToNew = 0
    initiateTransition()


def changeDrawingMode():
    mrksMngr.drawingMode = round(random.uniform(1, 4))
    # mrksMngr.startNewLineProb = 0.005
    mrksMngr.changeTimeController.slotRate = round(random.uniform(20, 33))

    if mrksMngr.drawingMode in {2, 3}:
        # mrksMngr.startNewLineProb = 0.1
        mrksMngr.changeTimeController.slotRate = round(random.uniform(33, 63))

    pieceLogger(f" => New Drawing Mode: {mrksMngr.drawingMode} slotRate{mrksMngr.changeTimeController.slotRate}")


def changePalettes():
    mrksMngr.activePalette = random.choice(mrksMngr.paletteSets)
    pieceLogger(f"===> New Palette : {mrksMngr.activePalette.name}", 4, True)
    setBGColor()
    config.canvasDraw.rectangle((0, 0, mrksMngr.pictureWidth, mrksMngr.pictureHeight), fill=(mrksMngr.bgColor))
    config.canvasDraw.rectangle((0, 0, mrksMngr.pictureWidth, mrksMngr.pictureHeight), fill=(mrksMngr.bgColor))
    config.underLayerDraw.rectangle((0, 0, mrksMngr.pictureWidth, mrksMngr.pictureHeight), fill=(mrksMngr.bgColor))
    config.underLayerDraw.rectangle((0, 0, mrksMngr.pictureWidth, mrksMngr.pictureHeight), fill=(mrksMngr.bgColor))
    primeCanvas()
    # pieceLogger(f" New bg Color : {mrksMngr.bgColor}")
    # pieceLogger(f"brightness calculated = {colorutils.brightness(mrksMngr.bgColor[0],mrksMngr.bgColor[1],mrksMngr.bgColor[2])}")
    mrksMngr.changeColorSetTimeToUse = round(random.uniform(mrksMngr.changeColorSetTime, round(mrksMngr.changeColorSetTime * mrksMngr.changeColorSetTimeMaxMultiplier)))
    mrksMngr.paletteController.slotRate = mrksMngr.changeColorSetTimeToUse

    mrksMngr.bgBoxRange = mrksMngr.activePalette.bgBoxRange
    mrksMngr.drawLineAsEnvelope = mrksMngr.activePalette.drawLineAsEnvelope
    mrksMngr.doJitterProb = mrksMngr.activePalette.doJitterProb

    pieceLogger(f"mrksMngr.drawLineAsEnvelope {mrksMngr.drawLineAsEnvelope} <== {mrksMngr.activePalette.drawLineAsEnvelope}")
    pieceLogger(f"mrksMngr.doJitterProb {mrksMngr.doJitterProb} ")


def initiateTransition():
    pieceLogger(" ITNITATE TRANSITION", 3)
    mrksMngr.transitionStateHandler.sourceImage = config.finalCompositeLayer
    mrksMngr.transitionStateHandler.initiateTransition()


# ------------------------------------------- PEN ACTIONS ---------------------------------------------------#


def startNewLine(_pen):
    # pieceLogger(f"=========>   startNewLine _pen ==> {_pen.name} {mrksMngr.activePalette.pens}")
    setPenProperties(_pen)
    setPenColor(_pen)
    _img = generateSmoothLinePoints(_pen)
    _pen._p = 1
    mrksMngr.dripsArray = []

    # LINE LAYER IS NOW config.lineLayer
    # config.image = Image.new("RGBA", (mrksMngr.pictureWidth, mrksMngr.pictureHeight))
    # config.draw = ImageDraw.Draw(config.image)


def setPenProperties(pen):
    # pieceLogger(f"setting {pen} {pen.name}")
    setPenPropsByName(pen.name, pen)
    setPenColor(pen)


def setPenPropsByName(_name, pen):

    # TODO Add some specific pen based rules for shapes based on where
    # the center may end up and how much we want the pen to exit the edges
    # or stay close to the edge - i.e. like Jerry, close to the edge but
    # not over the edge
    _penProps = None

    for _p in mrksMngr.marksPalette:
        _penProps = _p
        if _p.name == _name:
            _penProps = _p
            break
    pen.name = _name

    """
    Added Scribble like marks - the marks that are a sign or signifier for mark
    making - marks as constrution of the image plane that recall the hand as
    much as stand in for the hand - since painting has become algorithmic of
    its own accord - maybe so much exposure to all the art ever made means 
    the act of marking is more an act of choice of type of mark
    """
    if "scribble" in pen.name:
        # pen.points = R(_penProps.minNumPoints, _penProps.maxNumPoints, True)
        pen.loopsMin = _penProps.loopsMin
        pen.loopsMax = _penProps.loopsMax

        pen.noiseX = _penProps.noiseX
        pen.noiseY = _penProps.noiseY

        # // line sizing
        pen.height = _penProps.height
        pen.radiusX = _penProps.radiusX
        pen.radiusY = _penProps.radiusY
        pen.radiusXMin = _penProps.radiusXMin
        pen.radiusXMax = _penProps.radiusXMax
        pen.radiusYMin = _penProps.radiusYMin
        pen.radiusYMax = _penProps.radiusYMax
        pen.xRadiusDelta = _penProps.xRadiusDelta
        pen.yRadiusDelta = _penProps.yRadiusDelta
        pen.deltaRadiusXChangeProb = _penProps.deltaRadiusXChangeProb
        pen.deltaRadiusYChangeProb = _penProps.deltaRadiusYChangeProb

        # // line placement and centering
        pen.centerXDelta = _penProps.centerXDelta
        pen.centerYDelta = _penProps.centerYDelta
        pen.deltaRadiusXCenterChangeProb = _penProps.deltaRadiusXCenterChangeProb
        pen.deltaRadiusYCenterChangeProb = _penProps.deltaRadiusYCenterChangeProb
        pen.loops = R(pen.loopsMin, pen.loopsMax, True)
        pen.points = round(pen.loops * _penProps.pointsPerLoop)

        """"
        # putting pen speed variables in the palette config rather than in the 
        # pen configuration
        """
        pen.penSpeedMinVal = mrksMngr.activePalette.penSpeedMinVal
        pen.penSpeedMaxVal = mrksMngr.activePalette.penSpeedMaxVal

        pen.speed = round(random.uniform(_penProps.penSpeedMinVal, _penProps.penSpeedMaxVal))

        pen.loopDirection = -1
        if random.random() < 0.5:
            pen.loopDirection = 1
    else:
        pen.minNumPoints = _penProps.minNumPoints
        pen.maxNumPoints = _penProps.maxNumPoints
        pen.num_points = round(random.uniform(pen.minNumPoints, pen.maxNumPoints))
        pen.turns = round(random.uniform(_penProps.turnsRange[0], _penProps.turnsRange[1]))
        pen.minInterpolatedPoints = _penProps.minInterpolatedPoints
        pen.maxInterpolatedPoints = _penProps.maxInterpolatedPoints

        pen.baseRadiusFactor = random.uniform(_penProps.baseRadiusFactorRange[0], _penProps.baseRadiusFactorRange[1])
        pen.yRadiusFactor = random.uniform(_penProps.yRadiusFactorRange[0], _penProps.yRadiusFactorRange[1])
        pen.xRadiusFactor = random.uniform(_penProps.xRadiusFactorRange[0], _penProps.xRadiusFactorRange[1])

        pen.xRadiusFactorNoiseFactor = _penProps.xRadiusFactorNoiseFactor
        pen.yRadiusFactorNoiseFactor = _penProps.yRadiusFactorNoiseFactor
        pen.yRandom = round(random.uniform(_penProps.yRandomRange[0], _penProps.yRandomRange[1]))
        pen.xRandom = round(random.uniform(_penProps.xRandomRange[0], _penProps.xRandomRange[1]))

        pen.rotationFactor = _penProps.rotationFactor
        pen.rotationAngle = random.uniform(-math.pi / 2 / pen.rotationFactor, math.pi / 2 / pen.rotationFactor)

        pen.changePenColorWhileDrawingProb = mrksMngr.activePalette.changePenColorWhileDrawingProb

        pen.xTravelRange = _penProps.xTravelRange
        pen.yTravelRange = _penProps.yTravelRange
        pen.xTravelIncr = _penProps.xTravelIncrRange
        pen.yTravelIncr = _penProps.yTravelIncrRange
        pen.xtravelMode = 1 if random.random() < _penProps.xtravelProb else 0
        pen.ytravelMode = 1 if random.random() < _penProps.ytravelProb else 0

        pen.radiusChangePerRound = _penProps.radiusChangePerRound
        pen.linePpoints = _penProps.linePoints
        pen.lopOff = _penProps.lopOff

        # _penSpeedMax = max(1, math.ceil(pen.penSpeedMaxVal))
        # pen.speed = round(random.uniform(1, _penSpeedMax))
        """"
        # putting pen speed variables in the palette config rather than in the 
        # pen configuration
        """
        pen.penSpeedMinVal = mrksMngr.activePalette.penSpeedMinVal
        pen.penSpeedMaxVal = mrksMngr.activePalette.penSpeedMaxVal

        pen.speed = round(random.uniform(_penProps.penSpeedMinVal, _penProps.penSpeedMaxVal))

        pen.loopDirection = -1
        if random.random() < 0.5:
            pen.loopDirection = 1
    # pieceLogger(f"pen.speed {pen.speed} / {_penSpeedMax}")

    pen.drawingSize = [mrksMngr.pictureWidth, mrksMngr.pictureHeight]
    if pen.xOffsetRange is not None:
        pen.xOffset = round(random.uniform(pen.xOffsetRange[0], pen.xOffsetRange[1]))
    else:
        pen.xOffset = round(random.uniform(mrksMngr.activePalette.xOffsetRange[0], mrksMngr.activePalette.xOffsetRange[1]))

    if pen.yOffsetRange is not None:
        pen.yOffset = round(random.uniform(pen.yOffsetRange[0], pen.yOffsetRange[1]))
    else:
        pen.yOffset = round(random.uniform(mrksMngr.activePalette.yOffsetRange[0], mrksMngr.activePalette.yOffsetRange[1]))

    pen._w = _penProps.w
    pen.minMarkWidth = _penProps.minMarkWidth
    pen.maxMarkWidth = _penProps.maxMarkWidth
    pen.changeMarkWidthProb = _penProps.changeMarkWidthProb
    pen.mode = _penProps.mode
    pen.incrementFactor = _penProps.incrementFactor

    if pen.incrementFactor == 0:
        pen._w = round(random.uniform(_penProps.minMarkWidth, _penProps.maxMarkWidth))
    # pen.drawingSize = [180, 180]
    pen.lastPoint = [mrksMngr.pictureWidth / 2, mrksMngr.pictureHeight / 2]
    # pen.centerVariationX = random.randint(mrksMngr.pen_centerVariationXMin, mrksMngr.pen_centerVariationXMin)
    # pen.centerVariationY = random.randint(mrksMngr.pen_centerVariationYMin, mrksMngr.pen_centerVariationYMax)

    # genral size of drawing
    pen.drawingSkipProb = random.uniform(0.0, _penProps.drawingSkip)

    pen._p = 0
    pen.smooth_points = []

    pen.attenuating = False
    pen.enlarging = False
    pen.forceOrientation = _penProps.forceOrientation
    pen.angleDiffMax = _penProps.angleDiffMax

    # if _penProps.drawLineAsEnvelope is not None :
    # pen.drawLineAsEnvelope = _penProps.drawLineAsEnvelope
    # else :
    pen.drawLineAsEnvelope = mrksMngr.activePalette.drawLineAsEnvelope
    pen.outlineStroke = mrksMngr.activePalette.outlineStroke
    pen.outlineStrokeColor = mrksMngr.activePalette.outlineStrokeColor

    # pieceLogger(f"\n===> setting pen props pen.name {pen.name} mrksMngr.drawLineAsEnvelope = {pen.drawLineAsEnvelope} <== {mrksMngr.drawLineAsEnvelope}")
    # pieceLogger(f"pen.drawingSkip {pen.drawingSkip}")
    # pieceLogger("--")


def setPenColor(_pen):

    cR = random.choice(mrksMngr.activePalette.penColorSets)
    # cR = mrksMngr.activePalette.penColor

    # pieceLogger(f"{mrksMngr.activePalette.noPenGrays}")

    _penAlpha = round(random.uniform(mrksMngr.activePalette.penAlphaRange[0], mrksMngr.activePalette.penAlphaRange[1]))

    if _pen.forcedPalette is None:
        _pen.lineColor = colorutils.getRandomColorHSV(cR[0], cR[1], cR[2], cR[3], cR[4], cR[5], cR[6], cR[7], _penAlpha, config.brightness)
    else:
        _pen.lineColor = colorutils.getRandomColorHSV(
            _pen.forcedPalette[0],
            _pen.forcedPalette[1],
            _pen.forcedPalette[2],
            _pen.forcedPalette[3],
            _pen.forcedPalette[4],
            _pen.forcedPalette[5],
            _pen.forcedPalette[6],
            _pen.forcedPalette[7],
            _penAlpha,
            config.brightness,
        )


def choosePenMark():
    _penName = random.choice(mrksMngr.activePalette.pens)
    # pieceLogger(f"\nLooking for this pen mark: {_penName}\n")
    for _pen in mrksMngr.marksPalette:
        # pieceLogger(f"{_pen.name} {mrksMngr.activePalette.pens}")
        if _pen.name == _penName:
            # pieceLogger(f"we chose {_pen.name}")
            return _pen


def generateSmoothLinePoints(_pen):

    if "lineMarks" in _pen.name:
        # clearCurrentDrawing()
        generateLine(_pen)
    elif "scribble" in _pen.name:
        generateScribble(_pen)
    else:
        generateCurve(_pen)
    # pieceLogger("Line properties:")
    # for _pnt in range(len(_pen.smooth_points)-2) :
    #     _dy = _pen.smooth_points[_pnt + 1][1] - _pen.smooth_points[_pnt][1]
    #     _dx = _pen.smooth_points[_pnt + 1][0] - _pen.smooth_points[_pnt][0]
    #     _ang = abs(math.atan(_dy/_dx) * 360/math.pi)
    #     pieceLogger(_ang)


def generateLine(_pen):

    points = []
    _rangex = _pen.yRandomRange[0]
    _rangey = _pen.yRandomRange[1]

    _yD = _pen.maxNumPoints
    _pts = round(mrksMngr.pictureHeight / _yD) + 2

    _pen.smooth_points = []

    # pieceLogger(f"=========>  Creating line  {_pen.name} ( {_pen.xOffset} , {_pen.yOffset}) pts {_pts} {_yD}")
    for i in range(_pts):
        if _pen.forceOrientation == "horizontal":
            _y = _rangex - (_rangex * 2 * random.random())
            _x = _yD * i
        else:
            _x = _rangex - (_rangex * 2 * random.random())
            _y = _yD * i + random.uniform(-_rangey, _rangey)
        points.append([_x, _y])
    # for i in range(_pts):
    #     if _pen.forceOrientation == "horizontal":
    #         _y  =  (_rangex - (_rangex * 2 * random.random()))
    #         _x  = _yD * i
    #     else:
    #         _x  =  (_rangex - (_rangex * 2 * random.random()))
    #         _y  = _yD * i + random.uniform(-_rangey,_rangey)
    #     points.append([_x,_y])
    # _pen.smooth_points.append((_x +_pen.xOffset,_y + _pen.yOffset))
    # smoothLine(points, _pen)
    _pen.smooth_points = []
    ratio = random.uniform(0.6, 0.8)
    res = chaikins_corner_cutting(points, 2, ratio).tolist()

    # for lines, really need to handle the yOffset more carefully
    # This has GOT to be a parameter ......
    if _pen.name in ["lineMarksVert", "lineMarksVertTest", "lineMarksVertNarrow"]:
        _pen.yOffset = 0

    _pen.smooth_points.extend((pt[0] + _pen.xOffset, pt[1] + _pen.yOffset) for pt in res)
    # either clockwise or counter
    # if random.random() < 0.5:
    #     _pen.smooth_points.reverse()


def generateScribble(_pen):
    points = generate_loop_stroke(_pen)
    _res = get_curve_points(points, True, 10)

    # _pen.xOffset = 200
    # _pen.yOffset = 200
    _pen.smooth_points = []
    _pen.smooth_points.extend((pt[0] + _pen.xOffset, pt[1] + _pen.yOffset) for pt in _res)

    if random.random() < 0.5:
        _pen.smooth_points.reverse()


def generateCurve(_pen):
    width = _pen.drawingSize[0]
    height = _pen.drawingSize[1]
    num_points = _pen.num_points

    # Generate initial points in a circle
    base_radius = min(width, height) // _pen.baseRadiusFactor
    # Generate random points around a circle
    angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
    points = [_pen.lastPoint]
    points = []

    # center_x = width // 2  # + _pen.xOffset  # + round(centerVariationX - random.random() * centerVariationX * 2)
    # center_y = height // 2  # + _pen.yOffset  # + round(centerVariationY - random.random() * centerVariationY * 2)
    center_x = 0
    center_y = 0

    # pieceLogger(f"Making curve _pen.xOffset {_pen.xOffset} _pen.yOffset {_pen.yOffset}")

    _xTravel = random.uniform(_pen.xTravelRange[0], _pen.xTravelRange[1])
    _yTravel = random.uniform(_pen.yTravelRange[0], _pen.yTravelRange[1])

    _xTravelIncr = random.uniform(_pen.xTravelIncr[0], _pen.xTravelIncr[1])
    _yTravelIncr = random.uniform(_pen.yTravelIncr[0], _pen.yTravelIncr[1])

    for _ in range(_pen.turns):
        for angle in angles:
            # Add random variation to the radius
            radius_x = base_radius * _pen.xRadiusFactor + (_pen.xRadiusFactorNoiseFactor - 2 * _pen.xRadiusFactorNoiseFactor * (random.random()))
            radius_y = base_radius * _pen.yRadiusFactor + (_pen.yRadiusFactorNoiseFactor - 2 * _pen.yRadiusFactorNoiseFactor * (random.random()))
            x = center_x + radius_x * np.cos(angle)
            y = center_y + radius_y * np.sin(angle)

            if random.random() < 0.1:
                x += _pen.xRandom
            if random.random() < 0.1:
                y += _pen.yRandom
            base_radius += random.uniform(-5, 5)

            base_radius += _pen.radiusChangePerRound

            points.append([x, y])

            if _pen.xtravelMode == 1:
                center_x += _xTravel
                _xTravel *= _xTravelIncr
            else:
                center_x += random.uniform(_pen.xTravelRange[0], _pen.xTravelRange[1])

            if _pen.ytravelMode == 1:
                center_y += _yTravel
                _yTravel *= _yTravelIncr
            else:
                center_y += random.uniform(_pen.yTravelRange[0], _pen.yTravelRange[1])
        _pen.lastPoint = [x, y]

    # Close the shape by repeating the first point
    points.append(points[0])
    # smoothLine(points, _pen)

    _pen.smooth_points = []
    res = chaikins_corner_cutting(points, 2).tolist()
    _pen.smooth_points.extend((pt[0] + _pen.xOffset, pt[1] + _pen.yOffset) for pt in res)
    # either clockwise or counter

    if random.random() < 0.5:
        _pen.smooth_points.reverse()


def generate_loop_stroke(_pen):

    pts = []
    _radiusX = _pen.radiusX
    _radiusY = _pen.radiusY
    deltaRadiusX = R(-_pen.xRadiusDelta, _pen.xRadiusDelta)
    deltaRadiusY = R(-_pen.yRadiusDelta, _pen.yRadiusDelta)

    deltaRadiusXCenter = R(-_pen.centerXDelta, _pen.centerXDelta)
    deltaRadiusYCenter = R(-_pen.centerYDelta, _pen.centerYDelta)

    _xCenter = 0
    _yCenter = 0

    points = _pen.points

    # pieceLogger(f"deltaRadiusX {round(deltaRadiusX,4)}")
    # pieceLogger(f"deltaRadiusY {round(deltaRadiusY,4)}")
    # pieceLogger(f"deltaRadiusXCenter {round(deltaRadiusXCenter,4)}")
    # pieceLogger(f"deltaRadiusYCenter {round(deltaRadiusYCenter,4)}")
    # pieceLogger(f"_pen.loops {_pen.loops}")
    # pieceLogger(f"points {points}")
    # pieceLogger(f"_pen.speed {_pen.speed}")
    # pieceLogger(f"_pen.xOffset {_pen.xOffset}")
    # _pen.speed = 8

    for i in range(points):
        t = i / (points - 1)
        ang = _pen.loopDirection * t * math.pi * 2 * _pen.loops
        x = _xCenter + math.sin(ang) * _radiusX + R(-_pen.noiseX, _pen.noiseX)
        y = _yCenter - math.cos(ang) * _radiusY - t * _pen.height + R(-_pen.noiseY, _pen.noiseY)

        _radiusX += deltaRadiusX
        _radiusY += deltaRadiusY

        _xCenter += deltaRadiusXCenter
        _yCenter += deltaRadiusYCenter

        if R(0, 1.0) < _pen.deltaRadiusXChangeProb:
            deltaRadiusX = R(-_pen.xRadiusDelta, _pen.xRadiusDelta)

        if R(0, 1.0) < _pen.deltaRadiusYChangeProb:
            deltaRadiusY = R(-_pen.yRadiusDelta, _pen.yRadiusDelta)

        if R(0, 1.0) < _pen.deltaRadiusXCenterChangeProb:
            deltaRadiusXCenter = R(-_pen.centerXDelta, _pen.centerXDelta)

        if R(0, 1.0) < _pen.deltaRadiusYCenterChangeProb:
            deltaRadiusYCenter = R(-_pen.centerYDelta, _pen.centerYDelta)

        pts.append((x, y))

    # Extra points for smoother Bézier start/end
    pts.insert(0, pts[0])
    pts.append(pts[-1])
    pts.append(pts[-1])

    return pts


def get_curve_points(points, curve_drawn=True, resolution=50):

    if not curve_drawn or len(points) < 2:
        return points

    curve_points = []
    n = len(points)

    for i in range(n - 1):
        p0 = points[max(0, i - 1)]
        p1 = points[i]
        p2 = points[i + 1]
        p3 = points[min(n - 1, i + 2)]

        for step in range(resolution):
            t = step / float(resolution)  # 0 <= t < 1

            x = catmull_rom(p0[0], p1[0], p2[0], p3[0], t)
            y = catmull_rom(p0[1], p1[1], p2[1], p3[1], t)

            curve_points.append((x, y))

    return curve_points


def smoothLine(points, _pen):
    _lopOff = -round(_pen.lopOff)

    # pieceLogger(f"_lopOff {_pen.lopOff} {_lopOff}")
    points = np.array(points)

    # Fit a B-spline to the points
    tck, u = splprep([points[:, 0], points[:, 1]], s=0, k=3, per=1)
    # tck, u = splprep([points[:, 0], points[:, 1]], s=0, k=3, per=1)

    # Generate more points along the spline for smoothness
    _mp = round(random.uniform(_pen.minInterpolatedPoints, _pen.maxInterpolatedPoints))
    u_new = np.linspace(0, 1, _mp)
    smooth_points = splev(u_new, tck)

    # Convert to list of tuples for PIL
    smooth_points_c = list(zip(smooth_points[0], smooth_points[1]))
    # _pen.rotationAngle = 0
    smooth_points_r = []
    for pt in smooth_points_c:
        ptx = pt[0] * np.cos(_pen.rotationAngle) - pt[1] * np.sin(_pen.rotationAngle)
        pty = pt[1] * np.cos(_pen.rotationAngle) + pt[0] * np.sin(_pen.rotationAngle)
        _pen.rotationAngle += _pen.rotationAngle / 500
        smooth_points_r.append((ptx + _pen.xOffset, pty + _pen.yOffset))

    _pen.smooth_points = smooth_points_r[:_lopOff]

    # either clockwise or counter
    if random.random() < 0.5:
        _pen.smooth_points.reverse()

    # pieceLogger(f"line: {_mp} {_n} {noise_factor} ")

    # # Draw the shape
    # color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # for _p in range(1,len(smooth_points)) :
    #     _p1 = smooth_points[_p - 1]
    #     _p2 = smooth_points[_p]
    #     config.draw.line((_p1,_p2), fill = color, width=3)

    # config.draw.polygon(smooth_points, fill=None, outline=color, width=4)

    # return image
    return True


def pauseDrawing():
    mrksMngr.stoppedAndWaitingToDraw = True
    mrksMngr.canDraw = False
    mrksMngr.drawingController.slotRate = random.uniform(mrksMngr.activePalette.startNewLineDelayRange[0], mrksMngr.activePalette.startNewLineDelayRange[1])
    pieceLogger(
        f"Line Drawing paused for {mrksMngr.drawingController.slotRate} {mrksMngr.activePalette.startNewLineDelayRange[0]}/{mrksMngr.activePalette.startNewLineDelayRange[1]} : lines drawn: {mrksMngr.linesDrawnCount}",
        1,
    )


def releaseDrawing():
    mrksMngr.stoppedAndWaitingToDraw = False
    mrksMngr.canDraw = True
    pieceLogger(" Pen released", 2)


def penLoopActions():
    if random.random() < mrksMngr.activePalette.changePenColorWhileDrawingProb:
        setPenColor((mrksMngr.activePalette.activePen))

    # chooses a new pen - however, does not necessarily use it just yet
    # if random.random() < mrksMngr.startNewLineProb and mrksMngr.activePalette.activePen._p == 0 and mrksMngr.canDraw:
    if random.random() < mrksMngr.startNewLineProb and mrksMngr.activePalette.activePen._p == 0:
        _pen = choosePenMark()
        mrksMngr.activePalette.activePen = _pen
        startNewLine(_pen)
        # pieceLogger(f"Next line: {mrksMngr.activePalette.activePen.name}",4)

    if mrksMngr.canDraw and not mrksMngr.addingTo:
        drawLine(mrksMngr.activePalette.activePen)


def drawLine(_pen):
    if _pen.drawLineAsEnvelope:
        drawLinePolyEnvelope(_pen)
    else:
        drawLineSegments(_pen)
    drawDrips()


def drawDrips():
    for _d in mrksMngr.dripsArray:
        if not _d[4]:
            _p1 = _d[0]
            _long = _d[1]
            _wide = _d[2]
            _lineColor = _d[3]
            _speed = _d[5]
            _step = _d[6]
            config.lineLayerDraw.rectangle((_p1[0], _p1[1], _p1[0] + _wide, _p1[1] + _step * _long), fill=_lineColor)
            # config.draw.rectangle((_p1[0], _p1[1], _p1[0] + _wide, _p1[1] + _step * _long), fill=_lineColor)
            _step += 1
            _d[6] = _step
            if _step > _speed:
                _d[4] = True


def drawLinePolyEnvelope(_pen):
    # Draw the shape
    if _pen._p == 1:
        pieceLogger(f"Drawing Line with: {_pen.name}")
        # { _pen.drawingSkipProb}
    _penSkip = random.random() <= _pen.drawingSkipProb
    for _ in range(_pen.speed):
        if _pen._p < len(_pen.smooth_points) and _pen._p > 0:
            _p1 = _pen.smooth_points[_pen._p - 1]
            _p2 = _pen.smooth_points[_pen._p]
            # if abs(_p1[0] - _p2[0])<10 and abs(_p1[1] - _p2[1]) < 30 :
            _dy = _p1[1] - _p2[1]
            _dx = _p1[0] - _p2[0]
            # changed 10-30-2025
            # _angle = (math.atan(_dy/_dx) * 360/math.pi)
            _angle = math.atan2(_dy, _dx) * 360 / math.pi

            if _angle < 0:
                _angle += 360

            _penWidth = _pen._w
            _lineColor = _pen.lineColor

            # old way, very chunky
            # config.draw.line((_p1, _p2), fill=_lineColor, width=_penWidth)

            _orthoAngle = math.pi - math.atan2(_dy, _dx)
            _sinOrthoAngle = math.sin(_orthoAngle)
            _cosOrthoAngle = math.cos(_orthoAngle)

            _orthoD = _penWidth / 2.2

            _orthoP1x = round(_orthoD * _sinOrthoAngle + _p1[0])
            _orthoP1y = round(_orthoD * _cosOrthoAngle + _p1[1])

            _orthoP2x = round(_orthoD * _sinOrthoAngle + _p2[0])
            _orthoP2y = round(_orthoD * _cosOrthoAngle + _p2[1])

            _orthoP3x = round(-_orthoD * _sinOrthoAngle + _p2[0])
            _orthoP3y = round(-_orthoD * _cosOrthoAngle + _p2[1])

            _orthoP4x = round(-_orthoD * _sinOrthoAngle + _p1[0])
            _orthoP4y = round(-_orthoD * _cosOrthoAngle + _p1[1])

            _drawdot = False
            try:
                if _pen._p > 1:
                    _drawdot = True

                    _orthoP1x = _pen.lastOrthoPoint[0]
                    _orthoP1y = _pen.lastOrthoPoint[1]

                    _orthoP4x = _pen.lastOrthoPoint[2]
                    _orthoP4y = _pen.lastOrthoPoint[3]

            except Exception as e:
                pieceLogger(e)

            _poly = ((_orthoP1x, _orthoP1y), (_orthoP2x, _orthoP2y), (_orthoP3x, _orthoP3y), (_orthoP4x, _orthoP4y), (_orthoP1x, _orthoP1y))

            if not _penSkip:
                # config.draw.polygon(_poly, fill=_lineColor, outline=None)
                config.lineLayerDraw.polygon(_poly, fill=_lineColor, outline=None)

            if _pen.outlineStroke:
                config.lineLayerDraw.line(((_orthoP1x, _orthoP1y), (_orthoP2x, _orthoP2y)), fill=_pen.outlineStrokeColor, width=2)
                config.lineLayerDraw.line(((_orthoP3x, _orthoP3y), (_orthoP4x, _orthoP4y)), fill=_pen.outlineStrokeColor, width=2)
                # config.draw.line(((_orthoP1x, _orthoP1y), (_orthoP2x, _orthoP2y)), fill=(0, 0, 0, 200), width=2)
                # config.draw.line(((_orthoP3x, _orthoP3y), (_orthoP4x, _orthoP4y)), fill=(0, 0, 0, 200), width=2)

            # config.draw.line((_p1, _p2), fill=(255,0,0,255), width=1)

            if random.random() < mrksMngr.activePalette.dripProbablility:
                _wide = round(random.uniform(0, mrksMngr.activePalette.dripWidthMax))
                _speed = round(random.uniform(mrksMngr.activePalette.dripSpeedMin, mrksMngr.activePalette.dripSpeedMax))
                _long = round(random.uniform(2, mrksMngr.activePalette.dripLengthMax) / _speed)
                # config.draw.rectangle((_p1[0],_p1[1],_p1[0]+_wide,_p1[1]+_long), fill=_lineColor)
                _drip = [_p1, _long, _wide, _lineColor, False, _speed, 0]
                mrksMngr.dripsArray.append(_drip)

            # if not _markDrawn :
            _pen.lastAngle = _angle
            _pen._p += 1
            _pen.lastOrthoPoint = [_orthoP2x, _orthoP2y, _orthoP3x, _orthoP3y]

            mrksMngr.doingDrawing = True
        if _pen._p == len(_pen.smooth_points):
            _pen._p = 0
            drawLineStopped()

        if random.random() < _pen.changeMarkWidthProb:
            if not _pen.attenuating and not _pen.enlarging:
                if random.random() < 0.5:
                    _pen.attenuating = True
                else:
                    _pen.enlarging = True
            elif random.random() < _pen.changeMarkWidthProb * 2:
                if _pen.attenuating:
                    _pen.enlarging = True
                    _pen.attenuating = False
                else:
                    _pen.enlarging = False
                    _pen.attenuating = True

        if _pen._w > _pen.maxMarkWidth:
            _pen.enlarging = False

        if _pen._w <= _pen.minMarkWidth:
            _pen.attenuating = False
            _pen._w = _pen.minMarkWidth

        if _pen.enlarging:
            _pen._w += round(1 * _pen.incrementFactor)
        if _pen.attenuating:
            _pen._w -= round(1 * _pen.incrementFactor)

        # time.sleep(.5)


def drawLineSegments(_pen):
    # Draw the shape
    # pieceLogger(f"pen {_pen.name}")
    _penSkip = random.random() <= _pen.drawingSkip
    for _ in range(_pen.speed):
        if _pen._p < len(_pen.smooth_points) and _pen._p > 0:
            _p1 = _pen.smooth_points[_pen._p - 1]
            _p2 = _pen.smooth_points[_pen._p]
            # if abs(_p1[0] - _p2[0])<10 and abs(_p1[1] - _p2[1]) < 30 :
            # changed 10-30-2025
            # _angle = abs(math.atan(_p2[1] - _p1[1])/(_p2[0] - _p1[0]))
            _angle = math.atan2(_p2[1] - _p1[1], _p2[0] - _p1[0])
            _penWidth = _pen._w
            if _angle > 30:
                _penWidth - 1
            # pieceLogger(_angle)
            if not _penSkip:
                config.lineLayerDraw.line((_p1, _p2), fill=_pen.lineColor, width=_penWidth)
                # config.draw.line((_p1, _p2), fill=_pen.lineColor, width=_penWidth)
            _pen._p += 1
            mrksMngr.doingDrawing = True
        if _pen._p == len(_pen.smooth_points):
            _pen._p = 0
            drawLineStopped()

        if random.random() < _pen.changeMarkWidthProb:
            if not _pen.attenuating and not _pen.enlarging:
                if random.random() < 0.5:
                    _pen.attenuating = True
                else:
                    _pen.enlarging = True
            elif random.random() < _pen.changeMarkWidthProb * 2:
                if _pen.attenuating:
                    _pen.enlarging = True
                    _pen.attenuating = False
                else:
                    _pen.enlarging = False
                    _pen.attenuating = True

        if _pen._w > _pen.maxMarkWidth:
            _pen.enlarging = False

        if _pen._w <= _pen.minMarkWidth:
            _pen.attenuating = False
            _pen._w = _pen.minMarkWidth

        if _pen.enlarging:
            _pen._w += round(1 * _pen.incrementFactor)
        if _pen.attenuating:
            _pen._w -= round(1 * _pen.incrementFactor)


def drawLineStopped():
    # pieceLogger("Pen stopped")
    mrksMngr.doingDrawing = False
    mrksMngr.linesDrawnCount += 1
    if mrksMngr.linesDrawnCount > mrksMngr.linesDrawnCountMin:
        pauseDrawing()
    if random.random() < mrksMngr.doJitterWhenAddingBGUseProb:
        pieceLogger(f"Doing jitter after LINE has been drawn")
        mrksMngr.doingJitter = False
        mrksMngr.jitterIterations = 0
        doDrawingJitter()


# ----------------------------------------------------


def progressiveJitter():
    """The underLayer has both the blocks as well as the lines and the texture"""

    if random.random() < mrksMngr.doJitterEventPerCyleProb:
        # pieceLogger(f"Jitter {mrksMngr.jitterIterations}")
        glitchBox(
            config.underLayer,
            mrksMngr.pictureWidth,
            mrksMngr.pictureHeight,
            mrksMngr.jitterDisplacementHorizontal,
            mrksMngr.jitterDisplacementVertical,
        )
        mrksMngr.jitterIterations -= 1
        if mrksMngr.jitterIterations <= 0:
            mrksMngr.doingJitter = False
            pieceLogger(f"==> Progressive jitter ended")
            # config.directorController.slotRate *= .25


def doDrawingJitter():
    if not mrksMngr.doingJitter and mrksMngr.jitterIterations == 0:
        mrksMngr.jitterIterations = round(random.uniform(mrksMngr.jitterIterationsMin, mrksMngr.jitterIterationsMax))

        if random.random() < mrksMngr.doProgressiveJitterProb:
            mrksMngr.doingJitter = True
            pieceLogger(f"==> Progressive jitters tarting: jitterIterations {mrksMngr.jitterIterations}/{mrksMngr.jitterIterationsMax}")
        else:
            pieceLogger(f"==> Single bulk jitter: jitterIterations {mrksMngr.jitterIterations}/{mrksMngr.jitterIterationsMax}")
            """ The underLayer has both the blocks as well as the lines and the texture """
            for _ in range(mrksMngr.jitterIterations):
                glitchBox(
                    config.underLayer,
                    mrksMngr.pictureWidth,
                    mrksMngr.pictureHeight,
                    mrksMngr.jitterDisplacementHorizontal,
                    mrksMngr.jitterDisplacementVertical,
                )


def bgColorBlocksFilling(arg):
    global config

    pieceLogger(f"Drawing the background blocks addingTo: {arg}")
    # if not arg:
    #     pieceLogger(f"drawing a bg box {mrksMngr.blendLevel}")

    xPos = math.floor(random.uniform(mrksMngr.activePalette.bgBoxRange[0], mrksMngr.activePalette.bgBoxRange[1]))
    yPos = math.floor(random.uniform(mrksMngr.activePalette.bgBoxRange[2], mrksMngr.activePalette.bgBoxRange[3]))

    config.tileSizeWidth = round(random.uniform(mrksMngr.bgTileSizeWidthMin, mrksMngr.bgTileSizeWidthMax))
    config.tileSizeHeight = round(random.uniform(mrksMngr.bgTileSizeHeightMin, mrksMngr.bgTileSizeHeightMax))

    if arg or mrksMngr.addingTo:
        mrksMngr.blendLevelRate = mrksMngr.blendLevelRateBase
        mrksMngr.blendLevel = 0.0
        config.blockLayer = Image.new("RGBA", (mrksMngr.pictureWidth, mrksMngr.pictureHeight))
        config.blockLayerDraw = ImageDraw.Draw(config.blockLayer)
        config.blankLayer = Image.new("RGBA", (mrksMngr.pictureWidth, mrksMngr.pictureHeight))
        config.blankLayerDraw = ImageDraw.Draw(config.blankLayer)

        _drawLayer = config.blockLayer
        _drawTo = config.blockLayerDraw

        mrksMngr.addingTo = True
        mrksMngr.justHitPause = True
        # adding bit to prevent trying to draw a line when painting  a backgound chunk
        # mrksMngr.canDraw = False

    else:
        _drawLayer = config.underLayer
        _drawTo = config.underLayerDraw

    # _drawLayer = config.blockLayer
    # _drawTo = config.blockLayerDraw

    if random.SystemRandom().random() < mrksMngr.clearbgBoxProb:
        xPos = yPos = 0
        mrksMngr.bgBoxBox = (
            xPos,
            yPos,
            xPos + mrksMngr.pictureWidth,
            yPos + mrksMngr.pictureHeight,
        )
        mrksMngr.bgBoxFill = (0, 0, 0, 0)
    else:
        mrksMngr.bgBoxBox = (
            xPos,
            yPos,
            xPos + config.tileSizeWidth,
            yPos + config.tileSizeHeight,
        )

        cR = random.choice(mrksMngr.activePalette.bgBoxColorSets)
        # cR = mrksMngr.activePalette.bgBoxColorRange
        # pieceLogger(cR)
        mrksMngr.bgBoxFill = colorutils.getRandomColorHSV(
            cR[0],
            cR[1],
            cR[2],
            cR[3],
            cR[4],
            cR[5],
            cR[6],
            cR[7],
            round(random.uniform(mrksMngr.activePalette.bgBoxAlphaRange[0], mrksMngr.activePalette.bgBoxAlphaRange[1])),
            config.brightness,
        )

        if random.random() < mrksMngr.totalRandomBGBoxColorProb:
            mrksMngr.bgBoxFill = colorutils.getRandomColorHSV(
                0, 360, 0.1, 1.0, 0.1, 1.0, 0, 0, round(random.uniform(mrksMngr.activePalette.bgBoxAlphaRange[0], mrksMngr.activePalette.bgBoxAlphaRange[1])), config.brightness
            )

    _drawTo.rectangle(mrksMngr.bgBoxBox, fill=mrksMngr.bgBoxFill)

    # always roughen the blocks being drawn
    jitteriterations = round(random.uniform(mrksMngr.jitterIterationsMin_roughing, mrksMngr.jitterIterationsMax_roughing))
    for _ in range(jitteriterations):
        glitchBox(
            _drawLayer,
            mrksMngr.pictureWidth,
            mrksMngr.pictureHeight,
            mrksMngr.jitterDisplacementHorizontal_roughing,
            mrksMngr.jitterDisplacementVertical_roughing,
        )


def glitchBox(
    imageRef,
    apparentWidth,
    apparentHeight,
    imageGlitchDisplacementHorizontal,
    imageGlitchDisplacementVertical,
):

    global config

    # apparentWidth = config.canvasImage.size[0]
    # apparentHeight = config.canvasImage.size[1]

    dx = round(random.uniform(-imageGlitchDisplacementHorizontal, imageGlitchDisplacementHorizontal))
    dy = round(random.uniform(-imageGlitchDisplacementVertical, imageGlitchDisplacementVertical))

    sectionWidth = round(random.uniform(2, apparentWidth - dx))
    sectionHeight = round(random.uniform(2, apparentHeight - dy))

    # pieceLogger(f"jitter {sectionWidth} {sectionHeight} {dx} {dx}")

    # 95% of the time they dance together as mirrors
    try:
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
        pieceLogger(f"jitter prom {e} {dx + sectionWidth} , {dy + sectionHeight}")
    # end try


# ----------------------------------------------------#


def setBGColor():

    _bgColorSet = random.choice(mrksMngr.activePalette.bgColorSets)
    mrksMngr.bgColor = colorutils.getRandomColorHSV(*_bgColorSet)
    # mrksMngr.bgColor = colorutils.getRandomColorHSV(*mrksMngr.activePalette.bgColor)
    # pieceLogger(f"New BGColor: mrksMngr.activePalette.bgColor {mrksMngr.activePalette.bgColor} --> mrksMngr.bgColor {mrksMngr.bgColor}")


def primeCanvas(_i=3):
    global config
    for _ in range(_i):
        bgColorBlocksFilling(False)


def chooseTexture():
    _textureName = mrksMngr.activePalette.textureName
    for _t in mrksMngr.textureSets:
        # pieceLogger(f"{_pen.name} {mrksMngr.activePalette.pens}")
        if _t.name == _textureName:
            # pieceLogger(f"we chose {_pen.name}")
            return _t


# ----------------------------------------------------#


def createImageLayers(arg=None):
    global config
    pieceLogger("===> Setting up all layers")

    config.image = Image.new("RGBA", (mrksMngr.pictureWidth, mrksMngr.pictureHeight))
    config.draw = ImageDraw.Draw(config.image)

    config.blankLayer = Image.new("RGBA", (mrksMngr.pictureWidth, mrksMngr.pictureHeight))
    config.blankLayerDraw = ImageDraw.Draw(config.blankLayer)

    config.underLayer = Image.new("RGBA", (mrksMngr.pictureWidth, mrksMngr.pictureHeight))
    config.underLayerDraw = ImageDraw.Draw(config.underLayer)

    config.blockLayer = Image.new("RGBA", (mrksMngr.pictureWidth, mrksMngr.pictureHeight))
    config.blockLayerDraw = ImageDraw.Draw(config.blockLayer)

    config.lineLayer = Image.new("RGBA", (mrksMngr.pictureWidth, mrksMngr.pictureHeight))
    config.lineLayerDraw = ImageDraw.Draw(config.lineLayer)

    config.canvasImage = Image.new("RGBA", (mrksMngr.pictureWidth, mrksMngr.pictureHeight))
    config.canvasDraw = ImageDraw.Draw(config.canvasImage)

    config.textureLayer = Image.new("RGBA", (mrksMngr.pictureWidth, mrksMngr.pictureHeight))
    config.textureLayerDraw = ImageDraw.Draw(config.textureLayer)

    config.finalCompositeLayer = Image.new("RGBA", (config.screenWidth, config.screenHeight))
    config.finalCompositeLayerDraw = ImageDraw.Draw(config.finalCompositeLayer)

    config.renderImageFullOverlay = Image.new("RGBA", (mrksMngr.pictureWidth, mrksMngr.pictureHeight))
    config.renderDrawOver = ImageDraw.Draw(config.renderImageFullOverlay)

    mrksMngr.addingTo = False


def createTextureLayer(tex):
    mrksMngr.useTextureLayer = tex.useTextureLayer
    mrksMngr.textureBlendMode = tex.blendMode
    mrksMngr.textureOption = random.choice([0, 1, 2])
    pieceLogger(f"===> mrksMngr.useTextureLayer {mrksMngr.useTextureLayer} texture option {mrksMngr.textureOption}")
    for _row in range(tex.blockRows):
        for _col in range(tex.blockCols):
            if random.random() > tex.skipProb:
                for _r in range(0, tex.rows, tex.step):
                    for _c in range(0, tex.cols, tex.step):
                        x1 = _c + _col * tex.cols
                        y1 = _r + _row * tex.rows
                        x2 = x1 + tex.px
                        y2 = y1 + tex.px
                        _rate = random.uniform(1, 3)
                        _a = 2 + round(tex.base / tex.base * _r / ((tex.rows - _r) * tex.rate) * _c / ((tex.cols - _c) * tex.rate))

                        if tex.base == 255:
                            _a = tex.base
                        if random.random() < tex.drawMark:
                            if tex.usedots:
                                config.textureLayerDraw.ellipse((x1, y1, x2, y2), fill=(tex.clr_r, tex.clr_g, tex.clr_b, _a), outline=None)
                            else:
                                config.textureLayerDraw.rectangle((x1, y1, x2 + tex.xtick, y2 + tex.ytick), fill=(tex.clr_r, tex.clr_g, tex.clr_b, _a), outline=None)
                                # config.textureLayerDraw.line((x1, y1, x2+_xtick, y2+_ytick), fill=(_clr_r, _clr_g, _clr_b, 255), width=0)
    if tex.blur > 0:
        config.textureLayer = config.textureLayer.filter(ImageFilter.GaussianBlur(radius=tex.blur))


def initDrawings():
    global config
    pieceLogger(f"===> Init drawings: {mrksMngr.activePalette.name}", 4, True)

    createTextureLayer(chooseTexture())
    config.underLayerDraw.rectangle((0, 0, mrksMngr.pictureWidth, mrksMngr.pictureHeight), fill=mrksMngr.bgColor)
    primeCanvas()

    _pen = choosePenMark()
    mrksMngr.activePalette.activePen = _pen
    mrksMngr.startNewLineProb = mrksMngr.activePalette.startNewLineProb
    mrksMngr.usebgBoxProb = mrksMngr.activePalette.usebgBoxProb
    mrksMngr.clearCurrentDrawingProb = mrksMngr.activePalette.clearCurrentDrawingProb

    mrksMngr.doJitterProb = mrksMngr.activePalette.doJitterProb
    mrksMngr.doJitterAfterLineUseProb = mrksMngr.activePalette.doJitterAfterLineUseProb
    mrksMngr.doProgressiveJitterProb = mrksMngr.activePalette.doProgressiveJitterProb
    mrksMngr.doJitterWhenAddingBGUseProb = mrksMngr.activePalette.doJitterWhenAddingBGUseProb
    mrksMngr.doJitterEventPerCyleProb = mrksMngr.activePalette.doJitterEventPerCyleProb
    mrksMngr.jitterIterationsMaxAfterDraw = mrksMngr.activePalette.jitterIterationsMaxAfterDraw
    mrksMngr.jitterIterationsMin = mrksMngr.activePalette.jitterIterationsMin
    mrksMngr.jitterIterationsMax = mrksMngr.activePalette.jitterIterationsMax
    mrksMngr.jitterDisplacementHorizontal = mrksMngr.activePalette.jitterDisplacementHorizontal
    mrksMngr.jitterDisplacementVertical = mrksMngr.activePalette.jitterDisplacementVertical
    mrksMngr.jitterIterationsMin_roughing = mrksMngr.activePalette.jitterIterationsMin_roughing
    mrksMngr.jitterIterationsMax_roughing = mrksMngr.activePalette.jitterIterationsMax_roughing
    mrksMngr.jitterDisplacementHorizontal_roughing = mrksMngr.activePalette.jitterDisplacementHorizontal_roughing
    mrksMngr.jitterDisplacementVertical_roughing = mrksMngr.activePalette.jitterDisplacementVertical_roughing
    mrksMngr.jitterIterations = 0
    mrksMngr.linesDrawnCountMin = mrksMngr.activePalette.linesDrawnCountMin
    mrksMngr.linesDrawnCount = 0

    startNewLine(_pen)

    # pieceLogger("Jitter trigger after inti drawing")
    # doDrawingJitter()


# ----------------------------------------------------##----------------------------------------------------#


def runWork():
    while True:
        config.directorController.checkTime()
        if config.directorController.advance:
            iterate()

        time.sleep(config.redrawSpeed)


def iterate():
    global config

    if random.random() < mrksMngr.justHitPauseProb and not mrksMngr.justHitPause and mrksMngr.linesDrawnCount >= mrksMngr.activePalette.linesDrawnCountMin:
        mrksMngr.justHitPause = True
        pieceLogger(f"I am paused {mrksMngr.justHitPauseProb}", 1)

    if random.random() < mrksMngr.releaseFromJustHitPauseProb and mrksMngr.justHitPause:
        mrksMngr.justHitPause = False
        pieceLogger("I am un paused", 2)

    if mrksMngr.doingJitter:
        progressiveJitter()

    if not mrksMngr.justHitPause:

        def maybe_change_drawing_mode():
            if mrksMngr.changeDrawingModeTime > 0:
                mrksMngr.changeTimeController.checkTime()
                if mrksMngr.changeTimeController.advance:
                    changeDrawingMode()

        def maybe_change_color_set():
            if mrksMngr.changeColorSetTime > 0 and not mrksMngr.transitionStateHandler.inTransition:
                mrksMngr.paletteController.checkTime()
                if mrksMngr.paletteController.advance:
                    pieceLogger(f"===>  changeDrawing(True) prob: mrksMngr.changeColorSetTime {mrksMngr.changeColorSetTime}")
                    changeDrawing(True)

        def maybe_release_drawing():
            if mrksMngr.stoppedAndWaitingToDraw:
                mrksMngr.drawingController.checkTime()
                if mrksMngr.drawingController.advance:
                    releaseDrawing()

        def maybe_set_bg_color():
            if random.SystemRandom().random() < mrksMngr.changeBGColorProb:
                setBGColor()

        def maybe_clear_current_drawing():
            if random.random() < mrksMngr.clearCurrentDrawingProb and not mrksMngr.transitionStateHandler.inTransition:
                pieceLogger(f"===>  clearCurrentDrawing() prob: mrksMngr.clearCurrentDrawingProb {mrksMngr.clearCurrentDrawingProb}")
                clearCurrentDrawing()

        def maybe_bg_color_blocks_filling():
            if random.SystemRandom().random() < mrksMngr.usebgBoxProb and not mrksMngr.doingDrawing and not mrksMngr.transitionStateHandler.inTransition:
                bgColorBlocksFilling(True)
                if random.random() < mrksMngr.doJitterWhenAddingBGUseProb:
                    pieceLogger("Calling for jitter after BG blocks are drawn")
                    doDrawingJitter()

        def maybe_do_drawing_jitter():
            if not mrksMngr.doingDrawing and random.random() < mrksMngr.doJitterProb and not mrksMngr.transitionStateHandler.inTransition:
                pieceLogger("Calling for jitter")
                doDrawingJitter()

        # maybe_change_drawing_mode()
        maybe_change_color_set()
        maybe_release_drawing()
        maybe_set_bg_color()
        maybe_clear_current_drawing()
        maybe_bg_color_blocks_filling()
        maybe_do_drawing_jitter()
        penLoopActions()

        overlayControls.handleOverlayActions()
    renderImage()


def renderImage():
    global config

    def maybe_take_snapshot(img):
        mrksMngr.stateReportController.checkTime()
        path = "/Users/lamshell/Desktop/outputs/"
        if mrksMngr.stateReportController.advance:
            pieceLogger("Saving image to file", 2)
            currentTime = time.time()
            baseName = f"{str(currentTime)}"
            baseName = baseName.replace(".", "")
            _img = img.convert("RGBA")
            _temp = Image.new("RGBA", (mrksMngr.pictureWidth, mrksMngr.pictureHeight))
            _tempDraw = ImageDraw.Draw(_temp)
            _tempDraw.rectangle((0, 0, mrksMngr.pictureWidth, mrksMngr.pictureHeight), fill=(0, 0, 0, 255))
            _temp.paste(_img)
            _temp = _temp.convert("RGB")
            _temp = _temp.rotate(-90)
            fn = f"{path}{baseName}.png"
            _temp.save(fn)
            # fn2 = f"{baseName}-palette.txt"
            fn2 = "palettes.txt"
            with open(f"/Users/lamshell/Desktop/outputs/{fn2}", "a+") as f:
                _bg = colorutils.rgb_to_hsv(mrksMngr.bgColor[0], mrksMngr.bgColor[1], mrksMngr.bgColor[2], mrksMngr.bgColor[3], True)
                _bgf = colorutils.rgb_to_hsv(mrksMngr.bgBoxFill[0], mrksMngr.bgBoxFill[1], mrksMngr.bgBoxFill[2], mrksMngr.bgBoxFill[3], True)
                _pc = colorutils.rgb_to_hsv(
                    mrksMngr.activePalette.activePen.lineColor[0],
                    mrksMngr.activePalette.activePen.lineColor[1],
                    mrksMngr.activePalette.activePen.lineColor[2],
                    mrksMngr.activePalette.activePen.lineColor[3],
                    True,
                )

                f.write(f"\n{baseName} bg:{_bg} {mrksMngr.bgColor[3]} fill:{_bgf} {mrksMngr.bgBoxFill[3]} pen:{_pc} {mrksMngr.activePalette.activePen.lineColor[3]}")

    config.underLayer.paste(config.lineLayer, (0, 0), config.lineLayer)
    config.canvasImage.paste(config.underLayer, (0, 0), config.underLayer)

    """ TEXTURE APPEARANCE"""
    if mrksMngr.useTextureLayer and mrksMngr.textureBlendMode is None:
        # config.textureLayerDraw.rectangle((50,50,150,150), fill=(255,255,0,200))

        # some subtleties here  -- can be any of these and might be something
        # to paramterize - it's a bit like a scumble as the texture affects
        # the bg and the line and can be distorted

        if mrksMngr.textureOption == 0:
            """this means the topmost layer gets the texture - most visible version"""
            config.lineLayer.paste(config.textureLayer, (0, 0), config.textureLayer)

        if mrksMngr.textureOption == 1:
            """# the composite gets it -- more subtle"""
            config.canvasImage.paste(config.textureLayer, (0, 0), config.textureLayer)

        if mrksMngr.textureOption == 2:
            """this means only the underlayer gets the texture - not so great"""
            config.underLayer.paste(config.textureLayer, (0, 0), config.textureLayer)

    """ deprecated -------->"""
    # handling transition between drawings
    # if mrksMngr.fadeThruToNew < 255:
    #     mrksMngr.fadeThruToNew += 4
    #     # pieceLogger(f"mrksMngr.fadeThruToNew  {mrksMngr.fadeThruToNew }")
    #     config.canvasDraw.rectangle((0, 0, mrksMngr.pictureWidth, mrksMngr.pictureHeight), fill=(mrksMngr.bgColor[0], mrksMngr.bgColor[1], mrksMngr.bgColor[2], mrksMngr.fadeThruToNew))

    # elif not mrksMngr.fadeThruToNewDone:
    #     mrksMngr.fadeThruToNewDone = True
    #     initDrawings()
    """ <-------- """
    # when new layer is added, blend into existing canvas
    if mrksMngr.addingTo:
        _tempImage = ImageChops.blend(config.blankLayer, config.blockLayer, mrksMngr.blendLevel)
        mrksMngr.blendLevel += mrksMngr.blendLevelRate
        if mrksMngr.blendLevel >= 1.0:
            mrksMngr.blendLevelRate = 0.0
            mrksMngr.blendLevel = 1.0
            mrksMngr.addingTo = False
            config.lineLayer.paste(_tempImage, (0, 0), _tempImage)
            # pieceLogger("POOF",4)
            mrksMngr.justHitPause = False
            # mrksMngr.canDraw = True
        else:
            config.lineLayer.paste(_tempImage, (0, 0), _tempImage)

    if not mrksMngr.debugMode:
        config.finalCompositeLayerDraw.rectangle((0, 0, mrksMngr.pictureWidth, mrksMngr.pictureHeight), fill=(mrksMngr.bgColor))
        if mrksMngr.textureBlendMode == "subtract":
            _tempImage = ImageChops.subtract(config.canvasImage, config.textureLayer)
            config.finalCompositeLayer.paste(_tempImage, (0, 0), _tempImage)
        else:
            config.finalCompositeLayer.paste(config.canvasImage, (0, 0), config.canvasImage)

    """ FOR DEBUGGING """
    # else:
    #     layerCompositing(config)

    if mrksMngr.transitionStateHandler.inTransition:
        mrksMngr.transitionStateHandler.transition()
        config.render(mrksMngr.transitionStateHandler.intermediateImage, 0, 0)
        # maybe_take_snapshot(mrksMngr.transitionStateHandler.intermediateImage)
    else:
        # pieceLogger("FINAL COMP RENDER",2)
        config.render(config.finalCompositeLayer, 0, 0)
        # maybe_take_snapshot(config.finalCompositeLayer)


""" FOR DEBUGGING """
# def layerCompositing(config):
#     config.finalCompositeLayerDraw.rectangle((0, 0, config.screenWidth, config.screenHeight), fill=(125, 125, 125))
#     config.finalCompositeLayerDraw.rectangle((0, 550, mrksMngr.pictureWidth, 550 + mrksMngr.pictureHeight), fill=(mrksMngr.bgColor))

#     config.finalCompositeLayer.paste(config.textureLayer, (0, 0), config.textureLayer)
#     config.finalCompositeLayer.paste(config.image, (280, 0), config.image)
#     config.finalCompositeLayer.paste(config.underLayer, (0, 280), config.underLayer)

#     config.finalCompositeLayerDraw.rectangle((280, 280, mrksMngr.pictureWidth + 280, 280 + mrksMngr.pictureHeight), fill=(mrksMngr.bgColor))
#     config.finalCompositeLayer.paste(config.canvasImage, (280, 280), config.canvasImage)


def clearCurrentDrawing():
    if not mrksMngr.transitionStateHandler.inTransition:
        initiateTransition()

        pieceLogger("Clearing", 2)
        mrksMngr.linesDrawnCount = 0
        mrksMngr.jitterIterations = 0

        config.underLayerDraw.rectangle((0, 0, mrksMngr.pictureWidth, mrksMngr.pictureHeight), fill=(mrksMngr.bgColor[0], mrksMngr.bgColor[1], mrksMngr.bgColor[2], 200))

        config.image = Image.new("RGBA", (mrksMngr.pictureWidth, mrksMngr.pictureHeight))
        config.draw = ImageDraw.Draw(config.image)

        config.underLayer = Image.new("RGBA", (mrksMngr.pictureWidth, mrksMngr.pictureHeight))
        config.underLayerDraw = ImageDraw.Draw(config.underLayer)

        config.blankLayer = Image.new("RGBA", (mrksMngr.pictureWidth, mrksMngr.pictureHeight))
        config.blankLayerDraw = ImageDraw.Draw(config.blankLayer)

        config.underLayer = Image.new("RGBA", (mrksMngr.pictureWidth, mrksMngr.pictureHeight))
        config.underLayerDraw = ImageDraw.Draw(config.underLayer)

        config.blockLayer = Image.new("RGBA", (mrksMngr.pictureWidth, mrksMngr.pictureHeight))
        config.blockLayerDraw = ImageDraw.Draw(config.blockLayer)

        config.lineLayer = Image.new("RGBA", (mrksMngr.pictureWidth, mrksMngr.pictureHeight))
        config.lineLayerDraw = ImageDraw.Draw(config.lineLayer)

        primeCanvas(2)
        config.canvasDraw.rectangle((0, 0, mrksMngr.pictureWidth, mrksMngr.pictureHeight), fill=(mrksMngr.bgColor[0], mrksMngr.bgColor[1], mrksMngr.bgColor[2], 225))
        mrksMngr.linesDrawnCount = 0


# ----------------------------------------------------##----------------------------------------------------#


def main(run=True):
    global config, workConfig, mrksMngr
    mrksMngr = MarksManager(config)
    mrksMngr.setUp(workConfig)

    # initiate
    global overlayControls
    overlayControls = BlanksAndDitherRemapping(config, workConfig, "drawingField")
    if run:
        runWork()


def _load_texture_values(_tName):
    tex = Texture()
    tex.name = _tName
    textureConfig = configparser.ConfigParser()
    textureConfig.read(f"{mrksMngr.assetPath}/textures/{_tName}.cfg")
    tex.useTextureLayer = textureConfig.getboolean("texture", "useTextureLayer", fallback=False)
    pieceLogger(f"{mrksMngr.assetPath}/textures/{_tName}.cfg {_tName} {tex.useTextureLayer}")
    tex.step = textureConfig.getint("texture", "texture_step", fallback=7)
    tex.px = textureConfig.getint("texture", "texture_px", fallback=2)
    tex.blockRows = textureConfig.getint("texture", "texture_blockRows", fallback=8)
    tex.blockCols = textureConfig.getint("texture", "texture_blockCols", fallback=8)
    tex.rows = textureConfig.getint("texture", "texture_rows", fallback=64)
    tex.cols = textureConfig.getint("texture", "texture_cols", fallback=32)
    tex.rate = textureConfig.getint("texture", "texture_rate", fallback=2)
    tex.base = textureConfig.getint("texture", "texture_base", fallback=125)
    tex.clr_r = textureConfig.getint("texture", "texture_clr_r", fallback=40)
    tex.clr_g = textureConfig.getint("texture", "texture_clr_g", fallback=40)
    tex.clr_b = textureConfig.getint("texture", "texture_clr_b", fallback=240)
    tex.skipProb = textureConfig.getfloat("texture", "texture_skipProb", fallback=0.7)
    tex.blur = textureConfig.getint("texture", "texture_blur", fallback=1)
    tex.xtick = textureConfig.getint("texture", "texture_xtick", fallback=0)
    tex.ytick = textureConfig.getint("texture", "texture_ytick", fallback=0)
    tex.drawMark = textureConfig.getfloat("texture", "texture_drawMark", fallback=0.9)
    tex.usedots = textureConfig.getboolean("texture", "texture_usedots", fallback=True)
    tex.blendMode = textureConfig.get("texture", "blendMode", fallback=None)
    return tex


def _load_single_pen(_penConfigName):
    _mark = Mark()
    _mark.name = f"{_penConfigName}".replace("\n", "")

    markConfig = configparser.ConfigParser()
    pathToCfg = f"{mrksMngr.assetPath}marks/{_mark.name}.cfg"
    pieceLogger(f"{pathToCfg}")
    markConfig.read(pathToCfg)

    _mark.turnsRange = list(map(lambda x: int(x), markConfig.get("markParams", "turnsRange", fallback="2,2").split(",")))

    if "scribble" in _mark.name:

        _mark.loopsMin = _mark.turnsRange[0]
        _mark.loopsMax = _mark.turnsRange[1]

        _mark.pointsPerLoop = int(markConfig.get("markParams", "pointsPerLoop"))
        _mark.noiseX = float(markConfig.get("markParams", "noiseX"))
        _mark.noiseY = float(markConfig.get("markParams", "noiseY"))

        _mark.height = float(markConfig.get("markParams", "height"))
        _mark.radiusX = float(markConfig.get("markParams", "radiusX"))
        _mark.radiusY = float(markConfig.get("markParams", "radiusY"))
        _mark.radiusXMin = float(markConfig.get("markParams", "radiusXMin"))
        _mark.radiusXMax = float(markConfig.get("markParams", "radiusXMax"))
        _mark.radiusYMin = float(markConfig.get("markParams", "radiusYMin"))
        _mark.radiusYMax = float(markConfig.get("markParams", "radiusYMax"))
        _mark.xRadiusDelta = float(markConfig.get("markParams", "xRadiusDelta"))
        _mark.yRadiusDelta = float(markConfig.get("markParams", "yRadiusDelta"))
        _mark.deltaRadiusXChangeProb = float(markConfig.get("markParams", "deltaRadiusXChangeProb"))
        _mark.deltaRadiusYChangeProb = float(markConfig.get("markParams", "deltaRadiusYChangeProb"))

        _mark.xCenter = float(markConfig.get("markParams", "xCenter"))
        _mark.yCenter = float(markConfig.get("markParams", "yCenter"))
        _mark.centerXDelta = float(markConfig.get("markParams", "centerXDelta"))
        _mark.centerYDelta = float(markConfig.get("markParams", "centerYDelta"))
        _mark.deltaRadiusXCenterChangeProb = float(markConfig.get("markParams", "deltaRadiusXCenterChangeProb"))
        _mark.deltaRadiusYCenterChangeProb = float(markConfig.get("markParams", "deltaRadiusYCenterChangeProb"))

    else:

        _mark.minNumPoints = int(markConfig.get("markParams", "minNumPoints", fallback=4))
        _mark.maxNumPoints = int(markConfig.get("markParams", "maxNumPoints", fallback=8))
        _mark.minInterpolatedPoints = int(markConfig.get("markParams", "minInterpolatedPoints", fallback=200))
        _mark.maxInterpolatedPoints = int(markConfig.get("markParams", "maxInterpolatedPoints", fallback=200))

        _mark.baseRadiusFactorRange = list(map(lambda x: float(x), markConfig.get("markParams", "baseRadiusFactorRange", fallback="1.0,1.0").split(",")))
        _mark.xRadiusFactorRange = list(map(lambda x: float(x), markConfig.get("markParams", "xRadiusFactorRange", fallback=".2,.2").split(",")))
        _mark.yRadiusFactorRange = list(map(lambda x: float(x), markConfig.get("markParams", "yRadiusFactorRange", fallback=".2,.2").split(",")))

        _mark.xRadiusFactorNoiseFactor = float(markConfig.get("markParams", "xRadiusFactorNoiseFactor", fallback=1.0))
        _mark.yRadiusFactorNoiseFactor = float(markConfig.get("markParams", "yRadiusFactorNoiseFactor", fallback=1.0))
        _mark.xRandomRange = list(map(lambda x: int(x), markConfig.get("markParams", "xRandomRange", fallback="-1,1").split(",")))
        _mark.yRandomRange = list(map(lambda x: int(x), markConfig.get("markParams", "yRandomRange", fallback="-1,1").split(",")))

        _mark.rotationFactor = float(markConfig.get("markParams", "rotationFactor", fallback=8.0))

        # adding parameters to enable geometric progression in x and y in addition to random arithmetic travel in x and y
        _mark.xTravelRange = list(map(lambda x: int(x), markConfig.get("markParams", "xTravelRange", fallback="-1,1").split(",")))
        _mark.yTravelRange = list(map(lambda x: int(x), markConfig.get("markParams", "yTravelRange", fallback="-1,1").split(",")))
        _mark.xTravelIncrRange = list(map(lambda x: float(x), markConfig.get("markParams", "xTravelIncrRange", fallback="-1,1").split(",")))
        _mark.yTravelIncrRange = list(map(lambda x: float(x), markConfig.get("markParams", "yTravelIncrRange", fallback="-1,1").split(",")))
        _mark.xtravelProb = float(markConfig.get("markParams", "xtravelProb", fallback=0.1))
        _mark.ytravelProb = float(markConfig.get("markParams", "ytravelProb", fallback=0.1))
        _mark.radiusChangePerRound = float(markConfig.get("markParams", "radiusChangePerRound", fallback="0"))

        _mark.linePoints = float(markConfig.get("markParams", "linePoints", fallback="20"))
        _mark.lopOff = float(markConfig.get("markParams", "lopOff", fallback="20"))

    _mark.xOffsetRange = markConfig.get("markParams", "xOffsetRange", fallback=None)
    _mark.incrementFactor = float(markConfig.get("markParams", "incrementFactor", fallback="1"))
    _mark.yOffsetRange = markConfig.get("markParams", "yOffsetRange", fallback=None)

    if _mark.xOffsetRange is not None:
        _mark.xOffsetRange = list(map(lambda x: int(x), markConfig.get("markParams", "xOffsetRange").split(",")))

    if _mark.yOffsetRange is not None:
        _mark.yOffsetRange = list(map(lambda x: int(x), markConfig.get("markParams", "yOffsetRange").split(",")))

    _mark.w = int(markConfig.get("markParams", "w", fallback=1))
    _mark.minMarkWidth = int(markConfig.get("markParams", "minMarkWidth", fallback=2))
    _mark.maxMarkWidth = int(markConfig.get("markParams", "maxMarkWidth", fallback=7))
    _mark.changeMarkWidthProb = float(markConfig.get("markParams", "changeMarkWidthProb", fallback=".02"))
    _mark.mode = int(markConfig.get("markParams", "mode", fallback=1))

    _mark.forceOrientation = markConfig.get("markParams", "forceOrientation", fallback="vertical")
    _mark.forcedPalette = markConfig.get("markParams", "forcedPalette", fallback=None)
    if _mark.forcedPalette is not None:
        _mark.forcedPalette = list(map(lambda x: float(x), markConfig.get("markParams", "forcedPalette", fallback=None).split(",")))

    _mark.angleDiffMax = float(markConfig.get("markParams", "angleDiffMax", fallback=180))
    _mark.drawingSkip = float(markConfig.get("markParams", "drawingSkip", fallback=0.01))

    _mark.drawLineAsEnvelope = markConfig.getboolean("markParams", "drawLineAsEnvelope", fallback=mrksMngr.drawLineAsEnvelope)

    return _mark


# ----------------------------------------------------##----------------------------------------------------#
# uncomment to silence logging

# def pieceLogger(*kwargs) :
#     return True
