# ################################################### #
import time
import random
import math
import Image
import sys

r=g=b=125
pulseSpeed = .01

# defaults
boxWidth = 32
boxHeight = 32

rows  = 1
cols = 2
theta = 0
radius = 100
PI = math.pi

def clrAdjust(clr) :
        clrr = int(clr[0] * config.brightness)
        clrg = int(clr[1] * config.brightness)
        clrb = int(clr[2] * config.brightness)
        return (clrr,clrg,clrb)


def drawRects() :
        # Draw blacks of color on each panel
        # increace the lumens on each as if flashing lights - so 
        # increase is probably something like relates to a rate of
        # 2 Pi r or 

        global config
        global theta, radius, PI
        global colorSwitch
        global boxWidth,boxHeight
        global rows, cols

        rLevel = int((math.cos(theta) * 255))
        bLevel = int((math.sin(theta) * 255))
        clr = [(rLevel,0,0),(0,0,bLevel)]
        theta += PI/6

        for n in range(0,2) :
                xStart = n * boxWidth
                xEnd = xStart + boxWidth
                yStart = 0
                yEnd = boxHeight
                config.draw.rectangle((xStart, yStart, xEnd, yEnd ),  fill=clrAdjust(clr[n]) )

def redraw():
        global config
        drawRects()
        config.render(config.image,0,0,config.screenWidth,config.screenHeight, False)

        
# adapted to show Soliloguy of The Point
def animator(arg, mode = "cols") :
        global rHeight,rWidth, numSquares, colorSwitch, pulseSpeed, msg
        global rows, cols, columnLimit
        
        rows = 1
        cols = 1

        # reseting render image size
        config.renderImage = Image.new("RGBA", (config.actualScreenWidth , 32))
        config.image = config.Image.new("RGBA", (config.screenWidth, config.screenHeight))
        config.draw  = config.ImageDraw.Draw(config.image)
        config.id = config.image.im.id
        #config.matrix.Clear()

        count = 0
    
        rWidth = config.screenWidth
        rHeight = config.screenHeight

        countLimit = arg * 6
        interval = 4

        i = 0

        while (count < countLimit) :
                redraw()
                count += 1
                i += 1
                time.sleep(pulseSpeed)

        config.matrix.Clear()
        config.matrix.Fill(0)

