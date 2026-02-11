import time
import random
import math
import gc
import drawing_scribbles_classes
import drawing_scribbles_setpalette


from interstate75 import Interstate75, DISPLAY_INTERSTATE75_64X64



def R(a, b, rounded=False):
    if not rounded:
        return random.uniform(a, b)
    else:
        return round(random.uniform(a, b))


def changeColor(clrRef, hmin, hmax, smin, smax, vmin, vmax, init=False):
    if init:
        clrRef.h = random.uniform(hmin, hmax)
        clrRef.s = random.uniform(smin, smax)
        clrRef.v = random.uniform(vmin, vmax)
    else:
        clrRef.newh = random.uniform(hmin, hmax)
        clrRef.news = random.uniform(smin, smax)
        clrRef.newv = random.uniform(vmin, vmax)


def setColor(_clrRef, _clrSetRef):
    _clrSet = _clrSetRef[round(random.uniform(0, len(_clrSetRef) - 1))]
    _minh = _clrSet[0]
    _maxh = _clrSet[1]
    _h = random.uniform(_minh, _maxh)
    if _minh > _maxh:
        _h = random.uniform(_minh, 1.0 - _maxh)

    _clrRef.h = _h
    _clrRef.s = random.uniform(_clrSet[2], _clrSet[3])
    _clrRef.v = random.uniform(_clrSet[4], _clrSet[5])


# ----------------------------------------------------##----------------------------------------------------#


def catmull_rom(p0, p1, p2, p3, t):
    t2 = t * t
    t3 = t2 * t

    return 0.5 * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3)


def generateScribble(_pen):
    gc.collect()
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

            _ol = False
            if _penWidth >= 0.5 and _pen.outline:
                _ol = True
            drawLineEnvelope(_poly, _ol)

            _pen.lastAngle = _angle
            _pen._p += 1
            _pen.lastOrthoPoint = [_orthoP2x, _orthoP2y, _orthoP3x, _orthoP3y]

            config.doingDrawing = True
        if _pen._p == len(_pen.smooth_points):
            _pen._p = 0
            # print("Drawing stopped.")
            penMark.linesDrawn += 1
            _pen.drawingDone = True
            time.sleep(random.uniform(0, penMark.timeDelayBeforeDrawingAgain))
            # startUpNewLine()

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


def drawLineEnvelope(_poly, ol=False):
    global penG, probLineChangesColor, OutlineG
    display.reset_pen(penG)
    if random.random() < probLineChangesColor:
        setColor(penClr, penMark.penColorSets)
    penG = display.create_pen_hsv(penClr.h, penClr.s, penClr.v * brightness)
    display.set_pen(penG)
    display.polygon(_poly)

    if ol:
        display.set_pen(OutlineG)
        display.line(_poly[0][0], _poly[0][1], _poly[1][0], _poly[1][1], 2)
        display.line(_poly[2][0], _poly[2][1], _poly[3][0], _poly[3][1], 2)


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
    penMark.drawingDone = False
    penMark.loopDirection = -1
    if random.random() < 0.5:
        penMark.loopDirection = 1

    setColor(penClr, penMark.penColorSets)
    penG = display.create_pen_hsv(penClr.h, penClr.s, penClr.v * penBrightness)
    display.reset_pen(penG)
    # print(f"line - will be drawing {penMark.linesDrawn + 1} /  {penMark.linesToDraw} line(s)")
    generateScribble(penMark)


# ----------------------------------------------------##----------------------------------------------------#


def setShapes():
    global shapes
    _count = 0
    _dd = 2
    for _r in range(ROWS):
        for _c in range(COLS):
            _shp = shapes[_count]
            _wd = random.uniform(4, 32)
            _wd2 = _wd / 2
            _rx = _c * PWIDTH / COLS + random.uniform(-_wd2, _wd2) - _r * _dd
            _ry = _r * PHEIGHT / ROWS + random.uniform(-_wd2, _wd2) - _c * _dd
            _shp.initP1 = drawing_scribbles_classes.Point(_rx, _ry)
            _shp.initP2 = drawing_scribbles_classes.Point(_rx, _ry + _wd)
            _shp.initP3 = drawing_scribbles_classes.Point(_rx + _wd, _ry + _wd)
            _shp.initP4 = drawing_scribbles_classes.Point(_rx + _wd, _ry)
            _shp.setup()
            _count += 1


def _setShapes():
    global shapes
    for _shp in shapes:
        _wd = random.uniform(4, 5)
        _rx = random.uniform(0, PWIDTH - _wd / 2)
        _ry = random.uniform(0, PHEIGHT - _wd / 2)
        _shp.initP1 = Point(_rx, _ry)
        _shp.initP2 = Point(_rx, _ry + _wd)
        _shp.initP3 = Point(_rx + _wd, _ry + _wd)
        _shp.initP4 = Point(_rx + _wd, _ry)
        _shp.setup()


def drawBGPanelBlocks():
    global shapes
    for shp in shapes:
        drawBGPanelBlock(shp)


def drawBGPanelBlock(shp):
    global ForeG, probPanelBlockChangesColor
    display.reset_pen(ForeG)
    display.set_pen(ForeG)
    if random.random() < probPanelBlockChangesColor:
        setColor(fgClr, penMark.bgBoxColorSets)
    ForeG = display.create_pen_hsv(fgClr.h, fgClr.s, fgClr.v * brightness)
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


# ----------------------------------------------------##----------------------------------------------------#

# Setup for the display
i75 = Interstate75(display=DISPLAY_INTERSTATE75_64X64)
display = i75.display


def checkTime():
    hour  = time.localtime()[3]
    minute = time.localtime()[4]
    keepOn = False
    if hour >= 8 and hour <= 23 :
        keepOn = True
        
    return keepOn
        

    
BLANKSCREEN = display.create_pen_hsv(0,0,0)


# -------------------------------------------  -SETTINGS ---------------------------------------------------#

INTERVAL = 0.02
PWIDTH = 64
PHEIGHT = 64
NUMSQRS = 25
ROWS = 5
COLS = 5

brightness = 0.9
penBrightness = 0.9
numPalettes = 6

startNewLineProb = 0.25
eraseProb = 0.5
changePaletteProb = 0.925
probPanelBlockChangesColor = 0.01
probLineChangesColor = 0.005

# ----------------------------------------------------##----------------------------------------------------#

panelBGBlockCount = 0

penMark = drawing_scribbles_classes.PenMark()
config = drawing_scribbles_classes.Config()
outLineClr = drawing_scribbles_classes.ColorObj()
outLineClr.h = random.uniform(0, 1.0)
outLineClr.s = random.uniform(0.2, 1.0)
outLineClr.v = random.uniform(0.01, 0.1)
OutlineG = display.create_pen_hsv(outLineClr.h, outLineClr.s, outLineClr.v)

penMark.name = "scribbleLine1"
penMark.linesToDrawMin = 1
penMark.linesToDrawMax = 4
penMark.timeDelayBeforeDrawingAgain = 5
penMark.probDarkBG = 0.025
penMark.bgColorSets = []
penMark.bgBoxColorSets = []
penMark.penColorSets = []

drawing_scribbles_setpalette.setPalette(0, penMark)

OutlineG = display.create_pen_hsv(outLineClr.h, outLineClr.s, outLineClr.v)
display.reset_pen(OutlineG)
penMark.loops = R(penMark.loopsMin, penMark.loopsMax, True)
penMark.points = round(penMark.loops * penMark.pointsPerLoop)
penMark.linesToDraw = round(random.uniform(penMark.linesToDrawMin, penMark.linesToDrawMax))
penMark.outline = False
if random.random() < penMark.outlineProb:
    penMark.outline = True


# ----------------------------------------------------##----------------------------------------------------#
# SETUPS #

shapes = []

bgClr = drawing_scribbles_classes.ColorObj()
setColor(bgClr, penMark.bgColorSets)
Bg = display.create_pen_hsv(bgClr.h, bgClr.s, bgClr.v)

fgClr = drawing_scribbles_classes.ColorObj()
setColor(fgClr, penMark.bgBoxColorSets)
fgClr.change()
ForeG = display.create_pen_hsv(fgClr.h, fgClr.s, fgClr.v)

penClr = drawing_scribbles_classes.ColorObj()
setColor(penClr, penMark.penColorSets)
penG = display.create_pen_hsv(penClr.h, penClr.s, penClr.v)

for _ in range(NUMSQRS):
    _shp = drawing_scribbles_classes.AbsShape()
    shapes.append(_shp)

setShapes()
startUpNewLine()

display.set_pen(ForeG)
display.set_pen(penG)
display.set_pen(Bg)
display.clear()

generateScribble(penMark)
drawBGPanelBlocks()


while True:

    if penMark.drawingDone and random.random() < startNewLineProb and penMark.linesDrawn < penMark.linesToDraw:
        # print(penMark.linesDrawn, penMark.linesToDraw)
        if gc.mem_free() < 3000:
            gc.collect()
        startUpNewLine()

    if random.random() < eraseProb and panelBGBlockCount == 0 and penMark.linesDrawn >= penMark.linesToDraw:
        if gc.mem_free() < 3000:
            gc.collect()
        if random.random() < changePaletteProb:
            arg = math.floor(random.uniform(0, numPalettes))
            # print(f"setting to palette {arg}")
            drawing_scribbles_setpalette.setPalette(arg, penMark)
        setColor(fgClr, penMark.bgBoxColorSets)
        ForeG = display.create_pen_hsv(fgClr.h, fgClr.s, fgClr.v)
        outLineClr.h = random.uniform(210 / 360, 240 / 360)
        outLineClr.s = random.uniform(0.8, 1.0)
        outLineClr.v = random.uniform(0.01, 0.1)
        if penMark.num == 3:  # for noir, dark blue on gray is an acquired taste
            outLineClr.v = random.uniform(0.0, 0.001)
            outLineClr.s = random.uniform(0.01, 0.10)
        OutlineG = display.create_pen_hsv(outLineClr.h, outLineClr.s, outLineClr.v)
        display.reset_pen(OutlineG)
        setShapes()
        display.reset_pen(ForeG)
        display.set_pen(ForeG)
        panelBGBlockCount = 1
        penMark.linesDrawn = 0
        penMark.loops = R(penMark.loopsMin, penMark.loopsMax, True)
        penMark.points = round(penMark.loops * penMark.pointsPerLoop)
        penMark.linesToDraw = round(random.uniform(penMark.linesToDrawMin, penMark.linesToDrawMax))
        penMark.outline = False
        if random.random() < penMark.outlineProb:
            penMark.outline = True
        # print( penMark.linesToDraw)

    if panelBGBlockCount > 0:
        drawBGPanelBlock(shapes[panelBGBlockCount])
        panelBGBlockCount += 1
        if panelBGBlockCount >= NUMSQRS:
            panelBGBlockCount = 0

    display.reset_pen(penG)
    display.set_pen(penG)

    if panelBGBlockCount == 0 and not penMark.drawingDone:
        drawLinePolyEnvelope(penMark)

    # _on  = checkTime()
    
    # if not _on:
    #     display.clear()
    #     display.reset_pen(BLANKSCREEN)
    #     display.set_pen(BLANKSCREEN)
    #     display.clear()

        
    # Update the display
    i75.update()
    time.sleep(INTERVAL)
