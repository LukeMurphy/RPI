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


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


def transformImage(img):
    width, height = img.size
    m = -0.5
    xshift = abs(m) * 420
    new_width = width + int(round(xshift))

    img = img.transform((new_width, height), Image.AFFINE, (1, m, 0, 0, 1, 0), Image.BICUBIC)
    img = img.transform((new_width, height), Image.PERSPECTIVE, config.transformTuples, Image.BICUBIC)
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
    config.t1 = time.time()
    config.t2 = time.time()


def _update_color_ranges():
    if config.usePresets:
        if config.quiltPattern == "stars":
            _update_stars_color_ranges()
        else:
            _update_triangles_color_ranges()
    # No else needed, commented out code is unused

    config.fillColorSet = [
        ColorSet(config.c1HueRange, config.c1SaturationRange, config.c1ValueRange),
        ColorSet(config.c2HueRange, config.c2SaturationRange, config.c2ValueRange),
        ColorSet(config.c3HueRange, config.c3SaturationRange, config.c3ValueRange),
    ]


def _update_stars_color_ranges():
    newHueRange = randomRange(360, True)
    # stars: CENTER SQUARE
    config.c3HueRange = newHueRange
    config.c3ValueRange = randomRange()
    if random.SystemRandom().random() < 0.25:
        choice = round(random.SystemRandom().uniform(1, 3))
        if choice == 1:
            # yellow centers
            config.c3HueRange = (30, 60)
        elif choice == 2:
            # red centers
            config.c3HueRange = (0, 30)
        else:
            # all colors
            config.c3HueRange = (0, 360)
        config.c3ValueRange = (0.4, 1)
        config.c3SaturationRange = (0.6, 1)


def _update_triangles_color_ranges():
    # triangles: major outline squares and diamonds
    newHueRange = (0, 360)
    newSaturationRange = randomRange(0.2, 1)
    newValueRange = randomRange(0.2, 1)

    config.c1HueRange = newHueRange
    config.c1SaturationRange = newSaturationRange
    config.c1ValueRange = newValueRange

    # triangles: wings of the 8-point inner starts
    newHueRange = randomRange(360, True)
    newSaturationRange = randomRange()
    newValueRange = randomRange()

    config.c2HueRange = newHueRange
    config.c2SaturationRange = newSaturationRange
    config.c2ValueRange = newValueRange

    # triangles: the star center diamond
    if random.SystemRandom().random() < 0.5:
        newHueRange = randomRange(360, True)
    newSaturationRange = randomRange()
    newValueRange = randomRange()

    config.c3HueRange = newHueRange
    config.c3SaturationRange = newSaturationRange
    config.c2ValueRange = newValueRange  # This looks like a possible bug, should this be c3?


def _resize_and_refresh_pieces():
    if random.SystemRandom().random() >= config.resetSizeProbability:
        return
    if config.quiltPattern == "stars":
        _extracted_from__resize_and_refresh_pieces_4(11, createstarpieces)
    else:
        _extracted_from__resize_and_refresh_pieces_4(16, createtrianglepieces)
    config.blockLength = config.blockSize
    config.blockHeight = config.blockSize
    config.doingRefresh = 0
    config.doingRefreshCount = 100


# TODO Rename this here and in `_resize_and_refresh_pieces`
def _extracted_from__resize_and_refresh_pieces_4(arg0, arg1):
    config.blockSize = round(random.SystemRandom().uniform(config.blockSizeMin, config.blockSizeMax))
    large = config.blockSize >= arg0
    config.blockCols = config.blockColsMin if large else config.blockColsMax
    config.blockRows = config.blockRowsMin if large else config.blockRowsMax
    arg1.createPieces(config, large)


def _refresh_palette():
    if config.quiltPattern == "stars":
        createstarpieces.refreshPalette(config)
    else:
        createtrianglepieces.refreshPalette(config)
        setInitialColors(True)


def _update_rotation():
    if random.SystemRandom().random() < 0.5:
        config.rotation = random.SystemRandom().uniform(-config.rotationRange, config.rotationRange)


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
    global config, directionOrder, workConfig
    print("---------------------")
    print("QUILT TRIANGLES or STARS Loaded")

    ########################################################################
    # CREATE THE IMAGE HOLDERS
    # canvasImage will get the drawing
    # disturbanceImage will get the disturbance / glitching
    # image will be the final output

    config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.canvasDraw = ImageDraw.Draw(config.canvasImage)
    config.disturbanceImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))

    config.directorController = Director(config)
    config.redrawSpeed = float(workConfig.get("quilt-triangles", "redrawSpeed"))
    config.directorController.slotRate = float(workConfig.get("quilt-triangles", "slotRate"))

    config.brightness = float(workConfig.get("displayconfig", "brightness"))
    colorutils.brightness = config.brightness
    config.canvasImageWidth = config.screenWidth
    config.canvasImageHeight = config.screenHeight
    config.canvasImageWidth -= 4
    config.canvasImageHeight -= 4

    config.outlineColorObj = coloroverlay.ColorOverlay()
    config.outlineColorObj.randomRange = (5.0, 30.0)
    config.outlineColorObj.colorTransitionSetup()

    config.quiltPattern = workConfig.get("quilt-triangles", "pattern")

    # these control the timing of the individual color transitions - longer is slower
    config.transitionStepsMin = float(workConfig.get("quilt-triangles", "transitionStepsMin"))
    config.transitionStepsMax = float(workConfig.get("quilt-triangles", "transitionStepsMax"))

    try:
        # Some triangles will re-draw like a tick - on triangles quilt
        config.resetTrianglesProb = float(workConfig.get("quilt-triangles", "resetTrianglesProb"))
        # The probability that at the beginning of a new quilt image the size of the
        # elements will change
        config.resetSizeProbability = float(workConfig.get("quilt-triangles", "resetSizeProbability"))
    except Exception as e:
        print(e)
        config.resetTrianglesProb = 0.001
        config.resetSizeProbability = 0.001

    # the time in seconds given before the quilt image resets to new parameters
    config.timeToComplete = int(workConfig.get("quilt-triangles", "timeToComplete"))

    try:
        config.transformShape = workConfig.getboolean("quilt-triangles", "transformShape")
        transformTuples = workConfig.get("quilt-triangles", "transformTuples").split(",")
        config.transformTuples = tuple(float(i) for i in transformTuples)

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
        config.transformShape = False

    redRange = workConfig.get("quilt-triangles", "redRange").split(",")
    config.redRange = tuple(int(i) for i in redRange)

    try:
        # the mins and maxes for the size of the units
        config.gapSize = int(workConfig.get("quilt-triangles", "gapSize"))
        config.blockSizeMin = int(workConfig.get("quilt-triangles", "blockSizeMin"))
        config.blockSizeMax = int(workConfig.get("quilt-triangles", "blockSizeMax"))
        config.blockSize = round(random.SystemRandom().uniform(config.blockSizeMin, config.blockSizeMax))
    except Exception as e:
        print(e)
        config.blockSize = int(workConfig.get("quilt-triangles", "blockSize"))

    try:
        _blockRowConfigs(workConfig, config)
    except Exception as e:
        print(e)
        config.blockCols = int(workConfig.get("quilt-triangles", "blockCols"))
        config.blockRows = int(workConfig.get("quilt-triangles", "blockRows"))
    # can adjust the quilt image offset
    config.cntrOffsetX = int(workConfig.get("quilt-triangles", "cntrOffsetX"))
    config.cntrOffsetY = int(workConfig.get("quilt-triangles", "cntrOffsetY"))

    # frame rate
    config.delay = float(workConfig.get("quilt-triangles", "delay"))

    # the probabilty that any triangle will pop to another color
    config.colorPopProb = float(workConfig.get("quilt-triangles", "colorPopProb"))

    config.brightnessFactorDark = float(workConfig.get("quilt-triangles", "brightnessFactorDark"))
    config.brightnessFactorLight = float(workConfig.get("quilt-triangles", "brightnessFactorLight"))
    config.lines = workConfig.getboolean("quilt-triangles", "lines")
    config.patternPrecision = workConfig.getboolean("quilt-triangles", "patternPrecision")

    config.activeSet = workConfig.get("quilt-triangles", "activeSet")

    config.c1HueRange = tuple(
        float(i)
        for i in workConfig.get(config.activeSet, "c1HueRange").split(",")
    )
    config.c1SaturationRange = tuple(float(i) for i in workConfig.get(config.activeSet, "c1SaturationRange").split(","))
    config.c1ValueRange = tuple(float(i) for i in workConfig.get(config.activeSet, "c1ValueRange").split(","))

    config.c2HueRange = tuple(float(i) for i in workConfig.get(config.activeSet, "c2HueRange").split(","))
    config.c2SaturationRange = tuple(float(i) for i in workConfig.get(config.activeSet, "c2SaturationRange").split(","))
    config.c2ValueRange = tuple(float(i) for i in workConfig.get(config.activeSet, "c2ValueRange").split(","))

    config.c3HueRange = tuple(float(i) for i in workConfig.get(config.activeSet, "c3HueRange").split(","))
    config.c3SaturationRange = tuple(float(i) for i in workConfig.get(config.activeSet, "c3SaturationRange").split(","))
    config.c3ValueRange = tuple(float(i) for i in workConfig.get(config.activeSet, "c3ValueRange").split(","))

    # for now, all squares
    config.blockLength = config.blockSize
    config.blockHeight = config.blockSize

    # config.canvasImage = Image.new(
    # 	"RGBA", (config.canvasImageWidth, config.canvasImageHeight)
    # )

    config.fillColorSet = []
    config.fillColorSet.append(ColorSet(config.c1HueRange, config.c1SaturationRange, config.c1ValueRange))
    config.fillColorSet.append(ColorSet(config.c2HueRange, config.c2SaturationRange, config.c2ValueRange))
    config.fillColorSet.append(ColorSet(config.c3HueRange, config.c3SaturationRange, config.c3ValueRange))

    # ------------------------------------------------------------------ #
    # BUILDS THE QUILT PATTERN FROM COMMON MODULES
    # ------------------------------------------------------------------ #

    config.unitArray = []
    if config.quiltPattern == "triangles":
        createtrianglepieces.createPieces(config)
    elif config.quiltPattern == "stars":
        createstarpieces.createPieces(config)

    try:
        config.usePresets = workConfig.getboolean("quilt-triangles", "usePresets")
    except Exception as e:
        print(e)
        config.usePresets = True

    try:
        config.rotationRange = float(workConfig.get("quilt-triangles", "rotationRange"))
    except Exception as e:
        config.rotationRange = 0
        print(e)

    try:
        _extracted_from_main_166(workConfig, config)
    except Exception as e:
        print(e)
        config.drawBlock = False
        config.drawBlockShape = lambda: True

    setInitialColors()

    config.t1 = time.time()
    config.t2 = time.time()

    config.doingRefresh = 100
    config.doingRefreshCount = 100

    distortions.distortionsConfigs(config, workConfig)

    if run:
        runWork()


# TODO Rename this here and in `main`
def _extracted_from_main_166(workConfig, config):
    drawBlockCoordsRaw = [
        list((i).split(","))
        for i in workConfig.get("drawBlock", "drawBlockCoords").split("|")
    ]
    config.drawBlockCoords = []
    config.drawBlockCoords.extend(
        tuple(int(ii) for ii in i) for i in drawBlockCoordsRaw
    )
    config.drawBlockCoords = tuple(config.drawBlockCoords)

    config.drawBlockFixedColor = tuple(int(i) for i in workConfig.get("drawBlock", "drawBlockFixedColor").split(","))
    config.drawBlock_c1HueRange = tuple(float(i) for i in workConfig.get("drawBlock", "c1HueRange").split(","))
    config.drawBlock_c1SaturationRange = tuple(float(i) for i in workConfig.get("drawBlock", "c1SaturationRange").split(","))
    config.drawBlock_c1ValueRange = tuple(float(i) for i in workConfig.get("drawBlock", "c1ValueRange").split(","))

    config.canvasImageDraw = ImageDraw.Draw(config.image)

    config.drawBlock = True
    config.drawBlockShape = lambda: config.canvasImageDraw.polygon(config.drawBlockCoords, fill=config.drawBlockFixedColor)


# TODO Rename this here and in `main`
def _blockRowConfigs(workConfig, config):
    config.blockRowsMin = int(workConfig.get("quilt-triangles", "blockRowsMin"))
    config.blockRowsMax = int(workConfig.get("quilt-triangles", "blockRowsMax"))
    config.blockColsMin = int(workConfig.get("quilt-triangles", "blockColsMin"))
    config.blockColsMax = int(workConfig.get("quilt-triangles", "blockColsMax"))
    config.blockCols = config.blockColsMax
    config.blockRows = config.blockRowsMax


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
    # if config.doingRefresh < config.doingRefreshCount:
    #     # print("crossfade...",  config.doingRefresh/config.doingRefreshCount)
    #     if config.doingRefresh == 0:
    #         config.snapShot = config.canvasImage.copy()
    #     crossFade = Image.blend(
    #         config.snapShot,
    #         config.canvasImage,
    #         config.doingRefresh / config.doingRefreshCount,
    #     )
    #     config.drawBlockShape()
    #     config.render(crossFade, 0, 0)
    #     config.doingRefresh += 1
    # else:
    #     temp = Image.new("RGBA", (config.canvasImageWidth, config.canvasImageHeight))
    #     temp.paste(config.canvasImage, (0, 0), config.canvasImage)
    #     if config.transformShape == True:
    #         temp = transformImage(temp)
    #     config.drawBlockShape()
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

    if config.transformShape == True:
        temp1 = transformImage(temp1)

    if config.useWaveDistortion == True:
        temp1 = ImageOps.deform(temp1, distortions.WaveDeformer(config))
        config.waveDeformXPos += config.waveDeformXPosRate
        if config.waveDeformXPos > config.screenWidth:
            config.waveDeformXPos = 0

    config.render(temp1, config.imgcanvasOffsetX, config.imgcanvasOffsetY, config.canvasWidth, config.canvasHeight)
    # Done

    config.t2 = time.time()
    delta = config.t2 - config.t1

    if delta > config.timeToComplete:
        if config.sectionDisturbance == True:
            # these functions are run to restart disturber
            distortions.resetFunction(config)
        restartPiece()


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
