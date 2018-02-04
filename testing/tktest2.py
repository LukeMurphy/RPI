# Run tkinter code in another thread

import tkMessageBox
from Tkinter import *
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os, sys, getopt, time, random, math, datetime, textwrap
import ConfigParser, io
from subprocess import call
import threading
global thrd

class App(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)
		self.start()

	def callback(self):
		self.root.quit()

	def run(self):
		self.root = Tk()
		#self.root.protocol("WM_DELETE_WINDOW", self.callback)

		#label = Label(self.root, text="Hello World")
		#label.pack()

		Button(self.root, text="Quit",command=self.root.quit).pack()


		self.cnvs = Canvas(self.root , width=200, height=200)
		self.cnvs.pack()
		self.cnvs.create_rectangle(0, 0, 200,200, fill="blue")
		self.cnvs.update()

		self.root.mainloop()


root = Tk()

def task():
    print("hello")
    root.after(2000, task)  # reschedule event in 2 seconds

root.after(2000, task)
root.mainloop()
