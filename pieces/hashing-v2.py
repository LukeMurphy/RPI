from logging import config
import random
import time
import math
from noise import *
from modules.configuration import bcolors, pieceLogger
from modules import colorutils, panelDrawing, badpixels
from PIL import Image, ImageDraw, ImageChops

# ################################################### #
# hatching hashing lines


class InformalLine:

    points = 1
    pointPerLine = 3
    resolution = 50
    drawingHeight = 100
    noiseAmplitude = 1.0
    xOffset = 100
    yOffset = 0
    angle = 0
    direction = 0

    def __init__(self, unitNumber):
        self.unitNumber = unitNumber
        self.canvas = Image.new("RGBA", (config.largestDim, config.largestDim))
        self.draw = ImageDraw.Draw(self.canvas)

    def reconfigure(self):
        self.lineSpeed = random.randint(self.lineSpeedRange[0], self.lineSpeedRange[1])
        self.baseWidth = random.uniform(self.baseWidthRange[0], self.baseWidthRange[1])
        self.noiseAmplitude = random.uniform(float(self.noiseAmplitudeRange[0]), float(self.noiseAmplitudeRange[1]))

    def getCurvePoints(self):

        self.curvedPoints = []

        for i in range(self.points):
            p0 = self.rawPts[max(0, i - 1)]
            p1 = self.rawPts[i]
            p2 = self.rawPts[i + 1]
            p3 = self.rawPts[min(self.points - 1, i + 2)]

            for step in range(self.resolution):
                t = step / float(self.resolution)  # 0 <= t < 1

                x = catmull_rom(p0[0], p1[0], p2[0], p3[0], t)
                y = catmull_rom(p0[1], p1[1], p2[1], p3[1], t)

                self.curvedPoints.append([x, y])

    def generateRawLine(self):
        self.rawPts = []
        pointSpacing = self.drawingHeight / self.points

        for i in range(self.points):
            a = i * pointSpacing
            b = R(-self.noiseAmplitude, self.noiseAmplitude)
            if random.random() < config.tangleProb and i != 0 and i != self.points - 1 and abs(b) > self.noiseAmplitude * 0.75:
                a -= random.uniform(config.backTrackRange[0], config.backTrackRange[1])
            self.rawPts.append((round(b + self.xOffset), round(a + self.yOffset)))

        # ensures the last point at the right or bottom closes the box
        self.rawPts.append([b + self.xOffset, self.drawingHeight + self.yOffset])
        # Extra points for smoother Bézier start/end
        # pts.insert(0, pts[0])

    def generateInformalLine(self):

        self.points = random.randint(3, self.pointPerLine)
        self.ratioFactor = random.uniform(config.ratioFactorRange[0], config.ratioFactorRange[1])
        self.resolution = config.curveResolution
        self.direction = 1 if random.random() < 0.5 else 0

        self.generateRawLine()
        self.getCurvePoints()
        self.smoothPointsForDrawing = []
        self.smoothPointsForDrawing.extend([pt[0] + self.xOffset, pt[1] + self.yOffset] for pt in self.curvedPoints)
        # pieceLogger(f"Made line {self.xOffset}  {self.yOffset} {self.drawingHeight}")


# -------- Util Functions   -------------- #


def R(a, b, rounded=False):
    if not rounded:
        return random.uniform(a, b)
    else:
        return round(random.uniform(a, b))


def catmull_rom(p0, p1, p2, p3, t):
    t2 = t * t
    t3 = t2 * t

    return 0.5 * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3)


def getColor(r, g, b, a):
    clr = list(round(i * config.brightness) for i in [r, g, b])
    clr.append(a)
    return tuple(clr)


# -------- Line Attribute Function --------- #


def setLineColor():
    _line_alpha = config.line_alpha
    # _minVal = 0.0
    # _maxVal = 0.1
    if config.lightMode:
        _minVal = 0.65
        _maxVal = 1.0

    config.lineColor = colorutils.getRandomColorHSV(
        config.line_minHue,
        config.line_maxHue,
        config.line_minSaturation,
        config.line_maxSaturation,
        config.line_minValue,
        config.line_maxValue,
        0,
        0,
        _line_alpha,
        config.brightness,
    )
    # pieceLogger(f"New Line Color {config.lineColor}")


def setBGColor():
    _bg_alpha = round(config.bg_alpha)
    _minVal = 0.5
    _maxVal = 0.70
    if config.lightMode:
        _minVal = 0.0
        _maxVal = 0.1
    config.bgColor = colorutils.getRandomColorHSV(
        config.bg_minHue,
        config.bg_maxHue,
        config.bg_minSaturation,
        config.bg_maxSaturation,
        config.bg_minValue,
        config.bg_maxValue,
        config.bg_dropHueMin,
        config.bg_dropHueMax,
        _bg_alpha,
        config.brightness,
    )

    if random.random() <  .5 :
        badpixels.blankColor = config.bgColor
    else :
        badpixels.blankColor = (0,0,0,255)

    # pieceLogger("New BG")


# -------- Line Functions    -------------- #


def setLines():
    pieceLogger(f"New Lines: {config.drawingShape}")
    config.informalLineUnits = []

    if config.drawingShape == "grid":
        setGridLines()
    else:
        setRegularSpacing()
        for _u in range(config.numberOfinformalLines):
            informalLine = InformalLine(_u)
            informalLine.angle = config.singleLinesAngle
            informalLine.lineColor = colorutils.getRandomColorHSV(
                config.line_minHue,
                config.line_maxHue,
                config.line_minSaturation,
                config.line_maxSaturation,
                config.line_minValue,
                config.line_maxValue,
                0,
                0,
                round(random.uniform(config.line_alpha_range[0], config.line_alpha_range[1])),
                config.brightness,
            )

            if config.singleLineRegularSpacing:
                informalLine.xOffset = config.xOffset + config.rowSpacing * _u

            informalLine.drawingHeight = round(random.uniform(config.drawingHeightRange[0], config.drawingHeightRange[1]))
            informalLine.xOffset = round(config.xOffset + config.largestDim / 2 + random.uniform(-config.distributionRange, config.distributionRange))
            informalLine.yOffset = round(config.largestDim - informalLine.drawingHeight - config.yOffset)

            informalLine.lineSpeed = random.randint(config.lineSpeedRange[0], config.lineSpeedRange[1])
            informalLine.baseWidth = random.uniform(config.baseWidthRange[0], config.baseWidthRange[1])
            informalLine.noiseAmplitude = random.uniform(float(config.noiseAmplitudeRange[0]), float(config.noiseAmplitudeRange[1]))

            informalLine.generateInformalLine()
            config.informalLineUnits.append(informalLine)


def setRegularSpacing():
    config.colInterval = random.randint(int(config.colIntervalRange[0]), int(config.colIntervalRange[1]))

    # if uniformRatio, the column ratio is used for the rows as well - this means even rectangles across field
    if config.uniformRatio:
        config.rowInterval = config.colInterval
    else:
        config.rowInterval = random.randint(int(config.rowIntervalRange[0]), int(config.rowIntervalRange[1]))

    config.colSpacing = (config.drawingWidth - 2 * config.xOffset) / config.colInterval
    config.rowSpacing = (config.drawingHeight - 2 * config.yOffset) / config.rowInterval

    # if squareRatio, the column ratio and spacing is used for the rows as well - this means all squares across field
    if config.squareRatio:
        config.rowSpacing = config.colSpacing


def setGridLines():
    pieceLogger(f"Making Grid: {config.drawingShape} {config.drawingWidth } {config.drawingHeight }")

    setRegularSpacing()

    config.noiseAmplitudeCol = random.uniform(float(config.noiseAmplitudeRangeCol[0]), float(config.noiseAmplitudeRangeCol[1]))
    config.noiseAmplitudeRow = random.uniform(float(config.noiseAmplitudeRangeRow[0]), float(config.noiseAmplitudeRangeRow[1]))

    # config.h_pts = []
    for row in range(config.rowInterval + config.rowAdj):
        informalLine = InformalLine(row)
        # h_pts = generateInformalLine(config.pointsPerLineRow, config.xOffset, config.yOffset + config.rowSpacing * row, True)
        # config.h_pts.append(h_pts)
        informalLine.xOffset = config.xOffset + config.rowSpacing * row
        informalLine.yOffset = config.yOffset
        informalLine.drawingHeight = config.drawingWidth - 2 * config.xOffset
        informalLine.angle = 90
        informalLine.pointPerLine = config.pointsPerLineRow
        informalLine.lineSpeedRange = config.horizLineSpeedRange
        informalLine.baseWidthRange = config.horizBaseWidthRange
        informalLine.noiseAmplitudeRange = config.noiseAmplitudeRangeRow

        informalLine.lineColor = colorutils.getRandomColorHSV(
            config.line_minHue,
            config.line_maxHue,
            config.line_minSaturation,
            config.line_maxSaturation,
            config.line_minValue,
            config.line_maxValue,
            0,
            0,
            round(random.uniform(config.line_alpha_range[0], config.line_alpha_range[1])),
            config.brightness,
        )

        informalLine.reconfigure()
        informalLine.generateInformalLine()
        config.informalLineUnits.append(informalLine)

    # config.v_pts = []
    for col in range(config.colInterval + config.colAdj):
        # v_pts = generateInformalLine(config.pointsPerLineCol, config.xOffset + config.colSpacing * col, config.yOffset, False)
        # config.v_pts.append(v_pts)
        informalLine = InformalLine(col)
        informalLine.xOffset = config.xOffset + config.colSpacing * col
        informalLine.yOffset = config.yOffset
        informalLine.drawingHeight = config.drawingHeight - 2 * config.yOffset

        informalLine.pointPerLine = config.pointsPerLineCol
        informalLine.lineSpeedRange = config.vertLineSpeedRange
        informalLine.baseWidthRange = config.vertBaseWidthRange
        informalLine.noiseAmplitudeRange = config.noiseAmplitudeRangeCol

        informalLine.lineColor = colorutils.getRandomColorHSV(
            config.line_minHue,
            config.line_maxHue,
            config.line_minSaturation,
            config.line_maxSaturation,
            config.line_minValue,
            config.line_maxValue,
            0,
            0,
            round(random.uniform(config.line_alpha_range[0], config.line_alpha_range[1])),
            config.brightness,
        )
        informalLine.reconfigure()
        informalLine.generateInformalLine()
        # pieceLogger(f"{informalLine.xOffset}")
        config.informalLineUnits.append(informalLine)

    config.vertLineChange = R(config.vertLineChangeRange[0], config.vertLineChangeRange[1])
    config.horizLineChange = R(config.horizLineChangeRange[0], config.horizLineChangeRange[1])
    config.line_alpha = R(config.line_alpha_range[0], config.line_alpha_range[1], True)
    config.bg_alpha_base = R(config.bg_alpha_range[0], config.bg_alpha_range[1], True)

    config.numberOfinformalLines = len(config.informalLineUnits)
    # pieceLogger(f"New Lines {config.numberOfinformalLines}")


def changeLine():
    _changeLine = random.randint(0, len(config.informalLineUnits) - 1)
    config.informalLineUnits[_changeLine].reconfigure()


def drawTheLine(p1x, p1y, p2x, p2y, _n, _lineUnit):

    _p1 = [p1x, p1y]
    _p2 = [p2x, p2y]

    _dy = _p1[1] - _p2[1]
    _dx = _p1[0] - _p2[0]

    _angle = math.atan2(_dy, _dx) * 360 / math.pi

    if _angle < 0:
        _angle += 360

    _totalPts = len(_lineUnit.curvedPoints)
    _ratio1 = _n / _totalPts
    _ratio1a = _ratio1 / _lineUnit.ratioFactor
    _ratio2 = (_totalPts - _n) / _totalPts
    _ratio2a = _ratio2 / _lineUnit.ratioFactor

    _t = (_n / math.pi) / 70
    _ratio = math.sin(_t + math.pi / 5) * math.pow(math.sin(_t), 0) * _ratio1a

    _ratio = 1.0
    _ratio1a = 1.0

    _penWidth = _lineUnit.baseWidth * _ratio * _ratio1a

    _alphaBase = 2

    _r = round(190 * (_ratio * 3))
    _g = round(100 * _ratio)
    _b = round(20 * (_totalPts - _n) / _totalPts)
    _a = round(_alphaBase * _ratio)

    fillClr = [_r, _g, _b, _a]

    fillClr = _lineUnit.lineColor

    if config.drawingShape == "grid":
        # _lineUnit.draw.line([_p1[0], _p1[1], _p2[0], _p2[1]], fill=tuple(fillClr), width=round(_lineUnit.baseWidth))
        if _lineUnit.angle == 90:
            config.draw.line([_p1[1], _p1[0], _p2[1], _p2[0]], fill=tuple(fillClr), width=round(_lineUnit.baseWidth))
        else:
            config.draw.line([_p1[0], _p1[1], _p2[0], _p2[1]], fill=tuple(fillClr), width=round(_lineUnit.baseWidth))

    else:

        _orthoAngle = math.pi - math.atan2(_dy, _dx)
        _sinOrthoAngle = math.sin(_orthoAngle)
        _cosOrthoAngle = math.cos(_orthoAngle)

        _orthoD = _penWidth

        _orthoP1x = round(_orthoD * _sinOrthoAngle + _p1[0])
        _orthoP1y = round(_orthoD * _cosOrthoAngle + _p1[1])

        _orthoP2x = round(_orthoD * _sinOrthoAngle + _p2[0])
        _orthoP2y = round(_orthoD * _cosOrthoAngle + _p2[1])

        _orthoP3x = round(-_orthoD * _sinOrthoAngle + _p2[0])
        _orthoP3y = round(-_orthoD * _cosOrthoAngle + _p2[1])

        _orthoP4x = round(-_orthoD * _sinOrthoAngle + _p1[0])
        _orthoP4y = round(-_orthoD * _cosOrthoAngle + _p1[1])

        if _n > 1:
            _orthoP1x = _lineUnit.lastOrthoPoint[0]
            _orthoP1y = _lineUnit.lastOrthoPoint[1]

            _orthoP4x = _lineUnit.lastOrthoPoint[2]
            _orthoP4y = _lineUnit.lastOrthoPoint[3]

        _poly = ((_orthoP1x, _orthoP1y), (_orthoP2x, _orthoP2y), (_orthoP3x, _orthoP3y), (_orthoP4x, _orthoP4y), (_orthoP1x, _orthoP1y))

        if config.renderLinesAsEnvelope:
            _lineUnit.draw.polygon(_poly, fill=tuple(fillClr), outline=None)
        else:
            if _lineUnit.angle == 90:
                _lineUnit.draw.line([_p1[1], _p1[0], _p2[1], _p2[0]], fill=tuple(fillClr), width=round(_lineUnit.baseWidth))
            else:
                _lineUnit.draw.line([_p1[0], _p1[1], _p2[0], _p2[1]], fill=tuple(fillClr), width=round(_lineUnit.baseWidth))

        # config.draw.polygon(_poly, fill=tuple(fillClr), outline=None)

        _lineUnit.lastOrthoPoint = [_orthoP2x, _orthoP2y, _orthoP3x, _orthoP3y]


def drawTheBG():
    config.bgColor = (config.bgColor[0], config.bgColor[1], config.bgColor[2], round(config.bg_alpha))
    config.draw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=config.bgColor)

    # if config.bg_alpha != config.bg_alpha_base :
    #     pieceLogger(f"{config.bg_alpha}  /  {config.bg_alpha_base}")


def informalLines():
    global config

    for informalLineUnitIndex in range(0, len(config.informalLineUnits)):
        lineUnit = config.informalLineUnits[informalLineUnitIndex]
        lineUnit.lastOrthoPoint = []
        pointsToDraw = lineUnit.curvedPoints
        lastPt = [pointsToDraw[0][0], pointsToDraw[0][1]]

        lineUnit.draw.rectangle((0, 0, config.largestDim, config.largestDim), fill=(0, 0, 0, 0))

        _ptCounter = 0
        for pt in pointsToDraw:
            drawTheLine(lastPt[0], lastPt[1], pt[0], pt[1], _ptCounter, lineUnit)
            lastPt = [pt[0], pt[1]]
            _ptCounter += 1

        if (lineUnit.angle != 0 and random.random() < config.horizontalMovementProb) or (lineUnit.angle == 0 and random.random() < config.verticalMovementProb):
            if lineUnit.direction == 0:
                for _ in range(lineUnit.lineSpeed):
                    _lstpt = pointsToDraw[0][0]
                    for pt in range(0, len(pointsToDraw) - 1):
                        pointsToDraw[pt][0] = pointsToDraw[pt + 1][0]
                    pointsToDraw[pt + 1][0] = _lstpt
            else:
                for _ in range(lineUnit.lineSpeed):
                    _lstpt = pointsToDraw[len(pointsToDraw) - 1][0]
                    for pt in range(len(pointsToDraw) - 1, 0, -1):
                        pointsToDraw[pt][0] = pointsToDraw[pt - 1][0]
                    pointsToDraw[pt + 1][0] = _lstpt


def runWork():
    global config
    print(bcolors.OKGREEN + "** " + bcolors.BOLD)
    print("Running hatchingmarks.py")
    print(bcolors.ENDC)

    while config.isRunning == True:
        iterate()
        time.sleep(config.redrawSpeed)
        if config.standAlone == False:
            config.callBack()


def reDraw():
    # pieceLogger(f"{config.bg_alpha} {config.bg_alpha_base}")
    if config.bg_alpha < config.bg_alpha_base:
        config.bg_alpha += config.bg_alpha_returnrate

    if config.bg_alpha > config.bg_alpha_base:
        config.bg_alpha = config.bg_alpha_base

    drawTheBG()
    informalLines()

    # adding check on bg alpha as index of transition state - don't want another transition
    # stomping on the one in progress

    if random.random() < config.changeBGProb and config.bg_alpha == config.bg_alpha_base and not config.noChange:
        # config.bg_alpha = 0
        setBGColor()
        setLineColor()

    if random.random() < config.changeLinesProb and not config.noChange:
        # config.lightMode = False if random.random() > config.lightModeProb else True
        config.bg_alpha = 0
        setLines()

    if random.random() < config.pauseProb:
        config.noChange = True

    if random.random() < config.unpauseProb:
        config.noChange = False


def iterate():
    reDraw()

 
    if random.random() <  config.resetBlanksProb :
        badpixels.setBlanksOnScreen(config)
    

    ########### RENDERING AS A MOCKUP OR AS REAL ###########
    if config.useDrawingPoints == True:
        config.panelDrawing.canvasToUse = config.image
        config.panelDrawing.render()
    else:
        _xDiff = round((config.largestDim - config.canvasWidth) / 1)
        _yDiff = round((config.largestDim - config.canvasHeight) / 1)

        # config.draw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=(255,255,255,255))
        if config.drawingShape != "grid":
            config.draw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=config.bgColor)

            _tempImage = Image.new("RGBA", (config.largestDim, config.largestDim))
            for n in config.informalLineUnits:
                # n.draw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=(100, 0, 0, 2))
                _tempImage = ImageChops.add(n.canvas, _tempImage)

                # _temp = n.canvas.rotate(n.angle)
                # @todo fix this bs later  .....
                # if n.angle == 0:
                #     config.image.paste(_temp, (-_xDiff, -0), _temp)
                # else:
                #     config.image.paste(_temp, (-_xDiff, -_yDiff), _temp)
            _tempImage = _tempImage.rotate(n.angle)
            config.image.paste(_tempImage, (0, 0), _tempImage)
            badpixels.drawBlanks(config.image, False)
            config.render(config.image, 0, 0, config.canvasWidth, config.canvasHeight)
        else:
            badpixels.drawBlanks(config.image, False)
            config.render(config.image, 0, 0, config.canvasWidth, config.canvasHeight)

        
    # Done


def main(run=True):
    global config
    global workConfig
    config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.draw = ImageDraw.Draw(config.image)
    config.redrawSpeed = float(workConfig.get("hatchingmarks", "redrawSpeed"))
    config.drawingShape = workConfig.get("hatchingmarks", "drawingShape")

    # refinements for setting points per column and row so amplitude of noise can be adjusted to be more even if aspect ratio is more extreme - e.g narrow beam
    # but also, lower number makes the line more purely rectilinear so can give a greater focus to one directions linearity
    config.pointsPerLine = int(workConfig.get("hatchingmarks", "pointsPerLine"))
    config.pointsPerLineCol = int(workConfig.get("hatchingmarks", "pointsPerLineCol", fallback=config.pointsPerLine))
    config.pointsPerLineRow = int(workConfig.get("hatchingmarks", "pointsPerLineRow", fallback=config.pointsPerLine))

    # the +/- variability of the points
    config.noiseAmplitude = float(workConfig.get("hatchingmarks", "noiseAmplitude"))
    config.noiseAmplitudeRange = [float(x) for x in workConfig.get("hatchingmarks", "noiseAmplitudeRange", fallback="1,4").split(",")]
    config.distributionRange = float(workConfig.get("hatchingmarks", "distributionRange"))

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
        _hspacing = round(config.canvasWidth / (config.numberOfinformalLines + 2))
        _vspacing = round(config.canvasHeight / (config.numberOfinformalLines + 2))
        config.rowIntervalRange = [_vspacing, _vspacing]
        config.colIntervalRange = [_hspacing, _hspacing]

    # means the row interval is the same as the column interval - if they are independent then
    # there can be more extreme column or row spacing, othewise they get the same ratio
    config.uniformRatio = workConfig.getboolean("hatchingmarks", "uniformRatio", fallback=False)

    # forces grid to squares - but is not currently compensated to will get ragged and missing
    # grids at edges of drawing
    config.squareRatio = workConfig.getboolean("hatchingmarks", "squareRatio", fallback=False)

    config.noiseAmplitudeRangeRow = [
        float(x) for x in workConfig.get("hatchingmarks", "noiseAmplitudeRangeRow", fallback=workConfig.get("hatchingmarks", "noiseAmplitude")).split(",")
    ]
    config.noiseAmplitudeRangeCol = [
        float(x) for x in workConfig.get("hatchingmarks", "noiseAmplitudeRangeCol", fallback=workConfig.get("hatchingmarks", "noiseAmplitude")).split(",")
    ]

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
    config.vertBaseWidthRange = [int(x) for x in workConfig.get("hatchingmarks", "vertBaseWidthRange", fallback="18,180").split(",")]
    config.horizBaseWidthRange = [int(x) for x in workConfig.get("hatchingmarks", "horizBaseWidthRange", fallback="18,180").split(",")]

    config.rowAdj = int(workConfig.get("hatchingmarks", "rowAdj", fallback=0))
    config.colAdj = int(workConfig.get("hatchingmarks", "colAdj", fallback=0))

    """
    # PROBABILITIES ----------------
    # generally based on an interval rate of .03, i.e. 3/100's of a second per cycle ~ 33.33 frames/second
    # so the chance of change is .001 per frame, then the chance per second is ~ 3.33%
    config.changeLinesProb = float(workConfig.get("hatchingmarks", "changeLinesProb", fallback=0.01))
    """

    config.changeLinesProb = float(workConfig.get("hatchingmarks", "changeLinesProb", fallback=0.01))

    # probablility background changes
    config.changeBGProb = float(workConfig.get("hatchingmarks", "changeBGProb", fallback=0.001))
    config.bg_alpha_range = [int(x) for x in workConfig.get("hatchingmarks", "bg_alpha_range", fallback="10,40").split(",")]
    config.line_alpha_range = [int(x) for x in workConfig.get("hatchingmarks", "line_alpha_range", fallback="18,180").split(",")]
    config.bg_alpha_returnrate = float(workConfig.get("hatchingmarks", "bg_alpha_returnrate", fallback=2.0))

    # light lines on background - more like a drawing on a screen
    config.lightMode = workConfig.getboolean("hatchingmarks", "lightMode", fallback=False)
    config.lightModeProb = float(workConfig.get("hatchingmarks", "lightModeProb", fallback=1.0))
    config.pauseProb = float(workConfig.get("hatchingmarks", "pauseProb", fallback=0.0001))
    config.unpauseProb = float(workConfig.get("hatchingmarks", "unpauseProb", fallback=0.0001))
    config.noChange = False

    # overrides the variable background and line alpha changes and fixes at one value the rate at which the vertical and horizontal lines
    config.useSingleMode = workConfig.getboolean("hatchingmarks", "useSingleMode", fallback=True)

    config.line_minHue = float(workConfig.get("hatchingmarks", "line_minHue"))
    config.line_maxHue = float(workConfig.get("hatchingmarks", "line_maxHue"))
    config.line_maxSaturation = float(workConfig.get("hatchingmarks", "line_maxSaturation"))
    config.line_minSaturation = float(workConfig.get("hatchingmarks", "line_minSaturation"))
    config.line_minValue = float(workConfig.get("hatchingmarks", "line_minValue"))
    config.line_maxValue = float(workConfig.get("hatchingmarks", "line_maxValue"))
    config.line_alpha = int(workConfig.get("hatchingmarks", "line_alpha", fallback="180"))

    config.bg_minHue = float(workConfig.get("hatchingmarks", "bg_minHue"))
    config.bg_maxHue = float(workConfig.get("hatchingmarks", "bg_maxHue"))
    config.bg_maxSaturation = float(workConfig.get("hatchingmarks", "bg_maxSaturation"))
    config.bg_minSaturation = float(workConfig.get("hatchingmarks", "bg_minSaturation"))
    config.bg_minValue = float(workConfig.get("hatchingmarks", "bg_minValue"))
    config.bg_maxValue = float(workConfig.get("hatchingmarks", "bg_maxValue"))
    config.bg_dropHueMin = float(workConfig.get("hatchingmarks", "bg_dropHueMin", fallback="0"))
    config.bg_dropHueMax = float(workConfig.get("hatchingmarks", "bg_dropHueMax", fallback="0"))
    config.bg_alpha = int(workConfig.get("hatchingmarks", "bg_alpha", fallback="40"))
    config.bg_alpha_base = config.bg_alpha

    config.drawingWidth = int(workConfig.get("hatchingmarks", "drawingWidth", fallback=f"{config.canvasWidth}"))
    config.drawingHeight = int(workConfig.get("hatchingmarks", "drawingHeight", fallback=f"{config.canvasHeight}"))

    config.largestDim = max(config.canvasWidth, config.canvasHeight)

    config.rebuildingVerticals = False

    setLines()
    setLineColor()
    setBGColor()

    config.resetBlanksProb =  config.bg_dropHueMax = float(workConfig.get("hatchingmarks", "resetBlanksProb", fallback="0.001"))
    badpixels.numberOfDeadPixels = int(workConfig.get("hatchingmarks", "numberOfDeadPixels", fallback="1"))
    badpixels.probabilityOfBlockBlanks = .0
    badpixels.sizeTarget = [int(x) for x in workConfig.get("hatchingmarks", "sizeTarget", fallback=f"{config.canvasWidth},{config.canvasHeight}").split(",")]
    badpixels.colsRange = [int(x) for x in workConfig.get("hatchingmarks", "colsRange", fallback="32,256").split(",")]
    badpixels.rowsRange = [int(x) for x in workConfig.get("hatchingmarks", "rowsRange", fallback="32,256").split(",")]
    badpixels.setBlanksOnScreen(config)

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
    if run:
        runWork()
