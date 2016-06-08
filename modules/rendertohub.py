from Tkinter import *
import tkMessageBox
import PIL.Image
import PIL.ImageTk
from PIL import Image, ImageTk, ImageDraw, ImageFont
from PIL import ImageFilter, ImageChops
import random
import numpy, time

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

global root
memoryUsage = 0
debug = False

canvasOffsetX = 4
canvasOffsetY = 7

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def setUp():
	global root, canvasOffsetX, canvasOffsetY
	if(config.MID == "studio-mac") : 
		config.path = "./"
		windowOffset = [1900,20]
		#windowOffset = [4,45]
	else :
		windowOffset = [-1,13]

	# -----> this is somewhat arbitrary - just to get the things aligned
	# after rotation
	#if(config.rotation == 90) : canvasOffsetY = -25

	buff  =  8

	root = Tk()
	w = config.screenWidth + buff
	h = config.screenHeight  + buff
	x = windowOffset[0]
	y = windowOffset[1]

	root.overrideredirect(False)
	root.geometry('%dx%d+%d+%d' % (w, h, x, y))
	#root.protocol("WM_DELETE_WINDOW", on_closing)

	#Button(root, text="Quit", command=root.quit).pack(side="bottom")
	root.lift()

	cnvs = Canvas(root, width=config.screenWidth + buff, height=config.screenHeight + buff)
	config.cnvs = cnvs
	config.cnvs.pack()
	config.cnvs.create_rectangle(0, 0, config.screenWidth + buff, config.screenHeight + buff, fill="black")
	
	tempImage = PIL.ImageTk.PhotoImage(config.renderImageFull)
	config.cnvs._image_id = config.cnvs.create_image(canvasOffsetX, canvasOffsetY, image=tempImage, anchor='nw')

	#config.cnvs.update()
	config.cnvs.update_idletasks()

	root.after(0, startWork)
	root.call('wm', 'attributes', '.', '-topmost', '1')
	root.mainloop()

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def on_closing():
	global root
	return True

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def startWork(*args) :
	global config, work, root
	while True :
		try :
			work.runWork()
		except Exception,e :
			print(str(e))
			#work.runWork(False)
			root.quit()
			sys.exit()
			root.destroy()

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def updateCanvas() :
	global canvasOffsetX, canvasOffsetY
	## For testing ...
	#draw1  = ImageDraw.Draw(config.renderImageFull)
	#draw1.rectangle((xOffset+32,yOffset,xOffset + 32 + 32, yOffset +32), fill=(255,100,0))
	config.cnvs._image_tk = ImageTk.PhotoImage(config.renderImageFull)
	config.cnvs._image_id = config.cnvs.create_image(canvasOffsetX, canvasOffsetY, image=config.cnvs._image_tk, anchor='nw')
	config.cnvs.update()

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def render( imageToRender,xOffset,yOffset,w=128,h=64,nocrop=False, overlayBottom=False, updateCanvasCall=True) :
	global memoryUsage
	global config, debug

	# Render to canvas
	# This needs to be optomized !!!!!!

	if(config.rotation != 0) : 
		if(config.fullRotation == False) :
			# This rotates the image sent to be rendered
			imageToRender = imageToRender.rotate(-config.rotation)
			#imageToRender = ImageChops.offset(imageToRender, -40, 40) 
		else :
			# This rotates the image that is painted i.e. after pasting-in the image sent
			config.renderImageFull = config.renderImageFull.rotate(-config.rotation)

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
	
	if(config.useFilters) :
		
		newimage = Image.new('P', config.renderImageFull.size)
		newimage = config.renderImageFull.convert("P", colors = 64)
		config.renderImageFull =  newimage.convert("RGB")

		'''
		# Produces an ordered dithering - looks good for movement but not so good
		# on still images 
		im = config.renderImageFull.convert('CMYK').split()

		for ch in im:
			ordered_dithering(ch.load(), ch.size, gen_matrix(1)[0])
		im = Image.merge("CMYK",im).convert("RGB")
		config.renderImageFull = im
		'''

	if(config.rotation != 0) : 
		if(config.rotationTrailing or config.fullRotation) : 
			# This rotates the image that is painted back to where it was
			# basically same thing as rotating the image to be pasted in
			# except in some cases, more trailing is created
			config.renderImageFull = config.renderImageFull.rotate(config.rotation)
		
	if(updateCanvasCall) : updateCanvas() 

	#mem = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)/1024/1024
	#if mem > memoryUsage and debug :
	#	memoryUsage = mem 
	#	print 'Memory usage: %s (mb)' % str(memoryUsage)


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def drawBeforeConversion() :
	return True

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def gen_matrix( e ):
	''' Generating new matrix.
	@param e The width and height of the matrix is 2^e.
	@return New 2x2 to 2^e x 2^e matrix list.
	'''
	if e < 1: return None
	m_list = [ [[1,2],[3,0]] ]
	_b = m_list[0]
	for n in xrange(1, e):
		m = m_list[ n - 1 ]
		m_list.append( [
		[4*i+_b[0][0] for i in m[0]] + [4*i+_b[0][1] for i in m[0]],
		[4*i+_b[0][0] for i in m[1]] + [4*i+_b[0][1] for i in m[1]],
		[4*i+_b[1][0] for i in m[0]] + [4*i+_b[1][1] for i in m[0]],
		[4*i+_b[1][0] for i in m[1]] + [4*i+_b[1][1] for i in m[1]],
		] )
	return m_list

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def ordered_dithering( pixel, size, matrix ):
	""" Dithering on a single channel.
	  @param pixel PIL PixelAccess object.
	  @param size A tuple to represent the size of pixel.
	  @param matrix Must be NxN, and N == 2^e where e>=1
	"""
	X, Y = size
	N = len(matrix)

	T = [[255*(matrix[x][y]+0.01)/N/N for x in xrange(N)] for y in xrange(N)]

	#print(T)

	for y in xrange(0, Y):
		for x in xrange(0, X):
			pixel[x,y] = 255 if pixel[x,y] > T[x%N][y%N] else 0


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

