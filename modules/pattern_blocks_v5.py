#!/usr/bin/python
import argparse
import itertools
import math
import random
import time
import types

from modules.configuration import bcolors
from modules.configuration import ArtWorkConfig
from modules import badpixels, coloroverlay, colorutils, panelDrawing, configuration
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps, ImageFilter
import numpy as np
import noise
from noise import *


def fishscalepatternFunction(func):
    """Decorator for fish scale pattern drawing functions.
    This decorator wraps a function that returns drawing parameters for a fish scale pattern, and performs the drawing using those parameters. It abstracts the common drawing logic for fish scale patterns, allowing the decorated function to focus on color and configuration selection.
    Args:
        func: A function that returns a tuple containing (config, bgFill, patternFill, patternOutLine, hilight).
    Returns:
        A wrapper function that executes the drawing logic for the fish scale pattern.
    """

    def wrapper(*args):
        res = func(*args)
        config = res[0]
        bgFill = res[1]
        patternFill = res[2]
        patternOutLine = res[3]
        hilight = res[4]
        w = 4
        h = 4
        x = config.xIncrementer
        y = config.yIncrementer

        config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=bgFill, outline=None)

        numRows = config.numShingleRows
        boxWidth = config.blockWidth / numRows

        for r in range(numRows, -1, -1):
            yPos = -2 + r * boxWidth
            for i in range(3):
                config.blockDraw.ellipse((i * boxWidth - boxWidth / 2, yPos, i * boxWidth + boxWidth - boxWidth / 2, yPos + boxWidth), outline=(patternOutLine), fill=patternFill)

            for i in range(2):
                config.blockDraw.ellipse((i * boxWidth, yPos - boxWidth / 2, i * boxWidth + boxWidth, yPos + boxWidth / 2), outline=(patternOutLine), fill=patternFill)

    return wrapper


@fishscalepatternFunction
def fishScales3(config, paletteObj):
    """Generates parameters for a fish scale pattern using the provided palette.
    Returns the configuration and color values needed to draw a fish scale pattern with the specified palette object.
    Args:
        config: The configuration object containing drawing parameters.
        paletteObj: The palette object providing color values.
    Returns:
        A tuple containing (config, bgFill, patternFill, patternOutLine, hilight).
    """
    # return "A","B","C"
    bgFill = tuple(int(a) for a in (paletteObj.c1.currentColor))
    patternFill = tuple(int(a) for a in (paletteObj.c1.currentColor))
    patternOutLine = tuple(int(a) for a in (paletteObj.c4.currentColor))
    hilight = tuple(int(a) for a in (paletteObj.c4.currentColor))
    return config, bgFill, patternFill, patternOutLine, hilight


@fishscalepatternFunction
def fishScales2(config, paletteObj):
    # return "B","C","A"
    bgFill = tuple(int(a) for a in (paletteObj.c1.currentColor))
    patternFill = tuple(int(a) for a in (paletteObj.c2.currentColor))
    patternOutLine = tuple(int(a) for a in (paletteObj.c1.currentColor))
    hilight = tuple(int(a) for a in (paletteObj.c4.currentColor))
    return config, bgFill, patternFill, patternOutLine, hilight


@fishscalepatternFunction
def fishScales(config, paletteObj):
    # return "B","C","A"
    bgFill = tuple(int(a) for a in (paletteObj.c3.currentColor))
    patternFill = tuple(int(a) for a in (paletteObj.c3.currentColor))
    patternOutLine = tuple(int(a) for a in (paletteObj.c1.currentColor))
    hilight = tuple(int(a) for a in (paletteObj.c4.currentColor))
    return config, bgFill, patternFill, patternOutLine, hilight


# --------------------------------------- #


def gothicPatternFunction(func):
    def wrapper(*args):
        res = func(*args)
        config = res[0]
        bgFill = res[1]
        patternFill = res[2]
        patternOutLine = res[3]
        hilight = res[4]
        w = 4
        h = 4
        x = config.xIncrementer
        y = config.yIncrementer

        config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=bgFill, outline=None)

        numLines = 1
        steps = 1
        _w = config.blockWidth / 2
        _h = config.blockHeight / 2

        _draw_circles(config, _w - _w / 2, 0, numLines, steps, patternFill, patternFill, patternFill, _w, _h)
        _draw_circles(config, _w - _w / 2, _h, numLines, steps, patternFill, patternFill, patternFill, _w, _h)
        _draw_circles(config, 0, _h - _h / 2, numLines, steps, patternFill, patternFill, patternFill, _w, _h)
        _draw_circles(config, _w, _h - _h / 2, numLines, steps, patternFill, patternFill, patternFill, _w, _h)

    return wrapper


@gothicPatternFunction
def gothic1(config, paletteObj):
    # return "A","B","C"
    bgFill = tuple(int(a) for a in (paletteObj.c1.currentColor))
    patternFill = tuple(int(a) for a in (paletteObj.c2.currentColor))
    patternOutLine = tuple(int(a) for a in (paletteObj.c4.currentColor))
    hilight = tuple(int(a) for a in (paletteObj.c4.currentColor))
    return config, bgFill, patternFill, patternOutLine, hilight


@gothicPatternFunction
def gothic2(config, paletteObj):
    # return "B","C","A"
    bgFill = tuple(int(a) for a in (paletteObj.c1.currentColor))
    patternFill = tuple(int(a) for a in (paletteObj.c4.currentColor))
    patternOutLine = tuple(int(a) for a in (paletteObj.c1.currentColor))
    hilight = tuple(int(a) for a in (paletteObj.c4.currentColor))
    return config, bgFill, patternFill, patternOutLine, hilight


# --------------------------------------- #


def ballsPatternFunction(func):
    def wrapper(*args):
        res = func(*args)
        config = res[0]
        bgFill = res[1]
        patternFill = res[2]
        patternOutLine = res[3]
        hilight = res[4]
        w = 4
        h = 4
        x = config.xIncrementer
        y = config.yIncrementer

        config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=bgFill, outline=None)

        numRows = config.numDotRows
        boxWidth = config.blockWidth
        density = numRows * 4
        dotWidth = boxWidth / 2 / numRows - 2
        outline = None

        for r in range(numRows):

            for i in range(density):
                yPos = r * (dotWidth * 2) + r * 4
                config.blockDraw.ellipse(
                    (i * 2 * boxWidth / density - boxWidth / density, yPos, i * 2 * boxWidth / density - boxWidth / density + dotWidth, yPos + dotWidth),
                    outline=(outline),
                    fill=patternFill,
                )

            for i in range(density):
                config.blockDraw.ellipse(
                    (i * 2 * boxWidth / density, yPos + 2 * boxWidth / density, i * 2 * boxWidth / density + dotWidth, yPos + 2 * boxWidth / density + dotWidth),
                    outline=(outline),
                    fill=patternFill,
                )

    return wrapper


@ballsPatternFunction
def balls(config, paletteObj):
    # return "A","B","C"
    bgFill = tuple(int(a) for a in (paletteObj.c1.currentColor))
    patternFill = tuple(int(a) for a in (paletteObj.c2.currentColor))
    patternOutLine = tuple(int(a) for a in (paletteObj.c4.currentColor))
    hilight = tuple(int(a) for a in (paletteObj.c4.currentColor))
    return config, bgFill, patternFill, patternOutLine, hilight


@ballsPatternFunction
def balls_hili(config, paletteObj):
    # return "B","C","A"
    bgFill = tuple(int(a) for a in (paletteObj.c1.currentColor))
    patternFill = tuple(int(a) for a in (paletteObj.c4.currentColor))
    patternOutLine = tuple(int(a) for a in (paletteObj.c1.currentColor))
    hilight = tuple(int(a) for a in (paletteObj.c4.currentColor))
    return config, bgFill, patternFill, patternOutLine, hilight


# --------------------------------------- #


def compassPatternFunction(func):
    def wrapper(*args):
        res = func(*args)
        config = res[0]
        bgFill = res[1]
        patternFill = res[2]
        patternOutLine = res[3]
        hilight = res[4]
        w = 4
        h = 4
        x = config.xIncrementer
        y = config.yIncrementer

        config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=bgFill, outline=None)

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
            config.blockDraw.polygon(isoTriangle, fill=patternFill, outline=outlineClr)
            isoTriangle = (
                (midx - grid * len1, midy),
                (midx, midy - grid),
                (midx + grid * len1, midy),
                (midx, midy + grid),
                (midx - grid * len1, midy),
            )
            config.blockDraw.polygon(isoTriangle, fill=patternFill, outline=outlineClr)
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
            config.blockDraw.polygon(isoTriangle, fill=patternFill, outline=outlineClr)

    return wrapper


@compassPatternFunction
def compass(config, paletteObj):
    # return "A","B","C"
    bgFill = tuple(int(a) for a in (paletteObj.c1.currentColor))
    patternFill = tuple(int(a) for a in (paletteObj.c2.currentColor))
    patternOutLine = tuple(int(a) for a in (paletteObj.c3.currentColor))
    hilight = tuple(int(a) for a in (paletteObj.c4.currentColor))
    return config, bgFill, patternFill, patternOutLine, hilight


@compassPatternFunction
def compass_hili(config, paletteObj):
    # return "B","C","A"
    bgFill = tuple(int(a) for a in (paletteObj.c1.currentColor))
    patternFill = tuple(int(a) for a in (paletteObj.c4.currentColor))
    patternOutLine = tuple(int(a) for a in (paletteObj.c3.currentColor))
    hilight = tuple(int(a) for a in (paletteObj.c4.currentColor))
    return config, bgFill, patternFill, patternOutLine, hilight


# --------------------------------------- #


def randomizerPatternFunction(func):
    def wrapper(*args):
        res = func(*args)
        config = res[0]
        bgFill = (res[1][0], res[1][1], res[1][2], 190)
        patternFill = res[2]
        patternOutLine = res[3]
        hilight = res[4]
        w = 4
        h = 4
        x = config.xIncrementer
        y = config.yIncrementer

        w = config.randomBlockWidth
        h = config.randomBlockHeight

        config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=bgFill, outline=None)

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

    return wrapper


@randomizerPatternFunction
def randomizer(config, paletteObj):
    # return "A","B","C"
    bgFill = tuple(int(a) for a in (paletteObj.c1.currentColor))
    patternFill = tuple(int(a) for a in (paletteObj.c2.currentColor))
    patternOutLine = tuple(int(a) for a in (paletteObj.c3.currentColor))
    hilight = tuple(int(a) for a in (paletteObj.c4.currentColor))
    return config, bgFill, patternFill, patternOutLine, hilight


@randomizerPatternFunction
def randomizer2(config, paletteObj):
    # return "B","C","A"
    bgFill = tuple(int(a) for a in (paletteObj.c1.currentColor))
    patternFill = tuple(int(a) for a in (paletteObj.c4.currentColor))
    patternOutLine = tuple(int(a) for a in (paletteObj.c1.currentColor))
    hilight = tuple(int(a) for a in (paletteObj.c4.currentColor))
    return config, bgFill, patternFill, patternOutLine, hilight


@randomizerPatternFunction
def randomizer3(config, paletteObj):
    # return "B","C","A"
    bgFill = tuple(int(a) for a in (paletteObj.c1.currentColor))
    patternFill = tuple(int(a) for a in (paletteObj.c4.currentColor))
    patternOutLine = tuple(int(a) for a in (paletteObj.c1.currentColor))
    hilight = tuple(int(a) for a in (paletteObj.c4.currentColor))
    return config, bgFill, patternFill, patternOutLine, hilight


# --------------------------------------- #


def wavePatternFunction(func):
    def wrapper(*args):
        res = func(*args)
        config = res[0]
        bgFill = res[1]
        patternFill = res[2]
        patternOutLine = res[3]
        hilight = res[4]
        w = 4
        h = 4
        x = config.xIncrementer
        y = config.yIncrementer

        # clr3 = tuple(int(a) for a in (paletteObj.c1.currentColor))
        # clr = tuple(int(a) for a in (paletteObj.c2.currentColor))
        # clr2 = tuple(int(a) for a in (paletteObj.c3.currentColor))

        # clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
        # clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
        # clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
        # clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))

        config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=bgFill, outline=bgFill)

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
            config.blockDraw.polygon((a, b, c, a), fill=patternFill, outline=None)

        phase = round(config.blockWidth / config.phaseFactor)
        for i in range(0, numPoints, steps2):
            angle = (i - config.speedFactor * config.xIncrementer + phase) * rads
            angle2 = (i - config.speedFactor * config.xIncrementer + phase + steps2) * rads
            a = (i, math.cos(angle) * amplitude2 + yOffset2)
            b = (i + steps2, math.cos(angle) * amplitude2 + yOffset2)
            c = (i + steps2, math.cos(angle2) * amplitude2 + yOffset2)

            if c[1] < a[1]:
                b = (i, math.cos(angle2) * amplitude2 + yOffset2)
            config.blockDraw.polygon((a, b, c, a), fill=patternOutLine, outline=None)

        config.xIncrementer += config.xSpeed
        config.yIncrementer += config.ySpeed

        if config.xIncrementer >= config.blockWidth * 1:
            config.xIncrementer = -0
        if config.yIncrementer >= config.blockHeight - 4:
            config.yIncrementer = 0

    return wrapper


@wavePatternFunction
def wavePattern(config, paletteObj):
    # return "A","B","C"
    bgFill = tuple(int(a) for a in (paletteObj.c1.currentColor))
    patternFill = tuple(int(a) for a in (paletteObj.c2.currentColor))
    patternOutLine = tuple(int(a) for a in (paletteObj.c3.currentColor))
    hilight = tuple(int(a) for a in (paletteObj.c4.currentColor))
    return config, bgFill, patternFill, patternOutLine, hilight


# @wavePatternFunction
# def wavePattern2(config, paletteObj):
#     # return "B","C","A"
#     bgFill = tuple(int(a) for a in (paletteObj.c1.currentColor))
#     patternFill = tuple(int(a) for a in (paletteObj.c4.currentColor))
#     patternOutLine = tuple(int(a) for a in (paletteObj.c3.currentColor))
#     hilight = tuple(int(a) for a in (paletteObj.c4.currentColor))
#     return config,bgFill,patternFill,patternOutLine,hilight

# --------------------------------------- #


def logcabinPatternFunction(func):
    def wrapper(*args):
        res = func(*args)
        config = res[0]
        bgFill = res[1]
        patternFill = res[2]
        patternOutLine = res[3]
        hilight = res[4]

        # clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
        # clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
        # clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
        # clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))

        config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=bgFill, outline=None)

        _blockSize = config.blockWidth - 0
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
                if random.random() < config.popRandomColorProb:
                    _clr = colorutils.getRandomColorHSV(0, 360, 0.65, 1.0, 0.5, 0.75, 0, 0, 255)
                else:
                    _clr = colorutils.getRandomColorHSV(320, 340, 0.65, 1.0, 0.5, 0.75, 0, 0, 255)

            _clrReduced = tuple(round(i * 0.85) for i in _clr) if _rowCount < numberOfBars / 2 else tuple(round(i * 1.0) for i in _clr)

            if col == 1:
                _clrReduced = (255, 0, 100, 255)
            config.blockDraw.rectangle((_x, _y, _x + _w, _y + _h), fill=_clrReduced, outline=None)

        for _rowCount, row in enumerate(_seq):
            _w = row * gridSize
            _x = round(_mid[0] - _w / 2)
            _y = round((_rowCount) * gridSize)
            _h = gridSize
            _clr = patternFill
            if _rowCount % 2 != 0:
                if random.random() < config.popRandomColorProb:
                    _clr = colorutils.getRandomColorHSV(0, 360, 0.65, 1.0, 0.5, 0.75, 0, 0, 255)
                else:
                    _clr = colorutils.getRandomColorHSV(320, 340, 0.65, 1.0, 0.5, 0.75, 0, 0, 255)
            _clrReduced = tuple(round(i * 0.65) for i in _clr) if _rowCount < numberOfBars / 2 else tuple(round(i * 1.0) for i in _clr)
            if row == 1:
                _clrReduced = (255, 0, 100, 255)
            config.blockDraw.rectangle((_x, _y, _x + _w, _y + _h), fill=_clrReduced, outline=None)

    return wrapper


@logcabinPatternFunction
def logcabin(config, paletteObj):
    bgFill = tuple(int(a) for a in (paletteObj.c1.currentColor))
    patternFill = tuple(int(a) for a in (paletteObj.c2.currentColor))
    patternOutLine = tuple(int(a) for a in (paletteObj.c3.currentColor))
    hilight = tuple(int(a) for a in (paletteObj.c4.currentColor))
    return config, bgFill, patternFill, patternOutLine, hilight


@logcabinPatternFunction
def logcabinAlt1(config, paletteObj):
    bgFill = tuple(int(a) for a in (paletteObj.c1.currentColor))
    patternFill = tuple(int(a) for a in (paletteObj.c2.currentColor))
    patternOutLine = tuple(int(a) for a in (paletteObj.c3.currentColor))
    hilight = tuple(int(a) for a in (paletteObj.c4.currentColor))
    return config, bgFill, patternFill, patternOutLine, hilight


@logcabinPatternFunction
def logcabinAlt2(config, paletteObj):
    bgFill = tuple(int(a) for a in (paletteObj.c1.currentColor))
    patternFill = tuple(int(a) for a in (paletteObj.c4.currentColor))
    patternOutLine = tuple(int(a) for a in (paletteObj.c3.currentColor))
    hilight = tuple(int(a) for a in (paletteObj.c4.currentColor))
    return config, bgFill, patternFill, patternOutLine, hilight


# --------------------------------------- #


def wavePattern2(config, paletteObj=None):
    # sourcery skip: use-itertools-product
    w = 4
    h = 4
    x = config.xIncrementer
    y = config.yIncrementer

    # clr3 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    # clr = tuple(int(a) for a in (paletteObj.c2.currentColor))
    # clr2 = tuple(int(a) for a in (paletteObj.c3.currentColor))

    clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
    clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))

    config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=clr1, outline=clr1)

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
            config.blockDraw.line((a, c), fill=clr2)
            config.blockDraw.line((a, c2), fill=clr2)

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

    config.xIncrementer += config.xSpeed
    config.yIncrementer += config.ySpeed

    if config.xIncrementer >= config.blockWidth * 1:
        config.xIncrementer = -0
    if config.yIncrementer >= config.blockHeight - 4:
        config.yIncrementer = 0


def runningSpiral(config, paletteObj=None):
    # 16px grid box spiral for now
    w = 4
    h = 4
    x = config.xIncrementer
    y = config.yIncrementer
    # clr3 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    # clr = tuple(int(a) for a in (paletteObj.c2.currentColor))
    # clr2 = tuple(int(a) for a in (paletteObj.c3.currentColor))

    clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
    clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))

    config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=clr1, outline=None)

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
        config.blockDraw.line((p1[0], p1[1], p2[0], p2[1]), fill=clr2)
        p1[0] = p2[0]
        distance += d
        p2[1] = p2[1] + distance * direction
        config.blockDraw.line((p1[0], p1[1], p2[0], p2[1]), fill=clr2)
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
        config.blockDraw.line((p1[0], p1[1], p2[0], p2[1]), fill=clr3)
        p1[0] = p2[0]
        distance += d
        p2[1] = p2[1] + distance * direction
        config.blockDraw.line((p1[0], p1[1], p2[0], p2[1]), fill=clr3)
        direction *= -1
        p1[1] = p2[1]


def chainLinks(config, paletteObj=None):
    config.circlesPackedSize = 0.1

    # clr3 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    # clr = tuple(int(a) for a in (paletteObj.c2.currentColor))
    # clr2 = tuple(int(a) for a in (paletteObj.c3.currentColor))

    clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
    clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))
    config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=clr1, outline=None)

    numRows = config.numDotRows
    steps = 3
    var = 8
    overlap = config.blockWidth / 4 - var
    dotWidth = (config.blockWidth - overlap - var) / 1
    dotWidth = config.blockWidth
    outline = clr2

    _unitLength = 1 / 16 * config.blockWidth
    _wd = 3
    for _c in range(2):
        x0 = _unitLength * 1 + _c * _unitLength * 8
        y0 = _unitLength * 2
        x1 = _unitLength * 5 + _c * _unitLength * 8
        y1 = _unitLength * 6

        config.blockDraw.arc((x0, y0, x1, y1), 0, 180, fill=outline, width = _wd)
        config.blockDraw.line((x0, y0 + 2 * _unitLength, x0, 0), fill=outline, width = _wd)
        config.blockDraw.line((x1, y0 + 2 * _unitLength, x1, 0), fill=outline, width = _wd)

        # 2nd link
        x0 = _unitLength * 3 + _c * _unitLength * 8
        y0 = _unitLength * 3
        x1 = _unitLength * 7 + _c * _unitLength * 8
        y1 = _unitLength * 7

        config.blockDraw.arc((x0, y0, x1, y1), 180, 250, fill=clr3, width = _wd)
        config.blockDraw.arc((x0, y0, x1, y1), 290, 0, fill=clr3, width = _wd)
        # config.blockDraw.arc((x0, y0, x1, y1), 180, 0, fill=clr3, width = _wd)
        # config.blockDraw.arc((x0, y0, x1, y1), 90, 0, fill=clr3, width = _wd)


        config.blockDraw.line((x0, y0 + 2 * _unitLength, x0, _unitLength * 12), fill=clr3, width = _wd)
        config.blockDraw.line((x1, y0 + 2 * _unitLength, x1, _unitLength * 12), fill=clr3, width = _wd)

        x0 = _unitLength * 3 + _c * _unitLength * 8
        y0 = _unitLength * 3 + _unitLength * 7
        x1 = _unitLength * 7 + _c * _unitLength * 8
        y1 = _unitLength * 7 + _unitLength * 7

        config.blockDraw.arc((x0, y0, x1, y1), 0, 180, fill=clr3, width = _wd)

        x0 = _unitLength * 1 + _c * _unitLength * 8
        y0 = _unitLength * 2 + _unitLength * 9
        x1 = _unitLength * 5 + _c * _unitLength * 8
        y1 = _unitLength * 6 + _unitLength * 9

        config.blockDraw.arc((x0, y0, x1, y1), 180, 0, fill=outline, width = _wd)
        config.blockDraw.line((x0, y0 + 2 * _unitLength, x0, _unitLength * 16), fill=outline, width = _wd)
        config.blockDraw.line((x1, y0 + 3 * _unitLength, x1, _unitLength * 16), fill=outline, width = _wd)



def circlesPacked(config, paletteObj=None):
    config.circlesPackedSize = 0.1

    # clr3 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    # clr = tuple(int(a) for a in (paletteObj.c2.currentColor))
    # clr2 = tuple(int(a) for a in (paletteObj.c3.currentColor))

    clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
    clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))
    config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=clr1, outline=None)

    numRows = config.numDotRows
    steps = 3
    var = 8
    overlap = config.blockWidth / 4 - var
    dotWidth = (config.blockWidth - overlap - var) / 1
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

            config.blockDraw.ellipse((x0, y0, x1, y1), outline=(outline), fill=None)
            config.blockDraw.ellipse((x0 + 4, y0 + 4, x1 - 4, y1 - 4), outline=(outline), fill=None)

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

    #         config.blockDraw.ellipse((x0,y0,x1,y1), outline=(outline), fill=clr1)


def shingles(config, paletteObj=None):
    w = 4
    h = 4
    x = config.xIncrementer
    y = config.yIncrementer

    # clr = tuple(int(a) for a in (paletteObj.c1.currentColor))
    # clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    # clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))

    clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
    clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))

    config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=clr2, outline=None)

    numRows = config.numShingleRows
    boxWidth = config.blockWidth / numRows
    shingleWidth = config.blockWidth / numRows - config.shingleVariationAmount

    for r in range(numRows, -1, -1):
        yPos = -1 + r * boxWidth

        for i in range(3):
            config.blockDraw.rectangle((i * boxWidth - boxWidth / 2, yPos, i * boxWidth + shingleWidth - boxWidth / 2, yPos + boxWidth - 1), outline=(clr1), fill=clr2)
        for i in range(2):
            config.blockDraw.rectangle((i * boxWidth, yPos - boxWidth / 2, i * boxWidth + shingleWidth, yPos + boxWidth / 2 - 1), outline=(clr1), fill=clr2)


def shellScales(config, paletteObj=None):
    # clr, clr2, clr3 = _get_colors(config, paletteObj)

    clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
    clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))

    config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=clr3, outline=None)

    numRows = config.numShingleRows
    boxWidth = config.blockWidth / numRows
    numLines = round(config.waveScaleRings * 1.0)
    numLinesHalf = round(numLines / 2)
    rads = math.pi * 2 / numLines
    radius = boxWidth / 2

    for r in range(numRows, -1, -1):
        yPos = -2 + r * boxWidth
        _draw_row_of_ellipses(config, yPos, boxWidth, clr2, clr1, numLinesHalf, rads, radius, clr3)
        _draw_offset_row_of_ellipses(config, yPos, boxWidth, clr2, clr1, numLinesHalf, rads, radius, clr3)


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
    # clr, clr2, clr3 = _get_colors(config, paletteObj)

    clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
    clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))

    config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=clr1, outline=None)

    numRows = 2
    boxWidth = 2 * config.blockWidth / numRows
    rings = config.waveScaleRings
    step = config.waveScaleSteps
    patternRows = numRows + 1

    if config.linesOnly:
        config.altLineColoring = False

    startFirstSet = 1 if config.altLineColoring and step != 2 else 0
    lineToUse = clr2

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


def waveScales(config, paletteObj=None):
    # clr, clr2, clr3 = _get_colors(config, paletteObj)

    clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
    clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))

    config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=clr3, outline=None)

    numRows = 2
    boxWidth = 2 * config.blockWidth / numRows
    rings = config.waveScaleRings
    step = config.waveScaleSteps
    patternRows = numRows + 1

    if config.linesOnly:
        config.altLineColoring = False

    lineToUse = clr2

    for r in range(patternRows, -patternRows, -1):
        yPos = -2 + r * boxWidth
        _draw_wave_scale_set(config, yPos, boxWidth, rings, step, clr3, clr2, clr4, lineToUse)


def _draw_wave_scale_set(config, yPos, boxWidth, rings, step, clr3, clr2, clr4, lineToUse):
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


def circles(config, paletteObj=None):
    # clr, clr2, clr3 = _get_colors(config, paletteObj)
    clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
    clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))

    config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=clr1, outline=None)

    numLines = config.blockWidth - 1
    steps = 3

    _draw_circles(config, 0, 0, numLines, steps, clr2, clr3, clr1, config.blockWidth, config.blockHeight)

    for c in range(2):
        xOff = c * config.blockWidth - config.blockWidth / 2
        for r in range(2):
            yOff = r * config.blockHeight - config.blockHeight / 2
            _draw_circles(config, xOff, yOff, numLines, steps, clr2, clr1, clr3, config.blockWidth, config.blockHeight)  # Swapped clr2 and clr3 for outline


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


def tripart(config, paletteObj=None):

    clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
    clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))

    if random.random() < config.popRandomColorProb:
        # hideos override until I can pair palettes and patterns in a
        # more flexible way
        if paletteObj.paletteName == "galah":
            clr4 = colorutils.getRandomColorHSV(0, 360, 0.65, 1.0, 0.5, 0.75, 60, 170, 255)
        else:
            clr4 = colorutils.getRandomColorHSV(0, 360, 0.65, 1.0, 0.5, 0.75, 0, 0, 255)

    config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=clr1, outline=None)

    midPt = (config.blockWidth / 2, config.blockWidth / 2)

    poly1 = ((0, 0), (midPt[0], midPt[1]), (0, config.blockHeight), (0, 0))
    config.blockDraw.polygon(poly1, fill=clr2)

    poly2 = ((config.blockWidth, 0), (midPt[0], midPt[1]), (config.blockWidth, config.blockHeight), (config.blockWidth, 0))
    config.blockDraw.polygon(poly2, fill=clr3)

    poly3 = ((config.blockWidth, 0), (midPt[0], midPt[1]), (0, 0), (config.blockWidth, 0))
    config.blockDraw.polygon(poly3, fill=clr4)


def bars(config, paletteObj=None):
    # clr3 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    # clr = tuple(int(a) for a in (paletteObj.c2.currentColor))
    # clr2 = tuple(int(a) for a in (paletteObj.c3.currentColor))

    clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
    clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))

    config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=clr1, outline=None)

    barWidth = 4
    for count, i in enumerate(range(0, config.numConcentricBoxes, 2)):
        outClr = clr2
        if count % 2 == 0 and config.altLineColoring == True:
            outClr = clr2
        config.blockDraw.rectangle((0, i * barWidth, config.blockWidth - 1, i * barWidth), outline=(outClr), fill=None)


def peaceCross(config, paletteObj=None):

    clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
    clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))

    # hideos override until I can pair palettes and patterns in a
    # more flexible way
    # if paletteObj.paletteName == "galah" :
    #     clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))

    config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=clr2, outline=None)

    _blockSize = config.blockWidth
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

        if random.random() < config.popRandomColorProb / 14:
            _clr = colorutils.getRandomColorHSV(0, 360, 0.2, 0.40, 0.5, 0.5, 70, 190, 255)

        # 4 squares around cross
        if _rowCount in [5, 7, 15, 13]:
            if random.random() > config.popRandomColorProb / 14:
                _clr = colorutils.getRandomColorHSV(0, 360, 0.05, 0.10, 0.75, 0.95, 70, 190, 255)
            else:
                _clr = tuple(round(i * 0.75) for i in clr4)

        # cross shape
        if _rowCount in [6, 9, 10, 11, 14]:
            _clr = tuple(round(i * 0.5) for i in clr1)
            if random.random() < config.popRandomColorProb / 18:
                _clr = colorutils.getRandomColorHSV(0, 360, 0.2, 0.40, 0.1, 0.3, 70, 190, 255)

        _y = _xOffset
        _x = _yOffset

        # if _rowCount %2 != 0 :
        #     if random.random() < config.popRandomColorProb :
        #         _clr = colorutils.getRandomColorHSV(0, 360, 0.65, 1.0, 0.5, 0.75, 0, 0, 255)
        #     else:
        #         _clr = colorutils.getRandomColorHSV(320, 340, 0.65, 1.0, 0.5, 0.75, 0, 0, 255)

        config.blockDraw.rectangle((_x, _y, _x + _w, _y + _h), fill=_clr, outline=None)


def fiboSeq(n):
    _seq = []
    _seq.extend(2 * i - 1 for i in range(n, 1, -1))
    _seq.extend(2 * i - 1 for i in range(1, n + 1))
    return _seq


def logcabin(config, paletteObj=None):

    clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
    clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))

    # hideos override until I can pair palettes and patterns in a
    # more flexible way
    if paletteObj.paletteName == "galah":
        clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))

    config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=clr3, outline=None)

    _blockSize = config.blockWidth - 0
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
            if random.random() < config.popRandomColorProb:
                _clr = colorutils.getRandomColorHSV(0, 360, 0.65, 1.0, 0.5, 0.75, 0, 0, 255)
            else:
                _clr = colorutils.getRandomColorHSV(320, 340, 0.65, 1.0, 0.5, 0.75, 0, 0, 255)

        _clrReduced = tuple(round(i * 0.85) for i in _clr) if _rowCount < numberOfBars / 2 else tuple(round(i * 1.0) for i in _clr)

        if col == 1:
            _clrReduced = (255, 0, 100, 255)
        config.blockDraw.rectangle((_x, _y, _x + _w, _y + _h), fill=_clrReduced, outline=None)

    for _rowCount, row in enumerate(_seq):
        _w = row * gridSize
        _x = round(_mid[0] - _w / 2)
        _y = round((_rowCount) * gridSize)
        _h = gridSize
        _clr = clr1
        if _rowCount % 2 != 0:
            if random.random() < config.popRandomColorProb:
                _clr = colorutils.getRandomColorHSV(0, 360, 0.65, 1.0, 0.5, 0.75, 0, 0, 255)
            else:
                _clr = colorutils.getRandomColorHSV(320, 340, 0.65, 1.0, 0.5, 0.75, 0, 0, 255)
        _clrReduced = tuple(round(i * 0.65) for i in _clr) if _rowCount < numberOfBars / 2 else tuple(round(i * 1.0) for i in _clr)
        if row == 1:
            _clrReduced = (255, 0, 100, 255)
        config.blockDraw.rectangle((_x, _y, _x + _w, _y + _h), fill=_clrReduced, outline=None)


def littleCones(config, paletteObj=None):
    clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
    clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))

    config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=clr1, outline=None)
    _mid = [config.blockWidth / 2, config.blockHeight / 2]
    fibo = 5
    numberOfBars = fibo + fibo - 1
    gridSize = math.ceil(config.blockWidth / numberOfBars / 1)

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
        config.blockDraw.rectangle((_x, _y, _x + _w, _y + gridSize), fill=_clr, outline=None)


def coloredBlocks(config, paletteObj=None):

    clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
    clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))

    config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=clr2, outline=None)
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
    # clr3 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    # clr = tuple(int(a) for a in (paletteObj.c2.currentColor))
    # clr2 = tuple(int(a) for a in (paletteObj.c3.currentColor))

    clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
    clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))

    config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=clr1, outline=None)

    count = 0

    for i in range(0, config.numConcentricBoxes, 2):

        if config.altLineColoring == True:
            outClr = clr3
            if count % 2 == 0:
                outClr = clr2
        else:
            outClr = clr2

        try:
            config.blockDraw.rectangle((i - 1, i - 1, config.blockWidth - 1 * i, config.blockHeight - 1 * i), outline=(outClr), fill=None)
            count += 1
        except Exception as e:
            print(f"Concentric boxes error prob too many {e}")


def decoBoxes(config, paletteObj=None):

    # clr3 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    # clr = tuple(int(a) for a in (paletteObj.c2.currentColor))
    # clr2 = tuple(int(a) for a in (paletteObj.c3.currentColor))

    clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
    clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))

    config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=clr1, outline=None)

    clr = clr1
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

    config.blockImage.paste(temp, (xOff, yOff), temp)


def diamond(config, paletteObj=None):  # sourcery skip: low-code-quality, use-itertools-product
    # clr = tuple(int(a) for a in paletteObj.c2.currentColor)
    # clr2 = tuple(int(a) for a in paletteObj.c1.currentColor)

    clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
    clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))

    x = config.xIncrementer
    y = config.yIncrementer

    # needs to be in odd grid
    config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=clr1, outline=None)

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
                for r in range(row):
                    x = r + mid - row / 2 + c * blockHeight
                    y = i + config.yIncrementer + rw * blockHeight

                    if y >= blockHeight * rows:
                        y -= blockHeight * rows

                    if (r % 2) != 1:
                        config.blockDraw.rectangle((x, y, w + x, h + y), fill=(clr2), outline=None)
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
    # clr3 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    # clr = tuple(int(a) for a in (paletteObj.c2.currentColor))
    # clr2 = tuple(int(a) for a in (paletteObj.c3.currentColor))

    clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
    clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))

    w = 4
    h = 4
    x = config.xIncrementer
    y = config.yIncrementer

    config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=clr1, outline=None)
    config.blockDraw.rectangle((x, y, w + x, h + y), fill=(clr2), outline=None)
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

    # bgColor = (clr1[0], clr1[1], clr1[3], 255)

    # clr3 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    # clr = tuple(int(a) for a in (paletteObj.c2.currentColor))
    # clr2 = tuple(int(a) for a in (paletteObj.c3.currentColor))

    clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
    clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))

    config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=clr1, outline=None)

    lineMult = config.lineDiff * 2
    numLines = round(config.blockWidth / config.lineDiff * 2)

    y1 = 0
    for i in range(numLines):

        x1 = -2 * config.blockWidth + config.xIncrementer + i * lineMult
        x2 = -2 * config.blockWidth + config.blockWidth + config.xIncrementer + i * lineMult
        y2 = config.blockHeight

        config.blockDraw.line((x1, y1, x2, y2), fill=(clr2))
        if config.useDoubleLine == True:
            config.blockDraw.line(
                (
                    -2 * config.blockWidth + config.xIncrementer + i * lineMult + 1,
                    0,
                    -2 * config.blockWidth + config.blockWidth + config.xIncrementer + i * lineMult + 1,
                    config.blockHeight,
                ),
                fill=(clr3),
            )

    config.xIncrementer += config.xSpeed
    config.yIncrementer += 0

    """
    """
    if config.xIncrementer > (config.blockWidth + 0):
        config.xIncrementer = -config.xSpeed
    if config.yIncrementer >= config.blockHeight - 4:
        config.yIncrementer = 0


def grainLines(config, paletteObj=None):

    # print(f"grainLines running {grainLines}")
    bgFill = tuple(int(a) for a in (paletteObj.c1.currentColor))
    patternFill = tuple(int(a) for a in (paletteObj.c4.currentColor))
    patternOutLine = tuple(int(a) for a in (paletteObj.c3.currentColor))
    hilight = tuple(int(a) for a in (paletteObj.c4.currentColor))

    if random.random() < config.popRandomColorProb:
        # hideos override until I can pair palettes and patterns in a
        # more flexible way
        if paletteObj.paletteName == "galah":
            hilight = colorutils.getRandomColorHSV(0, 360, 0.65, 1.0, 0.5, 0.75, 60, 170, 255)
        else:
            hilight = colorutils.getRandomColorHSV(0, 360, 0.65, 1.0, 0.5, 0.75, 0, 0, 255)

    config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=bgFill, outline=None)

    midPt = (config.blockWidth / 2, config.blockWidth / 2)
    rndFactor = 0.01
    rnd = random.random() + rndFactor
    rnd2 = random.random() + rndFactor

    _w = round(random.uniform(1, 3))
    _gradientCount = 0
    _gradientPeriod = round(random.uniform(3, 8))
    _lineGap = int(random.uniform(1, 2))
    for yPt in range(-config.blockHeight, 2 * config.blockHeight, _lineGap):
        _lastX = 0
        _lastY = 0
        for xPt in range(-32, config.blockWidth, _w):
            _x1 = _lastX
            _x2 = xPt * _w
            _y1 = _lastY
            _y2 = noise.pnoise2(rnd * _x2 / 120 + 0.2, rnd2 * yPt / 120) * 100
            config.blockDraw.line((_x1, _y1 + yPt, _x2, _y2 + yPt), fill=(patternFill[0], patternFill[1], patternFill[2], round(255 * (_gradientCount / _gradientPeriod + 0.45))))
            _lastX = _x2
            _lastY = _y2
        _gradientCount += 1
        if _gradientCount > _gradientPeriod:
            _gradientCount = 0
            _gradientPeriod = round(random.uniform(3, 8))
            rnd2 = random.random() + rndFactor
    # poly1 = ((0, 0), (midPt[0], midPt[1]), (0, config.blockHeight), (0, 0))
    # config.blockDraw.polygon(poly1, fill=clr2)

    # poly2 = ((config.blockWidth, 0), (midPt[0], midPt[1]), (config.blockWidth, config.blockHeight), (config.blockWidth, 0))
    # config.blockDraw.polygon(poly2, fill=clr3)

    # poly3 = ((config.blockWidth, 0), (midPt[0], midPt[1]), (0, 0), (config.blockWidth, 0))
    # config.blockDraw.polygon(poly3, fill=clr4)


def colorGrid(config, paletteObj=None):
    # clr3 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    # clr = tuple(int(a) for a in (paletteObj.c2.currentColor))
    # clr2 = tuple(int(a) for a in (paletteObj.c3.currentColor))

    clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
    clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))

    bgFill = tuple(int(a) for a in (paletteObj.c1.currentColor))

    config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=clr1, outline=None)

    _divs = round(random.uniform(1, 4))
    _w = round(config.blockWidth / _divs)
    _h = round(config.blockHeight / _divs)

    for _r in range(_divs):
        for _c in range(_divs):
            clr = colorutils.getRandomColorHSV(0, 360, 0.3, 1.0, 0.3, 0.90, 100, 170, 255, config.brightness)
            if (_c % 2 == 0 or _r % 2 == 0) and random.random() < 0.5:
                # rosetone ;)
                clr = colorutils.getRandomColorHSV(320, 355, 0.3, 1.0, 0.3, 0.90, 100, 170, 255, config.brightness)
            config.blockDraw.rectangle((_c * _w, _r * _h, _c * _w + _w, _r * _h + _h), outline=None, fill=clr)


def colorGridTriangles(config, paletteObj=None):
    # clr3 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    # clr = tuple(int(a) for a in (paletteObj.c2.currentColor))
    # clr2 = tuple(int(a) for a in (paletteObj.c3.currentColor))

    clr1 = tuple(int(a) for a in (paletteObj.c1.currentColor))
    clr2 = tuple(int(a) for a in (paletteObj.c2.currentColor))
    clr3 = tuple(int(a) for a in (paletteObj.c3.currentColor))
    clr4 = tuple(int(a) for a in (paletteObj.c4.currentColor))

    bgFill = tuple(int(a) for a in (paletteObj.c1.currentColor))

    config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=clr1, outline=None)

    _divs = round(random.uniform(1, 4))
    _w = round(config.blockWidth / _divs)
    _h = round(config.blockHeight / _divs)

    for _r in range(_divs):
        for _c in range(_divs):
            clr1 = colorutils.getRandomColorHSV(0, 360, 0.3, 1.0, 0.3, 0.90, 100, 170, 255, config.brightness)
            clr2 = colorutils.getRandomColorHSV(0, 360, 0.3, 1.0, 0.3, 0.90, 100, 170, 255, config.brightness)
            if (_c % 2 == 0 or _r % 2 == 0) and random.random() < 0.5:
                # rosetone ;)
                clr1 = colorutils.getRandomColorHSV(320, 355, 0.3, 1.0, 0.3, 0.90, 100, 170, 255, config.brightness)
                clr2 = colorutils.getRandomColorHSV(320, 355, 0.3, 1.0, 0.3, 0.90, 100, 170, 255, config.brightness)
            # config.blockDraw.rectangle(( _c * _w, _r * _h, _c * _w + _w, _r * _h + _h), outline=(0,0,0,125), fill=clr)
            config.blockDraw.polygon(((_c * _w, _r * _h), (_c * _w + _w, _r * _h + _h), (_c * _w, _r * _h + _h), (_c * _w, _r * _h)), outline=None, fill=clr1)
            config.blockDraw.polygon(((_c * _w, _r * _h), (_c * _w + _w, _r * _h), (_c * _w + _w, _r * _h + _h), (_c * _w, _r * _h)), outline=None, fill=clr2)


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


def floralConfig(config):
    config.floral = ArtWorkConfig("Florals", True)

    _choice = random.randint(0, 7)

    match _choice:

        case 0:
            config.floral._petals = 9
            config.floral._w = config.blockWidth * 0.51
            config.floral._lobe = config.floral._w * 0.8
            config.floral._h = config.blockWidth / 8

        case 1:
            config.floral._petals = 7
            config.floral._w = config.blockWidth * 0.51
            config.floral._lobe = config.floral._w * 0.8
            config.floral._h = config.blockWidth / 8

        case 2:
            config.floral._petals = 4
            config.floral._w = config.blockWidth * 0.51
            config.floral._lobe = config.floral._w * 0.7
            config.floral._h = config.blockWidth / 4

        case 3:
            config.floral._petals = 5
            config.floral._w = config.blockWidth * 0.51
            config.floral._lobe = config.floral._w * 0.7
            config.floral._h = config.blockWidth / 4

        case 4:
            config.floral._petals = 3
            config.floral._w = config.blockWidth * 0.51
            config.floral._lobe = config.floral._w * 0.4
            config.floral._h = config.blockWidth / 4

        case 5:
            config.floral._petals = 4
            config.floral._w = config.blockWidth * 0.6
            config.floral._lobe = config.floral._w * 0.2
            config.floral._h = config.blockWidth / 4

        case 6:
            config.floral._petals = 5
            config.floral._w = config.blockWidth * 0.6
            config.floral._lobe = config.floral._w * 0.2
            config.floral._h = config.blockWidth / 4

        case 7:
            config.floral._lobe = round(random.uniform(4, config.blockWidth * 0.7))
            config.floral._w = round(random.uniform(config.floral._lobe, config.blockWidth * 0.8))
            config.floral._h = round(random.uniform(4, config.blockHeight / 8))
            # config.floral._extension = config.blockWidth / 2
            config.floral._petals = round(random.uniform(4, 7))
    # config.floral.debugSelf()


def petals(config, paletteObj=None):

    # print(f"grainLines running {grainLines}")
    # print(paletteObj.c1.currentColor)
    bgFill = tuple(int(a) for a in (paletteObj.c1.currentColor))
    patternFill = tuple(int(a) for a in (paletteObj.c4.currentColor))
    patternOutLine = tuple(int(a) for a in (paletteObj.c3.currentColor))
    hilight = tuple(int(a) for a in (paletteObj.c4.currentColor))

    if random.random() < config.popRandomColorProb:
        # hideos override until I can pair palettes and patterns in a
        # more flexible way
        if paletteObj.paletteName == "galah":
            hilight = colorutils.getRandomColorHSV(0, 360, 0.65, 1.0, 0.5, 0.75, 60, 170, 255)
        else:
            hilight = colorutils.getRandomColorHSV(0, 360, 0.65, 1.0, 0.5, 0.75, 0, 0, 255)

    config.blockDraw.rectangle((0, 0, config.blockWidth, config.blockHeight), fill=bgFill, outline=None)

    midPt = (round(config.blockWidth / 2), round(config.blockWidth / 2))
    rndFactor = 0.01
    rnd = random.random() + rndFactor
    rnd2 = random.random() + rndFactor

    points = [
        midPt,
        (midPt[0] + config.floral._lobe, midPt[1] - config.floral._h),
        (midPt[0] + config.floral._w, midPt[1]),
        (midPt[0] + config.floral._lobe, midPt[1] + config.floral._h),
        midPt,
    ]
    res = chaikins_corner_cutting(points, 6).tolist()

    _pts = tuple(tuple(_e) for _e in res)

    _petalImg = Image.new("RGBA", (config.blockWidth, config.blockHeight))
    _floralImg = Image.new("RGBA", (config.blockWidth, config.blockHeight))
    _petalDraw = ImageDraw.Draw(_petalImg)
    _petalDraw.polygon(_pts, fill=patternFill)
    _petalDraw.line((midPt[0], midPt[1], midPt[0] + config.floral._w / 2, midPt[1] + 3), fill=bgFill, width=1)
    _petalDraw.line((midPt[0], midPt[1], midPt[0] + config.floral._w / 2, midPt[1] - 3), fill=bgFill, width=1)

    _angle = 360 / config.floral._petals

    for _p in range(config.floral._petals):
        _floralImg.paste(_petalImg.rotate(_angle * _p), (0, 0), _petalImg.rotate(_angle * _p))

    _sizeChange = random.uniform(0.25, 0.85)
    _newSize = (round(config.blockWidth * _sizeChange), round(config.blockWidth * _sizeChange))
    _floralTemp = _floralImg.resize((_newSize[0], _newSize[1]), 1)
    config.blockImage.paste(_floralTemp, (midPt[0], 0), _floralTemp)
    config.blockImage.paste(_floralTemp, (-midPt[0], 0), _floralTemp)
    config.blockImage.paste(_floralTemp, (0, midPt[1]), _floralTemp)
    config.blockImage.paste(_floralTemp, (0, -midPt[1]), _floralTemp)

    # config.blockDraw.rectangle((0,0,10,10), fill=(random.randint(0,255),random.randint(0,255),random.randint(0,255),255))

    if random.random() < 0.01:
        floralConfig(config)
