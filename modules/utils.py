import time
import random
import math
import sys

screenWidth =  128
screenHeight = 64

I = 0
lastI = 1

# for now, 2 panels means a stack of two 32x64 + 32x64
# or, 4x2 x 32
panels = 2
path = "/home/pi/rpimain"

msg = ["Infinite beatitude of existence! I am; and there is nothing else beside I.",
"I fill all Space, and what I fill, I am.", 
"What I think, that I utter; and what I utter, that I hear; and I itself is Thinker, Utterer, Hearer, Thought, Word, Audition; ",
"it is the One, and yet the All in All.",
"Ah, the happiness, ah, the happiness of Being! Ah, the joy, ah, the joy of Thought! "
"What can I not achieve by thinking! My own Thought coming to myself, suggestive of my disparagement, thereby to enhance My happiness! ",
"Sweet rebellion stirred up to result in triumph! Ah, the divine creative power of the All in One! Ah, the joy, the joy of Being!", 
"Me me me I mine mine mine is"] 

msg = [""]

global imageTop,imageBottom,image,config

def opp((r,g,b)) :
    minRGB = min(r,min(g,b))
    maxRGB = max(r,max(g,b))
    minmax = minRGB + maxRGB
    r = int((minmax - r) )
    g = int((minmax - g) )
    b = int((minmax -b)  )
    return (r,g,b)

def soliloquy(override = False) :
    global I, lastI, msg
    length = len(msg)
    if(length > 1) :
        if(random.random() > .9 or override) :
                I = int(random.random() * length)

                while (I == lastI):
                        I = int(random.random() * length)
                sys.stdout.write(msg[I])
                sys.stdout.flush()
                #print(msg[I]),
                lastI = I

def test() : matrix.Fill(244,255,0)                 

def changeColor(rnd = False) :
                
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

def render(imageTemp,xOffset,yOffset,w=128,h=64,crop=True, overlayBottom=False):

    global imageTop, imageBottom, screenHeight, screenWidth, panels, matrix, image, renderImage
    yOffset2 = 0
    # the rendered image is the screen size
    #renderImage = Image.new("RGBA", (screenWidth * panels , 32))
    if(crop == True) :
        imageTop = imageTemp.crop((xOffset, yOffset, xOffset + screenWidth, 32+yOffset))
        imageBottom = imageTemp.crop((xOffset, 32+yOffset, xOffset + screenWidth, 64+yOffset))
        renderImage.paste(imageTop, (0,0))
        renderImage.paste(imageBottom, (screenWidth,0))
    else:
        # this is what I'd like to do ....
        # renderImage.paste(imageTemp, (xOffset, yOffset))

        # get the overlap of the retangle to be rendered with the size of the "top" panel
        # draw the top "half" to the first set of panels then draw the bottom half
        # to the second panels, offset by screenWidth and difference over 32 pix

        xOL = max(0, min(xOffset + w, screenWidth) - max(xOffset, 0));
        yOL = max(0, min(yOffset + h, 32) - max(yOffset, 0));

        p1x = 0
        p1y = 0
        p2x = xOL
        p2y = yOL

        if(xOffset < 0) : 
            p1x = w - xOL
            p2x = w
        if(yOffset < 0) : 
            p1y = h - yOL
            p2y = h

        p1Crop = (p1x, p1y, p2x, p2y)
        p2Crop = (p1x, p2y, p2x, p2y + (h - yOL))

        imageTop = imageTemp.crop(p1Crop)

        if(imageTop.size[1] != 0) :
            renderImage.paste(imageTop, (  xOffset + p1Crop[0], yOffset + p1Crop[1], 
                                            xOffset + p1Crop[2], yOffset + p1Crop[3]))

        # Only offset the bottom if its top is more than 32
        if((yOffset+h) > 32) : 
            yOffset2 = min(yOffset - 32, 0) 
            if(yOffset > 32) : yOffset2 = yOffset - 32

            imageBottom = imageTemp.crop(p2Crop)
            renderImage.paste(imageBottom, (    xOffset + p2Crop[0] + screenWidth, yOffset2 + p2Crop[1], 
                                                xOffset + p2Crop[2] + screenWidth, yOffset2 + p2Crop[3]))


    if(overlayBottom) :
        renderImage = Image.new("RGBA", (w , h))
        renderImage.paste(imageTemp, (0,0))
        iid = renderImage.im.id
        idtemp = image.im.id
        matrix.SetImage(iid, xOffset + screenWidth, 0)
    else :
        iid = renderImage.im.id
        idtemp = image.im.id
        matrix.SetImage(iid, 0, 0)

    # DEBUG .....
    #time.sleep(10)
    #exit()
    # ************************************ #
   




