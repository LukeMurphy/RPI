#!/usr/bin/python
import argparse
import itertools
import math
import random
import time
import types
from modules.configuration import bcolors
from modules import badpixels, coloroverlay, colorutils, panelDrawing
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps, ImageFilter
import numpy as np


def runningSpiral(config, paletteObj=None):
    # 16px grid box spiral for now
    w = 4
    h = 4
    x = config.xIncrementer
    y = config.yIncrementer

    clr = tuple(int(a * config.brightness) for a in (config.linecolOverlay.currentColor))

    clr2 = tuple(int(a * config.brightness) for a in (config.linecolOverlay2.currentColor))

    if paletteObj != None:
        clr3 = tuple(int(a) for a in (paletteObj.colOverlay.currentColor))
        clr = tuple(int(a) for a in (paletteObj.linecolOverlay.currentColor))
        clr2 = tuple(int(a) for a in (paletteObj.linecolOverlay2.currentColor))

    config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=config.bgColor, outline=None)

    lineMult = config.lineDiff * 2
    numLines = round(config.blockWidth / config.lineDiff * 2)

    d = 3
    direction = 1
    distance = 1

    mid = [config.blockWidth / 2 - 1, config.blockHeight / 2 - 1]

    p1 = [mid[0], mid[1]]
    p2 = [mid[0], mid[1]]

    # clr = (0,255,255)

    for _ in range(numLines):
        distance += d
        p2[0] = p2[0] + distance * direction
        config.blockDraw.line((p1[0], p1[1], p2[0], p2[1]), fill=clr)
        p1[0] = p2[0]
        distance += d
        p2[1] = p2[1] + distance * direction
        config.blockDraw.line((p1[0], p1[1], p2[0], p2[1]), fill=clr)
        direction *= -1
        p1[1] = p2[1]

    direction = -1
    distance = 1

    p1 = [mid[0] + 1, mid[1] + 3]
    p2 = [mid[0] + 1, mid[1] + 3]

    # clr2 = (255,0,255)
    for _ in range(numLines):
        distance += d
        p2[0] = p2[0] + distance * direction
        config.blockDraw.line((p1[0], p1[1], p2[0], p2[1]), fill=clr2)
        p1[0] = p2[0]
        distance += d
        p2[1] = p2[1] + distance * direction
        config.blockDraw.line((p1[0], p1[1], p2[0], p2[1]), fill=clr2)
        direction *= -1
        p1[1] = p2[1]


def balls(config, paletteObj=None):
    w = 4
    h = 4
    x = config.xIncrementer
    y = config.yIncrementer

    clr = tuple(int(a * config.brightness) for a in (config.linecolOverlay.currentColor))

    clr2 = tuple(int(a * config.brightness) for a in (config.linecolOverlay2.currentColor))

    if paletteObj != None:
        clr3 = tuple(int(a) for a in (paletteObj.colOverlay.currentColor))
        clr = tuple(int(a) for a in (paletteObj.linecolOverlay.currentColor))
        clr2 = tuple(int(a) for a in (paletteObj.linecolOverlay2.currentColor))

    config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=config.bgColor, outline=None)

    numRows = config.numDotRows
    boxWidth = config.blockWidth
    density = numRows * 4
    dotWidth = boxWidth / 2 / numRows - 2
    outline = None

    for r in range(numRows):

        for i in range(density):
            yPos = r * (dotWidth * 2) + r * 4
            config.blockDraw.ellipse(
                (i * 2 * boxWidth / density - boxWidth / density, yPos, i * 2 * boxWidth / density - boxWidth / density + dotWidth, yPos + dotWidth), outline=(outline), fill=clr
            )

        for i in range(density):
            config.blockDraw.ellipse(
                (i * 2 * boxWidth / density, yPos + 2 * boxWidth / density, i * 2 * boxWidth / density + dotWidth, yPos + 2 * boxWidth / density + dotWidth),
                outline=(outline),
                fill=clr,
            )


def circlesPacked(config, paletteObj=None):
    config.circlesPackedSize = 0.1
    clr = tuple(int(a * config.brightness) for a in (config.linecolOverlay.currentColor))

    clr2 = tuple(int(a * config.brightness) for a in (config.linecolOverlay2.currentColor))

    if paletteObj != None:
        clr3 = tuple(int(a) for a in (paletteObj.colOverlay.currentColor))
        clr = tuple(int(a) for a in (paletteObj.linecolOverlay.currentColor))
        clr2 = tuple(int(a) for a in (paletteObj.linecolOverlay2.currentColor))

    # config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=config.bgColor, outline=clr)

    numRows = config.numDotRows
    boxWidth = round(config.blockWidth * config.circlesPackedSize)
    dotWidth = boxWidth / 2
    outline = clr
    steps = 2
    yPos = 0
    numLines = config.blockWidth - 1
    for i in range(4):
        xPos = i * dotWidth * 1 - dotWidth / 2
        for r in range(0, numLines, steps):
            x0 = r - 1 + xPos
            y0 = r - 1 + yPos
            x1 = x0 + (dotWidth - 1) * r
            y1 = y0 + (dotWidth - 1) * r

            x1 = max(x1, x0)
            y1 = max(y1, y0)

            config.blockDraw.ellipse((x0, y0, x1, y1), outline=(outline), fill=clr3)

    yPos = 2 * dotWidth / 2 * math.sin(2 * math.pi / 6) + 2

    for i in range(4):
        xPos = i * dotWidth * 1
        for r in range(0, numLines, steps):
            x0 = r - 1 + xPos
            y0 = r - 1 + yPos
            x1 = x0 + (dotWidth - 1) * r
            y1 = y0 + (dotWidth - 1) * r

            x1 = max(x1, x0)
            y1 = max(y1, y0)

            # config.blockDraw.ellipse((x0,y0,x1,y1), outline=(outline), fill=config.bgColor)


def shingles(config, paletteObj=None):
    w = 4
    h = 4
    x = config.xIncrementer
    y = config.yIncrementer

    clr = tuple(int(a * config.brightness) for a in (config.linecolOverlay.currentColor))

    clr2 = tuple(int(a * config.brightness) for a in (config.linecolOverlay2.currentColor))

    clr2 = config.bgColor

    if paletteObj is not None:
        # print(f"paletteObj == {paletteObj.linecolOverlay.currentColor}")
        clr = tuple(int(a) for a in (paletteObj.colOverlay.currentColor))
        clr2 = tuple(int(a) for a in (paletteObj.linecolOverlay.currentColor))
        clr3 = tuple(int(a) for a in (paletteObj.linecolOverlay2.currentColor))

    config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=clr2, outline=None)

    numRows = config.numShingleRows
    boxWidth = config.blockWidth / numRows
    shingleWidth = config.blockWidth / numRows - config.shingleVariationAmount

    for r in range(numRows, -1, -1):
        yPos = -1 + r * boxWidth

        for i in range(3):
            config.blockDraw.rectangle((i * boxWidth - boxWidth / 2, yPos, i * boxWidth + shingleWidth - boxWidth / 2, yPos + boxWidth - 1), outline=(clr), fill=clr2)
        for i in range(2):
            config.blockDraw.rectangle((i * boxWidth, yPos - boxWidth / 2, i * boxWidth + shingleWidth, yPos + boxWidth / 2 - 1), outline=(clr), fill=clr2)


def fishScales(config, paletteObj=None):
    w = 4
    h = 4
    x = config.xIncrementer
    y = config.yIncrementer

    clr = tuple(int(a * config.brightness) for a in (config.linecolOverlay.currentColor))

    clr2 = tuple(int(a * config.brightness) for a in (config.linecolOverlay2.currentColor))

    clr3 = tuple(int(a * config.brightness) for a in (config.colOverlay.currentColor))

    if paletteObj != None:
        # print(f"paletteObj == {paletteObj.linecolOverlay.currentColor}")
        clr = tuple(int(a) for a in (paletteObj.colOverlay.currentColor))
        clr2 = tuple(int(a) for a in (paletteObj.linecolOverlay.currentColor))
        clr3 = tuple(int(a) for a in (paletteObj.linecolOverlay2.currentColor))

    config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=clr3, outline=None)

    numRows = config.numShingleRows
    boxWidth = config.blockWidth / numRows

    for r in range(numRows, -1, -1):
        yPos = -2 + r * boxWidth
        for i in range(3):
            config.blockDraw.ellipse((i * boxWidth - boxWidth / 2, yPos, i * boxWidth + boxWidth - boxWidth / 2, yPos + boxWidth), outline=(clr), fill=clr3)

        for i in range(2):
            config.blockDraw.ellipse((i * boxWidth, yPos - boxWidth / 2, i * boxWidth + boxWidth, yPos + boxWidth / 2), outline=(clr), fill=clr3)


def shellScales(config, paletteObj=None):
    clr, clr2, clr3 = _get_colors(config, paletteObj)

    config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=clr3, outline=None)

    numRows = config.numShingleRows
    boxWidth = config.blockWidth / numRows
    numLines = round(config.waveScaleRings * 1.0)
    numLinesHalf = round(numLines / 2)
    rads = math.pi * 2 / numLines
    radius = boxWidth / 2

    for r in range(numRows, -1, -1):
        yPos = -2 + r * boxWidth
        _draw_row_of_ellipses(config, yPos, boxWidth, clr, clr3, numLinesHalf, rads, radius, clr2)
        _draw_offset_row_of_ellipses(config, yPos, boxWidth, clr, clr3, numLinesHalf, rads, radius, clr2)


def _get_colors(config, paletteObj):
    clr = tuple(int(a * config.brightness) for a in config.linecolOverlay.currentColor)
    clr2 = tuple(int(a * config.brightness) for a in config.linecolOverlay2.currentColor)
    clr3 = tuple(int(a * config.brightness) for a in config.colOverlay.currentColor)

    if paletteObj is not None:
        clr = tuple(int(a) for a in paletteObj.linecolOverlay.currentColor)
        clr2 = tuple(int(a) for a in paletteObj.linecolOverlay2.currentColor)
        clr3 = tuple(int(a) for a in paletteObj.colOverlay.currentColor)
    return clr, clr2, clr3


def _draw_row_of_ellipses(config, yPos, boxWidth, clr, clr3, numLinesHalf, rads, radius, clr2):
    for i in range(3):
        config.blockDraw.ellipse((i * boxWidth - boxWidth / 2, yPos, i * boxWidth + boxWidth - boxWidth / 2, yPos + boxWidth), outline=clr, fill=clr3)

        for q in range(-numLinesHalf, numLinesHalf):
            angle = rads * q
            x0 = i * boxWidth
            y0 = yPos
            xP = i * boxWidth + radius * math.cos(angle)
            yP = yPos + boxWidth - boxWidth / 2 + radius * math.sin(angle)
            clrToUse = clr2 if q % 2 == 0 else clr
            config.blockDraw.line((x0, y0, xP, yP), fill=clrToUse)


def _draw_offset_row_of_ellipses(config, yPos, boxWidth, clr, clr3, numLinesHalf, rads, radius, clr2):
    for i in range(2):
        config.blockDraw.ellipse((i * boxWidth, yPos - boxWidth / 2, i * boxWidth + boxWidth, yPos + boxWidth / 2), outline=clr, fill=clr3)

        for q in range(-numLinesHalf, numLinesHalf):
            angle = rads * q
            x0 = i * boxWidth + boxWidth / 2
            y0 = yPos - boxWidth / 2
            xP = i * boxWidth + boxWidth / 2 + radius * math.cos(angle)
            yP = yPos + boxWidth - boxWidth + radius * math.sin(angle)  # Corrected yP calculation
            clrToUse = clr2 if q % 2 == 0 else clr
            config.blockDraw.line((x0, y0, xP, yP), fill=clrToUse)


def ellipses(config, paletteObj=None):
    clr, clr2, clr3 = _get_colors(config, paletteObj)
    config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=clr3, outline=None)

    numRows = 2
    boxWidth = 2 * config.blockWidth / numRows
    rings = config.waveScaleRings
    step = config.waveScaleSteps
    patternRows = numRows + 1

    if config.linesOnly:
        config.altLineColoring = False

    startFirstSet = 1 if config.altLineColoring and step != 2 else 0
    lineToUse = clr

    for r in range(patternRows, -patternRows, -1):
        yPos = -2 + r * boxWidth
        _draw_ellipse_set(config, yPos, boxWidth, rings, step, clr3, clr2, lineToUse)


def _draw_ellipse_set(config, yPos, boxWidth, rings, step, clr3, clr2, lineToUse):
    xOffSet = -boxWidth / 2
    yOffSet = boxWidth
    y = boxWidth / 4 - yPos / 2

    for i in range(3):
        xSizeOfBox = i * boxWidth
        for n in range(0, rings * step, step):  # Removed startFirstSet as it's always 0 here
            clrToUse = clr3 if not config.altLineColoring or n % 2 == 0 else clr2
            x0 = xSizeOfBox + xOffSet + n
            x1 = xSizeOfBox + xOffSet + boxWidth - n
            y0 = yPos + n + y - y  # Simplified y-coordinate calculation
            y1 = yPos + yOffSet - n

            x1 = max(x1, x0)
            y1 = max(y1, y0)
            config.blockDraw.ellipse((x0, y0, x1, y1), outline=lineToUse, fill=clrToUse)

    xOffSet = 0
    yOffSet /= 2
    y = boxWidth / 2 - yPos / 2

    for i in range(2):
        xSizeOfBox = i * boxWidth
        for n in range(rings * step, step):  # rings * step is always greater than step, resulting in an empty loop
            clrToUse = clr3 if not config.altLineColoring or n % 2 == 0 else clr2
            x0 = xSizeOfBox + xOffSet + n
            x1 = xSizeOfBox + xOffSet + boxWidth - n + 20
            y0 = yPos - yOffSet + n + y - y  # Simplified y-coordinate calculation
            y1 = yPos + yOffSet - n + y - y  # Simplified y-coordinate calculation

            x1 = max(x1, x0)
            y1 = max(y1, y0)
            config.blockDraw.ellipse((x0, y0, x1, y1), outline=lineToUse, fill=clrToUse)


def _get_colors(config, paletteObj):
    clr = tuple(int(a * config.brightness) for a in config.linecolOverlay.currentColor)
    clr2 = tuple(int(a * config.brightness) for a in config.linecolOverlay2.currentColor)
    clr3 = config.colOverlay.currentColor

    if paletteObj is not None:
        clr3 = tuple(int(a) for a in paletteObj.colOverlay.currentColor)
        clr = tuple(int(a) for a in paletteObj.linecolOverlay.currentColor)
        clr2 = tuple(int(a) for a in paletteObj.linecolOverlay2.currentColor)
    return clr, clr2, clr3


def waveScales(config, paletteObj=None):
    clr, clr2, clr3 = _get_colors(config, paletteObj)
    config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=clr3, outline=None)

    numRows = 2
    boxWidth = 2 * config.blockWidth / numRows
    rings = config.waveScaleRings
    step = config.waveScaleSteps
    patternRows = numRows + 1

    if config.linesOnly:
        config.altLineColoring = False

    lineToUse = clr

    for r in range(patternRows, -patternRows, -1):
        yPos = -2 + r * boxWidth
        _draw_wave_scale_set(config, yPos, boxWidth, rings, step, clr3, clr2, lineToUse)


def _draw_wave_scale_set(config, yPos, boxWidth, rings, step, clr3, clr2, lineToUse):
    xOffSet = -boxWidth / 2
    yOffSet = boxWidth
    y = boxWidth / 4 - yPos / 2

    for i in range(3):
        xSizeOfBox = i * boxWidth
        for n in range(0, rings * step, step):
            clrToUse = clr3 if not config.altLineColoring or n % 2 == 0 else clr2
            x0 = xSizeOfBox + xOffSet + n
            x1 = xSizeOfBox + xOffSet + boxWidth - n
            y0 = yPos + n + y
            y1 = yPos + yOffSet - n + y

            _draw_ellipse(config, x0, y0, x1, y1, lineToUse, clrToUse)

    xOffSet = 0
    yOffSet /= 2
    y = boxWidth / 2 - yPos / 2

    for i in range(2):
        xSizeOfBox = i * boxWidth
        for n in range(0, rings * step, step):
            clrToUse = clr3 if not config.altLineColoring or n % 2 == 0 else clr2
            x0 = xSizeOfBox + xOffSet + n
            x1 = xSizeOfBox + xOffSet + boxWidth - n
            y0 = yPos - yOffSet + n + y
            y1 = yPos + yOffSet - n + y

            _draw_ellipse(config, x0, y0, x1, y1, lineToUse, clrToUse)


def _draw_ellipse(config, x0, y0, x1, y1, lineToUse, clrToUse):
    x1 = max(x1, x0)
    y1 = max(y1, y0)
    config.blockDraw.ellipse((x0, y0, x1, y1), outline=lineToUse, fill=clrToUse)


def gothic1(config, paletteObj=None):
    clr, clr2, clr3 = _get_colors(config, paletteObj)

    config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=config.bgColor, outline=None)

    numLines = 1
    steps = 1
    _w = config.blockWidth / 2
    _h = config.blockHeight / 2

    _draw_circles(config, _w - _w / 2, 0, numLines, steps, clr, clr, clr, _w, _h)
    _draw_circles(config, _w - _w / 2, _h, numLines, steps, clr, clr, clr, _w, _h)
    _draw_circles(config, 0, _h - _h / 2, numLines, steps, clr, clr, clr, _w, _h)
    _draw_circles(config, _w, _h - _h / 2, numLines, steps, clr, clr, clr, _w, _h)


def circles(config, paletteObj=None):
    clr, clr2, clr3 = _get_colors(config, paletteObj)

    config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=config.bgColor, outline=None)

    numLines = config.blockWidth - 1
    steps = 3

    _draw_circles(config, 0, 0, numLines, steps, clr, clr2, clr3, config.blockWidth, config.blockHeight)

    for c in range(2):
        xOff = c * config.blockWidth - config.blockWidth / 2
        for r in range(2):
            yOff = r * config.blockHeight - config.blockHeight / 2
            _draw_circles(config, xOff, yOff, numLines, steps, clr, clr3, clr2, config.blockWidth, config.blockHeight)  # Swapped clr2 and clr3 for outline


def _draw_circles(config, xOff, yOff, numLines, steps, outlineClr, fillClr1, fillClr2, width, height):
    for i in range(0, numLines, steps):
        x1 = i - 1 + xOff
        y1 = i - 1 + yOff
        x2 = width - 1 * i + xOff
        y2 = height - 1 * i + yOff

        x2 = max(x2, x1 + 1)  # Ensure x2 is greater than or equal to x1 + 1
        y2 = max(y2, y1 + 1)  # Ensure y2 is greater than or equal to y1 + 1

        fillClr = fillClr1 if i % 2 == 0 else fillClr2
        config.blockDraw.ellipse((x1, y1, x2, y2), outline=(outlineClr), fill=fillClr)


def compass(config, paletteObj=None):
    clr = tuple(int(a * config.brightness) for a in (config.linecolOverlay.currentColor))
    clr2 = tuple(int(a * config.brightness) for a in (config.linecolOverlay2.currentColor))

    if paletteObj != None:
        clr3 = tuple(int(a) for a in (paletteObj.colOverlay.currentColor))
        clr = tuple(int(a) for a in (paletteObj.linecolOverlay.currentColor))
        clr2 = tuple(int(a) for a in (paletteObj.linecolOverlay2.currentColor))

    config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=config.bgColor, outline=None)

    count = 0
    barWidth = 4
    grid = round(config.blockWidth / 16)
    len1 = 5
    len2 = 2

    origins = (
        (0, 0),
        (config.blockWidth, 0),
        (round(config.blockWidth / 2), round(config.blockWidth / 2)),
        (0, config.blockWidth),
        (config.blockWidth, config.blockWidth),
    )

    outlineClr = None
    outlineClr = clr2
    for i in range(5):

        midx = origins[i][0]
        midy = origins[i][1]

        isoTriangle = (
            (midx - grid, midy),
            (midx, midy - len1 * grid),
            (midx + grid, midy),
            (midx, midy + len1 * grid),
            (midx - grid, midy),
        )
        config.blockDraw.polygon(isoTriangle, fill=clr, outline=outlineClr)
        isoTriangle = (
            (midx - grid * len1, midy),
            (midx, midy - grid),
            (midx + grid * len1, midy),
            (midx, midy + grid),
            (midx - grid * len1, midy),
        )
        config.blockDraw.polygon(isoTriangle, fill=clr, outline=outlineClr)
        isoTriangle = (
            (midx - grid * len2, midy - grid * len2),
            (midx, midy - grid),
            (midx + grid * len2, midy - grid * len2),
            (midx + grid, midy),
            (midx + grid * len2, midy + grid * len2),
            (midx, midy + grid),
            (midx - grid * len2, midy + grid * len2),
            (midx - grid, midy),
        )
        config.blockDraw.polygon(isoTriangle, fill=clr, outline=outlineClr)


def bars(config, paletteObj=None):
    clr = tuple(int(a * config.brightness) for a in (config.linecolOverlay.currentColor))
    clr2 = tuple(int(a * config.brightness) for a in (config.linecolOverlay2.currentColor))

    if paletteObj != None:
        clr3 = tuple(int(a) for a in (paletteObj.colOverlay.currentColor))
        clr = tuple(int(a) for a in (paletteObj.linecolOverlay.currentColor))
        clr2 = tuple(int(a) for a in (paletteObj.linecolOverlay2.currentColor))

    config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=config.bgColor, outline=None)

    count = 0
    barWidth = 4
    for i in range(0, config.numConcentricBoxes, 2):

        if config.altLineColoring == True:
            outClr = clr2
            if count % 2 == 0:
                outClr = clr
        else:
            outClr = clr
        config.blockDraw.rectangle((0, i * barWidth, config.blockWidth - 1, i * barWidth), outline=(outClr), fill=None)
        count += 1


def coloredBlocks(config, paletteObj=None):
    clr = tuple(int(a * config.brightness) for a in (config.linecolOverlay.currentColor))
    clr2 = tuple(int(a * config.brightness) for a in (config.linecolOverlay2.currentColor))

    if paletteObj != None:
        clr3 = tuple(int(a) for a in (paletteObj.colOverlay.currentColor))
        clr = tuple(int(a) for a in (paletteObj.linecolOverlay.currentColor))
        clr2 = tuple(int(a) for a in (paletteObj.linecolOverlay2.currentColor))

    config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=clr, outline=None)
    # config.blockDraw.rectangle((5, 5, 10, 15), fill=(255,0,0,255), outline=None)

    # count = 0
    # barWidth = 4
    # for i in range(config.numConcentricBoxes, 2):

    #     if config.altLineColoring == True:
    #         outClr = clr2
    #         if count % 2 == 0:
    #             outClr = clr
    #     else:
    #         outClr = clr

    #     outClr = None
    #     # config.blockDraw.rectangle((0,i * barWidth,config.blockWidth-1,i * barWidth), outline=(outClr), fill=None)
    #     count += 1


def concentricBoxes(config, paletteObj=None):

    clr = tuple(int(a * config.brightness) for a in (config.linecolOverlay.currentColor))
    clr2 = tuple(int(a * config.brightness) for a in (config.linecolOverlay2.currentColor))

    if paletteObj != None:
        clr3 = tuple(int(a) for a in (paletteObj.colOverlay.currentColor))
        clr = tuple(int(a) for a in (paletteObj.linecolOverlay.currentColor))
        clr2 = tuple(int(a) for a in (paletteObj.linecolOverlay2.currentColor))

    config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=config.bgColor, outline=None)

    count = 0

    for i in range(0, config.numConcentricBoxes, 2):

        if config.altLineColoring == True:
            outClr = clr2
            if count % 2 == 0:
                outClr = clr
        else:
            outClr = clr

        try:
            config.blockDraw.rectangle((i - 1, i - 1, config.blockWidth - 1 * i, config.blockHeight - 1 * i), outline=(outClr), fill=None)
            count += 1
        except Exception as e:
            print(f"Concentric boxes error prob too many {e}")


def decoBoxes(config, paletteObj=None):

    clr = tuple(int(a * config.brightness) for a in (config.linecolOverlay2.currentColor))
    clr2 = tuple(int(a * config.brightness) for a in (config.linecolOverlay.currentColor))

    if paletteObj != None:
        clr3 = tuple(int(a) for a in (paletteObj.colOverlay.currentColor))
        clr = tuple(int(a) for a in (paletteObj.linecolOverlay.currentColor))
        clr2 = tuple(int(a) for a in (paletteObj.linecolOverlay2.currentColor))

    config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=config.bgColor, outline=None)

    clr = config.bgColor
    numConcentricBoxes = config.blockWidth + 1
    altLineColoring = True
    w = round(random.uniform(2, 5))
    w = config.decoBoxBandWidth
    width = config.blockWidth

    blockWidth = width
    blockHeight = width
    halfSide = width / 2

    diagonal = round(math.sqrt(halfSide * halfSide * 2))
    diagonal = width

    temp = Image.new("RGBA", (width * 3, width * 3))
    tempDraw = ImageDraw.Draw(temp)

    temp2 = Image.new("RGBA", (width, width))
    temp2Draw = ImageDraw.Draw(temp2)

    # print(diagonal)

    for count, i in enumerate(range(1, numConcentricBoxes)):

        if altLineColoring:
            outClr = clr2
            if count % 2 == 0:
                outClr = clr
        else:
            outClr = clr

        x1 = width - w * i
        y1 = width - w * i

        y1 = max(y1, 0)
        x1 = max(x1, 0)
        temp2Draw.rectangle((0, 0, x1, y1), outline=(None), fill=outClr)
    for c, r in itertools.product(range(4), range(4)):
        # temp = temp.rotate(-45)
        xOff = c * w
        yOff = r * w
        temp.paste(temp2, (c * diagonal - xOff, r * diagonal - yOff), temp2)

    szFactor = 1 / 3
    temp = temp.rotate(
        135,
        expand=True,
    )
    # print(temp)
    ex = 12
    temp = temp.resize((round(width / szFactor) + ex, round(width / szFactor) + ex))

    # print(temp)
    # print('')

    xOff = -round(width / 1)
    yOff = -round(width / 1)

    config.blockImage.paste(temp, (xOff, yOff), temp)


def randomizer2(config, paletteObj=None):

    w = config.randomBlockWidth
    h = config.randomBlockHeight

    clr3 = tuple(int(a) for a in (paletteObj.colOverlay.currentColor))
    clr = tuple(int(a) for a in (paletteObj.linecolOverlay.currentColor))
    clr2 = tuple(int(a) for a in (paletteObj.linecolOverlay2.currentColor))

    config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=clr, outline=None)

    rows = config.blockHeight
    cols = config.blockWidth

    step = w
    hStep = h

    if w == 0:
        step = 1
    if h == 0:
        hStep = 1

    for r in range(0, rows, hStep):
        for c in range(0, cols, step):
            clr = colorutils.getRandomRGB(config.brightness / 2)
            if random.random() < config.randomBlockProb:
                config.blockDraw.rectangle((c, r, w + c, h + r), fill=(clr), outline=None)


def randomizer(config, paletteObj=None):

    w = config.randomBlockWidth
    h = config.randomBlockHeight

    config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=config.bgColor, outline=None)

    rows = config.blockHeight
    cols = config.blockWidth

    step = w
    hStep = h

    if w == 0:
        step = 1
    if h == 0:
        hStep = 1

    for r in range(0, rows, hStep):
        for c in range(0, cols, step):
            clr = colorutils.getRandomRGB(config.brightness / 2)
            if random.random() < config.randomBlockProb:
                config.blockDraw.rectangle((c, r, w + c, h + r), fill=(clr), outline=None)


def diamond(config, paletteObj=None):
    clr = tuple(int(a * config.brightness) for a in config.linecolOverlay.currentColor)
    clr2 = tuple(int(a * config.brightness) for a in config.colOverlay.currentColor)
    if paletteObj is not None:
        clr = tuple(int(a) for a in paletteObj.linecolOverlay.currentColor)
        clr2 = tuple(int(a) for a in paletteObj.colOverlay.currentColor)

    x = config.xIncrementer
    y = config.yIncrementer

    # needs to be in odd grid
    config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=config.bgColor, outline=None)

    step = config.diamondStep
    row = 1
    delta = 0
    w = 0
    h = 0
    rows = config.numRows
    blockHeight = round(config.blockHeight / rows)
    mid = round(blockHeight / 2)

    for rw in range(rows):
        for c in range(rows):
            for i in range(0, blockHeight, step * 2):
                for r in range(0, row, 1):
                    x = r + mid - row / 2 + c * blockHeight
                    y = i + config.yIncrementer + rw * blockHeight

                    if y >= blockHeight * rows:
                        y -= blockHeight * rows

                    if (r % 2) != 1:
                        config.blockDraw.rectangle((x, y, w + x, h + y), fill=(clr), outline=None)
                if config.diamondUseTriangles == False:
                    row = 2 * i + step + delta
                    if i > (blockHeight / 2):
                        row = round(2 * (blockHeight - i)) + delta
                        # delta += -2
                else:
                    row = i + step

    config.yIncrementer += config.ySpeed

    if config.yIncrementer >= blockHeight * 2:
        config.yIncrementer = 0


def diagonalMove(config, paletteObj=None):
    clr = (255, 0, 0, 210)

    if paletteObj != None:
        clr3 = tuple(int(a) for a in (paletteObj.colOverlay.currentColor))
        clr = tuple(int(a) for a in (paletteObj.linecolOverlay.currentColor))
        clr2 = tuple(int(a) for a in (paletteObj.linecolOverlay2.currentColor))

    w = 4
    h = 4
    x = config.xIncrementer
    y = config.yIncrementer

    config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=config.bgColor, outline=None)
    config.blockDraw.rectangle((x, y, w + x, h + y), fill=(clr), outline=None)
    config.xIncrementer += 1
    config.yIncrementer += 1

    if config.xIncrementer >= config.blockWidth - 4:
        config.xIncrementer = 0
    if config.yIncrementer >= config.blockHeight - 4:
        config.yIncrementer = 0


def reMove(config, paletteObj=None):

    w = 4
    h = 4
    x = config.xIncrementer
    y = config.yIncrementer

    bgColor = (config.bgColor[0], config.bgColor[1], config.bgColor[3], 255)

    clr = tuple(int(a * config.brightness) for a in (config.linecolOverlay.currentColor))
    clr2 = tuple(int(a * config.brightness) for a in (config.linecolOverlay2.currentColor))

    if paletteObj != None:
        clr3 = tuple(int(a) for a in (paletteObj.colOverlay.currentColor))
        clr = tuple(int(a) for a in (paletteObj.linecolOverlay.currentColor))
        clr2 = tuple(int(a) for a in (paletteObj.linecolOverlay2.currentColor))

    config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=config.bgColor, outline=None)

    lineMult = config.lineDiff * 2
    numLines = round(config.blockWidth / config.lineDiff * 2)

    y1 = 0
    for i in range(numLines):

        x1 = -2 * config.blockWidth + config.xIncrementer + i * lineMult
        x2 = -2 * config.blockWidth + config.blockWidth + config.xIncrementer + i * lineMult
        y2 = config.blockHeight

        config.blockDraw.line((x1, y1, x2, y2), fill=(clr))
        if config.useDoubleLine == True:
            config.blockDraw.line(
                (
                    -2 * config.blockWidth + config.xIncrementer + i * lineMult + 1,
                    0,
                    -2 * config.blockWidth + config.blockWidth + config.xIncrementer + i * lineMult + 1,
                    config.blockHeight,
                ),
                fill=(clr2),
            )

    config.xIncrementer += 0  # config.xSpeed
    config.yIncrementer += 0

    """
    """
    if config.xIncrementer > (config.blockWidth + 0):
        config.xIncrementer = -config.xSpeed
    if config.yIncrementer >= config.blockHeight - 4:
        config.yIncrementer = 0


def wavePattern(config, paletteObj=None):
    w = 4
    h = 4
    x = config.xIncrementer
    y = config.yIncrementer

    clr = tuple(int(a * config.brightness) for a in (config.linecolOverlay.currentColor))
    clr2 = tuple(int(a * config.brightness) for a in (config.linecolOverlay2.currentColor))
    if paletteObj != None:
        clr3 = tuple(int(a) for a in (paletteObj.colOverlay.currentColor))
        clr = tuple(int(a) for a in (paletteObj.linecolOverlay.currentColor))
        clr2 = tuple(int(a) for a in (paletteObj.linecolOverlay2.currentColor))

    config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=config.bgColor, outline=config.bgColor)

    numPoints = round(config.blockWidth)
    amplitude = config.amplitude
    yOffset = config.yOffset
    amplitude2 = config.amplitude2
    yOffset2 = config.yOffset2
    steps = config.steps
    steps2 = config.steps2
    rads = 2 * 22 / 7 / numPoints

    for i in range(0, numPoints, steps):
        angle = (i + config.xIncrementer) * rads
        angle2 = (i + config.xIncrementer + steps) * rads
        a = (i, math.sin(angle) * amplitude + yOffset)
        b = (i + steps, math.sin(angle) * amplitude + yOffset)
        c = (i + steps, math.sin(angle2) * amplitude + yOffset)

        if c[1] < a[1]:
            b = (i, math.sin(angle2) * amplitude + yOffset)
        config.blockDraw.polygon((a, b, c, a), fill=clr, outline=None)

    phase = round(config.blockWidth / config.phaseFactor)
    for i in range(0, numPoints, steps2):
        angle = (i - config.speedFactor * config.xIncrementer + phase) * rads
        angle2 = (i - config.speedFactor * config.xIncrementer + phase + steps2) * rads
        a = (i, math.cos(angle) * amplitude2 + yOffset2)
        b = (i + steps2, math.cos(angle) * amplitude2 + yOffset2)
        c = (i + steps2, math.cos(angle2) * amplitude2 + yOffset2)

        if c[1] < a[1]:
            b = (i, math.cos(angle2) * amplitude2 + yOffset2)
        config.blockDraw.polygon((a, b, c, a), fill=clr2, outline=None)

    config.xIncrementer += config.xSpeed
    config.yIncrementer += config.ySpeed

    if config.xIncrementer >= config.blockWidth * 1:
        config.xIncrementer = -0
    if config.yIncrementer >= config.blockHeight - 4:
        config.yIncrementer = 0


def wavePattern2(config, paletteObj=None):
    w = 4
    h = 4
    x = config.xIncrementer
    y = config.yIncrementer

    clr = tuple(int(a * config.brightness) for a in (config.linecolOverlay.currentColor))
    clr2 = tuple(int(a * config.brightness) for a in (config.linecolOverlay2.currentColor))

    if paletteObj != None:
        clr3 = tuple(int(a) for a in (paletteObj.colOverlay.currentColor))
        clr = tuple(int(a) for a in (paletteObj.linecolOverlay.currentColor))
        clr2 = tuple(int(a) for a in (paletteObj.linecolOverlay2.currentColor))

    config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=config.bgColor, outline=config.bgColor)

    numPoints = round(config.blockWidth)
    amplitude = config.amplitude
    yOffset = config.yOffset
    amplitude2 = config.amplitude2
    yOffset2 = config.yOffset2
    steps = config.steps
    steps2 = config.steps2
    rads = 2 * 22 / 7 / numPoints

    for iy in range(-numPoints, numPoints * 2, steps * 2):
        for i in range(0, numPoints, steps):
            angle = (i + config.xIncrementer) * rads
            angle2 = (i + config.xIncrementer + steps) * rads
            a = (i, math.sin(angle) * amplitude + yOffset + iy)
            b = (i + steps, math.sin(angle) * amplitude + yOffset + iy)
            c = (i + steps, math.sin(angle2) * amplitude + yOffset + iy)
            c2 = (i + steps, math.sin(angle2) * amplitude + yOffset + iy + 1)

            if c[1] < a[1]:
                b = (i, math.sin(angle2) * amplitude + yOffset)
            # config.blockDraw.polygon((a, b, c, a), fill=None, outline=clr)
            config.blockDraw.line((a, c), fill=clr)
            config.blockDraw.line((a, c2), fill=clr)

    # phase = round(config.blockWidth/config.phaseFactor)
    # for i in range(0, numPoints, steps2):
    #     angle = (i - config.speedFactor*config.xIncrementer + phase) * rads
    #     angle2 = (i - config.speedFactor *
    #               config.xIncrementer + phase + steps2) * rads
    #     a = (i, math.cos(angle) * amplitude2 + yOffset2)
    #     b = (i + steps2, math.cos(angle) * amplitude2 + yOffset2)
    #     c = (i + steps2, math.cos(angle2) * amplitude2 + yOffset2)

    #     if c[1] < a[1]:
    #         b = (i, math.cos(angle2) * amplitude2 + yOffset2)
    #     config.blockDraw.polygon((a, b, c, a), fill=clr2, outline=None)

    # config.xIncrementer += config.xSpeed
    # config.yIncrementer += config.ySpeed

    if config.xIncrementer >= config.blockWidth * 1:
        config.xIncrementer = -0
    if config.yIncrementer >= config.blockHeight - 4:
        config.yIncrementer = 0
