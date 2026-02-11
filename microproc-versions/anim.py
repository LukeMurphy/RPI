import time
from interstate75 import Interstate75, DISPLAY_INTERSTATE75_64X64
import pngdec
import os
import random
import gc


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

    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y
        self.initX = _x
        self.initY = _y
        self.xMax = XMAXDRIFT
        self.yMax = YMAXDRIFT
        self.pt = [self.x, self.y]

    def change(self, changeY = True):

        self.dx = self.newX - self.x
        if changeY :
            self.dy = self.newY - self.y

        self.xSpeed = self.dx / self.speedFactor
        if changeY :
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
    dx = 4
    dy = 4
    initP1 = (3, 64)
    initP2 = (2, 1)
    initP3 = (62, 1)
    initP4 = (59, 64)
    resetProb = 0.25

    def __init__(self):
        self.p1 = Point(self.initP1[0], self.initP1[1])
        self.p2 = Point(self.initP2[0], self.initP2[1])
        self.p3 = Point(self.initP3[0], self.initP3[1])
        self.p4 = Point(self.initP4[0], self.initP4[1])
        pass

    def update(self):

        pts = [
            (self.p1, 0.25, False, self.initP1),
            (self.p2, 0.96, True, self.initP2),
            (self.p3, 0.96, True, self.initP3),
            (self.p4, 0.25, False, self.initP4),
        ]

        for pt, prob, changeY, initPt in pts:
            if random.random() < prob:
                pt.newX = pt.pt[0] + random.uniform(-self.dx, self.dx)
                if changeY:
                    pt.newY = pt.pt[1] + random.uniform(-self.dy, self.dy)
                pt.change(changeY)
            if random.random() < self.resetProb:
                pt.newX = initPt[0]
                pt.change(False)
            if random.random() < self.resetProb:
                pt.newY = initPt[1]
                pt.change()


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


def changeColor(clrRef, hmin, hmax, smin, smax, vmin, vmax, init=False):

    clr  =  rColor( hmin, hmax, smin, smax, vmin, vmax)
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


# Setup for the display
i75 = Interstate75(display=DISPLAY_INTERSTATE75_64X64)
display = i75.display
p = pngdec.PNG(display)


def checkTime():
    hour  = time.localtime()[3]
    minute = time.localtime()[4]
    keepOn = False
    if hour >= 8 and hour <= 23 :
        keepOn = True
        
    return keepOn
        
BLANKSCREEN = display.create_pen_hsv(0,0,0)



# ---------- SETTINGS ---------------#
INTERVAL = 0.03
activeAnim = 0
changeAnimProb = 0.001
shapeChangeProb = 0.001
dx = 6
dy = 6
XMAXDRIFT = 4
YMAXDRIFT = 4

animConfigs = [
    {"dir": "imagesets/pensive-left", "nopauseFrames": [9, 10, 11, 12], "offsets": [-1, 2], "pauseProb": 0.05, "unpauseProb": 0.02},
    {"dir": "imagesets/bbear-2", "nopauseFrames": [4, 5, 6, 7, 8], "offsets": [2, 0], "pauseProb": 0.05, "unpauseProb": 0.02},
    {"dir": "imagesets/obear-turning", "nopauseFrames": [4, 5, 6, 7, 8, 9, 10, 13, 14, 15, 16, 17, 18, 19], "offsets": [0, 0], "pauseProb": 0.5, "unpauseProb": 0.01},
    {"dir": "imagesets/bbear-left", "nopauseFrames": [1, 2], "offsets": [4, 0], "pauseProb": 0.05, "unpauseProb": 0.02},
    {"dir": "imagesets/bbunny-rad", "nopauseFrames": [8, 9, 10], "offsets": [-2, 2], "pauseProb": 0.05, "unpauseProb": 0.02},
    {"dir": "imagesets/bbunny1", "nopauseFrames": [10, 11], "offsets": [0, 0], "pauseProb": 0.05, "unpauseProb": 0.02},
    {"dir": "imagesets/fig-left", "nopauseFrames": [6, 7, 8, 9], "offsets": [0, 2], "pauseProb": 0.05, "unpauseProb": 0.02},
    {"dir": "imagesets/mousey", "nopauseFrames": [3, 4, 5, 6, 7], "offsets": [0, 0], "pauseProb": 0.05, "unpauseProb": 0.02},
]


# ---------- SETTING UP ---------------#
anims = []

for _dir in animConfigs:
    # make a list of files in the gif fo
    # lder
    # print(_dir)
    _files = os.listdir(_dir["dir"])
    _images = []

    for file in _files:
        if file.endswith(".png" or ".PNG"):
            img = f"{_dir['dir']}/{file}"
            _images.append(img)

    _numImages = len(_images) - 1
    anims.append([_images, _numImages])

shp = AbsShape()
shp.dx = dx
shp.dy = dy

bgClr = ColorObj()
changeColor(bgClr, 45 / 360, 45 / 360, 1.0, 1.0, 0.35, 0.35, True)
Bg = display.create_pen_hsv(bgClr.h, bgClr.s, bgClr.v)

fgClr = ColorObj()
changeColor(fgClr, 350 / 360, 260 / 360, 0.90, 1.0, 0.45, 0.65, True)
ForeG = display.create_pen_hsv(fgClr.h, fgClr.s, fgClr.v)

display.set_pen(Bg)
display.clear()

pause = False
count = 0
incr = 1
activeAnim = round(random.uniform(0, len(anims) - 1))
pauseProb = animConfigs[activeAnim]["pauseProb"]
unpauseProb = animConfigs[activeAnim]["unpauseProb"]
unpauseProbInit = animConfigs[activeAnim]["unpauseProb"]
numImages = anims[activeAnim][1]


while True:

    if not pause:
        count += incr

        if count >= numImages:
            incr = -1
            pause = True
            unpauseProb = 0.1

        if count <= 0:
            incr = 1
            pause = True
            unpauseProb = unpauseProbInit

        if random.random() < pauseProb and count not in animConfigs[activeAnim]["nopauseFrames"]:
            pause = True
            # sometimes just goes back
            if random.random() < 0.5:
                incr *= -1
            # print(f"paused on {count} {incr}")

    if random.random() < unpauseProb:
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

    # OverflowError: overflow converting long int to machine word

    display.polygon(
        [
            (round(shp.p1.pt[0]), round(shp.p1.pt[1])),
            (round(shp.p2.pt[0]), round(shp.p2.pt[1])),
            (round(shp.p3.pt[0]), round(shp.p3.pt[1])),
            (round(shp.p4.pt[0]), round(shp.p4.pt[1])),
            (round(shp.p1.pt[0]), round(shp.p1.pt[1])),
        ]
    )

    if count >= anims[activeAnim][1]:
        # print(f"Error : {count} {activeAnim} {anims[activeAnim]}")
        count = len(anims[activeAnim][0]) - 1
        incr *= -1
    img = anims[activeAnim][0][count]

    p.open_file(img)
    # Decode our PNG file and set the X and Y
    p.decode(animConfigs[activeAnim]["offsets"][0], animConfigs[activeAnim]["offsets"][1])

    if random.random() < shapeChangeProb:
        shp.update()

    if random.random() < changeAnimProb and (count < 1 or count > 12):
        # activeAnim += 1
        # if activeAnim >= len(anims):
        #     activeAnim = 0
        if gc.mem_free() < 3000:
            gc.collect()

        activeAnim = round(random.uniform(0, len(anims) - 1))
        count = 0
        incr = 1
        numImages = anims[activeAnim][1]
        pauseProb = animConfigs[activeAnim]["pauseProb"]
        unpauseProb = animConfigs[activeAnim]["unpauseProb"]
        unpauseProbInit = animConfigs[activeAnim]["unpauseProb"]

        changeColor(bgClr, 0 / 360, 360 / 360, 0.50, 1.0, 0.1, 0.35)
        bgClr.change()

        changeColor(fgClr, 330 / 360, 260 / 360, 0.90, 1.0, 0.5, 0.60)
        fgClr.change()

        shp.update()
        
    # _on  = checkTime()
    
    # if not _on:
    #     display.clear()
    #     display.reset_pen(BLANKSCREEN)
    #     display.set_pen(BLANKSCREEN)
    #     display.clear()

    i75.update()
    time.sleep(INTERVAL)


