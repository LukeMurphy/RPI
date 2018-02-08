# -*- coding: utf-8 -*-
from Tkinter import *
 
TITLE = "Drawing a Curve"
WIDTH = 200
HEIGHT = 200
CENTREX = WIDTH/2
CENTREY = HEIGHT/2
NODE_RADIUS = 3
NODE_COLOUR = "red"
LINE_COLOUR= "yellow"
 
formatString = "x: %03d, y: %03d"
 
class Canvassing():
  def __init__(self, parent = None):
    self.canvas = Canvas(width=WIDTH,height=HEIGHT, bg = "blue")
    self.canvas.pack()
    self.readout = Label(text="This is a label")
    self.readout.pack()
    self.canvas.bind("<Motion>",self.onMouseMotion)
    self.line = None
    self.canvas.master.wm_title(string = TITLE)
    self.points = [(CENTREX-WIDTH/4, CENTREY-HEIGHT/4),
            (CENTREX, CENTREY)
            ]
 
  def onMouseMotion(self,event):  # really should rename this as we're doing something different now
    self.readout.config(text = formatString%(event.x, event.y))
    allItems = self.canvas.find_all()
    for i in allItems:  # delete all the items on the canvas
      self.canvas.delete(i)
    # deleting everything every time is inefficient, but it doesn't matter for our purposes.
    for p in self.points:
      self.drawNode(p)
    p = (event.x, event.y)  # now repurpose p to be the point under the mouse
    #self.line = self.canvas.create_line(self.points, p, width=2, fill = LINE_COLOUR)
    self.line = self.canvas.create_line(self.points, p, width=2, fill = LINE_COLOUR, smooth = True)
    self.drawNode(p)
 
  def drawNode(self, p):
      boundingBox = (p[0]-NODE_RADIUS, p[1]+NODE_RADIUS, p[0]+NODE_RADIUS,p[1]-NODE_RADIUS)
      # mixed + and - because y runs from top to bottom not bottom to top
      self.canvas.create_oval(boundingBox, fill=NODE_COLOUR)

 
Canvassing()
mainloop()