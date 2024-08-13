import random
import threading
import time
import tkinter as tk

from modules.filters import *
from PIL import (
    Image,
    ImageChops,
    ImageDraw,
    ImageEnhance,
    ImageFilter,
    ImageFont,
    ImageTk,
)

# from Tkinter import *
# import tkMessageBox
# import PIL.Image
# import PIL.ImageTk
# import gc, os

"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""


class AppWindow:
    '''[summary]
    
    [description]
    
    Variables:
        ) {[type]} -- [description]
    '''
    def __init__(self, masterConfig):
        print("** App Window Initialized ** ")
        self.masterConfig = masterConfig

    def setUp(self):
        # global root
        # global root, canvasOffsetX, canvasOffsetY, buff, config
        self.memoryUsage = 0
        self.debug = False
        self.counter = 0

        self.canvasOffsetX = 4
        self.canvasOffsetY = 7
        self.buff = 8
        gc.enable()
        if self.masterConfig.MID == "studio-mac":
            self.masterConfig.path = "./"
            windowOffset = [1900, 20]
            windowOffset = [2560, 24]
            # windowOffset = [
            # 	self.masterConfig.windowXOffset,
            # 	self.masterConfig.windowYOffset,
            # ]
            # windowOffset = [4,45]
        else:
            windowOffset = [-1, 13]
            # windowOffset = [
            # 	self.masterConfig.windowXOffset,
            # 	self.masterConfig.windowYOffset,
            # ]

        # -----> this is somewhat arbitrary - just to get the things aligned
        # after rotation
        # if(config.rotation == 90) : canvasOffsetY = -25

        self.root = tk.Tk()
        # w = self.masterConfig.screenWidth
        # h = self.masterConfig.screenHeight
        w = 100
        h = 100
        x = windowOffset[0]
        y = windowOffset[1]

        self.root.overrideredirect(False)
        self.root.geometry("%dx%d+%d+%d" % (w, h, x, y))
        self.root.lift()


    '''[summary]
    
    [description]
    '''
    def createMainCanvas(self):
        self.masterConfig.root = self.root
        
        self.masterConfig.screenWidth = 250
        self.masterConfig.screenHeight = 250
        self.masterConfig.canvasOffsetX = 250
        self.masterConfig.canvasOffsetY = 250

        self.masterConfig.cnvs = tk.Canvas(
            self.root,
            width=self.masterConfig.screenWidth + self.buff,
            height=self.masterConfig.screenHeight + self.buff,
            border=0,
        )

        self.masterConfig.cnvs.create_rectangle(
            0, 0, self.masterConfig.screenWidth + self.buff, self.masterConfig.screenHeight + self.buff, fill="black"
        )
        #config.cnvs.pack()
        self.masterConfig.cnvs.place(
            bordermode="outside",
            width=self.masterConfig.screenWidth + self.buff,
            height=self.masterConfig.screenHeight + self.buff,
        )
        # root.protocol("WM_DELETE_WINDOW", on_closing)
        # Button(root, text="Quit", command=root.quit).pack(side="bottom")
        self.masterConfig.renderImageFull  = PIL.Image.new("RGBA", (self.masterConfig.screenWidth, self.masterConfig.screenHeight))
        self.masterConfig.tempImage = ImageTk.PhotoImage(self.masterConfig.renderImageFull)
        self.masterConfig.cnvs._image_id = self.masterConfig.cnvs.create_image(self.masterConfig.canvasOffsetX, self.masterConfig.canvasOffsetY, image=self.masterConfig.tempImage, anchor="nw", tag="mainer"
    )


    def startWork(self, work):
        # global config, work, root, counter
        global counter

        ### Putting the animation on its own thread
        ### Still throws and error when manually closed though...

        print("Starting threads")


        '''
        try:
            threadRunning = threading.Thread(target=work.runWork)
            print(threadRunning)
            threadRunning.start()
            threadRunning.join()
        except Exception as e:
            print("DID NOT WORK")
            print(str(e))
        '''
        self.activeWork = work

        try:
            
            #t = threading.Thread.__init__(work.runWork())
            t = threading.Thread(target=work.runWork)
            work.threadRef = t
            t.start()
            t.join()

        except tk.TclError as details:
            print(details)
            pass
            #exit()


    def run(self):
        self.root.call("wm", "attributes", ".", "-topmost", "1")
        self.root.mainloop()

        """
        while True:
            self.root.update_idletasks()
            self.root.update()
        """
