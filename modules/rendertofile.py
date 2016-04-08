import moviepy.editor as mpy
import moviepy.video.VideoClip as mpv
from moviepy.video import *
from PIL import Image, ImageTk, ImageDraw, ImageFont
from PIL import ImageFilter

def setUp(mode) :
	global config
	iterateWork(mode)

# Just drop any rendering call as this module pulls the full image 
# and sends to FFMEG or MoviePy etc
def render(*args):
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

	## Sends image data as PNG to FFMPEG
	imgFormat = "PNG"

	p = Popen(['ffmpeg', '-y', '-f', 'image2pipe', '-vcodec', vcodecImg, '-r', str(fps) , '-i', '-', 
		'-vcodec', vcodec, '-qscale', str(duration) , '-r', str(fps) , 'video.avi'], stdin=PIPE)
	for i in range(fps * duration):
	    #im = Image.new("RGB", (640, 480), (i, 1, 1))
	    im  = videoClipMaker()
	    im.save(p.stdin, imgFormat)
	p.stdin.close()
	p.wait()


