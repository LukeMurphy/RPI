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
INTERVAL = 0.02

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

fgClr = ColorObj()
fgClr.h = random.uniform(0, 1.0)
fgClr.s = random.uniform(0.2, 1.0)
fgClr.v = random.uniform(0.2, 0.80)

Bg = display.create_pen_hsv(bgClr.h, bgClr.s, bgClr.v)
ForeG = display.create_pen_hsv(fgClr.h, fgClr.s, fgClr.v)

shp = AbsShape()

while True:
    display.set_pen(Bg)
    display.clear()

    # Reset the pen so we can reuse it
    display.reset_pen(ForeG)
    display.set_pen(ForeG)
    # display.circle(x, y, 10)
    # display.rectangle(x, y, 10, 10)
    shp.p1.pointStep()
    shp.p4.pointStep()
    shp.p3.pointStep()
    shp.p4.pointStep()
    bgClr.clrStep()
    fgClr.clrStep()

    Bg = display.create_pen_hsv(bgClr.h, bgClr.s, bgClr.v)
    # ForeG = display.create_pen_hsv(fgClr.h, fgClr.s, fgClr.v)

    display.polygon(
        [
            tuple(shp.p1.pt),
            tuple(shp.p2.pt),
            tuple(shp.p3.pt),
            tuple(shp.p4.pt),
        ]
    )
    # Update the display
    i75.update()

    if random.random() < 0.002:
        bgClr.newh = random.uniform(0, 1.0)
        bgClr.news = random.uniform(0, 1.0)
        bgClr.newv = random.uniform(0.2, 0.50)
        bgClr.change()

    if random.random() < 0.001:
        fgClr.newh = random.uniform(0, 1.0)
        fgClr.news = random.uniform(0.2, 1.0)
        fgClr.newv = random.uniform(0.2, 0.50)
        fgClr.change()

    if random.random() < 0.01:
        shp.update()

    time.sleep(INTERVAL)
