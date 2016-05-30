from Tkinter import *
import tkMessageBox
import PIL.Image
import PIL.ImageTk
from PIL import Image, ImageTk, ImageDraw, ImageFont
from PIL import ImageFilter
import random
import numpy, time

global root
memoryUsage = 0
debug = False

canvasOffsetX = 3
canvasOffsetY = 3

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
	if(config.rotation == 90) : canvasOffsetY = -25

	root = Tk()
	w = config.screenWidth + 8
	h = config.screenHeight  + 8
	x = windowOffset[0]
	y = windowOffset[1]

	root.overrideredirect(False)
	root.geometry('%dx%d+%d+%d' % (w, h, x, y))
	#root.protocol("WM_DELETE_WINDOW", on_closing)

	#Button(root, text="Quit", command=root.quit).pack(side="bottom")
	root.lift()

	cnvs = Canvas(root, width=config.screenWidth + 4, height=config.screenHeight + 4)
	config.cnvs = cnvs
	config.cnvs.pack()
	config.cnvs.create_rectangle(0, 0, config.screenWidth + 8, config.screenHeight + 8, fill="black")
	
	tempImage = PIL.ImageTk.PhotoImage(config.renderImageFull)
	config.cnvs._image_id = config.cnvs.create_image(canvasOffsetX, canvasOffsetY, image=tempImage, anchor='nw')

	#config.cnvs.update()
	config.cnvs.update_idletasks()

	root.after(0, startWork)
	root.call('wm', 'attributes', '.', '-topmost', '1')
	root.mainloop()

def on_closing():
	global root


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

def updateCanvas() :
	global canvasOffsetX, canvasOffsetY
	## For testing ...
	#draw1  = ImageDraw.Draw(config.renderImageFull)
	#draw1.rectangle((xOffset+32,yOffset,xOffset + 32 + 32, yOffset +32), fill=(255,100,0))
	config.cnvs._image_tk = ImageTk.PhotoImage(config.renderImageFull)
	config.cnvs._image_id = config.cnvs.create_image(canvasOffsetX, canvasOffsetY, image=config.cnvs._image_tk, anchor='nw')
	config.cnvs.update()

def render( imageToRender,xOffset,yOffset,w=128,h=64,nocrop=False, overlayBottom=False, updateCanvasCall=True) :
	global memoryUsage
	global config, debug

	# Render to canvas
	# This needs to be optomized !!!!!!
	#*******************************************************************************

	if(config.rotation != 0) : 
		config.renderImageFull = config.renderImageFull.rotate(-config.rotation)
		#config.renderImageFull = ImageChops.offset(config.renderImageFull, -10, 0) 

	'''
	if(config.useFilters) :
		#------------------------------------------------------------------------
		#              FILTERS                                                   
		# ugly hippy 
		#config.image = config.image.filter(ImageFilter.GaussianBlur(radius=1))
		#config.image = config.image.filter(ImageFilter.UnsharpMask(radius=20, percent=150,threshold=2))
		#config.renderImageFull.paste(config.image, (xOffset, yOffset))
		#
		#im1 = config.image.filter(ImageFilter.GaussianBlur(radius=0))
		#im2 = im1.filter(ImageFilter.UnsharpMask(radius=20, percent=100,threshold=2))
		#         Paste to Render                                       
		config.renderImageFull.paste(im2, (xOffset, yOffset))

	else :
		#if(updateCanvasCall) : config.renderDraw.rectangle((0, 0, config.screenWidth + 8, config.screenHeight + 8), fill=(0,0,0))
		config.renderImageFull.paste(imageToRender, (xOffset, yOffset), imageToRender)
	'''
	

	'''#******** NOTES ***************'''

	try :
		config.renderImageFull.paste(imageToRender, (xOffset, yOffset), imageToRender)
		config.renderImageFull = config.renderImageFull.convert("RGB")
		config.renderDraw = ImageDraw.Draw(config.renderImageFull)
	except  :
		config.renderImageFull.paste(imageToRender, (xOffset, yOffset))
		config.renderImageFull = config.renderImageFull.convert("RGB")
		config.renderDraw = ImageDraw.Draw(config.renderImageFull)

	''' 
	# For planes, only this works - has to do with transparency of repeated pasting of
	# PNG's I think
	'''
	
	#newimage = Image.new('RGBA', config.renderImageFull.size)
	#newimage.paste(config.renderImageFull, (0, 0))
	#config.renderImageFull =  newimage.convert("RGB")
	
	''' -------------------------------'''

	
	if(config.useFilters) :
		
		newimage = Image.new('P', config.renderImageFull.size)
		newimage = config.renderImageFull.convert("P", colors = 64)
		config.renderImageFull =  newimage.convert("RGB")


		'''
		# Random bright pixel patches -- of limited value aesthetically
		d = -50
		for t in range(100) :
			xp = int(random.uniform(1,config.screenWidth-4))
			yp = int(random.uniform(1,config.screenHeight-4))
			vr,vg,vb = config.renderImageFull.getpixel((xp,yp))
			if(vr == 0 and vg ==0 and vb == 0) :
				pass
			else :
				config.renderImageFull.putpixel((xp,yp),(vr-d,vg-d,vb-d))
				config.renderImageFull.putpixel((xp+1,yp),(vr-d,vg-d,vb-d))
				config.renderImageFull.putpixel((xp+1,yp+1),(vr-d,vg-d,vb-d))
				config.renderImageFull.putpixel((xp,yp+1),(vr-d,vg-d,vb-d))
		'''

		'''
		arr = numpy.array(config.renderImageFull)
		config.renderImageFull = Image.fromarray(arr)
		'''

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
		config.renderImageFull = config.renderImageFull.rotate(config.rotation)
		

	if(updateCanvasCall) : updateCanvas() 

	#mem = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)/1024/1024
	#if mem > memoryUsage and debug :
	#	memoryUsage = mem 
	#	print 'Memory usage: %s (mb)' % str(memoryUsage)


	#*******************************************************************************

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

	#*******************************************************************************
	#*******************************************************************************