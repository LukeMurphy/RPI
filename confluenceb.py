#!/usr/bin/python


from seqs import utils
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


matrix = Adafruit_RGBmatrix(32, 4)

image = Image.new("RGBA", (26, 60))
image2 = Image.new("RGBA", (26, 60))
blockTest = Image.new("RGBA", (32,20))
draw  = ImageDraw.Draw(image)
draw2 = ImageDraw.Draw(image2)
id1 = image.im.id
id2 = image2.im.id
matrix.SetImage(id1, 0, 0)
matrix.SetImage(id2, 60, 0)

config =  utils
config.matrix = matrix
config.id = id1
config.draw = draw
config.image = image

motions = []

def stroop(config, arg, clr, oppClr, speed = 1, direction = "Left"):

                fontSize  = 72
                font = ImageFont.truetype('/home/pi/rpi-rgb-led-matrix-master/fonts/freefont/FreeSansBold.ttf', fontSize)
                font2 = ImageFont.truetype('/home/pi/rpi-rgb-led-matrix-master/fonts/freefont/FreeSansBold.ttf', fontSize)
                pixLen = config.draw.textsize(arg, font = font)

                yOffset = int((pixLen[1] - 26)/4)

                image = Image.new("RGBA", pixLen)
                image2 = Image.new("RGBA", (64,max(32,pixLen[1])))
                draw  = ImageDraw.Draw(image)
                
                id = image.im.id
                # If not passed in, make the background the "opposite" color - from the seqs directory
                if(oppClr == ()) : oppClr  =  utils.opp(clr)
                draw.rectangle((0,0,image.size[0], max(32,pixLen[1])), fill=oppClr)

                # fudged shadow
                draw.text((-1,-1-yOffset),arg,(0,0,0),font=font2)
                draw.text((1,1-yOffset),arg,(0,0,0),font=font2)
                draw.text((0,-yOffset),arg,clr,font=font)
                
                matrix.Clear()
                
                start = 0
                if (direction == "Right"): start = 64
                motions.append([image,0,id,direction,start, speed])

def runAnimation(direction="out", stepsSpeed = 1):
                global motions
                c = 0
                
                dirUnit = 1 * stepsSpeed
                blockWidth = 1
                blockPos = 0
                blockDir = 1
                panelWidth = 64
                if (direction == "in") : dirUnit =  -1 * stepsSpeed
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
                            motions[i][1]= n - dirUnit*speed
                            xPos = 0
                            xBlock = panelWidth - blockWidth - blockPos*blockDir
                        else :
                            motions[i][1]= n + dirUnit*blockDir*speed
                            xPos = panelWidth
                            xBlock = 0 + blockPos
                            #xPos - blockWidth

                        blockTest = Image.new("RGBA", (64,64))
                        d  = ImageDraw.Draw(blockTest)
                        d.rectangle((xBlock,0,xBlock+blockWidth,38), fill=(255,255,0))
                        
                        #blockPos += 1
                        if (blockPos > 64):
                            blockPos = 0
                            #blockDir *= -1
                        # crop and load
                        image2 = ImageChops.offset(image,n,0)
                        image2 = image2.crop((0,0,64,38))
                        image3 = ImageChops.difference( blockTest, image2)

                        image3.load()
                        idB = image3.im.id
                        idA = image2.im.id
                   
                        config.matrix.SetImage(idA, xPos, -5)
                        time.sleep(0.005)
                c = c + 1



stroop(config," THINGS OF BEAUTY ",(255,67,0),(),3,"Right")
stroop(config," TWO @ ONE TIME ",(255,255,0),(),3,"Left")
runAnimation("in")

