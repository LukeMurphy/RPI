# Run tkinter code in another thread

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
import tkinter as tk


from PIL import Image, ImageDraw, ImageFont, ImageTk

global thrd


class App():
	def __init__(self):
		#threading.Thread
		#threading.Thread.__init__(self)
		#self.start()
		pass

	def callback(self):
		self.root.quit()

	def run(self):
		self.root = tk.Tk()
		# self.root.protocol("WM_DELETE_WINDOW", self.callback)

		# label = Label(self.root, text="Hello World")
		# label.pack()

		tk.Button(self.root, text="Quit", command=self.root.quit).pack()

		self.cnvs = tk.Canvas(self.root, width=200, height=200)
		self.cnvs.pack()
		self.cnvs.create_rectangle(0, 0, 200, 200, fill="blue")
		self.cnvs.update()
		self.root.mainloop()

	def render(self):
		#self.cnvs.delete("main1")
		self.cnvs._image_tk = PIL.ImageTk.PhotoImage(self.renderImageFull)
		self.cnvs._image_id = self.cnvs.create_image(
			self.config.canvasOffsetX,
			self.config.canvasOffsetY,
			image=self.cnvs._image_tk,
			anchor="nw",
			tag="main1",
		)
		self.cnvs.update()


'''
root = tk.Tk()

def task():
	print("hello")
	root.after(2000, task)  # reschedule event in 2 seconds


root.after(2000, task)
root.mainloop()
'''


a = App()
a.run()