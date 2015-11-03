# ################################################### #
import time
import random
import math

vx = 0
vy = 0
x = y = 0
r=g=b=125

colorSwitch = False

def drawImg() :
        global config
        global r,g,b
        global colorSwitch
        matrix = config.matrix
        draw = config.draw
        id = config.id

        screenWidth = config.screenWidth-1
        screenHeight = config.screenHeight-1

        for n in range(0,16):
                # Alternate Bands of Color
                changeColor(colorSwitch)
                config.draw.rectangle((n,n,screenWidth-n,screenHeight-n),  outline=(r,g,b))



# ################################################### #

def redraw():
        global config
        global x,y,vx,vy
        global colorSwitch
        
        # forces color animation
        changeColor()
        drawImg()
        config.matrix.SetImage(config.id,x,y)
        if(random.random() > .9) : colorSwitch = True
                


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
        #config.image = config.Image.new("RGBA", (config.screenWidth, config.screenHeight))
        #config.draw  = config.ImageDraw.Draw(config.image)
        #config.id = config.image.im.id
        count = 0
        while (count < arg * 2) :
                redraw()
                count+=1
                time.sleep(.125)
