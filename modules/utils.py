import time
import random
import math

screenWidth =  128
screenHeight = 32

#scroll speed and steps per cycle
scrollSpeed = 0.01
steps = 6

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
