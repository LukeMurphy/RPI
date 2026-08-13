import itertools
import math
import random
import time
from PIL import Image, ImageDraw
from modules.configuration import bcolors
from modules import coloroverlay, colorutils, panelDrawing
from modules.holder_director import Director

# import numpy
# import beepy as beeper
# beeper.beep(sound=1) # integer as argument
# ------------------------------------------------------------------- #

class Palette:
    tLimitBase = 0
    minHue = 0
    maxHue = 0
    minSaturation = 0
    maxSaturation = 0
    minValue = 0
    maxValue = 0
    dropHueMin = 0
    dropHueMin = 0

    l_tLimitBase = 0
    l_minHue = 0
    l_maxHue = 0
    l_minSaturation = 0
    l_maxSaturation = 0
    l_minValue = 0
    l_maxValue = 0
    l_dropHueMin = 0
    l_dropHueMax = 0

    l2_tLimitBase = 0
    l2_minHue = 0
    l2_maxHue = 0
    l2_minSaturation = 0
    l2_maxSaturation = 0
    l2_minValue = 0
    l2_maxValue = 0
    l2_dropHueMin = 0
    l2_dropHueMax = 0

    def __init__(self):
        pass

    def getBarColors(self):
        return [
            self.minHue,
            self.maxHue,
            self.minSaturation,
            self.maxSaturation,
            self.minValue,
            self.maxValue,
            self.dropHueMin,
            self.dropHueMax,
            self.tLimitBase,
        ]

    def getLineColors(self):
        return [
            self.l_minHue,
            self.l_maxHue,
            self.l_minSaturation,
            self.l_maxSaturation,
            self.l_minValue,
            self.l_maxValue,
            self.l_dropHueMin,
            self.l_dropHueMax,
            self.l_tLimitBase,
        ]

    def getLineColors2(self):
        return [
            self.l2_minHue,
            self.l2_maxHue,
            self.l2_minSaturation,
            self.l2_maxSaturation,
            self.l2_minValue,
            self.l2_maxValue,
            self.l2_dropHueMin,
            self.l2_dropHueMax,
            self.l2_tLimitBase,
        ]


class Block:
    def __init__(self, config, i, blksMngr):
        # print ("init Fludd", i)

        # self.boxMax = config.screenWidth - 1
        # self.boxMaxAlt = self.boxMax + int(random.uniform(10,30) * config.screenWidth)
        # self.boxHeight = config.screenHeight - 2        #

        self.unitNumber = i
        self.config = config
        self.blksMngr = blksMngr

        self.xPos = 0
        self.yPos = 0
        self.blockWidth = 128
        self.blockHeight = 128
        self.barWidth = 4
        self.gap = 0
        self.rotation = 0
        self.polyDeltaX = 0
        self.polyDeltaY = 0

    def setUp(self, palette, linePalette):
        self.blockImage = Image.new("RGBA", (self.blockWidth, self.blockHeight))
        self.blockDraw = ImageDraw.Draw(self.blockImage)

        # [minHue,maxHue,minSaturation,maxSaturation,minValue,maxValue,tLimitBase]

        self.colOverlay = getConfigOverlay(palette, self.blksMngr.usePaletteOverride)
        self.colOverlay2 = getConfigOverlay(linePalette, self.blksMngr.usePaletteOverride)

    def bars(self):

        clr = tuple(round(a * self.config.brightness) for a in (self.colOverlay.currentColor))
        clr2 = tuple(round(a * self.config.brightness) for a in (self.colOverlay2.currentColor))

        self.blockDraw.rectangle(
            (0, 0, self.blockWidth, self.blockHeight),
            fill=self.blksMngr.bgColor,
            outline=None,
        )

        count = 0
        numBars = round(self.blockHeight / self.barWidth)
        for i in range(numBars):
            outClr = clr2
            if count % 2 == 0:
                outClr = clr
            # if self.gap < 3 :
            self.polyDeltaX = round(random.uniform(-self.blksMngr.deltaXVal, self.blksMngr.deltaXVal))
            self.polyDeltaY = round(random.uniform(-self.blksMngr.deltaXVal, self.blksMngr.deltaYVal))
            x1 = 0
            y1 = i * (self.barWidth + self.gap)
            x2 = self.blockWidth - 1 + self.polyDeltaX
            y2 = i * (self.barWidth + self.gap) + self.barWidth + self.polyDeltaY

            # self.blockDraw.rectangle((x1,y1,x2,y2),outline=(None), fill=outClr)
            if self.blksMngr.drawOutlines:
                self.blockDraw.polygon(
                    ((x1, y1), (x2, y1), (x2, y2), (x1, y2)),
                    outline=(clr2),
                    fill=outClr,
                )
            else:
                self.blockDraw.polygon(((x1, y1), (x2, y1), (x2, y2), (x1, y2)), outline=None, fill=outClr)
            count += 1

class BlocksManager:
    def __init__(self, config):
        self.config = config

    def setUp(self, workConfig):
        config = self.config
        config.redrawSpeed = float(workConfig.get("movingpattern", "redrawSpeed"))
        self.changeGridProb = float(workConfig.get("movingpattern", "changeGridProb"))
        self.changeQuiverProb = float(workConfig.get("movingpattern", "changeQuiverProb"))

        try:
            self.changeQuiverOnProb = float(workConfig.get("movingpattern", "changeQuiverOnProb"))
            self.changeQuiverOffProb = float(workConfig.get("movingpattern", "changeQuiverOffProb"))
            # comment:
        except Exception as e:
            print(e)
            self.changeQuiverOnProb = float(workConfig.get("movingpattern", "changeQuiverProb"))
            self.changeQuiverOffProb = float(workConfig.get("movingpattern", "changeQuiverProb"))
        # end try

        self.rotationVariation = float(workConfig.get("movingpattern", "rotationVariation"))
        self.blockWidth = int(workConfig.get("movingpattern", "blockWidth"))
        self.blockHeight = int(workConfig.get("movingpattern", "blockHeight"))
        self.rows = int(workConfig.get("movingpattern", "rows"))
        self.cols = int(workConfig.get("movingpattern", "cols"))
        self.barWidthMin = int(workConfig.get("movingpattern", "barWidthMin"))
        self.barWidthMax = int(workConfig.get("movingpattern", "barWidthMax"))
        self.gapWidthMin = int(workConfig.get("movingpattern", "gapWidthMin"))
        self.gapWidthMax = int(workConfig.get("movingpattern", "gapWidthMax"))
        self.drawOutlines = workConfig.getboolean("movingpattern", "drawOutlines")

        self.blurPatchProb = float(workConfig.get("movingpattern", "blurPatchProb"))

        try:
            self.filterRemapping = workConfig.getboolean("movingpattern", "filterRemapping")
            self.filterRemappingProb = float(workConfig.get("movingpattern", "filterRemappingProb"))
            self.filterRemapminHoriSize = int(workConfig.get("movingpattern", "filterRemapminHoriSize"))
            self.filterRemapminVertSize = int(workConfig.get("movingpattern", "filterRemapminVertSize"))
            self.filterRemapRangeX = int(workConfig.get("movingpattern", "filterRemapRangeX"))
            self.filterRemapRangeY = int(workConfig.get("movingpattern", "filterRemapRangeY"))
        except Exception as e:
            print(e)
            self.filterRemapping = False
            self.filterRemappingProb = 0.0
            self.filterRemapminHoriSize = 24
            self.filterRemapminVertSize = 24
            self.filterRemapRangeX = config.canvasWidth
            self.filterRemapRangeY = config.canvasHeight

        self.sizeArrayVals = workConfig.get("movingpattern", "sizeArray")
        self.sizeArray = self.sizeArrayVals.split(",")
        self.sizeArray = list(map(lambda x: int(x), self.sizeArray))

        createImageLayers(config)

        try:
            self.deltaXVal = int(workConfig.get("movingpattern", "deltaVal"))
            self.deltaYVal = int(workConfig.get("movingpattern", "deltaVal"))
            self.deltaVal = int(workConfig.get("movingpattern", "deltaVal"))
        except Exception as e:
            print(e)
            self.deltaXVal = 1
            self.deltaYVal = 1
            self.deltaVal = 1

        # ---------------------------------------

        try:
            self.mixedPaletteProb = float(workConfig.get("movingpattern", "mixedPaletteProb"))
            self.mixedPalettes = False
        except Exception as e:
            print(e)
            self.mixedPalettes = True
            self.mixedPaletteProb = 1.0

        try:
            self.paletteOverrideNames = workConfig.get("movingpattern", "paletteOverrideNames").split(",")
            self.paletteOverrideProb = float(workConfig.get("movingpattern", "paletteOverrideProb"))
            self.usePaletteOverride = True
            self.fixedPaletteIndex = 0
        except Exception as e:
            print(e)
            self.usePaletteOverride = False
            self.paletteOverrideProb = 0.0
            self.fixedPaletteIndex = 0

        self.palettes = workConfig.get("movingpattern", "palettes").split(",")

        self.workingPalettes = []

        for _p in self.palettes:
            plt = Palette()
            plt.name = _p
            makePalette(plt.name, plt)
            makeLinePalette(plt.name, plt)
            self.workingPalettes.append(plt)

        # Right now the background is controlled by the first palette in the list of
        # palettes to use
        self.paletteIndex = 0
        self.colOverlay = getConfigOverlay(getPalette(config, self.paletteIndex), self.usePaletteOverride)

        # ---------------------------------------

        self.gridOptions = ["buildGrid", "buildGrid", "buildUniformGrid"]

        index = math.floor(random.random() * len(self.gridOptions))
        if index > len(self.gridOptions):
            index = 0

        print(f"Running a :{str(self.gridOptions[index])}")

        eval(self.gridOptions[index])(config, self)

        # managing speed of animation and framerate
        config.directorController = Director(config)

        try:
            # comment:
            config.directorController.slotRate = float(workConfig.get("movingpattern", "slotRate"))
        except Exception as e:
            print(f"slotRate not defined {e} : defaulting to 0.03")
            config.directorController.slotRate = 0.03
        # end try

        # THIS IS USED AS WAY TO MOCKUP A CONFIGURATION OF RECTANGULAR PANELS
        # panelDrawing.mockupBlock(config, workConfig)

        # """
        #     # Need to add something like this at final render call  as well

        #     ########### RENDERING AS A MOCKUP OR AS REAL ###########
        #     if config.useDrawingPoints  :
        #         config.panelDrawing.canvasToUse = config.renderImageFull
        #         config.panelDrawing.render()
        #     else :
        #         # config.render(config.canvasImage, 0, 0, config.canvasWidth, config.canvasHeight)
        #         # config.render(config.image, 0, 0)
        #         config.render(config.renderImageFull, 0, 0)
        # """

# ------------------------------------------------------------------- #

def createImageLayers(config):
    config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.canvasDraw = ImageDraw.Draw(config.canvasImage)

    config.destinationImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))


def redraw(config, blksMngr):

    config.canvasDraw.rectangle(
        (0, 0, config.canvasWidth, config.canvasHeight),
        fill=blksMngr.bgColor,
        outline=None,
    )

    for b in blksMngr.barBlocks:
        b.bars()
        temp = b.blockImage.copy()
        if b.rotation != 0:
            temp = temp.rotate(b.rotation, 0, True)
        config.canvasImage.paste(temp, (b.xPos, b.yPos), temp)
        b.colOverlay.stepTransition()
        b.colOverlay2.stepTransition()


def getConfigOverlay(palette, forceSelection=False):
    colOverlay = coloroverlay.ColorOverlay()
    colOverlay.randomSteps = False
    colOverlay.timeTrigger = True
    colOverlay.maxBrightness = 1
    colOverlay.steps = 50
    if not forceSelection:
        colOverlay.minHue = palette[0]
        colOverlay.maxHue = palette[1]
        colOverlay.minSaturation = palette[2]
        colOverlay.maxSaturation = palette[3]
        colOverlay.minValue = palette[4]
        colOverlay.maxValue = palette[5]
        colOverlay.dropHueMin = palette[6]
        colOverlay.dropHueMax = palette[7]
        colOverlay.tLimitBase = palette[8]
    else:
        # This needs to be configurable
        fixedPaletteIndex = blksMngr.fixedPaletteIndex

        if blksMngr.mixedPalettes:
            fixedPaletteIndex = round(random.uniform(0, len(blksMngr.paletteOverrideNames) - 1))

        paletteColor = colorutils.getNamedPalette(blksMngr.paletteOverrideNames[fixedPaletteIndex])
        # print(("fixedPaletteIndex: {} palette name: {}  paletteColor: {}").format(fixedPaletteIndex, blksMngr.paletteOverrideNames[fixedPaletteIndex], paletteColor))

        paletteColorHSV = colorutils.rgb_to_hsv(paletteColor[0], paletteColor[1], paletteColor[2])

        colOverlay.minHue = paletteColorHSV[0]
        colOverlay.maxHue = paletteColorHSV[0]
        colOverlay.minSaturation = paletteColorHSV[1]
        colOverlay.maxSaturation = paletteColorHSV[1]
        colOverlay.minValue = paletteColorHSV[2]
        colOverlay.maxValue = paletteColorHSV[2]
        colOverlay.tLimitBase = 25
    colOverlay.colorTransitionSetup()
    return colOverlay


def getLinePalette(rex, indx):
    paletteObj = blksMngr.workingPalettes[indx]
    return paletteObj.getBarColors()


def getPalette(configRef, indx):
    paletteObj = blksMngr.workingPalettes[indx]
    # print(f"Returning colors for {paletteObj.name}")
    return paletteObj.getLineColors()


def makePalette(palette, paletteObj):
    global workConfig
    print(f"Loading palette {palette}")
    paletteObj.tLimitBase = int(workConfig.get(palette, "tLimitBase"))
    paletteObj.minHue = float(workConfig.get(palette, "minHue"))
    paletteObj.maxHue = float(workConfig.get(palette, "maxHue"))
    paletteObj.minSaturation = float(workConfig.get(palette, "minSaturation"))
    paletteObj.maxSaturation = float(workConfig.get(palette, "maxSaturation"))
    paletteObj.minValue = float(workConfig.get(palette, "minValue"))
    paletteObj.maxValue = float(workConfig.get(palette, "maxValue"))
    try:
        paletteObj.dropHueMin = float(workConfig.get(palette, "dropHueMin"))
        paletteObj.dropHueMax = float(workConfig.get(palette, "dropHueMax"))
    except Exception as e:
        print("\n------------------------------")
        print(f"Check palette config:{palette} {e}")
        paletteObj.dropHueMax = 0
        paletteObj.dropHueMin = 0


def makeLinePalette(palette, paletteObj):
    paletteObj.l_tLimitBase = int(workConfig.get(palette, "line_tLimitBase"))
    paletteObj.l_minHue = float(workConfig.get(palette, "line_minHue"))
    paletteObj.l_maxHue = float(workConfig.get(palette, "line_maxHue"))
    paletteObj.l_minSaturation = float(workConfig.get(palette, "line_minSaturation"))
    paletteObj.l_maxSaturation = float(workConfig.get(palette, "line_maxSaturation"))
    paletteObj.l_minValue = float(workConfig.get(palette, "line_minValue"))
    paletteObj.l_maxValue = float(workConfig.get(palette, "line_maxValue"))
    try:
        paletteObj.l_dropHueMin = float(workConfig.get(palette, "line_dropHueMin"))
        paletteObj.l_dropHueMax = float(workConfig.get(palette, "line_dropHueMax"))
    except Exception as e:
        print(e)
        paletteObj.l_dropHueMax = 0
        paletteObj.l_dropHueMin = 0


def makeLine2Palette(palette, paletteObj):
    # This is not really used - for future use sometime
    try:
        _makeL2Palette(palette, paletteObj)
    except Exception as e:
        print(e)
        paletteObj.l2_tLimitBase = 0
        paletteObj.l2_minHue = 0
        paletteObj.l2_maxHue = 0
        paletteObj.l2_minSaturation = 0
        paletteObj.l2_maxSaturation = 0
        paletteObj.l2_minValue = 0
        paletteObj.l2_maxValue = 0
        paletteObj.l2_dropHueMin = 0
        paletteObj.l2_dropHueMax = 0
        paletteObj.l2_dropHueMax = 0
        paletteObj.l2_dropHueMin = 0


# TODO Rename this here and in `makeLine2Palette`
def _makeL2Palette(palette, paletteObj):
    paletteObj.l2_tLimitBase = int(workConfig.get(palette, "line2_tLimitBase"))
    paletteObj.l2_minHue = float(workConfig.get(palette, "line2_minHue"))
    paletteObj.l2_maxHue = float(workConfig.get(palette, "line2_maxHue"))
    paletteObj.l2_minSaturation = float(workConfig.get(palette, "line2_minSaturation"))
    paletteObj.l2_maxSaturation = float(workConfig.get(palette, "line2_maxSaturation"))
    paletteObj.l2_minValue = float(workConfig.get(palette, "line2_minValue"))
    paletteObj.l2_maxValue = float(workConfig.get(palette, "line2_maxValue"))
    paletteObj.l2_dropHueMin = float(workConfig.get(palette, "line2_dropHueMin"))
    paletteObj.l2_dropHueMax = float(workConfig.get(palette, "line2_dropHueMax"))



# Builds flexible grid
def buildGrid(config, blksMngr):
    """Builds a flexible grid of bar blocks."""
    count = 0
    blksMngr.barBlocks = []
    delta = 0
    rows = round(config.canvasHeight / blksMngr.blockHeight)
    cols = round(config.canvasWidth / blksMngr.blockWidth)
    cols = min(cols, 80)
    gridSize = 8
    availableCoords = _create_available_coords_grid(rows, cols, gridSize)

    for row in range(len(availableCoords) - 2):
        for col in range(len(availableCoords[row])):
            if _is_valid_coord(availableCoords, row, col):
                _create_and_place_block(config, blksMngr, availableCoords, row, col, count, delta, gridSize)
                count += 1


def _create_available_coords_grid(rows, cols, gridSize):
    """Creates a grid of available coordinates."""
    availableCoords = []
    for r in range(rows):
        availableCoords.append([])
        for c in range(cols):
            availableCoords[r].append([c * gridSize, r * gridSize, 0])
    return availableCoords


def _is_valid_coord(availableCoords, row, col):
    """Checks if the given coordinate is valid and available."""
    return (availableCoords[row][col][2] == 0 and
            availableCoords[row + 1][col][2] == 0 and
            availableCoords[row + 2][col][2] == 0)


def _create_and_place_block(config, blksMngr, availableCoords, row, col, count, delta, gridSize):
    """Creates and places a bar block at the given coordinate."""
    index = math.floor(random.uniform(0, len(blksMngr.sizeArray)))
    blockWidth = blksMngr.sizeArray[index]

    removedPointsSize = round(blockWidth / gridSize)
    if (removedPointsSize + col < len(availableCoords[row]) and
            availableCoords[row][col + removedPointsSize][2] == 1):
        newIndex = math.floor(random.uniform(0, 3))
        blockWidth = blksMngr.sizeArray[newIndex]

    blockHeight = blockWidth

    barBlockUnit = Block(config, count, blksMngr)
    barBlockUnit.blockWidth = round(random.uniform(blockWidth - delta, blockWidth + delta))
    barBlockUnit.blockHeight = blockHeight

    barBlockUnit.xPos = availableCoords[row][col][0]
    barBlockUnit.yPos = availableCoords[row][col][1]

    barBlockUnit.barWidth = round(random.uniform(blksMngr.barWidthMin, blksMngr.barWidthMax))
    barBlockUnit.gap = round(random.uniform(blksMngr.gapWidthMin, blksMngr.gapWidthMax))
    barBlockUnit.rotation = (round(random.uniform(90 - blksMngr.rotationVariation, 90 + blksMngr.rotationVariation))
                             if count % 2 != 0 else round(random.uniform(-blksMngr.rotationVariation, blksMngr.rotationVariation)))

    paletteIndex = (math.floor(random.uniform(0, len(blksMngr.palettes)))
                    if blksMngr.mixedPalettes else blksMngr.paletteIndex)
    barBlockUnit.setUp(getPalette(config, paletteIndex), getLinePalette(config, paletteIndex))

    blksMngr.barBlocks.append(barBlockUnit)

    removedPointsSize = round(blockWidth / gridSize)
    for r in range(removedPointsSize):
        for c in range(removedPointsSize):
            if (col + c) < len(availableCoords[row]) and (row + r) < len(availableCoords):
                availableCoords[row + r][col + c][2] = 1


'''
# Builds flexible grid
def _buildGrid(config):

    count = 0
    config.barBlocks = []
    delta = 0
    # sizes = [16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120, 128]
    rows = round(config.canvasHeight / config.blockHeight) * 1
    cols = round(config.canvasWidth / config.blockWidth)

    cols = min(cols, 80)
    # print("---- buildGrid --")
    # print(("Rows:{}  cols:{} paletteIndex:{} overridePalette:{}  mixedPalettes:{}").format(
    #     rows, cols, config.paletteIndex, config.usePaletteOverride, config.mixedPalettes))
    # print("------")

    gridSize = 8
    availableCoords = []
    for r in range(rows):
        availableCoords.append([])
        for c in range(cols):
            availableCoords[r].append([c * gridSize, r * gridSize, 0])

    # first one is upper left
    for row in range(len(availableCoords) - 2):
        for col in range(len(availableCoords[row])):
            if availableCoords[row][col][2] == 0 and availableCoords[row + 1][col][2] == 0 and availableCoords[row + 2][col][2] == 0:

                # set size of patch
                index = math.floor(random.uniform(0, len(config.sizeArray)))
                blockWidth = config.sizeArray[index]

                # see if the width is too wide sometimes
                removedPointsSize = round(blockWidth / gridSize)
                if removedPointsSize + col < len(availableCoords[row]) and availableCoords[row][col + removedPointsSize][2] == 1:
                    newIndex = math.floor(random.uniform(0, 3))
                    blockWidth = config.sizeArray[newIndex]

                blockHeight = blockWidth

                barBlockUnit = Block(config, count)
                barBlockUnit.blockWidth = round(random.uniform(blockWidth - delta, blockWidth + delta))
                barBlockUnit.blockHeight = blockHeight

                barBlockUnit.xPos = availableCoords[row][col][0]
                barBlockUnit.yPos = availableCoords[row][col][1]

                barBlockUnit.barWidth = round(random.uniform(config.barWidthMin, config.barWidthMax))
                barBlockUnit.gap = round(random.uniform(config.gapWidthMin, config.gapWidthMax))
                if count % 2 != 0:
                    barBlockUnit.rotation = round(random.uniform(90 - config.rotationVariation, 90 + config.rotationVariation))
                else:
                    barBlockUnit.rotation = round(random.uniform(-config.rotationVariation, config.rotationVariation))

                paletteIndex = math.floor(random.uniform(0, len(config.palettes)))
                if config.mixedPalettes:
                    paletteIndex = math.floor(random.uniform(0, len(config.palettes)))
                else:
                    paletteIndex = config.paletteIndex
                barBlockUnit.setUp(
                    getPalette(config, paletteIndex),
                    getLinePalette(config, paletteIndex),
                )

                config.barBlocks.append(barBlockUnit)
                count += 1

                removedPointsSize = round(blockWidth / gridSize)
                # print(removedPointsSize, len(availableCoords))

                for r in range(removedPointsSize):
                    for c in range(removedPointsSize):
                        if (col + c) < len(availableCoords[row]) and (row + r) < len(availableCoords):
                            availableCoords[row + r][col + c][2] = 1
'''

# Builds overlapped grid
def buildOverlapGrid(config, blksMngr):

    count = 0
    blksMngr.barBlocks = []
    delta = 0

    rows = 7
    cols = 7

    # print("---- buildOverlapGrid --")
    # print(
    #     (
    #         "Rows:{}  cols:{} paletteIndex:{} overridePalette:{}  mixedPalettes:{}"
    #     ).format(
    #         rows,
    #         cols,
    #         config.paletteIndex,
    #         config.usePaletteOverride,
    #         config.mixedPalettes,
    #     )
    # )

    gridSize = 32
    availableCoords = [
        [c * gridSize, r * gridSize]
        for r, c in itertools.product(range(rows), range(cols))
    ]
    # first one is upper left
    for item in availableCoords:
        index = math.floor(random.uniform(0, len(blksMngr.sizeArray)))
        blockWidth = blksMngr.sizeArray[index]
        # blockHeight = config.blockWidth
        barBlockUnit = Block(config, count, blksMngr)
        barBlockUnit.blockWidth = round(random.uniform(blockWidth - delta, blockWidth + delta))
        barBlockUnit.blockHeight = barBlockUnit.blockWidth
        barBlockUnit.xPos = item[0]
        barBlockUnit.yPos = item[1]

        barBlockUnit.barWidth = round(random.uniform(blksMngr.barWidthMin, blksMngr.barWidthMax))
        barBlockUnit.gap = round(random.uniform(blksMngr.gapWidthMin, blksMngr.gapWidthMax))
        barBlockUnit.rotation = (
            round(
                random.uniform(
                    90 - blksMngr.rotationVariation,
                    90 + blksMngr.rotationVariation,
                )
            )
            if count % 2 != 0
            else round(
                random.uniform(
                    -blksMngr.rotationVariation, blksMngr.rotationVariation
                )
            )
        )
        paletteIndex = math.floor(random.uniform(0, len(blksMngr.palettes)))
        if blksMngr.mixedPalettes:
            paletteIndex = math.floor(random.uniform(0, len(blksMngr.palettes)))
        else:
            paletteIndex = blksMngr.paletteIndex

        barBlockUnit.setUp(getPalette(config, paletteIndex), getLinePalette(config, paletteIndex))
        blksMngr.barBlocks.append(barBlockUnit)
        count += 1


# Builds uniform grid
def buildUniformGrid(config, blksMngr):

    count = 0
    blksMngr.barBlocks = []
    delta = 0
    index = math.floor(random.uniform(0, len(blksMngr.sizeArray)))
    blockWidth = blksMngr.sizeArray[index]
    blockHeight = blockWidth

    rows = round(config.canvasHeight / blockHeight) * 2
    cols = round(config.canvasWidth / blockWidth)

    # print("----> buildUniformGrid --")
    # print(
    #     (
    #         "Rows:{}  cols:{} paletteIndex:{} overridePalette:{}  mixedPalettes:{}"
    #     ).format(
    #         rows,
    #         cols,
    #         config.paletteIndex,
    #         config.usePaletteOverride,
    #         config.mixedPalettes,
    #     )
    # )

    for r in range(rows):
        lastX = 0
        for _ in range(cols):
            barBlockUnit = Block(config, count, blksMngr)
            barBlockUnit.blockWidth = round(random.uniform(blockWidth - delta, blockWidth + delta))
            barBlockUnit.blockHeight = barBlockUnit.blockWidth
            barBlockUnit.xPos = lastX  # c * barBlockUnit.blockWidth
            lastX += barBlockUnit.blockWidth
            barBlockUnit.yPos = r * blockHeight

            barBlockUnit.barWidth = round(random.uniform(blksMngr.barWidthMin, blksMngr.barWidthMax))
            barBlockUnit.gap = round(random.uniform(blksMngr.gapWidthMin, blksMngr.gapWidthMax))
            if count % 2 != 0:
                barBlockUnit.rotation = round(random.uniform(90 - blksMngr.rotationVariation, 90 + blksMngr.rotationVariation))
            else:
                barBlockUnit.rotation = round(random.uniform(-blksMngr.rotationVariation, blksMngr.rotationVariation))

            if blksMngr.mixedPalettes:
                paletteIndex = math.floor(random.uniform(0, len(blksMngr.palettes)))
            else:
                paletteIndex = blksMngr.paletteIndex

            barBlockUnit.setUp(
                getPalette(config, paletteIndex),
                getLinePalette(config, paletteIndex),
            )
            blksMngr.barBlocks.append(barBlockUnit)
            count += 1


def iterate():
    global config, blksMngr
    blksMngr.colOverlay.stepTransition()

    blksMngr.bgColor = tuple(round(a * config.brightness) for a in (blksMngr.colOverlay.currentColor))

    redraw(config, blksMngr)

    # dithering movement
    if random.random() < blksMngr.filterRemappingProb:
        _extracted_from_iterate_11(config, blksMngr)
    if random.random() < blksMngr.blurPatchProb:
        _extracted_from_iterate_22(config)
            # print(config.blurSection)

    if random.random() < blksMngr.changeGridProb:

        _extracted_from_iterate_48(config, blksMngr)
    if random.random() < blksMngr.changeQuiverOnProb:
        blksMngr.deltaXVal = round(random.uniform(0, blksMngr.deltaVal))
        blksMngr.deltaYVal = round(random.uniform(0, blksMngr.deltaVal))

    if random.random() < blksMngr.changeQuiverOffProb:
        # a bit more often, things just go still
        blksMngr.deltaXVal = blksMngr.deltaYVal = 0

    # if config.useDrawingPoints :
    #     config.panelDrawing.canvasToUse = config.canvasImage
    #     config.panelDrawing.render()
    # else:
    #     config.render(config.canvasImage, 0, 0, config.canvasWidth, config.canvasHeight)
    config.render(config.canvasImage, 0, 0, config.canvasWidth, config.canvasHeight)


# TODO Rename this here and in `iterate`
def _extracted_from_iterate_48(config, blksMngr):
    # beeper.beep(sound=1) # integer as argument
    # change the palette - used if the mixed palettes option is False and the
    # palette override is False
    blksMngr.paletteIndex = math.floor(random.uniform(0, len(blksMngr.palettes)))

    # Decide what changes

    # paletteOverride sustitutes a fixed palette for a
    # randomized HSV one

    if random.random() < blksMngr.paletteOverrideProb:
        blksMngr.usePaletteOverride = True
        blksMngr.fixedPaletteIndex = round(random.uniform(0, len(blksMngr.paletteOverrideNames) - 1))
    else:
        blksMngr.usePaletteOverride = False

    # mixedPalette means either use one palette for all
    # the blocks or randonly choice between the set of palettes
    blksMngr.mixedPalettes = random.random() < blksMngr.mixedPaletteProb
    print(f"Change Build : {blksMngr.palettes[blksMngr.paletteIndex]}")

    # choose the layout
    index = math.floor(random.random() * len(blksMngr.gridOptions))
    if index > len(blksMngr.gridOptions):
        index = 0
    print(f"Running a :{str(blksMngr.gridOptions[index])}")
    eval(blksMngr.gridOptions[index])(config, blksMngr)


# TODO Rename this here and in `iterate`
def _extracted_from_iterate_22(config):
    x1 = round(random.uniform(0, config.canvasWidth / 2))
    y1 = round(random.uniform(0, config.canvasHeight / 2))
    x2 = round(random.uniform(5, config.canvasWidth))
    y2 = round(random.uniform(5, config.canvasHeight))

    config.useBlur = True
    config.blurXOffset = x1
    config.blurYOffset = y1
    config.blurSectionWidth = x2
    config.blurSectionHeight = y2
    config.sectionBlurRadius = 3

    config.blurSection = (
        config.blurXOffset,
        config.blurYOffset,
        config.blurXOffset + config.blurSectionWidth,
        config.blurYOffset + config.blurSectionHeight,
    )


# TODO Rename this here and in `iterate`
def _extracted_from_iterate_11(config, blksMngr):
    config.useFilters = True
    config.remapImageBlock = True

    startX = round(random.uniform(0, blksMngr.filterRemapRangeX))
    startY = round(random.uniform(0, blksMngr.filterRemapRangeY))
    endX = round(random.uniform(4, blksMngr.filterRemapminHoriSize))
    endY = round(random.uniform(4, blksMngr.filterRemapminVertSize))
    config.remapImageBlockSection = [startX, startY, startX + endX, startY + endY]
    config.remapImageBlockDestination = [startX, startY]
    # Done


def runWork():
    global config
    print(f"{bcolors.OKGREEN}** {bcolors.BOLD}")
    print("Running barblocks.py")
    print(bcolors.ENDC)
    while config.isRunning:
        config.directorController.checkTime()
        if config.directorController.advance:
            iterate()
        time.sleep(config.redrawSpeed)
        if not config.standAlone:
            config.callBack()


def main(run=True):
    global config, blksMngr
    blksMngr = BlocksManager(config)
    blksMngr.setUp(workConfig)

    if run:
        runWork()
