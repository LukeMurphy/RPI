import importlib
import os
import random
import subprocess
import sys
import threading
import time
import tkinter as tk
from importlib import util
from tkinter import *

import PIL.Image
import proc1file as workDef2
import procfileclass as work
from PIL import (
    Image,
    ImageChops,
    ImageDraw,
    ImageEnhance,
    ImageFilter,
    ImageFont,
    ImageTk,
)

sys.path.append("./")


def new_window(*args):
	global root
	print("new window")
	window = t.Toplevel(root)
	label = t.Label(window, text="my new window")
	label.pack(side="top", fill="both", padx=10, pady=10)

	cnvs = tk.Canvas(window, width=200, height=200, border=0)
	# self.config.cnvs = self.cnvs
	cnvs.create_rectangle(0, 0, 100, 100, fill="blue")
	cnvs.pack()
	cnvs.place(bordermode="outside", width=200, height=200, x=10)
	window.mainloop()


def proc1(**kwargs):
	while True:
	    draw1.rectangle((0, 0, 250, 500), fill="red")
	    draw1.rectangle(
	        (0, 0, round(random.uniform(10, 100)), round(random.uniform(10, 200))),
	        fill="green",
	    )
	    time.sleep(0.2)


def proc2(**kwargs):
	while True:
	    draw2.rectangle((100, 0, 250, 500), fill="red")
	    draw2.rectangle(
	        (
	            100,
	            0,
	            100 + round(random.uniform(10, 100)),
	            round(random.uniform(10, 200)),
	        ),
	        fill="yellow",
	    )
	    time.sleep(0.02)


def cnvsCall0():
	while True:
	    # cnvs1.delete("main1")
	    draw0.rectangle((0, 0, 500, 500), fill="red")
	    renderImageFull0.paste(renderImageFull1, (0, 0), renderImageFull1)
	    renderImageFull0.paste(renderImageFull2, (0, 0), renderImageFull2)
	    cnvs1._image_tk = PIL.ImageTk.PhotoImage(renderImageFull0)
	    cnvs1._image_id = cnvs1.create_image(
	        10, 10, image=cnvs1._image_tk, anchor="nw", tag="main1"
	    )
	    cnvs1.update()
	    time.sleep(0.02)


def cnvsCall(fcu, clr, x, cnvs):
	# cnvs = tk.Canvas(root, width=200, height=200, border=0)
	# self.config.cnvs = self.cnvs
	cnvs.create_rectangle(0, 0, 180, 180, fill=clr)
	# cnvs.pack()
	# cnvs.place(bordermode='outside', width=200, height=200, x = x)
	thrd2 = threading.Thread(target=fcu, kwargs=dict(cnvs=cnvs))
	thrd2.start()
	thrd2.join()


# Udates the canvas
def cnvsThrd0():
	print("Starting cnvsThrd0")
	t0 = threading.Thread.__init__(cnvsCall0())
	t0.start()
	# thrd = threading.Thread(target=cnvsCall0)
	# thrd.start()


# Draws
def cnvsThrd1():
	print("Starting cnvsThrd1 \n" + str(p1.__dict__))
	# t1  = threading.Thread.__init__(proc1())
	# t1.start()

	thrd = threading.Thread(target=workDef1.proc1)
	# thrd = threading.Thread(target=p1.proc1)
	thrd.start()


# Draws
def cnvsThrd2():
	print("Starting cnvsThrd2 \n" + str(p2.__dict__))
	# t2  = threading.Thread.__init__(proc2())
	# t2.start()
	# kwargs=dict(fcu=proc2,clr='blue', x=30
	# thrd = threading.Thread(target=proc2)

	thrd = threading.Thread(target=workDef2.proc1)
	# thrd = threading.Thread(target=p2.proc1)
	thrd.start()


def startThreads():
	print("")
	cnvsThrd1()
	cnvsThrd2()
	cnvsThrd0()


"""
def binder():
	thrd = threading.Thread(target=binderCall)
	thrd.start()

def binderCall():
	#this can be run in another thread
	root.event_generate("<<newwin>>",when="tail")
"""

renderImageFull0 = Image.new("RGBA", (500, 500))
renderImageFull1 = Image.new("RGBA", (500, 500))
renderImageFull2 = Image.new("RGBA", (500, 500))

draw0 = ImageDraw.Draw(renderImageFull0)
draw1 = ImageDraw.Draw(renderImageFull1)
draw2 = ImageDraw.Draw(renderImageFull2)

p1 = work.Proc(drawRef=draw1, xpos=0, delay=0.2, clr="blue")
p2 = work.Proc(drawRef=draw2, xpos=100, delay=0.01, clr="green")

workDef1.drawRef = draw1

workDef2.drawRef = draw2
workDef2.clr = "blue"
workDef2.delay = 0.01
workDef2.xpos = 100

root = tk.Tk()
root.title("Control center")

x = -4
cnvs1 = tk.Canvas(root, width=400, height=400, border=0)
cnvs1.pack()
cnvs1.place(bordermode="outside", width=200, height=200, x=x)


cnvs1.delete("main1")
cnvs1._image_tk = PIL.ImageTk.PhotoImage(renderImageFull0)
cnvs1._image_id = cnvs1.create_image(
	10, 10, image=cnvs1._image_tk, anchor="nw", tag="main1"
)
cnvs1.update()

"""
x = 50
cnvs2 = tk.Canvas(root, width=200, height=200, border=-4)
cnvs2.pack()
cnvs2.place(bordermode='outside', width=200, height=200, x = x)
"""

root.bind("<<newwin>>", new_window)
# root.after(1000, binder)
root.after(100, startThreads)
root.mainloop()
