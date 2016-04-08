from Tkinter import *
import tkMessageBox
import PIL.Image
import PIL.ImageTk
from PIL import Image, ImageTk, ImageDraw, ImageFont
from PIL import ImageFilter
import numpy

memoryUsage = 0
debug = False

def setUp():

	if(config.MID == "studio-mac") : 
		config.path = "./"
		windowOffset = [38,38]
	else :
		windowOffset = [4,4]

	root = Tk()
	w = config.screenWidth + 8
	h = config.screenHeight  + 8
	x = windowOffset[0]
	y = windowOffset[1]

	#root.overrideredirect(True)
	root.geometry('%dx%d+%d+%d' % (w, h, x, y))

	cnvs = Canvas(root, width=config.screenWidth + 4, height=config.screenHeight + 4)
	config.cnvs = cnvs
	config.cnvs.pack()
	config.cnvs.create_rectangle(0, 0, config.screenWidth + 8, config.screenHeight + 8, fill="black")
	
	tempImage = PIL.ImageTk.PhotoImage(config.renderImageFull)
	config.cnvs._image_id = config.cnvs.create_image(3, 3, image=tempImage, anchor='nw')

	#config.cnvs.update()
	config.cnvs.update_idletasks()

	root.after(0, startWork)
	root.mainloop() 

def startWork(*args) :
	global config, work
	while True :
		work.runWork()


def render( imageToRender,xOffset,yOffset,w=128,h=64,nocrop=False, overlayBottom=False) :
	global memoryUsage
	global config, debug

	# Render to canvas
	# This needs to be optomized !!!!!!
	#*******************************************************************************
	#*******************************************************************************
	#*******************************************************************************

	#print(imageToRender.size,xOffset,yOffset)


	if(config.useFilters) :
		'''------------------------------------------------------------------------'''
		'''              FILTERS                                                   '''

		''' ugly hippy ...
		config.image = config.image.filter(ImageFilter.GaussianBlur(radius=1))
		config.image = config.image.filter(ImageFilter.UnsharpMask(radius=20, percent=150,threshold=2))
		config.renderImageFull.paste(config.image, (xOffset, yOffset))
		'''
		im1 = config.image.filter(ImageFilter.GaussianBlur(radius=0))
		im2 = im1.filter(ImageFilter.UnsharpMask(radius=20, percent=100,threshold=2))

		'''             Paste to Render                                       '''

		config.renderImageFull.paste(im2, (xOffset, yOffset))

		'''------------------------------------------------------------------------'''

	else :
		config.renderImageFull.paste(config.image, (xOffset, yOffset))

	## For testing ...
	#draw1  = ImageDraw.Draw(config.renderImageFull)
	#draw1.rectangle((xOffset+32,yOffset,xOffset + 32+ 32, yOffset +32), fill=(255,0,0))

	config.cnvs._image_tk = ImageTk.PhotoImage(config.renderImageFull)
	config.cnvs._image_id = config.cnvs.create_image(3, 3, image=config.cnvs._image_tk, anchor='nw')
	config.cnvs.update()


	'''

	mem = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)/1024/1024

	if mem > memoryUsage and debug :
		memoryUsage = mem 
		print 'Memory usage: %s (mb)' % str(memoryUsage)
	'''

	#*******************************************************************************
	#*******************************************************************************
	#*******************************************************************************