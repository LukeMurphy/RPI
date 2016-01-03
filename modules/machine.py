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
redrawSpeed = .01
boxHeight = 30
boxWidth = 26
smile = -1


def drawMachine(mDisplacey = -1) :
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
        # m1 is left point start, mw is mouth width
        m1 = 6
        mw = 12
        # Sets a frowm :[ upsidedown :]
        #mDisplacey = -1
        mDisplacex = 0

        # Fill colors
        rf = gf = bf = 0

        # line width
        w = 1

        # First state is  :[ second state is :]
        if (r == 0 ):
                rf = int(255 * config.brightness)
                gf = 0
                r = 0
                g = int(255 * config.brightness)
                b = 0
        else :
                rf = 0
                gf = int(255 * config.brightness)
                r = int(255 * config.brightness)
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

        #left corner
        #config.draw.line((x1+3,y1+d2,x1+2,y1+d2 +1), fill=(r,g,b), width = w)
        config.draw.line((m1 - mDisplacex, y1 + d2 + mDisplacey, m1, y1 + d2), fill=(r,g,b), width = w)
        #center
        config.draw.line((m1, y1 + d2, m1 + mw, y1 + d2), fill=(r,g,b), width = w)
        #rigth corner
        #config.draw.line((x1+d2+1,y1+d2,x1+d2 +2,y1+d2+1), fill=(r,g,b), width = w)
        config.draw.line((m1 + mw, y1 + d2, m1 + mw + mDisplacex, y1 + d2 + mDisplacey), fill=(r,g,b), width = w)

def redraw():
        global config
        global x,y,vx,vy, boxWidth, boxHeight, smile
        speed = 1

        xMax = config.screenWidth - 12
        yMax = config.screenHeight - 12

        buffer = 12
        x = x + vx
        y = y + vy

        drawMachine(smile)

        # Render using main render function - manages the matrix tiling
        config.render(config.image,x,y,boxWidth,boxHeight,False)

                
        if (x > xMax + buffer):
                vx = vx * -1
                changeColor()
                if(random.random() > .5): vx = int(vx * 2 * random.random())
                x = xMax +  buffer - 2
                changeSmile()
        if (x < 0 - 26 + 1):
                vx = vx * -1
                changeColor()
                if(random.random() > .5): vx = int(vx * 2 * random.random())
                x = -26 + 1
                changeSmile()
        if (y > yMax + buffer):
                vy = vy * -1
                changeColor()
                if(random.random() > .5): vx = int(vy * 2 * random.random())
                y = yMax + buffer -  2
                changeSmile()
        if(y < 0 - boxHeight):
                vy = vy * -1
                changeColor()
                if(random.random() > .5): vx = int(vy * 2 * random.random())
                y = 0 - boxHeight
                changeSmile()

def changeSmile() :
        global smile
        frownProb = .85
        if(random.random() > frownProb) : 
                smile = 1
        else :
                smile = -1

def changeColor( rnd = False) :
                global r,g,b        
                if (rnd == False) :
                                if(r == int(255 * config.brightness)) :
                                                r = 0
                                                g = int(255 * config.brightness)
                                                b = 0
                                else :
                                                g = 0
                                                r = int(255 * config.brightness)
                                                b = 0
                else :
                                r = int(random.uniform(0,255))
                                g = int(random.uniform(0,255))
                                b = int(random.uniform(0,255))

def machineAnimator(arg) :
        global redrawSpeed, x, y, vx, vy
        config.renderImage = Image.new("RGBA", (config.actualScreenWidth, config.screenHeight))
        config.image = config.Image.new("RGBA", (26, 30))
        config.draw  = config.ImageDraw.Draw(config.image)
        config.id = config.image.im.id

        x = int(random.random() * config.screenWidth)
        y = int(random.random() * config.screenHeight)

        x=50
        y=50
        #vx = 0
        #vy = 0

        count = 0

        while (count < arg * 2) :
                redraw()
                count+=1
                time.sleep(redrawSpeed)

