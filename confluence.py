#!/usr/bin/python

from modules.dm import dM
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


matrix = Adafruit_RGBmatrix(32, 4)

image = Image.new("RGBA", (26, 60))
image2 = Image.new("RGBA", (26, 60))
draw  = ImageDraw.Draw(image)
draw2 = ImageDraw.Draw(image2)
id1 = image.im.id
id2 = image2.im.id
matrix.SetImage(id1, 0, 0)
matrix.SetImage(id2, 60, 0)

config =  dM('Config 1')
config.matrix = matrix
config.id = id1
config.draw = draw
config.image = image


motions = []

def draw() :
    True    
def opp((r,g,b)) :
    minRGB = min(r,min(g,b))
    maxRGB = max(r,max(g,b))
    minmax = minRGB + maxRGB
    r = int((minmax - r) )
    g = int((minmax - g) )
    b = int((minmax -b)  )
    return (r,g,b)

def stroop(config, arg, clr, oppClr, speed = 0.006, direction = "Left"):

                speed = .018
                font = ImageFont.truetype('/home/pi/rpi-rgb-led-matrix-master/fonts/freefont/FreeSansBold.ttf',50)
                font2 = ImageFont.truetype('/home/pi/rpi-rgb-led-matrix-master/fonts/freefont/FreeSansBold.ttf',50)
                pixLen = config.draw.textsize(arg, font = font)

                yOffset = int((pixLen[1] - 32)/4)

                image = Image.new("RGBA", pixLen)
                image2 = Image.new("RGBA", (64,max(32,pixLen[1])))
                draw  = ImageDraw.Draw(image)
                
                id = image.im.id
                if(oppClr == ()) : oppClr  =  opp(clr)
                draw.rectangle((0,0,image.size[0], max(32,pixLen[1])), fill=oppClr)
                draw.text((-1,-1-yOffset),arg,(0,0,0),font=font2)
                draw.text((1,1-yOffset),arg,(0,0,0),font=font2)
                draw.text((0,-yOffset),arg,clr,font=font)
                matrix.Clear()
                
                start = 0
                if (direction == "Right"): start = 64
                motions.append([image,0,id,direction,start, speed])

def runAnimation(direction="out"):
                global motions
                c = 0
                dirUnit = 1
                if (direction == "in") : dirUnit =  -1
                while ( c < 100) :
                    for i in range(0,2) :
                                               
                        ref  = motions[i]

                        image = ref[0]
                        n = ref[1]
                        iid = ref[2]
                        direction = ref[3]
                        offset = ref[4]
                        speed = ref[5]



                        if(direction == "Left") :
                            motions[i][1]= n - dirUnit
                            xPos = 0
                        else :
                            motions[i][1]= n + dirUnit
                            xPos = 64
                        
                        image2 = ImageChops.offset(image,n,0)
                        image2 = image2.crop((0,0,64,38))
                        image2.load()
                        iid = image2.im.id
                   
                        config.matrix.SetImage(iid, xPos, -5)
                        time.sleep(0.006)
                c = c + 1



stroop(config,"-----",(255,67,0),(67,0,255),.008,"Right")
stroop(config,"-----",(255,67,0),(67,0,255),.004,"Left")
runAnimation("out")

