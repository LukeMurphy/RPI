import tkMessageBox
from Tkinter import *
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os, sys, getopt, time, random, math, datetime, textwrap
import ConfigParser, io
from subprocess import call
import threading
global thrd


from cntrlscripts import off_signal
from modules import scroll
from modules import colorutils


class App():

    xPos = 4
    yPos = 4

    vx = 2
    vy = 3

    ## Create a blank dummy object container for now
    config = type('', (object,), {})()
    scrollObj = scroll

    def __init__(self):
        self.root = Tk()
        #self.root.overrideredirect(1)
        '''
        self.frame = Frame(self.root, width=128, height=128,
                           borderwidth=0, padx=0, pady=0)
        self.frame.pack_propagate(False)
        self.frame.pack()
        '''
        '''
        self.bQuit = Button(self.root, text="Quit",
                            command=self.root.quit)
        self.bQuit.pack(padx=1,pady=6)
        '''

        baseconfig = ConfigParser.ConfigParser()
        baseconfig.read('./config.cfg')

        usingHub = False
        try:
            usingHub = bool(baseconfig.getboolean("config", 'useHub'))
        except :
            pass


        self.config.Image = Image
        self.config.ImageDraw = ImageDraw
        self.config.ImageFont = ImageFont

        self.config.screenHeight = int(baseconfig.get("config", 'screenHeight'))
        self.config.screenWidth =  int(baseconfig.get("config", 'screenWidth'))
        self.config.image = Image.new("RGBA", (self.config.screenWidth, self.config.screenHeight))
        self.config.renderImageA = Image.new("RGBA", (self.config.screenWidth + 8, self.config.screenHeight + 8))
        self.config.draw = ImageDraw.Draw(self.config.image)
        self.config.render = self.render

        self.config.tileSize = (int(baseconfig.get("config", 'tileSizeHeight')),int(baseconfig.get("config", 'tileSizeWidth')))
        self.config.rows = int(baseconfig.get("config", 'rows'))
        self.config.cols = int(baseconfig.get("config", 'cols'))

        self.config.actualScreenWidth  = int(baseconfig.get("config", 'actualScreenWidth'))
        self.config.useMassager = bool(baseconfig.getboolean("config", 'useMassager'))
        self.config.renderImage = Image.new("RGBA", (self.config.actualScreenWidth, 32))
        self.config.brightness =  float(baseconfig.get("config", 'brightness'))
        self.config.path = baseconfig.get("config", 'path')
        self.config.transWiring = bool(baseconfig.getboolean("config", 'transWiring'))

        self.scrollObj.config = self.config
        self.scrollObj.fontSize = int(baseconfig.get("scroll", 'fontSize'))
        self.scrollObj.vOffset = int(baseconfig.get("scroll", 'vOffset'))
        self.scrollObj.scrollSpeed = float(baseconfig.get("scroll", 'scrollSpeed'))
        self.scrollObj.stroopSpeed = float(baseconfig.get("scroll", 'stroopSpeed'))
        self.scrollObj.stroopSteps = float(baseconfig.get("scroll", 'stroopSteps'))
        self.scrollObj.stroopFontSize = int(baseconfig.get("scroll", 'stroopFontSize'))

        #self.cnvs._image_tk = ImageTk.PhotoImage(self.config.image)
        #self.cimage = ImageTk.PhotoImage("RGB", (132,132)) 
        #self.cnvs._image_id = self.cnvs.create_image(0, 0, image=self.cnvs._image_tk, anchor='nw')
        #self.cnvs._image_id = self.cnvs.create_image(0, 0, image=self.cimage, anchor='nw')

        #self.fontt = self.config.ImageFont.truetype(self.config.path  + '/fonts/freefont/FreeSerifBold.ttf',20)

        self.cnvs = Canvas(self.root , width=self.config.screenWidth, height=self.config.screenHeight)
        self.cnvs.pack()
        self.cnvs.create_rectangle(0, 0, self.config.screenWidth, self.config.screenHeight, fill="black")
        self.cnvs.update()


        self.root.after(0, self.startAnimation)
        self.root.mainloop()     

    def render(self, imageToRender,xOffset,yOffset,w=128,h=64,nocrop=False, overlayBottom=False) :
        # Render to canvas
        self.config.renderImageA.paste(imageToRender, (xOffset, yOffset + 2))
        temp = ImageTk.PhotoImage(self.config.renderImageA)
        self.cnvs._image_id = self.cnvs.create_image(0, 0, image=temp, anchor='nw')
        self.cnvs.update()

    def stroopSequence(self) :
        directionStr = self.getDirection()
        #directionStr = "Bottom"
        if(random.random() > .7) :self.scrollObj.stroop("YELLOW",(255,0,225),directionStr)
        if(random.random() > .7) :self.scrollObj.stroop("VIOLET",(230,225,0),directionStr)
        if(random.random() > .7) :self.scrollObj.stroop("RED",(0,255,0),directionStr)
        if(random.random() > .7) :self.scrollObj.stroop("BLUE",(225,100,0),directionStr)
        if(random.random() > .7) :self.scrollObj.stroop("GREEN",(255,0,0),directionStr)
        if(random.random() > .7) :self.scrollObj.stroop("ORANGE",(0,0,200),directionStr)

    def getDirection(self) :
        d = int(random.uniform(1,4))
        direction = "Left"
        if (d == 1) : direction = "Left"
        if (d == 2) : direction = "Right"
        if (d == 3) : direction = "Bottom"
        return direction

    def startAnimation(self) :
        try :
            while True :
                self.runStroop()
        except TclError, details:
            print(details)
            pass
            exit()


    def runStroop(self) :
        numRuns = int(random.uniform(2,6))
        numRuns =  1
        for i in range(0,numRuns) : 
            if(self.scrollObj.opticalOpposites) : 
                self.scrollObj.opticalOpposites = False
            else : 
                self.scrollObj.opticalOpposites = True
            self.stroopSequence()

    def animation(self) :
        r = 200
        g = 0
        b = 0
        while True:
            self.draw.rectangle((self.xPos, self.yPos, 20 + self.xPos, 20 + self.yPos ),  outline=(r,g,b), fill=(0,0,0))

            self.yPos += self.vy
            self.xPos += self.vx

            if(self.yPos > 64 or self.yPos <0) : self.vy *= -1
            if(self.xPos > 128 or self.xPos <0) : self.vx *= -1

            #cnvs.create_line(0, 0, 200, 100)
            #cnvs.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))
            #cnvs.create_rectangle(50, 25, 150, 75, fill="blue")


            self.cnvs._image_tk = ImageTk.PhotoImage(self.image)
            self.cnvs._image_id = self.cnvs.create_image(0, 0, image=self.cnvs._image_tk, anchor='nw')
            self.cnvs.update()
            time.sleep(.02)
        #self.run()


app = App()
#app.root.mainloop()
