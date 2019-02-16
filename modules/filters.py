## Filters
import PIL.Image
from PIL import Image, ImageDraw, ImageFont
from PIL import ImageFilter, ImageChops, ImageEnhance
import random
import numpy, time
import gc, os

from modules import colorutils

lev = 0
levdiff  = 1
unsharpMaskPercent = 100


def ditherFilter(renderImageFull,xOffset, yOffset, config):
	#return orderedDither(renderImageFull,xOffset, yOffset)
	#return dither(renderImageFull,xOffset, yOffset, unsharpMaskPercent, blurRadius)
	return ditherGlitch(renderImageFull,xOffset, yOffset, config)


def dither(renderImageFull,xOffset, yOffset, config):
	global lev, levdiff
	lev += levdiff

	if(lev >= 120) : 
		levdiff = -1
	if(lev <= 20) : 
		levdiff = 1

	im1 = renderImageFull.filter(ImageFilter.GaussianBlur(radius=config.blurRadius))
	im2 = im1.filter(ImageFilter.UnsharpMask(radius=lev, percent=unsharpMaskPercent,threshold=2))

	'''#######################    Paste to Render       #######################'''

	renderImageFull.paste(im2, (xOffset, yOffset))
	nc = int(random.uniform(2,255))

	#newimage = renderImageFull.convert("P", palette=Image.WEB, colors = nc)
	newimage = renderImageFull.convert("P", dither=Image.FLOYDSTEINBERG, colors = nc)
	renderImageFull =  newimage.convert("RGB")

	return renderImageFull

def ditherGlitch(renderImageFull,xOffset, yOffset, config):
	global lev, levdiff
	lev += levdiff

	if(lev >= 120) : 
		levdiff = -1
	if(lev <= 20) : 
		levdiff = 1

	im1 = renderImageFull.filter(ImageFilter.GaussianBlur(radius=config.blurRadius))
	im2 = im1.filter(ImageFilter.UnsharpMask(radius=lev, percent=config.unsharpMaskPercent,threshold=2))

	'''#######################    Paste to Render       #######################'''

	renderImageFull.paste(im2, (xOffset, yOffset))
	nc = int(random.uniform(2,255))


	#newimage = renderImageFull.convert("P", palette=Image.WEB, colors = nc)
	newimage = renderImageFull.convert("P", dither=Image.FLOYDSTEINBERG, colors = nc)

	renderImageFull =  newimage.convert("RGB")
	return renderImageFull

def pixelSort(imageToModify, config):
	
	pixSortXOffset = config.pixSortXOffset
	pixSortYOffset = config.pixSortYOffset

	pixSortboxHeight = config.pixSortboxHeight
	pixSortboxWidth = config.pixSortboxWidth

	pixSortgap = config.pixSortgap
	pixSortprobDraw = config.pixSortprobDraw
	pixSortprobGetNextColor = config.pixSortprobGetNextColor
	pixSortSampleVariance = config.pixSortSampleVariance
	pixSortDrawVariance = config.pixSortDrawVariance
	pixSortProbDecriment = config.pixSortProbDecriment
	pixSortSizeDecriment = config.pixSortSizeDecriment
	pixSortDirection = config.pixSortDirection
	randomColorProbabilty = config.randomColorProbabilty
	brightnessVarLow = config.brightnessVarLow
	brightnessVarHi = config.brightnessVarHi



	tempDraw = ImageDraw.Draw(imageToModify)

	pixSortxStart = 0
	pixSortyStart = 0

	# For now draw 4 layers 
	for col in range(0,4):
		if (col > 0) : 
			if pixSortDirection == "lateral":
				pixSortxStart += pixSortboxWidth
				pixSortboxWidth *= pixSortSizeDecriment
			else :
				pixSortyStart += pixSortboxHeight
				pixSortboxHeight *= pixSortSizeDecriment

			pixSortprobDraw *= pixSortProbDecriment


		# Each layer is made up of 4 blocks separated by a variable gap
		for b in range(0,4):
			if pixSortDirection == "lateral":
				pixSortyStart = b * pixSortboxHeight 
				if (b > 0) : pixSortyStart += pixSortgap * b * random.random()
			else:
				pixSortxStart = b * pixSortboxWidth 
				if (b > 0) : pixSortxStart += pixSortgap * b * random.random()

			varx = int(random.uniform(-pixSortDrawVariance,pixSortDrawVariance))

			# In each block, sample the color at the end of the block and either
			# draw a line in that color from the start to the end, or a variable difference to the end
			# or repeat the same color. If the probability to sample is low (pixSortprobGetNextColor)
			# then there is a tendancy to draw solid blocks of color repeatedly. This is closer to the 
			# condition when a single LED panel is totally whacked vs a line of LEDS is whacked ;)

			colorSampleColor = (10,10,10) #colorutils.getRandomRGB(random.random())
			colorSampleColorAlpha = (10,10,10,10) #colorutils.getRandomRGB(random.random())
			if pixSortDirection == "lateral":
				## i.e. draw horizontal lines
				boxRange = int(pixSortboxHeight)
			else:
				## i.e. draw vertical lines
				boxRange = int(pixSortboxWidth)


			for i in range(boxRange) :

				var = int(random.uniform(0,pixSortSampleVariance))

				if(random.random() < pixSortprobGetNextColor or i == 0) : 
					# take a sample point color
					if pixSortDirection == "lateral":
						### Sample UP
						#samplePoint = (pixSortboxWidth + var + pixSortxStart, i + pixSortyStart)
						### Smaple DOWN
						samplePoint = (var + pixSortxStart + pixSortXOffset, i + pixSortyStart + pixSortYOffset)
					else:
						#samplePoint = (pixSortxStart + i, pixSortboxHeight + var + pixSortyStart)
						samplePoint = (pixSortxStart + i + pixSortXOffset,  var + pixSortyStart + pixSortYOffset)

					#print(samplePoint,imageToModify.size[0],imageToModify.size[1])

					# Just make sure the sample point is actually within the bounds of the image
					if(samplePoint[0] < imageToModify.size[0] and samplePoint[1] < imageToModify.size[1]):
						colorSample = imageToModify.getpixel(samplePoint)

						#randomize brightness a little
						colorSampleColor = tuple(int(round(c * random.uniform(brightnessVarLow,brightnessVarHi))) for c in colorSample)

				# Once in a little while, the color is just random
				if(random.random() < randomColorProbabilty) : colorSampleColor = colorutils.getRandomRGB(random.random())

				colorSampleColorAlpha = tuple(int(c) for c in colorSampleColor) 

				#colorSampleColorAlpha = (100,0,0,0)

				#print(colorSampleColorAlpha)
				# Variable probability that the line will even draw. Lower probability means more
				# glitchy lines
				if(random.random() < pixSortprobDraw and colorSampleColor != (0,0,0)) :
					if pixSortDirection == "lateral":
						tempDraw.line((
							pixSortxStart + pixSortXOffset- varx, 							i + pixSortyStart + pixSortYOffset, 
							pixSortboxWidth - varx + pixSortxStart +  pixSortXOffset, 	i + pixSortyStart + pixSortYOffset) , 
							fill = colorSampleColorAlpha)
					else :
						tempDraw.line((
							i + pixSortxStart + pixSortXOffset, 		pixSortyStart + pixSortYOffset - varx, 
							i + pixSortxStart + pixSortXOffset, 		pixSortyStart - varx + pixSortboxHeight + pixSortYOffset), 
							fill = colorSampleColorAlpha)

	return imageToModify


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