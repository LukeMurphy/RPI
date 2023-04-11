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
from modules import colorutils
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
)
import numpy as np


class movieClip:

    frameCount = 0
    currentFrame = 0
    imageDirectory = "./"
    paused = False
    canvasSize = (320, 240)
    clipWidth = 320
    clipHeight = 240
    clipRotate = 0

    def __init__(self, config):
        print("Initializing clip player")
        self.config = config

    def loadImage(self, arg, callback):

        image = Image.open(arg, "r")
        image.load()
        image = image.convert("RGBA")
        self.imageLayer.paste(image, (0, 0), image)

    def loadFrame(self):
        
        if random.random() < self.randomPauseProb :
            self.paused = True

    
        if self.paused == False:
            self.loadImage(self.imageDirectory +
                           str(self.currentFrame) + ".jpg", None)
            self.currentFrame += 1

            if self.currentFrame >= self.frameCount:
                self.currentFrame = 0

        if random.random() < self.overlayChangeProb:
            self.colorOverlay = colorutils.getRandomColorHSV(
                0, 360, .65, 1.0, .5, .5, 0, 0, self.colorOverlayAlpha)

        if random.random() < self.overlayChangeSizeProb:
            self.clrBlkWidth = round(
                random.uniform(5, self.clrBlkWidthSet * 1.25))
            self.clrBlkHeight = round(
                random.uniform(5, self.clrBlkHeightSet * 1.25))

        if random.random() < self.overlayChangePosProb:
            self.overlayxPos = round(
                random.uniform(0, 2 * self.canvasSize[0] / 3))
            self.overlayyPos = round(
                random.uniform(0, 2 * self.canvasSize[1] / 3))

        if random.random() < self.overlayChangePosProb / 2.0:
            self.overlayxPos = self.overlayxPosOrig
            self.overlayyPos = self.overlayyPosOrig

        self.colorize(self.colorOverlay)

        for i in range(0, 10):
            xC1 = round(random.uniform(0, 200))
            yC1 = round(random.uniform(0, 200))
            xC2 = 200 + xC1
            yC2 = 200 + yC1

            temp = self.imageLayer.crop((xC1, yC1, xC2, yC2))
            self.canvasImage.paste(temp, (xC1, yC1), temp)
        
        if self.paused == True :
            if random.random() < 2 * self.randomUnPauseProb :
                self.paused = False

    def setUp(self, workConfig):

        print("Image Sequence Player Piece Loaded")
        config = self.config
        
        self.videoWidth = int(
            workConfig.get("imageSequencePlayer", "videoWidth"))
        self.videoHeight = int(
            workConfig.get("imageSequencePlayer", "videoHeight"))
        self.clipWidth = int(
            workConfig.get("imageSequencePlayer", "clipWidth"))
        self.clipHeight = int(
            workConfig.get("imageSequencePlayer", "clipHeight"))
        
        self.canvasSize = (self.videoWidth,self.videoHeight)

        # Generate image holders
        self.workImage = Image.new(
            "RGBA", (self.canvasSize[0], self.canvasSize[1]))
        self.workImageDraw = ImageDraw.Draw(self.workImage)

        self.canvasImage = Image.new(
            "RGBA", (self.canvasSize[0] * 1, self.canvasSize[1]))
        self.canvasImageDraw = ImageDraw.Draw(self.canvasImage)

        self.imageLayer = Image.new(
            "RGBA", (self.canvasSize[0] * 1, self.canvasSize[1]))
        self.imageLayerDraw = ImageDraw.Draw(self.canvasImage)

        # Sets the image size  -- should probably be set to canvasHeight
        self.channelHeight = self.canvasSize[1]

        self.imageDirectory = workConfig.get(
            "imageSequencePlayer", "imageDirectory")
        self.frameCount = int(
            workConfig.get("imageSequencePlayer", "frameCount"))
        self.currentFrame = 0
        self.imageDirectory = self.imageDirectory
        self.imageLayer = self.imageLayer

        self.clrBlkWidth = int(workConfig.get(
            "imageSequencePlayer", "clrBlkWidth"))
        self.clrBlkHeight = int(workConfig.get(
            "imageSequencePlayer", "clrBlkHeight"))
        self.clrBlkWidthSet = int(
            workConfig.get("imageSequencePlayer", "clrBlkWidth"))
        self.clrBlkHeightSet = int(
            workConfig.get("imageSequencePlayer", "clrBlkHeight"))


        self.overlayxPosOrig = int(
            workConfig.get("imageSequencePlayer", "overlayxPos"))
        self.overlayyPosOrig = int(
            workConfig.get("imageSequencePlayer", "overlayyPos"))
        self.overlayxPos = int(workConfig.get(
            "imageSequencePlayer", "overlayxPos"))
        self.overlayyPos = int(workConfig.get(
            "imageSequencePlayer", "overlayyPos"))
        self.overlayChangeProb = float(
            workConfig.get("imageSequencePlayer", "overlayChangeProb"))
        self.overlayChangePosProb = float(
            workConfig.get("imageSequencePlayer", "overlayChangePosProb"))
        self.overlayChangeSizeProb = float(
            workConfig.get("imageSequencePlayer", "overlayChangeSizeProb"))
        self.randomPauseProb = float(
            workConfig.get("imageSequencePlayer", "randomPauseProb"))
        self.randomUnPauseProb = float(
            workConfig.get("imageSequencePlayer", "randomUnPauseProb"))

        overlayColor = workConfig.get(
            "imageSequencePlayer", "overlayColor").split(',')

        self.overlayColor = tuple(map(lambda x: int(x), overlayColor))
        self.colorOverlay = self.overlayColor

        self.colorOverlayAlpha = int(
            workConfig.get("imageSequencePlayer", "colorOverlayAlpha"))
        
        
        self.maskBoxWidth = int(workConfig.get("imageSequencePlayer", "maskBoxWidth"))
        self.maskBoxHeight = int(workConfig.get("imageSequencePlayer", "maskBoxHeight"))
        self.maskBoxX = int(workConfig.get("imageSequencePlayer", "maskBoxX"))
        self.maskBoxY = int(workConfig.get("imageSequencePlayer", "maskBoxY"))

        self.overLayMode = 0
        print(bcolors.OKBLUE + "** " + bcolors.BOLD)
        
        self.removalMask = Image.new("RGBA", (self.clipWidth,self.clipHeight))
        removalMaskDraw = ImageDraw.Draw(self.removalMask)
        removalMaskDraw.rectangle((0,0,self.clipWidth,self.clipHeight), fill = (200,0,0,255))
        removalMaskDraw.rectangle((self.maskBoxX,self.maskBoxY,self.maskBoxX + self.maskBoxWidth,self.maskBoxY + self.maskBoxHeight), fill = (200,0,0,0))
        self.removalMask = self.removalMask.rotate(self.clipRotate, 0, expand=1)

    def colorize(self, clr=(250, 0, 250, 255), recolorize=False):

        # Colorize via overlay etc
        w = self.canvasImage.size[0]
        h = self.canvasImage.size[1]

        clrBlock = Image.new(self.workImage.mode, (w, h))
        clrBlockDraw = ImageDraw.Draw(clrBlock)

        # Color overlay on b/w PNG sprite
        # clrBlockDraw.rectangle((0, 0, w, h), fill=(255, 255, 255))
        clrBlockDraw.rectangle(
            (
                self.overlayxPos,
                self.overlayyPos,
                self.clrBlkWidth + self.overlayxPos,
                self.clrBlkHeight + self.overlayyPos,
            ),
            fill=clr,
        )

        try:

            if self.overLayMode == 0:
                imgTemp = ImageChops.add_modulo(clrBlock, self.imageLayer)
                if random.random() < .001:
                    self.overLayMode = 1
            else:
                imgTemp = ImageChops.darker(clrBlock, self.imageLayer)
                if random.random() < .001:
                    self.overLayMode = 0

            self.imageLayer.paste(imgTemp, (0, 0), imgTemp)

        except Exception as e:
            print(e, clrBlock.mode, self.config.renderImageFull.mode)
            pass
