# dRAWING uSER Class

import time
import random
import math

centerx = 0 #config.screenWidth/2
centery = 0 #32

offsety = 0
offsetx = 0

userCenterx = 0
userCentery = -0

scale = 1

userList = []

def drawUser(n = 0) :

        global centery, centery, offsetx, offsety, userCenterx, userCentery, userList
        global config, scale

        userCenterx = userList[n][0]
        userCentery = userList[n][1]

        hw = 18 * scale
        hh = 18 * scale
        mw = 6 * scale
        mh = 4 * scale
        bw = 32 * scale
        bh = 32 * scale

        hx1 = userCenterx + bw/2 - hw/2 + offsetx * scale
        hx2 = hx1 + hw
        hy1 = userCentery + offsety * scale
        hy2 = userCentery + hh + offsety * scale

        mx1 = userCenterx - mw/2 + bw/2 + offsetx * scale
        mx2 = mx1 + mw
        my1 = userCentery + hw * 2/3 + offsety * scale
        my2 = my1

        bx1 = userCenterx + offsetx * scale
        bx2 = bx1 + bw
        by1 = userCentery + hh -3 + offsety * scale
        by2 = 3 + by1 + bh

        r=g=b=int(124 * config.brightness)
        b = int(255 * config.brightness)

        onColor = (0,0,100,1)
        oColor  = (int(400 * config.brightness),int(random.uniform(50,300) * config.brightness),int(0 * config.brightness),1)
        
        matrix = config.matrix
        draw = config.draw

        #### BODY
        config.draw.ellipse((bx1,by1,bx2,by2),fill=(r,g,b,1), outline=1)
        draw.arc((int(bx1-1),int(by1-1),int(bx2+1),int(by2+1)),180,360,fill=onColor)
        #### HEAD
        draw.ellipse((hx1,hy1,hx2,hy2),fill=(r,g,b,1), outline=1)
        draw.arc((int(hx1-1),int(hy1-1),int(hx2+1),int(hy2+1)),130,420,fill=onColor)
        #### MOUTH
       
        if (random.random() > .8) :
                r = int(random.uniform(0,255) * config.brightness)
                g = int(random.uniform(0,255) * config.brightness)
                b = int(random.uniform(0,255) * config.brightness)
                #### BODY
                draw.ellipse((bx1,by1,bx2,by2),fill=(r,g,b,1), outline=1)
                ## Cleanup
                draw.arc((int(bx1-1),int(by1-1),int(bx2+1),int(by2+1)),180,360,fill=oColor)
                #### HEAD
                draw.ellipse((hx1,hy1,hx2,hy2),fill=(r,g,b,1), outline=1)
                draw.arc((int(hx1-1),int(hy1-1),int(hx2+1),int(hy2+1)),130,420,fill=oColor)
                draw.ellipse((mx1,my1- mh/2,mx2,my2 + mh/2), fill=(int(180 * config.brightness),int(80 * config.brightness),int(80 * config.brightness),2), outline=1)
                
        else :
                draw.line((mx1, my1, mx1+mw, my2), fill=1)


def userAnimator(arg, numUsers=-1, fixed = False) :
        global config, userList, userCenterx, userCentery , scale 
        config.image = config.Image.new("RGBA", (config.screenWidth, config.screenHeight))
        config.draw  = config.ImageDraw.Draw(config.image)
        #config.draw.rectangle((0,0,int(32 * scale), int(32 * scale)), fill= (0,0,0))
        #config.id = image.im.id
        
        if(numUsers == -1) : numUsers = int(random.uniform(1,3))
        userList = [[0,0]]*numUsers

        xPosInit = 0
        xMid = int(32 * scale) #config.screenWidth/config.cols
        for n in range(0,numUsers) :
                if(fixed == False) : 
                        xPos = int(random.uniform(xPosInit+2,(config.screenWidth-32) * 2/3))
                else :
                        xPos = userCenterx + n * (xMid + userCenterx)
                userList[n] = [xPos + xPosInit, userCentery]
                #xPosInit =  xPos + 32

        count = 0
        while (count < arg) :
                for n in range(0,numUsers) : drawUser(n)
                config.render(config.image, 0, 0,128,128)
                count+=1
                t = random.uniform(.01,.3)
                time.sleep(t)
        #if(random.random() > .5) :  userAnimator(arg)



