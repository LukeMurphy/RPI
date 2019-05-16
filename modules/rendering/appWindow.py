import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont
from PIL import ImageFilter, ImageChops, ImageEnhance
import random
import time
import threading

from modules.filters import *

#from Tkinter import *
#import tkMessageBox
#import PIL.Image
#import PIL.ImageTk
#import gc, os

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''



class AppWindow:
	def __init__(self, masterConfig):
		print("** App Window Initialized ** ")
		self.masterConfig = masterConfig

	def setUp(self):
		#global root
		#global root, canvasOffsetX, canvasOffsetY, buff, config
		self.memoryUsage = 0
		self.debug = False
		self.counter = 0

		self.canvasOffsetX = 4
		self.canvasOffsetY = 7
		self.buff  =  8
		gc.enable()
		if(self.masterConfig.MID == "studio-mac") : 
			self.masterConfig.path = "./"
			windowOffset = [1900,20]
			windowOffset = [2560,24]
			windowOffset = [self.masterConfig.windowXOffset, self.masterConfig.windowYOffset]
			#windowOffset = [4,45]
		else :
			windowOffset = [-1,13]
			windowOffset = [self.masterConfig.windowXOffset, self.masterConfig.windowYOffset]

		# -----> this is somewhat arbitrary - just to get the things aligned
		# after rotation
		#if(config.rotation == 90) : canvasOffsetY = -25

		self.root = tk.Tk()
		w = self.masterConfig.screenWidth
		h = self.masterConfig.screenHeight
		x = windowOffset[0]
		y = windowOffset[1]

		self.root.overrideredirect(False)
		self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
		#root.protocol("WM_DELETE_WINDOW", on_closing)
		#Button(root, text="Quit", command=root.quit).pack(side="bottom")

	def run(self):
		self.root.lift()
		self.root.call('wm', 'attributes', '.', '-topmost', '1')
		self.root.mainloop()
		
		'''
		while True:
			self.root.update_idletasks()
			self.root.update()
		'''

