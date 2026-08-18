import random
import time
from modules.configuration import bcolors, pieceLogger
from modules import coloroverlay, colorutils
from modules.quilting import (
    createpolypieces,
)
from modules.quilting.colorset import ColorSet
from PIL import Image, ImageDraw, ImageOps
from modules.holder_director import Director
from modules import distortions

## This quilt supercedes the quilt.py module because it accounts for a zero irregularity
## as well as the infomal bar construction


# ------------------------------------------------------------------ #

class QuiltManager:
    def __init__(self, config):
        self.config = config

    def setUp(self, workConfig):
        self.canvasImageWidth = self.config.screenWidth
        self.canvasImageHeight = self.config.screenHeight
        self.canvasImageWidth -= 4
        self.canvasImageHeight -= 4

        self.config.outlineColorObj = coloroverlay.ColorOverlay()
        self.config.outlineColorObj.randomRange = (5.0, 30.0)
        self.config.outlineColorObj.colorTransitionSetup()

        self.quiltPattern = workConfig.get("quilt-polys", "pattern")

        # these control the timing of the individual color transitions - longer is slower
        self.config.transitionStepsMin = float(workConfig.get("quilt-polys", "transitionStepsMin"))
        self.config.transitionStepsMax = float(workConfig.get("quilt-polys", "transitionStepsMax"))

        # Some triangles will re-draw like a tick - on triangles quilt
        self.resetTrianglesProb = float(workConfig.get("quilt-polys", "resetTrianglesProb"))

        # The probability that at the beginning of a new quilt image the size of the
        # elements will change
        self.resetSizeProbability = float(workConfig.get("quilt-polys", "resetSizeProbability"))

        # the time in seconds given before the quilt image resets to new parameters
        self.timeToComplete = int(workConfig.get("quilt-polys", "timeToComplete"))

        self.transformShape = workConfig.getboolean("quilt-polys", "transformShape")
        transformTuples = workConfig.get("quilt-polys", "transformTuples").split(",")
        self.transformTuples = tuple(float(i) for i in transformTuples)

        redRange = workConfig.get("quilt-polys", "redRange").split(",")
        self.redRange = tuple(int(i) for i in redRange)

        # the mins and maxes for the size of the units
        self.config.gapSize = int(workConfig.get("quilt-polys", "gapSize"))
        self.blockSizeMin = int(workConfig.get("quilt-polys", "blockSizeMin"))
        self.blockSizeMax = int(workConfig.get("quilt-polys", "blockSizeMax"))
        self.blockSize = round(random.SystemRandom().uniform(self.blockSizeMin, self.blockSizeMax))

        self.blockRowsMin = int(workConfig.get("quilt-polys", "blockRowsMin"))
        self.blockRowsMax = int(workConfig.get("quilt-polys", "blockRowsMax"))
        self.blockColsMin = int(workConfig.get("quilt-polys", "blockColsMin"))
        self.blockColsMax = int(workConfig.get("quilt-polys", "blockColsMax"))
        self.config.blockCols = self.blockColsMax
        self.config.blockRows = self.blockRowsMax

        # can adjust the quilt image offset
        self.config.cntrOffsetX = int(workConfig.get("quilt-polys", "cntrOffsetX"))
        self.config.cntrOffsetY = int(workConfig.get("quilt-polys", "cntrOffsetY"))

        # frame rate
        self.config.delay = float(workConfig.get("quilt-polys", "delay"))

        # the probabilty that any triangle will pop to another color
        self.config.colorPopProb = float(workConfig.get("quilt-polys", "colorPopProb"))

        self.config.brightnessFactorDark = float(workConfig.get("quilt-polys", "brightnessFactorDark"))
        self.config.brightnessFactorLight = float(workConfig.get("quilt-polys", "brightnessFactorLight"))
        self.config.lines = workConfig.getboolean("quilt-polys", "lines")
        self.config.patternPrecision = workConfig.getboolean("quilt-polys", "patternPrecision")

        self.activeSet = workConfig.get("quilt-polys", "activeSet")

        self.c1HueRange = tuple(float(i) for i in workConfig.get(self.activeSet, "c1HueRange").split(","))
        self.c1SaturationRange = tuple(float(i) for i in workConfig.get(self.activeSet, "c1SaturationRange").split(","))
        self.c1ValueRange = tuple(float(i) for i in workConfig.get(self.activeSet, "c1ValueRange").split(","))

        self.c2HueRange = tuple(float(i) for i in workConfig.get(self.activeSet, "c2HueRange").split(","))
        self.c2SaturationRange = tuple(float(i) for i in workConfig.get(self.activeSet, "c2SaturationRange").split(","))
        self.c2ValueRange = tuple(float(i) for i in workConfig.get(self.activeSet, "c2ValueRange").split(","))

        self.c3HueRange = tuple(float(i) for i in workConfig.get(self.activeSet, "c3HueRange").split(","))
        self.c3SaturationRange = tuple(float(i) for i in workConfig.get(self.activeSet, "c3SaturationRange").split(","))
        self.c3ValueRange = tuple(float(i) for i in workConfig.get(self.activeSet, "c3ValueRange").split(","))

        # for now, all squares
        self.config.blockLength = self.blockSize
        self.config.blockHeight = self.blockSize

        self.config.unitArray = []

        self.config.fillColorSet = []
        self.config.fillColorSet.append(ColorSet(self.c1HueRange, self.c1SaturationRange, self.c1ValueRange))
        self.config.fillColorSet.append(ColorSet(self.c2HueRange, self.c2SaturationRange, self.c2ValueRange))
        self.config.fillColorSet.append(ColorSet(self.c3HueRange, self.c3SaturationRange, self.c3ValueRange))

        try:
            self.rotationRange = float(workConfig.get("quilt-polys", "rotationRange"))
        except Exception as e:
            self.rotationRange = 0
            pieceLogger(e)

        try:
            self.refreshCount = float(workConfig.get("quilt-polys", "refreshCount"))
        except Exception as e:
            self.refreshCount = 100
            pieceLogger(e)

        try:
            self.config.randomness = int(workConfig.get("quilt-polys", "randomness"))
            self.randomnessBase = int(workConfig.get("quilt-polys", "randomness"))
        except Exception as e:
            self.config.randomness = 0
            pieceLogger(e)

        try:
            drawBlockCoordsRaw = [list((i).split(",")) for i in workConfig.get("drawBlock", "drawBlockCoords").split("|")]
            self.drawBlockCoords = []
            self.drawBlockCoords.extend(tuple(int(ii) for ii in i) for i in drawBlockCoordsRaw)
            self.drawBlockCoords = tuple(self.drawBlockCoords)

            self.drawBlockFixedColor = tuple(int(i) for i in workConfig.get("drawBlock", "drawBlockFixedColor").split(","))
            self.drawBlock_c1HueRange = tuple(float(i) for i in workConfig.get("drawBlock", "c1HueRange").split(","))
            self.drawBlock_c1SaturationRange = tuple(float(i) for i in workConfig.get("drawBlock", "c1SaturationRange").split(","))
            self.drawBlock_c1ValueRange = tuple(float(i) for i in workConfig.get("drawBlock", "c1ValueRange").split(","))

            self.config.canvasImageDraw = ImageDraw.Draw(self.config.image)
            self.drawBlock = True
            self.drawBlockShape = lambda: self.config.canvasImageDraw.polygon(self.drawBlockCoords, fill=self.drawBlockFixedColor)

        except Exception as e:
            pieceLogger(e)
            self.drawBlock = False
            self.drawBlockShape = lambda: True

        createpolypieces.createPieces(self.config)

        setInitialColors()

        self.t1 = time.time()
        self.t2 = time.time()

        self.doingRefresh = self.refreshCount
        self.doingRefreshCount = self.refreshCount
        self.doingCrossFade = False

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
    return (round(a), round(b)) if rounding else (a, b)


def restartPiece():
    mrksMngr.t1 = time.time()
    mrksMngr.t2 = time.time()

    """
    ## The "dark" color to the spokes
    mrksMngr.c1HueRange = randomRange(0,360,True)
    mrksMngr.c2SaturationRange = randomRange(.4,.95)
    mrksMngr.c1ValueRange = randomRange(.3,.5)

    # the light color on the 8 spokes / points
    # these ones should always have the maximum variability
    mrksMngr.c2HueRange = (0,360) #randomRange(0,360,True)
    mrksMngr.c2SaturationRange = randomRange(.4,1)
    mrksMngr.c2ValueRange = randomRange(.8,1)

    ## The background -- ie the squares etc
    mrksMngr.c3HueRange = randomRange(0,360,True)
    mrksMngr.c3SaturationRange = randomRange()
    mrksMngr.c3ValueRange = randomRange()
    """

    if random.random() < 0.25:
        choice = round(random.SystemRandom().uniform(1, 3))
        pieceLogger("Choice {0}".format(choice))
        if choice == 1:
            # ruby pink bgs
            mrksMngr.c3HueRange = (350, 40)
            mrksMngr.c3SaturationRange = (0.7, 1)
            mrksMngr.c3ValueRange = (0.4, 1)
        elif choice == 2:
            # blue bg
            mrksMngr.c3HueRange = (220, 260)
            mrksMngr.c3SaturationRange = (0.9, 1)
            mrksMngr.c3ValueRange = (0.3, 0.95)
        else:
            # saturated
            mrksMngr.c3HueRange = (0, 360)
            mrksMngr.c3SaturationRange = (0.8, 1)
            mrksMngr.c3ValueRange = (0.3, 1)

    config.fillColorSet = []
    config.fillColorSet.append(ColorSet(mrksMngr.c1HueRange, mrksMngr.c1SaturationRange, mrksMngr.c1ValueRange))
    config.fillColorSet.append(ColorSet(mrksMngr.c2HueRange, mrksMngr.c2SaturationRange, mrksMngr.c2ValueRange))
    config.fillColorSet.append(ColorSet(mrksMngr.c3HueRange, mrksMngr.c3SaturationRange, mrksMngr.c3ValueRange))

    if random.random() < mrksMngr.resetSizeProbability:
        mrksMngr.rotation = random.SystemRandom().uniform(-mrksMngr.rotationRange, mrksMngr.rotationRange)
        # mrksMngr.doingRefresh = 0
        # mrksMngr.doingRefreshCount = mrksMngr.refreshCount

    if random.random() < mrksMngr.resetSizeProbability:
        mrksMngr.blockSize = round(random.SystemRandom().uniform(mrksMngr.blockSizeMin, mrksMngr.blockSizeMax))

        if mrksMngr.blockSize >= 11:
            config.blockCols = mrksMngr.blockColsMin
            config.blockRows = mrksMngr.blockRowsMin
        else:
            config.blockCols = mrksMngr.blockColsMax
            config.blockRows = mrksMngr.blockRowsMax

        config.blockLength = mrksMngr.blockSize
        config.blockHeight = mrksMngr.blockSize
        # mrksMngr.doingRefresh = 0
        # mrksMngr.doingRefreshCount = mrksMngr.refreshCount
        createpolypieces.createPieces(config, True)

    # poly specific
    if random.random() < mrksMngr.resetSizeProbability:
        config.randomness = random.SystemRandom().uniform(0, mrksMngr.randomnessBase)
        # mrksMngr.doingRefresh = 0
        # mrksMngr.doingRefreshCount = mrksMngr.refreshCount

    createpolypieces.refreshPalette(config)
    setInitialColors(True)


def setInitialColors(refresh=False):
    ## Better initial color when piece is turned on
    for i in range(len(config.unitArray)):
        obj = config.unitArray[i]
        for c in range(len(obj.polys)):
            colOverlay = obj.polys[c][1]
            colOverlay.colorB = colorutils.randomColor(config.brightness * 0.8)
            colOverlay.colorA = colorutils.randomColor(config.brightness * 0.8)
            colOverlay.colorTransitionSetup()
            colOverlay.colorTransitionSetupValues()


def main(run=True):
    global config, directionOrder, workConfig, mrksMngr
    pieceLogger("---------------------")
    pieceLogger("QUILT Loaded")

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
    config.redrawSpeed = float(workConfig.get("quilt-polys", "redrawSpeed"))
    config.directorController.slotRate = float(workConfig.get("quilt-polys", "slotRate"))

    config.brightness = float(workConfig.get("displayconfig", "brightness"))
    colorutils.brightness = config.brightness

    mrksMngr = QuiltManager(config)
    mrksMngr.setUp(workConfig)

    if run:
        runWork()
        runWork()
        runWork()


def runWork():
    global config
    pieceLogger(f"**", 2)
    pieceLogger("RUNNING quilt-poly-v2.py", 2)
    while config.isRunning:
        config.directorController.checkTime()
        if config.directorController.advance:
            iterate()
        time.sleep(config.redrawSpeed)
        if not config.standAlone:
            config.callBack()


def iterate():
    global config
    config.outlineColorObj.stepTransition()

    # Need to do a crossfade
    # if mrksMngr.doingRefresh < mrksMngr.doingRefreshCount:
    #     # pieceLogger("crossfade...",  mrksMngr.doingRefresh/mrksMngr.doingRefreshCount)
    #     if mrksMngr.doingRefresh == 0:
    #         mrksMngr.snapShot = config.image.copy()
    #     crossFade = Image.blend(
    #         mrksMngr.snapShot,
    #         config.canvasImage,
    #         mrksMngr.doingRefresh / mrksMngr.doingRefreshCount,
    #     )
    #     mrksMngr.drawBlockShape()
    #     # config.render(crossFade, 0, 0)
    #     mrksMngr.doingRefresh += 1
    # else:
    #     temp = Image.new("RGBA", (mrksMngr.canvasImageWidth, mrksMngr.canvasImageHeight))
    #     temp.paste(config.image, (0, 0), config.image)
    #     if mrksMngr.transformShape :
    #         temp = transformImage(temp)
    #     mrksMngr.drawBlockShape()
    #     config.render(temp, 0, 0)

    for i in range(len(config.unitArray)):
        obj = config.unitArray[i]
        obj.update()
        obj.render()

    if config.sectionDisturbance:
        distortions.iterationFunction(config)

    # previous non-disturbing iteration just rendered the temp image
    # config.render(temp, 0, 0)

    temp1 = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    # temp1Draw = ImageDraw.Draw(temp1)

    config.image.paste(config.canvasImage, (0, 0), config.canvasImage)
    temp1.paste(config.image, (0, 0), config.image)

    if mrksMngr.transformShape:
        temp1 = transformImage(temp1)

    if config.useWaveDistortion:
        temp1 = ImageOps.deform(temp1, distortions.WaveDeformer(config))
        config.waveDeformXPos += config.waveDeformXPosRate
        if config.waveDeformXPos > config.screenWidth:
            config.waveDeformXPos = 0

    config.render(temp1, config.imgcanvasOffsetX, config.imgcanvasOffsetY, config.canvasWidth, config.canvasHeight)
    # Done

    mrksMngr.t2 = time.time()
    delta = mrksMngr.t2 - mrksMngr.t1

    if delta > mrksMngr.timeToComplete:
        if config.sectionDisturbance:
            # these functions are run to restart disturber
            distortions.resetFunction(config)

        restartPiece()

