import os
import random
import subprocess
import sys
import threading
import time
import tkinter as tk
from tkinter import *

import PIL.Image
from PIL import (
	Image,
	ImageChops,
	ImageDraw,
	ImageEnhance,
	ImageFilter,
	ImageFont,
	ImageTk,
)


def print_time(args):
	print("From print_time", time.time(), args)


def print_some_times():
	print("time one", time.time())
	Timer(2, print_time, ()).start()
	Timer(4, print_time, ()).start()
	# time.sleep(8)  # sleep while time-delay events execute
	print("time two", time.time())


def setInterval(func, sec, args):
	def func_wrapper():
	    func(args)
	    setInterval(func, sec, args)

	t = threading.Timer(sec, func_wrapper)
	t.start()
	return t


# print_some_times()


def Init():

	n = setInterval(print_time, 0.5, "fiver")
	ns = setInterval(print_time, 0.1, ".1er")


def run():
	root = tk.Tk()
	w = 600
	h = 500
	foo = Canvas
	Init()
	root.mainloop()


# run()

# import Queue

# q = Queue.Queue()

# Run tkinter code in another thread


class App(threading.Thread):
	def __init__(self):
	    threading.Thread.__init__(self)
	    self.start()

	def callback(self):
	    self.root.quit()

	def run(self):
	    self.root = tk.Tk()
	    self.root.protocol("WM_DELETE_WINDOW", self.callback)

	    label = tk.Label(self.root, text="Hello World")
	    label.pack()

	    self.root.mainloop()


app = App()
print("Now we can continue running code while mainloop runs!")
