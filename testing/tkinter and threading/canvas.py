# -*- coding: utf-8 -*-
import random
import threading
import time
import tkinter as tk
from PIL import (
	Image,
	ImageChops,
	ImageDraw,
	ImageEnhance,
	ImageFilter,
	ImageFont,
	ImageTk,
)

TITLE = "Drawing a Curve"
WIDTH = 200
HEIGHT = 200
CENTREX = WIDTH / 2
CENTREY = HEIGHT / 2
NODE_RADIUS = 3
NODE_COLOUR = "red"
LINE_COLOUR = "yellow"

formatString = "x: %03d, y: %03d"


class Canvassing:
	def __init__(self, parent=None):
	    self.canvas = tk.Canvas(width=WIDTH, height=HEIGHT, bg="blue")
	    self.canvas.pack()
	    self.readout = tk.Label(text="This is a label")
	    self.readout.pack()
	    self.canvas.bind("<Motion>", self.onMouseMotion)
	    self.line = None
	    self.canvas.master.wm_title(string=TITLE)
	    self.points = [(CENTREX - WIDTH / 4, CENTREY - HEIGHT / 4), (CENTREX, CENTREY)]
	    self.canvas.mainloop()

	def onMouseMotion(self, event):  # really should rename this as we're doing something different now
	    self.readout.config(text=formatString % (event.x, event.y))
	    allItems = self.canvas.find_all()

	    # deleting everything every time is inefficient, but it doesn't matter for our purposes.
	    for i in allItems:  # delete all the items on the canvas
	        self.canvas.delete(i)
	    
	    # self.line = self.canvas.create_line(self.points, p, width=2, fill = LINE_COLOUR)
	    for p in self.points:
	        self.drawNode(p)
	    
	    # now repurpose p to be the point under the mouse
	    p = (event.x, event.y)  


	    self.line = self.canvas.create_line(
	        self.points, p, width=2, fill=LINE_COLOUR, smooth=True
	    )
	    
	    self.drawNode(p)

	def drawNode(self, p):
	    boundingBox = (
	        p[0] - NODE_RADIUS,
	        p[1] + NODE_RADIUS,
	        p[0] + NODE_RADIUS,
	        p[1] - NODE_RADIUS,
	    )
	    
	    # mixed + and - because y runs from top to bottom not bottom to top
	    self.canvas.create_oval(boundingBox, fill=NODE_COLOUR)


c =  Canvassing()
