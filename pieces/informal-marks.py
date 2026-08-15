import random
import time
import math
from noise import *
from PIL import Image, ImageDraw
from modules import colorutils, panelDrawing
# from modules import configuration
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
    imMngr.bgBoxBox = (
        xPos,
        yPos,
        xPos + config.canvasWidth,
        yPos + config.canvasHeight,
    )
    imMngr.bgBoxFill = (0, 0, 0, 0)
    config.underLayerDraw.rectangle(imMngr.bgBoxBox, fill=imMngr.bgBoxFill)
    imMngr.bgBoxColorRange = random.choice(imMngr.activePalette.bgBoxColorRanges)


def bgColorsFilling():

    # config.useBgBox = False if config.useBgBox   else True
    # pieceLogger("bgBox")
    # xPos = config.tileSizeWidth * math.floor(random.uniform(0, config.cols))
    # yPos = config.tileSizeHeight * math.floor(random.uniform(0, config.rows))

    xPos = math.floor(random.uniform(0, config.canvasWidth))
    yPos = math.floor(random.uniform(0, config.canvasHeight))

    imMngr.tileSizeWidth = round(random.uniform(imMngr.bgTileSizeWidthMin, imMngr.bgTileSizeWidthMax))
    imMngr.tileSizeHeight = round(random.uniform(imMngr.bgTileSizeHeightMin, imMngr.bgTileSizeHeightMax))

    imMngr.bgBoxBox = (
        xPos,
        yPos,
        xPos + imMngr.tileSizeWidth,
        yPos + imMngr.tileSizeHeight,
    )
    cR = imMngr.bgBoxColorRange
    # print(cR)
    bgBoxFill = colorutils.getRandomColorHSV(cR[0], cR[1], cR[2], cR[3], cR[4], cR[5], cR[6], cR[7])
    # print(bgBoxFill)
    imMngr.bgBoxFill = (
        round(config.brightness * bgBoxFill[0]),
        round(config.brightness * bgBoxFill[1]),
        round(config.brightness * bgBoxFill[2]),
        round(random.uniform(imMngr.activePalette.bgBoxAlphaRange[0], imMngr.activePalette.bgBoxAlphaRange[1])),
    )

    config.underLayerDraw.rectangle(imMngr.bgBoxBox, fill=imMngr.bgBoxFill)

    glitchIterations = round(random.uniform(imMngr.bgGlitchCyclesMin, imMngr.bgGlitchCyclesMax))
    for _ in range(glitchIterations):
        glitchBox(
            config.underLayer,
            config.canvasWidth,
            config.canvasHeight,
            imMngr.bgGlitchDisplacementHorizontal,
            imMngr.bgGlitchDisplacementVertical,
        )


# -------- Line Attribute Function --------- #


def setLineColor():
    if not imMngr.lightMode:
        if imMngr.lightLinesOnGround:
            return colorutils.getRandomColorHSV(
                imMngr.activePalette.line_mid_minHue,
                imMngr.activePalette.line_mid_maxHue,
                imMngr.activePalette.line_mid_minSaturation,
                imMngr.activePalette.line_mid_maxSaturation,
                imMngr.activePalette.line_mid_minValue,
                imMngr.activePalette.line_mid_maxValue,
                imMngr.activePalette.line_mid_minDropHue,
                imMngr.activePalette.line_mid_maxDropHue,
                round(random.uniform(imMngr.activePalette.line_mid_alpha_range[0], imMngr.activePalette.line_mid_alpha_range[1])),
                config.brightness,
            )
        else:
            return colorutils.getRandomColorHSV(
                imMngr.activePalette.line_minHue,
                imMngr.activePalette.line_maxHue,
                imMngr.activePalette.line_minSaturation,
                imMngr.activePalette.line_maxSaturation,
                imMngr.activePalette.line_minValue,
                imMngr.activePalette.line_maxValue,
                imMngr.activePalette.line_minDropHue,
                imMngr.activePalette.line_maxDropHue,
                round(random.uniform(imMngr.activePalette.line_alpha_range[0], imMngr.activePalette.line_alpha_range[1])),
                config.brightness,
            )
    else:
        return colorutils.getRandomColorHSV(
            imMngr.activePalette.line_light_minHue,
            imMngr.activePalette.line_light_maxHue,
            imMngr.activePalette.line_light_minSaturation,
            imMngr.activePalette.line_light_maxSaturation,
            imMngr.activePalette.line_light_minValue,
            imMngr.activePalette.line_light_maxValue,
            imMngr.activePalette.line_light_minDropHue,
            imMngr.activePalette.line_light_maxDropHue,
            round(random.uniform(imMngr.activePalette.line_light_alpha_range[0], imMngr.activePalette.line_light_alpha_range[1])),
            config.brightness,
        )

    # pieceLogger(f"New Line Color {config.lineColor}")


def setBGColor():

    imMngr.activePalette = random.choice(imMngr.paletteSets)
    pieceLogger(f"[setBGColor] NEW palette: {imMngr.activePalette.name}")

    imMngr.bg_alpha = round(random.uniform(imMngr.activePalette.bg_alpha_range[0], imMngr.activePalette.bg_alpha_range[1]))
    imMngr.bg_minHue = imMngr.activePalette.bg_minHue
    imMngr.bg_maxHue = imMngr.activePalette.bg_maxHue
    imMngr.bg_minSaturation = imMngr.activePalette.bg_minSaturation
    imMngr.bg_maxSaturation = imMngr.activePalette.bg_maxSaturation
    imMngr.bg_minValue = imMngr.activePalette.bg_minValue
    imMngr.bg_maxValue = imMngr.activePalette.bg_maxValue
    imMngr.bg_dropHueMin = imMngr.activePalette.bg_dropHueMin
    imMngr.bg_dropHueMax = imMngr.activePalette.bg_dropHueMax

    imMngr.lineColorIsBgColor = imMngr.activePalette.lineColorIsBgColor

    _minVal = imMngr.bg_minValue
    _maxVal = imMngr.bg_maxValue
    _minSat = imMngr.bg_minSaturation
    _maxSat = imMngr.bg_maxSaturation

    if imMngr.lightMode:
        _minVal = 0.2
        _maxVal = 0.5
        _minSat = 0.5
        _maxSat = 0.99

    imMngr.bgColor = colorutils.getRandomColorHSV(
        imMngr.bg_minHue,
        imMngr.bg_maxHue,
        _minSat,
        _maxSat,
        _minVal,
        _maxVal,
        imMngr.bg_dropHueMin,
        imMngr.bg_dropHueMax,
        imMngr.bg_alpha,
        config.brightness,
    )

    if random.random() < imMngr.lightLinesOnGroundProb:
        imMngr.lightLinesOnGround = True
    else:
        imMngr.lightLinesOnGround = False

    imMngr.bgBoxColorRange = random.choice(imMngr.activePalette.bgBoxColorRanges)


# -------- Line Functions    -------------- #


def generateMark(col, row, _lastX, _lastY, _drawingHeight, _skipMark, _markType="scribble"):

    # -------------------------------------- #
    if _markType == "scribble":
        informalLine = InformalLine()
        informalLine.curveResolution = imMngr.curveResolution
        informalLine.backTrackRange = imMngr.backTrackRange
        informalLine.lineColorIsBgColor = False
        informalLine.draw = config.draw
        if imMngr.useBgBox and imMngr.scribbleOnTop:
            informalLine.draw = config.underLayerDraw
        informalLine.lineType = 1
        informalLine.scribbleHeight = random.uniform(imMngr.scribbleHeightRange[0], imMngr.scribbleHeightRange[1])
        informalLine.xOffset = imMngr.scribblexOffset + col * imMngr.scribbleRadiusXRange[1] * imMngr.scibbleXPacking
        informalLine.yOffset = imMngr.scribbleyOffset + row * imMngr.scribbleRadiusYRange[1] * imMngr.scibbleYPacking
        informalLine.radiusX = random.uniform(imMngr.scribbleRadiusXRange[0], imMngr.scribbleRadiusXRange[1])
        informalLine.radiusY = random.uniform(imMngr.scribbleRadiusYRange[0], imMngr.scribbleRadiusYRange[1])
        informalLine.baseWidth = int(random.uniform(0, imMngr.scribbleLineBaseWidthRange))
        informalLine.points = imMngr.scribblePoints
        informalLine.loops = int(random.uniform(imMngr.scribbleLoopsRange[0], imMngr.scribbleLoopsRange[1]))
        informalLine.noiseX = random.uniform(imMngr.scribbleNoiseXRange[0], imMngr.scribbleNoiseXRange[1])
        informalLine.noiseY = random.uniform(imMngr.scribbleNoiseYRange[0], imMngr.scribbleNoiseYRange[1])
        informalLine.lineColor = setLineColor()
        if random.random() < imMngr.scribbleAltColorProb:
            informalLine.lineColor = (int(random.uniform(40, 255)), 6, 30, 60)
        if random.random() < imMngr.scribbleAltColorProb:
            _tVal = int(random.uniform(40, 255))
            informalLine.lineColor = (0, _tVal, _tVal, 60)
        if random.random() < imMngr.scribbleSkipMarksProb:
            _skipMark = True

        if not _skipMark:
            informalLine.generateScribble()
            imMngr.informalLineUnits.append(informalLine)

    # -------------------------------------- #
    if _markType == "single":
        informalLine = InformalLine()
        informalLine.lineType = 0
        informalLine.curveResolution = imMngr.curveResolution
        informalLine.backTrackRange = imMngr.backTrackRange
        informalLine.lineColorIsBgColor = False
        informalLine.draw = config.draw
        if imMngr.useBgBox and imMngr.singlesOnTop:
            informalLine.draw = config.underLayerDraw
        informalLine.baseWidthRange = imMngr.vertLineWidthRange
        informalLine.drawingHeight = _drawingHeight
        informalLine.xOffset = _lastX + imMngr.xOffset
        # informalLine.xOffset = col * imMngr.markMinWidth
        informalLine.yOffset = _lastY - informalLine.drawingHeight / 4 * random.random()
        informalLine.angle = random.uniform(imMngr.angleAltRange[0], imMngr.angleAltRange[1])
        informalLine.pointPerLine = imMngr.pointsPerLineCol
        informalLine.lineSpeedRange = imMngr.lineSpeedRange
        informalLine.lineSpeedRange = imMngr.vertLineSpeedRange
        informalLine.noiseAmplitudeRange = imMngr.noiseAmplitudeRangeCol
        informalLine.horizontalMovementProb = imMngr.horizontalMovementProb
        informalLine.verticalMovementProb = imMngr.verticalMovementProb
        informalLine.lineColor = setLineColor()
        if random.random() < imMngr.marksAltColorProb:
            informalLine.lineColor = (int(random.uniform(40, 255)), 6, 30, 60)
        if random.random() < imMngr.marksAltColorProb:
            _tVal = int(random.uniform(40, 255))
            informalLine.lineColor = (0, _tVal, _tVal, 60)

        if not _skipMark:
            informalLine.reconfigure()
            informalLine.generateInformalLine()
            imMngr.informalLineUnits.append(informalLine)

    # -------------------------------------- #
    if _markType == "x":
        _clr = None
        for i in range(0, 2):
            informalLine = InformalLine()
            informalLine.lineType = 0
            informalLine.curveResolution = imMngr.curveResolution
            informalLine.backTrackRange = imMngr.backTrackRange
            informalLine.lineColorIsBgColor = False
            informalLine.draw = config.draw
            if imMngr.useBgBox and imMngr.xsOnTop:
                informalLine.draw = config.underLayerDraw

            informalLine.baseWidthRange = imMngr.vertLineWidthRange
            informalLine.drawingHeight = _drawingHeight
            informalLine.xOffset = imMngr.xOffset + _lastX
            informalLine.yOffset = _lastY - informalLine.drawingHeight / 4 * random.random()
            informalLine.angle = random.uniform(imMngr.angleRange[0], imMngr.angleRange[1])
            if i == 1:
                informalLine.angle *= -1
                if random.random() < 0.5:
                    informalLine.angle = -random.uniform(imMngr.angleRange[0], imMngr.angleRange[1])
                informalLine.xOffset -= informalLine.drawingHeight / 2

            informalLine.pointPerLine = imMngr.pointsPerLineCol
            informalLine.lineSpeedRange = imMngr.lineSpeedRange
            informalLine.lineSpeedRange = imMngr.vertLineSpeedRange
            informalLine.noiseAmplitudeRange = imMngr.noiseAmplitudeRangeCol
            informalLine.horizontalMovementProb = imMngr.horizontalMovementProb
            informalLine.verticalMovementProb = imMngr.verticalMovementProb
            if i == 0:
                informalLine.lineColor = setLineColor()
                if random.random() < imMngr.marksAltColorProb:
                    informalLine.lineColor = (int(random.uniform(40, 255)), 6, 30, 60)
                if random.random() < imMngr.marksAltColorProb:
                    _tVal = int(random.uniform(40, 255))
                    informalLine.lineColor = (0, _tVal, _tVal, 60)
                _clr = informalLine.lineColor
            else:
                informalLine.lineColor = _clr

            if not _skipMark:
                informalLine.reconfigure()
                informalLine.generateInformalLine()
                imMngr.informalLineUnits.append(informalLine)


# -------------------------------------- #


def setLines():
    pieceLogger(f"[setLines] New Lines:")
    # config.informalLineUnits = []
    generateMarksGrid()
    generateScribbleGrid()


def generateScribbleGrid():
    pieceLogger(f"[generateScribbleGrid] Making scribble marks")
    imMngr.line_alpha = randomRange(imMngr.activePalette.line_alpha_range[0], imMngr.activePalette.line_alpha_range[1], True)
    imMngr.bg_alpha_base = randomRange(imMngr.activePalette.bg_alpha_range[0], imMngr.activePalette.bg_alpha_range[1], True)

    for _row in range(0, imMngr.scribbleRows):
        for _col in range(0, imMngr.scribbleCols):
            _skipMark = False
            generateMark(_col, _row, 0, 0, 0, _skipMark, "scribble")
    imMngr.numberOfinformalLines = len(imMngr.informalLineUnits)


def generateMarksGrid():
    pieceLogger(f"[generateMarksGrid] Making Grid:  {imMngr.drawingWidth } {imMngr.drawingHeight }")

    imMngr.colInterval = random.randint(int(imMngr.colIntervalRange[0]), int(imMngr.colIntervalRange[1]))
    imMngr.rowInterval = random.randint(int(imMngr.rowIntervalRange[0]), int(imMngr.rowIntervalRange[1]))
    imMngr.noiseAmplitudeCol = random.uniform(float(imMngr.noiseAmplitudeRangeCol[0]), float(imMngr.noiseAmplitudeRangeCol[1]))
    imMngr.noiseAmplitudeRow = random.uniform(float(imMngr.noiseAmplitudeRangeRow[0]), float(imMngr.noiseAmplitudeRangeRow[1]))
    imMngr.vertLineChange = randomRange(imMngr.vertLineChangeRange[0], imMngr.vertLineChangeRange[1])
    imMngr.horizLineChange = randomRange(imMngr.horizLineChangeRange[0], imMngr.horizLineChangeRange[1])
    imMngr.line_alpha = randomRange(imMngr.activePalette.line_alpha_range[0], imMngr.activePalette.line_alpha_range[1], True)
    imMngr.bg_alpha_base = randomRange(imMngr.activePalette.bg_alpha_range[0], imMngr.activePalette.bg_alpha_range[1], True)

    for _row in range(imMngr.rowInterval):
        _lastX = 0
        _lastY = imMngr.yOffset + _row * (imMngr.minYSpacing)
        for col in range(imMngr.colInterval):
            _drawingHeight = imMngr.markMinHeight + random.uniform(-imMngr.sizeRange, imMngr.sizeRange)
            _skipMark = False
            _altMark = False
            if random.random() < imMngr.skipMarksProb:
                _skipMark = True
            if random.random() < imMngr.altMarksProb:
                _altMark = True
                _drawingHeight = imMngr.markMinHeight + random.uniform(-imMngr.sizeRange, imMngr.sizeRange)

            _lastX += imMngr.markMinWidth + imMngr.minXSpacing
            if col == 0:
                _lastX /= 2

            if _altMark:
                generateMark(col, _row, _lastX, _lastY, _drawingHeight, _skipMark, "single")
            else:
                generateMark(col, _row, _lastX, _lastY, _drawingHeight, _skipMark, "x")

    imMngr.numberOfinformalLines = len(imMngr.informalLineUnits)
    # pieceLogger(f"New Lines {config.numberOfinformalLines}")


def changeLine():
    _changeLine = random.randint(0, len(imMngr.informalLineUnits) - 1)
    _lineUnit: InformalLine = imMngr.informalLineUnits[_changeLine]
    if _lineUnit.lineType == 0:
        _lineUnit.reconfigure()


def drawTheBG():
    imMngr.bgColor = (imMngr.bgColor[0], imMngr.bgColor[1], imMngr.bgColor[2], round(imMngr.bg_alpha))
    imMngr.draw.rectangle((0, 0, imMngr.drawingWidth, imMngr.drawingHeight), fill=imMngr.bgColor)


def updateLines():
    for _informalLineUnitIndex in range(0, len(imMngr.informalLineUnits)):
        _lineUnit: InformalLine
        _lineUnit = imMngr.informalLineUnits[_informalLineUnitIndex]
        if _lineUnit.lineType == 0:
            _lineUnit.drawTheLineComplete()
            # _lineUnit.drawLinePoints()
        if _lineUnit.lineType == 1:
            _lineUnit.drawTheLineComplete()


# ---- looping and redrawing --------


def runWork():
    _config : ArtWorkConfig
    _config = config

    print(bcolors.OKGREEN + "** " + bcolors.BOLD)
    print("Running informalMarksGrid.py")
    print(bcolors.ENDC)
    # _config.debugSelf()

    while _config.isRunning == True:
        _config.directorController.checkTime()
        if _config.directorController.advance:
            iterate()

        if _config.standAlone == False:
            _config.callBack()

        time.sleep(_config.redrawSpeed)


def reDraw():

    if random.random() < imMngr.useBgBoxProb and imMngr.useBgBox:
        bgColorsFilling()

    if imMngr.bg_alpha < imMngr.bg_alpha_base:
        imMngr.bg_alpha += imMngr.bg_alpha_returnrate

    if imMngr.bg_alpha > imMngr.bg_alpha_base:
        imMngr.bg_alpha = imMngr.bg_alpha_base

    drawTheBG()
    updateLines()

    # in-place refresh of mark
    for _u in range(imMngr.numberOfinformalLines):
        if random.random() < imMngr.changeLinesProb and not imMngr.noChange:
            _informalLine: InformalLine = imMngr.informalLineUnits[_u]
            if _informalLine.lineType == 0:
                _informalLine.reconfigure()
                _informalLine.generateInformalLine()

            if _informalLine.lineType == 1:
                _informalLine.generateScribble()

    # all marks changed
    if random.random() < imMngr.changeAllLinesProb and not imMngr.noChange:
        imMngr.lightMode = False if random.random() > imMngr.lightModeProb else True
        imMngr.bg_alpha = 0
        clearbgBox()
        setBGColor()
        setLines()
        # doFrame()
        pieceLogger(f"[reDraw] change ALL LINES  lightMode:{imMngr.lightMode} {imMngr.bg_alpha}")

    if random.random() < imMngr.pauseProb:
        imMngr.noChange = True

    if random.random() < imMngr.unpauseProb:
        imMngr.noChange = False

    if random.random() < imMngr.clearbgBoxProb:
        clearbgBox()


def iterate():
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
        imMngr.paletteSets.append(palette)

    imMngr.activePalette = random.choice(imMngr.paletteSets)


class InformalMarksManager:
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
    global imMngr
    
    # ---- initialize  -----------------
    # imMngr = "informal marks manager"
    imMngr = InformalMarksManager(config)
    imMngr.setUp(workConfig)

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


    imMngr.draw = config.draw
    imMngr.imageDraw = config.imageDraw


    loadColorConfigs()
    setLines()

    imMngr.lineColor = setLineColor()
    setBGColor()

    # enFramingSetup()

    if imMngr.useBgBox:
        for _ in range(imMngr.initialRunsOfBgBlocks):
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
