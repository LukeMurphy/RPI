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

global workConfig, config
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


## -------------------------------------------------##

def callBack():
    global config
    print("CALLBACL")
    return True

## -------------------------------------------------##

class WaveDeformer:

    def transform(self, x, y):
        y = y + config.amplitude*math.sin((x + config.xPos)/config.period) 
        return x, y

    def transform_rectangle(self, x0, y0, x1, y1):
        return (*self.transform(x0, y0),
                *self.transform(x0, y1),
                *self.transform(x1, y1),
                *self.transform(x1, y0),
                )

    def getmesh(self, img):
        self.w, self.h = img.size
        gridspace = config.gridSpace

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
    global config
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

def doDrawing() :
    global config

    config.workImageDraw.rectangle((0,0,config.canvasWidth,config.canvasHeight), fill = config.bgColor)

    
    for n in range(len(config.flameSets)) :
        
        refFlame = config.flameSets[n]
        
        numFlames = len(refFlame.flames)
        for n in range(0,numFlames): 
            flamePart = refFlame.flames[n]
        
            line_points = list(tuple(x) for x in flamePart[0])
            line_points_small = list(tuple(x) for x in flamePart[1])
            
            refFlame.draw.polygon(line_points, fill=refFlame.clr2)
            refFlame.draw.polygon(line_points_small, fill=refFlame.clr3)
            flickerRange = 0
            if random.random() < config.flickerRate :
                flickerRange = 4
            refFlame.draw.line(line_points, width=round(random.uniform(4,4 + flickerRange)), fill=refFlame.clr1, joint="curve")
            

        config.workImage.paste(refFlame.image, (refFlame.xOffset, refFlame.yOffset), refFlame.image)
    
        refFlame.update()

        if random.random() < config.reMakeRate :
            refFlame.make()
    
    # config.d += config.drate
    # config.workImageDraw.rectangle((0,0,100,100), fill = (255,0,0,255))
    # config.workImageDraw.rectangle((config.d,60,200,200), fill = (0,255,0,10))
    
    # if config.d >= 200 :
    #     config.d = 0
    #     # config.drate = 0
    #     config.workImageDraw.rectangle((0,60,200,200), fill = (0,255,0,10))
        
    # if random.random() < .001 :
    #     config.line_points.clear()
    #     resetPoints() 
    # config.workImageDraw.rectangle((x,y,x+100,y+100), fill = (255,0,0,100))
    # config.renderImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.renderImage.paste(config.workImage, (0,0))

    

## -------------------------------------------------##

def iterate(n=0):

    doDrawing()
    config.render(config.renderImage, 0, 0)
    # alterImage()

## -------------------------------------------------##


class FlameUnit :
    def __init__(self):
        self.u = 0
        self.flamesPerUnit  =  config.flamesPerUnit
        self.flameShape_1 = config.flameShape_1
        self.flames = []
        self.flameDeltaX = config.flameDeltaX
        self.flameDelta = config.flameDelta
        self.xMultiplierSize = config.xMultiplierSize
        self.yMultiplierSize = config.yMultiplierSize
        
        self.image = Image.new("RGBA", (400, 400))
        self.draw = ImageDraw.Draw(self.image)
        
        
    def make(self) :
        self.xOffset = round(random.uniform(0,config.canvasWidth))
        self.yOffset = round(random.uniform(0,config.canvasHeight))
        
        xOffset = random.uniform(0,10)
        yOffset = random.uniform(0,10)
        
        self.flameDeltaX *= random.uniform(.8,1.2)
        mult = (config.canvasHeight/ (yOffset+1)/10)
        if mult > 3 :
            mult = 3.0
        self.flameDelta *= random.uniform(.8,1.2 )
        # self.flameDelta *= random.uniform(.8,1.2) * yOffset / config.canvasHeight
        self.xMultiplierSize *= random.uniform(.8,1.2)
        self.yMultiplierSize *= random.uniform(.8,1.2)
        
        self.clr1 = colorutils.getRandomColorHSL(340,20,.50,1.0,.5,.5,0,0,190,1.0)
        self.clr2 = colorutils.getRandomColorHSL(25,55,1.0,1.0,.5,.75,0,0,220,1.0)
        self.clr3 = colorutils.getRandomColorHSL(190,300,1.0,1.0,.5,.85,0,0,70,1.0)

        self.flames = []
        for n in range(0, self.flamesPerUnit) :
            line_points = []
            line_points_small = []
            for p in self.flameShape_1 :
                line_points.append([xOffset + p[0] * self.xMultiplierSize, yOffset + p[1] * self.yMultiplierSize])
            for p in self.flameShape_1 :
                line_points_small.append([xOffset + 11 + p[0] * self.xMultiplierSize * .55 , yOffset + 30  + p[1] * self.yMultiplierSize * .5])
            self.flames.append([line_points,line_points_small])
            
    def update(self):
        
        for n in range(0, len(self.flames)) :
            for n2 in range(0, len(self.flames[n])) :
                for n3 in range(0,len(self.flames[n][n2])) :
                    for p in range(0,len(self.flames[n][n2][n3])) :
                        if random.random() < config.changeRate :
                            self.flames[n][n2][n3][0] += random.uniform(-self.flameDeltaX,self.flameDeltaX)
                        if random.random() < config.changeRate :
                            self.flames[n][n2][n3][1] += random.uniform(-self.flameDelta,self.flameDelta)






def createFlames() :
    global config
    config.flameSets = []
    for f in range(0, config.numberOfFlames) :
        _flame = FlameUnit()
        _flame.make()
        config.flameSets.append(_flame)
        
        
        

def main(run=True) :
    global workConfig, config
    
    config.workImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.renderImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.img =  config.workImage
    config.workImageDraw = ImageDraw.Draw(config.workImage)
    config.renderImageDraw = ImageDraw.Draw(config.renderImage)
    config.clr = (180,0,0,7)
    config.clr2 = (255,200,0,10)
    config.clr3 = (25,10,240,3)
    config.line_points = []
    config.line_points_small = []
    
    config.d = 0
    config.drate = 1
  
    config.flameSets = []
    firstSet = [[100, 100], [130, 260], [120, 280], [100, 300], [80, 260] ,[100, 90],[100, 100]]
    
    flameShape_1 = [[4,1],[5,6],[5,8],[4,8],[3,8],[3,6],[4,2],[4,1]]
    flameShape_1 = [[4,3],[5,6],[5,8],[4,8],[3,8],[3,6],[4,2],[4,3]]
    flameShape_1 = [[2,2],[4,1],[5,1],[7,2],[8,4],[8,7],[5,8],[2,6],[2,3]]
    
    config.flameShape_1 = [[4,1],[5,6],[5,8],[4,8],[3,8],[3,6],[4,2],[4,1]]
    config.flameShape_1 = [[2,2],[5,1],[7,2],[8,4],[8,6],[3,8],[3,7],[2,8],[1,5]]
    config.flameShape_1 = [[2,3],[3,1.5],[4,1],[5,1],[8,3],[8,5],[7,2],[8,3],[8,5],[7,7],[5,8],[4,8],[2,7],[1,5],[1.5,3.5],[1,4]]
    
    config.bgColor = (0,0,0,1)
    config.numberOfFlames = 80
    config.flamesPerUnit = 1
    config.flameDeltaX = .5
    config.flameDelta = 2.5
    config.xOffset = 0
    config.yOffset = 0
    config.xMultiplierSize = 6
    config.yMultiplierSize = 7
    
    config.reMakeRate = .0001
    config.flickerRate = .02
    config.changeRate = .01

    createFlames()     

    config.playSpeed = .02

    # config.img = loadImage(workConfig.get("distortion", "imageAsset"))
    config.xPos = int(workConfig.get("distortion", "xPos"))
    config.yPos = int(workConfig.get("distortion", "yPos"))
    config.scrollSpeed = float(workConfig.get("distortion", "scrollSpeed"))
    config.xNoiseFactor = float(workConfig.get("distortion", "xNoiseFactor"))
    config.yNoiseFactor = float(workConfig.get("distortion", "yNoiseFactor"))

    config.period = float(workConfig.get("distortion", "period"))
    config.rads = math.pi / config.canvasWidth * config.period
    config.amplitude = float(workConfig.get("distortion", "amplitude"))
    config.gridSpace = int(workConfig.get("distortion", "gridSpace"))


