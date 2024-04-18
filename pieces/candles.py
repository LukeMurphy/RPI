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


    config.renderImage = ImageOps.deform(config.img, WaveDeformer())

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
        
        self.imageContainer = Image.new("RGBA", (300, 300))
        self.image = Image.new("RGBA", (160, 160))
        self.draw = ImageDraw.Draw(self.image)
        self.flickering = False
        self.flickerRate = config.flickerRate
        self.flickerRange = config.flickerRange
        self.winkOutProb = config.winkOutProb
        self.stopFlickerProb = config.stopFlickerProb
        self.diameter = 0
        self.diameterMin = 0
        self.diameterMax = 0
        self.centerxOffset = config.centeryOffset
        self.centeryOffset = config.centeryOffset
        self.flickerCount = 0
        
    def make(self) :
        self.flickerCount = 0
        self.xOffset = round(random.uniform(config.xPositionOffset,config.canvasWidth)) - self.flickerRange
        self.yOffset = round(random.uniform(config.yPositionOffset,config.canvasHeight)) - self.flickerRange
        self.zOffset = round(random.uniform(config.yPositionOffset,config.canvasHeight)) - self.flickerRange
        self.diameter = round(random.uniform(self.diameterMin, self.diameterMax))
        
        self.flameDeltaX *= random.uniform(.8,1.2)
        mult = (config.canvasHeight/ (self.centeryOffset+1)/10)
        if mult > 3 :
            mult = 3.0
        self.flameDelta *= random.uniform(.8,1.2 )
        # self.flameDelta *= random.uniform(.8,1.2) * yOffset / config.canvasHeight
        self.xMultiplierSize *= random.uniform(.8,1.2)
        self.yMultiplierSize *= random.uniform(.8,1.2)
        
        pseudoDepth = 1.0 
        pseudoDepthAlpha = 1.0 
        if config.usePerspective == True :
            # sizeRatio = self.diameter/self.diameterMax
            # pr = d / (d + dz)
            pseudoDepth  = config.perspectiveD / ( config.perspectiveD  + self.zOffset +self.flickerRange)
            pseudoDepthAlpha  = config.perspectiveD / ( config.perspectiveD  + self.zOffset + self.flickerRange) * 1.5
            self.yOffset = round(config.canvasHeight * pseudoDepth)
            self.diameter = self.diameterMax * pseudoDepth
        
        alpha = round(random.uniform(40,255) * pseudoDepthAlpha)
   
        # self.clr1 = colorutils.getRandomColorHSL(340,40,.50,1.0,.5,.55,0,0,alpha,1.0)
        # self.clr2 = colorutils.getRandomColorHSL(25,40,1.0,1.0,.45,.55,0,0,alpha,1.0)
        # self.clr3 = colorutils.getRandomColorHSL(190,300,1.0,1.0,.5,.85,0,0,alpha,1.0)
        # self.clr3 = colorutils.getRandomColorHSL(25,55,1.0,1.0,.75,.85,0,0,round(alpha/2),1.0)
            
        self.clr1 = colorutils.getRandomColorHSL(config.clr1[0],config.clr1[1],config.clr1[2],config.clr1[3],config.clr1[4],config.clr1[5],config.clr1[6],config.clr1[7],alpha,1.0)
        self.clr2 = colorutils.getRandomColorHSL(config.clr2[0],config.clr2[1],config.clr2[2],config.clr2[3],config.clr2[4],config.clr2[5],config.clr2[6],config.clr2[7],alpha,1.0)
        self.clr3 = colorutils.getRandomColorHSL(config.clr3[0],config.clr3[1],config.clr3[2],config.clr3[3],config.clr3[4],config.clr3[5],config.clr3[6],config.clr3[7],round(alpha/2),1.0)
        self.flames = []
        
        centerxOffset = self.diameter/2
        centeryOffset = self.diameter/2
        for n in range(0, self.flamesPerUnit) :
            line_points = []
            line_points_small = []
            pts = 24
            rads = math.pi * 2 /pts
            for p in range(0,pts) :
                line_points.append([centerxOffset + math.cos(p * rads) * self.diameter/2, centeryOffset+ math.sin(p * rads) * self.diameter/2])
                line_points_small.append([centerxOffset + math.cos(p * rads) * self.diameter/8, centeryOffset+ math.sin(p * rads) * self.diameter/8])

            line_points.append([centerxOffset + math.cos(0 * rads) * self.diameter/2, centeryOffset+ math.sin(0 * rads) * self.diameter/2])
            line_points_small.append([centerxOffset + math.cos(0 * rads) * self.diameter/8, centeryOffset+ math.sin(0 * rads) * self.diameter/8])
            
            '''
            for p in self.flameShape_1 :
                line_points.append([self.centerxOffset + p[0] * self.xMultiplierSize, self.centeryOffset + p[1] * self.yMultiplierSize])
                
            for p in self.flameShape_1 :
                line_points_small.append([self.centerxOffset  + p[0] * self.xMultiplierSize * .55, self.centeryOffset + p[1] * self.yMultiplierSize * .5])
                # line_points_small.append([xOffset + 1 + p[0] * self.xMultiplierSize * .55 , yOffset + 3 + p[1] * self.yMultiplierSize * .5])
            '''
                
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


    def render(self) :
        
        if random.random() < self.flickerRate :
            self.flickering =  True
                
        if random.random() < self.winkOutProb and self.flickering == True and self.flickerCount > config.flickerCountMax:
            self.flickering =  False
            self.make()
            
        if random.random() < self.stopFlickerProb:
            self.flickering =  False
            self.flickerCount = 0
        
        numFlames = len(self.flames)
        
        for n in range(0,numFlames): 
            flamePart = self.flames[n]
        
            line_points = list(tuple(x) for x in flamePart[0])
            line_points_small = list(tuple(x) for x in flamePart[1])
            
            # self.draw.polygon(line_points, fill=self.clr2)
            # self.draw.ellipse((-self.diameter,-self.diameter,self.diameter*2,self.diameter*2), fill=config.bgColor)
            self.draw.rectangle((0,0,300,300), fill=config.bgColor)
            flickerRange = 0
            flickerRangeX = 0
            flickerRangeY = 0
            if self.flickering == True :
                flickerRangeX = self.flickerRangeX
                flickerRangeY = self.flickerRangeY
                self.flickerCount += 1
                
            centerxOffset = self.diameter/2 + self.flickerRangeX
            centeryOffset = self.diameter/2 + self.flickerRangeY
            
            boxX = round(random.uniform(self.diameter,self.diameter + flickerRangeX)) 
            boxY = round(random.uniform(self.diameter,self.diameter + flickerRangeY)) 
            # horizontal & vertical centering
            boxX0 = - boxX/2 + centerxOffset + self.centerxOffset
            boxY0 = - boxY/2 + centeryOffset + self.centeryOffset

            
            # correction to make "base" of ellipse same as initial undistorted circle
            yBase =  self.diameter - boxY
            
            shape = [(boxX0, boxY0 + yBase), (boxX + centerxOffset + self.centerxOffset, boxY + centeryOffset + yBase + self.centeryOffset)] 
            
            shape2 = [(boxX0 * config.holderXSize + config.holderXOff, 
                       (boxY0 + yBase) * config.holderYSize + config.holderYOff), 
                      ((boxX + centerxOffset + self.centerxOffset) * config.holderXSize + config.holderXOff, 
                       (boxY + centeryOffset + yBase + self.centeryOffset) * config.holderYSize + config.holderYOff)] 
            # self.draw.line(line_points, width=round(random.uniform(2,2 + flickerRange/2)), fill=self.clr1, joint="curve")
            self.draw.ellipse(shape2, fill=self.clr3, outline=None)
            self.draw.ellipse(shape, fill=self.clr2, outline=self.clr1)
            # self.draw.polygon(line_points_small, fill=self.clr3)
            
        # enhancer = ImageEnhance.Sharpness(self.image)
        # res = enhancer.enhance(10.0) 
        
        # res = self.image.filter(ImageFilter.GaussianBlur(radius=4))
        # config.workImage.paste(res, (self.xOffset, self.yOffset), res)
        rez = self.image.rotate(random.uniform(-2,2))
        
        self.imageContainer.paste(rez, (round(boxX/2),round(boxY/2)), rez)
        
        config.workImage.paste(self.imageContainer, (round(self.xOffset), round(self.yOffset)), self.imageContainer)
    
        self.update()

        if random.random() < config.reMakeRate :
            self.make()



def createFlames() :
    global config
    config.flameSets = []
    for f in range(0, config.numberOfFlames) :
        _flame = FlameUnit()
        _flame.diameterMin = config.diameterMin
        _flame.diameterMax = config.diameterMax
        _flame.centerxOffset  = config.centerxOffset 
        _flame.centeryOffset  = config.centeryOffset 
        
        _flame.flickerRangeX  = config.flickerRangeX 
        _flame.flickerRangeY  = config.flickerRangeY 
        
        _flame.make()
        config.flameSets.append(_flame)
        


## -------------------------------------------------##

def doDrawing() :
    global config

    config.workImageDraw.rectangle((0,0,config.canvasWidth,config.canvasHeight), fill = config.bgColor)

    for n in range(len(config.flameSets)) :
        refFlame = config.flameSets[n]
        refFlame.render()
    
    config.renderImage = ImageChops.add(config.workImage2, config.workImage, scale=1.42, offset=0)
    config.workImage2 = config.workImage.copy()
    # alterImage()
    

    # res = config.renderImage.filter(ImageFilter.GaussianBlur(radius=2))
    # enhancer = ImageEnhance.Sharpness(config.renderImage)
    # res = enhancer.enhance(10.0) 
    # res = res.filter(ImageFilter.GaussianBlur(radius=2))

    # config.render(res, 0, 0)
    config.render(config.renderImage, 0, 0)

## -------------------------------------------------##

def iterate(n=0):
    doDrawing()

## -------------------------------------------------##

     

def main(run=True) :
    global workConfig, config
    
    config.workImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.workImage2 = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.renderImage = Image.new("RGBA", (config.canvasWidth, config.canvasHeight))
    config.img =  config.workImage
    config.workImageDraw = ImageDraw.Draw(config.workImage)
    config.renderImageDraw = ImageDraw.Draw(config.renderImage)
    config.clr = (180,0,0,1)
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
        
    config.bgColor = tuple(int(x) for x in (workConfig.get("distortion", "bgColor")).split(","))
    config.clr1 = tuple(float(x) for x in (workConfig.get("distortion", "clr1")).split(","))
    config.clr2 = tuple(float(x) for x in (workConfig.get("distortion", "clr2")).split(","))
    config.clr3 = tuple(float(x) for x in (workConfig.get("distortion", "clr3")).split(","))
    config.numberOfFlames = int(workConfig.get("distortion", "numberOfFlames"))
    config.flamesPerUnit = int(workConfig.get("distortion", "flamesPerUnit"))
    config.flameDeltaX = int(workConfig.get("distortion", "flameDeltaX"))
    config.flameDelta = int(workConfig.get("distortion", "flameDelta"))
    config.xOffset = int(workConfig.get("distortion", "xOffset"))
    config.yOffset = int(workConfig.get("distortion", "yOffset"))
    config.xPositionOffset = int(workConfig.get("distortion", "xPositionOffset"))
    config.yPositionOffset = int(workConfig.get("distortion", "yPositionOffset"))
    
    
    config.xMultiplierSize = float(workConfig.get("distortion", "xMultiplierSize"))
    config.yMultiplierSize = float(workConfig.get("distortion", "yMultiplierSize"))
    config.centerxOffset = float(workConfig.get("distortion", "centeryOffset"))
    config.centeryOffset = float(workConfig.get("distortion", "centeryOffset"))
    config.diameterMin = float(workConfig.get("distortion", "diameterMin"))
    config.diameterMax = float(workConfig.get("distortion", "diameterMax"))

    config.holderXSize = float(workConfig.get("distortion", "holderXSize"))
    config.holderYSize = float(workConfig.get("distortion", "holderYSize"))
    config.holderXOff = float(workConfig.get("distortion", "holderXOff"))
    config.holderYOff = float(workConfig.get("distortion", "holderYOff"))

    config.reMakeRate = float(workConfig.get("distortion", "reMakeRate"))
    config.flickerRange = float(workConfig.get("distortion", "flickerRange"))
    config.flickerRangeX = float(workConfig.get("distortion", "flickerRangeX"))
    config.flickerRangeY = float(workConfig.get("distortion", "flickerRangeY"))
    config.flickerRate = float(workConfig.get("distortion", "flickerRate"))
    config.stopFlickerProb = float(workConfig.get("distortion", "stopFlickerProb"))
    config.changeRate = float(workConfig.get("distortion", "changeRate"))
    config.winkOutProb = float(workConfig.get("distortion", "winkOutProb"))
    config.flickerCountMax = float(workConfig.get("distortion", "flickerCountMax"))

    config.usePerspective = (workConfig.getboolean("distortion", "usePerspective"))
    config.perspectiveD = float(workConfig.get("distortion", "perspectiveD"))
        

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


