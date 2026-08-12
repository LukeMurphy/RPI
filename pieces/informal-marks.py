from logging import config
import random
import time
import math
from noise import *
from PIL import Image, ImageDraw
from modules import colorutils, panelDrawing
from modules import configuration
from modules.holder_director import Director
from modules.configuration import ArtWorkConfig, bcolors, pieceLogger
from modules.informal_line import InformalLine
from pieces.screen import Holder

# -------- Util Functions   -------------- #




def randomRange(a, b, rounded=False):
    if not rounded:
        return random.uniform(a, b)
    else:
        return round(random.uniform(a, b))


def getColor(r, g, b, a):
    clr = list(round(i * config.brightness) for i in [r, g, b])
    clr.append(a)
    return tuple(clr)


# ------------------------------------------#


def glitchBox(
    imageRef,
    apparentWidth,
    apparentHeight,
    imageGlitchDisplacementHorizontal,
    imageGlitchDisplacementVertical,
):

    global config

    apparentWidth = config.canvasImage.size[0]
    apparentHeight = config.canvasImage.size[1]

    dx = round(random.uniform(-imageGlitchDisplacementHorizontal, imageGlitchDisplacementHorizontal))
    dy = round(random.uniform(-imageGlitchDisplacementVertical, imageGlitchDisplacementVertical))

    sectionWidth = round(random.uniform(2, apparentWidth - dx))
    sectionHeight = round(random.uniform(2, apparentHeight - dy))

    # 95% of the time they dance together as mirrors
    try:
        if random.SystemRandom().random() < 0.97:
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
        pieceLogger(e, 1)
        pieceLogger(dx + sectionWidth, dy + sectionHeight)
    # end try


def clearbgBox():
    xPos = yPos = 0
    informalMarks.bgBoxBox = (
        xPos,
        yPos,
        xPos + config.canvasWidth,
        yPos + config.canvasHeight,
    )
    informalMarks.bgBoxFill = (0, 0, 0, 0)
    config.underLayerDraw.rectangle(informalMarks.bgBoxBox, fill=informalMarks.bgBoxFill)
    informalMarks.bgBoxColorRange = random.choice(informalMarks.activePalette.bgBoxColorRanges)


def bgColorsFilling():
    global config
    # config.useBgBox = False if config.useBgBox   else True
    # pieceLogger("bgBox")
    # xPos = config.tileSizeWidth * math.floor(random.uniform(0, config.cols))
    # yPos = config.tileSizeHeight * math.floor(random.uniform(0, config.rows))

    xPos = math.floor(random.uniform(0, config.canvasWidth))
    yPos = math.floor(random.uniform(0, config.canvasHeight))

    informalMarks.tileSizeWidth = round(random.uniform(informalMarks.bgTileSizeWidthMin, informalMarks.bgTileSizeWidthMax))
    informalMarks.tileSizeHeight = round(random.uniform(informalMarks.bgTileSizeHeightMin, informalMarks.bgTileSizeHeightMax))

    informalMarks.bgBoxBox = (
        xPos,
        yPos,
        xPos + informalMarks.tileSizeWidth,
        yPos + informalMarks.tileSizeHeight,
    )
    cR = informalMarks.bgBoxColorRange
    # print(cR)
    bgBoxFill = colorutils.getRandomColorHSV(cR[0], cR[1], cR[2], cR[3], cR[4], cR[5], cR[6], cR[7])
    # print(bgBoxFill)
    informalMarks.bgBoxFill = (
        round(config.brightness * bgBoxFill[0]),
        round(config.brightness * bgBoxFill[1]),
        round(config.brightness * bgBoxFill[2]),
        round(random.uniform(informalMarks.activePalette.bgBoxAlphaRange[0], informalMarks.activePalette.bgBoxAlphaRange[1])),
    )

    config.underLayerDraw.rectangle(informalMarks.bgBoxBox, fill=informalMarks.bgBoxFill)

    glitchIterations = round(random.uniform(informalMarks.bgGlitchCyclesMin, informalMarks.bgGlitchCyclesMax))
    for _ in range(glitchIterations):
        glitchBox(
            config.underLayer,
            config.canvasWidth,
            config.canvasHeight,
            informalMarks.bgGlitchDisplacementHorizontal,
            informalMarks.bgGlitchDisplacementVertical,
        )


# -------- Line Attribute Function --------- #


def setLineColor():
    if not informalMarks.lightMode:
        if informalMarks.lightLinesOnGround:
            return colorutils.getRandomColorHSV(
                informalMarks.activePalette.line_mid_minHue,
                informalMarks.activePalette.line_mid_maxHue,
                informalMarks.activePalette.line_mid_minSaturation,
                informalMarks.activePalette.line_mid_maxSaturation,
                informalMarks.activePalette.line_mid_minValue,
                informalMarks.activePalette.line_mid_maxValue,
                informalMarks.activePalette.line_mid_minDropHue,
                informalMarks.activePalette.line_mid_maxDropHue,
                round(random.uniform(informalMarks.activePalette.line_mid_alpha_range[0], informalMarks.activePalette.line_mid_alpha_range[1])),
                config.brightness,
            )
        else:
            return colorutils.getRandomColorHSV(
                informalMarks.activePalette.line_minHue,
                informalMarks.activePalette.line_maxHue,
                informalMarks.activePalette.line_minSaturation,
                informalMarks.activePalette.line_maxSaturation,
                informalMarks.activePalette.line_minValue,
                informalMarks.activePalette.line_maxValue,
                informalMarks.activePalette.line_minDropHue,
                informalMarks.activePalette.line_maxDropHue,
                round(random.uniform(informalMarks.activePalette.line_alpha_range[0], informalMarks.activePalette.line_alpha_range[1])),
                config.brightness,
            )
    else:
        return colorutils.getRandomColorHSV(
            informalMarks.activePalette.line_light_minHue,
            informalMarks.activePalette.line_light_maxHue,
            informalMarks.activePalette.line_light_minSaturation,
            informalMarks.activePalette.line_light_maxSaturation,
            informalMarks.activePalette.line_light_minValue,
            informalMarks.activePalette.line_light_maxValue,
            informalMarks.activePalette.line_light_minDropHue,
            informalMarks.activePalette.line_light_maxDropHue,
            round(random.uniform(informalMarks.activePalette.line_light_alpha_range[0], informalMarks.activePalette.line_light_alpha_range[1])),
            config.brightness,
        )

    # pieceLogger(f"New Line Color {config.lineColor}")


def setBGColor():

    informalMarks.activePalette = random.choice(informalMarks.paletteSets)
    pieceLogger(f"[setBGColor] NEW palette: {informalMarks.activePalette.name}")

    informalMarks.bg_alpha = round(random.uniform(informalMarks.activePalette.bg_alpha_range[0], informalMarks.activePalette.bg_alpha_range[1]))
    informalMarks.bg_minHue = informalMarks.activePalette.bg_minHue
    informalMarks.bg_maxHue = informalMarks.activePalette.bg_maxHue
    informalMarks.bg_minSaturation = informalMarks.activePalette.bg_minSaturation
    informalMarks.bg_maxSaturation = informalMarks.activePalette.bg_maxSaturation
    informalMarks.bg_minValue = informalMarks.activePalette.bg_minValue
    informalMarks.bg_maxValue = informalMarks.activePalette.bg_maxValue
    informalMarks.bg_dropHueMin = informalMarks.activePalette.bg_dropHueMin
    informalMarks.bg_dropHueMax = informalMarks.activePalette.bg_dropHueMax

    informalMarks.lineColorIsBgColor = informalMarks.activePalette.lineColorIsBgColor

    _minVal = informalMarks.bg_minValue
    _maxVal = informalMarks.bg_maxValue
    _minSat = informalMarks.bg_minSaturation
    _maxSat = informalMarks.bg_maxSaturation

    if informalMarks.lightMode:
        _minVal = 0.2
        _maxVal = 0.5
        _minSat = 0.5
        _maxSat = 0.99

    informalMarks.bgColor = colorutils.getRandomColorHSV(
        informalMarks.bg_minHue,
        informalMarks.bg_maxHue,
        _minSat,
        _maxSat,
        _minVal,
        _maxVal,
        informalMarks.bg_dropHueMin,
        informalMarks.bg_dropHueMax,
        informalMarks.bg_alpha,
        config.brightness,
    )

    if random.random() < informalMarks.lightLinesOnGroundProb:
        informalMarks.lightLinesOnGround = True
    else:
        informalMarks.lightLinesOnGround = False

    informalMarks.bgBoxColorRange = random.choice(informalMarks.activePalette.bgBoxColorRanges)


# -------- Line Functions    -------------- #


def generateMark(col, row, _lastX, _lastY, _drawingHeight, _skipMark, _markType="scribble"):

    # -------------------------------------- #
    if _markType == "scribble":
        informalLine = InformalLine()
        informalLine.curveResolution = informalMarks.curveResolution
        informalLine.backTrackRange = informalMarks.backTrackRange
        informalLine.lineColorIsBgColor = False
        informalLine.draw = config.draw
        if informalMarks.useBgBox and informalMarks.scribbleOnTop:
            informalLine.draw = config.underLayerDraw
        informalLine.lineType = 1
        informalLine.scribbleHeight = random.uniform(informalMarks.scribbleHeightRange[0], informalMarks.scribbleHeightRange[1])
        informalLine.xOffset = informalMarks.scribblexOffset + col * informalMarks.scribbleRadiusXRange[1] * informalMarks.scibbleXPacking
        informalLine.yOffset = informalMarks.scribbleyOffset + row * informalMarks.scribbleRadiusYRange[1] * informalMarks.scibbleYPacking
        informalLine.radiusX = random.uniform(informalMarks.scribbleRadiusXRange[0], informalMarks.scribbleRadiusXRange[1])
        informalLine.radiusY = random.uniform(informalMarks.scribbleRadiusYRange[0], informalMarks.scribbleRadiusYRange[1])
        informalLine.baseWidth = int(random.uniform(0, informalMarks.scribbleLineBaseWidthRange))
        informalLine.points = informalMarks.scribblePoints
        informalLine.loops = int(random.uniform(informalMarks.scribbleLoopsRange[0], informalMarks.scribbleLoopsRange[1]))
        informalLine.noiseX = random.uniform(informalMarks.scribbleNoiseXRange[0], informalMarks.scribbleNoiseXRange[1])
        informalLine.noiseY = random.uniform(informalMarks.scribbleNoiseYRange[0], informalMarks.scribbleNoiseYRange[1])
        informalLine.lineColor = setLineColor()
        if random.random() < informalMarks.scribbleAltColorProb:
            informalLine.lineColor = (int(random.uniform(40, 255)), 6, 30, 60)
        if random.random() < informalMarks.scribbleAltColorProb:
            _tVal = int(random.uniform(40, 255))
            informalLine.lineColor = (0, _tVal, _tVal, 60)
        if random.random() < informalMarks.scribbleSkipMarksProb:
            _skipMark = True

        if not _skipMark:
            informalLine.generateScribble()
            informalMarks.informalLineUnits.append(informalLine)

    # -------------------------------------- #
    if _markType == "single":
        informalLine = InformalLine()
        informalLine.lineType = 0
        informalLine.curveResolution = informalMarks.curveResolution
        informalLine.backTrackRange = informalMarks.backTrackRange
        informalLine.lineColorIsBgColor = False
        informalLine.draw = config.draw
        if informalMarks.useBgBox and informalMarks.singlesOnTop:
            informalLine.draw = config.underLayerDraw
        informalLine.baseWidthRange = informalMarks.vertLineWidthRange
        informalLine.drawingHeight = _drawingHeight
        informalLine.xOffset = _lastX + informalMarks.xOffset
        # informalLine.xOffset = col * informalMarks.markMinWidth
        informalLine.yOffset = _lastY - informalLine.drawingHeight / 4 * random.random()
        informalLine.angle = random.uniform(informalMarks.angleAltRange[0], informalMarks.angleAltRange[1])
        informalLine.pointPerLine = informalMarks.pointsPerLineCol
        informalLine.lineSpeedRange = informalMarks.lineSpeedRange
        informalLine.lineSpeedRange = informalMarks.vertLineSpeedRange
        informalLine.noiseAmplitudeRange = informalMarks.noiseAmplitudeRangeCol
        informalLine.horizontalMovementProb = informalMarks.horizontalMovementProb
        informalLine.verticalMovementProb = informalMarks.verticalMovementProb
        informalLine.lineColor = setLineColor()
        if random.random() < informalMarks.marksAltColorProb:
            informalLine.lineColor = (int(random.uniform(40, 255)), 6, 30, 60)
        if random.random() < informalMarks.marksAltColorProb:
            _tVal = int(random.uniform(40, 255))
            informalLine.lineColor = (0, _tVal, _tVal, 60)

        if not _skipMark:
            informalLine.reconfigure()
            informalLine.generateInformalLine()
            informalMarks.informalLineUnits.append(informalLine)

    # -------------------------------------- #
    if _markType == "x":
        _clr = None
        for i in range(0, 2):
            informalLine = InformalLine()
            informalLine.lineType = 0
            informalLine.curveResolution = informalMarks.curveResolution
            informalLine.backTrackRange = informalMarks.backTrackRange
            informalLine.lineColorIsBgColor = False
            informalLine.draw = config.draw
            if informalMarks.useBgBox and informalMarks.xsOnTop:
                informalLine.draw = config.underLayerDraw

            informalLine.baseWidthRange = informalMarks.vertLineWidthRange
            informalLine.drawingHeight = _drawingHeight
            informalLine.xOffset = informalMarks.xOffset + _lastX
            informalLine.yOffset = _lastY - informalLine.drawingHeight / 4 * random.random()
            informalLine.angle = random.uniform(informalMarks.angleRange[0], informalMarks.angleRange[1])
            if i == 1:
                informalLine.angle *= -1
                if random.random() < 0.5:
                    informalLine.angle = -random.uniform(informalMarks.angleRange[0], informalMarks.angleRange[1])
                informalLine.xOffset -= informalLine.drawingHeight / 2

            informalLine.pointPerLine = informalMarks.pointsPerLineCol
            informalLine.lineSpeedRange = informalMarks.lineSpeedRange
            informalLine.lineSpeedRange = informalMarks.vertLineSpeedRange
            informalLine.noiseAmplitudeRange = informalMarks.noiseAmplitudeRangeCol
            informalLine.horizontalMovementProb = informalMarks.horizontalMovementProb
            informalLine.verticalMovementProb = informalMarks.verticalMovementProb
            if i == 0:
                informalLine.lineColor = setLineColor()
                if random.random() < informalMarks.marksAltColorProb:
                    informalLine.lineColor = (int(random.uniform(40, 255)), 6, 30, 60)
                if random.random() < informalMarks.marksAltColorProb:
                    _tVal = int(random.uniform(40, 255))
                    informalLine.lineColor = (0, _tVal, _tVal, 60)
                _clr = informalLine.lineColor
            else:
                informalLine.lineColor = _clr

            if not _skipMark:
                informalLine.reconfigure()
                informalLine.generateInformalLine()
                informalMarks.informalLineUnits.append(informalLine)


# -------------------------------------- #


def setLines():
    pieceLogger(f"[setLines] New Lines:")
    # config.informalLineUnits = []
    generateMarksGrid()
    generateScribbleGrid()


def generateScribbleGrid():
    pieceLogger(f"[generateScribbleGrid] Making scribble marks")
    informalMarks.line_alpha = randomRange(informalMarks.activePalette.line_alpha_range[0], informalMarks.activePalette.line_alpha_range[1], True)
    informalMarks.bg_alpha_base = randomRange(informalMarks.activePalette.bg_alpha_range[0], informalMarks.activePalette.bg_alpha_range[1], True)

    for _row in range(0, informalMarks.scribbleRows):
        for _col in range(0, informalMarks.scribbleCols):
            _skipMark = False
            generateMark(_col, _row, 0, 0, 0, _skipMark, "scribble")
    informalMarks.numberOfinformalLines = len(informalMarks.informalLineUnits)


def generateMarksGrid():
    pieceLogger(f"[generateMarksGrid] Making Grid:  {informalMarks.drawingWidth } {informalMarks.drawingHeight }")

    informalMarks.colInterval = random.randint(int(informalMarks.colIntervalRange[0]), int(informalMarks.colIntervalRange[1]))
    informalMarks.rowInterval = random.randint(int(informalMarks.rowIntervalRange[0]), int(informalMarks.rowIntervalRange[1]))
    informalMarks.noiseAmplitudeCol = random.uniform(float(informalMarks.noiseAmplitudeRangeCol[0]), float(informalMarks.noiseAmplitudeRangeCol[1]))
    informalMarks.noiseAmplitudeRow = random.uniform(float(informalMarks.noiseAmplitudeRangeRow[0]), float(informalMarks.noiseAmplitudeRangeRow[1]))
    informalMarks.vertLineChange = randomRange(informalMarks.vertLineChangeRange[0], informalMarks.vertLineChangeRange[1])
    informalMarks.horizLineChange = randomRange(informalMarks.horizLineChangeRange[0], informalMarks.horizLineChangeRange[1])
    informalMarks.line_alpha = randomRange(informalMarks.activePalette.line_alpha_range[0], informalMarks.activePalette.line_alpha_range[1], True)
    informalMarks.bg_alpha_base = randomRange(informalMarks.activePalette.bg_alpha_range[0], informalMarks.activePalette.bg_alpha_range[1], True)

    for _row in range(informalMarks.rowInterval):
        _lastX = 0
        _lastY = informalMarks.yOffset + _row * (informalMarks.minYSpacing)
        for col in range(informalMarks.colInterval):
            _drawingHeight = informalMarks.markMinHeight + random.uniform(-informalMarks.sizeRange, informalMarks.sizeRange)
            _skipMark = False
            _altMark = False
            if random.random() < informalMarks.skipMarksProb:
                _skipMark = True
            if random.random() < informalMarks.altMarksProb:
                _altMark = True
                _drawingHeight = informalMarks.markMinHeight + random.uniform(-informalMarks.sizeRange, informalMarks.sizeRange)

            _lastX += informalMarks.markMinWidth + informalMarks.minXSpacing
            if col == 0:
                _lastX /= 2

            if _altMark:
                generateMark(col, _row, _lastX, _lastY, _drawingHeight, _skipMark, "single")
            else:
                generateMark(col, _row, _lastX, _lastY, _drawingHeight, _skipMark, "x")

    informalMarks.numberOfinformalLines = len(informalMarks.informalLineUnits)
    # pieceLogger(f"New Lines {config.numberOfinformalLines}")


def changeLine():
    _changeLine = random.randint(0, len(informalMarks.informalLineUnits) - 1)
    _lineUnit: InformalLine = informalMarks.informalLineUnits[_changeLine]
    if _lineUnit.lineType == 0:
        _lineUnit.reconfigure()


def drawTheBG():
    informalMarks.bgColor = (informalMarks.bgColor[0], informalMarks.bgColor[1], informalMarks.bgColor[2], round(informalMarks.bg_alpha))
    informalMarks.draw.rectangle((0, 0, informalMarks.drawingWidth, informalMarks.drawingHeight), fill=informalMarks.bgColor)


def updateLines():
    global config

    for _informalLineUnitIndex in range(0, len(informalMarks.informalLineUnits)):
        _lineUnit: InformalLine
        _lineUnit = informalMarks.informalLineUnits[_informalLineUnitIndex]
        if _lineUnit.lineType == 0:
            _lineUnit.drawTheLineComplete()
            # _lineUnit.drawLinePoints()
        if _lineUnit.lineType == 1:
            _lineUnit.drawTheLineComplete()


# ---- looping and redrawing --------


def runWork():
    global config
    _config : ArtWorkConfig
    _config = config

    print(bcolors.OKGREEN + "** " + bcolors.BOLD)
    print("Running informalMarksGrid.py")
    print(bcolors.ENDC)
    _config.debugSelf()

    while _config.isRunning == True:
        _config.directorController.checkTime()
        if _config.directorController.advance:
            iterate()

        if _config.standAlone == False:
            _config.callBack()

        time.sleep(_config.redrawSpeed)


def reDraw():

    if random.random() < informalMarks.useBgBoxProb and informalMarks.useBgBox:
        bgColorsFilling()

    if informalMarks.bg_alpha < informalMarks.bg_alpha_base:
        informalMarks.bg_alpha += informalMarks.bg_alpha_returnrate

    if informalMarks.bg_alpha > informalMarks.bg_alpha_base:
        informalMarks.bg_alpha = informalMarks.bg_alpha_base

    drawTheBG()
    updateLines()

    # in-place refresh of mark
    for _u in range(informalMarks.numberOfinformalLines):
        if random.random() < informalMarks.changeLinesProb and not informalMarks.noChange:
            _informalLine: InformalLine = informalMarks.informalLineUnits[_u]
            if _informalLine.lineType == 0:
                _informalLine.reconfigure()
                _informalLine.generateInformalLine()

            if _informalLine.lineType == 1:
                _informalLine.generateScribble()

    # all marks changed
    if random.random() < informalMarks.changeAllLinesProb and not informalMarks.noChange:
        informalMarks.lightMode = False if random.random() > informalMarks.lightModeProb else True
        informalMarks.bg_alpha = 0
        clearbgBox()
        setBGColor()
        setLines()
        # doFrame()
        pieceLogger(f"[reDraw] change ALL LINES  lightMode:{informalMarks.lightMode} {informalMarks.bg_alpha}")

    if random.random() < informalMarks.pauseProb:
        informalMarks.noChange = True

    if random.random() < informalMarks.unpauseProb:
        informalMarks.noChange = False

    if random.random() < informalMarks.clearbgBoxProb:
        clearbgBox()


def iterate():
    global config, overlayControls
    reDraw()

    ########### RENDERING AS A MOCKUP OR AS REAL ###########
    # if config.useDrawingPoints == True:
    #     config.panelDrawing.canvasToUse = config.image
    #     config.panelDrawing.render()

    config.destinationImage.paste(config.image, (0, 0), config.image)
    config.destinationImage.paste(config.underLayer, (0, 0), config.underLayer)
    # config.destinationImage.paste(config.frameLayer, (0, 0), config.frameLayer)

    config.render(config.destinationImage, 0, 0)


# ---- initialize  -----------------


def loadConfigValue(obj, workConfig, section, option, default, type_converter):
    try:
        if type_converter == bool:
            setattr(obj, option, type_converter(workConfig.getboolean(section, option)))
        else:
            setattr(obj, option, type_converter(workConfig.get(section, option)))
    except Exception as e:
        pieceLogger(f" ==> Config value not loaded: {option} ==> will be set to {default} \n  {e}", 1)
        setattr(obj, option, default)


def loadColorConfigs():

    paletteList = workConfig.get("informalMarksGrid", "paletteSets").split(",")

    for p in paletteList:
        palette = Holder(config)

        palette.name = p
        palette.line_minHue = float(workConfig.get(p, "line_minHue"))
        palette.line_maxHue = float(workConfig.get(p, "line_maxHue"))
        palette.line_maxSaturation = float(workConfig.get(p, "line_maxSaturation"))
        palette.line_minSaturation = float(workConfig.get(p, "line_minSaturation"))
        palette.line_minValue = float(workConfig.get(p, "line_minValue"))
        palette.line_maxValue = float(workConfig.get(p, "line_maxValue"))
        palette.line_minDropHue = float(workConfig.get(p, "line_minDropHue", fallback=0))
        palette.line_maxDropHue = float(workConfig.get(p, "line_maxDropHue", fallback=0))
        palette.line_alpha_range = [int(x) for x in workConfig.get(p, "line_alpha_range", fallback="18,180").split(",")]

        palette.line_mid_minHue = float(workConfig.get(p, "line_mid_minHue", fallback=palette.line_minHue))
        palette.line_mid_maxHue = float(workConfig.get(p, "line_mid_maxHue", fallback=palette.line_maxHue))
        palette.line_mid_minSaturation = float(workConfig.get(p, "line_mid_minSaturation", fallback=palette.line_minSaturation))
        palette.line_mid_maxSaturation = float(workConfig.get(p, "line_mid_maxSaturation", fallback=palette.line_maxSaturation))
        palette.line_mid_minValue = float(workConfig.get(p, "line_mid_minValue", fallback=palette.line_minValue))
        palette.line_mid_maxValue = float(workConfig.get(p, "line_mid_maxValue", fallback=palette.line_maxValue))
        palette.line_mid_minDropHue = float(workConfig.get(p, "line_mid_minDropHue", fallback=0))
        palette.line_mid_maxDropHue = float(workConfig.get(p, "line_mid_maxDropHue", fallback=0))
        palette.line_mid_alpha_range = [int(x) for x in workConfig.get(p, "line_mid_alpha_range", fallback="150,190").split(",")]

        palette.line_light_minHue = float(workConfig.get(p, "line_light_minHue"))
        palette.line_light_maxHue = float(workConfig.get(p, "line_light_maxHue"))
        palette.line_light_maxSaturation = float(workConfig.get(p, "line_light_maxSaturation"))
        palette.line_light_minSaturation = float(workConfig.get(p, "line_light_minSaturation"))
        palette.line_light_minValue = float(workConfig.get(p, "line_light_minValue"))
        palette.line_light_maxValue = float(workConfig.get(p, "line_light_maxValue"))
        palette.line_light_minDropHue = float(workConfig.get(p, "line_light_minDropHue", fallback=0))
        palette.line_light_maxDropHue = float(workConfig.get(p, "line_light_maxDropHue", fallback=0))
        palette.line_light_alpha_range = [int(x) for x in workConfig.get(p, "line_light_alpha_range", fallback="150,190").split(",")]

        palette.bg_minHue = float(workConfig.get(p, "bg_minHue"))
        palette.bg_maxHue = float(workConfig.get(p, "bg_maxHue"))
        palette.bg_maxSaturation = float(workConfig.get(p, "bg_maxSaturation"))
        palette.bg_minSaturation = float(workConfig.get(p, "bg_minSaturation"))
        palette.bg_minValue = float(workConfig.get(p, "bg_minValue"))
        palette.bg_maxValue = float(workConfig.get(p, "bg_maxValue"))
        palette.bg_dropHueMin = float(workConfig.get(p, "bg_dropHueMin", fallback="0"))
        palette.bg_dropHueMax = float(workConfig.get(p, "bg_dropHueMax", fallback="0"))
        palette.bg_alpha_range = [int(x) for x in workConfig.get(p, "bg_alpha_range", fallback="10,40").split(",")]
        palette.bg_alpha = round(random.uniform(palette.bg_alpha_range[0], palette.bg_alpha_range[1]))
        palette.bg_alpha_base = 20

        palette.lineColorIsBgColor = workConfig.getboolean(p, "lineColorIsBgColor", fallback=False)

        palette.bgBoxColorRanges = []
        bgBoxColorRanges = workConfig.get(p, "bgBoxColorRanges").split("|")
        for _bgelement in bgBoxColorRanges:
            bgRange = list(
                map(
                    lambda x: float(x),
                    _bgelement.split(","),
                )
            )
            palette.bgBoxColorRanges.append(bgRange)
        palette.bgBoxColorRange = random.choice(palette.bgBoxColorRanges)
        palette.bgBoxAlphaRange = tuple(
            map(
                lambda x: int(x),
                workConfig.get(p, "bgBoxAlphaRange").split(","),
            )
        )
        informalMarks.paletteSets.append(palette)

    informalMarks.activePalette = random.choice(informalMarks.paletteSets)


class InformalMarks:
    config
    paletteSets = []
    informalLineUnits = []
    activePalette =  None

    def __init__(self, config):
        self.config = config

    def setUp(self,workConfig):
        self.image = Image.new("RGBA", (self.config.canvasWidth, self.config.canvasHeight))
        self.imageDraw = ImageDraw.Draw(self.image)
        self.draw = ImageDraw.Draw(self.image)

        self.canvasImage = Image.new("RGBA", (self.config.canvasWidth, self.config.canvasHeight))

        self.destinationImage = Image.new("RGBA", (self.config.canvasWidth, self.config.canvasHeight))
        self.destinationImageDraw = ImageDraw.Draw(self.destinationImage)

        self.overlayImage = Image.new("RGBA", (self.config.canvasWidth, self.config.canvasHeight))
        self.overlayImageDraw = ImageDraw.Draw(self.overlayImage)

        self.underLayer = Image.new("RGBA", (self.config.canvasWidth, self.config.canvasHeight))
        self.underLayerDraw = ImageDraw.Draw(self.underLayer)

        self.drawingWidth = int(workConfig.get("informalMarksGrid", "drawingWidth", fallback=f"{self.config.canvasWidth}"))
        self.drawingHeight = int(workConfig.get("informalMarksGrid", "drawingHeight", fallback=f"{self.config.canvasHeight}"))

        self.largestDim = max(self.drawingWidth, self.drawingHeight)

        # refinements for setting points per column and row so amplitude of noise can be adjusted to be more even if aspect ratio is more extreme - e.g narrow beam
        # but also, lower number makes the line more purely rectilinear so can give a greater focus to one directions linearity
        self.pointsPerLine = int(workConfig.get("informalMarksGrid", "pointsPerLine"))
        self.pointsPerLineCol = int(workConfig.get("informalMarksGrid", "pointsPerLineCol", fallback=self.pointsPerLine))
        self.pointsPerLineRow = int(workConfig.get("informalMarksGrid", "pointsPerLineRow", fallback=self.pointsPerLine))

        # adjust higher for higer resolution
        self.curveResolution = int(workConfig.get("informalMarksGrid", "curveResolution", fallback=10))

        # not really used - was used in first iteration using Perlin Noise
        self.noiseSeed = random.random()

        # if the shape is not single-lines, will be determined by rows and columns
        self.numberOfinformalLines = int(workConfig.get("informalMarksGrid", "numberOfinformalLines", fallback="3"))
        # the edge spacing - critical to making the drawing as the edges matter more than the sum of the lines
        self.xOffset = int(workConfig.get("informalMarksGrid", "xOffset"))
        self.yOffset = int(workConfig.get("informalMarksGrid", "yOffset"))

        # for single linesneSpeed
        self.renderLinesAsEnvelope = workConfig.getboolean("informalMarksGrid", "renderLinesAsEnvelope", fallback=False)
        self.drawVertical = workConfig.getboolean("informalMarksGrid", "drawVertical", fallback=True)
        self.drawHorizontal = workConfig.getboolean("informalMarksGrid", "drawHorizontal", fallback=True)
        self.singleLineRegularSpacing = workConfig.getboolean("informalMarksGrid", "singleLineRegularSpacing", fallback=False)
        self.drawingHeightRange = [int(x) for x in workConfig.get("informalMarksGrid", "drawingHeightRange", fallback="18,180").split(",")]
        self.lineSpeedRange = [int(x) for x in workConfig.get("informalMarksGrid", "lineSpeedRange", fallback="1,20").split(",")]
        self.baseWidthRange = [int(x) for x in workConfig.get("informalMarksGrid", "baseWidthRange", fallback="18,180").split(",")]
        self.backTrackRange = [int(x) for x in workConfig.get("informalMarksGrid", "backTrackRange", fallback="0,0").split(",")]

        self.verticalMovement = workConfig.getboolean("informalMarksGrid", "verticalMovement", fallback=False)
        self.horizontalMovement = workConfig.getboolean("informalMarksGrid", "horizontalMovement", fallback=False)
        self.horizontalMovementProb = float(workConfig.get("informalMarksGrid", "horizontalMovementProb", fallback="0.25"))
        self.verticalMovementProb = float(workConfig.get("informalMarksGrid", "verticalMovementProb", fallback="0.25"))
        self.singleLinesAngle = float(workConfig.get("informalMarksGrid", "singleLinesAngle", fallback="0"))
        self.tangleProb = float(workConfig.get("informalMarksGrid", "tangleProb", fallback="0"))

        if self.singleLineRegularSpacing:
            _hspacing = round(self.drawingWidth / (self.numberOfinformalLines + 2))
            _vspacing = round(self.drawingHeight / (self.numberOfinformalLines + 2))
            self.rowIntervalRange = [_vspacing, _vspacing]
            self.colIntervalRange = [_hspacing, _hspacing]

        # the +/- variability of the points
        self.noiseAmplitudeRangeRow = [float(x) for x in workConfig.get("informalMarksGrid", "noiseAmplitudeRangeRow", fallback="1,1").split(",")]
        self.noiseAmplitudeRangeCol = [float(x) for x in workConfig.get("informalMarksGrid", "noiseAmplitudeRangeCol", fallback="1,1").split(",")]
        self.colFirst = workConfig.getboolean("informalMarksGrid", "colFirst", fallback=False)

        self.vertLineChange = float(workConfig.get("informalMarksGrid", "vertLineChange", fallback=0.01))
        self.horizLineChange = float(workConfig.get("informalMarksGrid", "horizLineChange", fallback=0.01))

        self.vertLineChangeRange = [float(x) for x in workConfig.get("informalMarksGrid", "vertLineChangeRange", fallback=".05,.6").split(",")]
        self.horizLineChangeRange = [float(x) for x in workConfig.get("informalMarksGrid", "horizLineChangeRange", fallback=".05,.6").split(",")]

        self.vertlineSpeedRange = [int(x) for x in workConfig.get("informalMarksGrid", "lineSpeedRange", fallback="1,20").split(",")]
        self.horzlineSpeedRange = [int(x) for x in workConfig.get("informalMarksGrid", "lineSpeedRange", fallback="1,20").split(",")]

        self.rowIntervalRange = [int(x) for x in workConfig.get("informalMarksGrid", "rowIntervalRange", fallback="1,1").split(",")]
        self.colIntervalRange = [int(x) for x in workConfig.get("informalMarksGrid", "colIntervalRange", fallback="1,1").split(",")]

        self.horizLineSpeedRange = [int(x) for x in workConfig.get("informalMarksGrid", "horizLineSpeedRange", fallback="1,20").split(",")]
        self.vertLineSpeedRange = [int(x) for x in workConfig.get("informalMarksGrid", "vertLineSpeedRange", fallback="1,20").split(",")]
        self.vertLineWidthRange = [int(x) for x in workConfig.get("informalMarksGrid", "vertLineWidthRange", fallback="18,180").split(",")]
        self.horizBaseWidthRange = [int(x) for x in workConfig.get("informalMarksGrid", "horizBaseWidthRange", fallback="18,180").split(",")]

        self.angleRange = [float(x) for x in workConfig.get("informalMarksGrid", "angleRange", fallback="0,0").split(",")]
        self.angleAltRange = [float(x) for x in workConfig.get("informalMarksGrid", "angleAltRange", fallback="-10,10").split(",")]
        self.sizeRange = float(workConfig.get("informalMarksGrid", "sizeRange", fallback=10))
        self.minXSpacing = float(workConfig.get("informalMarksGrid", "minXSpacing", fallback=-3))
        self.minYSpacing = float(workConfig.get("informalMarksGrid", "minYSpacing", fallback=-3))
        self.skipMarksProb = float(workConfig.get("informalMarksGrid", "skipMarksProb", fallback=0.25))
        self.altMarksProb = float(workConfig.get("informalMarksGrid", "altMarksProb", fallback=0.5))
        self.markMinHeight = float(workConfig.get("informalMarksGrid", "markMinHeight", fallback=24))
        self.markMinWidth = float(workConfig.get("informalMarksGrid", "markMinWidth", fallback=24))

        self.scribblexOffset = int(workConfig.get("informalMarksGrid", "scribblexOffset", fallback=0))
        self.scribbleyOffset = int(workConfig.get("informalMarksGrid", "scribbleyOffset", fallback=0))
        self.scibbleXPacking = float(workConfig.get("informalMarksGrid", "scibbleXPacking", fallback=0))
        self.scibbleYPacking = float(workConfig.get("informalMarksGrid", "scibbleYPacking", fallback=0))

        self.scribbleSkipMarksProb = float(workConfig.get("informalMarksGrid", "scribbleSkipMarksProb", fallback=0))
        self.scribbleAltMarksProb = float(workConfig.get("informalMarksGrid", "scribbleAltMarksProb", fallback=0))

        self.scribbleHeightRange = [float(x) for x in workConfig.get("informalMarksGrid", "scribbleHeightRange", fallback="4,10").split(",")]
        self.scribbleLineBaseWidthRange = int(workConfig.get("informalMarksGrid", "scribbleLineBaseWidthRange", fallback=1))

        self.scribbleRadiusXRange = [float(x) for x in workConfig.get("informalMarksGrid", "scribbleRadiusXRange", fallback="4,8").split(",")]
        self.scribbleRadiusYRange = [float(x) for x in workConfig.get("informalMarksGrid", "scribbleRadiusYRange", fallback="8,24").split(",")]

        self.scribblePoints = int(workConfig.get("informalMarksGrid", "scribblePoints", fallback=8))
        self.scribbleLoopsRange = [int(x) for x in workConfig.get("informalMarksGrid", "scribbleLoopsRange", fallback="2,2").split(",")]

        self.scribbleNoiseXRange = [float(x) for x in workConfig.get("informalMarksGrid", "anglscribbleNoiseXRangeeRange", fallback="5,5").split(",")]
        self.scribbleNoiseYRange = [float(x) for x in workConfig.get("informalMarksGrid", "scribbleNoiseYRange", fallback="5,5").split(",")]

        self.scribbleRows = int(workConfig.get("informalMarksGrid", "scribbleRows", fallback=8))
        self.scribbleCols = int(workConfig.get("informalMarksGrid", "scribbleCols", fallback=8))

        self.marksAltColorProb = float(workConfig.get("informalMarksGrid", "marksAltColorProb", fallback=0.04))
        self.scribbleAltColorProb = float(workConfig.get("informalMarksGrid", "scribbleAltColorProb", fallback=0.04))
        self.changeLinesProb = float(workConfig.get("informalMarksGrid", "changeLinesProb", fallback=0.01))
        self.changeAllLinesProb = float(workConfig.get("informalMarksGrid", "changeAllLinesProb", fallback=0.01))
        # probablility background changes
        self.changeBGProb = float(workConfig.get("informalMarksGrid", "changeBGProb", fallback=0.001))
        self.pauseProb = float(workConfig.get("informalMarksGrid", "pauseProb", fallback=0.0001))
        self.unpauseProb = float(workConfig.get("informalMarksGrid", "unpauseProb", fallback=0.0001))
        self.noChange = False

        # overrides the variable background and line alpha changes and fixes at one value the rate at which the vertical and horizontal lines
        self.useSingleMode = workConfig.getboolean("informalMarksGrid", "useSingleMode", fallback=True)

        self.scribbleOnTop = workConfig.getboolean("informalMarksGrid", "scribbleOnTop", fallback=True)
        self.singlesOnTop = workConfig.getboolean("informalMarksGrid", "singlesOnTop", fallback=False)
        self.xsOnTop = workConfig.getboolean("informalMarksGrid", "xsOnTop", fallback=False)

        # light lines on background - more like a drawing on a screen
        self.lightMode = workConfig.getboolean("informalMarksGrid", "lightMode", fallback=False)
        self.lightModeProb = float(workConfig.get("informalMarksGrid", "lightModeProb", fallback=1.0))
        self.bg_alpha_returnrate = float(workConfig.get("informalMarksGrid", "bg_alpha_returnrate", fallback=2.0))
        self.lightLinesOnGroundProb = float(workConfig.get("informalMarksGrid", "lightLinesOnGroundProb", fallback=0.0))
        self.lightLinesOnGround = workConfig.getboolean("informalMarksGrid", "lightLinesOnGround", fallback=False)

        # really there are 3 modes - black/dark lines on lighter ground, mid to light lines on lighter ground, light lines on dark ground
        self.rebuildingVerticals = False

        self.useBgBox = workConfig.getboolean("informalMarksGrid", "forcebgBox")
        self.useBgBoxProb = float(workConfig.get("informalMarksGrid", "useBgBoxProb"))
        self.bgBoxBox = tuple(map(lambda x: int(x), workConfig.get("informalMarksGrid", "bgBoxBox").split(",")))
        self.renderImageFullOverlay = Image.new("RGBA", (self.config.canvasWidth, self.config.canvasHeight))
        self.renderDrawOver = ImageDraw.Draw(self.renderImageFullOverlay)
        self.bgBoxFill = (100, 0, 80, 100)

        self.bgTileSizeWidthMin = float(workConfig.get("informalMarksGrid", "bgTileSizeWidthMin"))
        self.bgTileSizeWidthMax = float(workConfig.get("informalMarksGrid", "bgTileSizeWidthMax"))
        self.bgTileSizeHeightMin = float(workConfig.get("informalMarksGrid", "bgTileSizeHeightMin"))
        self.bgTileSizeHeightMax = float(workConfig.get("informalMarksGrid", "bgTileSizeHeightMax"))

        self.clearbgBoxProb = float(workConfig.get("informalMarksGrid", "clearbgBoxProb"))
        self.bgGlitchCyclesMin = float(workConfig.get("informalMarksGrid", "bgGlitchCyclesMin"))
        self.bgGlitchCyclesMax = float(workConfig.get("informalMarksGrid", "bgGlitchCyclesMax"))
        self.bgGlitchDisplacementHorizontal = float(workConfig.get("informalMarksGrid", "bgGlitchDisplacementHorizontal"))
        self.bgGlitchDisplacementVertical = float(workConfig.get("informalMarksGrid", "bgGlitchDisplacementVertical"))

        self.pauseProb = float(workConfig.get("informalMarksGrid", "pauseProb", fallback=".001"))
        # config.backgroundColorChangeProb = float(workConfig.get("informalMarksGrid", "backgroundColorChangeProb", fallback=".001"))

        self.initialRunsOfBgBlocks = int(workConfig.get("informalMarksGrid", "initialRunsOfBgBlocks", fallback=0))
        

def main(run=True):
    global config 
    global workConfig
    global overlayControls
    global informalMarks

    informalMarks = InformalMarks(config)
    informalMarks.setUp(workConfig)

    config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.imageDraw = ImageDraw.Draw(config.image)
    config.draw = ImageDraw.Draw(config.image)

    config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))

    config.destinationImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.destinationImageDraw = ImageDraw.Draw(config.destinationImage)

    config.overlayImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.overlayImageDraw = ImageDraw.Draw(config.overlayImage)

    config.underLayer = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.underLayerDraw = ImageDraw.Draw(config.underLayer)


    loadColorConfigs()
    setLines()

    informalMarks.lineColor = setLineColor()
    setBGColor()

    # enFramingSetup()

    if informalMarks.useBgBox:
        for _ in range(informalMarks.initialRunsOfBgBlocks):
            bgColorsFilling()

    ### THIS IS USED AS WAY TO MOCKUP A CONFIGURATION OF RECTANGULAR PANELS
    panelDrawing.mockupBlock(config, workConfig)
    #### Need to add something like this at final render call  as well
    """ 
        ########### RENDERING AS A MOCKUP OR AS REAL ###########
        if config.useDrawingPoints == True :
            config.panelDrawing.canvasToUse = config.renderImageFull
            config.panelDrawing.render()
        else :
            #config.render(config.canvasImage, 0, 0, config.canvasWidth, config.canvasHeight)
            #config.render(config.image, 0, 0)
            config.render(config.renderImageFull, 0, 0)
    """

    # managing speed of animation and framerate
    config.redrawSpeed = float(workConfig.get("informalMarksGrid", "redrawSpeed", fallback=0.02))
    config.slotRate = float(workConfig.get("informalMarksGrid", "slotRate", fallback=0.03))
    config.directorController = Director(config)
    config.directorController.slotRate = config.slotRate

    if run:
        runWork()
