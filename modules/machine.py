# ################################################### #
import time
import random
import math
import Image

vx = 1
vy = 2
x = 0
y = 0
r=g=b=125
redrawSpeed = .015
boxHeight = 30
boxWidth = 26


def drawMachine() :
        global config
        global r,g,b
        matrix = config.matrix
        draw = config.draw
        id = config.id

        screenWidth = config.screenWidth
        screenHeight = config.screenHeight
        
        # x1, y1 are inital face points (left eye)
        x1 = 5
        y1 = 12
        # d is size of eye X
        d = 4
        # d2 is mouth / right eye
        d2 = 10

        # Fill colors
        rf = gf = bf = 0

        # line width
        w = 1

        if (r == 0 ):
                rf = 255
                gf = 0
                r = 0
                g = 255
                b = 0
        else :
                rf = 0
                gf = 255
                r = 255
                g = 0
                b = 0
                w = 2

        # outline
        config.draw.rectangle((1,1,24,28), fill=(rf,gf,bf), outline=(r,g,b))
        
        # eyes
        config.draw.line((x1,y1,x1+d,y1+d), fill=(r,g,b), width = w)
        config.draw.line((x1,y1+d,x1+d,y1), fill=(r,g,b), width = w)

        x1 = x1 + d2

        config.draw.line((x1,y1,x1+d,y1+d), fill=(r,g,b), width = w)
        config.draw.line((x1,y1+d,x1+d,y1), fill=(r,g,b), width = w)

        # mouth
        x1 = x1 - d2
        y1 = y1 + -1

        config.draw.line((x1+3,y1+d2,x1+2,y1+d2 +1), fill=(r,g,b), width = w)
        config.draw.line((x1+4,y1+d2,x1+d2,y1+d2), fill=(r,g,b), width = w)
        config.draw.line((x1+d2+1,y1+d2,x1+d2 +2,y1+d2+1), fill=(r,g,b), width = w)

def redraw():
        global config
        global x,y,vx,vy, boxWidth, boxHeight
        speed = 1

        xMax = config.screenWidth - 12
        yMax = config.screenHeight - 12

        buffer = 12
        x = x + vx
        y = y + vy

        drawMachine()

        # Render using main render function - manages the matrix tiling
        config.render(config.image,x,y,boxWidth,boxHeight,False)

                
        if (x > xMax + buffer):
                vx = vx * -1
                changeColor()
                if(random.random() > .5): vx = int(vx * 2 * random.random())
                x = xMax +  buffer - 2
        if (x < 0 - 26 + 1):
                vx = vx * -1
                changeColor()
                if(random.random() > .5): vx = int(vx * 2 * random.random())
                x = -26 + 1
        if (y > yMax + buffer):
                vy = vy * -1
                changeColor()
                if(random.random() > .5): vx = int(vy * 2 * random.random())
                y = yMax + buffer -  2
        if(y < 0 - boxHeight):
                vy = vy * -1
                changeColor()
                if(random.random() > .5): vx = int(vy * 2 * random.random())
                y = 0 - boxHeight


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

def machineAnimator(arg) :
        global redrawSpeed, x, y, vx, vy
        config.renderImage = Image.new("RGBA", (config.screenWidth * config.panels , config.screenHeight))
        config.image = config.Image.new("RGBA", (26, 30))
        config.draw  = config.ImageDraw.Draw(config.image)
        config.id = config.image.im.id

        x = int(random.random() * config.screenWidth)
        y = int(random.random() * config.screenHeight)

        count = 0

        while (count < arg * 2) :
                redraw()
                count+=1
                time.sleep(redrawSpeed)
