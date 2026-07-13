import random
import time
import math
from noise import *
from PIL import Image, ImageDraw, ImageChops
from modules.configuration import bcolors, pieceLogger
from modules import colorutils, panelDrawing, badpixels
from modules.blanks_and_dither_rempping import BlanksAndDitherRemapping
from modules.holder_director import Director
from pieces.screen import Holder
from modules.informal_line import InformalLine

# ################################################### #
# hatching hashing lines


class Pen:
    def __init__(self):
        pass


# -------- Util Functions   -------------- #


def R(a, b, rounded=False):
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


def _bgColorsFilling(config):
    # config.useBgBox = False if config.useBgBox   else True
    # print("bgBox")
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

    # if random.random() <= config.blankColorAsColorProb:
    #     badpixels.blankColor = config.bgColor
    #     config.blankColor = config.bgColor
    # else:
    #     badpixels.blankColor = (0, 0, 0, 255)
    #     # setting the alpha to a lower number so that when
    #     # the blank changes, it comes in over a second or two
    #     config.blankColor = (0, 0, 0, 15)

    if random.random() < config.lightLinesOnGroundProb:
        config.lightLinesOnGround = True
    else:
        config.lightLinesOnGround = False

    config.bgBoxColorRange = random.choice(config.activePalette.bgBoxColorRanges)

    # pieceLogger("New BG")


# -------- Line Functions    -------------- #

# ---- TO BE COMBINED WHEN PIECE IS MORE CLEAR ----- #
# ---- --------------------------------------------- #

def generateMark(col, row, _lastX, _lastY, _drawingHeight, _skipMark, _markType):
    informalLine = InformalLine(1, 10)
    informalLine.lineType = 1
    informalLine.curveResolution = config.curveResolution
    informalLine.ratioFactorRange = config.ratioFactorRange
    informalLine.backTrackRange = config.backTrackRange
    informalLine.lineColorIsBgColor = False
    informalLine.tangleProb = config.tangleProb
    informalLine.draw = config.draw
    # informalLine.drawingHeight = _drawingHeight
    informalLine.scribbleHeight = random.uniform(config.scribbleHeightRange[0], config.scribbleHeightRange[1])

    informalLine.xOffset = config.scribblexOffset + col * config.scribbleRadiusXRange[1] * config.scibbleXPacking
    informalLine.yOffset = config.scribbleyOffset + row * config.scribbleRadiusYRange[1] * config.scibbleYPacking

    informalLine.radiusX = random.uniform(config.scribbleRadiusXRange[0], config.scribbleRadiusXRange[1])
    informalLine.radiusY = random.uniform(config.scribbleRadiusYRange[0], config.scribbleRadiusYRange[1])
    informalLine.baseWidth = int(random.uniform(0, config.scribbleLineBaseWidthRange))
    # informalLine.pointPerLine = 16
    # informalLine.pointsPerLoop = 16
    informalLine.points = config.scribblePoints
    informalLine.loops = int(random.uniform(config.scribbleLoopsRange[0], config.scribbleLoopsRange[1]))

    informalLine.noiseX = random.uniform(config.scribbleNoiseXRange[0], config.scribbleNoiseXRange[1])
    informalLine.noiseY = random.uniform(config.scribbleNoiseYRange[0], config.scribbleNoiseYRange[1])

    informalLine.lineColor = setLineColor()
    if random.random() < 0.02:
        informalLine.lineColor = (int(random.uniform(40, 255)), 6, 30, 60)
    if random.random() < 0.02:
        _tVal = int(random.uniform(40, 255))
        informalLine.lineColor = (0, _tVal, _tVal, 60)
    if random.random() < config.scribbleSkipMarksProb:
        _skipMark = True
    if not _skipMark:
        informalLine.generateScribble()
        config.informalLineUnits.append(informalLine)


def drawSingleMark(col, row, _lastX, _lastY, _drawingHeight, _skipMark):
    informalLine = InformalLine(col)
    informalLine.curveResolution = config.curveResolution
    informalLine.ratioFactorRange = config.ratioFactorRange
    informalLine.backTrackRange = config.backTrackRange
    informalLine.lineColorIsBgColor = False
    informalLine.tangleProb = config.tangleProb
    informalLine.draw = config.draw

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
    if random.random() < 0.05:
        informalLine.lineColor = (int(random.uniform(40, 255)), 6, 30, 60)
    if random.random() < 0.05:
        _tVal = int(random.uniform(40, 255))
        informalLine.lineColor = (0, _tVal, _tVal, 60)
    informalLine.reconfigure()
    informalLine.generateInformalLine()
    informalLine.isColumn = 1
    if not _skipMark:
        config.informalLineUnits.append(informalLine)


def drawXMark(col, row, _lastX, _lastY, _drawingHeight, _skipMark):
    _clr = None
    for i in range(0, 2):
        informalLine = InformalLine(col, max(config.markMinWidth, config.markMinHeight))
        informalLine.curveResolution = config.curveResolution
        informalLine.ratioFactorRange = config.ratioFactorRange
        informalLine.backTrackRange = config.backTrackRange
        informalLine.lineColorIsBgColor = False
        informalLine.tangleProb = config.tangleProb
        informalLine.draw = config.draw

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
            if random.random() < 0.05:
                informalLine.lineColor = (int(random.uniform(40, 255)), 6, 30, 60)
            if random.random() < 0.05:
                _tVal = int(random.uniform(40, 255))
                informalLine.lineColor = (0, _tVal, _tVal, 60)
            _clr  = informalLine.lineColor 
        else :
            informalLine.lineColor = _clr


        informalLine.reconfigure()
        informalLine.generateInformalLine()
        informalLine.isColumn = 1
        if not _skipMark:
            config.informalLineUnits.append(informalLine)

# ---- --------------------------------------------- #
# ---- --------------------------------------------- #


def setLines():
    pieceLogger(f"[setLines] New Lines:")
    config.informalLineUnits = []
    setGridLines()
    generateScribbles()


def generateScribbles():
    pieceLogger(f"[generateScribbles] Making scribble marks")     
    config.line_alpha = R(config.activePalette.line_alpha_range[0], config.activePalette.line_alpha_range[1], True)
    config.bg_alpha_base = R(config.activePalette.bg_alpha_range[0], config.activePalette.bg_alpha_range[1], True)

    for _row in range(0, config.scribbleRows):
        for _col in range(0, config.scribbleCols):
            _skipMark = False
            generateMark(_col, _row, 0, 0, 0, _skipMark, 1)
    config.numberOfinformalLines = len(config.informalLineUnits)


def setGridLines():
    pieceLogger(f"[setGridLines] Making Grid:  {config.drawingWidth } {config.drawingHeight }")

    config.colInterval = random.randint(int(config.colIntervalRange[0]), int(config.colIntervalRange[1]))
    config.rowInterval = random.randint(int(config.rowIntervalRange[0]), int(config.rowIntervalRange[1]))

    # config.markMinWidth = round(config.canvasWidth/config.colInterval,2)
    # pieceLogger(f"colInterval {config.colInterval} {config.markMinWidth} {config.xOffset}")

    config.noiseAmplitudeCol = random.uniform(float(config.noiseAmplitudeRangeCol[0]), float(config.noiseAmplitudeRangeCol[1]))
    config.noiseAmplitudeRow = random.uniform(float(config.noiseAmplitudeRangeRow[0]), float(config.noiseAmplitudeRangeRow[1]))
    config.vertLineChange = R(config.vertLineChangeRange[0], config.vertLineChangeRange[1])
    config.horizLineChange = R(config.horizLineChangeRange[0], config.horizLineChangeRange[1])
    config.line_alpha = R(config.activePalette.line_alpha_range[0], config.activePalette.line_alpha_range[1], True)
    config.bg_alpha_base = R(config.activePalette.bg_alpha_range[0], config.activePalette.bg_alpha_range[1], True)

    def add_col_lines():
        # config.v_pts = []
        for row in range(config.rowInterval):
            _lastX = 0
            _lastY = config.yOffset + row * (config.minYSpacing)
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
                    drawSingleMark(col, row, _lastX, _lastY, _drawingHeight, _skipMark)
                else:
                    drawXMark(col, row, _lastX, _lastY, _drawingHeight, _skipMark)

    add_col_lines()

    config.numberOfinformalLines = len(config.informalLineUnits)
    # pieceLogger(f"New Lines {config.numberOfinformalLines}")


def changeLine():
    _changeLine = random.randint(0, len(config.informalLineUnits) - 1)
    _lineUnit: InformalLine = config.informalLineUnits[_changeLine]
    if _lineUnit.lineType == 0:
        _lineUnit.reconfigure()


def drawTheBG():

    # config.bg_alpha = 255
    config.bgColor = (config.bgColor[0], config.bgColor[1], config.bgColor[2], round(config.bg_alpha))
    config.draw.rectangle((0, 0, config.drawingWidth, config.drawingHeight), fill=config.bgColor)

    # if config.bg_alpha != config.bg_alpha_base :
    #     pieceLogger(f"{config.bg_alpha}  /  {config.bg_alpha_base}")


def updateLines():
    global config

    for informalLineUnitIndex in range(0, len(config.informalLineUnits)):
        lineUnit: InformalLine
        lineUnit = config.informalLineUnits[informalLineUnitIndex]
        if lineUnit.lineType == 0:
            # lineUnit.drawTheLineComplete()
            lineUnit.drawLinePoints()
        if lineUnit.lineType == 1:
            lineUnit.drawTheLineComplete()


# ---- looping and redrawing --------


def runWork():
    global configk
    print(bcolors.OKGREEN + "** " + bcolors.BOLD)
    print("Running hatchingmarks.py")
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

    # adding check on bg alpha as index of transition state - don't want another transition
    # stomping on the one in progress

    # if random.random() < config.changeBGProb and not config.noChange:
    if random.random() < config.changeBGProb and config.bg_alpha == config.bg_alpha_base and not config.noChange:
        config.bg_alpha = 0
        # config.lightMode = False if random.random() > config.lightModeProb else True
        # pieceLogger(f"change BG {config.lightMode} {config.bg_alpha}")
        # setBGColor()
        # setLines()

        for _u in range(config.numberOfinformalLines):
            informalLine = config.informalLineUnits[_u]
            informalLine.lineColor = setLineColor()

            # pieceLogger(f"line {informalLine.lineColor} <= {config.lightMode}")

    for _u in range(config.numberOfinformalLines):
        if random.random() < config.changeLinesProb and not config.noChange:
            informalLine: InformalLine = config.informalLineUnits[_u]
            if informalLine.lineType == 0:
                informalLine.reconfigure()
                informalLine.generateInformalLine()

            if informalLine.lineType == 1:
                informalLine.generateScribble()

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
        _bgColorsFilling(config)

    reDraw()

    if random.SystemRandom().random() < config.clearbgBoxProb:
        clearbgBox()

    ########### RENDERING AS A MOCKUP OR AS REAL ###########
    if config.useDrawingPoints == True:
        config.panelDrawing.canvasToUse = config.image
        config.panelDrawing.render()

    # badpixels.drawBlanks(config.image, False)
    config.destinationImage.paste(config.image, (round(config.imageXPOS), round(config.imageYPOS)), config.image)
    config.destinationImage.paste(config.image, (round(config.imageXPOS - config.drawingWidth), round(config.imageYPOS)), config.image)
    config.destinationImage.paste(config.underLayer, (0, 0), config.underLayer)
    if not config.lightMode:
        config.imageXPOS += config.imageXPOSSpeed
    # config.imageYPOS += config.YPOSSpeed

    if config.imageXPOS >= config.drawingWidth:
        config.imageXPOS = 0

    # if config.imageYPOS >= config.pictureHeight:
    # config.render(config.image, round(0, 0, config.drawingWidth, config.drawingHeight)
    # if config.usingPanelOverlays:
    #     drawPanelVariations(config.destinationImage)
    overlayControls.targetImageRef = config.destinationImage
    overlayControls.overlayImageRef = config.overlayImage
    overlayControls.handleOverlayActions()
    config.render(config.destinationImage, 0, 0)


# # ----- panel based overlays ---------
# # adding panel modulation to mimic physical panel differences
# def setPanelOverlays():
#     global config
#     if not config.usingPanelOverlays:
#         return

#     panelOverLayList = []
#     config.panelOverLayList = []
#     config.overlayImageDraw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=(0, 0, 0, 0))

#     _totalPanels = config.panelRows * config.panelColumns
#     _numPanels = random.randint(config.panelOverlayRange[0], min(_totalPanels, config.panelOverlayRange[1]))

#     # create an array of panel spots then joggle it
#     for c in range(0, config.panelColumns):
#         for r in range(0, config.panelRows):
#             panelOverLayList.append([c, r])

#     random.shuffle(panelOverLayList)

#     for i in range(_numPanels):
#         config.panelOverLayList.append(panelOverLayList[i])


# def drawPanelVariations(targetImageRef):
#     global config
#     for p in config.panelOverLayList:
#         x0 = p[0] * config.panelWidth
#         y0 = p[1] * config.panelHeight
#         x1 = x0 + config.panelWidth
#         y1 = y0 + config.panelHeight
#         config.overlayImageDraw.rectangle((x0, y0, x1, y1), fill=config.bgColor)

#     # tempImage = ImageChops.blend(targetImageRef, config.overlayImage, config.panelOverlayAmount)
#     tempImage = ImageChops.add(targetImageRef, config.overlayImage, round(100 * config.panelOverlayAmount))
#     targetImageRef.paste(tempImage, (0, 0), tempImage)


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
    paletteList = workConfig.get("hatchingmarks", "paletteSets").split(",")

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

    config.imageXPOS = 0
    config.imageXPOSSpeed = float(workConfig.get("hatchingmarks", "imageXPOSSpeed", fallback=0))
    config.imageYPOS = 0
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

    config.drawingWidth = int(workConfig.get("hatchingmarks", "drawingWidth", fallback=f"{config.canvasWidth}"))
    config.drawingHeight = int(workConfig.get("hatchingmarks", "drawingHeight", fallback=f"{config.canvasHeight}"))

    config.largestDim = max(config.drawingWidth, config.drawingHeight)

    # refinements for setting points per column and row so amplitude of noise can be adjusted to be more even if aspect ratio is more extreme - e.g narrow beam
    # but also, lower number makes the line more purely rectilinear so can give a greater focus to one directions linearity
    config.pointsPerLine = int(workConfig.get("hatchingmarks", "pointsPerLine"))
    config.pointsPerLineCol = int(workConfig.get("hatchingmarks", "pointsPerLineCol", fallback=config.pointsPerLine))
    config.pointsPerLineRow = int(workConfig.get("hatchingmarks", "pointsPerLineRow", fallback=config.pointsPerLine))

    # adjust higher for higer resolution
    config.curveResolution = int(workConfig.get("hatchingmarks", "curveResolution", fallback=10))

    # not really used - was used in first iteration using Perlin Noise
    config.noiseSeed = random.random()

    # if the shape is not single-lines, will be determined by rows and columns
    config.numberOfinformalLines = int(workConfig.get("hatchingmarks", "numberOfinformalLines", fallback="3"))
    # the edge spacing - critical to making the drawing as the edges matter more than the sum of the lines
    config.xOffset = int(workConfig.get("hatchingmarks", "xOffset"))
    config.yOffset = int(workConfig.get("hatchingmarks", "yOffset"))

    # for single linesneSpeed
    config.renderLinesAsEnvelope = workConfig.getboolean("hatchingmarks", "renderLinesAsEnvelope", fallback=False)
    config.drawVertical = workConfig.getboolean("hatchingmarks", "drawVertical", fallback=True)
    config.drawHorizontal = workConfig.getboolean("hatchingmarks", "drawHorizontal", fallback=True)
    config.singleLineRegularSpacing = workConfig.getboolean("hatchingmarks", "singleLineRegularSpacing", fallback=False)
    config.drawingHeightRange = [int(x) for x in workConfig.get("hatchingmarks", "drawingHeightRange", fallback="18,180").split(",")]
    config.lineSpeedRange = [int(x) for x in workConfig.get("hatchingmarks", "lineSpeedRange", fallback="1,20").split(",")]
    config.baseWidthRange = [int(x) for x in workConfig.get("hatchingmarks", "baseWidthRange", fallback="18,180").split(",")]
    config.backTrackRange = [int(x) for x in workConfig.get("hatchingmarks", "backTrackRange", fallback="0,0").split(",")]
    config.ratioFactorRange = [float(x) for x in workConfig.get("hatchingmarks", "ratioFactorRange", fallback="18,180").split(",")]
    config.verticalMovement = workConfig.getboolean("hatchingmarks", "verticalMovement", fallback=False)
    config.horizontalMovement = workConfig.getboolean("hatchingmarks", "horizontalMovement", fallback=False)
    config.horizontalMovementProb = float(workConfig.get("hatchingmarks", "horizontalMovementProb", fallback="0.25"))
    config.verticalMovementProb = float(workConfig.get("hatchingmarks", "verticalMovementProb", fallback="0.25"))
    config.singleLinesAngle = float(workConfig.get("hatchingmarks", "singleLinesAngle", fallback="0"))
    config.tangleProb = float(workConfig.get("hatchingmarks", "tangleProb", fallback="0"))

    if config.singleLineRegularSpacing:
        _hspacing = round(config.drawingWidth / (config.numberOfinformalLines + 2))
        _vspacing = round(config.drawingHeight / (config.numberOfinformalLines + 2))
        config.rowIntervalRange = [_vspacing, _vspacing]
        config.colIntervalRange = [_hspacing, _hspacing]

    # means the row interval is the same as the column interval - if they are independent then
    # there can be more extreme column or row spacing, othewise they get the same ratio
    config.uniformRatio = workConfig.getboolean("hatchingmarks", "uniformRatio", fallback=False)

    # forces grid to squares - but is not currently compensated to will get ragged and missing
    # grids at edges of drawing
    config.squareRatio = workConfig.getboolean("hatchingmarks", "squareRatio", fallback=False)

    # the +/- variability of the points
    config.noiseAmplitudeRangeRow = [float(x) for x in workConfig.get("hatchingmarks", "noiseAmplitudeRangeRow", fallback="1,1").split(",")]
    config.noiseAmplitudeRangeCol = [float(x) for x in workConfig.get("hatchingmarks", "noiseAmplitudeRangeCol", fallback="1,1").split(",")]
    config.colFirst = workConfig.getboolean("hatchingmarks", "colFirst", fallback=False)

    config.vertLineChange = float(workConfig.get("hatchingmarks", "vertLineChange", fallback=0.01))
    config.horizLineChange = float(workConfig.get("hatchingmarks", "horizLineChange", fallback=0.01))

    config.vertLineChangeRange = [float(x) for x in workConfig.get("hatchingmarks", "vertLineChangeRange", fallback=".05,.6").split(",")]
    config.horizLineChangeRange = [float(x) for x in workConfig.get("hatchingmarks", "horizLineChangeRange", fallback=".05,.6").split(",")]

    config.vertlineSpeedRange = [int(x) for x in workConfig.get("hatchingmarks", "lineSpeedRange", fallback="1,20").split(",")]
    config.horzlineSpeedRange = [int(x) for x in workConfig.get("hatchingmarks", "lineSpeedRange", fallback="1,20").split(",")]

    config.rowIntervalRange = [int(x) for x in workConfig.get("hatchingmarks", "rowIntervalRange", fallback="1,1").split(",")]
    config.colIntervalRange = [int(x) for x in workConfig.get("hatchingmarks", "colIntervalRange", fallback="1,1").split(",")]

    config.horizLineSpeedRange = [int(x) for x in workConfig.get("hatchingmarks", "horizLineSpeedRange", fallback="1,20").split(",")]
    config.vertLineSpeedRange = [int(x) for x in workConfig.get("hatchingmarks", "vertLineSpeedRange", fallback="1,20").split(",")]
    config.vertLineWidthRange = [int(x) for x in workConfig.get("hatchingmarks", "vertLineWidthRange", fallback="18,180").split(",")]
    config.horizBaseWidthRange = [int(x) for x in workConfig.get("hatchingmarks", "horizBaseWidthRange", fallback="18,180").split(",")]

    config.rowAdj = int(workConfig.get("hatchingmarks", "rowAdj", fallback=0))
    config.colAdj = int(workConfig.get("hatchingmarks", "colAdj", fallback=0))

    config.angleRange = [float(x) for x in workConfig.get("hatchingmarks", "angleRange", fallback="0,0").split(",")]
    config.angleAltRange = [float(x) for x in workConfig.get("hatchingmarks", "angleAltRange", fallback="-10,10").split(",")]
    config.sizeRange = float(workConfig.get("hatchingmarks", "sizeRange", fallback=10))
    config.minXSpacing = float(workConfig.get("hatchingmarks", "minXSpacing", fallback=-3))
    config.minYSpacing = float(workConfig.get("hatchingmarks", "minYSpacing", fallback=-3))
    config.skipMarksProb = float(workConfig.get("hatchingmarks", "skipMarksProb", fallback=0.25))
    config.altMarksProb = float(workConfig.get("hatchingmarks", "altMarksProb", fallback=0.5))
    config.markMinHeight = float(workConfig.get("hatchingmarks", "markMinHeight", fallback=24))
    config.markMinWidth = float(workConfig.get("hatchingmarks", "markMinWidth", fallback=24))

    config.scribblexOffset = int(workConfig.get("hatchingmarks", "colAdj", fallback=0))
    config.scribbleyOffset = int(workConfig.get("hatchingmarks", "scribbleyOffset", fallback=0))
    config.scibbleXPacking = float(workConfig.get("hatchingmarks", "scibbleXPacking", fallback=0))
    config.scibbleYPacking = float(workConfig.get("hatchingmarks", "scibbleYPacking", fallback=0))

    config.scribbleSkipMarksProb = float(workConfig.get("hatchingmarks", "scribbleSkipMarksProb", fallback=0))
    config.scribbleAltMarksProb = float(workConfig.get("hatchingmarks", "scribbleAltMarksProb", fallback=0))

    config.scribbleHeightRange = [float(x) for x in workConfig.get("hatchingmarks", "scribbleHeightRange", fallback="4,10").split(",")]
    config.scribbleLineBaseWidthRange = int(workConfig.get("hatchingmarks", "scribbleLineBaseWidthRange", fallback=1))

    config.scribbleRadiusXRange = [float(x) for x in workConfig.get("hatchingmarks", "scribbleRadiusXRange", fallback="4,8").split(",")]
    config.scribbleRadiusYRange = [float(x) for x in workConfig.get("hatchingmarks", "scribbleRadiusYRange", fallback="8,24").split(",")]

    config.scribblePoints = int(workConfig.get("hatchingmarks", "scribblePoints", fallback=8))
    config.scribbleLoopsRange = [int(x) for x in workConfig.get("hatchingmarks", "scribbleLoopsRange", fallback="2,2").split(",")]

    config.scribbleNoiseXRange = [float(x) for x in workConfig.get("hatchingmarks", "anglscribbleNoiseXRangeeRange", fallback="5,5").split(",")]
    config.scribbleNoiseYRange = [float(x) for x in workConfig.get("hatchingmarks", "scribbleNoiseYRange", fallback="5,5").split(",")]

    config.scribbleRows = int(workConfig.get("hatchingmarks", "scribbleRows", fallback=8))
    config.scribbleCols = int(workConfig.get("hatchingmarks", "scribbleCols", fallback=8))

    config.changeLinesProb = float(workConfig.get("hatchingmarks", "changeLinesProb", fallback=0.01))
    config.changeAllLinesProb = float(workConfig.get("hatchingmarks", "changeAllLinesProb", fallback=0.01))
    # probablility background changes
    config.changeBGProb = float(workConfig.get("hatchingmarks", "changeBGProb", fallback=0.001))
    config.pauseProb = float(workConfig.get("hatchingmarks", "pauseProb", fallback=0.0001))
    config.unpauseProb = float(workConfig.get("hatchingmarks", "unpauseProb", fallback=0.0001))
    config.noChange = False

    # overrides the variable background and line alpha changes and fixes at one value the rate at which the vertical and horizontal lines
    config.useSingleMode = workConfig.getboolean("hatchingmarks", "useSingleMode", fallback=True)

    # light lines on background - more like a drawing on a screen
    config.lightMode = workConfig.getboolean("hatchingmarks", "lightMode", fallback=False)
    config.lightModeProb = float(workConfig.get("hatchingmarks", "lightModeProb", fallback=1.0))
    config.bg_alpha_returnrate = float(workConfig.get("hatchingmarks", "bg_alpha_returnrate", fallback=2.0))
    config.lightLinesOnGroundProb = float(workConfig.get("hatchingmarks", "lightLinesOnGroundProb", fallback=0.0))
    config.lightLinesOnGround = workConfig.getboolean("hatchingmarks", "lightLinesOnGround", fallback=False)

    # really there are 3 modes - black/dark lines on lighter ground, mid to light lines on lighter ground, light lines on dark ground
    config.rebuildingVerticals = False

    config.useBgBox = workConfig.getboolean("hatchingmarks", "forcebgBox")
    config.useBgBoxProb = float(workConfig.get("hatchingmarks", "useBgBoxProb"))
    config.bgBoxBox = tuple(map(lambda x: int(x), workConfig.get("hatchingmarks", "bgBoxBox").split(",")))
    config.renderImageFullOverlay = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.renderDrawOver = ImageDraw.Draw(config.renderImageFullOverlay)
    config.bgBoxFill = (100, 0, 80, 100)

    config.bgTileSizeWidthMin = float(workConfig.get("hatchingmarks", "bgTileSizeWidthMin"))
    config.bgTileSizeWidthMax = float(workConfig.get("hatchingmarks", "bgTileSizeWidthMax"))
    config.bgTileSizeHeightMin = float(workConfig.get("hatchingmarks", "bgTileSizeHeightMin"))
    config.bgTileSizeHeightMax = float(workConfig.get("hatchingmarks", "bgTileSizeHeightMax"))

    config.clearbgBoxProb = float(workConfig.get("hatchingmarks", "clearbgBoxProb"))
    config.bgGlitchCyclesMin = float(workConfig.get("hatchingmarks", "bgGlitchCyclesMin"))
    config.bgGlitchCyclesMax = float(workConfig.get("hatchingmarks", "bgGlitchCyclesMax"))
    config.bgGlitchDisplacementHorizontal = float(workConfig.get("hatchingmarks", "bgGlitchDisplacementHorizontal"))
    config.bgGlitchDisplacementVertical = float(workConfig.get("hatchingmarks", "bgGlitchDisplacementVertical"))

    config.drawMoire = workConfig.getboolean("hatchingmarks", "drawMoire")
    config.drawMoireProb = float(workConfig.get("hatchingmarks", "drawMoireProb"))
    config.drawMoireProbOff = float(workConfig.get("hatchingmarks", "drawMoireProbOff"))

    config.moireXPos = int(workConfig.get("hatchingmarks", "moireXPos"))
    config.moireYPos = int(workConfig.get("hatchingmarks", "moireYPos"))
    config.moireXDistance = int(workConfig.get("hatchingmarks", "moireXDistance"))
    config.moireYDistance = int(workConfig.get("hatchingmarks", "moireYDistance"))
    config.setMoireColor = workConfig.getboolean("hatchingmarks", "setMoireColor")
    config.moireColorAltProb = float(workConfig.get("hatchingmarks", "moireColorAltProb"))
    config.moireColor = tuple(map(lambda x: int(x), workConfig.get("hatchingmarks", "moireColor").split(",")))
    config.moireColorAlt = tuple(
        map(
            lambda x: int(x),
            workConfig.get("hatchingmarks", "moireColorAlt").split(","),
        )
    )

    config.pauseProb = float(workConfig.get("hatchingmarks", "pauseProb", fallback=".001"))
    # config.backgroundColorChangeProb = float(workConfig.get("hatchingmarks", "backgroundColorChangeProb", fallback=".001"))

    config.initialRunsOfBgBlocks = int(workConfig.get("hatchingmarks", "initialRunsOfBgBlocks", fallback=0))

    loadColorConfigs()
    # loadFilterRemapping()
    # resetPolyBlanks()
    # if config.usingPanelOverlays:
    #     setPanelOverlays()
    setLines()
    config.lineColor = setLineColor()
    setBGColor()

    # badpixels.setBlanksOnScreen(config)

    if config.useBgBox:
        for _ in range(config.initialRunsOfBgBlocks):
            _bgColorsFilling(config)

    overlayControls = BlanksAndDitherRemapping(config, workConfig, "hatchingmarks")
    # for blanks
    overlayControls.destinationImageDraw = config.destinationImageDraw
    overlayControls.targetImageRef = config.destinationImage
    # for overlay
    overlayControls.overlayImage = config.overlayImage
    overlayControls.overlayImageDraw = config.overlayImageDraw
    overlayControls.setPanelOverlays()

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
    config.redrawSpeed = float(workConfig.get("hatchingmarks", "redrawSpeed", fallback=0.02))
    config.slotRate = float(workConfig.get("hatchingmarks", "slotRate", fallback=0.03))
    config.directorController = Director(config)
    config.directorController.slotRate = config.slotRate

    if run:
        runWork()
