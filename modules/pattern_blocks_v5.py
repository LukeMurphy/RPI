#!/usr/bin/python
import itertools
import math
import random

from modules.configuration import pieceLogger
from modules.configuration import ArtWorkConfig
from modules import colorutils
from PIL import Image, ImageDraw
import numpy as np
import noise
from noise import *

"""
Current List 2025-10-6
fishScales3
fishScales2
fishScales
gothic1
gothic2
balls
balls_hili
compass
compass_hili
randomizer
randomizer2
randomizer3
wavePattern
logcabin
logcabinAlt1
logcabinAlt2
ropePattern
wavePattern2
runningSpiral
chainLinks
circlesPacked
shingles
shellScales
ellipses
waveScales
circles
tripart
bars
peaceCross
fiboSeq
logcabin
littleCones
coloredBlocks
concentricBoxes
decoBoxes
diamond
diagonalMove
reMove
grainLines
colorGrid
colorGridTriangles
floralConfig
petals

addint TVPaletteTest

"""


def fishscalepatternFunction(func):
    """Decorator for fish scale pattern drawing functions.
    This decorator wraps a function that returns drawing parameters for a fish scale pattern, and performs the drawing using those parameters. It abstracts the common drawing logic for fish scale patterns, allowing the decorated function to focus on color and configuration selection.
    Args:
        func: A function that returns a tuple containing (refConfig, bgFill, patternFill, patternOutLine, hilight).
    Returns:
        A wrapper function that executes the drawing logic for the fish scale pattern.
    """

    def wrapper(*args):
        res = func(*args)
        refConfig = res[0]
        bgFill = res[1]
        patternFill = res[2]
        patternOutLine = res[3]
        hilight = res[4]
        w = 4
        h = 4
        x = refConfig.xIncrementer
        y = refConfig.yIncrementer

        refConfig.blockDraw.rectangle((0, 0, refConfig.blockWidth, refConfig.blockHeight), fill=bgFill, outline=None)

        numRows = refConfig.numShingleRows
        boxWidth = refConfig.blockWidth / numRows

        for r in range(numRows, -1, -1):
            yPos = -2 + r * boxWidth
            for i in range(3):
                refConfig.blockDraw.ellipse((i * boxWidth - boxWidth / 2, yPos, i * boxWidth + boxWidth - boxWidth / 2, yPos + boxWidth), outline=(patternOutLine), fill=patternFill)

            for i in range(2):
                refConfig.blockDraw.ellipse((i * boxWidth, yPos - boxWidth / 2, i * boxWidth + boxWidth, yPos + boxWidth / 2), outline=(patternOutLine), fill=patternFill)

    return wrapper


@fishscalepatternFunction
def fishScales3(refConfig, paletteObj):
    """Generates parameters for a fish scale pattern using the provided palette.
    Returns the configuration and color values needed to draw a fish scale pattern with the specified palette object.
    Args:
        refConfig: The configuration object containing drawing parameters.
        paletteObj: The palette object providing color values.
    Returns:
        A tuple containing (refConfig, bgFill, patternFill, patternOutLine, hilight).
    """
    # return "A","B","C"
    bgFill = tuple(int(a) for a in (paletteObj.c1.currentColor))
    patternFill = tuple(int(a) for a in (paletteObj.c1.currentColor))
    patternOutLine = tuple(int(a) for a in (paletteObj.c4.currentColor))
    hilight = tuple(int(a) for a in (paletteObj.c4.currentColor))
    return refConfig, bgFill, patternFill, patternOutLine, hilight


@fishscalepatternFunction
def fishScales2(refConfig, paletteObj):
    # return "B","C","A"
    bgFill = tuple(int(a) for a in (paletteObj.c1.currentColor))
    patternFill = tuple(int(a) for a in (paletteObj.c2.currentColor))
    patternOutLine = tuple(int(a) for a in (paletteObj.c1.currentColor))
    hilight = tuple(int(a) for a in (paletteObj.c4.currentColor))
    return refConfig, bgFill, patternFill, patternOutLine, hilight


@fishscalepatternFunction
def fishScales(refConfig, paletteObj):
    # return "B","C","A"
    bgFill = tuple(int(a) for a in (paletteObj.c3.currentColor))
    patternFill = tuple(int(a) for a in (paletteObj.c3.currentColor))
    patternOutLine = tuple(int(a) for a in (paletteObj.c1.currentColor))
    hilight = tuple(int(a) for a in (paletteObj.c4.currentColor))
    return refConfig, bgFill, patternFill, patternOutLine, hilight


# --------------------------------------- #


def gothicPatternFunction(func):
    def wrapper(*args):
        res = func(*args)
        refConfig = res[0]
        bgFill = res[1]
        patternFill = res[2]
        patternOutLine = res[3]
        hilight = res[4]
        w = 4
        h = 4
        x = refConfig.xIncrementer
        y = refConfig.yIncrementer

        refConfig.blockDraw.rectangle((0, 0, refConfig.blockWidth, refConfig.blockHeight), fill=bgFill, outline=None)

        numLines = 1
        steps = 1
        _w = refConfig.blockWidth / 2
        _h = refConfig.blockHeight / 2

        _draw_circles(refConfig, _w - _w / 2, 0, numLines, steps, patternFill, patternFill, patternFill, _w, _h)
        _draw_circles(refConfig, _w - _w / 2, _h, numLines, steps, patternFill, patternFill, patternFill, _w, _h)
        _draw_circles(refConfig, 0, _h - _h / 2, numLines, steps, patternFill, patternFill, patternFill, _w, _h)
        _draw_circles(refConfig, _w, _h - _h / 2, numLines, steps, patternFill, patternFill, patternFill, _w, _h)

    return wrapper


@gothicPatternFunction
def gothic1(refConfig, paletteObj):
    # return "A","B","C"
    bgFill = tuple(int(a) for a in (paletteObj.c1.currentColor))
    patternFill = tuple(int(a) for a in (paletteObj.c2.currentColor))
    patternOutLine = tuple(int(a) for a in (paletteObj.c4.currentColor))
    hilight = tuple(int(a) for a in (paletteObj.c4.currentColor))
    return refConfig, bgFill, patternFill, patternOutLine, hilight


@gothicPatternFunction
def gothic2(refConfig, paletteObj):
    # return "B","C","A"
    bgFill = tuple(int(a) for a in (paletteObj.c1.currentColor))
    patternFill = tuple(int(a) for a in (paletteObj.c4.currentColor))
    patternOutLine = tuple(int(a) for a in (paletteObj.c1.currentColor))
    hilight = tuple(int(a) for a in (paletteObj.c4.currentColor))
    return refConfig, bgFill, patternFill, patternOutLine, hilight


# --------------------------------------- #


def ballsPatternFunction(func):
    def wrapper(*args):
        res = func(*args)
        refConfig = res[0]
        bgFill = res[1]
        patternFill = res[2]
        patternOutLine = res[3]
        hilight = res[4]
        w = 4
        h = 4
        x = refConfig.xIncrementer
        y = refConfig.yIncrementer

        refConfig.blockDraw.rectangle((0, 0, refConfig.blockWidth, refConfig.blockHeight), fill=bgFill, outline=None)

        numRows = refConfig.numDotRows
        boxWidth = refConfig.blockWidth
        density = numRows * 4
        dotWidth = boxWidth / 2 / numRows - 2
        outline = None

        if len(res) > 5:
            offset = res[5]
            density = numRows * 2
        else:
            offset = boxWidth

        for r in range(numRows):

            for i in range(density):
                yPos = r * (dotWidth * 2) + r * 4
                refConfig.blockDraw.ellipse(
                    (i * 2 * boxWidth / density - offset / density, yPos, i * 2 * boxWidth / density - offset / density + dotWidth, yPos + dotWidth),
                    outline=(outline),
                    fill=patternFill,
                )

            for i in range(density):
                refConfig.blockDraw.ellipse(
                    (i * 2 * boxWidth / density, yPos + 2 * boxWidth / density, i * 2 * boxWidth / density + dotWidth, yPos + 2 * boxWidth / density + dotWidth),
                    outline=(outline),
                    fill=patternFill,
                )

    return wrapper


@ballsPatternFunction
def balls(refConfig, paletteObj):
    # return "A","B","C"
    bgFill = tuple(int(a) for a in (paletteObj.c1.currentColor))
    patternFill = tuple(int(a) for a in (paletteObj.c2.currentColor))
    patternOutLine = tuple(int(a) for a in (paletteObj.c4.currentColor))
    hilight = tuple(int(a) for a in (paletteObj.c4.currentColor))
    return refConfig, bgFill, patternFill, patternOutLine, hilight


@ballsPatternFunction
def ballsRegularDots(refConfig, paletteObj):
    # return "A","B","C"
    bgFill = tuple(int(a) for a in (paletteObj.c1.currentColor))
    patternFill = tuple(int(a) for a in (paletteObj.c2.currentColor))
    patternOutLine = tuple(int(a) for a in (paletteObj.c4.currentColor))
    hilight = tuple(int(a) for a in (paletteObj.c4.currentColor))
    offset = 0
    return refConfig, bgFill, patternFill, patternOutLine, hilight, offset


@ballsPatternFunction
def balls_hili(refConfig, paletteObj):
    # return "B","C","A"
    bgFill = tuple(int(a) for a in (paletteObj.c1.currentColor))
    patternFill = tuple(int(a) for a in (paletteObj.c4.currentColor))
    patternOutLine = tuple(int(a) for a in (paletteObj.c1.currentColor))
    hilight = tuple(int(a) for a in (paletteObj.c4.currentColor))
    return refConfig, bgFill, patternFill, patternOutLine, hilight


# --------------------------------------- #


def compassPatternFunction(func):
    def wrapper(*args):
        res = func(*args)
        refConfig = res[0]
        bgFill = res[1]
        patternFill = res[2]
        patternOutLine = res[3]
        hilight = res[4]
        w = 4
        h = 4
        x = refConfig.xIncrementer
        y = refConfig.yIncrementer

        refConfig.blockDraw.rectangle((0, 0, refConfig.blockWidth, refConfig.blockHeight), fill=bgFill, outline=None)

        count = 0
        barWidth = 4
        grid = round(refConfig.blockWidth / 16)
        len1 = 5
        len2 = 2

        origins = (
            (0, 0),
            (refConfig.blockWidth, 0),
            (round(refConfig.blockWidth / 2), round(refConfig.blockWidth / 2)),
            (0, refConfig.blockWidth),
            (refConfig.blockWidth, refConfig.blockWidth),
        )

        outlineClr = None
        outlineClr = patternOutLine
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
            refConfig.blockDraw.polygon(isoTriangle, fill=patternFill, outline=outlineClr)
            isoTriangle = (
                (midx - grid * len1, midy),
                (midx, midy - grid),
                (midx + grid * len1, midy),
                (midx, midy + grid),
                (midx - grid * len1, midy),
            )
            refConfig.blockDraw.polygon(isoTriangle, fill=patternFill, outline=outlineClr)
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
            refConfig.blockDraw.polygon(isoTriangle, fill=patternFill, outline=outlineClr)

    return wrapper


@compassPatternFunction
def compass(refConfig, paletteObj):
    # return "A","B","C"
    bgFill = tuple(int(a) for a in (paletteObj.c1.currentColor))
    patternFill = tuple(int(a) for a in (paletteObj.c2.currentColor))
    patternOutLine = tuple(int(a) for a in (paletteObj.c3.currentColor))
    hilight = tuple(int(a) for a in (paletteObj.c4.currentColor))
    return refConfig, bgFill, patternFill, patternOutLine, hilight


@compassPatternFunction
def compass_hili(refConfig, paletteObj):
    # return "B","C","A"
    bgFill = tuple(int(a) for a in (paletteObj.c1.currentColor))
    patternFill = tuple(int(a) for a in (paletteObj.c4.currentColor))
    patternOutLine = tuple(int(a) for a in (paletteObj.c3.currentColor))
    hilight = tuple(int(a) for a in (paletteObj.c4.currentColor))
    return refConfig, bgFill, patternFill, patternOutLine, hilight


# --------------------------------------- #


def randomizerPatternFunction(func):
    def wrapper(*args):
        res = func(*args)
        refConfig = res[0]
        bgFill = (res[1][0], res[1][1], res[1][2], 190)
        patternFill = res[2]
        patternOutLine = res[3]
        hilight = res[4]
        randomix = res[5]
        paletteRef = res[6]

        w = 4
        h = 4
        x = refConfig.xIncrementer
        y = refConfig.yIncrementer

        w = refConfig.randomBlockWidth
        h = refConfig.randomBlockHeight

        refConfig.blockDraw.rectangle((0, 0, refConfig.blockWidth, refConfig.blockHeight), fill=bgFill, outline=None)

        rows = refConfig.blockHeight
        cols = refConfig.blockWidth

        step = w
        hStep = h

        if w == 0:
            step = 1
        if h == 0:
            hStep = 1

        for r in range(0, rows, hStep):
            for c in range(0, cols, step):
                clr = colorutils.getRandomRGB(refConfig.brightness / 2)
                if randomix == 1:
                    clr = colorutils.getRandomColorHSV(
                        paletteRef.minHue, paletteRef.maxHue, paletteRef.minSaturation, paletteRef.maxSaturation, paletteRef.minValue, paletteRef.maxValue
                    )
                if random.random() < refConfig.randomBlockProb:
                    refConfig.blockDraw.rectangle((c, r, w + c, h + r), fill=(clr), outline=None)

    return wrapper


@randomizerPatternFunction
def randomizer(refConfig, paletteObj):
    # return "A","B","C"
    bgFill = tuple(int(a) for a in (paletteObj.c1.currentColor))
    patternFill = tuple(int(a) for a in (paletteObj.c2.currentColor))
    patternOutLine = tuple(int(a) for a in (paletteObj.c3.currentColor))
    hilight = tuple(int(a) for a in (paletteObj.c4.currentColor))
    return refConfig, bgFill, patternFill, patternOutLine, hilight, 0, None


@randomizerPatternFunction
def randomizer2(refConfig, paletteObj):
    # return "B","C","A"
    bgFill = tuple(int(a) for a in (paletteObj.c1.currentColor))
    patternFill = tuple(int(a) for a in (paletteObj.c4.currentColor))
    patternOutLine = tuple(int(a) for a in (paletteObj.c1.currentColor))
    hilight = tuple(int(a) for a in (paletteObj.c4.currentColor))
    return refConfig, bgFill, patternFill, patternOutLine, hilight, 0, None


@randomizerPatternFunction
def randomizer3(refConfig, paletteObj):
    # return "B","C","A"
    bgFill = tuple(int(a) for a in (paletteObj.c1.currentColor))
    patternFill = tuple(int(a) for a in (paletteObj.c4.currentColor))
    patternOutLine = tuple(int(a) for a in (paletteObj.c1.currentColor))
    hilight = tuple(int(a) for a in (paletteObj.c4.currentColor))
    return refConfig, bgFill, patternFill, patternOutLine, hilight, 0, None


@randomizerPatternFunction
def randomizer4(refConfig, paletteObj):
    # return "B","C","A"
    bgFill = tuple(int(a) for a in (paletteObj.c1.currentColor))
    patternFill = tuple(int(a) for a in (paletteObj.c4.currentColor))
    patternOutLine = tuple(int(a) for a in (paletteObj.c1.currentColor))
    hilight = tuple(int(a) for a in (paletteObj.c4.currentColor))
    return refConfig, bgFill, patternFill, patternOutLine, hilight, 1, paletteObj.c4


# --------------------------------------- #


def wavePatternFunction(func):
    def wrapper(*args):
        res = func(*args)
        refConfig = res[0]
        bgFill = res[1]
        patternFill = res[2]
        patternOutLine = res[3]
        hilight = res[4]
        w = 4
        h = 4
        x = refConfig.xIncrementer
        y = refConfig.yIncrementer

        # clr3 = tuple(int(a) for a in (paletteObj.c1.currentColor))
        # clr = tuple(int(a) for a in (paletteObj.c2.currentColor))
        # clr2 = tuple(int(a) for a in (paletteObj.c3.currentColor))

        # clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
        # clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
        # clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
        # clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))

        refConfig.blockDraw.rectangle((0, 0, refConfig.blockWidth, refConfig.blockHeight), fill=bgFill, outline=bgFill)

        numPoints = round(refConfig.blockWidth)
        amplitude = refConfig.amplitude
        yOffset = refConfig.yOffset
        amplitude2 = refConfig.amplitude2
        yOffset2 = refConfig.yOffset2
        steps = refConfig.steps
        steps2 = refConfig.steps2
        rads = 2 * 22 / 7 / numPoints

        for i in range(0, numPoints, steps):
            angle = (i + refConfig.xIncrementer) * rads
            angle2 = (i + refConfig.xIncrementer + steps) * rads
            a = (i, math.sin(angle) * amplitude + yOffset)
            b = (i + steps, math.sin(angle) * amplitude + yOffset)
            c = (i + steps, math.sin(angle2) * amplitude + yOffset)

            if c[1] < a[1]:
                b = (i, math.sin(angle2) * amplitude + yOffset)
            refConfig.blockDraw.polygon((a, b, c, a), fill=patternFill, outline=None)

        phase = round(refConfig.blockWidth / refConfig.phaseFactor)
        for i in range(0, numPoints, steps2):
            angle = (i - refConfig.speedFactor * refConfig.xIncrementer + phase) * rads
            angle2 = (i - refConfig.speedFactor * refConfig.xIncrementer + phase + steps2) * rads
            a = (i, math.cos(angle) * amplitude2 + yOffset2)
            b = (i + steps2, math.cos(angle) * amplitude2 + yOffset2)
            c = (i + steps2, math.cos(angle2) * amplitude2 + yOffset2)

            if c[1] < a[1]:
                b = (i, math.cos(angle2) * amplitude2 + yOffset2)
            refConfig.blockDraw.polygon((a, b, c, a), fill=patternOutLine, outline=None)

        refConfig.xIncrementer += refConfig.xSpeed
        refConfig.yIncrementer += refConfig.ySpeed

        if refConfig.xIncrementer >= refConfig.blockWidth * 1:
            refConfig.xIncrementer = -0
        if refConfig.yIncrementer >= refConfig.blockHeight - 4:
            refConfig.yIncrementer = 0

    return wrapper


@wavePatternFunction
def wavePattern(refConfig, paletteObj):
    # return "A","B","C"
    bgFill = tuple(int(a) for a in (paletteObj.c1.currentColor))
    patternFill = tuple(int(a) for a in (paletteObj.c2.currentColor))
    patternOutLine = tuple(int(a) for a in (paletteObj.c3.currentColor))
    hilight = tuple(int(a) for a in (paletteObj.c4.currentColor))
    return refConfig, bgFill, patternFill, patternOutLine, hilight


# @wavePatternFunction
# def wavePattern2(refConfig, paletteObj):
#     # return "B","C","A"
#     bgFill = tuple(int(a) for a in (paletteObj.c1.currentColor))
#     patternFill = tuple(int(a) for a in (paletteObj.c4.currentColor))
#     patternOutLine = tuple(int(a) for a in (paletteObj.c3.currentColor))
#     hilight = tuple(int(a) for a in (paletteObj.c4.currentColor))
#     return refConfig,bgFill,patternFill,patternOutLine,hilight

# --------------------------------------- #


def logcabinPatternFunction(func):
    def wrapper(*args):
        res = func(*args)
        refConfig = res[0]
        bgFill = res[1]
        patternFill = res[2]
        patternOutLine = res[3]
        hilight = res[4]

        # clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
        # clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
        # clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
        # clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))

        refConfig.blockDraw.rectangle((0, 0, refConfig.blockWidth, refConfig.blockHeight), fill=bgFill, outline=None)

        _blockSize = refConfig.blockWidth - 0
        _mid = [_blockSize / 2, _blockSize / 2]
        fibo = 7
        _seq = fiboSeq(fibo)
        numberOfBars = len(_seq)
        gridSize = math.ceil(_blockSize / numberOfBars)

        for _rowCount, col in enumerate(_seq):
            _h = col * gridSize
            _w = gridSize
            _y = round(_mid[1] - _h / 2)
            _x = round((_rowCount) * gridSize)
            _clr = patternFill
            if _rowCount % 2 != 0:
                if random.random() < refConfig.popRandomColorProb:
                    _clr = colorutils.getRandomColorHSV(0, 360, 0.65, 1.0, 0.5, 0.75, 0, 0, 255)
                else:
                    _clr = colorutils.getRandomColorHSV(320, 340, 0.65, 1.0, 0.5, 0.75, 0, 0, 255)

            _clrReduced = tuple(round(i * 0.85) for i in _clr) if _rowCount < numberOfBars / 2 else tuple(round(i * 1.0) for i in _clr)

            if col == 1:
                _clrReduced = (255, 0, 100, 255)
            refConfig.blockDraw.rectangle((_x, _y, _x + _w, _y + _h), fill=_clrReduced, outline=None)

        for _rowCount, row in enumerate(_seq):
            _w = row * gridSize
            _x = round(_mid[0] - _w / 2)
            _y = round((_rowCount) * gridSize)
            _h = gridSize
            _clr = patternFill
            if _rowCount % 2 != 0:
                if random.random() < refConfig.popRandomColorProb:
                    _clr = colorutils.getRandomColorHSV(0, 360, 0.65, 1.0, 0.5, 0.75, 0, 0, 255)
                else:
                    _clr = colorutils.getRandomColorHSV(320, 340, 0.65, 1.0, 0.5, 0.75, 0, 0, 255)
            _clrReduced = tuple(round(i * 0.65) for i in _clr) if _rowCount < numberOfBars / 2 else tuple(round(i * 1.0) for i in _clr)
            if row == 1:
                _clrReduced = (255, 0, 100, 255)
            refConfig.blockDraw.rectangle((_x, _y, _x + _w, _y + _h), fill=_clrReduced, outline=None)

    return wrapper


@logcabinPatternFunction
def logcabin(refConfig, paletteObj):
    bgFill = tuple(int(a) for a in (paletteObj.c1.currentColor))
    patternFill = tuple(int(a) for a in (paletteObj.c2.currentColor))
    patternOutLine = tuple(int(a) for a in (paletteObj.c3.currentColor))
    hilight = tuple(int(a) for a in (paletteObj.c4.currentColor))
    return refConfig, bgFill, patternFill, patternOutLine, hilight


@logcabinPatternFunction
def logcabinAlt1(refConfig, paletteObj):
    bgFill = tuple(int(a) for a in (paletteObj.c1.currentColor))
    patternFill = tuple(int(a) for a in (paletteObj.c2.currentColor))
    patternOutLine = tuple(int(a) for a in (paletteObj.c3.currentColor))
    hilight = tuple(int(a) for a in (paletteObj.c4.currentColor))
    return refConfig, bgFill, patternFill, patternOutLine, hilight


@logcabinPatternFunction
def logcabinAlt2(refConfig, paletteObj):
    bgFill = tuple(int(a) for a in (paletteObj.c1.currentColor))
    patternFill = tuple(int(a) for a in (paletteObj.c4.currentColor))
    patternOutLine = tuple(int(a) for a in (paletteObj.c3.currentColor))
    hilight = tuple(int(a) for a in (paletteObj.c4.currentColor))
    return refConfig, bgFill, patternFill, patternOutLine, hilight


# --------------------------------------- #


def ropePattern(refConfig, paletteObj=None):
    # sourcery skip: use-itertools-product
    w = 4
    h = 4
    x = refConfig.xIncrementer
    y = refConfig.yIncrementer

    # clr3 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    # clr = tuple(int(a) for a in (paletteObj.c2.currentColor))
    # clr2 = tuple(int(a) for a in (paletteObj.c3.currentColor))

    clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
    clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))

    refConfig.blockDraw.rectangle((0, 0, refConfig.blockWidth, refConfig.blockHeight), fill=clr1, outline=clr1)

    numPoints = round(refConfig.blockWidth)
    amplitude = refConfig.blockWidth / 2 - 3
    # yOffset = refConfig.yOffset
    yOffset = refConfig.blockWidth / 2
    steps = refConfig.steps
    rads = 2 * math.pi / numPoints
    phase = 2 / 3 * math.pi
    for _s in range(3):
        for i in range(-1, numPoints + 2, 2):
            angle1 = (i + refConfig.xIncrementer) * rads + _s * phase
            angle2 = (i + refConfig.xIncrementer + steps) * rads + _s * phase
            a = (i, math.sin(angle1) * amplitude + yOffset)
            c = (i + steps, math.sin(angle2) * amplitude + yOffset)
            refConfig.blockDraw.line((a, c), fill=clr2, width=6)

    refConfig.xIncrementer += refConfig.xSpeed
    refConfig.yIncrementer += refConfig.ySpeed

    if refConfig.xIncrementer >= refConfig.blockWidth * 1:
        refConfig.xIncrementer = -0
    if refConfig.yIncrementer >= refConfig.blockHeight - 4:
        refConfig.yIncrementer = 0


def wavePattern2(refConfig, paletteObj=None):
    # sourcery skip: use-itertools-product
    w = 4
    h = 4
    x = refConfig.xIncrementer
    y = refConfig.yIncrementer

    # clr3 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    # clr = tuple(int(a) for a in (paletteObj.c2.currentColor))
    # clr2 = tuple(int(a) for a in (paletteObj.c3.currentColor))

    clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
    clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))

    refConfig.blockDraw.rectangle((0, 0, refConfig.blockWidth, refConfig.blockHeight), fill=clr1, outline=clr1)

    numPoints = round(refConfig.blockWidth)
    amplitude = refConfig.amplitude
    yOffset = refConfig.yOffset
    amplitude2 = refConfig.amplitude2
    yOffset2 = refConfig.yOffset2
    steps = refConfig.steps
    steps2 = refConfig.steps2
    rads = 2 * 22 / 7 / numPoints

    for iy in range(-numPoints, numPoints * 2, steps * 2):
        for i in range(0, numPoints, steps):
            angle = (i + refConfig.xIncrementer) * rads
            angle2 = (i + refConfig.xIncrementer + steps) * rads
            a = (i, math.sin(angle) * amplitude + yOffset + iy)
            b = (i + steps, math.sin(angle) * amplitude + yOffset + iy)
            c = (i + steps, math.sin(angle2) * amplitude + yOffset + iy)
            c2 = (i + steps, math.sin(angle2) * amplitude + yOffset + iy + 1)

            if c[1] < a[1]:
                b = (i, math.sin(angle2) * amplitude + yOffset)
            # refConfig.blockDraw.polygon((a, b, c, a), fill=None, outline=clr)
            refConfig.blockDraw.line((a, c), fill=clr2)
            refConfig.blockDraw.line((a, c2), fill=clr2)

    # phase = round(refConfig.blockWidth/refConfig.phaseFactor)
    # for i in range(0, numPoints, steps2):
    #     angle = (i - refConfig.speedFactor*refConfig.xIncrementer + phase) * rads
    #     angle2 = (i - refConfig.speedFactor *
    #               refConfig.xIncrementer + phase + steps2) * rads
    #     a = (i, math.cos(angle) * amplitude2 + yOffset2)
    #     b = (i + steps2, math.cos(angle) * amplitude2 + yOffset2)
    #     c = (i + steps2, math.cos(angle2) * amplitude2 + yOffset2)

    #     if c[1] < a[1]:
    #         b = (i, math.cos(angle2) * amplitude2 + yOffset2)
    #     refConfig.blockDraw.polygon((a, b, c, a), fill=clr2, outline=None)

    refConfig.xIncrementer += refConfig.xSpeed
    refConfig.yIncrementer += refConfig.ySpeed

    if refConfig.xIncrementer >= refConfig.blockWidth * 1:
        refConfig.xIncrementer = -0
    if refConfig.yIncrementer >= refConfig.blockHeight - 4:
        refConfig.yIncrementer = 0


def runningSpiral(refConfig, paletteObj=None):
    # 16px grid box spiral for now
    w = 4
    h = 4
    x = refConfig.xIncrementer
    y = refConfig.yIncrementer
    # clr3 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    # clr = tuple(int(a) for a in (paletteObj.c2.currentColor))
    # clr2 = tuple(int(a) for a in (paletteObj.c3.currentColor))

    clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
    clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))

    refConfig.blockDraw.rectangle((0, 0, refConfig.blockWidth, refConfig.blockHeight), fill=clr1, outline=None)

    lineMult = refConfig.lineDiff * 2
    numLines = round(refConfig.blockWidth / refConfig.lineDiff * 2)

    d = 3
    direction = 1
    distance = 1

    mid = [refConfig.blockWidth / 2 - 1, refConfig.blockHeight / 2 - 1]

    p1 = [mid[0], mid[1]]
    p2 = [mid[0], mid[1]]

    # clr = (0,255,255)

    for _ in range(numLines):
        distance += d
        p2[0] = p2[0] + distance * direction
        refConfig.blockDraw.line((p1[0], p1[1], p2[0], p2[1]), fill=clr2)
        p1[0] = p2[0]
        distance += d
        p2[1] = p2[1] + distance * direction
        refConfig.blockDraw.line((p1[0], p1[1], p2[0], p2[1]), fill=clr2)
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
        refConfig.blockDraw.line((p1[0], p1[1], p2[0], p2[1]), fill=clr3)
        p1[0] = p2[0]
        distance += d
        p2[1] = p2[1] + distance * direction
        refConfig.blockDraw.line((p1[0], p1[1], p2[0], p2[1]), fill=clr3)
        direction *= -1
        p1[1] = p2[1]


def chainLinks(refConfig, paletteObj=None):
    refConfig.circlesPackedSize = 0.1

    # clr3 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    # clr = tuple(int(a) for a in (paletteObj.c2.currentColor))
    # clr2 = tuple(int(a) for a in (paletteObj.c3.currentColor))

    clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
    clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))
    refConfig.blockDraw.rectangle((0, 0, refConfig.blockWidth, refConfig.blockHeight), fill=clr1, outline=None)

    numRows = refConfig.numDotRows
    steps = 3
    var = 8
    overlap = refConfig.blockWidth / 4 - var
    dotWidth = (refConfig.blockWidth - overlap - var) / 1
    dotWidth = refConfig.blockWidth
    outline = clr2

    _unitLength = max(4, 1 / 16 * refConfig.blockWidth)
    _wd = 4
    for _c in range(4):

        _yOff = 0
        if _c % 2 == 0:
            _yOff = _unitLength * 2
        x0 = _unitLength * 0 + _c * _unitLength * 4
        y0 = _unitLength * -2 + _yOff
        x1 = _unitLength * 4 + _c * _unitLength * 4
        y1 = _unitLength * 2 + _yOff
        refConfig.blockDraw.arc((x0, y0, x1, y1), 0, 180, fill=outline, width=_wd)
        refConfig.blockDraw.line((x0 + _wd / 2, y0 + 2 * _unitLength, x0 - _wd / 2, 0 - _wd / 2), fill=outline, width=_wd)
        refConfig.blockDraw.line((x1 + _wd / 2, y0 + 2 * _unitLength, x1 - _wd / 2, 0 - _wd / 2), fill=outline, width=_wd)

        x0 = _unitLength * 0 + _c * _unitLength * 4
        y0 = _unitLength * 2 + _yOff
        x1 = _unitLength * 4 + _c * _unitLength * 4
        y1 = _unitLength * 6 + _yOff
        refConfig.blockDraw.arc((x0, y0, x1, y1), 180, 0, fill=outline, width=_wd)
        refConfig.blockDraw.line((x0, y0 + 1 * _unitLength + _wd / 2, x0, y1 + 1 * _unitLength + _wd / 2), fill=outline, width=_wd)
        refConfig.blockDraw.line((x1 - _wd / 2, y0 + 1 * _unitLength + _wd / 2, x1 - _wd / 2, y1 + 1 * _unitLength + _wd / 2), fill=outline, width=_wd)

        # refConfig.blockDraw.rectangle((x0 + (x1 - x0) / 2 - _wd / 2 - 1,
        #                             y0 - _unitLength * 3,
        #                             x0 + (x1 - x0) / 2 + _wd / 2 + 0,
        #                             y1 - _unitLength * 1),
        #                             fill=(outline), outline=(clr1))
        try:
            # comment: 
        # end try
            refConfig.blockDraw.rounded_rectangle(
                (x0 + (x1 - x0) / 2 - _wd / 2 - 1, y0 - _unitLength * 3, x0 + (x1 - x0) / 2 + _wd / 2 + 0, y1 - _unitLength * 1), fill=(outline), radius=4, outline=(clr1), corners=None
            )
        except Exception as e:
            refConfig.blockDraw.rectangle(
                (x0 + (x1 - x0) / 2 - _wd / 2 - 1, y0 - _unitLength * 3, x0 + (x1 - x0) / 2 + _wd / 2 + 0, y1 - _unitLength * 1), fill=(outline),  outline=(clr1)
            )
            pieceLogger(e)

        # rounded_rectangle(xy, radius=0, fill=None, outline=None, width=1, corners=None)[source]

        # refConfig.blockDraw.arc((x0 + (x1 - x0) / 2 - _wd / 2 - 0,
        #                       y0 - _wd * 3,
        #                       x0 + (x1 - x0) / 2 + _wd / 2 - 1,
        #                       y0 - _wd), 180, 0, fill=(outline), width=_wd)
        # refConfig.blockDraw.arc((x0 + (x1 - x0) / 2 - _wd / 2 - 0,
        #                       y1  - _wd * 2,
        #                       x0 + (x1 - x0) / 2 + _wd / 2 - 1,
        #                       y1 - _wd), 0, 180, fill=(outline), width=_wd)

        x0 = _unitLength * 0 + _c * _unitLength * 4
        y0 = _unitLength * 5 + _yOff
        x1 = _unitLength * 4 + _c * _unitLength * 4
        y1 = _unitLength * 10 + _yOff
        refConfig.blockDraw.arc((x0, y0, x1, y1), 0, 180, fill=outline, width=_wd)
        # refConfig.blockDraw.line((x1 - _wd/2, y0, x1- _wd/2, y1 - 1*_unitLength), fill=outline, width=_wd)

        # 3rd link top
        x0 = _unitLength * 0 + _c * _unitLength * 4
        y0 = _unitLength * 3 + _unitLength * 7 + _yOff
        x1 = _unitLength * 4 + _c * _unitLength * 4
        y1 = _unitLength * 7 + _unitLength * 7 + _yOff
        refConfig.blockDraw.arc((x0, y0, x1, y1), 180, 0, fill=outline, width=_wd)
        refConfig.blockDraw.line((x0, y0 + 2 * _unitLength, x0, y1 + 3 * _unitLength), fill=outline, width=_wd)
        refConfig.blockDraw.line((x1 - _wd / 2, y0 + 2 * _unitLength, x1 - _wd / 2, y1 + 3 * _unitLength), fill=outline, width=_wd)

        try:
            refConfig.blockDraw.rounded_rectangle(
                (x0 + (x1 - x0) / 2 - _wd / 2 - 1, y0 - _unitLength * 3, x0 + (x1 - x0) / 2 + _wd / 2, y1 - _unitLength * 1), radius=4, corners=None, fill=(outline), outline=(clr1)
            )
        except Exception as e:
            pieceLogger(e)
            refConfig.blockDraw.rectangle(
                (x0 + (x1 - x0) / 2 - _wd / 2 - 1, y0 - _unitLength * 3, x0 + (x1 - x0) / 2 + _wd / 2, y1 - _unitLength * 1), fill=(outline), outline=(clr1)
            )

        # refConfig.blockDraw.arc((x0 + (x1 - x0) / 2 - _wd / 2 - 0,
        #                       y1 + _unitLength  + 1,
        #                       x0 + (x1 - x0) / 2 + _wd / 2 - 1,
        #                       y1 + _unitLength + _wd * 1), 180, 0, fill=(outline), width=_wd)

        # refConfig.blockDraw.arc((x0 + (x1 - x0) / 2 - _wd / 2 - 0,
        #                       _unitLength * 6 + _yOff,
        #                       x0 + (x1 - x0) / 2 + _wd / 2 - 1,
        #                       _unitLength * 6 + _yOff + _wd * 2), 180, 0, fill=(outline), width=_wd)

        # refConfig.blockDraw.arc((x0 + (x1 - x0) / 2 - _wd / 2 - 0,
        #                       _unitLength * 12 + _yOff,
        #                       x0 + (x1 - x0) / 2 + _wd / 2 - 1,
        #                       _unitLength * 12 + _yOff + _wd * 1), 0, 180, fill=(outline), width=_wd)

        # 3rd link shafts
        # refConfig.blockDraw.line((x0, y0 + 2 * _unitLength, x0, _unitLength * 16), fill=outline, width=_wd)
        # refConfig.blockDraw.line((x1, y0 + 3 * _unitLength, x1, _unitLength * 16), fill=outline, width=_wd)

        # # 2nd link top
        # x0 = _unitLength * 3 + _c * _unitLength * 8
        # y0 = _unitLength * 1
        # x1 = _unitLength * 7 + _c * _unitLength * 8
        # y1 = _unitLength * 5
        # refConfig.blockDraw.arc((x0, y0, x1, y1), 180, 250, fill=clr3, width=_wd + 1)
        # refConfig.blockDraw.arc((x0, y0, x1, y1), 290, 0, fill=clr3, width=_wd + 1)

        # # 2nd link shafts
        # refConfig.blockDraw.line((x0 + 2, y0 + 2 * _unitLength, x0 + 2, _unitLength * 10), fill=clr3, width=_wd)
        # refConfig.blockDraw.line((x1 - 3, y0 + 2 * _unitLength, x1 - 3, _unitLength * 10), fill=clr3, width=_wd)

        # # 2nd link bottom
        # x0 = _unitLength * 3 + _c * _unitLength * 8
        # y0 = _unitLength * 3 + _unitLength * 5
        # x1 = _unitLength * 7 + _c * _unitLength * 8
        # y1 = _unitLength * 7 + _unitLength * 5
        # refConfig.blockDraw.arc((x0, y0, x1, y1), 0, 180, fill=clr3, width=_wd)


def circlesPacked(refConfig, paletteObj=None):
    refConfig.circlesPackedSize = 0.1

    # clr3 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    # clr = tuple(int(a) for a in (paletteObj.c2.currentColor))
    # clr2 = tuple(int(a) for a in (paletteObj.c3.currentColor))

    clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
    clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))
    refConfig.blockDraw.rectangle((0, 0, refConfig.blockWidth, refConfig.blockHeight), fill=clr1, outline=None)

    numRows = refConfig.numDotRows
    steps = 3
    var = 8
    overlap = refConfig.blockWidth / 4 - var
    dotWidth = (refConfig.blockWidth - overlap - var) / 1
    outline = clr2
    for _r in range(steps):
        # xPos = i * dotWidth * 1 - dotWidth / 2
        for _c in range(steps):
            x0 = _c * (dotWidth) - dotWidth / 2 - _c * overlap - var
            y0 = _r * (dotWidth) - dotWidth / 2 - _r * overlap - var
            x1 = x0 + (dotWidth * 1)
            y1 = y0 + (dotWidth * 1)

            # x1 = max(x1, x0)
            # y1 = max(y1, y0)

            refConfig.blockDraw.ellipse((x0, y0, x1, y1), outline=(outline), fill=None)
            refConfig.blockDraw.ellipse((x0 + 4, y0 + 4, x1 - 4, y1 - 4), outline=(outline), fill=None)

    # yPos = 2 * dotWidth / 2 * math.sin(2 * math.pi / 6) + 2

    # for i in range(4):
    #     xPos = i * dotWidth * 1
    #     for r in range(0, numLines, steps):
    #         x0 = r - 1 + xPos
    #         y0 = r - 1 + yPos
    #         x1 = x0 + (dotWidth - 1) * r
    #         y1 = y0 + (dotWidth - 1) * r

    #         x1 = max(x1, x0)
    #         y1 = max(y1, y0)

    #         refConfig.blockDraw.ellipse((x0,y0,x1,y1), outline=(outline), fill=clr1)


def shingles(refConfig, paletteObj=None):
    w = 4
    h = 4
    x = refConfig.xIncrementer
    y = refConfig.yIncrementer

    # clr = tuple(int(a) for a in (paletteObj.c1.currentColor))
    # clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    # clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))

    clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
    clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))

    refConfig.blockDraw.rectangle((0, 0, refConfig.blockWidth, refConfig.blockHeight), fill=clr2, outline=None)

    numRows = refConfig.numShingleRows
    boxWidth = refConfig.blockWidth / numRows
    shingleWidth = refConfig.blockWidth / numRows - refConfig.shingleVariationAmount

    for r in range(numRows, -1, -1):
        yPos = -1 + r * boxWidth

        for i in range(3):
            refConfig.blockDraw.rectangle((i * boxWidth - boxWidth / 2, yPos, i * boxWidth + shingleWidth - boxWidth / 2, yPos + boxWidth - 1), outline=(clr1), fill=clr2)
        for i in range(2):
            refConfig.blockDraw.rectangle((i * boxWidth, yPos - boxWidth / 2, i * boxWidth + shingleWidth, yPos + boxWidth / 2 - 1), outline=(clr1), fill=clr2)


def shellScales(refConfig, paletteObj=None):
    # clr, clr2, clr3 = _get_colors(refConfig, paletteObj)

    clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
    clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))

    refConfig.blockDraw.rectangle((0, 0, refConfig.blockWidth, refConfig.blockHeight), fill=clr3, outline=None)

    numRows = refConfig.numShingleRows
    boxWidth = refConfig.blockWidth / numRows
    numLines = round(refConfig.waveScaleRings * 1.0)
    numLinesHalf = round(numLines / 2)
    rads = math.pi * 2 / numLines
    radius = boxWidth / 2

    for r in range(numRows, -1, -1):
        yPos = -2 + r * boxWidth
        _draw_row_of_ellipses(refConfig, yPos, boxWidth, clr2, clr1, numLinesHalf, rads, radius, clr3)
        _draw_offset_row_of_ellipses(refConfig, yPos, boxWidth, clr2, clr1, numLinesHalf, rads, radius, clr3)


def _draw_row_of_ellipses(refConfig, yPos, boxWidth, clr, clr3, numLinesHalf, rads, radius, clr2):
    for i in range(3):
        refConfig.blockDraw.ellipse((i * boxWidth - boxWidth / 2, yPos, i * boxWidth + boxWidth - boxWidth / 2, yPos + boxWidth), outline=clr, fill=clr3)

        for q in range(-numLinesHalf, numLinesHalf):
            angle = rads * q
            x0 = i * boxWidth
            y0 = yPos
            xP = i * boxWidth + radius * math.cos(angle)
            yP = yPos + boxWidth - boxWidth / 2 + radius * math.sin(angle)
            clrToUse = clr2 if q % 2 == 0 else clr
            refConfig.blockDraw.line((x0, y0, xP, yP), fill=clrToUse)


def _draw_offset_row_of_ellipses(refConfig, yPos, boxWidth, clr, clr3, numLinesHalf, rads, radius, clr2):
    for i in range(2):
        refConfig.blockDraw.ellipse((i * boxWidth, yPos - boxWidth / 2, i * boxWidth + boxWidth, yPos + boxWidth / 2), outline=clr, fill=clr3)

        for q in range(-numLinesHalf, numLinesHalf):
            angle = rads * q
            x0 = i * boxWidth + boxWidth / 2
            y0 = yPos - boxWidth / 2
            xP = i * boxWidth + boxWidth / 2 + radius * math.cos(angle)
            yP = yPos + boxWidth - boxWidth + radius * math.sin(angle)  # Corrected yP calculation
            clrToUse = clr2 if q % 2 == 0 else clr
            refConfig.blockDraw.line((x0, y0, xP, yP), fill=clrToUse)


def ellipses(refConfig, paletteObj=None):
    # clr, clr2, clr3 = _get_colors(refConfig, paletteObj)

    clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
    clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))

    refConfig.blockDraw.rectangle((0, 0, refConfig.blockWidth, refConfig.blockHeight), fill=clr1, outline=None)

    numRows = 2
    boxWidth = 2 * refConfig.blockWidth / numRows
    rings = refConfig.waveScaleRings
    step = refConfig.waveScaleSteps
    patternRows = numRows + 1

    if refConfig.linesOnly:
        refConfig.altLineColoring = False

    startFirstSet = 1 if refConfig.altLineColoring and step != 2 else 0
    lineToUse = clr2

    for r in range(patternRows, -patternRows, -1):
        yPos = -2 + r * boxWidth
        _draw_ellipse_set(refConfig, yPos, boxWidth, rings, step, clr3, clr2, lineToUse)


def _draw_ellipse_set(refConfig, yPos, boxWidth, rings, step, clr3, clr2, lineToUse):
    xOffSet = -boxWidth / 2
    yOffSet = boxWidth
    y = boxWidth / 4 - yPos / 2

    for i in range(3):
        xSizeOfBox = i * boxWidth
        for n in range(0, rings * step, step):  # Removed startFirstSet as it's always 0 here
            clrToUse = clr3 if not refConfig.altLineColoring or n % 2 == 0 else clr2
            x0 = xSizeOfBox + xOffSet + n
            x1 = xSizeOfBox + xOffSet + boxWidth - n
            y0 = yPos + n + y - y  # Simplified y-coordinate calculation
            y1 = yPos + yOffSet - n

            x1 = max(x1, x0)
            y1 = max(y1, y0)
            refConfig.blockDraw.ellipse((x0, y0, x1, y1), outline=lineToUse, fill=clrToUse)

    xOffSet = 0
    yOffSet /= 2
    y = boxWidth / 2 - yPos / 2

    for i in range(2):
        xSizeOfBox = i * boxWidth
        for n in range(rings * step, step):  # rings * step is always greater than step, resulting in an empty loop
            clrToUse = clr3 if not refConfig.altLineColoring or n % 2 == 0 else clr2
            x0 = xSizeOfBox + xOffSet + n
            x1 = xSizeOfBox + xOffSet + boxWidth - n + 20
            y0 = yPos - yOffSet + n + y - y  # Simplified y-coordinate calculation
            y1 = yPos + yOffSet - n + y - y  # Simplified y-coordinate calculation

            x1 = max(x1, x0)
            y1 = max(y1, y0)
            refConfig.blockDraw.ellipse((x0, y0, x1, y1), outline=lineToUse, fill=clrToUse)


def waveScales(refConfig, paletteObj=None):
    # clr, clr2, clr3 = _get_colors(refConfig, paletteObj)

    clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
    clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))

    refConfig.blockDraw.rectangle((0, 0, refConfig.blockWidth, refConfig.blockHeight), fill=clr3, outline=None)

    numRows = 2
    boxWidth = 2 * refConfig.blockWidth / numRows
    rings = refConfig.waveScaleRings
    step = refConfig.waveScaleSteps
    patternRows = numRows + 1

    if refConfig.linesOnly:
        refConfig.altLineColoring = False

    lineToUse = clr2

    for r in range(patternRows, -patternRows, -1):
        yPos = -2 + r * boxWidth
        _draw_wave_scale_set(refConfig, yPos, boxWidth, rings, step, clr3, clr2, clr4, lineToUse)


def _draw_wave_scale_set(refConfig, yPos, boxWidth, rings, step, clr3, clr2, clr4, lineToUse):
    xOffSet = -boxWidth / 2
    yOffSet = boxWidth
    y = boxWidth / 4 - yPos / 2

    for i in range(3):
        xSizeOfBox = i * boxWidth
        for n in range(0, rings * step, step):
            clrToUse = clr3 if not refConfig.altLineColoring or n % 2 == 0 else clr2
            x0 = xSizeOfBox + xOffSet + n
            x1 = xSizeOfBox + xOffSet + boxWidth - n
            y0 = yPos + n + y
            y1 = yPos + yOffSet - n + y

            _draw_ellipse(refConfig, x0, y0, x1, y1, lineToUse, clrToUse)

    xOffSet = 0
    yOffSet /= 2
    y = boxWidth / 2 - yPos / 2

    for i in range(2):
        xSizeOfBox = i * boxWidth
        for n in range(0, rings * step, step):
            clrToUse = clr3 if not refConfig.altLineColoring or n % 2 == 0 else clr2
            x0 = xSizeOfBox + xOffSet + n
            x1 = xSizeOfBox + xOffSet + boxWidth - n
            y0 = yPos - yOffSet + n + y
            y1 = yPos + yOffSet - n + y

            _draw_ellipse(refConfig, x0, y0, x1, y1, lineToUse, clrToUse)


def _draw_ellipse(refConfig, x0, y0, x1, y1, lineToUse, clrToUse):
    x1 = max(x1, x0)
    y1 = max(y1, y0)
    refConfig.blockDraw.ellipse((x0, y0, x1, y1), outline=lineToUse, fill=clrToUse)


def circles(refConfig, paletteObj=None):
    # clr, clr2, clr3 = _get_colors(refConfig, paletteObj)
    clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
    clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))

    refConfig.blockDraw.rectangle((0, 0, refConfig.blockWidth, refConfig.blockHeight), fill=clr1, outline=None)

    numLines = refConfig.blockWidth - 1
    steps = 3

    _draw_circles(refConfig, 0, 0, numLines, steps, clr2, clr3, clr1, refConfig.blockWidth, refConfig.blockHeight)

    for c in range(2):
        xOff = c * refConfig.blockWidth - refConfig.blockWidth / 2
        for r in range(2):
            yOff = r * refConfig.blockHeight - refConfig.blockHeight / 2
            _draw_circles(refConfig, xOff, yOff, numLines, steps, clr2, clr1, clr3, refConfig.blockWidth, refConfig.blockHeight)  # Swapped clr2 and clr3 for outline


def _draw_circles(refConfig, xOff, yOff, numLines, steps, outlineClr, fillClr1, fillClr2, width, height):
    for i in range(0, numLines, steps):
        x1 = i - 1 + xOff
        y1 = i - 1 + yOff
        x2 = width - 1 * i + xOff
        y2 = height - 1 * i + yOff

        x2 = max(x2, x1 + 1)  # Ensure x2 is greater than or equal to x1 + 1
        y2 = max(y2, y1 + 1)  # Ensure y2 is greater than or equal to y1 + 1

        fillClr = fillClr1 if i % 2 == 0 else fillClr2
        refConfig.blockDraw.ellipse((x1, y1, x2, y2), outline=(outlineClr), fill=fillClr)


def tripart(refConfig, paletteObj=None):

    clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
    clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))

    if random.random() < refConfig.popRandomColorProb:
        # hideos override until I can pair palettes and patterns in a
        # more flexible way
        if paletteObj.paletteName == "galah":
            clr4 = colorutils.getRandomColorHSV(0, 360, 0.65, 1.0, 0.5, 0.75, 60, 170, 255)
        else:
            clr4 = colorutils.getRandomColorHSV(0, 360, 0.65, 1.0, 0.5, 0.75, 0, 0, 255)

    refConfig.blockDraw.rectangle((0, 0, refConfig.blockWidth, refConfig.blockHeight), fill=clr1, outline=None)

    midPt = (refConfig.blockWidth / 2, refConfig.blockWidth / 2)

    poly1 = ((0, 0), (midPt[0], midPt[1]), (0, refConfig.blockHeight), (0, 0))
    refConfig.blockDraw.polygon(poly1, fill=clr2)

    poly2 = ((refConfig.blockWidth, 0), (midPt[0], midPt[1]), (refConfig.blockWidth, refConfig.blockHeight), (refConfig.blockWidth, 0))
    refConfig.blockDraw.polygon(poly2, fill=clr3)

    poly3 = ((refConfig.blockWidth, 0), (midPt[0], midPt[1]), (0, 0), (refConfig.blockWidth, 0))
    refConfig.blockDraw.polygon(poly3, fill=clr4)


def bars(refConfig, paletteObj=None):
    # clr3 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    # clr = tuple(int(a) for a in (paletteObj.c2.currentColor))
    # clr2 = tuple(int(a) for a in (paletteObj.c3.currentColor))

    clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
    clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))

    refConfig.blockDraw.rectangle((0, 0, refConfig.blockWidth, refConfig.blockHeight), fill=clr1, outline=None)

    barWidth = 4
    for count, i in enumerate(range(0, refConfig.numConcentricBoxes, 2)):
        outClr = clr2
        if count % 2 == 0 and refConfig.altLineColoring == True:
            outClr = clr2
        refConfig.blockDraw.rectangle((0, i * barWidth, refConfig.blockWidth - 1, i * barWidth), outline=(outClr), fill=None)


def peaceCross(refConfig, paletteObj=None):

    clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
    clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))

    # hideos override until I can pair palettes and patterns in a
    # more flexible way
    # if paletteObj.paletteName == "galah" :
    #     clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))

    refConfig.blockDraw.rectangle((0, 0, refConfig.blockWidth, refConfig.blockHeight), fill=clr2, outline=None)

    _blockSize = refConfig.blockWidth
    _mid = [_blockSize / 2, _blockSize / 2]
    gridSize = math.ceil(_blockSize / 4)

    _clrBase = colorutils.getRandomColorHSV(0, 360, 0.1, 0.20, 0.5, 0.75, 70, 190, 255)

    _clrBase = clr4

    for _rowCount, (_row, _col) in enumerate(itertools.product(range(4), range(4))):
        _clr = _clrBase
        _gridSize = gridSize
        _xOffset = _col * _gridSize
        _yOffset = _row * _gridSize
        _h = _gridSize
        _w = _gridSize

        if random.random() < refConfig.popRandomColorProb / 14:
            _clr = colorutils.getRandomColorHSV(0, 360, 0.2, 0.40, 0.5, 0.5, 70, 190, 255)

        # 4 squares around cross
        if _rowCount in [5, 7, 15, 13]:
            if random.random() > refConfig.popRandomColorProb / 14:
                _clr = colorutils.getRandomColorHSV(0, 360, 0.05, 0.10, 0.75, 0.95, 70, 190, 255)
            else:
                _clr = tuple(round(i * 0.75) for i in clr4)

        # cross shape
        if _rowCount in [6, 9, 10, 11, 14]:
            _clr = tuple(round(i * 0.5) for i in clr1)
            if random.random() < refConfig.popRandomColorProb / 18:
                _clr = colorutils.getRandomColorHSV(0, 360, 0.2, 0.40, 0.1, 0.3, 70, 190, 255)

        _y = _xOffset
        _x = _yOffset

        # if _rowCount %2 != 0 :
        #     if random.random() < refConfig.popRandomColorProb :
        #         _clr = colorutils.getRandomColorHSV(0, 360, 0.65, 1.0, 0.5, 0.75, 0, 0, 255)
        #     else:
        #         _clr = colorutils.getRandomColorHSV(320, 340, 0.65, 1.0, 0.5, 0.75, 0, 0, 255)

        refConfig.blockDraw.rectangle((_x, _y, _x + _w, _y + _h), fill=_clr, outline=None)


def fiboSeq(n):
    _seq = []
    _seq.extend(2 * i - 1 for i in range(n, 1, -1))
    _seq.extend(2 * i - 1 for i in range(1, n + 1))
    return _seq


def logcabin(refConfig, paletteObj=None):

    clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
    clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))

    # hideos override until I can pair palettes and patterns in a
    # more flexible way
    if paletteObj.paletteName == "galah":
        clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))

    refConfig.blockDraw.rectangle((0, 0, refConfig.blockWidth, refConfig.blockHeight), fill=clr3, outline=None)

    _blockSize = refConfig.blockWidth - 0
    _mid = [_blockSize / 2, _blockSize / 2]
    fibo = 7
    _seq = fiboSeq(fibo)
    numberOfBars = len(_seq)
    gridSize = math.ceil(_blockSize / numberOfBars)

    for _rowCount, col in enumerate(_seq):
        _h = col * gridSize
        _w = gridSize
        _y = round(_mid[1] - _h / 2)
        _x = round((_rowCount) * gridSize)
        _clr = clr1
        if _rowCount % 2 != 0:
            if random.random() < refConfig.popRandomColorProb:
                _clr = colorutils.getRandomColorHSV(0, 360, 0.65, 1.0, 0.5, 0.75, 0, 0, 255)
            else:
                _clr = colorutils.getRandomColorHSV(320, 340, 0.65, 1.0, 0.5, 0.75, 0, 0, 255)

        _clrReduced = tuple(round(i * 0.85) for i in _clr) if _rowCount < numberOfBars / 2 else tuple(round(i * 1.0) for i in _clr)

        if col == 1:
            _clrReduced = (255, 0, 100, 255)
        refConfig.blockDraw.rectangle((_x, _y, _x + _w, _y + _h), fill=_clrReduced, outline=None)

    for _rowCount, row in enumerate(_seq):
        _w = row * gridSize
        _x = round(_mid[0] - _w / 2)
        _y = round((_rowCount) * gridSize)
        _h = gridSize
        _clr = clr1
        if _rowCount % 2 != 0:
            if random.random() < refConfig.popRandomColorProb:
                _clr = colorutils.getRandomColorHSV(0, 360, 0.65, 1.0, 0.5, 0.75, 0, 0, 255)
            else:
                _clr = colorutils.getRandomColorHSV(320, 340, 0.65, 1.0, 0.5, 0.75, 0, 0, 255)
        _clrReduced = tuple(round(i * 0.65) for i in _clr) if _rowCount < numberOfBars / 2 else tuple(round(i * 1.0) for i in _clr)
        if row == 1:
            _clrReduced = (255, 0, 100, 255)
        refConfig.blockDraw.rectangle((_x, _y, _x + _w, _y + _h), fill=_clrReduced, outline=None)


def littleCones(refConfig, paletteObj=None):
    clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
    clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))

    refConfig.blockDraw.rectangle((0, 0, refConfig.blockWidth, refConfig.blockHeight), fill=clr1, outline=None)
    _mid = [refConfig.blockWidth / 2, refConfig.blockHeight / 2]
    fibo = 5
    numberOfBars = fibo + fibo - 1
    gridSize = math.ceil(refConfig.blockWidth / numberOfBars / 1)

    for row in range(2 * fibo, 0, -1):
        _w = row * gridSize
        # if row >= fibo:
        #     _w = row * gridSize
        _x = _mid[0] - _w / 2
        _y = row * gridSize
        _clr = clr4
        if row % 2 == 0:
            # _clr = colorutils.getRandomColorHSV(0, 360, 0.5, 0.5, 0.5, 0.5, 0, 0, 255)
            _clr = clr2
        refConfig.blockDraw.rectangle((_x, _y, _x + _w, _y + gridSize), fill=_clr, outline=None)


def coloredBlocks(refConfig, paletteObj=None):

    clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
    clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))

    refConfig.blockDraw.rectangle((0, 0, refConfig.blockWidth, refConfig.blockHeight), fill=clr2, outline=None)
    # refConfig.blockDraw.rectangle((5, 5, 10, 15), fill=(255,0,0,255), outline=None)

    # count = 0
    # barWidth = 4
    # for i in range(refConfig.numConcentricBoxes, 2):

    #     if refConfig.altLineColoring == True:
    #         outClr = clr2
    #         if count % 2 == 0:
    #             outClr = clr
    #     else:
    #         outClr = clr

    #     outClr = None
    #     # refConfig.blockDraw.rectangle((0,i * barWidth,refConfig.blockWidth-1,i * barWidth), outline=(outClr), fill=None)
    #     count += 1


def concentricBoxes(refConfig, paletteObj=None):
    # clr3 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    # clr = tuple(int(a) for a in (paletteObj.c2.currentColor))
    # clr2 = tuple(int(a) for a in (paletteObj.c3.currentColor))

    clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
    clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))

    refConfig.blockDraw.rectangle((0, 0, refConfig.blockWidth, refConfig.blockHeight), fill=clr1, outline=None)

    count = 0
    numConcentricBoxes = refConfig.numConcentricBoxes * 3

    # pieceLogger(f"numConcentricBoxes = {numConcentricBoxes}")

    for i in range(0, numConcentricBoxes, 2):

        if refConfig.altLineColoring == True:
            outClr = clr3
            if count % 2 == 0:
                outClr = clr2
        else:
            outClr = clr2

        try:
            if refConfig.blockWidth - 1 * i >= i - 1:
                refConfig.blockDraw.rectangle((i - 1, i - 1, refConfig.blockWidth - 1 * i, refConfig.blockHeight - 1 * i), outline=(outClr), fill=None)
                count += 1
        except Exception as e:
            print(f"Concentric boxes error prob too many {e}")


def decoBoxes(refConfig, paletteObj=None):

    # clr3 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    # clr = tuple(int(a) for a in (paletteObj.c2.currentColor))
    # clr2 = tuple(int(a) for a in (paletteObj.c3.currentColor))

    clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
    clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))

    refConfig.blockDraw.rectangle((0, 0, refConfig.blockWidth, refConfig.blockHeight), fill=clr1, outline=None)

    clr = clr1
    numConcentricBoxes = refConfig.blockWidth + 1
    altLineColoring = True
    w = round(random.uniform(2, 5))
    w = refConfig.decoBoxBandWidth
    width = refConfig.blockWidth

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
            outClr = clr3
            if count % 2 == 0:
                outClr = clr2
        else:
            outClr = clr2

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

    refConfig.blockImage.paste(temp, (xOff, yOff), temp)


def diamond(refConfig, paletteObj=None):  # sourcery skip: low-code-quality, use-itertools-product
    # clr = tuple(int(a) for a in paletteObj.c2.currentColor)
    # clr2 = tuple(int(a) for a in paletteObj.c1.currentColor)

    clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
    clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))

    x = refConfig.xIncrementer
    y = refConfig.yIncrementer

    # needs to be in odd grid
    refConfig.blockDraw.rectangle((0, 0, refConfig.blockWidth, refConfig.blockHeight), fill=clr1, outline=None)

    step = refConfig.diamondStep
    row = 1
    delta = 0
    w = 0
    h = 0
    rows = refConfig.numRows
    blockHeight = round(refConfig.blockHeight / rows)
    mid = round(blockHeight / 2)

    for rw in range(rows):
        for c in range(rows):
            for i in range(0, blockHeight, step * 2):
                for r in range(row):
                    x = r + mid - row / 2 + c * blockHeight
                    y = i + refConfig.yIncrementer + rw * blockHeight

                    if y >= blockHeight * rows:
                        y -= blockHeight * rows

                    if (r % 2) != 1:
                        refConfig.blockDraw.rectangle((x, y, w + x, h + y), fill=(clr2), outline=None)
                if refConfig.diamondUseTriangles == False:
                    row = 2 * i + step + delta
                    if i > (blockHeight / 2):
                        row = round(2 * (blockHeight - i)) + delta
                        # delta += -2
                else:
                    row = i + step

    refConfig.yIncrementer += refConfig.ySpeed

    if refConfig.yIncrementer >= blockHeight * 2:
        refConfig.yIncrementer = 0


def diagonalMove(refConfig, paletteObj=None):
    # clr3 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    # clr = tuple(int(a) for a in (paletteObj.c2.currentColor))
    # clr2 = tuple(int(a) for a in (paletteObj.c3.currentColor))

    clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
    clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))

    w = 4
    h = 4
    x = refConfig.xIncrementer
    y = refConfig.yIncrementer

    refConfig.blockDraw.rectangle((0, 0, refConfig.blockWidth, refConfig.blockHeight), fill=clr1, outline=None)
    refConfig.blockDraw.rectangle((x, y, w + x, h + y), fill=(clr2), outline=None)
    refConfig.xIncrementer += 1
    refConfig.yIncrementer += 1

    if refConfig.xIncrementer >= refConfig.blockWidth - 4:
        refConfig.xIncrementer = 0
    if refConfig.yIncrementer >= refConfig.blockHeight - 4:
        refConfig.yIncrementer = 0


def reMove(refConfig, paletteObj=None):

    w = 4
    h = 4
    x = refConfig.xIncrementer
    y = refConfig.yIncrementer

    # bgColor = (clr1[0], clr1[1], clr1[3], 255)

    # clr3 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    # clr = tuple(int(a) for a in (paletteObj.c2.currentColor))
    # clr2 = tuple(int(a) for a in (paletteObj.c3.currentColor))

    clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
    clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))

    refConfig.blockDraw.rectangle((0, 0, refConfig.blockWidth, refConfig.blockHeight), fill=clr1, outline=None)

    lineMult = refConfig.lineDiff * 2
    numLines = round(refConfig.blockWidth / refConfig.lineDiff * 2)

    y1 = 0
    for i in range(numLines):

        x1 = -2 * refConfig.blockWidth + refConfig.xIncrementer + i * lineMult
        x2 = -2 * refConfig.blockWidth + refConfig.blockWidth + refConfig.xIncrementer + i * lineMult
        y2 = refConfig.blockHeight

        refConfig.blockDraw.line((x1, y1, x2, y2), fill=(clr2))
        if refConfig.useDoubleLine == True:
            refConfig.blockDraw.line(
                (
                    -2 * refConfig.blockWidth + refConfig.xIncrementer + i * lineMult + 1,
                    0,
                    -2 * refConfig.blockWidth + refConfig.blockWidth + refConfig.xIncrementer + i * lineMult + 1,
                    refConfig.blockHeight,
                ),
                fill=(clr3),
            )

    refConfig.xIncrementer += refConfig.xSpeed
    refConfig.yIncrementer += 0

    """
    """
    if refConfig.xIncrementer > (refConfig.blockWidth + 0):
        refConfig.xIncrementer = -refConfig.xSpeed
    if refConfig.yIncrementer >= refConfig.blockHeight - 4:
        refConfig.yIncrementer = 0


def grainLines(refConfig, paletteObj=None):

    # print(f"grainLines running {grainLines}")
    bgFill = tuple(int(a) for a in (paletteObj.c1.currentColor))
    patternFill = tuple(int(a) for a in (paletteObj.c4.currentColor))
    patternOutLine = tuple(int(a) for a in (paletteObj.c3.currentColor))
    hilight = tuple(int(a) for a in (paletteObj.c4.currentColor))

    if random.random() < refConfig.popRandomColorProb:
        # hideos override until I can pair palettes and patterns in a
        # more flexible way
        if paletteObj.paletteName == "galah":
            hilight = colorutils.getRandomColorHSV(0, 360, 0.65, 1.0, 0.5, 0.75, 60, 170, 255)
        else:
            hilight = colorutils.getRandomColorHSV(0, 360, 0.65, 1.0, 0.5, 0.75, 0, 0, 255)

    refConfig.blockDraw.rectangle((0, 0, refConfig.blockWidth, refConfig.blockHeight), fill=bgFill, outline=None)

    midPt = (refConfig.blockWidth / 2, refConfig.blockWidth / 2)
    rndFactor = 0.01
    rnd = random.random() + rndFactor
    rnd2 = random.random() + rndFactor

    _w = round(random.uniform(1, 3))
    _gradientCount = 0
    _gradientPeriod = round(random.uniform(3, 8))
    _lineGap = int(random.uniform(1, 2))
    for yPt in range(-refConfig.blockHeight, 2 * refConfig.blockHeight, _lineGap):
        _lastX = 0
        _lastY = 0
        for xPt in range(-32, refConfig.blockWidth, _w):
            _x1 = _lastX
            _x2 = xPt * _w
            _y1 = _lastY
            _y2 = noise.pnoise2(rnd * _x2 / 120 + 0.2, rnd2 * yPt / 120) * 100
            refConfig.blockDraw.line((_x1, _y1 + yPt, _x2, _y2 + yPt), fill=(patternFill[0], patternFill[1], patternFill[2], round(255 * (_gradientCount / _gradientPeriod + 0.45))))
            _lastX = _x2
            _lastY = _y2
        _gradientCount += 1
        if _gradientCount > _gradientPeriod:
            _gradientCount = 0
            _gradientPeriod = round(random.uniform(3, 8))
            rnd2 = random.random() + rndFactor
    # poly1 = ((0, 0), (midPt[0], midPt[1]), (0, refConfig.blockHeight), (0, 0))
    # refConfig.blockDraw.polygon(poly1, fill=clr2)

    # poly2 = ((refConfig.blockWidth, 0), (midPt[0], midPt[1]), (refConfig.blockWidth, refConfig.blockHeight), (refConfig.blockWidth, 0))
    # refConfig.blockDraw.polygon(poly2, fill=clr3)

    # poly3 = ((refConfig.blockWidth, 0), (midPt[0], midPt[1]), (0, 0), (refConfig.blockWidth, 0))
    # refConfig.blockDraw.polygon(poly3, fill=clr4)


def colorGrid(refConfig, paletteObj=None):
    # clr3 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    # clr = tuple(int(a) for a in (paletteObj.c2.currentColor))
    # clr2 = tuple(int(a) for a in (paletteObj.c3.currentColor))

    clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
    clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))

    bgFill = tuple(int(a) for a in (paletteObj.c1.currentColor))

    refConfig.blockDraw.rectangle((0, 0, refConfig.blockWidth, refConfig.blockHeight), fill=clr1, outline=None)

    _divs = round(random.uniform(1, 4))
    _w = round(refConfig.blockWidth / _divs)
    _h = round(refConfig.blockHeight / _divs)

    for _r in range(_divs):
        for _c in range(_divs):
            clr = colorutils.getRandomColorHSV(0, 360, 0.3, 1.0, 0.3, 0.90, 100, 170, 255, refConfig.brightness)
            if (_c % 2 == 0 or _r % 2 == 0) and random.random() < 0.5:
                # rosetone ;)
                clr = colorutils.getRandomColorHSV(320, 355, 0.3, 1.0, 0.3, 0.90, 100, 170, 255, refConfig.brightness)
            refConfig.blockDraw.rectangle((_c * _w, _r * _h, _c * _w + _w, _r * _h + _h), outline=None, fill=clr)


def colorGridTriangles(refConfig, paletteObj=None):
    # clr3 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    # clr = tuple(int(a) for a in (paletteObj.c2.currentColor))
    # clr2 = tuple(int(a) for a in (paletteObj.c3.currentColor))

    clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
    clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))

    bgFill = tuple(int(a) for a in (paletteObj.c1.currentColor))

    refConfig.blockDraw.rectangle((0, 0, refConfig.blockWidth, refConfig.blockHeight), fill=clr1, outline=None)

    _divs = round(random.uniform(1, 4))
    _w = round(refConfig.blockWidth / _divs)
    _h = round(refConfig.blockHeight / _divs)

    for _r in range(_divs):
        for _c in range(_divs):
            clr1 = colorutils.getRandomColorHSV(0, 360, 0.3, 1.0, 0.3, 0.90, 100, 170, 255, refConfig.brightness)
            clr2 = colorutils.getRandomColorHSV(0, 360, 0.3, 1.0, 0.3, 0.90, 100, 170, 255, refConfig.brightness)
            if (_c % 2 == 0 or _r % 2 == 0) and random.random() < 0.5:
                # rosetone ;)
                clr1 = colorutils.getRandomColorHSV(320, 355, 0.3, 1.0, 0.3, 0.90, 100, 170, 255, refConfig.brightness)
                clr2 = colorutils.getRandomColorHSV(320, 355, 0.3, 1.0, 0.3, 0.90, 100, 170, 255, refConfig.brightness)
            # refConfig.blockDraw.rectangle(( _c * _w, _r * _h, _c * _w + _w, _r * _h + _h), outline=(0,0,0,125), fill=clr)
            refConfig.blockDraw.polygon(((_c * _w, _r * _h), (_c * _w + _w, _r * _h + _h), (_c * _w, _r * _h + _h), (_c * _w, _r * _h)), outline=None, fill=clr1)
            refConfig.blockDraw.polygon(((_c * _w, _r * _h), (_c * _w + _w, _r * _h), (_c * _w + _w, _r * _h + _h), (_c * _w, _r * _h)), outline=None, fill=clr2)


def TVTestPattern(refConfig, paletteObj=None):
    # clr3 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    # clr = tuple(int(a) for a in (paletteObj.c2.currentColor))
    # clr2 = tuple(int(a) for a in (paletteObj.c3.currentColor))

    clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
    clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))

    bgFill = tuple(int(a) for a in (paletteObj.c1.currentColor))

    _alpha = int(random.uniform(200,250))
    # pieceLogger(_alpha)

    refConfig.blockDraw.rectangle((0, 0, refConfig.blockWidth, refConfig.blockHeight), fill=clr1, outline=None)

    tileSizeWidth = round(refConfig.blockWidth / 7)
    tileSizeHeight = round(refConfig.blockHeight / 3)
    bottomY = 2 * round(tileSizeHeight + tileSizeHeight / 6) - 1
    bottomH = 2 * round(tileSizeHeight / 3)

    # Top 2/3: 7 primary/secondary SMPTE bars at 75%
    for col, hsv in enumerate(
        [
            (0, 0, 0.75),
            (60, 1.0, 0.75),
            (180, 1.0, 0.75),
            (120, 1.0, 0.75),
            (300, 1.0, 0.75),
            (0, 1.0, 0.75),
            (220, 1.0, 0.75),
        ]
    ):
        xPos = col * tileSizeWidth
        refConfig.blockDraw.rectangle(
            (xPos, 0, xPos + tileSizeWidth, 2 * tileSizeHeight),
            fill=colorutils.HSVToRGB(*hsv, _alpha, refConfig.brightness),
            outline=None,
        )

    # Middle strip: reversed colors interleaved with near-black
    for col, hsv in enumerate(
        [
            (220, 1.0, 0.75),
            (0, 0, 0.07),
            (300, 1.0, 0.75),
            (0, 0, 0.07),
            (180, 1.0, 0.75),
            (0, 0, 0.07),
            (0, 0, 0.75),
        ]
    ):
        xPos = col * tileSizeWidth
        refConfig.blockDraw.rectangle(
            (xPos, 2 * tileSizeHeight, xPos + tileSizeWidth - 1, 2 * tileSizeHeight + round(tileSizeHeight / 3) - 1),
            fill=colorutils.HSVToRGB(*hsv, _alpha, refConfig.brightness),
            outline=None,
        )

    # Bottom-left: I, White, Q tiles across left half
    leftTileWidth = round(refConfig.blockWidth / 2 / 3)
    for col, hsv in enumerate([(214, 1.0, 0.3), (0, 0, 1.0), (268, 1.0, 0.42)]):
        xPos = col * leftTileWidth
        refConfig.blockDraw.rectangle(
            (xPos, bottomY, xPos + leftTileWidth, bottomY + bottomH),
            fill=colorutils.HSVToRGB(*hsv, _alpha, refConfig.brightness),
            outline=None,
        )

    # Bottom-center: near-black from midpoint to 5th column
    refConfig.blockDraw.rectangle(
        (round(refConfig.blockWidth / 2), bottomY, round(5 * tileSizeWidth) - 1, bottomY + bottomH),
        fill=colorutils.HSVToRGB(0, 0, 0.07, _alpha, refConfig.brightness),
        outline=None,
    )

    # Bottom-right: 6 near-black gradient tiles
    smallTileWidth = tileSizeWidth / 3
    for col, hsv in enumerate(
        [
            (0, 0, 0.0),
            (0, 0, 0.04),
            (0, 0, 0.07),
            (0, 0, 0.11),
            (0, 0, 0.07),
            (0, 0, 0.07),
        ]
    ):
        xPos = round(5 * tileSizeWidth) + int(smallTileWidth * col)
        refConfig.blockDraw.rectangle(
            (xPos, bottomY, xPos + int(smallTileWidth), bottomY + bottomH),
            fill=colorutils.HSVToRGB(*hsv, _alpha, refConfig.brightness),
            outline=None,
        )


# ----------------------------------------------------##----------------------------------------------------#


def chaikins_corner_cutting(coords, refinements=5, ratio=0.75):
    # https://stackoverflow.com/questions/47068504/where-to-find-python-implementation-of-chaikins-corner-cutting-algorithm
    coords = np.array(coords)

    for _ in range(refinements):
        L = coords.repeat(2, axis=0)
        R = np.empty_like(L)
        R[0] = L[0]
        R[2::2] = L[1:-1:2]
        R[1:-1:2] = L[2::2]
        R[-1] = L[-1]
        coords = L * ratio + R * (1.00 - ratio)

    return coords


def floralConfig(refConfig):
    refConfig.floral = ArtWorkConfig("Florals", True)

    _choice = random.randint(0, 7)
    # removing python 3.10 match code for now
    # match _choice:

    if _choice == 0:
            refConfig.floral._petals = 9
            refConfig.floral._w = refConfig.blockWidth * 0.51
            refConfig.floral._lobe = refConfig.floral._w * 0.8
            refConfig.floral._h = refConfig.blockWidth / 8

    if _choice == 1:
            refConfig.floral._petals = 7
            refConfig.floral._w = refConfig.blockWidth * 0.51
            refConfig.floral._lobe = refConfig.floral._w * 0.8
            refConfig.floral._h = refConfig.blockWidth / 8

    if _choice == 2:
            refConfig.floral._petals = 4
            refConfig.floral._w = refConfig.blockWidth * 0.51
            refConfig.floral._lobe = refConfig.floral._w * 0.7
            refConfig.floral._h = refConfig.blockWidth / 4

    if _choice == 3:
            refConfig.floral._petals = 5
            refConfig.floral._w = refConfig.blockWidth * 0.51
            refConfig.floral._lobe = refConfig.floral._w * 0.7
            refConfig.floral._h = refConfig.blockWidth / 4

    if _choice == 4:
            refConfig.floral._petals = 3
            refConfig.floral._w = refConfig.blockWidth * 0.51
            refConfig.floral._lobe = refConfig.floral._w * 0.4
            refConfig.floral._h = refConfig.blockWidth / 4

    if _choice == 5:
            refConfig.floral._petals = 4
            refConfig.floral._w = refConfig.blockWidth * 0.6
            refConfig.floral._lobe = refConfig.floral._w * 0.2
            refConfig.floral._h = refConfig.blockWidth / 4

    if _choice == 6:
            refConfig.floral._petals = 5
            refConfig.floral._w = refConfig.blockWidth * 0.6
            refConfig.floral._lobe = refConfig.floral._w * 0.2
            refConfig.floral._h = refConfig.blockWidth / 4

    if _choice == 7:
            refConfig.floral._lobe = round(random.uniform(4, refConfig.blockWidth * 0.7))
            refConfig.floral._w = round(random.uniform(refConfig.floral._lobe, refConfig.blockWidth * 0.8))
            refConfig.floral._h = round(random.uniform(4, refConfig.blockHeight / 8))
            # refConfig.floral._extension = refConfig.blockWidth / 2
            refConfig.floral._petals = round(random.uniform(4, 7))
    # refConfig.floral.debugSelf()


def petals(refConfig, paletteObj=None):

    # print(f"grainLines running {grainLines}")
    # print(paletteObj.c1.currentColor)
    bgFill = tuple(int(a) for a in (paletteObj.c1.currentColor))
    patternFill = tuple(int(a) for a in (paletteObj.c4.currentColor))
    patternOutLine = tuple(int(a) for a in (paletteObj.c3.currentColor))
    hilight = tuple(int(a) for a in (paletteObj.c4.currentColor))

    if random.random() < refConfig.popRandomColorProb:
        # hideos override until I can pair palettes and patterns in a
        # more flexible way
        if paletteObj.paletteName == "galah":
            hilight = colorutils.getRandomColorHSV(0, 360, 0.65, 1.0, 0.5, 0.75, 60, 170, 255)
        else:
            hilight = colorutils.getRandomColorHSV(0, 360, 0.65, 1.0, 0.5, 0.75, 0, 0, 255)

    refConfig.blockDraw.rectangle((0, 0, refConfig.blockWidth, refConfig.blockHeight), fill=bgFill, outline=None)

    midPt = (round(refConfig.blockWidth / 2), round(refConfig.blockWidth / 2))
    rndFactor = 0.01
    rnd = random.random() + rndFactor
    rnd2 = random.random() + rndFactor

    points = [
        midPt,
        (midPt[0] + refConfig.floral._lobe, midPt[1] - refConfig.floral._h),
        (midPt[0] + refConfig.floral._w, midPt[1]),
        (midPt[0] + refConfig.floral._lobe, midPt[1] + refConfig.floral._h),
        midPt,
    ]
    res = chaikins_corner_cutting(points, 6).tolist()

    _pts = tuple(tuple(_e) for _e in res)

    _petalImg = Image.new("RGBA", (refConfig.blockWidth, refConfig.blockHeight))
    _floralImg = Image.new("RGBA", (refConfig.blockWidth, refConfig.blockHeight))
    _petalDraw = ImageDraw.Draw(_petalImg)
    _petalDraw.polygon(_pts, fill=patternFill)
    _petalDraw.line((midPt[0], midPt[1], midPt[0] + refConfig.floral._w / 2, midPt[1] + 3), fill=bgFill, width=1)
    _petalDraw.line((midPt[0], midPt[1], midPt[0] + refConfig.floral._w / 2, midPt[1] - 3), fill=bgFill, width=1)

    _angle = 360 / refConfig.floral._petals

    for _p in range(refConfig.floral._petals):
        _floralImg.paste(_petalImg.rotate(_angle * _p), (0, 0), _petalImg.rotate(_angle * _p))

    _sizeChange = random.uniform(0.25, 0.85)
    _newSize = (round(refConfig.blockWidth * _sizeChange), round(refConfig.blockWidth * _sizeChange))
    _floralTemp = _floralImg.resize((_newSize[0], _newSize[1]), 1)
    refConfig.blockImage.paste(_floralTemp, (midPt[0], 0), _floralTemp)
    refConfig.blockImage.paste(_floralTemp, (-midPt[0], 0), _floralTemp)
    refConfig.blockImage.paste(_floralTemp, (0, midPt[1]), _floralTemp)
    refConfig.blockImage.paste(_floralTemp, (0, -midPt[1]), _floralTemp)

    # refConfig.blockDraw.rectangle((0,0,10,10), fill=(random.randint(0,255),random.randint(0,255),random.randint(0,255),255))

    if random.random() < 0.01:
        floralConfig(refConfig)
