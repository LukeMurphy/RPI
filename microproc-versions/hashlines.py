import time
import os
import random
import gc
from interstate75 import Interstate75, DISPLAY_INTERSTATE75_64X64


class Config:
    def __init__(self):
        """
        Purpose: holds state
        """


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
        self.speedFactor = 12
        self.intransition = False

    def change(self):
        dh = self.newh - self.h

        if dh >= 0.5:
            dh *= -1

        self.dh = dh / self.speedFactor
        self.ds = (self.news - self.s) / self.speedFactor
        self.dv = (self.newv - self.v) / self.speedFactor
        self.intransition = True

    def clrStep(self):
        self.h = self.h + self.dh
        self.s = self.s + self.ds
        self.v = self.v + self.dv

        if self.h > 1.0:
            self.h = self.h - 1.0
        if self.h < 0.0:
            self.h = 1.0 + self.h

        if round(self.h * 10) == round(self.newh * 10):
            self.dh = 0
        if round(self.s * 10) == round(self.news * 10):
            self.ds = 0
        if round(self.v * 10) == round(self.newv * 10):
            self.dv = 0

        if self.dh == 0 and self.ds == 0 and self.dv == 0:
            self.intransition = False


def changeColor(clrRef, hmin, hmax, smin, smax, vmin, vmax, init=False):

    clr = rColor(hmin, hmax, smin, smax, vmin, vmax)
    if init:
        clrRef.h = clr[0]
        clrRef.s = clr[1]
        clrRef.v = clr[2]
    else:
        clrRef.newh = clr[0]
        clrRef.news = clr[1]
        clrRef.newv = clr[2]

    # print(f"Color change {_hmin} {hmax} ==> {clrRef.newh}")


def rColor(hmin, hmax, smin, smax, vmin, vmax):

    if hmin > hmax:
        _hmin = 0 - hmin
    else:
        _hmin = hmin

    _h = random.uniform(_hmin, hmax)
    if _h < 0:
        _h += 1.0
    _s = random.uniform(smin, smax)
    _v = random.uniform(vmin, vmax)

    return [_h, _s, _v]


def R(a, b, rounded=False):
    if not rounded:
        return random.uniform(a, b)
    else:
        return round(random.uniform(a, b))


def catmull_rom(p0, p1, p2, p3, t):
    t2 = t * t
    t3 = t2 * t

    return 0.5 * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3)


def generateRawLine(points=20, horiz=True):
    pts = []
    if horiz:
        pointSpacing = (config.canvasWidth - 1 * config.xOffset) / points
    else:
        pointSpacing = (config.canvasHeight - 1 * config.yOffset) / points

    for i in range(points):
        a = i * pointSpacing
        b = R(-config.noiseAmplitude, config.noiseAmplitude)
        if horiz:
            pts.append((round(a), round(b)))
        else:
            pts.append((round(b), round(a)))

    # ensures the last point at the right or bottom closes the box
    if horiz:
        pts.append([config.canvasWidth - 2 * config.xOffset, b])
    else:
        pts.append([b, config.canvasHeight - 2 * config.yOffset])
    # Extra points for smoother Bézier start/end
    # pts.insert(0, pts[0])
    return pts


def getCurvePoints(points, resolution=50):

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


def generateInformalLine(pts=20, xOffset=0, yOffset=0, horiz=True):
    points = generateRawLine(pts, horiz)
    _curvedPoints = getCurvePoints(points, config.curveResolution)
    _smoothPointsForDrawing = []
    _smoothPointsForDrawing.extend((pt[0] + xOffset, pt[1] + yOffset) for pt in _curvedPoints)
    return _smoothPointsForDrawing


def getColor(r, g, b, a):
    clr = list(round(i * config.brightness) for i in [r, g, b])
    clr.append(a)
    return tuple(clr)


def hashlines2():
    global config
    _lineWidth = 1
    _ptCount = 0
    for h_pts in config.h_pts:
        if random.random() < config.horizLineChange:
            h_pts = generateInformalLine(config.pointsPerLine, config.xOffset, config.yOffset + config.rowSpacing * _ptCount, True)
            config.h_pts[_ptCount] = h_pts
        lastPt = [h_pts[0][0], h_pts[0][1]]
        for pt in h_pts:
            drawTheLine(lastPt[0], lastPt[1], pt[0], pt[1], _lineWidth)
            lastPt = [pt[0], pt[1]]
        _ptCount += 1

    _ptCount = 0
    for v_pts in config.v_pts:
        if random.random() < config.vertLineChange:
            v_pts = generateInformalLine(config.pointsPerLine, config.xOffset + config.colSpacing * _ptCount, config.yOffset, False)
            config.v_pts[_ptCount] = v_pts
        lastPt = [v_pts[0][0], v_pts[0][1]]
        for pt in v_pts:
            drawTheLine(lastPt[0], lastPt[1], pt[0], pt[1], _lineWidth)
            lastPt = [pt[0], pt[1]]
        _ptCount += 1

    # config.scroll += config.scrollRate


def drawTheLine(p1x, p1y, p2x, p2y, _lineWidth):
    display.line(round(p1x), round(p1y), round(p2x), round(p2y), _lineWidth)


def setLineColor():
    global ForeG
    _minVal = 0.0
    _maxVal = 0.04
    if config.lightMode:
        _minVal = 0.65
        _maxVal = 1.0
    changeColor(config.fgClr, config.line_minHue / 360, config.line_maxHue / 360, config.line_minSaturation, config.line_maxSaturation, _minVal, _maxVal, False)
    ForeG = display.create_pen_hsv(config.fgClr.h, config.fgClr.s, config.fgClr.v)
    config.fgClr.change()


def setBGColor():
    global Bg
    _minVal = 0.5
    _maxVal = 0.990
    if config.lightMode:
        _minVal = 0.0
        _maxVal = 0.1
    changeColor(config.bgClr, config.bg_minHue / 360, config.bg_maxHue / 360, config.bg_minSaturation, config.bg_maxSaturation, _minVal, _maxVal, False)
    Bg = display.create_pen_hsv(config.bgClr.h, config.bgClr.s, config.bgClr.v)
    config.bgClr.change()



def resetLines():
    global config

    config.colInterval = random.randint(int(config.rowAndColIntervalRange[0]), int(config.rowAndColIntervalRange[1]))
    config.rowInterval = random.randint(int(config.rowAndColIntervalRange[0]), int(config.rowAndColIntervalRange[1]))
    config.noiseAmplitude = random.uniform(float(config.noiseAmplitudeRange[0]), float(config.noiseAmplitudeRange[1]))
    config.rowSpacing = (config.canvasHeight - 2 * config.yOffset + config.rowAdj) / config.rowInterval
    config.colSpacing = (config.canvasWidth - 2 * config.xOffset + config.colAdj) / config.colInterval

    config.h_pts = []
    for row in range(config.rowInterval + config.rowAdj):
        h_pts = generateInformalLine(config.pointsPerLine, config.xOffset, config.yOffset + config.rowSpacing * row, True)
        config.h_pts.append(h_pts)

    config.v_pts = []
    for col in range(config.colInterval + config.colAdj):
        v_pts = generateInformalLine(config.pointsPerLine, config.xOffset + config.colSpacing * col, config.yOffset, False)
        config.v_pts.append(v_pts)


# ---------- SETTINGS ---------------#
# Setup for the display
i75 = Interstate75(display=DISPLAY_INTERSTATE75_64X64)
display = i75.display

config = Config()

def checkTime():
    hour  = time.localtime()[3]
    minute = time.localtime()[4]
    keepOn = False
    if hour >= 8 and hour <= 23 :
        keepOn = True
        
    return keepOn
        

    
BLANKSCREEN = display.create_pen_hsv(0,0,0)


# ---------------------------------#
# Framerate
config.interval = 0.03

config.pointsPerLine = 8
config.curveResolution = 5

config.xOffset = 4
config.colInterval = 10
config.colAdj = 1

config.yOffset = 4
config.rowInterval = 10
config.rowAdj = 1

config.vertLineChange = 0.002
config.horizLineChange = 0.002
config.changeLinesProb = 0.003
config.lightModeProb = 0.1
config.changeBGProb = 0.003

config.rowAndColIntervalRange = 4, 48
config.noiseAmplitude = 2
config.noiseAmplitudeRange = 1.05, 3.1

config.line_minHue = 0
config.line_maxHue = 60
config.line_minSaturation = 0.0
config.line_maxSaturation = 0.90
config.line_minValue = 0.0
config.line_maxValue = 0.010
# config.line_alpha = 180

config.bg_minHue = 0
config.bg_maxHue = 60
config.bg_minSaturation = 0.5
config.bg_maxSaturation = 0.9
config.bg_minValue = 0.4
config.bg_maxValue = 0.7
# config.bg_alpha = 40

config.canvasWidth = 64
config.canvasHeight = 64

config.lightMode = False


config.bgClr = ColorObj()
changeColor(config.bgClr, config.bg_minHue / 360, config.bg_maxHue / 360, config.bg_minSaturation, config.bg_maxSaturation, config.bg_minValue, config.bg_maxValue, True)
Bg = display.create_pen_hsv(config.bgClr.h, config.bgClr.s, config.bgClr.v)

config.fgClr = ColorObj()
changeColor(
    config.fgClr, config.line_minHue / 360, config.line_maxHue / 360, config.line_minSaturation, config.line_maxSaturation, config.line_minValue, config.line_maxValue, True
)
ForeG = display.create_pen_hsv(config.fgClr.h, config.fgClr.s, config.fgClr.v)

display.clear()

resetLines()
pause = False
print(config.bgClr.intransition)

while True:

    config.bgClr.clrStep()
    Bg = display.create_pen_hsv(config.bgClr.h, config.bgClr.s, config.bgClr.v)
    display.set_pen(Bg)
    display.clear()

    config.fgClr.clrStep()
    ForeG = display.create_pen_hsv(config.fgClr.h, config.fgClr.s, config.fgClr.v)
    display.reset_pen(ForeG)
    display.set_pen(ForeG)

    hashlines2()

    if random.random() < config.changeBGProb:
        if not config.bgClr.intransition : setBGColor()
        if not config.fgClr.intransition : setLineColor()

    if random.random() < config.changeLinesProb:
        config.lightMode = False if random.random() > config.lightModeProb else True
        resetLines()
        if not config.bgClr.intransition : setBGColor()
        if not config.fgClr.intransition : setLineColor()
        
    # _on  = checkTime()
    # if not _on:
    #     display.clear()
    #     display.reset_pen(BLANKSCREEN)
    #     display.set_pen(BLANKSCREEN)
    #     display.clear()
        
    i75.update()
    time.sleep(config.interval)


