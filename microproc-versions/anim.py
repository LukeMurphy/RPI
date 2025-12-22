import time
from interstate75 import Interstate75, DISPLAY_INTERSTATE75_64X64
import pngdec
import os
import random


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
    speedFactor = 8

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
    dx = 5
    dy = 5
    initP1 = Point(3, 64)
    initP2 = Point(3, 2)
    initP3 = Point(60, 2)
    initP4 = Point(60, 64)

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

        if random.random() < 0.96:
            self.p2.newX = self.p2.pt[0] + round(random.uniform(-self.dx, self.dx))
            self.p2.newY = self.p2.pt[1] + round(random.uniform(-self.dy, self.dy))
            self.p2.change()

        if random.random() < 0.96:
            self.p3.newX = self.p3.pt[0] + round(random.uniform(-self.dx, self.dx))
            self.p3.newY = self.p3.pt[1] + round(random.uniform(-self.dy, self.dy))
            self.p3.change()

        if random.random() < 0.25:
            self.p4.newX = self.p4.pt[0] + round(random.uniform(-self.dx, self.dx))
            self.p4.newY = self.p4.pt[1]
            self.p4.change()

        if random.random() < 0.15:
            self.p1.newX = self.initP1.pt[0]
            self.p1.newY = self.initP1.pt[1]
            self.p1.change()
        if random.random() < 0.15:
            self.p2.newX = self.initP2.pt[0]
            self.p2.newY = self.initP2.pt[1]
            self.p2.change()
        if random.random() < 0.15:
            self.p3.newX = self.initP3.pt[0]
            self.p3.newY = self.initP3.pt[1]
            self.p3.change()
        if random.random() < 0.15:
            self.p4.newX = self.initP4.pt[0]
            self.p4.newY = self.initP4.pt[1]
            self.p4.change()


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
        self.speedFactor = 40

    def change(self):
        dh = self.newh - self.h

        if dh >= 0.5:
            dh *= -1

        self.dh = dh / self.speedFactor
        self.ds = (self.news - self.s) / self.speedFactor
        self.dv = (self.newv - self.v) / self.speedFactor

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


# Time to pause between frames
INTERVAL = 0.03

# Setup for the display
i75 = Interstate75(display=DISPLAY_INTERSTATE75_64X64)
display = i75.display

p = pngdec.PNG(display)

# animDirs = ["gif3", "gif2", "gif"]
animDirs = [
    "pensive-left",
    "bbear-2",
    "obear-turning",
    "bbear-left",
    "bbunny-rad",
    "bbunny1",
    "fig-left",
    "mousey",
]
# frames that are allowed to pause
animCanNotPauseFrames = [[9, 10, 11, 12], [4, 5, 6, 7], [3, 4, 5, 17, 18], [2], [9], [10, 11], [11, 12, 13, 14, 15], []]
animOffsets = [[0, 2], [0, 0], [0, 0], [0, 0], [0, 2], [0, 0], [0, 2], [0, 0]]
anims = []

for _dir in animDirs:
    # make a list of files in the gif folder
    _files = os.listdir(_dir)
    _images = []

    for file in _files:
        if file.endswith(".png" or ".PNG"):
            img = f"{_dir}/{file}"
            _images.append(img)
    _numImages = len(_images) - 1
    anims.append([_images, _numImages])

bgClr = ColorObj()
bgClr.h = random.uniform(45 / 360, 45 / 360)
bgClr.s = random.uniform(1.0, 1.0)
bgClr.v = random.uniform(0.35, 0.350)
Bg = display.create_pen_hsv(bgClr.h, bgClr.s, bgClr.v)

fgClr = ColorObj()
fgClr.h = random.uniform(0, 1.0)
fgClr.s = random.uniform(0.9, 1.0)
fgClr.v = random.uniform(0.45, 0.5)
ForeG = display.create_pen_hsv(fgClr.h, fgClr.s, fgClr.v)

display.set_pen(Bg)
display.clear()

count = 0
incr = 1
pause = False
activeAnim = 0
numImages = anims[activeAnim][1]

shp = AbsShape()


while True:

    img = anims[activeAnim][0][count]

    if not pause:
        count += incr

        if count >= numImages:
            incr = -1
            pause = True

        if count <= 0:
            incr = 1
            pause = True

    if random.random() < 0.00 and count not in animCanNotPauseFrames[activeAnim]:
        # pause = True
        # sometimes just goes back
        if random.random() < 0.5:
            incr *= -1

    if random.random() < 0.01:
        pause = False

    # bgClr.clrStep()
    # Bg = display.create_pen_hsv(bgClr.h, bgClr.s, bgClr.v)
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
            tuple(shp.p1.pt),
            tuple(shp.p2.pt),
            tuple(shp.p3.pt),
            tuple(shp.p4.pt),
        ]
    )

    p.open_file(img)
    # Decode our PNG file and set the X and Y
    p.decode(animOffsets[activeAnim][0], animOffsets[activeAnim][1])
    # i75.update()

    # print("Displaying: " + img)


    # if random.random() < 0.002:
    #     fgClr.newh = random.uniform(0, 1.0)
    #     fgClr.news = random.uniform(0.9, 1.0)
    #     fgClr.newv = random.uniform(0.4, 0.60)
    #     fgClr.change()

    if random.random() < 0.01:
        shp.update()

    if random.random() < 0.001 and (count  < 1 or count > 12):
        # activeAnim += 1
        # if activeAnim >= len(anims):
        #     activeAnim = 0
        activeAnim = round(random.uniform(0, len(anims) - 1))
        count = 0
        incr = 1
        numImages = anims[activeAnim][1]

        bgClr.newh = random.uniform(0.0, 1.0)
        bgClr.news = random.uniform(0.5, 1.0)
        bgClr.newv = random.uniform(0.1, 0.350)
        bgClr.change()

        fgClr.newh = random.uniform(0, 1.0)
        fgClr.news = random.uniform(0.9, 1.0)
        fgClr.newv = random.uniform(0.4, 0.60)
        fgClr.change()

        shp.update()


    i75.update()
    time.sleep(INTERVAL)