import time, threading, random
import sys
import os
import subprocess
from tkinter import *
import tkinter as tk

import PIL.Image

from PIL import Image, ImageTk, ImageDraw, ImageFont
from PIL import ImageFilter, ImageChops, ImageEnhance



def new_window(*args):
	global root
	print ("new window")
	window = t.Toplevel(root)
	label = t.Label(window, text="my new window")
	label.pack(side="top", fill="both", padx=10, pady=10)

	cnvs = tk.Canvas(window, width=200, height=200, border=0)
	#self.config.cnvs = self.cnvs
	cnvs.create_rectangle(0, 0, 100, 100, fill="blue")
	cnvs.pack()
	cnvs.place(bordermode='outside', width=200, height=200, x = 10)

	window.mainloop()

def proc1(cnvs):
	while True:
		#print("proc 1")
		'''
		cnvs1.delete("main1")
		cnvs1._image_tk = PIL.ImageTk.PhotoImage(renderImageFull1)
		cnvs1._image_id = cnvs.create_image(10, 10, image=cnvs._image_tk, anchor='nw', tag="main1")
		cnvs1.update()
		draw1.rectangle( (0, 0, 200, 200), fill = 'red')
		'''
		draw1.rectangle( (0, 0, round(random.uniform(10,200)), round(random.uniform(10,200) )), fill = 'green')
		time.sleep(.03)
		#cnvs.create_rectangle(round(random.uniform(0,100)), round(random.uniform(0,100)), 10, 10, fill="green")

def proc2(cnvs):
	while True:
		'''
		cnvs2.delete("main1")
		cnvs2._image_tk = PIL.ImageTk.PhotoImage(renderImageFull2)
		cnvs2._image_id = cnvs.create_image(10, 10, image=cnvs._image_tk, anchor='nw', tag="main1")
		cnvs2.update()
		draw2.rectangle( (0, 0, 200, 200), fill = 'blue')
		'''
		draw2.rectangle( (0, 0, round(random.uniform(10,200)), round(random.uniform(10,200) )), fill = 'yellow')
		#print("proc 2")
		time.sleep(.35)

		#cnvs.create_rectangle(round(random.uniform(0,100)), round(random.uniform(0,100)), 10, 10, fill="yellow")


def cnvsCall0(cnvs):
	while True:
		cnvs.delete("main1")
		cnvs._image_tk = PIL.ImageTk.PhotoImage(renderImageFull0)
		cnvs._image_id = cnvs.create_image(10, 10, image=cnvs._image_tk, anchor='nw', tag="main1")
		renderImageFull0.paste(renderImageFull1, (0,0), renderImageFull1)
		cnvs.update()
		time.sleep(.02)

def cnvsCall(fcu,clr,x,cnvs):
	#cnvs = tk.Canvas(root, width=200, height=200, border=0)
	#self.config.cnvs = self.cnvs
	cnvs.create_rectangle(0, 0, 180, 180, fill=clr)
	#cnvs.pack()
	#cnvs.place(bordermode='outside', width=200, height=200, x = x)
	thrd2 = threading.Thread(target=fcu, kwargs=dict(cnvs=cnvs))
	thrd2.start()
	thrd2.join()


def cnvsThrd0():
	thrd = threading.Thread(target=cnvsCall0, kwargs=dict(cnvs=cnvs1))
	thrd.start()

def cnvsThrd1():
	thrd = threading.Thread(target=cnvsCall, kwargs=dict(fcu=proc1,clr='red', x =0, cnvs=cnvs1))
	thrd.start()

def cnvsThrd2():
	thrd = threading.Thread(target=cnvsCall, kwargs=dict(fcu=proc2,clr='blue', x=30, cnvs=cnvs1))
	thrd.start()

def binder():
	thrd = threading.Thread(target=binderCall)
	thrd.start()

def binderCall():
	#this can be run in another thread
	root.event_generate("<<newwin>>",when="tail")


renderImageFull0 = Image.new("RGBA", (500  , 500))
renderImageFull1 = Image.new("RGBA", (200  , 200))
renderImageFull2 = Image.new("RGBA", (200  , 200))

draw1  = ImageDraw.Draw(renderImageFull1)
draw2  = ImageDraw.Draw(renderImageFull2)

root = tk.Tk()
root.title("Control center")

x = 0
cnvs1 = tk.Canvas(root, width=200, height=200, border=-8)
cnvs1.pack()
cnvs1.place(bordermode='outside', width=200, height=200, x = x)


cnvs1.delete("main1")
cnvs1._image_tk = PIL.ImageTk.PhotoImage(renderImageFull0)
cnvs1._image_id = cnvs1.create_image(10, 10, image=cnvs1._image_tk, anchor='nw', tag="main1")
renderImageFull0.paste(renderImageFull1, (0,0), renderImageFull1)
cnvs1.update()
'''
x = 50
cnvs2 = tk.Canvas(root, width=200, height=200, border=-4)
cnvs2.pack()
cnvs2.place(bordermode='outside', width=200, height=200, x = x)
'''

root.bind("<<newwin>>",new_window)
#root.after(1000, binder)
root.after(100, cnvsThrd0)
root.after(100, cnvsThrd1)
#root.after(200, cnvsThrd2)


root.mainloop()

