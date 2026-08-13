import math
import random
import textwrap
import time
import noise
from noise import *
from modules.configuration import bcolors
from modules import badpixels, coloroverlay, colorutils
from modules.quilting import createstarpieces, createtrianglepieces
from modules.quilting.colorset import ColorSet
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFont, ImageOps
from modules.holder_director import Holder
from modules.holder_director import Director
from modules import distortions


# ------------------------------------------------------------------ #

class QuiltManager:
    def __init__(self, config):
        self.config = config

    def setUp(self, workConfig):
        self.canvasImageWidth = self.config.screenWidth
        self.canvasImageHeight = self.config.screenHeight
        self.canvasImageWidth -= 4
        self.canvasImageHeight -= 4

        self.outlineColorObj = coloroverlay.ColorOverlay()
        self.outlineColorObj.randomRange = (5.0, 30.0)
        self.outlineColorObj.colorTransitionSetup()

        self.quiltPattern = workConfig.get("quilt-triangles", "pattern")

        # these control the timing of the individual color transitions - longer is slower
        self.transitionStepsMin = float(workConfig.get("quilt-triangles", "transitionStepsMin"))
        self.transitionStepsMax = float(workConfig.get("quilt-triangles", "transitionStepsMax"))

        try:
            # Some triangles will re-draw like a tick - on triangles quilt
            self.resetTrianglesProb = float(workConfig.get("quilt-triangles", "resetTrianglesProb"))
            # The probability that at the beginning of a new quilt image the size of the
            # elements will change
            self.resetSizeProbability = float(workConfig.get("quilt-triangles", "resetSizeProbability"))
        except Exception as e:
            print(e)
            self.resetTrianglesProb = 0.001
            self.resetSizeProbability = 0.001

        # the time in seconds given before the quilt image resets to new parameters
        self.timeToComplete = int(workConfig.get("quilt-triangles", "timeToComplete"))

        try:
            self.transformShape = workConfig.getboolean("quilt-triangles", "transformShape")
            transformTuples = workConfig.get("quilt-triangles", "transformTuples").split(",")
            self.transformTuples = tuple(float(i) for i in transformTuples)

            """
            e.g.
            #transformTuples_ = .9, 0, 0, -0.05,  .6, 0, -0.001, 0
            #transformTuples__ = 1.2, .5, 0, 0.081,  1, 0, 0.0009, 0.0

            #transformTuples = 1.2, .5, 0, 0.071,  1, 0, 0.0005, 0.0
            ## No transform
            transformTuples = 1, .5, 0, 0.0,  1, 0, 0.0, 0.0

            #transformTuples = 1, 0, 0, 0.0,  1, 0, 0, 0.0
            #transformTuples = 0, 0, 0, 0,  0, 0, 0, 0.0
            """

        except Exception as e:
            print(e)
            self.transformShape = False

        redRange = workConfig.get("quilt-triangles", "redRange").split(",")
        self.redRange = tuple(int(i) for i in redRange)

        try:
            # the mins and maxes for the size of the units
            self.gapSize = int(workConfig.get("quilt-triangles", "gapSize"))
            self.blockSizeMin = int(workConfig.get("quilt-triangles", "blockSizeMin"))
            self.blockSizeMax = int(workConfig.get("quilt-triangles", "blockSizeMax"))
            self.blockSize = round(random.SystemRandom().uniform(self.blockSizeMin, self.blockSizeMax))
        except Exception as e:
            print(e)
            self.blockSize = int(workConfig.get("quilt-triangles", "blockSize"))

        try:
            self.blockRowsMin = int(workConfig.get("quilt-triangles", "blockRowsMin"))
            self.blockRowsMax = int(workConfig.get("quilt-triangles", "blockRowsMax"))
            self.blockColsMin = int(workConfig.get("quilt-triangles", "blockColsMin"))
            self.blockColsMax = int(workConfig.get("quilt-triangles", "blockColsMax"))
            self.blockCols = self.blockColsMax
            self.blockRows = self.blockRowsMax
        except Exception as e:
            print(e)
            self.blockCols = int(workConfig.get("quilt-triangles", "blockCols"))
            self.blockRows = int(workConfig.get("quilt-triangles", "blockRows"))
        # can adjust the quilt image offset
        self.cntrOffsetX = int(workConfig.get("quilt-triangles", "cntrOffsetX"))
        self.cntrOffsetY = int(workConfig.get("quilt-triangles", "cntrOffsetY"))

        # frame rate
        self.delay = float(workConfig.get("quilt-triangles", "delay"))

        # the probabilty that any triangle will pop to another color
        self.colorPopProb = float(workConfig.get("quilt-triangles", "colorPopProb"))

        self.brightnessFactorDark = float(workConfig.get("quilt-triangles", "brightnessFactorDark"))
        self.brightnessFactorLight = float(workConfig.get("quilt-triangles", "brightnessFactorLight"))
        self.lines = workConfig.getboolean("quilt-triangles", "lines")
        self.patternPrecision = workConfig.getboolean("quilt-triangles", "patternPrecision")

        self.activeSet = workConfig.get("quilt-triangles", "activeSet")

        self.c1HueRange = tuple(
            float(i)
            for i in workConfig.get(self.activeSet, "c1HueRange").split(",")
        )
        self.c1SaturationRange = tuple(float(i) for i in workConfig.get(self.activeSet, "c1SaturationRange").split(","))
        self.c1ValueRange = tuple(float(i) for i in workConfig.get(self.activeSet, "c1ValueRange").split(","))

        self.c2HueRange = tuple(float(i) for i in workConfig.get(self.activeSet, "c2HueRange").split(","))
        self.c2SaturationRange = tuple(float(i) for i in workConfig.get(self.activeSet, "c2SaturationRange").split(","))
        self.c2ValueRange = tuple(float(i) for i in workConfig.get(self.activeSet, "c2ValueRange").split(","))

        self.c3HueRange = tuple(float(i) for i in workConfig.get(self.activeSet, "c3HueRange").split(","))
        self.c3SaturationRange = tuple(float(i) for i in workConfig.get(self.activeSet, "c3SaturationRange").split(","))
        self.c3ValueRange = tuple(float(i) for i in workConfig.get(self.activeSet, "c3ValueRange").split(","))

        # for now, all squares
        self.blockLength = self.blockSize
        self.blockHeight = self.blockSize

        self.fillColorSet = []
        self.fillColorSet.append(ColorSet(self.c1HueRange, self.c1SaturationRange, self.c1ValueRange))
        self.fillColorSet.append(ColorSet(self.c2HueRange, self.c2SaturationRange, self.c2ValueRange))
        self.fillColorSet.append(ColorSet(self.c3HueRange, self.c3SaturationRange, self.c3ValueRange))

        # ------------------------------------------------------------------ #
        # the values above are read directly off config by the shared quilting
        # modules (createtrianglepieces/createstarpieces + their Unit classes)
        # and by runWork(), so mirror them onto config before those run
        # @todo change this so they are not shared via the config - maybe quiltConfig 
        # or something like that
        # ------------------------------------------------------------------ #
        self.config.outlineColorObj = self.outlineColorObj
        self.config.transitionStepsMin = self.transitionStepsMin
        self.config.transitionStepsMax = self.transitionStepsMax
        self.config.resetTrianglesProb = self.resetTrianglesProb
        self.config.gapSize = self.gapSize
        self.config.blockCols = self.blockCols
        self.config.blockRows = self.blockRows
        self.config.cntrOffsetX = self.cntrOffsetX
        self.config.cntrOffsetY = self.cntrOffsetY
        self.config.delay = self.delay
        self.config.colorPopProb = self.colorPopProb
        self.config.brightnessFactorDark = self.brightnessFactorDark
        self.config.brightnessFactorLight = self.brightnessFactorLight
        self.config.lines = self.lines
        self.config.patternPrecision = self.patternPrecision
        self.config.blockLength = self.blockLength
        self.config.blockHeight = self.blockHeight
        self.config.fillColorSet = self.fillColorSet

        # ------------------------------------------------------------------ #
        # BUILDS THE QUILT PATTERN FROM COMMON MODULES
        # ------------------------------------------------------------------ #

        self.config.unitArray = []
        if self.quiltPattern == "triangles":
            createtrianglepieces.createPieces(self.config)
        elif self.quiltPattern == "stars":
            createstarpieces.createPieces(self.config)

        try:
            self.usePresets = workConfig.getboolean("quilt-triangles", "usePresets")
        except Exception as e:
            print(e)
            self.usePresets = True

        try:
            self.rotationRange = float(workConfig.get("quilt-triangles", "rotationRange"))
        except Exception as e:
            self.rotationRange = 0
            print(e)

        try:
            drawBlockCoordsRaw = [
                list((i).split(","))
                for i in workConfig.get("drawBlock", "drawBlockCoords").split("|")
            ]
            self.drawBlockCoords = []
            self.drawBlockCoords.extend(
                tuple(int(ii) for ii in i) for i in drawBlockCoordsRaw
            )
            self.drawBlockCoords = tuple(self.drawBlockCoords)

            self.drawBlockFixedColor = tuple(int(i) for i in workConfig.get("drawBlock", "drawBlockFixedColor").split(","))
            self.drawBlock_c1HueRange = tuple(float(i) for i in workConfig.get("drawBlock", "c1HueRange").split(","))
            self.drawBlock_c1SaturationRange = tuple(float(i) for i in workConfig.get("drawBlock", "c1SaturationRange").split(","))
            self.drawBlock_c1ValueRange = tuple(float(i) for i in workConfig.get("drawBlock", "c1ValueRange").split(","))

            self.canvasImageDraw = ImageDraw.Draw(self.config.image)

            self.drawBlock = True
            self.drawBlockShape = lambda: self.canvasImageDraw.polygon(self.drawBlockCoords, fill=self.drawBlockFixedColor)
        except Exception as e:
            print(e)
            self.drawBlock = False
            self.drawBlockShape = lambda: True

        setInitialColors()

        self.t1 = time.time()
        self.t2 = time.time()

        self.doingRefresh = 100
        self.doingRefreshCount = 100

        distortions.distortionsConfigs(self.config, workConfig)

def transformImage(img):
    width, height = img.size
    m = -0.5
    xshift = abs(m) * 420
    new_width = width + int(round(xshift))

    img = img.transform((new_width, height), Image.AFFINE, (1, m, 0, 0, 1, 0), Image.BICUBIC)
    img = img.transform((new_width, height), Image.PERSPECTIVE, mrksMngr.transformTuples, Image.BICUBIC)
    return img


# this could be written to use A as the starting point
# for b's range - but this way it makes for some more
# mixed up results
def randomRange(A=0, B=1, rounding=False):
    a = random.SystemRandom().uniform(A, B)
    b = random.SystemRandom().uniform(A, B)
    return (a, b) if rounding == False else (round(a), round(b))


def restartPiece():
    _reset_timers()
    _update_color_ranges()
    _resize_and_refresh_pieces()
    _refresh_palette()
    _update_rotation()


def _reset_timers():
    mrksMngr.t1 = time.time()
    mrksMngr.t2 = time.time()


def _update_color_ranges():
    if mrksMngr.usePresets:
        if mrksMngr.quiltPattern == "stars":
            _update_stars_color_ranges()
        else:
            _update_triangles_color_ranges()
    # No else needed, commented out code is unused

    config.fillColorSet = [
        ColorSet(mrksMngr.c1HueRange, mrksMngr.c1SaturationRange, mrksMngr.c1ValueRange),
        ColorSet(mrksMngr.c2HueRange, mrksMngr.c2SaturationRange, mrksMngr.c2ValueRange),
        ColorSet(mrksMngr.c3HueRange, mrksMngr.c3SaturationRange, mrksMngr.c3ValueRange),
    ]


def _update_stars_color_ranges():
    newHueRange = randomRange(360, True)
    # stars: CENTER SQUARE
    mrksMngr.c3HueRange = newHueRange
    mrksMngr.c3ValueRange = randomRange()
    if random.SystemRandom().random() < 0.25:
        choice = round(random.SystemRandom().uniform(1, 3))
        if choice == 1:
            # yellow centers
            mrksMngr.c3HueRange = (30, 60)
        elif choice == 2:
            # red centers
            mrksMngr.c3HueRange = (0, 30)
        else:
            # all colors
            mrksMngr.c3HueRange = (0, 360)
        mrksMngr.c3ValueRange = (0.4, 1)
        mrksMngr.c3SaturationRange = (0.6, 1)


def _update_triangles_color_ranges():
    # triangles: major outline squares and diamonds
    newHueRange = (0, 360)
    newSaturationRange = randomRange(0.2, 1)
    newValueRange = randomRange(0.2, 1)

    mrksMngr.c1HueRange = newHueRange
    mrksMngr.c1SaturationRange = newSaturationRange
    mrksMngr.c1ValueRange = newValueRange

    # triangles: wings of the 8-point inner starts
    newHueRange = randomRange(360, True)
    newSaturationRange = randomRange()
    newValueRange = randomRange()

    mrksMngr.c2HueRange = newHueRange
    mrksMngr.c2SaturationRange = newSaturationRange
    mrksMngr.c2ValueRange = newValueRange

    # triangles: the star center diamond
    if random.SystemRandom().random() < 0.5:
        newHueRange = randomRange(360, True)
    newSaturationRange = randomRange()
    newValueRange = randomRange()

    mrksMngr.c3HueRange = newHueRange
    mrksMngr.c3SaturationRange = newSaturationRange
    mrksMngr.c2ValueRange = newValueRange  # This looks like a possible bug, should this be c3?


def _resize_and_refresh_pieces():
    if random.SystemRandom().random() >= mrksMngr.resetSizeProbability:
        return
    if mrksMngr.quiltPattern == "stars":
        _extracted_from__resize_and_refresh_pieces_4(11, createstarpieces)
    else:
        _extracted_from__resize_and_refresh_pieces_4(16, createtrianglepieces)
    config.blockLength = mrksMngr.blockSize
    config.blockHeight = mrksMngr.blockSize
    mrksMngr.doingRefresh = 0
    mrksMngr.doingRefreshCount = 100


# TODO Rename this here and in `_resize_and_refresh_pieces`
def _extracted_from__resize_and_refresh_pieces_4(arg0, arg1):
    mrksMngr.blockSize = round(random.SystemRandom().uniform(mrksMngr.blockSizeMin, mrksMngr.blockSizeMax))
    large = mrksMngr.blockSize >= arg0
    config.blockCols = mrksMngr.blockColsMin if large else mrksMngr.blockColsMax
    config.blockRows = mrksMngr.blockRowsMin if large else mrksMngr.blockRowsMax
    arg1.createPieces(config, large)


def _refresh_palette():
    if mrksMngr.quiltPattern == "stars":
        createstarpieces.refreshPalette(config)
    else:
        createtrianglepieces.refreshPalette(config)
        setInitialColors(True)


def _update_rotation():
    if random.SystemRandom().random() < 0.5:
        mrksMngr.rotation = random.SystemRandom().uniform(-mrksMngr.rotationRange, mrksMngr.rotationRange)


def setInitialColors(refresh=False):
    ## Better initial color when piece is turned on

    for i in range(len(config.unitArray)):
        obj = config.unitArray[i]
        # print("number of colorOverlay objs {}".format(len(obj.triangles)) )
        for c in range(len(obj.triangles)):
            colOverlay = obj.triangles[c][1]
            # colOverlay.colorB = colorutils.randomColorAlpha(config.brightness * .8,0)
            colOverlay.colorA = colorutils.randomColorAlpha(config.brightness * 0.8, 0)
            colOverlay.colorTransitionSetup()
            colOverlay.colorTransitionSetupValues()


def main(run=True):
    global config, directionOrder, workConfig, mrksMngr
    print("---------------------")
    print("QUILT TRIANGLES or STARS Loaded")

    # ------------------------------------------------------------------ #
    # CREATE THE IMAGE HOLDERS
    # canvasImage will get the drawing
    # disturbanceImage will get the disturbance / glitching
    # image will be the final output
    # ------------------------------------------------------------------ #

    config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.canvasDraw = ImageDraw.Draw(config.canvasImage)
    config.disturbanceImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))

    config.directorController = Director(config)
    config.redrawSpeed = float(workConfig.get("quilt-triangles", "redrawSpeed"))
    config.directorController.slotRate = float(workConfig.get("quilt-triangles", "slotRate"))

    config.brightness = float(workConfig.get("displayconfig", "brightness"))
    colorutils.brightness = config.brightness

    mrksMngr = QuiltManager(config)
    mrksMngr.setUp(workConfig)

    if run:
        runWork()


def runWork():
    global config
    print(f"{bcolors.OKGREEN}** {bcolors.BOLD}")
    print("RUNNING quilt-triangles.py")
    print(bcolors.ENDC)
    while config.isRunning == True:
        iterate()
        time.sleep(config.delay)
        if config.standAlone == False:
            config.callBack()


def iterate():
    global config
    config.outlineColorObj.stepTransition()

    # Need to do a crossfade
    # if mrksMngr.doingRefresh < mrksMngr.doingRefreshCount:
    #     # print("crossfade...",  mrksMngr.doingRefresh/mrksMngr.doingRefreshCount)
    #     if mrksMngr.doingRefresh == 0:
    #         mrksMngr.snapShot = config.canvasImage.copy()
    #     crossFade = Image.blend(
    #         mrksMngr.snapShot,
    #         config.canvasImage,
    #         mrksMngr.doingRefresh / mrksMngr.doingRefreshCount,
    #     )
    #     mrksMngr.drawBlockShape()
    #     config.render(crossFade, 0, 0)
    #     mrksMngr.doingRefresh += 1
    # else:
    #     temp = Image.new("RGBA", (mrksMngr.canvasImageWidth, mrksMngr.canvasImageHeight))
    #     temp.paste(config.canvasImage, (0, 0), config.canvasImage)
    #     if mrksMngr.transformShape == True:
    #         temp = transformImage(temp)
    #     mrksMngr.drawBlockShape()
    #     config.render(temp, 0, 0)

    for i in range(len(config.unitArray)):
        obj = config.unitArray[i]
        obj.update()
        obj.render()

    if config.sectionDisturbance == True:
        distortions.iterationFunction(config)

    # previous non-disturbing iteration just rendered the temp image
    # config.render(temp, 0, 0)

    temp1 = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    temp1Draw = ImageDraw.Draw(temp1)

    config.image.paste(config.canvasImage, (0, 0), config.canvasImage)
    temp1.paste(config.image, (0, 0), config.image)

    if mrksMngr.transformShape == True:
        temp1 = transformImage(temp1)

    if config.useWaveDistortion == True:
        temp1 = ImageOps.deform(temp1, distortions.WaveDeformer(config))
        config.waveDeformXPos += config.waveDeformXPosRate
        if config.waveDeformXPos > config.screenWidth:
            config.waveDeformXPos = 0

    config.render(temp1, config.imgcanvasOffsetX, config.imgcanvasOffsetY, config.canvasWidth, config.canvasHeight)
    # Done

    mrksMngr.t2 = time.time()
    delta = mrksMngr.t2 - mrksMngr.t1

    if delta > mrksMngr.timeToComplete:
        if config.sectionDisturbance == True:
            # these functions are run to restart disturber
            distortions.resetFunction(config)
        restartPiece()