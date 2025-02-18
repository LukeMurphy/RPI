# ################################################### #
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
    def __init__(self, config, i):
        # print ("init Fludd", i)

        # self.boxMax = config.screenWidth - 1
        # self.boxMaxAlt = self.boxMax + int(random.uniform(10,30) * config.screenWidth)
        # self.boxHeight = config.screenHeight - 2        #

        self.unitNumber = i
        self.config = config

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

        self.colOverlay = getConfigOverlay(palette, config.usePaletteOverride)
        self.colOverlay2 = getConfigOverlay(linePalette, config.usePaletteOverride)

    def bars(self):

        clr = tuple(round(a * self.config.brightness) for a in (self.colOverlay.currentColor))
        clr2 = tuple(round(a * self.config.brightness) for a in (self.colOverlay2.currentColor))

        self.blockDraw.rectangle(
            (0, 0, self.blockWidth, self.blockHeight),
            fill=self.config.bgColor,
            outline=None,
        )

        count = 0
        numBars = round(self.blockHeight / self.barWidth)
        for i in range(numBars):
            outClr = clr2
            if count % 2 == 0:
                outClr = clr
            # if self.gap < 3 :
            self.polyDeltaX = round(random.uniform(-self.config.deltaXVal, self.config.deltaXVal))
            self.polyDeltaY = round(random.uniform(-self.config.deltaXVal, self.config.deltaYVal))
            x1 = 0
            y1 = i * (self.barWidth + self.gap)
            x2 = self.blockWidth - 1 + self.polyDeltaX
            y2 = i * (self.barWidth + self.gap) + self.barWidth + self.polyDeltaY

            # self.blockDraw.rectangle((x1,y1,x2,y2),outline=(None), fill=outClr)
            if self.config.drawOutlines:
                self.blockDraw.polygon(
                    ((x1, y1), (x2, y1), (x2, y2), (x1, y2)),
                    outline=(clr2),
                    fill=outClr,
                )
            else:
                self.blockDraw.polygon(((x1, y1), (x2, y1), (x2, y2), (x1, y2)), outline=None, fill=outClr)
            count += 1


def redraw(config):

    config.canvasDraw.rectangle(
        (0, 0, config.canvasWidth, config.canvasHeight),
        fill=config.bgColor,
        outline=None,
    )

    for b in config.barBlocks:
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
        fixedPaletteIndex = config.fixedPaletteIndex

        if config.mixedPalettes:
            fixedPaletteIndex = round(random.uniform(0, len(config.paletteOverrideNames) - 1))

        paletteColor = colorutils.getNamedPalette(config.paletteOverrideNames[fixedPaletteIndex])
        # print(("fixedPaletteIndex: {} palette name: {}  paletteColor: {}").format(fixedPaletteIndex, config.paletteOverrideNames[fixedPaletteIndex], paletteColor))

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
    paletteObj = config.workingPalettes[indx]
    return paletteObj.getBarColors()


def getPalette(configRef, indx):
    paletteObj = config.workingPalettes[indx]
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
def buildGrid(config):
    """Builds a flexible grid of bar blocks."""
    count = 0
    config.barBlocks = []
    delta = 0
    rows = round(config.canvasHeight / config.blockHeight)
    cols = round(config.canvasWidth / config.blockWidth)
    cols = min(cols, 80)
    gridSize = 8
    availableCoords = _create_available_coords_grid(rows, cols, gridSize)

    for row in range(len(availableCoords) - 2):
        for col in range(len(availableCoords[row])):
            if _is_valid_coord(availableCoords, row, col):
                _create_and_place_block(config, availableCoords, row, col, count, delta, gridSize)
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


def _create_and_place_block(config, availableCoords, row, col, count, delta, gridSize):
    """Creates and places a bar block at the given coordinate."""
    index = math.floor(random.uniform(0, len(config.sizeArray)))
    blockWidth = config.sizeArray[index]

    removedPointsSize = round(blockWidth / gridSize)
    if (removedPointsSize + col < len(availableCoords[row]) and
            availableCoords[row][col + removedPointsSize][2] == 1):
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
    barBlockUnit.rotation = (round(random.uniform(90 - config.rotationVariation, 90 + config.rotationVariation))
                             if count % 2 != 0 else round(random.uniform(-config.rotationVariation, config.rotationVariation)))

    paletteIndex = (math.floor(random.uniform(0, len(config.palettes)))
                    if config.mixedPalettes else config.paletteIndex)
    barBlockUnit.setUp(getPalette(config, paletteIndex), getLinePalette(config, paletteIndex))

    config.barBlocks.append(barBlockUnit)

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
def buildOverlapGrid(config):

    count = 0
    config.barBlocks = []
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
        index = math.floor(random.uniform(0, len(config.sizeArray)))
        blockWidth = config.sizeArray[index]
        # blockHeight = config.blockWidth
        barBlockUnit = Block(config, count)
        barBlockUnit.blockWidth = round(random.uniform(blockWidth - delta, blockWidth + delta))
        barBlockUnit.blockHeight = barBlockUnit.blockWidth
        barBlockUnit.xPos = item[0]
        barBlockUnit.yPos = item[1]

        barBlockUnit.barWidth = round(random.uniform(config.barWidthMin, config.barWidthMax))
        barBlockUnit.gap = round(random.uniform(config.gapWidthMin, config.gapWidthMax))
        barBlockUnit.rotation = (
            round(
                random.uniform(
                    90 - config.rotationVariation,
                    90 + config.rotationVariation,
                )
            )
            if count % 2 != 0
            else round(
                random.uniform(
                    -config.rotationVariation, config.rotationVariation
                )
            )
        )
        paletteIndex = math.floor(random.uniform(0, len(config.palettes)))
        if config.mixedPalettes:
            paletteIndex = math.floor(random.uniform(0, len(config.palettes)))
        else:
            paletteIndex = config.paletteIndex

        barBlockUnit.setUp(getPalette(config, paletteIndex), getLinePalette(config, paletteIndex))
        config.barBlocks.append(barBlockUnit)
        count += 1


# Builds uniform grid
def buildUniformGrid(config):

    count = 0
    config.barBlocks = []
    delta = 0
    index = math.floor(random.uniform(0, len(config.sizeArray)))
    blockWidth = config.sizeArray[index]
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
            barBlockUnit = Block(config, count)
            barBlockUnit.blockWidth = round(random.uniform(blockWidth - delta, blockWidth + delta))
            barBlockUnit.blockHeight = barBlockUnit.blockWidth
            barBlockUnit.xPos = lastX  # c * barBlockUnit.blockWidth
            lastX += barBlockUnit.blockWidth
            barBlockUnit.yPos = r * blockHeight

            barBlockUnit.barWidth = round(random.uniform(config.barWidthMin, config.barWidthMax))
            barBlockUnit.gap = round(random.uniform(config.gapWidthMin, config.gapWidthMax))
            if count % 2 != 0:
                barBlockUnit.rotation = round(random.uniform(90 - config.rotationVariation, 90 + config.rotationVariation))
            else:
                barBlockUnit.rotation = round(random.uniform(-config.rotationVariation, config.rotationVariation))

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


def iterate():
    global config
    config.colOverlay.stepTransition()

    config.bgColor = tuple(round(a * config.brightness) for a in (config.colOverlay.currentColor))

    redraw(config)

    # dithering movement
    if random.random() < config.filterRemappingProb:
        _extracted_from_iterate_11(config)
    if random.random() < config.blurPatchProb:
        _extracted_from_iterate_22(config)
            # print(config.blurSection)

    if random.random() < config.changeGridProb:

        _extracted_from_iterate_48(config)
    if random.random() < config.changeQuiverOnProb:
        config.deltaXVal = round(random.uniform(0, config.deltaVal))
        config.deltaYVal = round(random.uniform(0, config.deltaVal))

    if random.random() < config.changeQuiverOffProb:
        # a bit more often, things just go still
        config.deltaXVal = config.deltaYVal = 0

    # if config.useDrawingPoints :
    #     config.panelDrawing.canvasToUse = config.canvasImage
    #     config.panelDrawing.render()
    # else:
    #     config.render(config.canvasImage, 0, 0, config.canvasWidth, config.canvasHeight)
    config.render(config.canvasImage, 0, 0, config.canvasWidth, config.canvasHeight)


# TODO Rename this here and in `iterate`
def _extracted_from_iterate_48(config):
    # beeper.beep(sound=1) # integer as argument
    # change the palette - used if the mixed palettes option is False and the
    # palette override is False
    config.paletteIndex = math.floor(random.uniform(0, len(config.palettes)))

    # Decide what changes

    # paletteOverride sustitutes a fixed palette for a
    # randomized HSV one

    if random.random() < config.paletteOverrideProb:
        config.usePaletteOverride = True
        config.fixedPaletteIndex = round(random.uniform(0, len(config.paletteOverrideNames) - 1))
    else:
        config.usePaletteOverride = False

    # mixedPalette means either use one palette for all
    # the blocks or randonly choice between the set of palettes
    config.mixedPalettes = random.random() < config.mixedPaletteProb
    print(f"Change Build : {config.palettes[config.paletteIndex]}")

    # choose the layout
    index = math.floor(random.random() * len(config.gridOptions))
    if index > len(config.gridOptions):
        index = 0
    print(f"Running a :{str(config.gridOptions[index])}")
    eval(config.gridOptions[index])(config)


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
def _extracted_from_iterate_11(config):
    config.useFilters = True
    config.remapImageBlock = True

    startX = round(random.uniform(0, config.filterRemapRangeX))
    startY = round(random.uniform(0, config.filterRemapRangeY))
    endX = round(random.uniform(4, config.filterRemapminHoriSize))
    endY = round(random.uniform(4, config.filterRemapminVertSize))
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
    global config
    config.redrawSpeed = float(workConfig.get("movingpattern", "redrawSpeed"))
    config.changeGridProb = float(workConfig.get("movingpattern", "changeGridProb"))
    config.changeQuiverProb = float(workConfig.get("movingpattern", "changeQuiverProb"))

    try:
        config.changeQuiverOnProb = float(workConfig.get("movingpattern", "changeQuiverOnProb"))
        config.changeQuiverOffProb = float(workConfig.get("movingpattern", "changeQuiverOffProb"))
        # comment:
    except Exception as e:
        print(e)
        config.changeQuiverOnProb = float(workConfig.get("movingpattern", "changeQuiverProb"))
        config.changeQuiverOffProb = float(workConfig.get("movingpattern", "changeQuiverProb"))
    # end try

    config.rotationVariation = float(workConfig.get("movingpattern", "rotationVariation"))
    config.blockWidth = int(workConfig.get("movingpattern", "blockWidth"))
    config.blockHeight = int(workConfig.get("movingpattern", "blockHeight"))
    config.rows = int(workConfig.get("movingpattern", "rows"))
    config.cols = int(workConfig.get("movingpattern", "cols"))
    config.barWidthMin = int(workConfig.get("movingpattern", "barWidthMin"))
    config.barWidthMax = int(workConfig.get("movingpattern", "barWidthMax"))
    config.gapWidthMin = int(workConfig.get("movingpattern", "gapWidthMin"))
    config.gapWidthMax = int(workConfig.get("movingpattern", "gapWidthMax"))
    config.drawOutlines = workConfig.getboolean("movingpattern", "drawOutlines")

    config.blurPatchProb = float(workConfig.get("movingpattern", "blurPatchProb"))

    try:
        config.filterRemapping = workConfig.getboolean("movingpattern", "filterRemapping")
        config.filterRemappingProb = float(workConfig.get("movingpattern", "filterRemappingProb"))
        config.filterRemapminHoriSize = int(workConfig.get("movingpattern", "filterRemapminHoriSize"))
        config.filterRemapminVertSize = int(workConfig.get("movingpattern", "filterRemapminVertSize"))
        config.filterRemapRangeX = int(workConfig.get("movingpattern", "filterRemapRangeX"))
        config.filterRemapRangeY = int(workConfig.get("movingpattern", "filterRemapRangeY"))
    except Exception as e:
        print(e)
        config.filterRemapping = False
        config.filterRemappingProb = 0.0
        config.filterRemapminHoriSize = 24
        config.filterRemapminVertSize = 24
        config.filterRemapRangeX = config.canvasWidth
        config.filterRemapRangeY = config.canvasHeight

    config.sizeArrayVals = workConfig.get("movingpattern", "sizeArray")
    config.sizeArray = config.sizeArrayVals.split(",")
    config.sizeArray = list(map(lambda x: int(x), config.sizeArray))

    config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.canvasDraw = ImageDraw.Draw(config.canvasImage)

    config.destinationImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))

    try:
        config.deltaXVal = int(workConfig.get("movingpattern", "deltaVal"))
        config.deltaYVal = int(workConfig.get("movingpattern", "deltaVal"))
        config.deltaVal = int(workConfig.get("movingpattern", "deltaVal"))
    except Exception as e:
        print(e)
        config.deltaXVal = 1
        config.deltaYVal = 1
        config.deltaVal = 1

    # ---------------------------------------

    try:
        config.mixedPaletteProb = float(workConfig.get("movingpattern", "mixedPaletteProb"))
        config.mixedPalettes = False
    except Exception as e:
        print(e)
        config.mixedPalettes = True
        config.mixedPaletteProb = 1.0

    try:
        config.paletteOverrideNames = workConfig.get("movingpattern", "paletteOverrideNames").split(",")
        config.paletteOverrideProb = float(workConfig.get("movingpattern", "paletteOverrideProb"))
        config.usePaletteOverride = True
        config.fixedPaletteIndex = 0
    except Exception as e:
        print(e)
        config.usePaletteOverride = False
        config.paletteOverrideProb = 0.0
        config.fixedPaletteIndex = 0

    config.palettes = workConfig.get("movingpattern", "palettes").split(",")

    config.workingPalettes = []

    for _p in config.palettes:
        plt = Palette()
        plt.name = _p
        makePalette(plt.name, plt)
        makeLinePalette(plt.name, plt)
        config.workingPalettes.append(plt)

    # Right now the background is controlled by the first palette in the list of
    # palettes to use
    config.paletteIndex = 0
    config.colOverlay = getConfigOverlay(getPalette(config, config.paletteIndex), config.usePaletteOverride)

    # ---------------------------------------

    config.gridOptions = ["buildGrid", "buildGrid", "buildUniformGrid"]

    index = math.floor(random.random() * len(config.gridOptions))
    if index > len(config.gridOptions):
        index = 0

    print(f"Running a :{str(config.gridOptions[index])}")

    eval(config.gridOptions[index])(config)

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

    if run:
        runWork()
