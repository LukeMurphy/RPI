""" """

import time
from interstate75 import Interstate75, DISPLAY_INTERSTATE75_64X64
import pngdec
import os
import random


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


# Time to pause between frames
INTERVAL = .03

# Setup for the display
i75 = Interstate75(display=DISPLAY_INTERSTATE75_64X64)
display = i75.display

WIDTH = i75.width
HEIGHT = i75.height

x = 10
y = 10

bgClr = ColorObj()
bgClr.h = random.uniform(0, 1.0)
bgClr.s = random.uniform(0, 1.0)
bgClr.v = random.uniform(0.2, 0.50)
Bg = display.create_pen_hsv(bgClr.h, bgClr.s, bgClr.v)

fgClr = ColorObj()
fgClr.h = random.uniform(0, 1.0)
fgClr.s = random.uniform(0.2, 1.0)
fgClr.v = random.uniform(0.2, 0.80)
ForeG = display.create_pen_hsv(fgClr.h, fgClr.s, fgClr.v)

outLineClr = ColorObj()
outLineClr.h = random.uniform(0, 1.0)
outLineClr.s = random.uniform(0.2, 1.0)
outLineClr.v = random.uniform(0.0, 0.01)
OutlineG = display.create_pen_hsv(outLineClr.h, outLineClr.s, outLineClr.v)

shp = AbsShape()

bottomY = 63

startHoofX = random.randint(6, 12)
hoofWidth = random.randint(1, 4)
hoofHeight = random.randint(0, 3)
# also the chest
neckX = startHoofX + hoofWidth
neckWidth = random.randint(8, 8)
earCutInWidth = random.randint(4, 4)
earLength = random.randint(3, 12)

neckTopY = random.randint(30, 34)
backTopY = random.randint(30, 32)
backWidth = random.randint(30, 32)
bellyBottom = random.randint(44, 48)

mouthX = random.randint(6, 6)
noseX = mouthX
noseY = neckTopY
noseTopY = noseY - random.randint(1, 8)

foreHeadLength = random.randint(6, 6)
foreHeadX = mouthX + random.randint(2, 2) + foreHeadLength
foreHeadY = noseTopY - random.randint(8, 8)

headTopY = foreHeadY

earTip1X = foreHeadX + earLength
earTip1Y = headTopY - random.randint(0, 4)

earHeight = random.randint(4, 4)

earTip2X = random.randint(earTip1X, earTip1X)
earTip2Y = earTip1Y + earHeight

earBaseX = neckX + neckWidth - 2
earBaseY = earTip2Y 

tailCurlY = random.randint(30, 32)
tailCurlTipY = backTopY - random.randint(2, 12)
tailCurlHeight = random.randint(2, 4)
backCurlWidth = random.randint(3, 4)
tailWidth = random.randint(3, 4)
tailCurlBaseY = random.randint(18, 18)
tailEndY = 43
tailJoinY = 45
backLegFarX = neckX + neckWidth + backWidth + tailWidth

legWidth = random.randint(6, 6)
legSeparation = random.randint(3, 3)

thld = .2
over = 1

while True:


    if random.random() < thld : startHoofX = random.randint(6, 12)
    if random.random() < thld : hoofWidth = random.randint(1, 4)
    if random.random() < thld : hoofHeight = random.randint(2, 3)
    # also the chest
    neckX = startHoofX + hoofWidth
    if random.random() < thld : neckWidth = random.randint(8, 8)
    if random.random() < thld : earCutInWidth = random.randint(4, 4)
    if random.random() < thld : earLength = random.randint(3, 12)

    if random.random() < thld : neckTopY = random.randint(30, 34)
    if random.random() < thld : backTopY = random.randint(30, 32)
    if random.random() < thld : backWidth = random.randint(30, 32)
    if random.random() < thld : bellyBottom = random.randint(44, 48)

    if random.random() < thld : mouthX = random.randint(6, 6)
    noseX = mouthX
    noseY = neckTopY
    if random.random() < thld : noseTopY = noseY - random.randint(1, 8)

    if random.random() < thld : foreHeadLength = random.randint(6, 6)
    if random.random() < thld : foreHeadX = mouthX + random.randint(2, 2) + foreHeadLength
    if random.random() < thld : foreHeadY = noseTopY - random.randint(8, 8)
    
    headTopY = foreHeadY

    earTip1X = foreHeadX + earLength
    if random.random() < thld : earTip1Y = headTopY - random.randint(0, 4)
    
    if random.random() < thld : earHeight = random.randint(4, 4)
    
    if random.random() < thld : earTip2X = random.randint(earTip1X, earTip1X)
    earTip2Y = earTip1Y + earHeight
    
    earBaseX = neckX + neckWidth - 2
    earBaseY = earTip2Y 

    if random.random() < thld : tailCurlY = random.randint(30, 32)
    if random.random() < thld*over : tailCurlTipY = backTopY - random.randint(2, 18)
    if random.random() < thld : tailCurlHeight = random.randint(2, 4)
    if random.random() < thld : backCurlWidth = random.randint(3, 4)
    if random.random() < thld*over : tailWidth = random.randint(2, 5)
    if random.random() < thld : tailCurlBaseY = random.randint(18, 18)

    backLegFarX = neckX + neckWidth + backWidth + tailWidth

    if random.random() < thld : legWidth = random.randint(6, 6)
    if random.random() < thld : legSeparation = random.randint(3, 3)

    polyOutline = [
        (startHoofX, bottomY),
        (startHoofX + hoofWidth, bottomY - hoofHeight),
        (startHoofX + hoofWidth, bellyBottom),
        (startHoofX + hoofWidth, neckTopY),
        # 
        (startHoofX + hoofWidth - mouthX, neckTopY),
        (startHoofX + hoofWidth - noseX, noseY), #top of nose
        (startHoofX + hoofWidth - noseX, noseTopY), 
        (foreHeadX, foreHeadY), # first forehead point
        (earTip1X, earTip1Y),
        (earTip2X, earTip2Y),
        (earBaseX, earBaseY),
        # 
        (neckX + neckWidth, earBaseY),
        (neckX + neckWidth, backTopY),
        (neckX + neckWidth + backWidth, backTopY),
        # 
        (neckX + neckWidth + backWidth, backTopY),
        (neckX + neckWidth + backWidth, tailCurlTipY),
        (neckX + neckWidth + backWidth - backCurlWidth, tailCurlTipY),
        # 
        (neckX + neckWidth + backWidth - backCurlWidth, tailCurlTipY - tailCurlHeight),
        (neckX + neckWidth + backWidth + tailWidth, tailCurlTipY - tailCurlHeight),
        (neckX + neckWidth + backWidth + tailWidth, tailEndY),
        (backLegFarX, tailJoinY),
        # 
        (backLegFarX, bottomY),
        (backLegFarX - legWidth, bottomY),
        (backLegFarX - legWidth + hoofWidth, bottomY - hoofHeight),
        (backLegFarX - legWidth + hoofWidth, bellyBottom),
        (backLegFarX - legWidth + hoofWidth - legSeparation, bellyBottom),
        (backLegFarX - legWidth + hoofWidth - legSeparation, bottomY),
        (backLegFarX - legWidth - legWidth - legSeparation, bottomY),
        (backLegFarX - legWidth - legWidth - legSeparation + hoofWidth * 2, bottomY - hoofHeight),
        (backLegFarX - legWidth - legWidth - legSeparation + hoofWidth * 2, bellyBottom),
        (neckX + legWidth + legWidth, bellyBottom),
        (neckX + legWidth + legWidth, bottomY),
        (neckX + legWidth, bottomY),
        (neckX + legWidth + hoofWidth, bottomY - hoofHeight),
        (neckX + legWidth + hoofWidth, bellyBottom),
        (neckX + legWidth - hoofWidth, bellyBottom),
        (neckX + legWidth - hoofWidth, bottomY),
        (startHoofX, bottomY),
    ]

    display.set_pen(Bg)
    display.clear()

    # Reset the pen so we can reuse it
    display.reset_pen(ForeG)
    display.set_pen(ForeG)
    # display.circle(x, y, 10)
    # display.rectangle(x, y, 10, 10)
    bgClr.clrStep()
    fgClr.clrStep()

    Bg = display.create_pen_hsv(bgClr.h, bgClr.s, bgClr.v)
    ForeG = display.create_pen_hsv(fgClr.h, fgClr.s, fgClr.v)

    display.polygon(polyOutline)

    display.reset_pen(OutlineG)
    display.set_pen(OutlineG)
    for p in range(0, len(polyOutline) - 1):
        display.line(polyOutline[p][0], polyOutline[p][1], polyOutline[p + 1][0], polyOutline[p + 1][1])

    display.rectangle(startHoofX + hoofWidth+ 3, neckTopY - 5, 2,2)
    if random.random() < 0.002:
        fgClr.newh = random.uniform(0, 1.0)
        fgClr.news = random.uniform(0.7, 1.0)
        fgClr.newv = random.uniform(0.5, 0.70)
        fgClr.change()

    if random.random() < 0.002:
        bgClr.newh = random.uniform(0, 1.0)
        bgClr.news = random.uniform(0.1, .50)
        bgClr.newv = random.uniform(0.01, 0.20)
        bgClr.change()

    # Update the display
    i75.update()
    time.sleep(INTERVAL)



