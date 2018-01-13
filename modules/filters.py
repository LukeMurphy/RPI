## Filters
import PIL.Image
import PIL.ImageTk
from PIL import Image, ImageTk, ImageDraw, ImageFont
from PIL import ImageFilter, ImageChops, ImageEnhance
import random
import numpy, time
import gc, os

lev = 0
levdiff  = 1
unsharpMaskPercent = 100

def ditherFilter(renderImageFull,xOffset, yOffset, unsharpMaskPercent = 50, blurRadius = 0):
	#return orderedDither(renderImageFull,xOffset, yOffset)
	return dither(renderImageFull,xOffset, yOffset, unsharpMaskPercent, blurRadius)


def dither(renderImageFull,xOffset, yOffset, unsharpMaskPercent = 50, blurRadius = 0):
	global lev, levdiff
	lev += levdiff

	if(lev >= 120) : 
		levdiff = -1
	if(lev <= 20) : 
		levdiff = 1

	im1 = renderImageFull.filter(ImageFilter.GaussianBlur(radius=blurRadius))
	im2 = im1.filter(ImageFilter.UnsharpMask(radius=lev, percent=unsharpMaskPercent,threshold=2))

	'''#######################    Paste to Render       #######################'''

	renderImageFull.paste(im2, (xOffset, yOffset))
	nc = int(random.uniform(2,255))

	#newimage = renderImageFull.convert("P", palette=Image.WEB, colors = nc)
	newimage = renderImageFull.convert("P", dither=Image.FLOYDSTEINBERG, colors = nc)
	renderImageFull =  newimage.convert("RGB")

	return renderImageFull


def orderedDither(renderImageFull,xOffset, yOffset):
	# Produces an ordered dithering - SLOW!!!

	im = renderImageFull.convert('CMYK').split()

	for ch in im:
		ordered_dithering(ch.load(), ch.size, gen_matrix(1)[0])
	im = Image.merge("CMYK",im).convert("RGB")
	return im

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