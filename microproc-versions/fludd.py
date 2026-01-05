import time
import os
import random
import gc
from interstate75 import Interstate75, DISPLAY_INTERSTATE75_64X64


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


# Setup for the display
i75 = Interstate75(display=DISPLAY_INTERSTATE75_64X64)
display = i75.display

# ---------- SETTINGS ---------------#
INTERVAL = 0.05
activeAnim = 0
changeAnimProb = 0.003
changeAnimProbBase = 0.003

CORNERPOINT_A = [0, -1]
CORNERPOINT_B = [64, -1]
CORNERPOINT_C = [64, 63]
CORNERPOINT_D = [0, 63]

# drift 
POINTDRIFT = 1
POINTDRIFTMIN = 1
POINTDRIFTMAX = 2
# inset from sides
POINTINSET = 2
POINTINSETMIN = 1
POINTINSETMAX = 3

SQRPT_A_INIT = [CORNERPOINT_A[0] + POINTINSET, CORNERPOINT_A[1] + POINTINSET]
SQRPT_B_INIT = [CORNERPOINT_B[0] - POINTINSET, POINTINSET]
SQRPT_C_INIT = [CORNERPOINT_C[0]- POINTINSET, CORNERPOINT_C[1]- POINTINSET]
SQRPT_D_INIT = [POINTINSET, CORNERPOINT_D[1] - POINTINSET]

SQRPT_A = [4, 4]
SQRPT_B = [60, 4]
SQRPT_C = [60, 60]
SQRPT_D = [4, 60]


shp1 = [CORNERPOINT_A, CORNERPOINT_B, SQRPT_B, SQRPT_A]
shp2 = [CORNERPOINT_B, CORNERPOINT_C, SQRPT_C, SQRPT_B]
shp3 = [CORNERPOINT_D, CORNERPOINT_C, SQRPT_C, SQRPT_D]
shp4 = [CORNERPOINT_A, CORNERPOINT_D, SQRPT_D, SQRPT_A]

# shapeArray = [shp2]
shapeArray = [shp1, shp2, shp3, shp4]


clr = changeColor(45 / 360, 45 / 360, 1.50, 1.0, 0.0, 0.0)
bgClr = display.create_pen_hsv(clr[0], clr[1], clr[2])

fgMinHue = 350 / 360
fgMaxHue = 0 / 360
fgMinSat = 0.5
fgMaxSat = 0.5
fgMinVal = 0.47
fgMaxVal = 0.47

clr = changeColor(fgMinHue, fgMaxHue, fgMinSat, fgMaxSat, fgMinVal, fgMaxVal)
fgClr = display.create_pen_hsv(clr[0], clr[1], clr[2])

display.set_pen(bgClr)
display.clear()

while True:
    # bgClr.clrStep()
    # Bg = display.create_pen_hsv(bgClr.h, bgClr.s, bgClr.v)
    display.set_pen(bgClr)
    display.clear()

    # fgClr.clrStep()
    # ForeG = display.create_pen_hsv(fgClr.h, fgClr.s, fgClr.v)
    display.reset_pen(fgClr)
    display.set_pen(fgClr)

    display.polygon([tuple(CORNERPOINT_A), tuple(CORNERPOINT_B), tuple(SQRPT_B), tuple(SQRPT_A), tuple(CORNERPOINT_A)])
    display.polygon([tuple(CORNERPOINT_B), tuple(CORNERPOINT_C), tuple(SQRPT_C), tuple(SQRPT_B), tuple(CORNERPOINT_B)])
    display.polygon([tuple(CORNERPOINT_D), tuple(CORNERPOINT_C), tuple(SQRPT_C), tuple(SQRPT_D), tuple(CORNERPOINT_D)])
    display.polygon([tuple(CORNERPOINT_A), tuple(CORNERPOINT_D), tuple(SQRPT_D), tuple(SQRPT_A), tuple(CORNERPOINT_A)])

    clr = changeColor(fgMinHue, fgMaxHue, fgMinSat, fgMaxSat, fgMinVal, fgMaxVal)
    fgClr = display.create_pen_hsv(clr[0], clr[1], clr[2])

    SQRPT_A = [random.randint(SQRPT_A_INIT[0] - POINTDRIFT, SQRPT_A_INIT[0] + POINTDRIFT), random.randint(SQRPT_A_INIT[1] - POINTDRIFT, SQRPT_A_INIT[1] + POINTDRIFT)]
    SQRPT_B = [random.randint(SQRPT_B_INIT[0] - POINTDRIFT, SQRPT_B_INIT[0] + POINTDRIFT), random.randint(SQRPT_B_INIT[1] - POINTDRIFT, SQRPT_B_INIT[1] + POINTDRIFT)]
    SQRPT_C = [random.randint(SQRPT_C_INIT[0] - POINTDRIFT, SQRPT_C_INIT[0] + POINTDRIFT), random.randint(SQRPT_C_INIT[1] - POINTDRIFT, SQRPT_C_INIT[1] + POINTDRIFT)]
    SQRPT_D = [random.randint(SQRPT_D_INIT[0] - POINTDRIFT, SQRPT_D_INIT[0] + POINTDRIFT), random.randint(SQRPT_D_INIT[1] - POINTDRIFT, SQRPT_D_INIT[1] + POINTDRIFT)]


    if random.random() < changeAnimProb:
        if gc.mem_free() < 3000:
            gc.collect()

        POINTDRIFT = random.randint(POINTDRIFTMIN,POINTDRIFTMAX)
        POINTINSET = random.randint(POINTINSETMIN,POINTINSETMAX)

        SQRPT_A_INIT = [CORNERPOINT_A[0] + POINTINSET, CORNERPOINT_A[1] + POINTINSET]
        SQRPT_B_INIT = [CORNERPOINT_B[0] - POINTINSET, POINTINSET]
        SQRPT_C_INIT = [CORNERPOINT_C[0]- POINTINSET, CORNERPOINT_C[1]- POINTINSET]
        SQRPT_D_INIT = [POINTINSET, CORNERPOINT_D[1] - POINTINSET]

        clrMode = random.choice([1,2,3])
        
        if clrMode ==1 :
            fgMinHue = 0
            fgMaxHue = 1.0
            fgMinSat = 0.5
            fgMaxSat = 0.5
            INTERVAL = random.uniform(.04,.070)
            fgMinVal = .4
            fgMaxVal = .7
        elif clrMode == 2 :
            fgMinSat = 0.0
            fgMaxSat = 0.05 
            fgMinVal = .4
            fgMaxVal = .8
            INTERVAL = random.uniform(.04,.10)
        elif clrMode == 3 :
            fgMinHue = 0
            fgMaxHue = 50/360
            fgMinSat = 0.60
            fgMaxSat = 1.0 
            fgMinVal = .4
            fgMaxVal = .7
            INTERVAL = random.uniform(.03,.07)

        changeAnimProb = changeAnimProbBase * INTERVAL / .03
        print(INTERVAL, changeAnimProb)

    i75.update()
    time.sleep(INTERVAL)