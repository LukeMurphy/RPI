import time
import os
import random
import gc
from interstate75 import Interstate75, DISPLAY_INTERSTATE75_64X64


# Setup for the display
i75 = Interstate75(display=DISPLAY_INTERSTATE75_64X64)
display = i75.display

class Config:
    def __init__(self):
        """
        Purpose: holds state 
        """

# ---------- SETTINGS ---------------#

config = Config()

config.interval = 0.03
config.changeAnimProbBase = 0.0004
config.changeColorProbBase = 0.85

config.changeAnimProb = config.changeAnimProbBase * config.interval / 0.03
config.changeColorProb = config.changeColorProbBase * config.interval / 0.03

config.scaleMode = False

CORNERPOINT_A = [0, -1]
CORNERPOINT_B = [64, -1]
CORNERPOINT_C = [64, 63]
CORNERPOINT_D = [0, 63]

# drift
config.pointDrift = 1
config.pointDriftMIN = 1
config.pointDriftMAX = 2
# inset from sides
config.pointInset = 10
config.pointInsetMIN = 10
config.pointInsetMAX = 10

config.sqrPt_A_Init = [0, 0]
config.sqrPt_B_Init = []
config.sqrPt_C_Init = []
config.sqrPt_D_Init = []

config.insetDelta = 3
config.hasInset = False
config.fgMinHue = 0.0
config.fgMaxHue = 0.0
config.fgMinSat = 0.0
config.fgMaxSat = 0.0
config.fgMinVal = 0.0
config.fgMaxVal = 0.0


def changeColor(hmin, hmax, smin, smax, vmin, vmax):

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

    # print(f"Color change {_hmin} {hmax} ==> {clrRef.newh}")


def changeClrMode(clrMode):
    if clrMode == 0:
        # all colors = no color
        config.interval = random.uniform(0.01, 0.030)
        config.hasInset = False
        config.fgMinHue = 0
        config.fgMaxHue = 1.0
        config.fgMinSat = 0.5
        config.fgMaxSat = 0.5
        config.fgMinVal = 0.5
        config.fgMaxVal = 0.5
        config.changeColorProb = 0.85
        config.changeColorProbBase = 0.85
        clr = changeColor(config.fgMinHue, config.fgMaxHue, config.fgMinSat, config.fgMaxSat, config.fgMinVal, config.fgMaxVal)
        config.fgClr = display.create_pen_hsv(clr[0], clr[1], clr[2])
        config.pointDrift = 1
        config.pointDriftMIN = 1
        config.pointDriftMAX = 2
        # inset from sides
        config.pointInset = 2
        config.pointInsetMIN = 1
        config.pointInsetMAX = 16
        if random.random() < 0.01 and config.interval < 0.07:
            config.scaleMode = True
        print("Changed to plenum")

    if clrMode == 1:
        # all colors = no color
        config.interval = random.uniform(0.055, 1.50)
        config.hasInset = False
        config.fgMinHue = 0
        config.fgMaxHue = 1.0
        config.fgMinSat = 0.5
        config.fgMaxSat = 0.5
        config.fgMinVal = 0.5
        config.fgMaxVal = 0.5
        config.changeColorProb = 0.85
        config.changeColorProbBase = 0.85
        clr = changeColor(config.fgMinHue, config.fgMaxHue, config.fgMinSat, config.fgMaxSat, config.fgMinVal, config.fgMaxVal)
        config.fgClr = display.create_pen_hsv(clr[0], clr[1], clr[2])
        config.pointDrift = 1
        config.pointDriftMIN = 1
        config.pointDriftMAX = 2
        # inset from sides
        config.pointInset = 2
        config.pointInsetMIN = 12
        config.pointInsetMAX = 24
        if random.random() < 0.01 and config.interval < 0.07:
            config.scaleMode = True

    elif clrMode == 2:
        # plenum white
        config.interval = random.uniform(0.055, 0.150)
        config.hasInset = True if random.random() < 0.5 else False
        config.fgMinHue = 0
        config.fgMaxHue = 1.0
        config.fgMinSat = 0.0
        config.fgMaxSat = 0.0
        config.fgMinVal = 0.5
        config.fgMaxVal = 0.7
        if config.hasInset:
            config.fgMaxVal = 0.99
        config.changeColorProb = 0.005
        config.changeColorProbBase = 0.005
        clr = changeColor(config.fgMinHue, config.fgMaxHue, config.fgMinSat, config.fgMaxSat, config.fgMinVal, config.fgMaxVal)
        config.fgClr = display.create_pen_hsv(clr[0], clr[1], clr[2])
        config.pointDrift = 1
        config.pointDriftMIN = 1
        config.pointDriftMAX = 3
        # inset from sides
        config.pointInset = 2
        config.pointInsetMIN = 1
        config.pointInsetMAX = 16

    elif clrMode == 3:
        # fire voids
        config.interval = random.uniform(0.05, 0.09)
        config.hasInset = True if random.random() < 0.01 else False
        config.fgMinHue = 0
        config.fgMaxHue = 50 / 360
        config.fgMinSat = 0.60
        config.fgMaxSat = 1.0
        config.fgMinVal = 0.4
        config.fgMaxVal = 0.7
        if config.hasInset:
            config.fgMaxVal = 0.5
        config.changeColorProb = 0.5
        config.changeColorProbBase = 0.5
        clr = changeColor(config.fgMinHue, config.fgMaxHue, config.fgMinSat, config.fgMaxSat, config.fgMinVal, config.fgMaxVal)
        config.fgClr = display.create_pen_hsv(clr[0], clr[1], clr[2])
        config.pointDrift = 1
        config.pointDriftMIN = 1
        config.pointDriftMAX = 3
        # inset from sides
        config.pointInset = 2
        config.pointInsetMIN = 1
        config.pointInsetMAX = 4

    config.pointDrift = random.randint(config.pointDriftMIN, config.pointDriftMAX)
    config.pointInset = random.randint(config.pointInsetMIN, config.pointInsetMAX)

    if config.pointInset > 3:
        config.changeColorProb = 0.001
        config.changeColorProbBase = 0.001

    config.changeAnimProb = config.changeAnimProbBase * config.interval / 0.03
    config.changeColorProb = config.changeColorProbBase * config.interval / 0.03

    config.sqrPt_A_Init = [CORNERPOINT_A[0] + config.pointInset, CORNERPOINT_A[1] + config.pointInset]
    config.sqrPt_B_Init = [CORNERPOINT_B[0] - config.pointInset, config.pointInset]
    config.sqrPt_C_Init = [CORNERPOINT_C[0] - config.pointInset, CORNERPOINT_C[1] - config.pointInset]
    config.sqrPt_D_Init = [config.pointInset, CORNERPOINT_D[1] - config.pointInset]


config.sqrPt_A = [4, 4]
config.sqrPt_B = [60, 4]
config.sqrPt_C = [60, 60]
config.sqrPt_D = [4, 60]

config.sqrPt_IN_A = [4, 4]
config.sqrPt_IN_B = [60, 4]
config.sqrPt_IN_C = [60, 60]
config.sqrPt_IN_D = [4, 60]

shp1 = [CORNERPOINT_A, CORNERPOINT_B, config.sqrPt_B, config.sqrPt_A]
shp2 = [CORNERPOINT_B, CORNERPOINT_C, config.sqrPt_C, config.sqrPt_B]
shp3 = [CORNERPOINT_D, CORNERPOINT_C, config.sqrPt_C, config.sqrPt_D]
shp4 = [CORNERPOINT_A, CORNERPOINT_D, config.sqrPt_D, config.sqrPt_A]

# shapeArray = [shp2]
shapeArray = [shp1, shp2, shp3, shp4]

clr = changeColor(45 / 360, 45 / 360, 1.50, 1.0, 0.0, 0.0)
bgClr = display.create_pen_hsv(clr[0], clr[1], clr[2])


display.set_pen(bgClr)
display.clear()

changeClrMode(1)

while True:
    # bgClr.clrStep()
    # Bg = display.create_pen_hsv(bgClr.h, bgClr.s, bgClr.v)
    display.set_pen(bgClr)
    display.clear()

    # config.fgClr.clrStep()
    # ForeG = display.create_pen_hsv(config.fgClr.h, config.fgClr.s, config.fgClr.v)
    display.reset_pen(config.fgClr)
    display.set_pen(config.fgClr)

    display.polygon([tuple(CORNERPOINT_A), tuple(CORNERPOINT_B), tuple(config.sqrPt_B), tuple(config.sqrPt_A), tuple(CORNERPOINT_A)])
    display.polygon([tuple(CORNERPOINT_B), tuple(CORNERPOINT_C), tuple(config.sqrPt_C), tuple(config.sqrPt_B), tuple(CORNERPOINT_B)])
    display.polygon([tuple(CORNERPOINT_D), tuple(CORNERPOINT_C), tuple(config.sqrPt_C), tuple(config.sqrPt_D), tuple(CORNERPOINT_D)])
    display.polygon([tuple(CORNERPOINT_A), tuple(CORNERPOINT_D), tuple(config.sqrPt_D), tuple(config.sqrPt_A), tuple(CORNERPOINT_A)])
    if config.hasInset:
        display.polygon(
            [
                tuple(config.sqrPt_IN_A),
                tuple(config.sqrPt_IN_B),
                tuple(config.sqrPt_IN_C),
                tuple(config.sqrPt_IN_D),
                tuple(config.sqrPt_IN_A),
            ]
        )

    if random.random() < config.changeColorProb:
        clr = changeColor(config.fgMinHue, config.fgMaxHue, config.fgMinSat, config.fgMaxSat, config.fgMinVal, config.fgMaxVal)
        config.fgClr = display.create_pen_hsv(clr[0], clr[1], clr[2])

    config.sqrPt_A = [random.randint(config.sqrPt_A_Init[0] - config.pointDrift, config.sqrPt_A_Init[0] + config.pointDrift), random.randint(config.sqrPt_A_Init[1] - config.pointDrift, config.sqrPt_A_Init[1] + config.pointDrift)]
    config.sqrPt_B = [random.randint(config.sqrPt_B_Init[0] - config.pointDrift, config.sqrPt_B_Init[0] + config.pointDrift), random.randint(config.sqrPt_B_Init[1] - config.pointDrift, config.sqrPt_B_Init[1] + config.pointDrift)]
    config.sqrPt_C = [random.randint(config.sqrPt_C_Init[0] - config.pointDrift, config.sqrPt_C_Init[0] + config.pointDrift), random.randint(config.sqrPt_C_Init[1] - config.pointDrift, config.sqrPt_C_Init[1] + config.pointDrift)]
    config.sqrPt_D = [random.randint(config.sqrPt_D_Init[0] - config.pointDrift, config.sqrPt_D_Init[0] + config.pointDrift), random.randint(config.sqrPt_D_Init[1] - config.pointDrift, config.sqrPt_D_Init[1] + config.pointDrift)]

    if config.hasInset:
        config.sqrPt_IN_A = [
            random.randint(config.sqrPt_A_Init[0] - config.pointDrift, config.sqrPt_A_Init[0] + config.pointDrift) + config.insetDelta,
            random.randint(config.sqrPt_A_Init[1] - config.pointDrift, config.sqrPt_A_Init[1] + config.pointDrift) + config.insetDelta,
        ]
        config.sqrPt_IN_B = [
            random.randint(config.sqrPt_B_Init[0] - config.pointDrift, config.sqrPt_B_Init[0] + config.pointDrift) - config.insetDelta,
            random.randint(config.sqrPt_B_Init[1] - config.pointDrift, config.sqrPt_B_Init[1] + config.pointDrift) + config.insetDelta,
        ]
        config.sqrPt_IN_C = [
            random.randint(config.sqrPt_C_Init[0] - config.pointDrift, config.sqrPt_C_Init[0] + config.pointDrift) - config.insetDelta,
            random.randint(config.sqrPt_C_Init[1] - config.pointDrift, config.sqrPt_C_Init[1] + config.pointDrift) - config.insetDelta,
        ]
        config.sqrPt_IN_D = [
            random.randint(config.sqrPt_D_Init[0] - config.pointDrift, config.sqrPt_D_Init[0] + config.pointDrift) + config.insetDelta,
            random.randint(config.sqrPt_D_Init[1] - config.pointDrift, config.sqrPt_D_Init[1] + config.pointDrift) - config.insetDelta,
        ]

    if random.random() < config.changeAnimProb:
        if gc.mem_free() < 3000:
            gc.collect()

        clrMode = random.choice([1, 2, 3])
        config.scaleMode = False
        print("now")
        changeClrMode(clrMode)

    if config.scaleMode:
        config.pointDrift = random.randint(config.pointDriftMIN, config.pointDriftMAX)
        config.pointInset = random.randint(config.pointInsetMIN, config.pointInsetMAX)

        config.sqrPt_A_Init = [CORNERPOINT_A[0] + config.pointInset, CORNERPOINT_A[1] + config.pointInset]
        config.sqrPt_B_Init = [CORNERPOINT_B[0] - config.pointInset, config.pointInset]
        config.sqrPt_C_Init = [CORNERPOINT_C[0] - config.pointInset, CORNERPOINT_C[1] - config.pointInset]
        config.sqrPt_D_Init = [config.pointInset, CORNERPOINT_D[1] - config.pointInset]

    i75.update()
    time.sleep(config.interval)
