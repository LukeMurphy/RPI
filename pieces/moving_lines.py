from logging import config
import random
import time
import noise
import math
from noise import *
from modules.configuration import bcolors, pieceLogger
from modules import colorutils, panelDrawing
from PIL import Image, ImageDraw, ImageChops, ImageEnhance

# ################################################### #
# hatching hashing lines


class FlameLine:

    points = 1
    pointPerLine = 1
    resolution = 50
    drawingHeight = 100
    noiseAmplitude = 1.0
    xOffset = 100
    yOffset = 0

    def __init__(self, unitNumber):
        self.unitNumber = unitNumber
        self.canvas = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
        self.draw = ImageDraw.Draw(self.canvas)
        self.reconfigure()


    def reconfigure(self) :
        self.flameSpeed = random.randint(config.flameSpeedRange[0],config.flameSpeedRange[1])
        self.baseWidth = random.uniform(config.baseWidthRange[0],config.baseWidthRange[1])
        self.noiseAmplitude = random.uniform(float(config.noiseAmplitudeRange[0]), float(config.noiseAmplitudeRange[1]))
        self.drawingHeight = round(random.uniform(config.drawingHeightRange[0],config.drawingHeightRange[1]))
        self.xOffset = round(config.xOffset + config.canvasWidth/2 + random.uniform(-config.distributionRange, config.distributionRange))
        self.yOffset = round(config.canvasHeight - self.drawingHeight - config.yOffset)
        self.points = random.randint(5, config.pointsPerLine)
        self.points = 14
        self.ratioFactor = random.uniform(config.ratioFactorRange[0],config.ratioFactorRange[1])
        self.resolution = config.curveResolution

        self.generateInformalLine()


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
            b = R(-self.noiseAmplitude, self.noiseAmplitude) #* i/self.points
            self.rawPts.append((round(b + self.xOffset), round(a + self.yOffset)))

        # ensures the last point at the right or bottom closes the box
        self.rawPts.append([b + self.xOffset, self.drawingHeight + self.yOffset])
        # Extra points for smoother Bézier start/end
        # pts.insert(0, pts[0])


    def generateInformalLine(self):
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
    _minVal = 0.0
    _maxVal = 0.1

    config.lineColor = colorutils.getRandomColorHSV(
        config.line_minHue,
        config.line_maxHue,
        config.line_minSaturation,
        config.line_maxSaturation,
        _minVal,
        _maxVal,
        0,
        0,
        _line_alpha,
        config.brightness,
    )
    # pieceLogger("New Line Color")


def setBGColor():
    _bg_alpha = round(config.bg_alpha)
    _minVal = 0.5
    _maxVal = 0.70
    config.lightMode = True
    if config.lightMode:
        _minVal = 0.0
        _maxVal = 0.1
    config.bgColor = colorutils.getRandomColorHSV(
        config.bg_minHue,
        config.bg_maxHue,
        config.bg_minSaturation,
        config.bg_maxSaturation,
        _minVal,
        _maxVal,
        config.bg_dropHueMin,
        config.bg_dropHueMax,
        _bg_alpha,
        config.brightness,
    )
    # pieceLogger("New BG")


# -------- Line Functions    -------------- #


def setLines():
    pieceLogger("New Lines")
    config.flameLineUnits = []
    for _u in range(config.numberOfFlameLines):
        flameLine = FlameLine(_u)
        config.flameLineUnits.append(flameLine)


def changeLine() :
    _changeLine = random.randint(0,len(config.flameLineUnits)-1)
    config.flameLineUnits[_changeLine].reconfigure()


def flameLines():
    global config

    for flameLineUnitIndex in range(0, len(config.flameLineUnits)):
        lineUnit = config.flameLineUnits[flameLineUnitIndex]
        lineUnit.lastOrthoPoint = []
        pointsToDraw = lineUnit.curvedPoints
        lastPt = [pointsToDraw[0][0], pointsToDraw[0][1]]

        lineUnit.draw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=(0,0,0,5))

        _ptCounter = 0
        for pt in pointsToDraw:
            drawTheLine(lastPt[0], lastPt[1], pt[0], pt[1], _ptCounter, lineUnit)
            lastPt = [pt[0], pt[1]]
            _ptCounter += 1

        for _ in range(lineUnit.flameSpeed):
            _lstpt = pointsToDraw[0][0]
            for pt in range(0, len(pointsToDraw) - 1):
                pointsToDraw[pt][0] = pointsToDraw[pt + 1][0]
            pointsToDraw[pt + 1][0] = _lstpt


def drawTheLine(p1x, p1y, p2x, p2y, _n, _lineUnit):

    _p1 = [p1x, p1y]
    _p2 = [p2x, p2y]

    _dy = _p1[1] - _p2[1]
    _dx = _p1[0] - _p2[0]

    _angle = math.atan2(_dy, _dx) * 360 / math.pi

    if _angle < 0:
        _angle += 360

    _totalPts = len(_lineUnit.curvedPoints) 
    _ratio1 = _n /_totalPts
    _ratio1a = _ratio1 / _lineUnit.ratioFactor
    _ratio2 = (_totalPts - _n) /_totalPts 
    _ratio2a = _ratio2 / _lineUnit.ratioFactor

    _t = (_n / math.pi ) / 70 
    _ratio = math.sin(_t + math.pi/5) * math.pow(math.sin(_t),0) * _ratio1a

    _penWidth = _lineUnit.baseWidth * _ratio * _ratio1a
    
    _alphaBase = 2

    _r  = round(190 * (_ratio * 3))
    _g = round(100 * _ratio)
    _b = round(20  * (_totalPts - _n) /_totalPts)
    _a = round(_alphaBase * _ratio)

    fillClr = [_r, _g, _b, _a]

    # _alphaBase = 100
    # _r  = round(190 * (_ratio * 3))
    # _g = round(100 * _ratio2)
    # _b = round(220  * _ratio)
    # _a = round(_alphaBase * _ratio)

    # outlineClr = [_r, _g, _b, _a]

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

    _lineUnit.draw.polygon(_poly, fill=tuple(fillClr), outline=None)
    _lineUnit.lastOrthoPoint = [_orthoP2x, _orthoP2y, _orthoP3x, _orthoP3y]
    # config.draw.polygon(_poly, fill=tuple(fillClr), outline=None)
    # config.lastOrthoPoint = [_orthoP2x, _orthoP2y, _orthoP3x, _orthoP3y]


def drawTheBG():
    config.bgColor = (config.bgColor[0], config.bgColor[1], config.bgColor[2], round(config.bg_alpha))
    config.draw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=config.bgColor)

    # if config.bg_alpha != config.bg_alpha_base :
    #     pieceLogger(f"{config.bg_alpha}  /  {config.bg_alpha_base}")


def reDraw():
    # pieceLogger(f"{config.bg_alpha} {config.bg_alpha_base}")
    if config.bg_alpha < config.bg_alpha_base:
        config.bg_alpha += config.bg_alpha_returnrate

    if config.bg_alpha > config.bg_alpha_base:
        config.bg_alpha = config.bg_alpha_base

    drawTheBG()
    flameLines()

    # adding check on bg alpha as index of transition state - don't want another transition
    # stomping on the one in progress

    if random.random() < config.changeBGProb and config.bg_alpha == config.bg_alpha_base and not config.noChange:
        # config.bg_alpha = 0
        setBGColor()
        setLineColor()

    if random.random() < config.changeLinesProb and not config.noChange:
        changeLine()

    if random.random() < config.pauseProb:
        config.noChange = True

    if random.random() < config.unpauseProb:
        config.noChange = False


def iterate():
    reDraw()

    ########### RENDERING AS A MOCKUP OR AS REAL ###########
    if config.useDrawingPoints == True:
        config.panelDrawing.canvasToUse = config.image
        config.panelDrawing.render()
    else:
        config.draw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=config.bgColor)
        for n in config.flameLineUnits:
            # n.draw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=(100, 0, 0, 2))
            config.image = ImageChops.screen(n.canvas, config.image)
            config.image.paste(n.canvas, (0,0), n.canvas)

        config.render(config.image, 0, 0, config.canvasWidth, config.canvasHeight)
    # Done


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


def main(run=True):
    global config
    global workConfig
    config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.draw = ImageDraw.Draw(config.image)
    config.redrawSpeed = float(workConfig.get("hatchingmarks", "redrawSpeed"))
    config.pointsPerLine = int(workConfig.get("hatchingmarks", "pointsPerLine"))
    config.numberOfFlameLines = int(workConfig.get("hatchingmarks", "numberOfFlameLines"))

    # the +/- variability of the points
    config.noiseAmplitude = float(workConfig.get("hatchingmarks", "noiseAmplitude"))
    config.noiseAmplitudeRange = [float(x) for x in workConfig.get("hatchingmarks", "noiseAmplitudeRange", fallback="1,4").split(",")]

    # adjust higher for higer resolution
    config.curveResolution = int(workConfig.get("hatchingmarks", "curveResolution", fallback=10))

    # not really used - was used in first iteration using Perlin Noise
    config.noiseSeed = random.random()

    # the edge spacing - critical to making the drawing as the edges matter more than the sum of the lines
    config.xOffset = int(workConfig.get("hatchingmarks", "xOffset"))
    config.yOffset = int(workConfig.get("hatchingmarks", "yOffset"))
    config.distributionRange = float(workConfig.get("hatchingmarks", "distributionRange"))

    """
    # PROBABILITIES ----------------
    """

    config.changeLinesProb = float(workConfig.get("hatchingmarks", "changeLinesProb", fallback=0.01))
    config.vertLineChange = float(workConfig.get("hatchingmarks", "vertLineChange", fallback=0.01))

    config.vertLineChangeRange = [float(x) for x in workConfig.get("hatchingmarks", "vertLineChangeRange", fallback=".05,.6").split(",")]

    # probablility background changes
    config.changeBGProb = float(workConfig.get("hatchingmarks", "changeBGProb", fallback=0.001))
    config.bg_alpha_range = [int(x) for x in workConfig.get("hatchingmarks", "bg_alpha_range", fallback="10,40").split(",")]
    config.line_alpha_range = [int(x) for x in workConfig.get("hatchingmarks", "line_alpha_range", fallback="18,180").split(",")]


    config.drawingHeightRange = [int(x) for x in workConfig.get("hatchingmarks", "drawingHeightRange", fallback="18,180").split(",")]
    config.flameSpeedRange = [int(x) for x in workConfig.get("hatchingmarks", "flameSpeedRange", fallback="1,20").split(",")]
    config.baseWidthRange = [int(x) for x in workConfig.get("hatchingmarks", "baseWidthRange", fallback="18,180").split(",")]
    config.ratioFactorRange = [float(x) for x in workConfig.get("hatchingmarks", "ratioFactorRange", fallback="18,180").split(",")]





    config.pauseProb = float(workConfig.get("hatchingmarks", "pauseProb", fallback=0.0001))
    config.unpauseProb = float(workConfig.get("hatchingmarks", "unpauseProb", fallback=0.0001))
    config.noChange = False


    config.line_minHue = float(workConfig.get("hatchingmarks", "line_minHue"))
    config.line_maxHue = float(workConfig.get("hatchingmarks", "line_maxHue"))
    config.line_maxSaturation = float(workConfig.get("hatchingmarks", "line_maxSaturation"))
    config.line_minSaturation = float(workConfig.get("hatchingmarks", "line_minSaturation"))
    config.line_maxValue = float(workConfig.get("hatchingmarks", "line_maxValue"))
    config.line_minValue = float(workConfig.get("hatchingmarks", "line_minValue"))
    config.line_alpha = int(workConfig.get("hatchingmarks", "line_alpha", fallback="180"))

    config.bg_minHue = float(workConfig.get("hatchingmarks", "bg_minHue"))
    config.bg_maxHue = float(workConfig.get("hatchingmarks", "bg_maxHue"))
    config.bg_maxSaturation = float(workConfig.get("hatchingmarks", "bg_maxSaturation"))
    config.bg_minSaturation = float(workConfig.get("hatchingmarks", "bg_minSaturation"))
    config.bg_maxValue = float(workConfig.get("hatchingmarks", "bg_maxValue"))
    config.bg_minValue = float(workConfig.get("hatchingmarks", "bg_minValue"))
    config.bg_dropHueMin = float(workConfig.get("hatchingmarks", "bg_dropHueMin", fallback="0"))
    config.bg_dropHueMax = float(workConfig.get("hatchingmarks", "bg_dropHueMax", fallback="0"))
    config.bg_alpha = int(workConfig.get("hatchingmarks", "bg_alpha", fallback="40"))
    config.bg_alpha_base = config.bg_alpha

    config.drawingWidth = int(workConfig.get("hatchingmarks", "drawingWidth", fallback=f"{config.canvasWidth}"))
    config.drawingHeight = int(workConfig.get("hatchingmarks", "drawingHeight", fallback=f"{config.canvasHeight}"))

    config.verticalMovement = workConfig.getboolean("hatchingmarks", "verticalMovement", fallback=False)
    config.verticalMovementProb = float(workConfig.get("hatchingmarks", "verticalMovementProb", fallback="0.25"))
    config.rebuildingVerticals = False

    setLines()
    setLineColor()
    setBGColor()

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
