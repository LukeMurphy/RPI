import moviepy.editor as mpy
import moviepy.video.VideoClip as mpv
from moviepy.video import *
from PIL import Image, ImageTk, ImageDraw, ImageFont
from PIL import ImageFilter
import time, datetime

def setUp(mode) :
	global config
	iterateWork(mode)

# Just drop any rendering call as this module pulls the full image 
# and sends to FFMEG or MoviePy etc
def render(*args):
	pass

def updateCanvas(*args) :
	pass

def iterateWork(mode):
	if(mode  == "avi"):
		'''*************  PROBLEMS *****************'''
		clip = mpy.VideoClip(clipMaker, duration=duration)
		#clip.size = (config.screenWidth, config.screenHeight)
		clip.write_videofile("test.avi", fps=fps, audio=None, codec="rawvideo")

	elif(mode == "video"):
		#clip = mpy.VideoClip(clipMaker, duration=duration)
		#clip.write_videofile("test.mp4", fps=fps, audio=None, codec="mpeg4")
		toVideo()

	elif(mode == "gif"):
		#** Make Gifs
		clip = mpy.VideoClip(clipMaker, duration=duration)
		clip.write_gif("test.gif", fps=fps)

def clipMaker(t) :
	global config
	(imageToRender,xOffset,yOffset) = config.workRef.interate()
	config.renderImageFull.paste(imageToRender, (xOffset, yOffset))
	img = config.renderImageFull

	#nArray = outputArray.reshape(img.size[1], img.size[0], 3)
	#outputArray = numpy.array(numpy.rollaxis(outputArray,0,3))

	outputArray = numpy.array(img)
	return outputArray

def videoClipMaker() :
	global config, work
	#(imageToRender,xOffset,yOffset) = config.workRef.interate()
	work.iterate()

	imageToRender = config.image
	xOffset = work.x
	yOffset = work.y	

	# xOffset+config.workRef.wd, yOffset+config.workRef.ht
	if(config.useFilters) :
		'''------------------------------------------------------------------------'''
		'''#######################    FILTERS               #######################'''

		im1 = config.image.filter(ImageFilter.GaussianBlur(radius=0))
		im2 = im1.filter(ImageFilter.UnsharpMask(radius=20, percent=100,threshold=2))

		'''#######################    Paste to Render       #######################'''

		config.renderImageFull.paste(im2, (xOffset, yOffset))
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


	else :
		config.renderImageFull.paste(imageToRender, (xOffset, yOffset))
	
	#img = config.renderImageFull.resize((640,480))
	img = config.renderImageFull
	#img = img.filter(ImageFilter.UnsharpMask(radius=10, percent=200,threshold=0))
	return img

def toVideo() :
	global config, duration, fps
	from subprocess import Popen, PIPE

	#config.workRef.iterate()

	#vcodecImg = "mjpeg"
	vcodecImg = "png"
	#vcodec = "rawvideo"
	#vcodec = "mpeg4"
	vcodec = "h264"
	#vcodec = "libxvid"
	#vcodec = "prores"
	# -c:v prores -profile:v 3
	## Sends image data as PNG to FFMPEG
	imgFormat = "PNG"

	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d--%H-%M-%S')
	name = config.WRKINID + "_" + st + "_video.avi"

	'''
	p = Popen(['ffmpeg', '-y', '-f', 'image2pipe', '-vcodec', vcodecImg, '-r', str(fps) , '-i', '-', 
		'-vcodec', vcodec, '-qscale', str(duration) , '-r', str(fps) , name], stdin=PIPE)
	'''

	p = Popen(['ffmpeg', '-y', '-f', 'image2pipe', '-vcodec', vcodecImg, '-r', str(fps) , '-i', '-', 
		'-vcodec', vcodec, '-qscale', str(duration) , '-r', str(fps) , name], stdin=PIPE)

	for i in range(fps * duration):
	    #im = Image.new("RGB", (640, 480), (i, 1, 1))
	    im  = videoClipMaker()
	    im.save(p.stdin, imgFormat)
	p.stdin.close()
	p.wait()

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
