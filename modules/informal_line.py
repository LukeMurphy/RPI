from PIL import Image, ImageDraw, ImageChops
import random
import time
import math
from modules.configuration import bcolors, pieceLogger
from pieces.actionmarks_v2 import bgColorBlocksFilling

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

    lineSpeedRange = []
    baseWidthRange = []
    noiseAmplitudeRange = []
    ratioFactorRange = []
    backTrackRange = []
    largestDim = 0
    curveResolution = 1.0
    tangleProb = 0.0
    lineColorIsBgColor = False

    horizontalMovementProb = 0.0
    veticalMovementProb = 0.0

    bgColor = (0,0,0,255)



    def __init__(self, _unitNumber, _largestDim, _config=None):
        self.unitNumber = _unitNumber
        self.config = _config
        self.largestDim = _largestDim
        # self.lineColor = (0,0,0,255)
        # self.canvas = Image.new("RGBA", (self.largestDim, self.largestDim))
        # self.draw = ImageDraw.Draw(self.canvas)
        # self.draw = self.config.draw


    def reconfigure(self):
        self.lineSpeed = random.randint(self.lineSpeedRange[0], self.lineSpeedRange[1])
        self.baseWidth = random.uniform(self.baseWidthRange[0], self.baseWidthRange[1])
        self.noiseAmplitude = random.uniform(float(self.noiseAmplitudeRange[0]), float(self.noiseAmplitudeRange[1]))


    def catmull_rom(self, p0, p1, p2, p3, t):
        t2 = t * t
        t3 = t2 * t
        return 0.5 * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3)


    def randomRange(self, a, b, rounded=False):
        if not rounded:
            return random.uniform(a, b)
        else:
            return round(random.uniform(a, b))


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
        theta = self.angle * math.pi/180
        # theta = (self.angle - 2 * self.angle  * random.random())* math.pi/180
        for pt in rawPts:
            _x = pt[0] * math.cos(theta) - pt[1] * math.sin(theta)
            _y = pt[0] * math.sin(theta) + pt[1] * math.cos(theta)
            self.rawPts.append((_x + self.xOffset,_y + self.yOffset))
        self.rawPts.append([_x + self.xOffset, _y + self.yOffset])


    def generateInformalLine(self):

        self.points = random.randint(3, self.pointPerLine)
        self.ratioFactor = random.uniform(self.ratioFactorRange[0], self.ratioFactorRange[1])
        self.resolution = self.curveResolution
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

        # self.draw.rectangle((0, 0, self.largestDim, self.largestDim), fill=(0, 0, 0, 0))
        # self.draw.rectangle((0, 0, self.largestDim, self.largestDim), fill=(255, 0, 0, 100))

        _ptCounter = 0
        for pt in pointsToDraw:
            self.drawTheLine(lastPt[0], lastPt[1], pt[0], pt[1], _ptCounter)
            lastPt = [pt[0], pt[1]]
            _ptCounter += 1

        _ptCounter = 0
        self.smooth_points = pointsToDraw
        # self._w = 1
        # self.maxMarkWidth = 8
        # self.minMarkWidth = 1
        # self.changeMarkWidthProb = .3
        # self.incrementFactor = .710
        for pt in pointsToDraw:
            self._p = _ptCounter
            # self.drawLinePolyEnvelope()
            _ptCounter += 1

        for _ in range(self.lineSpeed):
            _lstpt = pointsToDraw[len(pointsToDraw) - 1][0]
            _lstpt2 = pointsToDraw[len(pointsToDraw) - 1][1]
            for pt in range(len(pointsToDraw) - 1, 0, -1):
                pointsToDraw[pt][0] = pointsToDraw[pt - 1][0]
                pointsToDraw[pt][1] = pointsToDraw[pt - 1][1]
            pointsToDraw[pt + 1][0] = _lstpt
            pointsToDraw[pt + 1][1] = _lstpt2

        # if (self.angle != 0 and random.random() < self.horizontalMovementProb) or (self.angle == 0 and random.random() < self.verticalMovementProb):
        #     if self.direction == 0:
        #         for _ in range(self.lineSpeed):
        #             _lstpt = pointsToDraw[0][0]
        #             for pt in range(0, len(pointsToDraw) - 1):
        #                 pointsToDraw[pt][0] = pointsToDraw[pt + 1][0]
        #             pointsToDraw[pt + 1][0] = _lstpt
        #     else:
        #         for _ in range(self.lineSpeed):
        #             _lstpt = pointsToDraw[len(pointsToDraw) - 1][0]
        #             for pt in range(len(pointsToDraw) - 1, 0, -1):
        #                 pointsToDraw[pt][0] = pointsToDraw[pt - 1][0]
        #             pointsToDraw[pt + 1][0] = _lstpt


    def drawTheLine(self, p1x, p1y, p2x, p2y, _n):

        _p1 = [p1x, p1y]
        _p2 = [p2x, p2y]

        _ratio = 1.0
        _ratio1a = 1.0

        _penWidth = self.baseWidth * _ratio * _ratio1a

        fillClr = self.lineColor
        if self.lineColorIsBgColor:
            fillClr = self.bgColor

        # pieceLogger(f"{_p1} --> {_p2}")
        # pieceLogger(fillClr)

        if self.angle == 90:
            self.draw.line([_p1[1], _p1[0], _p2[1], _p2[0]], fill=tuple(fillClr), width=round(self.baseWidth))
        else:
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

