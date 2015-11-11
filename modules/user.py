# dRAWING uSER Class

import time
import random
import math



def drawUser() :

        centerx = 16 #config.screenWidth/2
        centery = 0 #32

        offsety = 3
        offsetx = -1

        dx = -5
        dy = 0
        bw = 34
        bh = 35
        bx1 = centerx - bw/2 + offsetx
        bx2 = bx1 + bw
        by1 = centery + bh /2 - 3 + offsety
        by2 = by1 + bh

        hw = 18
        hh = 18
        hx1 = centerx - hw/2 + offsetx
        hx2 = hx1 + hw
        hy1 = centery + offsety
        hy2 = centery + hh + offsety

        mw = 6
        mh = 4
        mx1 = centerx - mw/2 + offsetx
        mx2 = mx1 + mw
        my1 = centery + hw * 2/3 + offsety
        my2 = my1

        r=g=b=124
        b = 255
        global config
        matrix = config.matrix
        draw = config.draw
        id = config.id
        # x1, y1, x2, y2 of bounding box
        
        #### BODY
        config.draw.ellipse((bx1,by1,bx2,by2),fill=(r,g,b,1), outline=1)
        #### HEAD
        config.draw.ellipse((hx1,hy1,hx2,hy2),fill=(r,g,b,1), outline=1)
        #### MOUTH
       
        if (random.random() > .8) :
                r = int(random.uniform(0,255))
                g = int(random.uniform(0,255))
                b = int(random.uniform(0,255))
                #### BODY
                draw.ellipse((bx1,by1,bx2,by2),fill=(r,g,b,1), outline=1)
                #### HEAD
                draw.ellipse((hx1,hy1,hx2,hy2),fill=(r,g,b,1), outline=1)
                draw.ellipse((mx1,my1- mh/2,mx2,my2 + mh/2),fill=(180,80,80,2), outline=1)

                #matrix.SetImage(config.id, config.screenWidth/2 - centerx,centery)
                #config.render(config.image,  0, 0, config.screenWidth, config.screenHeight)
                
        else :
                draw.line((mx1, my1, mx1+mw, my2), fill=1)
                #matrix.SetImage(id,config.screenWidth/2  - centerx,centery)
                #config.render(config.image, 0, 0, config.screenWidth, config.screenHeight)

        config.render(config.image, 16, 32, 31, 32, False, True)      


def userAnimator(arg) :
        global config      
        image = config.Image.new("RGBA", (32, 32))
        config.draw  = config.ImageDraw.Draw(config.image)
        config.id = image.im.id
        count = 0
        while (count < arg) :
                drawUser()
                count+=1
                time.sleep(.25)
        #if(random.random() > .5) : burst(20)



