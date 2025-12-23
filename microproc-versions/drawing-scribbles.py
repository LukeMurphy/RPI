""" """

import time
import os
import random
import math

"""
"""
import pngdec
from interstate75 import Interstate75, DISPLAY_INTERSTATE75_64X64

# ----------------------------------------------------##----------------------------------------------------#


class Palette:
    def __init__(self):
        pass


class Pen:
    def __init__(self):
        pass


class Config:
    def __init__(self):
        pass


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
        self.h = self.h + self.dh
        self.s = self.s + self.ds
        self.v = self.v + self.dv

        if round(self.h * 10) == round(self.newh * 10):
            self.dh = 0
        if round(self.s * 10) == round(self.news * 10):
            self.ds = 0
        if round(self.v * 10) == round(self.newv * 10):
            self.dv = 0


class Point:

    x = 0
    y = 0
    dx = 0
    dy = 0
    newX = 0
    newY = 0
    diffX = 0
    diffY = 0
    xSpeed = 0
    ySpeed = 0
    pt = []
    speedFactor = 12

    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y
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
        self.p1 = self.initP1
        self.p2 = self.initP2
        self.p3 = self.initP3
        self.p4 = self.initP4
        pass

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
    # Draw the shape
    # print(f"should be drawing {_pen} {_pen.speed} {_pen.points}")
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

            _poly = [(_orthoP1x, _orthoP1y), (_orthoP2x, _orthoP2y), (_orthoP3x, _orthoP3y), (_orthoP4x, _orthoP4y), (_orthoP1x, _orthoP1y)]

            drawPolygon(_poly)

            # if random.random() < config.activePalette.dripProbablility:
            #     _wide = round(random.uniform(0, config.activePalette.dripWidthMax))
            #     _speed = round(random.uniform(config.activePalette.dripSpeedMin, config.activePalette.dripSpeedMax))
            #     _long = round(random.uniform(2, config.activePalette.dripLengthMax) / _speed)
            #     # config.draw.rectangle((_p1[0],_p1[1],_p1[0]+_wide,_p1[1]+_long), fill=_lineColor)
            #     _drip = [_p1, _long, _wide, _lineColor, False, _speed, 0]
            #     config.dripsArray.append(_drip)

            # if not _markDrawn :
            _pen.lastAngle = _angle
            _pen._p += 1
            _pen.lastOrthoPoint = [_orthoP2x, _orthoP2y, _orthoP3x, _orthoP3y]

            config.doingDrawing = True
        if _pen._p == len(_pen.smooth_points):
            _pen._p = 0
            print("Drawing stopped.")
            startNew()

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


# Time to pause between frames
INTERVAL = 0.02

# Setup for the display
i75 = Interstate75(display=DISPLAY_INTERSTATE75_64X64)
display = i75.display

WIDTH = i75.width
HEIGHT = i75.height

x = 10
y = 10

bgClr = ColorObj()
changeColor(bgClr, 45 / 360, 45 / 360, 1.0, 1.0, 0.35, 0.35, True)
Bg = display.create_pen_hsv(bgClr.h, bgClr.s, bgClr.v)

fgClr = ColorObj()
changeColor(fgClr, 0 / 360, 360 / 360, 0.90, 1.0, 0.45, 0.5, True)
ForeG = display.create_pen_hsv(fgClr.h, fgClr.s, fgClr.v)

penClr = ColorObj()
changeColor(penClr, 0 / 360, 360 / 360, 0.90, 1.0, 0.45, 0.5, True)
penG = display.create_pen_hsv(penClr.h, penClr.s, penClr.v)
print(penClr.h, penClr.s, penClr.v)

display.set_pen(ForeG)
display.set_pen(penG)
display.set_pen(Bg)
display.clear()


shp = AbsShape()
_pen = Pen()
config = Config()

_pen.name = "scribbleLine1"
_pen.pointsPerLoop = 5
_pen.loopsMin = 3
_pen.loopsMax = 7
_pen.minMarkWidth = 1
_pen.maxMarkWidth = 5
_pen.changeMarkWidthProb = 0.05
_pen.incrementFactor = 1
_pen.height = 30
_pen.radiusX = 10
_pen.radiusY = 10
_pen.radiusXMin = 10
_pen.radiusXMax = 20
_pen.radiusYMin = 10
_pen.radiusYMax = 20
_pen.noiseX = 10
_pen.noiseY = 10
_pen.xRadiusDelta = 2
_pen.yRadiusDelta = 2
_pen.deltaRadiusXChangeProb = 0.2
_pen.deltaRadiusYChangeProb = 0.2
_pen.xCenter = 0
_pen.yCenter = 0
_pen.xOffset = 32
_pen.yOffset = 32
_pen.centerXDelta = 10
_pen.centerYDelta = 8
_pen.deltaRadiusXCenterChangeProb = 0.4
_pen.deltaRadiusYCenterChangeProb = 0.4
_pen.loops = R(_pen.loopsMin, _pen.loopsMax, True)
_pen.points = round(_pen.loops * _pen.pointsPerLoop)
_pen.penSpeedMinVal = 1
_pen.penSpeedMaxVal = 1
_pen.speed = round(random.uniform(_pen.penSpeedMinVal, _pen.penSpeedMaxVal))
_pen._p = 1
_pen._w = 2
_pen.enlarging = False
_pen.attenuating = False
_pen.lineColor = ""
_pen.loopDirection = -1
if random.random() < 0.5:
    _pen.loopDirection = 1

generateScribble(_pen)

def drawPolygon(_poly):
    global penG
    display.reset_pen(penG)
    penG = display.create_pen_hsv(penClr.h, penClr.s, penClr.v)
    display.set_pen(penG)
    display.polygon(_poly)

def startNew():
    _pen.loops = R(_pen.loopsMin, _pen.loopsMax, True)
    _pen.points = round(_pen.loops * _pen.pointsPerLoop)
    _pen.speed = round(random.uniform(_pen.penSpeedMinVal, _pen.penSpeedMaxVal))
    _pen._p = 1
    _pen._w = 2
    _pen.enlarging = False
    _pen.attenuating = False
    
    changeColor(penClr, 0 / 360, 360 / 360, 0.90, 1.0, 0.1, 0.15, True)
    print(penClr.h, penClr.s, penClr.v)
    penG = display.create_pen_hsv(penClr.h, penClr.s, penClr.v)
    display.reset_pen(penG)
    
    generateScribble(_pen)

display.set_pen(Bg)
display.clear()
while True:
    # display.set_pen(Bg)
    # display.clear()

    # Reset the pen so we can reuse it
    # display.reset_pen(ForeG)
    # display.set_pen(ForeG)

    # shp.p1.pointStep()
    # shp.p2.pointStep()
    # shp.p3.pointStep()
    # shp.p4.pointStep()
    #bgClr.clrStep()
    # fgClr.clrStep()

    #Bg = display.create_pen_hsv(bgClr.h, bgClr.s, bgClr.v)
    # ForeG = display.create_pen_hsv(fgClr.h, fgClr.s, fgClr.v)

    # display.polygon(
    #     [
    #         tuple(shp.p1.pt),
    #         tuple(shp.p2.pt),
    #         tuple(shp.p3.pt),
    #         tuple(shp.p4.pt),
    #     ]
    # )

    if random.random() < 0.002:
        bgClr.newh = random.uniform(0, 1.0)
        bgClr.news = random.uniform(0, 1.0)
        bgClr.newv = random.uniform(0.2, 0.50)
        bgClr.change()

    # if random.random() < 0.001:
    #     fgClr.newh = random.uniform(0, 1.0)
    #     fgClr.news = random.uniform(0.2, 1.0)
    #     fgClr.newv = random.uniform(0.2, 0.50)
    #     fgClr.change()

    display.reset_pen(penG)
    display.set_pen(penG)
    drawLinePolyEnvelope(_pen)

    if random.random() < 0.01:
        shp.update()

    # Update the display
    i75.update()
    time.sleep(INTERVAL)


