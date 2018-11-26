import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont
from PIL import ImageFilter, ImageChops, ImageEnhance
import random
import time
import threading

from modules.filters import *

#from Tkinter import *
#import tkMessageBox
#import PIL.Image
#import PIL.ImageTk
#import gc, os

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

global root
memoryUsage = 0
debug = False
counter = 0

canvasOffsetX = 4
canvasOffsetY = 7
buff  =  8

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def setUp():
	global root, canvasOffsetX, canvasOffsetY, buff, config
	gc.enable()
	if(config.MID == "studio-mac") : 
		config.path = "./"
		windowOffset = [1900,20]
		windowOffset = [2560,24]
		windowOffset = [config.windowXOffset, config.windowYOffset]
		#windowOffset = [4,45]
	else :
		windowOffset = [-1,13]
		windowOffset = [config.windowXOffset, config.windowYOffset]

	# -----> this is somewhat arbitrary - just to get the things aligned
	# after rotation
	#if(config.rotation == 90) : canvasOffsetY = -25

	root = tk.Tk()
	w = config.screenWidth + buff
	h = config.screenHeight  + buff
	x = windowOffset[0]
	y = windowOffset[1]

	root.overrideredirect(False)
	root.geometry('%dx%d+%d+%d' % (w, h, x, y))
	#root.protocol("WM_DELETE_WINDOW", on_closing)

	#Button(root, text="Quit", command=root.quit).pack(side="bottom")
	root.lift()

	config.root = root

	cnvs = tk.Canvas(root, width=config.screenWidth + buff, height=config.screenHeight + buff)
	config.cnvs = cnvs
	config.cnvs.pack()
	config.cnvs.create_rectangle(0, 0, config.screenWidth + buff, config.screenHeight + buff, fill="black")
	
	#tempImage = PIL.ImageTk.PhotoImage(config.renderImageFull)
	tempImage = ImageTk.PhotoImage(config.renderImageFull)
	config.cnvs._image_id = config.cnvs.create_image(canvasOffsetX, canvasOffsetY, image=tempImage, anchor='nw', tag="mainer")

	#config.cnvs.update()
	#config.cnvs.update_idletasks()


	root.after(100, startWork)
	root.call('wm', 'attributes', '.', '-topmost', '1')
	root.mainloop()

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def on_closing():
	global root
	return True

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def startWork(*args) :
	global config, work, root, counter

	### Putting the animation on its own thread
	### Still throws and error when manually closed though...

	try:
		t  = threading.Thread.__init__(work.runWork())
		t.start()
	except tk.TclError as details:
		print(details)
		pass
		exit()

	#work.runWork()
	


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def updateCanvas() :
	global canvasOffsetX, canvasOffsetY, root, counter, buff
	## For testing ...
	#draw1  = ImageDraw.Draw(config.renderImageFull)
	#draw1.rectangle((xOffset+32,yOffset,xOffset + 32 + 32, yOffset +32), fill=(255,100,0))
	counter +=1
	if(counter > 1000) :
		#print(gc.get_count())
		# I don't know if this really really helps
		gc.collect()
		counter = 0

	# This significantly helped performance !!
	config.cnvs.delete("main")
	config.cnvs._image_tk = PIL.ImageTk.PhotoImage(config.renderImageFull)
	config.cnvs._image_id = config.cnvs.create_image(canvasOffsetX, canvasOffsetY, image=config.cnvs._image_tk, anchor='nw', tag="main")
	config.cnvs.update()
	
	# This *should* be more efficient 
	#config.cnvs.update_idletasks()
	#root.update()

	############################################################
	######  Check if config file has changed and reload    #####
	############################################################

	if(config.checkForConfigChanges == True) :
		currentTime = time.time()
		f = os.path.getmtime(config.fileName )
		config.delta = ((currentTime - f ))

		if(config.delta <= 1) : 
			if(config.reloadConfig == False) :
				print ("LAST MODIFIED DELTA: ", config.delta)
				config.doingReload = True
				config.loadFromArguments(True)
			config.reloadConfig = True
		else :
			config.reloadConfig = False


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def render( imageToRender,xOffset,yOffset,w=128,h=64,nocrop=False, overlayBottom=False, updateCanvasCall=True) :
	global memoryUsage
	global config, debug

	# Render to canvas
	# This needs to be optomized !!!!!!

	if(config.rotation != 0) : 
		if(config.fullRotation == True) :
			# This rotates the image that is painted i.e. after pasting-in the image sent
			config.renderImageFull = config.renderImageFull.rotate(-config.rotation, expand=False)
		else :
			# This rotates the image sent to be rendered
			imageToRender = imageToRender.rotate(-config.rotation, expand=True )
			#imageToRender = ImageChops.offset(imageToRender, -40, 40) 

	try :
		config.renderImageFull.paste(imageToRender, (xOffset, yOffset), imageToRender)

	except  :
		config.renderImageFull.paste(imageToRender, (xOffset, yOffset))

	#config.drawBeforeConversion()

	config.renderImageFull = config.renderImageFull.convert("RGB")
	config.renderDraw = ImageDraw.Draw(config.renderImageFull)

	#config.renderImageFull = ImageChops.offset(config.renderImageFull, 40, 40) 

	# For planes, only this works - has to do with transparency of repeated pasting of
	# PNG's I think
	#newimage = Image.new('RGBA', config.renderImageFull.size)
	#newimage.paste(config.renderImageFull, (0, 0))
	#config.renderImageFull =  newimage.convert("RGB")
	
	#enhancer = ImageEnhance.Brightness(config.renderImageFull)
	#config.renderImageFull = enhancer.enhance(.75)


	if config.useFilters == True :
		config.renderImageFull = ditherFilter(config.renderImageFull,xOffset, yOffset, config)

	if config.usePixelSort == True and config.pixelSortRotatesWithImage == True :
		if(random.random()< config.pixelSortAppearanceProb) :
			config.renderImageFull =  pixelSort(config.renderImageFull, config)

	if config.rotation != 0  : 
		if(config.rotationTrailing or config.fullRotation) : 
			# This rotates the image that is painted back to where it was
			# basically same thing as rotating the image to be pasted in
			# except in some cases, more trailing is created
			config.renderImageFull = config.renderImageFull.rotate(config.rotation)

	if config.usePixelSort and config.pixelSortRotatesWithImage == False  :
		if(random.random()< config.pixelSortAppearanceProb) :
			config.renderImageFull =  pixelSort(config.renderImageFull, config)

	if config.remapImageBlock == True :
		crop = config.renderImageFull.crop(config.remapImageBlockSection)
		crop = crop.convert("RGBA")
		'''
		config.renderDraw = ImageDraw.Draw(config.renderImageFull)
		config.renderDraw.rectangle((config.remapImageBlockDestination[0], config.remapImageBlockDestination[1],
			config.remapImageBlockSection[2], 
			config.remapImageBlockSection[3] ), fill=(0,0,0,216))
		'''

		if config.remapImageBlockRotation != 0 :
			crop = crop.rotate(config.remapImageBlockRotation)
			#crop = crop.transpose(Image.ROTATE_90)
		config.renderImageFull.paste(crop, config.remapImageBlockDestination, crop)

	if config.remapImageBlock2 == True :
		crop = config.renderImageFull.crop(config.remapImageBlockSection2)
		crop = crop.convert("RGBA")
		config.renderImageFull.paste(crop, config.remapImageBlockDestination2, crop)	

	if config.remapImageBlock3 == True :
		crop = config.renderImageFull.crop(config.remapImageBlockSection3)
		crop = crop.convert("RGBA")
		config.renderImageFull.paste(crop, config.remapImageBlockDestination3, crop)
		
	if config.useBlur == True :
		crop = config.renderImageFull.crop(config.blurSection)
		destination = (config.blurXOffset, config.blurYOffset)
		crop = crop.convert("RGBA")

		crop = crop.filter(ImageFilter.GaussianBlur(radius=config.sectionBlurRadius))
		config.renderImageFull.paste(crop, destination, crop)

	if(updateCanvasCall) : updateCanvas() 

	#mem = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)/1024/1024
	#if mem > memoryUsage and debug :
	#	memoryUsage = mem 
	#	print 'Memory usage: %s (mb)' % str(memoryUsage)


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Might be used at some point

def remappingFunctionTemp() :
	for i in range (0,4) :
		## Map the one below to the next set of 4
		pix = 16
		colWidth = 128
		row = i
		cropRow = i * 2 + 1

		remapImageBlockSection = (0, cropRow * pix, colWidth, cropRow * pix + pix)
		remapImageBlockDestination = (colWidth, row * 16)
		crop = config.renderImageFull.crop(remapImageBlockSection)
		crop = crop.convert("RGBA")
		config.renderImageFull.paste(crop, remapImageBlockDestination, crop)
		## Move a row "up"

		remapImageBlockSection = (0, (cropRow-1) * pix, colWidth, (cropRow-1) * pix + pix)
		remapImageBlockDestination = (0, (row) * pix)
		crop = config.renderImageFull.crop(remapImageBlockSection)
		crop = crop.convert("RGBA")
		config.renderImageFull.paste(crop, remapImageBlockDestination, crop)


def drawBeforeConversion() :
	return True

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''



