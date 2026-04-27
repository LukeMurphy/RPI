#!/usr/bin/python
import math
import random
import time
from noise import *
from modules.configuration import bcolors, pieceLogger
from modules import badpixels, colorutils, coloroverlay, panelDrawing
from PIL import Image, ImageDraw, ImageEnhance, ImageChops
from modules.holder_director import Holder, Director

xPos = 320
yPos = 0
bads = badpixels


# ============================================================
# InformalLine class (from hashing-v2)
# ============================================================

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
        self.lineColor = None
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
                t = step / float(self.resolution)
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
        self.rawPts.append([b + self.xOffset, self.drawingHeight + self.yOffset])

    def generateInformalLine(self):
        self.points = random.randint(3, self.pointPerLine)
        self.ratioFactor = random.uniform(config.ratioFactorRange[0], config.ratioFactorRange[1])
        self.resolution = config.curveResolution
        self.direction = 1 if random.random() < 0.5 else 0
        self.generateRawLine()
        self.getCurvePoints()
        self.smoothPointsForDrawing = []
        self.smoothPointsForDrawing.extend([pt[0] + self.xOffset, pt[1] + self.yOffset] for pt in self.curvedPoints)


# ============================================================
# spriteAnimation class (from spritesheet3)
# ============================================================

class spriteAnimation:

    frameWidth = 128
    frameHeight = 128
    totalFrames = 24
    frameCols = 4
    frameRows = 5
    sliceCol = 0
    sliceRow = 0
    sliceWidth = 128
    sliceHeight = 128
    sliceXOffset = 0
    sliceYOffset = 0
    startFrame = 0
    endFrame = 24
    currentFrame = 0
    playCount = 0
    step = 1
    animSpeedMin = 2
    animSpeedMax = 4
    direction = 1
    reversing = False
    animationRotation = 0
    animationRotationRate = 0
    randomPlacement = True
    resizeAnimationToFit = False
    animationWidth = 256
    animationHeight = 256
    name = "default"
    xPos = 0
    yPos = 0
    frameArray = []
    pause = False

    def __init__(self, config):
        self.config = config
        self.imageFrame = Image.new("RGBA", (self.frameWidth, self.frameHeight))

    def prepSlices(self):
        frame = 0
        self.frameArray = []
        for r in range(self.frameRows):
            for c in range(self.frameCols):
                if frame < self.totalFrames:
                    xPos = c * self.frameWidth + self.sliceXOffset
                    yPos = r * self.frameHeight + self.sliceYOffset
                    frameSlice = self.image.crop((xPos, yPos, xPos + self.sliceWidth, yPos + self.sliceHeight))
                    if self.resizeAnimationToFit:
                        frameSlice = frameSlice.resize((self.animationWidth, self.animationHeight))
                    if self.animationRotation != 0:
                        frameSlice = frameSlice.rotate(self.animationRotation, 0, 1)
                    if self.config.brightness != 1.0:
                        enhancer = ImageEnhance.Brightness(frameSlice)
                        frameSlice = enhancer.enhance(self.config.brightness)
                    if frame == 0:
                        self.firstFrame = frameSlice.copy()
                    self.frameArray.append(frameSlice)
                    frame += 1
        pieceLogger(f"{self.name} prep done. Number of Frames:{len(self.frameArray)}")

    def getNextFrame(self):
        if self.totalFrames == 1:
            self.currentFrame = 0
        elif not self.pause:
            self.playCount += self.step
            if self.reversing:
                if self.playCount % self.animSpeed == 0:
                    self.currentFrame += self.direction
                if self.currentFrame >= self.endFrame:
                    self.direction *= -1
                    self.currentFrame = self.endFrame - 1
                if self.currentFrame < self.startFrame:
                    self.direction *= -1
                    self.currentFrame = self.startFrame
            elif self.playCount % self.animSpeed == 0:
                self.currentFrame += 1
                if self.currentFrame >= self.endFrame:
                    self.currentFrame = self.startFrame

    def nextFrameImg(self):
        return self.frameArray[self.currentFrame]


# ============================================================
# Hashing utility functions (from hashing-v2)
# ============================================================

def R(a, b, rounded=False):
    if not rounded:
        return random.uniform(a, b)
    else:
        return round(random.uniform(a, b))


def catmull_rom(p0, p1, p2, p3, t):
    t2 = t * t
    t3 = t2 * t
    return 0.5 * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3)


def setLineColor():
    if not config.lightMode:
        if config.lightLinesOnGround:
            return colorutils.getRandomColorHSV(
                config.line_mid_minHue, config.line_mid_maxHue,
                config.line_mid_minSaturation, config.line_mid_maxSaturation,
                config.line_mid_minValue, config.line_mid_maxValue,
                config.line_mid_minDropHue, config.line_mid_maxDropHue,
                round(random.uniform(config.line_mid_alpha_range[0], config.line_mid_alpha_range[1])),
                config.brightness,
            )
        else:
            return colorutils.getRandomColorHSV(
                config.line_minHue, config.line_maxHue,
                config.line_minSaturation, config.line_maxSaturation,
                config.line_minValue, config.line_maxValue,
                config.line_minDropHue, config.line_maxDropHue,
                round(random.uniform(config.line_alpha_range[0], config.line_alpha_range[1])),
                config.brightness,
            )
    else:
        return colorutils.getRandomColorHSV(
            config.line_light_minHue, config.line_light_maxHue,
            config.line_light_minSaturation, config.line_light_maxSaturation,
            config.line_light_minValue, config.line_light_maxValue,
            config.line_light_minDropHue, config.line_light_maxDropHue,
            round(random.uniform(config.line_light_alpha_range[0], config.line_light_alpha_range[1])),
            config.brightness,
        )


def setBGColor():
    _bg_alpha = round(random.uniform(config.bg_alpha_range[0], config.bg_alpha_range[1]))

    if len(config.bgSets) > 0:
        bgSet = random.choice(config.bgSets)
        config.bg_minHue = bgSet[0]
        config.bg_maxHue = bgSet[1]
        config.bg_minSaturation = bgSet[2]
        config.bg_maxSaturation = bgSet[3]
        config.bg_minValue = bgSet[4]
        config.bg_maxValue = bgSet[5]
        config.bg_dropHueMin = 0
        config.bg_dropHueMax = 0

    _minVal = config.bg_minValue
    _maxVal = config.bg_maxValue
    if config.lightMode:
        _minVal = 0.0
        _maxVal = 0.1
    config.bgColor = colorutils.getRandomColorHSV(
        config.bg_minHue, config.bg_maxHue,
        config.bg_minSaturation, config.bg_maxSaturation,
        _minVal, _maxVal,
        config.bg_dropHueMin, config.bg_dropHueMax,
        _bg_alpha,
        config.brightness,
    )

    if random.random() <= config.blankColorAsColorProb:
        badpixels.blankColor = config.bgColor
        config.blankColor = config.bgColor
    else:
        badpixels.blankColor = (0, 0, 0, 255)
        config.blankColor = (0, 0, 0, 10)

    if random.random() < config.lightLinesOnGroundProb:
        config.lightLinesOnGround = True
    else:
        config.lightLinesOnGround = False


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
            informalLine.lineColor = setLineColor()
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
    if config.uniformRatio:
        config.rowInterval = config.colInterval
    else:
        config.rowInterval = random.randint(int(config.rowIntervalRange[0]), int(config.rowIntervalRange[1]))
    config.colSpacing = (config.drawingWidth - 2 * config.xOffset) / config.colInterval
    config.rowSpacing = (config.drawingHeight - 2 * config.yOffset) / config.rowInterval
    if config.squareRatio:
        config.rowSpacing = config.colSpacing


def setGridLines():
    pieceLogger(f"Making Grid: {config.drawingShape} {config.drawingWidth} {config.drawingHeight}")
    setRegularSpacing()

    config.noiseAmplitudeCol = random.uniform(float(config.noiseAmplitudeRangeCol[0]), float(config.noiseAmplitudeRangeCol[1]))
    config.noiseAmplitudeRow = random.uniform(float(config.noiseAmplitudeRangeRow[0]), float(config.noiseAmplitudeRangeRow[1]))

    def add_col_lines():
        for col in range(config.colInterval + config.colAdj):
            informalLine = InformalLine(col)
            informalLine.xOffset = config.xOffset + config.colSpacing * col
            informalLine.yOffset = config.yOffset
            informalLine.drawingHeight = config.drawingHeight - 2 * config.yOffset
            informalLine.pointPerLine = config.pointsPerLineCol
            informalLine.lineSpeedRange = config.vertLineSpeedRange
            informalLine.baseWidthRange = config.vertBaseWidthRange
            informalLine.noiseAmplitudeRange = config.noiseAmplitudeRangeCol
            informalLine.lineColor = setLineColor()
            informalLine.reconfigure()
            informalLine.generateInformalLine()
            config.informalLineUnits.append(informalLine)

    def add_row_lines():
        for row in range(config.rowInterval + config.rowAdj):
            informalLine = InformalLine(row)
            informalLine.xOffset = config.xOffset + config.rowSpacing * row
            informalLine.yOffset = config.yOffset
            informalLine.drawingHeight = config.drawingWidth - 2 * config.xOffset
            informalLine.angle = 90
            informalLine.pointPerLine = config.pointsPerLineRow
            informalLine.lineSpeedRange = config.horizLineSpeedRange
            informalLine.baseWidthRange = config.horizBaseWidthRange
            informalLine.noiseAmplitudeRange = config.noiseAmplitudeRangeRow
            informalLine.lineColor = setLineColor()
            informalLine.reconfigure()
            informalLine.generateInformalLine()
            config.informalLineUnits.append(informalLine)

    if config.colFirst:
        add_col_lines()
        add_row_lines()
    else:
        add_row_lines()
        add_col_lines()

    config.vertLineChange = R(config.vertLineChangeRange[0], config.vertLineChangeRange[1])
    config.horizLineChange = R(config.horizLineChangeRange[0], config.horizLineChangeRange[1])
    config.line_alpha = R(config.line_alpha_range[0], config.line_alpha_range[1], True)
    config.bg_alpha_base = R(config.bg_alpha_range[0], config.bg_alpha_range[1], True)
    config.numberOfinformalLines = len(config.informalLineUnits)


def drawTheLine(p1x, p1y, p2x, p2y, _n, _lineUnit):
    _p1 = [p1x, p1y]
    _p2 = [p2x, p2y]
    _ratio = 1.0
    _ratio1a = 1.0
    _penWidth = _lineUnit.baseWidth * _ratio * _ratio1a
    fillClr = _lineUnit.lineColor

    if config.drawingShape == "grid":
        if _lineUnit.angle == 90:
            config.draw.line([_p1[1], _p1[0], _p2[1], _p2[0]], fill=tuple(fillClr), width=round(_lineUnit.baseWidth))
        else:
            config.draw.line([_p1[0], _p1[1], _p2[0], _p2[1]], fill=tuple(fillClr), width=round(_lineUnit.baseWidth))
    else:
        _dy = _p1[1] - _p2[1]
        _dx = _p1[0] - _p2[0]
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
        _lineUnit.lastOrthoPoint = [_orthoP2x, _orthoP2y, _orthoP3x, _orthoP3y]


def drawTheBG():
    config.bgColor = (config.bgColor[0], config.bgColor[1], config.bgColor[2], round(config.bg_alpha))
    config.draw.rectangle((0, 0, config.drawingWidth, config.drawingHeight), fill=config.bgColor)


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


def resetPolyBlanks():
    config.blanks_list = []
    config.blanks_numberOfDeadPixels = random.randint(1, config.blanks_maxNumberOfDeadPixels)
    for _ in range(config.blanks_numberOfDeadPixels):
        width1 = random.randint(config.blanks_colsRange[0], config.blanks_colsRange[1])
        height1 = random.randint(config.blanks_rowsRange[0], config.blanks_rowsRange[1])
        width2 = width1 + random.randint(-config.blankPolyVariation, config.blankPolyVariation)
        height2 = height1 + random.randint(-config.blankPolyVariation, config.blankPolyVariation)
        x0 = random.randint(0, config.blanks_sizeTarget[0])
        y0 = random.randint(0, config.blanks_sizeTarget[1])
        x1 = x0 + width1
        y1 = y0 + random.randint(-config.blankPolyVariation, config.blankPolyVariation)
        x2 = x1 + random.randint(-config.blankPolyVariation, config.blankPolyVariation)
        y2 = y1 + height1
        x3 = x2 - width2
        y3 = y2 + random.randint(-config.blankPolyVariation, config.blankPolyVariation)
        _poly = ((x0, y0), (x1, y1), (x2, y2), (x3, y3), (x0, y0))
        config.blanks_list.append(_poly)


def drawPolyBlanks(_drawRef):
    for p in range(config.blanks_numberOfDeadPixels):
        _poly = config.blanks_list[p]
        _drawRef.polygon(_poly, fill=config.blankColor)


def setPanelOverlays():
    global config
    panelOverLayList = []
    config.panelOverLayList = []
    config.overlayImageDraw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=(0, 0, 0, 0))
    _totalPanels = config.panelRows * config.panelColumns
    _numPanels = random.randint(config.panelOverlayRange[0], min(_totalPanels, config.panelOverlayRange[1]))
    for c in range(0, config.panelColumns):
        for r in range(0, config.panelRows):
            panelOverLayList.append([c, r])
    random.shuffle(panelOverLayList)
    for i in range(_numPanels):
        config.panelOverLayList.append(panelOverLayList[i])


def drawPanelVariations(targetImageRef):
    global config
    for p in config.panelOverLayList:
        x0 = p[0] * config.panelWidth
        y0 = p[1] * config.panelHeight
        x1 = x0 + config.panelWidth
        y1 = y0 + config.panelHeight
        config.overlayImageDraw.rectangle((x0, y0, x1, y1), fill=config.bgColor)
    tempImage = ImageChops.add(targetImageRef, config.overlayImage, round(100 * config.panelOverlayAmount))
    targetImageRef.paste(tempImage, (0, 0), tempImage)


def hash_reDraw():
    if config.bg_alpha < config.bg_alpha_base:
        config.bg_alpha += config.bg_alpha_returnrate
    if config.bg_alpha > config.bg_alpha_base:
        config.bg_alpha = config.bg_alpha_base

    drawTheBG()
    informalLines()

    if random.random() < config.changeBGProb and config.bg_alpha == config.bg_alpha_base and not config.noChange:
        config.bg_alpha = 0
        config.lightMode = False if random.random() > config.lightModeProb else True
        setBGColor()
        for _u in range(config.numberOfinformalLines):
            informalLine = config.informalLineUnits[_u]
            informalLine.lineColor = setLineColor()

    if random.random() < config.changeLinesProb and not config.noChange:
        config.lightMode = False if random.random() > config.lightModeProb else True
        config.bg_alpha = 0
        setBGColor()
        setLines()

    if random.random() < config.pauseProb:
        config.noChange = True
    if random.random() < config.unpauseProb:
        config.noChange = False


def hash_handleFilterRemapping():
    if random.random() < config.hash_filterRemappingChangeProb and (config.useFilters and config.hash_filterRemapping):
        hash_remapFilter()


def hash_expandFilterRemap():
    _pos = list(config.hash_remapImageBlockSection)
    _pos[0] = max(_pos[0] - config.hash_expandXSpeed, config.hash_newFilterStartX)
    _pos[2] += config.hash_expandXSpeed
    if _pos[0] <= (config.hash_newFilterStartX):
        config.hash_filterRemappingProb = config.hash_basefilterRemappingProb
        config.hash_remapImageBlockSection = (_pos[0], _pos[1], _pos[2], _pos[3])
        config.hash_remapImageBlockDestination = [_pos[0], _pos[1]]
        config.hash_filterRemapContracting = 1
        config.hash_filterRemappingChangeProb = config.hash_filterRemappingProb
    else:
        config.hash_remapImageBlockSection = (_pos[0], _pos[1], _pos[2], _pos[3])
        config.hash_remapImageBlockDestination = [_pos[0], _pos[1]]
        config.hash_filterRemappingChangeProb = 1.0


def hash_contractFilterRemap():
    _pos = list(config.hash_remapImageBlockSection)
    _pos[0] += config.hash_contractXSpeed
    _pos[2] -= config.hash_contractXSpeed
    _pos[1] += config.hash_contractYSpeed
    _pos[3] -= config.hash_contractYSpeed
    if _pos[0] >= _pos[2] or _pos[1] >= _pos[3]:
        config.hash_filterRemappingProb = config.hash_basefilterRemappingProb
        config.hash_filterRemapContracting = 0
        config.hash_remapImageBlockSection = (_pos[2], _pos[3], _pos[2], _pos[3])
        config.hash_remapImageBlockDestination = [_pos[0], _pos[1]]
        config.hash_filterRemappingChangeProb = config.hash_filterRemappingReappearProb
    else:
        config.hash_remapImageBlockSection = tuple(_pos)
        config.hash_remapImageBlockDestination = [_pos[0], _pos[1]]
        config.hash_filterRemappingChangeProb = 1.0


def hash_remapFilter():
    config.filterRemap = True
    if config.hash_filterRemappingProb != 1.0 and config.hash_filterRemapContracting == 0:
        config.hash_filterRemapContracting = 2
        config.hash_newFilterStartX = round(random.uniform(0, config.hash_filterRemapRangeX))
        config.hash_newFilterStartY = round(random.uniform(0, config.hash_filterRemapRangeY))
        config.hash_newFilterEndX = round(random.uniform(config.hash_filterRemapMinHoriSize, config.hash_filterRemapMaxHoriSize))
        config.hash_newFilterEndY = round(random.uniform(config.hash_filterRemapMinVertSize, config.hash_filterRemapMaxVertSize))
        config.hash_remapImageBlockSection = (
            config.hash_newFilterStartX + config.hash_newFilterEndX,
            config.hash_newFilterStartY,
            config.hash_newFilterStartX + config.hash_newFilterEndX,
            config.hash_newFilterStartY + config.hash_newFilterEndY,
        )
    if config.hash_filterRemapContracting == 1:
        hash_contractFilterRemap()
    if config.hash_filterRemapContracting == 2:
        hash_expandFilterRemap()


def loadConfigValue(obj, workConfig, section, option, default, type_converter):
    try:
        if type_converter == bool:
            setattr(obj, option, type_converter(workConfig.getboolean(section, option)))
        else:
            setattr(obj, option, type_converter(workConfig.get(section, option)))
    except Exception as e:
        pieceLogger(f" ==> Config value not loaded: {option} ==> will be set to {default} \n  {e}", 1)
        setattr(obj, option, default)


# ============================================================
# Spritesheet utility functions (from spritesheet3)
# ============================================================

def loadImage(spriteSheet):
    image = Image.open(spriteSheet, "r")
    image.load()
    return image


def glitchBox(imageRef, apparentWidth, apparentHeight, imageGlitchDisplacementHorizontal, imageGlitchDisplacementVertical):
    global config
    apparentWidth = config.canvasImage.size[0]
    apparentHeight = config.canvasImage.size[1]
    dx = round(random.uniform(-imageGlitchDisplacementHorizontal, imageGlitchDisplacementHorizontal))
    dy = round(random.uniform(-imageGlitchDisplacementVertical, imageGlitchDisplacementVertical))
    sectionWidth = round(random.uniform(2, apparentWidth - dx))
    sectionHeight = round(random.uniform(2, apparentHeight - dy))
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
    except Exception as e:
        pieceLogger(e, 1)
        pieceLogger(dx + sectionWidth, dy + sectionHeight)


def animationBackGroundFadeIn():
    currentAnimation = config.animations[config.currentAnimationIndex]
    if currentAnimation.bg_alpha <= currentAnimation.bg_alpha_max:
        currentAnimation.bg_alpha += 2


def reConfigAnimationCell(anim, aConfig):
    global config
    anim.animSpeed = round(random.uniform(anim.animSpeedMin, anim.animSpeedMax))
    anim.animationRotation = aConfig.animationRotation + random.uniform(-aConfig.animationRotationJitter, aConfig.animationRotationJitter)
    if aConfig.animationRotation != 0:
        maxDim = max(anim.frameHeight, anim.frameWidth)
        anim.imageFrame = Image.new("RGBA", (maxDim, maxDim))
    anim.image = aConfig.spriteSheet1
    if anim.randomPlacement:
        anim.xPos = round(random.SystemRandom().random() * aConfig.randomPlacemnetXRange)
        anim.yPos = round(random.SystemRandom().random() * aConfig.randomPlacemnetYRange)
    anim.sliceCol = round(random.SystemRandom().random() * anim.frameCols)
    anim.sliceRow = round(random.SystemRandom().random() * anim.frameRows)
    anim.startFrame = anim.sliceCol + anim.sliceRow * aConfig.frameCols
    anim.startFrame = 0
    anim.endFrame = anim.totalFrames
    anim.playCount = 0
    anim.currentFrame = 0
    anim.sliceXOffset = 0
    anim.sliceYOffset = 0
    anim.sliceWidth = round(random.uniform(aConfig.sliceWidthMin, aConfig.sliceWidth))
    anim.sliceHeight = round(random.uniform(aConfig.sliceHeightMin, aConfig.sliceHeight))
    if anim.sliceWidth + anim.sliceXOffset > anim.frameWidth:
        anim.sliceWidth = anim.frameWidth - anim.sliceXOffset
    if anim.sliceHeight + anim.sliceYOffset > anim.frameHeight:
        anim.sliceHeight = anim.frameHeight - anim.sliceYOffset
    anim.animationRotationRate = random.uniform(-aConfig.animationRotationRateRange, aConfig.animationRotationRateRange)


def filterRemapCall(ovrd=False):
    config.filterRemap = True
    startX = round(random.uniform(0, config.filterRemapRangeX))
    startY = round(random.uniform(0, config.filterRemapRangeY))
    endX = round(random.uniform(config.filterRemapminHoriSize, config.filterRemapmaxHoriSize))
    endY = round(random.uniform(config.filterRemapminVertSize, config.filterRemapmaxVertSize))
    if ovrd:
        startX = 0
        startY = 0
        endX = 200
        endY = 200
    config.remapImageBlockSection = [startX, startY, startX + endX, startY + endY]
    config.remapImageBlockDestination = [startX, startY]


# ============================================================
# Combined main
# ============================================================

def main(run=True):
    global config, workConfig, blocks, simulBlocks, bads

    pieceLogger("SpriteSheet + Hashing Grid Piece Loaded\n", 2, True)

    # ---- spritesheet3 init ----
    config.directorController = Director(config)
    config.delay = float(workConfig.get("base-parameters", "delay"))
    config.directorController.slotRate = float(workConfig.get("base-parameters", "slotRate"))

    config.filterRemapping = workConfig.getboolean("base-parameters", "filterRemapping")
    config.filterRemappingProb = float(workConfig.get("base-parameters", "filterRemappingProb"))

    config.filterRemapminHoriSize = int(workConfig.get("base-parameters", "filterRemapminHoriSize"))
    config.filterRemapminVertSize = int(workConfig.get("base-parameters", "filterRemapminVertSize"))

    try:
        config.filterRemapmaxHoriSize = int(workConfig.get("base-parameters", "filterRemapmaxHoriSize"))
        config.filterRemapmaxVertSize = int(workConfig.get("base-parameters", "filterRemapmaxVertSize"))
    except Exception as e:
        pieceLogger(e, 1)
        config.filterRemapmaxHoriSize = config.filterRemapminHoriSize
        config.filterRemapmaxVertSize = config.filterRemapminVertSize
        config.filterRemapminHori = 8
        config.filterRemapminVertSize = 8

    config.filterRemapRangeX = int(workConfig.get("base-parameters", "filterRemapRangeX"))
    config.filterRemapRangeY = int(workConfig.get("base-parameters", "filterRemapRangeY"))

    try:
        if config.usePixelSort:
            config.pixelSortProbOn = float(workConfig.get("base-parameters", "pixelSortProbOn"))
            config.pixelSortProbOff = float(workConfig.get("base-parameters", "pixelSortProbOff"))
        else:
            config.pixelSortProbOn = 0
            config.pixelSortProbOff = 0
    except Exception as e:
        pieceLogger(e, 1)
        config.pixelSortProbOn = 0
        config.pixelSortProbOff = 0

    config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.canvasDraw = ImageDraw.Draw(config.canvasImage)

    config.underLayer = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.underLayerDraw = ImageDraw.Draw(config.underLayer)
    config.underLayerDraw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=(100, 0, 80, 100))

    config.allPause = False

    animationNames = workConfig.get("base-parameters", "animations").split(",")
    playTimes = workConfig.get("base-parameters", "playTimes").split(",")
    config.playInOrder = workConfig.getboolean("base-parameters", "playInOrder")

    config.drawMoire = workConfig.getboolean("base-parameters", "drawMoire")
    config.drawMoireProb = float(workConfig.get("base-parameters", "drawMoireProb"))
    config.drawMoireProbOff = float(workConfig.get("base-parameters", "drawMoireProbOff"))
    config.moireXPos = int(workConfig.get("base-parameters", "moireXPos"))
    config.moireYPos = int(workConfig.get("base-parameters", "moireYPos"))
    config.moireXDistance = int(workConfig.get("base-parameters", "moireXDistance"))
    config.moireYDistance = int(workConfig.get("base-parameters", "moireYDistance"))
    config.setMoireColor = workConfig.getboolean("base-parameters", "setMoireColor")
    config.moireColorAltProb = float(workConfig.get("base-parameters", "moireColorAltProb"))
    config.moireColor = tuple(map(lambda x: int(x), workConfig.get("base-parameters", "moireColor").split(",")))
    config.moireColorAlt = tuple(map(lambda x: int(x), workConfig.get("base-parameters", "moireColorAlt").split(",")))

    config.animationNames = animationNames
    config.animations = []
    config.currentAnimationIndex = 0
    config.animationController = Director(config)

    config.bgBoxColorRange = list(map(lambda x: float(x), workConfig.get("base-parameters", "bgBoxColorRange").split(",")))
    config.bgBoxAlphaRange = tuple(map(lambda x: int(x), workConfig.get("base-parameters", "bgBoxAlphaRange").split(",")))
    config.usebgBox = workConfig.getboolean("base-parameters", "forcebgBox")
    config.usebgBoxProb = float(workConfig.get("base-parameters", "usebgBoxProb"))
    config.bgBoxBox = tuple(map(lambda x: int(x), workConfig.get("base-parameters", "bgBoxBox").split(",")))
    config.renderImageFullOverlay = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.renderDrawOver = ImageDraw.Draw(config.renderImageFullOverlay)
    config.bgBoxFill = (100, 0, 80, 100)

    config.bgTileSizeWidthMin = float(workConfig.get("base-parameters", "bgTileSizeWidthMin"))
    config.bgTileSizeWidthMax = float(workConfig.get("base-parameters", "bgTileSizeWidthMax"))
    config.bgTileSizeHeightMin = float(workConfig.get("base-parameters", "bgTileSizeHeightMin"))
    config.bgTileSizeHeightMax = float(workConfig.get("base-parameters", "bgTileSizeHeightMax"))

    config.animationFrameXOffset = int(workConfig.get("base-parameters", "animationFrameXOffset"))
    config.animationFrameYOffset = int(workConfig.get("base-parameters", "animationFrameYOffset"))

    config.clearbgBoxProb = float(workConfig.get("base-parameters", "clearbgBoxProb"))
    config.bgGlitchCyclesMin = float(workConfig.get("base-parameters", "bgGlitchCyclesMin"))
    config.bgGlitchCyclesMax = float(workConfig.get("base-parameters", "bgGlitchCyclesMax"))
    config.bgGlitchDisplacementHorizontal = float(workConfig.get("base-parameters", "bgGlitchDisplacementHorizontal"))
    config.bgGlitchDisplacementVertical = float(workConfig.get("base-parameters", "bgGlitchDisplacementVertical"))

    config.playTimes = tuple(map(lambda x: int(x), playTimes))
    config.animationController.slotRate = config.playTimes[0]

    try:
        config.preGlitchNumber = int(workConfig.get("base-parameters", "preGlitchNumber"))
        config.preGlitchNumberMin = int(workConfig.get("base-parameters", "preGlitchNumberMin"))
        config.preGlitchRedo = float(workConfig.get("base-parameters", "preGlitchRedo"))
    except Exception as e:
        pieceLogger(e, 1)
        config.preGlitchNumberMin = 1
        config.preGlitchNumber = 2
        config.preGlitchRedo = 0.5

    config.changeAnimProb = float(workConfig.get("base-parameters", "changeAnimProb", fallback=".001"))
    config.pauseProb = float(workConfig.get("base-parameters", "pauseProb", fallback=".001"))
    config.unPauseProb = float(workConfig.get("base-parameters", "unPauseProb", fallback=".001"))
    config.freezeGlitchProb = float(workConfig.get("base-parameters", "freezeGlitchProb", fallback=".001"))
    config.unFreezeGlitchProb = float(workConfig.get("base-parameters", "unFreezeGlitchProb", fallback=".001"))
    config.backgroundColorChangeProb = float(workConfig.get("base-parameters", "backgroundColorChangeProb", fallback=".001"))

    for a in config.animationNames:
        aConfig = Holder(config)
        aConfig.name = a
        aConfig.imageToLoad = workConfig.get(a, "i1")
        aConfig.animationWidth = int(workConfig.get(a, "animationWidth"))
        aConfig.animationHeight = int(workConfig.get(a, "animationHeight"))
        aConfig.resizeAnimationToFit = workConfig.getboolean(a, "resizeAnimationToFit")
        aConfig.animationRotation = float(workConfig.get(a, "animationRotation"))
        aConfig.animationImage = Image.new("RGBA", (aConfig.animationWidth, aConfig.animationHeight))
        if abs(aConfig.animationRotation) == 90:
            aConfig.animationImage = Image.new("RGBA", (aConfig.animationHeight, aConfig.animationWidth))
        aConfig.animationImageDraw = ImageDraw.Draw(aConfig.animationImage)
        aConfig.animationArray = []
        aConfig.spriteSheet1 = loadImage(config.path + aConfig.imageToLoad)
        aConfig.randomPlacement = workConfig.getboolean(a, "randomPlacement")
        aConfig.fixedPosition = workConfig.getboolean(a, "fixedPosition")
        aConfig.frameWidth = int(workConfig.get(a, "frameWidth"))
        aConfig.frameHeight = int(workConfig.get(a, "frameHeight"))
        aConfig.totalFrames = int(workConfig.get(a, "totalFrames"))
        aConfig.frameCols = int(workConfig.get(a, "frameCols"))
        aConfig.frameRows = int(workConfig.get(a, "frameRows"))
        aConfig.sliceWidth = int(workConfig.get(a, "sliceWidth"))
        aConfig.sliceHeight = int(workConfig.get(a, "sliceHeight"))
        aConfig.sliceWidthMin = int(workConfig.get(a, "sliceWidthMin"))
        aConfig.sliceHeightMin = int(workConfig.get(a, "sliceHeightMin"))
        aConfig.numberOfCells = int(workConfig.get(a, "numberOfCells"))
        aConfig.animSpeedMin = float(workConfig.get(a, "animSpeedMin"))
        aConfig.animSpeedMax = float(workConfig.get(a, "animSpeedMax"))
        aConfig.animationRotationRateRange = float(workConfig.get(a, "animationRotationRateRange"))
        aConfig.animationRotationJitter = float(workConfig.get(a, "animationRotationJitter"))
        aConfig.animationXOffset = int(workConfig.get(a, "animationXOffset"))
        aConfig.animationYOffset = int(workConfig.get(a, "animationYOffset"))
        aConfig.randomPlacemnetXRange = int(workConfig.get(a, "randomPlacemnetXRange"))
        aConfig.randomPlacemnetYRange = int(workConfig.get(a, "randomPlacemnetYRange"))
        aConfig.bg_minHue = int(workConfig.get(a, "bg_minHue"))
        aConfig.bg_maxHue = int(workConfig.get(a, "bg_maxHue"))
        aConfig.bg_minSaturation = float(workConfig.get(a, "bg_minSaturation"))
        aConfig.bg_maxSaturation = float(workConfig.get(a, "bg_maxSaturation"))
        aConfig.bg_minValue = float(workConfig.get(a, "bg_minValue"))
        aConfig.bg_maxValue = float(workConfig.get(a, "bg_maxValue"))
        aConfig.bg_dropHueMinValue = float(workConfig.get(a, "bg_dropHueMinValue"))
        aConfig.bg_dropHueMaxValue = float(workConfig.get(a, "bg_dropHueMaxValue"))
        aConfig.bg_alpha = int(workConfig.get(a, "bg_alpha"))
        aConfig.bg_alpha_max = int(workConfig.get(a, "bg_alpha"))
        aConfig.backgroundColorChangeProb = float(workConfig.get(a, "backgroundColorChangeProb", fallback=config.backgroundColorChangeProb))
        aConfig.changeAnimProb = float(workConfig.get(a, "changeAnimProb", fallback=config.changeAnimProb))
        aConfig.pauseProb = float(workConfig.get(a, "pauseProb", fallback=config.pauseProb))
        aConfig.unPauseProb = float(workConfig.get(a, "unPauseProb", fallback=config.unPauseProb))
        aConfig.freezeGlitchProb = float(workConfig.get(a, "freezeGlitchProb", fallback=config.freezeGlitchProb))
        aConfig.unFreezeGlitchProb = float(workConfig.get(a, "unFreezeGlitchProb", fallback=config.unFreezeGlitchProb))
        try:
            aConfig.pauseOnFirstFrameProb = float(workConfig.get(a, "pauseOnFirstFrameProb"))
            aConfig.pauseOnLastFrameProb = float(workConfig.get(a, "pauseOnLastFrameProb"))
        except Exception as e:
            pieceLogger(e, 1)
            aConfig.pauseOnFirstFrameProb = 0.0
            aConfig.pauseOnLastFrameProb = 0.0
        try:
            aConfig.reversing = workConfig.getboolean(a, "reversing")
        except Exception as e:
            pieceLogger(e, 1)
            aConfig.reversing = False

        aConfig.glitching = True
        aConfig.preDistorted = False
        aConfig.imageGlitchDisplacementHorizontal = int(workConfig.get(a, "imageGlitchDisplacementHorizontal"))
        aConfig.imageGlitchDisplacementVertical = int(workConfig.get(a, "imageGlitchDisplacementVertical"))

        aConfig.colOverlay = coloroverlay.ColorOverlay()
        aConfig.colOverlay.randomSteps = True
        aConfig.colOverlay.timeTrigger = True
        aConfig.colOverlay.tLimitBase = 5
        aConfig.colOverlay.steps = 10
        aConfig.colOverlay.maxBrightness = config.brightness
        aConfig.colOverlay.minSaturation = aConfig.bg_minSaturation
        aConfig.colOverlay.maxSaturation = aConfig.bg_maxSaturation
        aConfig.colOverlay.minValue = aConfig.bg_minValue
        aConfig.colOverlay.maxValue = aConfig.bg_maxValue
        aConfig.colOverlay.minHue = aConfig.bg_minHue
        aConfig.colOverlay.maxHue = aConfig.bg_maxHue
        aConfig.colOverlay.dropHueMin = aConfig.bg_dropHueMinValue
        aConfig.colOverlay.dropHueMax = aConfig.bg_dropHueMaxValue
        aConfig.colOverlay.colorTransitionSetup()

        anim = spriteAnimation(config)
        anim.frameWidth = aConfig.frameWidth
        anim.frameHeight = aConfig.frameHeight
        anim.totalFrames = aConfig.totalFrames
        anim.frameCols = aConfig.frameCols
        anim.frameRows = aConfig.frameRows
        anim.animSpeedMin = aConfig.animSpeedMin
        anim.animSpeedMax = aConfig.animSpeedMax
        anim.animationWidth = aConfig.animationWidth
        anim.animationHeight = aConfig.animationHeight
        anim.resizeAnimationToFit = aConfig.resizeAnimationToFit
        anim.randomPlacement = aConfig.randomPlacement
        anim.reversing = aConfig.reversing
        anim.currentFrame = 0
        anim.name = aConfig.name
        aConfig.imagePath = f"{config.path}/assets/imgs/"
        aConfig.imageList = [aConfig.imageToLoad]
        config.animations.append(aConfig)
        reConfigAnimationCell(anim, aConfig)
        anim.prepSlices()
        aConfig.anim = anim

    if config.brightness < 1.0:
        delta = config.ditherFilterBrightness - config.brightness
        config.ditherFilterBrightness -= delta / 4
        pieceLogger(config.ditherFilterBrightness)

    # ---- hashing-v2 init ----
    config.imageXPOS = 0
    config.imageXPOSSpeed = float(workConfig.get("hatchingmarks", "imageXPOSSpeed", fallback=0))
    config.imageYPOS = 0
    config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.imageDraw = ImageDraw.Draw(config.image)
    config.draw = ImageDraw.Draw(config.image)

    config.destinationImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.destinationImageDraw = ImageDraw.Draw(config.destinationImage)

    config.overlayImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.overlayImageDraw = ImageDraw.Draw(config.overlayImage)

    config.drawingShape = workConfig.get("hatchingmarks", "drawingShape")
    config.drawingWidth = int(workConfig.get("hatchingmarks", "drawingWidth", fallback=f"{config.canvasWidth}"))
    config.drawingHeight = int(workConfig.get("hatchingmarks", "drawingHeight", fallback=f"{config.canvasHeight}"))
    config.largestDim = max(config.drawingWidth, config.drawingHeight)

    config.pointsPerLine = int(workConfig.get("hatchingmarks", "pointsPerLine"))
    config.pointsPerLineCol = int(workConfig.get("hatchingmarks", "pointsPerLineCol", fallback=config.pointsPerLine))
    config.pointsPerLineRow = int(workConfig.get("hatchingmarks", "pointsPerLineRow", fallback=config.pointsPerLine))
    config.curveResolution = int(workConfig.get("hatchingmarks", "curveResolution", fallback=10))
    config.noiseSeed = random.random()
    config.numberOfinformalLines = int(workConfig.get("hatchingmarks", "numberOfinformalLines", fallback="3"))
    config.xOffset = int(workConfig.get("hatchingmarks", "xOffset"))
    config.yOffset = int(workConfig.get("hatchingmarks", "yOffset"))

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

    config.uniformRatio = workConfig.getboolean("hatchingmarks", "uniformRatio", fallback=False)
    config.squareRatio = workConfig.getboolean("hatchingmarks", "squareRatio", fallback=False)
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
    config.vertBaseWidthRange = [int(x) for x in workConfig.get("hatchingmarks", "vertBaseWidthRange", fallback="18,180").split(",")]
    config.horizBaseWidthRange = [int(x) for x in workConfig.get("hatchingmarks", "horizBaseWidthRange", fallback="18,180").split(",")]
    config.rowAdj = int(workConfig.get("hatchingmarks", "rowAdj", fallback=0))
    config.colAdj = int(workConfig.get("hatchingmarks", "colAdj", fallback=0))

    config.changeLinesProb = float(workConfig.get("hatchingmarks", "changeLinesProb", fallback=0.01))
    config.changeBGProb = float(workConfig.get("hatchingmarks", "changeBGProb", fallback=0.001))
    config.noChange = False

    config.useSingleMode = workConfig.getboolean("hatchingmarks", "useSingleMode", fallback=True)
    config.lightMode = workConfig.getboolean("hatchingmarks", "lightMode", fallback=False)
    config.lightModeProb = float(workConfig.get("hatchingmarks", "lightModeProb", fallback=1.0))
    config.bg_alpha_returnrate = float(workConfig.get("hatchingmarks", "bg_alpha_returnrate", fallback=2.0))
    config.lightLinesOnGroundProb = float(workConfig.get("hatchingmarks", "lightLinesOnGroundProb", fallback=0.0))
    config.lightLinesOnGround = workConfig.getboolean("hatchingmarks", "lightLinesOnGround", fallback=False)

    config.line_minHue = float(workConfig.get("hatchingmarks", "line_minHue"))
    config.line_maxHue = float(workConfig.get("hatchingmarks", "line_maxHue"))
    config.line_maxSaturation = float(workConfig.get("hatchingmarks", "line_maxSaturation"))
    config.line_minSaturation = float(workConfig.get("hatchingmarks", "line_minSaturation"))
    config.line_minValue = float(workConfig.get("hatchingmarks", "line_minValue"))
    config.line_maxValue = float(workConfig.get("hatchingmarks", "line_maxValue"))
    config.line_minDropHue = float(workConfig.get("hatchingmarks", "line_minDropHue", fallback=0))
    config.line_maxDropHue = float(workConfig.get("hatchingmarks", "line_maxDropHue", fallback=0))
    config.line_alpha_range = [int(x) for x in workConfig.get("hatchingmarks", "line_alpha_range", fallback="18,180").split(",")]

    config.line_mid_minHue = float(workConfig.get("hatchingmarks", "line_mid_minHue", fallback=config.line_minHue))
    config.line_mid_maxHue = float(workConfig.get("hatchingmarks", "line_mid_maxHue", fallback=config.line_maxHue))
    config.line_mid_minSaturation = float(workConfig.get("hatchingmarks", "line_mid_minSaturation", fallback=config.line_minSaturation))
    config.line_mid_maxSaturation = float(workConfig.get("hatchingmarks", "line_mid_maxSaturation", fallback=config.line_maxSaturation))
    config.line_mid_minValue = float(workConfig.get("hatchingmarks", "line_mid_minValue", fallback=config.line_minValue))
    config.line_mid_maxValue = float(workConfig.get("hatchingmarks", "line_mid_maxValue", fallback=config.line_maxValue))
    config.line_mid_minDropHue = float(workConfig.get("hatchingmarks", "line_mid_minDropHue", fallback=0))
    config.line_mid_maxDropHue = float(workConfig.get("hatchingmarks", "line_mid_maxDropHue", fallback=0))
    config.line_mid_alpha_range = [int(x) for x in workConfig.get("hatchingmarks", "line_mid_alpha_range", fallback="150,190").split(",")]

    config.line_light_minHue = float(workConfig.get("hatchingmarks", "line_light_minHue"))
    config.line_light_maxHue = float(workConfig.get("hatchingmarks", "line_light_maxHue"))
    config.line_light_maxSaturation = float(workConfig.get("hatchingmarks", "line_light_maxSaturation"))
    config.line_light_minSaturation = float(workConfig.get("hatchingmarks", "line_light_minSaturation"))
    config.line_light_minValue = float(workConfig.get("hatchingmarks", "line_light_minValue"))
    config.line_light_maxValue = float(workConfig.get("hatchingmarks", "line_light_maxValue"))
    config.line_light_minDropHue = float(workConfig.get("hatchingmarks", "line_light_minDropHue", fallback=0))
    config.line_light_maxDropHue = float(workConfig.get("hatchingmarks", "line_light_maxDropHue", fallback=0))
    config.line_light_alpha_range = [int(x) for x in workConfig.get("hatchingmarks", "line_light_alpha_range", fallback="150,190").split(",")]

    config.bg_minHue = float(workConfig.get("hatchingmarks", "bg_minHue"))
    config.bg_maxHue = float(workConfig.get("hatchingmarks", "bg_maxHue"))
    config.bg_maxSaturation = float(workConfig.get("hatchingmarks", "bg_maxSaturation"))
    config.bg_minSaturation = float(workConfig.get("hatchingmarks", "bg_minSaturation"))
    config.bg_minValue = float(workConfig.get("hatchingmarks", "bg_minValue"))
    config.bg_maxValue = float(workConfig.get("hatchingmarks", "bg_maxValue"))
    config.bg_dropHueMin = float(workConfig.get("hatchingmarks", "bg_dropHueMin", fallback="0"))
    config.bg_dropHueMax = float(workConfig.get("hatchingmarks", "bg_dropHueMax", fallback="0"))
    config.bg_alpha_range = [int(x) for x in workConfig.get("hatchingmarks", "bg_alpha_range", fallback="10,40").split(",")]
    config.bg_alpha = round(random.uniform(config.bg_alpha_range[0], config.bg_alpha_range[1]))
    config.bg_alpha_base = 20

    bgSets = workConfig.get("hatchingmarks", "bgSets", fallback="").split("|")
    config.bgSets = []
    if len(bgSets[0]) > 0:
        for bg in bgSets:
            config.bgSets.append(list(float(x) for x in bg.split(",")))

    config.rebuildingVerticals = False

    config.resetBlanksProb = float(workConfig.get("hatchingmarks", "resetBlanksProb", fallback="0.001"))
    config.blankColorAsColorProb = float(workConfig.get("hatchingmarks", "blankColorAsColorProb", fallback="0.5"))
    config.blanks_maxNumberOfDeadPixels = int(workConfig.get("hatchingmarks", "numberOfDeadPixels", fallback="1"))
    config.blanks_probabilityOfBlockBlanks = 0.0
    config.blanks_sizeTarget = [int(x) for x in workConfig.get("hatchingmarks", "sizeTarget", fallback=f"{config.drawingWidth},{config.drawingHeight}").split(",")]
    config.blanks_colsRange = [int(x) for x in workConfig.get("hatchingmarks", "colsRange", fallback="32,256").split(",")]
    config.blanks_rowsRange = [int(x) for x in workConfig.get("hatchingmarks", "rowsRange", fallback="32,256").split(",")]
    config.blankPolyVariation = int(workConfig.get("hatchingmarks", "blankPolyVariation", fallback="10"))

    resetPolyBlanks()

    badpixels.numberOfDeadPixels = int(workConfig.get("hatchingmarks", "numberOfDeadPixels", fallback="1"))
    badpixels.probabilityOfBlockBlanks = 0.0
    badpixels.sizeTarget = [int(x) for x in workConfig.get("hatchingmarks", "sizeTarget", fallback=f"{config.drawingWidth},{config.drawingHeight}").split(",")]
    badpixels.colsRange = [int(x) for x in workConfig.get("hatchingmarks", "colsRange", fallback="32,256").split(",")]
    badpixels.rowsRange = [int(x) for x in workConfig.get("hatchingmarks", "rowsRange", fallback="32,256").split(",")]

    config.panelWidth = int(workConfig.get("hatchingmarks", "panelWidth", fallback="64"))
    config.panelHeight = int(workConfig.get("hatchingmarks", "panelHeight", fallback="32"))
    config.panelColumns = int(workConfig.get("hatchingmarks", "panelColumns", fallback="10"))
    config.panelRows = int(workConfig.get("hatchingmarks", "panelRows", fallback="10"))
    config.panelOverlayRange = [int(x) for x in workConfig.get("hatchingmarks", "panelOverlayRange", fallback="1,30").split(",")]
    config.panelOverlayChangeProb = float(workConfig.get("hatchingmarks", "panelOverlayChangeProb", fallback=".0003"))
    config.panelOverlayAmount = float(workConfig.get("hatchingmarks", "panelOverlayAmount", fallback=".1"))
    config.usingPanelOverlays = True
    if config.panelColumns == 0 or config.panelRows == 0:
        config.usingPanelOverlays = False

    if config.usingPanelOverlays:
        setPanelOverlays()

    # hashing filter remapping (prefixed to avoid conflict with spritesheet3's filter remap)
    config.hash_filterRemapping = workConfig.getboolean("hatchingmarks", "filterRemapping", fallback=False)
    config.hash_filterRemappingProb = float(workConfig.get("hatchingmarks", "filterRemappingProb", fallback="0.0"))
    config.hash_filterRemappingReappearProb = float(workConfig.get("hatchingmarks", "filterRemappingReappearProb", fallback="0.10"))
    config.hash_filterRemapMinHoriSize = int(workConfig.get("hatchingmarks", "filterRemapMinHoriSize", fallback="1"))
    config.hash_filterRemapMaxHoriSize = int(workConfig.get("hatchingmarks", "filterRemapMaxHoriSize", fallback="1"))
    config.hash_filterRemapMinVertSize = int(workConfig.get("hatchingmarks", "filterRemapMinVertSize", fallback="1"))
    config.hash_filterRemapMaxVertSize = int(workConfig.get("hatchingmarks", "filterRemapMaxVertSize", fallback="1"))
    config.hash_filterRemapRangeY = int(workConfig.get("hatchingmarks", "filterRemapRangeY", fallback="1"))
    config.hash_filterRemapRangeX = int(workConfig.get("hatchingmarks", "filterRemapRangeX", fallback="1"))
    config.hash_contractXSpeed = int(workConfig.get("hatchingmarks", "contractXSpeed", fallback="2"))
    config.hash_contractYSpeed = int(workConfig.get("hatchingmarks", "contractYSpeed", fallback="2"))
    config.hash_expandXSpeed = int(workConfig.get("hatchingmarks", "expandXSpeed", fallback="2"))
    config.hash_expandYSpeed = int(workConfig.get("hatchingmarks", "expandYSpeed", fallback="2"))
    config.hash_filterRemappingChangeProb = config.hash_filterRemappingProb
    config.hash_filterRemapContracting = 0
    config.hash_basefilterRemappingProb = config.hash_filterRemappingProb

    setLines()
    config.lineColor = setLineColor()
    setBGColor()

    badpixels.setBlanksOnScreen(config)
    panelDrawing.mockupBlock(config, workConfig)

    if run:
        runWork()


# ============================================================
# Combined runWork / iterate
# ============================================================

def runWork():
    pieceLogger("Running spritesheet3-hashing.py", 2, True)
    while config.isRunning:
        config.directorController.checkTime()
        if config.directorController.advance:
            iterate()
            time.sleep(config.delay)
        if not config.standAlone:
            config.callBack()


def iterate(n=0):
    global config, xPos, yPos

    # ====== spritesheet3: build animation background layer ======
    currentAnimation = config.animations[config.currentAnimationIndex]
    currentAnimation.colOverlay.stepTransition()
    bgColor = currentAnimation.colOverlay.currentColor

    config.canvasImage.paste(
        currentAnimation.animationImage,
        (config.animationFrameXOffset, config.animationFrameYOffset),
        currentAnimation.animationImage,
    )
    animationBackGroundFadeIn()

    if config.allPause:
        if currentAnimation.glitching:
            glitchBox(
                currentAnimation.animationImage,
                currentAnimation.animationWidth,
                currentAnimation.animationHeight,
                currentAnimation.imageGlitchDisplacementHorizontal,
                currentAnimation.imageGlitchDisplacementVertical,
            )
            if random.SystemRandom().random() < currentAnimation.freezeGlitchProb:
                currentAnimation.glitching = False
    else:
        _moireOverLay(currentAnimation, config, bgColor)

    composite = config.canvasImage

    if random.SystemRandom().random() < config.usebgBoxProb and config.usebgBox and not config.allPause:
        _bgColorsFilling(config)

    if random.SystemRandom().random() < config.clearbgBoxProb:
        config.underLayer = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
        config.underLayerDraw = ImageDraw.Draw(config.underLayer)

    # ====== hashing-v2: build grid overlay layer ======
    hash_reDraw()
    hash_handleFilterRemapping()

    if random.random() < config.resetBlanksProb:
        resetPolyBlanks()

    if random.random() < config.panelOverlayChangeProb:
        setPanelOverlays()

    # Scroll the grid tile into destinationImage (clear first so overlay stays transparent)
    config.destinationImageDraw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=(0, 0, 0, 0))
    config.destinationImage.paste(config.image, (round(config.imageXPOS), round(config.imageYPOS)), config.image)
    config.destinationImage.paste(config.image, (round(config.imageXPOS - config.drawingWidth), round(config.imageYPOS)), config.image)

    if not config.lightMode:
        config.imageXPOS += config.imageXPOSSpeed
    if config.imageXPOS >= config.drawingWidth:
        config.imageXPOS = 0

    if config.usingPanelOverlays:
        drawPanelVariations(config.destinationImage)
    drawPolyBlanks(config.destinationImageDraw)

    # Paste grid overlay on top of the sprite animation background
    composite.paste(config.destinationImage, (0, 0), config.destinationImage)

    # ====== single render call ======
    if config.useDrawingPoints:
        config.panelDrawing.canvasToUse = config.f.blendedImage
        config.panelDrawing.render()
    else:
        config.render(composite, 0, 0, config.canvasWidth, config.canvasHeight)

    # ====== spritesheet3: probability checks and animation advancement ======
    if random.SystemRandom().random() < config.drawMoireProb:
        config.drawMoire = True
    if random.SystemRandom().random() < config.drawMoireProbOff:
        config.drawMoire = False

    if random.SystemRandom().random() < config.filterRemappingProb and (config.useFilters and config.filterRemapping):
        filterRemapCall()

    if random.SystemRandom().random() < config.pixelSortProbOn:
        config.usePixelSort = True
    if random.SystemRandom().random() < config.pixelSortProbOff:
        config.usePixelSort = False

    if config.allPause and random.SystemRandom().random() < currentAnimation.unFreezeGlitchProb:
        currentAnimation.glitching = True
    if config.allPause and random.SystemRandom().random() < currentAnimation.unPauseProb:
        config.allPause = False

    config.animationController.checkTime()
    if config.animationController.advance:
        _drawNextFrames(currentAnimation, config)


# ============================================================
# spritesheet3 internal helpers
# ============================================================

def _drawNextFrames(currentAnimation, config):
    currentAnimation.glitching = False

    if config.playInOrder:
        config.currentAnimationIndex += 1
        if config.currentAnimationIndex >= len(config.animations):
            config.currentAnimationIndex = 0
        pieceLogger("Next Animation : " + str(config.animations[config.currentAnimationIndex].name))
    else:
        choice = math.floor(random.uniform(0, len(config.animations)))
        config.currentAnimationIndex = choice
        pieceLogger("Next Animation : " + str(config.animations[choice].name))

    config.animationController.slotRate = config.playTimes[config.currentAnimationIndex]
    currentAnimation = config.animations[config.currentAnimationIndex]
    currentAnimation.preDistorted = False

    if currentAnimation.totalFrames == 1:
        if random.SystemRandom().random() < 0.5:
            currentAnimation.anim.frameArray[0] = currentAnimation.anim.firstFrame.copy()
        tempImageRef = currentAnimation.anim.nextFrameImg()
        glitchyCycles = random.SystemRandom().randrange(config.preGlitchNumberMin, config.preGlitchNumber)
        for _ in range(glitchyCycles):
            glitchBox(
                tempImageRef,
                currentAnimation.animationWidth,
                currentAnimation.animationHeight,
                currentAnimation.imageGlitchDisplacementHorizontal,
                currentAnimation.imageGlitchDisplacementVertical,
            )
        if random.SystemRandom().random() < config.preGlitchRedo:
            for _ in range(glitchyCycles):
                glitchBox(
                    tempImageRef,
                    currentAnimation.animationWidth,
                    currentAnimation.animationHeight,
                    currentAnimation.imageGlitchDisplacementHorizontal,
                    currentAnimation.imageGlitchDisplacementVertical,
                )

    currentAnimation.preDistorted = True
    currentAnimation.bg_alpha = 10
    config.allPause = False
    currentAnimation.anim.currentFrame = 0


def _bgColorsFilling(config):
    xPos = math.floor(random.uniform(0, config.canvasWidth))
    yPos = math.floor(random.uniform(0, config.canvasHeight))

    config.tileSizeWidth = round(random.uniform(config.bgTileSizeWidthMin, config.bgTileSizeWidthMax))
    config.tileSizeHeight = round(random.uniform(config.bgTileSizeHeightMin, config.bgTileSizeHeightMax))

    if random.SystemRandom().random() < config.clearbgBoxProb:
        xPos = yPos = 0
        config.bgBoxBox = (xPos, yPos, xPos + config.canvasWidth, yPos + config.canvasHeight)
        config.bgBoxFill = (0, 0, 0, 0)
    else:
        config.bgBoxBox = (xPos, yPos, xPos + config.tileSizeWidth, yPos + config.tileSizeHeight)
        cR = config.bgBoxColorRange
        bgBoxFill = colorutils.getRandomColorHSV(cR[0], cR[1], cR[2], cR[3], cR[4], cR[5], cR[6], cR[7])
        config.bgBoxFill = (
            round(config.brightness * bgBoxFill[0]),
            round(config.brightness * bgBoxFill[1]),
            round(config.brightness * bgBoxFill[2]),
            round(random.uniform(config.bgBoxAlphaRange[0], config.bgBoxAlphaRange[1])),
        )

    config.underLayerDraw.rectangle(config.bgBoxBox, fill=config.bgBoxFill)

    glitchIterations = round(random.uniform(config.bgGlitchCyclesMin, config.bgGlitchCyclesMax))
    for _ in range(glitchIterations):
        glitchBox(config.underLayer, config.canvasWidth, config.canvasHeight, config.bgGlitchDisplacementHorizontal, config.bgGlitchDisplacementVertical)


def _moireOverLay(currentAnimation, config, bgColor):
    _draw_background(currentAnimation, config, bgColor)
    _draw_moire_pattern(currentAnimation, config)
    _paste_animation_frame(currentAnimation)

    if not config.allPause:
        _animate(currentAnimation.anim, currentAnimation, config)

    currentAnimation.anim.pause = config.allPause

    if random.SystemRandom().random() < currentAnimation.changeAnimProb:
        reConfigAnimationCell(currentAnimation.anim, currentAnimation)


def _draw_background(currentAnimation, config, bgColor):
    bgColor = (
        round(config.brightness * bgColor[0]),
        round(config.brightness * bgColor[1]),
        round(config.brightness * bgColor[2]),
        currentAnimation.bg_alpha,
    )
    currentAnimation.animationImageDraw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=bgColor)

    if config.usebgBox:
        currentAnimation.animationImage.paste(config.underLayer, (0, 0), config.underLayer)


def _draw_moire_pattern(currentAnimation, config):
    if not config.drawMoire:
        return
    c1 = (round(config.brightness * 150), round(config.brightness * 50), 0, 150)
    if config.setMoireColor:
        c1 = config.moireColor
        if random.SystemRandom().random() < config.moireColorAltProb:
            c1 = config.moireColorAlt
    for ii in range(2):
        xc = ii * config.moireXDistance + config.moireXPos
        yc = ii * config.moireYDistance + config.moireYPos
        for i in range(1200):
            w = 3 * config.canvasWidth - i * 6
            if w > 1:
                x0 = xc - w / 2
                y0 = yc - w / 2
                x1 = xc + w / 2
                y1 = yc + w / 2
                x1 = max(x0 + 1, x1)
                y1 = max(y0 + 1, y1)
                currentAnimation.animationImageDraw.ellipse((x0, y0, x1, y1), fill=None, outline=c1)


def _paste_animation_frame(currentAnimation):
    anim = currentAnimation.anim
    tempImageRef = anim.nextFrameImg()
    currentAnimation.animationImage.paste(
        tempImageRef,
        (anim.xPos + currentAnimation.animationXOffset, anim.yPos + currentAnimation.animationYOffset),
        tempImageRef,
    )


def _animate(anim, currentAnimation, config):
    anim.getNextFrame()
    anim.getNextFrame()
    anim.getNextFrame()

    if random.SystemRandom().random() < currentAnimation.pauseOnFirstFrameProb and anim.currentFrame == anim.startFrame:
        anim.pause = True
        config.allPause = True

    if random.SystemRandom().random() < currentAnimation.pauseOnLastFrameProb and anim.currentFrame == anim.endFrame - 1:
        config.allPause = True
        anim.pause = True

    if (anim.pause or config.allPause) and random.SystemRandom().random() < currentAnimation.unPauseProb:
        anim.pause = False
        config.allPause = False

    if random.SystemRandom().random() < currentAnimation.pauseProb:
        anim.pause = True
        config.allPause = True
        if random.SystemRandom().random() < 0.5:
            anim.direction *= -1


def callBack():
    global config
    pieceLogger("CALLBACK")
    return True
