#####
#import Image
#import ImageDraw
import time
import random
#from rgbmatrix import Adafruit_RGBmatrix
import math
import messenger

def explosion():
        global config

        if(config.useMassager == True) : 
                messenger.soliloquy(True)

        #image = Image.new("RGBA", (32, 32))
        #draw  = ImageDraw.Draw(image)

        ## Uses the same "global" image to draw to
        image = config.image
        #config.matrix.SetImage(image.im.id, 0,0)
        particles = []
        # Traces / no traces
        traces = False
        if(random.random() > .98) : traces = True
        # Number of sparks
        p = int(50 + (random.uniform(10,90)))
        angle = 2 * math.pi/p

        # initial center position
        x = int(random.random()*config.screenWidth)
        y = int(random.random()*16)
        
        for n in range (0, p) :
                # variation in initial velocity
                f = random.random() * 4
                vx = math.cos(angle * n) * f
                vy = math.sin(angle * n) * f
                r = int(random.uniform(0,255))
                g = int(random.uniform(0,255))
                b = int(random.uniform(0,255))
                particles.append({'id':n,'xpos':x,'ypos':y,'vx':vx,'vy':vy, 'c':[r,g,b]})

        for i in range (0,50) :
                if(traces == False) : config.matrix.Clear()
                #config.matrix.SetImage(config.image.im.id, 0,0)
                if(random.random() > .98) : traces = True
                decr = 20
                decr = int(random.uniform(1,15))        

                for q in range (0, p) :
                        ref = particles[q]
                        ref['xpos'] = ref['vx'] + ref['xpos']
                        ref['ypos'] = ref['vy'] + ref['ypos']

                        # deacelleration
                        ref['vy'] = ref['vy']* .9
                        ref['vx'] = ref['vx']* .9

                        # pseudo gravity
                        ref['vy'] = ref['vy'] + .1

                        particles[q]['c'][0] = particles[q]['c'][0] - decr
                        particles[q]['c'][1] = particles[q]['c'][1] - decr
                        particles[q]['c'][2] = particles[q]['c'][2] - decr

                        if(particles[q]['c'][0] <= 0) : particles[q]['c'][0] = 0
                        if(particles[q]['c'][1] <= 0) : particles[q]['c'][1] = 0
                        if(particles[q]['c'][2] <= 0) : particles[q]['c'][2] = 0

                        r = particles[q]['c'][0]
                        g = particles[q]['c'][1]
                        b = particles[q]['c'][2]

                        if(random.random() > .9) :
                                r = 220
                                g = 220
                                b = 255

                        #if (q ==0) : print (particles[q]['c'][0])
                        xDisplayPos = ref['xpos']
                        yDisplayPos = ref['ypos']

                        if(xDisplayPos > config.screenWidth) :
                                xDisplayPos += config.screenWidth

                        if(yDisplayPos > 32 and yDisplayPos <64) :
                                yDisplayPos -=32
                                xDisplayPos += config.screenWidth
                        if(yDisplayPos > 64) :
                                yDisplayPos -=64
                                xDisplayPos += config.screenWidth*2

                        config.matrix.SetPixel(int(xDisplayPos),int(yDisplayPos),r,g,b)
                        
                time.sleep(0.015)
        if(random.random() > .1) : explosion()

def burst(a=10) :
        config.matrix.Clear()
        count = 0
        stars = False
        p = 50
        actualScreenWidth = config.tileSize[1]*config.cols*config.rows
        if(random.random() > .5):
                        stars = True
                        p = 20
        while (count < a) :
                        config.matrix.Clear()
                        for n in range(0,p) :
                                        r = int(random.uniform(0,255))
                                        g = int(random.uniform(0,255))
                                        b = int(random.uniform(0,255))
                                        x = int(random.random()*actualScreenWidth)
                                        y = int(random.random()*31)

                                        rn = random.random()

                                        if(rn > .3 and rn  < .6) :
                                                        r = 0
                                                        g = 0
                                                        b = 200
                                        elif (rn > .6 and rn < .9) :
                                                        r = 255
                                                        g = 0
                                                        b = 0
                                        else :
                                                        True

                                        config.matrix.SetPixel(x,y,r,g,b)
                                        if(stars) :
                                                        config.matrix.SetPixel(x+1,y,r,g,b)
                                                        config.matrix.SetPixel(x-1,y,r,g,b)
                                                        config.matrix.SetPixel(x,y+1,r,g,b)
                                                        config.matrix.SetPixel(x,y-1,r,g,b)
                        time.sleep(.08)
                        count += 1
        if(random.random() > .5) : burst()


def glitch(a=10) :
        count = 0
        while (count < a) :
                yStart = int(random.uniform(0,16))
                for n in range(0,30) :
                        r = int(random.uniform(0,255))
                        g = int(random.uniform(0,255))
                        b = int(random.uniform(0,255))
                        x = int(random.random()*config.screenWidth)

                        yEnd = yStart + int(random.uniform(0,16))
                        y = int(random.uniform(yStart,yEnd))

                        lineLength = int(random.random()*30)
                        for xpos in range (0, lineLength) :
                                config.matrix.SetPixel(x + xpos ,y,r,g,b)

                drawBlanks()
                time.sleep(.01)
                count += 1
        time.sleep(int(random.uniform(.1,4)))
        #exit()


# ################################################## #

blankPixels = []
cols = int(random.uniform(2,20))
rows = int(random.uniform(2,20))
def setBlanks() :
        #print("Setting Blanks")
        global config,blankPixels,cols,rows
        blankPixels = []
        count = 0
        # scatter horizontally
        for n in range (0, 10) :
                x = int(random.random()*config.actualScreenWidth)
                y = int(random.random()*32)
                blankPixels.append((x,y))
                if(random.random() > .9):
                        cols = int(random.uniform(2,20))
                        rows = int(random.uniform(2,20))

                        for ii in range(0,rows):
                                blankPixels.append((x,y + ii))
                                for i in range (0,cols) :
                                        blankPixels.append((x+i,y + ii))
                

def drawBlanks() :
        global config, blankPixels, rows, cols   
        if (len(blankPixels) == 0): setBlanks()
        count = 0
        blankNum=len(blankPixels)
             
        for n in range (0, blankNum) :
                config.matrix.SetPixel(blankPixels[n][0],blankPixels[n][1],0,0,0)
        


