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
from modules.movieClip import movieClip
from PIL import (
    Image,
    ImageChops,
    ImageFont,
    ImageDraw,
    ImageEnhance,
    ImageFilter,
    ImageMath,
    ImagePalette,
)
import numpy as np

xPos = 320
yPos = 0

bads = badpixels


class Director:
    """docstring for Director"""

    slotRate = 0.5

    def __init__(self, config):
        super(Director, self).__init__()
        self.config = config
        self.tT = time.time()

    def checkTime(self):
        if (time.time() - self.tT) >= self.slotRate:
            self.tT = time.time()
            self.advance = True
        else:
            self.advance = False

    def next(self):

        self.checkTime()


def main(run=True):
    global config, workConfig, blocks, simulBlocks, bads
    # Generate image holders
    config.workImage = Image.new(
        "RGBA", (config.canvasWidth, config.canvasHeight))
    config.workImageDraw = ImageDraw.Draw(config.workImage)

    config.canvasImage = Image.new(
        "RGBA", (config.canvasWidth * 10, config.canvasHeight))
    config.canvasImageDraw = ImageDraw.Draw(config.canvasImage)

    config.imageLayer = Image.new(
        "RGBA", (config.canvasWidth * 10, config.canvasHeight))
    config.imageLayerDraw = ImageDraw.Draw(config.canvasImage)

    # Sets the image size  -- should probably be set to canvasHeight
    config.channelHeight = config.canvasHeight
    
    # managing speed of animation and framerate
    config.directorController = Director(config)

    try:
        config.delay = float(workConfig.get("imageSequence", "delay"))
    except Exception as e:
        print(str(e))
        config.delay = 0.02
    try:
        config.directorController.slotRate = float(
            workConfig.get("imageSequence", "slotRate"))
    except Exception as e:
        print(str(e))
        print("SHOULD ADJUST TO USE slotRate AS FRAMERATE ")
        config.directorController.slotRate = 0.0

    config.clipMain = movieClip(config)
    config.clipMain.canvasSize = (320,240)
    config.clipMain.setUp(workConfig)

    if run:
        runWork()


def runWork():
    print(bcolors.OKGREEN + "** " + bcolors.BOLD)
    print("Running image.py")
    print(bcolors.ENDC)
    # gc.enable()

    while config.isRunning == True:
        config.directorController.checkTime()
        if config.directorController.advance == True:
            iterate()
            time.sleep(config.delay)
        if config.standAlone == False:
            config.callBack()


def iterate(n=0):
    global config, blocks
    global xPos, yPos

    config.clipMain.loadFrame()
    temp = config.clipMain.canvasImage.rotate(90,0,True)
    temp = temp.resize((120,160))
    config.canvasImage.paste(temp, (0, 0), temp)

    # config.canvasImage.paste(config.clipMain.canvasImage, (0, 0), config.clipMain.canvasImage)
    config.render(config.canvasImage, 0, 0)


def redrawBackGround():
    config.imageLayerDraw.rectangle(
        (0, 0, config.screenWidth, config.screenHeight), fill=(100, 0, 0)
    )
    config.canvasImageDraw.rectangle(
        (0, 0, config.screenWidth, config.screenHeight), fill=(100, 0, 0)
    )
    # if(random.random() > .99) : gc.collect()
    # if(random.random() > .97) : config.renderImageFull = Image.new("RGBA", (config.screenWidth, config.screenHeight))
    return True


def callBack():
    global config
    print("CALLBACL")
    return True


#####################
