#!/usr/bin/python


from modules import utils
#from seqs.dm import dM
import Image
import ImageDraw
import ImageChops
import time
import random
from rgbmatrix import Adafruit_RGBmatrix
import datetime
import ImageFont
import textwrap
import math


#matrix = Adafruit_RGBmatrix(32, 12)

image = Image.new("RGBA", (96, 64))
invertedBlock = Image.new("RGBA", (96, 64))
draw  = ImageDraw.Draw(image)
draw2 = ImageDraw.Draw(invertedBlock)
id1 = image.im.id
id2 = invertedBlock.im.id


config = utils
config.matrix = Adafruit_RGBmatrix(32, 12)
config.image = Image.new("RGBA", (192, 64))
config.draw = ImageDraw.Draw(config.image)
config.Image = Image
config.ImageDraw = ImageDraw

config.tileSize = (32,64)
config.rows = 2
config.cols = 3
config.screenHeight =  64
config.screenWidth =  192
config.actualScreenWidth  = 192 * 2
config.useMassager = False
config.renderImage = Image.new("RGBA", (config.actualScreenWidth, 32))
config.brightness =  .125
config.path = "/home/pi/RPI1"

motions = []

def stroop(arg, clr, oppClr, speed = 1, direction = "Left"):
    global config
    fontSize  = 108
    font = ImageFont.truetype(config.path + '/fonts/freefont/FreeSansBold.ttf', fontSize)
    font2 = ImageFont.truetype(config.path + '/fonts/freefont/FreeSansBold.ttf', fontSize)
    pixLen = config.draw.textsize(arg, font = font)

    yOffset = int((pixLen[1] - 26)/4)

    image = Image.new("RGBA", pixLen)
    draw  = ImageDraw.Draw(image)
    clr = tuple(int(a*config.brightness) for a in (clr))

    # If not passed in, make the background the "opposite" color - from the seqs directory
    if(oppClr == ()) : oppClr  =  config.opp(clr)
    draw.rectangle((0,0,image.size[0], max(32,pixLen[1])), fill=oppClr)

    # fudged shadow
    draw.text((-1,-1-yOffset),arg,(0,0,0),font=font2)
    draw.text((1,1-yOffset),arg,(0,0,0),font=font2)
    draw.text((0,-yOffset),arg,clr,font=font)
    
    config.matrix.Clear()
    
    start = 0
    if (direction == "Right"): start = config.screenWidth/2
    motions.append([image,0,direction,start, speed])

def runAnimation(direction="out", stepsSpeed = 1):
    global motions, config
    c = 0
    
    dirUnit = 1 * stepsSpeed
    blockWidth = 1
    blockPos = 0
    blockDir = 1
    panelWidth = 96
    panelHeight = 64
    if (direction == "in") : dirUnit =  -1 * stepsSpeed
    while ( c < 100) :
        for i in range(0,2) :
                                   
            ref  = motions[i]
            image = ref[0]
            n = ref[1]
            direction = ref[2]
            offset = ref[3]
            speed = ref[4]

            if(direction == "Left") :
                motions[i][1] = n - dirUnit*speed
                xPos = 0
                xBlock = panelWidth - blockWidth - blockPos*blockDir
            else :
                motions[i][1] = n + dirUnit*blockDir*speed
                xPos = panelWidth
                xBlock = 0 + blockPos

            invertingBlock = Image.new("RGBA", (panelWidth,panelHeight))
            d = ImageDraw.Draw(invertingBlock)
            d.rectangle((xBlock,0,xBlock+blockWidth,panelHeight), fill=(255,255,0))
            
            #blockPos += 1
            if (blockPos > config.screenWidth/2):
                blockPos = 0

            # crop and load
            invertedBlock = ImageChops.offset(image,n,0)
            invertedBlock = invertedBlock.crop((0,0,panelWidth,panelHeight))
            imageToRender = ImageChops.difference( invertingBlock, invertedBlock)

            imageToRender.load()

            #idB = imageToRender.im.id
            #idA = invertedBlock.im.id
            #config.matrix.SetImage(idA, xPos, -5)

            config.render(invertedBlock,xPos,0,panelWidth,panelHeight,False)
            time.sleep(0.02)
    c = c + 1



stroop(" THINGS OF BEAUTY ",(255,67,0),(),4,"Right")
stroop(" TWO @ ONE TIME ",[255,255,0],(),4,"Left")
runAnimation("in")

