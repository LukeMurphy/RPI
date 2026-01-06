import random

class PenMark:
    drawingDone = False

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

