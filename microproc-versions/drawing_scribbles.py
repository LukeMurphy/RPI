import time
import random
import math

from interstate75 import Interstate75, DISPLAY_INTERSTATE75_64X64

# ----------------------------------------------------##----------------------------------------------------#
INTERVAL = 0.02
PWIDTH = 64
PHEIGHT = 64
NUMSQRS = 19

bgColorSets = [(159 / 360, 190 / 360, 0.70, 0.92, 0.45, 0.7, 0, 0), 
               (159 / 360, 190 / 360, 0.80, 0.92, 0.45, 0.7, 0, 0)]
bgBoxColorSets = [(12 / 360, 27 / 360, 0.77, 0.97, 0.35, 0.77, 0, 0), 
                  (215 / 360, 218 / 360, 0.77, 0.97, 0.35, 0.87, 0, 0), 
                  (159 / 360, 190 / 360, 0.70, 0.92, 0.45, 0.7, 0, 0),
                  (159 / 360, 190 / 360, 0.70, 0.92, 0.45, 0.7, 0, 0), 
               (159 / 360, 190 / 360, 0.80, 0.92, 0.45, 0.7, 0, 0)]
penColorSets = [
    (28 / 360, 30 / 360, 0.5, 0.99, 0.95, 0.99, 0, 0),
    (18 / 360, 20 / 360, 0.65, 0.650, 0.93, 0.99, 0, 0),
    (10 / 360, 18 / 360, 0.5, 0.50, 0.95, 0.99, 0, 0),
    (10 / 360, 18 / 360, 0.25, 0.350, 0.95, 0.99, 0, 0),
    (10 / 360, 20 / 360, 0.5, 0.750, 0.25, 0.49, 0, 0),
]


shapes = []

# Setup for the display
i75 = Interstate75(display=DISPLAY_INTERSTATE75_64X64)
display = i75.display


class PenMark:
    def __init__(self):
        pass


class Config:
    def __init__(self):
        self.doingDrawing = False


class ColorObj:
    def __init__(self):
        self.h = 0
        self.s = 0
        self.v = 0
        self.dh = 0
        self.ds = 0
        self.dv = 0
        self.newh = 0
        self.news = 0
        self.newv = 0
        self.speedFactor = 200

    def change(self):
        self.dh = (self.newh - self.h) / self.speedFactor
        self.ds = (self.news - self.s) / self.speedFactor
        self.dv = (self.newv - self.v) / self.speedFactor

    def clrStep(self):
        self.h += self.dh
        self.s += self.ds
        self.v += self.dv

        if round(self.h * 10) == round(self.newh * 10):
            self.dh = 0
        if round(self.s * 10) == round(self.news * 10):
            self.ds = 0
        if round(self.v * 10) == round(self.newv * 10):
            self.dv = 0


class Point:
    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y
        self.newX = _x
        self.newY = _y
        self.dx = 0
        self.dy = 0
        self.xSpeed = 0
        self.ySpeed = 0
        self.speedFactor = 12
        self.pt = [self.x, self.y]

    def change(self):
        self.dx = self.newX - self.x
        self.dy = self.newY - self.y

        self.xSpeed = self.dx / self.speedFactor
        self.ySpeed = self.dy / self.speedFactor

    def pointStep(self):
        self.x = round(self.x + self.xSpeed)
        self.y = round(self.y + self.ySpeed)

        if self.x == self.newX:
            self.dx = 0
            self.xSpeed = 0

        if self.y == self.newY:
            self.dy = 0
            self.ySpeed = 0

        self.pt = [self.x, self.y]


class AbsShape:
    inColorTrans = False
    inShapeTrans = False
    dx = 8
    dy = 8
    initP1 = Point(15, 64)
    initP2 = Point(15, 12)
    initP3 = Point(50, 12)
    initP4 = Point(50, 64)

    def __init__(self):
        pass

    def setup(self):
        self.p1 = self.initP1
        self.p2 = self.initP2
        self.p3 = self.initP3
        self.p4 = self.initP4

    def update(self):
        if random.random() < 0.25:
            self.p1.newX = self.p1.pt[0] + round(random.uniform(-self.dx, self.dx))
            self.p1.newY = self.p1.pt[1]
            self.p1.change()

        if random.random() < 0.25:
            self.p2.newX = self.p2.pt[0] + round(random.uniform(-self.dx, self.dx))
            self.p2.newY = self.p2.pt[1] + round(random.uniform(-self.dy, self.dy))
            self.p2.change()

        if random.random() < 0.25:
            self.p3.newX = self.p3.pt[0] + round(random.uniform(-self.dx, self.dx))
            self.p3.newY = self.p3.pt[1] + round(random.uniform(-self.dy, self.dy))
            self.p3.change()

        if random.random() < 0.25:
            self.p4.newX = self.p4.pt[0] + round(random.uniform(-self.dx, self.dx))
            self.p4.newY = self.p4.pt[1]
            self.p4.change()

        if random.random() < 0.01:
            self.p1.newX = self.initP1.pt[0]
            self.p1.newY = self.initP1.pt[1]
            self.p1.change()
        if random.random() < 0.01:
            self.p2.newX = self.initP2.pt[0]
            self.p2.newY = self.initP2.pt[1]
            self.p2.change()
        if random.random() < 0.01:
            self.p3.newX = self.initP3.pt[0]
            self.p3.newY = self.initP3.pt[1]
            self.p3.change()
        if random.random() < 0.01:
            self.p4.newX = self.initP4.pt[0]
            self.p4.newY = self.initP4.pt[1]
            self.p4.change()


def changeColor(clrRef, hmin, hmax, smin, smax, vmin, vmax, init=False):
    if init:
        clrRef.h = random.uniform(hmin, hmax)
        clrRef.s = random.uniform(smin, smax)
        clrRef.v = random.uniform(vmin, vmax)
    else:
        clrRef.newh = random.uniform(hmin, hmax)
        clrRef.news = random.uniform(smin, smax)
        clrRef.newv = random.uniform(vmin, vmax)


def catmull_rom(p0, p1, p2, p3, t):
    t2 = t * t
    t3 = t2 * t

    return 0.5 * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3)


def R(a, b, rounded=False):
    if not rounded:
        return random.uniform(a, b)
    else:
        return round(random.uniform(a, b))


def generateScribble(_pen):
    points = generate_loop_stroke(_pen)
    _res = get_curve_points(points, True, 10)

    _pen.smooth_points = []
    _pen.smooth_points.extend((pt[0] + _pen.xOffset, pt[1] + _pen.yOffset) for pt in _res)

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

        pts.append((x, y))

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


def drawLinePolyEnvelope(_pen):
    for _ in range(_pen.speed):
        if _pen._p < len(_pen.smooth_points) and _pen._p > 0:
            _p1 = _pen.smooth_points[_pen._p - 1]
            _p2 = _pen.smooth_points[_pen._p]
            _dy = _p1[1] - _p2[1]
            _dx = _p1[0] - _p2[0]
            _angle = math.atan2(_dy, _dx) * 360 / math.pi

            if _angle < 0:
                _angle += 360

            _penWidth = _pen._w
            # _lineColor = _pen.lineColor
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

            last_ortho_point = getattr(_pen, "lastOrthoPoint", None)
            if _pen._p > 1 and last_ortho_point:
                _orthoP1x = last_ortho_point[0]
                _orthoP1y = last_ortho_point[1]

                _orthoP4x = last_ortho_point[2]
                _orthoP4y = last_ortho_point[3]

            _poly = [(_orthoP1x, _orthoP1y), (_orthoP2x, _orthoP2y), (_orthoP3x, _orthoP3y), (_orthoP4x, _orthoP4y), (_orthoP1x, _orthoP1y)]

            drawLineEnvelope(_poly)

            _pen.lastAngle = _angle
            _pen._p += 1
            _pen.lastOrthoPoint = [_orthoP2x, _orthoP2y, _orthoP3x, _orthoP3y]

            config.doingDrawing = True
        if _pen._p == len(_pen.smooth_points):
            _pen._p = 0
            # print("Drawing stopped.")

            time.sleep(random.uniform(0, 7))
            startUpNewLine()

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


def setShapes():
    global shapes
    for _shp in shapes:
        _wd = random.uniform(4, 43)
        _rx = random.uniform(0, PWIDTH - _wd)
        _ry = random.uniform(0, PHEIGHT - _wd)
        _shp.initP1 = Point(_rx, _ry)
        _shp.initP2 = Point(_rx, _ry + _wd)
        _shp.initP3 = Point(_rx + _wd, _ry + _wd)
        _shp.initP4 = Point(_rx + _wd, _ry)
        _shp.setup()


def drawLineEnvelope(_poly):
    global penG
    display.reset_pen(penG)
    if random.random() < .02 :
        setColor(penClr, penColorSets)
    penG = display.create_pen_hsv(penClr.h, penClr.s, penClr.v)
    display.set_pen(penG)
    display.polygon(_poly)


def startUpNewLine():
    global penMark
    penMark.loops = R(penMark.loopsMin, penMark.loopsMax, True)
    penMark.points = round(penMark.loops * penMark.pointsPerLoop)
    penMark.speed = round(random.uniform(penMark.penSpeedMinVal, penMark.penSpeedMaxVal))
    penMark._p = 1
    penMark._w = 0.5
    penMark.lastOrthoPoint = None
    penMark.enlarging = False
    penMark.attenuating = False
    penMark.loopDirection = -1
    if random.random() < 0.5:
        penMark.loopDirection = 1

    setColor(penClr, penColorSets)
    penG = display.create_pen_hsv(penClr.h, penClr.s, penClr.v)
    display.reset_pen(penG)

    generateScribble(penMark)


def drawBGPanelBlocks():
    global shapes
    for shp in shapes:
        drawBGPanelBlock(shp)


def drawBGPanelBlock(shp):
    global ForeG
    display.reset_pen(ForeG)
    display.set_pen(ForeG)
    if random.random() < .02 :
        setColor(fgClr, bgBoxColorSets)
    ForeG = display.create_pen_hsv(fgClr.h, fgClr.s, fgClr.v)
    shp.p1.pointStep()
    shp.p3.pointStep()
    shp.p2.pointStep()
    shp.p4.pointStep()

    display.polygon(
        [
            tuple(shp.p1.pt),
            tuple(shp.p2.pt),
            tuple(shp.p3.pt),
            tuple(shp.p4.pt),
        ]
    )


def setColor(_clrRef, _clrSetRef):
    _clrSet = _clrSetRef[round(random.uniform(0, len(_clrSetRef) - 1))]
    _clrRef.h = random.uniform(_clrSet[0], _clrSet[1])
    _clrRef.s = random.uniform(_clrSet[2], _clrSet[3])
    _clrRef.v = random.uniform(_clrSet[5], _clrSet[5])


# ----------------------------------------------------##----------------------------------------------------#
# SETUPS #

bgClr = ColorObj()
setColor(bgClr, bgColorSets)
Bg = display.create_pen_hsv(bgClr.h, bgClr.s, bgClr.v)

fgClr = ColorObj()
setColor(fgClr, bgBoxColorSets)
fgClr.change()
ForeG = display.create_pen_hsv(fgClr.h, fgClr.s, fgClr.v)

penClr = ColorObj()
setColor(penClr, penColorSets)
penG = display.create_pen_hsv(penClr.h, penClr.s, penClr.v)


for _ in range(NUMSQRS):
    _shp = AbsShape()
    shapes.append(_shp)

setShapes()

penMark = PenMark()
config = Config()

penMark.name = "scribbleLine1"
penMark.pointsPerLoop = 8
penMark.loopsMin = 3
penMark.loopsMax = 4

penMark.minMarkWidth = 1
penMark.maxMarkWidth = 5
penMark.changeMarkWidthProb = 0.03
penMark.incrementFactor = 1

penMark.height = 10
penMark.radiusX = 20
penMark.radiusY = 32
penMark.radiusXMin = 5
penMark.radiusXMax = 30
penMark.radiusYMin = 5
penMark.radiusYMax = 30
penMark.noiseX = 5
penMark.noiseY = 5
penMark.xRadiusDelta = 1
penMark.yRadiusDelta = 1
penMark.deltaRadiusXChangeProb = 0.02
penMark.deltaRadiusYChangeProb = 0.02

penMark.xCenter = 0
penMark.yCenter = 0
penMark.xOffset = 32
penMark.yOffset = 32
penMark.centerXDelta = 2
penMark.centerYDelta = 1
penMark.deltaRadiusXCenterChangeProb = 0.04
penMark.deltaRadiusYCenterChangeProb = 0.04
penMark.loops = R(penMark.loopsMin, penMark.loopsMax, True)
penMark.points = round(penMark.loops * penMark.pointsPerLoop)
penMark.penSpeedMinVal = 2
penMark.penSpeedMaxVal = 3


startUpNewLine()

display.set_pen(ForeG)
display.set_pen(penG)
display.set_pen(Bg)
display.clear()

generateScribble(penMark)
drawBGPanelBlocks()

panelBGBlockCount = 0

while True:
    if random.random() < 0.005:
        setColor(fgClr, bgBoxColorSets)
        ForeG = display.create_pen_hsv(fgClr.h, fgClr.s, fgClr.v)
        setShapes()
        display.reset_pen(ForeG)
        display.set_pen(ForeG)
        panelBGBlockCount = 1
        
    # this needs refinement b/c the bg can overpaint the line too often
    if panelBGBlockCount > 0:
        drawBGPanelBlock(shapes[panelBGBlockCount])
        panelBGBlockCount += 1
        if panelBGBlockCount >= NUMSQRS:
            panelBGBlockCount = 0

    display.reset_pen(penG)
    display.set_pen(penG)

    if panelBGBlockCount == 0:
        drawLinePolyEnvelope(penMark)

    # Update the display
    i75.update()
    time.sleep(INTERVAL)

