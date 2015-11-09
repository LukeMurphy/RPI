# ################################################### #
import time
import random
import math

vx = 0
vy = 0
x = y = 0
r=g=b=125

colorSwitch = False

'''
make script to reduce from one square to 2 to 4 to 8 to 16...
'''

rHeight = 0
rWidth = 0
numSquares = 1

def drawImg() :
        global config
        global r,g,b
        global colorSwitch
        global rHeight,rWidth,numSquares

        matrix = config.matrix
        draw = config.draw
        id = config.id

        lines = rHeight/2
        for i in range(0, numSquares):
                xOffset = i * rWidth
                for n in range(0,lines):
                        # Alternate Bands of Color
                        changeColor(colorSwitch)
                        xStart = xOffset + n
                        xEnd = xOffset+rWidth-n-1
                        yStart = n
                        yEnd =rHeight-n-1
                        config.draw.rectangle((xStart, yStart, xEnd, yEnd ),  outline=(r,g,b))


def redraw():
        global config
        global x,y,vx,vy
        global colorSwitch
        
        # forces color animation
        changeColor()
        drawImg()

        #config.matrix.SetImage(config.id,x,y)
        config.render(config.image,x,y,config.screenWidth,config.screenHeight)

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



def animator(arg) :
        global rHeight,rWidth, numSquares, colorSwitch

        config.image = config.Image.new("RGBA", (config.screenWidth, config.screenHeight))
        config.draw  = config.ImageDraw.Draw(config.image)
        config.id = config.image.im.id
        count = 0
        
        rHeight = config.screenHeight
        rWidth = config.screenWidth

        while (count < arg * 2) :
                redraw()
                count+=1
                if(random.random() > .97 and numSquares < 33) : 
                        colorSwitch = False
                        rWidth = rWidth/2
                        numSquares *=2

                time.sleep(.125)
