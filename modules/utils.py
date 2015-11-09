import time
import random
import math

screenWidth =  128
screenHeight = 64

# for now, 2 panels means a stack of two 32x64 + 32x64
# or, 4x2 x 32
panels = 2


path = "/home/pi/rpimain"

global imageTop,imageBottom,image

def opp((r,g,b)) :
    minRGB = min(r,min(g,b))
    maxRGB = max(r,max(g,b))
    minmax = minRGB + maxRGB
    r = int((minmax - r) )
    g = int((minmax - g) )
    b = int((minmax -b)  )
    return (r,g,b)


def test() :
        matrix.Fill(244,255,0)

def change() :
        print("")                     

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


def render(imageTemp,xOffset,yOffset,w=128,h=64,crop=True):

    global imageTop, imageBottom, screenHeight, screenWidth, panels, matrix, image, renderImage

    # the rendered image is the screen size
    #renderImage = Image.new("RGBA", (screenWidth * panels , 32))
    if(crop == True) :
        imageTop = imageTemp.crop((xOffset, yOffset, xOffset + 128, 32+yOffset))
        imageBottom = imageTemp.crop((xOffset, 32+yOffset, xOffset + 128, 64+yOffset))
        renderImage.paste(imageTop, (0,0))
        renderImage.paste(imageBottom, (128,0))
    else:
        # this is what I'd like to do ....
        # renderImage.paste(imageTemp, (xOffset, yOffset))

        # get the overlap of the retangle to be rendered with the size of the "top" panel
        # draw the top "half" to the first set of panels then draw the bottom half
        # to the second panels, offset by screenWidth and difference over 32 pix
        xOL = max(0, min(xOffset + w, 128) - max(xOffset, 0));
        yOL = max(0, min(yOffset + h, 32) - max(yOffset, 0));

        

        imageTop = imageTemp.crop((0, 0, xOL, yOL))
        imageBottom = imageTemp.crop((0, yOL, xOL, h+1))

        
    

        renderImage.paste(imageTop, (xOffset, yOffset,xOL + xOffset, yOL + yOffset))

        # Only offset the bottom if its top is more than 32
        if((yOffset+h) > 32) : 
            yOffset2 = max(yOffset,32)
            #print(imageBottom,xOL,yOL)
            #print(xOffset + 128, yOffset2-32, xOffset + 128 + xOL, yOffset2-32 + h)
            renderImage.paste(imageBottom, (xOffset + 128, yOffset2-32, xOffset + 128 + xOL, yOffset2-32 + h +1 - yOL))


    iid = renderImage.im.id
    idtemp = image.im.id

    matrix.SetImage(iid, 0, 0)

