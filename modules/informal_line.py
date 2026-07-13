from PIL import Image, ImageDraw, ImageChops
import random
import time
import math
from matplotlib.pyplot import pie
import numpy as np
from modules.configuration import pieceLogger


class InformalLine:

    points = 1
    pointPerLine = 3
    resolution = 50
    drawingHeight = 100
    xOffset = 100
    yOffset = 0

    configxOffset = 0
    configyOffset = 0
    angle = 0
    direction = 0
    name = ""

    """
    lineType = 0 ==> straight lines
    lineType = 1 ==> scribble lines
    """
    lineType = 0

    attenuating = False
    enlarging = False

    lineSpeedRange = []
    lineSpeed = 1
    speed = 1

    baseWidthRange = []
    baseWidth = 100

    noiseAmplitudeRange = []
    noiseAmplitude = 1.0

    ratioFactorRange = []
    backTrackRange = []
    largestDim = 0
    curveResolution = 1.0
    tangleProb = 0.0
    lineColorIsBgColor = False

    horizontalMovementProb = 0.0
    veticalMovementProb = 0.0

    bgColor = (0, 0, 0, 255)
    lineColor = (0, 0, 0, 255)

    # -----  CURVES ----- #
    turnsRange = [2, 2]
    loopsMin = 2
    loopsMax = 2
    loops = 2
    speed = 1
    loopDirection = 1

    pointsPerLoop = 8
    points = 8
    noiseX = 1
    noiseY = 1

    scribbleHeight = 50
    radiusX = 50
    radiusY = 50
    radiusXMin = 50
    radiusXMax = 50
    radiusYMin = 50
    radiusYMax = 50
    xRadiusDelta = 0
    yRadiusDelta = 0
    deltaRadiusXChangeProb = 0.0
    deltaRadiusYChangeProb = 0.0

    xCenter = 100
    yCenter = 100
    centerXDelta = 0
    centerYDelta = 0
    deltaRadiusXCenterChangeProb = 0.0
    deltaRadiusYCenterChangeProb = 0.0

    def __init__(self, _unitNumber=0, _config=None):
        self.unitNumber = _unitNumber
        self.config = _config

    # --------------- UTILS ------------------------ #
    def randomRange(self, a, b, rounded=False):
        if not rounded:
            return random.uniform(a, b)
        else:
            return round(random.uniform(a, b))

    def catmull_rom(self, p0, p1, p2, p3, t):
        t2 = t * t
        t3 = t2 * t
        return 0.5 * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3)

    def chaikins_corner_cutting(self, coords, refinements=2, ratio=0.75):
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

    # ---------------------------------------------- #

    # --------------- curves ----------------------- #

    def get_curve_points(self, points, curve_drawn=True, resolution=50):

        if not curve_drawn or len(points) < 2:
            return []

        self.curve_points = []
        n = len(points)

        for i in range(n - 1):
            p0 = points[max(0, i - 1)]
            p1 = points[i]
            p2 = points[i + 1]
            p3 = points[min(n - 1, i + 2)]

            for step in range(resolution):
                t = step / float(resolution)  # 0 <= t < 1

                x = self.catmull_rom(p0[0], p1[0], p2[0], p3[0], t)
                y = self.catmull_rom(p0[1], p1[1], p2[1], p3[1], t)

                self.curve_points.append((x, y))

    def generateScribble(self):
        points = self.generate_loop_stroke()
        self.get_curve_points(points, True, 10)

        self.smooth_points = []
        self.smooth_points.extend([pt[0] + self.xOffset, pt[1] + self.yOffset] for pt in self.curve_points)

        if random.random() < 0.5:
            self.smooth_points.reverse()

        self.curvedPoints = []
        self.curvedPoints.extend([pt[0] + self.xOffset, pt[1] + self.yOffset] for pt in self.curve_points)

        if random.random() < 0.5:
            self.curvedPoints.reverse()

    def generateCurve(self):
        width = self.drawingSize[0]
        height = self.drawingSize[1]
        num_points = self.num_points

        # Generate initial points in a circle
        base_radius = min(width, height) // self.baseRadiusFactor
        # Generate random points around a circle
        angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
        points = [self.lastPoint]
        points = []

        # center_x = width // 2  # + self.xOffset  # + round(centerVariationX - random.random() * centerVariationX * 2)
        # center_y = height // 2  # + self.yOffset  # + round(centerVariationY - random.random() * centerVariationY * 2)
        center_x = 0
        center_y = 0

        # pieceLogger(f"Making curve self.xOffset {self.xOffset} self.yOffset {self.yOffset}")

        _xTravel = random.uniform(self.xTravelRange[0], self.xTravelRange[1])
        _yTravel = random.uniform(self.yTravelRange[0], self.yTravelRange[1])

        _xTravelIncr = random.uniform(self.xTravelIncr[0], self.xTravelIncr[1])
        _yTravelIncr = random.uniform(self.yTravelIncr[0], self.yTravelIncr[1])

        for _ in range(self.turns):
            for angle in angles:
                # Add random variation to the radius
                radius_x = base_radius * self.xRadiusFactor + (self.xRadiusFactorNoiseFactor - 2 * self.xRadiusFactorNoiseFactor * (random.random()))
                radius_y = base_radius * self.yRadiusFactor + (self.yRadiusFactorNoiseFactor - 2 * self.yRadiusFactorNoiseFactor * (random.random()))
                x = center_x + radius_x * np.cos(angle)
                y = center_y + radius_y * np.sin(angle)

                if random.random() < 0.1:
                    x += self.xRandom
                if random.random() < 0.1:
                    y += self.yRandom
                base_radius += random.uniform(-5, 5)

                base_radius += self.radiusChangePerRound

                points.append([x, y])

                if self.xtravelMode == 1:
                    center_x += _xTravel
                    _xTravel *= _xTravelIncr
                else:
                    center_x += random.uniform(self.xTravelRange[0], self.xTravelRange[1])

                if self.ytravelMode == 1:
                    center_y += _yTravel
                    _yTravel *= _yTravelIncr
                else:
                    center_y += random.uniform(self.yTravelRange[0], self.yTravelRange[1])
            self.lastPoint = [x, y]

        # Close the shape by repeating the first point
        points.append(points[0])
        # smoothLine(points, )

        self.smooth_points = []
        self.curvedPoints = []
        res = self.chaikins_corner_cutting(points, 2).tolist()
        self.smooth_points.extend((pt[0] + self.xOffset, pt[1] + self.yOffset) for pt in res)
        self.curvedPoints.extend((pt[0] + self.xOffset, pt[1] + self.yOffset) for pt in res)
        # either clockwise or counter

        if random.random() < 0.5:
            self.smooth_points.reverse()
            self.curvedPoints.reverse()

    def generate_loop_stroke(self):

        pts = []
        _radiusX = self.radiusX
        _radiusY = self.radiusY
        deltaRadiusX = self.randomRange(-self.xRadiusDelta, self.xRadiusDelta)
        deltaRadiusY = self.randomRange(-self.yRadiusDelta, self.yRadiusDelta)

        deltaRadiusXCenter = self.randomRange(-self.centerXDelta, self.centerXDelta)
        deltaRadiusYCenter = self.randomRange(-self.centerYDelta, self.centerYDelta)

        _xCenter = 0
        _yCenter = 0
        _initAng = random.uniform(0, math.pi)

        points = self.points

        # pieceLogger(f"deltaRadiusX {round(deltaRadiusX,4)}")
        # pieceLogger(f"deltaRadiusY {round(deltaRadiusY,4)}")
        # pieceLogger(f"deltaRadiusXCenter {round(deltaRadiusXCenter,4)}")
        # pieceLogger(f"deltaRadiusYCenter {round(deltaRadiusYCenter,4)}")
        # pieceLogger(f"self.loops {self.loops}")
        # pieceLogger(f"points {points}")
        # pieceLogger(f"self.speed {self.speed}")
        # pieceLogger(f"self.xOffset {self.xOffset}")
        # self.speed = 8

        for i in range(points):
            t = i / (points - 1)
            ang = self.loopDirection * t * math.pi * 2 * self.loops
            x = _xCenter + math.sin(_initAng + ang) * _radiusX + self.randomRange(-self.noiseX, self.noiseX)
            y = _yCenter - math.cos(_initAng + ang) * _radiusY - t * self.scribbleHeight + self.randomRange(-self.noiseY, self.noiseY)

            _radiusX += deltaRadiusX
            _radiusY += deltaRadiusY

            _xCenter += deltaRadiusXCenter
            _yCenter += deltaRadiusYCenter

            if self.randomRange(0, 1.0) < self.deltaRadiusXChangeProb:
                deltaRadiusX = self.randomRange(-self.xRadiusDelta, self.xRadiusDelta)

            if self.randomRange(0, 1.0) < self.deltaRadiusYChangeProb:
                deltaRadiusY = self.randomRange(-self.yRadiusDelta, self.yRadiusDelta)

            if self.randomRange(0, 1.0) < self.deltaRadiusXCenterChangeProb:
                deltaRadiusXCenter = self.randomRange(-self.centerXDelta, self.centerXDelta)

            if self.randomRange(0, 1.0) < self.deltaRadiusYCenterChangeProb:
                deltaRadiusYCenter = self.randomRange(-self.centerYDelta, self.centerYDelta)

            pts.append((x, y))

        # Extra points for smoother Bézier start/end
        pts.insert(0, pts[0])
        pts.append(pts[-1])
        pts.append(pts[-1])

        return pts

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

    # ---------------------------------------------- #

    def generateRawLine(self):
        self.rawPts = []
        rawPts = []
        pointSpacing = self.drawingHeight / self.points

        for i in range(self.points):
            a = i * pointSpacing
            b = self.randomRange(-self.noiseAmplitude, self.noiseAmplitude)
            if random.random() < self.tangleProb and i != 0 and i != self.points - 1 and abs(b) > self.noiseAmplitude * 0.75:
                a -= random.uniform(self.backTrackRange[0], self.backTrackRange[1])
            rawPts.append((round(b), round(a)))

        # ensures the last point at the right or bottom closes the box
        # rawPts.append([b + self.xOffset, self.drawingHeight + self.yOffset])
        # Extra points for smoother Bézier start/end
        # pts.insert(0, pts[0])

        # rotate the points
        theta = self.angle * math.pi / 180
        # theta = (self.angle - 2 * self.angle  * random.random())* math.pi/180
        for pt in rawPts:
            _x = pt[0] * math.cos(theta) - pt[1] * math.sin(theta)
            _y = pt[0] * math.sin(theta) + pt[1] * math.cos(theta)
            self.rawPts.append((_x + self.xOffset, _y + self.yOffset))
        self.rawPts.append([_x + self.xOffset, _y + self.yOffset])

    def generateInformalLine(self):

        self.points = random.randint(3, self.pointPerLine)
        self.ratioFactor = random.uniform(self.ratioFactorRange[0], self.ratioFactorRange[1])
        self.resolution = self.curveResolution
        self.direction = 1 if random.random() < 0.5 else 0

        self.generateRawLine()
        self.getCurvePoints()
        self.smoothPointsForDrawing = []
        self.smoothPointsForDrawing.extend([pt[0] + self.configxOffset, pt[1] + self.configyOffset] for pt in self.curvedPoints)
        # pieceLogger(f"Made line {self.xOffset}  {self.yOffset} {self.drawingHeight}")
        # pieceLogger(f"[generateInformalLine] {self.curvedPoints}")

    def drawLinePoints(self):

        self.lastOrthoPoint = []
        pointsToDraw = self.curvedPoints
        lastPt = [pointsToDraw[0][0], pointsToDraw[0][1]]

        # self.draw.rectangle((0, 0, self.largestDim, self.largestDim), fill=(0, 0, 0, 0))
        # self.draw.rectangle((0, 0, self.largestDim, self.largestDim), fill=(255, 0, 0, 100))

        _ptCounter = 0
        for pt in pointsToDraw:
            self.drawTheLine(lastPt[0], lastPt[1], pt[0], pt[1], _ptCounter)
            lastPt = [pt[0], pt[1]]
            _ptCounter += 1

        _ptCounter = 0
        self.smooth_points = pointsToDraw

        for pt in pointsToDraw:
            self._p = _ptCounter

            _ptCounter += 1

        for _ in range(self.lineSpeed):
            _lstpt = pointsToDraw[len(pointsToDraw) - 1][0]
            _lstpt2 = pointsToDraw[len(pointsToDraw) - 1][1]
            for pt in range(len(pointsToDraw) - 1, 0, -1):
                pointsToDraw[pt][0] = pointsToDraw[pt - 1][0]
                pointsToDraw[pt][1] = pointsToDraw[pt - 1][1]
            pointsToDraw[pt + 1][0] = _lstpt
            pointsToDraw[pt + 1][1] = _lstpt2

    # ---------------------------------------------- #

    def drawTheLineComplete(self):
        pointsToDraw = self.curvedPoints
        fillClr = self.lineColor
        _ptCount = 0
        _p1 = [pointsToDraw[0][0], pointsToDraw[0][1]]
        _p2 = [pointsToDraw[1][0], pointsToDraw[1][1]]

        for pt in pointsToDraw:
            if _ptCount < len(pointsToDraw) - 1:
                self.draw.line([_p1[0], _p1[1], _p2[0], _p2[1]], fill=tuple(fillClr), width=round(self.baseWidth))
                _ptCount += 1
                _p1 = [pointsToDraw[_ptCount - 1][0], pointsToDraw[_ptCount - 1][1]]
                _p2 = [pointsToDraw[_ptCount][0], pointsToDraw[_ptCount][1]]

    def drawTheLine(self, p1x, p1y, p2x, p2y, _n):

        _p1 = [p1x, p1y]
        _p2 = [p2x, p2y]

        _ratio = 1.0
        _ratio1a = 1.0

        Width = self.baseWidth * _ratio * _ratio1a

        fillClr = self.lineColor
        if self.lineColorIsBgColor:
            fillClr = self.bgColor

        self.draw.line([_p1[0], _p1[1], _p2[0], _p2[1]], fill=tuple(fillClr), width=round(self.baseWidth))

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

            self.config.draw.polygon(_poly, fill=_lineColor, outline=None)

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

    # ---------------------------------------------- #
    def reconfigure(self):
        self.lineSpeed = random.randint(self.lineSpeedRange[0], self.lineSpeedRange[1])
        self.baseWidth = random.uniform(self.baseWidthRange[0], self.baseWidthRange[1])
        self.noiseAmplitude = random.uniform(float(self.noiseAmplitudeRange[0]), float(self.noiseAmplitudeRange[1]))


"""
 
_mark.turnsRange = list(map(lambda x: int(x), markConfig.get("markParams", "turnsRange", fallback="2,2").split(",")))
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
 

self.turnsRange = [2,2]
self.loopsMin = 2
self.loopsMax = 2

self.pointsPerLoop = 8
self.noiseX = 1
self.noiseY = 1

self.height = 50
self.radiusX = 50
self.radiusY = 50
self.radiusXMin = 50
self.radiusXMax = 50
self.radiusYMin = 50
self.radiusYMax = 50
self.xRadiusDelta = 2
self.yRadiusDelta = 2
self.deltaRadiusXChangeProb = .5
self.deltaRadiusYChangeProb = .5

self.xCenter = 100
self.yCenter = 100
self.centerXDelta = 2
self.centerYDelta = 2
self.deltaRadiusXCenterChangeProb = .5
self.deltaRadiusYCenterChangeProb = .5

"""
