# ################################################### #
import argparse
from logging import config
import math
import random
import time
import types
import noise
from noise import *
from modules.configuration import bcolors
from modules import badpixels, coloroverlay, colorutils, panelDrawing
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps

import numpy as np

lastRate = 0
colorutils.brightness = 1


def R(a, b, rounded=False):
    if not rounded:
        return random.uniform(a, b)
    else:
        return round(random.uniform(a, b))


def catmull_rom(p0, p1, p2, p3, t):
    t2 = t * t
    t3 = t2 * t

    return 0.5 * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3)


def generateRawLine(points=20, horiz=True):
    pts = []
    pointSpacing = (config.canvasWidth - 1 * config.xOffset) / points

    for i in range(points):
        x = i * pointSpacing
        y = R(-config.noiseAmplitude, config.noiseAmplitude)
        if horiz:
            pts.append((round(x), round(y)))
        else:
            pts.append((round(y), round(x)))

    # ensures the last point at the right or bottom closes the box
    if horiz:
        pts.append([config.canvasWidth - 2 * config.xOffset, y])
    else:
        pts.append([y, config.canvasWidth - 2 * config.xOffset])
    # Extra points for smoother Bézier start/end
    # pts.insert(0, pts[0])
    return pts


def getCurvePoints(points, resolution=50):

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


def generateInformalLine(pts=20, xOffset=0, yOffset=0, horiz=True):
    points = generateRawLine(pts, horiz)
    _curvedPoints = getCurvePoints(points, config.curveResolution)
    _smoothPointsForDrawing = []
    _smoothPointsForDrawing.extend((pt[0] + xOffset, pt[1] + yOffset) for pt in _curvedPoints)
    return _smoothPointsForDrawing


def getColor(r, g, b, a):
    clr = list(round(i * config.brightness) for i in [r, g, b])
    clr.append(a)
    return tuple(clr)


def reDraw():
    if config.function == "hashlines":
        hashlines()
    if config.function == "hashlines2":
        hashlines2()
    if random.random() < config.changeLinesProb:
        config.lightMode = False if random.random() > config.lightModeProb else True
        resetLines()


def hashlines2():
    global config
    config.draw.rectangle((0, 0, 500, 500), fill=config.bgColor)
    if random.random() < 1:
        config.noiseSeed = random.random()
    _fillColor = getColor(config.lineColor[0], config.lineColor[1], config.lineColor[2], config.line_alpha)

    # for row in range(0, config.canvasHeight - 2 * config.yOffset + config.rowAndColAdj, config.rowInterval):
    rowSpacing = (config.canvasHeight - 2 * config.yOffset + config.rowAndColAdj) / config.rowInterval
    colSpacing = (config.canvasWidth - 2 * config.xOffset + config.rowAndColAdj) / config.colInterval

    for row in range(config.rowInterval + config.rowAndColAdj):
        pts = generateInformalLine(config.pointsPerLine, config.xOffset, config.yOffset + rowSpacing * row)
        lastPt = [pts[0][0], pts[0][1]]
        for pt in pts:
            config.draw.line((lastPt[0], lastPt[1], pt[0], pt[1]), fill=_fillColor, width=1)
            lastPt = [pt[0], pt[1]]

    for col in range(config.colInterval + config.rowAndColAdj):
        pts = generateInformalLine(config.pointsPerLine, config.xOffset + colSpacing * col, config.yOffset, False)
        lastPt = [pts[0][0], pts[0][1]]
        for pt in pts:
            config.draw.line((lastPt[0], lastPt[1], pt[0], pt[1]), fill=_fillColor, width=1)
            lastPt = [pt[0], pt[1]]

    # config.scroll += config.scrollRate


def hashlines():
    global config
    config.draw.rectangle((0, 0, 500, 500), fill=config.bgColor)
    if random.random() < 1:
        config.noiseSeed = random.random()

    lastx = [0, 0, 0]
    lasty = [0, 0, 0]
    _fillColor = getColor(config.lineColor[0], config.lineColor[1], config.lineColor[2], config.line_alpha)

    for col in range(0, config.canvasWidth - 2 * config.xOffset, config.colInterval):
        lasty = [0, 0, 0]
        lineWidth = random.choice([0, 1])

        for row in range(0, config.canvasHeight - 2 * config.yOffset, config.rowInterval):
            y = row
            x = round(noise.pnoise2((col + config.scroll), y / (10 * config.noiseSeed) + config.scroll, 2) * config.noiseAmplitude + col)
            lineWidth = random.choice([0, 1])

            config.draw.line(
                (lastx[0] + config.xOffset, lasty[0] + config.yOffset, x + config.xOffset, y + config.yOffset),
                fill=_fillColor,
                width=lineWidth,
            )

            # config.draw.line(
            #     (col + config.xOffset, row + config.yOffset, config.canvasWidth - 2 * config.xOffset, row + config.yOffset),
            #     fill=_fillColor,
            #     width=lineWidth,
            # )
            config.draw.line(
                (lasty[0] + config.yOffset, lastx[0] + config.xOffset, y + config.yOffset, x + config.xOffset),
                fill=getColor(config.lineColor[0], config.lineColor[1], config.lineColor[2], config.line_alpha),
                width=lineWidth,
            )

            lastx = [x, x, x]
            lasty = [y, y, y]
        # octv += 1
    config.scroll += config.scrollRate


def resetLines():
    config.colInterval = random.randint(int(config.rowAndColIntervalRange[0]), int(config.rowAndColIntervalRange[1]))
    config.rowInterval = random.randint(int(config.rowAndColIntervalRange[0]), int(config.rowAndColIntervalRange[1]))
    config.noiseAmplitude = random.uniform(float(config.noiseAmplitudeRange[0]), float(config.noiseAmplitudeRange[1]))
    setLineColor()
    setBGColor()


def runWork():
    global config
    print(bcolors.OKGREEN + "** " + bcolors.BOLD)
    print("Running noisescroller.py")
    print(bcolors.ENDC)

    config.draw.rectangle((0, 0, config.canvasWidth, config.canvasHeight), fill=config.bgColor)

    while config.isRunning == True:
        iterate()
        time.sleep(config.redrawSpeed)
        if config.standAlone == False:
            config.callBack()


def setLineColor():
    _minVal = 0.0
    _maxVal = 0.1
    if config.lightMode:
        _minVal = 0.65
        _maxVal = 1.0

    config.lineColor = colorutils.getRandomColorHSV(
        config.line_minHue,
        config.line_maxHue,
        config.line_minSaturation,
        config.line_maxSaturation,
        _minVal,
        _maxVal,
        0,
        0,
        config.line_alpha,
        config.brightness,
    )


def setBGColor():
    _minVal = 0.5
    _maxVal = 1.0
    if config.lightMode:
        _minVal = 0.0
        _maxVal = 0.1
    config.bgColor = colorutils.getRandomColorHSV(
        config.bg_minHue, config.bg_maxHue, config.bg_minSaturation, config.bg_maxSaturation, _minVal, _maxVal, 0, 0, config.bg_alpha, config.brightness
    )


def iterate():
    reDraw()

    ########### RENDERING AS A MOCKUP OR AS REAL ###########
    if config.useDrawingPoints == True:
        config.panelDrawing.canvasToUse = config.image
        config.panelDrawing.render()
    else:
        config.render(config.image, 0, 0, config.canvasWidth, config.canvasHeight)
    # Done


def main(run=True):
    global config
    global workConfig
    config.image = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.canvasImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.draw = ImageDraw.Draw(config.image)
    config.lightMode = True

    config.pointsPerLine = int(workConfig.get("noisescroller", "pointsPerLine"))
    config.rowAndColAdj = int(workConfig.get("noisescroller", "rowAndColAdj"))

    config.redrawSpeed = float(workConfig.get("noisescroller", "redrawSpeed"))
    config.noiseAmplitude = float(workConfig.get("noisescroller", "noiseAmplitude"))
    config.curveResolution = int(workConfig.get("noisescroller", "curveResolution", fallback=10))
    config.noiseSeed = random.random()

    config.xOffset = int(workConfig.get("noisescroller", "xOffset"))
    config.yOffset = int(workConfig.get("noisescroller", "yOffset"))

    config.scroll = 0
    config.scrollRate = float(workConfig.get("noisescroller", "scrollRate"))
    config.lightModeProb = float(workConfig.get("noisescroller", "lightModeProb", fallback=1.0))
    config.changeLinesProb = float(workConfig.get("noisescroller", "changeLinesProb", fallback=0.01))
    config.rowInterval = int(workConfig.get("noisescroller", "rowInterval"))
    config.colInterval = int(workConfig.get("noisescroller", "colInterval"))
    config.function = workConfig.get("noisescroller", "function")
    config.rowAndColIntervalRange = workConfig.get("noisescroller", "rowAndColIntervalRange", fallback="20,20").split(",")
    config.noiseAmplitudeRange = workConfig.get("noisescroller", "noiseAmplitudeRange", fallback="1,4").split(",")

    config.line_minHue = float(workConfig.get("noisescroller", "line_minHue"))
    config.line_maxHue = float(workConfig.get("noisescroller", "line_maxHue"))
    config.line_maxSaturation = float(workConfig.get("noisescroller", "line_maxSaturation"))
    config.line_minSaturation = float(workConfig.get("noisescroller", "line_minSaturation"))
    config.line_maxValue = float(workConfig.get("noisescroller", "line_maxValue"))
    config.line_minValue = float(workConfig.get("noisescroller", "line_minValue"))
    config.line_alpha = int(workConfig.get("noisescroller", "line_alpha"))

    config.bg_minHue = float(workConfig.get("noisescroller", "bg_minHue"))
    config.bg_maxHue = float(workConfig.get("noisescroller", "bg_maxHue"))
    config.bg_maxSaturation = float(workConfig.get("noisescroller", "bg_maxSaturation"))
    config.bg_minSaturation = float(workConfig.get("noisescroller", "bg_minSaturation"))
    config.bg_maxValue = float(workConfig.get("noisescroller", "bg_maxValue"))
    config.bg_minValue = float(workConfig.get("noisescroller", "bg_minValue"))
    config.bg_alpha = int(workConfig.get("noisescroller", "bg_alpha"))

    setLineColor()
    setBGColor()

    ### THIS IS USED AS WAY TO MOCKUP A CONFIGURATION OF RECTANGULAR PANELS
    panelDrawing.mockupBlock(config, workConfig)
    #### Need to add something like this at final render call  as well
    """ 
        ########### RENDERING AS A MOCKUP OR AS REAL ###########
        if config.useDrawingPoints == True :
            config.panelDrawing.canvasToUse = config.renderImageFull
            config.panelDrawing.render()
        else :
            #config.render(config.canvasImage, 0, 0, config.canvasWidth, config.canvasHeight)
            #config.render(config.image, 0, 0)
            config.render(config.renderImageFull, 0, 0)
    """
    if run:
        runWork()
