#!/usr/bin/python
# import modules
import datetime
import gc
import getopt
import importlib
import io
import math
import os
import random
import sys
import textwrap
import time
from random import shuffle
from subprocess import call
from modules.configuration import bcolors
from modules.faderclass import FaderObj
from modules import badpixels, colorutils, configuration, panelDrawing
from modules.imagesprite import ImageSprite
from PIL import (
    Image,
    ImageChops,
    ImageFont,
    ImageDraw,
    ImageEnhance,
    ImageFilter,
    ImageMath,
    ImagePalette,
    ImageOps
)
import numpy as np
import noise
from noise import *


## -------------------------------------------------##

def loadImage(arg):
        image = Image.open(arg, "r")
        image.load()
        imgHeight = image.getbbox()[3]
        return image

## -------------------------------------------------##

def runWork():
    print(bcolors.OKGREEN + "** " + bcolors.BOLD)
    print("Running image.py")
    print(bcolors.ENDC)
    # gc.enable()

    while config.isRunning == True:
        iterate()
        time.sleep(config.playSpeed)
        if config.standAlone == False:
            config.callBack()

## -------------------------------------------------##

def callBack():
    global config
    print("CALLBACL")
    return True

## -------------------------------------------------##

class WaveDeformer:

    def transform(self, x, y):
        y = y + 20*math.sin((x + config.xPos)/20) 
        return x, y

    def transform_rectangle(self, x0, y0, x1, y1):
        return (*self.transform(x0, y0),
                *self.transform(x0, y1),
                *self.transform(x1, y1),
                *self.transform(x1, y0),
                )

    def getmesh(self, img):
        self.w, self.h = img.size
        gridspace = 20

        target_grid = []
        for x in range(0, self.w, gridspace):
            for y in range(0, self.h, gridspace):
                target_grid.append((x, y, x + gridspace, y + gridspace))

        source_grid = [self.transform_rectangle(*rect) for rect in target_grid]

        return [t for t in zip(target_grid, source_grid)]


class SingleDeformer:

    def getmesh(self, img):
        #Map a target rectangle onto a source quad
        return [(
                # target rectangle
                (0, 0, 400, 224),
                # corresponding source quadrilateral
                (0, 0, 0, config.xPos, 100, 200, config.xPos, 0)
                )]


def alterImage() :
    im = np.array(config.img)
    imTemp = np.array(config.img)

    rows, cols = im.shape[0], im.shape[1]

    w = im.shape[1]
    h = im.shape[0]


    # im.shape[0]
    # im.shape[1]
    yRange = config.canvasWidth


    config.workImage = ImageOps.deform(config.img, WaveDeformer())

    '''
    for y in range(config.canvasHeight):
        for x in range(config.canvasWidth):
            xPos = x + config.xPos
            if xPos >= w :
                xPos -= w
            yDisplace = math.floor(y + config.amplitude * math.sin(xPos * config.rads) * (noise.pnoise2(xPos/config.xNoiseFactor,y/config.yNoiseFactor)))
            xDisplace = math.floor(x + config.amplitude * math.sin(y * config.rads) * (noise.pnoise2(y/config.xNoiseFactor,x/config.yNoiseFactor)))
            if yDisplace >= h :
                yDisplace -= h
            if yDisplace < 0 :
                yDisplace += h
            imTemp[y,x] = im[yDisplace,  xDisplace]

    '''

    #config.workImage = Image.fromarray(imTemp.astype(np.uint8))
    config.xPos += config.scrollSpeed

    if config.xPos >= w :
        config.xPos = 0



## -------------------------------------------------##

def iterate(n=0):
    alterImage()
    config.render(config.workImage, 0, 0)

## -------------------------------------------------##

def main(run=True) :
    config.workImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.workImageDraw = ImageDraw.Draw(config.workImage)
    config.playSpeed = .02


    #config.img = loadImage('./assets/imgs/miscl/lena.jpg')
    config.img = loadImage('./assets/imgs/bgs/water2.jpg')
    config.xPos = 0
    config.yPos = 0
    config.scrollSpeed = 1
    config.xNoiseFactor = 10
    config.yNoiseFactor = 100

    config.period = 20.0
    config.rads = math.pi / config.canvasWidth * config.period
    config.amplitude = 20.0


