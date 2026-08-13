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
    infrmlMarksMngr.bgBoxBox = (
        xPos,
        yPos,
        xPos + config.canvasWidth,
        yPos + config.canvasHeight,
    )
    infrmlMarksMngr.bgBoxFill = (0, 0, 0, 0)
    config.underLayerDraw.rectangle(infrmlMarksMngr.bgBoxBox, fill=infrmlMarksMngr.bgBoxFill)
    infrmlMarksMngr.bgBoxColorRange = random.choice(infrmlMarksMngr.activePalette.bgBoxColorRanges)


def bgColorsFilling():
    global config
    # config.useBgBox = False if config.useBgBox   else True
    # pieceLogger("bgBox")
    # xPos = config.tileSizeWidth * math.floor(random.uniform(0, config.cols))
    # yPos = config.tileSizeHeight * math.floor(random.uniform(0, config.rows))

    xPos = math.floor(random.uniform(0, config.canvasWidth))
    yPos = math.floor(random.uniform(0, config.canvasHeight))

    infrmlMarksMngr.tileSizeWidth = round(random.uniform(infrmlMarksMngr.bgTileSizeWidthMin, infrmlMarksMngr.bgTileSizeWidthMax))
    infrmlMarksMngr.tileSizeHeight = round(random.uniform(infrmlMarksMngr.bgTileSizeHeightMin, infrmlMarksMngr.bgTileSizeHeightMax))

    infrmlMarksMngr.bgBoxBox = (
        xPos,
        yPos,
        xPos + infrmlMarksMngr.tileSizeWidth,
        yPos + infrmlMarksMngr.tileSizeHeight,
    )
    cR = infrmlMarksMngr.bgBoxColorRange
    # print(cR)
    bgBoxFill = colorutils.getRandomColorHSV(cR[0], cR[1], cR[2], cR[3], cR[4], cR[5], cR[6], cR[7])
    # print(bgBoxFill)
    infrmlMarksMngr.bgBoxFill = (
        round(config.brightness * bgBoxFill[0]),
        round(config.brightness * bgBoxFill[1]),
        round(config.brightness * bgBoxFill[2]),
        round(random.uniform(infrmlMarksMngr.activePalette.bgBoxAlphaRange[0], infrmlMarksMngr.activePalette.bgBoxAlphaRange[1])),
    )

    config.underLayerDraw.rectangle(infrmlMarksMngr.bgBoxBox, fill=infrmlMarksMngr.bgBoxFill)

    glitchIterations = round(random.uniform(infrmlMarksMngr.bgGlitchCyclesMin, infrmlMarksMngr.bgGlitchCyclesMax))
    for _ in range(glitchIterations):
        glitchBox(
            config.underLayer,
            config.canvasWidth,
            config.canvasHeight,
            infrmlMarksMngr.bgGlitchDisplacementHorizontal,
            infrmlMarksMngr.bgGlitchDisplacementVertical,
        )


# -------- Line Attribute Function --------- #


def setLineColor():
    if not infrmlMarksMngr.lightMode:
        if infrmlMarksMngr.lightLinesOnGround:
            return colorutils.getRandomColorHSV(
                infrmlMarksMngr.activePalette.line_mid_minHue,
                infrmlMarksMngr.activePalette.line_mid_maxHue,
                infrmlMarksMngr.activePalette.line_mid_minSaturation,
                infrmlMarksMngr.activePalette.line_mid_maxSaturation,
                infrmlMarksMngr.activePalette.line_mid_minValue,
                infrmlMarksMngr.activePalette.line_mid_maxValue,
                infrmlMarksMngr.activePalette.line_mid_minDropHue,
                infrmlMarksMngr.activePalette.line_mid_maxDropHue,
                round(random.uniform(infrmlMarksMngr.activePalette.line_mid_alpha_range[0], infrmlMarksMngr.activePalette.line_mid_alpha_range[1])),
                config.brightness,
            )
        else:
            return colorutils.getRandomColorHSV(
                infrmlMarksMngr.activePalette.line_minHue,
                infrmlMarksMngr.activePalette.line_maxHue,
                infrmlMarksMngr.activePalette.line_minSaturation,
                infrmlMarksMngr.activePalette.line_maxSaturation,
                infrmlMarksMngr.activePalette.line_minValue,
                infrmlMarksMngr.activePalette.line_maxValue,
                infrmlMarksMngr.activePalette.line_minDropHue,
                infrmlMarksMngr.activePalette.line_maxDropHue,
                round(random.uniform(infrmlMarksMngr.activePalette.line_alpha_range[0], infrmlMarksMngr.activePalette.line_alpha_range[1])),
                config.brightness,
            )
    else:
        return colorutils.getRandomColorHSV(
            infrmlMarksMngr.activePalette.line_light_minHue,
            infrmlMarksMngr.activePalette.line_light_maxHue,
            infrmlMarksMngr.activePalette.line_light_minSaturation,
            infrmlMarksMngr.activePalette.line_light_maxSaturation,
            infrmlMarksMngr.activePalette.line_light_minValue,
            infrmlMarksMngr.activePalette.line_light_maxValue,
            infrmlMarksMngr.activePalette.line_light_minDropHue,
            infrmlMarksMngr.activePalette.line_light_maxDropHue,
            round(random.uniform(infrmlMarksMngr.activePalette.line_light_alpha_range[0], infrmlMarksMngr.activePalette.line_light_alpha_range[1])),
            config.brightness,
        )

    # pieceLogger(f"New Line Color {config.lineColor}")


def setBGColor():

    infrmlMarksMngr.activePalette = random.choice(infrmlMarksMngr.paletteSets)
    pieceLogger(f"[setBGColor] NEW palette: {infrmlMarksMngr.activePalette.name}")

    infrmlMarksMngr.bg_alpha = round(random.uniform(infrmlMarksMngr.activePalette.bg_alpha_range[0], infrmlMarksMngr.activePalette.bg_alpha_range[1]))
    infrmlMarksMngr.bg_minHue = infrmlMarksMngr.activePalette.bg_minHue
    infrmlMarksMngr.bg_maxHue = infrmlMarksMngr.activePalette.bg_maxHue
    infrmlMarksMngr.bg_minSaturation = infrmlMarksMngr.activePalette.bg_minSaturation
    infrmlMarksMngr.bg_maxSaturation = infrmlMarksMngr.activePalette.bg_maxSaturation
    infrmlMarksMngr.bg_minValue = infrmlMarksMngr.activePalette.bg_minValue
    infrmlMarksMngr.bg_maxValue = infrmlMarksMngr.activePalette.bg_maxValue
    infrmlMarksMngr.bg_dropHueMin = infrmlMarksMngr.activePalette.bg_dropHueMin
    infrmlMarksMngr.bg_dropHueMax = infrmlMarksMngr.activePalette.bg_dropHueMax

    infrmlMarksMngr.lineColorIsBgColor = infrmlMarksMngr.activePalette.lineColorIsBgColor

    _minVal = infrmlMarksMngr.bg_minValue
    _maxVal = infrmlMarksMngr.bg_maxValue
    _minSat = infrmlMarksMngr.bg_minSaturation
    _maxSat = infrmlMarksMngr.bg_maxSaturation

    if infrmlMarksMngr.lightMode:
        _minVal = 0.2
        _maxVal = 0.5
        _minSat = 0.5
        _maxSat = 0.99

    infrmlMarksMngr.bgColor = colorutils.getRandomColorHSV(
        infrmlMarksMngr.bg_minHue,
        infrmlMarksMngr.bg_maxHue,
        _minSat,
        _maxSat,
        _minVal,
        _maxVal,
        infrmlMarksMngr.bg_dropHueMin,
        infrmlMarksMngr.bg_dropHueMax,
        infrmlMarksMngr.bg_alpha,
        config.brightness,
    )

    if random.random() < infrmlMarksMngr.lightLinesOnGroundProb:
        infrmlMarksMngr.lightLinesOnGround = True
    else:
        infrmlMarksMngr.lightLinesOnGround = False

    infrmlMarksMngr.bgBoxColorRange = random.choice(infrmlMarksMngr.activePalette.bgBoxColorRanges)


# -------- Line Functions    -------------- #


def generateMark(col, row, _lastX, _lastY, _drawingHeight, _skipMark, _markType="scribble"):

    # -------------------------------------- #
    if _markType == "scribble":
        informalLine = InformalLine()
        informalLine.curveResolution = infrmlMarksMngr.curveResolution
        informalLine.backTrackRange = infrmlMarksMngr.backTrackRange
        informalLine.lineColorIsBgColor = False
        informalLine.draw = config.draw
        if infrmlMarksMngr.useBgBox and infrmlMarksMngr.scribbleOnTop:
            informalLine.draw = config.underLayerDraw
        informalLine.lineType = 1
        informalLine.scribbleHeight = random.uniform(infrmlMarksMngr.scribbleHeightRange[0], infrmlMarksMngr.scribbleHeightRange[1])
        informalLine.xOffset = infrmlMarksMngr.scribblexOffset + col * infrmlMarksMngr.scribbleRadiusXRange[1] * infrmlMarksMngr.scibbleXPacking
        informalLine.yOffset = infrmlMarksMngr.scribbleyOffset + row * infrmlMarksMngr.scribbleRadiusYRange[1] * infrmlMarksMngr.scibbleYPacking
        informalLine.radiusX = random.uniform(infrmlMarksMngr.scribbleRadiusXRange[0], infrmlMarksMngr.scribbleRadiusXRange[1])
        informalLine.radiusY = random.uniform(infrmlMarksMngr.scribbleRadiusYRange[0], infrmlMarksMngr.scribbleRadiusYRange[1])
        informalLine.baseWidth = int(random.uniform(0, infrmlMarksMngr.scribbleLineBaseWidthRange))
        informalLine.points = infrmlMarksMngr.scribblePoints
        informalLine.loops = int(random.uniform(infrmlMarksMngr.scribbleLoopsRange[0], infrmlMarksMngr.scribbleLoopsRange[1]))
        informalLine.noiseX = random.uniform(infrmlMarksMngr.scribbleNoiseXRange[0], infrmlMarksMngr.scribbleNoiseXRange[1])
        informalLine.noiseY = random.uniform(infrmlMarksMngr.scribbleNoiseYRange[0], infrmlMarksMngr.scribbleNoiseYRange[1])
        informalLine.lineColor = setLineColor()
        if random.random() < infrmlMarksMngr.scribbleAltColorProb:
            informalLine.lineColor = (int(random.uniform(40, 255)), 6, 30, 60)
        if random.random() < infrmlMarksMngr.scribbleAltColorProb:
            _tVal = int(random.uniform(40, 255))
            informalLine.lineColor = (0, _tVal, _tVal, 60)
        if random.random() < infrmlMarksMngr.scribbleSkipMarksProb:
            _skipMark = True

        if not _skipMark:
            informalLine.generateScribble()
            infrmlMarksMngr.informalLineUnits.append(informalLine)

    # -------------------------------------- #
    if _markType == "single":
        informalLine = InformalLine()
        informalLine.lineType = 0
        informalLine.curveResolution = infrmlMarksMngr.curveResolution
        informalLine.backTrackRange = infrmlMarksMngr.backTrackRange
        informalLine.lineColorIsBgColor = False
        informalLine.draw = config.draw
        if infrmlMarksMngr.useBgBox and infrmlMarksMngr.singlesOnTop:
            informalLine.draw = config.underLayerDraw
        informalLine.baseWidthRange = infrmlMarksMngr.vertLineWidthRange
        informalLine.drawingHeight = _drawingHeight
        informalLine.xOffset = _lastX + infrmlMarksMngr.xOffset
        # informalLine.xOffset = col * infrmlMarksMngr.markMinWidth
        informalLine.yOffset = _lastY - informalLine.drawingHeight / 4 * random.random()
        informalLine.angle = random.uniform(infrmlMarksMngr.angleAltRange[0], infrmlMarksMngr.angleAltRange[1])
        informalLine.pointPerLine = infrmlMarksMngr.pointsPerLineCol
        informalLine.lineSpeedRange = infrmlMarksMngr.lineSpeedRange
        informalLine.lineSpeedRange = infrmlMarksMngr.vertLineSpeedRange
        informalLine.noiseAmplitudeRange = infrmlMarksMngr.noiseAmplitudeRangeCol
        informalLine.horizontalMovementProb = infrmlMarksMngr.horizontalMovementProb
        informalLine.verticalMovementProb = infrmlMarksMngr.verticalMovementProb
        informalLine.lineColor = setLineColor()
        if random.random() < infrmlMarksMngr.marksAltColorProb:
            informalLine.lineColor = (int(random.uniform(40, 255)), 6, 30, 60)
        if random.random() < infrmlMarksMngr.marksAltColorProb:
            _tVal = int(random.uniform(40, 255))
            informalLine.lineColor = (0, _tVal, _tVal, 60)

        if not _skipMark:
            informalLine.reconfigure()
            informalLine.generateInformalLine()
            infrmlMarksMngr.informalLineUnits.append(informalLine)

    # -------------------------------------- #
    if _markType == "x":
        _clr = None
        for i in range(0, 2):
            informalLine = InformalLine()
            informalLine.lineType = 0
            informalLine.curveResolution = infrmlMarksMngr.curveResolution
            informalLine.backTrackRange = infrmlMarksMngr.backTrackRange
            informalLine.lineColorIsBgColor = False
            informalLine.draw = config.draw
            if infrmlMarksMngr.useBgBox and infrmlMarksMngr.xsOnTop:
                informalLine.draw = config.underLayerDraw

            informalLine.baseWidthRange = infrmlMarksMngr.vertLineWidthRange
            informalLine.drawingHeight = _drawingHeight
            informalLine.xOffset = infrmlMarksMngr.xOffset + _lastX
            informalLine.yOffset = _lastY - informalLine.drawingHeight / 4 * random.random()
            informalLine.angle = random.uniform(infrmlMarksMngr.angleRange[0], infrmlMarksMngr.angleRange[1])
            if i == 1:
                informalLine.angle *= -1
                if random.random() < 0.5:
                    informalLine.angle = -random.uniform(infrmlMarksMngr.angleRange[0], infrmlMarksMngr.angleRange[1])
                informalLine.xOffset -= informalLine.drawingHeight / 2

            informalLine.pointPerLine = infrmlMarksMngr.pointsPerLineCol
            informalLine.lineSpeedRange = infrmlMarksMngr.lineSpeedRange
            informalLine.lineSpeedRange = infrmlMarksMngr.vertLineSpeedRange
            informalLine.noiseAmplitudeRange = infrmlMarksMngr.noiseAmplitudeRangeCol
            informalLine.horizontalMovementProb = infrmlMarksMngr.horizontalMovementProb
            informalLine.verticalMovementProb = infrmlMarksMngr.verticalMovementProb
            if i == 0:
                informalLine.lineColor = setLineColor()
                if random.random() < infrmlMarksMngr.marksAltColorProb:
                    informalLine.lineColor = (int(random.uniform(40, 255)), 6, 30, 60)
                if random.random() < infrmlMarksMngr.marksAltColorProb:
                    _tVal = int(random.uniform(40, 255))
                    informalLine.lineColor = (0, _tVal, _tVal, 60)
                _clr = informalLine.lineColor
            else:
                informalLine.lineColor = _clr

            if not _skipMark:
                informalLine.reconfigure()
                informalLine.generateInformalLine()
                infrmlMarksMngr.informalLineUnits.append(informalLine)


# -------------------------------------- #


def setLines():
    pieceLogger(f"[setLines] New Lines:")
    # config.informalLineUnits = []
    generateMarksGrid()
    generateScribbleGrid()


def generateScribbleGrid():
    pieceLogger(f"[generateScribbleGrid] Making scribble marks")
    infrmlMarksMngr.line_alpha = randomRange(infrmlMarksMngr.activePalette.line_alpha_range[0], infrmlMarksMngr.activePalette.line_alpha_range[1], True)
    infrmlMarksMngr.bg_alpha_base = randomRange(infrmlMarksMngr.activePalette.bg_alpha_range[0], infrmlMarksMngr.activePalette.bg_alpha_range[1], True)

    for _row in range(0, infrmlMarksMngr.scribbleRows):
        for _col in range(0, infrmlMarksMngr.scribbleCols):
            _skipMark = False
            generateMark(_col, _row, 0, 0, 0, _skipMark, "scribble")
    infrmlMarksMngr.numberOfinformalLines = len(infrmlMarksMngr.informalLineUnits)


def generateMarksGrid():
    pieceLogger(f"[generateMarksGrid] Making Grid:  {infrmlMarksMngr.drawingWidth } {infrmlMarksMngr.drawingHeight }")

    infrmlMarksMngr.colInterval = random.randint(int(infrmlMarksMngr.colIntervalRange[0]), int(infrmlMarksMngr.colIntervalRange[1]))
    infrmlMarksMngr.rowInterval = random.randint(int(infrmlMarksMngr.rowIntervalRange[0]), int(infrmlMarksMngr.rowIntervalRange[1]))
    infrmlMarksMngr.noiseAmplitudeCol = random.uniform(float(infrmlMarksMngr.noiseAmplitudeRangeCol[0]), float(infrmlMarksMngr.noiseAmplitudeRangeCol[1]))
    infrmlMarksMngr.noiseAmplitudeRow = random.uniform(float(infrmlMarksMngr.noiseAmplitudeRangeRow[0]), float(infrmlMarksMngr.noiseAmplitudeRangeRow[1]))
    infrmlMarksMngr.vertLineChange = randomRange(infrmlMarksMngr.vertLineChangeRange[0], infrmlMarksMngr.vertLineChangeRange[1])
    infrmlMarksMngr.horizLineChange = randomRange(infrmlMarksMngr.horizLineChangeRange[0], infrmlMarksMngr.horizLineChangeRange[1])
    infrmlMarksMngr.line_alpha = randomRange(infrmlMarksMngr.activePalette.line_alpha_range[0], infrmlMarksMngr.activePalette.line_alpha_range[1], True)
    infrmlMarksMngr.bg_alpha_base = randomRange(infrmlMarksMngr.activePalette.bg_alpha_range[0], infrmlMarksMngr.activePalette.bg_alpha_range[1], True)

    for _row in range(infrmlMarksMngr.rowInterval):
        _lastX = 0
        _lastY = infrmlMarksMngr.yOffset + _row * (infrmlMarksMngr.minYSpacing)
        for col in range(infrmlMarksMngr.colInterval):
            _drawingHeight = infrmlMarksMngr.markMinHeight + random.uniform(-infrmlMarksMngr.sizeRange, infrmlMarksMngr.sizeRange)
            _skipMark = False
            _altMark = False
            if random.random() < infrmlMarksMngr.skipMarksProb:
                _skipMark = True
            if random.random() < infrmlMarksMngr.altMarksProb:
                _altMark = True
                _drawingHeight = infrmlMarksMngr.markMinHeight + random.uniform(-infrmlMarksMngr.sizeRange, infrmlMarksMngr.sizeRange)

            _lastX += infrmlMarksMngr.markMinWidth + infrmlMarksMngr.minXSpacing
            if col == 0:
                _lastX /= 2

            if _altMark:
                generateMark(col, _row, _lastX, _lastY, _drawingHeight, _skipMark, "single")
            else:
                generateMark(col, _row, _lastX, _lastY, _drawingHeight, _skipMark, "x")

    infrmlMarksMngr.numberOfinformalLines = len(infrmlMarksMngr.informalLineUnits)
    # pieceLogger(f"New Lines {config.numberOfinformalLines}")


def changeLine():
    _changeLine = random.randint(0, len(infrmlMarksMngr.informalLineUnits) - 1)
    _lineUnit: InformalLine = infrmlMarksMngr.informalLineUnits[_changeLine]
    if _lineUnit.lineType == 0:
        _lineUnit.reconfigure()


def drawTheBG():
    infrmlMarksMngr.bgColor = (infrmlMarksMngr.bgColor[0], infrmlMarksMngr.bgColor[1], infrmlMarksMngr.bgColor[2], round(infrmlMarksMngr.bg_alpha))
    infrmlMarksMngr.draw.rectangle((0, 0, infrmlMarksMngr.drawingWidth, infrmlMarksMngr.drawingHeight), fill=infrmlMarksMngr.bgColor)


def updateLines():
    global config

    for _informalLineUnitIndex in range(0, len(infrmlMarksMngr.informalLineUnits)):
        _lineUnit: InformalLine
        _lineUnit = infrmlMarksMngr.informalLineUnits[_informalLineUnitIndex]
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

    if random.random() < infrmlMarksMngr.useBgBoxProb and infrmlMarksMngr.useBgBox:
        bgColorsFilling()

    if infrmlMarksMngr.bg_alpha < infrmlMarksMngr.bg_alpha_base:
        infrmlMarksMngr.bg_alpha += infrmlMarksMngr.bg_alpha_returnrate

    if infrmlMarksMngr.bg_alpha > infrmlMarksMngr.bg_alpha_base:
        infrmlMarksMngr.bg_alpha = infrmlMarksMngr.bg_alpha_base

    drawTheBG()
    updateLines()

    # in-place refresh of mark
    for _u in range(infrmlMarksMngr.numberOfinformalLines):
        if random.random() < infrmlMarksMngr.changeLinesProb and not infrmlMarksMngr.noChange:
            _informalLine: InformalLine = infrmlMarksMngr.informalLineUnits[_u]
            if _informalLine.lineType == 0:
                _informalLine.reconfigure()
                _informalLine.generateInformalLine()

            if _informalLine.lineType == 1:
                _informalLine.generateScribble()

    # all marks changed
    if random.random() < infrmlMarksMngr.changeAllLinesProb and not infrmlMarksMngr.noChange:
        infrmlMarksMngr.lightMode = False if random.random() > infrmlMarksMngr.lightModeProb else True
        infrmlMarksMngr.bg_alpha = 0
        clearbgBox()
        setBGColor()
        setLines()
        # doFrame()
        pieceLogger(f"[reDraw] change ALL LINES  lightMode:{infrmlMarksMngr.lightMode} {infrmlMarksMngr.bg_alpha}")

    if random.random() < infrmlMarksMngr.pauseProb:
        infrmlMarksMngr.noChange = True

    if random.random() < infrmlMarksMngr.unpauseProb:
        infrmlMarksMngr.noChange = False

    if random.random() < infrmlMarksMngr.clearbgBoxProb:
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
        infrmlMarksMngr.paletteSets.append(palette)

    infrmlMarksMngr.activePalette = random.choice(infrmlMarksMngr.paletteSets)


class InformalMarksManager:
    config
    paletteSets = []
    informalLineUnits = []
    activePalette =  None

    def __init__(self, config):
        self.config = config

    def setUp(self,workConfig):

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
    global infrmlMarksMngr

    infrmlMarksMngr = InformalMarksManager(config)
    infrmlMarksMngr.setUp(workConfig)

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


    infrmlMarksMngr.draw = config.draw
    infrmlMarksMngr.imageDraw = config.imageDraw


    loadColorConfigs()
    setLines()

    infrmlMarksMngr.lineColor = setLineColor()
    setBGColor()

    # enFramingSetup()

    if infrmlMarksMngr.useBgBox:
        for _ in range(infrmlMarksMngr.initialRunsOfBgBlocks):
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
