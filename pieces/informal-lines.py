import random
import time
import math
from noise import *
from PIL import Image, ImageDraw
from modules.configuration import bcolors, pieceLogger
from modules import colorutils, panelDrawing
from modules.holder_director import Director
from pieces.screen import Holder
from modules.informal_line import InformalLine


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
    config.bgBoxBox = (
        xPos,
        yPos,
        xPos + config.canvasWidth,
        yPos + config.canvasHeight,
    )
    config.bgBoxFill = (0, 0, 0, 0)
    config.underLayerDraw.rectangle(config.bgBoxBox, fill=config.bgBoxFill)
    config.bgBoxColorRange = random.choice(config.activePalette.bgBoxColorRanges)


def bgColorsFilling():
    global config
    # config.useBgBox = False if config.useBgBox   else True
    # pieceLogger("bgBox")
    # xPos = config.tileSizeWidth * math.floor(random.uniform(0, config.cols))
    # yPos = config.tileSizeHeight * math.floor(random.uniform(0, config.rows))

    xPos = math.floor(random.uniform(0, config.canvasWidth))
    yPos = math.floor(random.uniform(0, config.canvasHeight))

    config.tileSizeWidth = round(random.uniform(config.bgTileSizeWidthMin, config.bgTileSizeWidthMax))
    config.tileSizeHeight = round(random.uniform(config.bgTileSizeHeightMin, config.bgTileSizeHeightMax))

    config.bgBoxBox = (
        xPos,
        yPos,
        xPos + config.tileSizeWidth,
        yPos + config.tileSizeHeight,
    )
    cR = config.bgBoxColorRange
    # print(cR)
    bgBoxFill = colorutils.getRandomColorHSV(cR[0], cR[1], cR[2], cR[3], cR[4], cR[5], cR[6], cR[7])
    # print(bgBoxFill)
    config.bgBoxFill = (
        round(config.brightness * bgBoxFill[0]),
        round(config.brightness * bgBoxFill[1]),
        round(config.brightness * bgBoxFill[2]),
        round(random.uniform(config.activePalette.bgBoxAlphaRange[0], config.activePalette.bgBoxAlphaRange[1])),
    )

    config.underLayerDraw.rectangle(config.bgBoxBox, fill=config.bgBoxFill)

    glitchIterations = round(random.uniform(config.bgGlitchCyclesMin, config.bgGlitchCyclesMax))
    for _ in range(glitchIterations):
        glitchBox(
            config.underLayer,
            config.canvasWidth,
            config.canvasHeight,
            config.bgGlitchDisplacementHorizontal,
            config.bgGlitchDisplacementVertical,
        )


# -------- Line Attribute Function --------- #


def setLineColor():
    if not config.lightMode:
        if config.lightLinesOnGround:
            return colorutils.getRandomColorHSV(
                config.activePalette.line_mid_minHue,
                config.activePalette.line_mid_maxHue,
                config.activePalette.line_mid_minSaturation,
                config.activePalette.line_mid_maxSaturation,
                config.activePalette.line_mid_minValue,
                config.activePalette.line_mid_maxValue,
                config.activePalette.line_mid_minDropHue,
                config.activePalette.line_mid_maxDropHue,
                round(random.uniform(config.activePalette.line_mid_alpha_range[0], config.activePalette.line_mid_alpha_range[1])),
                config.brightness,
            )
        else:
            return colorutils.getRandomColorHSV(
                config.activePalette.line_minHue,
                config.activePalette.line_maxHue,
                config.activePalette.line_minSaturation,
                config.activePalette.line_maxSaturation,
                config.activePalette.line_minValue,
                config.activePalette.line_maxValue,
                config.activePalette.line_minDropHue,
                config.activePalette.line_maxDropHue,
                round(random.uniform(config.activePalette.line_alpha_range[0], config.activePalette.line_alpha_range[1])),
                config.brightness,
            )
    else:
        return colorutils.getRandomColorHSV(
            config.activePalette.line_light_minHue,
            config.activePalette.line_light_maxHue,
            config.activePalette.line_light_minSaturation,
            config.activePalette.line_light_maxSaturation,
            config.activePalette.line_light_minValue,
            config.activePalette.line_light_maxValue,
            config.activePalette.line_light_minDropHue,
            config.activePalette.line_light_maxDropHue,
            round(random.uniform(config.activePalette.line_light_alpha_range[0], config.activePalette.line_light_alpha_range[1])),
            config.brightness,
        )

    # pieceLogger(f"New Line Color {config.lineColor}")


def setBGColor():

    config.activePalette = random.choice(config.paletteSets)
    pieceLogger(f"[setBGColor] NEW palette: {config.activePalette.name}")

    config.bg_alpha = round(random.uniform(config.activePalette.bg_alpha_range[0], config.activePalette.bg_alpha_range[1]))
    config.bg_minHue = config.activePalette.bg_minHue
    config.bg_maxHue = config.activePalette.bg_maxHue
    config.bg_minSaturation = config.activePalette.bg_minSaturation
    config.bg_maxSaturation = config.activePalette.bg_maxSaturation
    config.bg_minValue = config.activePalette.bg_minValue
    config.bg_maxValue = config.activePalette.bg_maxValue
    config.bg_dropHueMin = config.activePalette.bg_dropHueMin
    config.bg_dropHueMax = config.activePalette.bg_dropHueMax

    config.lineColorIsBgColor = config.activePalette.lineColorIsBgColor

    _minVal = config.bg_minValue
    _maxVal = config.bg_maxValue
    _minSat = config.bg_minSaturation
    _maxSat = config.bg_maxSaturation

    if config.lightMode:
        _minVal = 0.2
        _maxVal = 0.5
        _minSat = 0.5
        _maxSat = 0.99

    config.bgColor = colorutils.getRandomColorHSV(
        config.bg_minHue,
        config.bg_maxHue,
        _minSat,
        _maxSat,
        _minVal,
        _maxVal,
        config.bg_dropHueMin,
        config.bg_dropHueMax,
        config.bg_alpha,
        config.brightness,
    )

    if random.random() < config.lightLinesOnGroundProb:
        config.lightLinesOnGround = True
    else:
        config.lightLinesOnGround = False

    config.bgBoxColorRange = random.choice(config.activePalette.bgBoxColorRanges)


# -------- Line Functions    -------------- #


def generateMark(col, row, _lastX, _lastY, _drawingHeight, _skipMark, _markType="scribble"):

    # -------------------------------------- #
    if _markType == "scribble":
        informalLine = InformalLine()
        informalLine.curveResolution = config.curveResolution
        informalLine.backTrackRange = config.backTrackRange
        informalLine.lineColorIsBgColor = False
        informalLine.draw = config.draw
        if config.useBgBox and config.scribbleOnTop:
            informalLine.draw = config.underLayerDraw
        informalLine.lineType = 1
        informalLine.scribbleHeight = random.uniform(config.scribbleHeightRange[0], config.scribbleHeightRange[1])
        informalLine.xOffset = config.scribblexOffset + col * config.scribbleRadiusXRange[1] * config.scibbleXPacking
        informalLine.yOffset = config.scribbleyOffset + row * config.scribbleRadiusYRange[1] * config.scibbleYPacking
        informalLine.radiusX = random.uniform(config.scribbleRadiusXRange[0], config.scribbleRadiusXRange[1])
        informalLine.radiusY = random.uniform(config.scribbleRadiusYRange[0], config.scribbleRadiusYRange[1])
        informalLine.baseWidth = int(random.uniform(0, config.scribbleLineBaseWidthRange))
        informalLine.points = config.scribblePoints
        informalLine.loops = int(random.uniform(config.scribbleLoopsRange[0], config.scribbleLoopsRange[1]))
        informalLine.noiseX = random.uniform(config.scribbleNoiseXRange[0], config.scribbleNoiseXRange[1])
        informalLine.noiseY = random.uniform(config.scribbleNoiseYRange[0], config.scribbleNoiseYRange[1])
        informalLine.lineColor = setLineColor()
        if random.random() < config.scribbleAltColorProb:
            informalLine.lineColor = (int(random.uniform(40, 255)), 6, 30, 60)
        if random.random() < config.scribbleAltColorProb:
            _tVal = int(random.uniform(40, 255))
            informalLine.lineColor = (0, _tVal, _tVal, 60)
        if random.random() < config.scribbleSkipMarksProb:
            _skipMark = True

        if not _skipMark:
            informalLine.generateScribble()
            config.informalLineUnits.append(informalLine)

    # -------------------------------------- #
    if _markType == "single":
        informalLine = InformalLine()
        informalLine.lineType = 0
        informalLine.curveResolution = config.curveResolution
        informalLine.backTrackRange = config.backTrackRange
        informalLine.lineColorIsBgColor = False
        informalLine.draw = config.draw
        if config.useBgBox and config.singlesOnTop:
            informalLine.draw = config.underLayerDraw
        informalLine.baseWidthRange = config.vertLineWidthRange
        informalLine.drawingHeight = _drawingHeight
        informalLine.xOffset = _lastX + config.xOffset
        # informalLine.xOffset = col * config.markMinWidth
        informalLine.yOffset = _lastY - informalLine.drawingHeight / 4 * random.random()
        informalLine.angle = random.uniform(config.angleAltRange[0], config.angleAltRange[1])
        informalLine.pointPerLine = config.pointsPerLineCol
        informalLine.lineSpeedRange = config.lineSpeedRange
        informalLine.lineSpeedRange = config.vertLineSpeedRange
        informalLine.noiseAmplitudeRange = config.noiseAmplitudeRangeCol
        informalLine.horizontalMovementProb = config.horizontalMovementProb
        informalLine.verticalMovementProb = config.verticalMovementProb
        informalLine.lineColor = setLineColor()
        if random.random() < config.marksAltColorProb:
            informalLine.lineColor = (int(random.uniform(40, 255)), 6, 30, 60)
        if random.random() < config.marksAltColorProb:
            _tVal = int(random.uniform(40, 255))
            informalLine.lineColor = (0, _tVal, _tVal, 60)

        if not _skipMark:
            informalLine.reconfigure()
            informalLine.generateInformalLine()
            config.informalLineUnits.append(informalLine)

    # -------------------------------------- #
    if _markType == "x" :
        _clr = None
        for i in range(0, 2):
            informalLine = InformalLine()
            informalLine.lineType = 0
            informalLine.curveResolution = config.curveResolution
            informalLine.backTrackRange = config.backTrackRange
            informalLine.lineColorIsBgColor = False
            informalLine.draw = config.draw
            if config.useBgBox and config.xsOnTop:
                informalLine.draw = config.underLayerDraw

            informalLine.baseWidthRange = config.vertLineWidthRange
            informalLine.drawingHeight = _drawingHeight
            informalLine.xOffset = config.xOffset + _lastX
            informalLine.yOffset = _lastY - informalLine.drawingHeight / 4 * random.random()
            informalLine.angle = random.uniform(config.angleRange[0], config.angleRange[1])
            if i == 1:
                informalLine.angle *= -1
                if random.random() < 0.5:
                    informalLine.angle = -random.uniform(config.angleRange[0], config.angleRange[1])
                informalLine.xOffset -= informalLine.drawingHeight / 2

            informalLine.pointPerLine = config.pointsPerLineCol
            informalLine.lineSpeedRange = config.lineSpeedRange
            informalLine.lineSpeedRange = config.vertLineSpeedRange
            informalLine.noiseAmplitudeRange = config.noiseAmplitudeRangeCol
            informalLine.horizontalMovementProb = config.horizontalMovementProb
            informalLine.verticalMovementProb = config.verticalMovementProb
            if i == 0 :
                informalLine.lineColor = setLineColor()
                if random.random() < config.marksAltColorProb:
                    informalLine.lineColor = (int(random.uniform(40, 255)), 6, 30, 60)
                if random.random() < config.marksAltColorProb:
                    _tVal = int(random.uniform(40, 255))
                    informalLine.lineColor = (0, _tVal, _tVal, 60)
                _clr  = informalLine.lineColor 
            else :
                informalLine.lineColor = _clr

            if not _skipMark:
                informalLine.reconfigure()
                informalLine.generateInformalLine()
                config.informalLineUnits.append(informalLine)


# -------------------------------------- #


def setLines():
    pieceLogger(f"[setLines] New Lines:")
    config.informalLineUnits = []
    generateMarksGrid()
    generateScribbleGrid()


def generateScribbleGrid():
    pieceLogger(f"[generateScribbleGrid] Making scribble marks")     
    config.line_alpha = randomRange(config.activePalette.line_alpha_range[0], config.activePalette.line_alpha_range[1], True)
    config.bg_alpha_base = randomRange(config.activePalette.bg_alpha_range[0], config.activePalette.bg_alpha_range[1], True)

    for _row in range(0, config.scribbleRows):
        for _col in range(0, config.scribbleCols):
            _skipMark = False
            generateMark(_col, _row, 0, 0, 0, _skipMark, "scribble")
    config.numberOfinformalLines = len(config.informalLineUnits)


def generateMarksGrid():
    pieceLogger(f"[generateMarksGrid] Making Grid:  {config.drawingWidth } {config.drawingHeight }")

    config.colInterval = random.randint(int(config.colIntervalRange[0]), int(config.colIntervalRange[1]))
    config.rowInterval = random.randint(int(config.rowIntervalRange[0]), int(config.rowIntervalRange[1]))
    config.noiseAmplitudeCol = random.uniform(float(config.noiseAmplitudeRangeCol[0]), float(config.noiseAmplitudeRangeCol[1]))
    config.noiseAmplitudeRow = random.uniform(float(config.noiseAmplitudeRangeRow[0]), float(config.noiseAmplitudeRangeRow[1]))
    config.vertLineChange = randomRange(config.vertLineChangeRange[0], config.vertLineChangeRange[1])
    config.horizLineChange = randomRange(config.horizLineChangeRange[0], config.horizLineChangeRange[1])
    config.line_alpha = randomRange(config.activePalette.line_alpha_range[0], config.activePalette.line_alpha_range[1], True)
    config.bg_alpha_base = randomRange(config.activePalette.bg_alpha_range[0], config.activePalette.bg_alpha_range[1], True)

    for _row in range(config.rowInterval):
        _lastX = 0
        _lastY = config.yOffset + _row * (config.minYSpacing)
        for col in range(config.colInterval):
            _drawingHeight = config.markMinHeight + random.uniform(-config.sizeRange, config.sizeRange)
            _skipMark = False
            _altMark = False
            if random.random() < config.skipMarksProb:
                _skipMark = True
            if random.random() < config.altMarksProb:
                _altMark = True
                _drawingHeight = config.markMinHeight + random.uniform(-config.sizeRange, config.sizeRange)

            _lastX += config.markMinWidth + config.minXSpacing
            if col == 0:
                _lastX /= 2

            if _altMark:
                generateMark(col, _row, _lastX, _lastY, _drawingHeight, _skipMark, "single")
            else:
                generateMark(col, _row, _lastX, _lastY, _drawingHeight, _skipMark, "x")

    config.numberOfinformalLines = len(config.informalLineUnits)
    # pieceLogger(f"New Lines {config.numberOfinformalLines}")


def changeLine():
    _changeLine = random.randint(0, len(config.informalLineUnits) - 1)
    _lineUnit: InformalLine = config.informalLineUnits[_changeLine]
    if _lineUnit.lineType == 0:
        _lineUnit.reconfigure()


def drawTheBG():
    config.bgColor = (config.bgColor[0], config.bgColor[1], config.bgColor[2], round(config.bg_alpha))
    config.draw.rectangle((0, 0, config.drawingWidth, config.drawingHeight), fill=config.bgColor)


def updateLines():
    global config

    for _informalLineUnitIndex in range(0, len(config.informalLineUnits)):
        _lineUnit: InformalLine
        _lineUnit = config.informalLineUnits[_informalLineUnitIndex]
        if _lineUnit.lineType == 0:
            # _lineUnit.drawTheLineComplete()
            _lineUnit.drawLinePoints()
        if _lineUnit.lineType == 1:
            _lineUnit.drawTheLineComplete()


# ---- looping and redrawing --------


def runWork():
    global configk
    print(bcolors.OKGREEN + "** " + bcolors.BOLD)
    print("Running informalMarksGrid.py")
    print(bcolors.ENDC)

    while config.isRunning == True:
        config.directorController.checkTime()
        if config.directorController.advance:
            iterate()

        if config.standAlone == False:
            config.callBack()

        time.sleep(config.redrawSpeed)


def reDraw():
    # pieceLogger(f"{config.bg_alpha} {config.bg_alpha_base}")
    if config.bg_alpha < config.bg_alpha_base:
        config.bg_alpha += config.bg_alpha_returnrate

    if config.bg_alpha > config.bg_alpha_base:
        config.bg_alpha = config.bg_alpha_base

    drawTheBG()
    updateLines()

    # in-place refresh of mark
    for _u in range(config.numberOfinformalLines):
        if random.random() < config.changeLinesProb and not config.noChange:
            _informalLine: InformalLine = config.informalLineUnits[_u]
            if _informalLine.lineType == 0:
                _informalLine.reconfigure()
                _informalLine.generateInformalLine()

            if _informalLine.lineType == 1:
                _informalLine.generateScribble()

    # all marks changed
    if random.random() < config.changeAllLinesProb and not config.noChange:
        config.lightMode = False if random.random() > config.lightModeProb else True
        config.bg_alpha = 0
        setBGColor()
        setLines()
        pieceLogger(f"[reDraw] change ALL LINES  lightMode:{config.lightMode} {config.bg_alpha}")

    if random.random() < config.pauseProb:
        config.noChange = True

    if random.random() < config.unpauseProb:
        config.noChange = False


def iterate():
    global config, overlayControls
    if random.SystemRandom().random() < config.useBgBoxProb and config.useBgBox:
        bgColorsFilling()

    reDraw()

    if random.SystemRandom().random() < config.clearbgBoxProb:
        clearbgBox()

    ########### RENDERING AS A MOCKUP OR AS REAL ###########
    if config.useDrawingPoints == True:
        config.panelDrawing.canvasToUse = config.image
        config.panelDrawing.render()

    # badpixels.drawBlanks(config.image, False)
    config.destinationImage.paste(config.image, (0,0), config.image)
    config.destinationImage.paste(config.underLayer, (0, 0), config.underLayer)

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

    config.paletteSets = []
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
        config.paletteSets.append(palette)

    config.activePalette = random.choice(config.paletteSets)


def main(run=True):
    global config
    global workConfig
    global overlayControls


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

    config.drawingWidth = int(workConfig.get("informalMarksGrid", "drawingWidth", fallback=f"{config.canvasWidth}"))
    config.drawingHeight = int(workConfig.get("informalMarksGrid", "drawingHeight", fallback=f"{config.canvasHeight}"))

    config.largestDim = max(config.drawingWidth, config.drawingHeight)

    # refinements for setting points per column and row so amplitude of noise can be adjusted to be more even if aspect ratio is more extreme - e.g narrow beam
    # but also, lower number makes the line more purely rectilinear so can give a greater focus to one directions linearity
    config.pointsPerLine = int(workConfig.get("informalMarksGrid", "pointsPerLine"))
    config.pointsPerLineCol = int(workConfig.get("informalMarksGrid", "pointsPerLineCol", fallback=config.pointsPerLine))
    config.pointsPerLineRow = int(workConfig.get("informalMarksGrid", "pointsPerLineRow", fallback=config.pointsPerLine))

    # adjust higher for higer resolution
    config.curveResolution = int(workConfig.get("informalMarksGrid", "curveResolution", fallback=10))

    # not really used - was used in first iteration using Perlin Noise
    config.noiseSeed = random.random()

    # if the shape is not single-lines, will be determined by rows and columns
    config.numberOfinformalLines = int(workConfig.get("informalMarksGrid", "numberOfinformalLines", fallback="3"))
    # the edge spacing - critical to making the drawing as the edges matter more than the sum of the lines
    config.xOffset = int(workConfig.get("informalMarksGrid", "xOffset"))
    config.yOffset = int(workConfig.get("informalMarksGrid", "yOffset"))

    # for single linesneSpeed
    config.renderLinesAsEnvelope = workConfig.getboolean("informalMarksGrid", "renderLinesAsEnvelope", fallback=False)
    config.drawVertical = workConfig.getboolean("informalMarksGrid", "drawVertical", fallback=True)
    config.drawHorizontal = workConfig.getboolean("informalMarksGrid", "drawHorizontal", fallback=True)
    config.singleLineRegularSpacing = workConfig.getboolean("informalMarksGrid", "singleLineRegularSpacing", fallback=False)
    config.drawingHeightRange = [int(x) for x in workConfig.get("informalMarksGrid", "drawingHeightRange", fallback="18,180").split(",")]
    config.lineSpeedRange = [int(x) for x in workConfig.get("informalMarksGrid", "lineSpeedRange", fallback="1,20").split(",")]
    config.baseWidthRange = [int(x) for x in workConfig.get("informalMarksGrid", "baseWidthRange", fallback="18,180").split(",")]
    config.backTrackRange = [int(x) for x in workConfig.get("informalMarksGrid", "backTrackRange", fallback="0,0").split(",")]

    config.verticalMovement = workConfig.getboolean("informalMarksGrid", "verticalMovement", fallback=False)
    config.horizontalMovement = workConfig.getboolean("informalMarksGrid", "horizontalMovement", fallback=False)
    config.horizontalMovementProb = float(workConfig.get("informalMarksGrid", "horizontalMovementProb", fallback="0.25"))
    config.verticalMovementProb = float(workConfig.get("informalMarksGrid", "verticalMovementProb", fallback="0.25"))
    config.singleLinesAngle = float(workConfig.get("informalMarksGrid", "singleLinesAngle", fallback="0"))
    config.tangleProb = float(workConfig.get("informalMarksGrid", "tangleProb", fallback="0"))

    if config.singleLineRegularSpacing:
        _hspacing = round(config.drawingWidth / (config.numberOfinformalLines + 2))
        _vspacing = round(config.drawingHeight / (config.numberOfinformalLines + 2))
        config.rowIntervalRange = [_vspacing, _vspacing]
        config.colIntervalRange = [_hspacing, _hspacing]

    # the +/- variability of the points
    config.noiseAmplitudeRangeRow = [float(x) for x in workConfig.get("informalMarksGrid", "noiseAmplitudeRangeRow", fallback="1,1").split(",")]
    config.noiseAmplitudeRangeCol = [float(x) for x in workConfig.get("informalMarksGrid", "noiseAmplitudeRangeCol", fallback="1,1").split(",")]
    config.colFirst = workConfig.getboolean("informalMarksGrid", "colFirst", fallback=False)

    config.vertLineChange = float(workConfig.get("informalMarksGrid", "vertLineChange", fallback=0.01))
    config.horizLineChange = float(workConfig.get("informalMarksGrid", "horizLineChange", fallback=0.01))

    config.vertLineChangeRange = [float(x) for x in workConfig.get("informalMarksGrid", "vertLineChangeRange", fallback=".05,.6").split(",")]
    config.horizLineChangeRange = [float(x) for x in workConfig.get("informalMarksGrid", "horizLineChangeRange", fallback=".05,.6").split(",")]

    config.vertlineSpeedRange = [int(x) for x in workConfig.get("informalMarksGrid", "lineSpeedRange", fallback="1,20").split(",")]
    config.horzlineSpeedRange = [int(x) for x in workConfig.get("informalMarksGrid", "lineSpeedRange", fallback="1,20").split(",")]

    config.rowIntervalRange = [int(x) for x in workConfig.get("informalMarksGrid", "rowIntervalRange", fallback="1,1").split(",")]
    config.colIntervalRange = [int(x) for x in workConfig.get("informalMarksGrid", "colIntervalRange", fallback="1,1").split(",")]

    config.horizLineSpeedRange = [int(x) for x in workConfig.get("informalMarksGrid", "horizLineSpeedRange", fallback="1,20").split(",")]
    config.vertLineSpeedRange = [int(x) for x in workConfig.get("informalMarksGrid", "vertLineSpeedRange", fallback="1,20").split(",")]
    config.vertLineWidthRange = [int(x) for x in workConfig.get("informalMarksGrid", "vertLineWidthRange", fallback="18,180").split(",")]
    config.horizBaseWidthRange = [int(x) for x in workConfig.get("informalMarksGrid", "horizBaseWidthRange", fallback="18,180").split(",")]


    config.angleRange = [float(x) for x in workConfig.get("informalMarksGrid", "angleRange", fallback="0,0").split(",")]
    config.angleAltRange = [float(x) for x in workConfig.get("informalMarksGrid", "angleAltRange", fallback="-10,10").split(",")]
    config.sizeRange = float(workConfig.get("informalMarksGrid", "sizeRange", fallback=10))
    config.minXSpacing = float(workConfig.get("informalMarksGrid", "minXSpacing", fallback=-3))
    config.minYSpacing = float(workConfig.get("informalMarksGrid", "minYSpacing", fallback=-3))
    config.skipMarksProb = float(workConfig.get("informalMarksGrid", "skipMarksProb", fallback=0.25))
    config.altMarksProb = float(workConfig.get("informalMarksGrid", "altMarksProb", fallback=0.5))
    config.markMinHeight = float(workConfig.get("informalMarksGrid", "markMinHeight", fallback=24))
    config.markMinWidth = float(workConfig.get("informalMarksGrid", "markMinWidth", fallback=24))

    config.scribblexOffset = int(workConfig.get("informalMarksGrid", "scribblexOffset", fallback=0))
    config.scribbleyOffset = int(workConfig.get("informalMarksGrid", "scribbleyOffset", fallback=0))
    config.scibbleXPacking = float(workConfig.get("informalMarksGrid", "scibbleXPacking", fallback=0))
    config.scibbleYPacking = float(workConfig.get("informalMarksGrid", "scibbleYPacking", fallback=0))

    config.scribbleSkipMarksProb = float(workConfig.get("informalMarksGrid", "scribbleSkipMarksProb", fallback=0))
    config.scribbleAltMarksProb = float(workConfig.get("informalMarksGrid", "scribbleAltMarksProb", fallback=0))

    config.scribbleHeightRange = [float(x) for x in workConfig.get("informalMarksGrid", "scribbleHeightRange", fallback="4,10").split(",")]
    config.scribbleLineBaseWidthRange = int(workConfig.get("informalMarksGrid", "scribbleLineBaseWidthRange", fallback=1))

    config.scribbleRadiusXRange = [float(x) for x in workConfig.get("informalMarksGrid", "scribbleRadiusXRange", fallback="4,8").split(",")]
    config.scribbleRadiusYRange = [float(x) for x in workConfig.get("informalMarksGrid", "scribbleRadiusYRange", fallback="8,24").split(",")]

    config.scribblePoints = int(workConfig.get("informalMarksGrid", "scribblePoints", fallback=8))
    config.scribbleLoopsRange = [int(x) for x in workConfig.get("informalMarksGrid", "scribbleLoopsRange", fallback="2,2").split(",")]

    config.scribbleNoiseXRange = [float(x) for x in workConfig.get("informalMarksGrid", "anglscribbleNoiseXRangeeRange", fallback="5,5").split(",")]
    config.scribbleNoiseYRange = [float(x) for x in workConfig.get("informalMarksGrid", "scribbleNoiseYRange", fallback="5,5").split(",")]

    config.scribbleRows = int(workConfig.get("informalMarksGrid", "scribbleRows", fallback=8))
    config.scribbleCols = int(workConfig.get("informalMarksGrid", "scribbleCols", fallback=8))

    config.marksAltColorProb = float(workConfig.get("informalMarksGrid", "marksAltColorProb", fallback=0.04))
    config.scribbleAltColorProb = float(workConfig.get("informalMarksGrid", "scribbleAltColorProb", fallback=0.04))
    config.changeLinesProb = float(workConfig.get("informalMarksGrid", "changeLinesProb", fallback=0.01))
    config.changeAllLinesProb = float(workConfig.get("informalMarksGrid", "changeAllLinesProb", fallback=0.01))
    # probablility background changes
    config.changeBGProb = float(workConfig.get("informalMarksGrid", "changeBGProb", fallback=0.001))
    config.pauseProb = float(workConfig.get("informalMarksGrid", "pauseProb", fallback=0.0001))
    config.unpauseProb = float(workConfig.get("informalMarksGrid", "unpauseProb", fallback=0.0001))
    config.noChange = False

    # overrides the variable background and line alpha changes and fixes at one value the rate at which the vertical and horizontal lines
    config.useSingleMode = workConfig.getboolean("informalMarksGrid", "useSingleMode", fallback=True)

    config.scribbleOnTop = workConfig.getboolean("informalMarksGrid", "scribbleOnTop", fallback=True)
    config.singlesOnTop = workConfig.getboolean("informalMarksGrid", "singlesOnTop", fallback=False)
    config.xsOnTop = workConfig.getboolean("informalMarksGrid", "xsOnTop", fallback=False)



    # light lines on background - more like a drawing on a screen
    config.lightMode = workConfig.getboolean("informalMarksGrid", "lightMode", fallback=False)
    config.lightModeProb = float(workConfig.get("informalMarksGrid", "lightModeProb", fallback=1.0))
    config.bg_alpha_returnrate = float(workConfig.get("informalMarksGrid", "bg_alpha_returnrate", fallback=2.0))
    config.lightLinesOnGroundProb = float(workConfig.get("informalMarksGrid", "lightLinesOnGroundProb", fallback=0.0))
    config.lightLinesOnGround = workConfig.getboolean("informalMarksGrid", "lightLinesOnGround", fallback=False)

    # really there are 3 modes - black/dark lines on lighter ground, mid to light lines on lighter ground, light lines on dark ground
    config.rebuildingVerticals = False

    config.useBgBox = workConfig.getboolean("informalMarksGrid", "forcebgBox")
    config.useBgBoxProb = float(workConfig.get("informalMarksGrid", "useBgBoxProb"))
    config.bgBoxBox = tuple(map(lambda x: int(x), workConfig.get("informalMarksGrid", "bgBoxBox").split(",")))
    config.renderImageFullOverlay = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.renderDrawOver = ImageDraw.Draw(config.renderImageFullOverlay)
    config.bgBoxFill = (100, 0, 80, 100)

    config.bgTileSizeWidthMin = float(workConfig.get("informalMarksGrid", "bgTileSizeWidthMin"))
    config.bgTileSizeWidthMax = float(workConfig.get("informalMarksGrid", "bgTileSizeWidthMax"))
    config.bgTileSizeHeightMin = float(workConfig.get("informalMarksGrid", "bgTileSizeHeightMin"))
    config.bgTileSizeHeightMax = float(workConfig.get("informalMarksGrid", "bgTileSizeHeightMax"))

    config.clearbgBoxProb = float(workConfig.get("informalMarksGrid", "clearbgBoxProb"))
    config.bgGlitchCyclesMin = float(workConfig.get("informalMarksGrid", "bgGlitchCyclesMin"))
    config.bgGlitchCyclesMax = float(workConfig.get("informalMarksGrid", "bgGlitchCyclesMax"))
    config.bgGlitchDisplacementHorizontal = float(workConfig.get("informalMarksGrid", "bgGlitchDisplacementHorizontal"))
    config.bgGlitchDisplacementVertical = float(workConfig.get("informalMarksGrid", "bgGlitchDisplacementVertical"))

    config.pauseProb = float(workConfig.get("informalMarksGrid", "pauseProb", fallback=".001"))
    # config.backgroundColorChangeProb = float(workConfig.get("informalMarksGrid", "backgroundColorChangeProb", fallback=".001"))

    config.initialRunsOfBgBlocks = int(workConfig.get("informalMarksGrid", "initialRunsOfBgBlocks", fallback=0))

    loadColorConfigs()
    setLines()

    config.lineColor = setLineColor()
    setBGColor()

    if config.useBgBox:
        for _ in range(config.initialRunsOfBgBlocks):
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
