# Run tkinter code in another thread

import ConfigParser
import datetime
import getopt
import io
import math
import os
import random
import sys
import textwrap
import threading
import time
from subprocess import call
from Tkinter import *

import tkMessageBox
from PIL import Image, ImageDraw, ImageFont, ImageTk

global thrd


class App(threading.Thread):
	def __init__(self):
	    threading.Thread.__init__(self)
	    self.start()

	def callback(self):
	    self.root.quit()

	def run(self):
	    self.root = Tk()
	    # self.root.protocol("WM_DELETE_WINDOW", self.callback)

	    # label = Label(self.root, text="Hello World")
	    # label.pack()

	    Button(self.root, text="Quit", command=self.root.quit).pack()

	    self.cnvs = Canvas(self.root, width=200, height=200)
	    self.cnvs.pack()
	    self.cnvs.create_rectangle(0, 0, 200, 200, fill="blue")
	    self.cnvs.update()

	    self.root.mainloop()


root = Tk()


def task():
	print("hello")
	root.after(2000, task)  # reschedule event in 2 seconds


root.after(2000, task)
root.mainloop()
