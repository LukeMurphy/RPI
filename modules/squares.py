# ################################################### #
import time
import random
import math
import Image
import sys


vx = 0
vy = 0
x = y = 0
r=g=b=125
pulseSpeed = .1
colorSwitch = False
columnLimit = 16

'''
make script to reduce from one square to 2 to 4 to 8 to 16...
'''

rHeight = 0
rWidth = 0
numSquares = 1
rows  = 2
cols = 2

def drawImg() :
        global config
        global r,g,b
        global colorSwitch
        global rHeight,rWidth,numSquares

        #matrix = config.matrix
        #draw = config.draw
        #id = config.id

        lines = rHeight/2
        for i in range(0, numSquares):
                xOffset = i * rWidth
                #changeColor(colorSwitch)
                for n in range(0,lines):
                        # Alternate Bands of Color
                        changeColor(colorSwitch)
                        xStart = xOffset + n
                        xEnd = xOffset+rWidth-n-1
                        yStart = n
                        yEnd =rHeight-n-1
                        config.draw.rectangle((xStart, yStart, xEnd, yEnd ),  outline=(r,g,b))
def drawRects() :
        global config
        global r,g,b
        global colorSwitch
        global rHeight,rWidth,numSquares
        global rows, cols

        changeColor(colorSwitch)
        for row in range(0, rows):
                rHeight = int(config.screenHeight / (rows))
                yOffset = int(row * rHeight)
                lines = int(rHeight/2)
                #changeColor(colorSwitch)
                for col in range(0, cols):
                        rWidth = int(config.screenWidth / (cols))
                        xOffset = int(col * rWidth)
                        #changeColor(colorSwitch)
                        for n in range(0,lines):
                                # Alternate Bands of Color
                                changeColor(colorSwitch)
                                xStart = n + xOffset
                                xEnd = rWidth - n - 1 + xOffset
                                yStart = n + yOffset
                                yEnd = rHeight - n - 1 + yOffset
                                config.draw.rectangle((xStart, yStart, xEnd, yEnd ),  outline=(r,g,b))

def redraw():
        global config
        global x,y,vx,vy
        global colorSwitch
        
        # forces color animation
        # changeColor()
        #drawImg()
        drawRects()

        #config.matrix.SetImage(config.id,x,y)
        config.render(config.image,x,y,config.screenWidth,config.screenHeight, False)

        if(random.random() > .93) : colorSwitch = True
                
def changeColor( rnd = False) :
                global r,g,b        
                if (rnd == False) :
                                if(r == 255) :
                                                r = 0
                                                g = 255
                                                b = 0
                                else :
                                                g = 0
                                                r = 255
                                                b = 0
                else :
                                r = int(random.uniform(0,255))
                                g = int(random.uniform(0,255))
                                b = int(random.uniform(0,255))

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
        numSquares = 1
        rWidth = config.screenWidth
        rHeight = config.screenHeight
        
        arg = 20
        pulseSpeed = .1

        countLimit = arg * 6
        interval = 4

        i = 0

        if (mode == "rows") :
                rowIncrement = True
                while (count < countLimit) :
                        redraw()
                        count += 1
                        interval = arg - rows * 2 - cols
                        i += 1
                        if(i > interval and cols <= 8) : 
                                i = 0
                                colorSwitch = False
                                if(rowIncrement) :
                                        rows *= 2
                                        rowIncrement = False
                                else :
                                        cols *= 2
                                        rowIncrement = True
                        config.soliloquy()
                        time.sleep(pulseSpeed)
        if (mode == "cols") :
                colIncrement = True
                while (count < countLimit) :
                        redraw()
                        count += 1
                        interval = arg - rows * 2 - cols
                        i += 1
                        if(i > interval and cols <= columnLimit) : 
                                i = 0
                                colorSwitch = False
                                if(colIncrement) :
                                        cols *= 2
                                        colIncrement = False
                                else :
                                        rows *= 2
                                        colIncrement = True
                        config.soliloquy()
                        time.sleep(pulseSpeed)
        else :
                while (count < countLimit) :
                        redraw()
                        count += 1
                        i += 1
                        if(i > interval and numSquares < 17) : 
                                i = 0
                                colorSwitch = False
                                rWidth = rWidth/2
                                numSquares *=2
                        config.soliloquy()
                        time.sleep(pulseSpeed)

        config.matrix.Clear()
        config.matrix.Fill(0)

