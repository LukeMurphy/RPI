from logging import config
import random
import time
import math
from noise import *
from modules.configuration import ArtWorkConfig, bcolors, pieceLogger
from modules import colorutils, panelDrawing
from modules.blanks_and_dither_rempping import BlanksAndDitherRemapping
from PIL import Image, ImageDraw
from modules.holder_director import Director
from pieces.screen import Holder

# ################################################### #
# hatching hashing lines

global hashLines


class HashingMarksLines :

    # These are all overwritten but useful to have 
    # for code hinting....
    drawingWidth = 385
    drawingHeight = 320
    imageXPOS = 0
    imageXPOSSpeed = 0.0
    imageYPOS = 0
    largestDim = 385
    pointsPerLine = 28
    pointsPerLineCol = 28
    pointsPerLineRow = 28
    curveResolution = 10
    noiseSeed = 0.2754912575422065
    numberOfinformalLines = 122
    xOffset = 8
    yOffset = 8
    renderLinesAsEnvelope = True
    drawVertical = True
    drawHorizontal = True
    singleLineRegularSpacing = False
    drawingHeightRange = [18, 180]
    lineSpeedRange = [1, 20]
    baseWidthRange = [18, 180]
    backTrackRange = [1, 10]
    ratioFactorRange = [18.0, 180.0]
    verticalMovement = True
    horizontalMovement = True
    horizontalMovementProb = 0.002
    verticalMovementProb = 0.002
    singleLinesAngle = 0.0
    tangleProb = 1.0
    uniformRatio = False
    squareRatio = False
    noiseAmplitudeRangeRow = [1.1, 4.0]
    noiseAmplitudeRangeCol = [1.1, 4.0]
    colFirst = True
    vertLineChange = 0.0148
    horizLineChange = 0.0018
    vertLineChangeRange = [0.001, 0.02]
    horizLineChangeRange = [0.001, 0.002]
    vertlineSpeedRange = [1, 20]
    horzlineSpeedRange = [1, 20]
    rowIntervalRange = [20, 80]
    colIntervalRange = [20, 80]
    horizLineSpeedRange = [1, 3]
    vertLineSpeedRange = [1, 3]
    vertBaseWidthRange = [0, 0]
    horizBaseWidthRange = [0, 0]
    rowAdj = 1
    colAdj = 1
    changeLinesProb = 0.0004
    changeBGProb = 0.0003
    pauseProb = 0.0002
    unpauseProb = 0.003
    noChange = False
    useSingleMode = False
    lightMode = False
    lightModeProb = 0.0
    bg_alpha_returnrate = 0.2
    lightLinesOnGroundProb = 0.0
    lightLinesOnGround = False
    rebuildingVerticals = False
    useBgBox = False
    useBgBoxProb = 0.01
    bgBoxBox = (0, 0, 256, 256)
    bgBoxFill = (100, 0, 80, 100)
    bgTileSizeWidthMin = 64.0
    bgTileSizeWidthMax = 128.0
    bgTileSizeHeightMin = 64.0
    bgTileSizeHeightMax = 129.0
    clearbgBoxProb = 0.0003
    bgGlitchCyclesMin = 4.0
    bgGlitchCyclesMax = 30.0
    bgGlitchDisplacementHorizontal = 10.0
    bgGlitchDisplacementVertical = 10.0

    initialRunsOfBgBlocks = 30
    paletteSets = []
    activePalette = None
    informalLineUnits = []
    colInterval = 54
    rowInterval = 66
    colSpacing = 6.83
    rowSpacing = 4.606
    noiseAmplitudeCol = 2.919
    noiseAmplitudeRow = 1.557

    line_alpha = 22
    bg_alpha_base = 39
    lineColor = (14, 8, 7, 24)
    bg_alpha = 89
    bg_minHue = 355.0
    bg_maxHue = 10.0
    bg_minSaturation = 0.1
    bg_maxSaturation = 0.4
    bg_minValue = 0.9
    bg_maxValue = 0.9
    bg_dropHueMin = 0.0
    bg_dropHueMax = 0.0
    lineColorIsBgColor = False
    bgColor = (230, 183, 176, 89)
    bgBoxColorRange = [345.0, 10.0, 0.5, 1.0, 0.2, 1.0, 0.0, 0.0]

    def __init__(self):
        pass

    def debugSelf(self):
        allArgs = self.__dict__
        for element in allArgs:
            print(f"{element} = {allArgs[element]}")

        method_list = [attribute for attribute in dir(self) if callable(getattr(self, attribute)) and attribute.startswith("__") is False]
        # print(f"[RepeatedPatterns] {method_list}")


class Pen:
    def __init__(self):
        pass


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
    isColumn = 1
    name = ""

    attenuating = False
    enlarging = False

    def __init__(self, _unitNumber, _config=None):
        self.unitNumber = _unitNumber
        self.lineColor = None
        self.canvas = Image.new("RGBA", (hashLines.largestDim, hashLines.largestDim))
        self.draw = ImageDraw.Draw(self.canvas)
        self.config = _config


    def reconfigure(self):
        self.lineSpeed = random.randint(self.lineSpeedRange[0], self.lineSpeedRange[1])
        self.baseWidth = random.uniform(self.baseWidthRange[0], self.baseWidthRange[1])
        self.noiseAmplitude = random.uniform(float(self.noiseAmplitudeRange[0]), float(self.noiseAmplitudeRange[1]))


    def catmull_rom(self, p0, p1, p2, p3, t):
        t2 = t * t
        t3 = t2 * t
        return 0.5 * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3)


    def getCurvePoints(self):

        self.curvedPoints = []

        for i in range(self.points):
            p0 = self.rawPts[max(0, i - 1)]
            p1 = self.rawPts[i]
            p2 = self.rawPts[i + 1]
            p3 = self.rawPts[min(self.points - 1, i + 2)]

            for step in range(self.resolution):
                t = step / float(self.resolution)  # 0 <= t < 1

                x = self.catmull_rom(p0[0], p1[0], p2[0], p3[0], t)
                y = self.catmull_rom(p0[1], p1[1], p2[1], p3[1], t)

                self.curvedPoints.append([x, y])


    def generateRawLine(self):
        self.rawPts = []
        pointSpacing = self.drawingHeight / self.points

        for i in range(self.points):
            a = i * pointSpacing
            b = R(-self.noiseAmplitude, self.noiseAmplitude)
            if random.random() < hashLines.tangleProb and i != 0 and i != self.points - 1 and abs(b) > self.noiseAmplitude * 0.75:
                a -= random.uniform(hashLines.backTrackRange[0], hashLines.backTrackRange[1])
            self.rawPts.append((round(b + self.xOffset), round(a + self.yOffset)))

        # ensures the last point at the right or bottom closes the box
        self.rawPts.append([b + self.xOffset, self.drawingHeight + self.yOffset])
        # Extra points for smoother Bézier start/end
        # pts.insert(0, pts[0])


    def generateInformalLine(self):

        self.points = random.randint(3, self.pointPerLine)
        self.ratioFactor = random.uniform(hashLines.ratioFactorRange[0], hashLines.ratioFactorRange[1])
        self.resolution = hashLines.curveResolution
        self.direction = 1 if random.random() < 0.5 else 0

        self.generateRawLine()
        self.getCurvePoints()
        self.smoothPointsForDrawing = []
        self.smoothPointsForDrawing.extend([pt[0] + self.xOffset, pt[1] + self.yOffset] for pt in self.curvedPoints)
        # pieceLogger(f"Made line {self.xOffset}  {self.yOffset} {self.drawingHeight}")


    def makeLinePoints(self):

        self.lastOrthoPoint = []
        pointsToDraw = self.curvedPoints
        lastPt = [pointsToDraw[0][0], pointsToDraw[0][1]]

        self.draw.rectangle((0, 0, hashLines.largestDim, hashLines.largestDim), fill=(0, 0, 0, 0))

        _ptCounter = 0
        for pt in pointsToDraw:
            self.drawTheLine(lastPt[0], lastPt[1], pt[0], pt[1], _ptCounter)
            lastPt = [pt[0], pt[1]]
            _ptCounter += 1

        _ptCounter = 0
        self.smooth_points = pointsToDraw
        self._w = 1
        self.maxMarkWidth = 8
        self.minMarkWidth = 1
        self.changeMarkWidthProb = .3
        self.incrementFactor = .710
        for pt in pointsToDraw:
            self._p = _ptCounter
            # self.drawLinePolyEnvelope()
            _ptCounter += 1

        if (self.angle != 0 and random.random() < hashLines.horizontalMovementProb) or (self.angle == 0 and random.random() < hashLines.verticalMovementProb):
            if self.direction == 0:
                for _ in range(self.lineSpeed):
                    _lstpt = pointsToDraw[0][0]
                    for pt in range(0, len(pointsToDraw) - 1):
                        pointsToDraw[pt][0] = pointsToDraw[pt + 1][0]
                    pointsToDraw[pt + 1][0] = _lstpt
            else:
                for _ in range(self.lineSpeed):
                    _lstpt = pointsToDraw[len(pointsToDraw) - 1][0]
                    for pt in range(len(pointsToDraw) - 1, 0, -1):
                        pointsToDraw[pt][0] = pointsToDraw[pt - 1][0]
                    pointsToDraw[pt + 1][0] = _lstpt


    def drawTheLine(self, p1x, p1y, p2x, p2y, _n):

        _p1 = [p1x, p1y]
        _p2 = [p2x, p2y]

        _ratio = 1.0
        _ratio1a = 1.0

        _penWidth = self.baseWidth * _ratio * _ratio1a

        fillClr = self.lineColor
        if hashLines.lineColorIsBgColor:
            fillClr = hashLines.bgColor

        if self.angle == 90:
            config.draw.line([_p1[1], _p1[0], _p2[1], _p2[0]], fill=tuple(fillClr), width=round(self.baseWidth))
        else:
            config.draw.line([_p1[0], _p1[1], _p2[0], _p2[1]], fill=tuple(fillClr), width=round(self.baseWidth))


    def drawLinePolyEnvelope(self):
        # Draw the shape
        if self._p == 1:
            pieceLogger(f"Drawing Line with: {self.name}")

        if self._p < len(self.smooth_points) and self._p > 0:
            _p1 = self.smooth_points[self._p - 1]
            _p2 = self.smooth_points[self._p]
            _base = math.pi
            if self.angle == 90:
                _p1[0] = self.smooth_points[self._p - 1][1]
                _p1[1] = self.smooth_points[self._p - 1][0]
                _p2[0] = self.smooth_points[self._p][1]
                _p2[1] = self.smooth_points[self._p][0]
                _base = 0

            _dy = _p1[1] - _p2[1]
            _dx = _p1[0] - _p2[0]
            
            _orthoAngle = _base - math.atan2(_dy, _dx)

            _angle = math.atan2(_dy, _dx) * 360 / math.pi

            if _angle < 0:
                _angle += 360

            selfWidth = self._w
            _lineColor = self.lineColor

            _sinOrthoAngle = math.sin(_orthoAngle)
            _cosOrthoAngle = math.cos(_orthoAngle)

            _orthoD = selfWidth / 2.2

            _orthoP1x = round(_orthoD * _sinOrthoAngle + _p1[0])
            _orthoP1y = round(_orthoD * _cosOrthoAngle + _p1[1])

            _orthoP2x = round(_orthoD * _sinOrthoAngle + _p2[0])
            _orthoP2y = round(_orthoD * _cosOrthoAngle + _p2[1])

            _orthoP3x = round(-_orthoD * _sinOrthoAngle + _p2[0])
            _orthoP3y = round(-_orthoD * _cosOrthoAngle + _p2[1])

            _orthoP4x = round(-_orthoD * _sinOrthoAngle + _p1[0])
            _orthoP4y = round(-_orthoD * _cosOrthoAngle + _p1[1])

            try:
                if self._p > 1:

                    _orthoP1x = self.lastOrthoPoint[0]
                    _orthoP1y = self.lastOrthoPoint[1]

                    _orthoP4x = self.lastOrthoPoint[2]
                    _orthoP4y = self.lastOrthoPoint[3]

            except Exception as e:
                print(e)

            _poly = ((_orthoP1x, _orthoP1y), (_orthoP2x, _orthoP2y), (_orthoP3x, _orthoP3y), (_orthoP4x, _orthoP4y), (_orthoP1x, _orthoP1y))

            config.draw.polygon(_poly, fill=_lineColor, outline=None)

            self.lastAngle = _angle
            self._p += 1
            self.lastOrthoPoint = [_orthoP2x, _orthoP2y, _orthoP3x, _orthoP3y]

            if self._p == len(self.smooth_points):
                self._p = 0

            if random.random() < self.changeMarkWidthProb:
                if not self.attenuating and not self.enlarging:
                    if random.random() < 0.5:
                        self.attenuating = True
                    else:
                        self.enlarging = True
                elif random.random() < self.changeMarkWidthProb * 2:
                    if self.attenuating:
                        self.enlarging = True
                        self.attenuating = False
                    else:
                        self.enlarging = False
                        self.attenuating = True

            if self._w > self.maxMarkWidth:
                self.enlarging = False

            if self._w <= self.minMarkWidth:
                self.attenuating = False
                self._w = self.minMarkWidth

            if self.enlarging:
                self._w += round(1 * self.incrementFactor)
            if self.attenuating:
                self._w -= round(1 * self.incrementFactor)


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
    hashLines.bgBoxFill = (0, 0, 0, 0)
    config.underLayerDraw.rectangle(hashLines.bgBoxBox, fill=hashLines.bgBoxFill)
    hashLines.bgBoxColorRange = random.choice(hashLines.activePalette.bgBoxColorRanges)


def _bgColorsFilling():
    # config.useBgBox = False if config.useBgBox   else True
    # print("bgBox")
    # xPos = config.tileSizeWidth * math.floor(random.uniform(0, config.cols))
    # yPos = config.tileSizeHeight * math.floor(random.uniform(0, config.rows))

    xPos = math.floor(random.uniform(0, config.canvasWidth))
    yPos = math.floor(random.uniform(0, config.canvasHeight))

    hashLines.tileSizeWidth = round(random.uniform(hashLines.bgTileSizeWidthMin, hashLines.bgTileSizeWidthMax))
    hashLines.tileSizeHeight = round(random.uniform(hashLines.bgTileSizeHeightMin, hashLines.bgTileSizeHeightMax))

    hashLines.bgBoxBox = (
        xPos,
        yPos,
        xPos + hashLines.tileSizeWidth,
        yPos + hashLines.tileSizeHeight,
    )
    cR = hashLines.bgBoxColorRange
    # print(cR)
    bgBoxFill = colorutils.getRandomColorHSV(cR[0], cR[1], cR[2], cR[3], cR[4], cR[5], cR[6], cR[7])
    # print(bgBoxFill)
    hashLines.bgBoxFill = (
        round(config.brightness * bgBoxFill[0]),
        round(config.brightness * bgBoxFill[1]),
        round(config.brightness * bgBoxFill[2]),
        round(random.uniform(hashLines.activePalette.bgBoxAlphaRange[0], hashLines.activePalette.bgBoxAlphaRange[1])),
    )

    config.underLayerDraw.rectangle(hashLines.bgBoxBox, fill=hashLines.bgBoxFill)

    glitchIterations = round(random.uniform(hashLines.bgGlitchCyclesMin, hashLines.bgGlitchCyclesMax))
    for _ in range(glitchIterations):
        glitchBox(
            config.underLayer,
            config.canvasWidth,
            config.canvasHeight,
            hashLines.bgGlitchDisplacementHorizontal,
            hashLines.bgGlitchDisplacementVertical,
        )


# -------- Line Attribute Function --------- #


def setLineColor():
    if not hashLines.lightMode:
        if hashLines.lightLinesOnGround:
            return colorutils.getRandomColorHSV(
                hashLines.activePalette.line_mid_minHue,
                hashLines.activePalette.line_mid_maxHue,
                hashLines.activePalette.line_mid_minSaturation,
                hashLines.activePalette.line_mid_maxSaturation,
                hashLines.activePalette.line_mid_minValue,
                hashLines.activePalette.line_mid_maxValue,
                hashLines.activePalette.line_mid_minDropHue,
                hashLines.activePalette.line_mid_maxDropHue,
                round(random.uniform(hashLines.activePalette.line_mid_alpha_range[0], hashLines.activePalette.line_mid_alpha_range[1])),
                config.brightness,
            )
        else:
            return colorutils.getRandomColorHSV(
                hashLines.activePalette.line_minHue,
                hashLines.activePalette.line_maxHue,
                hashLines.activePalette.line_minSaturation,
                hashLines.activePalette.line_maxSaturation,
                hashLines.activePalette.line_minValue,
                hashLines.activePalette.line_maxValue,
                hashLines.activePalette.line_minDropHue,
                hashLines.activePalette.line_maxDropHue,
                round(random.uniform(hashLines.activePalette.line_alpha_range[0], hashLines.activePalette.line_alpha_range[1])),
                config.brightness,
            )
    else:
        return colorutils.getRandomColorHSV(
            hashLines.activePalette.line_light_minHue,
            hashLines.activePalette.line_light_maxHue,
            hashLines.activePalette.line_light_minSaturation,
            hashLines.activePalette.line_light_maxSaturation,
            hashLines.activePalette.line_light_minValue,
            hashLines.activePalette.line_light_maxValue,
            hashLines.activePalette.line_light_minDropHue,
            hashLines.activePalette.line_light_maxDropHue,
            round(random.uniform(hashLines.activePalette.line_light_alpha_range[0], hashLines.activePalette.line_light_alpha_range[1])),
            config.brightness,
        )

    # pieceLogger(f"New Line Color {config.lineColor}")


def setBGColor():

    hashLines.activePalette = random.choice(hashLines.paletteSets)
    pieceLogger(f"NEW palette: {hashLines.activePalette.name}")

    hashLines.bg_alpha = round(random.uniform(hashLines.activePalette.bg_alpha_range[0], hashLines.activePalette.bg_alpha_range[1]))
    hashLines.bg_minHue = hashLines.activePalette.bg_minHue
    hashLines.bg_maxHue = hashLines.activePalette.bg_maxHue
    hashLines.bg_minSaturation = hashLines.activePalette.bg_minSaturation
    hashLines.bg_maxSaturation = hashLines.activePalette.bg_maxSaturation
    hashLines.bg_minValue = hashLines.activePalette.bg_minValue
    hashLines.bg_maxValue = hashLines.activePalette.bg_maxValue
    hashLines.bg_dropHueMin = hashLines.activePalette.bg_dropHueMin
    hashLines.bg_dropHueMax = hashLines.activePalette.bg_dropHueMax

    hashLines.lineColorIsBgColor = hashLines.activePalette.lineColorIsBgColor

    _minVal = hashLines.bg_minValue
    _maxVal = hashLines.bg_maxValue
    if hashLines.lightMode:
        _minVal = 0.0
        _maxVal = 0.1
    hashLines.bgColor = colorutils.getRandomColorHSV(
        hashLines.bg_minHue,
        hashLines.bg_maxHue,
        hashLines.bg_minSaturation,
        hashLines.bg_maxSaturation,
        _minVal,
        _maxVal,
        hashLines.bg_dropHueMin,
        hashLines.bg_dropHueMax,
        hashLines.bg_alpha,
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

    if random.random() < hashLines.lightLinesOnGroundProb:
        hashLines.lightLinesOnGround = True
    else:
        hashLines.lightLinesOnGround = False

    hashLines.bgBoxColorRange = random.choice(hashLines.activePalette.bgBoxColorRanges)

    # pieceLogger("New BG")


# -------- Line Functions    -------------- #


def setLines():
    global hashLines
    pieceLogger(f"New Lines:")
    hashLines.informalLineUnits = []
    setGridLines(hashLines)


def setRegularSpacing():
    hashLines.colInterval = random.randint(int(hashLines.colIntervalRange[0]), int(hashLines.colIntervalRange[1]))

    # if uniformRatio, the column ratio is used for the rows as well - this means even rectangles across field
    if hashLines.uniformRatio:
        hashLines.rowInterval = hashLines.colInterval
    else:
        hashLines.rowInterval = random.randint(int(hashLines.rowIntervalRange[0]), int(hashLines.rowIntervalRange[1]))

    hashLines.colSpacing = (hashLines.drawingWidth - 2 * hashLines.xOffset) / hashLines.colInterval
    hashLines.rowSpacing = (hashLines.drawingHeight - 2 * hashLines.yOffset) / hashLines.rowInterval

    # if squareRatio, the column ratio and spacing is used for the rows as well - this means all squares across field
    if hashLines.squareRatio:
        hashLines.rowSpacing = hashLines.colSpacing


def setGridLines(hashLines):
    pieceLogger(f"Making Grid:  {hashLines.drawingWidth } {hashLines.drawingHeight }")

    setRegularSpacing()

    hashLines.noiseAmplitudeCol = random.uniform(float(hashLines.noiseAmplitudeRangeCol[0]), float(hashLines.noiseAmplitudeRangeCol[1]))
    hashLines.noiseAmplitudeRow = random.uniform(float(hashLines.noiseAmplitudeRangeRow[0]), float(hashLines.noiseAmplitudeRangeRow[1]))

    def add_col_lines():
        # config.v_pts = []
        for col in range(hashLines.colInterval + hashLines.colAdj):
            # v_pts = generateInformalLine(hashLines.pointsPerLineCol, hashLines.xOffset + hashLines.colSpacing * col, hashLines.yOffset, False)
            # hashLines.v_pts.append(v_pts)
            informalLine = InformalLine(col)
            informalLine.xOffset = hashLines.xOffset + hashLines.colSpacing * col
            informalLine.yOffset = hashLines.yOffset
            informalLine.drawingHeight = hashLines.drawingHeight - 2 * hashLines.yOffset

            informalLine.pointPerLine = hashLines.pointsPerLineCol
            informalLine.lineSpeedRange = hashLines.vertLineSpeedRange
            informalLine.baseWidthRange = hashLines.vertBaseWidthRange
            informalLine.noiseAmplitudeRange = hashLines.noiseAmplitudeRangeCol
            # _bg_alpha = round(hashLines.bg_alpha)

            informalLine.lineColor = setLineColor()
            informalLine.reconfigure()
            informalLine.generateInformalLine()
            informalLine.isColumn = 1
            # pieceLogger(f"{informalLine.lineColor}")
            hashLines.informalLineUnits.append(informalLine)

    def add_row_lines():
        # config.h_pts = []
        for row in range(hashLines.rowInterval + hashLines.rowAdj):
            informalLine = InformalLine(row)
            # h_pts = generateInformalLine(hashLines.pointsPerLineRow, hashLines.xOffset, hashLines.yOffset + hashLines.rowSpacing * row, True)
            # hashLines.h_pts.append(h_pts)
            informalLine.xOffset = hashLines.xOffset + hashLines.rowSpacing * row
            informalLine.yOffset = hashLines.yOffset
            informalLine.drawingHeight = hashLines.drawingWidth - 2 * hashLines.xOffset
            informalLine.angle = 90
            informalLine.pointPerLine = hashLines.pointsPerLineRow
            informalLine.lineSpeedRange = hashLines.horizLineSpeedRange
            informalLine.baseWidthRange = hashLines.horizBaseWidthRange
            informalLine.noiseAmplitudeRange = hashLines.noiseAmplitudeRangeRow
            informalLine.lineColor = setLineColor()
            informalLine.reconfigure()
            informalLine.generateInformalLine()
            informalLine.isColumn = 0
            hashLines.informalLineUnits.append(informalLine)

    if hashLines.colFirst:
        add_col_lines()
        add_row_lines()
    else:
        add_row_lines()
        add_col_lines()

    hashLines.vertLineChange = R(hashLines.vertLineChangeRange[0], hashLines.vertLineChangeRange[1])
    hashLines.horizLineChange = R(hashLines.horizLineChangeRange[0], hashLines.horizLineChangeRange[1])
    hashLines.line_alpha = R(hashLines.activePalette.line_alpha_range[0], hashLines.activePalette.line_alpha_range[1], True)
    hashLines.bg_alpha_base = R(hashLines.activePalette.bg_alpha_range[0], hashLines.activePalette.bg_alpha_range[1], True)
    hashLines.numberOfinformalLines = len(hashLines.informalLineUnits)
    # pieceLogger(f"New Lines {hashLines.numberOfinformalLines}")


def changeLine():
    _changeLine = random.randint(0, len(hashLines.informalLineUnits) - 1)
    hashLines.informalLineUnits[_changeLine].reconfigure()


def drawTheBG():
    hashLines.bgColor = (hashLines.bgColor[0], hashLines.bgColor[1], hashLines.bgColor[2], round(hashLines.bg_alpha))
    config.draw.rectangle((0, 0, hashLines.drawingWidth, hashLines.drawingHeight), fill=hashLines.bgColor)

    # if config.bg_alpha != config.bg_alpha_base :
    #     pieceLogger(f"{config.bg_alpha}  /  {config.bg_alpha_base}")


def updateLines():
    global hashLines

    for informalLineUnitIndex in range(0, len(hashLines.informalLineUnits)):
        lineUnit: InformalLine
        lineUnit = hashLines.informalLineUnits[informalLineUnitIndex]
        lineUnit.makeLinePoints()


# ---- looping and redrawing --------


def runWork():
    global config, hashLines
    print(bcolors.OKGREEN + "** " + bcolors.BOLD)
    print("Running hatchingmarks.py")
    print(bcolors.ENDC)
    # hashLines.debugSelf()

    while config.isRunning == True:
        config.directorController.checkTime()
        if config.directorController.advance:
            iterate()

        if config.standAlone == False:
            config.callBack()

        time.sleep(config.redrawSpeed)


def reDraw():
    # pieceLogger(f"{config.bg_alpha} {config.bg_alpha_base}")
    if hashLines.bg_alpha < hashLines.bg_alpha_base:
        hashLines.bg_alpha += hashLines.bg_alpha_returnrate

    if hashLines.bg_alpha > hashLines.bg_alpha_base:
        hashLines.bg_alpha = hashLines.bg_alpha_base

    drawTheBG()
    updateLines()

    # adding check on bg alpha as index of transition state - don't want another transition
    # stomping on the one in progress

    # if random.random() < config.changeBGProb and not config.noChange:
    if random.random() < hashLines.changeBGProb and hashLines.bg_alpha == hashLines.bg_alpha_base and not hashLines.noChange:
        hashLines.bg_alpha = 0
        hashLines.lightMode = False if random.random() > hashLines.lightModeProb else True
        # pieceLogger(f"change BG {hashLines.lightMode} {hashLines.bg_alpha}")
        setBGColor()
        # setLines()

        for _u in range(hashLines.numberOfinformalLines):
            informalLine = hashLines.informalLineUnits[_u]
            informalLine.lineColor = setLineColor()

            # pieceLogger(f"line {informalLine.lineColor} <= {config.lightMode}")

    if random.random() < hashLines.changeLinesProb and not hashLines.noChange:
        hashLines.lightMode = False if random.random() > hashLines.lightModeProb else True
        hashLines.bg_alpha = 0
        setBGColor()
        setLines()
        # pieceLogger(f"change LINE {config.lightMode} {config.bg_alpha}")

    if random.random() < hashLines.pauseProb:
        hashLines.noChange = True

    if random.random() < hashLines.unpauseProb:
        hashLines.noChange = False


def iterate():
    global config, overlayControls, hashLines
    if random.SystemRandom().random() < hashLines.useBgBoxProb and hashLines.useBgBox:
        _bgColorsFilling(hashLines)

    reDraw()

    if random.SystemRandom().random() < hashLines.clearbgBoxProb:
        clearbgBox()

    ########### RENDERING AS A MOCKUP OR AS REAL ###########
    if config.useDrawingPoints == True:
        config.panelDrawing.canvasToUse = config.image
        config.panelDrawing.render()

    # badpixels.drawBlanks(config.image, False)
    config.destinationImage.paste(config.image, (round(hashLines.imageXPOS), round(hashLines.imageYPOS)), config.image)
    config.destinationImage.paste(config.image, (round(hashLines.imageXPOS - hashLines.drawingWidth), round(hashLines.imageYPOS)), config.image)
    config.destinationImage.paste(config.underLayer, (0, 0), config.underLayer)
    if not hashLines.lightMode:
        hashLines.imageXPOS += hashLines.imageXPOSSpeed
    # hashLines.imageYPOS += hashLines.YPOSSpeed

    if hashLines.imageXPOS >= hashLines.drawingWidth:
        hashLines.imageXPOS = 0

    # if hashLines.imageYPOS >= hashLines.pictureHeight:
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
    hashLines.paletteSets = []
    paletteList = workConfig.get("hatchingmarks", "paletteSets").split(",")

    for p in paletteList:
        palette = Holder(hashLines)

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
        hashLines.paletteSets.append(palette)

    hashLines.activePalette = random.choice(hashLines.paletteSets)


def main(run=True):
    global config 
    global workConfig
    global overlayControls
    global hashLines

    hashLines = HashingMarksLines()
    _config : ArtWorkConfig = config
    
    # Images and Drawing are set to the main config
    _config.image = Image.new("RGBA", (_config.canvasWidth, _config.canvasHeight))
    _config.imageDraw = ImageDraw.Draw(_config.image)
    _config.draw = ImageDraw.Draw(_config.image)

    _config.canvasImage = Image.new("RGBA", (_config.canvasWidth, _config.canvasHeight))

    _config.destinationImage = Image.new("RGBA", (_config.canvasWidth, _config.canvasHeight))
    _config.destinationImageDraw = ImageDraw.Draw(_config.destinationImage)

    _config.overlayImage = Image.new("RGBA", (_config.canvasWidth, _config.canvasHeight))
    _config.overlayImageDraw = ImageDraw.Draw(_config.overlayImage)

    _config.underLayer = Image.new("RGBA", (_config.canvasWidth, _config.canvasHeight))
    _config.underLayerDraw = ImageDraw.Draw(_config.underLayer)

    hashLines.drawingWidth = int(workConfig.get("hatchingmarks", "drawingWidth", fallback=f"{_config.canvasWidth}"))
    hashLines.drawingHeight = int(workConfig.get("hatchingmarks", "drawingHeight", fallback=f"{_config.canvasHeight}"))
    hashLines.imageXPOS = 0
    hashLines.imageXPOSSpeed = float(workConfig.get("hatchingmarks", "imageXPOSSpeed", fallback=0))
    hashLines.imageYPOS = 0
    hashLines.largestDim = max(hashLines.drawingWidth, hashLines.drawingHeight)

    # refinements for setting points per column and row so amplitude of noise can be adjusted to be more even if aspect ratio is more extreme - e.g narrow beam
    # but also, lower number makes the line more purely rectilinear so can give a greater focus to one directions linearity
    hashLines.pointsPerLine = int(workConfig.get("hatchingmarks", "pointsPerLine"))
    hashLines.pointsPerLineCol = int(workConfig.get("hatchingmarks", "pointsPerLineCol", fallback=hashLines.pointsPerLine))
    hashLines.pointsPerLineRow = int(workConfig.get("hatchingmarks", "pointsPerLineRow", fallback=hashLines.pointsPerLine))

    # adjust higher for higer resolution
    hashLines.curveResolution = int(workConfig.get("hatchingmarks", "curveResolution", fallback=10))

    # not really used - was used in first iteration using Perlin Noise
    hashLines.noiseSeed = random.random()

    # if the shape is not single-lines, will be determined by rows and columns
    hashLines.numberOfinformalLines = int(workConfig.get("hatchingmarks", "numberOfinformalLines", fallback="3"))
    # the edge spacing - critical to making the drawing as the edges matter more than the sum of the lines
    hashLines.xOffset = int(workConfig.get("hatchingmarks", "xOffset"))
    hashLines.yOffset = int(workConfig.get("hatchingmarks", "yOffset"))

    # for single linesneSpeed
    hashLines.renderLinesAsEnvelope = workConfig.getboolean("hatchingmarks", "renderLinesAsEnvelope", fallback=False)
    hashLines.drawVertical = workConfig.getboolean("hatchingmarks", "drawVertical", fallback=True)
    hashLines.drawHorizontal = workConfig.getboolean("hatchingmarks", "drawHorizontal", fallback=True)
    hashLines.singleLineRegularSpacing = workConfig.getboolean("hatchingmarks", "singleLineRegularSpacing", fallback=False)
    hashLines.drawingHeightRange = [int(x) for x in workConfig.get("hatchingmarks", "drawingHeightRange", fallback="18,180").split(",")]
    hashLines.lineSpeedRange = [int(x) for x in workConfig.get("hatchingmarks", "lineSpeedRange", fallback="1,20").split(",")]
    hashLines.baseWidthRange = [int(x) for x in workConfig.get("hatchingmarks", "baseWidthRange", fallback="18,180").split(",")]
    hashLines.backTrackRange = [int(x) for x in workConfig.get("hatchingmarks", "backTrackRange", fallback="0,0").split(",")]
    hashLines.ratioFactorRange = [float(x) for x in workConfig.get("hatchingmarks", "ratioFactorRange", fallback="18,180").split(",")]
    hashLines.verticalMovement = workConfig.getboolean("hatchingmarks", "verticalMovement", fallback=False)
    hashLines.horizontalMovement = workConfig.getboolean("hatchingmarks", "horizontalMovement", fallback=False)
    hashLines.horizontalMovementProb = float(workConfig.get("hatchingmarks", "horizontalMovementProb", fallback="0.25"))
    hashLines.verticalMovementProb = float(workConfig.get("hatchingmarks", "verticalMovementProb", fallback="0.25"))
    hashLines.singleLinesAngle = float(workConfig.get("hatchingmarks", "singleLinesAngle", fallback="0"))
    hashLines.tangleProb = float(workConfig.get("hatchingmarks", "tangleProb", fallback="0"))

    if hashLines.singleLineRegularSpacing:
        _hspacing = round(hashLines.drawingWidth / (hashLines.numberOfinformalLines + 2))
        _vspacing = round(hashLines.drawingHeight / (hashLines.numberOfinformalLines + 2))
        hashLines.rowIntervalRange = [_vspacing, _vspacing]
        hashLines.colIntervalRange = [_hspacing, _hspacing]

    # means the row interval is the same as the column interval - if they are independent then
    # there can be more extreme column or row spacing, othewise they get the same ratio
    hashLines.uniformRatio = workConfig.getboolean("hatchingmarks", "uniformRatio", fallback=False)

    # forces grid to squares - but is not currently compensated to will get ragged and missing
    # grids at edges of drawing
    hashLines.squareRatio = workConfig.getboolean("hatchingmarks", "squareRatio", fallback=False)

    # the +/- variability of the points
    hashLines.noiseAmplitudeRangeRow = [float(x) for x in workConfig.get("hatchingmarks", "noiseAmplitudeRangeRow", fallback="1,1").split(",")]
    hashLines.noiseAmplitudeRangeCol = [float(x) for x in workConfig.get("hatchingmarks", "noiseAmplitudeRangeCol", fallback="1,1").split(",")]
    hashLines.colFirst = workConfig.getboolean("hatchingmarks", "colFirst", fallback=False)

    hashLines.vertLineChange = float(workConfig.get("hatchingmarks", "vertLineChange", fallback=0.01))
    hashLines.horizLineChange = float(workConfig.get("hatchingmarks", "horizLineChange", fallback=0.01))

    hashLines.vertLineChangeRange = [float(x) for x in workConfig.get("hatchingmarks", "vertLineChangeRange", fallback=".05,.6").split(",")]
    hashLines.horizLineChangeRange = [float(x) for x in workConfig.get("hatchingmarks", "horizLineChangeRange", fallback=".05,.6").split(",")]

    hashLines.vertlineSpeedRange = [int(x) for x in workConfig.get("hatchingmarks", "lineSpeedRange", fallback="1,20").split(",")]
    hashLines.horzlineSpeedRange = [int(x) for x in workConfig.get("hatchingmarks", "lineSpeedRange", fallback="1,20").split(",")]

    hashLines.rowIntervalRange = [int(x) for x in workConfig.get("hatchingmarks", "rowIntervalRange", fallback="1,1").split(",")]
    hashLines.colIntervalRange = [int(x) for x in workConfig.get("hatchingmarks", "colIntervalRange", fallback="1,1").split(",")]

    hashLines.horizLineSpeedRange = [int(x) for x in workConfig.get("hatchingmarks", "horizLineSpeedRange", fallback="1,20").split(",")]
    hashLines.vertLineSpeedRange = [int(x) for x in workConfig.get("hatchingmarks", "vertLineSpeedRange", fallback="1,20").split(",")]
    hashLines.vertBaseWidthRange = [int(x) for x in workConfig.get("hatchingmarks", "vertBaseWidthRange", fallback="18,180").split(",")]
    hashLines.horizBaseWidthRange = [int(x) for x in workConfig.get("hatchingmarks", "horizBaseWidthRange", fallback="18,180").split(",")]

    hashLines.rowAdj = int(workConfig.get("hatchingmarks", "rowAdj", fallback=0))
    hashLines.colAdj = int(workConfig.get("hatchingmarks", "colAdj", fallback=0))

    hashLines.changeLinesProb = float(workConfig.get("hatchingmarks", "changeLinesProb", fallback=0.01))
    # probablility background changes
    hashLines.changeBGProb = float(workConfig.get("hatchingmarks", "changeBGProb", fallback=0.001))
    hashLines.pauseProb = float(workConfig.get("hatchingmarks", "pauseProb", fallback=0.0001))
    hashLines.unpauseProb = float(workConfig.get("hatchingmarks", "unpauseProb", fallback=0.0001))
    hashLines.noChange = False

    # overrides the variable background and line alpha changes and fixes at one value the rate at which the vertical and horizontal lines
    hashLines.useSingleMode = workConfig.getboolean("hatchingmarks", "useSingleMode", fallback=True)

    # light lines on background - more like a drawing on a screen
    hashLines.lightMode = workConfig.getboolean("hatchingmarks", "lightMode", fallback=False)
    hashLines.lightModeProb = float(workConfig.get("hatchingmarks", "lightModeProb", fallback=1.0))
    hashLines.bg_alpha_returnrate = float(workConfig.get("hatchingmarks", "bg_alpha_returnrate", fallback=2.0))
    hashLines.lightLinesOnGroundProb = float(workConfig.get("hatchingmarks", "lightLinesOnGroundProb", fallback=0.0))
    hashLines.lightLinesOnGround = workConfig.getboolean("hatchingmarks", "lightLinesOnGround", fallback=False)

    # really there are 3 modes - black/dark lines on lighter ground, mid to light lines on lighter ground, light lines on dark ground
    hashLines.rebuildingVerticals = False

    hashLines.useBgBox = workConfig.getboolean("hatchingmarks", "forcebgBox")
    hashLines.useBgBoxProb = float(workConfig.get("hatchingmarks", "useBgBoxProb"))
    hashLines.bgBoxBox = tuple(map(lambda x: int(x), workConfig.get("hatchingmarks", "bgBoxBox").split(",")))
    _config.renderImageFullOverlay = Image.new("RGBA", (_config.canvasWidth, _config.canvasHeight))
    _config.renderDrawOver = ImageDraw.Draw(_config.renderImageFullOverlay)
    hashLines.bgBoxFill = (100, 0, 80, 100)

    hashLines.bgTileSizeWidthMin = float(workConfig.get("hatchingmarks", "bgTileSizeWidthMin"))
    hashLines.bgTileSizeWidthMax = float(workConfig.get("hatchingmarks", "bgTileSizeWidthMax"))
    hashLines.bgTileSizeHeightMin = float(workConfig.get("hatchingmarks", "bgTileSizeHeightMin"))
    hashLines.bgTileSizeHeightMax = float(workConfig.get("hatchingmarks", "bgTileSizeHeightMax"))

    hashLines.clearbgBoxProb = float(workConfig.get("hatchingmarks", "clearbgBoxProb"))
    hashLines.bgGlitchCyclesMin = float(workConfig.get("hatchingmarks", "bgGlitchCyclesMin"))
    hashLines.bgGlitchCyclesMax = float(workConfig.get("hatchingmarks", "bgGlitchCyclesMax"))
    hashLines.bgGlitchDisplacementHorizontal = float(workConfig.get("hatchingmarks", "bgGlitchDisplacementHorizontal"))
    hashLines.bgGlitchDisplacementVertical = float(workConfig.get("hatchingmarks", "bgGlitchDisplacementVertical"))

    hashLines.pauseProb = float(workConfig.get("hatchingmarks", "pauseProb", fallback=".001"))
    # hashLines.backgroundColorChangeProb = float(workConfig.get("hatchingmarks", "backgroundColorChangeProb", fallback=".001"))

    hashLines.initialRunsOfBgBlocks = int(workConfig.get("hatchingmarks", "initialRunsOfBgBlocks", fallback=0))

    loadColorConfigs()
    # loadFilterRemapping()
    # resetPolyBlanks()
    # if _config.usingPanelOverlays:
    #     setPanelOverlays()
    setLines()
    hashLines.lineColor = setLineColor()
    setBGColor()

    # badpixels.setBlanksOnScreen(_config)


    if hashLines.useBgBox:
        for _ in range(hashLines.initialRunsOfBgBlocks):
            _bgColorsFilling(hashLines)

    # these need to be set for BlanksAndDitherRemapping
    hashLines.canvasWidth = _config.canvasWidth
    hashLines.canvasHeight = _config.canvasHeight
    overlayControls = BlanksAndDitherRemapping(hashLines,  workConfig, "hatchingmarks")

    # for blanks
    overlayControls.destinationImageDraw = _config.destinationImageDraw
    overlayControls.targetImageRef = _config.destinationImage
    
    # for overlay
    overlayControls.overlayImage = _config.overlayImage
    overlayControls.overlayImageDraw = _config.overlayImageDraw
    overlayControls.setPanelOverlays()
    
    ### THIS IS USED AS WAY TO MOCKUP A CONFIGURATION OF RECTANGULAR PANELS
    panelDrawing.mockupBlock(_config, workConfig)
    #### Need to add something like this at final render call  as well
    """ 
        ########### RENDERING AS A MOCKUP OR AS REAL ###########
        if _config.useDrawingPoints == True :
            _config.panelDrawing.canvasToUse = _config.renderImageFull
            _config.panelDrawing.render()
        else :
            #_config.render(_config.canvasImage, 0, 0, _config.canvasWidth, _config.canvasHeight)
            #_config.render(_config.image, 0, 0)
            _config.render(_config.renderImageFull, 0, 0)
    """


    
    # managing speed of animation and framerate
    _config.redrawSpeed = float(workConfig.get("hatchingmarks", "redrawSpeed", fallback=0.02))
    _config.slotRate = float(workConfig.get("hatchingmarks", "slotRate", fallback=0.03))
    _config.directorController = Director(_config)
    _config.directorController.slotRate = _config.slotRate

    if run:
        runWork()
