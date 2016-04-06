#!/usr/bin/python
#import modules
from Tkinter import *
import tkMessageBox

import PIL.Image
import PIL.ImageTk
from PIL import Image, ImageTk, ImageDraw, ImageFont

import numpy
import os, sys, getopt, time, random, math, datetime, textwrap
import gc
import ConfigParser, io
import threading
import importlib 
import resource
from subprocess import call

import moviepy.editor as mpy
import moviepy.video.VideoClip as mpv
from moviepy.video import *

from modules import colorutils

global thrd, config
global imageTop,imageBottom,image,config,transWiring

memoryUsage = 0
inited = True
debug = False

class Config:
	def __init__(self):
		self


config = Config()

config.screenHeight =  480
config.screenWidth = 640
config.brightness = 1
config.renderImageFull = PIL.Image.new("RGBA", (config.screenWidth, config.screenHeight))
config.image = PIL.Image.new("RGBA", (config.screenWidth, config.screenHeight))
config.draw = ImageDraw.Draw(config.image)
config.count  = 0


def make_frame(t):
    """ returns a numpy array of the frame at time t """
    global config

    xD = 10
    yD = 10
    boxWidth = 30
    boxHeight = 30
    colorutils.brightness = 1
    clr = colorutils.getRandomRGB()
    config.draw.rectangle((xD,yD,boxWidth+xD,boxHeight+yD), fill=clr )
    #config.image.save("out/img" + str(config.count) + ".png","PNG")
    config.count += 1
    img = config.image
    #exit()
    frame = numpy.array(img)
    #frame = numpy.array(Image.fromarray(numpy.uint8(img)))
    #frame = numpy.reshape(frame, (640,640,3), order='A')
    return img

#clip = mpy.VideoClip(make_frame, duration=10) # 3-second clip
#clip.write_videofile("test.mp4", fps=30, codec="png") # export as video
#clip.write_gif("test.gif", fps=24) # export as GIF



from subprocess import Popen, PIPE

fps = 24
duration = 5
p = Popen(['ffmpeg', '-y', '-f', 'image2pipe', '-vcodec', 'png', '-r', '24', '-i', '-', '-vcodec', 'mpeg4', '-qscale', '5', '-r', '24', 'video.avi'], stdin=PIPE)
for i in range(fps * duration):
    im = Image.new("RGB", (640, 480), (i, 1, 1))
    im  = make_frame(0)
    im.save(p.stdin, 'PNG')
p.stdin.close()
p.wait()










