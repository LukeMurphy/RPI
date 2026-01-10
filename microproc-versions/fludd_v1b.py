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


class Point:

    x = 0
    y = 0
    dx = 0
    dy = 0
    newX = 0
    newY = 0
    initX = 0
    initY = 0
    diffX = 0
    diffY = 0
    xSpeed = 0
    ySpeed = 0
    pt = []
    speedFactor = 8
    xMax = 6
    yMax = 6

    def __init__(self, _x, _y, xMaxDrift, yMaxDrift):
        self.x = _x
        self.y = _y
        self.initX = _x
        self.initY = _y
        self.xMax = xMaxDrift
        self.yMax = yMaxDrift
        self.pt = [self.x, self.y]

    def change(self, changeY=True):
        self.dx = self.newX - self.x
        self.dy = self.newY - self.y
        self.xSpeed = self.dx / self.speedFactor
        self.ySpeed = self.dy / self.speedFactor


    def pointStep(self):
        self.x = self.x + self.xSpeed
        self.y = self.y + self.ySpeed

        if round(self.x) == round(self.newX):
            self.dx = 0
            self.xSpeed = 0

        if round(self.y) == round(self.newY):
            self.dy = 0
            self.ySpeed = 0

        if self.x > self.initX + self.xMax or self.x < self.initX - self.xMax:
            self.newX = self.initX
            self.change()

        if self.y > self.initY + self.yMax or self.y < self.initY - self.yMax:
            self.newY = self.initY
            self.change()

        self.pt = [self.x, self.y]


class AbsShape:
    inColorTrans = False
    inShapeTrans = False
    # range of changes
    dx = 0
    dy = 0
    initP1 = (0, 0)
    initP2 = (0, 0)
    initP3 = (0, 0)
    initP4 = (0, 0)
    resetProb = 0.0025
    pointchangeProb = 0.25
    xMaxDrift = 0
    yMaxDrift = 0
    inset = 0
    insetMin = 0
    insetArray = []
    constantInsetRedraw = False
    drawInset = False
    pointspeedFactor = 8

    def init(self):
        self.p1 = Point(self.initP1[0], self.initP1[1], self.xMaxDrift, self.yMaxDrift)
        self.p2 = Point(self.initP2[0], self.initP2[1], self.xMaxDrift, self.yMaxDrift)
        self.p3 = Point(self.initP3[0], self.initP3[1], self.xMaxDrift, self.yMaxDrift)
        self.p4 = Point(self.initP4[0], self.initP4[1], self.xMaxDrift, self.yMaxDrift)

        self.p1.speedFactor = self.pointspeedFactor
        self.p2.speedFactor = self.pointspeedFactor
        self.p3.speedFactor = self.pointspeedFactor
        self.p4.speedFactor = self.pointspeedFactor

        self.inset_p1 = Point(self.initP1[0] + self.inset, self.initP1[1] - self.inset, 0, 0)
        self.inset_p2 = Point(self.initP2[0] + self.inset, self.initP2[1] + self.inset, 0, 0)
        self.inset_p3 = Point(self.initP3[0] - self.inset, self.initP3[1] + self.inset, 0, 0)
        self.inset_p4 = Point(self.initP4[0] - self.inset, self.initP4[1] - self.inset, 0, 0)

        self.resetInsets()
        self.setInsetPts()

    def resetInsets(self):
        self.insetArray = []
        self.insetArray.append([random.randint(self.insetMin, self.inset), -random.randint(self.insetMin, self.inset)])
        self.insetArray.append([random.randint(self.insetMin, self.inset), random.randint(self.insetMin, self.inset)])
        self.insetArray.append([-random.randint(self.insetMin, self.inset), random.randint(self.insetMin, self.inset)])
        self.insetArray.append([-random.randint(self.insetMin, self.inset), -random.randint(self.insetMin, self.inset)])

    def setInsetPts(self):
        if self.constantInsetRedraw:
            self.resetInsets()
        self.inset_p1.x = self.p1.x + self.insetArray[0][0]
        self.inset_p1.y = self.p1.y + self.insetArray[0][1]
        self.inset_p2.x = self.p2.x + self.insetArray[1][0]
        self.inset_p2.y = self.p2.y + self.insetArray[1][1]
        self.inset_p3.x = self.p3.x + self.insetArray[2][0]
        self.inset_p3.y = self.p3.y + self.insetArray[2][1]
        self.inset_p4.x = self.p4.x + self.insetArray[3][0]
        self.inset_p4.y = self.p4.y + self.insetArray[3][1]

    def update(self, _override=False):
        _prob = self.pointchangeProb
        if _override:
            _prob = 1.0
        pts = [
            (self.p1, _prob, True, self.initP1),
            (self.p2, _prob, True, self.initP2),
            (self.p3, _prob, True, self.initP3),
            (self.p4, _prob, True, self.initP4),
        ]

        for pt, prob, changeY, initPt in pts:
            if random.random() < prob and pt.xSpeed == 0 and pt.ySpeed == 0:
                pt.newX = pt.pt[0] + random.uniform(-self.dx, self.dx)
                pt.newY = pt.pt[1] + random.uniform(-self.dy, self.dy)

            if random.random() < self.resetProb:
                pt.newX = initPt[0]
                pt.newY = initPt[1]
            pt.change()
            self.resetInsets()


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
        self.speedFactor = 8
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


# ---------- SETTINGS ---------------#
# Setup for the display
i75 = Interstate75(display=DISPLAY_INTERSTATE75_64X64)
display = i75.display

config = Config()

config.interval = 0.03
changeAnimProb = 0.001
shapeChangeProb = 0.009
initialInsetFromEdges = 12

shp = AbsShape()
shp.dx = 3
shp.dy = 3
shp.xMaxDrift = 4
shp.yMaxDrift = 4
shp.pointspeedFactor = 10
shp.inset = 4
shp.insetMin = 1
shp.initP1 = (initialInsetFromEdges, 63 - initialInsetFromEdges)
shp.initP2 = (initialInsetFromEdges, initialInsetFromEdges - 1)
shp.initP3 = (63 - initialInsetFromEdges, initialInsetFromEdges - 1)
shp.initP4 = (63 - initialInsetFromEdges, 63 - initialInsetFromEdges)
shp.resetProb = 0.05
shp.constantInsetRedraw = False
shp.drawInset = False
shp.init()

bgClr = ColorObj()
bgClr.speedFactor = 20
changeColor(bgClr, 45 / 360, 45 / 360, 1.0, 1.0, 0.35, 0.65, True)
Bg = display.create_pen_hsv(bgClr.h, bgClr.s, bgClr.v)

fgClr = ColorObj()
changeColor(fgClr, 350 / 360, 260 / 360, 0.90, 1.0, 0.0, 0.0, True)
ForeG = display.create_pen_hsv(fgClr.h, fgClr.s, fgClr.v)

display.clear()

pause = False


while True:

    bgClr.clrStep()
    Bg = display.create_pen_hsv(bgClr.h, bgClr.s, bgClr.v)
    display.set_pen(Bg)
    display.clear()

    fgClr.clrStep()
    ForeG = display.create_pen_hsv(fgClr.h, fgClr.s, fgClr.v)
    display.reset_pen(ForeG)
    display.set_pen(ForeG)

    shp.p1.pointStep()
    shp.p2.pointStep()
    shp.p3.pointStep()
    shp.p4.pointStep()

    display.polygon(
        [
            (round(shp.p1.pt[0]), round(shp.p1.pt[1])),
            (round(shp.p2.pt[0]), round(shp.p2.pt[1])),
            (round(shp.p3.pt[0]), round(shp.p3.pt[1])),
            (round(shp.p4.pt[0]), round(shp.p4.pt[1])),
            (round(shp.p1.pt[0]), round(shp.p1.pt[1])),
        ]
    )
    Bg = display.create_pen_hsv(bgClr.h, bgClr.s, bgClr.v)
    display.set_pen(Bg)

    if shp.drawInset:
        shp.setInsetPts()
        display.polygon(
            [
                (round(shp.inset_p1.x), round(shp.inset_p1.y)),
                (round(shp.inset_p2.x), round(shp.inset_p2.y)),
                (round(shp.inset_p3.x), round(shp.inset_p3.y)),
                (round(shp.inset_p4.x), round(shp.inset_p4.y)),
                (round(shp.inset_p1.x), round(shp.inset_p1.y)),
            ]
        )

        if random.random() < shapeChangeProb:
            shp.constantInsetRedraw = True
        if random.random() < shapeChangeProb:
            shp.constantInsetRedraw = False

    if random.random() < shapeChangeProb:
        print("change")
        shp.update()

        if random.random() < 0.333 and not bgClr.intransition:
            changeColor(bgClr, 350 / 360, 260 / 360, 0.50, 1.0, 0.4, 0.45)
            bgClr.change()

    if random.random() < changeAnimProb:
        print("reset")
        if gc.mem_free() < 3000:
            gc.collect()
        shp.update(True)
        if shp.drawInset:
            shp.drawInset = False
        else:
            shp.drawInset = True

    i75.update()
    time.sleep(config.interval)
