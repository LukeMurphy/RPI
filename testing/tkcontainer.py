import tkMessageBox
from Tkinter import *
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os, sys, getopt, time, random, math, datetime, textwrap
import ConfigParser, io
from subprocess import call
import threading
global thrd


#from cntrlscripts import off_signal
#from modules import scroll
#from modules import colorutils
import gc


class App():

	xPos = 4
	yPos = 4

	vx = 2
	vy = 3

	## Create a blank dummy object container for now
	config = type('', (object,), {})()
	#scrollObj = scroll

	def __init__(self):
		self.root = Tk()
		#self.root.overrideredirect(1)
		
		self.frame = Frame(self.root, width=128, height=128,
						   borderwidth=0, padx=0, pady=0)
		self.frame.pack_propagate(False)
		self.frame.pack()
		
		''''''
		Button(self.root, text="Quit",command=self.root.quit).pack()

		
		self.config.screenWidth = 200
		self.config.screenHeight =  200

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

	def startAnimation(self) :
		try :
			while True :
				self.animation()
		except TclError, details:
			print(details)
			pass
			exit()

	def animation(self) :
		r = 200
		g = 0
		b = 0
		while True:


			self.yPos += self.vy
			self.xPos += self.vx

			if(self.yPos > self.config.screenWidth or self.yPos <0) : self.vy *= -1
			if(self.xPos > self.config.screenHeight or self.xPos <0) : self.vx *= -1

			#cnvs.create_line(0, 0, 200, 100)
			#cnvs.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))
			self.cnvs.create_rectangle(self.xPos ,self.yPos, self.xPos+30, self.yPos+29, fill="red", outline="#00FF00")

			self.cnvs.update_idletasks()

			gc.collect()
			time.sleep(.02)
		#self.run()


app = App()
app.root.mainloop()
