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
        self.speedFactor = 40

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
animCanNotPauseFrames = [[9, 10, 11, 12], [4, 5], [5, 6, 7, 8, 9], [], [], [], [], []]
animOffsets = [[0, 2], [0, 0], [0, 0], [0, 0], [0, 2], [0, 0], [0, 0], [0, 0]]
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
bgClr.h = random.uniform(0, 1.0)
bgClr.s = random.uniform(0.7, 1.0)
bgClr.v = random.uniform(0.5, 0.50)
Bg = display.create_pen_hsv(bgClr.h, bgClr.s, bgClr.v)

display.set_pen(Bg)
display.clear()

count = 0
incr = 1
pause = False
activeAnim = 0

while True:

    numImages = anims[activeAnim][1]
    # open each file in the gif folder
    for n in range(numImages * 2):

        if count >= anims[activeAnim][1]:
            count -= 1
        if count < 0:
            count = 0

        img = anims[activeAnim][0][count]

        bgClr.clrStep()
        Bg = display.create_pen_hsv(bgClr.h, bgClr.s, bgClr.v)
        display.set_pen(Bg)
        display.clear()

        p.open_file(img)
        # Decode our PNG file and set the X and Y
        p.decode(animOffsets[activeAnim][0], animOffsets[activeAnim][1])
        i75.update()

        # print("Displaying: " + img)
        if not pause:
            count += incr

        if count >= numImages:
            incr = -1
            pause = True

        if count <= 0:
            incr = 1
            pause = True

        if random.random() < 0.03 and count not in animCanNotPauseFrames[activeAnim]:
            pause = True
            # sometimes just goes back
            if random.random() < 0.5:
                incr *= -1

        if random.random() < 0.01:
            pause = False

        if random.random() < 0.005 and (count < 2 or count > 12):
            activeAnim = round(random.uniform(0, len(anims) - 1))
            bgClr.newh = random.uniform(0, 1.0)
            bgClr.news = random.uniform(0.8, 1.0)
            bgClr.newv = random.uniform(0.5, 0.50)
            bgClr.change()
            # Bg = display.create_pen_hsv(bgClr.h, bgClr.s, bgClr.v)
            count = 0
            incr = 1
            numImages = anims[activeAnim][1]
            break

        # if random.random() < 0.002:
        #     bgClr.newh = random.uniform(0, 1.0)
        #     bgClr.news = random.uniform(0.8, 1.0)
        #     bgClr.newv = random.uniform(0.5, 0.50)
        #     bgClr.change()

        time.sleep(INTERVAL)
