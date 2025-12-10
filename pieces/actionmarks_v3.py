import math
import random
import time
import configparser
import re
from tkinter import NO

from matplotlib.pylab import rand
from matplotlib.pyplot import pie
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

# from scipy.spatial import Voronoi
from scipy.interpolate import splprep, splev
from shapely import length  # For spline interpolation
from modules.holder_director import Director
from modules.configuration import pieceLogger
from modules import colorutils
from modules.rendering.render import saveImageToFile


"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
"""""" """""" """ This version uses bundles of marks and textures             """
"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""



# ----------------------------------------------------##----------------------------------------------------#
class Palette:
    def __init__(self):
        pass


class Pen:
    def __init__(self):
        pass


class Mark:
    lastAngle = 0
    angleDiffMax = 70

    def __init__(self):
        pass


class Texture:
    def __init__(self):
        pass


class TransitionStates:
    rate = 0.02
    count = 0
    countMax = 20
    inTransition = False
    chunckSize = 140

    def __init__(self, config):
        self.transitionController = Director(config)
        self.transitionController.slotRate = self.rate

    def initiateTransition(self):
        self.inTransition = True
        self.count = 0

        self.destinationImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
        self.intermediateImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))

        self.destinationImageDraw = ImageDraw.Draw(self.destinationImage)
        self.destinationImageDraw.rectangle((0, 0, 50, 50), fill=(200, 0, 0, 200))

    def transition(self):
        self.transitionController.checkTime()
        if self.transitionController.advance:
            self.stepThru()

    def stepThru(self):

        # print(self.count)
        if self.count < self.countMax:
            _x = round(random.uniform(-self.chunckSize / 2, config.canvasWidth))
            _y = round(random.uniform(-self.chunckSize / 2, config.canvasHeight))
            _part = self.sourceImage.crop((_x, _y, _x + self.chunckSize, _y + self.chunckSize))
            self.intermediateImage.paste(_part, (_x, _y), _part)
            self.count += 1
        else:
            self.inTransition = False


# ----------------------------------------------------##----------------------------------------------------#


def chaikins_corner_cutting(coords, refinements=2, ratio=0.75):
    # https://stackoverflow.com/questions/47068504/where-to-find-python-implementation-of-chaikins-corner-cutting-algorithm
    coords = np.array(coords)

    for _ in range(refinements):
        L = coords.repeat(2, axis=0)
        R = np.empty_like(L)
        R[0] = L[0]
        R[2::2] = L[1:-1:2]
        R[1:-1:2] = L[2::2]
        R[-1] = L[-1]
        coords = L * ratio + R * (1.00 - ratio)

    return coords


def catmull_rom(p0, p1, p2, p3, t):
    t2 = t * t
    t3 = t2 * t

    return 0.5 * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3)


def R(a, b, rounded=False):
    if not rounded :
        return random.uniform(a, b)
    else :
        return round(random.uniform(a, b))

# ----------------------------------------------------##----------------------------------------------------#


def filterRemapImage(config):
    config.useFilters = True
    config.remapImageBlock = False
    startX = round(random.uniform(0, config.filterRemapRangeX))
    startY = round(random.uniform(0, config.filterRemapRangeY))
    endX = round(random.uniform(config.filterRemapMinHorzSize, config.filterRemapMaxHorzSize))
    endY = round(random.uniform(config.filterRemapMinVertSize, config.filterRemapMaxVertSize))
    config.remapImageBlockSection = [startX, startY, startX + endX, startY + endY]
    config.remapImageBlockDestination = [startX, startY]


def changeDrawing(args):
    global config
    pieceLogger("CHANGE DRAWING/PAINTING", 2)
    createImageLayers()
    changePalettes()
    initDrawings()

    config.systemController = Director(config)
    _newTime = round(random.uniform(config.totalResetTime, round(float(config.totalResetTime) * config.totalResetTimeMaxMultiplier)))
    config.systemController.slotRate = _newTime

    # config.underLayerDraw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=config.bgColor)
    # config.finalCompositeLayerDraw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=config.bgColor)
    config.fadeThruToNew = 0
    initiateTransition()


def changeDrawingMode():
    config.drawingMode = round(random.uniform(1, 4))
    # config.startNewLineProb = 0.005
    config.changeTimeController.slotRate = round(random.uniform(20, 33))

    if config.drawingMode in {2, 3}:
        # config.startNewLineProb = 0.1
        config.changeTimeController.slotRate = round(random.uniform(33, 63))

    # print(f" => New Drawing Mode: {config.drawingMode}")


def changePalettes():
    config.activePalette = random.choice(config.paletteSets)
    pieceLogger(f"New Palette : {config.activePalette.name}", 4, True)
    setBGColor()
    config.canvasDraw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=(config.bgColor))
    config.canvasDraw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=(config.bgColor))
    config.underLayerDraw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=(config.bgColor))
    config.underLayerDraw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=(config.bgColor))
    primeCanvas()
    # print(f" New bg Color : {config.bgColor}")
    # print(f"brightness calculated = {colorutils.brightness(config.bgColor[0],config.bgColor[1],config.bgColor[2])}")
    config.changeColorSetTimeToUse = round(random.uniform(config.changeColorSetTime, round(config.changeColorSetTime * config.changeColorSetTimeMaxMultiplier)))
    config.paletteController.slotRate = config.changeColorSetTimeToUse
    config.slownessFactor = config.activePalette.slownessFactor

    config.bgBoxRange = config.activePalette.bgBoxRange
    config.drawLineAsEnvelope = config.activePalette.drawLineAsEnvelope
    config.doJitterProb = config.activePalette.doJitterProb

    pieceLogger(f"config.drawLineAsEnvelope {config.drawLineAsEnvelope} <== {config.activePalette.drawLineAsEnvelope}")
    pieceLogger(f"config.doJitterProb {config.doJitterProb} ")


def initiateTransition():
    # print("\n ITNITATE TRANSITION")
    config.transitionStateHandler.sourceImage = config.finalCompositeLayer
    config.transitionStateHandler.initiateTransition()


# ------------------------------------------- PEN ACTIONS ---------------------------------------------------#


def startNewLine(_pen):
    # pieceLogger(f"=========>   startNewLine _pen ==> {_pen.name} {config.activePalette.pens}")
    setPenProperties(_pen)
    setPenColor(_pen)
    _img = generateSmoothLinePoints(_pen)
    _pen._p = 1
    config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.draw = ImageDraw.Draw(config.image)


def setPenProperties(pen):
    # print(f"setting {pen} {pen.name}")
    setPenPropsByName(pen.name, pen)
    setPenColor(pen)


def setPenPropsByName(_name, pen):

    # TODO Add some specific pen based rules for shapes based on where
    # the center may end up and how much we want the pen to exit the edges
    # or stay close to the edge - i.e. like Jerry, close to the edge but
    # not over the edge
    _penProps = None

    for _p in config.marksPalette:
        _penProps = _p
        if _p.name == _name:
            _penProps = _p
            break
    pen.name = _name

    '''
    Added Scribble like marks - the marks that are a sign or signifier for mark
    making - marks as constrution of the image plane that recall the hand as
    much as stand in for the hand - since painting has become algorithmic of
    its own accord - maybe so much exposure to all the art ever made means 
    the act of marking is more an act of choice of type of mark
    '''
    if "scribble" in pen.name :
        # pen.points = R(_penProps.minNumPoints, _penProps.maxNumPoints, True)
        pen.loopsMin = _penProps.loopsMin
        pen.loopsMax = _penProps.loopsMax

        pen.noiseX = _penProps.noiseX
        pen.noiseY = _penProps.noiseY

        # // line sizing
        pen.height = _penProps.height
        pen.radiusX = _penProps.radiusX
        pen.radiusY = _penProps.radiusY
        pen.radiusXMin = _penProps.radiusXMin
        pen.radiusXMax = _penProps.radiusXMax
        pen.radiusYMin = _penProps.radiusYMin
        pen.radiusYMax = _penProps.radiusYMax
        pen.xRadiusDelta = _penProps.xRadiusDelta
        pen.yRadiusDelta = _penProps.yRadiusDelta
        pen.deltaRadiusXChangeProb = _penProps.deltaRadiusXChangeProb
        pen.deltaRadiusYChangeProb = _penProps.deltaRadiusYChangeProb

        # // line placement and centering
        pen.centerXDelta = _penProps.centerXDelta
        pen.centerYDelta = _penProps.centerYDelta
        pen.deltaRadiusXCenterChangeProb = _penProps.deltaRadiusXCenterChangeProb
        pen.deltaRadiusYCenterChangeProb = _penProps.deltaRadiusYCenterChangeProb
        pen.loops = R(pen.loopsMin, pen.loopsMax, True)
        pen.points = round(pen.loops * _penProps.pointsPerLoop)

        """"
        # putting pen speed variables in the palette config rather than in the 
        # pen configuration
        """
        pen.penSpeedMinVal = config.activePalette.penSpeedMinVal
        pen.penSpeedMaxVal = config.activePalette.penSpeedMaxVal

        pen.speed = round(random.uniform(_penProps.penSpeedMinVal, _penProps.penSpeedMaxVal))

        pen.loopDirection = -1
        if random.random() < .5  :
            pen.loopDirection = 1
    else :   
        pen.minNumPoints = _penProps.minNumPoints
        pen.maxNumPoints = _penProps.maxNumPoints
        pen.num_points = round(random.uniform(pen.minNumPoints, pen.maxNumPoints))     
        pen.turns = round(random.uniform(_penProps.turnsRange[0], _penProps.turnsRange[1]))
        pen.minInterpolatedPoints = _penProps.minInterpolatedPoints
        pen.maxInterpolatedPoints = _penProps.maxInterpolatedPoints

        pen.baseRadiusFactor = random.uniform(_penProps.baseRadiusFactorRange[0], _penProps.baseRadiusFactorRange[1])
        pen.yRadiusFactor = random.uniform(_penProps.yRadiusFactorRange[0], _penProps.yRadiusFactorRange[1])
        pen.xRadiusFactor = random.uniform(_penProps.xRadiusFactorRange[0], _penProps.xRadiusFactorRange[1])

        pen.xRadiusFactorNoiseFactor = _penProps.xRadiusFactorNoiseFactor
        pen.yRadiusFactorNoiseFactor = _penProps.yRadiusFactorNoiseFactor
        pen.yRandom = round(random.uniform(_penProps.yRandomRange[0], _penProps.yRandomRange[1]))
        pen.xRandom = round(random.uniform(_penProps.xRandomRange[0], _penProps.xRandomRange[1]))

        pen.rotationFactor = _penProps.rotationFactor
        pen.rotationAngle = random.uniform(-math.pi / 2 / pen.rotationFactor, math.pi / 2 / pen.rotationFactor)

        pen.changePenColorWhileDrawingProb = config.activePalette.changePenColorWhileDrawingProb

        pen.xTravelRange = _penProps.xTravelRange
        pen.yTravelRange = _penProps.yTravelRange
        pen.xTravelIncr = _penProps.xTravelIncrRange
        pen.yTravelIncr = _penProps.yTravelIncrRange
        pen.xtravelMode = 1 if random.random() < _penProps.xtravelProb else 0
        pen.ytravelMode = 1 if random.random() < _penProps.ytravelProb else 0

        pen.radiusChangePerRound = _penProps.radiusChangePerRound
        pen.linePpoints = _penProps.linePoints
        pen.lopOff = _penProps.lopOff

        _penSpeedMax = max(1, math.ceil(5 / config.slownessFactor + 1))
        pen.speed = round(random.uniform(1, _penSpeedMax))
    # print(f"pen.speed {pen.speed} / {_penSpeedMax}")

    pen.drawingSize = [config.canvasWidth, config.canvasHeight]
    if pen.xOffsetRange is not None:
        pen.xOffset = round(random.uniform(pen.xOffsetRange[0], pen.xOffsetRange[1]))
    else:
        pen.xOffset = round(random.uniform(config.activePalette.xOffsetRange[0], config.activePalette.xOffsetRange[1]))

    if pen.yOffsetRange is not None:
        pen.yOffset = round(random.uniform(pen.yOffsetRange[0], pen.yOffsetRange[1]))
    else:
        pen.yOffset = round(random.uniform(config.activePalette.yOffsetRange[0], config.activePalette.yOffsetRange[1]))

    pen._w = _penProps.w
    pen.minMarkWidth = _penProps.minMarkWidth
    pen.maxMarkWidth = _penProps.maxMarkWidth
    pen.changeMarkWidthProb = _penProps.changeMarkWidthProb
    pen.mode = _penProps.mode
    pen.incrementFactor = _penProps.incrementFactor

    if pen.incrementFactor == 0:
        pen._w = round(random.uniform(_penProps.minMarkWidth, _penProps.maxMarkWidth))
    # pen.drawingSize = [180, 180]
    pen.lastPoint = [config.canvasWidth / 2, config.canvasHeight / 2]
    # pen.centerVariationX = random.randint(config.pen_centerVariationXMin, config.pen_centerVariationXMin)
    # pen.centerVariationY = random.randint(config.pen_centerVariationYMin, config.pen_centerVariationYMax)

    # genral size of drawing
    pen.drawingSkipProb = random.uniform(0.0, _penProps.drawingSkip)

    pen._p = 0
    pen.smooth_points = []

    pen.attenuating = False
    pen.enlarging = False
    pen.forceOrientation = _penProps.forceOrientation
    pen.angleDiffMax = _penProps.angleDiffMax

    # if _penProps.drawLineAsEnvelope is not None :
    # pen.drawLineAsEnvelope = _penProps.drawLineAsEnvelope
    # else :
    pen.drawLineAsEnvelope = config.activePalette.drawLineAsEnvelope

    pieceLogger(f"\n===> setting pen props pen.name {pen.name} config.drawLineAsEnvelope = {pen.drawLineAsEnvelope} <== {config.drawLineAsEnvelope}")
    # pieceLogger(f"pen.drawingSkip {pen.drawingSkip}")
    # pieceLogger("--")


def setPenColor(_pen):

    cR = random.choice(config.activePalette.penColorSets)
    # cR = config.activePalette.penColor

    # pieceLogger(f"{config.activePalette.noPenGrays}")

    _penAlpha = round(random.uniform(config.activePalette.penAlphaRange[0], config.activePalette.penAlphaRange[1]))

    if _pen.forcedPalette is None:
        _pen.lineColor = colorutils.getRandomColorHSV(cR[0], cR[1], cR[2], cR[3], cR[4], cR[5], cR[6], cR[7], _penAlpha, config.brightness)
    else:
        _pen.lineColor = colorutils.getRandomColorHSV(
            _pen.forcedPalette[0],
            _pen.forcedPalette[1],
            _pen.forcedPalette[2],
            _pen.forcedPalette[3],
            _pen.forcedPalette[4],
            _pen.forcedPalette[5],
            _pen.forcedPalette[6],
            _pen.forcedPalette[7],
            _penAlpha,
            config.brightness,
        )


def choosePenMark():
    _penName = random.choice(config.activePalette.pens)
    # print(f"\nLooking for this pen mark: {_penName}\n")
    for _pen in config.marksPalette:
        # print(f"{_pen.name} {config.activePalette.pens}")
        if _pen.name == _penName:
            # print(f"we chose {_pen.name}")
            return _pen


def generateSmoothLinePoints(_pen):

    if "lineMarks" in _pen.name:
        # clearCurrentDrawing()
        generateLine(_pen)
    elif "scribble" in _pen.name:
        generateScribble(_pen)
    else :
        generateCurve(_pen)
    # pieceLogger("Line properties:")
    # for _pnt in range(len(_pen.smooth_points)-2) :
    #     _dy = _pen.smooth_points[_pnt + 1][1] - _pen.smooth_points[_pnt][1]
    #     _dx = _pen.smooth_points[_pnt + 1][0] - _pen.smooth_points[_pnt][0]
    #     _ang = abs(math.atan(_dy/_dx) * 360/math.pi)
    #     pieceLogger(_ang)


def generateLine(_pen):

    points = []
    _rangex = _pen.yRandomRange[0]
    _rangey = _pen.yRandomRange[1]

    _yD = _pen.maxNumPoints
    _pts = round(config.canvasHeight / _yD) + 2

    _pen.smooth_points = []

    pieceLogger(f"=========>  Creating line  {_pen.name} ( {_pen.xOffset} , {_pen.yOffset}) pts {_pts} {_yD}")
    for i in range(_pts):
        if _pen.forceOrientation == "horizontal":
            _y = _rangex - (_rangex * 2 * random.random())
            _x = _yD * i
        else:
            _x = _rangex - (_rangex * 2 * random.random())
            _y = _yD * i + random.uniform(-_rangey, _rangey)
        points.append([_x, _y])
    # for i in range(_pts):
    #     if _pen.forceOrientation == "horizontal":
    #         _y  =  (_rangex - (_rangex * 2 * random.random()))
    #         _x  = _yD * i
    #     else:
    #         _x  =  (_rangex - (_rangex * 2 * random.random()))
    #         _y  = _yD * i + random.uniform(-_rangey,_rangey)
    #     points.append([_x,_y])
    # _pen.smooth_points.append((_x +_pen.xOffset,_y + _pen.yOffset))
    # smoothLine(points, _pen)
    _pen.smooth_points = []
    ratio = random.uniform(0.6, 0.8)
    res = chaikins_corner_cutting(points, 2, ratio).tolist()

    # for lines, really need to handle the yOffset more carefully
    # This has GOT to be a parameter ......
    if _pen.name in ["lineMarksVert", "lineMarksVertTest", "lineMarksVertNarrow"]:
        _pen.yOffset = 0

    _pen.smooth_points.extend((pt[0] + _pen.xOffset, pt[1] + _pen.yOffset) for pt in res)
    # either clockwise or counter
    # if random.random() < 0.5:
    #     _pen.smooth_points.reverse()


def generateScribble(_pen):
    points = generate_loop_stroke(_pen)
    _res = get_curve_points(points, True, 10)

    # _pen.xOffset = 200
    # _pen.yOffset = 200
    _pen.smooth_points = []
    _pen.smooth_points.extend((pt[0] + _pen.xOffset, pt[1] + _pen.yOffset) for pt in _res)

    if random.random() < 0.5:
        _pen.smooth_points.reverse()


def generateCurve(_pen):
    width = _pen.drawingSize[0]
    height = _pen.drawingSize[1]
    num_points = _pen.num_points

    # Generate initial points in a circle
    base_radius = min(width, height) // _pen.baseRadiusFactor
    # Generate random points around a circle
    angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
    points = [_pen.lastPoint]
    points = []

    # center_x = width // 2  # + _pen.xOffset  # + round(centerVariationX - random.random() * centerVariationX * 2)
    # center_y = height // 2  # + _pen.yOffset  # + round(centerVariationY - random.random() * centerVariationY * 2)
    center_x = 0
    center_y = 0

    # pieceLogger(f"Making curve _pen.xOffset {_pen.xOffset} _pen.yOffset {_pen.yOffset}")

    _xTravel = random.uniform(_pen.xTravelRange[0], _pen.xTravelRange[1])
    _yTravel = random.uniform(_pen.yTravelRange[0], _pen.yTravelRange[1])

    _xTravelIncr = random.uniform(_pen.xTravelIncr[0], _pen.xTravelIncr[1])
    _yTravelIncr = random.uniform(_pen.yTravelIncr[0], _pen.yTravelIncr[1])

    for _ in range(_pen.turns):
        for angle in angles:
            # Add random variation to the radius
            radius_x = base_radius * _pen.xRadiusFactor + (_pen.xRadiusFactorNoiseFactor - 2 * _pen.xRadiusFactorNoiseFactor * (random.random()))
            radius_y = base_radius * _pen.yRadiusFactor + (_pen.yRadiusFactorNoiseFactor - 2 * _pen.yRadiusFactorNoiseFactor * (random.random()))
            x = center_x + radius_x * np.cos(angle)
            y = center_y + radius_y * np.sin(angle)

            if random.random() < 0.1:
                x += _pen.xRandom
            if random.random() < 0.1:
                y += _pen.yRandom
            base_radius += random.uniform(-5, 5)

            base_radius += _pen.radiusChangePerRound

            points.append([x, y])

            if _pen.xtravelMode == 1:
                center_x += _xTravel
                _xTravel *= _xTravelIncr
            else:
                center_x += random.uniform(_pen.xTravelRange[0], _pen.xTravelRange[1])

            if _pen.ytravelMode == 1:
                center_y += _yTravel
                _yTravel *= _yTravelIncr
            else:
                center_y += random.uniform(_pen.yTravelRange[0], _pen.yTravelRange[1])
        _pen.lastPoint = [x, y]

    # Close the shape by repeating the first point
    points.append(points[0])
    # smoothLine(points, _pen)

    _pen.smooth_points = []
    res = chaikins_corner_cutting(points, 2).tolist()
    _pen.smooth_points.extend((pt[0] + _pen.xOffset, pt[1] + _pen.yOffset) for pt in res)
    # either clockwise or counter

    if random.random() < 0.5:
        _pen.smooth_points.reverse()


def generate_loop_stroke(_pen):

    pts = []
    _radiusX = _pen.radiusX
    _radiusY = _pen.radiusY
    deltaRadiusX = R(-_pen.xRadiusDelta, _pen.xRadiusDelta)
    deltaRadiusY = R(-_pen.yRadiusDelta, _pen.yRadiusDelta)

    deltaRadiusXCenter = R(-_pen.centerXDelta, _pen.centerXDelta)
    deltaRadiusYCenter = R(-_pen.centerYDelta, _pen.centerYDelta)

    _xCenter = 0
    _yCenter = 0

    points = _pen.points

    pieceLogger(f"deltaRadiusX {round(deltaRadiusX,4)}")
    pieceLogger(f"deltaRadiusY {round(deltaRadiusY,4)}")
    pieceLogger(f"deltaRadiusXCenter {round(deltaRadiusXCenter,4)}")
    pieceLogger(f"deltaRadiusYCenter {round(deltaRadiusYCenter,4)}")
    pieceLogger(f"_pen.loops {_pen.loops}")
    pieceLogger(f"points {points}")
    pieceLogger(f"_pen.speed {_pen.speed}")
    # pieceLogger(f"_pen.xOffset {_pen.xOffset}")
    # _pen.speed = 8

    for i in range(points):
        t = i / (points - 1)
        ang = _pen.loopDirection * t * math.pi * 2 * _pen.loops
        x = _xCenter + math.sin(ang) * _radiusX + R(-_pen.noiseX, _pen.noiseX)
        y = _yCenter - math.cos(ang) * _radiusY - t * _pen.height + R(-_pen.noiseY, _pen.noiseY)

        _radiusX += deltaRadiusX
        _radiusY += deltaRadiusY

        _xCenter += deltaRadiusXCenter
        _yCenter += deltaRadiusYCenter

        if R(0, 1.0) < _pen.deltaRadiusXChangeProb:
            deltaRadiusX = R(-_pen.xRadiusDelta, _pen.xRadiusDelta)

        if R(0, 1.0) < _pen.deltaRadiusYChangeProb:
            deltaRadiusY = R(-_pen.yRadiusDelta, _pen.yRadiusDelta)

        if R(0, 1.0) < _pen.deltaRadiusXCenterChangeProb:
            deltaRadiusXCenter = R(-_pen.centerXDelta, _pen.centerXDelta)

        if R(0, 1.0) < _pen.deltaRadiusYCenterChangeProb:
            deltaRadiusYCenter = R(-_pen.centerYDelta, _pen.centerYDelta)

        pts.append((x,y))

    # Extra points for smoother Bézier start/end
    pts.insert(0, pts[0])
    pts.append(pts[-1])
    pts.append(pts[-1])

    return pts


def get_curve_points(points, curve_drawn=True, resolution=50):

    if not curve_drawn or len(points) < 2:
        return points

    curve_points = []
    n = len(points)

    for i in range(n - 1):
        p0 = points[max(0, i - 1)]
        p1 = points[i]
        p2 = points[i + 1]
        p3 = points[min(n - 1, i + 2)]

        for step in range(resolution):
            t = step / float(resolution)  # 0 <= t < 1

            x = catmull_rom(p0[0], p1[0], p2[0], p3[0], t)
            y = catmull_rom(p0[1], p1[1], p2[1], p3[1], t)

            curve_points.append((x, y))

    return curve_points


def smoothLine(points, _pen):
    _lopOff = -round(_pen.lopOff)

    # print(f"_lopOff {_pen.lopOff} {_lopOff}")
    points = np.array(points)

    # Fit a B-spline to the points
    tck, u = splprep([points[:, 0], points[:, 1]], s=0, k=3, per=1)
    # tck, u = splprep([points[:, 0], points[:, 1]], s=0, k=3, per=1)

    # Generate more points along the spline for smoothness
    _mp = round(random.uniform(_pen.minInterpolatedPoints, _pen.maxInterpolatedPoints))
    u_new = np.linspace(0, 1, _mp)
    smooth_points = splev(u_new, tck)

    # Convert to list of tuples for PIL
    smooth_points_c = list(zip(smooth_points[0], smooth_points[1]))
    # _pen.rotationAngle = 0
    smooth_points_r = []
    for pt in smooth_points_c:
        ptx = pt[0] * np.cos(_pen.rotationAngle) - pt[1] * np.sin(_pen.rotationAngle)
        pty = pt[1] * np.cos(_pen.rotationAngle) + pt[0] * np.sin(_pen.rotationAngle)
        _pen.rotationAngle += _pen.rotationAngle / 500
        smooth_points_r.append((ptx + _pen.xOffset, pty + _pen.yOffset))

    _pen.smooth_points = smooth_points_r[:_lopOff]

    # either clockwise or counter
    if random.random() < 0.5:
        _pen.smooth_points.reverse()

    # print(f"line: {_mp} {_n} {noise_factor} ")

    # # Draw the shape
    # color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # for _p in range(1,len(smooth_points)) :
    #     _p1 = smooth_points[_p - 1]
    #     _p2 = smooth_points[_p]
    #     config.draw.line((_p1,_p2), fill = color, width=3)

    # config.draw.polygon(smooth_points, fill=None, outline=color, width=4)

    # return image
    return True


def pauseDrawing():
    config.stoppedAndWaitingToDraw = True
    config.canDraw = False
    config.drawingController.slotRate = random.uniform(config.activePalette.startNewLineDelayRange[0], config.activePalette.startNewLineDelayRange[1])
    # pieceLogger(f"paused for {config.drawingController.slotRate}")


def releaseDrawing():
    # print("released")
    config.stoppedAndWaitingToDraw = False
    config.canDraw = True
    # pieceLogger("Pen released")


def penLoopActions():
    if random.random() < config.activePalette.changePenColorWhileDrawingProb:
        setPenColor((config.activePalette.activePen))

    # if random.random() < config.startNewLineProb and config.activePalette.activePen._p == 0 and config.canDraw:
    if random.random() < config.startNewLineProb and config.activePalette.activePen._p == 0:
        _pen = choosePenMark()
        config.activePalette.activePen = _pen
        startNewLine(_pen)
        # pieceLogger(f"Next line: {config.activePalette.activePen.name}",4)

    if config.canDraw:
        drawLine(config.activePalette.activePen)

    # if not config.doingDrawing and config.canDraw and not config.stoppedAndWaitingToDraw:
    #     print(f"config.activePalette.activePen._p {config.activePalette.activePen._p}")
    #     print(f"config.canDraw {config.canDraw}")
    #     pauseDrawing()


def drawLine(_pen):
    if _pen.drawLineAsEnvelope:
        drawLinePolyEnvelope(_pen)
    else:
        drawLineSegments(_pen)


def drawLinePolyEnvelope(_pen):
    # Draw the shape
    if _pen._p == 1:
        pieceLogger(f"Drawing Line with: {_pen.name}")
        # { _pen.drawingSkipProb}
    _penSkip = random.random() <= _pen.drawingSkipProb

    for _ in range(_pen.speed):
        if _pen._p < len(_pen.smooth_points) and _pen._p > 0:
            _p1 = _pen.smooth_points[_pen._p - 1]
            _p2 = _pen.smooth_points[_pen._p]
            # if abs(_p1[0] - _p2[0])<10 and abs(_p1[1] - _p2[1]) < 30 :
            _dy = _p1[1] - _p2[1]
            _dx = _p1[0] - _p2[0]
            # changed 10-30-2025
            # _angle = (math.atan(_dy/_dx) * 360/math.pi)
            _angle = math.atan2(_dy, _dx) * 360 / math.pi

            if _angle < 0:
                _angle += 360

            _penWidth = _pen._w
            _lineColor = _pen.lineColor

            # old way, very chunky
            # config.draw.line((_p1, _p2), fill=_lineColor, width=_penWidth)

            _orthoAngle = math.pi - math.atan2(_dy, _dx)
            _sinOrthoAngle = math.sin(_orthoAngle)
            _cosOrthoAngle = math.cos(_orthoAngle)

            _orthoD = _penWidth / 2.2

            _orthoP1x = round(_orthoD * _sinOrthoAngle + _p1[0])
            _orthoP1y = round(_orthoD * _cosOrthoAngle + _p1[1])

            _orthoP2x = round(_orthoD * _sinOrthoAngle + _p2[0])
            _orthoP2y = round(_orthoD * _cosOrthoAngle + _p2[1])

            _orthoP3x = round(-_orthoD * _sinOrthoAngle + _p2[0])
            _orthoP3y = round(-_orthoD * _cosOrthoAngle + _p2[1])

            _orthoP4x = round(-_orthoD * _sinOrthoAngle + _p1[0])
            _orthoP4y = round(-_orthoD * _cosOrthoAngle + _p1[1])

            _drawdot = False
            try:
                if _pen._p > 1:
                    _drawdot = True

                    _orthoP1x = _pen.lastOrthoPoint[0]
                    _orthoP1y = _pen.lastOrthoPoint[1]

                    _orthoP4x = _pen.lastOrthoPoint[2]
                    _orthoP4y = _pen.lastOrthoPoint[3]

            except Exception as e:
                print(e)

            _poly = ((_orthoP1x, _orthoP1y), (_orthoP2x, _orthoP2y), (_orthoP3x, _orthoP3y), (_orthoP4x, _orthoP4y), (_orthoP1x, _orthoP1y))

            if not _penSkip:
                config.draw.polygon(_poly, fill=_lineColor, outline=None)

            # config.draw.line((_p1, _p2), fill=(255,0,0,255), width=1)

            # if not _markDrawn :
            _pen.lastAngle = _angle
            _pen._p += 1
            _pen.lastOrthoPoint = [_orthoP2x, _orthoP2y, _orthoP3x, _orthoP3y]

            config.doingDrawing = True
        if _pen._p == len(_pen.smooth_points):
            _pen._p = 0
            drawLineStopped()

        if random.random() < _pen.changeMarkWidthProb:
            if not _pen.attenuating and not _pen.enlarging:
                if random.random() < 0.5:
                    _pen.attenuating = True
                else:
                    _pen.enlarging = True
            elif random.random() < _pen.changeMarkWidthProb * 2:
                if _pen.attenuating:
                    _pen.enlarging = True
                    _pen.attenuating = False
                else:
                    _pen.enlarging = False
                    _pen.attenuating = True

        if _pen._w > _pen.maxMarkWidth:
            _pen.enlarging = False

        if _pen._w <= _pen.minMarkWidth:
            _pen.attenuating = False
            _pen._w = _pen.minMarkWidth

        if _pen.enlarging:
            _pen._w += round(1 * _pen.incrementFactor)
        if _pen.attenuating:
            _pen._w -= round(1 * _pen.incrementFactor)

        # time.sleep(.5)


def drawLineSegments(_pen):
    # Draw the shape
    # pieceLogger(f"pen {_pen.name}")
    _penSkip = random.random() <= _pen.drawingSkip
    for _ in range(_pen.speed):
        if _pen._p < len(_pen.smooth_points) and _pen._p > 0:
            _p1 = _pen.smooth_points[_pen._p - 1]
            _p2 = _pen.smooth_points[_pen._p]
            # if abs(_p1[0] - _p2[0])<10 and abs(_p1[1] - _p2[1]) < 30 :
            # changed 10-30-2025
            # _angle = abs(math.atan(_p2[1] - _p1[1])/(_p2[0] - _p1[0]))
            _angle = math.atan2(_p2[1] - _p1[1], _p2[0] - _p1[0])
            _penWidth = _pen._w
            if _angle > 30:
                _penWidth - 1
            # pieceLogger(_angle)
            if not _penSkip:
                config.draw.line((_p1, _p2), fill=_pen.lineColor, width=_penWidth)
            _pen._p += 1
            config.doingDrawing = True
        if _pen._p == len(_pen.smooth_points):
            _pen._p = 0
            drawLineStopped()

        if random.random() < _pen.changeMarkWidthProb:
            if not _pen.attenuating and not _pen.enlarging:
                if random.random() < 0.5:
                    _pen.attenuating = True
                else:
                    _pen.enlarging = True
            elif random.random() < _pen.changeMarkWidthProb * 2:
                if _pen.attenuating:
                    _pen.enlarging = True
                    _pen.attenuating = False
                else:
                    _pen.enlarging = False
                    _pen.attenuating = True

        if _pen._w > _pen.maxMarkWidth:
            _pen.enlarging = False

        if _pen._w <= _pen.minMarkWidth:
            _pen.attenuating = False
            _pen._w = _pen.minMarkWidth

        if _pen.enlarging:
            _pen._w += round(1 * _pen.incrementFactor)
        if _pen.attenuating:
            _pen._w -= round(1 * _pen.incrementFactor)


def drawLineStopped():
    # pieceLogger("Pen stopped")
    config.doingDrawing = False
    pauseDrawing()
    if config.alwaysJitterLineAfterDrawn:
        doDrawingJitter()


# ----------------------------------------------------##----------------------------------------------------#


def doDrawingJitter():
    jitterIterations = round(random.uniform(config.jitterIterationsMin, config.jitterIterationsMax))
    # pieceLogger(f"jitterIterations {jitterIterations} {config.jitterIterationsMax}")
    # for _ in range(jitterIterations):
    #     glitchBox(
    #         config.image,
    #         config.canvasWidth,
    #         config.canvasHeight,
    #         config.jitterIterationsHoriz,
    #         config.jitterIterationsVert,
    #     )
    for _ in range(jitterIterations):
        glitchBox(
            config.underLayer,
            config.canvasWidth,
            config.canvasHeight,
            config.bgGlitchDisplacementHorizontal,
            config.bgGlitchDisplacementVertical,
        )


def bgColorBlocksFilling(arg):
    global config

    if not arg:
        pieceLogger(f"drawing a bg box {config.blendLevel}")
    config.blendLevelRate = config.blendLevelRateBase
    config.blendLevel = 0.0

    xPos = math.floor(random.uniform(config.activePalette.bgBoxRange[0], config.activePalette.bgBoxRange[1]))
    yPos = math.floor(random.uniform(config.activePalette.bgBoxRange[2], config.activePalette.bgBoxRange[3]))

    config.tileSizeWidth = round(random.uniform(config.bgTileSizeWidthMin, config.bgTileSizeWidthMax))
    config.tileSizeHeight = round(random.uniform(config.bgTileSizeHeightMin, config.bgTileSizeHeightMax))

    if random.SystemRandom().random() < config.clearbgBoxProb:
        xPos = yPos = 0
        config.bgBoxBox = (
            xPos,
            yPos,
            xPos + config.canvasWidth,
            yPos + config.canvasHeight,
        )
        config.bgBoxFill = (0, 0, 0, 0)
    else:

        # xPos = round(random.uniform(-0,config.tileSizeWidth) )
        # yPos = round(random.uniform(-0,config.tileSizeHeight) )
        config.bgBoxBox = (
            xPos,
            yPos,
            xPos + config.tileSizeWidth,
            yPos + config.tileSizeHeight,
        )

        cR = random.choice(config.activePalette.bgBoxColorSets)
        # cR = config.activePalette.bgBoxColorRange
        # print(cR)
        config.bgBoxFill = colorutils.getRandomColorHSV(
            cR[0],
            cR[1],
            cR[2],
            cR[3],
            cR[4],
            cR[5],
            cR[6],
            cR[7],
            round(random.uniform(config.activePalette.bgBoxAlphaRange[0], config.activePalette.bgBoxAlphaRange[1])),
            config.brightness,
        )

        if random.random() < config.totalRandomBGBoxColorProb:
            config.bgBoxFill = colorutils.getRandomColorHSV(
                0, 360, 0.1, 1.0, 0.1, 1.0, 0, 0, round(random.uniform(config.activePalette.bgBoxAlphaRange[0], config.activePalette.bgBoxAlphaRange[1])), config.brightness
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


def glitchBox(
    imageRef,
    apparentWidth,
    apparentHeight,
    imageGlitchDisplacementHorizontal,
    imageGlitchDisplacementVertical,
):

    global config

    # apparentWidth = config.canvasImage.size[0]
    # apparentHeight = config.canvasImage.size[1]

    dx = round(random.uniform(-imageGlitchDisplacementHorizontal, imageGlitchDisplacementHorizontal))
    dy = round(random.uniform(-imageGlitchDisplacementVertical, imageGlitchDisplacementVertical))

    sectionWidth = round(random.uniform(2, apparentWidth - dx))
    sectionHeight = round(random.uniform(2, apparentHeight - dy))

    # print(f"jitter {sectionWidth} {sectionHeight} {dx} {dx}")

    # 95% of the time they dance together as mirrors
    try:
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
        pieceLogger(f"jitter prom {e} {dx + sectionWidth} , {dy + sectionHeight}")
    # end try


# ----------------------------------------------------##----------------------------------------------------#


def setBGColor():

    _bgColorSet = random.choice(config.activePalette.bgColorSets)
    config.bgColor = colorutils.getRandomColorHSV(*_bgColorSet)
    # config.bgColor = colorutils.getRandomColorHSV(*config.activePalette.bgColor)
    # pieceLogger(f"New BGColor: config.activePalette.bgColor {config.activePalette.bgColor} --> config.bgColor {config.bgColor}")


def primeCanvas(_i=3):
    global config
    for _ in range(_i):
        bgColorBlocksFilling(True)


def chooseTexture():
    _textureName = config.activePalette.textureName
    for _t in config.textureSets:
        # print(f"{_pen.name} {config.activePalette.pens}")
        if _t.name == _textureName:
            # print(f"we chose {_pen.name}")
            return _t


# ----------------------------------------------------##----------------------------------------------------#


def createImageLayers(arg=None):
    global config

    pieceLogger("===> Setting up all layers")
    config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.draw = ImageDraw.Draw(config.image)

    config.underLayer = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.underLayerDraw = ImageDraw.Draw(config.underLayer)

    config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.canvasDraw = ImageDraw.Draw(config.canvasImage)

    config.textureLayer = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.textureLayerDraw = ImageDraw.Draw(config.textureLayer)

    config.finalCompositeLayer = Image.new("RGBA", (config.screenWidth, config.screenHeight))
    config.finalCompositeLayerDraw = ImageDraw.Draw(config.finalCompositeLayer)

    config.renderImageFullOverlay = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.renderDrawOver = ImageDraw.Draw(config.renderImageFullOverlay)


def createTextureLayer(tex):
    config.useTextureLayer = tex.useTextureLayer
    config.textureBlendMode = tex.blendMode
    pieceLogger(f"===> config.useTextureLayer {config.useTextureLayer}")
    for _row in range(tex.blockRows):
        for _col in range(tex.blockCols):
            if random.random() > tex.skipProb:
                for _r in range(0, tex.rows, tex.step):
                    for _c in range(0, tex.cols, tex.step):
                        x1 = _c + _col * tex.cols
                        y1 = _r + _row * tex.rows
                        x2 = x1 + tex.px
                        y2 = y1 + tex.px
                        _rate = random.uniform(1, 3)
                        _a = 2 + round(tex.base / tex.base * _r / ((tex.rows - _r) * tex.rate) * _c / ((tex.cols - _c) * tex.rate))

                        if tex.base == 255:
                            _a = tex.base
                        if random.random() < tex.drawMark:
                            if tex.usedots:
                                config.textureLayerDraw.ellipse((x1, y1, x2, y2), fill=(tex.clr_r, tex.clr_g, tex.clr_b, _a), outline=None)
                            else:
                                config.textureLayerDraw.rectangle((x1, y1, x2 + tex.xtick, y2 + tex.ytick), fill=(tex.clr_r, tex.clr_g, tex.clr_b, _a), outline=None)
                                # config.textureLayerDraw.line((x1, y1, x2+_xtick, y2+_ytick), fill=(_clr_r, _clr_g, _clr_b, 255), width=0)
    if tex.blur > 0:
        config.textureLayer = config.textureLayer.filter(ImageFilter.GaussianBlur(radius=tex.blur))


def initDrawings():
    global config
    pieceLogger(f"===> Init drawings: {config.activePalette.name}", 4, True)

    createTextureLayer(chooseTexture())
    config.underLayerDraw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=config.bgColor)

    primeCanvas()

    _pen = choosePenMark()
    config.activePalette.activePen = _pen
    config.startNewLineProb = config.activePalette.startNewLineProb
    config.usebgBoxProb = config.activePalette.usebgBoxProb
    config.clearCurrentDrawingProb = config.activePalette.clearCurrentDrawingProb
    config.doJitterProb = config.activePalette.doJitterProb
    config.bgGlitchCyclesMin = config.activePalette.bgGlitchCyclesMin
    config.bgGlitchCyclesMax = config.activePalette.bgGlitchCyclesMax
    config.bgGlitchDisplacementHorizontal = config.activePalette.bgGlitchDisplacementHorizontal
    config.bgGlitchDisplacementVertical = config.activePalette.bgGlitchDisplacementVertical

    startNewLine(_pen)
    doDrawingJitter()


# ----------------------------------------------------##----------------------------------------------------#


def runWork():
    while True:
        config.directorController.checkTime()
        if config.directorController.advance:
            iterate()

        time.sleep(config.redrawSpeed)


def iterate():
    global config

    if random.random() < config.justHitPauseProb and not config.justHitPause:
        config.justHitPause = True
        pieceLogger(f"I am paused {config.justHitPauseProb}")
    if random.random() < config.releaseFromJustHitPauseProb and config.justHitPause:
        config.justHitPause = False
        pieceLogger("I am un paused")

    if not config.justHitPause:

        def maybe_change_drawing_mode():
            if config.changeDrawingModeTime > 0:
                config.changeTimeController.checkTime()
                if config.changeTimeController.advance:
                    changeDrawingMode()

        def maybe_change_color_set():
            if config.changeColorSetTime > 0 and not config.transitionStateHandler.inTransition:
                config.paletteController.checkTime()
                if config.paletteController.advance:
                    pieceLogger(f"===>  changeDrawing(True) prob: config.changeColorSetTime {config.changeColorSetTime}")
                    changeDrawing(True)

        def maybe_release_drawing():
            if config.stoppedAndWaitingToDraw:
                config.drawingController.checkTime()
                if config.drawingController.advance:
                    releaseDrawing()

        def maybe_set_bg_color():
            if random.SystemRandom().random() < config.changeBGColorProb / config.slownessFactor:
                setBGColor()

        def maybe_clear_current_drawing():
            if random.random() < config.clearCurrentDrawingProb and not config.transitionStateHandler.inTransition:
                pieceLogger(f"===>  clearCurrentDrawing() prob: config.clearCurrentDrawingProb {config.clearCurrentDrawingProb}")
                clearCurrentDrawing()

        def maybe_bg_color_blocks_filling():
            if random.SystemRandom().random() < config.usebgBoxProb and not config.doingDrawing and not config.transitionStateHandler.inTransition:
                # pieceLogger("Doing bg blocks")
                if config.doJitterWhenAddingBG:
                    doDrawingJitter()
                bgColorBlocksFilling(config)

        def maybe_filter_remap_image():
            if random.random() < config.filterRemappingProb / config.slownessFactor:
                filterRemapImage(config)

        def maybe_do_drawing_jitter():
            if not config.doingDrawing and random.random() < config.doJitterProb / config.slownessFactor and not config.transitionStateHandler.inTransition:
                # pieceLogger("Doing jitter")
                doDrawingJitter()

        maybe_change_drawing_mode()
        maybe_change_color_set()
        maybe_release_drawing()
        maybe_set_bg_color()
        maybe_clear_current_drawing()
        maybe_bg_color_blocks_filling()
        maybe_filter_remap_image()
        maybe_do_drawing_jitter()
        penLoopActions()
    renderImage()


def renderImage():
    global config

    def maybe_take_snapshot(img):
        config.stateReportController.checkTime()
        path = "/Users/lamshell/Desktop/outputs/"
        if config.stateReportController.advance:
            pieceLogger("Saving image to file", 2)
            currentTime = time.time()
            baseName = f"{str(currentTime)}"
            baseName = baseName.replace(".", "")
            _img = img.convert("RGBA")
            _temp = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
            _tempDraw = ImageDraw.Draw(_temp)
            _tempDraw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=(0, 0, 0, 255))
            _temp.paste(_img)
            _temp = _temp.convert("RGB")
            _temp = _temp.rotate(-90)
            fn = f"{path}{baseName}.png"
            _temp.save(fn)
            # fn2 = f"{baseName}-palette.txt"
            fn2 = "palettes.txt"
            with open(f"/Users/lamshell/Desktop/outputs/{fn2}", "a+") as f:
                _bg = colorutils.rgb_to_hsv(config.bgColor[0], config.bgColor[1], config.bgColor[2], config.bgColor[3], True)
                _bgf = colorutils.rgb_to_hsv(config.bgBoxFill[0], config.bgBoxFill[1], config.bgBoxFill[2], config.bgBoxFill[3], True)
                _pc = colorutils.rgb_to_hsv(
                    config.activePalette.activePen.lineColor[0],
                    config.activePalette.activePen.lineColor[1],
                    config.activePalette.activePen.lineColor[2],
                    config.activePalette.activePen.lineColor[3],
                    True,
                )

                f.write(f"\n{baseName} bg:{_bg} {config.bgColor[3]} fill:{_bgf} {config.bgBoxFill[3]} pen:{_pc} {config.activePalette.activePen.lineColor[3]}")

    config.underLayer.paste(config.image, (0, 0), config.image)

    # config.textureLayerDraw.rectangle((50,50,100,150), fill=(200,0,200,200))
    if config.useTextureLayer and config.textureBlendMode is None:
        # config.underLayer.paste(config.textureLayer, (0, 0), config.textureLayer)
        config.canvasImage.paste(config.textureLayer, (0, 0), config.textureLayer)

    _tempImage = ImageChops.blend(config.canvasImage, config.underLayer, config.blendLevel)

    config.blendLevel += config.blendLevelRate

    if config.blendLevel >= 1.0:
        config.blendLevelRate = 0.0
        config.blendLevel = 1.0

    if config.fadeThruToNew < 255:
        config.fadeThruToNew += 4
        # print(f"config.fadeThruToNew  {config.fadeThruToNew }")
        config.canvasDraw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=(config.bgColor[0], config.bgColor[1], config.bgColor[2], config.fadeThruToNew))
    elif not config.fadeThruToNewDone:
        config.fadeThruToNewDone = True
        initDrawings()

    config.canvasImage.paste(config.underLayer, (0, 0), config.underLayer)
    # config.canvasImage.paste(_tempImage, (0, 0), _tempImage)

    if not config.debugMode:
        config.finalCompositeLayerDraw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=(config.bgColor))
        # config.canvasImage.paste(config.textureLayer, (0, 0), config.textureLayer)
        if config.textureBlendMode == "subtract":
            _tempImage = ImageChops.subtract(config.canvasImage, config.textureLayer)
            config.finalCompositeLayer.paste(_tempImage, (0, 0), _tempImage)
        else:
            config.finalCompositeLayer.paste(config.canvasImage, (0, 0), config.canvasImage)
        # config.finalCompositeLayer.paste(config.textureLayer, (0, 0), config.textureLayer)
    else:
        layerCompositing(config)

    if config.transitionStateHandler.inTransition:
        config.transitionStateHandler.transition()
        config.render(config.transitionStateHandler.intermediateImage, 0, 0)
        # maybe_take_snapshot(config.transitionStateHandler.intermediateImage)
    else:
        config.render(config.finalCompositeLayer, 0, 0)
        # maybe_take_snapshot(config.finalCompositeLayer)


def layerCompositing(config):
    config.finalCompositeLayerDraw.rectangle((0, 0, config.screenWidth, config.screenHeight), fill=(125, 125, 125))
    config.finalCompositeLayerDraw.rectangle((0, 550, config.canvasWidth, 550 + config.canvasHeight), fill=(config.bgColor))

    config.finalCompositeLayer.paste(config.textureLayer, (0, 0), config.textureLayer)
    config.finalCompositeLayer.paste(config.image, (280, 0), config.image)
    config.finalCompositeLayer.paste(config.underLayer, (0, 280), config.underLayer)

    config.finalCompositeLayerDraw.rectangle((280, 280, config.canvasWidth + 280, 280 + config.canvasHeight), fill=(config.bgColor))
    config.finalCompositeLayer.paste(config.canvasImage, (280, 280), config.canvasImage)


def clearCurrentDrawing():
    if not config.transitionStateHandler.inTransition:
        initiateTransition()

        config.underLayerDraw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=(config.bgColor[0], config.bgColor[1], config.bgColor[2], 200))

        config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
        config.draw = ImageDraw.Draw(config.image)

        config.underLayer = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
        config.underLayerDraw = ImageDraw.Draw(config.underLayer)

        primeCanvas(2)
        config.canvasDraw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=(config.bgColor[0], config.bgColor[1], config.bgColor[2], 225))


# ----------------------------------------------------##----------------------------------------------------#


def main(run=True):
    global config, workConfig
    _setBundlePath(config)
    _load_texture_models(config)
    createImageLayers(config)
    _load_filter_config(config)
    _load_drawing_configs(config)
    _load_pen_config(config)
    _load_and_initialize_system(config)
    if run:
        runWork()


def _setBundlePath(config):
    config.drawingBundle = workConfig.get("drawingField", "drawingBundle")
    config.assetPath = config.path
    if config.assetPath[-1] != "/":
        config.assetPath = f"{config.path}/"
    config.assetPath = f"{config.assetPath}configs/{config.drawingBundle}"
    if config.assetPath[-1] != "/":
        config.assetPath = f"{config.assetPath}/"
    # pieceLogger(f"{config.assetPath}",4)
    return config.assetPath


def _load_texture_models(config):
    config.useTextureLayer = True
    config.textureSetNames = workConfig.get("drawingField", "textureSets", fallback="texture1").split(",")
    config.textureSets = []
    for _t in config.textureSetNames:
        _tex = _load_texture_values(_t)
        config.textureSets.append(_tex)


def _load_texture_values(_tName):
    tex = Texture()
    tex.name = _tName
    textureConfig = configparser.ConfigParser()
    textureConfig.read(f"{config.assetPath}/textures/{_tName}.cfg")
    tex.useTextureLayer = textureConfig.getboolean("texture", "useTextureLayer", fallback=False)
    pieceLogger(f"{config.assetPath}/textures/{_tName}.cfg {_tName} {tex.useTextureLayer}")
    tex.step = textureConfig.getint("texture", "texture_step", fallback=7)
    tex.px = textureConfig.getint("texture", "texture_px", fallback=2)
    tex.blockRows = textureConfig.getint("texture", "texture_blockRows", fallback=8)
    tex.blockCols = textureConfig.getint("texture", "texture_blockCols", fallback=8)
    tex.rows = textureConfig.getint("texture", "texture_rows", fallback=64)
    tex.cols = textureConfig.getint("texture", "texture_cols", fallback=32)
    tex.rate = textureConfig.getint("texture", "texture_rate", fallback=2)
    tex.base = textureConfig.getint("texture", "texture_base", fallback=125)
    tex.clr_r = textureConfig.getint("texture", "texture_clr_r", fallback=40)
    tex.clr_g = textureConfig.getint("texture", "texture_clr_g", fallback=40)
    tex.clr_b = textureConfig.getint("texture", "texture_clr_b", fallback=240)
    tex.skipProb = textureConfig.getfloat("texture", "texture_skipProb", fallback=0.7)
    tex.blur = textureConfig.getint("texture", "texture_blur", fallback=1)
    tex.xtick = textureConfig.getint("texture", "texture_xtick", fallback=0)
    tex.ytick = textureConfig.getint("texture", "texture_ytick", fallback=0)
    tex.drawMark = textureConfig.getfloat("texture", "texture_drawMark", fallback=0.9)
    tex.usedots = textureConfig.getboolean("texture", "texture_usedots", fallback=True)
    tex.blendMode = textureConfig.get("texture", "blendMode", fallback=None)
    return tex


def _load_filter_config(config):
    """Loads filter-related configuration parameters."""
    config.filterRemapping = workConfig.getboolean("particles", "filterRemapping", fallback=False)
    config.filterRemappingProb = float(workConfig.get("drawingField", "filterRemappingProb", fallback=0.0))
    config.filterRemapMinHorzSize = int(workConfig.get("drawingField", "filterRemapMinHorzSize", fallback=24))
    config.filterRemapMinVertSize = int(workConfig.get("drawingField", "filterRemapMinVertSize", fallback=24))
    config.filterRemapMaxHorzSize = int(workConfig.get("drawingField", "filterRemapMaxHorzSize", fallback=24))
    config.filterRemapMaxVertSize = int(workConfig.get("drawingField", "filterRemapMaxVertSize", fallback=24))
    config.filterRemapRangeX = int(workConfig.get("drawingField", "filterRemapRangeX", fallback=config.canvasWidth))
    config.filterRemapRangeY = int(workConfig.get("drawingField", "filterRemapRangeY", fallback=config.canvasHeight))


def _load_drawing_configs(config):
    """Loads color-related configuration parameters."""
    config.doJitterProb = float(workConfig.get("drawingField", "doJitterProb", fallback=0.1))
    config.usebgBox = workConfig.getboolean("drawingField", "forcebgBox")
    config.bgTileSizeWidthMin = float(workConfig.get("drawingField", "bgTileSizeWidthMin"))
    config.bgTileSizeWidthMax = float(workConfig.get("drawingField", "bgTileSizeWidthMax"))
    config.bgTileSizeHeightMin = float(workConfig.get("drawingField", "bgTileSizeHeightMin"))
    config.bgTileSizeHeightMax = float(workConfig.get("drawingField", "bgTileSizeHeightMax"))
    # config.bgBoxFill = tuple(	map(lambda x: int(x), workConfig.get("drawingField", "bgBoxFill").split(",")))

    config.clearbgBoxProb = float(workConfig.get("drawingField", "clearbgBoxProb"))
    config.bgGlitchCyclesMin = float(workConfig.get("drawingField", "bgGlitchCyclesMin"))
    config.bgGlitchCyclesMax = float(workConfig.get("drawingField", "bgGlitchCyclesMax"))
    config.bgGlitchDisplacementHorizontal = float(workConfig.get("drawingField", "bgGlitchDisplacementHorizontal"))
    config.bgGlitchDisplacementVertical = float(workConfig.get("drawingField", "bgGlitchDisplacementVertical"))

    config.penAlpha = int(workConfig.get("drawingField", "penAlpha", fallback=200))
    config.bgColorAlpha = int(workConfig.get("drawingField", "bgColorAlpha", fallback=2))

    config.noPenGrays = 0.0
    config.nobgGrays = 0.0

    config.drawLineAsEnvelope = workConfig.getboolean("drawingField", "drawLineAsEnvelope", fallback=False)

    config.paletteSets = []
    paletteSets = workConfig.get("drawingField", "paletteSets").split(",")

    for _pRaw in paletteSets:
        palette = Palette()
        _p = _pRaw.replace("\n", "")
        palette.bgBoxAlphaRange = tuple(
            map(
                lambda x: int(x),
                workConfig.get(_p, "bgBoxAlphaRange").split(","),
            )
        )

        # config.bgColorAlpha

        # palette.nobgGrays = float(workConfig.get(_p, "nobgGrays", fallback=0))
        # palette.bgColor = list(
        #     map(
        #         lambda x: float(x),
        #         workConfig.get(_p, "bgColor").split(","),
        #     )
        # )
        # palette.bgColor.extend([config.bgColorAlpha, config.brightness, palette.nobgGrays])

        # palette.bgBoxColorRange = list(
        #     map(
        #         lambda x: float(x),
        #         workConfig.get(_p, "bgBoxColorRange").split(","),
        #     )
        # )

        # palette.penColor = tuple(
        #     map(
        #         lambda x: float(x),
        #         workConfig.get(_p, "penColor").split(","),
        #     )
        # )

        _bgColorSetsRaw = workConfig.get(_p, "bgColorSets")
        _bgColorSetsRaw = re.sub(r"[\(\)]", "", _bgColorSetsRaw)
        _bgColorSetsRaw = _bgColorSetsRaw.split("|")
        palette.bgColorSets = []
        palette.bgColorSets.extend(tuple(map(lambda x: float(x), _set.split(","))) for _set in _bgColorSetsRaw)

        _penColorSetsRaw = workConfig.get(_p, "penColorSets")
        _penColorSetsRaw = re.sub(r"[\(\)]", "", _penColorSetsRaw)
        _penColorSetsRaw = _penColorSetsRaw.split("|")
        palette.penColorSets = []
        palette.penColorSets.extend(tuple(map(lambda x: float(x), _set.split(","))) for _set in _penColorSetsRaw)

        _bgBoxColorSetsRaw = workConfig.get(_p, "bgBoxColorSets")
        _bgBoxColorSetsRaw = re.sub(r"[\(\)]", "", _bgBoxColorSetsRaw)
        _bgBoxColorSetsRaw = _bgBoxColorSetsRaw.split("|")
        palette.bgBoxColorSets = []
        palette.bgBoxColorSets.extend(tuple(map(lambda x: float(x), _set.split(","))) for _set in _bgBoxColorSetsRaw)

        palette.bgBoxRange = list(
            map(
                lambda x: int(x),
                workConfig.get(_p, "bgBoxRange", fallback="0,0,0,0").split(","),
            )
        )

        if palette.bgBoxRange == [0, 0, 0, 0]:
            palette.bgBoxRange = [0, config.canvasWidth, 0, config.canvasHeight]

        palette.noPenGrays = float(workConfig.get(_p, "noPenGrays", fallback=0))

        palette.pens = workConfig.get(_p, "penNames").split(",")
        palette.name = _p
        palette.textureName = workConfig.get(_p, "texture")
        palette.usebgBoxProb = float(workConfig.get(_p, "usebgBoxProb", fallback=".01"))
        palette.blendLevelRateBase = float(workConfig.get(_p, "blendLevelRateBase", fallback=".01"))
        palette.clearCurrentDrawingProb = float(workConfig.get(_p, "clearCurrentDrawingProb", fallback=".0001"))

        # when set to 1.0 and startNewLineDelayRange is set
        # then the new line starts as soon as the random delay
        # ends - since drawing is a major event and changes the
        # attention of the viewer, controlling when it happens
        # is probably better left to timing than just cycle-based
        # probability
        palette.startNewLineProb = float(workConfig.get(_p, "startNewLineProb", fallback=".01"))
        palette.startNewLineDelayRange = list(map(lambda x: float(x), workConfig.get(_p, "startNewLineDelayRange", fallback="1,10").split(",")))
        palette.slownessFactor = float(workConfig.get(_p, "slownessFactor", fallback="1.0"))

        palette.doJitterProb = float(workConfig.get(_p, "doJitterProb", fallback=config.doJitterProb))
        palette.bgGlitchCyclesMin = float(workConfig.get(_p, "bgGlitchCyclesMin", fallback=config.bgGlitchCyclesMin))
        palette.bgGlitchCyclesMax = float(workConfig.get(_p, "bgGlitchCyclesMax", fallback=config.bgGlitchCyclesMax))
        palette.bgGlitchDisplacementHorizontal = float(workConfig.get(_p, "bgGlitchDisplacementHorizontal", fallback=config.bgGlitchDisplacementHorizontal))
        palette.bgGlitchDisplacementVertical = float(workConfig.get(_p, "bgGlitchDisplacementVertical", fallback=config.bgGlitchDisplacementVertical))
        palette.penSpeedMinVal = float(workConfig.get(_p, "penSpeedMinVal", fallback=1)) 
        palette.penSpeedMaxVal = float(workConfig.get(_p, "penSpeedMaxVal", fallback=5)) 

        palette.xOffsetRange = list(
            map(
                lambda x: float(x),
                workConfig.get(_p, "xOffsetRange", fallback=f"0,{config.canvasWidth}").split(","),
            )
        )
        palette.yOffsetRange = list(
            map(
                lambda x: float(x),
                workConfig.get(_p, "yOffsetRange", fallback=f"0,{config.canvasHeight}").split(","),
            )
        )
        palette.penAlphaRange = list(
            map(
                lambda x: float(x),
                workConfig.get(_p, "penAlphaRange", fallback=f"{config.penAlpha},{config.penAlpha}").split(","),
            )
        )

        palette.changePenColorWhileDrawingProb = float(workConfig.get(_p, "changePenColorWhileDrawingProb", fallback=0.01))
        palette.drawLineAsEnvelope = workConfig.getboolean(_p, "drawLineAsEnvelope", fallback=config.drawLineAsEnvelope)

        pieceLogger(f"\n===> Loading palette: {palette.name}  Using enveloped line: {palette.drawLineAsEnvelope}")
        config.paletteSets.append(palette)

    config.activePalette = random.choice(config.paletteSets)
    config.slownessFactor = config.activePalette.slownessFactor
    pieceLogger(f"\n ===> New Palette : {config.activePalette.name} Using enveloped line: {palette.drawLineAsEnvelope}", 2, True)

    setBGColor()


def _load_pen_config(config):
    """Loads pen / brush related configuration parameters."""

    def _load_pen_config_globals(config):
        config.penNames = workConfig.get("drawingField", "penNames").split(",")
        config.marksPalette = []

    def _load_single_pen(_penConfigName):
        _mark = Mark()
        _mark.name = f"{_penConfigName}".replace("\n", "")

        markConfig = configparser.ConfigParser()
        pathToCfg = f"{config.assetPath}marks/{_mark.name}.cfg"
        pieceLogger(f"{pathToCfg}")
        markConfig.read(pathToCfg)

        _mark.turnsRange = list(map(lambda x: int(x), markConfig.get("markParams", "turnsRange", fallback="2,2").split(",")))

        if "scribble" in _mark.name :

            _mark.loopsMin = _mark.turnsRange[0]
            _mark.loopsMax = _mark.turnsRange[1]

            _mark.pointsPerLoop = int(markConfig.get("markParams", "pointsPerLoop")) 
            _mark.noiseX = float(markConfig.get("markParams", "noiseX")) 
            _mark.noiseY = float(markConfig.get("markParams", "noiseY")) 

            _mark.height = float(markConfig.get("markParams", "height")) 
            _mark.radiusX = float(markConfig.get("markParams", "radiusX")) 
            _mark.radiusY = float(markConfig.get("markParams", "radiusY")) 
            _mark.radiusXMin = float(markConfig.get("markParams", "radiusXMin")) 
            _mark.radiusXMax = float(markConfig.get("markParams", "radiusXMax")) 
            _mark.radiusYMin = float(markConfig.get("markParams", "radiusYMin")) 
            _mark.radiusYMax = float(markConfig.get("markParams", "radiusYMax")) 
            _mark.xRadiusDelta = float(markConfig.get("markParams", "xRadiusDelta")) 
            _mark.yRadiusDelta = float(markConfig.get("markParams", "yRadiusDelta")) 
            _mark.deltaRadiusXChangeProb = float(markConfig.get("markParams", "deltaRadiusXChangeProb")) 
            _mark.deltaRadiusYChangeProb = float(markConfig.get("markParams", "deltaRadiusYChangeProb")) 

            _mark.xCenter = float(markConfig.get("markParams", "xCenter")) 
            _mark.yCenter = float(markConfig.get("markParams", "yCenter")) 
            _mark.centerXDelta = float(markConfig.get("markParams", "centerXDelta")) 
            _mark.centerYDelta = float(markConfig.get("markParams", "centerYDelta")) 
            _mark.deltaRadiusXCenterChangeProb = float(markConfig.get("markParams", "deltaRadiusXCenterChangeProb")) 
            _mark.deltaRadiusYCenterChangeProb = float(markConfig.get("markParams", "deltaRadiusYCenterChangeProb")) 
            
        else :

            _mark.minNumPoints = int(markConfig.get("markParams", "minNumPoints"))
            _mark.maxNumPoints = int(markConfig.get("markParams", "maxNumPoints", fallback=8))
            _mark.minInterpolatedPoints = int(markConfig.get("markParams", "minInterpolatedPoints", fallback=200))
            _mark.maxInterpolatedPoints = int(markConfig.get("markParams", "maxInterpolatedPoints", fallback=200))

            _mark.baseRadiusFactorRange = list(map(lambda x: float(x), markConfig.get("markParams", "baseRadiusFactorRange", fallback="1.0,1.0").split(",")))
            _mark.xRadiusFactorRange = list(map(lambda x: float(x), markConfig.get("markParams", "xRadiusFactorRange", fallback=".2,.2").split(",")))
            _mark.yRadiusFactorRange = list(map(lambda x: float(x), markConfig.get("markParams", "yRadiusFactorRange", fallback=".2,.2").split(",")))

            _mark.xRadiusFactorNoiseFactor = float(markConfig.get("markParams", "xRadiusFactorNoiseFactor", fallback=1.0))
            _mark.yRadiusFactorNoiseFactor = float(markConfig.get("markParams", "yRadiusFactorNoiseFactor", fallback=1.0))
            _mark.xRandomRange = list(map(lambda x: int(x), markConfig.get("markParams", "xRandomRange", fallback="-1,1").split(",")))
            _mark.yRandomRange = list(map(lambda x: int(x), markConfig.get("markParams", "yRandomRange", fallback="-1,1").split(",")))

            _mark.rotationFactor = float(markConfig.get("markParams", "rotationFactor", fallback=8.0))
           
            # adding parameters to enable geometric progression in x and y in addition to random arithmetic travel in x and y
            _mark.xTravelRange = list(map(lambda x: int(x), markConfig.get("markParams", "xTravelRange", fallback="-1,1").split(",")))
            _mark.yTravelRange = list(map(lambda x: int(x), markConfig.get("markParams", "yTravelRange", fallback="-1,1").split(",")))
            _mark.xTravelIncrRange = list(map(lambda x: float(x), markConfig.get("markParams", "xTravelIncrRange", fallback="-1,1").split(",")))
            _mark.yTravelIncrRange = list(map(lambda x: float(x), markConfig.get("markParams", "yTravelIncrRange", fallback="-1,1").split(",")))
            _mark.xtravelProb = float(markConfig.get("markParams", "xtravelProb", fallback=0.1))
            _mark.ytravelProb = float(markConfig.get("markParams", "ytravelProb", fallback=0.1))
            _mark.radiusChangePerRound = float(markConfig.get("markParams", "radiusChangePerRound", fallback="0"))

            _mark.linePoints = float(markConfig.get("markParams", "linePoints", fallback="20"))
            _mark.lopOff = float(markConfig.get("markParams", "lopOff", fallback="20"))

        _mark.xOffsetRange = markConfig.get("markParams", "xOffsetRange", fallback=None)
        _mark.incrementFactor = float(markConfig.get("markParams", "incrementFactor", fallback="1"))
        _mark.yOffsetRange = markConfig.get("markParams", "yOffsetRange", fallback=None)

        if _mark.xOffsetRange is not None:
            _mark.xOffsetRange = list(map(lambda x: int(x), markConfig.get("markParams", "xOffsetRange").split(",")))

        if _mark.yOffsetRange is not None:
            _mark.yOffsetRange = list(map(lambda x: int(x), markConfig.get("markParams", "yOffsetRange").split(",")))

        _mark.w = int(markConfig.get("markParams", "w", fallback=1))
        _mark.minMarkWidth = int(markConfig.get("markParams", "minMarkWidth", fallback=2))
        _mark.maxMarkWidth = int(markConfig.get("markParams", "maxMarkWidth", fallback=7))
        _mark.changeMarkWidthProb = float(markConfig.get("markParams", "changeMarkWidthProb", fallback=".02"))
        _mark.mode = int(markConfig.get("markParams", "mode", fallback=1))

        _mark.forceOrientation = markConfig.get("markParams", "forceOrientation", fallback="vertical")
        _mark.forcedPalette = markConfig.get("markParams", "forcedPalette", fallback=None)
        if _mark.forcedPalette is not None:
            _mark.forcedPalette = list(map(lambda x: float(x), markConfig.get("markParams", "forcedPalette", fallback=None).split(",")))

        _mark.angleDiffMax = float(markConfig.get("markParams", "angleDiffMax", fallback=180))
        _mark.drawingSkip = float(markConfig.get("markParams", "drawingSkip", fallback=0.01))

        _mark.drawLineAsEnvelope = markConfig.getboolean("markParams", "drawLineAsEnvelope", fallback=config.drawLineAsEnvelope)

        return _mark

    _marksPath = _load_pen_config_globals(config)

    for _penConfigName in config.penNames:
        _mark = _load_single_pen(_penConfigName)
        config.marksPalette.append(_mark)
    # print(config.marksPalette)


def _load_and_initialize_system(config):
    """Initializes the system and related parameters."""
    """Loads rendering-related configuration parameters."""

    config.changeBGColorProb = float(workConfig.get("drawingField", "changeBGColorProb", fallback=0.001))
    config.totalResetTime = workConfig.getint("drawingField", "totalResetTime", fallback=33)
    config.totalResetTimeMaxMultiplier = float(workConfig.get("drawingField", "totalResetTimeMaxMultiplier", fallback=1.0))
    config.changeDrawingModeTime = float(workConfig.get("drawingField", "changeDrawingModeTime", fallback=100.0))
    config.jitterIterationsMin = workConfig.getint("drawingField", "jitterIterationsMin", fallback=1)
    config.jitterIterationsMax = workConfig.getint("drawingField", "jitterIterationsMax", fallback=10)
    config.jitterIterationsHoriz = workConfig.getint("drawingField", "jitterIterationsHoriz", fallback=2)
    config.jitterIterationsVert = workConfig.getint("drawingField", "jitterIterationsVert", fallback=2)
    config.alwaysJitterLineAfterDrawn = workConfig.getboolean("drawingField", "alwaysJitterLineAfterDrawn", fallback=False)

    config.doJitterWhenAddingBG = workConfig.getboolean("drawingField", "doJitterWhenAddingBG", fallback=True)
    config.blendLevelRateBase = float(workConfig.get("drawingField", "blendLevelRateBase", fallback=0.01))
    config.totalRandomPenColorProb = float(workConfig.get("drawingField", "totalRandomPenColorProb", fallback=0.0))
    config.totalRandomBGBoxColorProb = float(workConfig.get("drawingField", "totalRandomBGBoxColorProb", fallback=0.0))
    config.debugMode = workConfig.getboolean("drawingField", "debugMode", fallback=False)

    config.changeColorSetTime = float(workConfig.get("drawingField", "changeColorSetTime", fallback=0))
    config.changeColorSetTimeMaxMultiplier = float(workConfig.get("drawingField", "changeColorSetTimeMaxMultiplier", fallback=1))

    config.justHitPauseProb = float(workConfig.get("drawingField", "justHitPauseProb", fallback=0.0))
    config.releaseFromJustHitPauseProb = float(workConfig.get("drawingField", "releaseFromJustHitPauseProb", fallback=1.0))
    config.justHitPause = False

    if config.changeColorSetTime > 0:
        config.paletteController = Director(config)
        config.paletteController.slotRate = config.changeColorSetTime
        config.changeColorSetTimeToUse = config.changeColorSetTime

    if config.changeDrawingModeTime > 0:
        config.changeTimeController = Director(config)
        config.changeTimeController.slotRate = config.changeDrawingModeTime

    config.slotRate = float(workConfig.get("drawingField", "slotRate", fallback=0.03))
    config.redrawSpeed = float(workConfig.get("drawingField", "redrawSpeed", fallback=0.03))

    config.directorController = Director(config)
    config.directorController.slotRate = config.slotRate

    config.drawingController = Director(config)
    config.drawingController.slotRate = 10

    config.stateReportController = Director(config)
    config.stateReportController.slotRate = 25

    config.canDraw = True
    config.doingDrawing = False
    config.stoppedAndWaitingToDraw = False

    config.penArray = []
    config.drawingMode = 1

    initDrawings()
    config.blendLevel = 0.0
    config.blendLevelRate = 0.1
    config.fadeThruToNew = 255
    config.fadeThruToNewDone = True

    config.transitionStateHandler = TransitionStates(config)
    config.transitionStateHandler.sourceImage = config.finalCompositeLayer
    config.transitionStateHandler.targetImage = config.finalCompositeLayer
    config.inTransition = False

    # config.underLayerDraw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=(100, 0, 80, 100))
